# Ocean Frontier Radar

> ## 🚧 Work in progress — Phase 2 (sourcing pipeline) complete, Phase 3 not started
>
> This repository contains **research and a working sourcing pipeline**. There is no public application, no deployment, and no investment memo. Nothing here should be read as an investment recommendation.

---

## What this is

A research-first sourcing and diligence system for early-stage ocean technology, built as a portfolio project for an application to the **Investment Analyst** role at [Propeller](https://propellervc.com/), an early-stage venture firm investing "at the ocean's edge."

## Research question

**Can we systematically identify promising ocean-related technologies before they become obvious venture deals, and turn the strongest signals into an actionable venture diligence queue?**

The transition being watched:

```
research → technical validation → grants/IP → prototype
        → commercialization → startup/spinout → venture opportunity
```

## Why start with sourcing research rather than a dashboard

Most "VC tools" begin by scraping a list of startups and attaching a score. That approach fails twice over: by the time a company is scrapeable it is already visible to everyone, and a score with no evidence beneath it is decoration.

So this project starts one step earlier — at **federal grants, university licensing, and research commercialization programs** — where the signal appears 6–24 months before a company is fundable.

That choice is grounded in something Propeller says about its own portfolio: many of its companies "initially secure grants for research before launching their startup to commercialize innovations" ([How We Invest](https://propellervc.com/blog/how-we-invest)). At least 8 of 19 publicly named portfolio companies trace to a specific research institution or academic founder. Watching the grant stage is watching the stage Propeller says its companies come from.

## Current phase

| Phase | Status |
|---|---|
| **Phase 1 — Research foundation** | ✅ Complete |
| **Phase 2 — Sourcing pipeline + database** | ✅ Complete, awaiting review |
| Phase 3 — Deep diligence on one candidate | ⬜ Not started |
| Phase 4 — Public interface | ⬜ Not started |

**Phase 1 produced:** a sourced dossier on Propeller's public strategy; a working taxonomy; a mapped sourcing universe; an empirically tested data-source assessment; an evidence model; a prioritization framework; and **28 real, source-backed candidate opportunities**.

**Phase 2 produced:** a reproducible ingestion pipeline across five sources; a 13-table SQLite evidence store; a problem-first search lexicon; a two-stage retrieval/classification engine; conservative entity resolution; a six-dimension sourcing-priority score; **562 candidates (198 qualified) from 211,361 source records**; and 59 offline tests.

Phase 2 closed the Phase 1 blocker: SBIR.gov's *API* returns HTTP 403, but SBIR.gov publishes the complete award dataset as an official public download. Ingesting it brought in **ten agencies** — including the Navy and NOAA candidates Phase 1 was blind to. Three of the final top five come from sources Phase 1 could not reach.

## Methodology principles

1. **No fabricated data.** No invented companies, researchers, grants, patents, funding amounts, customers, or market sizes. Every factual claim about a real entity traces to a public source.
2. **Source everything.** Every candidate retains source URL, title, type, publication date where available, date accessed, and the extracted evidence.
3. **Fact, inference, and unknown are separate.** Every material observation is tagged **Observed** (supported by public evidence), **Inferred** (our reading), or **Unknown** (requires primary diligence). This is enforced by the schema, not by convention.
4. **A score is not a judgment.** Scores prioritize analyst attention. They do not estimate whether anyone should invest. Every score decomposes into evidence, and no total is ever stored without its components.
5. **Useful simplicity.** No vector database, no agent framework, no Kubernetes. Plain APIs, a SQLite file, and human review.
6. **AI assists, sources decide.** Where AI is used for classification or extraction, the underlying source stays visible and AI-derived content is labelled as such.
7. **Respect access controls.** No bypassing authentication, CAPTCHAs, paywalls, or anti-bot measures. Where a source returned 403, that is recorded as a finding — see `research/data_sources.md`.

## Evidence discipline

Sources that failed are documented as prominently as sources that worked. Phase 1 found that **SBIR.gov's API returns HTTP 403**, **ARPA-E blocks automated requests**, **patent APIs require keys**, and **WHOI's technology-transfer site has moved behind an intranet**. Each is recorded with its status code and its consequence for coverage — including the resulting NSF bias in the lead sample.

Nothing in this repository claims any knowledge of Propeller's internal pipeline, deal flow, or views. All firm analysis is outside-in, from public material. Portfolio "whitespace" is never asserted; the phrasing used throughout is *"not represented in the publicly disclosed portfolio reviewed"* — and six disclosed stealth companies are treated as a real limit on what can be said.

## Repository structure

```
ocean-frontier-radar/
├── README.md
├── config/
│   ├── thesis_lexicon.yaml          Problem-first search vocabulary, 8 concept groups
│   ├── curated_candidates.yaml      Hand-verified candidates with full provenance
│   └── analyst_views.yaml           Analyst interpretation (kept apart from evidence)
├── research/
│   ├── propeller_thesis.md          Firm dossier — themes, portfolio map, process, sourcing
│   ├── ocean_taxonomy.md            8 categories + ocean-centrality axis
│   ├── sourcing_universe.md         Institutions, funders, programs, conferences
│   ├── data_sources.md              Empirical access testing — what works, what is blocked
│   ├── evidence_model.md            Entity/schema design
│   ├── prioritization_framework.md  Sourcing-priority scoring (not investment scoring)
│   ├── initial_leads.csv / .md      Phase 1's 28 hand-built candidates
│   ├── phase1_report.md             Phase 1 decision gate
│   └── phase2_report.md             Phase 2 decision gate
├── src/ofr/
│   ├── schema.sql                   13 tables; facts and interpretation kept separate
│   ├── db.py  lexicon.py  entity.py  prioritize.py  export.py  pipeline.py
│   └── ingestion/                   sbir · nsf · usaspending · openalex · curated · views
├── outputs/                         Generated JSON — regenerate, do not edit
├── sources/source_registry.csv      20 data sources with tested access status
└── tests/                           59 offline tests
```

## Running the pipeline

```bash
# one-time: download the official SBIR bulk award dataset (~351MB, with abstracts)
mkdir -p data/raw
curl -L -o data/raw/sbir_award_data.csv \
  https://data.www.sbir.gov/awarddatapublic/award_data.csv

python3 src/ofr/pipeline.py --full     # ingest everything, resolve, score, export
python3 src/ofr/pipeline.py --score    # re-resolve, re-score and re-export only
python3 -m pytest tests -q             # 59 tests, no network required
```

`data/` is gitignored — the raw CSV and the SQLite database both regenerate. `outputs/*.json` are committed as derived views.

Ingestion shells out to `curl` deliberately: local TLS interception breaks Python's certificate verification, and disabling verification would be the wrong fix. See `research/data_sources.md` §12.

## How the pipeline avoids keyword sourcing

Phase 1 found that the strongest Propeller-relevant candidates often do not describe themselves as ocean companies. Allium Engineering sells rebar; Iowa State holds a $5M award on microbial anticorrosion coatings in a landlocked state.

So retrieval is organised by **technical problem**, not sector label, and each concept group carries a `requires_ocean_context` flag. Where the underlying problem is inherently marine-relevant — corrosion, biofouling, underwater acoustics — a record is retrieved **with no ocean vocabulary at all**. Every candidate then carries an `ocean_centrality` tag (`central_mechanism` · `primary_end_market` · `strong_adjacency` · `incidental`) that guards both failure modes: missing the landlocked corrosion lab, and forcing a generic AI company into an ocean thesis.

## Planned later phases

- **Phase 2 — Ingestion + storage.** Python harvesters against the sources validated in `data_sources.md`, writing to a SQLite database implementing `evidence_model.md`. Analyst-reviewed classification, with AI assisting extraction and every claim retaining its source.
- **Phase 3 — Interface.** A read-only diligence view: candidate queue, evidence trail per claim, decomposed scores, open diligence questions. Every displayed claim links to its source.
- **Phase 4 — Deep dive.** A full investment-style analysis of one candidate: technical diligence, market sizing built from public procurement data, competitive mapping, business-model analysis, unit economics, primary-research questions, and an Advance/Pass recommendation.

## Status of claims in this repository

Phase 1 makes **no investment recommendations**. It identifies candidates worth analyst time and states, for each, what is known, what is inferred, and what would have to be verified. The 28 leads are a research sample, not a pipeline.

---

*Sources accessed 2026-08-21. Built with AI assistance (Claude Code); all sources were retrieved and verified against primary URLs, and access failures are documented rather than worked around.*
