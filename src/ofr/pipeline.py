"""End-to-end Phase 2 pipeline.

    python3 src/ofr/pipeline.py --full     # rebuild everything (needs network + SBIR file)
    python3 src/ofr/pipeline.py --score    # re-resolve, re-score and re-export only

Each stage fails visibly and is logged to `ingest_log`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ofr import db, entity, export, prioritize
from ofr.ingestion import curated, nsf, quality, sbir, sbir_enrich, usaspending


def run(full: bool, db_path=None, sbir_min_year=2015, nsf_date_start="01/01/2024"):
    conn = db.connect(db_path)
    db.init_db(conn)

    if full:
        for name, fn in [
            ("sbir",        lambda: sbir.ingest(conn, min_year=sbir_min_year)),
            ("quality",     lambda: (quality.purge(conn), quality.sanitize_websites(conn))),
            ("sbir_enrich", lambda: sbir_enrich.enrich(conn)),
            ("nsf",         lambda: nsf.ingest(conn, date_start=nsf_date_start)),
            ("curated",     lambda: curated.ingest(conn)),
            ("usaspending", lambda: usaspending.ingest(conn)),
        ]:
            try:
                fn()
            except Exception as e:                       # fail visibly, keep going
                print(f"[pipeline] STAGE FAILED: {name}: {type(e).__name__}: {e}")
                db.log_ingest(conn, run_id=db.stable_id("run", name, db.now()),
                              module=name, started_at=db.now(), finished_at=db.now(),
                              status="error", message=f"{type(e).__name__}: {e}")
                conn.commit()

    entity.apply_merges(conn)
    entity.find_possible_relationships(conn)
    prioritize.score_all(conn)
    export.build(conn)
    return conn


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--full", action="store_true", help="run all ingestion stages")
    ap.add_argument("--score", action="store_true", help="resolve/score/export only")
    ap.add_argument("--db", default=None)
    a = ap.parse_args()
    run(full=a.full and not a.score, db_path=a.db)
