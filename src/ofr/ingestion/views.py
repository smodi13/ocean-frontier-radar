"""Load analyst interpretation from config/analyst_views.yaml.

Interpretation is written to `analyst_views`, never to `evidence`. The schema
enforces that any view_type='observed' cites evidence ids.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ofr import db

PATH = db.ROOT / "config" / "analyst_views.yaml"


def ingest(conn, path: Path = PATH, verbose: bool = True) -> dict:
    data = yaml.safe_load(path.read_text())
    added = skipped = 0
    for cid, views in (data.get("views") or {}).items():
        if not conn.execute("SELECT 1 FROM candidates WHERE candidate_id=?", (cid,)).fetchone():
            print(f"[views] WARNING: no candidate {cid!r}; skipping {len(views)} views")
            skipped += len(views)
            continue
        for v in views:
            conn.execute(
                """INSERT OR REPLACE INTO analyst_views
                   (view_id,candidate_id,view_type,statement,evidence_ids,author,created_at)
                   VALUES (?,?,?,?,?,?,?)""",
                (db.stable_id("av", cid, v["type"], v["statement"][:80]), cid,
                 v["type"], v["statement"], v.get("evidence_ids"), "analyst", db.now()))
            added += 1
    conn.commit()
    if verbose:
        print(f"[views] analyst views added={added} skipped={skipped}")
    return {"added": added, "skipped": skipped}


if __name__ == "__main__":
    conn = db.connect(); ingest(conn)
