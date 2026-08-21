# Initial Leads — Phase 1 Research Sample

**Prepared:** 2026-08-21 · **Count:** 28 candidates · All sources accessed 2026-08-21
**Machine-readable version:** `initial_leads.csv`

---

## How these were found

Every candidate came from one of four public, reproducible channels:

| Channel | Count | What the signal means |
|---|---|---|
| **NSF I-Corps / PFI / Convergence Accelerator** | 11 | Pre-company. A researcher with federal funding to do structured customer discovery or technology translation. |
| **NSF SBIR / STTR** | 12 | Company exists and has won competitive non-dilutive funding judged partly on commercial merit. |
| **University spinout with executed IP license** | 3 | Research → patent → license → company. The full transition, completed. |
| **Federal program / accelerator with verifiable award** | 2 | ARPA-E SEA-CO2; DOE water power + StartBlue. |

**What is deliberately absent.** No Crunchbase-derived list. No "top ocean startups" roundup. No company that has raised a large priced round. The best-known name here is atdepth MRV, and it is included for its ARPA-E award, not its press. This is a *research-stage* sample by construction, which is the point — the brief asked whether promising ocean technologies can be identified *before* they become obvious venture deals.

### Honest limitations of this sample

1. **NSF-biased.** SBIR.gov's API returned HTTP 403 (see `data_sources.md` §3), so Navy, NOAA, and DOE SBIR recipients are badly under-represented. That is precisely where Propeller's stated dual-use interest would show up. This is the biggest known hole.
2. **US-biased.** No systematic access to Canadian, EU, UK, or Norwegian award data — notable because Propeller has two Nova Scotia portfolio companies and participates in Canada's Ocean Supercluster.
3. **Public-footprint floor.** Companies that took no federal money and issued no press release are invisible to this method. Some of the best ones may be exactly those.
4. **Single-analyst classification.** Category assignment and ocean-centrality tagging were done by one person by hand. No inter-rater check.
5. **Marine CDR is deliberately under-weighted.** It is Propeller's densest area and the best-covered corner of ocean venture. Adding five more alkalinity companies would have inflated the count without adding sourcing value.

---

## Full sample

Scores are sourcing-priority only (see `prioritization_framework.md`) — **not investment judgments**. D1 Technical · D2 Commercial · D3 Timing · D4 Venture · D5 Propeller fit, each 0–3.

### Companies formed, with commercialization funding

