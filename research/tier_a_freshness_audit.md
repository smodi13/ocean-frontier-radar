# Tier-A Freshness Audit — Phase 2.5 (in progress)

**Prepared:** 2026-08-21 · All sources accessed 2026-08-21.
**Purpose:** prevent stale structured datasets from determining the shortlist. The SBIR bulk file ends in 2023; this audit checks every Phase 2 Tier-A candidate against current public sources.

> **Correction to Phase 2, recorded here rather than by editing that report.** Phase 2 §9 described ARMADA as backed by an "NSF STTR $255,821" with "roughly $290K raised". That understated the company materially. The Navy Phase II award **was already in our database** and I failed to surface it in the report narrative. That was a reporting failure, not only a data gap.

---

## 1. ARMADA Marine Robotics — materially understated

### Complete verified federal award history

Sources: SBIR bulk file (through 2023) and USAspending API (current), both accessed 2026-08-21.

| Start | Agency / Branch | Instrument | Amount | Award ID | Period ends |
|---|---|---|---:|---|---|
| 2020-08-01 | NSF | STTR Phase I (grant) | $255,821 | 2026230 | 2021-06-30 |
| 2021-10-20 | DoD / Navy | SBIR Phase I (contract) | $246,320 | N6833522C0035 | 2022-12-28 |
| 2023-01-30 | DoD / Navy | SBIR Phase II (contract) | **$1,998,926** | N6833523C0142 | **2028-03-20** |
| 2024-08-01 | DoC / NOAA | SBIR Phase I (grant) | $174,798 | NA24OARX021G0026 | 2025-01-31 |
| 2024-10-11 | DoD / Office of the Secretary of Defense | SBIR Phase I (purchase order) | $149,967 | HY023325PE002 | 2025-03-21 |
| 2024-11-15 | DoD / Navy | SBIR Phase I (contract) | $146,455 | N6833525C0057 | 2025-05-14 |
| | | **Total** | **$2,972,287** | | |

**Instrument classification, stated deliberately.** None of this is revenue. Five are competitively awarded SBIR/STTR development instruments; one (2026230) is an NSF grant. However, **three separate Phase I awards from three different agencies inside four months (Aug/Oct/Nov 2024) is defensible customer-validation evidence** — three independent technical review panels funded the company in one budget cycle.

### What changed versus Phase 2

| Fact | Phase 2 said | Verified now |
|---|---|---|
| Federal funding | $255,821 (NSF STTR) | **$2,972,287** across 4 agencies |
| Navy Phase II | Not surfaced | $1,998,926, **value doubled** from the $999,028 in the 2023 bulk record |
| Navy Phase II end date | Bulk file said 2025-01-31 | **2028-03-20** — a five-year runway |
| Most recent award | 2020 STTR implied | **2024-11-15** |
| Product lines | Asymmetric propulsion only | **Three**: propulsion; EPADS payload deployment; persistent sensing platform |
| CEO | not established | **Jeff Kaeli** (joint PhD, MIT/WHOI) |
| Stage | "pre-seed, ~$290K raised" | Pre-seed equity, but ~$3.0M non-dilutive and a contract to 2028 |

### Products and current maturity

ARMADA's own site describes "modular propulsion units **and** payload delivery systems". Three distinct threads are now visible:

1. **Asymmetric Propulsion** — the WHOI-licensed IP, NSF STTR 2020.
2. **EPADS (External Payload Deployment System)** — Navy SBIR Phase I→II. The Navy "identified a need for External Payload Deployment Systems for cylindrical UUVs between 5 and 21 inches in diameter"; Phase I settled on an A-size (4.875" × 36") payload body delivering a ~5 kg module. **This is where the money is.**
3. **Persistent sensing platform** — the NOAA 2024 award describes combining "innovative propulsion and ballast technologies to create a new class of uncrewed underwater sensing platform with both mobility and persistence", selectively riding ocean currents as "a constellation of platforms". The abstract opens: *"ARMADA has a bold plan to become the SpaceX of the sea."*

