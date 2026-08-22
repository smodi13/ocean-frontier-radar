'use client';

import { useInView, usePrefersReducedMotion } from '@/lib/motion';

interface Debate {
  id: string; title: string; subtitle?: string; current_view: string;
  bull: string[]; bear: string[]; unknown: string; upgrade: string; downgrade: string;
}

/**
 * Bull and bear arrive together, from opposite sides, then the unknown settles
 * beneath them. The motion carries the structure of the argument: two opposed
 * readings of the same evidence, and the thing neither can resolve.
 */
export function DebateCard({ debate, index }: { debate: Debate; index: number }) {
  const reduced = usePrefersReducedMotion();
  const [ref, inView] = useInView<HTMLElement>();
  const show = reduced || inView;

  const side = (dir: -1 | 1, delay: number) =>
    reduced
      ? undefined
      : {
          opacity: show ? 1 : 0,
          transform: show ? 'none' : `translateX(${dir * 12}px)`,
          transition: `opacity 520ms cubic-bezier(.22,.61,.36,1) ${delay}ms, transform 520ms cubic-bezier(.22,.61,.36,1) ${delay}ms`,
        };

  return (
    <article ref={ref} className="card p-5 sm:p-7">
      <div className="flex items-baseline gap-3">
        <span className="mono text-sea">{String(index + 1).padStart(2, '0')}</span>
        <div>
          <h3 className="h2 text-[19px]">{debate.title}</h3>
          {debate.subtitle && <p className="meta mt-1">{debate.subtitle}</p>}
        </div>
      </div>

      <div className="mt-5 rounded-md border-l-[3px] border-l-ink/25 bg-paper px-4 py-3">
        <p className="text-[12px] font-semibold uppercase tracking-wider text-ink/50">Current view</p>
        <p className="body mt-1 text-[14px]">{debate.current_view}</p>
      </div>

      <div className="mt-4 grid gap-3 lg:grid-cols-2">
        <div
          className="rounded-md border-l-[3px] border-l-moss bg-moss-pale/40 px-4 py-3"
          style={side(-1, 90)}
        >
          <p className="text-[12px] font-semibold uppercase tracking-wider text-moss">Bull evidence</p>
          <ul className="mt-2 space-y-1.5">
            {debate.bull.map((b, j) => <li key={j} className="body text-[13.5px]">{b}</li>)}
          </ul>
        </div>
        <div
          className="rounded-md border-l-[3px] border-l-rust bg-rust-pale/40 px-4 py-3"
          style={side(1, 90)}
        >
          <p className="text-[12px] font-semibold uppercase tracking-wider text-rust">Bear evidence</p>
          <ul className="mt-2 space-y-1.5">
            {debate.bear.map((b, j) => <li key={j} className="body text-[13.5px]">{b}</li>)}
          </ul>
        </div>
      </div>

      <div
        className="mt-4 rounded-md border-l-[3px] border-l-sea bg-sea-pale/40 px-4 py-3"
        style={
          reduced
            ? undefined
            : {
                opacity: show ? 1 : 0,
                transform: show ? 'none' : 'translateY(8px)',
                transition: 'opacity 480ms ease 330ms, transform 480ms ease 330ms',
              }
        }
      >
        <p className="text-[12px] font-semibold uppercase tracking-wider text-sea-deep">Unknown</p>
        <p className="body mt-1 text-[14px]">{debate.unknown}</p>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-wide text-ink/45">
            Would increase conviction
          </p>
          <p className="body mt-1 text-[13.5px]">{debate.upgrade}</p>
        </div>
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-wide text-ink/45">
            Would reduce conviction
          </p>
          <p className="body mt-1 text-[13.5px]">{debate.downgrade}</p>
        </div>
      </div>
    </article>
  );
}
