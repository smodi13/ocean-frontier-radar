# ARMADA — Bottom-Up Procurement Market

**Phase 3D** · Reproducible via `python3 src/ofr/models/procurement_audit.py` → `outputs/armada_procurement_audit.json`.

> **This is not a TAM and must not be quoted as one.** Every figure is *observed federal contract value in a keyword-derived sample* from USAspending. It is evidence that budgets and buying behaviour exist. It excludes classified programmes, foreign and allied buyers, commercial/offshore buyers, and any US federal spending that does not use the keywords searched. Real DoD undersea spending is certainly larger than this sample; **the sample's value is its granularity, not its completeness.**

---

## 1. Audit of the 87 contracts

87 maritime-autonomy contracts, **$244,757,931** observed, spanning **2014–2026** (13 years). Every contract is classified by a stated rule, and false comparables are removed transparently.

| Bucket | n | Observed value | Annualised | Why it is in this bucket |
|---|---:|---:|---:|---|
| R&D programme | 13 | $69,037,937 | $5,310,611 | Funded R&D. Demand signal, not a repeatable product line item. |
| Integration / prime | 3 | $65,732,962 | $5,056,382 | Prime and system-integration work. A subsystem vendor sells *into* this, it does not win it. |
| Platform purchase | 35 | $60,262,183 | $4,635,553 | Purchase or lease of a complete vehicle. |
| Services / support | 10 | $19,530,636 | $1,502,357 | Sustainment, evaluation and labour. |
| **Components / spares** | **11** | **$9,624,113** | **$740,316** | Component and consumable hardware — the propulsion-subsystem slice. |
| Sensors / payload dev | 6 | $9,575,985 | $736,614 | Sensor and comms payloads — what an EPADS pod would carry. |
| *Excluded: facilities* | 1 | $8,756,246 | — | **Military construction** (a $8.76M building). Not a UUV market. |
| **Payload deployment** | **4** | **$1,116,090** | **$85,853** | Payload carriage/deployment hardware — the EPADS slice. |
| Launch & recovery | 3 | $958,664 | $73,743 | Adjacent to, but not, propulsion or payload. |
| *Excluded: counter-UUV* | 1 | $163,115 | — | **Defeating** vehicles, not buying them. |

**Removed as false comparables: 2 contracts, $8,919,361** — a design-build contract for Building 1371 and a counter-UUV services contract. Both matched the keyword and neither is addressable by anyone selling UUV subsystems.

---

## 2. The two addressable cases

### Narrow addressable — what ARMADA could win *directly*
Components/spares + payload deployment: **15 contracts, $10,740,202 over 13 years ≈ $826,169 per year.**

This is the slice where a propulsion or payload subsystem could be the line item itself. It is dominated by Defense Logistics Agency hardware buys — W S Darley & Co appears **24 times** across the full sample, functioning as the government's UUV hardware reseller channel.

### Broad adjacency — reachable only through OEMs or by expanding scope
Narrow + complete-vehicle purchases + sensor/comms payloads + launch & recovery: **59 contracts, $81,537,034 ≈ $6,272,080 per year.**

### Platform-embedded case
If propulsion/control is taken as **10% of complete-vehicle contract value** — *an explicit analyst assumption, not sourced* — the observed platform spending of $60.3M implies **$6,026,218 of embedded subsystem value over 13 years, ≈$464K/year.**

---

## 3. What this actually says about ARMADA

**This is the most important — and most uncomfortable — finding in the diligence.**

The directly addressable federal procurement visible in this sample is **under $1M per year**. Even the generous adjacency case is ~$6.3M per year. A venture-scale outcome cannot be built on the slice of this sample that ARMADA can sell into directly.

Where the money actually is:
- **R&D programmes ($69.0M)** — which is precisely where ARMADA earns today. This is a real, sustained federal appetite, and it explains the company's funding record. But R&D contracts are won repeatedly and bespokely; they are the "engineering organisation" model, not the "component product" model.
- **Integration primes ($65.7M)** — Arete Associates alone took $41.6M for integration services. A subsystem vendor's route to this money is *through* a prime, on the prime's terms.
- **Complete platforms ($60.3M)** — the OEM channel. This is where propulsion revenue would live, and it requires an OEM to adopt.

### Honest caveats that cut *for* ARMADA
1. **The sample is not the market.** Large UUV programmes of record (e.g. XLUUV-class) are procured under nomenclature these keywords do not catch, and classified work is invisible. The true federal undersea market is far larger.
2. **DLA hardware buys are visible because they are small and routine.** Subsystem content inside a $24.8M DARPA programme does not appear as a component line.
3. **Payload deployment shows only $1.1M** — but that is arguably because *the capability does not exist yet*. A market cannot be observed before the product. This is the classic problem with bottom-up sizing of a genuinely new capability, and it is a fair rebuttal.

### Honest caveats that cut *against* ARMADA
1. Thirteen years of data show **no growth trend** in the component/spares bucket that would suggest an emerging subsystem market.
2. The most frequent supplier in the sample is a **distributor** (W S Darley), not a technology vendor — consistent with a market that buys commodity hardware and complete systems, not novel subsystems.
3. Universities and FFRDCs — UT Austin ARL, JHU APL, Penn State, WHOI — capture a large share of the R&D money. **ARMADA competes with its own former institution for this work**, and WHOI appears in the sample as a supplier on five contracts totalling ~$11.3M.

---

## 4. Demand-side conclusion

**OBSERVED:** federal demand for UUV capability is real, recurring across 13 years, and dominated by R&D and complete-platform procurement.

**INFERRED:** ARMADA's current revenue model is aligned with the *largest* observed bucket (R&D), and its stated product ambition (propulsion subsystems) is aligned with the *smallest* observed bucket. Closing that gap requires either an OEM design win — which converts the platform bucket into addressable revenue — or a shift toward selling complete vehicles or systems, which is a different and far more capital-intensive company.

**UNKNOWN:** whether any OEM relationship exists. Nothing public indicates one.