**Team (from armadamarinerobotics.com):** Jeff Kaeli (CEO, Founder — joint PhD MIT/WHOI); Robin Littlefield (Lead Engineer, Founder — WHOI senior engineer); Philip "Rusty" Warren (Lead Director, Founder — Harvard, US Army combat veteran, PhD, three decades federal/contractor leadership, board member of several blue-tech startups).

**Unknown:** equity financing since the Mar 2025 accelerator round; headcount (aggregator figure of ~8 is tier-3 and not ingested); any commercial, non-government customer.

---

## 2. ARMADA patent review

Technical/IP diligence only. **This is not a freedom-to-operate analysis and no legal opinion is offered.** WHOI's licensing announcement remains the primary source for the existence and exclusivity of the licences.

### US 9,873,499 B2 — "Asymmetric propulsion and maneuvering system"
- **Assignee:** Woods Hole Oceanographic Institution · **Status:** active, anticipated expiry 2035-04-02
- **Inventors:** Thomas Austin, Michael Purcell, Frederic Jaffre, Jeffrey Kaeli, Ben Allen, Robin Littlefield
- **Priority** 2014-04-04 · **Filed** 2015-04-02 · **Granted** 2018-01-23
- **Independent claim 1 (verbatim):** *"A marine propulsion system comprising: a. a motor; b. a motor driven propeller having a central hub with an axis of rotation with at least one thrusting surface which revolves around the axis of rotation; and, c. a controlling mechanism in communication with the motor; wherein the controlling mechanism is capable of regulating the motor speed to produce differential velocity within a single revolution of the propeller across sequential rotations and generate a turning moment."*
- **What is actually protected:** the *control method* — modulating motor speed within a single revolution to generate a turning moment — not a propeller shape. Note claim 1 says "at least one thrusting surface", so it is **not limited to single-bladed propellers**; the scope is broader than the company's public framing suggests.
- **Prior art of note:** US 2,371,160 (1945, single-blade propeller); US 3,312,286 (1967, surface propeller); **US 7,841,831 B2 (2010, "asymmetrically changing rotating blade shape (ACRBS) propeller")**; US 2016/0083077 (single blade, variable pitch). Single-blade marine propulsion is old; the differentiation rests on intra-revolution velocity control.
- **Obvious limitation:** claim 1 requires regulating *motor speed*. An implementation achieving the same steering effect by another means — cyclic pitch, for instance — may sit outside this claim.

### US 11,990,857 B2 — "Rotational feedback control system and method"
- **Assignee:** Woods Hole Oceanographic Institution · **Status:** active, expiry 2041-05-24
- **Inventors:** Jeffrey Kaeli, Frederic Jaffre
- **Priority** 2019-05-29 (prov. 62/853,775) · **Filed** 2020-05-27 · **Granted** 2024-05-21 · PCT/US2020/034620
- **Abstract:** a system of "a rotating element, a sensor and a digital controller… capable of monitoring, setting, and adjusting the inter-rotational angular velocity within a single revolution of the rotating element."
- **Cites** US 9,873,499. This is the **enabling sensing/control layer** that makes the first patent practical, and it is the longer-lived asset — 2041 versus 2035.

### The gap that matters: EPADS IP

The WHOI announcement of **7 January 2025** licensed *only* the two propulsion patents. The EPADS work traces to a separate WHOI patent:

**US 10,112,686 B2 — "System for the deployment of marine payloads"** (from US 2016/0221655 A1). Assignee WHOI; inventors Austin, Purcell, **Littlefield**, Jaffre, Packard, McDonald. Priority 2015-01-30, filed 2016-01-29, granted 2018-10-30, expiry 2036-01-29. Claim 1 covers a carrier with a deployment chamber holding payloads by **vacuum force** without a mechanical restraint, with passive buoyancy compensation.

> **Unknown, and material:** no public source reviewed states that ARMADA holds a licence to US 10,112,686. ARMADA's largest programme by value (the ~$2.0M Navy EPADS contract) rests on technology whose underlying patent is assigned to WHOI and **is not named in the licence announcement**. This is the single most important open question in the ARMADA case.

