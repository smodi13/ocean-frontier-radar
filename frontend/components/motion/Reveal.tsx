'use client';

import type { ReactNode } from 'react';
import { useInView, usePrefersReducedMotion } from '@/lib/motion';

const EASE = 'cubic-bezier(.22,.61,.36,1)';

/**
 * Section-level scroll reveal. Applied to content BLOCKS, never to individual
 * paragraphs — a page where every sentence fades in reads as a marketing site,
 * not a research tool.
 *
 * Uses transform + opacity only (compositor-friendly, no layout thrash), and
 * collapses to a plain wrapper under prefers-reduced-motion.
 */
export function Reveal({
  children, delay = 0, className = '',
}: { children: ReactNode; delay?: number; className?: string }) {
  const reduced = usePrefersReducedMotion();
  const [ref, inView] = useInView<HTMLDivElement>();

  if (reduced) return <div className={className}>{children}</div>;

  return (
    <div
      ref={ref}
      className={className}
      style={{
        opacity: inView ? 1 : 0,
        transform: inView ? 'none' : 'translateY(14px)',
        transition: `opacity 620ms ${EASE} ${delay}ms, transform 620ms ${EASE} ${delay}ms`,
        willChange: inView ? 'auto' : 'opacity, transform',
      }}
    >
      {children}
    </div>
  );
}

/**
 * Staggers a set of sibling blocks as the container enters view. Children are
 * wrapped in plain divs, so use this on grids rather than on <ul>/<ol>.
 */
export function RevealStagger({
  children, step = 70, className = '',
}: { children: ReactNode[]; step?: number; className?: string }) {
  const reduced = usePrefersReducedMotion();
  const [ref, inView] = useInView<HTMLDivElement>();

  // Conditional children ({cond && <Card/>}) arrive as `false`; wrapping those
  // would leave empty grid cells, so they are dropped before wrapping.
  const items = children.filter(Boolean);

  return (
    <div ref={ref} className={className}>
      {items.map((child, i) => (
        <div
          key={i}
          style={
            reduced
              ? undefined
              : {
                  opacity: inView ? 1 : 0,
                  transform: inView ? 'none' : 'translateY(12px)',
                  transition: `opacity 520ms ${EASE} ${i * step}ms, transform 520ms ${EASE} ${i * step}ms`,
                }
          }
        >
          {child}
        </div>
      ))}
    </div>
  );
}
