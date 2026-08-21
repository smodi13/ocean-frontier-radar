# Frontier Signals Queue

**Prepared:** 2026-08-21 · **Phase:** 2.5 · Machine-readable: `outputs/frontier_signals.json`

## Why this queue exists separately

Phase 1's hand-built sample was ~39% pre-company. Phase 2's qualified universe was ~6%. The cause was structural, not a bug: 200,000 SBIR company records numerically swamped a few dozen I-Corps awards, and pre-company signals **cannot** compete on a shared scale because they have no customers, no revenue and no financing by definition.

The fix is not to force the company queue back to 39%. It is to stop making them compete. Frontier signals get their own queue and their own framework.

### The frontier framework (deliberately different)

| Dimension | Max | What it measures |
|---|---:|---|
| `translation_intent` | 3 | Is someone actively trying to commercialize this? Licence/spinout = 3, I-Corps or PFI = 2, research funding only = 1 |
| `technical_depth` | 3 | Award scale as a proxy for research substance |
| `ocean_relevance` | 3 | Ocean centrality against the taxonomy |
| `recency` | 3 | Age of the latest signal |

**There is no commercial-traction dimension.** Having none is the norm here, not a weakness. Scores are 0–12 and are **never compared against the 0–17 company score.**

---

## Summary

**31 frontier signals** (target was 20–40).

| Signal type | Count |
|---|---:|
| NSF I-Corps (funded customer discovery, pre-company) | 17 |
| Commercialization grant (PFI / Convergence Accelerator / translation) | 14 |

| Taxonomy | Count |
|---|---:|
| Marine materials | 11 |
| Blue food / aquaculture | 7 |
| Ocean sensing | 5 |
| Offshore energy | 4 |
| Maritime autonomy | 2 |
| Coastal adaptation | 1 |
| Maritime software | 1 |

**Institutions represented:** 27 distinct, with Pratt Institute, Iowa State, MIT and UMCES each appearing twice. Notably **no institution dominates** — which is the point of watching translation programmes rather than a handful of famous labs.

**Recency:** signals span 2022-08 to 2026-08-19. Eight are dated within the last 12 months; the most recent is **two days** before this audit.

---

## The five most interesting Frontier Signals

Analyst judgment, not queue order. **No claim is made about whether Propeller has already seen any of these** — this is an outside-in exercise.

### 1. Autonomous subsea connection system — Oregon State University
*NSF I-Corps, 17 Aug 2026 · Geoffrey Hollinger · maritime autonomy*

**What it is.** An autonomous system that connects and disconnects underwater equipment without divers, handling the control problem created by constant wave motion.

**Why it surfaced.** An I-Corps award four days before this research — the earliest formal signal that a researcher is testing a commercial hypothesis.

**Why it is early.** No company, no product. I-Corps funds ~100 customer interviews; the team is deciding whether a business exists.

**What would have to happen.** Complete customer discovery; establish whether wind developers and cable operators buy autonomous connection as a product or push it to ROV service contractors; secure follow-on SBIR or licence OSU IP; form a company.

**Propeller-relevant problem.** Propeller's own July 2026 ocean-compute post names subsea interconnect and cabling as a hard problem. Commercial diving is described in the award abstract as one of the world's most dangerous professions, so there is a safety driver alongside cost. OSU is one of Propeller's five declared partner institutions — though this sits in the engineering college rather than the oceanography college.

**Next sourcing action.** Track for an SBIR Phase I filing or an OSU licence announcement over the next two to four quarters.

### 2. BioSPACE — biosensing surveillance of pathogens in aquaculture — UMass Lowell
*NSF Convergence Accelerator, $1,000,000, 18 Aug 2023 · blue food*

**What it is.** Biosensor-based surveillance for pathogen detection in aquaculture.

**Why it surfaced.** A $1M translation-track award in a category the Phase 1 research explicitly flagged as **not represented in the publicly disclosed Propeller portfolio reviewed** — aquaculture disease detection.

**Why it is early.** A university programme, not a company. No spinout announcement found.

