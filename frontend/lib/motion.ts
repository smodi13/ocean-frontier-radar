'use client';

import { useEffect, useRef, useState } from 'react';

/**
 * Motion primitives — deliberately dependency-free.
 *
 * Everything this site needs (scroll reveal, count-up, bar draw, scenario
 * number tweens, hero network) is expressible with IntersectionObserver,
 * requestAnimationFrame and CSS transforms. A general animation framework
 * would add tens of kilobytes of JavaScript to a static research site whose
 * whole point is being fast and inspectable, so these ~2KB of hooks stand in
 * for it.
 *
 * Every hook honours prefers-reduced-motion by jumping straight to the final
 * state — no animation, no delay, no loss of information.
 */

export function usePrefersReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const apply = () => setReduced(mq.matches);
    apply();
    mq.addEventListener('change', apply);
    return () => mq.removeEventListener('change', apply);
  }, []);
  return reduced;
}

/** Fires once when the element first enters the viewport, then disconnects. */
export function useInView<T extends HTMLElement>(
  // threshold 0, deliberately: a fractional threshold is unreachable for any
  // block taller than the viewport, which silently left long sections (the
  // 31-signal Frontier list, the evidence register) stuck at opacity 0
  // forever. Firing on first contact and letting rootMargin set the trigger
  // point is correct for every block size.
  { rootMargin = '0px 0px -12% 0px', threshold = 0 } = {},
): [React.RefObject<T | null>, boolean] {
  const ref = useRef<T | null>(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (typeof IntersectionObserver === 'undefined') {
      // Very old browsers: reveal on the next frame rather than synchronously,
      // so the effect never triggers a cascading render.
      const raf = requestAnimationFrame(() => setInView(true));
      return () => cancelAnimationFrame(raf);
    }
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          // `bottom <= 0` means the element is already above the viewport: the
          // reader arrived below it via an anchor link, a restored scroll
          // position or a jump-scroll that outran the observer. Content that
          // has been scrolled past must be visible, not stuck mid-fade.
          if (e.isIntersecting || e.boundingClientRect.bottom <= 0) {
            setInView(true);
            io.disconnect();   // reveal once; never re-trigger on scroll
          }
        }
      },
      { rootMargin, threshold },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [rootMargin, threshold]);

  return [ref, inView];
}

const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);

/** Tweens a number toward `target`. Used for count-ups and scenario switches. */
export function useTweenedNumber(target: number, duration = 900): number {
  const reduced = usePrefersReducedMotion();
  const [value, setValue] = useState(target);
  const fromRef = useRef(target);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    if (reduced || duration <= 0) {
      fromRef.current = target;
      return;   // value is derived below; no state update needed
    }
    const from = fromRef.current;
    if (from === target) return;
    const start = performance.now();

    const step = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      const v = from + (target - from) * easeOutCubic(t);
      setValue(v);
      if (t < 1) {
        rafRef.current = requestAnimationFrame(step);
      } else {
        fromRef.current = target;
        setValue(target);
      }
    };
    rafRef.current = requestAnimationFrame(step);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      fromRef.current = value;
    };
    // `value` intentionally excluded: including it would restart the tween each frame.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, duration, reduced]);

  // Under reduced motion the final value is returned directly, so the hook
  // never animates and never schedules a render.
  return reduced || duration <= 0 ? target : value;
}

/**
 * Counts up to `target` once the element is on screen.
 *
 * `null` means "show the real number": that is the state the server renders,
 * the state before the animation starts, and the state it returns to when the
 * animation finishes. This matters more than the animation does — the static
 * HTML of a research site must contain 579, not 0, so the figures are correct
 * with JavaScript broken, blocked or still loading, and correct again the
 * instant the count-up lands (no floating-point drift on the final frame).
 */
export function useCountUp(
  target: number,
  { duration = 1100 }: { duration?: number } = {},
): [React.RefObject<HTMLSpanElement | null>, number] {
  const reduced = usePrefersReducedMotion();
  const [ref, inView] = useInView<HTMLSpanElement>();
  const [value, setValue] = useState<number | null>(null);
  const done = useRef(false);

  // A number the reader can already see must never run backwards to zero to
  // animate. Anything on screen at load keeps its real value; the count-up is
  // for figures the reader scrolls to.
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const box = el.getBoundingClientRect();
    if (box.top < window.innerHeight && box.bottom > 0) done.current = true;
  }, [ref]);

  useEffect(() => {
    if (!inView || done.current || reduced) return;
    done.current = true;
    const start = performance.now();
    let raf = 0;
    const step = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      // The first frame lands near zero on its own, so the count never needs a
      // synchronous reset that would flash 0 over an already-correct number.
      setValue(t < 1 ? target * easeOutCubic(t) : null);
      if (t < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [inView, target, duration, reduced]);

  // Reduced motion shows the final value immediately, with no count-up.
  return [ref, reduced || value === null ? target : value];
}
