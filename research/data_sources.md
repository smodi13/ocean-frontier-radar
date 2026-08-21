# Data Source Assessment

**Prepared:** 2026-08-21 · All endpoints tested live on 2026-08-21 from a macOS/curl client.

> Every entry below reflects an **actual request I made**, not documentation I read. Where something failed, the failure is reported with its status code. Three sources I expected to be central turned out to be unusable, and that is reported rather than hidden.

**Access ethics stated up front:** I did not attempt to bypass any authentication, CAPTCHA, paywall, rate limit, or anti-bot control. Where a server returned 403 to an ordinary request, I recorded it as blocked and moved on. `robots.txt` was checked for the sites crawled.

---

## Summary table

| Source | Access method | Status | Recommendation |
|---|---|---|---|
| NSF Awards API | Public REST/JSON, no key | ✅ Working | **Core automated source** |
| USAspending API | Public REST/JSON, no key | ✅ Working | **Core automated source** (demand-side) |
| OpenAlex API | Public REST/JSON, no key | ✅ Working | **Supplemental automated source** |
| arXiv API | Public Atom API | ✅ Working | Supplemental automated source |
| Grants.gov Search2 API | Public REST/JSON | ✅ Working | Supplemental automated source |
| SEC EDGAR full-text search | Public JSON (`efts.sec.gov`) | ⚠️ Working, limited value | Supplemental / manual |
| Propeller website + sitemap | Public HTML/XML | ✅ Working | Core (firm intelligence) |
| University news (URI, UCSD) | Public HTML | ✅ Working | Supplemental automated source |
| **SBIR.gov API** | Public REST | ❌ **403 Forbidden** | **Not usable** — substitute NSF API + USAspending |
| **ARPA-E project pages** | Public HTML | ❌ **403 Forbidden** | Manual diligence source only |
| **PatentsView API** | REST | ❌ Requires API key | Deferred to Phase 2 |
| **USPTO Open Data API** | REST | ❌ **401 Unauthorized** | Deferred to Phase 2 |
| **WHOI tech transfer** | HTML | ❌ Moved to intranet | Manual diligence source only |

---

## 1. NSF Awards API — **Core automated source** ⭐

- **Endpoint:** `https://api.nsf.gov/services/v1/awards.json`
- **Access:** Public REST, JSON, **no API key required**, no registration.
- **Tested:** Yes — ran a full paginated harvest across 39 keywords, retrieving 116 filtered records across two passes.

**Useful fields (all verified returned):** `id`, `title`, `abstractText` (full text), `awardeeName`, `awardeeCity`, `awardeeStateCode`, `date`, `startDate`, `estimatedTotalAmt`, `fundProgramName`, `piFirstName`, `piLastName`.

**Query behaviour observed:**
- `keyword=` performs full-text search including abstracts — which is why precision is limited (see below).
- `dateStart=MM/DD/YYYY` filters effectively.
- `offset` + `rpp` (max 25) paginate correctly.
- `printFields` controls the response payload.

**Reliability:** Excellent. Zero failed requests across several hundred calls with a 0.1s delay between them.
**Rate limits:** None encountered or documented at this volume. I self-throttled anyway.
**Historical depth:** Deep — decades of awards.
**Terms:** US federal government open data.

**Why it is the backbone of this project.** The `fundProgramName` field allows filtering to exactly the programs that indicate *commercialization intent*:

| Program filter | What it means | Typical size |
|---|---|---|
| `I-Corps` | PI is doing customer discovery — **pre-company, commercially intentioned** | ~$50K |
| `SBIR Phase I` | Company exists, first non-dilutive validation | ~$305K |
| `SBIR Phase II` | Technical milestones met, scaling | ~$1.25M |
| `STTR Phase I/II` | Company + university partner (i.e. a licensed-IP spinout) | ~$305K+ |
| `PFI-TT` / `PFI-RP` | Explicit technology translation | $550K–$1M |
| `Convergence Accelerator` | Themed multi-million translation | $650K–$5M |

