-- Ocean Frontier Radar — canonical schema (Phase 2)
-- Design rule: observed facts (sources, evidence) are structurally separate
-- from interpretation (analyst_views, prioritization). Scores never overwrite facts.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------- sources
CREATE TABLE IF NOT EXISTS sources (
    source_id        TEXT PRIMARY KEY,
    url              TEXT,
    title            TEXT,
    publisher        TEXT,
    source_type      TEXT NOT NULL,      -- federal_award, patent, university_news, procurement, publication, company_site, press_release
    source_quality   TEXT NOT NULL,      -- tier1 | tier2 | tier3
    publication_date TEXT,               -- ISO8601 or NULL. NULL means unknown, never guessed.
    accessed_at      TEXT NOT NULL,
    retrieval_method TEXT,               -- api | bulk_download | http_fetch | manual
    raw_ref          TEXT,               -- pointer to retained raw payload
    CHECK (source_quality IN ('tier1','tier2','tier3'))
);

-- ------------------------------------------------------------- candidates
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id     TEXT PRIMARY KEY,   -- deterministic slug
    name             TEXT NOT NULL,
    candidate_type   TEXT NOT NULL,      -- company | research_project | spinout | lab_program
    institution      TEXT,
    company          TEXT,
    geography        TEXT,
    website          TEXT,
    current_stage    TEXT,               -- pre_formation | pre_seed | seed | series_a | beyond
    company_formed   INTEGER,            -- 1 | 0 | NULL(unknown)
    ocean_centrality TEXT,               -- central_mechanism | primary_end_market | strong_adjacency | incidental
    sourcing_signal  TEXT,               -- obvious | emerging | pre_company | hidden_adjacency
    -- Phase 2.5: recency must describe the CANDIDATE, never our retrieval.
    -- Derived as MAX(evidence.evidence_date); never from source.accessed_at.
    candidate_latest_signal_date TEXT,
    queue            TEXT,               -- tier_a | tier_b | tier_c | frontier
    date_first_seen  TEXT NOT NULL,
    date_last_updated TEXT NOT NULL,
    CHECK (candidate_type IN ('company','research_project','spinout','lab_program')),
    CHECK (ocean_centrality IS NULL OR ocean_centrality IN
           ('central_mechanism','primary_end_market','strong_adjacency','incidental')),
    CHECK (sourcing_signal IS NULL OR sourcing_signal IN
           ('obvious','emerging','pre_company','hidden_adjacency')),
    CHECK (company_formed IS NULL OR company_formed IN (0,1)),
    CHECK (queue IS NULL OR queue IN ('tier_a','tier_b','tier_c','frontier'))
);

-- ----------------------------------------------------------------- people
CREATE TABLE IF NOT EXISTS people (
    person_id    TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    name         TEXT NOT NULL,
    role         TEXT,                   -- PI, founder, CEO, CTO
    role_type    TEXT,                   -- academic_pi | founder | academic_and_founder | operator
    affiliation  TEXT,
    source_id    TEXT REFERENCES sources(source_id)
);

-- --------------------------------------------------------------- evidence
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id      TEXT PRIMARY KEY,
    candidate_id     TEXT NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    source_id        TEXT NOT NULL REFERENCES sources(source_id),   -- no orphan evidence
    evidence_type    TEXT NOT NULL,
    observed_claim   TEXT NOT NULL,      -- what the source says, not what we think
    verbatim_quote   TEXT,
    evidence_date    TEXT,               -- when the event happened
    source_date      TEXT,               -- when the source was published
    quantitative_value REAL,
    unit             TEXT,
    extraction_method TEXT NOT NULL,     -- structured_field | human_read | ai_extracted
    confidence       TEXT,               -- high | medium | low
    analyst_notes    TEXT,
    CHECK (extraction_method IN ('structured_field','human_read','ai_extracted')),
    CHECK (confidence IS NULL OR confidence IN ('high','medium','low'))
);

-- --------------------------------------------------------- taxonomy_links
CREATE TABLE IF NOT EXISTS taxonomy_links (
    candidate_id  TEXT NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    category_id   TEXT NOT NULL,         -- taxonomy category key from thesis_lexicon.yaml
    is_primary    INTEGER NOT NULL DEFAULT 0,
    rationale     TEXT,
    PRIMARY KEY (candidate_id, category_id)
);

-- ---------------------------------------------------------- prioritization
-- Component-level only. There is deliberately no stored total; totals are
-- computed on read so a number can never be cited without its components.
CREATE TABLE IF NOT EXISTS prioritization (
    candidate_id   TEXT NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    dimension      TEXT NOT NULL,        -- technical_evidence | commercialization_signal | timing | venture_potential | propeller_relevance | differentiated_sourcing
    points         INTEGER NOT NULL,
    max_points     INTEGER NOT NULL,
    rationale      TEXT NOT NULL,
    evidence_ids   TEXT,                 -- comma-separated evidence_id list
    analyst_override INTEGER NOT NULL DEFAULT 0,
    override_reason TEXT,
    scored_at      TEXT NOT NULL,
    PRIMARY KEY (candidate_id, dimension),
    CHECK (points >= 0 AND points <= max_points),
    CHECK (analyst_override IN (0,1)),
    CHECK (analyst_override = 0 OR override_reason IS NOT NULL)
);

