import summaryJson from '@/data/summary.json';
import candidatesJson from '@/data/candidates.json';
import themesJson from '@/data/themes.json';
import frontierJson from '@/data/frontier.json';
import armadaJson from '@/data/armada.json';
import registerJson from '@/data/evidenceRegister.json';
import detailJson from '@/data/candidateDetail.json';
import type { CandidateDetail, CandidateRow, EvidenceClaim, FrontierSignal, Summary, Theme } from './types';

export const summary = summaryJson as Summary;
export const candidates = candidatesJson as CandidateRow[];
export const themes = themesJson as Theme[];
export const frontier = frontierJson as {
  signals: FrontierSignal[];
  byType: Record<string, number>;
  byCategory: Record<string, number>;
  byInstitution: Record<string, number>;
  note: string;
};
/* eslint-disable @typescript-eslint/no-explicit-any */
export const armada = armadaJson as any;
export const evidenceRegister = registerJson as EvidenceClaim[];
const details = detailJson as unknown as Record<string, CandidateDetail>;

export function getCandidate(id: string): CandidateDetail | undefined {
  return details[id];
}
/** Candidates that get their own statically generated page. */
export function detailIds(): string[] {
  return candidates.filter((c) => c.queue === 'tier_a' || c.queue === 'frontier').map((c) => c.id);
}

// Label maps and formatters live in lib/labels.ts so client components can
// import them without pulling candidateDetail.json into the browser bundle.
export {
  CATEGORY_LABEL, CENTRALITY_LABEL, QUEUE_LABEL, SIGNAL_LABEL,
  evidenceTypeLabel, fmtMoney, fmtNum,
} from './labels';
