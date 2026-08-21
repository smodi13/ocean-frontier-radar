"""Entity resolution must never merge on similarity alone."""
import pytest
from ofr import db, entity


def _cand(conn, cid, name, website=None, seen="2026-01-01"):
    db.upsert_candidate(conn, cid=cid, name=name, candidate_type="company",
                        website=website, first_seen=seen)


def test_identical_normalized_names_merge(conn):
    _cand(conn, "armada-marine-robotics", "ARMADA Marine Robotics", seen="2026-01-01")
    _cand(conn, "armada-marine-robotics-2", "Armada Marine Robotics, Inc.", seen="2026-02-01")
    conn.commit()
    merges = entity.find_merges(conn)
    assert any(b == "identical_normalized_name" for _, _, b in merges)


def test_shared_domain_merges(conn):
    _cand(conn, "a-co", "A Co", website="https://acme-marine.com/about")
    _cand(conn, "b-co", "B Co", website="http://www.acme-marine.com")
    conn.commit()
    assert any(b == "shared_website_domain" for _, _, b in entity.find_merges(conn))


def test_similar_but_distinct_names_do_not_merge(conn):
    _cand(conn, "ocean-motion-technologies", "Ocean Motion Technologies")
    _cand(conn, "ocean-power-technologies", "Ocean Power Technologies")
    conn.commit()
    assert entity.find_merges(conn) == []


def test_social_domains_are_not_identity_evidence(conn):
    _cand(conn, "c-co", "C Co", website="https://linkedin.com/company/c")
    _cand(conn, "d-co", "D Co", website="https://linkedin.com/company/d")
    conn.commit()
    assert entity.find_merges(conn) == []


def test_merge_with_unexplainable_basis_is_refused(conn):
    _cand(conn, "e-co", "E Co")
    _cand(conn, "f-co", "F Co")
    conn.commit()
    with pytest.raises(ValueError, match="unexplainable basis"):
        entity.apply_merges(conn, [("e-co", "f-co", "semantic_similarity")], verbose=False)


def test_merge_moves_evidence_and_is_logged(conn):
    db.upsert_source(conn, source_id="s", url="u", title="t", publisher="p",
                     source_type="federal_award", source_quality="tier1",
                     publication_date=None, accessed_at="2026-08-21")
    _cand(conn, "keep-co", "Keep Co", seen="2026-01-01")
    _cand(conn, "dup-co", "Keep Co.", seen="2026-05-01")
    db.add_evidence(conn, candidate_id="dup-co", source_id="s",
                    evidence_type="sbir_phase_i", observed_claim="award")
    conn.commit()
    entity.apply_merges(conn, verbose=False)
    assert conn.execute("SELECT COUNT(*) c FROM candidates").fetchone()["c"] == 1
    assert conn.execute(
        "SELECT candidate_id FROM evidence").fetchone()["candidate_id"] == "keep-co"
    log = conn.execute("SELECT basis FROM merge_log").fetchone()
    assert log["basis"] == "identical_normalized_name"


def test_uncertain_links_are_recorded_not_merged(conn):
    db.upsert_source(conn, source_id="s", url="u", title="t", publisher="p",
                     source_type="federal_award", source_quality="tier1",
                     publication_date=None, accessed_at="2026-08-21")
    _cand(conn, "lab-project", "Subsea Connector Project")
    _cand(conn, "spinout-co", "Connector Robotics")
    db.add_person(conn, candidate_id="lab-project", name="Jane Roe", source_id="s")
    db.add_person(conn, candidate_id="spinout-co", name="Jane Roe", source_id="s")
    conn.commit()
    entity.find_possible_relationships(conn, verbose=False)
    rows = conn.execute("SELECT * FROM possible_relationships").fetchall()
    assert rows and rows[0]["relationship"] == "shares_person"
    assert conn.execute("SELECT COUNT(*) c FROM candidates").fetchone()["c"] == 2
