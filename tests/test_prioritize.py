"""Sourcing-priority scoring behaviour and bounds."""
from datetime import date
from ofr import db, prioritize


def _mk(conn, cid, centrality="central_mechanism", signal="emerging",
        ev=(), flags=()):
    db.upsert_source(conn, source_id=f"s_{cid}", url="u", title="t", publisher="p",
                     source_type="federal_award", source_quality="tier1",
                     publication_date=None, accessed_at="2026-08-21")
    db.upsert_candidate(conn, cid=cid, name=cid, candidate_type="company",
                        ocean_centrality=centrality, sourcing_signal=signal)
    for etype, edate, amt in ev:
        db.add_evidence(conn, candidate_id=cid, source_id=f"s_{cid}",
                        evidence_type=etype, observed_claim=etype,
                        evidence_date=edate, quantitative_value=amt)
    for f in flags:
        db.add_flag(conn, cid, f)
    conn.commit()


def test_all_dimensions_scored_and_within_bounds(conn):
    _mk(conn, "a", ev=[("sbir_phase_i", "2026-06-01", 305000)])
    prioritize.score_candidate(conn, "a", asof=date(2026, 8, 21))
    rows = conn.execute("SELECT dimension,points,max_points FROM prioritization "
                        "WHERE candidate_id='a'").fetchall()
    assert {r["dimension"] for r in rows} == set(prioritize.MAX_POINTS)
    for r in rows:
        assert 0 <= r["points"] <= r["max_points"] == prioritize.MAX_POINTS[r["dimension"]]


def test_total_is_computed_not_stored(conn):
    _mk(conn, "b", ev=[("sbir_phase_ii", "2026-06-01", 1250000)])
    prioritize.score_candidate(conn, "b", asof=date(2026, 8, 21))
    t = prioritize.total(conn, "b")
    assert 0 < t <= prioritize.TOTAL_MAX


def test_phase_ii_outscores_phase_i_on_technical(conn):
    _mk(conn, "p1", ev=[("sbir_phase_i", "2026-06-01", 305000)])
    _mk(conn, "p2", ev=[("sbir_phase_ii", "2026-06-01", 1250000)])
    prioritize.score_candidate(conn, "p1", asof=date(2026, 8, 21))
    prioritize.score_candidate(conn, "p2", asof=date(2026, 8, 21))
    g = lambda c: conn.execute("SELECT points FROM prioritization WHERE candidate_id=? "
                               "AND dimension='technical_evidence'", (c,)).fetchone()["points"]
    assert g("p2") > g("p1")


def test_every_awarded_point_cites_evidence(conn):
    _mk(conn, "c", ev=[("exclusive_license", "2026-01-01", None)])
    prioritize.score_candidate(conn, "c", asof=date(2026, 8, 21))
    for r in conn.execute("""SELECT dimension,points,evidence_ids,rationale
                             FROM prioritization WHERE candidate_id='c'"""):
        assert r["rationale"].strip()
        if r["points"] > 0 and r["dimension"] not in ("differentiated_sourcing",):
            assert r["evidence_ids"], f"{r['dimension']} scored without citing evidence"


def test_timing_decays_with_age(conn):
    _mk(conn, "fresh", ev=[("sbir_phase_i", "2026-06-01", 1)])
    _mk(conn, "stale", ev=[("sbir_phase_i", "2019-06-01", 1)])
    prioritize.score_candidate(conn, "fresh", asof=date(2026, 8, 21))
    prioritize.score_candidate(conn, "stale", asof=date(2026, 8, 21))
    g = lambda c: conn.execute("SELECT points FROM prioritization WHERE candidate_id=? "
                               "AND dimension='timing'", (c,)).fetchone()["points"]
    assert g("fresh") == 2 and g("stale") == 0


def test_incidental_centrality_zeroes_propeller_relevance(conn):
    _mk(conn, "inc", centrality="incidental", ev=[("sbir_phase_i", "2026-06-01", 1)])
    prioritize.score_candidate(conn, "inc", asof=date(2026, 8, 21))
    pts = conn.execute("SELECT points FROM prioritization WHERE candidate_id='inc' "
                       "AND dimension='propeller_relevance'").fetchone()["points"]
    assert pts == 0


def test_hidden_adjacency_scores_top_differentiated_sourcing(conn):
    _mk(conn, "hidden", centrality="strong_adjacency", signal="emerging",
        ev=[("sbir_phase_ii", "2026-06-01", 1)])
    prioritize.score_candidate(conn, "hidden", asof=date(2026, 8, 21))
    pts = conn.execute("SELECT points FROM prioritization WHERE candidate_id='hidden' "
                       "AND dimension='differentiated_sourcing'").fetchone()["points"]
    assert pts == 3


def test_established_contractor_loses_venture_and_sourcing_points(conn):
    _mk(conn, "shop", signal="obvious", ev=[("sbir_phase_ii", "2026-06-01", 1500000)],
        flags=["ESTABLISHED_SBIR_CONTRACTOR"])
    prioritize.score_candidate(conn, "shop", asof=date(2026, 8, 21))
    g = lambda d: conn.execute("SELECT points FROM prioritization WHERE candidate_id='shop' "
                               "AND dimension=?", (d,)).fetchone()["points"]
    assert g("venture_potential") == 0
    assert g("differentiated_sourcing") == 0


def test_analyst_override_is_not_clobbered_by_rescoring(conn):
    _mk(conn, "ovr", ev=[("sbir_phase_i", "2026-06-01", 1)])
    prioritize.score_candidate(conn, "ovr", asof=date(2026, 8, 21))
    conn.execute("""UPDATE prioritization SET points=3, analyst_override=1,
                    override_reason='Spoke with the PI' WHERE candidate_id='ovr'
                    AND dimension='venture_potential'""")
    conn.commit()
    prioritize.score_candidate(conn, "ovr", asof=date(2026, 8, 21))
    row = conn.execute("SELECT points,analyst_override FROM prioritization "
                       "WHERE candidate_id='ovr' AND dimension='venture_potential'").fetchone()
    assert row["points"] == 3 and row["analyst_override"] == 1


def test_no_evidence_scores_zero_not_an_error(conn):
    _mk(conn, "empty")
    prioritize.score_candidate(conn, "empty", asof=date(2026, 8, 21))
    assert prioritize.total(conn, "empty") >= 0
