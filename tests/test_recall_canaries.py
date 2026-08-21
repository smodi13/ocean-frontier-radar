"""Recall canaries: does the pipeline still surface known-relevant examples?

These detect SILENT recall degradation - the failure mode that lost Sea-Gal
and Hydrokinetx in Phase 2 without anything looking wrong in the output.

The tests assert survival through each pipeline stage and report WHICH stage
dropped a canary. They never assert a ranking, and the fixture names never
enter production output.
"""
from pathlib import Path

import pytest
import yaml

from ofr.lexicon import classify, match_text, retrieve

FIXTURES = Path(__file__).parent / "fixtures" / "recall_canaries.yaml"
CANARIES = yaml.safe_load(FIXTURES.read_text())["canaries"]
IDS = [c["id"] for c in CANARIES]


def _stage_report(text: str) -> dict:
    """Which stage, if any, loses this text."""
    matches = match_text(text)
    retrieved = retrieve(text, min_score=3)
    c = classify(text)
    return {
        "matched_any": bool(matches),
        "retrieved": bool(retrieved),
        "relevance": c.relevance,
        "category": c.category_id,
        "centrality": c.ocean_centrality,
        "top_score": matches[0].score if matches else 0,
    }


@pytest.mark.parametrize("canary", CANARIES, ids=IDS)
def test_canary_survives_lexicon_matching(canary):
    r = _stage_report(canary["text"])
    assert r["matched_any"], (
        f"STAGE 0 (lexicon matching) lost '{canary['id']}' ({canary['pattern']}): "
        f"no lexicon term matched at all.")


@pytest.mark.parametrize("canary", CANARIES, ids=IDS)
def test_canary_survives_stage_a_retrieval(canary):
    r = _stage_report(canary["text"])
    assert r["retrieved"], (
        f"STAGE A (retrieval) lost '{canary['id']}' ({canary['pattern']}): "
        f"matched terms but scored {r['top_score']}, below the retrieval gate.")


@pytest.mark.parametrize("canary", CANARIES, ids=IDS)
def test_canary_survives_stage_b_classification(canary):
    r = _stage_report(canary["text"])
    assert r["relevance"] != "not_relevant", (
        f"STAGE B (classification) lost '{canary['id']}' ({canary['pattern']}): "
        f"classified not_relevant as {r['category']}/{r['centrality']}.")


@pytest.mark.parametrize(
    "canary", [c for c in CANARIES if c.get("expect_category")],
    ids=[c["id"] for c in CANARIES if c.get("expect_category")])
def test_canary_lands_in_expected_category(canary):
    r = _stage_report(canary["text"])
    assert r["category"] == canary["expect_category"], (
        f"'{canary['id']}' drifted from {canary['expect_category']} to {r['category']}.")


@pytest.mark.parametrize(
    "canary", [c for c in CANARIES if c.get("expect_centrality")],
    ids=[c["id"] for c in CANARIES if c.get("expect_centrality")])
def test_canary_keeps_expected_centrality(canary):
    r = _stage_report(canary["text"])
    expected = canary["expect_centrality"]
    allowed = expected if isinstance(expected, list) else [expected]
    assert r["centrality"] in allowed, (
        f"'{canary['id']}' centrality drifted from {allowed} to {r['centrality']}.")


def test_every_thesis_pattern_has_a_canary():
    """Coverage guard: each thesis pattern must stay represented."""
    patterns = {c["pattern"].split(" / ")[0] for c in CANARIES}
    required = {"maritime autonomy", "marine materials", "ocean sensing",
                "offshore energy", "marine carbon", "blue food",
                "hidden adjacency", "pre-company research"}
    assert required <= patterns, f"missing canary coverage for: {required - patterns}"


def test_canaries_are_not_hardcoded_into_production():
    """The fixture must be test-only; production must not read it."""
    src = Path(__file__).parents[1] / "src"
    offenders = [p for p in src.rglob("*.py")
                 if "recall_canaries" in p.read_text()]
    assert not offenders, f"production code references the canary fixture: {offenders}"
