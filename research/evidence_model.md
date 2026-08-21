# Evidence Model

**Prepared:** 2026-08-21 · **Phase:** 1 (design only — no database built yet)

## Design principles

1. **A candidate is not a row.** A candidate is an *identity* with many evidence records attached. Cramming grants, patents, and publications into one wide row destroys provenance and makes conflicting evidence impossible to represent.
2. **Every claim carries its source.** Not "the candidate has a patent" but "this claim, extracted from this URL, retrieved on this date, says this."
3. **Fact and interpretation never share a field.** Enforced by schema, not by convention.
4. **AI output is a first-class citizen with a second-class status.** It is stored, attributed, and always displayed next to the source it came from.
5. **Rejections are data.** A candidate screened out is retained with a reason, so the filter can be audited. A sourcing system that silently discards is unauditable.

---

## Entity overview

```
                 ┌──────────────────┐
                 │    candidate     │  the opportunity (company OR pre-company project)
                 └────────┬─────────┘
                          │ 1
        ┌─────────────────┼─────────────────┬──────────────────┐
        │ n               │ n               │ n                │ n
┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼───────┐  ┌───────▼───────┐
│   evidence   │  │    person    │  │  assessment   │  │  diligence_q  │
│   (facts)    │  │ (researcher/ │  │ (our reading) │  │ (open questions)│
└───────┬──────┘  │   founder)   │  └───────────────┘  └───────────────┘
        │ n       └──────────────┘
┌───────▼──────┐
│    source    │  the retrieved artifact
└──────────────┘
```

The critical separation: **`evidence` holds what a source says. `assessment` holds what we think.** They are different tables and are rendered differently in the interface.

---

## 1. `candidate` — identity

| Field | Type | Notes |
|---|---|---|
| `candidate_id` | text PK | Stable slug, e.g. `armada-marine-robotics` |
| `name` | text | Company or project name |
| `entity_type` | enum | `company` · `research_project` · `spinout_in_formation` · `lab_program` |
| `institution` | text | Originating institution, if any |
| `geography` | text | City, state/region, country |
| `website` | text | Nullable — many genuine early candidates have none |
| `first_surfaced_date` | date | When *we* first saw it |
| `surfaced_via` | text | FK to the source that surfaced it — how we found it |
| `status` | enum | `new` · `screening` · `active` · `parked` · `rejected` |
| `rejection_reason` | text | Required when status = `rejected` |

**Note on `entity_type`.** This is load-bearing. About half the Phase 1 leads are `research_project` — a funded I-Corps team with no company yet. A model that assumes every candidate is a company cannot represent the stage this project is specifically designed to watch.

---

## 2. `source` — the retrieved artifact

Every fact traces to a row here. This is the provenance backbone.

| Field | Type | Notes |
|---|---|---|
| `source_id` | text PK | |
| `url` | text | Canonical URL |
| `title` | text | As published |
| `source_type` | enum | `federal_award` · `patent` · `publication` · `press_release` · `company_site` · `university_news` · `sec_filing` · `accelerator_page` · `conference_paper` · `trade_press` |
| `publisher` | text | NSF, WHOI, URI, SEC… |
| `published_date` | date | Nullable — **many pages have no date, and that absence is itself a quality signal** |
| `accessed_date` | date | **Required** |
| `retrieval_method` | enum | `api` · `http_fetch` · `manual` |
| `raw_ref` | text | Path to stored raw payload, so a claim can be re-verified if the page changes or dies |

**Why `accessed_date` is mandatory:** web sources mutate and disappear. `techtransfer.whoi.edu` became unreachable during this very research. A claim without an access date cannot be honestly defended later.

---

## 3. `evidence` — what a source says

The heart of the model. One row = one extracted claim from one source.

| Field | Type | Notes |
|---|---|---|
| `evidence_id` | text PK | |
| `candidate_id` | FK | |
| `source_id` | FK | **Required — no orphan evidence** |
| `evidence_type` | enum | see table below |
| `claim` | text | The extracted fact, stated plainly |
| `verbatim_quote` | text | Direct quote where available — the strongest form |
| `event_date` | date | When the *event* happened (not when we read it) |
| `quantitative_value` | numeric | Award amount, patent number, tonnage… |
| `unit` | text | |
| `extraction_method` | enum | `structured_field` · `human_read` · `ai_extracted` |
| `confidence` | enum | `high` · `medium` · `low` |

