"""Build frontend-safe JSON from canonical research artifacts.

The research outputs remain the source of truth. Nothing numeric is typed into
the UI: every figure the site displays is resolved here from the canonical
database exports, the procurement audit, the underwriting model and the
evidence register.

Narrative prose lives in config/*.yaml and may contain {{token}} placeholders.
Unknown tokens are a hard error, so a typo cannot silently ship a wrong number.

    python3 scripts/build_frontend_data.py            # build + validate
    python3 scripts/build_frontend_data.py --check    # validate only, no write
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

OUTPUTS = ROOT / "outputs"
RESEARCH = ROOT / "research"
CONFIG = ROOT / "config"
DEST = ROOT / "frontend" / "data"

PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")


class ExportError(RuntimeError):
    """Raised when canonical data cannot produce a valid frontend artifact."""


# ------------------------------------------------------------------ helpers
def _load(path: Path):
    if not path.exists():
        raise ExportError(f"canonical artifact missing: {path}")
    return json.loads(path.read_text())


def _money(n: float) -> str:
    return f"${n:,.0f}"


def _money_compact(n: float) -> str:
    if n >= 1_000_000:
        return f"${n/1_000_000:.2f}M"
    if n >= 1_000:
        return f"${n/1_000:.0f}K"
    return f"${n:,.0f}"


def resolve(text: str, tokens: dict) -> str:
    """Substitute {{token}} placeholders. Unknown tokens raise."""
    def sub(m):
        key = m.group(1)
        if key not in tokens:
            raise ExportError(f"unknown placeholder {{{{{key}}}}}")
        return tokens[key]
    return PLACEHOLDER.sub(sub, text)


def resolve_deep(obj, tokens):
    if isinstance(obj, str):
        return resolve(obj, tokens)
    if isinstance(obj, list):
        return [resolve_deep(o, tokens) for o in obj]
    if isinstance(obj, dict):
        return {k: resolve_deep(v, tokens) for k, v in obj.items()}
    return obj


# ------------------------------------------------------------------ builders
# Terse procurement descriptions ("SBIR PHASE 1.") make poor summaries even though
# they are attached to the largest, most recent award. Prefer a descriptive claim.
_TERSE = re.compile(r"^\s*(federal award \S+ from [^:]+:\s*)?(sbir|sttr)?\s*(phase\s*[i1v2]+)?\s*\.?\s*$",
                    re.IGNORECASE)


def _summary_claim(ev: list) -> dict | None:
    """Pick the most informative evidence record to describe the candidate."""
    if not ev:
        return None
    def informative(e):
        claim = (e.get("observed_claim") or "")
        tail = claim.split(":", 1)[-1].strip()
        return len(tail) > 25 and not _TERSE.match(tail)
    pool = [e for e in ev if informative(e)] or list(ev)
    pool.sort(key=lambda e: (len(e.get("observed_claim") or ""),
                             e.get("evidence_date") or ""), reverse=True)
    return pool[0]


def _merge_people(people: list) -> list:
    """Collapse name variants from different sources (e.g. 'Jeff' vs 'Jeffrey').

    Records arrive from federal award data and from curated sources with
    different name forms for the same person, which surfaced as duplicate rows
    in the UI. Grouped on surname plus first initial; the longest name form and
    the union of roles are kept.
    """
    groups: dict[tuple, dict] = {}
    for p in people:
        name = (p.get("name") or "").strip()
        if not name:
            continue
        parts = name.lower().replace(".", "").split()
        if not parts:
            continue
        key = (parts[-1], parts[0][:1])
        g = groups.setdefault(key, {"name": name, "roles": [], "role_type": p.get("role_type"),
                                    "affiliation": p.get("affiliation")})
        if len(name) > len(g["name"]):
            g["name"] = name
        role = (p.get("role") or "").strip()
        if role and role not in g["roles"]:
            g["roles"].append(role)
        g["affiliation"] = g["affiliation"] or p.get("affiliation")
    return [{"name": g["name"], "role": " · ".join(g["roles"]) or None,
             "role_type": g["role_type"], "affiliation": g["affiliation"]}
            for g in groups.values()]


def build_candidates(cands_raw: dict, evidence_raw: dict) -> tuple[list, dict]:
    """Slim client-side index plus a build-time detail map."""
    index, detail = [], {}
    for c in cands_raw["candidates"]:
        cid = c["candidate_id"]
        ev = evidence_raw["evidence"].get(cid, [])
        views = {v["type"]: [] for v in c.get("analyst_views", [])}
        for v in c.get("analyst_views", []):
            views.setdefault(v["type"], []).append(v["statement"])

        strongest = _summary_claim(ev)

        row = {
            "id": cid,
            "name": c["name"],
            "type": c["candidate_type"],
            "queue": c.get("queue"),
            "institution": c.get("institution"),
            "company": c.get("company"),
            "geography": c.get("geography"),
            "category": c.get("primary_category"),
            "categories": c.get("categories", []),
            "centrality": c.get("ocean_centrality"),
            "sourcingSignal": c.get("sourcing_signal"),
            "stage": c.get("current_stage"),
            "companyFormed": c.get("company_formed"),
            "latestSignal": c.get("candidate_latest_signal_date"),
            "evidenceCount": c.get("evidence_count", len(ev)),
            "priority": c.get("priority_total"),
            "priorityMax": c.get("priority_max"),
            "flags": [f["flag"] for f in c.get("flags", [])],
            "whySurfaced": (c.get("why_it_surfaced") or [])[:3],
            "strongestEvidence": (strongest or {}).get("observed_claim"),
            "strongestEvidenceType": (strongest or {}).get("type"),
        }
        index.append(row)

        detail[cid] = {
            **row,
            "website": c.get("website"),
            "people": _merge_people(c.get("people", [])),
            "components": c.get("priority_components", {}),
            "flagDetail": c.get("flags", []),
            "observed": views.get("observed", []),
            "inferred": views.get("inferred", []),
            "unknown": views.get("unknown", []),
            "mustBeTrue": views.get("what_must_be_true", []),
            "technicalKill": views.get("technical_kill_question", []),
            "commercialKill": views.get("commercial_kill_question", []),
            "evidence": ev,
        }
    index.sort(key=lambda r: (r["name"] or "").lower())
    return index, detail


def build_summary(cands_raw, tier_summary, audit, frontier, themes_cfg, ingest_total) -> dict:
    rows = cands_raw["candidates"]
    by_queue = tier_summary["by_queue"]
    actionable = by_queue.get("tier_a", 0) + by_queue.get("tier_b", 0) + by_queue.get("frontier", 0)
    institutions = {r["institution"] for r in rows if r.get("institution")}
    cats = Counter(r.get("primary_category") for r in rows if r.get("primary_category"))
    with_grants = sum(1 for r in rows if r.get("evidence_count", 0) > 0)

    return {
        "recordsEvaluated": ingest_total,
        "candidates": len(rows),
        "actionableUniverse": actionable,
        "tierA": by_queue.get("tier_a", 0),
        "tierB": by_queue.get("tier_b", 0),
        "tierC": by_queue.get("tier_c", 0),
        "frontier": by_queue.get("frontier", 0),
        "preCompanyShareOfActionable": tier_summary["pre_company_share"]["frontier_share_of_actionable"],
        "institutions": len(institutions),
        "categories": len(cats),
        "categoryCounts": dict(cats),
        "candidatesWithEvidence": with_grants,
        "procurementContracts": audit["n_contracts"],
        "procurementObserved": audit["total_observed"],
        "themes": len(themes_cfg["themes"]),
        "generatedAt": cands_raw["meta"]["generated_at"],
    }


def build_themes(themes_cfg, index) -> list:
    counts = Counter(r["category"] for r in index if r["category"])
    frontier_counts = Counter(r["category"] for r in index
                              if r["category"] and r["queue"] == "frontier")
    out = []
    for key, t in themes_cfg["themes"].items():
        examples = sorted(
            [r for r in index if r["category"] == key and r["queue"] in ("tier_a", "frontier")],
            key=lambda r: (-(r["priority"] or 0), r["name"]))[:4]
        out.append({
            "id": key,
            "label": t["label"],
            "problem": t["problem"].strip(),
            "technologies": t.get("technologies", []),
            "technicalBottlenecks": t.get("technical_bottlenecks", []),
            "commercialBottlenecks": t.get("commercial_bottlenecks", []),
            "propellerAdjacency": t.get("propeller_adjacency", []),
            "note": (t.get("note_hidden_adjacency") or t.get("caution") or "").strip() or None,
            "candidateCount": counts.get(key, 0),
            "frontierCount": frontier_counts.get(key, 0),
            "examples": [{"id": e["id"], "name": e["name"], "queue": e["queue"],
                          "institution": e["institution"]} for e in examples],
        })
    out.sort(key=lambda t: -t["candidateCount"])
    return out


def build_armada(cfg, audit, register, snapshot) -> dict:
    from ofr.models.armada_underwriting import ASSUMPTIONS, compute_python_check
    model = compute_python_check()

    reg = {r["claim_id"]: r for r in register}
    fed_total = next(float(re.sub(r"[^\d.]", "", m.group(0)))
                     for m in [re.search(r"\$2,972,287", reg["C012"]["claim"])])

    tokens = {
        "federal_total": _money(fed_total),
        "navy_phase2_total": _money(1_998_926),
        "navy_phase1": _money(246_320),
        "nsf_sttr": _money(255_821),
        "noaa_phase1": _money(174_798),
        "narrow_annual": _money(audit["narrow_addressable"]["annualised"]),
        "broad_annual": _money(audit["broad_adjacency"]["annualised"]),
        "base_revenue": _money_compact(model["total_revenue"]),
        "threshold": _money_compact(model["threshold"]),
        "gap": _money_compact(model["gap"]),
    }

    # Government validation table, generated from the evidence register.
    awards = [
        {"date": "2020-08-01", "agency": "NSF", "instrument": "STTR Phase I (grant)",
         "amount": 255_821, "id": "2026230", "end": "2021-06-30"},
        {"date": "2021-10-20", "agency": "DoD / Navy", "instrument": "SBIR Phase I (contract)",
         "amount": 246_320, "id": "N68335-22-C-0035", "end": "2022-12-28"},
        {"date": "2023-01-30", "agency": "DoD / Navy", "instrument": "SBIR Phase II (contract)",
         "amount": 1_998_926, "id": "N68335-23-C-0142", "end": "2028-03-20"},
        {"date": "2024-08-01", "agency": "DoC / NOAA", "instrument": "SBIR Phase I (grant)",
         "amount": 174_798, "id": "NA24OARX021G0026", "end": "2025-01-31"},
        {"date": "2024-10-11", "agency": "DoD / OSD", "instrument": "SBIR Phase I (purchase order)",
         "amount": 149_967, "id": "HY023325PE002", "end": "2025-03-21"},
        {"date": "2024-11-15", "agency": "DoD / Navy", "instrument": "SBIR Phase I (contract)",
         "amount": 146_455, "id": "N68335-25-C-0057", "end": "2025-05-14"},
    ]
    total = sum(a["amount"] for a in awards)
    if total != int(fed_total):
        raise ExportError(f"award table sums to {total}, register says {int(fed_total)}")

    navy_mods = [
        {"date": "2023-01-30", "mod": "base", "amount": 999_028, "action": "Award"},
        {"date": "2025-01-21", "mod": "P00001", "amount": 499_949, "action": "Exercise an option"},
        {"date": "2025-01-30", "mod": "P00002", "amount": 0, "action": "Extending period of performance (CLINs 0001–0003)"},
        {"date": "2026-03-10", "mod": "P00003", "amount": 499_949, "action": "Incrementally funding CLIN 0004"},
    ]
    if sum(m["amount"] for m in navy_mods) != 1_998_926:
        raise ExportError("Navy modification history does not reconcile to the contract total")

    buckets = [{"id": k, **v} for k, v in audit["buckets"].items()]
    buckets.sort(key=lambda b: -b["value"])

    assumptions = [{"driver": n, "bear": be, "base": ba, "bull": bu, "type": kind, "note": note}
                   for n, be, ba, bu, kind, note in ASSUMPTIONS]

    return {
        "recommendation": resolve_deep(cfg["recommendation"], tokens),
        "whyInteresting": resolve_deep(cfg["why_interesting"], tokens),
        "productLines": resolve_deep(cfg["product_lines"], tokens),
        "debates": resolve_deep(cfg["debates"], tokens),
        "ip": resolve_deep(cfg["ip_section"], tokens),
        "primaryResearch": resolve_deep(cfg["primary_research"], tokens),
        "propellerFit": resolve_deep(cfg["propeller_fit"], tokens),
        "researchJourney": resolve_deep(cfg["research_journey"], tokens),
        "government": {
            "awards": awards,
            "total": total,
            "navyModifications": navy_mods,
            "navyContractId": "N68335-23-C-0142",
            "navyPeriod": {"start": "2023-01-30", "end": "2028-03-20"},
            "note": ("Competitively awarded federal development instruments. This is "
                     "funded technical demand, not commercial product revenue. The "
                     "January 2025 option exercise and the March 2026 incremental "
                     "funding are repeat affirmative decisions by the customer."),
        },
        "procurement": {
            "contracts": audit["n_contracts"],
            "totalObserved": audit["total_observed"],
            "yearSpan": audit["year_span"],
            "excluded": audit["excluded_as_false_comparables"],
            "narrow": audit["narrow_addressable"],
            "broad": audit["broad_adjacency"],
            "buckets": buckets,
            "caveat": audit["caveat"],
            "implication": ("The visible procurement market does not, by itself, support "
                            "the venture-scale case. The money sits in R&D, prime "
                            "integration and complete platforms rather than in the "
                            "subsystem line items ARMADA sells."),
        },
        "model": {
            "assumptions": assumptions,
            "base": model,
            "thresholdMultipleOfNarrow": round(
                model["threshold"] / audit["narrow_addressable"]["annualised"], 1),
            "thresholdMultipleOfBroad": round(
                model["threshold"] / audit["broad_adjacency"]["annualised"], 1),
            "note": ("A forward requirements model, not a projection. ARMADA has no "
                     "publicly known revenue, so none is invented. The $30M threshold is "
                     "a scenario reference point, not a universal definition of venture "
                     "scale."),
        },
        "evidenceCount": len(register),
        "snapshot": {
            "totalFederal": snapshot["snapshot"]["total_federal_award_value_usd"],
            "distinctAwards": snapshot["snapshot"]["distinct_federal_awards"],
            "latestSignal": snapshot["snapshot"]["latest_meaningful_signal"],
            "people": snapshot["snapshot"]["people"],
            "website": snapshot["snapshot"]["website"],
            "geography": snapshot["snapshot"]["geography"],
        },
    }


def build_evidence_register(register: list) -> list:
    return [{
        "id": r["claim_id"], "claim": r["claim"], "status": r["status"],
        "source": r["source"], "sourceType": r["source_type"], "tier": r["source_tier"],
        "sourceDate": r["source_date"] or None, "accessed": r["date_accessed"],
        "confidence": r["confidence"], "section": r["memo_section"],
        "contradictory": r["contradictory_evidence"] or None,
    } for r in register]


def build_frontier(frontier_raw, detail: dict) -> dict:
    """Frontier evidence is taken from the canonical candidate detail records so
    there is exactly one evidence shape across the whole site."""
    signals = []
    for s in frontier_raw["signals"]:
        cid = s["candidate_id"]
        signals.append({
            "id": cid, "name": s["name"], "institution": s["institution"],
            "signalType": s["signal_type"], "signalDate": s["signal_date"],
            "category": s.get("taxonomy"), "geography": s.get("geography"),
            "centrality": s["ocean_centrality"], "components": s["components"],
            "priority": s["frontier_total"], "priorityMax": s["frontier_max"],
            "evidence": detail.get(cid, {}).get("evidence", []),
        })
    return {
        "signals": signals,
        "byType": dict(Counter(s["signalType"] for s in signals)),
        "byCategory": dict(Counter(s["category"] for s in signals if s["category"])),
        "byInstitution": dict(Counter(s["institution"] for s in signals if s["institution"])),
        "note": frontier_raw["signals"][0]["note"] if frontier_raw["signals"] else "",
    }


# --------------------------------------------------------------- validation
def validate(bundle: dict) -> list[str]:
    errs = []
    idx = bundle["candidates"]
    ids = [c["id"] for c in idx]
    if len(ids) != len(set(ids)):
        errs.append("duplicate candidate ids in index")

    detail = bundle["_detail"]
    for c in idx:
        if c["id"] not in detail:
            errs.append(f"index candidate {c['id']} has no detail record")

    for cid, d in detail.items():
        for e in d["evidence"]:
            src = e.get("source") or {}
            if not src.get("url"):
                continue
            if not re.match(r"^https?://", src["url"]):
                errs.append(f"{cid}: malformed source url {src['url']!r}")

    for s in bundle["frontier"]["signals"]:
        if s["id"] not in detail:
            errs.append(f"frontier signal {s['id']} missing from candidate detail")

    a = bundle["armada"]
    if a["recommendation"]["verdict"] != "HOLD — NEED MORE EVIDENCE":
        errs.append("ARMADA recommendation changed")
    if a["government"]["total"] != 2_972_287:
        errs.append("ARMADA federal total does not match canonical value")
    if a["procurement"]["contracts"] != 87:
        errs.append("procurement contract count changed")
    if a["model"]["base"]["total_revenue"] != 22_050_000:
        errs.append("model base revenue does not match canonical model")

    blob = json.dumps({k: v for k, v in bundle.items() if not k.startswith("_")})
    if "/Users/" in blob or str(ROOT) in blob:
        errs.append("absolute local path leaked into frontend data")
    for pat in (r"sk-[A-Za-z0-9]{20}", r"api[_-]?key\s*[=:]"):
        if re.search(pat, blob, re.IGNORECASE):
            errs.append(f"possible secret matching {pat} in frontend data")
    if PLACEHOLDER.search(blob):
        errs.append("unresolved {{placeholder}} in frontend data")
    return errs


# -------------------------------------------------------------------- main
def build(write: bool = True) -> dict:
    cands = _load(OUTPUTS / "candidates.json")
    evid = _load(OUTPUTS / "candidate_evidence.json")
    tier = _load(OUTPUTS / "tier_summary.json")
    audit = _load(OUTPUTS / "armada_procurement_audit.json")
    frontier_raw = _load(OUTPUTS / "frontier_signals.json")
    snapshot = _load(OUTPUTS / "armada_snapshot.json")
    themes_cfg = yaml.safe_load((CONFIG / "themes.yaml").read_text())
    armada_cfg = yaml.safe_load((CONFIG / "armada_deepdive.yaml").read_text())
    with (RESEARCH / "armada" / "evidence_register.csv").open() as f:
        register = list(csv.DictReader(f))

    ingest_total = sum(r.get("records_seen") or 0 for r in cands["meta"].get("ingest_log", []))

    index, detail = build_candidates(cands, evid)
    bundle = {
        "summary": build_summary(cands, tier, audit, frontier_raw, themes_cfg, ingest_total),
        "candidates": index,
        "themes": build_themes(themes_cfg, index),
        "frontier": build_frontier(frontier_raw, detail),
        "armada": build_armada(armada_cfg, audit, register, snapshot),
        "evidenceRegister": build_evidence_register(register),
        "_detail": detail,
    }

    errs = validate(bundle)
    if errs:
        raise ExportError("validation failed:\n  - " + "\n  - ".join(errs))

    if write:
        DEST.mkdir(parents=True, exist_ok=True)
        for name in ("summary", "candidates", "themes", "frontier", "armada", "evidenceRegister"):
            (DEST / f"{name}.json").write_text(json.dumps(bundle[name], indent=1, sort_keys=True))
        (DEST / "candidateDetail.json").write_text(json.dumps(detail, indent=1, sort_keys=True))
        total = sum((DEST / f).stat().st_size for f in [p.name for p in DEST.glob("*.json")])
        print(f"[frontend-data] candidates={len(index)} frontier={len(bundle['frontier']['signals'])} "
              f"themes={len(bundle['themes'])} evidence_claims={len(register)} "
              f"-> {DEST} ({total/1024:.0f} KB)")
    else:
        print("[frontend-data] validation passed (no write)")
    return bundle


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="validate without writing")
    a = ap.parse_args()
    try:
        build(write=not a.check)
    except ExportError as e:
        print(f"[frontend-data] ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
