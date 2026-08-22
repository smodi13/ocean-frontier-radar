# ARMADA — Competitive & Value-Chain Map

**Phase 3E** · Prepared 2026-08-21. Companies are placed by the **layer of the stack they occupy**, because "UUV competitor" is not a meaningful category for a subsystem vendor.

---

## The stack

```
  MISSION / SERVICE          survey & inspection contractors, Navy operators
        ▲
  PLATFORM (vehicle)         Teledyne, Kongsberg, HII, Saab, L3Harris, C2 Robotics,
        ▲                    Jaia, VATN, Orpheus Ocean
  SUBSYSTEM                  propulsion & control  ← ARMADA (Asymmetric Propulsion)
        ▲                    payload deployment    ← ARMADA (EPADS)
                             energy, navigation, comms
  COMPONENT                  motors, seals, connectors, batteries
```

ARMADA sits at the **subsystem layer, in two different boxes**. That placement determines everything: its customers at the platform layer are also, potentially, the parties who could build the capability themselves.

---

## 1. UUV platform companies — *customers or self-supply, not direct competitors*

| Company | Relevant position | Relationship to ARMADA |
|---|---|---|
| **Teledyne Marine** | Gavia/Slocum lines; appears in the procurement sample selling Navy spares and software maintenance ($1.75M, Jul 2025) | **Potential customer**; also the party most able to build propulsion in-house |
| **Kongsberg** | HUGIN AUVs, the reference product in commercial survey | Potential customer; strong internal engineering |
| **HII Unmanned Systems** (REMUS) | **The most important name here.** REMUS is the host vehicle ARMADA's EPADS was tested on; appears repeatedly in the sample selling MK18 parts and support services | **Potential customer and gatekeeper** — EPADS's demonstrated compatibility is with their vehicle |
| **Saab** | Sabertooth/Seaeye; sold NOAA a long-range AUV ($1.68M, Sep 2025) | Potential customer |
| **L3Harris** (Iver, Ocean Server) | Iver3 sales to Navy and USGS in the sample | Potential customer |
| **C2 Robotics** (AU) | Speartooth LUUV, $5.1M to US Navy Sep 2025 | Potential customer; evidences allied demand |
| **Jaia Robotics** | Micro-UUV pods, $431K Navy Apr 2026 | Potential customer at the small end |

**INFERRED — the structural risk.** Every one of these is simultaneously ARMADA's target customer and its most credible substitute. A propulsion architecture that works is something a platform OEM can attempt to design around or invent around, and the granted claim (regulating *motor speed* to produce intra-revolution differential velocity) does not obviously cover alternative means such as cyclic pitch.

---

## 2. Propulsion / control subsystem providers

**OBSERVED:** no public evidence was found of another company commercialising intra-revolution single-blade thrust vectoring for UUVs. The nearest prior art is patent literature (US 7,841,831, asymmetrically changing rotating blade shape) rather than a fielded product.

**INFERRED:** ARMADA's direct competition at this layer is not another startup — it is **the incumbent architecture itself** (thruster + fins + servos), supplied by established marine actuator and thruster vendors and by OEM in-house engineering. The competitor is inertia and qualification, not a rival product.

---

## 3. Payload delivery / integration

**OBSERVED:** the patent record shows a long history of UUV payload deployment work, including several 1990s-era Navy patents on keel-mounted and cylindrical payload deployment with compartment flooding, and later "autonomous underwater vehicle with external, deployable payload" patents (US 9,701,378; US 10,065,716). **The idea of external deployable payloads is not new.**

**INFERRED:** ARMADA's differentiation is narrower and more specific than "external payload delivery": it is the **zero-net-buoyancy flooding mechanism combined with no host modification and use of the host's native acoustic modem**. That combination is what the joint WO 2024/136933 claims. Whether it is defensible against the older art is a genuine question and is exactly why the US national-phase status matters.

**OBSERVED:** in the procurement sample the payload-deployment bucket is only **$1.1M across four contracts in 13 years** — there is barely an observable market for this capability yet.

---

