import type { Evidence } from '@/lib/types';
import { evidenceTypeLabel, fmtMoney } from '@/lib/labels';

const TIER_TONE: Record<string, string> = {
  tier1: 'chip-moss', tier2: 'chip-sea', tier3: 'chip-rust',
};

/**
 * Evidence card. Sources are shown inline and always linked — never hidden
 * behind a generic "learn more".
 */
export function EvidenceCard({ e }: { e: Evidence }) {
  const s = e.source;
  return (
    <li className="card card-evidence p-4">
      <div className="flex flex-wrap items-center gap-1.5">
        <span className="chip chip-sea">{evidenceTypeLabel(e.type)}</span>
        {e.evidence_date && <span className="mono text-ink/50">{e.evidence_date}</span>}
        {e.value ? <span className="chip chip-neutral">{fmtMoney(e.value)}</span> : null}
        {s.quality && (
          <span className={`chip ${TIER_TONE[s.quality] ?? 'chip-neutral'}`}>{s.quality}</span>
        )}
        {e.extraction_method === 'ai_extracted' && (
          <span className="chip chip-rust">AI-extracted</span>
        )}
      </div>
      <p className="body mt-2 text-[14px]">{e.observed_claim}</p>
      <div className="meta mt-2.5 flex flex-wrap items-center gap-x-2 gap-y-1">
        {s.publisher && <span className="font-medium text-ink/60">{s.publisher}</span>}
        {s.url && (
          <a href={s.url} target="_blank" rel="noopener noreferrer" className="link break-all">
            {shortUrl(s.url)} <span className="ext" aria-hidden>↗</span>
          </a>
        )}
        {s.accessed_at && <span className="text-ink/40">accessed {s.accessed_at}</span>}
      </div>
    </li>
  );
}

export function EvidenceList({ evidence }: { evidence: Evidence[] }) {
  if (!evidence.length) {
    return <p className="meta">No evidence records attached.</p>;
  }
  const sorted = [...evidence].sort((a, b) =>
    (b.evidence_date ?? '').localeCompare(a.evidence_date ?? ''),
  );
  return <ul className="space-y-3">{sorted.map((e) => <EvidenceCard key={e.evidence_id} e={e} />)}</ul>;
}

export function shortUrl(url: string): string {
  try {
    const u = new URL(url);
    const path = u.pathname.length > 40 ? `${u.pathname.slice(0, 38)}…` : u.pathname;
    return `${u.hostname.replace(/^www\./, '')}${path === '/' ? '' : path}`;
  } catch {
    return url;
  }
}
