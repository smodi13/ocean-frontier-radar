"""Phase 2.5 machine-readable exports.

All generated from the database. Nothing is hand-duplicated: if a fact appears
in a report and in JSON, both trace to the same rows.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ofr import db, frontier, prioritize, review, tiering

OUT = db.ROOT / "outputs"


def build(conn) -> dict:
    OUT.mkdir(exist_ok=True)
    meta = {
        "generated_at": db.now(),
        "phase": "2.5",
        "note": ("Queues allocate analyst attention. Numeric component scores are "
                 "DIAGNOSTIC METADATA only, never an investment ranking. Ordering "
                 "within Tier A is analyst judgment."),
        "tier_criteria": {
            "tier_a": (f"Not incidental, not established/beyond-stage, technical>="
                       f"{tiering.MIN_TECHNICAL_A}, commercial>={tiering.MIN_COMMERCIAL_A}, "
                       f"relevance>={tiering.MIN_RELEVANCE_A}, and latest signal within "
                       f"{tiering.RECENT_MONTHS} months."),
            "tier_b": "Relevant and not excluded, but missing one or two Tier A criteria.",
            "tier_c": "Incidental, established/beyond-stage, dormant, or too little evidence.",
            "frontier": ("Pre-company signals. Separate framework; never compared "
                         "numerically against funded companies."),
        },
    }

    # --- Tier A cards ------------------------------------------------------
    cards = review.build_all(conn, "tier_a")
    (OUT / "tier_a.json").write_text(json.dumps(
        {"meta": meta, "count": len(cards), "cards": cards}, indent=1))

    # --- Frontier queue ----------------------------------------------------
    fq = frontier.build_queue(conn)
    for d in fq:
        row = conn.execute(
            """SELECT c.geography, c.candidate_type,
                      (SELECT category_id FROM taxonomy_links t
                       WHERE t.candidate_id=c.candidate_id AND is_primary=1 LIMIT 1) cat
               FROM candidates c WHERE c.candidate_id=?""", (d["candidate_id"],)).fetchone()
        d["taxonomy"] = row["cat"]
        d["geography"] = row["geography"]
        d["candidate_type"] = row["candidate_type"]
        ev = conn.execute(
            """SELECT e.evidence_type, e.observed_claim, e.evidence_date,
                      e.quantitative_value, s.url
               FROM evidence e JOIN sources s USING(source_id)
               WHERE e.candidate_id=? ORDER BY e.evidence_date DESC""",
            (d["candidate_id"],)).fetchall()
        d["evidence"] = [dict(r) for r in ev]
        d["company_formed"] = False
    (OUT / "frontier_signals.json").write_text(json.dumps(
        {"meta": meta, "count": len(fq), "signals": fq}, indent=1))

    # --- Tier summary ------------------------------------------------------
    rows = conn.execute(
        """SELECT c.candidate_id, c.name, c.queue, c.candidate_type, c.ocean_centrality,
                  c.sourcing_signal, c.candidate_latest_signal_date,
                  (SELECT category_id FROM taxonomy_links t
                   WHERE t.candidate_id=c.candidate_id AND is_primary=1 LIMIT 1) cat
           FROM candidates c""").fetchall()
    summary = {
        "meta": meta,
        "total_candidates": len(rows),
        "by_queue": dict(Counter(r["queue"] for r in rows)),
        "by_queue_and_category": {
            q: dict(Counter(r["cat"] for r in rows if r["queue"] == q))
            for q in ("tier_a", "tier_b", "tier_c", "frontier")},
        "by_queue_and_centrality": {
            q: dict(Counter(r["ocean_centrality"] for r in rows if r["queue"] == q))
            for q in ("tier_a", "tier_b", "tier_c", "frontier")},
        "by_queue_and_type": {
            q: dict(Counter(r["candidate_type"] for r in rows if r["queue"] == q))
            for q in ("tier_a", "tier_b", "tier_c", "frontier")},
        "pre_company_share": {
            "frontier_count": sum(1 for r in rows if r["queue"] == "frontier"),
            "actionable_universe": sum(1 for r in rows
                                       if r["queue"] in ("tier_a", "tier_b", "frontier")),
        },
    }
    pcs = summary["pre_company_share"]
    pcs["frontier_share_of_actionable"] = round(
        pcs["frontier_count"] / max(pcs["actionable_universe"], 1), 3)
    (OUT / "tier_summary.json").write_text(json.dumps(summary, indent=1))

    # --- Candidate snapshots ----------------------------------------------
    for cid, fname in (("armada-marine-robotics", "armada_snapshot.json"),
                       ("3newable", "three_newable_snapshot.json")):
        card = review.build_card_checked(conn, cid)
        ev = conn.execute(
            """SELECT e.evidence_type, e.observed_claim, e.evidence_date,
                      e.quantitative_value, e.unit, e.extraction_method,
                      s.url, s.publisher, s.source_quality, s.accessed_at
               FROM evidence e JOIN sources s USING(source_id)
               WHERE e.candidate_id=? ORDER BY e.evidence_date DESC""", (cid,)).fetchall()
        card["full_evidence_chronology"] = [dict(r) for r in ev]
        (OUT / fname).write_text(json.dumps({"meta": meta, "snapshot": card}, indent=1))

    print(f"[export2.5] tier_a={len(cards)} frontier={len(fq)} "
          f"candidates={len(rows)} -> {OUT}")
    return {"tier_a": len(cards), "frontier": len(fq)}


if __name__ == "__main__":
    build(db.connect())
