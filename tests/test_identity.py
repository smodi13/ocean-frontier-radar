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


def test_latest_signal_date_uses_event_dates_not_retrieval_dates(tmp_path):
    """Phase 2.5 regression: `timing` previously tracked when OUR source was
    accessed rather than when anything happened to the candidate."""
    from ofr import freshness
    c = db.connect(tmp_path / "f.db")
    db.init_db(c)
    db.upsert_source(c, source_id="s1", url="u", title="t", publisher="p",
                     source_type="federal_award", source_quality="tier1",
                     publication_date="2026-08-21", accessed_at="2026-08-21")
    db.upsert_candidate(c, cid="x", name="X", candidate_type="company")
    db.add_evidence(c, candidate_id="x", source_id="s1", evidence_type="sbir_phase_i",
                    observed_claim="old award", evidence_date="2021-03-01")
    c.commit()
    # accessed_at is today; the only real signal is 2021.
    assert freshness.latest_signal_date(c, "x") == "2021-03-01"
    freshness.refresh_all(c, verbose=False)
    got = c.execute("SELECT candidate_latest_signal_date d FROM candidates "
                    "WHERE candidate_id='x'").fetchone()["d"]
    assert got == "2021-03-01"


def test_undated_evidence_yields_null_not_a_guessed_date(tmp_path):
    from ofr import freshness
    c = db.connect(tmp_path / "g.db")
    db.init_db(c)
    db.upsert_source(c, source_id="s1", url="u", title="t", publisher="p",
                     source_type="press_release", source_quality="tier2",
                     publication_date=None, accessed_at="2026-08-21")
    db.upsert_candidate(c, cid="y", name="Y", candidate_type="company")
    db.add_evidence(c, candidate_id="y", source_id="s1", evidence_type="patent_granted",
                    observed_claim="a patent", evidence_date=None)
    c.commit()
    assert freshness.latest_signal_date(c, "y") is None
