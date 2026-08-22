import type { Metadata } from 'next';
import Link from 'next/link';
import Nav from '@/components/Nav';
import PageTransition from '@/components/PageTransition';
import { INDEPENDENCE_DISCLAIMER, REPO_URL } from '@/lib/site';
import './globals.css';

export const metadata: Metadata = {
  title: 'Ocean Frontier Radar',
  description:
    'A research-to-venture sourcing system for finding emerging technologies at the ocean’s edge and turning public signals into an actionable diligence queue.',
};


export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Nav />

        <PageTransition>{children}</PageTransition>

        <footer className="mt-20 border-t border-paper-line bg-white">
          <div className="wrap py-10">
            <p className="meta max-w-prose">{INDEPENDENCE_DISCLAIMER}</p>
            <p className="meta mt-3 flex flex-wrap items-center gap-x-4 gap-y-1">
              <Link href="/methodology/" className="link">
                Methodology, limitations and AI disclosure
              </Link>
              <a href={REPO_URL} target="_blank" rel="noopener noreferrer" className="link">
                Source code on GitHub
              </a>
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