**Measured precision.** Of 69 SBIR/STTR records returned by ocean-vocabulary keywords, I hand-classified **~14 (≈20%)** as genuinely ocean-relevant. Of 47 I-Corps/PFI/Convergence records, **~13 (≈28%)** were genuinely relevant. The false positives are almost entirely biomedical and generic-materials awards that mention e.g. "vessel" (blood vessel), "acoustic" (ultrasound), or "harmful algal" incidentally in an abstract.

**Implication for Phase 2:** the retrieval layer is cheap and reliable; the *classification* layer is the real work. This is the correct place for AI assistance — reading abstracts and proposing a category + ocean-centrality tag — with the abstract and award URL retained so a human can overturn it. It is not a place for an AI score.

**Limitation:** NSF only. Misses NIH, DOE, DOD, NOAA, USDA SBIR entirely.

---

## 2. USAspending API — **Core automated source, but not for the reason I expected** ⭐

- **Endpoint:** `https://api.usaspending.gov/api/v2/search/spending_by_award/` (POST, JSON)
- **Access:** Public, no key. **Tested:** Yes, multiple keyword and award-type combinations.

**Useful fields:** Award ID, Recipient Name, Award Amount, Awarding Agency, Awarding Sub Agency, Description, Start Date.

**Reliability:** Excellent. **Historical depth:** Deep. **Terms:** US federal open data.

**Key finding — this is a demand-side instrument, not a discovery instrument.**
I queried it expecting to recover the SBIR awards that SBIR.gov denied me. Instead, ocean keyword queries returned overwhelmingly **procurement and services contracts**: Atlantic Diving Supply reselling hardware, Saab selling NOAA a long-range AUV ($1.68M), Teledyne spares, WHOI selling the Navy a REMUS 600 ($1.99M), Vision Point Systems providing Navy marine-corrosion engineering support ($4.06M and $3.44M), Florida Institute of Technology running Navy biofouling assessments.

None of those are venture leads. But collectively they answer a question that is *harder* to answer than "who exists": **who actually pays for this, how much, and how often.** That is a diligence input — it is evidence of a real budget line, and it names incumbent suppliers, i.e. the competitive set.

**Recommendation:** use it in the diligence layer to substantiate "identifiable urgent customer" claims, and to map incumbents. Do not use it to find companies.

---

## 3. SBIR.gov API — **Not usable** ❌

- **Endpoints tested:** `https://api.www.sbir.gov/public/api/awards`, `.../solicitations`, and legacy `https://www.sbir.gov/api/awards.json`
- **Result:** `{"message":"Forbidden"}`, **HTTP 403**, on every variant, with and without a browser-like User-Agent and explicit `Accept: application/json`. The legacy path returns a 404 HTML page.
- **robots.txt:** fetched and reviewed; the block is server-side, not a robots directive.

**Assessment.** This would have been the ideal source — cross-agency SBIR/STTR awards in one place, covering NOAA, Navy, DOE, and NSF together. It is documented as public but did not serve automated requests from this client on 2026-08-21.

**I did not attempt to work around it.** Repeated 403s to a plain, correctly-formed, self-throttled request are an access-control decision by the operator, and the correct response is to respect it and substitute.

**Substitutes adopted:**
1. NSF Awards API for NSF SBIR/STTR (works, full abstracts).
2. USAspending for contract-level SBIR data from other agencies.
3. Manual agency pages for NOAA/DOE SBIR.

**Consequence to state honestly:** the Phase 1 lead set is **NSF-biased**. Navy, NOAA, and DOE SBIR recipients are under-represented, which matters because Navy SBIR is precisely where Propeller's stated dual-use interest would show up. Closing this gap is Phase 2's highest-value data task. Options: request API access from SBIR.gov directly, or use their bulk CSV download if one is offered through an approved channel.

---

## 4. ARPA-E — **Manual diligence source only** ❌

- **URLs tested:** `arpa-e.energy.gov/programs-and-initiatives/view-all-programs/seasight`
- **Result:** **HTTP 403** via both WebFetch and direct curl with a browser User-Agent.

