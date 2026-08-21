"""Deterministic identity, slugs and date normalization."""
import pytest
from ofr import db


def test_candidate_id_is_deterministic():
    assert db.candidate_id("ARMADA Marine Robotics") == db.candidate_id("ARMADA Marine Robotics")


def test_legal_suffixes_do_not_create_duplicates():
    ids = {db.candidate_id(n) for n in
           ["ARMADA Marine Robotics", "ARMADA Marine Robotics, Inc.",
            "Armada Marine Robotics LLC", "armada marine robotics"]}
    assert len(ids) == 1, f"expected one id, got {ids}"


def test_accents_normalized():
    assert db.candidate_id("Muñoz Robotics") == db.candidate_id("Munoz Robotics")


def test_stable_id_deterministic_and_input_sensitive():
    assert db.stable_id("ev", "a", "b") == db.stable_id("ev", "a", "b")
    assert db.stable_id("ev", "a", "b") != db.stable_id("ev", "a", "c")


@pytest.mark.parametrize("raw,expected", [
    ("08/17/2026", "2026-08-17"),
    ("2026-08-17", "2026-08-17"),
    ("2026-08", "2026-08-01"),
    ("2023", "2023-01-01"),
])
def test_date_normalization(raw, expected):
    assert db.normalize_date(raw) == expected


def test_unparseable_date_returns_none_not_a_guess():
    # A fabricated date would be worse than a missing one.
    assert db.normalize_date("sometime last spring") is None
    assert db.normalize_date("") is None
    assert db.normalize_date(None) is None


def test_dotted_legal_acronyms_normalize():
    """Regression: 'NEXUMA L.L.C.' normalised to 'nexuma l l c', so it would not
    resolve to the same entity as 'Nexuma LLC'."""
    assert db.normalize_name("NEXUMA L.L.C.") == "nexuma"
    assert db.candidate_id("NEXUMA L.L.C.") == db.candidate_id("Nexuma LLC")
    assert db.candidate_id("American Ecotech L.C.") == db.candidate_id("American Ecotech LC")
