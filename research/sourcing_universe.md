# Sourcing Universe

**Prepared:** 2026-08-21 · **Phase:** 1 · All URLs accessed 2026-08-21

## Selection rule

Every entry answers: *why would a Propeller-relevant company plausibly emerge from here, and what specific signal can we observe?* Institutions are excluded if the only argument is prestige. MIT appears because of specific labs and a specific I-Corps award — not because it is MIT.

Entries are grouped into **Tier 1** (Propeller's declared partners — the surface they already work), **Tier 2** (institutions with demonstrable relevant output not publicly partnered with Propeller), **Funders**, **Commercialization programs**, and **Conferences**.

A note on Tier 1: these institutions are where Propeller has formal relationships. That means our *marginal* value there is low for finding companies they have not seen — but high for *understanding what good looks like*, and for catching things that fall between a partnership's cracks (e.g. an OSU robotics award in an engineering department, not the oceanography college).

---

## Tier 1 — Propeller's declared partner institutions

Source for all five: [Propeller launch PR](https://propellervc.com/blog/launchpressrelease) (WHOI, Oct 2022) and [URI GSO announcement](https://web.uri.edu/gso/news/propeller-welcomes-new-partnerships-with-oregon-state-university-university-of-hawaii-university-of-california-san-diego-and-university-of-rhode-island/) (13 Nov 2023).

### 1. Woods Hole Oceanographic Institution (WHOI)
- **Type:** Independent non-profit research institution · **URL:** https://www.whoi.edu
- **Why it belongs:** Propeller's *founding* partner, described as giving access to WHOI "minds and intellectual property." WHOI has already produced a Propeller portfolio company (**Orpheus Ocean**, incubated at WHOI) and an independent spinout with two exclusive patent licenses (**ARMADA Marine Robotics**, Jan 2025). WHOI hosted Propeller's Ocean MBA and two hackathons.
- **Categories:** 1, 2, 3, 4
- **Signal available:** Press releases announcing licenses and spinouts; named researchers (Anthony Kirincich — wind forecasting; Heidi Sosik — ecology/imaging; Annette Govindarajan — eDNA; Casey Machado — vehicles; Robin Littlefield, Jeff Kaeli — propulsion); federal awards to WHOI visible in NSF and USAspending.
- **Stage of opportunity:** Pre-formation through pre-seed
- **Public data accessibility:** ⚠️ **Degraded.** `techtransfer.whoi.edu` now 302-redirects to `intranet.whoi.edu/inventors`, which is not publicly reachable (connection failed, 2026-08-21). The public available-technologies listing that previously existed is no longer accessible. Licensing news must now be caught via whoi.edu press releases and trade press.
- **Automatable?** Partially — press-release monitoring yes; technology listings no longer.
- **Limitations:** Propeller has a formal partnership here. Assume low marginal sourcing value for obvious WHOI output; the value is in *speed* and in catching non-oceanography departments.

### 2. Scripps Institution of Oceanography / UC San Diego
- **Type:** University research institution · **URL:** https://scripps.ucsd.edu
- **Why it belongs:** Propeller partner since Nov 2023. Critically, Scripps hosts **StartBlue**, a no-cost/no-equity ocean accelerator run with the Rady School — a rare public, enumerable list of very early ocean ventures. Scripps produced **Hybrid Reefs** (Daniel Wangpraseurt, Coral Reef Engineering Lab), a 2026 UC San Diego Chancellor's Innovation Award *Startup of the Year* finalist.
- **Categories:** 2, 4, 5, 6
- **Signal available:** StartBlue cohort lists; Chancellor's Innovation Award finalists (published annually); UCSD Office of Innovation and Commercialization; named labs.
- **Stage:** Idea through seed
- **Public data accessibility:** Good — `innovation.ucsd.edu` returns HTTP 200; StartBlue publishes an impact page naming portfolio ventures.
- **Automatable?** Yes — StartBlue impact page and UCSD Today innovation stories are stable HTML.
- **Limitations:** Propeller partner; StartBlue companies are already visible to San Diego investors.

### 3. University of Rhode Island — Graduate School of Oceanography
- **Type:** University · **URL:** https://web.uri.edu/gso/
- **Why it belongs:** Propeller partner. **The most productive Tier 1 institution for our purposes right now.** In July 2026 URI spinout **Juice Robotics** licensed *four* URI technologies and raised from Rogue Island Ventures. URI runs an **Ocean Technology Center** pilot incubator at its Bay Campus (Juice Robotics operated there for two years), and in Aug 2026 URI Innovations received **$2.5M from the Office of Naval Research** to expand **RISE-UP**, explicitly framed around defense and maritime innovation — i.e. a funded dual-use pipeline, matching Propeller's stated dual-use interest.
- **Categories:** 1, 2, 3
- **Signal available:** URI news releases (`uri.edu/news`) announce licenses, spinouts, and funding with unusual specificity; Ocean Technology Center tenant lists; RISE-UP cohorts. Named researcher: Prof. Brennan Phillips (underwater robotics).
- **Stage:** Pre-formation through seed
- **Public data accessibility:** Very good — URI publishes detailed, dated news items naming companies, founders, and licensed technologies.
- **Automatable?** Yes — `uri.edu/news` is a clean, dated news index.
- **Limitations:** Propeller partner; Rhode Island's ecosystem is small and well-networked, so local investors see these early.

### 4. Oregon State University
- **Type:** University · **URL:** https://oregonstate.edu
- **Why it belongs:** Propeller partner. Operates **PacWave South**, the first US utility-scale grid-connected wave energy test site, with grid-connected testing expected spring/summer 2026 and a 2026–2030 BPA power purchase agreement — meaning OSU is a *physical validation venue* where marine energy hardware gets field-tested and where technical founders congregate. Separately, an OSU robotics I-Corps award (Aug 2026, Geoffrey Hollinger) on autonomous subsea connection shows relevant output from the *engineering* college, not the oceanography college.
- **Categories:** 1, 3
- **Signal available:** PacWave test berth occupancy (who is testing what, and when); OSU newsroom; NSF awards to OSU.
- **Stage:** Prototype through Series A
- **Public data accessibility:** Mixed — `tec.oregonstate.edu` failed to connect on 2026-08-21; `news.oregonstate.edu` and `pacwaveenergy.org` are reachable.
- **Automatable?** Partially — newsroom yes, test-site scheduling unclear.
- **Limitations:** Wave energy has a long history of capital-intensive failures; apply the capital-intensity screen hard here.

### 5. University of Hawai'i at Mānoa
- **Type:** University · **URL:** https://www.hawaii.edu
- **Why it belongs:** Propeller partner. Hawai'i is a natural testbed for tropical/Pacific ocean technology, coastal erosion, and marine energy. Two NSF SBIR Phase I awards to Hawai'i-based companies surfaced in this Phase 1 harvest alone (**Prime Pacific Enterprises**, Honolulu — autonomous coastal-erosion UAS; **Namaka Algae**, Kamuela — microalgae cultivation), plus an Aug 2026 NSF EPSCoR fellowship at UH on fiber-optic sensing for geophysics.
- **Categories:** 2, 6, 7
- **Signal available:** NSF awards to UH and to Hawai'i small businesses; UH news.
- **Stage:** Research through seed
- **Public data accessibility:** Good via NSF API (state filter `HI` is an efficient proxy).
- **Limitations:** Smaller commercialization infrastructure; geographic distance from Propeller's Boston base.

---

## Tier 2 — Institutions with demonstrable output, no public Propeller partnership

Included **only** where this Phase 1 research surfaced concrete, dated, relevant output. This is where outside-in sourcing has the most plausible marginal value.

### 6. Massachusetts Institute of Technology
- **Why:** Two disclosed Propeller companies trace to MIT (Allium Engineering — founders met there; Aquatic Labs — Allan Adams, MIT physicist), and **atdepth MRV** is an MIT spin-off that won **$2,524,964** from ARPA-E's SEA-CO2 program. An Aug 2026 MIT I-Corps award covers steel corrosion inspection and repair — directly adjacent to Allium's thesis.
- **Categories:** 1, 2, 4, 5 · **Stage:** Pre-formation through seed
- **Access:** Excellent — MIT News, NSF API, ARPA-E project pages (though ARPA-E blocks automated fetching; see `data_sources.md`).
- **Limitation:** Heavily trafficked by every investor alive. Value here comes from *category-specific* monitoring (corrosion, marine materials), not general MIT watching.

### 7. Northeastern University
- **Why:** Holds an NSF **PFI-TT** award ([2345791](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2345791), $550K, PI Purnima Makris) for compact coherent hydrophone arrays enabling wide-area passive ocean acoustic monitoring **from wind farms and other ocean platforms** — squarely at the intersection of categories 2 and 3, and PFI-TT is explicitly a technology-translation vehicle.
- **Categories:** 2, 3 · **Stage:** Pre-formation
- **Access:** Excellent via NSF API.

### 8. Iowa State University
- **Why:** The best illustration of the taxonomy's §5 argument. Iowa State holds a **$5.0M NSF Convergence Accelerator** award ([2452538](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2452538), PI Kaoru Ikuma) for **BioShield CP**, a *microbial coating system for corrosion protection*, following a Track M award ([2344389](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2344389)). Landlocked, no oceanography department, would never appear on an ocean-tech list — yet marine corrosion is one of the largest addressable corrosion markets and Propeller has bought a corrosion company.
- **Categories:** 5 · **Stage:** Pre-formation, well-funded
- **Access:** Excellent via NSF API. **Only discoverable via technical vocabulary, never via "ocean" keywords.**

### 9. Worcester Polytechnic Institute
- **Why:** NSF **PFI-RP** award ([2414953](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2414953), $1.0M, PI Mingjiang Tao) on sustainable enhancement of **coastal soils** against seawater intrusion and salinization — coastal adaptation infrastructure, matching Propeller's Aug 2026 adaptation thesis.
- **Categories:** 5, 6 · **Stage:** Pre-formation
- **Access:** Excellent via NSF API.

### 10. Virginia Institute of Marine Science (College of William & Mary)
- **Why:** Aug 2026 I-Corps award ([2637876](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2637876), PI William Walton) for marine-adapted RFID and analytics for **shellfish aquaculture** inventory management. VIMS is a major marine institution with no public Propeller partnership, and this sits in Propeller's thinnest named category (Organics).
- **Categories:** 7 · **Stage:** Pre-formation, active customer discovery
- **Access:** Excellent via NSF API; VIMS publishes news.

### 11. University of Washington
- **Why:** Origin of Propeller portfolio company **Banyu Carbon** (Alex Gagnon, Julian Sachs — career oceanographers). UW's School of Oceanography and Applied Physics Laboratory (APL-UW) are major sources of ocean sensing and vehicle technology.
- **Categories:** 1, 2, 4 · **Access:** NSF API good; `tco.uw.edu` failed to connect on 2026-08-21.

### 12. Caltech / USC
- **Why:** Joint origin of portfolio company **Calcarea** (Jess Adkins, Caltech; Will Berelson, USC) — marine geochemistry translated into shipboard carbon capture. Demonstrates the "professor with decades of chemistry becomes founder" pattern.
- **Categories:** 4 · **Access:** Good.

### 13. Harvard — Microrobotics Lab (Robert Wood)
- **Why:** Technology basis for portfolio company **Fleet Robotics**. Continues to produce soft/micro robotics with marine applicability.
- **Categories:** 1 · **Access:** Lab publications via OpenAlex/arXiv.

### 14. University of Alaska (Fairbanks / Anchorage)
- **Why:** Aug 2026 I-Corps award ([2630206](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2630206), PI Erin Trochim) on explainable AI for satellite-derived nearshore bathymetry — addressing that nearly half of US waters are unmapped to modern standards. Alaska also produced **Sitkana Inc** (Juneau, tidal energy STTR). Remote coastal communities are a genuine, underserved first market.
- **Categories:** 2, 3, 6 · **Access:** Excellent via NSF API.

### 15. University of Florida / East Coast coastal engineering cluster
- **Why:** Aug 2026 I-Corps award ([2633942](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2633942), PI Zhe Jiang) on AI surrogate models for coastal storm surge — with insurance pricing named as an application, which is the escape route from municipal budgets.
- **Categories:** 6 · **Access:** Excellent via NSF API.

### 16. University of California, Berkeley
- **Why:** I-Corps award ([2533913](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2533913), PI Reza Alam) on AI-driven wave prediction for shipping fuel efficiency — a $150B/yr fuel spend with >20% claimed lost to inefficient routing. Alam's lab has a long history in wave energy and ocean hydrodynamics.
- **Categories:** 2, 8 · **Access:** Excellent via NSF API.

### 17. University of Michigan — Naval Architecture & Marine Engineering
- **Why:** One of very few US departments dedicated to naval architecture. I-Corps award ([2531191](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2531191), PI David Singer) on maritime diagnostics.
- **Categories:** 1, 8 · **Access:** Excellent via NSF API.

### 18. Michigan State University
- **Why:** I-Corps award ([2348772](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2348772), PI Mariah Meek) integrating AI and genomics for seafood species identification — traceability, a category where Propeller discloses a stealth company.
- **Categories:** 7 · **Access:** Excellent via NSF API.

### 19. Dalhousie University / Nova Scotia cluster
- **Why:** Two disclosed Propeller companies are in Nova Scotia (**CarbonRun**, Halifax; **pHathom**). Propeller joined **Canada's Ocean Supercluster** Market Solutions Platform. This is a live, demonstrated geography for Propeller, not a guess.
- **Categories:** 4, 2 · **Access:** Canadian award data is separate from US systems — a real gap (see `data_sources.md`).

### 20. Florida Institute of Technology
- **Why:** Holds recurring **US Navy contracts for laboratory and field biofouling assessment** (visible in USAspending, 2024 and 2025). Institutions the Navy pays to test biofouling are where antifouling expertise concentrates — relevant to category 5 and to Fleet Robotics' adjacency.
- **Categories:** 5 · **Access:** Via USAspending.

---

## Federal and public funding sources

| Program | Why it matters | Categories | Stage signalled | Notes |
|---|---|---|---|---|
| **NSF SBIR/STTR** | Company already exists and has won competitive non-dilutive validation. Phase I ≈ $305K, Phase II ≈ $1.25M. | All | Pre-seed/seed | **Core automated source.** Accessible via NSF Awards API. Highest-precision company-discovery signal found in Phase 1. |
| **NSF I-Corps** | ~$50K awards where the PI is doing *customer discovery*. Pre-company but commercially intentioned. | All | Pre-formation | **The single most differentiated source identified.** Catches researchers 6–24 months before company formation. |
| **NSF PFI (TT / RP)** | Explicit technology-translation funding, $550K–$1M. | All | Pre-formation | Core automated source. |
| **NSF Convergence Accelerator** | Multi-million translation awards on themed tracks. | 4, 5, 6 | Pre-formation | Core automated source. |
| **ARPA-E (SEA-CO2)** | $36M/11 projects for mCDR measurement and validation; awardees include **atdepth MRV** ($2.52M) and WHOI. | 2, 4 | Prototype | ⚠️ arpa-e.energy.gov returns **403 to automated requests**. Manual/secondary sourcing only. |
| **NOAA** | Ocean Acidification Program, NOPP mCDR awards, Ocean Enterprise initiative, and **The Continuum** ($14M accelerator network). | 2, 4, 6, 7 | Research → seed | Award data partly via USAspending; program pages manual. |
| **DOE Water Power Technologies** | Funds marine energy and PacWave testing. | 3 | Prototype → demo | Manual + USAspending. |
| **ONR / Navy SBIR** | Dual-use demand signal Propeller explicitly cites. URI's RISE-UP is ONR-funded ($2.5M, Aug 2026). | 1, 2, 5 | Pre-seed → growth | ⚠️ SBIR.gov API returns **403**; use USAspending for contract-level data. |
| **USAspending.gov** | Full federal award coverage. | All | — | **Best used as a demand-side signal** (who is buying) rather than a company-discovery source — see the key insight in `phase1_report.md`. |
| **Grants.gov** | Forecasted/posted opportunities. | All | Pre-award | Working API. Useful for anticipating where money is about to flow. |

---

## Commercialization programs and accelerators

| Program | Type | Why it belongs | Access |
|---|---|---|---|
| **StartBlue** (Scripps + Rady, UCSD) | University ocean accelerator, no-cost/no-equity | Publicly names cohort ventures: Hybrid Reefs, Kai Pono Solutions, CalWave, Greenwater Scientific, Del Mar Oceanographic, Ocean Motion Technologies, AquaPoro. Runs since 2021. | [startblue.ucsd.edu](https://startblue.ucsd.edu/impact/) — good |
| **URI Ocean Technology Center** | University incubator (Bay Campus) | Housed Juice Robotics for two years pre-raise | URI news — good |
| **URI RISE-UP** | ONR-funded ($2.5M, Aug 2026) dual-use maritime program | Direct match to Propeller's dual-use thesis | URI news — good |
| **The Continuum** | $14M NOAA-backed accelerator network (Braid Theory, Ocean Exchange, Seaworthy Collective, St. Pete Innovation District, Tampa Bay Wave, World Ocean Council, USF) | Coordinated national ocean-enterprise pipeline aligned to NOAA Ocean Enterprise | Partner sites — moderate |
| **SeaAhead / BlueSwell** | Boston bluetech incubator (~$1.2M MassCEC) | Boston-local, same city as Propeller; alumnus **atdepth MRV** won ARPA-E $2.52M. 2026 Pilot program theme: **Coastal Resilience and Coastal Asset Protection** | [sea-ahead.com](https://www.sea-ahead.com) — good |
| **Seaworthy Collective** | Ocean Enterprise Studio & Incubator (Miami) | Cohort 7 announced; focused on ocean data technologies | Public cohort announcements — good |
| **Propeller Ocean MBA** | Propeller's own founder-formation program | Produced CarbonRun and Hum.ai. Not a sourcing target for us — it *is* Propeller's channel — but essential context | [propellervc.com](https://propellervc.com/blog/oceanmba) |
| **Hatch Blue** | Global aquaculture accelerator | Only serious dedicated aquaculture accelerator; category 7 | Public cohorts — good |
| **Katapult Ocean** | Norway-based ocean impact investor/accelerator | Named as a Propeller collaborator in the Ocean Supercluster Market Solutions Platform | Public portfolio — good |
| **Activate Fellowship** | Hard-tech research-to-company fellowship | Named as a Banyu Carbon backer by Propeller | Public fellow lists — good |
| **Canada's Ocean Supercluster** | Canadian ocean industry cluster | Propeller is a direct participant; explains Nova Scotia portfolio density | Public project announcements — good |

---

## Technical conferences

Deliberately short. Included only where early-stage technical work or technical founders are plausibly visible, with a note on what is actually extractable.

| Event | Why | Categories | What is extractable |
|---|---|---|---|
| **OCEANS (MTS/IEEE)** | The primary ocean engineering technical conference; where AUV, sensing, and acoustics work is first presented | 1, 2, 3 | Published proceedings via IEEE — author affiliations reveal pre-company technical teams |
| **Ocean Sciences Meeting (AGU/ASLO/TOS)** | Largest ocean science gathering; biennial | 2, 4 | Abstract archives |
| **AGU Fall Meeting** | Ocean carbon, coastal hazards | 4, 6 | Abstract archives |
| **PacWave / marine energy technical meetings** | Where WEC developers converge; OSU-linked | 3 | Test schedules, developer lists |
| **SF Climate Week / NY Climate Week** | Propeller hosts and attends; a *known Propeller channel* | All | Panel and attendee lists — useful for knowing what they already see |
| **World Ocean Summit (Economist Impact)** | Propeller writes about it; Economist Impact is an Ocean Supercluster partner | All | Agenda and speakers |
| **Aquaculture America / Aqua** | Category 7 industry technical event | 7 | Exhibitor and abstract lists |
| **NACE/AMPP (corrosion)** | Where marine corrosion and coatings work surfaces — the non-obvious one, per taxonomy §5 | 5 | Technical program |

**Caution:** conference mining is labor-intensive and returns unstructured data. In Phase 2 this should be a *manual analyst channel*, not an automated scraper. Ranked below grant data on effort-to-signal.

---

## Explicitly excluded

| Excluded | Reason |
|---|---|
| Crunchbase / PitchBook / Dealroom as primary sources | Paywalled; and by construction they list companies *after* they are fundable — the opposite of differentiated sourcing |
| General "top 100 ocean startups" listicles | No provenance, no dates, heavy survivorship bias |
| LinkedIn scraping | Prohibited by terms of service |
| Y Combinator batch lists | Already maximally visible; zero differentiation |
| Generic university news feeds without category filters | Signal-to-noise too low to justify |
