"""Analyst review cards, with a reporting-completeness guarantee.

WHY THE GUARANTEE EXISTS
------------------------
Phase 2.5's freshness audit found that ARMADA's ~$2.0M Navy Phase II award was
ALREADY INGESTED in the Phase 2 database, and the Phase 2 report still failed
to mention it. That is not a data-completeness failure - the pipeline worked.
It is a REPORTING-completeness failure: material evidence existed and the
summary layer silently dropped it.

Data completeness asks:      was the evidence ingested?
Reporting completeness asks: did material evidence reach the review?

`material_evidence()` derives, from the data alone, which evidence a review of
a given candidate MUST account for:

    * most recent material evidence
    * largest material funding/award evidence
    * strongest technical-validation evidence
    * strongest commercialization evidence

`check_completeness()` then verifies a generated card accounts for each one
that exists. No candidate, company name or dollar amount is hard-coded.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ofr import db, prioritize
from ofr.prioritize import COMM_1, COMM_2, COMM_3, TECH_1, TECH_2, TECH_3

FUNDING_TYPES = {"sbir_phase_i", "sbir_phase_ii", "sttr_phase_i", "sttr_phase_ii",
                 "research_grant", "commercialization_grant", "venture_financing",
                 "procurement_contract", "non_dilutive_prize"}

# Ranked strongest-first, mirroring the prioritization tiers.
TECH_RANK = [TECH_3, TECH_2, TECH_1]
COMM_RANK = [COMM_3, COMM_2, COMM_1]


_AWARD_ID_RE = re.compile(
    r"(?:contract|usaspending_award_id|nsf_award_id)=([A-Za-z0-9\-_/]+)")


def award_key(row) -> str | None:
    """Normalised award identifier, or None.

    The same award reaches us from more than one source: the SBIR bulk file
    records the Navy EPADS contract as "N68335-23-C-0142" at its original
    $999,028, while USAspending records the same contract as "N6833523C0142"
    at its current $1,998,926. Summing both double-counts the award and would
    have reported ARMADA's federal total as ~$4.7M instead of ~$3.0M.
    Stripping punctuation makes the two forms comparable.
    """
    m = _AWARD_ID_RE.search(row["analyst_notes"] or "")
    if not m:
        return None
    key = re.sub(r"[^A-Za-z0-9]", "", m.group(1)).upper()
    return key or None


def dedupe_funding(rows) -> list:
    """One row per distinct award, keeping the largest (most current) value."""
    best: dict[str, object] = {}
    loose: list = []
    for r in rows:
        k = award_key(r)
        if not k:
            loose.append(r)
            continue
        cur = best.get(k)
        if cur is None or (r["quantitative_value"] or 0) > (cur["quantitative_value"] or 0):
            best[k] = r
    # Hand-curated evidence often carries no award identifier and can restate an
    # award we already hold from an API. Drop a loose row when a keyed row has
    # the same type and value, so curation cannot inflate a total.
    keyed_sigs = {(r["evidence_type"], r["quantitative_value"]) for r in best.values()}
    loose = [r for r in loose
             if (r["evidence_type"], r["quantitative_value"]) not in keyed_sigs]
    return list(best.values()) + loose


def _rows(conn, cid):
    return conn.execute(
        """SELECT e.*, s.url, s.title AS src_title, s.publisher, s.source_quality
           FROM evidence e JOIN sources s USING(source_id)
           WHERE e.candidate_id=?""", (cid,)).fetchall()


def _best_by_rank(rows, ranked_sets):
    for tier in ranked_sets:
        hits = [r for r in rows if r["evidence_type"] in tier]
        if hits:
            return max(hits, key=lambda r: (r["evidence_date"] or "", r["evidence_id"]))
    return None


def material_evidence(conn, cid) -> dict:
    """The evidence a review of this candidate must account for. Derived, not curated."""
    rows = _rows(conn, cid)
    if not rows:
        return {}
    dated = [r for r in rows if r["evidence_date"]]
    funded = dedupe_funding([r for r in rows
                             if r["evidence_type"] in FUNDING_TYPES
                             and (r["quantitative_value"] or 0) > 0])
    out = {}
    if dated:
        out["most_recent"] = max(dated, key=lambda r: r["evidence_date"])
    if funded:
        out["largest_funding"] = max(funded, key=lambda r: r["quantitative_value"])
    t = _best_by_rank(rows, TECH_RANK)
    if t:
        out["strongest_technical"] = t
    c = _best_by_rank(rows, COMM_RANK)
    if c:
        out["strongest_commercial"] = c
    return out


def _fmt(r) -> str:
    amt = f" (${r['quantitative_value']:,.0f})" if r["quantitative_value"] else ""
    date = r["evidence_date"] or "date not published"
    return f"[{date}] {r['evidence_type']}{amt}: {r['observed_claim']}"


def build_card(conn, cid) -> dict:
    cand = conn.execute("SELECT * FROM candidates WHERE candidate_id=?", (cid,)).fetchone()
    if cand is None:
        raise KeyError(cid)
    mat = material_evidence(conn, cid)
    rows = _rows(conn, cid)

    views = conn.execute(
        "SELECT view_type, statement, evidence_ids, author FROM analyst_views "
        "WHERE candidate_id=?", (cid,)).fetchall()
    by_type: dict[str, list[str]] = {}
    for v in views:
        by_type.setdefault(v["view_type"], []).append(v["statement"])

    flags = [dict(r) for r in conn.execute(
        "SELECT flag, rationale FROM flags WHERE candidate_id=?", (cid,))]
    cats = [r["category_id"] for r in conn.execute(
        "SELECT category_id FROM taxonomy_links WHERE candidate_id=?", (cid,))]
    people = [dict(r) for r in conn.execute(
        "SELECT name, role, role_type, affiliation FROM people WHERE candidate_id=?", (cid,))]
    comps = {r["dimension"]: {"points": r["points"], "max": r["max_points"],
                             "rationale": r["rationale"]}
             for r in conn.execute(
                 "SELECT * FROM prioritization WHERE candidate_id=?", (cid,))}

    federal_rows = dedupe_funding(
        [r for r in rows if r["evidence_type"] in FUNDING_TYPES and r["unit"] == "USD"])
    total_federal = sum((r["quantitative_value"] or 0) for r in federal_rows)

    card = {
        "candidate": cand["name"],
        "candidate_id": cid,
        "candidate_type": cand["candidate_type"],
        "queue": cand["queue"],
        "institution": cand["institution"],
        "geography": cand["geography"],
        "website": cand["website"],
        "people": people,
        "taxonomy": sorted(set(cats)),
        "ocean_centrality": cand["ocean_centrality"],
        "differentiated_sourcing_signal": cand["sourcing_signal"],
        "latest_meaningful_signal": cand["candidate_latest_signal_date"],
        "total_federal_award_value_usd": round(total_federal, 2),
        "evidence_count": len(rows),

        # --- the four material items the review must account for ----------
        "material_evidence": {k: _fmt(v) for k, v in mat.items()},
        "material_evidence_ids": {k: v["evidence_id"] for k, v in mat.items()},

        "why_it_surfaced": None,      # filled below
        "technical_evidence": [_fmt(r) for r in rows
                               if r["evidence_type"] in (TECH_3 | TECH_2 | TECH_1)],
        "commercialization_evidence": [_fmt(r) for r in rows
                                       if r["evidence_type"] in (COMM_3 | COMM_2 | COMM_1)],
        "funding_evidence": sorted(
            (_fmt(r) for r in dedupe_funding(
                [r for r in rows if r["evidence_type"] in FUNDING_TYPES])), reverse=True),
        "distinct_federal_awards": len(federal_rows),

        # --- epistemic separation, enforced by the schema ------------------
        "observed": by_type.get("observed", []),
        "inferred": by_type.get("inferred", []),
        "unknown": by_type.get("unknown", []),
        "what_must_be_true": by_type.get("what_must_be_true", []),
        "technical_kill_question": by_type.get("technical_kill_question", []),
        "commercial_kill_question": by_type.get("commercial_kill_question", []),

        "flags": flags,
        "priority_components_diagnostic": comps,
        "priority_total_diagnostic": prioritize.total(conn, cid),
        "priority_note": ("Diagnostic metadata only. Not an investment ranking. "
                          "Ordering within Tier A is analyst judgment."),
        "sources": sorted({r["url"] for r in rows if r["url"]}),
    }

    surfaced = []
    for r in rows:
        if r["publisher"]:
            surfaced.append(r["publisher"])
    card["why_it_surfaced"] = sorted(set(surfaced))[:6]
    return card


class ReportingCompletenessError(AssertionError):
    """Material evidence exists in the data but is absent from the review card."""


def check_completeness(conn, cid, card: dict) -> list[str]:
    """Return the list of material evidence keys the card fails to account for."""
    required = material_evidence(conn, cid)
    missing = []
    reported_ids = set(card.get("material_evidence_ids", {}).values())
    blob = " ".join(str(v) for v in card.get("material_evidence", {}).values())
    for key, row in required.items():
        if row["evidence_id"] in reported_ids:
            continue
        if row["observed_claim"][:40] in blob:
            continue
        missing.append(key)
    return missing


def build_card_checked(conn, cid) -> dict:
    """Build a card and refuse to return one that drops material evidence."""
    card = build_card(conn, cid)
    missing = check_completeness(conn, cid, card)
    if missing:
        raise ReportingCompletenessError(
            f"{cid}: review card omits material evidence: {', '.join(missing)}")
    return card


def build_all(conn, queue: str = "tier_a") -> list[dict]:
    ids = [r["candidate_id"] for r in conn.execute(
        "SELECT candidate_id FROM candidates WHERE queue=? ORDER BY name", (queue,))]
    return [build_card_checked(conn, cid) for cid in ids]


if __name__ == "__main__":
    conn = db.connect()
    cards = build_all(conn)
    print(f"[review] built {len(cards)} Tier A cards, all passing completeness checks")
    for c in cards[:3]:
        print(f"  {c['candidate']}: material={list(c['material_evidence'])} "
              f"federal=${c['total_federal_award_value_usd']:,.0f}")
