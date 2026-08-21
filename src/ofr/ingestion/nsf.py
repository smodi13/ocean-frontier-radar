"""NSF Awards API ingestion — the recency source.

The SBIR bulk download effectively ends in 2023. The NSF Awards API returns
awards through the present day, so it is the only source of 2024-2026 signal.
It is also the only source of I-Corps awards, which fund PRE-COMPANY customer
discovery and were the highest-differentiation signal found in Phase 1.

Uses curl via subprocess: on the development machine TLS interception breaks
urllib certificate verification. Disabling verification would be the wrong fix;
Phase 3 should use requests with a certifi bundle.
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
from ofr.lexicon import classify, retrieve, secondary_categories

API = "https://api.nsf.gov/services/v1/awards.json"
UA = "OceanFrontierRadar/0.2 (research)"
FIELDS = ("id,title,awardeeName,awardeeStateCode,awardeeCity,date,startDate,"
          "estimatedTotalAmt,fundProgramName,piFirstName,piLastName,abstractText")

# Programs that indicate commercialization intent, mapped to evidence type
# and to what the award tells us about company formation.
PROGRAM_MAP = {
    "I-CORPS":                ("icorps",                  "research_project", 0, "pre_company"),
    "SBIR PHASE I":           ("sbir_phase_i",            "company",          1, "emerging"),
    "SBIR PHASE II":          ("sbir_phase_ii",           "company",          1, "emerging"),
    "SBIR FAST-TRACK":        ("sbir_phase_i",            "company",          1, "emerging"),
    "STTR PHASE I":           ("sttr_phase_i",            "company",          1, "emerging"),
    "STTR PHASE II":          ("sttr_phase_ii",           "company",          1, "emerging"),
    "PFI":                    ("commercialization_grant", "research_project", 0, "pre_company"),
    "CONVERGENCE ACCELERATOR":("commercialization_grant",  "research_project", 0, "pre_company"),
    "TRANSLATION":            ("commercialization_grant", "research_project", 0, "pre_company"),
}

DEFAULT_KEYWORDS = [
    "underwater", "subsea", "marine", "ocean", "offshore", "seawater", "coastal",
    "corrosion", "biofouling", "antifouling", "aquaculture", "seaweed", "kelp",
    "shellfish", "fisheries", "maritime", "hull", "sonar", "hydrophone",
    "bathymetry", "tidal", "wave energy", "desalination", "storm surge",
    "alkalinity", "carbon removal", "buoy", "glider", "mooring", "reef",
    "estuary", "harmful algal", "seafood", "vessel", "port", "acoustic",
]


def _fetch(keyword: str, offset: int, date_start: str) -> list[dict]:
    q = urllib.parse.urlencode({"keyword": keyword, "dateStart": date_start,
                                "offset": offset, "rpp": 25, "printFields": FIELDS})
    r = subprocess.run(["curl", "-s", "--max-time", "60", "-A", UA, f"{API}?{q}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed for {keyword!r}: {r.stderr[:200]}")
    try:
        return json.loads(r.stdout).get("response", {}).get("award", [])
    except json.JSONDecodeError:
        # Fail visibly rather than silently returning nothing.
        raise RuntimeError(f"NSF returned non-JSON for {keyword!r}: {r.stdout[:200]}")


def _program_info(fund_program: str):
    fp = (fund_program or "").upper()
    for key, val in PROGRAM_MAP.items():
        if key in fp:
            return val
    return None


def ingest(conn, keywords=None, date_start="01/01/2024", max_offset=200,
           verbose=True) -> dict:
    keywords = keywords or DEFAULT_KEYWORDS
    run_id = db.stable_id("run", "nsf", db.now())
    started = db.now()
    accessed = db.today()
    seen = kept = 0
    errors: list[str] = []
    by_program: dict[str, int] = {}

    for kw in keywords:
        for off in range(1, max_offset, 25):
            try:
                awards = _fetch(kw, off, date_start)
            except RuntimeError as e:
                errors.append(str(e))
                break
            if not awards:
                break
            for a in awards:
                seen += 1
                info = _program_info(a.get("fundProgramName"))
                if not info:
                    continue
                ev_type, cand_type, formed, signal = info

                text = " ".join(filter(None, [a.get("title"), a.get("abstractText")]))
                if not retrieve(text, min_score=3):
                    continue
                c = classify(text)
                if c.relevance == "not_relevant":
                    continue

                awardee = (a.get("awardeeName") or "").strip()
                title = (a.get("title") or "").strip()
                if not awardee:
                    continue

                # Pre-company awards are identified by the PROJECT, not the
                # university, so that one institution yields many candidates.
                if cand_type == "research_project":
                    clean = title.split(":", 1)[-1].strip() or title
                    name = clean[:110]
                    cid = db.candidate_id(f"{name} {awardee}")
                    institution, company = awardee, None
                else:
                    name = awardee
                    cid = db.candidate_id(awardee)
                    institution, company = None, awardee

                award_date = db.normalize_date(a.get("date"))
                aid = str(a.get("id"))
                url = f"https://www.nsf.gov/awardsearch/showAward?AWD_ID={aid}"
                sid = db.stable_id("src", "nsf", aid)
                db.upsert_source(conn, source_id=sid, url=url, title=title,
                                 publisher="National Science Foundation",
                                 source_type="federal_award", source_quality="tier1",
                                 publication_date=award_date, accessed_at=accessed,
                                 retrieval_method="api", raw_ref=f"nsf:{aid}")

                city = (a.get("awardeeCity") or "").strip()
                state = (a.get("awardeeStateCode") or "").strip()
                geo = ", ".join(p for p in (city, state) if p) or None
                amount = None
                try:
                    amount = float(a.get("estimatedTotalAmt"))
                except (TypeError, ValueError):
                    amount = None

                db.upsert_candidate(
                    conn, cid=cid, name=name, candidate_type=cand_type,
                    institution=institution, company=company, geography=geo,
                    current_stage="pre_formation" if not formed else "pre_seed",
                    company_formed=formed, ocean_centrality=c.ocean_centrality,
                    sourcing_signal=signal)

                db.add_evidence(
                    conn, candidate_id=cid, source_id=sid, evidence_type=ev_type,
                    observed_claim=f"NSF {a.get('fundProgramName')} award: {title}",
                    verbatim_quote=(a.get("abstractText") or "")[:2000] or None,
                    evidence_date=award_date, source_date=award_date,
                    quantitative_value=amount, unit="USD",
                    extraction_method="structured_field", confidence="high",
                    analyst_notes=f"nsf_award_id={aid}")

                pi = " ".join(filter(None, [a.get("piFirstName"), a.get("piLastName")])).strip()
                if pi:
                    db.add_person(conn, candidate_id=cid, name=pi,
                                  role="Principal Investigator",
                                  role_type="academic_pi" if cand_type == "research_project" else "founder",
                                  affiliation=awardee, source_id=sid)

                db.link_taxonomy(conn, cid, c.category_id, is_primary=1, rationale=c.rationale)
                for sec in secondary_categories(c.matches, c.category_id):
                    db.link_taxonomy(conn, cid, sec)
                conn.execute("""INSERT OR REPLACE INTO classifications
                       (classification_id,record_key,candidate_id,category_id,ocean_centrality,
                        relevance,rationale,classifier,source_text,created_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (db.stable_id("cls", sid), sid, cid, c.category_id, c.ocean_centrality,
                     c.relevance, c.rationale, "rules_v1", text[:4000], db.now()))
                by_program[ev_type] = by_program.get(ev_type, 0) + 1
                kept += 1
            time.sleep(0.1)
        conn.commit()

    db.log_ingest(conn, run_id=run_id, module="nsf", started_at=started,
                  finished_at=db.now(), records_seen=seen, records_kept=kept,
                  status="error" if errors else "ok",
                  message="; ".join(errors[:3]) if errors else f"date_start={date_start}")
    conn.commit()
    if verbose:
        print(f"[nsf] seen={seen} kept={kept} errors={len(errors)}")
        for p, n in sorted(by_program.items(), key=lambda x: -x[1]):
            print(f"       {n:4d}  {p}")
    return {"seen": seen, "kept": kept, "by_program": by_program, "errors": errors}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=None)
    ap.add_argument("--date-start", default="01/01/2024")
    a = ap.parse_args()
    conn = db.connect(a.db); db.init_db(conn)
    ingest(conn, date_start=a.date_start)
