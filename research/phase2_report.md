# Phase 2 Report — Decision Gate

**Prepared:** 2026-08-21 · **Status:** Phase 2 complete. **Phase 3 not started, pending review.**
SBIR bulk file downloaded 2026-08-21. All API sources accessed 2026-08-21.

Phase 2 turned the Phase 1 research process into a working pipeline: `SBIR bulk + NSF API + USAspending + OpenAlex + curated primary sources → rules classifier → SQLite → scored, exported candidate universe`. Everything below is reproducible with `python3 src/ofr/pipeline.py --full`.

---

## 1. Source records ingested

| Module | Records seen | Records kept | Status |
|---|---:|---:|---|
| **SBIR/STTR bulk** (`data.www.sbir.gov`) | 207,731 | 1,189 | ok |
| **NSF Awards API** | 3,312 | 81 | error (1 keyword failed, logged) |
| **USAspending** (procurement) | 306 | 306 | ok |
| **Curated primary sources** | 6 | 6 | ok |
| **OpenAlex** (corroboration only) | 6 | 1 | ok |

**Database totals:** 562 candidates · 1,396 evidence records · 1,500 sources · 877 people · 306 procurement rows · 32 analyst views · 43 possible relationships.

**Source quality:** 1,495 tier-1 (government awards, university announcements, procurement records), 5 tier-2 (trade press). **Zero tier-3 sources were ingested** — Crunchbase/PitchBook figures encountered during verification were read but deliberately not written to the database, consistent with the Phase 1 decision.

The NSF `error` status is one keyword returning malformed JSON. It is recorded in `ingest_log` with its message rather than swallowed — the "fail visibly" requirement working as intended.

---

## 2. Unique candidates after entity resolution

**562 candidates retrieved.** Entity resolution applied 0 merges in the final run and recorded **43 possible relationships** for analyst review.

Zero merges is the correct outcome, not a bug: deterministic `candidate_id` generation collapses name variants at write time (`ARMADA Marine Robotics`, `ARMADA Marine Robotics, Inc.` and `Armada Marine Robotics LLC` all produce `armada-marine-robotics`), so duplicates never enter the table. The merge path exists for the cases identity normalisation cannot catch — shared website domains and shared award identifiers.

**Nothing is merged on similarity.** `apply_merges` raises `ValueError` on any basis outside `identical_normalized_name`, `shared_website_domain`, `shared_award_id`, and every merge is written to `merge_log`. Uncertain links become `possible_relationships` rows (`shares_person`, `shares_institution`) for a human to adjudicate.

### The qualified universe

562 is the *retrieved* universe. The actionable set excludes firms the pipeline itself identifies as too mature:

| Filter | Count |
|---|---:|
| Retrieved | 562 |
| Less `ESTABLISHED_FIRM` / `ESTABLISHED_SBIR_CONTRACTOR` | 277 |
| **Qualified: not established AND priority ≥ 10** | **198** |
| Priority ≥ 11 | 121 |
| Priority ≥ 12 | 64 |
| Priority ≥ 13 | 9 |

The brief targeted 50–75 and allowed ~90 if quality held. **198 at ≥10 is more than that, and I do not claim all 198 are strong.** The defensible band is the 121 at ≥11; the genuinely differentiated set is far smaller, and §16 explains why the framework cannot rank the middle of this distribution.

---

## 3. Breakdown by type

Qualified set (198):

| Type | Count |
|---|---:|
| Company | 182 |
| Research project (pre-company) | 12 |
| Spinout | 4 |

Full retrieved universe (562): 543 companies, 15 research projects, 4 spinouts.

**This ratio is the single biggest disappointment of Phase 2.** Phase 1's most differentiated signal was NSF I-Corps — pre-company researchers doing customer discovery. The pipeline retrieved only 26 I-Corps awards, and pre-company candidates are 6% of the qualified set versus 39% in Phase 1's hand-built sample. The SBIR bulk file is 200,000 company records and it swamps everything else numerically. Addressed in §14 and §20.

---

## 4. Breakdown by taxonomy

Qualified set (198):

| Category | Count |
|---|---:|
| Marine Materials, Corrosion & Coastal Infrastructure | 54 |
| Blue Food, Aquaculture & Marine Biology | 51 |
| Maritime Autonomy & Robotics | 29 |
| Offshore Energy, Power & Subsea Infrastructure | 24 |
| Ocean Sensing, Data & Intelligence | 22 |
| Coastal Adaptation & Climate Risk | 11 |
| Marine Carbon & Ocean Chemistry | 4 |
| Industrial & Maritime Software / Applied AI | 3 |

