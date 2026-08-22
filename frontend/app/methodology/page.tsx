import { Callout, PageHeader, Section, Stat } from '@/components/Primitives';
import { fmtNum, summary } from '@/lib/data';

export const metadata = { title: 'Methodology · Ocean Frontier Radar' };

const TIERS = [
  ['1', 'Government and patent records', 'Federal award and procurement records, granted patents and published applications. Highest weight; used for every material financial fact.'],
  ['2', 'Company and institution primary sources', 'Company websites, university press releases, technology-transfer announcements.'],
  ['3', 'Technical papers', 'Peer-reviewed and conference publications.'],
  ['4', 'Credible secondary reporting', 'Trade press with named authors and dates.'],
  ['5', 'Secondary databases', 'Aggregators. Discovery only — never used to establish a material financial fact.'],
];

const TESTS = [
  ['Recall canaries', 'Twelve fixtures spanning every thesis pattern check that known-relevant examples still survive retrieval and classification. They exist because two candidates were once silently lost — one to a missing plural form, one to a threshold. Both failures were invisible from the output.'],
  ['Reporting completeness', 'For every high-priority candidate the review layer must account for its most recent, largest, strongest technical and strongest commercial evidence. Generation fails rather than quietly omitting something. This exists because an earlier report dropped a $2M award that was already in the database.'],
  ['Evidence traceability', 'A statement stored as “observed” must cite a real evidence record. The database rejects it otherwise.'],
  ['Procurement reconciliation', 'Bucket totals, exclusions and annualised figures are recomputed from the audit script and checked against the figures shown here.'],
  ['Model validation', 'The scenario workbook is asserted to contain live formulas and no hardcoded outputs, and its base case is recomputed independently in Python.'],
  ['Deterministic exports', 'Re-running the export produces byte-identical data, so a change in the site implies a change in the research.'],
  ['Entity resolution', 'Records merge only on identical normalised names, shared domains or shared award identifiers. Similarity alone never merges anything; uncertain links are recorded for review.'],
];

export default function MethodologyPage() {
  return (
    <>
      <PageHeader
        eyebrow="How this works"
        title="Methodology"
        lede="The system is built to be auditable. Every number on this site is generated from committed research artifacts, and the failure modes are documented alongside the results."
      />

      <Section title="Source hierarchy">
        <ol className="space-y-2">
          {TIERS.map(([n, name, desc]) => (
            <li key={n} className="card flex gap-4 p-4">
              <span className="mono text-sea">{n}</span>
              <div>
                <div className="text-[14px] font-semibold">{name}</div>
                <p className="meta mt-1">{desc}</p>
              </div>
            </li>
          ))}
        </ol>
      </Section>

      <Section title="Evidence discipline" className="pt-0">
        <p className="body max-w-prose">
          The project keeps three things structurally separate, in the database schema rather than
          by convention.
        </p>
        <div className="mt-5 space-y-3">
          <div className="epi epi-observed">
            <p className="text-[12px] font-semibold uppercase tracking-wider">Observed</p>
            <p className="body mt-1 text-[14px]">
              Directly supported by a cited public source. Cannot be stored without an evidence
              reference.
            </p>
          </div>
          <div className="epi epi-inferred">
            <p className="text-[12px] font-semibold uppercase tracking-wider">Inferred</p>
            <p className="body mt-1 text-[14px]">
              The analyst’s interpretation of evidence. Never presented as fact, and stored in a
              different table from evidence.
            </p>
          </div>
          <div className="epi epi-unknown">
            <p className="text-[12px] font-semibold uppercase tracking-wider">Unknown</p>
            <p className="body mt-1 text-[14px]">
              Identified gaps requiring primary research. Naming them is part of the work, not an
              omission from it.
            </p>
          </div>
        </div>
      </Section>

      <Section title="Retrieval by problem, not by sector" className="pt-0">
        <p className="body max-w-prose">
          The strongest candidates often never describe themselves as ocean companies. Retrieval is
          therefore organised around technical problems — corrosion, biofouling, underwater
          acoustics, subsea power — with a flag on each concept group indicating whether marine
          vocabulary is required at all. Where the underlying problem is inherently marine-relevant,
          a record is retrieved with no ocean vocabulary present.
        </p>
        <p className="body mt-3 max-w-prose">
          Each candidate then carries an <strong>ocean-centrality</strong> tag — mechanism, primary
          end market, strong adjacency or incidental — which guards both failure modes: missing the
          landlocked corrosion lab, and forcing a generic software company into an ocean thesis.
        </p>
      </Section>

      <Section title="Prioritization" className="pt-0">
        <Callout tone="sea" title="Research priority, not investment probability">
          Scores organise evidence and allocate analyst attention. They do not estimate whether
          anyone should invest. Every point cites the evidence that earned it, no total is stored in
          the database, and ordering within the top tier is explicitly analyst judgment rather than
          machine rank — because with integer components and a small range, the system cannot
          honestly separate the middle of the distribution.
        </Callout>
        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <Stat value={fmtNum(summary.tierA)} label="Tier A — diligence now" />
          <Stat value={fmtNum(summary.tierB)} label="Tier B — research queue" />
          <Stat value={fmtNum(summary.tierC)} label="Tier C — watch" />
          <Stat value={fmtNum(summary.frontier)} label="Frontier — pre-company" />
        </div>
      </Section>

      <Section title="Validation" className="pt-0">
        <p className="body max-w-prose">
          The research pipeline is covered by an automated test suite that runs without network
          access. Several tests exist specifically because something broke and the suite caught it.
        </p>
        <ul className="mt-5 space-y-2">
          {TESTS.map(([name, desc]) => (
            <li key={name} className="card p-4">
              <div className="text-[14px] font-semibold">{name}</div>
              <p className="meta mt-1">{desc}</p>
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Limitations" className="pt-0">
        <ul className="body max-w-prose list-disc space-y-2 pl-5">
          <li>Public data only. No proprietary company financials were accessed.</li>
          <li>No founder, customer or expert calls were conducted. Nothing on this site is based on a conversation.</li>
          <li>No access to any investor’s pipeline or internal views, and no claim is made about them.</li>
          <li>Federal procurement is an imperfect proxy for total commercial opportunity. It excludes classified programmes, allied and foreign buyers, and all commercial spending.</li>
          <li>Patent research here is technical and commercial reading of public records. It is not a legal opinion and not a freedom-to-operate assessment.</li>
          <li>Sourcing coverage depends on accessible public sources. Some sources returned access errors and were substituted or documented rather than worked around.</li>
          <li>Absence of public evidence is not evidence that something does not exist.</li>
          <li>Prioritization reflects outside-in analyst judgment and would differ between analysts.</li>
        </ul>
      </Section>

      <Section title="About and disclosure" className="pt-0">
        <div className="card max-w-prose p-6">
          <p className="body">
            This is an independent outside-in research project. It is not affiliated with Propeller,
            and not affiliated with any company researched. It uses public information only and is
            not investment advice.
          </p>
          <h3 className="h3 mt-5 mb-2 text-[14px]">AI disclosure</h3>
          <p className="body">
            AI tools were used to assist with software development, structured extraction and
            research workflows. Material claims were retained with source traceability and
            analyst-reviewed before inclusion. AI did not independently make investment decisions,
            and machine-generated classification is stored separately from source evidence so the
            two can never be confused.
          </p>
          <p className="meta mt-4">
            Data generated {summary.generatedAt.slice(0, 10)} from committed research outputs.
          </p>
        </div>
      </Section>
    </>
  );
}