ARPA-E's **SEA-CO2** program ($36M, 11 projects, mCDR measurement and validation) is highly relevant — it directly funds the MRV problem identified in taxonomy §4, and awardees include **atdepth MRV** ($2,524,964) and WHOI. Project descriptions are published as a PDF, and awardee information is recoverable from secondary sources and DOE press releases, which is how the atdepth record in `initial_leads.csv` was sourced.

**Recommendation:** treat as a manual, periodic analyst review. Do not build a scraper against a host returning 403.

---

## 5. Patent data — **Deferred to Phase 2** ❌

| Endpoint | Result |
|---|---|
| `search.patentsview.org/api/v1/patent/` | Empty response — requires a (free) API key |
| `api.uspto.gov/api/v1/patent/applications/search` | **HTTP 401 Unauthorized** — requires a key |

Both offer free keys via registration; neither was usable without one, and I did not register a key during Phase 1.

**This is a real gap.** Patents are a core evidence type in the model — the ARMADA lead is anchored on two specific patents (US 9,873,499 and US 11,990,857), which I sourced from press coverage rather than a patent database. For a system whose premise is *research → IP → spinout*, IP is not optional.

**Phase 2 action:** register a PatentsView key. Highest-value query pattern is **assignee = university**, which reveals what an institution owns *before* anything is licensed out — the earliest possible formal signal.

---

## 6. OpenAlex — **Supplemental automated source** ✅

- **Endpoint:** `https://api.openalex.org/works` · **Access:** Public, no key; polite-pool via `mailto=`.
- **Tested:** Yes — `ocean alkalinity enhancement` returned 61,818 works with an 85ms response.
- **Useful fields:** title, DOI, authors + institutional affiliations, publication date, concepts, citation counts, open-access status.
- **Reliability:** Excellent. **Depth:** Very deep.

**Use:** the *upstream* signal — identifying which researchers and labs are producing relevant work before any grant or company exists, and corroborating a founder's technical credibility.

**Limitation and warning.** Publication volume is **not** commercialization intent. Most published ocean science will never become a company, and treating citation counts as a venture signal would be exactly the "score pretending to be judgment" failure the project is meant to avoid. Publications belong in the evidence model as *supporting* records attached to candidates surfaced by commercialization signals — not as a primary discovery channel.

---

## 7. arXiv API — **Supplemental automated source** ✅

- **Endpoint:** `https://export.arxiv.org/api/query` (note: **HTTPS required**; the HTTP endpoint returned nothing).
- **Tested:** Yes — returned valid Atom for `all:"autonomous underwater vehicle"`.
- **Use:** timely signal for robotics, autonomy, and applied-AI work (categories 1, 2, 8), which is where preprint culture is strong.
- **Limitation:** near-useless for categories 4, 5, and 7 — ocean chemistry, materials, and aquaculture publish in journals, not on arXiv.

---

## 8. Grants.gov Search2 API — **Supplemental automated source** ✅

- **Endpoint:** `https://api.grants.gov/v1/api/search2` (POST) · **Access:** Public, no key.
- **Tested:** Yes — `{"keyword":"ocean","rows":2,"oppStatuses":"forecasted|posted"}` returned `hitCount: 43`.
- **Use:** *forecasted* opportunities show where federal money is about to flow, 6–18 months ahead of awards. That is a leading indicator for which technical areas are about to get a funding tailwind — useful for thesis work, not for finding individual companies.

---

## 9. SEC EDGAR full-text search — **Supplemental / manual** ⚠️

- **Endpoint:** `https://efts.sec.gov/LATEST/search-index` · **Access:** Public JSON; requires a descriptive User-Agent per SEC policy (I used one identifying the project and a contact address).
- **Tested:** Yes. A bare query returned HTTP 200 with valid results; adding `dateRange=custom` produced `{"message": "Internal server error"}`, while `startdt`/`enddt` alone worked.

**Assessment.** Form D filings mark a first priced financing, so in principle EDGAR reveals company formation and early raises. In practice the indexed Form D content is the `primary_doc.xml` — company name, address, industry code, offering amount — and **not** a technology description. A keyword search for `seaweed` returned an unrelated company. So it cannot be used to *discover* ocean companies by technology.

