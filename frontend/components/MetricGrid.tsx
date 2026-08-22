'use client';

import { Counter, type CounterFormat } from '@/components/motion/Counter';
import { RevealStagger } from '@/components/motion/Reveal';

export interface Metric {
  value: number;
  kind: 'count' | 'money' | 'percent';
  label: string;
  hint?: string;
}

const FORMAT: Record<Metric['kind'], CounterFormat> = {
  count: 'num',
  money: 'money',
  percent: 'percent',
};

export default function MetricGrid({ metrics }: { metrics: Metric[] }) {
  return (
    <RevealStagger
      step={45}
      className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4"
    >
      {metrics.map((m) => (
        <div key={m.label} className="card h-full p-4">
          <div className="stat-n text-sea-deep">
            <Counter value={m.value} format={FORMAT[m.kind]} />
          </div>
          <div className="stat-l">{m.label}</div>
          {m.hint && <div className="mt-1.5 text-[11px] leading-snug text-ink/40">{m.hint}</div>}
        </div>
      ))}
    </RevealStagger>
  );
}
