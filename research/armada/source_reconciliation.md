# ARMADA — Source Reconciliation

**Prepared:** 2026-08-21 · **Phase:** 3A · All sources accessed 2026-08-21.
**Purpose:** resolve the factual inconsistencies carried out of Phase 2/2.5 *before* any underwriting.

> Phase 1, Phase 2 and Phase 2.5 outputs are **not edited**. Corrections are recorded here. Where an earlier report was wrong, that is stated plainly.

---

## 1. EPADS IP — substantially resolved, and it changes the picture

### What Phase 2.5 said
> "The Jan 2025 WHOI licence announcement names US 9,873,499 and US 11,990,857 only. The EPADS work traces to US 10,112,686, also WHOI-assigned, which is not named. What rights ARMADA holds to the EPADS IP is unresolved."

That framing was **incomplete**. It assumed EPADS necessarily rested on the older WHOI vacuum-hold patents. Searching the patent record by applicant rather than by guessing the family produced a different answer.

### The complete publicly visible EPADS-relevant IP chain

| Publication | Title | Inventors | **Applicant(s)** | **Assignee** | Priority | Filed | Published/Granted | Status |
|---|---|---|---|---|---|---|---|---|
| **WO 2024/136933 A2** (A3 2024-08-02) | **External payload deployment system** | Jeffrey **Kaeli**, Robin **Littlefield**, Carl **Fiester** | **ARMADA Marine Robotics Inc *and* Woods Hole Oceanographic Institution (joint)** | ARMADA Marine Robotics Inc, WHOI | 2022-09-21 | 2023-09-21 | 2024-06-27 | PCT published |
| US 10,112,686 B2 | System for the deployment of marine payloads | Austin, Purcell, Littlefield, Jaffre, Packard, McDonald | WHOI | WHOI | 2015-01-30 | 2016-01-29 | granted 2018-10-30 | active, expiry 2036-01-29 |
| US 11,072,406 B2 | System for the deployment of marine payloads (CIP of the above) | same six | WHOI | WHOI | 2016-01-29 | 2018-09-19 | granted 2021-07-27 | active, expiry 2036-04-25 |
| US 10,640,188 B1 | Passive ballast device, system and methods | **Kaeli**, **Littlefield**, Jakuba, Guest | WHOI | WHOI | 2017-10-16 | 2018-10-16 | granted 2020-05-05 | active, expiry 2038-10-16 |
| US 2021/0276679 A1 | Passive ballast device (continuation) | as above | WHOI | WHOI | 2017-10-16 | — | published 2021-09-09 | application |

### The material finding

**WO 2024/136933 lists ARMADA Marine Robotics Inc as a joint applicant alongside WHOI, with ARMADA's CEO (Kaeli) and Lead Engineer (Littlefield) among the three named inventors.**

This is a different posture from "WHOI owns it, ARMADA licenses two unrelated patents". Two further points sharpen it:

1. **The mechanism differs from the older WHOI patents.** US 10,112,686 / 11,072,406 claim holding a payload by **vacuum force** and releasing it by breaking the vacuum. WO 2024/136933 claim 1 covers a deployment pod with "a hollow interior, a valve that selectively seals said hollow interior, a release, and a controller … configured to actuate said valve to flood said hollow interior in whole or part with water and actuate said release". The SBIR Phase II abstract describes the same approach: a neutrally ballasted payload where, on acoustic command, "a motor opens a valve that floods a vacuum, making the payload negatively buoyant". EPADS appears to be **new IP filed during ARMADA's Navy work**, related to but distinct from the older WHOI family.
2. **The priority date (2022-09-21) falls between the Navy Phase I award (Oct 2021) and Phase II (Jan 2023)** — consistent with invention arising from the funded programme.

### What is established and what is not