| # | Candidate | Location | Technology | Evidence | Score | Flags |
|---|---|---|---|---|---|---|
| 1 | **ARMADA Marine Robotics** | MA (WHOI) | Single-motor asymmetric propulsion for UUVs | 2 granted patents; 2 exclusive WHOI licenses; NSF STTR $255,821 | **13** | — |
| 2 | **Juice Robotics** | RI (URI) | Underwater sensing/comms/robotics; "High Dive" aerial-to-underwater fibre tether | 4 URI licenses; Rogue Island Ventures investment (Jul 2026) | **13** | — |
| 3 | **atdepth MRV** | MA (MIT) | GPU-based real-time ocean modelling for mCDR MRV | ARPA-E SEA-CO2 $2,524,964; Deep Sky partnership | **12** | Crowded category |
| 4 | **Sea-Gal Technologies** | PA | High-frequency MIMO underwater acoustic comms | NSF SBIR Phase I $304,999 | **12** | — |
| 5 | **Hydrokinetx Corporation** | IA | Wave energy for persistent ocean-sensor power | NSF STTR Phase I $304,950 | **11** | — |
| 6 | **Designer Ecosystems LLC** | VA | Submerged barriers + performance sensor platform | NSF SBIR Phase I $301,769 → **Phase II $1,242,694** | **11** | Municipal buyer |
| 7 | **Ocean Motion Technologies** | CA | Small-scale WECs powering at-sea data collection | DOE water power engagement; StartBlue C4 | **10** | — |
| 8 | **Nexuma L.L.C.** | FL | Microbial limestone reinforcement vs. bottom-up flooding | NSF SBIR **Phase II $1,149,796** | **10** | Municipal buyer |
| 9 | **Lightthought LLC** | NJ | AI imaging in turbid water for aquaculture | NSF STTR Phase I $304,925 (18 Aug 2026) | **10** | — |
| 10 | **Hybrid Reefs** | CA (Scripps) | CoralGuard antifouling coating, Snap-X, Symbion | Patent-pending; UCSD Chancellor's Innovation finalist; StartBlue C1 | **10** | Consultancy risk |
| 11 | **Grow Oyster Reefs, LLC** | VA | Biomimetic moulds for mass-produced reef substrate | NSF SBIR **Phase II $1,237,446** | **10** | Consultancy risk |
| 12 | **Cultimar Technologies** | PR | Protein filtration removing aquaculture off-flavour | NSF SBIR Phase I $304,645 | **10** | — |
| 13 | **Sitkana Inc** | AK | Modular tidal energy for remote coastal communities | NSF STTR Phase I $305,000 | **9** | Capex before validation |
| 14 | **Reef Arches, LLC** | FL | Eco-engineered coastal protection (claims ≤70% wave energy reduction) | NSF SBIR Phase I $154,646 | **9** | Municipal buyer |
| 15 | **Prime Pacific Enterprises** | HI | Autonomous UAS for coastal erosion prediction | NSF SBIR Phase I $305,000 | **9** | Consultancy risk |
| 16 | **Atlantic Fish Co LLC** | DC | Bioengineered fish cell lines for cultivated seafood | NSF SBIR Phase I $305,000 | **9** | — |
| 17 | **Namaka Algae, Inc** | HI | Light-distribution tech for dense microalgae cultures | NSF SBIR Phase I $304,541 | **9** | — |

### Pre-company research with commercialization intent

| # | Candidate | Institution | PI | Technology | Award | Score |
|---|---|---|---|---|---|---|
| 18 | **Autonomous subsea connection** | Oregon State | Geoffrey Hollinger | Diver-free subsea connect/disconnect under wave motion | I-Corps, **17 Aug 2026** | **9** |
| 19 | **Nearshore bathymetry XAI** | U. Alaska Fairbanks | Erin Trochim | Satellite → high-res depth maps, explainable | I-Corps, 19 Aug 2026 | **9** |
| 20 | **Coastal storm surge AI surrogate** | U. Florida | Zhe Jiang | Fast surge/water-level prediction for insurers & design | I-Corps, 19 Aug 2026 | **9** |
| 21 | **Steel corrosion digital workflow** | MIT | Anastasios Hart | Corrosion inspection, analysis, repair | I-Corps, 17 Aug 2026 | **9** |
| 22 | **BioShield CP** | Iowa State | Kaoru Ikuma | Microbial coating for corrosion protection | Convergence Accelerator **$4,999,999** | **9** |
| 23 | **POAWRS hydrophone arrays** | Northeastern | Purnima Makris | Wide-area passive acoustic monitoring from wind farms | PFI-TT $550,000 | **9** |
| 24 | **Shellfish aquaculture RFID** | VIMS / William & Mary | William Walton | Marine RFID + analytics for farm inventory | I-Corps, 19 Aug 2026 | **8** |
| 25 | **AI wave prediction for shipping** | UC Berkeley | Reza Alam | Low-cost sensors + routing to cut fuel waste | I-Corps, 31 Jul 2025 | **8** |
| 26 | **Seafood species ID** | Michigan State | Mariah Meek | AI + genomics for field species verification | I-Corps, 25 Jan 2024 | **7** |
| 27 | **Coastal soil enhancement** | WPI | Mingjiang Tao | Stabilising salinized coastal soils | PFI-RP $1,000,000 | **6** |
| 28 | **Maritime diagnostics** | U. Michigan | David Singer | Diagnostics across disparate data sources | I-Corps, 1 Jul 2025 | **6** |

---

# The Five Most Interesting

