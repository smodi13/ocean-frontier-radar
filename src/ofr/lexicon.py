"""Thesis lexicon loading and two-stage retrieval/classification matching.

Stage A (retrieval) favours recall: a record is retrieved if it hits enough
lexicon terms. Stage B (classification) decides relevance and ocean centrality
using evidence from the matched text, and records *why*.

Nothing here is an LLM. This is a deterministic, auditable rules classifier
(`rules_v1`). AI-assisted classification, if added, writes to the same
`classifications` table with classifier='ai_assisted' and never overwrites
these rows.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
LEXICON_PATH = ROOT / "config" / "thesis_lexicon.yaml"

# Ocean-centrality vocabulary (Phase 2, Step 7)
CENTRAL_MECHANISM = "central_mechanism"
PRIMARY_END_MARKET = "primary_end_market"
STRONG_ADJACENCY = "strong_adjacency"
INCIDENTAL = "incidental"
CENTRALITY_VALUES = (CENTRAL_MECHANISM, PRIMARY_END_MARKET, STRONG_ADJACENCY, INCIDENTAL)

RELEVANCE_VALUES = ("relevant", "borderline", "not_relevant")


@lru_cache(maxsize=1)
def load_lexicon(path: str | None = None) -> dict:
    p = Path(path) if path else LEXICON_PATH
    return yaml.safe_load(p.read_text())


def _compile(term: str) -> re.Pattern:
    """Word-boundary match, tolerant of hyphen/space variation and plurals.

    The optional trailing (?:s|es) matters more than it looks: without it,
    "underwater acoustic communication" failed to match the phrase
    "Underwater Acoustic Communications", silently dropping a real candidate
    (Sea-Gal Technologies) that Phase 1 had ranked in its top five.
    """
    esc = re.escape(term.lower()).replace(r"\ ", r"[\s\-]+")
    return re.compile(rf"(?<![a-z0-9]){esc}(?:e?s)?(?![a-z0-9])", re.IGNORECASE)


@lru_cache(maxsize=4096)
def _pattern(term: str) -> re.Pattern:
    return _compile(term)


@lru_cache(maxsize=1)
def _prefilter(path_key: str = "") -> re.Pattern:
    """One combined alternation over every technical term in the lexicon.

    Running ~150 individual regexes per record made bulk ingestion of 200k
    SBIR awards impractical. Almost every record matches nothing, so a single
    combined scan rejects the bulk of them in one pass; the per-term regexes
    then run only on survivors. Same results, ~40x faster.
    """
    lex = load_lexicon()
    terms = set()
    for cat in lex["categories"].values():
        terms.update(cat["direct_terms"])
        terms.update(cat["enabling_terms"])
    alts = sorted((re.escape(t.lower()).replace(r"\ ", r"[\s\-]+") for t in terms),
                  key=len, reverse=True)
    return re.compile(rf"(?<![a-z0-9])(?:{'|'.join(alts)})(?:e?s)?(?![a-z0-9])", re.IGNORECASE)


def _hits(text: str, terms) -> list[str]:
    out = []
    for t in terms:
        if _pattern(t).search(text):
            out.append(t)
    return out


def _occurrences(text: str, terms) -> int:
    """Total matches across all terms, counting repeats.

    Distinct-term counting cannot separate "this project is about corrosion"
    (Iowa State: the word appears five times) from "this reactor component
    happens to be corrosion resistant" (one passing mention). Frequency can.
    """
    return sum(len(_pattern(t).findall(text)) for t in terms)


@dataclass
class Match:
    """Result of matching one record against one category."""
    category_id: str
    direct: list[str] = field(default_factory=list)
    enabling: list[str] = field(default_factory=list)
    ocean: list[str] = field(default_factory=list)
    excluded_by: list[str] = field(default_factory=list)
    direct_occurrences: int = 0

    @property
    def score(self) -> int:
        # Direct terms name the problem itself and are weighted accordingly.
        return 3 * len(self.direct) + len(self.enabling)

    @property
    def has_ocean_context(self) -> bool:
        return bool(self.ocean)


@dataclass
class Classification:
    relevance: str
    category_id: str | None
    ocean_centrality: str | None
    rationale: str
    matches: list[Match] = field(default_factory=list)


def match_text(text: str, lex: dict | None = None) -> list[Match]:
    """Stage A. Return every category match for a block of text."""
    lex = lex or load_lexicon()
    text = (text or "").lower()
    if not text.strip():
        return []
    if not _prefilter().search(text):     # fast reject: no technical term at all
        return []
    global_ex = _hits(text, lex.get("global_exclusions", []))
    results: list[Match] = []
    for cat_id, cat in lex["categories"].items():
        direct = _hits(text, cat["direct_terms"])
        enabling = _hits(text, cat["enabling_terms"])
        if not direct and not enabling:
            continue
        ocean = _hits(text, cat.get("ocean_context", []))
        ex = list(global_ex) + _hits(text, cat.get("exclusions", []))
        occ = _occurrences(text, direct)
        results.append(Match(cat_id, direct, enabling, ocean, ex, occ))
    results.sort(key=lambda m: m.score, reverse=True)
    return results


def retrieve(text: str, min_score: int = 3, lex: dict | None = None) -> list[Match]:
    """Stage A gate. Deliberately loose - recall over precision."""
    return [m for m in match_text(text, lex) if m.score >= min_score]


def classify(text: str, lex: dict | None = None) -> Classification:
    """Stage B. Decide relevance + ocean centrality with a stated rationale."""
    lex = lex or load_lexicon()
    matches = match_text(text, lex)
    if not matches:
        return Classification("not_relevant", None, None, "No lexicon terms matched.")

    best = matches[0]
    cat = lex["categories"][best.category_id]
    requires_ocean = cat["requires_ocean_context"]

    # --- exclusion handling -------------------------------------------------
    # Exclusions veto only when the domain signal is weak. A strong direct-term
    # match plus ocean context survives an incidental biomedical word.
    if best.excluded_by:
        strong = len(best.direct) >= 2 or (best.direct and best.has_ocean_context)
        if not strong:
            return Classification(
                "not_relevant", best.category_id, None,
                f"Excluded by domain terms {best.excluded_by[:3]} with weak "
                f"in-domain signal (direct={len(best.direct)}, ocean={len(best.ocean)}).",
                matches)

    # --- ocean centrality ---------------------------------------------------
    n_direct, n_ocean = len(best.direct), len(best.ocean)
    if n_direct >= 1 and n_ocean >= 2:
        centrality = CENTRAL_MECHANISM
        why = f"{n_direct} direct problem term(s) with {n_ocean} marine context terms."
    elif n_direct >= 1 and n_ocean == 1:
        centrality = PRIMARY_END_MARKET
        why = f"{n_direct} direct problem term(s) with marine framing present."
    elif (n_direct >= 2 or best.direct_occurrences >= 3) and not requires_ocean:
        # The Iowa State clause: the technical problem is inherently
        # marine-relevant, so no ocean vocabulary is required.
        #
        # TWO direct terms are required, not one. At a threshold of one, a
        # single incidental "corrosion" admitted nuclear reactor components,
        # industrial heat storage and building repainting as marine materials.
        # Requiring two means the source text actually describes the problem
        # space rather than mentioning it in passing.
        centrality = STRONG_ADJACENCY
        why = (f"{n_direct} distinct direct term(s), {best.direct_occurrences} total "
               f"mentions, in '{best.category_id}' - a category whose problems are "
               f"acute in ocean-exposed industries; no marine vocabulary present.")
    elif n_ocean >= 1:
        centrality = PRIMARY_END_MARKET
        why = "Enabling terms only, but marine context present."
    elif n_direct >= 1 and not requires_ocean:
        centrality = INCIDENTAL
        why = (f"Only {best.direct_occurrences} mention(s) of one direct term in "
               f"'{best.category_id}' and no marine context - insufficient to establish "
               f"that the work targets this problem space.")
    else:
        centrality = INCIDENTAL
        why = "No direct problem terms and no marine context."

    # --- relevance ----------------------------------------------------------
    if centrality == INCIDENTAL:
        relevance = "not_relevant"
    elif requires_ocean and n_ocean == 0:
        # Category demands marine framing (e.g. maritime_software) and has none.
        relevance = "not_relevant"
        centrality = INCIDENTAL
        why += " Category requires marine context; none found."
    elif best.score >= 6 or (n_direct >= 1 and n_ocean >= 1):
        relevance = "relevant"
    elif n_direct >= 1:
        relevance = "borderline"
    else:
        relevance = "borderline"

    return Classification(relevance, best.category_id, centrality, why, matches)


def secondary_categories(matches: list[Match], primary: str | None,
                         min_score: int = 3) -> list[str]:
    return [m.category_id for m in matches
            if m.category_id != primary and m.score >= min_score]
