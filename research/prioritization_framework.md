# Sourcing Prioritization Framework

**Prepared:** 2026-08-21 · **Phase:** 1

## What this is, and what it is not

**This answers exactly one question: *which candidates deserve analyst time first?***

It is **not** an investment score. It does not estimate whether Propeller should invest, what a company is worth, or how likely it is to succeed. It is a triage instrument for allocating scarce hours across a queue that will eventually hold hundreds of candidates.

The distinction is not pedantic. A sourcing-priority score rewards *evidence density and timing* — how much can be learned quickly, and whether now is the moment. An investment judgment rewards *expected outcome*. A candidate can score high here and still be an obvious pass on the merits; that is a correct outcome, because the score's job was to get it looked at, and looking at it produced a fast, well-founded no.

### Rules the framework must obey

1. **Every point traces to evidence.** A point with no `evidence_id` cannot be awarded. Enforced by the schema in `evidence_model.md` §7.
2. **No stored total.** Totals are computed on read and always shown decomposed. There is no `total_score` column.
3. **No false precision.** Integer points, small ranges. Never "87.4% investment probability."
4. **Flags are not points.** Structural problems are surfaced as named flags, not silently netted against a score. A candidate can score 12/15 and still carry a `CONSULTANCY_RISK` flag, and the flag is what an analyst reads first.
5. **Absence of evidence is not evidence of absence.** A candidate scoring 0 on Commercial Signal may be too early to have any — which for this project is often *good*. Low scores route to a different queue, not to the bin.

---

## The five dimensions

Each scored **0–3**. Maximum 15. The scale is deliberately coarse; finer gradations would imply a discrimination the evidence cannot support.

---

### D1. Technical Evidence (0–3)

*Is there real technical substance, independently visible?*

| Points | Standard | Example evidence types |
|---|---|---|
| **0** | Claims only. Marketing language, no external validation. | company site alone |
| **1** | Credible technical basis. Peer-reviewed publication, or a technical grant awarded on scientific merit. | `peer_reviewed_publication`, `research_grant` |
| **2** | Built and demonstrated. Working prototype, granted patent, or SBIR Phase I. | `prototype_demonstrated`, `patent_granted`, `sbir_phase_i` |
| **3** | Validated beyond the lab. Field trial in a real environment, independent validation, SBIR Phase II, or executed exclusive license from a research institution. | `field_trial`, `independent_validation`, `sbir_phase_ii`, `exclusive_license` |

**Why an exclusive license scores 3:** a research institution's technology-transfer office performed its own diligence, negotiated terms, and assigned rights. That is third-party validation with real institutional cost behind it — a much stronger signal than a paper.

---

### D2. Commercial Signal (0–3)

*Is there any evidence a customer exists and cares?*

| Points | Standard |
|---|---|
| **0** | No commercial evidence of any kind |
| **1** | Commercialization *intent* demonstrated — I-Corps award (structured customer discovery), accelerator participation, or company incorporated |
| **2** | Commercialization *funding* won on commercial merit (SBIR/STTR — reviewers assess commercial potential), or a named industry partner |
| **3** | A real customer relationship — named pilot, procurement contract, offtake, or disclosed revenue |

**Deliberate design choice:** I-Corps scores 1, not 0. The programme requires ~100 customer interviews. A researcher doing that has crossed a real threshold of commercial seriousness, even with no company yet. This is precisely the population differentiated sourcing should catch — and it is why 11 of the Phase 1 leads are pre-company.

---

### D3. Timing Signal (0–3)

*Why now, and are we early?*

| Points | Standard |
|---|---|
| **0** | No activity in 24+ months — possibly dormant |
| **1** | Activity within 24 months |
| **2** | Activity within 12 months |
| **3** | Activity within 6 months, **or** a state-change event: new spinout, first license, first commercialization grant, founder transitioning from academia |

**The state-change clause carries most of the weight.** A recent award on a long-running project is weaker than a *first* license on a quiet one. Recency measures freshness; state change measures the transition this project exists to detect. Both route to 3, but the second is the one worth acting on, so state changes are labelled in the queue rather than merely scored.

---

### D4. Venture Potential (0–3)

*Could this plausibly become a venture-scale company — as opposed to a good product, a lab, or a consultancy?*

