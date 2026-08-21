"""Schema constraints, idempotency and fact/interpretation separation."""
import sqlite3
import pytest
from ofr import db


def test_reingest_does_not_duplicate(seeded):
    conn, _ = seeded
    for _ in range(3):
        db.upsert_candidate(conn, cid="acme-marine", name="Acme Marine Inc",
                            candidate_type="company")
        db.add_evidence(conn, candidate_id="acme-marine", source_id="src_x",
                        evidence_type="sbir_phase_i",
                        observed_claim="SBIR Phase I award", evidence_date="2026-01-15")
    conn.commit()
    assert conn.execute("SELECT COUNT(*) c FROM candidates").fetchone()["c"] == 1
    assert conn.execute("SELECT COUNT(*) c FROM evidence").fetchone()["c"] == 1


def test_evidence_requires_existing_source(conn):
    db.upsert_candidate(conn, cid="x", name="X", candidate_type="company")
    with pytest.raises(sqlite3.IntegrityError):
        db.add_evidence(conn, candidate_id="x", source_id="does_not_exist",
                        evidence_type="sbir_phase_i", observed_claim="c")


def test_evidence_requires_existing_candidate(conn):
    db.upsert_source(conn, source_id="s", url="u", title="t", publisher="p",
                     source_type="federal_award", source_quality="tier1",
                     publication_date=None, accessed_at="2026-08-21")
    with pytest.raises(sqlite3.IntegrityError):
        db.add_evidence(conn, candidate_id="ghost", source_id="s",
                        evidence_type="sbir_phase_i", observed_claim="c")


def test_source_quality_vocabulary_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        db.upsert_source(conn, source_id="bad", url="u", title="t", publisher="p",
                         source_type="federal_award", source_quality="tier9",
                         publication_date=None, accessed_at="2026-08-21")


def test_ocean_centrality_vocabulary_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        db.upsert_candidate(conn, cid="y", name="Y", candidate_type="company",
                            ocean_centrality="quite_oceanic")


def test_sourcing_signal_vocabulary_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        db.upsert_candidate(conn, cid="y", name="Y", candidate_type="company",
                            sourcing_signal="very_hidden")


def test_observed_analyst_view_requires_evidence_ids(seeded):
    """An 'observed' claim with no evidence is a schema violation, not a warning."""
    conn, eid = seeded
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("""INSERT INTO analyst_views
            (view_id,candidate_id,view_type,statement,evidence_ids,author,created_at)
            VALUES ('v1','acme-marine','observed','It works',NULL,'analyst','2026-08-21')""")
    conn.execute("""INSERT INTO analyst_views
        (view_id,candidate_id,view_type,statement,evidence_ids,author,created_at)
        VALUES ('v2','acme-marine','observed','It works',?, 'analyst','2026-08-21')""", (eid,))


def test_inferred_and_unknown_views_need_no_evidence(seeded):
    conn, _ = seeded
    for i, vt in enumerate(("inferred", "unknown", "technical_kill_question")):
        conn.execute("""INSERT INTO analyst_views
            (view_id,candidate_id,view_type,statement,evidence_ids,author,created_at)
            VALUES (?,?,?,?,NULL,'analyst','2026-08-21')""",
            (f"v{i}", "acme-marine", vt, "statement"))


def test_prioritization_points_bounded(seeded):
    conn, _ = seeded
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("""INSERT INTO prioritization
            (candidate_id,dimension,points,max_points,rationale,scored_at)
            VALUES ('acme-marine','technical_evidence',9,3,'too many','2026-08-21')""")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("""INSERT INTO prioritization
            (candidate_id,dimension,points,max_points,rationale,scored_at)
            VALUES ('acme-marine','technical_evidence',-1,3,'negative','2026-08-21')""")


def test_analyst_override_requires_written_reason(seeded):
    conn, _ = seeded
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("""INSERT INTO prioritization
            (candidate_id,dimension,points,max_points,rationale,analyst_override,
             override_reason,scored_at)
            VALUES ('acme-marine','venture_potential',3,3,'r',1,NULL,'2026-08-21')""")
    conn.execute("""INSERT INTO prioritization
        (candidate_id,dimension,points,max_points,rationale,analyst_override,
         override_reason,scored_at)
        VALUES ('acme-marine','venture_potential',3,3,'r',1,'Met the team','2026-08-21')""")


def test_no_total_score_column_exists(conn):
    """Totals must be computed on read so a number cannot be quoted alone."""
    cols = [r[1] for r in conn.execute("PRAGMA table_info(prioritization)")]
    assert "total" not in cols and "total_score" not in cols


def test_missing_fields_stay_null_rather_than_fabricated(conn):
    db.upsert_source(conn, source_id="s2", url=None, title="t", publisher="p",
                     source_type="press_release", source_quality="tier2",
                     publication_date=None, accessed_at="2026-08-21")
    row = conn.execute("SELECT publication_date, url FROM sources WHERE source_id='s2'").fetchone()
    assert row["publication_date"] is None
    assert row["url"] is None


def test_upsert_does_not_blank_existing_values(conn):
    db.upsert_candidate(conn, cid="z", name="Z", candidate_type="company",
                        website="https://z.example", geography="Boston, MA")
    db.upsert_candidate(conn, cid="z", name="Z", candidate_type="company")  # sparser source
    row = conn.execute("SELECT website, geography FROM candidates WHERE candidate_id='z'").fetchone()
    assert row["website"] == "https://z.example"
    assert row["geography"] == "Boston, MA"