**What the patent review adds overall:** it converts "two patents" from a headline into an assessable position — a broad-ish control claim with real prior art behind it, a longer-lived enabling patent to 2041, WHOI ownership with exclusivity via licence (terms not public: field of use, sublicensing, milestones, termination all unknown), and a disclosed gap around the EPADS IP.

---

## 3. 3newable — evidence timeline

| Date | Event | Source |
|---|---|---|
| 2020-06-29 | DOE STTR Phase I, $205,713, contract DE-SC0020921. Research institution: **WHOI** | SBIR bulk |
| 2021-08-23 | DOE STTR Phase II, $1,099,971 (same contract line), RI WHOI | SBIR bulk |
| 2022 | Project moves from OOI Pioneer New England Shelf Array to the **Coastal Endurance Array** | OOI |
| 2023 autumn | **First field deployment** | OOI |
| 2023-08-28 | DOE SBIR Phase II, $1,149,047 (same contract line) | SBIR bulk |
| — | Independent testing at **PNNL Marine and Coastal Research Laboratory** under DOE-sponsored TEAMER RFTS 2; outputs include imagery, quantitative biofouling mass and SEM analysis | TEAMER |
| 2025 spring | **Second deployment** at OOI buoy **CE04** | OOI |
| 2025-11-15 | DOE contract DE-SC0020921 period of performance **ends** | USAspending |
| 2025-12-04 | OOI publishes performance results and interview with CEO Julie Fouquet | OOI |
| 2025 | Company website active, copyright 2025; two product lines described | 3newable.com |

**Total verified federal funding: $2,474,731 — all on a single DOE contract line (DE-SC0020921), which ended 2025-11-15.** No awards from any other agency, and no public evidence of equity financing, a follow-on award, or a paying customer.

### What the published testing actually showed

Stated precisely, because Phase 2 overstated this:

- Laboratory capacity **up to 50 W**.
- Expected real-world yield **7–8 W time-averaged annually**.
- Most recent deployment: **net average 0.91 W over ~1.5 weeks**, with a **2.4 W peak net average over a five-minute interval**.

**Correction to Phase 2.** Phase 2 characterised this as roughly an order-of-magnitude shortfall. OOI's own framing is that the 0.91 W was achieved *"even in relatively low-energy conditions"* — i.e. it is a single measurement in benign sea states, not an annualised figure, and is therefore **not directly comparable** to the 7–8 W annual time-average. The honest statement is that public data show one low-energy-condition result well below the annual target, and that reconciling the two is exactly the technical question a diligence process should ask — not that the technology has demonstrably underperformed.

The UV illuminator is a separate product line: a retrofit module targeting biofouling on salinity-sensor conductivity cells, positioned against biocidal antifoulants such as tributyltin.

---

## 4. Remaining Tier-A cohort — federal award freshness

USAspending, accessed 2026-08-21. **Bold = material change from Phase 2.**

| Candidate | Awards found | Total | Latest award | Runs to | Assessment change |
|---|---:|---:|---|---|---|
| **Ocean Motion Technologies** | 6 | **~$7.15M** (DOE ×3, NSF ×2, NASA) | 2024-12-16 | **2027-12-15** | **Materially larger than Phase 2 knew.** Six awards across three agencies. Likely beyond early-stage framing; `emerging` signal is questionable. |
| **X-Hab 3D** | 7 | **~$3.98M** (Army, NASA ×2, USAF, DOT ×2) | 2025-09-29 | 2026-12-31 | **Very active**, but the portfolio is mostly general construction/3D-printing (Army, NASA, DOT). The marine artificial-reef thread is one strand — **ocean centrality weaker than Phase 2 assumed**. |
| **Certus Core** | 6 | **~$3.17M** (USAF ×3, SOCOM ×2, MDA) | 2025-12-29 | 2035-12-28 | **Confirms the Phase 2 §16(d) concern.** SBIR.gov firm page shows 9 employees, $4.46M total, and the largest award is a Semantic Knowledge Graph for **Air Force** data. **Ocean centrality overstated — demote.** |
| **Nexuma L.L.C.** | 2 | ~$1.45M (NSF) | 2026-07-01 | **2028-06-30** | **Currently funded**, Phase II runs two more years. Position holds or improves. |
| **Grow Oyster Reefs** | 2 | ~$1.51M (NSF) | 2025-09-15 | 2027-08-31 | Currently funded through 2027. Position holds. |
| **Designer Ecosystems** | 1 in USAspending | $301,769 visible | 2025-04-15 | 2026-03-31 | NSF Phase II (2604863, $1,242,694) present via NSF API but not yet in USAspending. Position holds. |
| **Juice Robotics** | **0** | — | — | — | **No federal awards at all.** Its evidence base is university licences plus one undisclosed VC round — a different, thinner evidence profile than the rest of Tier A. |