-- ------------------------------------------------------------- flags
CREATE TABLE IF NOT EXISTS flags (
    candidate_id TEXT NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    flag         TEXT NOT NULL,
    rationale    TEXT,
    PRIMARY KEY (candidate_id, flag)
);

-- ---------------------------------------------------------- analyst_views
-- Interpretation. Structurally separate from `evidence`.
CREATE TABLE IF NOT EXISTS analyst_views (
    view_id      TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    view_type    TEXT NOT NULL,          -- observed | inferred | unknown | what_must_be_true | technical_kill_question | commercial_kill_question
    statement    TEXT NOT NULL,
    evidence_ids TEXT,                   -- required when view_type = 'observed'
    author       TEXT NOT NULL,          -- analyst | ai_assisted
    created_at   TEXT NOT NULL,
    CHECK (view_type IN ('observed','inferred','unknown','what_must_be_true',
                         'technical_kill_question','commercial_kill_question')),
    CHECK (author IN ('analyst','ai_assisted')),
    CHECK (view_type <> 'observed' OR (evidence_ids IS NOT NULL AND evidence_ids <> ''))
);

-- ------------------------------------------------- classification (AI-assisted)
-- Kept apart from `evidence` so machine judgement is never mistaken for fact.
CREATE TABLE IF NOT EXISTS classifications (
    classification_id TEXT PRIMARY KEY,
    record_key      TEXT NOT NULL,       -- retrieval record this refers to
    candidate_id    TEXT REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    category_id     TEXT,
    ocean_centrality TEXT,
    relevance       TEXT,                -- relevant | borderline | not_relevant
    rationale       TEXT,
    classifier      TEXT NOT NULL,       -- rules_v1 | ai_assisted | analyst
    source_text     TEXT,                -- the text the decision was made on
    created_at      TEXT NOT NULL,
    CHECK (relevance IN ('relevant','borderline','not_relevant'))
);

-- ----------------------------------------------- possible entity relationships
-- Conservative entity resolution: when unsure we record a link, never a merge.
CREATE TABLE IF NOT EXISTS possible_relationships (
    candidate_id_a TEXT NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    candidate_id_b TEXT NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    relationship   TEXT NOT NULL,        -- possible_same_entity | spinout_of | shares_person | shares_institution
    basis          TEXT NOT NULL,        -- explainable reason; never "semantic similarity"
    confidence     TEXT NOT NULL,
    PRIMARY KEY (candidate_id_a, candidate_id_b, relationship),
    CHECK (confidence IN ('high','medium','low'))
);

-- ------------------------------------------------------------ merge audit
CREATE TABLE IF NOT EXISTS merge_log (
    merge_id       TEXT PRIMARY KEY,
    kept_id        TEXT NOT NULL,
    merged_id      TEXT NOT NULL,
    basis          TEXT NOT NULL,        -- explicit, explainable evidence for the merge
    merged_at      TEXT NOT NULL
);

-- ------------------------------------------------------ procurement evidence
-- Demand-side: proves a budget line exists. Never used as TAM.
CREATE TABLE IF NOT EXISTS procurement (
    procurement_id  TEXT PRIMARY KEY,
    theme           TEXT NOT NULL,       -- taxonomy category or problem area
    award_id        TEXT,
    recipient       TEXT,
    awarding_agency TEXT,
    awarding_sub_agency TEXT,
    amount          REAL,
    start_date      TEXT,
    description     TEXT,
    source_id       TEXT NOT NULL REFERENCES sources(source_id)
);

-- ------------------------------------------------------------- ingest log
CREATE TABLE IF NOT EXISTS ingest_log (
    run_id       TEXT NOT NULL,
    module       TEXT NOT NULL,
    started_at   TEXT NOT NULL,
    finished_at  TEXT,
    records_seen INTEGER,
    records_kept INTEGER,
    status       TEXT,                   -- ok | error
    message      TEXT
);

CREATE INDEX IF NOT EXISTS idx_evidence_candidate ON evidence(candidate_id);
CREATE INDEX IF NOT EXISTS idx_evidence_type      ON evidence(evidence_type);
CREATE INDEX IF NOT EXISTS idx_tax_category       ON taxonomy_links(category_id);
CREATE INDEX IF NOT EXISTS idx_prior_dim          ON prioritization(dimension);
CREATE INDEX IF NOT EXISTS idx_proc_theme         ON procurement(theme);