**Publicly established:**
- ARMADA is a **named joint applicant and joint listed assignee** on the published EPADS PCT application.
- ARMADA's CEO and Lead Engineer are **named inventors** on it.
- WHOI separately owns three earlier related patents on marine payload deployment and passive ballast, on which Littlefield and/or Kaeli are inventors.
- The Jan 2025 exclusive licences cover **only** the two propulsion patents (9,873,499 and 11,990,857), for use in underwater and marine surface vehicles.

**Not established from public records:**
- Whether a **US national-phase application** from WO 2024/136933 has been filed or published. A search of the patent corpus returned only the WO A2/A3 publications; no US family member was found. **A PCT publication is not a granted US patent and confers no US exclusionary right by itself.**
- The **ownership split, field-of-use, exclusivity, sublicensing and commercialization rights** as between ARMADA and WHOI on the jointly-applied EPADS application.
- Whether ARMADA holds any licence to US 10,112,686, US 11,072,406 or US 10,640,188 — none is named in any announcement found.

> **Correctly phrased diligence question:** *Public records establish that ARMADA is a joint applicant and joint listed assignee on the published EPADS PCT application with WHOI, and that its founders are named inventors. The allocation of ownership, field-of-use and commercialization rights between the co-applicants — and whether any US national-phase protection has been secured — could not be confirmed from public sources.*
>
> This is **not** a legal opinion, **not** a freedom-to-operate assessment, and **not** a claim that ARMADA lacks rights. Joint applicant status is materially stronger than the Phase 2.5 framing implied, and the residual question is narrower.

**Correction to Phase 2.5:** the statement that EPADS IP rights were "unresolved" with the implication that ARMADA might hold none understated ARMADA's position. The evidence supports joint applicant status. Phase 2.5 is left unedited; this supersedes it.

---

## 2. Navy Phase II contract N68335-23-C-0142 — fully reconciled

Authoritative source: USAspending award record `CONT_AWD_N6833523C0142_9700_-NONE-_-NONE-` plus its **complete transaction history**.

### Modification history (this is the reconciliation)

| Date | Mod | Obligation | Action |
|---|---|---:|---|
| 2023-01-30 | base | $999,028 | Award — "Research and Development" |
| 2025-01-21 | P00001 | +$499,949 | **EXERCISE AN OPTION** |
| 2025-01-30 | P00002 | $0 | **EXTENDING POP (CLINs 0001–0003)** |
| **2026-03-10** | **P00003** | **+$499,949** | **INCREMENTALLY FUNDING CLIN 0004** |
| | **Total obligated** | **$1,998,926** | |

The three obligations sum exactly to the record's `total_obligation` of $1,998,926. `base_exercised_options` is also $1,998,926; no separate `base_and_all_options_value` (ceiling) is published.

### Contract attributes
Definitive contract · Department of the Navy · NAICS 541715 (R&D in physical/engineering/life sciences) · PSC AC12 (National Defense R&D Services, Applied Research) · place of performance Falmouth, MA · date signed 2023-01-30 · period of performance **2023-01-30 → 2028-03-20**, potential end also 2028-03-20 · award record last modified 2026-03-10 · total outlay not published.

### Correcting the Phase 2 / 2.5 language

| Claim | Status |
|---|---|
| "The Navy Phase II value doubled" | **Imprecise.** It did not double by revaluation. The base was $999,028; the Navy **exercised an option** (+$499,949, Jan 2025) and then **incrementally funded a fourth CLIN** (+$499,949, Mar 2026). The mechanism matters — an exercised option is a customer decision, which is a *stronger* signal than a price increase. |
| "Runs to 2028" | **Supported by USAspending** (POP end 2028-03-20, potential end identical), which is the authoritative federal financial record and was last modified 2026-03-10. |
| SBIR.gov reportedly shows an end date in **January 2027** | **Could not be independently verified in this session.** SBIR.gov's award search is JavaScript-rendered and its API returns HTTP 403; no access-control bypass was attempted. The official SBIR bulk download I hold (data through 2023) records this contract at the **base $999,028 with end date 2025-01-31** — i.e. the pre-option state. A Jan-2027 figure would sit between the bulk file's 2025 date and USAspending's 2028 date, consistent with SBIR.gov reflecting mod P00002 but not P00003. **I am treating 2028-03-20 as the current figure because it comes from the authoritative financial system and is the more recently updated record, while flagging the discrepancy as unreconciled.** Anyone relying on the end date should confirm it directly. |