Selected on judgment, not score alone. Three of the five are the top three scorers; **Hydrokinetx (11)** was chosen over several 10s, and **Sea-Gal (12)** over **atdepth (12)** on differentiation grounds explained below.

---

## Card 1 — ARMADA Marine Robotics

**What it is.** A WHOI spin-off commercialising *Asymmetric Propulsion*: varying the speed of a single-bladed propeller through each rotation so that one motor delivers both thrust and steering. Eliminates fins and secondary motors from underwater vehicles.

**Why it surfaced.** WHOI executed **two exclusive patent licenses** to ARMADA in January 2025 — the cleanest possible research-to-venture signal, at Propeller's own founding partner institution.

**Technical claim.** Propulsion *and* low-speed manoeuvring from a single electric motor, removing fins and additional motors, thereby reducing weight, drag, complexity, and cost.

**Evidence available today.**
- **Observed:** Two granted US patents — Asymmetric Propulsion (US 9,873,499) and Rotational Feedback Control (US 11,990,857).
- **Observed:** Two exclusive WHOI license agreements, Jan 2025.
- **Observed:** NSF STTR Phase I, **$255,821**, to develop Asymmetric Propulsion with WHOI.
- **Observed:** Founders Robin Littlefield and Jeff Kaeli are WHOI engineers who developed the technology there.
- **Unknown:** Any customer, pilot, unit volume, or priced financing.

**Potential customer / problem.** Anyone deploying UUVs at volume: naval and defense, hydrographic survey, offshore inspection, and ocean science. The binding constraint on swarm-scale deployment is per-vehicle cost, and actuator count drives both cost and failure modes.

**Why now.** Licenses executed Jan 2025 and an STTR won subsequently — the company is at the exact moment when IP is secured but institutional capital has not yet arrived. Propeller also reports a rapid Navy adoption signal for maritime autonomy.

**Propeller relevance.** Category 1 (Industrials). WHOI is the founding partner. Dual-use, which Propeller wrote about in April 2026. Pre-seed, inside the stated $500K–$3M model. Note Propeller already holds two AUV companies (Orpheus, VATN) — ARMADA is a *propulsion component* play, which is either complementary or competitive depending on facts not yet public.

**Biggest technical question.** Does single-motor asymmetric propulsion retain adequate control authority in realistic currents and sea states? Reducing to one actuator is elegant precisely where conditions are benign; the risk is that control degrades exactly where cheap, expendable vehicles are most needed.

**Biggest commercial question.** Is vehicle cost actually the customer's binding constraint? Public procurement data shows buyers paying $1.68M (Saab → NOAA) and $1.99M (WHOI → Navy) for single AUVs, but the dominant lifetime cost in ocean operations is often the support ship, launch, and recovery. If so, a cheaper vehicle does not change the customer's economics.

**What we do not know.** Financing history; team size; whether a vehicle is being built or the technology is licensed to OEMs; license financial terms; any customer.

**Who we would want to speak with.** A UUV programme manager at a naval research organisation; an ocean survey operator who runs fleets; a WHOI engineer outside the company familiar with the propulsion work; a competing AUV manufacturer on where their cost actually sits.

