/** Site-level constants. The repository URL is filled in once the repo exists. */
export const REPO_URL = 'https://github.com/smodi13/ocean-frontier-radar';

export const AI_DISCLOSURE = [
  'This project was built with substantial AI assistance. Claude Code was used throughout: writing the ingestion, classification, entity-resolution and scoring code; building the export pipeline and this interface; debugging; organising research across phases; performing structured extraction and classification of award abstracts; and drafting and synthesising written analysis.',
  'What that does and does not mean for the claims on this site:',
] as const;

export const AI_DISCLOSURE_POINTS = [
  'Factual claims remain tied to their underlying public sources. Every evidence record keeps its source, publisher, publication date where available, and the date it was accessed, and those links are exposed directly in the interface rather than summarised away.',
  'AI-generated classification is stored separately from observed evidence. Category and ocean-centrality assignments live in their own table with the classifier named, so machine judgement is never mixed into the evidence record it was derived from.',
  'Investment interpretations are presented as analyst views, not source facts. The Observed / Inferred / Unknown split is enforced by the database schema: a statement stored as "observed" must cite a real evidence record, and interpretation is stored elsewhere.',
  'The system does not treat AI output as primary evidence. No conclusion on this site rests on a model assertion; where AI extracted a claim, the record is marked and the source is shown alongside it.',
  'AI did not independently make investment decisions. The recommendation, the tier assignments and the selection of which debates matter are analyst judgements.',
] as const;

export const AI_DISCLOSURE_CAVEAT =
  'Not every one of the 579 retrieved records has been individually read by a human. Tier A and Frontier records were reviewed; Tier B and Tier C are machine-classified and are labelled as such in the interface. The ARMADA diligence case was assembled claim by claim against primary sources.';

export const INDEPENDENCE_DISCLAIMER =
  'Ocean Frontier Radar is an independent research project and is not affiliated with, sponsored by, or endorsed by Propeller, ARMADA Marine Robotics, Woods Hole Oceanographic Institution, or any other company or institution referenced in the analysis. It is built entirely from public information and is not investment advice.';
