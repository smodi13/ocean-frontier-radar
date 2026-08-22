import Link from 'next/link';
import { Callout, Chip, PageHeader, Section, Stat } from '@/components/Primitives';
import { ProcurementBuckets } from '@/components/Procurement';
import ScenarioModel from '@/components/ScenarioModel';
import { armada, evidenceRegister, fmtMoney, fmtNum } from '@/lib/data';

export const metadata = { title: 'ARMADA Marine Robotics · Outside-In Diligence' };

/* eslint-disable @typescript-eslint/no-explicit-any */

export default function DeepDivePage() {
  const a = armada;
  const gov = a.government;
  const proc = a.procurement;
  const model = a.model;

  return (
    <>
      <PageHeader
        eyebrow="Outside-in venture diligence · public sources only"
        title="ARMADA Marine Robotics"
        lede="A WHOI spin-off building propulsion and payload-delivery subsystems for uncrewed underwater vehicles."
      />

      {/* ── Recommendation ─────────────────────────────────────────── */}
      <Section>
        <div className="card overflow-hidden">
          <div className="border-b border-paper-line bg-rust-pale/50 px-6 py-5 sm:px-8">
            <p className="eyebrow text-rust">Recommendation</p>
            <p className="mt-1 text-2xl font-semibold tracking-tight text-rust sm:text-3xl">
              {a.recommendation.verdict}
            </p>
          </div>
          <div className="px-6 py-6 sm:px-8">
            <p className="body max-w-prose">{a.recommendation.summary}</p>
            <h3 className="h3 mt-6 mb-3 text-[14px]">Three questions public information cannot answer</h3>
            <ol className="grid gap-3 lg:grid-cols-3">
              {a.recommendation.unresolved.map((u: any, i: number) => (
                <li key={u.title} className="rounded border border-paper-line bg-paper p-4">
                  <div className="mono text-rust">{String(i + 1).padStart(2, '0')}</div>
                  <div className="mt-1 text-[14px] font-semibold">{u.title}</div>
                  <p className="meta mt-1.5">{u.detail}</p>
                </li>
              ))}
            </ol>
            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              <div className="rounded-md border-l-[3px] border-l-moss bg-moss-pale/40 px-4 py-3">
                <p className="text-[12px] font-semibold uppercase tracking-wider text-moss">Advance if</p>
                <p className="body mt-1 text-[14px]">{a.recommendation.advance_if}</p>
              </div>
              <div className="rounded-md border-l-[3px] border-l-rust bg-rust-pale/40 px-4 py-3">
                <p className="text-[12px] font-semibold uppercase tracking-wider text-rust">Pass if</p>
                <p className="body mt-1 text-[14px]">{a.recommendation.pass_if}</p>
              </div>
            </div>
            <p className="meta mt-5 max-w-prose">{a.recommendation.no_invest_note}</p>
          </div>
        </div>
      </Section>

      {/* ── Why interesting ────────────────────────────────────────── */}
      <Section title="Why this is interesting" className="pt-0">
        <div className="grid gap-3 lg:grid-cols-3">
          {a.whyInteresting.map((w: any) => (
            <div key={w.title} className="card p-5">
              <h3 className="h3 text-[14px]">{w.title}</h3>
              <p className="body mt-2 text-[14px]">{w.detail}</p>
            </div>
          ))}
        </div>
      </Section>

      {/* ── Product lines ──────────────────────────────────────────── */}
      <Section title="Product lines" className="pt-0">
        <p className="body mb-5 max-w-prose">
          These are three distinct programmes with different customers, different maturity and
          different IP positions. Assessing them as one company-level technical claim would hide
          the most important tension in the case: the marketed product has the weakest evidence,
          and the best-evidenced product has one customer.
        </p>
        <div className="space-y-3">
          {a.productLines.map((p: any) => (
            <div key={p.id} className="card p-5 sm:p-6">
              <h3 className="h2 text-[19px]">{p.name}</h3>
              <p className="body mt-2 max-w-prose">{p.what}</p>
              <dl className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {[
                  ['Technical maturity', p.technical_maturity],
                  ['Key limitation', p.key_limitation],
                  ['Commercial validation', p.commercial_validation],
                  ['Funding', p.funding],
                  ['IP', p.ip],
                  ['Open question', p.open_question],
                ].map(([k, v]) => (
                  <div key={k as string}>
                    <dt className="text-[11px] font-semibold uppercase tracking-wide text-ink/45">{k}</dt>
                    <dd className="body mt-1 text-[13.5px]">{v as string}</dd>
                  </div>
                ))}
              </dl>
            </div>
          ))}
        </div>
      </Section>

      {/* ── Debates ────────────────────────────────────────────────── */}
      <Section title="The investment debates" className="pt-0">
        <p className="body mb-5 max-w-prose">
          Four debates determine the answer. Generic headings were discarded in favour of the
          questions the evidence actually produces.
        </p>
        <div className="space-y-4">
          {a.debates.map((d: any, i: number) => (
            <article key={d.id} className="card p-5 sm:p-7">
              <div className="flex items-baseline gap-3">
                <span className="mono text-sea">{String(i + 1).padStart(2, '0')}</span>
                <div>
                  <h3 className="h2 text-[19px]">{d.title}</h3>
                  {d.subtitle && <p className="meta mt-1">{d.subtitle}</p>}
                </div>
              </div>

              <div className="mt-5 rounded-md border-l-[3px] border-l-ink/25 bg-paper px-4 py-3">
                <p className="text-[12px] font-semibold uppercase tracking-wider text-ink/50">Current view</p>
                <p className="body mt-1 text-[14px]">{d.current_view}</p>
              </div>

              <div className="mt-4 grid gap-3 lg:grid-cols-2">
                <div className="rounded-md border-l-[3px] border-l-moss bg-moss-pale/40 px-4 py-3">
                  <p className="text-[12px] font-semibold uppercase tracking-wider text-moss">Bull evidence</p>
                  <ul className="mt-2 space-y-1.5">
                    {d.bull.map((b: string, j: number) => <li key={j} className="body text-[13.5px]">{b}</li>)}
                  </ul>
                </div>
                <div className="rounded-md border-l-[3px] border-l-rust bg-rust-pale/40 px-4 py-3">
                  <p className="text-[12px] font-semibold uppercase tracking-wider text-rust">Bear evidence</p>
                  <ul className="mt-2 space-y-1.5">
                    {d.bear.map((b: string, j: number) => <li key={j} className="body text-[13.5px]">{b}</li>)}
                  </ul>
                </div>
              </div>

              <div className="mt-4 rounded-md border-l-[3px] border-l-sea bg-sea-pale/40 px-4 py-3">
                <p className="text-[12px] font-semibold uppercase tracking-wider text-sea-deep">Unknown</p>
                <p className="body mt-1 text-[14px]">{d.unknown}</p>
              </div>

              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <div>
                  <p className="text-[11px] font-semibold uppercase tracking-wide text-ink/45">Would increase conviction</p>
                  <p className="body mt-1 text-[13.5px]">{d.upgrade}</p>
                </div>
                <div>
                  <p className="text-[11px] font-semibold uppercase tracking-wide text-ink/45">Would reduce conviction</p>
                  <p className="body mt-1 text-[13.5px]">{d.downgrade}</p>
                </div>
              </div>
            </article>
          ))}
        </div>
      </Section>

      {/* ── IP ─────────────────────────────────────────────────────── */}
      <Section title="Intellectual property" className="pt-0">
        <Callout tone="moss" title="A correction the research produced">
          {a.ip.correction_note}
        </Callout>
        <div className="mt-5 grid gap-3 lg:grid-cols-2">
          <div className="card p-5">
            <h3 className="h3 mb-1 text-[14px] text-moss">Publicly supported</h3>
            <p className="meta mb-3">Established by public patent and licensing records.</p>
            <ul className="space-y-2">
              {a.ip.publicly_supported.map((x: string, i: number) => (
                <li key={i} className="body text-[13.5px]">{x}</li>
              ))}
            </ul>
          </div>
          <div className="card p-5">
            <h3 className="h3 mb-1 text-[14px] text-rust">Still requires diligence</h3>
            <p className="meta mb-3">Not visible from outside; cheap to resolve from inside.</p>
            <ul className="space-y-2">
              {a.ip.still_requires_diligence.map((x: string, i: number) => (
                <li key={i} className="body text-[13.5px]">{x}</li>
              ))}
            </ul>
          </div>
        </div>
        <p className="meta mt-4 max-w-prose">{a.ip.disclaimer}</p>
      </Section>

      {/* ── Government validation ──────────────────────────────────── */}
      <Section title="Government-funded development" className="pt-0">
        <Callout tone="rust" title="This is funded technical demand, not commercial revenue">
          {gov.note}
        </Callout>

        <div className="mt-6 grid gap-4 lg:grid-cols-5">
          <div className="lg:col-span-3">
            <h3 className="h3 mb-3 text-[14px]">Verified federal awards</h3>
            <div className="card overflow-x-auto">
              <table className="w-full text-[13px]">
                <thead>
                  <tr className="border-b border-paper-line text-left text-[11px] uppercase tracking-wide text-ink/50">
                    <th className="px-4 py-2.5 font-medium">Start</th>
                    <th className="px-4 py-2.5 font-medium">Agency</th>
                    <th className="px-4 py-2.5 font-medium">Instrument</th>
                    <th className="px-4 py-2.5 text-right font-medium">Amount</th>
                    <th className="px-4 py-2.5 font-medium">Ends</th>
                  </tr>
                </thead>
                <tbody>
                  {gov.awards.map((w: any) => (
                    <tr key={w.id} className="border-b border-paper-line/60">
                      <td className="px-4 py-2 font-mono tabular-nums text-ink/60">{w.date}</td>
                      <td className="px-4 py-2">{w.agency}</td>
                      <td className="px-4 py-2 text-ink/70">{w.instrument}</td>
                      <td className="px-4 py-2 text-right font-mono tabular-nums">{fmtMoney(w.amount)}</td>
                      <td className="px-4 py-2 font-mono tabular-nums text-ink/50">{w.end}</td>
                    </tr>
                  ))}
                  <tr className="font-semibold">
                    <td className="px-4 py-2.5" colSpan={3}>Total verified federal awards</td>
                    <td className="px-4 py-2.5 text-right font-mono tabular-nums text-sea-deep">{fmtMoney(gov.total)}</td>
                    <td />
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div className="lg:col-span-2">
            <h3 className="h3 mb-3 text-[14px]">Navy Phase II, reconciled</h3>
            <div className="card p-5">
              <p className="meta mb-3">Contract {gov.navyContractId}, from its transaction history.</p>
              <ul className="space-y-2.5">
                {gov.navyModifications.map((m: any) => (
                  <li key={m.mod} className="flex items-baseline justify-between gap-3 border-b border-paper-line/60 pb-2 last:border-0">
                    <div>
                      <div className="text-[13px] font-medium">{m.action}</div>
                      <div className="meta">{m.date} · {m.mod}</div>
                    </div>
                    <span className="mono whitespace-nowrap">{m.amount ? `+${fmtMoney(m.amount)}` : '—'}</span>
                  </li>
                ))}
                <li className="flex items-baseline justify-between gap-3 pt-1 font-semibold">
                  <span className="text-[13px]">Total obligated</span>
                  <span className="mono text-sea-deep">{fmtMoney(1998926)}</span>
                </li>
              </ul>
              <p className="meta mt-3">
                Period of performance {gov.navyPeriod.start} → {gov.navyPeriod.end}.
              </p>
            </div>
          </div>
        </div>
      </Section>

      {/* ── Procurement ────────────────────────────────────────────── */}
      <Section title="Bottom-up procurement evidence" className="pt-0">
        <p className="body max-w-prose">
          Built from {proc.contracts} federal contracts already in the project database, each
          classified by a stated rule. This is an <strong>observed contract-value sample</strong>,
          not a market size estimate.
        </p>

        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <Stat value={fmtNum(proc.contracts)} label="Contracts audited" />
          <Stat value={fmtMoney(proc.totalObserved)} label={`Observed value, ${proc.yearSpan.first}–${proc.yearSpan.last}`} />
          <Stat value={fmtMoney(proc.narrow.annualised)} label="Narrow addressable, annualised"
                hint="Components/spares plus payload deployment — what a subsystem vendor could win directly" />
          <Stat value={fmtMoney(proc.broad.annualised)} label="Broad adjacency, annualised"
                hint="Reachable only through OEMs or by expanding scope" />
        </div>

        <div className="mt-6 grid gap-5 lg:grid-cols-2">
          <div>
            <h3 className="h3 mb-3 text-[14px]">Where the money actually sits</h3>
            <ProcurementBuckets buckets={proc.buckets} />
          </div>
          <div className="space-y-3">
            <Callout tone="rust" title="The investment implication">
              {proc.implication}
            </Callout>
            <div className="card p-5">
              <h4 className="h3 mb-2 text-[14px]">False comparables removed</h4>
              <p className="body text-[13.5px]">
                {proc.excluded.n} contracts totalling {fmtMoney(proc.excluded.value)} were removed
                transparently: a design-build contract for a <em>building</em>, and a counter-UUV
                services contract. Both matched the keyword; neither is addressable by anyone
                selling UUV subsystems.
              </p>
            </div>
            <div className="card p-5">
              <h4 className="h3 mb-2 text-[14px]">Limits of this analysis</h4>
              <p className="body text-[13.5px]">{proc.caveat}</p>
              <p className="body mt-2 text-[13.5px]">
                The fair rebuttal: payload-deployment spending is small partly because the
                capability does not exist yet. A market cannot be observed before the product.
              </p>
            </div>
          </div>
        </div>
      </Section>

      {/* ── Model ──────────────────────────────────────────────────── */}
      <Section title="Underwriting scenarios" className="pt-0">
        <p className="body max-w-prose">{model.note}</p>
        <p className="body mt-3 max-w-prose">
          At base the model reaches <strong>{fmtMoney(model.base.total_revenue)}</strong> against a{' '}
          <strong>{fmtMoney(model.base.threshold)}</strong> reference threshold — a shortfall of{' '}
          <strong>{fmtMoney(model.base.gap)}</strong>. That threshold is roughly{' '}
          <strong>{model.thresholdMultipleOfNarrow}×</strong> the narrow addressable procurement
          observed in the sample and <strong>{model.thresholdMultipleOfBroad}×</strong> the broad
          adjacency figure.
        </p>
        <div className="mt-6"><ScenarioModel assumptions={model.assumptions} /></div>
      </Section>

      {/* ── Primary research ───────────────────────────────────────── */}
      <Section title="What I would do next" className="pt-0">
        <p className="body max-w-prose">
          No one was contacted and no conversations occurred. This is the call plan that would run
          before an investment decision.
        </p>
        <div className="mt-6 grid gap-5 lg:grid-cols-2">
          <div>
            <h3 className="h3 mb-3 text-[14px]">Top five unanswered questions</h3>
            <ol className="space-y-2">
              {a.primaryResearch.questions.map((q: string, i: number) => (
                <li key={i} className="card flex gap-3 p-4">
                  <span className="mono text-sea">{i + 1}</span>
                  <span className="body text-[13.5px]">{q}</span>
                </li>
              ))}
            </ol>
          </div>
          <div>
            <h3 className="h3 mb-3 text-[14px]">First calls</h3>
            <ol className="space-y-2">
              {a.primaryResearch.first_calls.map((c: any, i: number) => (
                <li key={i} className="card p-4">
                  <div className="text-[14px] font-semibold">{i + 1}. {c.who}</div>
                  <p className="body mt-1.5 text-[13.5px]">{c.why}</p>
                </li>
              ))}
            </ol>
            <div className="mt-3 rounded-md border-l-[3px] border-l-sea bg-sea-pale/40 px-4 py-3">
              <p className="body text-[13.5px]">{a.primaryResearch.sequencing_rationale}</p>
            </div>
          </div>
        </div>
      </Section>

      {/* ── Research journey ───────────────────────────────────────── */}
      <Section title="How the view changed" className="pt-0">
        <div className="grid gap-4 lg:grid-cols-2">
          {a.researchJourney.stories.map((s: any) => (
            <div key={s.id} className="card p-5">
              <div className="flex items-center gap-2">
                <Chip tone={s.direction === 'strengthened_company' ? 'moss' : 'rust'}>
                  {s.direction === 'strengthened_company' ? 'View improved' : 'View weakened'}
                </Chip>
                <h3 className="h3 text-[15px]">{s.title}</h3>
              </div>
              <ol className="mt-4 space-y-2">
                {s.steps.map((step: string, i: number) => (
                  <li key={i} className="flex gap-3">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-sea/50" aria-hidden />
                    <span className="body text-[13.5px]">{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          ))}
        </div>
        <Callout tone="sea" title="The takeaway">{a.researchJourney.takeaway}</Callout>
      </Section>

      {/* ── Propeller fit ──────────────────────────────────────────── */}
      <Section title="Propeller fit" className="pt-0">
        <p className="body mb-5 max-w-prose">
          Assessed only against publicly stated criteria — themes, stage and check size taken from
          the firm’s own website.
        </p>
        <div className="card overflow-x-auto">
          <table className="w-full text-[13.5px]">
            <tbody>
              {a.propellerFit.criteria.map((c: any) => (
                <tr key={c.criterion} className="border-b border-paper-line/60 last:border-0 align-top">
                  <td className="w-48 px-4 py-3 font-medium">{c.criterion}</td>
                  <td className="px-4 py-3 text-ink/75">{c.assessment}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Callout tone="rust" title="On sourcing, stated plainly">
          {a.propellerFit.sourcing_caveat}
        </Callout>
      </Section>

      {/* ── Evidence register ──────────────────────────────────────── */}
      <Section title={`Evidence register (${evidenceRegister.length} claims)`} className="pt-0">
        <p className="body mb-4 max-w-prose">
          Every material claim in this case, with its status, source and source tier. Government and
          patent records outrank company sources, which outrank secondary reporting. Aggregator
          databases were deliberately excluded from all material financial facts.
        </p>
        <details className="card p-5">
          <summary className="cursor-pointer text-[14px] font-medium">Open the full register</summary>
          <ul className="mt-4 space-y-3">
            {evidenceRegister.map((r) => (
              <li key={r.id} className="border-b border-paper-line/60 pb-3 last:border-0">
                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="mono text-ink/40">{r.id}</span>
                  <span className={`chip ${r.status === 'observed' ? 'chip-moss' : r.status === 'inferred' ? 'chip-sea' : 'chip-rust'}`}>
                    {r.status}
                  </span>
                  <span className="chip chip-neutral">{r.tier}</span>
                </div>
                <p className="body mt-1.5 text-[13.5px]">{r.claim}</p>
                <p className="meta mt-1 break-all">
                  {r.source.startsWith('http')
                    ? <a href={r.source} target="_blank" rel="noopener noreferrer" className="link">{r.source}</a>
                    : r.source}
                  {' · accessed '}{r.accessed}
                </p>
                {r.contradictory && (
                  <p className="meta mt-1 text-rust">Contradictory / superseding: {r.contradictory}</p>
                )}
              </li>
            ))}
          </ul>
        </details>
        <p className="meta mt-6">
          <Link href="/methodology/" className="link">How sources are tiered and validated →</Link>
        </p>
      </Section>
    </>
  );
}
