"""Curated candidate ingestion from config/curated_candidates.yaml.

Some of the highest-value signals are structurally not machine-retrievable:
WHOI's technology-transfer listings moved behind an intranet and ARPA-E returns
403 to automated requests (see research/data_sources.md). Rather than pretend
those sources are automatable or drop the leads, they are curated by hand with
explicit provenance and pushed through the identical schema.

All evidence from this module is marked extraction_method='human_read' so it is
never confused with structured API output.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ofr import db

CURATED = db.ROOT / "config" / "curated_candidates.yaml"


def ingest(conn, path: Path = CURATED, verbose: bool = True) -> dict:
    data = yaml.safe_load(path.read_text())
    run_id = db.stable_id("run", "curated", db.now())
    started = db.now()
    accessed = db.today()
    kept = 0

    for entry in data.get("candidates", []):
        cid = db.candidate_id(entry["name"])
        db.upsert_candidate(
            conn, cid=cid, name=entry["name"],
            candidate_type=entry["candidate_type"],
            institution=entry.get("institution"), company=entry.get("company"),
            geography=entry.get("geography"), website=entry.get("website"),
            current_stage=entry.get("current_stage"),
            company_formed=1 if entry.get("company_formed") else 0,
            ocean_centrality=entry.get("ocean_centrality"),
            sourcing_signal=entry.get("sourcing_signal"))

        src_ids = {}
        for s in entry.get("sources", []):
            sid = db.stable_id("src", "curated", s["id"])
            src_ids[s["id"]] = sid
            db.upsert_source(
                conn, source_id=sid, url=s["url"], title=s["title"],
                publisher=s["publisher"], source_type=s["source_type"],
                source_quality=s["source_quality"],
                publication_date=db.normalize_date(s.get("publication_date")),
                accessed_at=accessed, retrieval_method="manual", raw_ref=s["id"])

        for ev in entry.get("evidence", []):
            sid = src_ids.get(ev["source"])
            if not sid:
                raise ValueError(f"{entry['name']}: evidence references unknown source {ev['source']!r}")
            db.add_evidence(
                conn, candidate_id=cid, source_id=sid, evidence_type=ev["type"],
                observed_claim=ev["claim"], evidence_date=db.normalize_date(ev.get("date")),
                source_date=db.normalize_date(ev.get("date")),
                quantitative_value=ev.get("amount"),
                unit="USD" if ev.get("amount") else None,
                extraction_method="human_read", confidence="high")

        for p in entry.get("people", []):
            db.add_person(conn, candidate_id=cid, name=p["name"], role=p.get("role"),
                          role_type=p.get("role_type"), affiliation=p.get("affiliation"),
                          source_id=next(iter(src_ids.values()), None))

        for i, cat in enumerate(entry.get("categories", [])):
            db.link_taxonomy(conn, cid, cat, is_primary=1 if i == 0 else 0,
                             rationale="Curated from primary source; analyst-assigned.")
        kept += 1

    conn.commit()
    db.log_ingest(conn, run_id=run_id, module="curated", started_at=started,
                  finished_at=db.now(), records_seen=kept, records_kept=kept, status="ok")
    conn.commit()
    if verbose:
        print(f"[curated] candidates={kept}")
    return {"kept": kept}


if __name__ == "__main__":
    conn = db.connect(); db.init_db(conn); ingest(conn)
