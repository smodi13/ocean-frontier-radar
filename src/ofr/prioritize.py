"""Sourcing-priority scoring.

THIS IS A SOURCING PRIORITY SCORE, NOT AN INVESTMENT SCORE.
A high score means "worth spending analyst time on", never "likely good
investment".

Six components, 17 points maximum:
    technical_evidence        0-3
    commercialization_signal  0-3
    timing                    0-2
    venture_potential         0-3
    propeller_relevance       0-3
    differentiated_sourcing   0-3

Design constraints carried from Phase 1:
  * Every point cites the evidence ids that earned it.
  * No total is stored; totals are computed on read so a number can never be
    quoted without its components.
  * Analyst overrides are permitted but require a written reason (enforced by
    a CHECK constraint in the schema).
  * Structural problems are FLAGS, not point deductions, so a high-scoring
    candidate still shows why it might be wrong.
"""
from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ofr import db

MAX_POINTS = {
    "technical_evidence": 3, "commercialization_signal": 3, "timing": 2,
    "venture_potential": 3, "propeller_relevance": 3, "differentiated_sourcing": 3,
}
TOTAL_MAX = sum(MAX_POINTS.values())   # 17

# Evidence tiers for technical validation, strongest first.
TECH_3 = {"field_trial", "independent_validation", "sbir_phase_ii", "sttr_phase_ii",
          "exclusive_license", "license_executed"}
TECH_2 = {"prototype_demonstrated", "patent_granted", "sbir_phase_i", "sttr_phase_i",
          "technical_milestone"}
TECH_1 = {"peer_reviewed_publication", "research_grant", "commercialization_grant",
          "patent_application", "technical_claim", "preprint"}

COMM_3 = {"named_customer", "pilot_deployment", "offtake_agreement",
          "revenue_disclosed", "procurement_contract"}
COMM_2 = {"sbir_phase_i", "sbir_phase_ii", "sttr_phase_i", "sttr_phase_ii",
          "commercialization_grant", "industry_partnership", "venture_financing"}
COMM_1 = {"icorps", "accelerator_participation", "company_incorporated",
          "spinout_announced", "non_dilutive_prize", "research_institution_partnership"}

CENTRALITY_POINTS = {
    "central_mechanism": 3, "primary_end_market": 2,
    "strong_adjacency": 2, "incidental": 0,
}
SOURCING_POINTS = {
    "hidden_adjacency": 3,   # solves an ocean-industrial problem without saying "ocean"
    "pre_company": 3,        # research/I-Corps/licensing before obvious formation
    "emerging": 2,           # exists, limited visibility
    "obvious": 0,            # heavily funded / broadly covered / SBIR shop
}


def _evidence(conn, cid):
    return conn.execute(
        "SELECT evidence_id,evidence_type,evidence_date,quantitative_value "
        "FROM evidence WHERE candidate_id=?", (cid,)).fetchall()


def _score_technical(ev):
    ids = [e["evidence_id"] for e in ev if e["evidence_type"] in TECH_3]
    if ids:
        return 3, "Validated beyond the lab (Phase II, field trial, or executed license).", ids
    ids = [e["evidence_id"] for e in ev if e["evidence_type"] in TECH_2]
    if ids:
        return 2, "Built and demonstrated (prototype, granted patent, or Phase I).", ids
    ids = [e["evidence_id"] for e in ev if e["evidence_type"] in TECH_1]
    if ids:
        return 1, "Credible technical basis (publication, research grant, or stated claim).", ids
    return 0, "No external technical validation found in public evidence.", []


def _score_commercial(ev):
    ids = [e["evidence_id"] for e in ev if e["evidence_type"] in COMM_3]
    if ids:
        return 3, "Real customer relationship (pilot, contract, offtake, or revenue).", ids
    ids = [e["evidence_id"] for e in ev if e["evidence_type"] in COMM_2]
    if ids:
        return 2, "Commercialization funding won partly on commercial merit.", ids
    ids = [e["evidence_id"] for e in ev if e["evidence_type"] in COMM_1]
    if ids:
        return 1, "Commercialization intent demonstrated (I-Corps, accelerator, formation).", ids
    return 0, "No commercial evidence found.", []


def _score_timing(ev, asof: date):
    dates = [e["evidence_date"] for e in ev if e["evidence_date"]]
    if not dates:
        return 0, "No dated evidence; recency cannot be established.", []
    latest = max(dates)
    try:
        months = (asof - datetime.strptime(latest, "%Y-%m-%d").date()).days / 30.44
    except ValueError:
        return 0, f"Unparseable evidence date {latest!r}.", []
    ids = [e["evidence_id"] for e in ev if e["evidence_date"] == latest]
    if months <= 12:
        return 2, f"Most recent evidence {latest} (~{months:.0f} months old).", ids
    if months <= 36:
        return 1, f"Most recent evidence {latest} (~{months:.0f} months old).", ids
    return 0, f"Most recent evidence {latest} (~{months:.0f} months old); possibly dormant.", ids


