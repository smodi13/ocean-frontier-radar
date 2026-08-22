# Ocean Frontier Radar

A research-to-venture sourcing system for finding emerging technologies at the ocean's edge and turning public signals into an actionable diligence queue.

It scans federal award records, research-translation programs and university licensing announcements; classifies what it finds by **technical problem** rather than by sector label; keeps every claim tied to its source; triages the result into queues that allocate analyst attention; and carries one candidate through a full outside-in diligence case ending in a stated recommendation.

**Status:** local product complete. Not deployed, not published.

---

## Why I built it

Most "VC sourcing tools" scrape a list of startups and attach a score. That fails twice: by the time a company is scrapeable it is already visible to everyone, and a score with no evidence beneath it is decoration.

Two observations shaped this project instead:

1. **The signal arrives before the company.** Federal grants, I-Corps customer-discovery awards and university licences appear 6–24 months before a company is fundable.
2. **The best candidates never say "ocean."** A landlocked university holds a $5M award on biocide-free anticorrosion coatings — a problem most acute on marine assets, in a state with no coastline. No ocean-keyword search finds it.

So retrieval is organised around technical problems, each concept group flagged for whether marine vocabulary is required at all.

---

## Workflow

```
public research signals → sourcing → evidence → prioritization → diligence → investment view
```

Every stage is implemented and inspectable. The site is the presentation layer; the research artifacts are the source of truth.

---

## Dataset and sourcing universe

| | |
|---|---:|
| Source records evaluated | 215,582 |
| Candidates retrieved | 579 |
| Actionable universe (Tier A + B + Frontier) | 134 |
| Tier A / Tier B / Tier C | 38 / 65 / 445 |
| Frontier (pre-company) | 31 |
| Institutions represented | 106 |
| Taxonomy categories | 8 |
| Procurement contracts audited | 87 |

Sources include the official SBIR/STTR bulk award dataset (207,731 records), the NSF Awards API, USAspending, OpenAlex and hand-curated primary sources where automation is blocked. Access failures are documented rather than worked around — SBIR.gov's API returns 403, ARPA-E blocks automated requests, and WHOI's technology-transfer listings moved behind an intranet.

## Frontier

Pre-company signals get their own queue and their own scoring framework, because they structurally cannot show customers, revenue or financing and would be buried in any shared ranking. 31 signals: 17 NSF I-Corps customer-discovery awards and 14 commercialization grants, across 27 institutions. Pre-company share of the actionable universe rose from 6% to 23%.

## ARMADA case study

A full outside-in diligence case on ARMADA Marine Robotics, a WHOI spinout building UUV propulsion and payload-delivery subsystems.

**Recommendation: HOLD — NEED MORE EVIDENCE.** No INVEST recommendation is possible on public information.

The case includes source reconciliation, technical and commercial diligence by product line, a targeted patent review, a bottom-up procurement market built from 87 audited contracts, a scenario model, and a primary-research call plan. Two findings moved the view in opposite directions: patent-family research **weakened** an earlier IP concern (ARMADA is a joint applicant with WHOI on the EPADS PCT, not merely a licensee), while a contract-by-contract procurement audit **weakened** the market thesis (narrow addressable observed procurement is ~$826K/year).

---

## Architecture

```
Python research layer                    Next.js presentation layer
─────────────────────                    ──────────────────────────
ingestion/  → SQLite (13 tables)  →  scripts/build_frontend_data.py  →  frontend/data/*.json  →  static site
                                          (schema validation)
```

- **Research layer** — Python. Ingestion modules, a problem-first search lexicon, a rules classifier, conservative entity resolution, triage, and an Excel scenario model with live formulas.
- **Export** — `scripts/build_frontend_data.py` generates frontend-safe JSON from canonical artifacts and fails on validation errors. Narrative prose lives in `config/*.yaml` with `{{token}}` placeholders resolved from the data; an unknown token is a hard error, so a typo cannot ship a wrong number.
- **Presentation** — Next.js 16, TypeScript, Tailwind, `output: 'export'`. Fully static: no database server, no auth, no API keys, no runtime dependencies, no live scraping.

