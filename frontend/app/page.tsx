import Link from 'next/link';
import HeroNetwork from '@/components/HeroNetwork';
import MetricGrid, { type Metric } from '@/components/MetricGrid';
import ResearchFunnel, { type FunnelStage } from '@/components/ResearchFunnel';
import { Reveal, RevealStagger } from '@/components/motion/Reveal';
import { Callout, Section } from '@/components/Primitives';
import { armada, fmtNum, summary, themes } from '@/lib/data';

export default function Home() {
  const s = summary;
  const pct = Math.round(s.preCompanyShareOfActionable * 100);

  // Every figure below comes from the canonical export; nothing is typed here.
  const metrics: Metric[] = [
    { value: s.recordsEvaluated, kind: 'count', label: 'Source records evaluated',
      hint: 'Federal award and procurement records scanned across all ingestion runs' },
    { value: s.candidates, kind: 'count', label: 'Candidates retrieved',
      hint: 'Records that passed retrieval and classification' },
    { value: s.actionableUniverse, kind: 'count', label: 'In active research queues',
      hint: 'Tier A + Tier B + Frontier. Records warranting analyst time — not investment recommendations.' },
    { value: s.institutions, kind: 'count', label: 'Institutions represented' },
    { value: s.tierA, kind: 'count', label: 'Tier A — diligence now' },
    { value: s.tierB, kind: 'count', label: 'Tier B — research queue' },
    { value: s.frontier, kind: 'count', label: 'Frontier — pre-company signals' },
    { value: pct, kind: 'percent', label: 'Pre-company share of actionable universe',
      hint: "The system's core purpose: seeing opportunities before company formation" },
    { value: s.themes, kind: 'count', label: 'Taxonomy categories' },
    { value: s.procurementContracts, kind: 'count', label: 'Procurement contracts audited',
      hint: 'Used for bottom-up demand evidence, not market sizing' },
    { value: s.procurementObserved, kind: 'money', label: 'Observed federal contract value',
      hint: 'Keyword-derived sample across 13 years. Not a market size estimate.' },
    { value: armada.evidenceCount, kind: 'count', label: 'Traceable claims in the diligence case' },
  ];

  const funnel: FunnelStage[] = [
    { value: s.recordsEvaluated, label: 'Public records evaluated',
      note: 'Federal awards, procurement, translation programmes' },
    { value: s.candidates, label: 'Candidates surfaced',
      note: 'Passed problem-first retrieval and classification' },
    { value: s.actionableUniverse, label: 'In active research queues',
      note: 'Tier A + Tier B + Frontier' },
    { value: s.tierA, label: 'Tier A', note: 'Enough evidence and current activity to justify work now',
      emphasis: 'strong', href: '/radar/' },
    { value: s.frontier, label: 'Frontier signals', note: 'Pre-company research, scored on its own framework',
      emphasis: 'strong', href: '/frontier/' },
    { value: null, display: 'ARMADA', label: 'Deep diligence case',
      note: 'One candidate carried to a stated recommendation',
      emphasis: 'terminal', href: '/deep-dive/' },
  ];

  return (
    <div className="ofr-page">
      {/* ── Hero ─────────────────────────────────────────────── */}
      <div className="relative overflow-hidden border-b border-paper-line bg-white">
        <HeroNetwork />
        <div className="wrap relative py-20 sm:py-28">
          <p className="eyebrow ofr-enter ofr-d1 mb-4">
            Research-to-venture sourcing · Independent project
          </p>
          <h1 className="h1 ofr-enter ofr-d2 max-w-4xl">Ocean Frontier Radar</h1>
          <p className="lede ofr-enter ofr-d3 mt-6 max-w-prose">
            A research-to-venture sourcing system for finding emerging technologies at the
            ocean&rsquo;s edge and turning public signals into an actionable diligence queue.
          </p>
          <p className="body ofr-enter ofr-d4 mt-5 max-w-prose">
            The system is built to surface research projects, commercialization programs, grants,
            spinouts and very early companies — rather than aggregate startups that are already
            venture-backed and already visible. Every figure below is generated from the
            project&rsquo;s committed research outputs.
          </p>
          <div className="ofr-enter ofr-d5 mt-8 flex flex-wrap gap-3">
            <Link
              href="/radar/"
              className="card-interactive rounded bg-sea px-4 py-2 text-[14px] font-medium text-white hover:bg-sea-deep"
            >
              Explore the Radar <span className="arrow" aria-hidden>→</span>
            </Link>
            <Link
              href="/deep-dive/"
              className="card-interactive rounded border border-paper-line bg-paper-card px-4 py-2 text-[14px] font-medium"
            >
              View ARMADA deep dive <span className="arrow" aria-hidden>→</span>
            </Link>
          </div>
          <dl className="ofr-enter ofr-d6 mt-10 flex flex-wrap gap-x-10 gap-y-3">
            {[
              [fmtNum(s.recordsEvaluated), 'records evaluated'],
              [fmtNum(s.candidates), 'candidates surfaced'],
              [fmtNum(s.frontier), 'pre-company signals'],
              [fmtNum(s.institutions), 'institutions'],
            ].map(([v, l]) => (
              <div key={l}>
                <dt className="font-mono text-lg font-semibold tabular-nums text-sea-deep">{v}</dt>
                <dd className="meta">{l}</dd>
              </div>
            ))}
          </dl>
        </div>
      </div>

      {/* ── Funnel ───────────────────────────────────────────── */}
      <Section kicker="How the universe narrows" title="From public record to diligence queue">
        <Reveal>
          <p className="body mb-8 max-w-prose">
            Software narrows the universe, evidence structures the work, and analyst judgment
            decides what earns diligence. Each step below is a real count from the pipeline.
          </p>
        </Reveal>
        <ResearchFunnel stages={funnel} />
      </Section>

      {/* ── Metrics ──────────────────────────────────────────── */}
      <Section kicker="What the system has processed" title="The sourcing universe" className="pt-0">
        <MetricGrid metrics={metrics} />
        <Reveal>
          <p className="meta mt-4">
            Generated from canonical research outputs on {s.generatedAt.slice(0, 10)}. Counts are
            not typed into this page; they are exported from the project&rsquo;s database and audit
            scripts.
          </p>
        </Reveal>
      </Section>

      {/* ── Workflow ─────────────────────────────────────────── */}
      <Section kicker="How it works" title="From public signal to investment view" className="pt-0">
        <RevealStagger step={60} className="grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {[
            ['Public research signals', 'Federal grants, SBIR/STTR awards, I-Corps, patents, university licensing.'],
            ['Sourcing', 'Retrieval by technical problem, not by the word “ocean”.'],
            ['Evidence', 'Every claim keeps its source, date and access date.'],
            ['Prioritization', 'Triage into queues. Research priority, never an investment score.'],
            ['Diligence', 'Technical, commercial, IP and procurement analysis on one candidate.'],
            ['Investment view', 'An outside-in recommendation with stated reversal conditions.'],
          ].map(([t, d], i) => (
            <div key={t} className="card h-full p-4">
              <div className="mono text-sea">{String(i + 1).padStart(2, '0')}</div>
              <div className="mt-1.5 text-[14px] font-semibold">{t}</div>
              <p className="meta mt-1.5">{d}</p>
            </div>
          ))}
        </RevealStagger>
      </Section>

      <Section className="pt-0">
        <Reveal>
          <Callout tone="sea" title="Why retrieval is organised by problem rather than by sector">
            The strongest candidates often never use ocean vocabulary. One example the system
            surfaces: a landlocked university holding a multi-million-dollar award on biocide-free
            anticorrosion coatings — a problem that is most acute on marine assets, in a state with
            no coastline. A keyword search for “ocean startup” cannot find it.{' '}
            <Link href="/methodology/" className="link">How the lexicon works</Link>.
          </Callout>
        </Reveal>
      </Section>

      {/* ── Themes ───────────────────────────────────────────── */}
      <Section kicker="Where activity clusters" title="Themes">
        <RevealStagger step={50} className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {themes.slice(0, 8).map((t) => (
            <Link key={t.id} href={`/themes/#${t.id}`} className="card-interactive block h-full rounded-lg border border-paper-line bg-paper-card p-4">
              <div className="text-[14px] font-semibold leading-snug">{t.label}</div>
              <div className="mono mt-2 text-sea">{t.candidateCount}</div>
              <div className="meta">candidates · {t.frontierCount} pre-company</div>
            </Link>
          ))}
        </RevealStagger>
      </Section>

      {/* ── ARMADA ───────────────────────────────────────────── */}
      <Section kicker="Diligence" title="ARMADA Marine Robotics" className="pt-0">
        <Reveal>
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
            <Link href="/deep-dive/" className="card-interactive mt-5 inline-block text-[14px] text-sea">
              Read the full case <span className="arrow" aria-hidden>→</span>
            </Link>
          </div>
        </Reveal>
      </Section>
    </div>
  );
}
