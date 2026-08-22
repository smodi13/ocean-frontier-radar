'use client';

import { fmtMoney, fmtNum } from '@/lib/labels';
import { useCountUp } from '@/lib/motion';

/**
 * `format` is a string token, not a function: most callers are server
 * components, and React cannot serialise a function across that boundary.
 * The tokens map to the same formatters used everywhere else, so an animated
 * figure always renders identically to a static one.
 */
export type CounterFormat = 'num' | 'money' | 'percent';

const FORMATTERS: Record<CounterFormat, (n: number) => string> = {
  num: fmtNum,
  money: fmtMoney,
  percent: (n) => `${n}%`,
};

/**
 * Counts a metric up when it first scrolls into view, then stops permanently.
 * The accessible name is always the final value, so assistive technology never
 * announces an intermediate number.
 */
export function Counter({
  value, format = 'num', className = '',
}: {
  value: number;
  format?: CounterFormat;
  className?: string;
}) {
  const fmt = FORMATTERS[format];
  const [ref, current] = useCountUp(value);
  return (
    <span ref={ref} className={className} aria-label={fmt(value)}>
      <span aria-hidden>{fmt(current)}</span>
    </span>
  );
}
