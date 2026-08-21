"""Database access and deterministic identity for Ocean Frontier Radar."""
from __future__ import annotations

import hashlib
import os
import re
import sqlite3
import unicodedata
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = ROOT / "data" / "ocean_frontier.db"
SCHEMA = Path(__file__).resolve().parent / "schema.sql"


# --------------------------------------------------------------- identity
_SLUG_RE = re.compile(r"[^a-z0-9]+")

# Legal suffixes are stripped before slugging so "ARMADA Marine Robotics" and
# "Armada Marine Robotics, Inc." resolve to the same candidate_id.
_LEGAL_SUFFIXES = (
    "incorporated", "inc", "llc", "l l c", "ltd", "limited", "corp",
    "corporation", "co", "company", "lp", "llp", "plc", "gmbh", "pbc", "sa",
)


def normalize_name(name: str) -> str:
    """Casefold, strip accents/punctuation and drop trailing legal suffixes."""
    if not name:
        return ""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    # Collapse dotted acronyms before punctuation is stripped, so "L.L.C." becomes
    # "llc" and is recognised as a legal suffix. Without this, "NEXUMA L.L.C."
    # normalised to "nexuma l l c" and would not match "Nexuma LLC".
    s = re.sub(r"\b(?:[a-z]\.){2,}", lambda m: m.group(0).replace(".", ""), s)
    s = _SLUG_RE.sub(" ", s).strip()
    parts = s.split()
    while parts and parts[-1] in _LEGAL_SUFFIXES:
        parts.pop()
    return " ".join(parts)


def slug(name: str) -> str:
    n = normalize_name(name)
    return _SLUG_RE.sub("-", n).strip("-")


def candidate_id(name: str, kind: str = "") -> str:
    """Deterministic candidate id: same input always yields the same id."""
    base = slug(name)
    if not base:
        base = "unnamed"
    if len(base) > 60:
        base = base[:60].rstrip("-")
    if kind:
        return f"{base}--{slug(kind)}"
    return base


def stable_id(prefix: str, *parts: Any) -> str:
    """Deterministic surrogate id derived from its inputs (no randomness)."""
    payload = "|".join("" if p is None else str(p) for p in parts)
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


# ------------------------------------------------------------------ dates
def normalize_date(value: Any) -> str | None:
    """Return ISO YYYY-MM-DD, or None. Never invents a date it cannot parse."""
    if value is None:
        return None
    if isinstance(value, (date, datetime)):
        return value.strftime("%Y-%m-%d")
    s = str(value).strip()
    if not s:
        return None
    fmts = ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%d %b %Y", "%b %d, %Y",
            "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%y")
    for f in fmts:
        try:
            return datetime.strptime(s, f).strftime("%Y-%m-%d")
        except ValueError:
            continue
    m = re.match(r"^(\d{4})$", s)          # bare year -> Jan 1, flagged by caller
    if m:
        return f"{m.group(1)}-01-01"
    m = re.match(r"^(\d{4})-(\d{2})$", s)
    if m:
        return f"{s}-01"
    return None


def today() -> str:
    return date.today().strftime("%Y-%m-%d")


def now() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


# --------------------------------------------------------------- connection
def connect(path: os.PathLike | str | None = None) -> sqlite3.Connection:
    p = Path(path) if path else DEFAULT_DB
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA.read_text())
    conn.commit()


# ------------------------------------------------------------- upsert helpers
# All writes are idempotent so ingestion can be re-run without duplicating.
def upsert_source(conn, *, source_id, url, title, publisher, source_type,
                  source_quality, publication_date, accessed_at,
                  retrieval_method=None, raw_ref=None) -> str:
    conn.execute(
        """INSERT INTO sources (source_id,url,title,publisher,source_type,
               source_quality,publication_date,accessed_at,retrieval_method,raw_ref)
           VALUES (?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(source_id) DO UPDATE SET
               url=excluded.url, title=excluded.title, publisher=excluded.publisher,
               source_type=excluded.source_type, source_quality=excluded.source_quality,
               publication_date=excluded.publication_date,
               accessed_at=excluded.accessed_at,
               retrieval_method=excluded.retrieval_method, raw_ref=excluded.raw_ref""",
        (source_id, url, title, publisher, source_type, source_quality,
         publication_date, accessed_at, retrieval_method, raw_ref))
    return source_id


