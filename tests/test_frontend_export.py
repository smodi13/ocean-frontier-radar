"""Validation for the frontend data export (Phase 4).

The site must never be able to display a number the research does not support,
so these tests reconcile the exported JSON against the canonical artifacts.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "frontend" / "data"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import build_frontend_data as bfd  # noqa: E402


def load(name: str):
    return json.loads((DATA / f"{name}.json").read_text())


@pytest.fixture(scope="module")
def bundle():
    return bfd.build(write=False)


# --------------------------------------------------------------- artifacts
def test_all_expected_artifacts_exist():
    for name in ("summary", "candidates", "themes", "frontier", "armada",
                 "evidenceRegister", "candidateDetail"):
        assert (DATA / f"{name}.json").exists(), f"missing {name}.json"


def test_export_is_deterministic():
    """Re-running the export must produce byte-identical files, so a change on
    the site always implies a change in the research."""
    before = {p.name: p.read_bytes() for p in DATA.glob("*.json")}
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_frontend_data.py")],
                   capture_output=True, check=True)
    after = {p.name: p.read_bytes() for p in DATA.glob("*.json")}
    assert before.keys() == after.keys()
    changed = [k for k in before if before[k] != after[k]]
    assert not changed, f"non-deterministic export: {changed}"


# ------------------------------------------------------------- referential
def test_no_duplicate_candidate_ids():
    ids = [c["id"] for c in load("candidates")]
    assert len(ids) == len(set(ids))


def test_every_candidate_has_a_detail_record():
    detail = load("candidateDetail")
    for c in load("candidates"):
        assert c["id"] in detail, f"{c['id']} missing detail"


def test_no_broken_evidence_references():
    detail = load("candidateDetail")
    for cid, d in detail.items():
        seen = set()
        for e in d["evidence"]:
            assert e["evidence_id"], f"{cid}: evidence with no id"
            assert e["evidence_id"] not in seen, f"{cid}: duplicate evidence id"
            seen.add(e["evidence_id"])
            assert e["observed_claim"].strip(), f"{cid}: empty evidence claim"


def test_frontier_signals_resolve_to_candidates():
    detail = load("candidateDetail")
    for s in load("frontier")["signals"]:
        assert s["id"] in detail, f"frontier signal {s['id']} has no candidate"


def test_theme_examples_resolve_to_candidates():
    detail = load("candidateDetail")
    for t in load("themes"):
        for e in t["examples"]:
            assert e["id"] in detail, f"theme {t['id']} example {e['id']} unresolved"


def test_source_urls_are_validly_structured():
    bad = []
    for d in load("candidateDetail").values():
        for e in d["evidence"]:
            url = (e.get("source") or {}).get("url")
            if url and not re.match(r"^https?://[^\s]+$", url):
                bad.append(url)
    assert not bad, f"malformed source urls: {bad[:5]}"


def test_evidence_register_sources_are_urls_or_named_records():
    for r in load("evidenceRegister"):
        assert r["source"].strip()
        assert r["status"] in {"observed", "inferred", "unknown"}
        assert r["tier"].strip()


# ------------------------------------------------------- canonical numbers
def test_summary_matches_canonical_tier_summary():
    tier = json.loads((ROOT / "outputs" / "tier_summary.json").read_text())
    s = load("summary")
    assert s["tierA"] == tier["by_queue"]["tier_a"]
    assert s["tierB"] == tier["by_queue"]["tier_b"]
    assert s["tierC"] == tier["by_queue"]["tier_c"]
    assert s["frontier"] == tier["by_queue"]["frontier"]
    assert s["actionableUniverse"] == s["tierA"] + s["tierB"] + s["frontier"]


def test_summary_candidate_count_matches_export():
    canonical = json.loads((ROOT / "outputs" / "candidates.json").read_text())
    assert load("summary")["candidates"] == len(canonical["candidates"])
    assert len(load("candidates")) == len(canonical["candidates"])


def test_armada_recommendation_is_unchanged():
    assert load("armada")["recommendation"]["verdict"] == "HOLD — NEED MORE EVIDENCE"


def test_armada_federal_awards_reconcile():
    gov = load("armada")["government"]
    assert sum(a["amount"] for a in gov["awards"]) == gov["total"] == 2_972_287


def test_navy_contract_modifications_reconcile():
    gov = load("armada")["government"]
    assert sum(m["amount"] for m in gov["navyModifications"]) == 1_998_926
    actions = " ".join(m["action"] for m in gov["navyModifications"]).lower()
    assert "exercise an option" in actions
    assert "clin 0004" in actions


def test_procurement_numbers_match_the_audit():
    audit = json.loads((ROOT / "outputs" / "armada_procurement_audit.json").read_text())
    p = load("armada")["procurement"]
    assert p["contracts"] == audit["n_contracts"] == 87
    assert p["totalObserved"] == audit["total_observed"]
    assert p["narrow"]["annualised"] == audit["narrow_addressable"]["annualised"]
    assert p["broad"]["annualised"] == audit["broad_adjacency"]["annualised"]
    assert p["excluded"]["n"] == 2


def test_procurement_buckets_sum_to_total():
    p = load("armada")["procurement"]
    assert abs(sum(b["value"] for b in p["buckets"]) - p["totalObserved"]) < 1


def test_model_outputs_match_the_canonical_model():
    from ofr.models.armada_underwriting import compute_python_check
    canonical = compute_python_check()
    m = load("armada")["model"]
    assert m["base"]["total_revenue"] == canonical["total_revenue"] == 22_050_000
    assert m["base"]["gap"] == canonical["gap"] == 7_950_000
    assert m["base"]["reaches_scale"] is False


def test_model_assumptions_are_labelled():
    for a in load("armada")["model"]["assumptions"]:
        assert a["type"] in {"ASSUMPTION", "OBSERVED-anchored"}
        assert a["note"].strip()


# ------------------------------------------------------------ safety rails
def test_no_absolute_local_paths_in_frontend_data():
    for p in DATA.glob("*.json"):
        text = p.read_text()
        assert "/Users/" not in text, f"{p.name} leaks an absolute path"
        assert str(ROOT) not in text, f"{p.name} leaks the repo root"


def test_no_secrets_in_frontend_data():
    pats = [r"sk-[A-Za-z0-9]{20}", r"api[_-]?key\s*[=:]\s*\S", r"BEGIN [A-Z ]*PRIVATE KEY"]
    for p in DATA.glob("*.json"):
        text = p.read_text()
        for pat in pats:
            assert not re.search(pat, text, re.IGNORECASE), f"{p.name} matches {pat}"


def test_no_unresolved_placeholders():
    for p in DATA.glob("*.json"):
        assert "{{" not in p.read_text(), f"{p.name} has an unresolved placeholder"


def test_unknown_placeholder_is_a_hard_error():
    with pytest.raises(bfd.ExportError, match="unknown placeholder"):
        bfd.resolve("value is {{not_a_real_token}}", {"real": "1"})


def test_validation_catches_a_changed_recommendation(bundle):
    tampered = json.loads(json.dumps({k: v for k, v in bundle.items()}))
    tampered["armada"]["recommendation"]["verdict"] = "ADVANCE"
    errs = bfd.validate(tampered)
    assert any("recommendation changed" in e for e in errs)


def test_validation_catches_a_changed_procurement_count(bundle):
    tampered = json.loads(json.dumps({k: v for k, v in bundle.items()}))
    tampered["armada"]["procurement"]["contracts"] = 999
    errs = bfd.validate(tampered)
    assert any("procurement contract count changed" in e for e in errs)


def test_no_grant_is_labelled_commercial_traction():
    gov = load("armada")["government"]
    note = gov["note"].lower()
    assert "not commercial product revenue" in note or "not commercial" in note
    blob = json.dumps(load("armada")).lower()
    assert "commercial traction" not in blob


def test_frontier_is_labelled_as_research_priority_not_investment_score():
    f = load("frontier")
    for s in f["signals"]:
        assert s["priorityMax"] == 12, "frontier uses its own scale"
    blob = json.dumps(f).lower()
    assert "investment score" not in blob


# ------------------------------------------------- presentation data quality
def test_person_name_variants_are_merged():
    """Federal award data and curated sources use different name forms for the
    same person ('Jeff' vs 'Jeffrey'), which surfaced as duplicate UI rows."""
    people = load("candidateDetail")["armada-marine-robotics"]["people"]
    names = [p["name"] for p in people]
    assert len(names) == len(set(names)), f"duplicate people: {names}"
    surnames = [n.split()[-1].lower() for n in names]
    assert len(surnames) == len(set(surnames)), f"unmerged name variants: {names}"


def test_merge_people_unions_roles():
    merged = bfd._merge_people([
        {"name": "Jeff Kaeli", "role": "Co-founder", "role_type": None, "affiliation": None},
        {"name": "Jeffrey Kaeli", "role": "Principal Investigator", "role_type": None, "affiliation": None},
    ])
    assert len(merged) == 1
    assert merged[0]["name"] == "Jeffrey Kaeli"          # longest form kept
    assert "Co-founder" in merged[0]["role"]
    assert "Principal Investigator" in merged[0]["role"]


def test_summary_claim_prefers_an_informative_record():
    """A terse procurement description must not become the candidate summary."""
    ev = [
        {"observed_claim": "Federal award N123 from Navy: SBIR PHASE 1.",
         "evidence_date": "2026-01-01", "value": 1_000_000},
        {"observed_claim": "SBIR Phase II award: External Payload Deployment System for "
                           "Cylindrical UUVs, characterising placement accuracy.",
         "evidence_date": "2023-01-30", "value": 999_028},
    ]
    picked = bfd._summary_claim(ev)
    assert "External Payload Deployment" in picked["observed_claim"]


def test_no_candidate_summary_is_a_contentless_phase_label():
    """Short award titles are fine — some real awards are acronyms like "HAMSS".
    What must not happen is a summary carrying no title at all, e.g.
    "Federal award N123 from Navy: SBIR PHASE 1."."""
    bad = []
    for cid, d in load("candidateDetail").items():
        claim = (d.get("strongestEvidence") or "").strip()
        if not claim:
            continue
        tail = claim.split(":", 1)[-1].strip()
        if bfd._TERSE.match(tail):
            bad.append((cid, claim))
    assert not bad, f"candidates summarised by a contentless label: {bad[:5]}"
