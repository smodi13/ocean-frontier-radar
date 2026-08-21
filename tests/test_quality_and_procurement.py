"""Data-quality guards and procurement summarisation."""
from ofr import db
from ofr.ingestion.quality import is_junk_name
from ofr.ingestion.usaspending import theme_demand_summary


def test_real_companies_are_not_treated_as_junk():
    """Regression: an earlier guard deleted NATRX, Giner and UES."""
    for name in ["NATRX INC", "GINER INC", "UES INC", "VY CORP", "D 2 INC",
                 "ARMADA Marine Robotics", "Ocean Motion Technologies Inc",
                 "Sea-Gal Technologies, Inc."]:
        assert not is_junk_name(name), name


def test_actual_junk_is_caught():
    for name in ["Steve", "", "  ", "Bob", "n/a", "unknown", "TBD"]:
        assert is_junk_name(name), name


def test_procurement_summary_reports_no_contracts_cleanly(conn):
    s = theme_demand_summary(conn, "maritime_autonomy")
    assert s["n_contracts"] == 0


def _proc(conn, pid, theme, recipient, agency, amount, start):
    db.upsert_source(conn, source_id=f"s_{pid}", url="u", title="t", publisher="USAspending",
                     source_type="procurement", source_quality="tier1",
                     publication_date=start, accessed_at="2026-08-21")
    conn.execute("""INSERT INTO procurement (procurement_id,theme,award_id,recipient,
        awarding_agency,awarding_sub_agency,amount,start_date,description,source_id)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (pid, theme, pid, recipient, agency, agency, amount, start, "d", f"s_{pid}"))


def test_procurement_summary_identifies_buyers_and_repeat_suppliers(conn):
    _proc(conn, "p1", "maritime_autonomy", "Saab", "Commerce", 1_680_000, "2024-01-01")
    _proc(conn, "p2", "maritime_autonomy", "Saab", "Navy", 900_000, "2025-01-01")
    _proc(conn, "p3", "maritime_autonomy", "Teledyne", "Navy", 1_750_000, "2026-01-01")
    conn.commit()
    s = theme_demand_summary(conn, "maritime_autonomy")
    assert s["n_contracts"] == 3
    assert s["max_contract_usd"] == 1_750_000
    assert dict(s["repeat_suppliers"]).get("Saab") == 2
    assert s["recurring"] is True


def test_procurement_summary_carries_a_not_tam_caveat(conn):
    _proc(conn, "p1", "ocean_sensing", "X", "Navy", 1000.0, "2024-01-01")
    conn.commit()
    s = theme_demand_summary(conn, "ocean_sensing")
    assert "NOT a market size estimate" in s["caveat"]


def test_contact_addresses_are_stripped_from_website_fields():
    """SBIR rows sometimes put a contact address in the Company Website column;
    storing contact details as a URL is both wrong and needless data retention."""
    from ofr.ingestion.quality import sanitize_website
    assert sanitize_website("http://www.df-nn.com/info@df-nn.com") == "http://www.df-nn.com"
    assert sanitize_website("https://info@bnonlinear.com") is None
    assert sanitize_website("https://armadamarinerobotics.com") == "https://armadamarinerobotics.com"
    assert sanitize_website(None) is None