| Points | Standard |
|---|---|
| **0** | No plausible venture path — inherently a service, a tool, or a research programme |
| **1** | Plausible product, but unclear scale or a small/fragmented market |
| **2** | Repeatable product with a credible large market and identifiable buyers |
| **3** | Repeatable product, large market, **and** a specific mechanism for durable advantage — a cost/performance step-change, protected IP, or a structural position |

This is the **most inference-heavy dimension and the most error-prone**, because at this stage it is largely judgement. It should always be recorded as `inferred` in the assessment table, with reasoning attached. Where a market-size claim is used it must be sourced — several Phase 1 leads carry figures taken directly from their NSF abstracts (e.g. off-flavour costing aquaculture $4.5B, shipping fuel >$150B/yr with >20% lost to routing), and those are attributed to the abstract, **not asserted as our own analysis**. They are the applicant's claim to a federal reviewer, which is evidence of a claim, not evidence of a market.

---

### D5. Propeller Relevance (0–3)

*Does this fit what Propeller publicly says it does?*

| Points | Standard |
|---|---|
| **0** | Outside stated themes, or ocean connection is `incidental` |
| **1** | Fits a stated theme, but ocean-centrality is `adjacent` or stage fit is poor |
| **2** | Fits a stated theme with `enabling_customer` centrality and plausible pre-seed/seed timing |
| **3** | Fits a stated theme with `central_mechanism` or `central_environment` centrality, at pre-seed/seed stage, in an area Propeller has publicly written about |

**Constraint:** this measures fit with **publicly stated** themes and the **publicly disclosed** portfolio. It never claims knowledge of Propeller's pipeline, current priorities, or internal views. A high D5 means "consistent with what they have published," nothing more.

---

## Flags — structural problems, surfaced not netted

Flags do not subtract points. They appear as labels beside the score, because a reader needs to see *why* a high-scoring candidate might still be wrong. These encode the specific failure modes named in the project brief.

| Flag | Trigger | Why it matters |
|---|---|---|
| `NO_COMMERCIALIZATION_PATH` | Strong science, no identifiable buyer or product form | The classic "great paper, no company" |
| `CONSULTANCY_RISK` | Revenue model looks like project work, engineering services, or grant-funded studies | Endemic in coastal adaptation and ocean data. Does not scale, does not fit venture. |
| `CAPEX_BEFORE_VALIDATION` | Requires large capital *before* technical or market proof — vessels, plants, offshore assets | Common in offshore energy and marine energy. A $500K–$3M check cannot meaningfully de-risk it. |
| `AI_WRAPPER` | Applied-AI claim with no proprietary data, no domain-specific model, no defensible position | The category 8 failure mode |
| `UNSUPPORTED_TECHNICAL_CLAIM` | Central performance claim with no publication, patent, prototype, or third-party validation | Direct application of the no-fabrication principle |
| `BEYOND_STAGE` | Already raised well past Series A, or is an established incumbent | Outside Propeller's stated $500K–$3M, pre-seed–Series A model |
| `OCEAN_INCIDENTAL` | Ocean is a use case or a keyword, not the mechanism, environment, or customer context | The main defense against a generic climate-startup list |
| `MUNICIPAL_BUYER_ONLY` | Sole customer is a grant-cycle public body | Structurally difficult venture customer. Escape route: insurers, developers, industrial asset owners. |
| `SINGLE_SOURCE` | Entire candidate rests on one source | Evidence-quality flag, not a judgement about the company |
| `CROWDED_CATEGORY` | Area already densely funded and heavily covered | Not disqualifying — but low differentiated-sourcing value. Applies to undifferentiated mCDR capture. |

---

## Routing — what the score actually does

The output is a **queue assignment**, not a ranking:

| Condition | Queue | Meaning |
|---|---|---|
| Score ≥ 11, no red flags | **Deep dive** | Warrants full technical + commercial diligence now |
| Score 8–10, or ≥ 11 with flags | **Active research** | Worth several hours; resolve flags and kill questions |
| Score 5–7 | **Watch** | Re-check on a state change; set a trigger, do not spend hours |
| Score ≤ 4 | **Archive** | Retained with reason. Not deleted. |
| **`entity_type = research_project`, any score** | **Watch (early)** | Separate queue — scored on a curve, because pre-company candidates *structurally cannot* score on D2 and D3 |