### `evidence_type` vocabulary

| Group | Types |
|---|---|
| **Technical validation** | `peer_reviewed_publication`, `preprint`, `prototype_demonstrated`, `field_trial`, `independent_validation`, `technical_milestone` |
| **IP** | `patent_granted`, `patent_application`, `license_executed`, `exclusive_license` |
| **Funding** | `research_grant`, `commercialization_grant`, `sbir_phase_i`, `sbir_phase_ii`, `sttr`, `icorps`, `venture_financing`, `form_d_filing`, `non_dilutive_prize` |
| **Commercial** | `named_customer`, `pilot_deployment`, `industry_partnership`, `offtake_agreement`, `revenue_disclosed`, `procurement_contract` |
| **Formation** | `company_incorporated`, `spinout_announced`, `accelerator_participation`, `founder_transition` |
| **Regulatory** | `permit_granted`, `regulatory_milestone`, `class_approval`, `standard_qualification` |
| **Demand-side** | `customer_budget_evidence`, `incumbent_supplier_identified` — *(evidence about the market, not the candidate; this is where USAspending contract data lands)* |

**`extraction_method` is the AI firewall.** `structured_field` means it came from an API field — highest trust. `human_read` means an analyst read the page. `ai_extracted` means a model read it, and the UI must show the source alongside. Any assertion in a memo resting only on `ai_extracted` evidence with no `verbatim_quote` is flagged before it can be relied on.

---

## 4. `person` — researchers and founders

| Field | Type | Notes |
|---|---|---|
| `person_id` | text PK | |
| `candidate_id` | FK | |
| `full_name` | text | |
| `role` | text | PI, founder, CEO, CTO |
| `affiliation` | text | |
| `role_type` | enum | `academic_pi` · `founder` · `academic_and_founder` · `operator` |
| `source_id` | FK | Where we learned this |

**Why `role_type` matters.** `academic_and_founder` is the transition this whole project is built to detect — the professor who becomes a founder. Propeller's portfolio is full of it (Gagnon and Sachs at UW → Banyu; Adkins and Berelson at Caltech/USC → Calcarea; Machado at WHOI → Orpheus; Littlefield and Kaeli at WHOI → ARMADA; Phillips at URI → Juice Robotics). A change in a person's `role_type` is arguably a stronger buy signal than anything about the technology.

**Privacy note.** Only professional information from public sources — names, affiliations, roles as published in awards and press releases. No personal contact details, no scraped social profiles, no inferred personal attributes.

---

## 5. `assessment` — our interpretation, kept separate

| Field | Type | Notes |
|---|---|---|
| `assessment_id` | text PK | |
| `candidate_id` | FK | |
| `dimension` | enum | `technology` · `market` · `business_model` · `capital_intensity` · `timing` · `propeller_fit` · `ocean_centrality` |
| `epistemic_status` | enum | **`observed` · `inferred` · `unknown`** |
| `statement` | text | |
| `supporting_evidence_ids` | text[] | **Required when status = `observed`** |
| `author` | enum | `analyst` · `ai_assisted` |
| `assessed_date` | date | |

This table implements the fact/inference/unknown discipline directly. An `observed` assessment with no supporting evidence IDs is a schema violation — the model makes the sloppy version impossible rather than merely discouraged.

### Category and fit fields (on the candidate, sourced from assessments)

