"""Canonical JSON exports.

Facts live in SQLite. These files are DERIVED views for later frontend use, so
nothing is hand-duplicated across documents; regenerate rather than edit.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ofr import db, prioritize

OUT = db.ROOT / "outputs"


def _candidate_rows(conn):
    return conn.execute("""
        SELECT c.*, (SELECT category_id FROM taxonomy_links t
                     WHERE t.candidate_id=c.candidate_id AND t.is_primary=1 LIMIT 1) primary_category
        FROM candidates c""").fetchall()


def build(conn) -> dict:
    OUT.mkdir(exist_ok=True)
    candidates, evidence_map = [], {}

    for r in _candidate_rows(conn):
        cid = r["candidate_id"]
        comps = {x["dimension"]: {"points": x["points"], "max": x["max_points"],
                                  "rationale": x["rationale"],
                                  "evidence_ids": (x["evidence_ids"] or "").split(",") if x["evidence_ids"] else [],
                                  "analyst_override": bool(x["analyst_override"])}
                 for x in conn.execute(
                     "SELECT * FROM prioritization WHERE candidate_id=?", (cid,))}
        cats = [x["category_id"] for x in conn.execute(
            "SELECT category_id FROM taxonomy_links WHERE candidate_id=?", (cid,))]
        people = [{"name": x["name"], "role": x["role"], "role_type": x["role_type"],
                   "affiliation": x["affiliation"]}
                  for x in conn.execute(
                      "SELECT name,role,role_type,affiliation FROM people WHERE candidate_id=?", (cid,))]
        flags = [{"flag": x["flag"], "rationale": x["rationale"]}
                 for x in conn.execute("SELECT flag,rationale FROM flags WHERE candidate_id=?", (cid,))]
        views = [{"type": x["view_type"], "statement": x["statement"],
                  "evidence_ids": (x["evidence_ids"] or "").split(",") if x["evidence_ids"] else [],
                  "author": x["author"]}
                 for x in conn.execute(
                     "SELECT * FROM analyst_views WHERE candidate_id=?", (cid,))]

        ev_rows = conn.execute("""
            SELECT e.*, s.url, s.title src_title, s.publisher, s.source_type,
                   s.source_quality, s.accessed_at
            FROM evidence e JOIN sources s USING(source_id)
            WHERE e.candidate_id=? ORDER BY e.evidence_date DESC""", (cid,)).fetchall()
        evidence_map[cid] = [{
            "evidence_id": e["evidence_id"], "type": e["evidence_type"],
            "observed_claim": e["observed_claim"], "evidence_date": e["evidence_date"],
            "value": e["quantitative_value"], "unit": e["unit"],
            "extraction_method": e["extraction_method"], "confidence": e["confidence"],
            "source": {"url": e["url"], "title": e["src_title"],
                       "publisher": e["publisher"], "type": e["source_type"],
                       "quality": e["source_quality"], "accessed_at": e["accessed_at"]},
        } for e in ev_rows]

        candidates.append({
            "candidate_id": cid, "name": r["name"], "candidate_type": r["candidate_type"],
            # Added in Phase 4: these columns exist in the database from Phase 2.5
            # but this export predated them, so the queue assignment and derived
            # recency were never reaching downstream consumers.
            "queue": r["queue"],
            "candidate_latest_signal_date": r["candidate_latest_signal_date"],
            "institution": r["institution"], "company": r["company"],
            "geography": r["geography"], "website": r["website"],
            "current_stage": r["current_stage"], "company_formed": r["company_formed"],
            "ocean_centrality": r["ocean_centrality"], "sourcing_signal": r["sourcing_signal"],
            "primary_category": r["primary_category"], "categories": sorted(set(cats)),
            "people": people, "flags": flags, "analyst_views": views,
            "priority_components": comps,
            "priority_total": prioritize.total(conn, cid),
            "priority_max": prioritize.TOTAL_MAX,
            "evidence_count": len(ev_rows),
            "date_first_seen": r["date_first_seen"],
        })

    candidates.sort(key=lambda c: (-c["priority_total"], c["name"]))
    top = [c for c in candidates if c["priority_total"] >= 11][:25]

    proc = {}
    from ofr.ingestion.usaspending import THEME_QUERIES, theme_demand_summary
    for theme in THEME_QUERIES:
        s = theme_demand_summary(conn, theme)
        if s.get("n_contracts"):
            proc[theme] = s

    meta = {
        "generated_at": db.now(),
        "n_candidates": len(candidates),
        "priority_max": prioritize.TOTAL_MAX,
        "note": ("Priority scores rank ANALYST ATTENTION, not investment quality. "
                 "Totals are computed from components and are meaningless without them."),
        "ingest_log": [dict(r) for r in conn.execute(
            "SELECT module,started_at,finished_at,records_seen,records_kept,status,message "
            "FROM ingest_log ORDER BY started_at")],
    }

    (OUT / "candidates.json").write_text(json.dumps(
        {"meta": meta, "candidates": candidates}, indent=1))
    (OUT / "candidate_evidence.json").write_text(json.dumps(
        {"meta": {"generated_at": meta["generated_at"]}, "evidence": evidence_map}, indent=1))
    (OUT / "top_candidates.json").write_text(json.dumps(
        {"meta": meta, "top_candidates": top}, indent=1))
    (OUT / "procurement_evidence.json").write_text(json.dumps(
        {"meta": {"generated_at": meta["generated_at"],
                  "caveat": "Evidence that budgets and buying behaviour exist. NOT market size."},
         "themes": proc}, indent=1))

    print(f"[export] candidates={len(candidates)} top={len(top)} themes={len(proc)} -> {OUT}")
    return {"candidates": len(candidates), "top": len(top)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--db", default=None)
    a = ap.parse_args(); build(db.connect(a.db))
