# ARMADA Marine Robotics
## Outside-In Venture Diligence

**Prepared:** 2026-08-21 · **Analyst:** outside-in, public sources only · All sources accessed 2026-08-21
**Evidence register:** `research/armada/evidence_register.csv` (45 claims) · **Model:** `models/armada_underwriting.xlsx`
**Phase 3 commit:** `bfd57afa4d48ee787b08210ff25441c6513b7773` (`bfd57af`)

---

### Recommendation

# HOLD — NEED MORE EVIDENCE

Not a pass. The technology is credible, the founders are unusually well-qualified, and a US Navy customer has twice put more money behind the work — most recently in **March 2026**. But three things a venture investor must know cannot be established from public information: **whether ARMADA controls the IP behind its best product, whether any commercial customer exists, and whether the addressable market is large enough.**

**No INVEST recommendation is possible or offered on public information.** What is possible is a precise statement of what would move this to ADVANCE, and the six calls that would settle it — most decisively the first two, which are cheap, binary, and could be completed in a week.

**Advance immediately if:** EPADS pods are consumable per deployment **and** ARMADA holds commercialisation rights on the jointly-filed EPADS IP.
**Pass if:** pods are recovered and reused, no commercial customer conversation has occurred in five years, and no OEM has evaluated the propulsion product.

---

### Why this is interesting

Three things are genuinely unusual.

**A repeat government customer that keeps deciding to continue.** ARMADA has $2,972,287 of verified federal awards across NSF, Navy, NOAA and OSD. On the Navy Phase II the government did not merely award — it **exercised an option** (Jan 2025) and then **incrementally funded a new contract line item** (Mar 2026). Three independent agencies also funded Phase I work inside four months in late 2024. That is a pattern of repeated affirmative decisions by technically expert reviewers.

**A quantified technical result on a real Navy vehicle.** Most seed-stage hardware companies offer a claim. ARMADA's Phase I validated hydrodynamic simulation against **in-water testing on a REMUS 600**, establishing an A-size (4.875" × 36") pod carrying a 5 kg module, with two pods costing **≤25% mission time and <10% parasitic drag**. That is a specific, falsifiable, third-party-relevant result.

**A possible consumable.** EPADS pods appear to be **left on the seafloor with the payload**. If true, this is not a subsystem sold once per vehicle — it is a consumable with recurring unit volume. That single fact is the difference between an engineering business and a venture business, and it is one sentence from a founder.

---

### Company / product overview

Founded 2019, East Falmouth MA. A WHOI spin-off and the first to use WHOI's Express License program. **Three people are publicly identified:** Jeff Kaeli (CEO, Co-Founder, Co-Inventor; PhD, MIT/WHOI Joint Program; led the Asymmetric Propulsion effort at WHOI), Robin Littlefield (Lead Engineer, Co-Founder, Co-Inventor; WHOI mechanical engineer, a year of cumulative sea time), Philip "Rusty" Warren (Lead Director, Co-Founder; 30+ years in federal government and government contracting).

| Line | What it is | Maturity | Funding | Customer evidence |
|---|---|---|---|---|
| **Asymmetric Propulsion** | Single-bladed propeller modulated within each revolution gives thrust *and* steering from one motor; removes fins and control actuators | 2 granted patents; 2018/2019 conference papers; self-reported 3D steering test (2022). **No public performance data.** | NSF STTR Phase I, $255,821 (2020) | **None** |
| **EPADS** | Fully external payload pod; no host modification; commands over the host's native acoustic modem; valve floods the cavity so the payload becomes negative and descends, at zero net buoyancy change to the vehicle | In-water tested on a REMUS 600; thresholds met; Phase II is characterising **placement accuracy** | Navy Phase I $246,320 → Phase II **$1,998,926** (base $999,028 + option $499,949 + CLIN 0004 $499,949), running to 2028-03-20 | **Funded Navy R&D customer only** |
| *Persistent sensing* | Passive-ballast float riding currents; "constellation" concept | **NOAA Phase I only, completed Jan 2025. Not a product; not on the company's site. No follow-on found.** | NOAA $174,798 | None |

**Government funding is not revenue.** No commercial sale, pilot, LOI or named commercial customer appears anywhere in the public record.

---

### Key investment debates

Full treatment in `research/armada/investment_debates.md`.

**1. Component company or engineering organisation?** *The central debate.* Today ARMADA is a three-person team funded by sequential government development contracts, holding an option on becoming a product company. Five years in there is zero commercial revenue and no public OEM relationship. The March 2026 CLIN funding is a positive signal that also *extends the R&D model*. Whether commercial development was attempted and failed, deliberately deferred, or never started is invisible from outside — and those imply three very different companies.