```
research/        Phase reports, taxonomy, evidence model, ARMADA diligence
src/ofr/         Ingestion, lexicon, entity resolution, tiering, models
config/          Search lexicon, curated candidates, analyst views, site narrative
scripts/         Validated frontend data export
frontend/        Next.js app (app router) + generated data
models/          armada_underwriting.xlsx
outputs/         Canonical JSON exports
tests/           184 offline tests
```

---

## Methodology

**Source hierarchy.** Government and patent records → company and institution primary sources → technical papers → credible secondary reporting → secondary databases. Aggregators are discovery-only and never establish a material financial fact.

**Evidence discipline.** Observed / Inferred / Unknown are separate, enforced in the schema: a statement stored as "observed" must cite a real evidence record.

**Prioritization.** Research priority, not investment probability. Every point cites the evidence that earned it, no total is stored, and ordering within the top tier is analyst judgment — because with integer components the system cannot honestly separate the middle of the distribution.

---

## Validation

184 tests, no network required (`python3 -m pytest tests -q`).

Several exist because something broke and the suite caught it:

- **Recall canaries** — 12 fixtures across every thesis pattern. They caught the lexicon failing to match "oceanographic", which would have rejected a real candidate's own award text.
- **Reporting completeness** — material evidence cannot vanish between database and review. Written after a report omitted a $2M award that was already ingested.
- **Award de-duplication** — the same contract arriving from two sources had inflated a federal total from $3.0M to $4.7M.
- **Procurement and model reconciliation** — site figures are checked against the audit script and the model, which is asserted to contain live formulas and no hardcoded outputs.
- **Deterministic exports** — re-running produces byte-identical data, so a change on the site implies a change in the research.

---

## Limitations

- Public data only; no proprietary company financials.
- No founder, customer or expert calls were conducted. Nothing here rests on a conversation.
- No access to any investor's pipeline, and no claim is made about it.
- Federal procurement is an imperfect proxy for total commercial opportunity — it excludes classified programmes, allied and foreign buyers, and all commercial spending.
- Patent research is a technical and commercial reading of public records. It is not a legal opinion and not a freedom-to-operate assessment.
- Sourcing coverage depends on accessible public sources; the SBIR bulk file lags roughly two years, which biases recency toward NSF.
- Absence of public evidence is not evidence that something does not exist.
- Prioritization reflects outside-in analyst judgment and would differ between analysts.

---

## How to run

```bash
# 1. Research data (one-time: download the official SBIR bulk dataset, ~351MB)
mkdir -p data/raw
curl -L -o data/raw/sbir_award_data.csv \
  https://data.www.sbir.gov/awarddatapublic/award_data.csv

python3 src/ofr/pipeline.py --full        # ingest, resolve, score, export
python3 src/ofr/tiering.py                # refresh signal dates, assign queues
python3 src/ofr/export_phase25.py         # tier cards, frontier queue, snapshots
python3 src/ofr/models/procurement_audit.py
python3 src/ofr/models/armada_underwriting.py

# 2. Frontend data (validated export)
python3 scripts/build_frontend_data.py

# 3. Site
cd frontend && npm install
npm run dev            # http://localhost:3000
npm run build          # static export to frontend/out

# 4. Tests
python3 -m pytest tests -q                # 184 tests, offline
cd frontend && npm run lint && npx tsc --noEmit
```

---

## AI disclosure

AI tools were used to assist with software development, structured extraction and research workflows. Material claims were retained with source traceability and analyst-reviewed before inclusion. AI did not independently make investment decisions, and machine-generated classification is stored separately from source evidence so the two cannot be confused.

This is an independent outside-in research project. It is not affiliated with Propeller, and not affiliated with any company researched. It uses public information only and is not investment advice.
