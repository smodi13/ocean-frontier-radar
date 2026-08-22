'use client';

import { useMemo } from 'react';
import { usePrefersReducedMotion } from '@/lib/motion';

/**
 * Abstract research network for the hero.
 *
 * The visual argument: public signals (research, grants, patents, licences,
 * institutions) drift inward along current-like paths, cross a set of
 * concentric survey arcs, and converge on a single dense point — the diligence
 * queue. It is a system diagram, not a radar screen and not a seascape.
 *
 * Implementation is pure SVG + CSS keyframes: no canvas, no WebGL, no
 * animation library, nothing recalculated on the main thread per frame.
 * Under prefers-reduced-motion the whole thing renders as a static diagram.
 */

const SIGNALS = [
  { label: 'Research',     r: 0.92, a: 198, dur: 34 },
  { label: 'Grants',       r: 0.80, a: 232, dur: 41 },
  { label: 'Patents',      r: 0.97, a: 264, dur: 37 },
  { label: 'Institutions', r: 0.71, a: 292, dur: 46 },
  { label: 'Licences',     r: 0.88, a: 318, dur: 39 },
  { label: 'Spinouts',     r: 0.63, a: 344, dur: 44 },
  { label: 'Evidence',     r: 0.99, a: 172, dur: 36 },
  { label: 'Companies',    r: 0.75, a: 146, dur: 43 },
];

// Focus point of the system, in viewBox units.
const CX = 640;
const CY = 300;

function polar(r: number, aDeg: number, scaleX = 560, scaleY = 250) {
  const a = (aDeg * Math.PI) / 180;
  return { x: CX + Math.cos(a) * r * scaleX, y: CY + Math.sin(a) * r * scaleY };
}

export default function HeroNetwork() {
  const reduced = usePrefersReducedMotion();

  const nodes = useMemo(
    () => SIGNALS.map((s) => ({ ...s, ...polar(s.r, s.a) })),
    [],
  );

  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 overflow-hidden"
    >
      <svg
        viewBox="0 0 1280 600"
        preserveAspectRatio="xMidYMid slice"
        className="h-full w-full"
      >
        <defs>
          {/* Fine coordinate grid — an operating environment, not decoration. */}
          <pattern id="ofr-grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M40 0H0V40" fill="none" stroke="#12566B" strokeWidth="0.5" opacity="0.10" />
          </pattern>
          {/* Fades the whole system out behind the text column. */}
          <linearGradient id="ofr-fade" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#F7F8F7" stopOpacity="1" />
            <stop offset="38%" stopColor="#F7F8F7" stopOpacity="0.94" />
            <stop offset="72%" stopColor="#F7F8F7" stopOpacity="0.30" />
            <stop offset="100%" stopColor="#F7F8F7" stopOpacity="0" />
          </linearGradient>
          <radialGradient id="ofr-core" cx="50%" cy="50%">
            <stop offset="0%" stopColor="#12566B" stopOpacity="0.30" />
            <stop offset="100%" stopColor="#12566B" stopOpacity="0" />
          </radialGradient>
        </defs>

        <rect width="1280" height="600" fill="url(#ofr-grid)" />

        {/* Bathymetric contours — depth, drawn as a survey would render it. */}
        <g fill="none" stroke="#12566B" strokeWidth="1">
          {[110, 190, 270, 350, 430].map((r, i) => (
            <ellipse
              key={r}
              cx={CX}
              cy={CY}
              rx={r * 1.55}
              ry={r * 0.72}
              opacity={0.13 - i * 0.015}
              className={reduced ? undefined : 'ofr-contour'}
              style={reduced ? undefined : { animationDelay: `${i * 1.6}s` }}
            />
          ))}
        </g>

        {/* Survey arcs — sonar-like sweep marks, static geometry. */}
        <g fill="none" stroke="#12566B" strokeLinecap="round">
          {[
            'M 1020 130 A 420 420 0 0 1 1020 470',
            'M 940 175 A 320 320 0 0 1 940 425',
            'M 860 220 A 220 220 0 0 1 860 380',
          ].map((d, i) => (
            <path
              key={d}
              d={d}
              strokeWidth={1}
              opacity={0.20 - i * 0.04}
              strokeDasharray="3 9"
              className={reduced ? undefined : 'ofr-arc'}
              style={reduced ? undefined : { animationDelay: `${i * 2.2}s` }}
            />
          ))}
        </g>

        {/* Signal trajectories converging on the diligence point. */}
        <g fill="none">
          {nodes.map((n, i) => {
            const midX = (n.x + CX) / 2 + (i % 2 ? 40 : -40);
            const midY = (n.y + CY) / 2 + (i % 3 ? -34 : 30);
            const d = `M ${n.x.toFixed(0)} ${n.y.toFixed(0)} Q ${midX.toFixed(0)} ${midY.toFixed(0)} ${CX} ${CY}`;
            return (
              <g key={n.label}>
                <path d={d} stroke="#12566B" strokeWidth="1" opacity="0.16" />
                {!reduced && (
                  <circle r="2.6" fill="#12566B" opacity="0.55">
                    <animateMotion
                      dur={`${n.dur}s`}
                      begin={`${i * 1.9}s`}
                      repeatCount="indefinite"
                      path={d}
                      keyPoints="0;1"
                      keyTimes="0;1"
                      calcMode="spline"
                      keySplines="0.4 0 0.5 1"
                    />
                  </circle>
                )}
              </g>
            );
          })}
        </g>

        {/* Signal origin markers. */}
        <g>
          {nodes.map((n, i) => (
            <g key={n.label}>
              <circle
                cx={n.x} cy={n.y} r="3.4"
                fill="#F7F8F7" stroke="#12566B" strokeWidth="1.2" opacity="0.75"
              />
              <circle
                cx={n.x} cy={n.y} r="3.4"
                fill="none" stroke="#12566B" strokeWidth="1"
                opacity="0"
                className={reduced ? undefined : 'ofr-ping'}
                style={reduced ? undefined : { animationDelay: `${i * 2.4}s` }}
              />
              <text
                x={n.x + 9} y={n.y + 3.5}
                fontSize="10.5"
                fill="#0B1622"
                opacity="0.42"
                fontFamily="ui-monospace, SFMono-Regular, Menlo, monospace"
                letterSpacing="0.04em"
              >
                {n.label}
              </text>
            </g>
          ))}
        </g>

        {/* The diligence queue: where every path terminates. */}
        <g>
          <circle cx={CX} cy={CY} r="86" fill="url(#ofr-core)" />
          <circle cx={CX} cy={CY} r="5" fill="#12566B" opacity="0.85" />
          <circle
            cx={CX} cy={CY} r="5" fill="none" stroke="#12566B" strokeWidth="1.2"
            opacity="0"
            className={reduced ? undefined : 'ofr-core-ping'}
          />
        </g>

        {/* Keep the headline column fully legible. */}
        <rect width="1280" height="600" fill="url(#ofr-fade)" />
      </svg>
    </div>
  );
}
