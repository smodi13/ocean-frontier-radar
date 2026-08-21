"""Conservative entity resolution.

The same opportunity can appear as a university project, an NSF grant, an SBIR
company, a professor, a spinout and a licensing announcement. Linking those is
valuable; merging them wrongly destroys evidence.

RULE: a merge requires EXPLICIT, EXPLAINABLE evidence — an identical
normalised company name, a shared website domain, or a shared federal award
identifier. Semantic or fuzzy similarity NEVER merges anything; it can only
create a `possible_relationship` row for an analyst to adjudicate.

Every merge is written to `merge_log` with its basis.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ofr import db

MERGE_BASES = ("identical_normalized_name", "shared_website_domain", "shared_award_id")


def _domain(url: str | None) -> str | None:
    if not url:
        return None
    u = url if "://" in url else f"http://{url}"
    host = (urlparse(u).netloc or "").lower().lstrip("www.")
    if not host or "." not in host:
        return None
    # Generic hosts are not identity evidence.
    if host in {"linkedin.com", "facebook.com", "twitter.com", "x.com", "github.com"}:
        return None
    return host


def _award_ids(conn, cid: str) -> set[str]:
    out = set()
    for r in conn.execute("SELECT analyst_notes FROM evidence WHERE candidate_id=?", (cid,)):
        note = r["analyst_notes"] or ""
        m = re.search(r"(?:contract|nsf_award_id)=([A-Za-z0-9\-]+)", note)
        if m and len(m.group(1)) > 4:
            out.add(m.group(1))
    return out


def find_merges(conn) -> list[tuple[str, str, str]]:
    """Return (keep_id, merge_id, basis) triples justified by hard evidence."""
    rows = conn.execute(
        "SELECT candidate_id,name,website,candidate_type,date_first_seen FROM candidates").fetchall()

    by_name: dict[str, list] = defaultdict(list)
    by_domain: dict[str, list] = defaultdict(list)
    for r in rows:
        by_name[db.normalize_name(r["name"])].append(r)
        d = _domain(r["website"])
        if d:
            by_domain[d].append(r)

    merges: list[tuple[str, str, str]] = []
    seen_pairs = set()

    def _record(group, basis):
        if len(group) < 2:
            return
        # Keep the earliest-seen record as canonical; deterministic tiebreak.
        ordered = sorted(group, key=lambda r: (r["date_first_seen"], r["candidate_id"]))
        keep = ordered[0]["candidate_id"]
        for other in ordered[1:]:
            pair = (keep, other["candidate_id"])
            if pair in seen_pairs or keep == other["candidate_id"]:
                continue
            seen_pairs.add(pair)
            merges.append((keep, other["candidate_id"], basis))

    for name, group in by_name.items():
        if name:
            _record(group, "identical_normalized_name")
    for dom, group in by_domain.items():
        _record(group, "shared_website_domain")
    return merges


def apply_merges(conn, merges=None, verbose=True) -> int:
    merges = merges if merges is not None else find_merges(conn)
    applied = 0
    for keep, drop, basis in merges:
        if basis not in MERGE_BASES:
            raise ValueError(f"Refusing merge with unexplainable basis: {basis!r}")
        if keep == drop:
            continue
        if not conn.execute("SELECT 1 FROM candidates WHERE candidate_id=?", (drop,)).fetchone():
            continue
        for table in ("evidence", "people", "taxonomy_links", "flags",
                      "analyst_views", "classifications", "prioritization"):
            try:
                conn.execute(f"UPDATE OR IGNORE {table} SET candidate_id=? WHERE candidate_id=?",
                             (keep, drop))
            except Exception:
                pass
        conn.execute("DELETE FROM candidates WHERE candidate_id=?", (drop,))
        conn.execute(
            "INSERT OR REPLACE INTO merge_log (merge_id,kept_id,merged_id,basis,merged_at) "
            "VALUES (?,?,?,?,?)",
            (db.stable_id("mrg", keep, drop), keep, drop, basis, db.now()))
        applied += 1
    conn.commit()
    if verbose:
        print(f"[entity] merges applied={applied}")
    return applied


def find_possible_relationships(conn, verbose=True) -> int:
    """Soft links only. These are flagged for review, never merged."""
    rows = conn.execute(
        "SELECT candidate_id,name,institution,company FROM candidates").fetchall()

    # 1. Shared person across candidates -> possible spinout / shared team.
    people = defaultdict(list)
    for r in conn.execute("SELECT candidate_id,name FROM people"):
        people[db.normalize_name(r["name"])].append(r["candidate_id"])

    added = 0
    for pname, cids in people.items():
        uniq = sorted(set(cids))
        if len(uniq) < 2 or not pname:
            continue
        for i in range(len(uniq)):
            for j in range(i + 1, len(uniq)):
                conn.execute(
                    """INSERT OR IGNORE INTO possible_relationships
                       (candidate_id_a,candidate_id_b,relationship,basis,confidence)
                       VALUES (?,?,?,?,?)""",
                    (uniq[i], uniq[j], "shares_person",
                     f"Both records list a person normalising to '{pname}'.", "medium"))
                added += 1

    # 2. A company whose research institution matches another record's institution.
    inst = defaultdict(list)
    for r in rows:
        if r["institution"]:
            inst[db.normalize_name(r["institution"])].append(r["candidate_id"])
    for iname, cids in inst.items():
        uniq = sorted(set(cids))
        if len(uniq) < 2 or len(uniq) > 12:   # skip huge university clusters as noise
            continue
        for i in range(len(uniq)):
            for j in range(i + 1, len(uniq)):
                conn.execute(
                    """INSERT OR IGNORE INTO possible_relationships
                       (candidate_id_a,candidate_id_b,relationship,basis,confidence)
                       VALUES (?,?,?,?,?)""",
                    (uniq[i], uniq[j], "shares_institution",
                     f"Both records list institution '{iname}'.", "low"))
                added += 1
    conn.commit()
    if verbose:
        n = conn.execute("SELECT COUNT(*) n FROM possible_relationships").fetchone()["n"]
        print(f"[entity] possible_relationships={n}")
    return added


if __name__ == "__main__":
    conn = db.connect()
    apply_merges(conn)
    find_possible_relationships(conn)