**Marine materials is the largest category, and that is the Phase 1 thesis confirmed.** It was the category argued to be structurally under-sourced because the work never uses ocean vocabulary. Given a problem-first lexicon, it produces the most candidates of any category.

**Marine carbon produces 4.** Propeller's densest disclosed theme is the thinnest in this universe. That is a real finding about where federal money flows, not a defect — see §12.

---

## 5. Breakdown by ocean centrality

| Level | Qualified (198) | All retrieved (562) |
|---|---:|---:|
| `central_mechanism` | 108 | 202 |
| `primary_end_market` | 53 | 244 |
| `strong_adjacency` | 37 | 116 |
| `incidental` | 0 (filtered) | 0 (filtered) |

`incidental` records are classified and logged in `classifications`, then excluded from the candidate table — the rejection is retained and auditable rather than silently dropped.

The 37 `strong_adjacency` candidates are the hidden-adjacency population: technologies solving problems acute in ocean-exposed industries that never mention the ocean. Getting this class *right* was the hardest engineering problem in Phase 2 (§16).

---

## 6. How much the SBIR/STTR data changed the universe

**Decisively.** It is the difference between a hand-built list and a sourcing system.

| | Phase 1 | Phase 2 |
|---|---:|---:|
| Candidates | 28 | 562 retrieved / 198 qualified |
| Agencies represented | NSF only | 10 |
| Navy/DoD-funded candidates | 0 | 677 records |
| NOAA/Commerce-funded candidates | 0 | 88 records |
| DOE-funded candidates | 0 | 216 records |

Phase 1 stated the SBIR.gov API 403 was the biggest hole, and specifically that it hid the Navy dual-use candidates Propeller says it likes. That is now closed: **DoD is the single largest source of candidates in the universe (677 records), and Navy is its largest branch.**

Concrete examples invisible to Phase 1 and now present:
- **3newable LLC** — DOE SBIR Phase II ($1,149,047) for preventing biofouling of oceanographic sensors, with WHOI as its STTR research-institution partner. **Now the #3 candidate overall.**
- **Blue Ocean Gear**, **CoastalOceanVision**, **Ocean's Balance** — all NOAA SBIR Phase I→II progressions in ocean sensing and blue food.
- **X-Hab 3D** — DARPA-funded 3D-printed artificial reef materials with Penn State.

### The critical caveat

**The SBIR bulk file effectively ends in 2023.** It contains 5,410 awards dated 2023 and only 24 dated 2024, against a current date of August 2026. It buys *cross-agency breadth*, not recency.

This is why both sources are ingested and why they are genuinely complementary: SBIR bulk gives ten agencies through 2023; the NSF API gives one agency through last week. The `timing` score exposes the split directly — nearly every SBIR-only candidate scores 0 or 1 on timing while NSF-sourced candidates score 2.

---

## 7. The 15 highest-priority candidates

Components are `Technical / Commercial / Timing / Venture / Propeller / Differentiated` (max 3/3/2/3/3/3 = 17).

**Ranks 1–9 are the complete machine ranking at ≥13.** Ranks 10–15 are selected by me from the 64-way tie at 12; that selection is analyst judgment, stated openly, not a machine result (§16).

