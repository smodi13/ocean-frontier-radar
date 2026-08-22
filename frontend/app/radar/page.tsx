import RadarBrowser from '@/components/RadarBrowser';
import { PageHeader, Section } from '@/components/Primitives';
import { candidates, detailIds, fmtNum, summary } from '@/lib/data';

export const metadata = { title: 'Radar · Ocean Frontier Radar' };

export default function RadarPage() {
  return (
    <>
      <PageHeader
        eyebrow="Sourcing"
        title="Radar"
        lede={
          <>
            The full retrieved universe: {fmtNum(summary.candidates)} candidates drawn from federal
            award records, university licensing announcements and research-translation programs.
            Retrieval is organised by technical problem, so records that never use ocean vocabulary
            still surface.
          </>
        }
      />
      <Section reveal={false}>
        <div className="mb-6 rounded-md border-l-[3px] border-l-sea bg-sea-pale/40 px-5 py-4">
          <p className="body text-[14px]">
            <strong>Two kinds of row.</strong> Records that have been through analyst review open an
            evidence detail page. Tier B (<em>research queue</em>) and Tier C (<em>watch</em>) records
            are shown with a dashed border and do not link anywhere — they have been surfaced and
            classified, but no diligence has been done on them. Nothing here creates the appearance
            of analysis that does not exist.
          </p>
        </div>
        <RadarBrowser rows={candidates} detailIds={detailIds()} />
      </Section>
    </>
  );
}
