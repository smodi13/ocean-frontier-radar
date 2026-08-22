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
      <Section>
        <RadarBrowser rows={candidates} detailIds={detailIds()} />
      </Section>
    </>
  );
}
