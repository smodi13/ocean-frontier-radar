"""Post-ingest enrichment: SBIR award history per company.

A company's TOTAL lifetime SBIR/STTR award count is a strong, cheap signal of
what kind of organisation it is. Firms with dozens of awards stretching back
decades are established federal R&D contractors ("SBIR shops"), not early-stage
venture candidates - Boston Engineering, Scientific Systems, Cornerstone
Research and similar all surfaced in the first ingest run.

This is descriptive, not a quality judgement: a long award history is evidence
about company type, and it drives `sourcing_signal`, not the priority score.
"""
from __future__ import annotations

import csv
import sys
from datetime import date
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ofr import db

csv.field_size_limit(10**9)
RAW = db.ROOT / "data" / "raw" / "sbir_award_data.csv"

# Thresholds are deliberately coarse and stated openly.
OBVIOUS_AWARD_COUNT = 15       # many lifetime awards -> federal R&D contractor
EMERGING_AWARD_COUNT = 6       # repeat recipient
ESTABLISHED_AGE_YEARS = 12     # first award this long ago -> not an early-stage company

# Name patterns that indicate a services/consulting business rather than a
# product company. Descriptive only: this raises a FLAG, never a score penalty.
CONSULTANCY_MARKERS = ("consultant", "consulting", "associates", "advisory",
                       "engineering services", "solutions group")


def enrich(conn, path: Path = RAW, verbose: bool = True) -> dict:
    wanted, names = {}, {}
    for r in conn.execute("SELECT candidate_id, name FROM candidates WHERE candidate_type='company'"):
        key = db.normalize_name(r["name"])
        wanted[key] = r["candidate_id"]
        names[key] = r["name"]
    if not wanted:
        return {}

    counts = defaultdict(int)
    first_year, last_year = {}, {}
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            key = db.normalize_name(row.get("Company") or "")
            if key in wanted:
                counts[key] += 1
                y = (row.get("Award Year") or "").strip()
                if y.isdigit():
                    y = int(y)
                    first_year[key] = min(first_year.get(key, y), y)
                    last_year[key] = max(last_year.get(key, y), y)

    updated = 0
    for key, cid in wanted.items():
        n = counts.get(key, 0)
        if not n:
            continue
        fy, ly = first_year.get(key), last_year.get(key)
        age = (date.today().year - fy) if fy else 0
        name = names[key]

        # Company AGE is a stronger maturity signal than award count. Ocean Power
        # Technologies has only 12 awards but has been taking them since 1995 -
        # it is a public company, not an early-stage candidate. An award-count
        # rule alone ranked it alongside genuine pre-seed companies.
        if age >= ESTABLISHED_AGE_YEARS:
            signal, note = "obvious", (
                f"{n} lifetime SBIR/STTR awards, first in {fy} ({age} years ago): "
                f"long-established firm, outside early-stage venture scope.")
            flag = "ESTABLISHED_FIRM"
        elif n >= OBVIOUS_AWARD_COUNT:
            signal, note = "obvious", (
                f"{n} lifetime SBIR/STTR awards ({fy}-{ly}): established federal "
                f"R&D contractor profile, not an early-stage venture candidate.")
            flag = "ESTABLISHED_SBIR_CONTRACTOR"
        elif n >= EMERGING_AWARD_COUNT:
            signal, note = "emerging", (
                f"{n} lifetime SBIR/STTR awards ({fy}-{ly}): repeat SBIR recipient.")
            flag = "REPEAT_SBIR_RECIPIENT"
        else:
            signal, note = "emerging", f"{n} lifetime SBIR/STTR award(s) ({fy}-{ly})."
            flag = None

        conn.execute("UPDATE candidates SET sourcing_signal=?, date_last_updated=? "
                     "WHERE candidate_id=?", (signal, db.today(), cid))
        if flag:
            db.add_flag(conn, cid, flag, note)
        if any(m in name.lower() for m in CONSULTANCY_MARKERS):
            db.add_flag(conn, cid, "CONSULTANCY_RISK",
                        "Company name indicates a services/consulting business; "
                        "verify whether revenue is product or project based.")
        conn.execute("""INSERT OR REPLACE INTO classifications
              (classification_id,record_key,candidate_id,category_id,ocean_centrality,
               relevance,rationale,classifier,source_text,created_at)
              VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (db.stable_id("cls", cid, "history"), f"history:{cid}", cid, None, None,
             "relevant", note, "rules_v1", None, db.now()))
        updated += 1
    conn.commit()
    if verbose:
        obv = conn.execute("SELECT COUNT(*) n FROM flags WHERE flag='ESTABLISHED_SBIR_CONTRACTOR'").fetchone()["n"]
        print(f"[sbir_enrich] companies enriched={updated} flagged_as_established={obv}")
    return {"updated": updated}


if __name__ == "__main__":
    conn = db.connect(); enrich(conn)
