import Link from 'next/link';
import type { ReactNode } from 'react';

export function PageHeader({
  eyebrow, title, lede, children,
}: { eyebrow?: string; title: string; lede?: ReactNode; children?: ReactNode }) {
  return (
    <div className="border-b border-paper-line bg-white">
      <div className="wrap py-12 sm:py-16">
        {eyebrow && <p className="eyebrow mb-3">{eyebrow}</p>}
        <h1 className="h1 max-w-3xl">{title}</h1>
        {lede && <div className="lede mt-5 max-w-prose">{lede}</div>}
        {children && <div className="mt-8">{children}</div>}
      </div>
    </div>
  );
}

export function Section({
  id, title, kicker, children, className = '',
}: { id?: string; title?: string; kicker?: string; children: ReactNode; className?: string }) {
  return (
    <section id={id} className={`wrap py-12 sm:py-16 ${className}`}>
      {kicker && <p className="eyebrow mb-2">{kicker}</p>}
      {title && <h2 className="h2 mb-6">{title}</h2>}
      {children}
    </section>
  );
}

export function Stat({ value, label, hint }: { value: string; label: string; hint?: string }) {
  return (
    <div className="card p-4">
      <div className="stat-n text-sea-deep">{value}</div>
      <div className="stat-l">{label}</div>
      {hint && <div className="mt-1.5 text-[11px] leading-snug text-ink/40">{hint}</div>}
    </div>
  );
}

export function Chip({ tone = 'neutral', children }: { tone?: 'neutral' | 'sea' | 'moss' | 'rust'; children: ReactNode }) {
  return <span className={`chip chip-${tone}`}>{children}</span>;
}

/** Observed / Inferred / Unknown — the core evidence-discipline component. */
export function Epistemic({
  kind, items, note,
}: { kind: 'observed' | 'inferred' | 'unknown'; items: string[]; note?: string }) {
  if (!items.length) return null;
  const copy = {
    observed: { label: 'Observed', hint: 'Directly supported by a cited public source.' },
    inferred: { label: 'Inferred', hint: 'Analyst interpretation of the evidence, not a sourced fact.' },
    unknown: { label: 'Unknown', hint: 'Requires primary diligence. Public sources cannot answer it.' },
  }[kind];
  return (
    <div className={`epi epi-${kind}`}>
      <div className="flex flex-wrap items-baseline gap-x-2">
        <span className="text-[12px] font-semibold uppercase tracking-wider">{copy.label}</span>
        <span className="text-[11px] text-ink/50">{note ?? copy.hint}</span>
      </div>
      <ul className="mt-2 space-y-1.5">
        {items.map((t, i) => (
          <li key={i} className="body text-[14px]">{t}</li>
        ))}
      </ul>
    </div>
  );
}

export function Callout({ tone = 'sea', title, children }: { tone?: 'sea' | 'rust' | 'moss'; title?: string; children: ReactNode }) {
  const border = { sea: 'border-l-sea', rust: 'border-l-rust', moss: 'border-l-moss' }[tone];
  const bg = { sea: 'bg-sea-pale/40', rust: 'bg-rust-pale/40', moss: 'bg-moss-pale/40' }[tone];
  return (
    <div className={`rounded-md border-l-[3px] ${border} ${bg} px-5 py-4`}>
      {title && <p className="mb-1.5 text-[13px] font-semibold">{title}</p>}
      <div className="body text-[14px]">{children}</div>
    </div>
  );
}

export function Bar({ value, max, tone = 'sea' }: { value: number; max: number; tone?: 'sea' | 'rust' | 'moss' }) {
  const pct = max > 0 ? Math.max(2, Math.round((value / max) * 100)) : 0;
  const c = { sea: 'bg-sea', rust: 'bg-rust', moss: 'bg-moss' }[tone];
  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-paper-line" role="presentation">
      <div className={`h-full rounded-full ${c}`} style={{ width: `${pct}%` }} />
    </div>
  );
}

export function BackLink({ href, label }: { href: string; label: string }) {
  return (
    <Link href={href} className="meta inline-flex items-center gap-1.5 hover:text-sea">
      <span aria-hidden>←</span> {label}
    </Link>
  );
}