**Correct use:** confirmation, not discovery. Once a candidate name is known, EDGAR verifies whether a Form D exists, when, and for how much — a genuinely useful, authoritative funding-evidence check for a candidate that otherwise has no press coverage.

---

## 10. University news and accelerator pages — **Supplemental automated source** ✅

| Site | Status | Value |
|---|---|---|
| `uri.edu/news` | ✅ 200 | Excellent — dated items naming companies, founders, licensed technologies (Juice Robotics) |
| `today.ucsd.edu` | ✅ 200 | Good — Chancellor's Innovation Award finalists (Hybrid Reefs) |
| `startblue.ucsd.edu/impact` | ✅ 200 | Good — enumerable cohort ventures |
| `innovation.ucsd.edu` | ✅ 200 | Good |
| `whoi.edu` press room | ✅ 200 | Good — license and spinout announcements |
| `techtransfer.whoi.edu` | ❌ 302 → `intranet.whoi.edu/inventors`, unreachable | **Regression** — previously public tech-transfer listing now internal |
| `tco.uw.edu` (UW CoMotion) | ❌ Connection failed | Retry in Phase 2 |
| `tec.oregonstate.edu` | ❌ Connection failed | Retry in Phase 2 |
| `web.uri.edu/rimtc` | ❌ 404 | Dead link |

**Assessment.** University news is high-value but structurally inconsistent — every institution uses a different CMS, and the useful items are a tiny fraction of total output. Per-institution scrapers are brittle and high-maintenance.

**Recommendation:** target a **small number** of high-yield institutions (URI, UCSD, WHOI) with narrow category filters rather than building a general university-news crawler. Accept that this channel needs periodic manual repair.

---

## 11. Propeller's own site — **Core source for firm intelligence** ✅

- `propellervc.com/sitemap.xml` enumerates all public pages (61 URLs), which is how the complete blog inventory was recovered.
- `robots.txt` disallows only HubSpot preview and preference-centre paths. Public content pages are permitted.
- The `/team` page returns **404** and is absent from the sitemap.

**Use:** thesis tracking. Propeller publishes its evolving thinking, and the two most recent posts (ocean compute, 28 Jul 2026; coastal heat adaptation, 13 Aug 2026) are direct statements of current interest. Monitoring this feed is the cheapest possible way to keep the taxonomy aligned with the firm.

---

## 12. Environment note

Python's `urllib` failed with `SSL: CERTIFICATE_VERIFY_FAILED (self-signed certificate in certificate chain)` on this machine, while `curl` succeeded against the same endpoints. This is local TLS interception, not a property of any source. The harvest scripts therefore shell out to `curl`. **In Phase 2 this should be handled by using `requests` with a proper CA bundle (`certifi`) rather than by disabling verification** — turning off certificate checking to make a scraper work would be an unacceptable trade.

---

## 13. Recommended Phase 2 source stack

**Core automated (daily/weekly):**
1. NSF Awards API — filtered to I-Corps, SBIR/STTR, PFI, Convergence Accelerator
2. USAspending — demand-side evidence and incumbent mapping
3. Propeller blog + sitemap — thesis drift monitoring

**Supplemental automated (weekly/monthly):**
4. OpenAlex — researcher and lab corroboration
5. arXiv — categories 1, 2, 8 only
6. Grants.gov forecasts — funding tailwind detection
7. URI / UCSD / WHOI news — narrow filters
8. PatentsView *(once a key is registered)* — university-assignee monitoring

**Manual analyst review (monthly/quarterly):**
9. ARPA-E program pages (403 to automation)
10. NOAA and DOE SBIR award pages
11. Accelerator cohort announcements (StartBlue, SeaAhead, Seaworthy, Hatch, Katapult)
12. Conference proceedings — OCEANS, Ocean Sciences, AMPP

**Not worth using:** Crunchbase/PitchBook (paywalled, and structurally too late), LinkedIn (ToS), listicles (no provenance), generic university news crawlers (signal-to-noise).
