"""SBIR/STTR bulk award ingestion.

Closes the Phase 1 data gap. The SBIR.gov *API* returns HTTP 403 to automated
requests, but SBIR.gov publishes the full award dataset as an official public
download, which is the sanctioned route and carries MORE fields than the API:

    https://data.www.sbir.gov/awarddatapublic/award_data.csv   (with abstracts)

Abstracts are essential for technical classification, so the abstract file is
used deliberately despite its size (~350MB, ~207k awards).

PRIVACY: the file contains contact and PI phone numbers and email addresses.
Those columns are deliberately NOT ingested. Only professional identity
(PI name, company, research institution) is retained.

KNOWN LIMITATION: as downloaded on 2026-08-21 this dataset effectively ends in
2023 (5,410 awards dated 2023; 24 in 2024). It delivers cross-agency BREADTH -
notably Navy, NOAA, DOE, NASA - but not recency. The NSF Awards API remains the
only source of 2025-2026 awards. Both are ingested for that reason.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ofr import db
from ofr.lexicon import classify, retrieve, secondary_categories

csv.field_size_limit(10**9)

RAW = db.ROOT / "data" / "raw" / "sbir_award_data.csv"
DOWNLOAD_URL = "https://data.www.sbir.gov/awarddatapublic/award_data.csv"
AWARD_PAGE = "https://www.sbir.gov/awards"

# Agencies prioritised by thesis relevance. Others are not excluded - they are
# retrieved too, and judged on technology, per the Phase 2 brief.
PRIORITY_AGENCIES = {
    "Department of Defense", "Department of Commerce", "Department of Energy",
    "National Science Foundation", "National Aeronautics and Space Administration",
    "Environmental Protection Agency", "Department of Homeland Security",
    "Department of Transportation",
}

# Columns that must never enter the database.
BLOCKED_COLUMNS = {"Contact Phone", "Contact Email", "PI Phone", "PI Email",
                   "RI POC Phone", "Contact Name", "RI POC Name"}


def _text_for_match(row: dict) -> str:
    return " ".join(filter(None, [row.get("Award Title"), row.get("Abstract")]))


def _phase_stage(phase: str) -> str:
    p = (phase or "").lower()
    if "ii" in p:
        return "seed"
    return "pre_seed"


def _evidence_type(phase: str, program: str) -> str:
    prog = (program or "").upper()
    p = (phase or "").upper()
    if "STTR" in prog:
        return "sttr_phase_ii" if "II" in p else "sttr_phase_i"
    return "sbir_phase_ii" if "II" in p else "sbir_phase_i"


def ingest(conn, path: Path = RAW, min_year: int = 2015, limit: int | None = None,
           verbose: bool = True) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Download it first:\n  curl -L -o {path} {DOWNLOAD_URL}")

    run_id = db.stable_id("run", "sbir", db.now())
    started = db.now()
    downloaded_at = (path.parent / "sbir_downloaded_at.txt")
    accessed = (downloaded_at.read_text().strip()[:10]
                if downloaded_at.exists() else db.today())

    seen = kept = 0
    by_agency: dict[str, int] = {}
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            seen += 1
            if limit and seen > limit:
                break
            year_raw = (row.get("Award Year") or "").strip()
            if not year_raw.isdigit() or int(year_raw) < min_year:
                continue

            text = _text_for_match(row)
            if not retrieve(text, min_score=3):     # Stage A: recall-oriented
                continue
            c = classify(text)                       # Stage B: relevance
            if c.relevance == "not_relevant":
                continue

            company = (row.get("Company") or "").strip()
            if not company:
                continue
            cid = db.candidate_id(company)
            contract = (row.get("Contract") or "").strip()
            tracking = (row.get("Agency Tracking Number") or "").strip()
            award_date = db.normalize_date(row.get("Proposal Award Date")) or \
                         db.normalize_date(year_raw)

            sid = db.stable_id("src", "sbir", contract or tracking or
                               f"{company}|{row.get('Award Title')}")
            db.upsert_source(
                conn, source_id=sid, url=AWARD_PAGE,
                title=(row.get("Award Title") or "").strip(),
                publisher=f"SBIR.gov / {row.get('Agency') or 'unknown'}",
                source_type="federal_award", source_quality="tier1",
                publication_date=award_date, accessed_at=accessed,
                retrieval_method="bulk_download", raw_ref=str(path.name))

            website = (row.get("Company Website") or "").strip() or None
            city, state = (row.get("City") or "").strip(), (row.get("State") or "").strip()
            geo = ", ".join(p for p in (city, state) if p) or None
            ri = (row.get("RI Name") or "").strip() or None

            db.upsert_candidate(
                conn, cid=cid, name=company, candidate_type="company",
                institution=ri, company=company, geography=geo, website=website,
                current_stage=_phase_stage(row.get("Phase")), company_formed=1,
                ocean_centrality=c.ocean_centrality, sourcing_signal="emerging")

            amount = None
            try:
                amount = float(str(row.get("Award Amount") or "").replace(",", "").replace("$", ""))
            except ValueError:
                amount = None

            agency = (row.get("Agency") or "").strip()
            branch = (row.get("Branch") or "").strip()
            agency_label = f"{agency}{' / ' + branch if branch else ''}"
            db.add_evidence(
                conn, candidate_id=cid, source_id=sid,
                evidence_type=_evidence_type(row.get("Phase"), row.get("Program")),
                observed_claim=(f"{row.get('Program')} {row.get('Phase')} award from "
                                f"{agency_label}: {row.get('Award Title')}"),
                verbatim_quote=(row.get("Abstract") or "")[:2000] or None,
                evidence_date=award_date, source_date=award_date,
                quantitative_value=amount, unit="USD",
                extraction_method="structured_field", confidence="high",
                analyst_notes=f"contract={contract or tracking}")

            pi = (row.get("PI Name") or "").strip()
            if pi:
                db.add_person(conn, candidate_id=cid, name=pi, role="Principal Investigator",
                              role_type="founder" if not ri else "academic_and_founder",
                              affiliation=company, source_id=sid)

            # STTR requires a research-institution partner: that is a licensed
            # or collaborative university link, i.e. a spinout-shaped signal.
            if ri and "STTR" in (row.get("Program") or "").upper():
                db.add_evidence(
                    conn, candidate_id=cid, source_id=sid,
                    evidence_type="research_institution_partnership",
                    observed_claim=f"STTR research institution partner: {ri}",
                    evidence_date=award_date, source_date=award_date,
                    extraction_method="structured_field", confidence="high")

            db.link_taxonomy(conn, cid, c.category_id, is_primary=1, rationale=c.rationale)
            for sec in secondary_categories(c.matches, c.category_id):
                db.link_taxonomy(conn, cid, sec)

            conn.execute(
                """INSERT OR REPLACE INTO classifications
                   (classification_id,record_key,candidate_id,category_id,
                    ocean_centrality,relevance,rationale,classifier,source_text,created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (db.stable_id("cls", sid), sid, cid, c.category_id, c.ocean_centrality,
                 c.relevance, c.rationale, "rules_v1", text[:4000], db.now()))

            by_agency[agency] = by_agency.get(agency, 0) + 1
            kept += 1

    conn.commit()
    db.log_ingest(conn, run_id=run_id, module="sbir", started_at=started,
                  finished_at=db.now(), records_seen=seen, records_kept=kept,
                  status="ok", message=f"min_year={min_year}")
    conn.commit()
    if verbose:
        print(f"[sbir] seen={seen} kept={kept}")
        for a, n in sorted(by_agency.items(), key=lambda x: -x[1])[:10]:
            print(f"        {n:5d}  {a}")
    return {"seen": seen, "kept": kept, "by_agency": by_agency}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=None)
    ap.add_argument("--min-year", type=int, default=2015)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    conn = db.connect(a.db)
    db.init_db(conn)
    ingest(conn, min_year=a.min_year, limit=a.limit)
