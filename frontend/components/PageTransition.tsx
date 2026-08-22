'use client';

import { usePathname } from 'next/navigation';

/**
 * Keys the page content by route so a navigation remounts it and replays the
 * short entrance. Deliberately a 260ms opacity/translate settle and nothing
 * more: a route change in a research tool should feel like a page arriving,
 * not like a slide deck advancing. Reduced motion zeroes it in globals.css.
 */
export default function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <main key={pathname} className="ofr-page">
      {children}
    </main>
  );
}