**Sources.** [WHOI press release](https://www.whoi.edu/press-room/news-release/armada) · [Newswise license announcement](https://www.newswise.com/articles/woods-hole-oceanographic-institution-licenses-ocean-technology-to-armada-marine-robotics) · [Ocean News & Technology, NSF contract](https://oceannews.com/news/science-technology/armada-marine-robotics-wins-nsf-contract/) · [armadamarinerobotics.com](https://www.armadamarinerobotics.com/)

---

## Card 2 — Juice Robotics

**What it is.** A URI spinout building miniaturised underwater sensing, communications, and robotic systems. Its named technology, **High Dive**, links aerial and underwater systems through an ultra-light fibre-optic tether for real-time comms, sensing, and control.

**Why it surfaced.** On **1 July 2026** — seven weeks before this research — URI announced Juice Robotics had licensed **four** URI technologies and taken investment from Rogue Island Ventures.

**Technical claim.** Dramatically reduces the size, complexity, and cost of underwater operations; High Dive enables real-time communication and control without the complexity and cost of conventional offshore operations.

**Evidence available today.**
- **Observed:** Four URI technologies licensed.
- **Observed:** Investment from Rogue Island Ventures (amount undisclosed).
- **Observed:** Two years incubating in URI's Ocean Technology Center.
- **Observed:** Team combines the URI professor who created the technology (Brennan Phillips, CSO), a URI alumnus (Matthew Jewell, CTO), and an experienced operator CEO (Stephen Piper, ex-IBM).
- **Unknown:** Three of four licensed technologies are unnamed; round size undisclosed; no named customer.

**Potential customer / problem.** Stated markets are defense, energy, research, and maritime. The underlying problem is that underwater work requires either a tethered ROV with a support ship or an autonomous vehicle with severely constrained bandwidth.

**Why now.** Licenses plus first institutional capital, both within the last two months. Separately, URI received **$2.5M from the Office of Naval Research** in August 2026 to expand RISE-UP, its dual-use maritime programme — the surrounding ecosystem is being actively capitalised.

**Propeller relevance.** Category 1 (Industrials). URI is a Propeller partner. Explicitly commercial, scientific, *and* defense — matching the dual-use thesis. Seed stage.

**Biggest technical question.** An ultra-light fibre tether from an aerial platform to an underwater vehicle must survive wind, wave, and drift loading. What is the real operational envelope — sea state, current, depth, duration — and how does the tether not become the failure mode it is meant to eliminate?

**Biggest commercial question.** Is this a products company or a services company? "Reducing the cost of underwater operations" can be sold as hardware or delivered as survey work. Given a defense-heavy market and a small team, the pull toward services will be strong, and that changes the venture case fundamentally.

**What we do not know.** Three of the four licensed technologies; round size and valuation; whether High Dive has been demonstrated at sea or in tank testing only; any customer or pilot.

**Who we would want to speak with.** Tom Sperry at Rogue Island Ventures on the thesis and the round; a URI Research Foundation licensing officer on what the four technologies cover; an offshore survey operator on whether air-launched underwater systems solve a problem they have; a competing tethered-ROV maker.

**Sources.** [URI announcement, 1 Jul 2026](https://www.uri.edu/news/2026/07/uri-ocean-technology-spinout-juice-robotics-secures-investment-from-rogue-island-ventures-and-licenses-four-uri-technologies/) · [URI RISE-UP / ONR expansion, Aug 2026](https://www.uri.edu/news/2026/08/uri-innovations-awarded-funding-to-expand-rise-up-program-strengthening-rhode-islands-defense-and-maritime-innovation-ecosystem/)

---

## Card 3 — Sea-Gal Technologies, Inc.

**What it is.** A company developing **high-frequency MIMO underwater acoustic communications**, operating outside the frequency range of marine mammal communication.

**Why it surfaced.** NSF SBIR Phase I award 2451589, $304,999, 1 April 2025 — and because underwater communications is an *enabling layer* absent from the publicly disclosed Propeller portfolio.

**Technical claim.** Multiple-input multiple-output acoustic communication achieving high data rates underwater while reducing marine ecosystem impact by operating above marine mammal communication bands.

**Evidence available today.**
- **Observed:** NSF SBIR Phase I, $304,999, competitively awarded.
- **Observed:** Explicit ecological design constraint in the frequency choice.
- **Unknown:** Achieved data rates, range, prototype status, team, customers, IP position.

This card has the **thinnest evidence base of the five** — a single federal award. It is here on the strength of the *problem*, not the proof, and that asymmetry is stated deliberately rather than papered over.

**Potential customer / problem.** Underwater bandwidth is the binding constraint beneath nearly everything else in this taxonomy. AUVs cannot stream sensor data. mCDR MRV cannot get measurements ashore in real time. Subsea monitoring depends on cables partly because wireless is so limited. Buyers would be AUV manufacturers, subsea infrastructure operators, defense, and ocean observing programmes.

**Why now.** Acoustic comms has been incrementally improved for decades; MIMO is a legitimate architectural change rather than a tuning exercise. The proliferation of low-cost AUVs — including two Propeller portfolio companies — creates demand for a comms layer that did not previously exist at volume.

**Propeller relevance.** Category 2. Horizontal enabler sitting beneath Orpheus, VATN, Aquatic Labs, and Indeximate. **Underwater acoustic communications is not represented in the publicly disclosed portfolio reviewed** — noting six stealth companies exist whose coverage cannot be seen.

**Biggest technical question.** Do MIMO gains survive real shallow-water channels? Underwater acoustic channels are severely multipath-limited with rapid time variability, and spatial multiplexing gains that work in simulation frequently collapse in the field. Higher frequency also means higher attenuation — the ecological benefit may cost range.

**Biggest commercial question.** Component or system? If Sea-Gal sells modems to AUV OEMs it is a component business with modest volumes and price pressure. If it sells complete underwater networks it faces a much longer sale into conservative buyers. Different companies entirely.

**What we do not know.** Almost everything operational. This is the highest-uncertainty, highest-optionality card of the five.

**Who we would want to speak with.** An underwater acoustics researcher at WHOI or URI on whether high-frequency MIMO is credible; an AUV manufacturer on what they currently pay for comms and what they wish existed; the PI, Junchen Bao.

**Sources.** [NSF Award 2451589](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2451589)

---

## Card 4 — atdepth MRV

**What it is.** An MIT spin-off building a **GPU-based real-time ocean modelling system** for measurement, reporting, and verification of marine carbon dioxide removal — spanning global ocean down to metre scale, combined with in-water monitoring.

**Why it surfaced.** ARPA-E awarded it **$2,524,964** under the SEA-CO2 program, one of 11 projects sharing $36M.

**Technical claim.** GPU-based modelling dramatically improves speed over conventional CPU approaches, unlocking multi-scale modelling from global oceans to metre scale with real-time performance. CEO Dr. Carlos Muñoz-Royo frames it as combining highly efficient numerical models with in-ocean monitoring data.

**Evidence available today.**
- **Observed:** ARPA-E SEA-CO2 award, $2,524,964 — a competitive, technically-reviewed federal program.
- **Observed:** Partnership with Deep Sky to advance direct ocean capture in Canada.
- **Observed:** SeaAhead/BlueSwell alumnus.
- **Observed:** Provides integrated monitoring of baseline conditions — pH, carbon content, physical oceanography.
- **Unknown:** Revenue, pricing model, whether registries accept the methodology.

**Potential customer / problem.** mCDR developers who must prove durable removal to sell credits; carbon registries; buyers like Frontier and Microsoft who need independent verification. MRV is the gating problem for the entire sector — a credit that cannot be verified cannot be sold.

**Why now.** mCDR capture companies (including at least five in Propeller's portfolio) are moving from lab to deployment, which is exactly when verification becomes the binding constraint rather than an academic question.

**Propeller relevance.** Category 4 — Propeller's densest theme. Aquatic Labs is the closest disclosed adjacency (ocean sensing for mCDR MRV), so there is genuine adjacency risk to examine: **complementary or overlapping is a real question, not a rhetorical one.** Being verification rather than capture makes it structurally complementary to Ebb, Calcarea, CarbonRun, pHathom, and Banyu.

**Biggest technical question.** Can a model-plus-sparse-sensor approach produce removal estimates with uncertainty bounds tight enough for a registry to certify and a buyer to pay for? This is the open scientific problem in mCDR, not a solved engineering task.

**Biggest commercial question.** Is MRV a durable standalone business? It could be absorbed by registries, built in-house by large capture developers, or displaced by publicly funded models. And whether GPU speed is a defensible moat or a temporary engineering lead is a genuine concern.

**What we do not know.** Revenue; whether any registry has accepted the methodology; team size; the exact split between modelling and hardware.

**Who we would want to speak with.** A carbon registry methodology lead on what verification standard they will actually accept; an mCDR developer on what they pay for MRV today; a physical oceanographer outside the company on the achievable uncertainty bounds; Deep Sky on the partnership scope.

**Sources.** [ARPA-E project page](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/scalable-integrated-real-time-gpu-based-modeling-system-enable-mrv-mcdr) · [DOE $36M announcement](https://www.energy.gov/articles/doe-announces-36-million-advance-marine-carbon-dioxide-removal-techniques-and-slash) · [Deep Sky partnership](https://www.deepskyclimate.com/blog/deep-sky-and-atdepth-mrv-partner-to-advance-direct-ocean-capture-in-canada)

---

## Card 5 — Hydrokinetx Corporation

**What it is.** A company using **wave energy to provide persistent power for ocean sensing platforms**, replacing batteries and solar which fail in remote or cloudy conditions.

**Why it surfaced.** NSF STTR Phase I award 2537673, $304,950, 17 June 2026. The STTR structure implies a university research partner.

**Technical claim.** Wave energy can supply long-duration, reliable power for maritime sensing where batteries and solar are inadequate, removing the endurance limit on ocean data collection.

**Evidence available today.**
- **Observed:** NSF STTR Phase I, $304,950.
- **Observed:** Problem framing tied to sensing endurance rather than grid generation.
- **Unknown:** Device design, power output, cost, prototype status, sea trials, customers.

**Potential customer / problem.** Ocean observing programmes, mCDR MRV operators, offshore wind monitoring, defense sensing, aquaculture. Every persistent sensing deployment in this taxonomy is ultimately limited by power — that is what forces ship-based servicing visits, which is where the cost actually lives.

**Why now.** Demand for persistent ocean data is rising sharply — mCDR verification, offshore wind monitoring, maritime domain awareness. Propeller's own framing that "almost every ocean market is under-resourced with information" describes a bottleneck that persistent power directly relieves.

**Propeller relevance.** Categories 2 and 3 (Industrials). Directly enables the ocean-data thesis Propeller articulates around Aquatic Labs and Hum.ai. Pre-seed.

**Notably, the framing avoids the classic marine energy trap.** Wave energy has a long history of capital-intensive failure chasing grid-scale generation. Powering a sensor is a completely different — and much more venture-appropriate — problem: small, modular, high value per watt, and no grid interconnection.

**Biggest technical question.** Can a wave energy converter small enough to power a sensor package survive the marine environment — biofouling, storms, corrosion, moving parts in seawater — for long enough to beat the alternative? Reliability, not conversion efficiency, is the real hurdle.

**Biggest commercial question.** What is the honest benchmark? The competitor is not another WEC; it is a bigger battery, a larger solar panel, or accepting a shorter mission. Hydrokinetx must beat those on total cost of ownership including servicing. If a battery swap every six months is cheap, the market disappears.

**What we do not know.** Device architecture; power output; the university STTR partner; whether anything has been tested at sea.

**Who we would want to speak with.** An ocean observing programme manager on what they actually spend servicing power systems; a marine energy engineer on small-scale WEC reliability; PI Blake Boren; Ocean Motion Technologies as a comparator on whether these economics close.

**Sources.** [NSF Award 2537673](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2537673)

---

## Why these five rose above the rest

**1. They sit at a state change, not just a recent date.** ARMADA (first exclusive licenses) and Juice Robotics (first licenses + first institutional round) are at the precise transition the project is built to detect. Recency alone is cheap; a state change is meaningful.

**2. Three of the five are enabling layers, not applications.** Sea-Gal (comms), Hydrokinetx (power), and atdepth (verification) each sit *beneath* multiple applications, including several Propeller portfolio companies. Enabling layers are systematically under-sourced because they are less legible than applications — nobody writes a press release about a modem.

**3. They survive the business-model screen.** Much of the broader sample carries `CONSULTANCY_RISK` or `MUNICIPAL_BUYER_ONLY` — coastal adaptation especially, where the buyer is often a municipality on a grant cycle. All five here have a plausible path to a product sold to a commercial or defense buyer.

**4. Ocean-centrality is `central`, not `adjacent`.** Each fails without the ocean. Compare the MIT corrosion workflow (score 9) — genuinely interesting, but its award describes transportation, energy, and logistics generally, so it carries `OCEAN_INCIDENTAL (pending confirmation)` and cannot be advanced until that is resolved.

**5. Enough public evidence exists to do real work.** Each has at least one substantial, verifiable document — granted patents, a university licensing announcement, a federal award abstract. Meaningful diligence is possible without privileged access.

### Near-misses, and why

- **Designer Ecosystems (11)** — the only candidate with a full SBIR Phase I → Phase II progression, and it matches Propeller's August 2026 adaptation thesis closely. Held back by `MUNICIPAL_BUYER_ONLY`: strong technical evidence, unresolved question of who pays.
- **Hybrid Reefs (10)** — a Scripps spinout with a genuinely interesting asset in **CoralGuard**, a biocide-free antifouling coating. The reef-restoration framing likely *understates* it; antifouling is a large regulated market under pressure to move off copper chemistry, and Propeller has written about hull coatings. Worth revisiting if the company reframes.
- **BioShield CP / Iowa State (9)** — a $5M award on biocide-free anticorrosion coatings at a landlocked university. The best single illustration of the project's core insight, but marine applicability is unconfirmed, so it cannot yet be advanced honestly.

---

# Deep-Dive Recommendation

## Primary: **ARMADA Marine Robotics**

**Why.** It is the only candidate where the full evidence chain is public *and* the market can be sized from public data.

1. **Technical diligence is genuinely possible.** Two granted US patents (9,873,499 and 11,990,857) mean the actual claims are readable. Most early candidates offer only a marketing sentence; here the engineering is disclosed and can be assessed on its merits.
2. **Market sizing can be built, not invented.** USAspending contains real AUV procurement — Saab selling NOAA a long-range AUV for $1.68M, WHOI selling the Navy a REMUS 600 for $1.99M, Teledyne spares and software maintenance. A bottom-up market model can be assembled from actual transactions rather than a cited TAM figure.
3. **The competitive set is mappable.** Teledyne, Kongsberg, Saab, L3Harris on the incumbent side; VATN and Orpheus among newer entrants — the latter two being Propeller portfolio companies, which makes the competitive and portfolio-adjacency analysis unusually concrete.
4. **Unit economics are tractable.** A component-level cost claim (fewer motors, no fins) can be modelled against known vehicle price points.
5. **The kill questions are sharp and answerable.** Whether control authority survives real sea states, and whether vehicle cost or support-ship cost dominates — both resolvable with a small number of expert calls.
6. **The sourcing story is coherent.** WHOI is Propeller's founding partner, so a deep dive also tests whether outside-in monitoring of partner-institution IP adds anything to an existing relationship. That is a useful result either way.

**Deliberately not chosen for press coverage.** ARMADA has comparatively little. It was chosen for *evidence density*.

## Backup: **Juice Robotics**

**Why.** Same structural profile — university spinout, licensed IP, dual-use, Propeller partner institution — with a different and useful contrast: it has already taken institutional capital, so a deep dive would test *pricing and syndicate* dynamics rather than pre-financing dynamics. URI's ONR-funded RISE-UP expansion also gives a concrete ecosystem to analyse.

**Why it is backup rather than primary.** Three of its four licensed technologies are unnamed publicly, so the IP position cannot be fully assessed from public sources, and the round size is undisclosed. Both gaps are closable with founder contact but not from public research alone — which makes it the weaker choice for a work product that must stand on public evidence.

**Not selected, and why:** *Sea-Gal* — evidence base too thin (one award) to support market sizing or competitive mapping. *atdepth MRV* — strong, but mCDR is Propeller's most crowded area and MRV market structure depends on registry decisions not yet made, making financial modelling speculative. *Hydrokinetx* — almost no public technical detail beyond the award abstract.