**What would have to happen.** Field validation on working farms; a sensor cheap enough for thin-margin producers; a decision on whether the buyer is the producer, the insurer or the certifier.

**Propeller-relevant problem.** Disease is among the most severe biological risks in aquaculture, and Propeller's Organics theme is its thinnest named area with one disclosed company.

**Next sourcing action.** Check for spinout formation and for follow-on SBIR; identify the PI and whether they have entered a commercialization programme.

### 3. Backyard Buoys — University of Washington
*NSF Convergence Accelerator, $4,981,779, 15 Sep 2022 · ocean sensing*

**What it is.** Equipping underserved coastal communities with ocean data capability, at ~$5M scale.

**Why it surfaced.** One of the largest translation awards in the queue, at the institution that produced Propeller portfolio company Banyu Carbon.

**Why it is early.** Structured as a research-and-deployment programme rather than a company; commercial vehicle unclear.

**What would have to happen.** A durable operating entity; a buyer other than grant programmes — the classic difficulty in community-facing ocean data.

**Propeller-relevant problem.** Directly addresses Propeller's stated view that "almost every ocean market is under-resourced with information to make decisions".

**Next sourcing action.** Determine whether any commercial entity or licensed technology has emerged; low-cost wave sensing hardware would be the interesting artifact.

### 4. Cost-effective anchor for offshore floating energy — Texas A&M
*NSF PFI, $250,000, 8 Aug 2022 · offshore energy*

**What it is.** A cheaper anchoring system for floating offshore energy platforms.

**Why it surfaced.** Anchoring and mooring are among the least glamorous and most binding cost constraints in floating offshore wind, and this is the only anchor-specific signal in the queue.

**Why it is early.** Small PFI award, oldest of the five, no visible company.

**What would have to happen.** Tank and field validation; engagement with a developer or installation contractor; the qualification path for a novel mooring component is long and standards-bound.

**Propeller-relevant problem.** Propeller holds Aikido (floating offshore wind platforms). Installation and mooring cost is exactly the bottleneck Aikido's port-assembly approach also attacks — potentially complementary.

**Next sourcing action.** Check for continued funding; a stale 2022 award with no follow-on would move this to dormant.

### 5. Marine-adapted RFID for shellfish aquaculture — VIMS / William & Mary
*NSF I-Corps, 19 Aug 2026 · blue food*

**What it is.** Marine-adapted RFID plus analytics for inventory management on commercial shellfish farms, replacing handwritten logs and spreadsheets.

**Why it surfaced.** An I-Corps award two days before this research, at a major marine institution with no public Propeller partnership.

**Why it is early.** Pre-company; PI William Walton is an established shellfish aquaculture researcher rather than a founder.

**What would have to happen.** Establish willingness to pay among small, capital-constrained growers — the perennial aquaculture software problem; decide between hardware sales and a subscription.

**Propeller-relevant problem.** Organics theme; Propeller discloses stealth companies in seafood traceability and processing, so the area appears live for them.

**Next sourcing action.** Watch for company formation or a follow-on SBIR; contact the PI after the I-Corps cohort concludes.

---

## Honest limitations of this queue

1. **It is NSF-only.** I-Corps and PFI are NSF programmes. Equivalent translation signals from DOE, NOAA and DoD are not captured, and no non-US signals are captured at all.
2. **Roughly five of 31 are marginal.** Vanderbilt's porous-silicon diagnostic sensors, UMass Amherst's drone-swarm tracking, Michigan State's water-main inspection robots and a couple of the coatings I-Corps awards are adjacent at best. They sit in a watch queue where a false positive is cheap, but the queue is not 31 strong signals.
3. **Award size is a crude proxy for technical depth.** A $5M Convergence Accelerator award and a $50K I-Corps award measure different things; the framework scores the former higher, which flatters programme scale over research quality.
4. **No PI-level tracking yet.** The highest-value signal in this whole category would be *a researcher's role changing* — academic to founder. That requires person-level monitoring the system does not do.
