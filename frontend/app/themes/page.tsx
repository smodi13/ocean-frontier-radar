import Link from 'next/link';
import { Callout, Chip, PageHeader, Section } from '@/components/Primitives';
import { Reveal } from '@/components/motion/Reveal';
import { Counter } from '@/components/motion/Counter';
import { themes } from '@/lib/data';

export const metadata = { title: 'Themes · Ocean Frontier Radar' };

export default function ThemesPage() {
  return (
    <>
      <PageHeader
        eyebrow="Taxonomy"
        title="Themes"
        lede={
          <>
            Eight categories derived from the investor’s publicly stated themes, then split into
            units that map onto a searchable technical vocabulary. Counts are computed from the
            candidate database, not written by hand.
          </>
        }
      />

      <Section>
        <Callout tone="sea" title="Why the taxonomy carries a second axis">
          Each candidate also gets an <strong>ocean-centrality</strong> tag — is the ocean the
          mechanism, the operating environment, the customer’s context, or merely incidental? That
          axis is what admits a corrosion-resistant rebar company and excludes a generic AI tool
          with one shipping logo.
        </Callout>
      </Section>

      <div className="wrap space-y-4 pb-16">
        {themes.map((t) => (
          <Reveal key={t.id}>
          <section id={t.id} className="card scroll-mt-20 p-6 sm:p-8">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <h2 className="h2 text-[22px]">{t.label}</h2>
              <div className="flex gap-1.5">
                <Chip tone="sea"><Counter value={t.candidateCount} /> candidates</Chip>
                {t.frontierCount > 0 && <Chip><Counter value={t.frontierCount} /> pre-company</Chip>}
              </div>
            </div>

            <p className="body mt-4 max-w-prose">{t.problem}</p>

            {t.note && (
              <div className="mt-4 rounded-md border-l-[3px] border-l-rust bg-rust-pale/40 px-4 py-3">
                <p className="body text-[14px]">{t.note}</p>
              </div>
            )}

            <div className="mt-6 grid gap-6 lg:grid-cols-3">
              <div>
                <h3 className="h3 mb-2 text-[14px]">Technologies</h3>
                <ul className="meta space-y-1">{t.technologies.map((x) => <li key={x}>{x}</li>)}</ul>
              </div>
              <div>
                <h3 className="h3 mb-2 text-[14px]">Technical bottlenecks</h3>
                <ul className="meta space-y-1">{t.technicalBottlenecks.map((x) => <li key={x}>{x}</li>)}</ul>
              </div>
              <div>
                <h3 className="h3 mb-2 text-[14px]">Commercial bottlenecks</h3>
                <ul className="meta space-y-1">{t.commercialBottlenecks.map((x) => <li key={x}>{x}</li>)}</ul>
              </div>
            </div>

            {t.examples.length > 0 && (
              <div className="mt-6">
                <h3 className="h3 mb-2 text-[14px]">Emerging signals in this theme</h3>
                <ul className="flex flex-wrap gap-2">
                  {t.examples.map((e) => (
                    <li key={e.id}>
                      <Link
                        href={`/radar/${e.id}/`}
                        className="card-interactive block rounded-lg border border-paper-line bg-paper-card px-3 py-2 text-[13px]"
                      >
                        <span className="font-medium">{e.name}</span>
                        {e.institution && <span className="text-ink/50"> · {e.institution}</span>}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {t.propellerAdjacency.length > 0 && (
              <div className="mt-6 border-t border-paper-line pt-4">
                <h3 className="h3 mb-2 text-[14px]">Publicly disclosed portfolio adjacency</h3>
                <p className="meta mb-2 max-w-prose">
                  From the investor’s public portfolio page. Listed as context for where the theme
                  already has exposure — not as a competitive assessment.
                </p>
                <ul className="meta space-y-1">
                  {t.propellerAdjacency.map((a) => (
                    <li key={a.company}><span className="font-medium text-ink/70">{a.company}</span> — {a.note}</li>
                  ))}
                </ul>
              </div>
            )}
          </section>
          </Reveal>
        ))}
      </div>
    </>
  );
}
