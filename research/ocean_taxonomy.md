# Ocean Frontier Taxonomy

**Prepared:** 2026-08-21 · **Phase:** 1 · **Status:** working taxonomy, expected to change

## How this taxonomy was built

This is **not** a generic "blue economy" category tree. It is derived in three steps:

1. Start from Propeller's own three public themes — **Industrials, Carbon, Organics** ([propellervc.com](https://propellervc.com/)).
2. Split those into sourcing-operable categories, i.e. categories that map onto a *searchable technical vocabulary* in grant, patent, and publication databases. "Industrials" is a fine investment theme and a useless search term.
3. Keep only categories where I could point to either (a) a disclosed Propeller portfolio company, or (b) an explicit written statement of interest from Propeller. Categories failing both tests are listed separately in §9 as *unvalidated*, not silently promoted.

### The one structural decision that matters

Propeller explicitly refuses to treat the ocean as a sector. In [The Climate Market Map](https://propellervc.com/blog/the-climate-market-map) they describe the ocean as **"a cross-sector catalyst for climate innovation"** rather than an eighth sector, and in [At The Ocean's Edge](https://propellervc.com/blog/at-the-oceans-edge) they ask what the ocean's "true edges" are.

So this taxonomy carries a second axis alongside category: **ocean-centrality**, defined in §10. A technology is in scope if the ocean is its *mechanism*, its *deployment environment*, or its *customer's operating environment* — not because the word "ocean" appears. This axis does real work: it is what admits Allium Engineering (rebar) and excludes an AI logistics tool that happens to have a shipping customer.

---

## 1. Maritime Autonomy & Robotics

**Propeller theme:** Industrials
**Disclosed portfolio:** Orpheus Ocean (full-ocean-depth AUVs), VATN Systems (low-cost modular AUVs), Fleet Robotics (hull-crawling biofouling robots), Navier (electric hydrofoiling vessels)

**Core problem.** Anything done in or on the water currently requires a crewed vessel, a diver, or a tethered ROV with a support ship behind it. Day rates for that support are the dominant cost line in almost every offshore activity. The technology question is how much of that can be replaced by autonomous, attritable, low-cost hardware.

**Customer groups.** Navies and defense primes; offshore wind developers and O&M contractors; subsea cable operators; oil & gas inspection; hydrographic survey and charting; ports and harbor security; scientific fleets; commercial shipping (hull services); fisheries enforcement.

**Technical bottlenecks.** Underwater positioning and navigation without GPS (INS drift, acoustic positioning); underwater communications bandwidth; energy density and endurance; pressure housings and connectors at depth; autonomous launch-and-recovery, which is frequently the real cost driver rather than the vehicle; manipulation and docking under wave motion; reliable autonomy in low-visibility, high-current conditions.

**Commercial bottlenecks.** Government procurement cycles; the pull toward becoming a services business (selling survey-days rather than vehicles); certification and class approval for uncrewed vessels; insurance for autonomous operation; the fact that many buyers want data, not robots, which pushes hardware companies into a lower-margin service model.

**Venture fit.** Strong. Hardware cost curves are falling, the dual-use demand signal is explicit — Propeller reports rapid Navy adoption "when the demand signal is clear" ([dual-use post](https://propellervc.com/blog/why-ocean-innovation-is-often-dual-use)) — and Propeller has already bought this category three times. Risk: capital intensity and the services trap.

**Where new companies come from.** WHOI (Orpheus, ARMADA), URI (Juice Robotics), MIT Sea Grant / AUV Lab, Harvard Microrobotics, Virginia Tech, Stevens, Florida Atlantic (SeaTech), Navy SBIR/ONR, university marine robotics labs, and the NSF I-Corps pipeline (e.g. Oregon State's autonomous subsea connection work).

---

## 2. Ocean Sensing, Data & Intelligence

**Propeller theme:** Carbon and Industrials
**Disclosed portfolio:** Aquatic Labs (real-time ocean sensing, mCDR MRV, eDNA), Hum.ai (Earth-observation foundation models), Indeximate (subsea cable monitoring)

**Core problem.** Propeller's own framing is the sharpest statement of it: *"almost every ocean market is under-resourced with information to make decisions, or measure appropriately"* ([Meet Aquatic Labs](https://propellervc.com/blog/meet-aquatic-labs)). Nearly half of US waters are unmapped to modern standards. Carbon markets, insurers, offshore developers, and regulators all need measurements that do not currently exist at the required density or cost.

**Customer groups.** mCDR developers and carbon registries; offshore wind and subsea cable operators; insurers and reinsurers; NOAA and defense; aquaculture operators; shipping (routing); coastal municipalities.

**Technical bottlenecks.** Sensor drift and calibration over long deployments; biofouling of optical and electrochemical sensors (a first-order failure mode, not a nuisance); power for persistent autonomous platforms; underwater data transmission; converting sparse point measurements into defensible area-wide estimates; validating remote-sensing inference against ground truth.

**Commercial bottlenecks.** Buyers are often grant-funded science budgets rather than commercial P&Ls; long sales cycles; the "is this a data company or an instrument company?" ambiguity; MRV value is tied to carbon market maturity, which remains policy-dependent.

**Venture fit.** Good, with a caveat. Sensing companies can become instrument vendors with modest TAM. The venture case usually requires either a data/analytics layer with recurring revenue or a regulatory mandate that forces purchase. MRV for mCDR is attractive precisely because verification may become mandatory.

**Where new companies come from.** ARPA-E SEA-CO2 (explicitly a sensing-for-mCDR program), NOAA Ocean Enterprise / The Continuum accelerators, Scripps, WHOI, Northeastern (POAWRS acoustics), NSF Ocean Technology & Interdisciplinary Coordination, university physical-oceanography labs.

---

## 3. Offshore Energy, Power & Subsea Infrastructure

**Propeller theme:** Industrials
**Disclosed portfolio:** Aikido Technologies (floating offshore wind platforms + ocean datacenters), Blue Energy (coastal submerged SMRs), Indeximate (subsea cable failure prevention), Vema Hydrogen (geologic hydrogen, maritime fuel)

**Core problem.** Offshore energy is bottlenecked on installation, maintenance, and interconnection cost, not on generation physics. Propeller's [ocean-compute post](https://propellervc.com/blog/summer-slowdown-the-ocean-is-heating) names the specific hard problems: subsea interconnect and cabling, materials and corrosion in saltwater, and regulatory frameworks for ocean use and heat discharge.

**Customer groups.** Offshore wind developers; utilities and grid operators; hyperscalers and datacenter developers; cable owners and installers; remote and island communities; marine fuel buyers.

**Technical bottlenecks.** Installation vessel scarcity and cost; connector and cable reliability at depth; subsea power distribution; corrosion, fatigue, and biofouling on 25-year assets; thermal management for submerged compute; the very small number of specialized installation vessels globally.

**Commercial bottlenecks.** Extreme capital intensity; permitting timelines measured in years; policy exposure — US offshore wind has proven politically volatile; utility procurement conservatism; project-finance structures that resist venture-style scaling.

**Venture fit.** Selective. This is the category most likely to fail the "capital required before validation" screen. The venture-appropriate slice is usually the *enabling component or software* — a connector, a monitoring system, an installation method — rather than the energy asset itself. Note that Propeller's own picks here are enabling: Aikido sells a *platform manufacturing method*, Indeximate sells *monitoring*.

**Where new companies come from.** DOE Water Power Technologies, PacWave (OSU), ARPA-E, NREL, Navy SBIR, OSU, University of Maine (floating wind), university offshore-engineering departments.

---

## 4. Marine Carbon & Ocean Chemistry

**Propeller theme:** Carbon — their densest area
**Disclosed portfolio:** Ebb Carbon (electrochemical OAE), Calcarea (onboard shipboard capture + ocean storage), CarbonRun (riverine alkalinity enhancement), pHathom (limestone capture + mineralization), Banyu Carbon (photochemical capture from seawater), Rewind (biomass to anoxic Black Sea), Aquatic Labs (MRV)

**Core problem.** The ocean already holds roughly 60× the carbon of the atmosphere and absorbs about a third of annual emissions ([Propeller](https://propellervc.com/blog/introducingpropeller)). Marine CDR aims to enhance that sink durably and measurably. The two gating issues are cost per tonne and verification.

**Customer groups.** Voluntary carbon buyers (Frontier, Microsoft, airlines); compliance markets if and when they arrive; shipping companies facing IMO pressure; industrial emitters co-located with seawater.

**Technical bottlenecks.** Energy intensity per tonne; MRV — proving durable removal in a moving, mixing fluid is genuinely hard and is the field's central scientific problem; ecological impact and permitting; alkalinity feedstock supply chains; scaling electrochemistry.

**Commercial bottlenecks.** Carbon price uncertainty; offtake concentration among a handful of buyers; permitting for ocean discharge; public perception of ocean intervention; registry methodology immaturity.

**Venture fit.** Propeller clearly believes so — 5+ of 19 disclosed companies are here, and they call mCDR "the ocean's superpower." **But this is now the most crowded and best-covered corner of ocean venture.** For *differentiated sourcing* purposes, undifferentiated mCDR capture plays are the least likely place to find something Propeller's network has not already seen. The more interesting sub-slice is **MRV and measurement**, where the science is unsettled and the buyer need is structural.

**Where new companies come from.** ARPA-E SEA-CO2, NOAA Ocean Acidification Program / NOPP, Carbon to Sea Initiative, WHOI, Scripps, UW, Dalhousie, Caltech.

---

## 5. Marine Materials, Corrosion & Coastal Infrastructure

**Propeller theme:** Industrials (explicitly includes "materials" and "adaptation")
**Disclosed portfolio:** Allium Engineering (stainless-clad rebar)

**Core problem.** Seawater destroys things. Corrosion costs the US over half a trillion dollars annually ([NSF Convergence Accelerator award 2452538](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2452538)). Biofouling drives ship fuel consumption and sensor failure. Coastal infrastructure faces saltwater intrusion, soil salinization, and increasing wave loading. Propeller's [Aug 2026 heat post](https://propellervc.com/blog/can-the-ocean-still-beat-the-heat) explicitly names hull coatings, lubricants, and buoyancy foams as areas of interest.

**Customer groups.** Infrastructure owners and DOTs; ports; shipowners; offshore wind and cable operators; coastal municipalities and insurers; the Navy (marine corrosion is a standing, funded Navy problem line).

**Technical bottlenecks.** Antifouling without biocides (regulatory pressure is closing off copper and organotin chemistry); coating adhesion and lifetime in immersion; qualification cycles — marine materials need multi-year field exposure data, which is slow and expensive; scaling novel materials into commodity-priced markets.

**Commercial bottlenecks.** Commodity pricing pressure; extremely conservative specification and standards regimes (ASTM, class societies, DOT); long qualification timelines; incumbent chemical majors.

**Venture fit.** Genuinely promising and **structurally under-sourced**, because these technologies do not self-identify as "ocean tech." They appear in materials science, civil engineering, and microbiology departments. Allium proves Propeller will buy it. The risk is slow qualification and commodity margins.

**Where new companies come from.** MIT, Iowa State (microbial corrosion coatings), WPI (coastal soils), Northeastern, Navy SBIR/NSWC, Florida Institute of Technology (Navy biofouling test services), materials-science departments generally — **not** ocean-science departments. This is the single most important structural insight in the taxonomy.

---

## 6. Coastal Adaptation & Climate Risk

**Propeller theme:** Industrials ("adaptation"), Carbon ("sensing, monitoring, modeling"), and one disclosed stealth company in "coastal adaptation"
**Disclosed portfolio:** one unnamed stealth company (coastal adaptation); Hum.ai and Aquatic Labs touch the data layer

**Core problem.** Propeller's most recent published thesis piece is about this: warming has already outrun mitigation timelines, and coastal industries need "pain-killers" now — with 2024 the first year above 1.5°C and warming accelerating to 0.3–0.4°C/decade ([Can the ocean still beat the heat?](https://propellervc.com/blog/can-the-ocean-still-beat-the-heat), 13 Aug 2026).

**Customer groups.** Coastal municipalities and utilities; property insurers and reinsurers; ports; homeowners and developers; state resilience agencies; FEMA-adjacent programs; aquaculture operators facing thermal stress.

**Technical bottlenecks.** Forecasting skill at actionable resolution and lead time; validating nature-based structures against engineering standards; durability of deployed structures; linking physical models to financial loss estimates credibly.

**Commercial bottlenecks.** The buyer is frequently a municipality with grant-cycle budgets, which is a hard venture customer. The escape route is selling to insurers, developers, or industrial asset owners with real P&Ls. Many businesses here are actually engineering-services firms in disguise — a specific screen in `prioritization_framework.md`.

**Venture fit.** Rising, and Propeller is publicly leaning in. But this category has the highest density of **consultancy-shaped businesses**, so it needs the harshest business-model screening.

**Where new companies come from.** NSF I-Corps (multiple 2026 awards in storm surge and bathymetry), NSF PFI, SBIR Phase I/II, SeaAhead's coastal-resilience Pilot program, university coastal engineering programs (Florida, Delaware, Texas A&M, WPI).

---

## 7. Blue Food, Aquaculture & Marine Biology

**Propeller theme:** Organics
**Disclosed portfolio:** Circle Seafoods (salmon supply chain); two stealth companies disclosed in "seafood traceability" and "seafood processing"

**Core problem.** Aquaculture is the fastest-growing US food-production segment ([NSF SBIR 2537706](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2537706)), but it runs on thin margins with severe biological risk — disease, off-flavor, feed cost, thermal stress — and remarkably little digital instrumentation.

**Customer groups.** Aquaculture producers (finfish, shellfish, seaweed); feed companies; processors and distributors; retail and foodservice buyers; certification bodies.

**Technical bottlenecks.** Disease detection at farm scale; feed conversion and alternative feed ingredients; off-flavor compounds; monitoring in turbid water; genetics and breeding; cold chain.

**Commercial bottlenecks.** Producer capital constraints and low willingness to pay; fragmented, often family-owned buyers; commodity pricing; regulatory permitting for offshore aquaculture in US waters; long biological cycles that slow sales.

**Venture fit.** Mixed, and honestly the weakest of the seven for classic venture returns — Propeller has exactly **one** named company here against ten in Industrials. Software and biotech layers fit venture better than production assets. Note the disclosed stealth companies suggest more activity than the named portfolio shows.

**Where new companies come from.** NSF SBIR (Cultimar, Lightthought), VIMS, Hatch Blue accelerator, University of Maine, Auburn, land-grant aquaculture programs, USDA NIFA.

---

## 8. Industrial & Maritime Software / Applied AI

**Propeller theme:** Industrials
**Disclosed portfolio:** Nexxa.ai (agentic AI for legacy heavy-industry software — rail, ports, shipyards), Hum.ai, Indeximate

**Core problem.** Maritime and heavy industry run on manual processes and decades-old software. Propeller frames Nexxa's opportunity as a market where "industrial engineering remains stubbornly manual" ([Meet Nexxa](https://propellervc.com/blog/meet-nexxa.ai)).

**Customer groups.** Shipping lines and charterers; ports and terminals; shipyards; classification societies; marine insurers; offshore operators.

**Technical bottlenecks.** Data access from legacy and air-gapped systems; connectivity at sea (though Starlink has materially changed this — Propeller says so directly); validating model outputs where errors are safety-critical; integration with vessel systems.

**Commercial bottlenecks.** Extremely conservative buyers; long pilot-to-contract cycles; fragmented decision-making split between owner, operator, charterer, and manager; low software spend per vessel historically.

**Venture fit.** Good margins and capital efficiency, **but** this is where the "ocean connection is incidental" failure mode lives. A generic AI tool with one shipping logo is not an ocean company. The ocean-centrality test in §10 exists largely to police this category.

**Where new companies come from.** Less from universities, more from operators and industry. NSF I-Corps does surface some (Berkeley wave routing, Michigan maritime diagnostics). Weakest category for research-first sourcing — a limitation worth stating plainly.

---

## 9. Categories considered and NOT promoted

Listed for transparency. Each failed the validation test — no disclosed portfolio company and no explicit written Propeller statement.

| Candidate category | Why not promoted |
|---|---|
| Deep-sea mining | No public Propeller signal; severe regulatory and reputational exposure |
| Ocean thermal energy conversion (OTEC) | No public signal; capital intensity likely fails stage fit |
| Marine pharmaceuticals / natural products | Launch-era language mentioned "marine-based pharmaceuticals" but no disclosed company and it has dropped from current site language; biotech timelines likely mismatch a $500K–$3M ocean fund |
| Ballast water & biosecurity | Genuine problem, no public Propeller signal; retained as a watch item |
| Marine spatial planning / permitting software | No public signal; likely small TAM |
| Desalination | No public signal; capital-intensive and incumbent-dominated |
| Ocean plastics remediation | No public signal; historically weak business models |

These are watch items, not scope. Promoting a category requires new public evidence.

---

## 10. The ocean-centrality axis

Every candidate is tagged on this axis independently of category. It is the mechanism that implements Propeller's "ocean's edge" framing, and it is the primary defense against a list full of generic climate startups.

| Tag | Definition | Test | Example |
|---|---|---|---|
| **Central — mechanism** | The ocean *is* the physical mechanism | Remove seawater and the technology ceases to function | Ebb Carbon; Banyu Carbon |
| **Central — environment** | Built specifically to survive/operate in the marine environment | Would need fundamental redesign for a land application | Orpheus Ocean; Allium Engineering |
| **Enabling — customer** | Customer's operations are ocean-based; tech is domain-adapted | Ocean domain knowledge is a real moat, not a logo | Indeximate; Nexxa.ai |
| **Adjacent** | Ocean is one market among several | Would the company change if the ocean market vanished? If no → deprioritize | Generic corrosion sensor |
| **Incidental** | Ocean appears only as a use case or keyword | Fails the screen | Generic AI ops tool with a port customer |

**Sourcing rule:** Central and Enabling are in scope. Adjacent requires an explicit argument. Incidental is filtered out and logged as a rejection with a reason — rejections are retained so the filter itself can be audited and tuned.

---

## 11. Taxonomy → search vocabulary

The operational purpose of this file. Each category maps to query terms used against NSF, USAspending, OpenAlex, and arXiv. Terms are deliberately technical, because — as §5 argues — the best candidates never use the word "ocean."

| Category | High-yield query terms |
|---|---|
| 1. Maritime Autonomy | autonomous underwater vehicle, AUV, USV, uncrewed surface vessel, subsea manipulation, launch and recovery, inertial navigation, station-keeping, ROV, bathymetric survey |
| 2. Ocean Sensing | ocean observing, hydrophone, eDNA, pCO2 sensor, ocean glider, moored buoy, acoustic telemetry, bathymetry, remote sensing coastal, MRV |
| 3. Offshore Energy | floating offshore wind, subsea cable, wet-mate connector, marine energy, tidal turbine, wave energy converter, offshore substation, mooring line |
| 4. Marine Carbon | ocean alkalinity enhancement, direct ocean capture, marine CDR, carbonate chemistry, electrochemical CO2, mineralization, carbon flux |
| 5. Marine Materials | marine corrosion, antifouling, biofouling, cathodic protection, marine coating, stainless clad, saltwater intrusion, chloride ingress, buoyancy foam |
| 6. Coastal Adaptation | storm surge, coastal resilience, living shoreline, nature-based coastal protection, shoreline erosion, sea level rise, marine heatwave, harmful algal bloom |
| 7. Blue Food | aquaculture, shellfish, finfish, seaweed, kelp, fish disease, aquafeed, off-flavor, hatchery, seafood traceability |
| 8. Maritime Software | vessel routing, voyage optimization, port operations, maritime domain awareness, hull performance, predictive maintenance vessel |

**Known limitation.** Category 5 terms (corrosion, coatings) return heavy non-marine noise; category 8 terms return heavy non-ocean noise. Both need the ocean-centrality filter applied downstream, and in Phase 1 that filter was applied by me, by hand. See `data_sources.md` §7 for measured false-positive rates.