**The last row is the important one.** A raw 15-point ranking would systematically bury exactly the pre-company research candidates this project exists to find — they cannot have customers or financings yet. Running them in a separate queue is what keeps the system from collapsing into "rank the companies that already look like companies," which is the thing every other sourcing tool already does.

---

## Worked examples

Applying the framework to three real Phase 1 leads. Full scoring for all leads is in `initial_leads.csv`.

### ARMADA Marine Robotics — 13/15 → Deep dive

| Dimension | Pts | Evidence |
|---|---|---|
| D1 Technical | **3** | Two granted US patents (9,873,499; 11,990,857); exclusive WHOI licenses; NSF STTR Phase I |
| D2 Commercial | **2** | NSF STTR Phase I $255,821 won on commercial merit; no named customer yet |
| D3 Timing | **3** | State change — first exclusive licenses executed Jan 2025 |
| D4 Venture | **2** | Component-level cost reduction in UUVs; large and growing market; but is the vehicle the cost driver? |
| D5 Propeller | **3** | Category 1, `central_environment`, WHOI (founding partner), pre-seed, dual-use — Propeller has written on all of this |

Flags: none. **Note:** `CROWDED_CATEGORY` was considered — Propeller holds two AUV companies — and deliberately *not* applied, because ARMADA is a component/propulsion play rather than a vehicle play. That distinction is itself a diligence question.

### Oregon State — Autonomous Subsea Connection System — 9/15 → Watch (early)

| Dimension | Pts | Evidence |
|---|---|---|
| D1 Technical | **1** | NSF I-Corps award; Hollinger's robotics lab is credible; no public prototype evidence |
| D2 Commercial | **1** | I-Corps = structured customer discovery underway |
| D3 Timing | **3** | Awarded 17 Aug 2026 — four days before this research |
| D5 Propeller | **3** | OSU is a Propeller partner; subsea connection is named in their ocean-compute post; `central_environment` |
| D4 Venture | **1** | Plausible but entirely unproven; wet-mate connection is a real bottleneck with entrenched incumbents |

Flags: none yet — too early for flags to be meaningful. Sits in the early queue precisely because D1/D2 *cannot* be high yet.

### A hypothetical maritime AI routing tool — 6/15 → Watch, flagged

| Dimension | Pts | Rationale |
|---|---|---|
| D1 Technical | 1 | Model exists, no independent validation |
| D2 Commercial | 2 | Two named pilots |
| D3 Timing | 2 | Recent launch |
| D4 Venture | 1 | Crowded, no proprietary data |
| D5 Propeller | 0 | `OCEAN_INCIDENTAL` |

Flags: `AI_WRAPPER`, `OCEAN_INCIDENTAL`. Note D2 = 2 outscores ARMADA's commercial signal — and the candidate is still correctly deprioritized. **This is the framework working as designed:** commercial traction alone does not buy relevance, and the flags carry the argument the number cannot.

---

## Known weaknesses

Stated plainly, because a framework presented without its failure modes is a sales pitch.

1. **D4 is barely evidence-based.** It is judgement wearing a number. It should probably be recorded as a label (`weak` / `plausible` / `strong`) rather than points; retained as points only for comparability. Revisit in Phase 2.
2. **Federal-award bias.** D1 and D2 lean heavily on grant evidence because that is the data that is reliably accessible (see `data_sources.md`). Companies that never took federal money — bootstrapped, foreign, or venture-first — are systematically under-scored. This is a *measurement* artifact, not a real quality difference.
3. **NSF-only bias, inherited.** With SBIR.gov returning 403, Navy/NOAA/DOE SBIR recipients are largely invisible, so D2 under-counts exactly the dual-use candidates Propeller says it likes.
4. **Recency is gameable and non-stationary.** D3 rewards whatever was funded most recently, which tracks federal budget cycles rather than technical readiness.
5. **No inter-rater reliability.** One person scored everything. With two analysts, the same candidate would likely differ by 1–2 points. Any comparison at that granularity is noise.
6. **The framework cannot see private companies with no public footprint** — which may be the most interesting ones. The system's floor is set by what is public, and that floor is real.