**The most important fact in this section is not the total.** It is that on **10 March 2026 — five months before this analysis — the Navy put another $499,949 onto a new CLIN.** That is the most recent hard evidence of ARMADA's operating status, and it is more current than anything on the company's own website, whose media page ends in January 2024.

---

## 3. Leadership

From ARMADA's own team page (armadamarinerobotics.com/team, accessed 2026-08-21), the company publicly identifies **three people**:

| Person | Title (verbatim) | Background (paraphrased from the page) |
|---|---|---|
| **Jeff Kaeli** | **CEO, Co-Founder, Co-Inventor** | PhD, MIT/WHOI Joint Program in Oceanographic Engineering. Published in underwater imaging, navigation, perception, autonomy. Operated underwater robots at naval bases in the US and Europe. "Jeff has led the Asymmetric Propulsion development effort over the past several years at WHOI." |
| **Philip "Rusty" Warren** | **Lead Director, Co-Founder** | 30+ years of business leadership within the federal government and government contractors; entrepreneur. |
| **Robin Littlefield** | **Lead Engineer, Co-Founder, Co-Inventor** | Mechanical engineer, 10+ years at WHOI; over a year of cumulative time at sea across deep-ocean searches and UUV operations supporting the US Navy. |

**Chronology note.** The WHOI release of 7 Jan 2025 describes Littlefield as "Senior Engineer in Applied Ocean Physics & Engineering **at WHOI**" and Kaeli as "Co-Founder and CEO". ARMADA's own page describes Littlefield's WHOI experience without stating he has left. **Unknown:** whether Littlefield is full-time at ARMADA or holds a continuing WHOI role. That matters for execution risk and is a founder question.

**Team size.** Only three people are publicly identified. A figure of ~8 employees appears in secondary aggregators and was deliberately **not** ingested (tier-3). Treat headcount as unknown.

---

## 4. Product / programme lines

ARMADA's own technology page describes **two** product lines. A third area exists in the funding record but is **not** presented as a product by the company.

### 4.1 Asymmetric Propulsion — propulsion/control subsystem

