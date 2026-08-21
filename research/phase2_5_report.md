# Phase 2.5 — Freshness and Analyst Calibration

**Prepared:** 2026-08-21 · **Status:** complete. **Phase 3 not started, pending review.**
Baseline checkpoint: `0ee89ef`. Completion commit: **`984fb27af9efd984b95dabc188eaccf568cd40ee`** (`984fb27`).
Phase 1 and Phase 2 reports are unchanged; every correction is recorded here.

**Commit sequence preserved:** `c077851` Phase 1 research → `8a7b4dc` Phase 2 pipeline → `0ee89ef` Phase 2.5 freshness discovery → `984fb27` Phase 2.5 completion. Nothing was amended or squashed; the trail shows the system exposing its own weaknesses and being repaired rather than the findings being rewritten.

---

## Why Phase 2.5 Was Necessary

Four problems, stated plainly.

**1. Structured data staleness.** The SBIR bulk file ends in 2023. Phase 2 scored 562 candidates against a world that was two and a half years out of date, and `timing` was effectively reporting *which source found a candidate* rather than anything about the candidate.

**2. A reporting omission — the worst of the four.** ARMADA's ~$2.0M Navy Phase II award **was already in the Phase 2 database**, and the Phase 2 report still described the company as backed by a $255,821 NSF STTR. The pipeline worked; the reporting layer silently dropped material evidence. That is not a stale-data problem and I am not going to soften it: a sourcing system whose summary layer can lose the largest award it holds is not trustworthy, however good its ingestion is.

**3. False ordinal precision.** 64 candidates tied at priority 12. Beyond about rank 9 the "ranking" was alphabetical order wearing a number.

**4. Pre-company underrepresentation.** Phase 1's hand-built sample was ~39% pre-company; Phase 2's qualified universe was ~6%. The project's core thesis is spotting opportunities *before* obvious company formation, and the pipeline had largely stopped doing it.

---

## ARMADA Freshness Correction

| Fact | Phase 2 said | Verified 2026-08-21 |
|---|---|---|
| Federal funding | $255,821 (NSF STTR) | **$2,972,287** across four agencies |
| Navy Phase II | not surfaced | **$1,998,926** — value doubled from the $999,028 in the 2023 bulk record |
| Navy Phase II end | bulk file: 2025-01-31 | **2028-03-20** |
| Most recent award | 2020 implied | **2024-11-15** |
| Product lines | propulsion only | **three** — propulsion, EPADS, persistent sensing |
| CEO | not established | **Jeff Kaeli** (joint PhD, MIT/WHOI) |

**Company snapshot.** ARMADA Marine Robotics, Inc., founded 2019, East Falmouth MA. First WHOI spin-off to use WHOI's Express License program. Leadership: Jeff Kaeli (CEO, Founder — joint PhD MIT/WHOI, published in underwater perception and autonomy); Robin Littlefield (Lead Engineer, Founder — WHOI senior engineer, multiple patents); Philip "Rusty" Warren (Lead Director, Founder — Harvard, US Army combat veteran, PhD, three decades in federal labs and government contracting, board member of several blue-tech startups).

**Three distinct programmes — not one technology:**

1. **Asymmetric Propulsion.** The WHOI-licensed IP. NSF STTR Phase I, 2020. Thrust and steering from a single motor, eliminating fins.
2. **EPADS — External Payload Deployment System.** Navy SBIR Phase I→II. The Navy identified a need for payload deployment from cylindrical UUVs 5–21 inches in diameter; Phase I settled on an A-size (4.875" × 36") body delivering a ~5 kg module. **The largest programme by value.**
3. **Persistent sensing constellation.** NOAA 2024. Combines "innovative propulsion and ballast technologies to create a new class of uncrewed underwater sensing platform with both mobility and persistence", selectively riding ocean currents. The abstract opens: *"ARMADA has a bold plan to become the SpaceX of the sea."*

**Stage.** Pre-seed on equity (no financing disclosed since a March 2025 accelerator round), but ~$3.0M of non-dilutive funding and a Navy contract running to 2028. Describing it as an "NSF-STTR-backed pre-seed company" is no longer defensible.

