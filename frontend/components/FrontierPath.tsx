'use client';

import { useInView, usePrefersReducedMotion } from '@/lib/motion';

const STAGES = [
  'Research',
  'Grant',
  'Prototype',
  'Commercialization program',
  'Company formation',
] as const;

/**
 * The whole queue sits at or before "commercialization program", so the marker
 * is drawn once for the queue rather than per signal — every signal here is an
 * I-Corps award or a translation grant, and a per-card path would imply a
 * differentiation the evidence does not contain.
 */
const REACHED = 4; // stages 1-4 evidenced; company formation is not

export default function FrontierPath({ count }: { count: number }) {
  const reduced = usePrefersReducedMotion();
  const [ref, inView] = useInView<HTMLDivElement>();
  const show = reduced || inView;
  const pct = ((REACHED - 1) / (STAGES.length - 1)) * 100;

  return (
    <div ref={ref} className="mt-6">
      <div className="relative h-[3px] w-full rounded-full bg-paper-line">
        <div
          className="absolute inset-y-0 left-0 rounded-full bg-sea"
          style={{
            width: show ? `${pct}%` : '0%',
            transition: reduced
              ? 'none'
              : 'width 1100ms cubic-bezier(.22,.61,.36,1) 120ms',
          }}
        />
        {STAGES.map((label, i) => {
          const on = i < REACHED;
          return (
            <span
              key={label}
              className={`absolute top-1/2 h-2.5 w-2.5 -translate-y-1/2 rounded-full ring-4 ring-paper ${
                on ? 'bg-sea' : 'border border-dashed border-ink/30 bg-paper'
              }`}
              style={{
                left: `calc(${(i / (STAGES.length - 1)) * 100}% - 5px)`,
                opacity: show ? 1 : 0,
                transition: reduced
                  ? 'none'
                  : `opacity 320ms ease ${140 + i * 210}ms`,
              }}
            />
          );
        })}
      </div>

      <div className="mt-3 grid grid-cols-5 gap-2">
        {STAGES.map((label, i) => (
          <span
            key={label}
            className={`text-[11px] leading-tight ${
              i < REACHED ? 'font-medium text-sea-deep' : 'text-ink/40'
            } ${i === 0 ? 'text-left' : i === STAGES.length - 1 ? 'text-right' : 'text-center'}`}
            style={{
              opacity: show ? 1 : 0,
              transform: show || reduced ? 'none' : 'translateY(4px)',
              transition: reduced ? 'none' : `opacity 320ms ease ${180 + i * 210}ms, transform 320ms ease ${180 + i * 210}ms`,
            }}
          >
            {label}
          </span>
        ))}
      </div>

      <p className="meta mt-4 max-w-prose">
        All {count} signals in this queue sit at or before “commercialization program”. None has a
        formed company; that is what makes it the frontier.
      </p>
    </div>
  );
}
