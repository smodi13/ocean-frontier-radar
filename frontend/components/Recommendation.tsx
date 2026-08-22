'use client';

import { useEffect, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { usePrefersReducedMotion } from '@/lib/motion';

interface Unresolved { title: string; detail: string }

/**
 * The verdict is the single most important thing on this page, so it arrives
 * first and on its own beat: the block settles, then the word, then the reasoning.
 * A sentinel below it drives the sticky summary bar — the reader should never
 * have to scroll back up to remember what the recommendation was.
 */
export function RecommendationCard({
  verdict, summary, unresolved, advanceIf, passIf, noInvestNote,
}: {
  verdict: string; summary: string; unresolved: Unresolved[];
  advanceIf: string; passIf: string; noInvestNote: ReactNode;
}) {
  const reduced = usePrefersReducedMotion();
  const sentinel = useRef<HTMLDivElement>(null);
  const [showSticky, setShowSticky] = useState(false);

  useEffect(() => {
    const el = sentinel.current;
    if (!el || typeof IntersectionObserver === 'undefined') return;
    const io = new IntersectionObserver(
      ([e]) => setShowSticky(!e.isIntersecting && e.boundingClientRect.top < 0),
      { threshold: 0 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  const enter = (n: number) => (reduced ? undefined : `ofr-enter ofr-d${n}`);

  return (
    <>
      <div className={`card overflow-hidden ${reduced ? '' : 'ofr-enter'}`}>
        <div className="border-b border-paper-line bg-rust-pale/50 px-6 py-5 sm:px-8">
          <p className={`eyebrow text-rust ${enter(1) ?? ''}`}>Recommendation</p>
          <p
            className={`mt-1 text-3xl font-semibold tracking-tight text-rust sm:text-4xl ${enter(2) ?? ''}`}
          >
            {verdict}
          </p>
        </div>
        <div className="px-6 py-6 sm:px-8">
          <p className={`body max-w-prose ${enter(3) ?? ''}`}>{summary}</p>

          <div className={enter(4)}>
            <h3 className="h3 mt-6 mb-3 text-[14px]">
              Three questions public information cannot answer
            </h3>
            <ol className="grid gap-3 lg:grid-cols-3">
              {unresolved.map((u, i) => (
                <li key={u.title} className="rounded border border-paper-line bg-paper p-4">
                  <div className="mono text-rust">{String(i + 1).padStart(2, '0')}</div>
                  <div className="mt-1 text-[14px] font-semibold">{u.title}</div>
                  <p className="meta mt-1.5">{u.detail}</p>
                </li>
              ))}
            </ol>
          </div>

          <div className={`mt-6 grid gap-3 sm:grid-cols-2 ${enter(5) ?? ''}`}>
            <div className="rounded-md border-l-[3px] border-l-moss bg-moss-pale/40 px-4 py-3">
              <p className="text-[12px] font-semibold uppercase tracking-wider text-moss">Advance if</p>
              <p className="body mt-1 text-[14px]">{advanceIf}</p>
            </div>
            <div className="rounded-md border-l-[3px] border-l-rust bg-rust-pale/40 px-4 py-3">
              <p className="text-[12px] font-semibold uppercase tracking-wider text-rust">Pass if</p>
              <p className="body mt-1 text-[14px]">{passIf}</p>
            </div>
          </div>

          <p className={`meta mt-5 max-w-prose ${enter(6) ?? ''}`}>{noInvestNote}</p>
        </div>
      </div>
      <div ref={sentinel} aria-hidden />

      {/* Desktop-only: the verdict stays available while the reader is deep in evidence. */}
      <div
        className="pointer-events-none fixed inset-x-0 top-14 z-30 hidden lg:block"
        style={{
          opacity: showSticky ? 1 : 0,
          transform: showSticky || reduced ? 'none' : 'translateY(-8px)',
          transition: reduced ? 'none' : 'opacity 300ms ease, transform 300ms ease',
        }}
      >
        <div className="border-b border-paper-line bg-paper/90 backdrop-blur-md">
          <div className="wrap flex h-11 items-center justify-between gap-4">
            <span className="text-[13px] font-medium text-ink/70">
              ARMADA Marine Robotics · outside-in diligence
            </span>
            <span className="flex items-center gap-2">
              <span className="text-[11px] uppercase tracking-wider text-ink/45">Recommendation</span>
              <span className="rounded bg-rust-pale px-2 py-0.5 text-[13px] font-semibold text-rust">
                {verdict}
              </span>
            </span>
          </div>
        </div>
      </div>
    </>
  );
}
