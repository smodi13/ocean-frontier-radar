# ARMADA — Technical Diligence

**Phase 3B** · Prepared 2026-08-21 · All sources accessed 2026-08-21.
Each product line is assessed independently before any company-level judgement. Claims are tagged **OBSERVED** (public source supports it), **INFERRED** (our reading), **UNKNOWN** (needs primary research).

---

## 1. Asymmetric Propulsion

### What it does
**OBSERVED.** Varying the rotational speed of a **single-bladed propeller within each revolution** produces both axial thrust and a lateral turning moment from one motor. The patent claim is on the *control method* — "regulating the motor speed to produce differential velocity within a single revolution of the propeller across sequential rotations and generate a turning moment" (US 9,873,499, claim 1) — not on a propeller geometry. US 11,990,857 adds the sensing/feedback layer that measures and adjusts inter-rotational angular velocity.

### Hardware it removes
**OBSERVED.** ARMADA states it eliminates "the need for fins and additional motors for control", reducing "size, weight, drag, and complexity".

**INFERRED.** On a conventional small/medium UUV this displaces a control-surface actuator set (typically 2–4 fin servos plus linkages and their pressure penetrations). Each penetration and actuator is a failure point and a drag source, so the reliability argument is structurally credible, independent of the marketing.

### The problem ARMADA says it solves
**OBSERVED.** From the technology page: UUVs are built for efficient large-area survey, but detailed inspection requires station-keeping and precise low-speed manoeuvring, which "typically require deploying an additional asset, such as a Remotely Operated Vehicle". Asymmetric Propulsion is positioned to give one vehicle both survey and inspection capability.

**INFERRED — and this is the sharper framing.** The value proposition is *not primarily cost per propeller*. It is **avoiding a second vessel-day and a second asset mobilisation**. That is a far larger economic unit than a propulsion module, and it is the argument that would justify an integration effort.

### Technical evidence ladder

| Rung | Evidence | Status |
|---|---|---|
| Theory / peer review | "AUV Propulsion and Maneuvering by Means of Asymmetric Thrust", IEEE/OES AUV Workshop, Porto **2018**; "Asymmetric Propulsion: Thrust and Maneuverability from a Single Degree of Freedom", MTS/IEEE OCEANS, Seattle **2019** | **OBSERVED** |
| Granted IP | US 9,873,499 (2018), US 11,990,857 (2024) | **OBSERVED** |
| Bench / component test | — | **UNKNOWN** |
| In-water vehicle test | Company blog: "Asymmetric Propulsion Passes a Critical 3D Steering Test", **28 Sep 2022** | **OBSERVED** (self-reported, not independently published) |
| Quantified efficiency data | No public figures for propulsive efficiency, turning radius, or power draw versus a finned baseline | **UNKNOWN** |
| Endurance / reliability data | No MTBF, no long-duration deployment data | **UNKNOWN** |
| Third-party or customer validation | None found | **UNKNOWN** |

### Limitations and open technical questions
- **INFERRED.** A single-bladed propeller is inherently unbalanced. Vibration, bearing loading and acoustic signature are the obvious concerns. **Acoustic signature matters disproportionately for a Navy customer**, and no public data addresses it.
- **INFERRED.** Generating a turning moment by modulating within a revolution implies the control authority scales with propeller RPM. At very low speed — precisely the station-keeping case ARMADA markets — thrust and therefore control authority may be smallest. Whether this is genuinely limiting or engineered around is the central unknown.
- **OBSERVED.** Prior art includes a 2010 patent on an "asymmetrically changing rotating blade shape propeller" and single-blade propellers dating to 1945/1967. The concept space is not empty; the differentiation is the intra-revolution velocity control.

### What would need to be true for an OEM to adopt it
1. The reliability gain from removing actuators must exceed the reliability risk of a novel unbalanced propulsion element **over a full deployment cycle**, with data.
2. Low-speed control authority must be sufficient for real inspection tasks in real currents — not just a tank demonstration.
3. Acoustic signature must be acceptable for defence use.
4. The integration must be genuinely drop-in. An OEM redesigning a hull form, control software and autonomy stack around a new propulsion architecture is a multi-year programme, not a purchase.
5. **The hardest barrier, INFERRED:** the buyer of a UUV is buying a *qualified system*. Changing propulsion invalidates qualification. This is the single largest adoption obstacle and it is commercial-technical, not purely technical.

---

## 2. EPADS — External Payload Delivery System

This is the **best-evidenced** part of ARMADA, and the evidence is specific and quantitative.

### Technical approach
**OBSERVED.** Fully external pod requiring **no mechanical modification** to the host robot; commands travel over **the robot's native acoustic modem**. The payload is neutrally ballasted; on acoustic release command "a motor opens a valve that floods a vacuum, making the payload negatively buoyant so it detaches and descends to the seafloor" (Navy Phase II abstract). ARMADA describes "a patented technique to affect a **zero net buoyancy change** on the robot before and after deployment".

