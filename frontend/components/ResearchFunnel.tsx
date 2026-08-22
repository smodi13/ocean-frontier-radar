'use client';

import Link from 'next/link';
import { Counter } from '@/components/motion/Counter';
import {  } from '@/lib/labels';
import { useInView, usePrefersReducedMotion } from '@/lib/motion';

export interface FunnelStage {
  value: number | null;
  label: string;
  note: string;
  emphasis?: 'default' | 'strong' | 'terminal';
  href?: string;
  display?: string;
}

/**
 * The narrowing sequence. This is the single clearest statement of what the
 * system does: software narrows the universe, evidence structures the work,
 * and analyst judgment decides what earns diligence.
 *
 * Values are passed in from canonical data — nothing here is hard-coded.
 */
export default function ResearchFunnel({ stages }: { stages: FunnelStage[] }) {
  const reduced = usePrefersReducedMotion();
  const [ref, inView] = useInView<HTMLDivElement>();

  return (
    <div ref={ref}>
      <ol className="relative grid gap-3 sm:grid-cols-2 lg:grid-cols-6">
        {/* Progress rail: draws left→right on desktop as the block enters view. */}
        <li aria-hidden className="pointer-events-none absolute inset-x-0 top-[38px] hidden lg:block">
          <div className="h-px w-full bg-paper-line" />
          <div
            className="-mt-px h-px bg-sea/60"
            style={{
              width: reduced ? '100%' : inView ? '100%' : '0%',
              transition: 'width 1500ms cubic-bezier(.22,.61,.36,1) 120ms',
            }}
          />
        </li>

        {stages.map((s, i) => {
          const tone =
            s.emphasis === 'terminal' ? 'text-rust'
            : s.emphasis === 'strong' ? 'text-sea-deep'
            : 'text-ink';
          const body = (
            <>
              <div className="relative mb-3 flex h-[18px] items-center">
                <span
                  className={`h-2 w-2 rounded-full ring-4 ring-paper ${
                    s.emphasis === 'terminal' ? 'bg-rust' : 'bg-sea'
                  }`}
                  style={
                    reduced
                      ? undefined
                      : {
                          opacity: inView ? 1 : 0,
                          transform: inView ? 'scale(1)' : 'scale(.4)',
                          transition: `opacity 380ms ease-out ${180 + i * 190}ms, transform 380ms cubic-bezier(.22,.61,.36,1) ${180 + i * 190}ms`,
                        }
                  }
                />
              </div>
              <div
                style={
                  reduced
                    ? undefined
                    : {
                        opacity: inView ? 1 : 0,
                        transform: inView ? 'none' : 'translateY(10px)',
                        transition: `opacity 520ms ease-out ${240 + i * 190}ms, transform 520ms cubic-bezier(.22,.61,.36,1) ${240 + i * 190}ms`,
                      }
                }
              >
                <div className={`font-mono text-2xl font-semibold tabular-nums tracking-tight ${tone}`}>
                  {s.value === null ? s.display : <Counter value={s.value} format="num" />}
                </div>
                <div className="mt-1 text-[13px] font-medium">{s.label}</div>
                <div className="meta mt-1">{s.note}</div>
              </div>
            </>
          );

          return (
            <li key={s.label} className="relative">
              {s.href ? (
                <Link href={s.href} className="card-interactive block rounded-lg border border-paper-line bg-paper-card p-4">
                  {body}
                  <span className="mt-2 inline-block text-[12px] font-medium text-sea">
                    Open <span className="arrow" aria-hidden>→</span>
                  </span>
                </Link>
              ) : (
                <div className="rounded-lg border border-paper-line bg-paper-card p-4">{body}</div>
              )}
            </li>
          );
        })}
      </ol>
    </div>
  );
}
