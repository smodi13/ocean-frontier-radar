/**
 * Client-safe label maps and formatters.
 *
 * IMPORTANT: this module must never import the generated JSON. `lib/data.ts`
 * imports candidateDetail.json (~3.2MB), and any client component that reaches
 * `lib/data` drags that file into the browser bundle. Client components import
 * from here instead.
 */
export const CATEGORY_LABEL: Record<string, string> = {
  maritime_autonomy: 'Maritime Autonomy & Robotics',
  ocean_sensing: 'Ocean Sensing, Data & Intelligence',
  offshore_energy: 'Offshore Energy, Power & Subsea Infrastructure',
  marine_carbon: 'Marine Carbon & Ocean Chemistry',
  marine_materials: 'Marine Materials, Corrosion & Coastal Infrastructure',
  coastal_adaptation: 'Coastal Adaptation & Climate Risk',
  blue_food: 'Blue Food, Aquaculture & Marine Biology',
  maritime_software: 'Industrial & Maritime Software / Applied AI',
};

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
