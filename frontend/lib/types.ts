export type Queue = 'tier_a' | 'tier_b' | 'tier_c' | 'frontier';
export type Centrality = 'central_mechanism' | 'primary_end_market' | 'strong_adjacency' | 'incidental';

export interface EvidenceSource {
  url: string | null; title: string | null; publisher: string | null;
  type: string | null; quality: string | null; accessed_at: string | null;
}
export interface Evidence {
  evidence_id: string; type: string; observed_claim: string;
  evidence_date: string | null; value: number | null; unit: string | null;
  extraction_method: string; confidence: string | null; source: EvidenceSource;
}
export interface CandidateRow {
  id: string; name: string; type: string; queue: Queue | null;
  institution: string | null; company: string | null; geography: string | null;
  category: string | null; categories: string[];
  centrality: Centrality | null; sourcingSignal: string | null;
  stage: string | null; companyFormed: number | null;
  latestSignal: string | null; evidenceCount: number;
  priority: number | null; priorityMax: number | null;
  flags: string[]; whySurfaced: string[];
  strongestEvidence: string | null; strongestEvidenceType: string | null;
}
export interface CandidateDetail extends CandidateRow {
  website: string | null;
  people: { name: string; role: string | null; role_type: string | null; affiliation: string | null }[];
  components: Record<string, { points: number; max: number; rationale: string }>;
  flagDetail: { flag: string; rationale: string | null }[];
  observed: string[]; inferred: string[]; unknown: string[];
  mustBeTrue: string[]; technicalKill: string[]; commercialKill: string[];
  evidence: Evidence[];
}
export interface Summary {
  recordsEvaluated: number; candidates: number; actionableUniverse: number;
  tierA: number; tierB: number; tierC: number; frontier: number;
  preCompanyShareOfActionable: number; institutions: number; categories: number;
  categoryCounts: Record<string, number>; candidatesWithEvidence: number;
  procurementContracts: number; procurementObserved: number; themes: number;
  generatedAt: string;
}
export interface Theme {
  id: string; label: string; problem: string; technologies: string[];
  technicalBottlenecks: string[]; commercialBottlenecks: string[];
  propellerAdjacency: { company: string; note: string }[];
  note: string | null; candidateCount: number; frontierCount: number;
  examples: { id: string; name: string; queue: string | null; institution: string | null }[];
}
export interface FrontierSignal {
  id: string; name: string; institution: string | null; signalType: string | null;
  signalDate: string | null; category: string | null; geography: string | null;
  centrality: string | null;
  components: Record<string, { points: number; max: number; why: string }>;
  priority: number; priorityMax: number; evidence: Evidence[];
}
export interface EvidenceClaim {
  id: string; claim: string; status: 'observed' | 'inferred' | 'unknown';
  source: string; sourceType: string; tier: string; sourceDate: string | null;
  accessed: string; confidence: string; section: string; contradictory: string | null;
}