**2. Does ARMADA control the EPADS IP?** Materially better than earlier phases concluded, still unresolved. ARMADA is a **joint applicant and joint listed assignee with WHOI** on WO 2024/136933, with its CEO and Lead Engineer among the inventors, and the claimed mechanism (valve-flooded cavity) is **distinct** from WHOI's older vacuum-hold patents — consistent with new invention from the funded work. But **no US national-phase application was found**, and the ownership split, field of use and sublicensing terms are entirely invisible.

**3. Will an OEM replace a qualified propulsion architecture?** The least-evidenced, most load-bearing assumption in the propulsion line. Changing propulsion invalidates vehicle qualification; every target OEM is also the party best able to build it in-house; and there is **no public performance data at all** for the product ARMADA says it is bringing to market. A physical concern also stands unanswered: control authority from intra-revolution modulation should scale with RPM, which is weakest at exactly the low speeds the station-keeping pitch depends on.

**4. Can the observable market support a venture outcome?** Not on what we can see. Narrow addressable observed procurement is **~$826K/year**; broad adjacency ~$6.3M/year. A $30M revenue threshold is ~36× and ~5× those figures respectively. The fair rebuttal is that a market cannot be observed before the product exists.

---

### Technical diligence

**Asymmetric Propulsion — credible foundation, no disclosed performance.** The patent protects a *control method*, not a propeller shape, and claim 1 covers "at least one thrusting surface" — broader than the single-blade marketing. Peer-reviewed conference publications (2018, 2019) and two granted patents give real substance. But there are **no public figures** for efficiency, turning radius, power draw, or acoustic signature, and single-blade propulsion has prior art to 1945, with a 2010 patent on an asymmetrically changing rotating blade shape. **[INFERRED]** An unbalanced single blade raises vibration, bearing-life and acoustic-signature questions that matter disproportionately to a Navy buyer.

**EPADS — the strongest evidence in the company.** The technical ladder is unusually complete: modelled → dummy payloads fabricated → **in-water tested on a REMUS 600** → quantified thresholds met. What remains unproven is the part that matters most operationally: **live release at depth and placement accuracy**, which is precisely what Phase II is for. The ≤25% mission-time figure should be read honestly — it is the *cost* of the capability, not a benefit.

**[INFERRED] The tension worth naming:** ARMADA's *marketed* product has the weakest evidence, and its *best-evidenced* product is single-customer Navy R&D.

---

### Commercial opportunity

By segment, with demonstrated relationships distinguished from potential ones:

- **US Navy / DoD** — the only demonstrated customer. Funded R&D with an exercised option. Extreme buyer concentration; SBIR Phase II → Phase III is a well-known valley of death.
- **UUV OEMs** (HII/REMUS, Teledyne, Kongsberg, Saab, L3Harris) — the route to recurring propulsion revenue. **No public relationship of any kind.** They are simultaneously the target customer and the most credible substitute.
- **Oceanographic institutions** — highest credibility, lowest revenue. A reference market, not a scale market. ARMADA's own origin institution competes here.
- **Offshore wind / subsea survey** — **[INFERRED] the most interesting untested hypothesis.** This is where "one vehicle does survey *and* inspection" maps to a large non-government budget, and where the saving is a vessel day rather than a component price. **No evidence ARMADA is pursuing it.**
- **Allied defence** — plausible follow-on; ITAR exposure unassessed.

---

### Market / procurement evidence

Built bottom-up from 87 federal contracts already in our database, reproducible via `src/ofr/models/procurement_audit.py`. **This is observed contract value in a keyword sample, not a TAM.**

| Bucket | n | Observed (2014–2026) | Annualised |
|---|---:|---:|---:|
| R&D programmes | 13 | $69.0M | $5.31M |
| Integration / primes | 3 | $65.7M | $5.06M |
| Complete platforms | 35 | $60.3M | $4.64M |
| Services / support | 10 | $19.5M | $1.50M |
| **Components / spares** | 11 | **$9.6M** | $0.74M |
| Sensors / payloads | 6 | $9.6M | $0.74M |
| **Payload deployment** | 4 | **$1.1M** | $0.09M |

Two contracts ($8.9M) were removed as false comparables — a design-build *building* and a counter-UUV services contract.

**Narrow addressable ≈ $826K/year. Broad adjacency ≈ $6.3M/year.** The money sits in R&D, primes and complete platforms — not in the subsystem line items ARMADA sells. Caveats cut both ways: the sample misses classified and programme-of-record spending, and payload deployment is small partly *because the capability does not exist yet*. But 13 years show **no growth trend** in components/spares, and the most frequent supplier is a **distributor** (W S Darley, 24 appearances) — the signature of a market that buys commodity hardware and complete systems.

---

### Competitive landscape

