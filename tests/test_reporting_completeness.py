"""Reporting completeness: material evidence must not vanish between the
database and the analyst review.

Phase 2 ingested ARMADA's ~$2.0M Navy Phase II award correctly and the Phase 2
report still failed to mention it. The pipeline was fine; the reporting layer
silently dropped it. These tests separate the two failure modes:

    DATA completeness      -> was the evidence ingested?
    REPORTING completeness -> did material evidence reach the review?

Nothing here hard-codes a company name or a dollar amount. Materiality is
derived from the data.
"""
import pytest

from ofr import db, prioritize, review


def _seed(conn, cid="acme", *, with_phase_ii=True):
    db.upsert_source(conn, source_id="s_small", url="https://example.org/small",
                     title="Phase I", publisher="NSF", source_type="federal_award",
                     source_quality="tier1", publication_date="2021-02-01",
                     accessed_at="2026-08-21")
    db.upsert_source(conn, source_id="s_big", url="https://example.org/big",
                     title="Phase II", publisher="Navy", source_type="federal_award",
                     source_quality="tier1", publication_date="2023-01-30",
                     accessed_at="2026-08-21")
    db.upsert_source(conn, source_id="s_recent", url="https://example.org/recent",
                     title="Licence", publisher="Institute",
                     source_type="press_release", source_quality="tier1",
                     publication_date="2025-01-01", accessed_at="2026-08-21")
    db.upsert_candidate(conn, cid=cid, name="Acme Marine", candidate_type="company",
                        ocean_centrality="central_mechanism", sourcing_signal="emerging",
                        company_formed=1)
    db.add_evidence(conn, candidate_id=cid, source_id="s_small",
                    evidence_type="sbir_phase_i", observed_claim="Small Phase I award",
                    evidence_date="2021-02-01", quantitative_value=250_000, unit="USD",
                    analyst_notes="contract=AAA-111")
    if with_phase_ii:
        db.add_evidence(conn, candidate_id=cid, source_id="s_big",
                        evidence_type="sbir_phase_ii",
                        observed_claim="Large Phase II award",
                        evidence_date="2023-01-30", quantitative_value=1_990_000,
                        unit="USD", analyst_notes="contract=BBB-222")
    db.add_evidence(conn, candidate_id=cid, source_id="s_recent",
                    evidence_type="exclusive_license",
                    observed_claim="Exclusive licence executed",
                    evidence_date="2025-01-01")
    conn.commit()
    return cid


# ---------------------------------------------------------------- data layer
def test_data_completeness_phase_ii_is_ingested(conn):
    cid = _seed(conn)
    rows = conn.execute("SELECT evidence_type FROM evidence WHERE candidate_id=?",
                        (cid,)).fetchall()
    assert "sbir_phase_ii" in {r["evidence_type"] for r in rows}


# ----------------------------------------------------------- reporting layer
def test_material_evidence_identifies_all_four_categories(conn):
    cid = _seed(conn)
    mat = review.material_evidence(conn, cid)
    assert set(mat) == {"most_recent", "largest_funding",
                        "strongest_technical", "strongest_commercial"}


def test_largest_award_is_the_phase_ii_not_the_phase_i(conn):
    cid = _seed(conn)
    mat = review.material_evidence(conn, cid)
    assert mat["largest_funding"]["quantitative_value"] == 1_990_000


def test_most_recent_is_by_event_date_not_retrieval_date(conn):
    """All three sources were accessed on the same day; recency must come from
    the event, not from when we happened to fetch it."""
    cid = _seed(conn)
    mat = review.material_evidence(conn, cid)
    assert mat["most_recent"]["evidence_date"] == "2025-01-01"


def test_review_card_surfaces_the_phase_ii_award(conn):
    """The exact Phase 2 failure, as a regression."""
    cid = _seed(conn)
    card = review.build_card_checked(conn, cid)
    blob = " ".join(card["funding_evidence"]) + " " + \
           " ".join(str(v) for v in card["material_evidence"].values())
    assert "1,990,000" in blob, "the largest award vanished from the review card"


def test_card_builder_refuses_to_drop_material_evidence(conn, monkeypatch):
    """If the reporting layer regresses, generation must FAIL rather than
    quietly emit an incomplete card."""
    cid = _seed(conn)
    original = review.build_card          # capture before patching, or we recurse

    def crippled(c, i):
        card = original(c, i)
        card["material_evidence"] = {}
        card["material_evidence_ids"] = {}
        return card

    monkeypatch.setattr(review, "build_card", crippled)
    with pytest.raises(review.ReportingCompletenessError):
        review.build_card_checked(conn, cid)


def test_completeness_check_names_what_is_missing(conn):
    """A material item counts as reported if it is accounted for ANYWHERE in the
    card, so the test drops every reference to it before asserting."""
    cid = _seed(conn)
    card = review.build_card(conn, cid)
    target = card["material_evidence_ids"]["largest_funding"]
    for key, eid in list(card["material_evidence_ids"].items()):
        if eid == target:
            card["material_evidence_ids"].pop(key)
            card["material_evidence"].pop(key, None)
    missing = review.check_completeness(conn, cid, card)
    assert "largest_funding" in missing