### Candidates whose view changed materially

1. **ARMADA** — up. ~$3.0M, four agencies, Navy contract to 2028, three product lines.
2. **Certus Core** — down. A defence data-platform company; ocean relevance is incidental.
3. **Ocean Motion Technologies** — reclassify. ~$7.15M across six awards is past the stage this system targets.
4. **X-Hab 3D** — qualify. Genuinely active, but predominantly non-marine.
5. **Juice Robotics** — qualify. Strong story, but zero federal corroboration; the case rests on one university announcement.

---

## 5. Bounded freshness repair applied

The audit proved the staleness was fixable, so a **bounded** repair was run — not a sourcing expansion. `src/ofr/ingestion/refresh.py` re-queries USAspending **by company name for a bounded cohort only** (the 121 candidates scoring ≥11) and adds awards we did not already hold. It never creates candidates, so it cannot widen the universe.

**Result: 633 new evidence rows across 121 candidates.**

Two data-integrity issues surfaced and were fixed:

1. **Double counting.** The same award arrives from two sources with different punctuation and different values — the SBIR bulk file records the Navy EPADS contract as `N68335-23-C-0142` at its original $999,028; USAspending records `N6833523C0142` at its current $1,998,926. Summing both reported ARMADA's federal total as **$4.7M instead of $3.0M**. Award identifiers are now normalised and deduplicated, keeping the larger (current) value. After the fix, the generated totals match the hand-verified figures **exactly**: ARMADA $2,972,287, 3newable $2,474,731.
2. **Phase misclassification.** A NOAA Phase I award of $174,798 was typed as Phase II because the words "phase II" appeared elsewhere in a long abstract. Award size now overrides free text below $400K. Ten rows were reclassified.

## 6. Final tier outcome for the Phase 2 Tier-A cohort

| Phase 2 Tier-A candidate | Phase 2.5 queue | Change |
|---|---|---|
| ARMADA Marine Robotics | **Tier A** | Strengthened — $2.97M verified, funded to 2028 |
| Juice Robotics | **Tier A** | Qualified — zero federal awards; thinnest corroboration in Tier A |
| 3newable LLC | **Tier A** | Qualified — single funder, contract ended Nov 2025 |
| Certus Core, Inc. | Tier A *(machine)* | **Analyst override: excluded.** Defence data-platform business; ocean centrality overstated |
| Designer Ecosystems LLC | **Tier A** | Unchanged |
| Grow Oyster Reefs, LLC | **Tier A** | Unchanged |
| NEXUMA L.L.C. | **Tier A** | Strengthened — Phase II now runs to 2028-06-30 |
| Ocean Motion Technologies | **Tier C** | **Demoted.** ~$7.15M across six awards → `BEYOND_STAGE` |
| X-HAB 3D, INC. | **Tier A** | Qualified — ~$3.98M but mostly non-marine construction work |

**Materially changed: five of nine.** Two demoted or overridden, one strengthened, two qualified. That is the audit earning its place: relying on the Phase 2 shortlist unchecked would have carried a defence data company and a $7M-funded firm into diligence.

## 7. Status

Phase 2.5 audit complete. See `research/phase2_5_report.md` for the decision gate, `research/frontier_signals.md` for the pre-company queue, and `outputs/` for machine-readable exports.
