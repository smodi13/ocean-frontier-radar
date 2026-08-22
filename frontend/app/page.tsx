import Link from 'next/link';
import { Callout, Section, Stat } from '@/components/Primitives';
import { armada, fmtMoney, fmtNum, summary, themes } from '@/lib/data';

export default function Home() {
  const s = summary;
  const pct = Math.round(s.preCompanyShareOfActionable * 100);

  return (
    <>
      <div className="border-b border-paper-line bg-white">
        <div className="wrap py-16 sm:py-24">
          <p className="eyebrow mb-4">Research-to-venture sourcing · Independent project</p>
          <h1 className="h1 max-w-4xl">Ocean Frontier Radar</h1>
          <p className="lede mt-6 max-w-prose">
            A research-to-venture sourcing system for finding emerging technologies at the
            ocean’s edge and turning public signals into an actionable diligence queue.
          </p>
          <p className="body mt-5 max-w-prose">
            The system is built to surface research projects, commercialization programs, grants,
            spinouts and very early companies — rather than aggregate startups that are already
            venture-backed and already visible. Every figure below is generated from the
            project’s committed research outputs.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/radar/" className="rounded bg-sea px-4 py-2 text-[14px] font-medium text-white hover:bg-sea-deep">
              Open the radar
            </Link>
            <Link href="/deep-dive/" className="rounded border border-paper-line bg-paper-card px-4 py-2 text-[14px] font-medium hover:border-sea/40">
              Read the ARMADA diligence case
            </Link>
          </div>
        </div>
      </div>

      <Section kicker="What the system has processed" title="The sourcing universe">
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          <Stat value={fmtNum(s.recordsEvaluated)} label="Source records evaluated"
                hint="Federal award and procurement records scanned across all ingestion runs" />
          <Stat value={fmtNum(s.candidates)} label="Candidates retrieved"
                hint="Records that passed retrieval and classification" />
          <Stat value={fmtNum(s.actionableUniverse)} label="Actionable universe"
                hint="Tier A + Tier B + Frontier" />
          <Stat value={fmtNum(s.institutions)} label="Institutions represented" />
          <Stat value={fmtNum(s.tierA)} label="Tier A — diligence now" />
          <Stat value={fmtNum(s.tierB)} label="Tier B — research queue" />
          <Stat value={fmtNum(s.frontier)} label="Frontier — pre-company signals" />
          <Stat value={`${pct}%`} label="Pre-company share of actionable universe"
                hint="The system's core purpose: seeing opportunities before company formation" />
          <Stat value={fmtNum(s.themes)} label="Taxonomy categories" />
          <Stat value={fmtNum(s.procurementContracts)} label="Procurement contracts audited"
                hint="Used for bottom-up demand evidence, not market sizing" />
          <Stat value={fmtMoney(s.procurementObserved)} label="Observed federal contract value"
                hint="Keyword-derived sample across 13 years. Not a market size estimate." />
          <Stat value={fmtNum(armada.evidenceCount)} label="Traceable claims in the diligence case" />
        </div>
        <p className="meta mt-4">
          Generated from canonical research outputs on {s.generatedAt.slice(0, 10)}. Counts are not
          typed into this page; they are exported from the project’s database and audit scripts.
        </p>
      </Section>

      <Section kicker="How it works" title="From public signal to investment view" className="pt-0">
        <ol className="grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {[
            ['Public research signals', 'Federal grants, SBIR/STTR awards, I-Corps, patents, university licensing.'],
            ['Sourcing', 'Retrieval by technical problem, not by the word “ocean”.'],
            ['Evidence', 'Every claim keeps its source, date and access date.'],
            ['Prioritization', 'Triage into queues. Research priority, never an investment score.'],
            ['Diligence', 'Technical, commercial, IP and procurement analysis on one candidate.'],
            ['Investment view', 'An outside-in recommendation with stated reversal conditions.'],
          ].map(([t, d], i) => (
            <li key={t} className="card p-4">
              <div className="mono text-sea">{String(i + 1).padStart(2, '0')}</div>
              <div className="mt-1.5 text-[14px] font-semibold">{t}</div>
              <p className="meta mt-1.5">{d}</p>
            </li>
          ))}
        </ol>
      </Section>

      <Section className="pt-0">
        <Callout tone="sea" title="Why retrieval is organised by problem rather than by sector">
          The strongest candidates often never use ocean vocabulary. One example the system
          surfaces: a landlocked university holding a multi-million-dollar award on biocide-free
          anticorrosion coatings — a problem that is most acute on marine assets, in a state with
          no coastline. A keyword search for “ocean startup” cannot find it.{' '}
          <Link href="/methodology/" className="link">How the lexicon works</Link>.
        </Callout>
      </Section>

      <Section kicker="Where activity clusters" title="Themes">
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {themes.slice(0, 8).map((t) => (
            <Link key={t.id} href={`/themes/#${t.id}`} className="card p-4 hover:border-sea/40">
              <div className="text-[14px] font-semibold leading-snug">{t.label}</div>
              <div className="mono mt-2 text-sea">{t.candidateCount}</div>
              <div className="meta">candidates · {t.frontierCount} pre-company</div>
            </Link>
          ))}
        </div>
      </Section>

      <Section kicker="Diligence" title="ARMADA Marine Robotics" className="pt-0">
        <div className="card p-6 sm:p-8">
          <div className="flex flex-wrap items-center gap-3">
            <span className="rounded border border-rust/30 bg-rust-pale px-2.5 py-1 text-[12px] font-semibold uppercase tracking-wide text-rust">
              {armada.recommendation.verdict}
            </span>
            <span className="meta">Outside-in venture diligence</span>
          </div>
          <p className="body mt-4 max-w-prose">{armada.recommendation.summary}</p>
          <ul className="mt-4 grid gap-2 sm:grid-cols-3">
            {armada.recommendation.unresolved.map((u: { title: string }) => (
              <li key={u.title} className="rounded border border-paper-line bg-paper px-3 py-2 text-[13px]">
                {u.title}
              </li>
            ))}
          </ul>
          <Link href="/deep-dive/" className="link mt-5 inline-block text-[14px]">
            Read the full case →
          </Link>
        </div>
      </Section>
    </>
  );
}