---

## ARMADA Federal Award History

| Start | Agency / Branch | Instrument | Amount | Award ID | Period ends |
|---|---|---|---:|---|---|
| 2020-08-01 | NSF | STTR Phase I (grant) | $255,821 | 2026230 | 2021-06-30 |
| 2021-10-20 | DoD / Navy | SBIR Phase I (contract) | $246,320 | N6833522C0035 | 2022-12-28 |
| 2023-01-30 | DoD / Navy | SBIR Phase II (contract) | **$1,998,926** | N6833523C0142 | **2028-03-20** |
| 2024-08-01 | DoC / NOAA | SBIR Phase I (grant) | $174,798 | NA24OARX021G0026 | 2025-01-31 |
| 2024-10-11 | DoD / OSD | SBIR Phase I (purchase order) | $149,967 | HY023325PE002 | 2025-03-21 |
| 2024-11-15 | DoD / Navy | SBIR Phase I (contract) | $146,455 | N6833525C0057 | 2025-05-14 |
| | | **Total** | **$2,972,287** | | |

**Instrument classification, deliberately.** **None of this is revenue.** Five are competitive SBIR/STTR development instruments; one is an NSF grant. But **three Phase I awards from three different agencies inside four months (Aug/Oct/Nov 2024)** is defensible customer-validation evidence — three independent technical review panels funded the company in one budget cycle. And the Phase II *doubling in value with a period extended to 2028* is the strongest single commercial signal in the file.

The generated total in `outputs/armada_snapshot.json` matches this hand-verified figure exactly, after award-ID deduplication.

---

## ARMADA Patent / Licence Review

Technical and IP diligence only. **This is not a freedom-to-operate analysis and no legal opinion is offered.** WHOI's announcement remains the primary source for the existence and exclusivity of the licences.

### US 9,873,499 B2 — "Asymmetric propulsion and maneuvering system"
**Assignee: Woods Hole Oceanographic Institution.** Inventors: Austin, Purcell, Jaffre, Kaeli, Allen, Littlefield. Priority 2014-04-04, filed 2015-04-02, granted 2018-01-23, expiry ~2035-04-02.

Independent claim 1 (verbatim): *"A marine propulsion system comprising: a. a motor; b. a motor driven propeller having a central hub with an axis of rotation with at least one thrusting surface which revolves around the axis of rotation; and, c. a controlling mechanism in communication with the motor; wherein the controlling mechanism is capable of regulating the motor speed to produce differential velocity within a single revolution of the propeller across sequential rotations and generate a turning moment."*

**What is actually protected:** the *control method* — modulating motor speed within a single revolution to generate a turning moment — not a propeller shape. Claim 1 says "at least one thrusting surface", so it is **not limited to single-bladed propellers**; the scope is broader than the company's public framing.
**Cited prior art of note:** US 2,371,160 (1945, single-blade propeller), US 3,312,286 (1967), **US 7,841,831 B2 (2010, asymmetrically changing rotating blade shape)**. Single-blade marine propulsion is old; differentiation rests on intra-revolution velocity control.
**Obvious limitation:** claim 1 requires regulating *motor speed*. An implementation achieving the same steering effect by another means — cyclic pitch, say — may fall outside it.

### US 11,990,857 B2 — "Rotational feedback control system and method"
**Assignee: WHOI.** Inventors: Kaeli, Jaffre. Priority 2019-05-29, filed 2020-05-27, granted 2024-05-21, expiry 2041-05-24. Cites US 9,873,499.
This is the **enabling sensing/control layer** that makes the first patent practical — monitoring and adjusting inter-rotational angular velocity within a single revolution — and it is the **longer-lived asset, to 2041 versus 2035**.

### What the review adds
It converts "two patents" from a headline into an assessable position: a moderately broad control claim with real prior art behind it, a longer-lived enabling patent, and — critically — **WHOI ownership with ARMADA holding exclusive licences**. ARMADA does not own the underlying patents. Licence terms are not public: field of use, sublicensing, diligence milestones and termination are all unknown.