## 4. Underwater sensing systems

Adjacent rather than competitive. EPADS is a **delivery mechanism for someone else's sensor**. Sensor vendors are therefore **complementors**, and the sensor/payload bucket in the procurement sample ($9.6M) represents payloads that would need delivering.

---

## 5. Defense primes / integrators

**OBSERVED:** Arete Associates ($41.6M integration services), Northrop Grumman (DARPA Hunter, $24.8M + $4.9M), General Dynamics Mission Systems, Metron, and the FFRDC/university complex (UT Austin ARL $15.8M+$8.9M+, JHU APL, Penn State).

**INFERRED:** these are the **channel and the competition simultaneously**. A subsystem reaches a programme of record through a prime, on the prime's commercial terms; and primes bid the same R&D dollars ARMADA currently lives on.

---

## 6. Research-developed alternatives — including ARMADA's own origin

**OBSERVED:** WHOI appears in the procurement sample as a **supplier** on five contracts totalling roughly $11.3M, including selling the Navy a REMUS 600 ($1.99M, Aug 2025) and next-generation AUV sensor development ($4.74M, Mar 2024).

**INFERRED:** this is a genuine and under-appreciated dynamic. WHOI owns the propulsion patents ARMADA licenses, is joint applicant on the EPADS filing, employs (or recently employed) ARMADA's Lead Engineer, and independently sells vehicles and R&D to the same Navy customer. That relationship is an asset — and a dependency worth understanding precisely.

---

## 7. Propeller portfolio adjacencies

Mapped separately and deliberately **not** labelled competitors by default. Nothing here implies any knowledge of Propeller's internal views or pipeline.

| Portfolio company | What it does (per Propeller's public description) | Relationship | Reasoning |
|---|---|---|---|
| **Orpheus Ocean** | "Reducing launch costs for full ocean depth monitoring" — low-cost untethered full-ocean-depth AUVs with seafloor sampling; incubated at WHOI | **Different layer of stack — potentially complementary** | Orpheus builds *vehicles*; ARMADA sells *subsystems*. In principle Orpheus is a customer. **However**: both are WHOI-originated, both target low-cost autonomy, and Orpheus does its own vehicle engineering including propulsion choices. Whether it would adopt an external subsystem or build its own is **unclear** and is a question for Propeller, not for us. |
| **VATN Systems** | "Low-cost, mixed-mission AUVs" with proprietary inertial navigation and interchangeable payloads; defence-focused | **Potentially competitive *and* potentially complementary** | VATN's stated design centre — low cost, modular, mixed-mission, attritable, defence — is the closest match in the disclosed portfolio to ARMADA's target application. "Interchangeable payloads" overlaps conceptually with EPADS. But VATN is a *platform* company and ARMADA a *subsystem* company, so the honest label is **potentially competitive at the capability level, complementary at the stack level**. Which it turns out to be depends on whether VATN buys or builds. |
| **Fleet Robotics** | Autonomous hull-crawling robots for biofouling removal | **Different layer / different mission** | Shares "maritime robotics" but addresses hull servicing, not free-swimming vehicle propulsion or payload delivery. No meaningful overlap. |
| **Navier** | Electric hydrofoiling surface vessels | **Unrelated** | Surface craft, passenger/transport, different physics and buyers. |
| **Aquatic Labs** | Real-time ocean sensing, mCDR MRV, eDNA | **Complementary** | A sensing company whose instruments are the kind of payload EPADS exists to deliver. |
| **Indeximate** | Subsea cable monitoring | **Complementary** | Cable inspection is a plausible end application for a survey-plus-inspection vehicle. |

**The portfolio-thinking point, stated carefully.** Propeller's disclosed portfolio contains **two AUV platform companies**. A subsystem vendor selling into AUV platforms sits in an unusual position relative to that: complementary if the platforms buy, awkward if they build, and a source of useful diligence access either way. **We cannot and do not claim to know how Propeller views this.** It is simply the most interesting portfolio-fit question the evidence raises, and it is one a partner is far better placed to answer than an outside analyst.
