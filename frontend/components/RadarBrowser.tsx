'use client';

import Link from 'next/link';
import { useMemo, useState } from 'react';
import type { CandidateRow } from '@/lib/types';
import { CATEGORY_LABEL, CENTRALITY_LABEL, QUEUE_LABEL } from '@/lib/data';

const QUEUE_TONE: Record<string, string> = {
  tier_a: 'chip-moss', frontier: 'chip-sea', tier_b: 'chip-neutral', tier_c: 'chip-neutral',
};

function Select({
  label, value, onChange, options,
}: { label: string; value: string; onChange: (v: string) => void; options: [string, string][] }) {
  return (
    <label className="flex flex-col gap-1">
      <span className="text-[11px] font-medium uppercase tracking-wide text-ink/50">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded border border-paper-line bg-white px-2.5 py-1.5 text-[13px]"
      >
        {options.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
      </select>
    </label>
  );
}

export default function RadarBrowser({ rows, detailIds }: { rows: CandidateRow[]; detailIds: string[] }) {
  const linkable = useMemo(() => new Set(detailIds), [detailIds]);
  const [q, setQ] = useState('');
  const [queue, setQueue] = useState('actionable');
  const [category, setCategory] = useState('all');
  const [centrality, setCentrality] = useState('all');
  const [kind, setKind] = useState('all');
  const [signal, setSignal] = useState('all');

  const categories = useMemo(
    () => Array.from(new Set(rows.map((r) => r.category).filter(Boolean) as string[])).sort(),
    [rows],
  );

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return rows.filter((r) => {
      if (queue === 'actionable' && !['tier_a', 'tier_b', 'frontier'].includes(r.queue ?? '')) return false;
      if (queue !== 'actionable' && queue !== 'all' && r.queue !== queue) return false;
      if (category !== 'all' && r.category !== category) return false;
      if (centrality !== 'all' && r.centrality !== centrality) return false;
      if (kind === 'company' && r.companyFormed !== 1) return false;
      if (kind === 'pre_company' && r.companyFormed === 1) return false;
      if (signal !== 'all' && r.sourcingSignal !== signal) return false;
      if (needle) {
        const hay = `${r.name} ${r.institution ?? ''} ${r.company ?? ''} ${r.geography ?? ''} ${r.strongestEvidence ?? ''}`.toLowerCase();
        if (!hay.includes(needle)) return false;
      }
      return true;
    });
  }, [rows, q, queue, category, centrality, kind, signal]);

  const reset = () => {
    setQ(''); setQueue('actionable'); setCategory('all');
    setCentrality('all'); setKind('all'); setSignal('all');
  };

  return (
    <div>
      <div className="card p-4">
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <label className="flex flex-col gap-1 lg:col-span-3">
            <span className="text-[11px] font-medium uppercase tracking-wide text-ink/50">Search</span>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Name, institution, geography, evidence…"
              className="rounded border border-paper-line bg-white px-3 py-2 text-[14px]"
            />
          </label>
          <Select label="Queue" value={queue} onChange={setQueue} options={[
            ['actionable', 'Actionable (Tier A + B + Frontier)'],
            ['tier_a', 'Tier A — diligence now'],
            ['tier_b', 'Tier B — research queue'],
            ['frontier', 'Frontier — pre-company'],
            ['tier_c', 'Tier C — watch'],
            ['all', 'All retrieved'],
          ]} />
          <Select label="Category" value={category} onChange={setCategory}
            options={[['all', 'All categories'], ...categories.map((c) => [c, CATEGORY_LABEL[c] ?? c] as [string, string])]} />
          <Select label="Ocean centrality" value={centrality} onChange={setCentrality} options={[
            ['all', 'Any centrality'],
            ['central_mechanism', 'Central — mechanism'],
            ['primary_end_market', 'Primary end market'],
            ['strong_adjacency', 'Strong adjacency'],
          ]} />
          <Select label="Maturity" value={kind} onChange={setKind} options={[
            ['all', 'Company or pre-company'],
            ['company', 'Company formed'],
            ['pre_company', 'Pre-company / research'],
          ]} />
          <Select label="Sourcing signal" value={signal} onChange={setSignal} options={[
            ['all', 'Any sourcing signal'],
            ['pre_company', 'Pre-company'],
            ['emerging', 'Emerging'],
            ['obvious', 'Widely visible'],
          ]} />
          <div className="flex items-end">
            <button onClick={reset} className="rounded border border-paper-line px-3 py-1.5 text-[13px] hover:border-sea/40">
              Reset filters
            </button>
          </div>
        </div>
      </div>

      <p className="meta mt-4">
        Showing <span className="font-semibold text-ink/70">{filtered.length.toLocaleString()}</span> of{' '}
        {rows.length.toLocaleString()} retrieved candidates. Detail pages are generated for Tier A and
        Frontier records; others show their summary row here.
      </p>

      <ul className="mt-4 space-y-2">
        {filtered.slice(0, 250).map((r) => {
          const hasDetail = linkable.has(r.id);
          const queueNote =
            r.queue === 'tier_b' ? 'Research queue' :
            r.queue === 'tier_c' ? 'Watch' : null;

          const inner = (
            <>
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="min-w-0">
                  <div className={`text-[15px] font-semibold leading-snug ${hasDetail ? '' : 'text-ink/75'}`}>
                    {r.name}
                  </div>
                  <div className="meta mt-0.5">
                    {[r.institution, r.geography].filter(Boolean).join(' · ') || '—'}
                  </div>
                </div>
                <div className="flex flex-wrap items-center gap-1.5">
                  {r.queue && <span className={`chip ${QUEUE_TONE[r.queue]}`}>{QUEUE_LABEL[r.queue].split(' — ')[0]}</span>}
                  {r.companyFormed !== 1 && <span className="chip chip-sea">Pre-company</span>}
                  {r.category && <span className="chip chip-neutral">{CATEGORY_LABEL[r.category] ?? r.category}</span>}
                </div>
              </div>

              {r.strongestEvidence && (
                <p className="body mt-2 line-clamp-2 text-[13.5px]">{r.strongestEvidence}</p>
              )}

              <div className="meta mt-2.5 flex flex-wrap items-center gap-x-3 gap-y-1">
                {r.centrality && <span>{CENTRALITY_LABEL[r.centrality]}</span>}
                {r.latestSignal && <span>Latest signal {r.latestSignal}</span>}
                <span>{r.evidenceCount} evidence record{r.evidenceCount === 1 ? '' : 's'}</span>
                {r.whySurfaced.length > 0 && <span>via {r.whySurfaced[0]}</span>}
                {r.flags.map((f) => (
                  <span key={f} className="chip chip-rust">{f.replace(/_/g, ' ').toLowerCase()}</span>
                ))}
              </div>

              {/* Affordance: linkable rows say so; queue records say why they are not. */}
              <div className="mt-3 border-t border-paper-line/70 pt-2.5">
                {hasDetail ? (
                  <span className="text-[12.5px] font-medium text-sea">
                    Open evidence detail <span aria-hidden>→</span>
                  </span>
                ) : (
                  <span className="text-[12px] text-ink/45">
                    {queueNote ?? 'Queue record'} — surfaced and classified, no diligence page.
                    Detail pages exist only where analyst review has been done.
                  </span>
                )}
              </div>
            </>
          );

          return (
            <li key={r.id}>
              {hasDetail ? (
                <Link
                  href={`/radar/${r.id}/`}
                  className="card block p-4 transition-colors hover:border-sea/50 hover:bg-sea-pale/20"
                >
                  {inner}
                </Link>
              ) : (
                <div
                  className="rounded-lg border border-dashed border-paper-line bg-paper/60 p-4 cursor-default"
                  aria-disabled="true"
                >
                  {inner}
                </div>
              )}
            </li>
          );
        })}
      </ul>

      {filtered.length > 250 && (
        <p className="meta mt-4">
          Showing the first 250 matches. Narrow the filters to see the rest.
        </p>
      )}
      {filtered.length === 0 && (
        <p className="meta mt-6">No candidates match these filters.</p>
      )}
    </div>
  );
}
