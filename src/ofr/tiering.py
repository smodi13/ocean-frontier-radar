"""Triage into queues. Replaces ordinal ranking.

WHY THIS EXISTS
---------------
Phase 2 produced a 64-way tie at priority 12, so beyond about rank 9 the
"ranking" degenerated into alphabetical order. Presenting that as an ordered
list claims a precision the evidence cannot support. The fix is NOT finer
weights - it is to stop pretending. The system allocates analyst attention;
it does not rank 562 opportunities.

The numeric component score is retained as DIAGNOSTIC METADATA only. It is
never presented as an investment ranking, and within Tier A ordering is
explicitly analyst judgment.

QUEUES
------
frontier : pre-company research signals. Scored on their own framework and
           NEVER numerically compared against funded SBIR companies, because
           they structurally cannot show customers or revenue.
tier_a   : Diligence Now - enough evidence, relevance and CURRENT activity.
tier_b   : Research Queue - relevant, missing one or two important pieces.
tier_c   : Watch - potentially relevant, not actionable yet.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ofr import db, freshness

# --- explicit, evidence-based thresholds -----------------------------------
RECENT_MONTHS = 24          # "current activity" window for Tier A
STALE_MONTHS = 48           # beyond this, a candidate is dormant for our purposes
MIN_TECHNICAL_A = 2         # built/demonstrated, granted patent, or Phase I+
MIN_COMMERCIAL_A = 2        # commercialization funding won on commercial merit
MIN_RELEVANCE_A = 2         # ocean centrality is real, not adjacency-by-accident

EXCLUDING_FLAGS = {"ESTABLISHED_FIRM", "ESTABLISHED_SBIR_CONTRACTOR", "BEYOND_STAGE"}


def _components(conn, cid) -> dict:
    return {r["dimension"]: r["points"] for r in conn.execute(
        "SELECT dimension, points FROM prioritization WHERE candidate_id=?", (cid,))}


def _flags(conn, cid) -> set:
    return {r["flag"] for r in conn.execute(
        "SELECT flag FROM flags WHERE candidate_id=?", (cid,))}


def assess(conn, cid, asof: date | None = None) -> tuple[str, list[str], list[str]]:
    """Return (queue, reasons_for, reasons_against). Every reason is explicit."""
    asof = asof or date.today()
    row = conn.execute(
        """SELECT candidate_type, ocean_centrality, sourcing_signal,
                  candidate_latest_signal_date
           FROM candidates WHERE candidate_id=?""", (cid,)).fetchone()
    if row is None:
        raise KeyError(cid)

    comp = _components(conn, cid)
    flags = _flags(conn, cid)
    age = freshness.months_since(row["candidate_latest_signal_date"], asof)
    for_, against = [], []

    # --- Frontier: pre-company signals get their own queue, always ---------
    # `company_formed` is the deciding fact. ARMADA carries a 'pre_company'
    # sourcing signal (it was surfaced pre-formation) but is an incorporated
    # company with ~$3M of federal awards; routing it to the Frontier queue on
    # the signal label alone was wrong.
    formed = conn.execute(
        "SELECT company_formed FROM candidates WHERE candidate_id=?", (cid,)).fetchone()[0]
    if row["candidate_type"] == "research_project" or (
            row["sourcing_signal"] == "pre_company" and formed != 1):
        for_.append("Pre-company signal: routed to the Frontier queue, which is "
                    "scored on its own framework and never compared numerically "
                    "against funded companies.")
        return "frontier", for_, against

    # --- hard exclusions ---------------------------------------------------
    if row["ocean_centrality"] == "incidental":
        against.append("Ocean connection is incidental.")
        return "tier_c", for_, against
    blocking = flags & EXCLUDING_FLAGS
    if blocking:
        against.append(f"Outside early-stage scope: {', '.join(sorted(blocking))}.")
        return "tier_c", for_, against

    # --- Tier A criteria, each checked and reported ------------------------
    tech = comp.get("technical_evidence", 0)
    comm = comp.get("commercialization_signal", 0)
    rel = comp.get("propeller_relevance", 0)

    checks = {
        "technical": tech >= MIN_TECHNICAL_A,
        "commercial": comm >= MIN_COMMERCIAL_A,
        "relevance": rel >= MIN_RELEVANCE_A,
        "current": age is not None and age <= RECENT_MONTHS,
    }

    if checks["technical"]:
        for_.append(f"Technical evidence {tech}/3: built, demonstrated, patented or Phase I+.")
    else:
        against.append(f"Technical evidence only {tech}/3.")
    if checks["commercial"]:
        for_.append(f"Commercialization evidence {comm}/3.")
    else:
        against.append(f"Commercialization evidence only {comm}/3.")
    if checks["relevance"]:
        for_.append(f"Propeller relevance {rel}/3 with ocean centrality "
                    f"'{row['ocean_centrality']}'.")
    else:
        against.append(f"Propeller relevance only {rel}/3.")
    if checks["current"]:
        for_.append(f"Current activity: latest signal {row['candidate_latest_signal_date']} "
                    f"(~{age:.0f} months old).")
    elif age is None:
        against.append("No dated evidence, so current activity cannot be established.")
    else:
        against.append(f"Latest signal {row['candidate_latest_signal_date']} "
                       f"(~{age:.0f} months old) is outside the {RECENT_MONTHS}-month window.")

    passed = sum(checks.values())
    if passed == 4:
        return "tier_a", for_, against
    if age is not None and age > STALE_MONTHS:
        against.append(f"Dormant: no signal in over {STALE_MONTHS} months.")
        return "tier_c", for_, against
    if passed >= 2:
        return "tier_b", for_, against
    return "tier_c", for_, against


def assign_all(conn, asof: date | None = None, verbose: bool = True) -> dict:
    counts: dict[str, int] = {}
    for r in conn.execute("SELECT candidate_id FROM candidates").fetchall():
        cid = r["candidate_id"]
        queue, for_, against = assess(conn, cid, asof)
        conn.execute("UPDATE candidates SET queue=?, date_last_updated=? WHERE candidate_id=?",
                     (queue, db.today(), cid))
        # Store the explanation as an analyst view so the reason is auditable.
        conn.execute(
            """INSERT OR REPLACE INTO analyst_views
               (view_id,candidate_id,view_type,statement,evidence_ids,author,created_at)
               VALUES (?,?,?,?,NULL,?,?)""",
            (db.stable_id("av", cid, "tier_reason"), cid, "inferred",
             f"Queue '{queue}'. For: {' '.join(for_) or 'none'} "
             f"Against: {' '.join(against) or 'none'}",
             "analyst", db.now()))
        counts[queue] = counts.get(queue, 0) + 1
    conn.commit()
    if verbose:
        print("[tiering] " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return counts


if __name__ == "__main__":
    conn = db.connect()
    freshness.refresh_all(conn)
    assign_all(conn)