| # | Candidate | Origin / source | Technology | Category | Maturity | Sourcing signal | Components | Total | Why interesting |
|---|---|---|---|---|---|---|---|---:|---|
| 1 | **ARMADA Marine Robotics** | WHOI spinout; DoD + NSF STTR | Single-motor asymmetric propulsion for UUVs | Maritime autonomy | Pre-seed, 8 staff | **Pre-company** | 3/2/1/3/3/3 | **15** | Two granted US patents, two exclusive WHOI licences, multi-agency validation, ~$290K raised — the complete research→IP→licence→company chain at Propeller's founding partner |
| 2 | **Juice Robotics** | URI spinout | Air-to-water fibre-optic tether ("High Dive"), subsea sensing/comms | Maritime autonomy | Seed | Emerging | 3/2/2/3/3/2 | **15** | Four URI licences plus first institutional round, July 2026, inside URI's ONR-funded dual-use ecosystem |
| 3 | **3newable LLC** | DOE SBIR II; WHOI STTR partner | Wave-energy-powered UV-C anti-biofouling for ocean sensors | Marine materials / sensing | Seed | Emerging | 3/2/2/2/3/2 | **14** | Attacks *both* gating constraints on persistent ocean sensing — power and biofouling; two field deployments on WHOI's OOI array; independent PNNL testing with published performance data |
| 4 | **Certus Core, Inc.** | DoD SBIR (SOCOM) | Semantic knowledge graph; AI-driven swarming AUVs | Maritime autonomy | Emerging | Emerging | 3/2/1/2/3/2 | **13** | AUV swarm autonomy for special operations; **but see §16 — ocean centrality is likely overstated by the classifier** |
| 5 | **Designer Ecosystems LLC** | NSF SBIR I→II | Submerged barriers plus performance sensor platform | Coastal adaptation | SBIR Phase II | Emerging | 2/2/2/2/3/2 | **13** | Full Phase I→II progression; pairs structure with measurement, unusual in nature-based coastal protection |
| 6 | **Grow Oyster Reefs, LLC** | NSF SBIR I→II | Biomimetic moulds for mass-produced reef substrate | Blue food / materials | SBIR Phase II | Emerging | 2/2/2/2/3/2 | **13** | The innovation is the *manufacturing method*, which is what turns restoration into a product |
| 7 | **NEXUMA L.L.C.** | NSF SBIR I→II | Microbial limestone reinforcement against bottom-up flooding | Marine materials | SBIR Phase II | Emerging | 2/2/2/2/3/2 | **13** | Addresses a failure mode seawalls do not solve, in the most exposed US coastal market |
| 8 | **Ocean Motion Technologies** | DOE SBIR I→II | Small-scale WECs powering at-sea data collection | Maritime autonomy | SBIR Phase II | Emerging | 3/2/1/2/3/2 | **13** | Same persistent-power thesis as 3newable, further along — the natural comparator for whether small-WEC economics close |
| 9 | **X-HAB 3D, INC.** | DARPA SBIR I→II (3rd-year option) | 3D-printed carbon-neutral concrete for artificial reefs / coastal protection | Coastal adaptation | SBIR Phase II | Emerging | 3/2/1/2/3/2 | **13** | Penn State materials partnership; DARPA extended into a third year — a defence-funded route into coastal infrastructure materials |
| 10 | **Hydrokinetx Corporation** | NSF STTR I (Jun 2026) | Wave energy for persistent ocean-sensor power | Offshore energy | Pre-seed | Emerging | 2/2/2/1/3/2 | 12 | Most recent award in the top tier; avoids the grid-scale trap that has killed wave energy companies |
| 11 | **WaveArray Antifouling Systems** | NSF SBIR I→II | Electronic, biocide-free antifouling for ship hulls | Marine materials | SBIR Phase II | Emerging | 3/2/0/2/3/2 | 12 | Biocide-free antifouling in a market under regulatory pressure to leave copper chemistry; Propeller has written about hull coatings |
| 12 | **Frontline Biotechnologies** | USDA SBIR I→II | Sorbent technology for eDNA collection, aquaculture disease detection | Ocean sensing | SBIR Phase II | Emerging | 3/2/0/2/3/2 | 12 | Aquaculture disease detection is not represented in the publicly disclosed Propeller portfolio reviewed |
| 13 | **Blue Ocean Gear Inc.** | NOAA SBIR I→II | Smart buoys tracking fishing gear | Blue food | SBIR Phase II | Emerging | 3/2/0/2/3/2 | 12 | A NOAA-funded company structurally invisible to Phase 1; lost-gear tracking has both an economic and a regulatory driver |
| 14 | **CoastalOceanVision, Inc** | NOAA SBIR I→II | Ocean optical sensing | Blue food / sensing | SBIR Phase II | Emerging | 3/2/0/2/3/2 | 12 | Based in North Falmouth, inside the Woods Hole cluster |
| 15 | **Sea-Gal Technologies** | NSF SBIR I (Apr 2025) | High-frequency MIMO underwater acoustic comms | Ocean sensing | Pre-seed | Emerging | 2/2/1/1/3/2 | 11 | Phase 1 top-five; underwater bandwidth is the enabling layer beneath the rest of the taxonomy |

---

## 8. The final top five

1. **ARMADA Marine Robotics** — 15
2. **Juice Robotics** — 15
3. **3newable LLC** — 14
4. **Designer Ecosystems LLC** — 13
5. **X-Hab 3D, Inc.** — 13

Selected over the other 13s on judgment: **Certus Core** is excluded because its core business is a defence data platform and the ocean application looks incidental; **Grow Oyster Reefs** and **Nexuma** are excluded in favour of Designer Ecosystems and X-Hab 3D, which pair structures with measurement and with a defence-funded materials programme respectively; **Ocean Motion Technologies** is excluded as the weaker of the two persistent-power candidates relative to 3newable.

