import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from ofr import db


@pytest.fixture
def conn(tmp_path):
    """Fresh in-file database per test. No network, no shared state."""
    c = db.connect(tmp_path / "test.db")
    db.init_db(c)
    yield c
    c.close()


@pytest.fixture
def seeded(conn):
    """One candidate with one source and one piece of evidence."""
    db.upsert_source(conn, source_id="src_x", url="https://example.org/a",
                     title="Award A", publisher="NSF", source_type="federal_award",
                     source_quality="tier1", publication_date="2026-01-15",
                     accessed_at="2026-08-21", retrieval_method="api")
    db.upsert_candidate(conn, cid="acme-marine", name="Acme Marine Inc",
                        candidate_type="company", ocean_centrality="central_mechanism",
                        sourcing_signal="emerging")
    eid = db.add_evidence(conn, candidate_id="acme-marine", source_id="src_x",
                          evidence_type="sbir_phase_i",
                          observed_claim="SBIR Phase I award", evidence_date="2026-01-15",
                          quantitative_value=305000, unit="USD")
    conn.commit()
    return conn, eid