**INFERRED.** The zero-net-buoyancy claim is the clever part. Releasing mass from a neutrally buoyant vehicle normally makes the vehicle positively buoyant and forces a trim correction; flooding the pod cavity as the payload departs conserves the vehicle's net buoyancy. That is what allows deployment mid-mission without disturbing vehicle trim — and it is what the WO 2024/136933 claim covers.

### Technical evidence ladder — the important table

| Rung | What was actually done | Status |
|---|---|---|
| **Modelled** | Hydrodynamic simulations of external payload carriage | **OBSERVED** |
| **Tank / dummy tested** | "Proprietary hydrodynamic A-size dummy payloads" fabricated | **OBSERVED** |
| **In-water tested on a real host vehicle** | Dummy payloads carried on a **REMUS 600 UUV**; simulations validated against in-water results | **OBSERVED** |
| **Quantified performance thresholds met** | Two external A-size payloads reduce UUV mission time by **≤25%**; parasitic drag **<10%** over unmodified vehicle | **OBSERVED** |
| **Live release demonstrated at depth** | Not described in any public source found. Phase II objective is "characterizing and optimizing the **placement accuracy**", which implies release testing is Phase II work in progress | **UNKNOWN** |
| **Placement accuracy quantified** | The stated Phase II goal; no results published | **UNKNOWN** |
| **End-customer validation / operational use** | None public | **UNKNOWN** |
| **Production order** | None public | **UNKNOWN** |

### Specifications established
**OBSERVED.** A-size form factor **4.875" diameter × 36"**, carrying a **5 kg module**; host compatibility target is cylindrical UUVs **5–21 inches** in diameter; demonstrated host is the **REMUS 600**.

### Reading the ≤25% / <10% numbers honestly
**INFERRED.** These are *acceptance thresholds confirmed*, not performance achievements. A 25% mission-time reduction from carrying two payloads is a **real operational cost** — it is the price of the capability, not a benefit. The correct interpretation is: the Navy set a bound, and ARMADA demonstrated the design stays inside it. For a mission where deploying the payload *is* the objective, that trade is obviously acceptable. For a survey operator who wants payload delivery as a secondary capability, a quarter of endurance is a significant tax.

### Open technical questions
- Placement accuracy in current — what CEP at what depth? This is the Phase II question and the answer determines whether EPADS serves precision applications (sensor emplacement, cable-adjacent work) or only approximate drops.
- Behaviour with **one** payload released and one retained — asymmetric drag and trim.
- Depth rating; corrosion and biofouling over long carriage durations.
- Whether the acoustic-modem command path is robust in multipath-limited shallow water.

---

## 3. Persistent sensing / passive-float work

**OBSERVED.** This is **not presented as a product** on ARMADA's technology page. It exists in one funding record: NOAA SBIR **Phase I**, $174,798, 2024-08-01 → 2025-01-31.

**OBSERVED (award abstract).** Objective is to combine "innovative propulsion and ballast technologies to create a new class of uncrewed underwater sensing platform with both mobility and persistence", using an operations strategy that "selectively rides ocean currents, enabling a constellation of platforms", reducing the carbon footprint of in-situ ocean monitoring and eliminating single-use sensor waste.

**INFERRED.** The technical basis is plausibly WHOI's **US 10,640,188** passive ballast patent — a chamber with a pressure-responsive compensator giving depth-varying buoyancy *without active pumping* — on which **Kaeli and Littlefield are named inventors**. Combining passive ballast with asymmetric propulsion would give a low-power platform that can change depth to select current layers and steer weakly. That is a coherent technical concept.

**UNKNOWN.** No licence to US 10,640,188 is publicly announced. No Phase II or follow-on award appears in USAspending. The Phase I ended in January 2025 and nothing public has followed.

> **Terminology discipline.** Calling this a "constellation" product overstates it. The correct description is: **a completed six-month NOAA Phase I R&D effort with no publicly evidenced continuation.** Phase 2.5 described it as a product line; that was wrong and is corrected here.

---

## 4. Company-level technical assessment

**Strengths (OBSERVED).** Two granted patents with readable claims and an exclusive licence; a third, jointly-applied patent family arising from the funded work; peer-reviewed conference publications; and — uniquely among the three lines — **EPADS has quantified in-water test results on a real Navy host vehicle.** The founding team's technical credibility is unusually well evidenced: a joint MIT/WHOI PhD who led the propulsion work at WHOI, and a WHOI mechanical engineer with a year of cumulative sea time.

**Weaknesses (OBSERVED/INFERRED).** No public performance data of any kind for the propulsion product ARMADA says it is "bringing to market" — no efficiency, turning-radius, power or acoustic figures. Three people publicly identified. The technical evidence is concentrated in the Navy-funded EPADS line, while the commercial pitch leads with propulsion.

**The technical tension worth naming.** ARMADA's *marketed* product (propulsion) has the weakest public evidence. Its *best-evidenced* work (EPADS) is a Navy-funded development programme. The strongest technical proof point and the strongest commercial story are not the same product line.
