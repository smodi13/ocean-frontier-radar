# Ocean Frontier Radar

> ## 🚧 Work in progress — Phase 1 (research) complete, Phase 2 not started
>
> This repository currently contains **research only**. There is no application, no deployment, and no product. Nothing here should be read as an investment recommendation.

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
| **Phase 1 — Research foundation** | ✅ Complete, awaiting review |
| Phase 2 — Ingestion pipeline + database | ⬜ Not started |
| Phase 3 — Diligence interface | ⬜ Not started |
| Phase 4 — Deep-dive investment analysis | ⬜ Not started |

**Phase 1 produced:** a sourced dossier on Propeller's public strategy; a working taxonomy; a mapped sourcing universe; an empirically tested data-source assessment; an evidence model; a prioritization framework; and **28 real, source-backed candidate opportunities**.

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
├── research/
│   ├── propeller_thesis.md          Firm dossier — themes, portfolio map, process, sourcing
│   ├── ocean_taxonomy.md            8 categories + ocean-centrality axis + search vocabulary
│   ├── sourcing_universe.md         Institutions, funders, programs, conferences
│   ├── data_sources.md              Empirical access testing — what works, what is blocked
│   ├── evidence_model.md            Entity/schema design for candidates and evidence
│   ├── prioritization_framework.md  Sourcing-priority scoring (not investment scoring)
│   ├── initial_leads.csv            28 candidates, machine-readable
│   ├── initial_leads.md             Narrative + 5 research cards + deep-dive recommendation
│   └── phase1_report.md             Decision-gate summary
├── sources/
│   └── source_registry.csv          20 data sources with tested access status
└── src/
    └── harvest/                     Small research utilities used to gather Phase 1 data
```

## Reproducing the Phase 1 data

The harvest scripts in `src/harvest/` query public APIs with no authentication:

```bash
python3 src/harvest/nsf_sbir_harvest.py    # NSF SBIR/STTR ocean-vocabulary awards
python3 src/harvest/nsf_translation_harvest.py  # NSF I-Corps / PFI / Convergence Accelerator
```

Both write JSON to `data/` (gitignored — raw harvests are not committed). They shell out to `curl` deliberately; see `research/data_sources.md` §12.

## Planned later phases

- **Phase 2 — Ingestion + storage.** Python harvesters against the sources validated in `data_sources.md`, writing to a SQLite database implementing `evidence_model.md`. Analyst-reviewed classification, with AI assisting extraction and every claim retaining its source.
- **Phase 3 — Interface.** A read-only diligence view: candidate queue, evidence trail per claim, decomposed scores, open diligence questions. Every displayed claim links to its source.
- **Phase 4 — Deep dive.** A full investment-style analysis of one candidate: technical diligence, market sizing built from public procurement data, competitive mapping, business-model analysis, unit economics, primary-research questions, and an Advance/Pass recommendation.

## Status of claims in this repository

Phase 1 makes **no investment recommendations**. It identifies candidates worth analyst time and states, for each, what is known, what is inferred, and what would have to be verified. The 28 leads are a research sample, not a pipeline.

---

*Sources accessed 2026-08-21. Built with AI assistance (Claude Code); all sources were retrieved and verified against primary URLs, and access failures are documented rather than worked around.*
