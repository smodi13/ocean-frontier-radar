# Phase 1 Report — Decision Gate

**Prepared:** 2026-08-21 · **Status:** Phase 1 complete. **Phase 2 not started, pending review.**
All sources accessed 2026-08-21.

---

## 1. What I learned about Propeller's investment strategy

**The basics (Observed).** Founded 2022. Fund I announced at $100M, reported closed at $117M (Axios, Jan 2024). Pre-seed through Series A, "sweet spot $500K–$3M," lead or follow, reserves for pro-rata. Boston-based. Three public themes — **Industrials, Carbon, Organics**. All deals go through an IC of five investment partners; a partner must first recruit at least one colleague before diligence begins; "to invest, we must have conviction."

**Four things that matter more than the basics:**

**(a) Propeller explicitly refuses to treat the ocean as a sector.** In [The Climate Market Map](https://propellervc.com/blog/the-climate-market-map) they call it "a cross-sector catalyst for climate innovation" and map ocean technology across all seven CTVC climate sectors. In [At The Ocean's Edge](https://propellervc.com/blog/at-the-oceans-edge) they ask what the ocean's "true edges" are. **Consequence: a keyword filter on "ocean" is the wrong primary filter.** Allium (rebar), Vema (geologic hydrogen), Blue Energy (SMRs), Nexxa (industrial software), and Rewind (Black Sea biomass) would not surface from one.

**(b) The aperture has widened since launch.** 2022 language was "decarbonizing maritime industries." Current language adds **automation, robotics, surveying, inspection, insurance, materials, and adaptation/dual-use**. Three pieces of evidence: an April 2026 post stating "we have a bunch of dual-use companies in our growing portfolio already" and reporting a strong Navy demand signal; a 28 July 2026 post on ocean-sited data centers; and a **13 August 2026** post — eight days before this research — arguing for coastal heat-adaptation "pain-killers" and naming hull coatings, lubricants, buoyancy foams, cooling, and aquaculture thermal management.

**(c) Their sourcing is institutional, not opportunistic.** Formal partnerships with **five oceanographic institutions**: WHOI (founding partner, Oct 2022), then Oregon State, University of Hawai'i, UC San Diego/Scripps, and URI (Nov 2023). They run their own **Ocean MBA** converting scientists into founders — which produced CarbonRun and Hum.ai — and have hosted hackathons at WHOI with Ørsted. This is a declared sourcing surface, not a guess.

**(d) They describe the research-to-company transition as their own pattern.** From [How We Invest](https://propellervc.com/blog/how-we-invest): many portfolio companies "initially secure grants for research before launching their startup to commercialize innovations." At least **8 of 19** named portfolio companies trace to a named institution or academic founder — UW (Banyu), Caltech/USC (Calcarea), WHOI (Orpheus), MIT (Allium, Aquatic Labs), Harvard (Fleet Robotics), plus Vema's founder-authored research base.

That last point is the empirical foundation of this project. Watching grant-stage research is watching the stage Propeller says its companies come from.

---

## 2. Final sourcing taxonomy

Eight categories, each validated against a disclosed portfolio company or an explicit written Propeller statement, plus a second axis.

| # | Category | Propeller theme | Disclosed portfolio anchor |
|---|---|---|---|
| 1 | Maritime Autonomy & Robotics | Industrials | Orpheus, VATN, Fleet Robotics, Navier |
| 2 | Ocean Sensing, Data & Intelligence | Carbon + Industrials | Aquatic Labs, Hum.ai, Indeximate |
| 3 | Offshore Energy, Power & Subsea Infrastructure | Industrials | Aikido, Blue Energy, Indeximate, Vema |
| 4 | Marine Carbon & Ocean Chemistry | Carbon | Ebb, Calcarea, CarbonRun, pHathom, Banyu, Rewind |
| 5 | Marine Materials, Corrosion & Coastal Infrastructure | Industrials | Allium |
| 6 | Coastal Adaptation & Climate Risk | Industrials + Carbon | one disclosed stealth company |
| 7 | Blue Food, Aquaculture & Marine Biology | Organics | Circle Seafoods (+2 stealth) |
| 8 | Industrial & Maritime Software / Applied AI | Industrials | Nexxa, Hum.ai |

**The second axis — ocean-centrality — is what makes this operable:** `central_mechanism` · `central_environment` · `enabling_customer` · `adjacent` · `incidental`. Central and Enabling are in scope; Adjacent requires an explicit argument; Incidental is filtered and logged with a reason. This is what admits stainless-clad rebar and excludes a generic AI tool with a port logo.

Seven candidate categories were considered and **not** promoted for lack of public Propeller signal (deep-sea mining, OTEC, marine pharma, ballast water, marine spatial planning, desalination, ocean plastics). They are watch items, listed transparently in `ocean_taxonomy.md` §9.

---

## 3. The ten most useful sourcing sources

| # | Source | Why it earns its place |
|---|---|---|
| 1 | **NSF Awards API** | Free, no key, full abstracts, and `fundProgramName` isolates exactly the commercialization-track programs. The backbone of the whole system. |
| 2 | **NSF I-Corps (via that API)** | ~$50K awards funding *pre-company customer discovery*. Catches researchers 6–24 months before formation. **The single most differentiated source found.** |
| 3 | **NSF SBIR/STTR (via that API)** | Company exists and has won funding judged partly on commercial merit. Highest-precision company-discovery signal. |
| 4 | **USAspending API** | Not for finding companies — for proving customers exist. Real AUV procurements, Navy corrosion engineering contracts, biofouling test services. Names incumbents. |
| 5 | **University licensing announcements (URI, WHOI, UCSD)** | The completed transition: patent → license → company. Produced three of the five top leads. |
| 6 | **Propeller's own blog + sitemap** | 61 URLs enumerating their evolving thesis. The cheapest way to keep the taxonomy aligned with the firm. |
| 7 | **NSF PFI / Convergence Accelerator** | Larger translation awards ($550K–$5M) with explicit commercialization mandate. |
| 8 | **StartBlue (Scripps/Rady)** | Publicly enumerable cohorts of very early ocean ventures at a Propeller partner institution. |
| 9 | **OpenAlex** | Free, fast, deep. Corroborates researcher credibility — but a supporting source, never a discovery channel. |
| 10 | **ARPA-E SEA-CO2 (manual)** | $36M/11 projects aimed squarely at mCDR MRV, the sector's gating problem. Manual only — the site blocks automation. |

---

## 4. Programmatic vs. manual

**Programmatic, tested and working:**

| Source | Result |
|---|---|
| NSF Awards API | HTTP 200 · ~116 filtered records across 39 keywords · zero failures |
| USAspending API | HTTP 200 · detailed contract records |
| OpenAlex | HTTP 200 · 61,818 works in 85ms |
| arXiv | HTTP 200 (**HTTPS required**) |
| Grants.gov Search2 | HTTP 200 · hitCount 43 |
| SEC EDGAR full-text | HTTP 200 with descriptive UA (limited value — see below) |
| Propeller site + sitemap | HTTP 200 |
| URI / UCSD / StartBlue / WHOI news | HTTP 200 |

**Manual only, with reason:**

| Source | Reason |
|---|---|
| **SBIR.gov API** | **HTTP 403 Forbidden** on every variant. Not bypassed. |
| **ARPA-E** | **HTTP 403** to WebFetch and curl alike. |
| **PatentsView** | Requires a free API key (not registered in Phase 1). |
| **USPTO ODP** | **HTTP 401 Unauthorized** — key required. |
| **WHOI tech transfer** | 302 → `intranet.whoi.edu`, unreachable. Previously public listings now internal. |
| UW CoMotion, OSU TEC | Connection failed. |
| Conference proceedings | Unstructured, partly paywalled; analyst channel, not a scraper. |

---

## 5. Candidates identified

**28 real, source-backed candidates.** Every one traces to a federal award record, a university licensing announcement, or a documented program award. No fabricated entries; no Crunchbase-derived filler.

| Channel | Count |
|---|---|
| NSF I-Corps / PFI / Convergence Accelerator (pre-company) | 11 |
| NSF SBIR / STTR (company formed) | 12 |
| University spinout with executed IP license | 3 |
| Federal program / accelerator with verified award | 2 |

**11 of 28 are pre-company research projects.** That ratio is the deliberate output of the differentiated-sourcing goal, not an accident of what was easy to find.

---

## 6. The ten most interesting leads

| # | Candidate | Type | Institution / Location | Technology | Key evidence | Score |
|---|---|---|---|---|---|---|
| 1 | **ARMADA Marine Robotics** | Spinout | WHOI · MA | Single-motor asymmetric propulsion for UUVs | 2 granted US patents; 2 exclusive WHOI licenses (Jan 2025); NSF STTR $255,821 | 13 |
| 2 | **Juice Robotics** | Spinout | URI · RI | Underwater sensing/comms; "High Dive" aerial-to-underwater fibre tether | 4 URI licenses + Rogue Island Ventures investment, 1 Jul 2026 | 13 |
| 3 | **atdepth MRV** | Company | MIT · MA | GPU-based real-time ocean modelling for mCDR MRV | ARPA-E SEA-CO2 $2,524,964; Deep Sky partnership | 12 |
| 4 | **Sea-Gal Technologies** | Company | PA | High-frequency MIMO underwater acoustic comms | NSF SBIR Phase I $304,999 | 12 |
| 5 | **Hydrokinetx Corp** | Company | IA | Wave energy powering persistent ocean sensors | NSF STTR Phase I $304,950 (Jun 2026) | 11 |
| 6 | **Designer Ecosystems** | Company | VA | Submerged barriers + performance sensor platform | SBIR Phase I $301,769 → **Phase II $1,242,694** | 11 |
| 7 | **Ocean Motion Technologies** | Company | San Diego · CA | Small-scale WECs powering at-sea data collection | DOE water power engagement; StartBlue C4 | 10 |
| 8 | **Hybrid Reefs** | Spinout | Scripps · CA | CoralGuard biocide-free antifouling coating + coral biomaterials | Patent-pending; UCSD Chancellor's Innovation finalist 2026 | 10 |
| 9 | **Nexuma LLC** | Company | FL | Microbial limestone reinforcement vs. bottom-up flooding | NSF SBIR **Phase II $1,149,796** | 10 |
| 10 | **OSU autonomous subsea connection** | Pre-company | Oregon State · OR | Diver-free subsea connect/disconnect under wave motion | NSF I-Corps, **17 Aug 2026** (4 days before this research) | 9 |

Scores are **sourcing priority**, not investment judgment.

---

## 7. The five deserving deeper research

1. **ARMADA Marine Robotics** — the complete research-to-venture chain at Propeller's founding partner, with readable patents.
2. **Juice Robotics** — four licenses plus first institutional capital, seven weeks old, inside a Propeller partner's ONR-funded dual-use ecosystem.
3. **Sea-Gal Technologies** — underwater comms is the bottleneck beneath everything else and is not represented in the publicly disclosed portfolio. Thinnest evidence of the five; included for the problem, not the proof.
4. **atdepth MRV** — MRV is the gating problem in Propeller's densest theme; a picks-and-shovels position beneath a crowded capture market.
5. **Hydrokinetx** — persistent power is the constraint on ocean sensing, and the framing (power a sensor, not the grid) avoids the trap that has killed wave energy companies.

Full research cards for each are in `initial_leads.md`.

**Three of the five are enabling layers rather than applications** — comms, power, verification. Enabling layers are systematically under-sourced because nobody writes a press release about a modem.

**Near-misses:** Designer Ecosystems (best technical progression, but `MUNICIPAL_BUYER_ONLY`); Hybrid Reefs (CoralGuard antifouling may be the real asset, understated by the reef-restoration framing); Iowa State BioShield CP (a $5M award on biocide-free anticorrosion coatings — marine applicability unconfirmed).

---

## 8. Deep-dive recommendation

### Primary: **ARMADA Marine Robotics**

The only candidate where the full evidence chain is public **and** the market can be sized from public transactions rather than a cited TAM.

- **Technical diligence is possible:** two granted US patents (9,873,499; 11,990,857) disclose the actual claims.
- **Market sizing can be built:** USAspending holds real AUV procurements — Saab→NOAA $1.68M, WHOI→Navy REMUS 600 $1.99M, Teledyne spares. Bottom-up from transactions.
- **Competitive set is mappable:** Teledyne, Kongsberg, Saab, L3Harris; plus VATN and Orpheus — both Propeller companies, making adjacency analysis concrete.
- **Kill questions are sharp:** does single-motor control authority survive real sea states, and is vehicle cost or support-ship cost the binding constraint?

Chosen for evidence density, explicitly *not* for press coverage — it has comparatively little.

### Backup: **Juice Robotics**

Same structural profile with a useful contrast — it has already priced a round, so a deep dive would test syndicate and pricing dynamics. Backup rather than primary because three of its four licensed technologies are unnamed publicly and the round size is undisclosed, so the IP position cannot be fully assessed from public sources.

---

## 9. The most interesting non-obvious sourcing insight

**The best candidates in Propeller's own thesis areas do not use ocean vocabulary, and the most differentiated federal signal is the one that funds people who do not yet have a company.**

Two findings that combine into one insight:

**(a) The vocabulary problem.** Propeller's Industrials theme explicitly includes *materials*, and Allium Engineering (stainless-clad rebar) proves they buy it. But searching ocean terms will never surface the best marine-materials work, because it lives in materials science and civil engineering departments. The clearest case found: **Iowa State University holds a $4,999,999 NSF Convergence Accelerator award for BioShield CP, a microbial coating system for corrosion protection** — biocide-free anticorrosion, at a landlocked university with no oceanography department, in a state with no coastline. Marine assets are the most corrosion-exposed asset class there is, and antifouling chemistry is under regulatory pressure to move off copper. No ocean-tech list on earth contains Iowa State.

**(b) The I-Corps discovery.** NSF I-Corps awards ~$50K for a researcher to conduct structured customer discovery (~100 interviews). It is **pre-company by construction** — which means it identifies technical founders *while they are deciding whether to start a company*. Four ocean-relevant I-Corps awards were issued in the **five days** before this research (17–20 Aug 2026), including Oregon State's autonomous subsea connection work — at a Propeller partner institution, in an engineering college rather than the oceanography college, on a problem Propeller itself named in its ocean-compute post.

**And a third finding that inverts an assumption.** I queried USAspending expecting to recover the SBIR awards that SBIR.gov denied me. It returned almost no startups — instead: Saab selling NOAA an AUV for $1.68M, Vision Point Systems on Navy marine-corrosion engineering for $4.06M, Florida Institute of Technology running Navy biofouling assessments. Useless for discovery, **genuinely valuable for diligence**: it is public, transaction-level proof that a budget line exists and it names the incumbents. The correct use of a source is not always the intended one.

---

## 10. Source-access and data-quality problems

**Access failures (all documented, none bypassed):**

| Problem | Consequence |
|---|---|
| **SBIR.gov API — HTTP 403** | The biggest hole. Navy, NOAA, and DOE SBIR recipients are badly under-represented — exactly where Propeller's dual-use interest would show up. **Phase 2's highest-value data task.** |
| **ARPA-E — HTTP 403** | SEA-CO2 (mCDR MRV) reachable only via secondary sources. |
| **PatentsView / USPTO — key required** | No systematic IP evidence. The ARMADA patents were sourced from press, not a patent database — unacceptable long-term for a project premised on research→IP→spinout. |
| **WHOI tech transfer → intranet** | Propeller's founding partner's technology listings are no longer public. A genuine regression. |
| **UW CoMotion, OSU TEC — connection failed** | Two partner institutions' TTOs unreachable. |

**Data-quality problems:**

1. **Keyword precision is poor.** NSF full-text keyword search yielded **~20%** relevant among SBIR/STTR hits and **~28%** among translation-program hits. False positives are biomedical "vessel," ultrasound "acoustic," incidental "harmful algal." Retrieval is cheap; **classification is the real work** — and the right place for AI assistance with sources retained.
2. **Missing dates.** Several Propeller "Meet …" posts carry no publication date, so portfolio investment timing is partly unknown.
3. **Ambiguous portfolio boundary.** Fleetzero and Ness Sea are named in Propeller's own writing among dual-use portfolio companies but absent from the portfolio page. Not resolved; not treated as confirmed portfolio.
4. **Six stealth companies.** Disclosed as covering ocean carbon capture, climate forecasting, seafood traceability, seafood processing, nuclear, and coastal adaptation. This is a hard limit on any adjacency claim, and is why the phrasing throughout is *"not represented in the publicly disclosed portfolio reviewed."*
5. **Geographic bias.** No systematic access to Canadian, EU, UK, or Norwegian award data — notable given two Nova Scotia portfolio companies and Propeller's Ocean Supercluster participation.
6. **`propellervc.com/team` returns 404** and is absent from the sitemap; current IC composition is unknown.

---

## 11. Recommended Phase 2 architecture

**Deliberately boring. The research is the hard part; the plumbing should not be.**

```
  NSF API ─┐
USAspending├─→ harvest/*.py ─→ raw JSON ─→ classify ─→ SQLite ─→ Next.js (static export) ─→ Vercel
 OpenAlex ─┤     (curl)        (data/,      (AI-assist   (7 tables,     read-only
   arXiv  ─┘                  gitignored)   + human)     evidence-first)
```

**Ingestion.** Python, one module per source, each emitting a normalized record with `source_url`, `accessed_date`, and raw payload retained. Run on demand and via a weekly GitHub Action. No orchestration framework — these are cron-shaped jobs.

**Storage.** **SQLite**, one file, foreign keys on, committed alongside the code. Seven tables per `evidence_model.md`: `candidate`, `source`, `evidence`, `person`, `assessment`, `diligence_question`, `score_component`. At the plausible ceiling — thousands of candidates, tens of thousands of evidence rows — nothing more is justified, and a single inspectable file keeps provenance auditable.

**No vector database.** Keyword + program filtering plus human review handled 116 records well. Revisit only if volume genuinely demands it.

**Classification — the one place AI belongs.** Given an award abstract, propose: category, ocean-centrality, and a one-line technology summary. Written as `evidence.extraction_method = 'ai_extracted'` and `assessment.author = 'ai_assisted'`, always rendered beside the source text. Given the measured ~20–28% precision, this is where the leverage is — and it must remain reviewable, because the analyst job posting asks candidates to disclose AI use.

**Frontend.** Next.js + TypeScript, **statically exported** from the SQLite file at build time, deployed to Vercel. No server, no API routes, no database connection from the browser. The dataset is small and updates weekly; static export makes the whole thing auditable and free to host.

**Citations.** Every displayed claim renders as a claim + source link + accessed date. A claim with no `source_id` cannot render — enforced at build time, so the site cannot ship an unsourced assertion.

**Automated vs. analyst-reviewed:**

| Automated | Analyst-reviewed |
|---|---|
| Retrieval, dedupe, normalization | Ocean-centrality tag (the judgment call) |
| Program-type filtering | All five score dimensions |
| Recency/state-change detection | All flags |
| Draft category + technology summary | Diligence and kill questions |
| Link health, source archiving | Anything entering a memo |

**Phase 2's first task is not code.** It is closing the SBIR.gov gap and registering a PatentsView key. The pipeline is worth little if it can only see NSF.

---

## 12. Where I think you may be approaching this incorrectly

Five honest observations. You asked for them.

**1. "20–30 leads" is the wrong success metric, and the brief half-knows it.** You said you would rather have 22 excellent leads than 200 shallow ones — correct. But the deeper issue is that *lead count* measures the wrong thing. What would actually impress a Propeller partner is **one non-obvious, well-argued sourcing insight** plus a working method. The Iowa State finding — a $5M biocide-free anticorrosion award at a landlocked university — says more about your thinking than 28 rows do. Consider making the *insight* the headline deliverable and the leads the supporting evidence.

**2. There is a real tension between "differentiated sourcing" and "verifiable evidence," and it should be named rather than resolved.** The genuinely earliest signals — a professor deciding to spin out, an unpublished result — are by definition unverifiable from public sources. Everything this system can see is already at least *somewhat* public. So the honest claim is not "we find what nobody sees"; it is **"we find what is public but unread, faster and more systematically than a human scanning press releases."** That is a defensible and genuinely useful claim. Overclaiming here would be the fastest way to lose credibility with a technical investor.

**3. Phase 4's financial model is the weakest planned deliverable, and I would consider cutting it.** A DCF or unit-economic model for a pre-revenue, pre-product company with two patents is a spreadsheet of assumptions. Every experienced investor knows this. A **bottom-up market model built from actual USAspending procurement transactions** — real AUV purchases at real prices — would be far more credible and far more unusual. The job posting asks for financial modeling, so build *something*; just make it the defensible kind.

**4. Building this for Propeller specifically carries a risk worth weighing.** The taxonomy is tuned to their public themes, which makes it a strong signal of genuine interest — but it also means a partner may reasonably ask "what would you have found if you weren't fitting our thesis?" Keeping the seven rejected categories (`ocean_taxonomy.md` §9) visible partly answers this. You might also consider surfacing **one candidate that does not fit Propeller's thesis but that you believe in anyway** — independent view formation is explicitly in the job description, and demonstrating it is worth more than perfect alignment.

**5. Do not build the polished site until the data is right.** You were right to defer it. But the pull toward Phase 3 will be strong because it is the visible part. The uncomfortable truth from Phase 1 is that the **SBIR.gov 403 and the missing patent data are more consequential than any UI decision** — a beautiful interface over NSF-only data is a beautiful interface over a partial picture. Fix the sources first.

**One thing you got notably right:** insisting on Observed/Inferred/Unknown from the start. It changed how the research was actually conducted, not just how it was written up — several claims I would otherwise have asserted casually ended up correctly tagged `[Unknown]`, including the Fleetzero/Ness Sea portfolio ambiguity, which a less disciplined process would have silently resolved the wrong way.

---

## 13. Files created

```
ocean-frontier-radar/
├── README.md                              Project overview, phases, principles
├── .gitignore                             Excludes data/, secrets, caches, OS files
├── research/
│   ├── propeller_thesis.md                Firm dossier — 19-company portfolio map, process, sourcing
│   ├── ocean_taxonomy.md                  8 categories + ocean-centrality axis + search vocabulary
│   ├── sourcing_universe.md               20 institutions, funders, programs, conferences
│   ├── data_sources.md                    Empirical access testing of 20 sources
│   ├── evidence_model.md                  7-table schema separating fact from inference
│   ├── prioritization_framework.md        5-dimension sourcing score + 10 structural flags
│   ├── initial_leads.csv                  28 candidates × 25 fields
│   ├── initial_leads.md                   Narrative + 5 research cards + deep-dive recommendation
│   └── phase1_report.md                   This document
├── sources/
│   └── source_registry.csv                20 sources × 18 fields with tested access status
└── src/harvest/
    ├── nsf_sbir_harvest.py                NSF SBIR/STTR harvester
    └── nsf_translation_harvest.py         NSF I-Corps/PFI/Convergence harvester
```

---

## 14. Test and validation status

Phase 1 was research, not software, but two harvest utilities were written and are committed.

| Check | Result |
|---|---|
| `python3 -m py_compile` on both harvesters | ✅ Pass |
| Live API smoke test (NSF fetch + SBIR filter) | ✅ Pass — 25 records returned, 2 SBIR matches |
| Full NSF SBIR/STTR harvest | ✅ 69 records across 39 keywords, 0 request failures |
| Full NSF translation-program harvest | ✅ 47 records across 24 keywords, 0 request failures |
| `initial_leads.csv` structure | ✅ 28 rows × 25 columns, no ragged rows |
| `source_registry.csv` structure | ✅ 20 rows × 18 columns, no ragged rows |
| Every lead has ≥1 source URL | ✅ Verified |
| Endpoint reachability tests | ✅ 20 sources tested; results recorded including all failures |

**No unit tests.** For two scripts that are thin wrappers over one HTTP call, tests would be ceremony. Phase 2's classification layer is where tests will genuinely matter — that is where correctness is non-obvious.

**Known defect, disclosed:** the harvesters shell out to `curl` because Python's `urllib` failed certificate verification under local TLS interception. This works but is not good practice; Phase 2 should use `requests` with a `certifi` CA bundle. Disabling verification would have been the wrong fix and was not done.

---

## 15. Git commit hash

See section below — recorded at commit time.

---

## Decision gate

**Phase 1 is complete. Phase 2 has not been started and will not be started without your review.**

The three questions I would most like your direction on:

1. **Is closing the SBIR.gov / patent-data gap worth doing before any pipeline work?** My view: yes, and it is not close.
2. **Should the deep dive proceed on ARMADA, or would you rather I widen sourcing first?** More leads or deeper on one — a genuine fork.
3. **Do you want the "one candidate that does not fit Propeller's thesis" addition from §12.4?** It is a deliberate risk with a real upside.
