"""Candidate recency, derived from evidence rather than from retrieval.

Phase 2 conflated three different dates and it corrupted the `timing` score:

    source.accessed_at              when WE retrieved the record
    evidence.evidence_date          when the underlying EVENT happened
    candidate_latest_signal_date    the candidate's most recent real signal

Because the SBIR bulk file ends in 2023 while the NSF API returns awards
through last week, `timing` was largely reporting *which source found the
candidate*. Ranking on that is ranking our own plumbing.

This module computes `candidate_latest_signal_date` strictly from
`evidence.evidence_date`. `accessed_at` is never consulted, and a candidate
with no dated evidence gets NULL rather than a fabricated date.
"""
from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ofr import db

# Evidence types that represent a real-world state change worth calling a
# "signal". Publications are excluded: an old paper is not company news.
SIGNAL_TYPES = {
    "sbir_phase_i", "sbir_phase_ii", "sttr_phase_i", "sttr_phase_ii",
    "icorps", "commercialization_grant", "research_grant",
    "venture_financing", "form_d_filing", "non_dilutive_prize",
    "exclusive_license", "license_executed", "patent_granted",
    "spinout_announced", "company_incorporated", "accelerator_participation",
    "named_customer", "pilot_deployment", "industry_partnership",
    "offtake_agreement", "revenue_disclosed", "procurement_contract",
    "field_trial", "independent_validation", "technical_milestone",
    "prototype_demonstrated", "regulatory_milestone",
    "research_institution_partnership",
}


def latest_signal_date(conn, candidate_id: str) -> str | None:
    row = conn.execute(
        """SELECT MAX(evidence_date) d FROM evidence
           WHERE candidate_id = ? AND evidence_date IS NOT NULL""",
        (candidate_id,)).fetchone()
    return row["d"] if row and row["d"] else None


def refresh_all(conn, verbose: bool = True) -> int:
    n = 0
    for r in conn.execute("SELECT candidate_id FROM candidates").fetchall():
        d = latest_signal_date(conn, r["candidate_id"])
        conn.execute(
            "UPDATE candidates SET candidate_latest_signal_date=? WHERE candidate_id=?",
            (d, r["candidate_id"]))
        n += 1
    conn.commit()
    if verbose:
        undated = conn.execute(
            "SELECT COUNT(*) n FROM candidates WHERE candidate_latest_signal_date IS NULL"
        ).fetchone()["n"]
        print(f"[freshness] refreshed {n} candidates ({undated} with no dated evidence)")
    return n


def months_since(signal_date: str | None, asof: date | None = None) -> float | None:
    """Age of the candidate's latest signal, or None if undated."""
    if not signal_date:
        return None
    asof = asof or date.today()
    try:
        d = datetime.strptime(signal_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (asof - d).days / 30.44