---

## The Unresolved EPADS IP Question

The WHOI announcement of **7 January 2025** licensed **only** US 9,873,499 and US 11,990,857.

The EPADS work traces to a separate WHOI patent: **US 10,112,686 B2 — "System for the deployment of marine payloads"** (from US 2016/0221655 A1). Assignee WHOI; inventors Austin, Purcell, **Littlefield**, Jaffre, Packard, McDonald. Priority 2015-01-30, granted 2018-10-30, expiry 2036-01-29. Claim 1 covers a carrier with a deployment chamber holding payloads by **vacuum force** without a mechanical restraint, with passive buoyancy compensation.

> **The exact question, phrased as outside-in diligence:**
> **What rights does ARMADA hold to the EPADS intellectual property supporting the Navy-funded programme?**
>
> This is **not** evidence that ARMADA lacks rights, **not** a legal conclusion, and **not** a freedom-to-operate concern stated as fact. There are several ordinary explanations — a separate unannounced licence, a Phase I/II data-rights arrangement, or independently developed IP. It is flagged because ARMADA's largest programme by value rests on technology whose underlying patent is assigned to WHOI and is not named in the only licence announcement we can find. That makes it the **primary Phase 3 diligence question**, and it is answerable with one founder conversation.

---

## 3newable Freshness Review

| Date | Event |
|---|---|
| 2020-06-29 | DOE STTR Phase I, $205,713, contract DE-SC0020921. Research institution: **WHOI** |
| 2021-08-23 | DOE STTR Phase II, $1,099,971 (same contract line) |
| 2022 | Project moves from OOI Pioneer array to the **Coastal Endurance Array** |
| 2023 autumn | **First field deployment** |
| 2023-08-28 | DOE SBIR Phase II, $1,149,047 (same contract line) |
| — | Independent testing at **PNNL Marine and Coastal Research Laboratory**, DOE-sponsored TEAMER RFTS 2; outputs include imagery, quantitative biofouling mass and SEM analysis |
| 2025 spring | **Second deployment** at OOI buoy **CE04** |
| **2025-11-15** | **DOE contract DE-SC0020921 period of performance ends** |
| 2025-12-04 | OOI publishes results and a CEO interview |
| 2025 | Website live, copyright 2025, two product lines described |

**Total verified federal funding: $2,474,731 — all on a single DOE contract line, ended 2025-11-15.** No awards from any other agency; no public evidence of equity financing or a paying customer.

### What the published testing does and does not prove

**Reported:** laboratory capacity **up to 50 W**; expected real-world yield **7–8 W time-averaged annually**; most recent deployment **net average 0.91 W over ~1.5 weeks**, with a **2.4 W peak** over a five-minute interval.

**Correction to Phase 2.** Phase 2 called this roughly an order-of-magnitude shortfall. OOI's own framing is that 0.91 W was achieved *"even in relatively low-energy conditions"*. It is therefore a **single measurement in benign sea states and is not directly comparable to an annualised target.**

- **It does prove:** the device was built, deployed twice at sea on a real ocean-observing array, instrumented, and measured — and that the team published a number rather than a claim. Independent third-party testing at a national laboratory exists.
- **It does not prove:** that the annual 7–8 W target is unreachable, nor that it is reachable. Reconciling one low-energy-condition measurement with an annual average is exactly the open technical question.

### Is 3newable actively commercializing in 2026?

**The honest answer is that public evidence does not establish it either way.** The website is live with a 2025 copyright; the most recent third-party coverage is December 2025; the sole federal contract ended November 2025. There is no 2026-dated public signal of any kind.

An expired award is **not** company failure — many companies transition to private capital precisely at that point. But continued activity cannot be assumed without evidence either. This is a material gap for a 2026 diligence case, and it is resolvable with one founder email.

---

## Tier-A Freshness Audit

Full detail in `research/tier_a_freshness_audit.md`. A bounded repair (`src/ofr/ingestion/refresh.py`) re-queried USAspending by company name for the 121 candidates scoring ≥11 — **633 new evidence rows**. It never creates candidates, so it cannot widen the universe.