ARMADA occupies the **subsystem layer in two different boxes**. Platform companies (HII/REMUS, Teledyne, Kongsberg, Saab, L3Harris, C2 Robotics, Jaia) are **potential customers and potential self-suppliers simultaneously** — the defining structural risk. At the propulsion layer the real competitor is not a rival startup but **the incumbent architecture and its qualification base**. In payload deployment, external deployable payloads are *not* a new idea — 1990s Navy patents and later work exist — so the differentiation narrows to the specific zero-net-buoyancy, no-host-modification combination.

Notably, **WHOI itself appears in the procurement sample as a supplier on five contracts (~$11.3M)**, including selling the Navy a REMUS 600. ARMADA's licensor, joint patent applicant and founder-employer is also an independent vendor to the same customer.

---

### Business model

**Current observed model: contract R&D.** Every known dollar is a competitively awarded federal development instrument.

Plausible scaled models, best first: **(B) consumable EPADS pods** — recurring unit volume, the most attractive economics available and the least examined; **(A) subsystem sales to OEMs** — recurring and capital-light but requires a design-in that invalidates qualification; **(C) licensing** — suits a three-person team but ARMADA's right to sublicense is unknown; **(D) complete vehicles** — captures the biggest bucket but is a different, capital-heavy company competing with HII and Kongsberg; **(E) continued contract R&D** — the proven default that does not compound.

**The venture question:** can ARMADA move from E to B? Public evidence cannot tell us whether that transition has begun.

---

### Underwriting scenarios

`models/armada_underwriting.xlsx` — a **forward requirements model, not a projection**. No revenue history is invented because none exists. Green cells are observed facts; amber cells are analyst assumptions; all outputs are live formulas.

| Base-case steady state | Value |
|---|---:|
| EPADS revenue (600 pods × $25K) | $15.0M |
| Propulsion revenue (120 × $40K) | $4.8M |
| Engineering / R&D revenue | $2.0M |
| Support | $0.25M |
| **Total revenue** | **$22.05M** |
| Gross profit | $10.6M |
| Operating cost (25 heads) | $5.95M |
| Operating profit | $4.7M |
| **Gap to $30M venture threshold** | **–$7.95M** |

**What the model actually says.** Even a Base case that assumes 600 consumable pods and 120 propulsion modules per year — **both entirely unevidenced** — lands short of a $30M revenue threshold. To clear it on EPADS alone requires ~1,200 pods/year at $25K. Against observed narrow addressable procurement of $826K/year, the threshold is ~36×. **The venture case therefore cannot rest on the federal procurement we can see.** It requires OEM channel volume, commercial offshore buyers, allied export, or spending our keywords do not capture. That is not fatal — but it must be underwritten explicitly rather than assumed.

---

### Team

Exceptional technical credibility for the domain, and thin on commercial evidence. Kaeli is a MIT/WHOI joint-program PhD who led the underlying research; Littlefield is a WHOI mechanical engineer with a year at sea; Warren brings federal contracting depth. That combination explains the funding record precisely — this is a team optimised to win and execute government R&D.

**[UNKNOWN]** Whether Littlefield is full-time at ARMADA or retains a WHOI role; total headcount; and whether anyone owns commercial sales. No commercial or manufacturing leadership is publicly identified.

---

### IP

**Propulsion:** US 9,873,499 (expiry 2035) and US 11,990,857 (expiry 2041), **owned by WHOI, exclusively licensed to ARMADA** for underwater and marine surface vehicles. ARMADA does not own them. Licence terms — field of use detail, sublicensing, milestones, termination — are not public.

**EPADS:** WO 2024/136933 lists **ARMADA and WHOI as joint applicants and joint assignees**, inventors Kaeli, Littlefield and Fiester, priority 2022-09-21. **No US national-phase application was found**; a PCT publication alone confers no US exclusionary right.

**Adjacent WHOI-owned patents not covered by any announced licence:** US 10,112,686 and US 11,072,406 (payload deployment by vacuum force) and US 10,640,188 (passive ballast — plausibly the basis of the NOAA float concept).

> **Stated precisely. This is not a legal opinion and not a freedom-to-operate assessment:** public records establish that ARMADA is a joint applicant and joint listed assignee on the published EPADS PCT with WHOI and that its founders are named inventors. The allocation of ownership, field-of-use and commercialisation rights between the co-applicants, and whether US national-phase protection has been secured, **could not be confirmed from public sources.** This is not evidence that ARMADA lacks rights.

---

### Risks

1. **Single-customer concentration.** ~$2.5M of $2.97M is DoD. Federal R&D budgets and SBIR policy are exogenous risks.
2. **The engineering-organisation trap.** The model that funds the company today does not compound.
3. **OEM adoption may never happen.** Qualification is the moat protecting incumbents *from* ARMADA.
4. **IP dependency on WHOI**, which is also an independent vendor to the same customer.
5. **Team depth.** Three publicly identified people; no commercial or manufacturing leadership.
6. **Small observable market** for the subsystem line items ARMADA actually sells.
7. **Phase III transition risk** — the well-documented SBIR valley of death.

