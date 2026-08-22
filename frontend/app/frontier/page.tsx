import { Callout, PageHeader, Section, Stat } from '@/components/Primitives';
import FrontierCard from '@/components/FrontierCard';
import FrontierPath from '@/components/FrontierPath';
import { Reveal, RevealStagger } from '@/components/motion/Reveal';
import { Counter } from '@/components/motion/Counter';
import { frontier, summary } from '@/lib/data';

export const metadata = { title: 'Frontier · Ocean Frontier Radar' };

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

        <RevealStagger className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4" step={70}>
          <Stat value={<Counter value={signals.length} format="num" />} label="Frontier signals" />
          <Stat value={<Counter value={institutions} format="num" />} label="Distinct institutions" hint="No institution dominates" />
          <Stat value={<Counter value={frontier.byType.icorps ?? 0} format="num" />} label="NSF I-Corps (customer discovery)" />
          <Stat
            value={<Counter value={Math.round(summary.preCompanyShareOfActionable * 100)} format="percent" />}
            label="Pre-company share of actionable universe" hint="Up from 6% before this queue existed" />
        </RevealStagger>
      </Section>

      <Section title="The research-to-company path" className="pt-0">
        <p className="body max-w-prose">
          Signals are placed on the transition below by the evidence actually present. A stage is
          only shown as reached where a public record supports it — nothing is implied.
        </p>
        <FrontierPath count={signals.length} />
      </Section>

      <Section title={`Signals (${signals.length})`} className="pt-0">
        <p className="meta mb-4">Ordered by most recent signal date, not by priority.</p>
        <ul className="space-y-3">
          {signals.map((s) => (
            <FrontierCard key={s.id} signal={s} />
          ))}
        </ul>
      </Section>

      <Section title="Known limitations of this queue" className="pt-0">
        <Reveal>
        <ul className="body max-w-prose list-disc space-y-2 pl-5">
          <li>It is NSF-only. I-Corps and PFI are NSF programs; equivalent translation signals from DOE, NOAA and DoD are not captured, and no non-US signals are captured at all.</li>
          <li>Roughly five of the signals are marginal — adjacent at best. They sit in a watch queue where a false positive is cheap, but this is not 31 uniformly strong signals.</li>
          <li>Award size is a crude proxy for technical depth, which flatters program scale over research quality.</li>
          <li>There is no person-level tracking. The highest-value pre-company signal would be a researcher’s role changing from academic to founder, which the system cannot yet see.</li>
        </ul>
        </Reveal>
      </Section>
    </>
  );
}