| Field | Evidence |
|---|---|
| **Technical problem** | UUVs are optimised for efficient large-area survey but detailed inspection needs station-keeping and precise low-speed manoeuvring, which typically requires deploying a *second* asset such as an ROV. |
| **Technical approach** | Vary the speed of a single-bladed propeller within each rotation, producing thrust *and* steering from one motor; eliminates fins and additional control motors. |
| **Maturity** | Peer-reviewed/conference publications 2018 (IEEE/OES AUV Workshop, Porto) and 2019 (MTS/IEEE OCEANS, Seattle). Company blog reports "Asymmetric Propulsion Passes a Critical 3D Steering Test" (28 Sep 2022). |
| **Funding** | NSF STTR Phase I, $255,821 (2020-08-01 → 2021-06-30), RI: WHOI. |
| **Customer evidence** | **None public.** Site says the propulsion solution is one ARMADA "is bringing to market" — future tense. |
| **IP** | US 9,873,499 and US 11,990,857 — WHOI-owned, **exclusively licensed to ARMADA** for underwater and marine surface vehicles (announced 30 Jul 2020 and again 7 Jan 2025 under WHOI's Express License program). |
| **Key unknown** | Whether any UUV OEM has integrated or committed to integrate it. |

### 4.2 EPADS — External Payload Delivery System

| Field | Evidence |
|---|---|
| **Technical problem** | Navy requirement for external payload deployment from cylindrical UUVs 5–21 inches in diameter. |
| **Technical approach** | Fully external pod, **no mechanical modification to the host robot**; commands over the robot's **native acoustic modem**; payload neutrally ballasted, and on acoustic release a motor opens a valve flooding the cavity so the payload becomes negatively buoyant and descends. Company claims "a patented technique to affect a **zero net buoyancy change** on the robot before and after deployment". |
| **Maturity** | Phase I established an **A-size (4.875" × 36")** body delivering a **5 kg module**; hydrodynamic simulations **validated with in-water testing** using dummy payloads carried on a **REMUS 600**. Confirmed two external A-size payloads reduce mission time by **≤25%** with **<10% parasitic drag**. Phase II goal: "characterizing and optimizing the placement accuracy". |
| **Funding** | Navy SBIR Phase I $246,320 (2021-10-20); Phase I Option (Jul 2022); Phase II $1,998,926 (2023-01-30 → 2028-03-20), option exercised Jan 2025, CLIN 0004 incrementally funded Mar 2026. |
| **Customer evidence** | **Funded development for the Navy. No production order or commercial sale is publicly evidenced.** |
| **IP** | WO 2024/136933 — **joint ARMADA/WHOI applicant**; related WHOI-owned US 10,112,686 / 11,072,406 (vacuum-hold family). |
| **Key unknown** | Whether Phase II leads to a programme of record or production contract; US national-phase IP status. |

### 4.3 Persistent sensing / passive-float work — **an R&D programme, not a product**

| Field | Evidence |
|---|---|
| **Status** | **Not listed on ARMADA's technology page.** It exists only in the NOAA award record. |
| **Funding** | NOAA SBIR Phase I, $174,798, 2024-08-01 → 2025-01-31. |
| **Stated objective** (award abstract) | Combine "innovative propulsion and ballast technologies to create a new class of uncrewed underwater sensing platform with both mobility and persistence", selectively riding ocean currents, aiming at "a constellation of platforms"; reduce the carbon footprint of in-situ ocean monitoring and eliminate single-use sensor waste. |
| **Related IP** | WHOI's **US 10,640,188** passive ballast patent names Kaeli and Littlefield as inventors — a plausible technical basis, though no licence to it is publicly announced. |
| **Key unknown** | Whether any Phase II followed; the Phase I ended Jan 2025 and no successor award appears in USAspending. |

> **Terminology correction to Phase 2.5.** Phase 2.5 called this a "persistent sensing constellation" product line. That over-reads the evidence: "constellation" is the *aspiration* stated in a Phase I proposal abstract. It should be described as **a completed NOAA Phase I R&D effort with no publicly evidenced follow-on**.

> **Also to be explicit:** SBIR/STTR awards and Navy contract obligations are **funded technical demand, not revenue and not product-market fit.** No commercial sale by ARMADA is evidenced anywhere in the public record reviewed.

---

## 5. Corrections summary

| # | Earlier statement | Correction |
|---|---|---|
| 1 | Phase 2.5: EPADS IP rights "unresolved", implying ARMADA might hold none | ARMADA is a **joint applicant and joint listed assignee** on the EPADS PCT (WO 2024/136933) with its founders as inventors. Residual question is narrower: ownership split, field of use, and US national-phase status. |
| 2 | Phase 2.5: Navy Phase II "value doubled" | Base $999,028 + **exercised option** $499,949 + **incremental CLIN 0004 funding** $499,949 = $1,998,926. The mechanism is a stronger signal than a revaluation. |
| 3 | Phase 2.5: "runs to 2028" | Supported by USAspending (2028-03-20). A reported SBIR.gov end date of Jan 2027 could not be verified in-session; discrepancy flagged, not resolved. |
| 4 | Phase 2.5: "persistent sensing constellation" as a product line | A completed **NOAA Phase I R&D effort**; "constellation" is proposal language. No follow-on evidenced. |
| 5 | Phase 2: ARMADA "~8 employees" (tier-3) | **Three** people publicly identified on the company site. Headcount unknown. |
