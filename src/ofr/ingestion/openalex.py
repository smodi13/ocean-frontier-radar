"""OpenAlex ingestion — researcher and publication corroboration.

Deliberately NOT a discovery channel. Phase 1 concluded that publication volume
is not commercialization intent, and treating citation counts as a venture
signal would be exactly the "score pretending to be judgment" failure this
project exists to avoid.

Its job here is narrow and useful: given a candidate that was surfaced by a
COMMERCIALIZATION signal (a grant, a license, a spinout), find peer-reviewed
work by its named people/institution and attach it as supporting technical
evidence. That is what upgrades a candidate's Technical Evidence score
honestly.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ofr import db

API = "https://api.openalex.org/works"
UA = "OceanFrontierRadar/0.2 (research)"
MAILTO = "ocean-frontier-radar@example.invalid"   # polite pool; no personal address


def _search(query: str, per_page: int = 5) -> list[dict]:
    q = urllib.parse.urlencode({"search": query, "per-page": per_page,
                                "mailto": MAILTO, "sort": "cited_by_count:desc"})
    r = subprocess.run(["curl", "-s", "--max-time", "60", "-A", UA, f"{API}?{q}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed for {query!r}: {r.stderr[:200]}")
    try:
        return json.loads(r.stdout).get("results", [])
    except json.JSONDecodeError:
        raise RuntimeError(f"OpenAlex returned non-JSON for {query!r}: {r.stdout[:200]}")


def corroborate(conn, candidate_ids: list[str] | None = None, max_works: int = 3,
                verbose: bool = True) -> dict:
    """Attach publication evidence to already-surfaced candidates only."""
    if candidate_ids:
        placeholders = ",".join("?" * len(candidate_ids))
        rows = conn.execute(
            f"SELECT candidate_id,name,institution FROM candidates "
            f"WHERE candidate_id IN ({placeholders})", candidate_ids).fetchall()
    else:
        rows = conn.execute("SELECT candidate_id,name,institution FROM candidates").fetchall()

    run_id = db.stable_id("run", "openalex", db.now())
    started = db.now()
    accessed = db.today()
    seen = kept = 0
    errors: list[str] = []

    for row in rows:
        cid = row["candidate_id"]
        people = conn.execute(
            "SELECT name, affiliation FROM people WHERE candidate_id=?", (cid,)).fetchall()
        if not people:
            continue
        for p in people[:2]:
            query = f"{p['name']} {row['institution'] or p['affiliation'] or ''}".strip()
            if len(query) < 6:
                continue
            try:
                works = _search(query, per_page=max_works)
            except RuntimeError as e:
                errors.append(str(e))
                continue
            for w in works:
                seen += 1
                # Only keep works where the person is genuinely an author.
                authors = " ".join(
                    (a.get("author") or {}).get("display_name", "") for a in w.get("authorships", []))
                if db.normalize_name(p["name"]).split()[-1] not in db.normalize_name(authors):
                    continue
                wid = (w.get("id") or "").rsplit("/", 1)[-1]
                if not wid:
                    continue
                doi = w.get("doi")
                sid = db.stable_id("src", "openalex", wid)
                db.upsert_source(
                    conn, source_id=sid, url=doi or w.get("id"),
                    title=(w.get("title") or "")[:400], publisher="OpenAlex",
                    source_type="publication", source_quality="tier2",
                    publication_date=db.normalize_date(w.get("publication_date")),
                    accessed_at=accessed, retrieval_method="api", raw_ref=f"openalex:{wid}")
                db.add_evidence(
                    conn, candidate_id=cid, source_id=sid,
                    evidence_type="peer_reviewed_publication",
                    observed_claim=f"Publication co-authored by {p['name']}: {w.get('title')}",
                    evidence_date=db.normalize_date(w.get("publication_date")),
                    source_date=db.normalize_date(w.get("publication_date")),
                    quantitative_value=w.get("cited_by_count"), unit="citations",
                    extraction_method="structured_field", confidence="medium",
                    analyst_notes="Corroboration only; publication volume is not "
                                  "commercialization intent.")
                kept += 1
            time.sleep(0.15)
        conn.commit()

    db.log_ingest(conn, run_id=run_id, module="openalex", started_at=started,
                  finished_at=db.now(), records_seen=seen, records_kept=kept,
                  status="error" if errors else "ok", message="; ".join(errors[:3]) or None)
    conn.commit()
    if verbose:
        print(f"[openalex] works_seen={seen} evidence_added={kept} errors={len(errors)}")
    return {"seen": seen, "kept": kept, "errors": errors}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=None)
    ap.add_argument("--candidates", nargs="*", default=None)
    a = ap.parse_args()
    conn = db.connect(a.db); db.init_db(conn)
    corroborate(conn, a.candidates)
