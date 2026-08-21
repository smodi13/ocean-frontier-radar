"""Bounded freshness repair for the top of the funnel.

NOT broad sourcing. Phase 2.5 exists because the SBIR bulk file ends in 2023
while candidates kept winning awards afterwards - the ARMADA audit found
$2.7M of federal activity dated after that cutoff. This module re-queries
USAspending *by company name*, for a bounded cohort only, and adds any award
we do not already hold.

It adds evidence to candidates that already exist. It never creates new
candidates, so it cannot widen the universe.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ofr import db

API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
UA = "OceanFrontierRadar/0.25 (research)"
GRANT_CODES = ["02", "03", "04", "05"]
CONTRACT_CODES = ["A", "B", "C", "D"]

FIELDS = ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency",
          "Awarding Sub Agency", "Description", "Start Date", "End Date"]


def _query(name: str, codes: list[str], start="2019-01-01", end=None) -> list[dict]:
    payload = {
        "filters": {"award_type_codes": codes, "keywords": [name],
                    "time_period": [{"start_date": start, "end_date": end or db.today()}]},
        "fields": FIELDS, "limit": 25, "page": 1, "sort": "Start Date", "order": "desc"}
    r = subprocess.run(
        ["curl", "-s", "--max-time", "90", "-X", "POST", API,
         "-H", "Content-Type: application/json", "-A", UA, "-d", json.dumps(payload)],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed for {name!r}: {r.stderr[:200]}")
    try:
        return json.loads(r.stdout).get("results", [])
    except json.JSONDecodeError:
        raise RuntimeError(f"USAspending returned non-JSON for {name!r}: {r.stdout[:200]}")


def _evidence_type(description: str, amount: float | None, is_grant: bool) -> str:
    d = (description or "").upper()
    sttr = "STTR" in d
    # Award size is a more reliable phase indicator than free text. A NOAA
    # Phase I award of $174,798 was classified Phase II purely because the
    # words "phase II" appeared elsewhere in a long abstract.
    small = amount is not None and amount < 400_000
    if ("PHASE II" in d or "PHASE 2" in d) and not small:
        return "sttr_phase_ii" if sttr else "sbir_phase_ii"
    if "PHASE I" in d or "PHASE 1" in d or small:
        return "sttr_phase_i" if sttr else "sbir_phase_i"
    # Large R&D contracts without an explicit phase label are typically Phase II
    # continuations; classify by size rather than guessing from the text.
    if amount and amount >= 750_000:
        return "sbir_phase_ii"
    return "research_grant" if is_grant else "procurement_contract"


def refresh_candidates(conn, candidate_ids: list[str], verbose: bool = True) -> dict:
    run_id = db.stable_id("run", "refresh", db.now())
    started = db.now()
    accessed = db.today()
    added = checked = 0
    errors: list[str] = []

    for cid in candidate_ids:
        row = conn.execute(
            "SELECT candidate_id, name, company FROM candidates WHERE candidate_id=?",
            (cid,)).fetchone()
        if not row:
            errors.append(f"unknown candidate {cid}")
            continue
        name = (row["company"] or row["name"]).strip()
        if len(name) < 4:
            continue
        checked += 1
        for codes, is_grant in ((GRANT_CODES, True), (CONTRACT_CODES, False)):
            try:
                results = _query(name, codes)
            except RuntimeError as e:
                errors.append(str(e))
                continue
            for r in results:
                # Only accept records whose recipient really is this candidate.
                if db.normalize_name(r.get("Recipient Name") or "") != db.normalize_name(name):
                    continue
                award_id = (r.get("Award ID") or "").strip()
                if not award_id:
                    continue
                sid = db.stable_id("src", "usaspending_award", award_id)
                start = db.normalize_date(r.get("Start Date"))
                db.upsert_source(
                    conn, source_id=sid,
                    url=f"https://www.usaspending.gov/search/?keywords={award_id}",
                    title=f"Federal award {award_id}", publisher="USAspending.gov",
                    source_type="federal_award", source_quality="tier1",
                    publication_date=start, accessed_at=accessed,
                    retrieval_method="api", raw_ref=f"usaspending:{award_id}")
                amount = None
                try:
                    amount = float(r.get("Award Amount"))
                except (TypeError, ValueError):
                    pass
                etype = _evidence_type(r.get("Description"), amount, is_grant)
                agency = " / ".join(filter(None, [r.get("Awarding Agency"),
                                                 r.get("Awarding Sub Agency")]))
                db.add_evidence(
                    conn, candidate_id=cid, source_id=sid, evidence_type=etype,
                    observed_claim=(f"Federal award {award_id} from {agency}: "
                                    f"{(r.get('Description') or '').strip()[:160]}"),
                    evidence_date=start, source_date=start,
                    quantitative_value=amount, unit="USD",
                    extraction_method="structured_field", confidence="high",
                    analyst_notes=f"usaspending_award_id={award_id}; "
                                  f"period_end={db.normalize_date(r.get('End Date'))}")
                added += 1
            time.sleep(0.2)
        conn.commit()

    db.log_ingest(conn, run_id=run_id, module="refresh", started_at=started,
                  finished_at=db.now(), records_seen=checked, records_kept=added,
                  status="error" if errors else "ok", message="; ".join(errors[:3]) or None)
    conn.commit()
    if verbose:
        print(f"[refresh] candidates_checked={checked} evidence_rows={added} errors={len(errors)}")
    return {"checked": checked, "added": added, "errors": errors}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=None)
    ap.add_argument("--min-score", type=int, default=12,
                    help="refresh candidates at or above this diagnostic score")
    ap.add_argument("--limit", type=int, default=60)
    a = ap.parse_args()
    conn = db.connect(a.db); db.init_db(conn)
    from ofr import prioritize
    rows = conn.execute("SELECT candidate_id FROM candidates").fetchall()
    scored = [(prioritize.total(conn, r["candidate_id"]), r["candidate_id"]) for r in rows]
    cohort = [c for s, c in sorted(scored, reverse=True) if s >= a.min_score][:a.limit]
    print(f"[refresh] cohort={len(cohort)} (score >= {a.min_score})")
    refresh_candidates(conn, cohort)
