'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

const NAV = [
  { href: '/radar/', label: 'Radar' },
  { href: '/frontier/', label: 'Frontier' },
  { href: '/themes/', label: 'Themes' },
  { href: '/deep-dive/', label: 'Deep Dive' },
  { href: '/methodology/', label: 'Methodology' },
];

export default function Nav() {
  const pathname = usePathname() ?? '/';
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-40 border-b transition-[background-color,border-color,box-shadow] duration-300 ${
        scrolled
          ? 'border-paper-line bg-paper/85 backdrop-blur-md shadow-[0_1px_0_rgba(11,22,34,.04)]'
          : 'border-transparent bg-paper/60 backdrop-blur-sm'
      }`}
    >
      <div className="wrap flex h-14 items-center justify-between gap-4">
        <Link href="/" className="group flex shrink-0 items-center gap-2.5">
          <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden className="text-sea">
            <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" strokeWidth="1.2" />
            <circle cx="12" cy="12" r="5.5" fill="none" stroke="currentColor" strokeWidth="1.2" opacity=".55" />
            <circle cx="15.5" cy="8.5" r="1.9" fill="currentColor" className="origin-center transition-transform duration-500 group-hover:scale-125" />
          </svg>
          <span className="text-[15px] font-semibold tracking-tight">Ocean Frontier Radar</span>
        </Link>
        <nav className="flex items-center gap-0.5 overflow-x-auto" aria-label="Primary">
          {NAV.map((n) => {
            const active = pathname.startsWith(n.href.replace(/\/$/, '')) && n.href !== '/';
            return (
              <Link
                key={n.href}
                href={n.href}
                data-active={active ? 'true' : 'false'}
                aria-current={active ? 'page' : undefined}
                className="nav-link whitespace-nowrap"
              >
                {n.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
