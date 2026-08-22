'use client';

import { fmtMoney } from '@/lib/labels';
import { useInView, usePrefersReducedMotion } from '@/lib/motion';

interface Bucket { id: string; n: number; value: number; annualised: number; reason: string }

const LABEL: Record<string, string> = {
  rnd_program: 'R&D programmes',
  integration_prime: 'Integration / primes',
  platform_purchase: 'Complete platforms',
  services_support: 'Services / support',
  components_spares: 'Components / spares',
  sensors_payload_dev: 'Sensors / payloads',
  payload_deployment: 'Payload deployment',
  launch_recovery: 'Launch & recovery',
  excluded_facilities: 'Excluded — facilities',
  excluded_counter_uuv: 'Excluded — counter-UUV',
  unclassified: 'Unclassified',
};

/** Addressable buckets for a propulsion/payload subsystem vendor. */
const ADDRESSABLE = new Set(['components_spares', 'payload_deployment']);

export function ProcurementBuckets({ buckets }: { buckets: Bucket[] }) {
  const max = Math.max(...buckets.map((b) => b.value));
  const reduced = usePrefersReducedMotion();
  const [ref, inView] = useInView<HTMLUListElement>();
  const show = reduced || inView;

  return (
    <ul ref={ref} className="space-y-2.5">
      {buckets.map((b, i) => {
        const excluded = b.id.startsWith('excluded_');
        const addressable = ADDRESSABLE.has(b.id);
        const pct = Math.max(1, Math.round((b.value / max) * 100));
        return (
          <li key={b.id}>
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <span className={`text-[13.5px] ${addressable ? 'font-semibold text-sea-deep' : excluded ? 'text-ink/40 line-through' : 'text-ink/80'}`}>
                {LABEL[b.id] ?? b.id}
                <span className="meta ml-2">{b.n} contract{b.n === 1 ? '' : 's'}</span>
              </span>
              <span className="mono text-ink/70">{fmtMoney(b.value)}</span>
            </div>
            <div className="mt-1 h-2 w-full overflow-hidden rounded-sm bg-paper-line">
              {/*
                Bars grow from zero when the chart enters view so the eye follows
                the size ordering; the widths themselves are the audited values.
              */}
              <div
                className={`bar-fill h-full ${addressable ? 'bg-sea' : excluded ? 'bg-ink/15' : 'bg-ink/35'}`}
                style={{
                  width: show ? `${pct}%` : '0%',
                  transitionDelay: reduced ? '0ms' : `${i * 70}ms`,
                }}
              />
            </div>
            <p className="mt-1 text-[11px] leading-snug text-ink/45">{b.reason}</p>
          </li>
        );
      })}
    </ul>
  );
}
