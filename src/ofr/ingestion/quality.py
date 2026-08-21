"""Data-quality guards applied after ingestion.

The SBIR bulk file contains occasional malformed rows where the Company column
holds a person's first name or a fragment. Those are removed and the removal is
logged.

CAUTION (learned the hard way): `normalize_name` strips legal suffixes, so
"NATRX INC" normalises to "natrx" - five characters, one token. An earlier
version of this guard treated short single tokens as junk and deleted real
companies (NATRX, Giner, UES). The presence of a legal suffix in the ORIGINAL
name is positive evidence that the row is an organisation, so it is checked
before any length heuristic applies.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ofr import db

JUNK_EXACT = {"steve", "n a", "na", "none", "unknown", "test", "tbd", "x", "tba"}
_LEGAL_MARKER = re.compile(
    r"\b(inc|incorporated|llc|l\.?l\.?c|ltd|limited|corp|corporation|co|company|"
    r"lp|llp|plc|gmbh|pbc|s\.?a|technologies|systems|labs?|research|group)\b\.?",
    re.IGNORECASE)


def is_junk_name(name: str) -> bool:
    raw = (name or "").strip()
    if not raw:
        return True
    normalized = db.normalize_name(raw)
    if normalized in JUNK_EXACT:
        return True
    # A legal/organisational marker in the raw name means this is an entity,
    # regardless of how short the remainder is after suffix stripping.
    if _LEGAL_MARKER.search(raw):
        return False
    if len(normalized) < 3:
        return True
    # No organisational marker AND a single short token -> almost certainly a
    # fragment or a person's first name.
    if len(normalized.split()) == 1 and len(normalized) < 5:
        return True
    return False


_EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def sanitize_website(url: str | None) -> str | None:
    """Strip email addresses out of the website field.

    Some SBIR rows put a contact address in the Company Website column, e.g.
    "http://www.df-nn.com/info@df-nn.com". Storing contact details as a URL is
    both wrong and an unnecessary way to hold personal/contact data, so the
    address is removed and only the site portion is kept.
    """
    if not url:
        return None
    cleaned = _EMAIL.sub("", url).rstrip("/ ")
    # Whatever survives must still look like a host, not a bare scheme.
    host = re.sub(r"^[a-z]+:/*", "", cleaned, flags=re.IGNORECASE).strip("/ ")
    if not host or "." not in host:
        return None
    return cleaned


def sanitize_websites(conn, verbose: bool = True) -> int:
    n = 0
    for r in conn.execute("SELECT candidate_id, website FROM candidates "
                          "WHERE website IS NOT NULL").fetchall():
        clean = sanitize_website(r["website"])
        if clean != r["website"]:
            conn.execute("UPDATE candidates SET website=? WHERE candidate_id=?",
                         (clean, r["candidate_id"]))
            n += 1
    conn.commit()
    if verbose:
        print(f"[quality] sanitized {n} website fields containing contact addresses")
    return n


def purge(conn, verbose: bool = True) -> list[str]:
    removed = []
    for r in conn.execute("SELECT candidate_id, name FROM candidates").fetchall():
        if is_junk_name(r["name"]):
            conn.execute("DELETE FROM candidates WHERE candidate_id=?", (r["candidate_id"],))
            removed.append(r["name"])
    conn.commit()
    if verbose:
        print(f"[quality] removed {len(removed)} malformed candidate names: {removed[:10]}")
    return removed


if __name__ == "__main__":
    conn = db.connect(); purge(conn); sanitize_websites(conn)
