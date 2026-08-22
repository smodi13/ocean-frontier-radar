import Link from 'next/link';
import { Bar, Callout, Chip, PageHeader, Section, Stat } from '@/components/Primitives';
import { CATEGORY_LABEL, SIGNAL_LABEL, frontier, fmtNum, summary } from '@/lib/data';

export const metadata = { title: 'Frontier · Ocean Frontier Radar' };

const DIM_LABEL: Record<string, string> = {
  translation_intent: 'Translation intent',
  technical_depth: 'Technical depth',
  ocean_relevance: 'Ocean relevance',
  recency: 'Recency',
};

export default function FrontierPage() {
  const signals = [...frontier.signals].sort(
    (a, b) => (b.signalDate ?? '').localeCompare(a.signalDate ?? ''),
  );
  const institutions = Object.keys(frontier.byInstitution).length;

  return (
    <>
      <PageHeader
        eyebrow="Pre-company sourcing"
        title="Frontier"
        lede={
          <>
            Research and commercialization signals that appear <em>before</em> obvious company
            formation: I-Corps customer-discovery awards, technology-translation grants and
            university commercialization programs.
          </>
        }
      />

      <Section>
        <Callout tone="sea" title="Frontier is a research-priority queue, not an investment ranking">
          These signals are scored on their own framework and are never compared numerically against
          funded companies, because they structurally cannot show customers, revenue or financing.
          A high research priority means <strong>worth an analyst’s time</strong>. It does not mean
          investable today — most of these have no company at all.
        </Callout>

        <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <Stat value={fmtNum(signals.length)} label="Frontier signals" />
          <Stat value={fmtNum(institutions)} label="Distinct institutions" hint="No institution dominates" />
          <Stat value={fmtNum(frontier.byType.icorps ?? 0)} label="NSF I-Corps (customer discovery)" />
          <Stat value={`${Math.round(summary.preCompanyShareOfActionable * 100)}%`}
                label="Pre-company share of actionable universe" hint="Up from 6% before this queue existed" />
        </div>
      </Section>

      <Section title="The research-to-company path" className="pt-0">
        <p className="body max-w-prose">
          Signals are placed on the transition below by the evidence actually present. A stage is
          only shown as reached where a public record supports it — nothing is implied.
        </p>
        <ol className="mt-5 flex flex-wrap items-center gap-2">
          {['Research', 'Grant', 'Prototype', 'Commercialization program', 'Company formation'].map((s, i, arr) => (
            <li key={s} className="flex items-center gap-2">
              <span className={`chip ${i <= 3 ? 'chip-sea' : 'chip-neutral'}`}>{s}</span>
              {i < arr.length - 1 && <span aria-hidden className="text-ink/30">→</span>}
            </li>
          ))}
        </ol>
        <p className="meta mt-3 max-w-prose">
          Every signal in this queue sits at or before “commercialization program”. None has a
          formed company; that is what makes it the frontier.
        </p>
      </Section>

      <Section title={`Signals (${signals.length})`} className="pt-0">
        <p className="meta mb-4">Ordered by most recent signal date, not by priority.</p>
        <ul className="space-y-3">
          {signals.map((s) => (
            <li key={s.id} className="card p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="min-w-0">
                  <h3 className="text-[15px] font-semibold leading-snug">{s.name}</h3>
                  <p className="meta mt-1">{[s.institution, s.geography].filter(Boolean).join(' · ')}</p>
                </div>
                <div className="flex flex-wrap items-center gap-1.5">
                  {s.signalType && <Chip tone="sea">{SIGNAL_LABEL[s.signalType] ?? s.signalType}</Chip>}
                  {s.category && <Chip>{CATEGORY_LABEL[s.category] ?? s.category}</Chip>}
                  {s.signalDate && <Chip>{s.signalDate}</Chip>}
                </div>
              </div>

              <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {Object.entries(s.components).map(([dim, v]) => (
                  <div key={dim}>
                    <div className="flex items-baseline justify-between gap-2">
                      <span className="text-[12px] font-medium text-ink/70">{DIM_LABEL[dim] ?? dim}</span>
                      <span className="mono text-ink/50">{v.points}/{v.max}</span>
                    </div>
                    <div className="mt-1"><Bar value={v.points} max={v.max} /></div>
                    <p className="mt-1.5 text-[11px] leading-snug text-ink/50">{v.why}</p>
                  </div>
                ))}
              </div>

              <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-paper-line pt-3">
                <span className="meta">
                  Research priority <span className="mono text-sea">{s.priority}/{s.priorityMax}</span>
                  {' '}· {s.evidence.length} evidence record{s.evidence.length === 1 ? '' : 's'}
                </span>
                <Link href={`/radar/${s.id}/`} className="link text-[13px]">Open detail →</Link>
              </div>
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Known limitations of this queue" className="pt-0">
        <ul className="body max-w-prose list-disc space-y-2 pl-5">
          <li>It is NSF-only. I-Corps and PFI are NSF programs; equivalent translation signals from DOE, NOAA and DoD are not captured, and no non-US signals are captured at all.</li>
          <li>Roughly five of the signals are marginal — adjacent at best. They sit in a watch queue where a false positive is cheap, but this is not 31 uniformly strong signals.</li>
          <li>Award size is a crude proxy for technical depth, which flatters program scale over research quality.</li>
          <li>There is no person-level tracking. The highest-value pre-company signal would be a researcher’s role changing from academic to founder, which the system cannot yet see.</li>
        </ul>
      </Section>
    </>
  );
}