- `primary_category` — one of the eight taxonomy categories
- `ocean_centrality` — `central_mechanism` · `central_environment` · `enabling_customer` · `adjacent` · `incidental`
- `propeller_theme` — `industrials` · `carbon` · `organics` (Propeller's own vocabulary only)
- `portfolio_relationship` — `complementary` · `potentially_competitive` · `unrelated` · `unclear`
- `stage_fit` — `pre_formation` · `pre_seed` · `seed` · `series_a` · `beyond_stage`

**Constraint on `portfolio_relationship`:** it describes a relationship to the **publicly disclosed portfolio only**. Six stealth companies exist. The value `unclear` must be available and must be used freely.

---

## 6. `diligence_question` — structured unknowns

| Field | Type | Notes |
|---|---|---|
| `question_id` | text PK | |
| `candidate_id` | FK | |
| `question_type` | enum | `must_be_true` · `technical_kill` · `commercial_kill` · `open_unknown` |
| `question` | text | |
| `why_it_matters` | text | |
| `evidence_for_ids` | text[] | |
| `evidence_against_ids` | text[] | |
| `resolution_method` | enum | `public_research` · `expert_call` · `founder_call` · `customer_call` · `lab_data` |
| `target_contact_type` | text | *Type* of person to speak with, not a named individual |
| `status` | enum | `open` · `partially_resolved` · `resolved` |

**`technical_kill` and `commercial_kill` are required fields for any candidate promoted to `active`.** Forcing the question "what single finding would end this?" early is the cheapest available discipline against motivated reasoning, and it is exactly the "pressure-test the science" work the analyst role describes.

---

## 7. `score_component` — decomposable, never a black box

| Field | Type | Notes |
|---|---|---|
| `candidate_id` | FK | |
| `dimension` | enum | The five prioritization dimensions |
| `points` | integer | Small integer, e.g. 0–3 |
| `rationale` | text | Required |
| `evidence_ids` | text[] | **Required — a point with no evidence cannot be awarded** |

There is deliberately **no `total_score` column**. The total is computed on read and always rendered alongside its components. Persisting a total invites it being cited on its own, which is precisely the failure mode this project is meant to avoid.

---

## 8. Worked example — ARMADA Marine Robotics

Showing how one real lead decomposes.

**candidate**
`armada-marine-robotics` · `company` · institution: WHOI · Massachusetts · `active` · surfaced_via: WHOI press release

**person**
- Robin Littlefield — co-founder — `academic_and_founder` (WHOI engineer)
- Jeff Kaeli — co-founder — `academic_and_founder` (WHOI engineer)

**evidence** (each with its own source row)
| type | claim | date | source |
|---|---|---|---|
| `exclusive_license` | WHOI executed two exclusive license agreements with ARMADA | Jan 2025 | WHOI/Newswise release |
| `patent_granted` | Asymmetric Propulsion, US Patent 9,873,499 | — | WHOI/Newswise release |
| `patent_granted` | Rotational Feedback Control, US Patent 11,990,857 | — | WHOI/Newswise release |
| `sttr` | NSF STTR Phase I, $255,821, with WHOI | — | Ocean News & Technology |
| `spinout_announced` | ARMADA is a WHOI spin-off co-founded by WHOI engineers | Jan 2025 | WHOI/Newswise release |

**assessment**
- `technology` / `observed` — "Provides propulsion and low-speed maneuvering from a single electric motor, eliminating fins and additional motors." → supported by the license release
- `market` / `inferred` — "Reducing actuator count should lower cost and failure modes in small UUVs, which is the binding constraint on swarm-scale deployment." → our reading, not a sourced claim
- `market` / `unknown` — "No public evidence of a paying customer or unit volume."

**diligence_question**
- `technical_kill` — "Does single-motor asymmetric propulsion retain adequate control authority in realistic currents and sea states, or does control degrade exactly where cheap vehicles are most needed?"
- `commercial_kill` — "Do UUV buyers actually value lower vehicle cost, or is the binding cost the launch, recovery, and support ship — in which case cheaper vehicles do not change the customer's economics?"

That second question is the kind of thing this structure is designed to force early, and it is a genuine risk to the investment case.

---

## 9. What deliberately is *not* in the model

| Excluded | Why |
|---|---|
| `investment_recommendation` | Phase 1 does not make recommendations. Adding the field invites filling it in. |
| `predicted_success_probability` | Unfalsifiable, unearned precision. Explicitly out of scope. |
| `valuation_estimate` | No public basis at this stage. |
| Vector embedding store | No demonstrated need. Keyword + program filtering plus human review handled 116 records well. Revisit only if volume genuinely demands it. |
| Personal contact details | Not needed to prioritize; a privacy liability. |
| Scraped social media | ToS problems and low evidential value. |

---

## 10. Implementation note for Phase 2

SQLite. Seven tables, foreign keys on, one file, versioned alongside the code and inspectable with any SQL client. At the scale this system will plausibly reach — thousands of candidates, tens of thousands of evidence rows — nothing more is justified, and the constraint of a single file keeps provenance auditable.

The one non-obvious requirement: **store raw payloads** (`source.raw_ref`) rather than only extracted fields. When a source changes or disappears — as WHOI's tech transfer site did during this research — the raw copy is the only remaining basis for a claim already made.