def test_candidate_with_no_evidence_is_not_an_error(conn):
    db.upsert_candidate(conn, cid="empty", name="Empty", candidate_type="company")
    conn.commit()
    assert review.material_evidence(conn, "empty") == {}
    card = review.build_card_checked(conn, "empty")
    assert card["evidence_count"] == 0


# ------------------------------------------------------- award de-duplication
def test_same_award_from_two_sources_is_not_double_counted(conn):
    """SBIR bulk and USAspending report the same contract with different
    punctuation and different values; summing both inflated ARMADA's federal
    total from ~$3.0M to ~$4.7M."""
    cid = _seed(conn)
    db.upsert_source(conn, source_id="s_dup", url="https://example.org/dup",
                     title="Same award, other source", publisher="USAspending.gov",
                     source_type="federal_award", source_quality="tier1",
                     publication_date="2023-01-30", accessed_at="2026-08-21")
    db.add_evidence(conn, candidate_id=cid, source_id="s_dup",
                    evidence_type="sbir_phase_ii",
                    observed_claim="Same Phase II, current value",
                    evidence_date="2023-01-30", quantitative_value=1_990_000,
                    unit="USD", analyst_notes="usaspending_award_id=BBB222")
    conn.commit()
    card = review.build_card_checked(conn, cid)
    assert card["distinct_federal_awards"] == 2       # Phase I + Phase II, not 3
    assert card["total_federal_award_value_usd"] == 2_240_000


def test_dedupe_keeps_the_larger_current_value(conn):
    cid = _seed(conn, with_phase_ii=False)
    for sid, val, note in (("s_v1", 999_028, "contract=CCC-333"),
                           ("s_v2", 1_998_926, "usaspending_award_id=CCC333")):
        db.upsert_source(conn, source_id=sid, url="u", title="t", publisher="p",
                         source_type="federal_award", source_quality="tier1",
                         publication_date="2023-01-30", accessed_at="2026-08-21")
        db.add_evidence(conn, candidate_id=cid, source_id=sid,
                        evidence_type="sbir_phase_ii", observed_claim=f"award {val}",
                        evidence_date="2023-01-30", quantitative_value=val,
                        unit="USD", analyst_notes=note)
    conn.commit()
    card = review.build_card_checked(conn, cid)
    assert card["total_federal_award_value_usd"] == 250_000 + 1_998_926


# ------------------------------------------------- epistemic separation holds
def test_card_keeps_observed_inferred_and_unknown_apart(conn):
    cid = _seed(conn)
    eid = conn.execute("SELECT evidence_id FROM evidence WHERE candidate_id=? LIMIT 1",
                       (cid,)).fetchone()["evidence_id"]
    conn.execute("""INSERT INTO analyst_views
        (view_id,candidate_id,view_type,statement,evidence_ids,author,created_at)
        VALUES ('v1',?, 'observed','Award exists',?,'analyst','2026-08-21')""", (cid, eid))
    conn.execute("""INSERT INTO analyst_views
        (view_id,candidate_id,view_type,statement,evidence_ids,author,created_at)
        VALUES ('v2',?, 'inferred','We think it scales',NULL,'ai_assisted','2026-08-21')""",
                 (cid,))
    conn.commit()
    card = review.build_card_checked(conn, cid)
    assert card["observed"] == ["Award exists"]
    assert card["inferred"] == ["We think it scales"]
    assert "We think it scales" not in card["technical_evidence"]


# ------------------------------------- observed views must cite real evidence
def test_observed_view_must_cite_a_real_evidence_id(conn, tmp_path):
    """An 'observed' claim citing a placeholder string is not traceable."""
    import yaml
    from ofr.ingestion import views as views_mod
    _seed(conn)
    bad = tmp_path / "bad.yaml"
    bad.write_text(yaml.safe_dump({"views": {"acme": [
        {"type": "observed", "statement": "Award exists",
         "evidence_ids": "see funding_evidence"}]}}))
    with pytest.raises(ValueError, match="traceable"):
        views_mod.ingest(conn, bad, verbose=False)


def test_observed_view_with_real_evidence_id_is_accepted(conn, tmp_path):
    import yaml
    from ofr.ingestion import views as views_mod
    cid = _seed(conn)
    eid = conn.execute("SELECT evidence_id FROM evidence WHERE candidate_id=? LIMIT 1",
                       (cid,)).fetchone()["evidence_id"]
    good = tmp_path / "good.yaml"
    good.write_text(yaml.safe_dump({"views": {cid: [
        {"type": "observed", "statement": "Award exists", "evidence_ids": eid}]}}))
    views_mod.ingest(conn, good, verbose=False)
    row = conn.execute("SELECT statement FROM analyst_views WHERE candidate_id=? "
                       "AND view_type='observed'", (cid,)).fetchone()
    assert row["statement"] == "Award exists"
