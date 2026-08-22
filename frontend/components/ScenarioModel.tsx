'use client';

import { useMemo, useState } from 'react';
import { fmtMoney } from '@/lib/data';

interface Assumption {
  driver: string; bear: number; base: number; bull: number; type: string; note: string;
}

const KEY = {
  podAsp: 'EPADS pod ASP ($)',
  pods: 'EPADS pods sold per year (steady state)',
  podGm: 'EPADS gross margin',
  propAsp: 'Propulsion module ASP ($)',
  props: 'Propulsion modules per year',
  propGm: 'Propulsion gross margin',
  eng: 'Engineering / R&D contract revenue ($/yr)',
  engGm: 'Engineering gross margin',
  support: 'Support / service revenue ($/yr)',
  heads: 'Headcount at steady state',
  cost: 'Fully loaded cost per head ($)',
  opex: 'Non-headcount opex ($/yr)',
  threshold: 'Venture-scale revenue threshold ($)',
} as const;

type Scenario = 'bear' | 'base' | 'bull';

export default function ScenarioModel({ assumptions }: { assumptions: Assumption[] }) {
  const [scenario, setScenario] = useState<Scenario>('base');
  const by = useMemo(
    () => Object.fromEntries(assumptions.map((a) => [a.driver, a])) as Record<string, Assumption>,
    [assumptions],
  );
  const v = (k: string) => by[k]?.[scenario] ?? 0;

  const epads = v(KEY.podAsp) * v(KEY.pods);
  const prop = v(KEY.propAsp) * v(KEY.props);
  const eng = v(KEY.eng);
  const support = v(KEY.support);
  const revenue = epads + prop + eng + support;
  const gross = epads * v(KEY.podGm) + prop * v(KEY.propGm) + eng * v(KEY.engGm);
  const opex = v(KEY.heads) * v(KEY.cost) + v(KEY.opex);
  const threshold = v(KEY.threshold);
  const gap = threshold - revenue;

  const lines: [string, number][] = [
    ['EPADS revenue', epads], ['Propulsion revenue', prop],
    ['Engineering / R&D revenue', eng], ['Support revenue', support],
  ];

  return (
    <div>
      <div className="flex flex-wrap items-center gap-2">
        {(['bear', 'base', 'bull'] as Scenario[]).map((s) => (
          <button
            key={s}
            onClick={() => setScenario(s)}
            className={`rounded border px-3 py-1.5 text-[13px] font-medium capitalize ${
              scenario === s
                ? 'border-sea bg-sea text-white'
                : 'border-paper-line bg-white text-ink/70 hover:border-sea/40'
            }`}
          >
            {s}
          </button>
        ))}
        <span className="meta ml-1">
          Interactive scenario switch. The canonical committed result is the <strong>base</strong> case.
        </span>
      </div>

      <div className="mt-5 grid gap-4 lg:grid-cols-2">
        <div className="card p-5">
          <h4 className="h3 mb-3 text-[14px]">Steady-state build</h4>
          <table className="w-full text-[13.5px]">
            <tbody>
              {lines.map(([label, val]) => (
                <tr key={label} className="border-b border-paper-line/70 last:border-0">
                  <td className="py-1.5 text-ink/75">{label}</td>
                  <td className="py-1.5 text-right font-mono tabular-nums">{fmtMoney(val)}</td>
                </tr>
              ))}
              <tr className="border-t-2 border-paper-line font-semibold">
                <td className="py-2">Total revenue</td>
                <td className="py-2 text-right font-mono tabular-nums text-sea-deep">{fmtMoney(revenue)}</td>
              </tr>
              <tr><td className="py-1.5 text-ink/75">Gross profit</td>
                  <td className="py-1.5 text-right font-mono tabular-nums">{fmtMoney(gross)}</td></tr>
              <tr><td className="py-1.5 text-ink/75">Operating cost</td>
                  <td className="py-1.5 text-right font-mono tabular-nums">({fmtMoney(opex)})</td></tr>
              <tr className="border-t border-paper-line font-medium">
                <td className="py-1.5">Operating profit</td>
                <td className="py-1.5 text-right font-mono tabular-nums">{fmtMoney(gross - opex)}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="card p-5">
          <h4 className="h3 mb-3 text-[14px]">Against the reference threshold</h4>
          <div className="space-y-3">
            <div>
              <div className="flex items-baseline justify-between text-[13.5px]">
                <span className="text-ink/75">Revenue</span>
                <span className="mono">{fmtMoney(revenue)}</span>
              </div>
              <div className="mt-1 h-3 w-full overflow-hidden rounded-sm bg-paper-line">
                <div className="h-full bg-sea" style={{ width: `${Math.min(100, (revenue / threshold) * 100)}%` }} />
              </div>
              <div className="meta mt-1">Reference threshold {fmtMoney(threshold)}</div>
            </div>
            <div className={`rounded-md border-l-[3px] px-4 py-3 ${gap > 0 ? 'border-l-rust bg-rust-pale/40' : 'border-l-moss bg-moss-pale/40'}`}>
              <p className="text-[13.5px] font-medium">
                {gap > 0
                  ? `Falls short of the reference threshold by ${fmtMoney(gap)}`
                  : `Clears the reference threshold by ${fmtMoney(-gap)}`}
              </p>
              <p className="meta mt-1">
                {scenario === 'base' &&
                  'And the base case already assumes pod and module volumes with no public evidence behind them.'}
                {scenario === 'bull' &&
                  'The bull case requires volumes far beyond anything evidenced in public records.'}
                {scenario === 'bear' &&
                  'The bear case is closer to what public evidence currently supports.'}
              </p>
            </div>
          </div>
        </div>
      </div>

      <details className="card mt-4 p-5">
        <summary className="cursor-pointer text-[14px] font-medium">
          All model inputs ({assumptions.length}) — every assumption labelled
        </summary>
        <table className="mt-4 w-full text-[13px]">
          <thead>
            <tr className="border-b border-paper-line text-left text-[11px] uppercase tracking-wide text-ink/50">
              <th className="py-2 pr-3 font-medium">Driver</th>
              <th className="py-2 pr-3 text-right font-medium">Bear</th>
              <th className="py-2 pr-3 text-right font-medium">Base</th>
              <th className="py-2 pr-3 text-right font-medium">Bull</th>
              <th className="py-2 font-medium">Basis</th>
            </tr>
          </thead>
          <tbody>
            {assumptions.map((a) => (
              <tr key={a.driver} className="border-b border-paper-line/60 align-top">
                <td className="py-2 pr-3">{a.driver}</td>
                {(['bear', 'base', 'bull'] as const).map((s) => (
                  <td key={s} className="py-2 pr-3 text-right font-mono tabular-nums">
                    {a[s] < 1 && a[s] > 0 ? `${(a[s] * 100).toFixed(0)}%` : a[s].toLocaleString()}
                  </td>
                ))}
                <td className="py-2">
                  <span className={`chip ${a.type.startsWith('OBSERVED') ? 'chip-moss' : 'chip-rust'}`}>
                    {a.type.startsWith('OBSERVED') ? 'observed-anchored' : 'analyst assumption'}
                  </span>
                  <p className="meta mt-1">{a.note}</p>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </details>
    </div>
  );
}
