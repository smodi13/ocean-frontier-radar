'use client';

import Link from 'next/link';
import type { FrontierSignal } from '@/lib/types';
import { CATEGORY_LABEL, SIGNAL_LABEL } from '@/lib/labels';
import { useInView, usePrefersReducedMotion } from '@/lib/motion';

const DIM_LABEL: Record<string, string> = {
  translation_intent: 'Translation intent',
  technical_depth: 'Technical depth',
  ocean_relevance: 'Ocean relevance',
  recency: 'Recency',
};

export default function FrontierCard({ signal }: { signal: FrontierSignal }) {
  const reduced = usePrefersReducedMotion();
  const [ref, inView] = useInView<HTMLLIElement>();
  const show = reduced || inView;

  return (
    <li ref={ref} className="card p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="text-[15px] font-semibold leading-snug">{signal.name}</h3>
          <p className="meta mt-1">
            {[signal.institution, signal.geography].filter(Boolean).join(' · ')}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-1.5">
          {signal.signalType && (
            <span className="chip chip-sea">
              {SIGNAL_LABEL[signal.signalType] ?? signal.signalType}
            </span>
          )}
          {signal.category && (
            <span className="chip chip-neutral">
              {CATEGORY_LABEL[signal.category] ?? signal.category}
            </span>
          )}
          {signal.signalDate && <span className="chip chip-neutral">{signal.signalDate}</span>}
        </div>
      </div>

      {/*
        Component bars draw from zero when the card enters view. The width is the
        real score; only the arrival is animated.
      */}
      <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {Object.entries(signal.components).map(([dim, v], i) => (
          <div key={dim}>
            <div className="flex items-baseline justify-between gap-2">
              <span className="text-[12px] font-medium text-ink/70">{DIM_LABEL[dim] ?? dim}</span>
              <span className="mono text-ink/50">
                {v.points}/{v.max}
              </span>
            </div>
            <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-paper-line">
              <div
                className="bar-fill h-full rounded-full bg-sea"
                style={{
                  width: show ? `${(v.points / v.max) * 100}%` : '0%',
                  transitionDelay: reduced ? '0ms' : `${120 + i * 90}ms`,
                }}
              />
            </div>
            <p className="mt-1.5 text-[11px] leading-snug text-ink/50">{v.why}</p>
          </div>
        ))}
      </div>

      <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-paper-line pt-3">
        <span className="meta">
          Research priority{' '}
          <span className="mono text-sea">
            {signal.priority}/{signal.priorityMax}
          </span>{' '}
          · {signal.evidence.length} evidence record{signal.evidence.length === 1 ? '' : 's'}
        </span>
        <Link href={`/radar/${signal.id}/`} className="group text-[13px] font-medium text-sea">
          Open detail <span className="arrow" aria-hidden>→</span>
        </Link>
      </div>
    </li>
  );
}