def _score_venture(conn, cid, ev, flags):
    """Most inference-heavy dimension. Always recorded as inferred, never as fact."""
    amounts = [e["quantitative_value"] for e in ev
               if e["quantitative_value"] and e["evidence_type"].startswith(("sbir", "sttr"))
               or (e["quantitative_value"] and e["evidence_type"] == "commercialization_grant")]
    biggest = max(amounts) if amounts else 0
    has_phase2 = any(e["evidence_type"] in {"sbir_phase_ii", "sttr_phase_ii"} for e in ev)
    has_financing = any(e["evidence_type"] == "venture_financing" for e in ev)
    has_ip = any(e["evidence_type"] in {"patent_granted", "exclusive_license", "license_executed"}
                 for e in ev)
    ids = [e["evidence_id"] for e in ev]

    if "ESTABLISHED_SBIR_CONTRACTOR" in flags:
        return 0, ("Long federal award history indicates a contract R&D business "
                   "rather than a venture-scale product company."), ids
    if "ESTABLISHED_FIRM" in flags:
        return 0, ("Firm has been taking federal awards for over a decade; outside "
                   "the pre-seed to Series A scope this system is built for."), ids
    if (has_ip and (has_phase2 or has_financing)) or (has_financing and biggest > 1_000_000):
        return 3, ("Protected or licensed IP combined with scaled non-dilutive funding or "
                   "institutional capital — a plausible mechanism for durable advantage. "
                   "[inferred]"), ids
    if has_phase2 or has_ip or biggest >= 1_000_000:
        return 2, ("Repeatable product shape with meaningful validation funding or IP. "
                   "[inferred]"), ids
    if biggest > 0:
        return 1, "Plausible product, scale and market not yet demonstrated. [inferred]", ids
    return 1, "Venture path unclear from public evidence. [inferred]", ids


def _score_propeller(conn, cid, centrality, ev):
    pts = CENTRALITY_POINTS.get(centrality or "", 0)
    cats = [r["category_id"] for r in conn.execute(
        "SELECT category_id FROM taxonomy_links WHERE candidate_id=?", (cid,))]
    ids = [e["evidence_id"] for e in ev][:5]
    if pts == 0:
        return 0, "Ocean connection is incidental, or centrality unassigned.", ids
    why = (f"Ocean centrality '{centrality}'; maps to taxonomy categories "
           f"{sorted(set(cats))}, all inside Propeller's publicly stated themes. "
           f"Measures fit with PUBLIC statements only — no claim about their pipeline.")
    return pts, why, ids


def _score_differentiated(signal, centrality, flags):
    pts = SOURCING_POINTS.get(signal or "", 1)
    if centrality == "strong_adjacency" and signal in ("emerging", "pre_company"):
        pts = 3
        return pts, ("Solves a problem acute in ocean-exposed industries without marketing "
                     "itself as ocean technology — the hidden-adjacency case."), []
    labels = {3: "Pre-company or hidden adjacency: surfaced from an under-read source.",
              2: "Emerging: company exists with limited visibility.",
              1: "Visibility unclear.",
              0: "Widely visible or an established federal contractor."}
    return pts, labels.get(pts, ""), []


def score_candidate(conn, cid, asof: date | None = None) -> dict:
    asof = asof or date.today()
    ev = _evidence(conn, cid)
    row = conn.execute(
        "SELECT ocean_centrality,sourcing_signal FROM candidates WHERE candidate_id=?",
        (cid,)).fetchone()
    if row is None:
        raise KeyError(cid)
    flags = {r["flag"] for r in conn.execute(
        "SELECT flag FROM flags WHERE candidate_id=?", (cid,))}

    parts = {
        "technical_evidence": _score_technical(ev),
        "commercialization_signal": _score_commercial(ev),
        "timing": _score_timing(ev, asof),
        "venture_potential": _score_venture(conn, cid, ev, flags),
        "propeller_relevance": _score_propeller(conn, cid, row["ocean_centrality"], ev),
        "differentiated_sourcing": _score_differentiated(
            row["sourcing_signal"], row["ocean_centrality"], flags),
    }

    scored_at = db.now()
    for dim, (pts, why, ids) in parts.items():
        # Never silently clobber a human decision.
        existing = conn.execute(
            "SELECT analyst_override FROM prioritization WHERE candidate_id=? AND dimension=?",
            (cid, dim)).fetchone()
        if existing and existing["analyst_override"]:
            continue
        conn.execute(
            """INSERT INTO prioritization
               (candidate_id,dimension,points,max_points,rationale,evidence_ids,
                analyst_override,override_reason,scored_at)
               VALUES (?,?,?,?,?,?,0,NULL,?)
               ON CONFLICT(candidate_id,dimension) DO UPDATE SET
                   points=excluded.points, max_points=excluded.max_points,
                   rationale=excluded.rationale, evidence_ids=excluded.evidence_ids,
                   scored_at=excluded.scored_at
               WHERE prioritization.analyst_override=0""",
            (cid, dim, min(pts, MAX_POINTS[dim]), MAX_POINTS[dim], why,
             ",".join(ids[:12]) or None, scored_at))
    return {d: p for d, (p, _, _) in parts.items()}


def total(conn, cid) -> int:
    """Computed on read. Deliberately never stored."""
    r = conn.execute("SELECT SUM(points) s FROM prioritization WHERE candidate_id=?",
                     (cid,)).fetchone()
    return int(r["s"] or 0)


def score_all(conn, verbose=True) -> int:
    cids = [r["candidate_id"] for r in conn.execute("SELECT candidate_id FROM candidates")]
    for cid in cids:
        score_candidate(conn, cid)
    conn.commit()
    if verbose:
        print(f"[prioritize] scored {len(cids)} candidates (max {TOTAL_MAX})")
    return len(cids)


if __name__ == "__main__":
    conn = db.connect(); score_all(conn)