**Five of the nine Phase 2 Tier-A candidates changed materially:**

| Candidate | Outcome | Why |
|---|---|---|
| **ARMADA** | Strengthened | $2.97M verified, four agencies, funded to 2028 |
| **Ocean Motion Technologies** | **Demoted to Tier C** | ~$7.15M across six awards → `BEYOND_STAGE` |
| **Certus Core** | **Analyst override, excluded** | Defence data-platform business; the AUV award is one thread among Air Force, SOCOM and MDA work |
| **X-Hab 3D** | Qualified | ~$3.98M but dominated by non-marine Army/NASA/DOT construction work |
| **Juice Robotics** | Qualified | **Zero federal awards**; entire case rests on one university announcement plus an undisclosed round |

Two data-integrity bugs surfaced and were fixed: **award double-counting** (the same contract from two sources inflated ARMADA's total to $4.7M) and **phase misclassification** (a $174,798 NOAA Phase I typed as Phase II from stray abstract text).

---

## From Ranking to Triage

The 64-way tie was not solved by adding decimals. Ordinal ranking was **removed**.

| Queue | Count | Criteria |
|---|---:|---|
| **Tier A — Diligence Now** | **38** | Not incidental; not established/beyond-stage; technical ≥2; commercial ≥2; Propeller relevance ≥2; **latest signal within 24 months** |
| **Tier B — Research Queue** | **65** | Relevant and not excluded, but missing one or two Tier A criteria |
| **Tier C — Watch** | **445** | Incidental, established/beyond-stage, dormant (>48 months), or too little evidence |
| **Frontier — Pre-company** | **31** | Separate framework; never compared numerically against funded companies |

Every assignment stores its reasons, for and against, as an auditable analyst view.

**The numeric score survives only as diagnostic metadata.** It is labelled as such in every export. **Ordering within Tier A is analyst judgment, not machine rank** — which is why Certus Core sits in machine Tier A and is excluded from the analyst shortlist below.

---

## Frontier Signals Queue

**31 signals** (target 20–40). Full analysis in `research/frontier_signals.md`.

| Signal type | Count |
|---|---:|
| NSF I-Corps (funded customer discovery) | 17 |
| Commercialization grant (PFI / Convergence Accelerator) | 14 |

**Taxonomy:** marine materials 11 · blue food 7 · ocean sensing 5 · offshore energy 4 · maritime autonomy 2 · coastal adaptation 1 · maritime software 1. 27 distinct institutions, none dominant.

**Five most interesting:** Oregon State autonomous subsea connection (I-Corps, 17 Aug 2026) · UMass Lowell BioSPACE aquaculture pathogen biosensing ($1M) · University of Washington Backyard Buoys ($4.98M) · Texas A&M cost-effective offshore anchor · VIMS shellfish RFID (I-Corps, 19 Aug 2026).

### Is the pre-company problem materially improved?

**Yes, though the honest metric matters.** Pre-company signals are 31 of 579 total candidates (5.4%) — barely different from Phase 2's 6%. But raw share of a universe dominated by 200,000 SBIR records was always the wrong denominator.

**Against the actionable universe** — Tier A + Tier B + Frontier = 134 — **frontier signals are 23.1%.** More importantly they now have a queue where they are never numerically outranked by a funded company, and a framework with no commercial-traction dimension to fail.

**What is still not fixed:** the queue is NSF-only (I-Corps and PFI are NSF programmes), roughly five of 31 are marginal, and there is no person-level tracking — the single highest-value pre-company signal would be *a researcher's role changing from academic to founder*, which the system cannot yet see.

---

## Recall Regression Tests

The Phase 2 failures (Sea-Gal lost to a missing plural, Hydrokinetx to a threshold) were invisible from the output. **12 recall canaries** now live in `tests/fixtures/recall_canaries.yaml`, covering every thesis pattern: maritime autonomy, marine materials, ocean sensing, offshore energy, marine carbon, blue food, hidden adjacency and pre-company research.

They assert **survival through each stage** and name which stage lost a canary. They never assert a ranking, and a test enforces that production code never reads the fixture.

**They immediately earned their place.** The 3newable canary failed on first run: **the lexicon term "ocean" does not match the word "oceanographic"** — a word appearing in almost every relevant abstract. 3newable's own award text classified as `incidental` and would have been rejected outright. Fixed by adding morphological variants (`oceanographic`, `oceanography`, `oceanic`) plus `buoy`, `mooring`, `hydrographic`, `bathymetric`, `littoral`, `nearshore`.

---

## ARMADA vs 3newable

| Dimension | ARMADA | 3newable |
|---|---|---|
| **Technical diligence surface** | Three programmes; two granted patents with readable claims; no published performance data | One tightly-scoped programme; **published quantitative performance** (50 W lab, 7–8 W target, 0.91 W measured, 2.4 W peak) |
| **Independent validation** | Six competitive awards across four agencies | **PNNL national-laboratory testing** under DOE TEAMER; two at-sea deployments on WHOI's OOI array |
| **Current activity** | **Navy contract to 2028-03-20**; latest award Nov 2024 | **Sole DOE contract ended Nov 2025**; no 2026-dated public signal |
| **Government validation** | **Four agencies** — NSF, Navy, NOAA, OSD | One agency — DOE |
| **Commercial evidence** | No named customer; Navy Phase II doubling is the closest proxy | No named customer; OOI is a co-development partner |
| **IP diligence** | Rich — 2 licensed patents + **1 unresolved EPADS patent question** | Thin — no patents identified in public sources |
| **Customer-budget evidence** | **Strong** — 87 maritime-autonomy procurement contracts, $244.8M observed, Navy-dominant | Weak — ocean observing is largely federal grant budgets; marine carbon procurement is one $58K contract |
| **Propeller thesis fit** | Category 1 Industrials, `central_mechanism`, dual-use — explicitly written about | Categories 2/5, `central_mechanism`; biofouling and persistent power are named bottlenecks |
| **Stage fit** | Pre-seed equity, ~$3.0M non-dilutive — **at the upper edge** of pre-seed | Seed, $2.47M non-dilutive, funding runway ended |
| **Differentiated sourcing** | **Weaker** — WHOI spinout; Propeller's founding partner | **Stronger** — surfaced from DOE SBIR bulk data, a source Phase 1 could not access |
| **Public evidence quality** | High — patents, six award records, company site, WHOI release | High but narrow — one contract line, one partner, one results article |
| **Key unresolved question** | **What rights does ARMADA hold to the EPADS IP?** | **Is the company still active and commercializing in 2026?** |

---

## The Application Work-Sample Tradeoff

The goal is not picking the better company. It is picking the candidate that best demonstrates technical diligence, commercial reasoning, independent judgment, Propeller relevance, and the ability to work from messy public evidence.

**ARMADA's weakness as a *sourcing* demonstration is real.** It is a WHOI spinout, and WHOI is Propeller's founding partner with a formal multi-year relationship. As an outside-in sourcing demonstration it proves less than finding something from an under-read source. **We do not know whether Propeller has evaluated ARMADA, and I make no claim either way.** The tradeoff is simply that a WHOI spinout is, structurally, the least differentiated place an outside analyst can point.

**But the work sample is a diligence exercise, not a sourcing exercise** — and Phase 2 already carries the sourcing demonstration (Iowa State's landlocked $5M anticorrosion award; the federal-money-versus-venture-attention inversion; the recall bugs the system caught on itself). Phase 3 is where technical and commercial reasoning must be shown.

On that test ARMADA is materially stronger: three distinguishable programmes to reason about separately; two readable patents plus a genuine unresolved IP question that a technical investor would actually want answered; a market sizeable bottom-up from 87 real procurement transactions; and a sharp, defensible commercial kill question (defence subcontractor versus venture-scale company) that the funding mix makes non-obvious.

**3newable's strength is narrower but genuine.** Published imperfect results are unusually good material — reasoning honestly about a 0.91 W measurement against a 7–8 W target, *and catching that the two are not directly comparable*, is exactly the judgment the role calls for. But its evidence is one contract, one partner and one article, its funding ended nine months ago, and it has no 2026 signal. Building a diligence case on it risks the most basic finding being "we cannot establish the company is still operating."

---

## Candidate Recommendation

### Primary: **ARMADA Marine Robotics**
Confirmed, on materially different and much stronger evidence than Phase 2 had. It supports a real technical deep dive, a bottom-up market model from actual transactions, and a genuine open IP question. The Navy contract running to 2028 means the company will still be a live subject when the work is finished.

### Backup: **3newable LLC**
Promoted over Juice Robotics, which has **zero federal awards** and rests entirely on a single university announcement. 3newable's published quantitative testing is the best technical-diligence material in the universe; its risk is that current activity cannot be confirmed.

### Analyst-selected top five (judgment, not machine rank)
1. **ARMADA Marine Robotics** — richest diligence surface, multi-agency validation, open IP question
2. **3newable LLC** — published independent performance data
3. **Designer Ecosystems LLC** — full Phase I→II progression; pairs structure with measurement
4. **NEXUMA L.L.C.** — Phase II funded to 2028; addresses a failure mode seawalls do not solve
5. **Grow Oyster Reefs, LLC** — the innovation is the manufacturing method, which is what makes it a product

**Excluded despite machine Tier A:** Certus Core (defence data platform, ocean incidental), Ocean Motion Technologies (beyond stage), X-Hab 3D (mostly non-marine), Juice Robotics (no independent corroboration).

---

## Remaining Evidence Gaps

1. **EPADS licence rights — the one that could change the recommendation.** If ARMADA has no rights to US 10,112,686, its largest programme sits on IP it does not control. Resolvable with one founder conversation; not resolvable from public sources.
2. **3newable's 2026 status.** No public signal after Dec 2025.
3. **ARMADA equity financing.** Nothing disclosed since March 2025; the aggregator figure (~$290K) is tier-3 and was deliberately not ingested.
4. **No commercial customer for either.** Both cases rest on government validation.
5. **Licence economics unknown** for all WHOI-licensed IP — royalties, field of use, milestones.
6. **Frontier queue is NSF-only.** DOE, NOAA and DoD translation programmes are not covered.
7. **Patent coverage is still manual.** PatentsView and USPTO ODP require keys; all patent work here was done through public patent pages by hand.
8. **The refresh was bounded** to 121 candidates, so tier assignment is most reliable at the top of the funnel and least reliable in Tier C.

---

## Phase 3 Diligence Plan

**Subject: ARMADA Marine Robotics. One candidate, done properly.**

1. **Programme separation.** Treat propulsion, EPADS and the sensing constellation as three businesses with different customers, IP and timelines. Do not average them.
2. **Technical diligence.** Read all three patents' claims. Assess control authority in realistic sea states for asymmetric propulsion; assess the vacuum-hold payload mechanism for EPADS. Identify what the Navy Phase II option exercise implies about milestones met.
3. **IP diligence — the primary question.** *What rights does ARMADA hold to the EPADS IP?* Map the three WHOI patents against the three programmes and identify which are covered by the announced licences.
4. **Market sizing, bottom-up from real transactions.** Use the 87 maritime-autonomy procurement contracts already in `procurement` ($244.8M observed, $441K median, Navy-dominant). No cited TAM.
5. **Competitive mapping.** Teledyne, Kongsberg, Saab, L3Harris; plus Propeller's own Orpheus and VATN — where the component-versus-vehicle distinction makes adjacency a real question.
6. **Unit economics** at component level against observed vehicle price points ($1.68M–$1.99M).
7. **Resolve the kill questions** already recorded in `analyst_views`: control authority in real conditions, and defence subcontractor versus venture-scale company.
8. **Primary-research targets:** a UUV programme manager; an ocean survey fleet operator; a WHOI engineer outside the company; a competing AUV manufacturer on where their cost actually sits.
9. **Output:** an Advance / Pass recommendation with reasoning, stating explicitly what would change the view.

**Still not to be built:** the frontend. The ranking is trustworthy only at the top, and an interface should be built around a finding worth displaying — which Phase 3 is meant to produce.
