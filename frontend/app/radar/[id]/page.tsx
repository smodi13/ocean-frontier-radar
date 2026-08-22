import { notFound } from 'next/navigation';
import { BackLink, Chip, Epistemic, PageHeader, Section } from '@/components/Primitives';
import { EvidenceList } from '@/components/Evidence';
import {
  CATEGORY_LABEL, CENTRALITY_LABEL, QUEUE_LABEL, detailIds, getCandidate,
} from '@/lib/data';

export function generateStaticParams() {
  return detailIds().map((id) => ({ id }));
}

// Next 16: `params` is a Promise in async server components and must be awaited.
export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const c = getCandidate(id);
  return { title: c ? `${c.name} · Ocean Frontier Radar` : 'Candidate · Ocean Frontier Radar' };
}

const DIM_LABEL: Record<string, string> = {
  technical_evidence: 'Technical evidence',
  commercialization_signal: 'Commercialization signal',
  timing: 'Timing',
  venture_potential: 'Venture potential',
  propeller_relevance: 'Propeller relevance',
  differentiated_sourcing: 'Differentiated sourcing',
};

export default async function CandidatePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const c = getCandidate(id);
  if (!c) notFound();

  const techEvidence = c.evidence.filter((e) =>
    /patent|publication|prototype|field_trial|independent_validation|technical|license/.test(e.type),
  );
  const commEvidence = c.evidence.filter((e) =>
    /sbir|sttr|grant|financing|customer|pilot|partnership|procurement|accelerator|spinout|incorporat/.test(e.type),
  );

  return (
    <>
      <PageHeader
        eyebrow={c.queue ? QUEUE_LABEL[c.queue] : 'Candidate'}
        title={c.name}
        lede={[c.institution, c.geography].filter(Boolean).join(' · ') || undefined}
      >
        <div className="flex flex-wrap gap-1.5">
          {c.category && <Chip tone="sea">{CATEGORY_LABEL[c.category] ?? c.category}</Chip>}
          {c.centrality && <Chip>{CENTRALITY_LABEL[c.centrality]}</Chip>}
          {c.companyFormed !== 1 && <Chip tone="sea">Pre-company</Chip>}
          {c.stage && <Chip>{c.stage.replace(/_/g, ' ')}</Chip>}
          {c.latestSignal && <Chip>Latest signal {c.latestSignal}</Chip>}
          {c.flags.map((f) => <Chip key={f} tone="rust">{f.replace(/_/g, ' ').toLowerCase()}</Chip>)}
        </div>
        <div className="mt-6"><BackLink href="/radar/" label="Back to radar" /></div>
      </PageHeader>

      <Section title="What it is">
        <p className="body max-w-prose">
          {c.strongestEvidence ??
            'No summary claim is attached to this candidate beyond its evidence records below.'}
        </p>
        {c.website && (
          <p className="meta mt-3">
            <a href={c.website} target="_blank" rel="noopener noreferrer" className="link">{c.website}</a>
          </p>
        )}
        {c.people.length > 0 && (
          <div className="mt-6">
            <h3 className="h3 mb-2">People named in public records</h3>
            <ul className="flex flex-wrap gap-2">
              {c.people.map((p, i) => (
                <li key={i} className="card px-3 py-2 text-[13px]">
                  <span className="font-medium">{p.name}</span>
                  {p.role && <span className="text-ink/55"> · {p.role}</span>}
                </li>
              ))}
            </ul>
          </div>
        )}
      </Section>

      <Section title="Why it surfaced" className="pt-0">
        <p className="body max-w-prose">
          Retrieved from {c.whySurfaced.length ? c.whySurfaced.join(', ') : 'federal award records'}.
          Classified into <strong>{c.category ? CATEGORY_LABEL[c.category] ?? c.category : 'an unassigned category'}</strong>
          {c.centrality && <> with ocean centrality <strong>{CENTRALITY_LABEL[c.centrality].toLowerCase()}</strong></>}.
        </p>
        {Object.keys(c.components).length > 0 && (
          <div className="mt-5">
            <h3 className="h3 mb-1">Diagnostic priority components</h3>
            <p className="meta mb-3 max-w-prose">
              These organise evidence and allocate analyst attention. They are not an investment
              score and not a probability.
            </p>
            <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
              {Object.entries(c.components).map(([dim, v]) => (
                <div key={dim} className="card p-3">
                  <div className="flex items-baseline justify-between gap-2">
                    <span className="text-[13px] font-medium">{DIM_LABEL[dim] ?? dim}</span>
                    <span className="mono text-sea">{v.points}/{v.max}</span>
                  </div>
                  <p className="meta mt-1.5">{v.rationale}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </Section>

      {(c.observed.length > 0 || c.inferred.length > 0 || c.unknown.length > 0) && (
        <Section title="Observed, inferred, unknown" className="pt-0">
          <p className="meta mb-4 max-w-prose">
            The project keeps source-supported facts structurally separate from analyst
            interpretation and from open questions. The database enforces it: an “observed”
            statement cannot be stored without citing an evidence record.
          </p>
          <div className="space-y-3">
            <Epistemic kind="observed" items={c.observed} />
            <Epistemic kind="inferred" items={c.inferred} />
            <Epistemic kind="unknown" items={c.unknown} />
          </div>
        </Section>
      )}

      {(c.technicalKill.length > 0 || c.commercialKill.length > 0 || c.mustBeTrue.length > 0) && (
        <Section title="Diligence questions" className="pt-0">
          <div className="grid gap-3 lg:grid-cols-3">
            {c.mustBeTrue.length > 0 && (
              <div className="card p-4">
                <h3 className="h3 mb-2 text-[14px]">What must be true</h3>
                <ul className="space-y-2">{c.mustBeTrue.map((t, i) => <li key={i} className="body text-[13.5px]">{t}</li>)}</ul>
              </div>
            )}
            {c.technicalKill.length > 0 && (
              <div className="card p-4">
                <h3 className="h3 mb-2 text-[14px]">Biggest technical question</h3>
                <ul className="space-y-2">{c.technicalKill.map((t, i) => <li key={i} className="body text-[13.5px]">{t}</li>)}</ul>
              </div>
            )}
            {c.commercialKill.length > 0 && (
              <div className="card p-4">
                <h3 className="h3 mb-2 text-[14px]">Biggest commercial question</h3>
                <ul className="space-y-2">{c.commercialKill.map((t, i) => <li key={i} className="body text-[13.5px]">{t}</li>)}</ul>
              </div>
            )}
          </div>
        </Section>
      )}

      <Section title="Technical evidence" className="pt-0">
        <EvidenceList evidence={techEvidence} />
      </Section>

      <Section title="Commercialization evidence" className="pt-0">
        <EvidenceList evidence={commEvidence} />
      </Section>

      <Section title={`All sources (${c.evidence.length})`} className="pt-0">
        <p className="meta mb-4 max-w-prose">
          Every record retains its source, publisher, publication date where available, and the date
          it was accessed. Sources are linked directly rather than hidden behind a summary.
        </p>
        <EvidenceList evidence={c.evidence} />
      </Section>
    </>
  );
}
