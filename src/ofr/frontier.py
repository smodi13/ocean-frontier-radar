"""Frontier Signals — the pre-company queue.

WHY IT IS SEPARATE
------------------
Phase 1's hand-built sample was ~39% pre-company. Phase 2's qualified universe
was ~6%, because 200,000 SBIR company records numerically swamped a few dozen
I-Corps awards. The core sourcing thesis is spotting opportunities BEFORE
obvious company formation, so losing them defeats the point.

The fix is NOT to force the company queue back to 39%. Pre-company signals
structurally cannot show customers, revenue or financing, so any shared
ranking buries them. They get their own queue and their own framework.

FRONTIER FRAMEWORK (deliberately different from the company score)
------------------------------------------------------------------
Frontier signals are assessed on:
    translation_intent   is someone actively trying to commercialize this?
    technical_depth      is there real research substance behind it?
    ocean_relevance      does it address a Propeller-relevant problem?
    recency              is the signal current?
There is no commercial-traction dimension, because having none is the norm
here rather than a weakness.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ofr import db, freshness

# Signal taxonomy for the frontier queue.
SIGNAL_TYPES = {
    "icorps": "NSF I-Corps — funded customer discovery, pre-company",
    "commercialization_grant": "PFI / Convergence Accelerator / translation award",
    "research_institution_partnership": "University research partnership",
    "license_executed": "Technology licence executed",
    "exclusive_license": "Exclusive technology licence",
    "spinout_announced": "Spinout announced",
    "accelerator_participation": "Research accelerator entrant",
    "research_grant": "Research grant with translation intent",
}

TRANSLATION_STRONG = {"license_executed", "exclusive_license", "spinout_announced"}
TRANSLATION_ACTIVE = {"icorps", "commercialization_grant", "accelerator_participation"}


def _evidence(conn, cid):
    return conn.execute(
        "SELECT * FROM evidence WHERE candidate_id=?", (cid,)).fetchall()


def signal_type(conn, cid) -> str | None:
    ev = _evidence(conn, cid)
    for group in (TRANSLATION_STRONG, TRANSLATION_ACTIVE):
        for r in ev:
            if r["evidence_type"] in group:
                return r["evidence_type"]
    for r in ev:
        if r["evidence_type"] in SIGNAL_TYPES:
            return r["evidence_type"]
    return None


def assess(conn, cid, asof: date | None = None) -> dict:
    asof = asof or date.today()
    row = conn.execute(
        """SELECT name, institution, ocean_centrality, candidate_latest_signal_date
           FROM candidates WHERE candidate_id=?""", (cid,)).fetchone()
    ev = _evidence(conn, cid)
    types = {r["evidence_type"] for r in ev}

    if types & TRANSLATION_STRONG:
        intent, intent_why = 3, "Licence executed or spinout announced — translation has happened."
    elif types & TRANSLATION_ACTIVE:
        intent, intent_why = 2, "Funded customer discovery or translation programme underway."
    else:
        intent, intent_why = 1, "Research funding present; commercialization intent not yet explicit."

    amounts = [r["quantitative_value"] or 0 for r in ev if r["unit"] == "USD"]
    biggest = max(amounts) if amounts else 0
    if biggest >= 1_000_000:
        depth, depth_why = 3, f"Substantial translation funding (${biggest:,.0f})."
    elif biggest >= 250_000:
        depth, depth_why = 2, f"Meaningful award (${biggest:,.0f})."
    else:
        depth, depth_why = 1, f"Small award (${biggest:,.0f})." if biggest else (1, "No award value recorded.")

    centrality = row["ocean_centrality"]
    relevance = {"central_mechanism": 3, "primary_end_market": 2,
                 "strong_adjacency": 2, "incidental": 0}.get(centrality or "", 1)

    age = freshness.months_since(row["candidate_latest_signal_date"], asof)
    def _age_phrase(months: float) -> str:
        m = round(months)
        if m < 1:
            return "Signal less than a month old."
        return f"Signal ~{m} month{'' if m == 1 else 's'} old."

    if age is None:
        rec, rec_why = 0, "No dated evidence."
    elif age <= 12:
        rec, rec_why = 3, _age_phrase(age)
    elif age <= 24:
        rec, rec_why = 2, _age_phrase(age)
    elif age <= 36:
        rec, rec_why = 1, _age_phrase(age)
    else:
        rec, rec_why = 0, _age_phrase(age) + " Likely dormant."

    return {
        "candidate_id": cid,
        "name": row["name"],
        "institution": row["institution"],
        "signal_type": signal_type(conn, cid),
        "signal_date": row["candidate_latest_signal_date"],
        "ocean_centrality": centrality,
        "components": {
            "translation_intent": {"points": intent, "max": 3, "why": intent_why},
            "technical_depth": {"points": depth, "max": 3, "why": depth_why},
            "ocean_relevance": {"points": relevance, "max": 3,
                                "why": f"Ocean centrality '{centrality}'."},
            "recency": {"points": rec, "max": 3, "why": rec_why},
        },
        "frontier_total": intent + depth + relevance + rec,
        "frontier_max": 12,
        "note": ("Frontier signals are scored on their own framework and are never "
                 "compared numerically against funded companies."),
    }


def build_queue(conn, asof: date | None = None) -> list[dict]:
    ids = [r["candidate_id"] for r in conn.execute(
        "SELECT candidate_id FROM candidates WHERE queue='frontier'")]
    out = [assess(conn, cid, asof) for cid in ids]
    out.sort(key=lambda d: (-d["frontier_total"], d["name"]))
    return out


if __name__ == "__main__":
    conn = db.connect()
    q = build_queue(conn)
    print(f"[frontier] {len(q)} signals")
    for d in q:
        print(f"  {d['frontier_total']:2d}/12 | {str(d['signal_type']):26s} | "
              f"{d['name'][:52]:52s} | {d['institution'] or ''}")