---

### Propeller Fit

Assessed **only** against publicly stated Propeller strategy. No claim is made about Propeller's internal views, pipeline, or whether ARMADA has been evaluated.

| Criterion (public) | Assessment |
|---|---|
| **Theme** | Ocean Industrials — Propeller's stated theme names "automation, robotics, surveying, inspection… and adaptation/dual-use applications". Direct fit. |
| **Stage** | Pre-seed on equity (no disclosed financing), with ~$3.0M non-dilutive. Consistent with a $500K–$3M first check, though the non-dilutive base is at the upper edge of "pre-seed". |
| **Check size** | Fits the stated ~$500K–$3M range. |
| **Science / engineering depth** | High — granted patents, joint MIT/WHOI PhD founder, peer-reviewed publications. |
| **Ocean relevance** | `central_mechanism`. The technology is meaningless outside a marine environment. |
| **Dual-use** | Propeller published on dual-use ocean innovation in April 2026 and named several portfolio companies as such. ARMADA is squarely dual-use. |
| **Portfolio adjacency** | Propeller's disclosed portfolio contains **two AUV platform companies** — Orpheus Ocean (WHOI-incubated) and VATN Systems. Relative to a subsystem vendor these are **complementary if they buy and awkward if they build**; VATN's low-cost modular mixed-mission positioning is the closest overlap. Labelled **unclear**, not competitive. |

**Explicit caveat on sourcing.** ARMADA is a WHOI spinout, and Propeller's founding partnership is with WHOI. It is therefore **highly likely to be visible within the broader ecosystem around Propeller**, and this memo is emphatically *not* offered as evidence of proprietary sourcing. Phase 2 carries the differentiated-sourcing demonstration. This case exists to demonstrate **outside-in diligence** — technical reasoning, IP analysis, procurement-based market work, and evidence discipline — on a company where enough public evidence exists to do real work. **No claim is made, in either direction, about whether Propeller has already diligenced ARMADA.**

---

### Questions public information cannot answer

1. Are EPADS pods consumed per deployment? *(Determines whether recurring unit economics exist at all.)*
2. What commercialisation rights does ARMADA hold on the jointly-filed EPADS IP, and has a US application been filed?
3. Has any UUV OEM evaluated Asymmetric Propulsion in five years?
4. Is there a sponsoring programme office for a Phase III transition?
5. What equity has been raised, from whom, and is the team full-time?

---

### Primary research plan

Full plan with per-call hypotheses in `research/armada/primary_research_plan.md`. **No one was contacted.**

**Week 1 — the binary questions.** Founders, then WHOI technology transfer. These resolve the IP position and the pod-consumability question. A bad answer on IP ends the process cheaply.
**Week 2 — the two commercial routes.** A UUV OEM engineering lead (will anyone design this in?) and a Navy/former-Navy undersea systems expert (does EPADS have a transition path?). Either route can carry the case; neither is evidenced today.
**Week 3 — validation and upside.** An independent propulsion expert on low-speed control authority and acoustics; an offshore survey contractor on whether the commercial market is real.

---

### What would change our view

**To ADVANCE:** pods confirmed consumable with a credible volume path; ARMADA confirmed to hold commercialisation rights with a broad field of use; **or** a named OEM in active evaluation; **or** an identified Phase III transition sponsor.

**To PASS:** pods recovered and reused; EPADS commercialisation rights controlled by WHOI; no OEM has ever evaluated the propulsion product; no commercial customer conversation in five years; or the team confirms it intends to remain an SBIR-funded engineering business.

---

### Sources

All accessed 2026-08-21. Full traceability in `research/armada/evidence_register.csv` (45 claims, each tagged observed/inferred/unknown with source tier).

**Tier 1 — government and patent records:** USAspending award and transaction records for N68335-23-C-0142, NA24OARX021G0026, HY023325PE002, N6833525C0057, N6833522C0035, 2026230 · SBIR.gov official bulk award dataset · Navy SBIR Phase II abstract (EPADS for Cylindrical UUVs) · US 9,873,499 · US 11,990,857 · US 10,112,686 · US 11,072,406 · US 10,640,188 · WO 2024/136933 A2/A3.

**Tier 2 — ARMADA and WHOI:** armadamarinerobotics.com (technology, team, media) · WHOI press release "WHOI Licenses Ocean Technology to ARMADA Marine Robotics", 7 Jan 2025 · Ocean News & Technology coverage.

**Tier 3 — Propeller (for fit assessment only):** propellervc.com portfolio, themes, and "How We Invest".

**Deliberately not relied upon:** Crunchbase, PitchBook, Tracxn and similar aggregators. A ~$290K funding figure and a ~8-employee headcount appear in such sources; both are excluded from all material findings and are flagged as tier-3 in the evidence register.