Notable: **three of the five come from sources Phase 1 could not access.**

---

## 9. Does ARMADA remain #1?

**Yes — but it was genuinely contested, and it moved for a reason.**

ARMADA scored 13 in Phase 1 and scores **15** now. The increase came from the `differentiated_sourcing` dimension added in Phase 2 (3/3, pre-company) and from `venture_potential` rising to 3 once granted patents plus executed exclusive licences were both present in the evidence table.

Re-verification (Step 12), all against public sources:

| Check | Result |
|---|---|
| Company identity | Confirmed. Founded 2019, East Falmouth MA, ~8 staff. |
| WHOI relationship | Confirmed. Two exclusive licence agreements executed Jan 2025; founders Robin Littlefield and Jeff Kaeli are WHOI engineers. |
| Patents | Confirmed. Asymmetric Propulsion **US 9,873,499**; Rotational Feedback Control **US 11,990,857**. |
| SBIR/STTR | Confirmed. NSF STTR Phase I **$255,821** with WHOI. Additional DoD and NOAA award records present in the SBIR bulk data. |
| Technical claim | Consistent across WHOI, trade press and the company site: thrust and steering from one motor, no fins. |
| Commercialization evidence | **Weak.** No named customer, pilot, or unit volume in any public source. |
| Current stage | Pre-seed. Aggregator profiles indicate roughly $290K raised across four rounds, latest an accelerator round Mar 2025. *Tier-3 source, not ingested; treat as indicative only.* |
| Portfolio adjacency | Propeller holds two AUV companies (Orpheus, VATN). ARMADA is a **propulsion component** play, not a vehicle play — complementary or competitive is a real open question. |

