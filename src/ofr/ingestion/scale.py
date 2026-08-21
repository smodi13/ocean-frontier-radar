"""Scale-based stage exclusion.

Award COUNT and company AGE (sbir_enrich) catch established federal
contractors. They do not catch a young company holding very large contracts.
The Phase 2.5 refresh surfaced candidates with $19.8M single awards sitting in
Tier A beside genuine pre-seed companies.

Propeller's stated model is $500K-$3M at pre-seed to Series A. Cumulative
federal awards well above that indicate a company operating at a different
scale. This is descriptive, not a quality judgement, and it raises a FLAG
rather than subtracting points.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ofr import db

TOTAL_FEDERAL_CEILING = 10_000_000   # cumulative awards above this -> beyond stage
SINGLE_AWARD_CEILING = 5_000_000     # any single award above this -> beyond stage

FUNDING_TYPES = ("sbir_phase_i", "sbir_phase_ii", "sttr_phase_i", "sttr_phase_ii",
                 "research_grant", "commercialization_grant", "procurement_contract")


def apply(conn, verbose: bool = True) -> int:
    placeholders = ",".join("?" * len(FUNDING_TYPES))
    rows = conn.execute(
        f"""SELECT candidate_id,
                   SUM(COALESCE(quantitative_value,0)) total,
                   MAX(COALESCE(quantitative_value,0)) biggest
            FROM evidence
            WHERE evidence_type IN ({placeholders}) AND unit='USD'
            GROUP BY candidate_id""", FUNDING_TYPES).fetchall()
    n = 0
    for r in rows:
        total, biggest = r["total"] or 0, r["biggest"] or 0
        if total >= TOTAL_FEDERAL_CEILING or biggest >= SINGLE_AWARD_CEILING:
            db.add_flag(conn, r["candidate_id"], "BEYOND_STAGE",
                        f"Cumulative federal awards ${total:,.0f} "
                        f"(largest ${biggest:,.0f}) indicate a company operating "
                        f"well above Propeller's stated $500K-$3M pre-seed to "
                        f"Series A model.")
            n += 1
    conn.commit()
    if verbose:
        print(f"[scale] flagged {n} candidates as BEYOND_STAGE")
    return n


if __name__ == "__main__":
    conn = db.connect(); apply(conn)
