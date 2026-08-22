import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'Ocean Frontier Radar',
  description:
    'A research-to-venture sourcing system for finding emerging technologies at the ocean’s edge and turning public signals into an actionable diligence queue.',
};

const NAV = [
  { href: '/radar/', label: 'Radar' },
  { href: '/frontier/', label: 'Frontier' },
  { href: '/themes/', label: 'Themes' },
  { href: '/deep-dive/', label: 'Deep Dive' },
  { href: '/methodology/', label: 'Methodology' },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="sticky top-0 z-40 border-b border-paper-line bg-paper/90 backdrop-blur">
          <div className="wrap flex h-14 items-center justify-between gap-4">
            <Link href="/" className="flex items-center gap-2.5 shrink-0">
              <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden className="text-sea">
                <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" strokeWidth="1.2" />
                <circle cx="12" cy="12" r="5.5" fill="none" stroke="currentColor" strokeWidth="1.2" opacity=".55" />
                <circle cx="15.5" cy="8.5" r="1.9" fill="currentColor" />
              </svg>
              <span className="text-[15px] font-semibold tracking-tight">Ocean Frontier Radar</span>
            </Link>
            <nav className="flex items-center gap-1 overflow-x-auto">
              {NAV.map((n) => (
                <Link
                  key={n.href}
                  href={n.href}
                  className="whitespace-nowrap rounded px-2.5 py-1.5 text-[13px] font-medium text-ink/70 hover:bg-sea-pale hover:text-sea-deep"
                >
                  {n.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>

        <main>{children}</main>

        <footer className="mt-20 border-t border-paper-line bg-white">
          <div className="wrap py-10">
            <p className="meta max-w-prose">
              Independent outside-in research project. Not affiliated with Propeller or with any
              company researched. Built entirely from public information. Not investment advice.
            </p>
            <p className="meta mt-3">
              <Link href="/methodology/" className="link">Methodology, limitations and AI disclosure</Link>
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
