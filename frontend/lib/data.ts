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

export const CATEGORY_LABEL: Record<string, string> = Object.fromEntries(
  themes.map((t) => [t.id, t.label]),
);
export const QUEUE_LABEL: Record<string, string> = {
  tier_a: 'Tier A — Diligence now',
  tier_b: 'Tier B — Research queue',
  tier_c: 'Tier C — Watch',
  frontier: 'Frontier — Pre-company',
};
export const CENTRALITY_LABEL: Record<string, string> = {
  central_mechanism: 'Central — mechanism',
  primary_end_market: 'Primary end market',
  strong_adjacency: 'Strong adjacency',
  incidental: 'Incidental',
};
export const SIGNAL_LABEL: Record<string, string> = {
  icorps: 'NSF I-Corps',
  commercialization_grant: 'Commercialization grant',
  exclusive_license: 'Exclusive licence',
  license_executed: 'Licence executed',
  spinout_announced: 'Spinout announced',
  accelerator_participation: 'Accelerator',
  research_grant: 'Research grant',
};

export function fmtMoney(n: number | null | undefined): string {
  if (n === null || n === undefined) return '—';
  if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toLocaleString()}`;
}
export function fmtNum(n: number): string {
  return n.toLocaleString();
}
export function evidenceTypeLabel(t: string): string {
  return t.replace(/_/g, ' ').replace(/\b\w/g, (m) => m.toUpperCase());
}