**The serious challenger was 3newable**, and on one axis it is better: it has *published independent performance data* (PNNL testing under DOE's TEAMER programme, plus reported field output of 0.91 W average against a 7–8 W target). Nobody publishes numbers like that about ARMADA.

ARMADA stays ahead on: granted patents whose claims can actually be read; a cleaner pre-seed stage fit against Propeller's $500K–$3M model; and a market whose demand side is measurable from public procurement (§13).

---

## 10. Recommended for Phase 3 deep diligence

### Primary: **ARMADA Marine Robotics**

Unchanged from Phase 1, now on stronger evidence. The reasoning is unchanged too: it is the candidate where the technical claim is publicly readable (two granted patents), the market can be sized bottom-up from real transactions rather than a cited TAM, the competitive set is enumerable, and the kill questions are sharp and answerable with a handful of expert calls.

### Backup: **3newable LLC**

Promoted over Juice Robotics. Rationale: 3newable has *published quantitative performance data including a shortfall against its own target*, which is unusually good material for technical diligence — and the gap between 0.91 W measured and 7–8 W expected is exactly the kind of question a technical investor should want to resolve. Juice Robotics remains strong but three of its four licensed technologies are undisclosed and its round size is unpublished, so more of its diligence depends on founder access.

---

## 11. Interesting, But Not a Clear Propeller Fit

### **LumiShield Technologies** (Pittsburgh, PA) — priority 12, `strong_adjacency`

**Why the technology is interesting.** LumiShield, a Carnegie Mellon and NETL spinout, developed an aqueous electroplating process depositing aluminium-rich coatings on steel, forming a hard, self-healing aluminium oxide layer. It targets displacement of hexavalent chromium plating. Aqueous aluminium deposition is a genuinely hard electrochemistry problem, and the regulatory driver is real: hexavalent chromium is a known carcinogen under sustained regulatory pressure. Evidence: NSF SBIR Phase II ($741,257) plus multiple Air Force SBIR awards.

**Why a generic deep-tech investor might investigate.** A validated, cheaper, less toxic replacement for a large entrenched plating market, with regulatory tailwind, defensible process IP, and a clear industrial buyer. That is a conventional advanced-materials venture thesis.

**Why I would not force it into Propeller's thesis.** The ocean is not the mechanism, the operating environment, or the primary customer context. LumiShield's disclosed markets are aerospace, defence and general industrial plating; marine corrosion is one application among many and is not what the company sells against. Its awards come from the Air Force, not the Navy. Founded 2014, roughly $997K raised over six rounds — twelve years in, likely past Propeller's pre-seed-to-Series-A window. Calling this an ocean company would be exactly the "forcing generic technology into an ocean thesis" error the centrality axis exists to prevent.

**What evidence would change that view.** A marine-specific qualification programme (seawater immersion data, class-society or NAVSEA approval); named offshore, subsea or marine-infrastructure customers; a Navy rather than Air Force award; or a deliberate repositioning toward offshore assets. Any of those would move it from `strong_adjacency` to `primary_end_market` and make it a legitimate candidate.

**It received no score boost for being a boundary case.** Its 12 comes from the same rules as everything else, and its `propeller_relevance` is 2 rather than 3 precisely because centrality is adjacency, not centrality.

---

## 12. Three strongest non-obvious sourcing insights

### (a) Federal money flows in almost exactly the inverse of venture attention

Propeller's densest disclosed theme is marine carbon — six of nineteen named portfolio companies. It is also the best-covered corner of ocean venture. In this universe, marine carbon yields **4 qualified candidates** and, in procurement, **one federal contract worth $58,350**.

Marine materials — the category Phase 1 argued was structurally under-sourced — yields **54 qualified candidates** and **$107M in observed recurring federal contracts** across Air Force, Navy and Army.

So the category with the most venture competition has almost no government demand signal, and the category with the least venture attention has a large, recurring, multi-agency budget line. Both facts are independently checkable, and together they say something sharper than either alone: **federal R&D funding and venture attention are not correlated in ocean technology, and the gap between them is where differentiated sourcing lives.**

### (b) NOAA buys survey services, not sensors — which reframes who ocean-data startups sell to

Ocean sensing procurement is 56 contracts, $256M observed, median $4.69M. NOAA is the buyer on **46 of 56**. But the top suppliers are Ocean Surveys Inc., eTrac/Woolpert and TerraSond — **survey service firms, not instrument makers.**

The implication for any ocean-data startup is uncomfortable and useful: the largest civilian ocean-data buyer procures *survey outcomes*, not hardware. A sensor company selling to NOAA is selling a component into a services value chain it does not control. That reframes the "is this a data company or an instrument company?" question flagged in Phase 1 — the answer may be that neither sells directly to the biggest buyer.

### (c) The pipeline's own recall bugs were the sharpest lesson

Two defects, both found by testing the system against Phase 1's hand-built list rather than by admiring the output:

1. **Plural forms did not match.** The lexicon term `underwater acoustic communication` failed against the phrase "Underwater Acoustic Communications". That single missing `s` silently dropped **Sea-Gal Technologies**, a Phase 1 top-five candidate, out of the universe entirely.
2. **The Stage A gate rejected single direct-term hits.** One direct term scores 3; the gate was 4. **Hydrokinetx** — also Phase 1 top-five — was excluded for matching "marine energy" and nothing else.

The lesson generalises: **a sourcing system's failures are invisible from its output.** A list of 562 plausible candidates looks like success whether or not it is missing the best ones. The only way these surfaced was holding a previously hand-built list as a regression fixture. Both are now regression tests (`test_plural_terms_match_singular_lexicon_entries`, `test_single_direct_term_passes_stage_a`).

---

## 13. Procurement evidence useful for bottom-up market sizing

From 306 contracts, reusable via `theme_demand_summary()`. **This is evidence that budgets and buying behaviour exist. It is not a market size estimate.**

| Theme | Contracts | Total observed | Median | Max | Dominant buyer | Incumbent suppliers | Recurring |
|---|---:|---:|---:|---:|---|---|---|
| **Maritime autonomy** | 87 | $244.8M | $441K | $41.6M | Navy (34), DLA (27), NOAA (9) | W S Darley (24), UT Austin (7), **WHOI (5)** | Yes |
| **Ocean sensing** | 56 | $256.4M | $4.69M | $12.0M | **NOAA (46)** | Ocean Surveys (9), eTrac/Woolpert (7), TerraSond (6) | Yes |
| **Marine materials** | 66 | $107.0M | $1.36M | $6.20M | Air Force (23), Navy (22), Army (13) | Corrpro (10), Pond & Co (7), Excet (3) | Yes |
| **Coastal adaptation** | 28 | $61.0M | $573K | $20.4M | Army (10), Navy (6) | Swift River Versar JV (3) | Yes |
| **Blue food** | 50 | $32.8M | $200K | $4.82M | USDA ARS (19), NOAA (17) | Center for Aquaculture Technologies (8) | Yes |
| **Offshore energy** | 18 | $30.2M | $1.23M | $6.65M | Navy (11) | **University of Washington (6)** | Yes |
| **Marine carbon** | 1 | $58K | $58K | $58K | NOAA (1) | Sunburst Sensors (1) | **No** |

**Directly usable for the ARMADA deep dive:** maritime autonomy shows 87 contracts, $244.8M observed, a $441K median and a $41.6M maximum, with the Navy as dominant buyer and repeat purchasing across multiple years. A bottom-up model can be built from actual transactions. Note WHOI itself appears as a *supplier* on five contracts — an incumbent that is also ARMADA's licensor.

**Two cautions I would attach to any use of this table.** These are keyword-search samples, not exhaustive extracts, so totals are lower bounds on observed spend within the sample and say nothing about the commercial market. And "recurring" only means contracts appear in three or more distinct years.

---

## 14. Biggest remaining data gaps

1. **SBIR bulk recency (worst gap).** The file ends in 2023. Every non-NSF candidate is at least two and a half years stale, which is why so many score 0 on timing. Whether SBIR.gov refreshes this file needs re-checking; if not, the agency-breadth advantage decays every month.
2. **Pre-company coverage collapsed.** 6% of the qualified set versus 39% in Phase 1. I-Corps and PFI are the highest-differentiation signal and they are numerically drowned by 200,000 SBIR company records. This needs a *separate pre-company queue*, not a shared ranking.
3. **Patents still absent.** PatentsView and USPTO ODP both require keys, still not registered. ARMADA's two patents came from a press release. For a system premised on research→IP→spinout, this remains the most conspicuous structural hole.
4. **ARPA-E still 403.** atdepth MRV's $2.52M award had to be curated by hand, and its missing award date costs it 2 timing points — which is why a genuinely strong candidate scores only 10.
5. **No non-US coverage.** No Canadian, EU, UK or Norwegian award data — notable given two Nova Scotia portfolio companies and Propeller's Ocean Supercluster participation.
6. **University licensing still manual.** WHOI's tech transfer remains behind an intranet; ARMADA, Juice Robotics and Hybrid Reefs all required hand curation.
7. **No company-formation or financing feed.** SEC Form D was assessed in Phase 1 as confirmation-only, and nothing fills the gap between "won a grant" and "raised a round".

---

## 15. Sources that proved too noisy or unreliable

- **SBIR bulk keyword retrieval, before tuning.** At the loosest threshold it returned 1,823 records and admitted nuclear reactor components, industrial heat storage and Air Force building repainting as "marine materials" on a single incidental "corrosion". Precision was restored by requiring either two distinct direct terms or three total mentions (§16).
- **OpenAlex — genuinely disappointing in practice.** 6 works examined, **1 evidence record added**. The author-verification step (surname must appear in the authorship list) rejected nearly everything, because company PIs from SBIR records are frequently not academic publishers. Its Phase 1 role — corroborating researcher credibility — only works for candidates with *academic* founders, which is a minority here. It should be retargeted at pre-company/I-Corps candidates or dropped.
- **USAspending for discovery — confirmed useless, as expected.** 306 records, zero candidates. Retained purely as demand-side evidence, which is where it is genuinely strong.
- **`maritime_software` category — 3 qualified candidates from 562.** Either the category is real and this lexicon cannot retrieve it, or it does not generate federally-funded early-stage companies. I suspect the former: maritime software companies come from industry, not grants, and this pipeline is grant-shaped.

---

## 16. Evidence the prioritization framework is producing bad rankings

**Yes, in three specific and reportable ways.**

### (a) It cannot rank the middle of the distribution

**64 candidates tie at exactly 12** and 121 sit at ≥11. Beyond rank 9 the ranking degenerates to alphabetical order. With six integer dimensions and a 17-point ceiling there is not enough resolution to separate 64 similar SBIR Phase II companies, because they genuinely share a profile: Phase II technical evidence (3), commercialization funding (2), stale timing (0), inferred venture potential (2), central mechanism (3), emerging (2).

This matters because **the ranking is only trustworthy at the top**. Ranks 10–15 in §7 are my selection from a tie, and I have said so rather than presenting them as machine output.

### (b) Timing is dominated by a source artifact, not by the candidates

Timing is effectively a proxy for *which source found the candidate*. SBIR-bulk candidates cannot score above 1 because the file ends in 2023; NSF candidates routinely score 2. **Hydrokinetx (NSF, Jun 2026) outranks WaveArray (NSF Phase II, 2022) partly on data freshness rather than on anything about the companies.** The dimension is measuring the pipeline, not the world.

### (c) Missing dates silently penalise the best-documented candidates

**atdepth MRV scores 10** — below dozens of routine SBIR companies — despite a $2,524,964 ARPA-E award, an MIT origin and a named commercial partner. Two causes: ARPA-E publishes no machine-readable award date, so timing scores 0; and `commercialization_grant` sits in the tier-1 technical bucket, so a $2.5M ARPA-E award scores *lower* on technical evidence than a $250K SBIR Phase II. **Hybrid Reefs (10) is penalised the same way.** The framework rewards *evidence that happens to be well-structured*, which is not the same as strong evidence.

### (d) Ocean centrality is over-assigned in defence records

**Certus Core ranks 4th** on an AUV-swarming SBIR, but its core business is a semantic knowledge graph for Air Force data. Defence abstracts are written to hit many capability keywords, so they trip the classifier's ocean-centrality logic more readily than they should. A defence-specific rule — requiring the ocean terms to appear in the *title* as well as the abstract — would likely fix it.

### What I would change before trusting this ranking further

Split the queue by source and stage rather than pooling everything; make timing relative to each source's own recency ceiling; move `commercialization_grant` into the strong technical tier when the amount exceeds $1M; and treat the middle band as an unranked pool for analyst triage rather than an ordered list.

---

## 17. Automated tests

**59 tests, all passing, none requiring network access.**

```
tests/test_identity.py                8   deterministic ids, legal-suffix and accent
                                          normalisation, dotted acronyms, date parsing,
                                          unparseable dates returning None not a guess
tests/test_lexicon.py                14   lexicon completeness, hidden adjacency without
                                          ocean vocabulary, biomedical rejection, incidental
                                          rejection, recall > precision at Stage A, plus
                                          4 regression tests for bugs found in Phase 2
tests/test_db_integrity.py           13   re-ingest idempotency, foreign keys, controlled
                                          vocabularies, 'observed' views requiring evidence,
                                          score bounds, overrides requiring a reason,
                                          absence of a stored total, nulls staying null
tests/test_entity.py                  7   merges only on explainable bases, similar-but-
                                          distinct names not merging, social domains not
                                          being identity, unexplainable basis raising,
                                          uncertain links recorded not merged
tests/test_prioritize.py             10   all dimensions bounded, total computed not stored,
                                          Phase II > Phase I, points citing evidence, timing
                                          decay, incidental zeroing relevance, hidden
                                          adjacency scoring 3, established firms demoted,
                                          analyst overrides surviving re-scoring
tests/test_quality_and_procurement.py 7   junk-name guard (incl. the NATRX regression),
                                          procurement summarisation, not-TAM caveat,
                                          contact addresses stripped from website fields
                                          ─────
                                             59
```

Run with `python3 -m pytest tests -q`. Runtime ~1s. Live-source calls are confined to ingestion modules and are never exercised by the suite.

**Five tests exist specifically because Phase 2 broke something and testing caught it:**
- `test_real_companies_are_not_treated_as_junk` — a junk-name guard deleted NATRX, Giner and UES because `normalize_name` strips legal suffixes, leaving "natrx" looking like a fragment.
- `test_plural_terms_match_singular_lexicon_entries` — the missing-`s` bug that dropped Sea-Gal.
- `test_single_direct_term_passes_stage_a` — the gate that dropped Hydrokinetx.
- `test_passing_mention_of_corrosion_is_not_marine_materials` — the over-correction that admitted nuclear reactors.
- `test_contact_addresses_are_stripped_from_website_fields` — SBIR rows that put a contact address in the Company Website column, which meant contact details were being stored and exported as URLs.

---

## 18. Files created or materially changed

**New — pipeline code**
```
src/ofr/schema.sql                      13-table schema; fact/interpretation separated
src/ofr/db.py                           deterministic ids, date normalisation, idempotent upserts
src/ofr/lexicon.py                      two-stage retrieval + rules_v1 classifier
src/ofr/entity.py                       conservative merges + possible_relationships
src/ofr/prioritize.py                   6-dimension scoring, computed totals, override protection
src/ofr/export.py                       canonical JSON exports
src/ofr/pipeline.py                     end-to-end runner
src/ofr/ingestion/sbir.py               SBIR/STTR bulk ingestion (closes the Phase 1 gap)
src/ofr/ingestion/sbir_enrich.py        award-history maturity signals
src/ofr/ingestion/quality.py            malformed-name guard
src/ofr/ingestion/nsf.py                NSF Awards API (recency + I-Corps)
src/ofr/ingestion/usaspending.py        procurement + reusable demand-summary functions
src/ofr/ingestion/openalex.py           publication corroboration
src/ofr/ingestion/curated.py            hand-curated primary sources
src/ofr/ingestion/views.py              analyst interpretation loader
```

**New — configuration**
```
config/thesis_lexicon.yaml              8 problem-first concept groups + Iowa State clause
config/curated_candidates.yaml          6 hand-verified candidates with full provenance
config/analyst_views.yaml               32 analyst views across 6 candidates
```

**New — tests**
```
tests/conftest.py  tests/test_identity.py  tests/test_lexicon.py
tests/test_db_integrity.py  tests/test_entity.py  tests/test_prioritize.py
tests/test_quality_and_procurement.py
```

**New — outputs (committed)**
```
outputs/candidates.json                 562 candidates with components and evidence counts
outputs/candidate_evidence.json         1,396 evidence records with sources
outputs/top_candidates.json             top 25
outputs/procurement_evidence.json       7 themes of demand-side evidence
research/phase2_report.md               this document
```

**Changed**
```
README.md                               Phase 2 status, architecture, reproduction steps
.gitignore                              excludes data/ (351MB SBIR file + 25MB database)
```

**Not committed:** `data/` — the raw SBIR CSV (351MB) and `ocean_frontier.db`. Both regenerate from `python3 src/ofr/pipeline.py --full`.

---

## 19. Git commit hash

**`8a7b4dc4e4c47e9acbb03ff76cb998a74c66a9aa`** (short: `8a7b4dc`) — "Phase 2: reproducible sourcing pipeline over 211k source records".

Preceded by `b8dccfc` and `c077851` (Phase 1). Repository remains independent of the home-directory repo.

---

## 20. Recommendation for Phase 3

**Do the ARMADA deep dive — but fix two things first, and neither takes long.**

**Before Phase 3 (roughly half a day):**
1. **Register a PatentsView API key.** ARMADA's entire technical case rests on two patents currently sourced from a press release. A deep dive that cannot read the claims from an authoritative patent database is not a technical deep dive. This is the single highest-value unblocked action.
2. **Split the pre-company queue.** Pre-company candidates fell from 39% to 6% of the set. They cannot compete on commercial or timing evidence and should never have been pooled with SBIR companies. This is a scoring-and-routing change, not new ingestion.

**Then Phase 3 — one candidate, done properly:**
- **Technical diligence** on ARMADA: read both patents; assess control authority in realistic sea states; establish whether asymmetric propulsion is a component sold to OEMs or a vehicle.
- **Market sizing bottom-up from the 87 maritime-autonomy procurement contracts already in the database** — real transactions, not a cited TAM. This is the deliverable I flagged in Phase 1 as more defensible than a speculative model, and the data is now sitting in `procurement`.
- **Competitive mapping** against Teledyne, Kongsberg, Saab, L3Harris, plus Propeller's own Orpheus and VATN — where the adjacency question is genuine and worth answering honestly.
- **Unit economics** at the component level, benchmarked against observed vehicle price points ($1.68M–$1.99M).
- **Resolve the two kill questions** already recorded in `analyst_views`.
- **Advance / Pass** with reasoning.

**What I would not do yet.** Do not build the Next.js frontend. The ranking is only trustworthy at the top (§16), and a polished interface over a 64-way tie would present false precision — which is the specific failure this project was set up to avoid. Build the interface after Phase 3, around a finding worth displaying.

**One caution about scope.** 562 candidates is a large enough universe to be tempting as its own deliverable. It should not be. The value of Phase 2 is not the count; it is that three of the final five came from sources Phase 1 could not reach, and that the two recall bugs in §12(c) were caught at all. A wider net that nobody has audited is worth less than a narrower one whose failure modes are known.

---

## Decision gate

**Phase 2 is complete. Phase 3 has not been started.**

Three questions where your direction would change what I do:

1. **Register the PatentsView key before Phase 3, or proceed without patents?** My view: register it — the ARMADA case is patent-shaped and currently rests on a press release.
2. **ARMADA or 3newable for the deep dive?** I recommend ARMADA, but 3newable has published independent performance data including a shortfall against its own target, which is unusually good diligence material. This is a closer call than Phase 1 suggested.
3. **Should I fix the framework's middle-band ranking problem now, or accept that the top 9 is all it can rank and move on?** My view: accept it for now, document it, and revisit only if Phase 3 shows the queue actually gets used below rank 10.
