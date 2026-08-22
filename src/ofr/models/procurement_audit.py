"""Bottom-up procurement audit for the ARMADA case (Phase 3D).

Classifies the maritime-autonomy contracts already in the database into
spending buckets, removes false comparables transparently, and derives a
narrow-addressable and broad-adjacency view.

DELIBERATELY NOT a TAM. Every figure is *observed federal contract value in a
keyword-derived sample*. It is evidence that budgets and buying behaviour
exist, and nothing more. The sample is not exhaustive and excludes classified
and non-federal spending entirely.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ofr import db

# --- classification rules, applied in order -------------------------------
# Each rule states WHY a contract lands in a bucket, so exclusions are auditable.
RULES = [
    ("excluded_facilities", r"DESIGN-BUILD|BUILDING \d|FACILITY CONSTRUCTION",
     "Military construction. A building is not an addressable UUV market."),
    ("excluded_counter_uuv", r"COUNTERING UNMANNED",
     "Counter-UUV mission, i.e. defeating vehicles rather than buying them."),
    ("services_support", r"SUPPORT SERVICES|TROUBLESHOOTING|MAINTENANCE, REPAIR|"
                         r"OPERATIONS AND MAINTENANCE|SCIENTIFIC, TECHNICAL|"
                         r"NON-PERSONAL SERVICE|EXPERT ANNOTATION|OPERATIONS CENTER|"
                         r"INDEPENDENT EVALUATION|EMPLOYMENT STUDY|TRAINING DEMONSTRATION",
     "Services, sustainment or evaluation labour, not hardware procurement."),
    ("integration_prime", r"INTEGRATION SERVICES|INCREMENTAL UPGRADES|BLOCK UPGRAD|"
                          r"BUILD&INTEGRATE|MISSION SUPPORT EQUIPMENT",
     "Prime/system-integration work; a subsystem vendor would sell into this, not win it."),
    ("rnd_program", r"HUNTER PROGRAM|INVESTIGATE MATERIALS|SEEKS TO DEVELOP|"
                    r"INNOVATIVE SIMULTANEOUS LOCALIZATION|SIMULATION|PROTOTYPE|"
                    r"DEVELOPMENT, INTEGRATION, TEST|DEVELOPMENT AND DEMONSTRATION|"
                    r"CAPABILITY DEMONSTRATION|OPERATIONAL DEMONSTRATION|"
                    r"TECHNOLOGY IMPROVEMENTS|SENSOR PACKAGE DEVELOPMENT",
     "Funded R&D. Relevant as demand signal; not a repeatable product line item."),
    ("launch_recovery", r"LAUNCH",
     "Launch-and-recovery hardware — adjacent to, but not, propulsion or payload."),
    ("payload_deployment", r"PAYLOAD|DEPLOYABLE|IGNITER",
     "Payload carriage or deployment hardware — the EPADS-relevant slice."),
    ("sensors_payload_dev", r"SENSOR SYSTEM|SENSOR PACKAGE|MAPPING|CAMERA|PROBE|"
                            r"ACOUSTIC COMMUNICATION|TACTICAL COM",
     "Sensor or comms payload procurement — what an EPADS pod would carry."),
    ("components_spares", r"SPARE|HARDWARE|CABLE|RECO|MICRO|PARTS PURCHASE|"
                          r"SUPPORT PACK|TRAINE|KITS, BATTER",
     "Component, spares and consumable hardware — the propulsion-subsystem slice."),
    ("platform_purchase", r"AUTONOMOUS UNDERWATER VEHICLE|UNMANNED UNDERWATER VEHICLE|"
                          r"UUV|AUV|SEAGLIDER|IVER3|SABERTOOTH|JAIABOT|SPEARTOOTH|REMUS",
     "Purchase or lease of a complete vehicle."),
]

# Buckets a propulsion/payload subsystem vendor could plausibly sell into.
NARROW_BUCKETS = {"components_spares", "payload_deployment"}
BROAD_EXTRA = {"platform_purchase", "sensors_payload_dev", "launch_recovery"}

# ANALYST ASSUMPTION: share of a complete vehicle's contract value attributable
# to the propulsion/control subsystem. Not sourced; used only to show what the
# adjacency case implies. Varied in the scenario model.
PROPULSION_SHARE_OF_PLATFORM = 0.10


def classify(description: str) -> tuple[str, str]:
    d = (description or "").upper()
    for bucket, pattern, why in RULES:
        if re.search(pattern, d):
            return bucket, why
    return "unclassified", "No rule matched; retained for manual review."


def audit(conn, theme: str = "maritime_autonomy") -> dict:
    rows = conn.execute(
        """SELECT award_id, recipient, awarding_agency, awarding_sub_agency,
                  amount, start_date, description
           FROM procurement WHERE theme=?""", (theme,)).fetchall()

    records, buckets = [], defaultdict(lambda: {"n": 0, "value": 0.0, "why": ""})
    for r in rows:
        bucket, why = classify(r["description"])
        amt = r["amount"] or 0.0
        records.append({
            "award_id": r["award_id"], "recipient": r["recipient"],
            "agency": r["awarding_sub_agency"] or r["awarding_agency"],
            "amount": amt, "start_date": r["start_date"], "bucket": bucket,
            "reason": why, "description": (r["description"] or "")[:160],
        })
        buckets[bucket]["n"] += 1
        buckets[bucket]["value"] += amt
        buckets[bucket]["why"] = why

    total_all = sum(r["amount"] for r in records)
    excluded = {k: v for k, v in buckets.items() if k.startswith("excluded_")}
    excluded_value = sum(v["value"] for v in excluded.values())

    years = sorted({r["start_date"][:4] for r in records if r["start_date"]})
    span = max(1, int(years[-1]) - int(years[0]) + 1) if years else 1

    narrow = sum(buckets[b]["value"] for b in NARROW_BUCKETS if b in buckets)
    narrow_n = sum(buckets[b]["n"] for b in NARROW_BUCKETS if b in buckets)
    platform_value = buckets.get("platform_purchase", {}).get("value", 0.0)
    broad = narrow + sum(buckets[b]["value"] for b in BROAD_EXTRA if b in buckets)
    broad_n = narrow_n + sum(buckets[b]["n"] for b in BROAD_EXTRA if b in buckets)

    return {
        "theme": theme,
        "caveat": ("Observed federal contract value in a keyword-derived sample. "
                   "NOT a market size estimate, NOT a TAM. Excludes classified "
                   "programmes, non-federal and non-US buyers entirely."),
        "n_contracts": len(records),
        "total_observed": round(total_all, 2),
        "year_span": {"first": years[0] if years else None,
                      "last": years[-1] if years else None, "years": span},
        "buckets": {k: {"n": v["n"], "value": round(v["value"], 2),
                        "annualised": round(v["value"] / span, 2), "reason": v["why"]}
                    for k, v in sorted(buckets.items(), key=lambda x: -x[1]["value"])},
        "excluded_as_false_comparables": {
            "n": sum(v["n"] for v in excluded.values()),
            "value": round(excluded_value, 2),
            "buckets": list(excluded)},
        "narrow_addressable": {
            "definition": ("Components/spares plus payload-deployment hardware — "
                           "line items a propulsion or payload subsystem vendor "
                           "could plausibly win directly."),
            "n": narrow_n, "value": round(narrow, 2),
            "annualised": round(narrow / span, 2)},
        "broad_adjacency": {
            "definition": ("Narrow plus complete-vehicle purchases, sensor/comms "
                           "payloads and launch-and-recovery — reachable only by "
                           "selling through OEMs or expanding scope."),
            "n": broad_n, "value": round(broad, 2),
            "annualised": round(broad / span, 2)},
        "platform_embedded_case": {
            "assumption": (f"ANALYST ASSUMPTION (not sourced): propulsion/control is "
                           f"{PROPULSION_SHARE_OF_PLATFORM:.0%} of complete-vehicle "
                           f"contract value."),
            "platform_value_observed": round(platform_value, 2),
            "implied_subsystem_value": round(platform_value * PROPULSION_SHARE_OF_PLATFORM, 2),
            "implied_annualised": round(platform_value * PROPULSION_SHARE_OF_PLATFORM / span, 2)},
        "records": sorted(records, key=lambda r: -r["amount"]),
    }


if __name__ == "__main__":
    conn = db.connect()
    out = audit(conn)
    dest = db.ROOT / "outputs" / "armada_procurement_audit.json"
    dest.write_text(json.dumps(out, indent=1))
    print(f"contracts={out['n_contracts']} total=${out['total_observed']:,.0f} "
          f"span={out['year_span']['first']}-{out['year_span']['last']}")
    print("\nbuckets:")
    for k, v in out["buckets"].items():
        print(f"  {k:22s} n={v['n']:3d}  ${v['value']:>13,.0f}  ann=${v['annualised']:>11,.0f}")
    print(f"\nexcluded as false comparables: n={out['excluded_as_false_comparables']['n']} "
          f"${out['excluded_as_false_comparables']['value']:,.0f}")
    print(f"narrow addressable : n={out['narrow_addressable']['n']:3d} "
          f"${out['narrow_addressable']['value']:,.0f} (ann ${out['narrow_addressable']['annualised']:,.0f})")
    print(f"broad adjacency    : n={out['broad_adjacency']['n']:3d} "
          f"${out['broad_adjacency']['value']:,.0f} (ann ${out['broad_adjacency']['annualised']:,.0f})")
    p = out["platform_embedded_case"]
    print(f"platform-embedded  : ${p['implied_subsystem_value']:,.0f} "
          f"(ann ${p['implied_annualised']:,.0f}) — {p['assumption']}")
