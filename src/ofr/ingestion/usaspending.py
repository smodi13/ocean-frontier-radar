"""USAspending procurement ingestion — demand-side evidence.

Phase 1 established that USAspending is weak for discovering startups and
strong for proving that a BUDGET LINE EXISTS. Queries return procurement and
services contracts: who buys, from whom, how much, how often.

This module formalises that. Records land in the `procurement` table, keyed by
THEME rather than candidate, and are never used as a market-size estimate. A
single contract is evidence of buying behaviour, not a TAM.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ofr import db

API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
UA = "OceanFrontierRadar/0.2 (research)"
CONTRACT_CODES = ["A", "B", "C", "D"]

# Themes map to the taxonomy. Each is a real purchasing question:
# "who currently pays to solve this problem?"
THEME_QUERIES = {
    "maritime_autonomy":  ["autonomous underwater vehicle", "unmanned underwater vehicle",
                           "remotely operated vehicle survey"],
    "ocean_sensing":      ["underwater acoustic communication", "hydrophone array",
                           "ocean observing system", "hydrographic survey"],
    "marine_materials":   ["marine corrosion", "biofouling", "antifouling coating",
                           "cathodic protection"],
    "offshore_energy":    ["subsea cable", "offshore wind survey", "marine energy"],
    "coastal_adaptation": ["coastal resilience", "shoreline protection", "storm surge modeling"],
    "blue_food":          ["aquaculture", "shellfish restoration"],
    "marine_carbon":      ["ocean acidification monitoring", "carbon dioxide removal ocean"],
}


def _query(keyword: str, start: str, end: str, limit: int = 50) -> list[dict]:
    payload = {
        "filters": {"award_type_codes": CONTRACT_CODES, "keywords": [keyword],
                    "time_period": [{"start_date": start, "end_date": end}]},
        "fields": ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency",
                   "Awarding Sub Agency", "Description", "Start Date"],
        "limit": limit, "page": 1, "sort": "Award Amount", "order": "desc"}
    r = subprocess.run(
        ["curl", "-s", "--max-time", "90", "-X", "POST", API,
         "-H", "Content-Type: application/json", "-A", UA, "-d", json.dumps(payload)],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed: {r.stderr[:200]}")
    try:
        return json.loads(r.stdout).get("results", [])
    except json.JSONDecodeError:
        raise RuntimeError(f"USAspending returned non-JSON: {r.stdout[:200]}")


def ingest(conn, start="2021-01-01", end=None, verbose=True) -> dict:
    end = end or db.today()
    run_id = db.stable_id("run", "usaspending", db.now())
    started = db.now()
    accessed = db.today()
    seen = kept = 0
    errors: list[str] = []

    for theme, keywords in THEME_QUERIES.items():
        for kw in keywords:
            try:
                rows = _query(kw, start, end)
            except RuntimeError as e:
                errors.append(f"{theme}/{kw}: {e}")
                continue
            for row in rows:
                seen += 1
                award_id = (row.get("Award ID") or "").strip()
                if not award_id:
                    continue
                sid = db.stable_id("src", "usaspending", award_id)
                db.upsert_source(
                    conn, source_id=sid,
                    url=f"https://www.usaspending.gov/search?keywords={kw.replace(' ', '%20')}",
                    title=f"Federal contract {award_id}", publisher="USAspending.gov",
                    source_type="procurement", source_quality="tier1",
                    publication_date=db.normalize_date(row.get("Start Date")),
                    accessed_at=accessed, retrieval_method="api",
                    raw_ref=f"usaspending:{award_id}")
                amount = None
                try:
                    amount = float(row.get("Award Amount"))
                except (TypeError, ValueError):
                    amount = None
                conn.execute(
                    """INSERT OR REPLACE INTO procurement
                       (procurement_id,theme,award_id,recipient,awarding_agency,
                        awarding_sub_agency,amount,start_date,description,source_id)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (db.stable_id("proc", award_id, theme), theme, award_id,
                     (row.get("Recipient Name") or "").strip(),
                     (row.get("Awarding Agency") or "").strip(),
                     (row.get("Awarding Sub Agency") or "").strip(),
                     amount, db.normalize_date(row.get("Start Date")),
                     (row.get("Description") or "").strip()[:1000], sid))
                kept += 1
        conn.commit()

    db.log_ingest(conn, run_id=run_id, module="usaspending", started_at=started,
                  finished_at=db.now(), records_seen=seen, records_kept=kept,
                  status="error" if errors else "ok", message="; ".join(errors[:3]) or None)
    conn.commit()
    if verbose:
        print(f"[usaspending] seen={seen} kept={kept} errors={len(errors)}")
    return {"seen": seen, "kept": kept, "errors": errors}


# ------------------------------------------------------- reusable analysis
# These exist so Phase 3 bottom-up market work can reuse them rather than
# re-deriving procurement facts by hand.
def theme_demand_summary(conn, theme: str) -> dict:
    rows = conn.execute(
        "SELECT recipient, awarding_agency, awarding_sub_agency, amount, start_date, "
        "description, award_id FROM procurement WHERE theme=? AND amount IS NOT NULL",
        (theme,)).fetchall()
    if not rows:
        return {"theme": theme, "n_contracts": 0}
    amounts = sorted(r["amount"] for r in rows)
    buyers = Counter(r["awarding_sub_agency"] or r["awarding_agency"] for r in rows)
    suppliers = Counter(r["recipient"] for r in rows)
    repeat = {s: n for s, n in suppliers.items() if n > 1}
    years = Counter((r["start_date"] or "")[:4] for r in rows if r["start_date"])
    return {
        "theme": theme,
        "n_contracts": len(rows),
        "total_observed_usd": round(sum(amounts), 2),
        "median_contract_usd": amounts[len(amounts) // 2],
        "max_contract_usd": amounts[-1],
        "top_buyers": buyers.most_common(5),
        "top_suppliers": suppliers.most_common(5),
        "repeat_suppliers": sorted(repeat.items(), key=lambda x: -x[1])[:5],
        "years_active": sorted(y for y in years if y),
        "recurring": len([y for y in years if y]) >= 3,
        "caveat": ("Observed contract sample from keyword search. Evidence that a "
                   "budget and buying behaviour exist. NOT a market size estimate."),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=None)
    ap.add_argument("--start", default="2021-01-01")
    a = ap.parse_args()
    conn = db.connect(a.db); db.init_db(conn)
    ingest(conn, start=a.start)