def upsert_candidate(conn, *, cid, name, candidate_type, institution=None,
                     company=None, geography=None, website=None,
                     current_stage=None, company_formed=None,
                     ocean_centrality=None, sourcing_signal=None,
                     first_seen=None) -> str:
    first_seen = first_seen or today()
    conn.execute(
        """INSERT INTO candidates (candidate_id,name,candidate_type,institution,company,
               geography,website,current_stage,company_formed,ocean_centrality,
               sourcing_signal,date_first_seen,date_last_updated)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(candidate_id) DO UPDATE SET
               name=excluded.name,
               candidate_type=excluded.candidate_type,
               -- COALESCE keeps an existing non-null value rather than
               -- letting a later, sparser source blank it out.
               institution=COALESCE(excluded.institution, candidates.institution),
               company=COALESCE(excluded.company, candidates.company),
               geography=COALESCE(excluded.geography, candidates.geography),
               website=COALESCE(excluded.website, candidates.website),
               current_stage=COALESCE(excluded.current_stage, candidates.current_stage),
               company_formed=COALESCE(excluded.company_formed, candidates.company_formed),
               ocean_centrality=COALESCE(excluded.ocean_centrality, candidates.ocean_centrality),
               sourcing_signal=COALESCE(excluded.sourcing_signal, candidates.sourcing_signal),
               date_last_updated=excluded.date_last_updated""",
        (cid, name, candidate_type, institution, company, geography, website,
         current_stage, company_formed, ocean_centrality, sourcing_signal,
         first_seen, today()))
    return cid


def add_evidence(conn, *, candidate_id, source_id, evidence_type, observed_claim,
                 verbatim_quote=None, evidence_date=None, source_date=None,
                 quantitative_value=None, unit=None,
                 extraction_method="structured_field", confidence=None,
                 analyst_notes=None) -> str:
    eid = stable_id("ev", candidate_id, source_id, evidence_type, observed_claim)
    conn.execute(
        """INSERT INTO evidence (evidence_id,candidate_id,source_id,evidence_type,
               observed_claim,verbatim_quote,evidence_date,source_date,
               quantitative_value,unit,extraction_method,confidence,analyst_notes)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(evidence_id) DO UPDATE SET
               observed_claim=excluded.observed_claim,
               evidence_date=excluded.evidence_date,
               quantitative_value=excluded.quantitative_value""",
        (eid, candidate_id, source_id, evidence_type, observed_claim,
         verbatim_quote, evidence_date, source_date, quantitative_value, unit,
         extraction_method, confidence, analyst_notes))
    return eid


def add_person(conn, *, candidate_id, name, role=None, role_type=None,
               affiliation=None, source_id=None) -> str | None:
    if not name or not name.strip():
        return None
    pid = stable_id("pe", candidate_id, normalize_name(name), role or "")
    conn.execute(
        """INSERT INTO people (person_id,candidate_id,name,role,role_type,affiliation,source_id)
           VALUES (?,?,?,?,?,?,?)
           ON CONFLICT(person_id) DO UPDATE SET
               role=COALESCE(excluded.role, people.role),
               role_type=COALESCE(excluded.role_type, people.role_type),
               affiliation=COALESCE(excluded.affiliation, people.affiliation)""",
        (pid, candidate_id, name.strip(), role, role_type, affiliation, source_id))
    return pid


def link_taxonomy(conn, candidate_id, category_id, is_primary=0, rationale=None):
    conn.execute(
        """INSERT INTO taxonomy_links (candidate_id,category_id,is_primary,rationale)
           VALUES (?,?,?,?)
           ON CONFLICT(candidate_id,category_id) DO UPDATE SET
               is_primary=MAX(taxonomy_links.is_primary, excluded.is_primary),
               rationale=COALESCE(excluded.rationale, taxonomy_links.rationale)""",
        (candidate_id, category_id, is_primary, rationale))


def add_flag(conn, candidate_id, flag, rationale=None):
    conn.execute(
        """INSERT INTO flags (candidate_id,flag,rationale) VALUES (?,?,?)
           ON CONFLICT(candidate_id,flag) DO UPDATE SET rationale=excluded.rationale""",
        (candidate_id, flag, rationale))


def log_ingest(conn, *, run_id, module, started_at, finished_at=None,
               records_seen=0, records_kept=0, status="ok", message=None):
    conn.execute(
        """INSERT INTO ingest_log (run_id,module,started_at,finished_at,
               records_seen,records_kept,status,message) VALUES (?,?,?,?,?,?,?,?)""",
        (run_id, module, started_at, finished_at, records_seen, records_kept,
         status, message))
