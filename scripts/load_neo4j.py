#!/usr/bin/env python3
"""
load_neo4j.py — Load data from SQLite (data/catalog/huayan.db) into Neo4j.

Three operating modes:
  1. Default:  Connect to neo4j://localhost:7687 and load all data.
  2. --generate:  Output Cypher statements to stdout for manual import.
  3. --verify:    Run validation Cypher queries against a running Neo4j instance.

Usage:
  python scripts/load_neo4j.py                          # load to local Neo4j
  python scripts/load_neo4j.py --generate > import.cypher  # dump Cypher
  python scripts/load_neo4j.py --verify                   # validate existing data
  python scripts/load_neo4j.py --uri bolt://host:7687 --user neo4j --password secret

Data sources (read from SQLite):
  - persons         →  (:Person)  nodes
  - locations       →  (:Location) nodes
  - lineage_edges   →  [:MASTER_OF|INFLUENCED|CONTEMPORARY|MASTER|INFLUENCE]
                       relationships between (:Person) nodes

Edge references (e.g. 'person_042') are mapped to persons.id integers.
Non-numeric references (e.g. 'person_000a', 'person_f01') are skipped with
a warning because they have no corresponding row in the persons table.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import textwrap
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQLITE_DB = PROJECT_ROOT / "data" / "catalog" / "huayan.db"

# Person columns read from SQLite → Neo4j node properties.
# (person_id is a synthetic key derived from the integer PK; see _format_person_ref.)
PERSON_COLUMNS = [
    "name_zh",
    "type",
    "birth_year",
    "death_year",
    "dynasty",
    "biography",
    "lineage_branch",
    "lineage_order",
    "verified",
]

LOCATION_COLUMNS = [
    "name_zh",
    "lat",
    "lng",
    "type",
    "dynasty",
    "description",
]

# Relationship types in lineage_edges.relation are used as-is for the Neo4j
# relationship type (uppercase, underscores allowed).
VALID_RELATIONS = {"MASTER_OF", "INFLUENCED", "CONTEMPORARY", "MASTER", "INFLUENCE"}

# Validation queries run by --verify mode.
VALIDATION_QUERIES = {
    "isolated_persons": """
        // Persons with no relationships at all
        MATCH (p:Person)
        WHERE NOT (p)-[]-()
        RETURN p.name_zh AS name, p.dynasty AS dynasty
        ORDER BY dynasty, name
    """,
    "huayan_five_patriarchs_chain": """
        // Verify 华严五祖 lineage chain from 杜顺 to 宗密
        MATCH path = (a:Person {name_zh: '杜顺'})-[:MASTER_OF|INFLUENCED*1..10]->(b:Person {name_zh: '宗密'})
        RETURN length(path) AS hops
    """,
    "duplicate_names": """
        // Persons sharing the same name_zh
        MATCH (p:Person)
        WITH p.name_zh AS name, collect(p) AS nodes
        WHERE size(nodes) > 1
        RETURN name, size(nodes) AS duplicates
        ORDER BY duplicates DESC
    """,
    "relation_counts": """
        // Count of each relationship type
        MATCH ()-[r]->()
        RETURN type(r) AS relation, count(*) AS cnt
        ORDER BY cnt DESC
    """,
    "dynasty_distribution": """
        // Persons per dynasty
        MATCH (p:Person)
        RETURN p.dynasty AS dynasty, count(*) AS cnt
        ORDER BY cnt DESC
    """,
    "location_summary": """
        // Location counts by type
        MATCH (l:Location)
        RETURN l.type AS type, count(*) AS cnt
        ORDER BY cnt DESC
    """,
    "node_counts": """
        // Total node counts
        MATCH (n)
        RETURN labels(n)[0] AS label, count(*) AS cnt
        ORDER BY cnt DESC
    """,
    "unmatched_edge_refs": """
        // Edge references that resolved to a Person node
        // (If load skipped any, they are logged during import.)
        MATCH ()-[r]->()
        RETURN type(r) AS relation, count(*) AS cnt
        ORDER BY cnt DESC
    """,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _format_person_ref(person_id: int) -> str:
    """Convert integer PK to the TEXT reference format used in edges.

    >>> _format_person_ref(42)
    'person_042'
    >>> _format_person_ref(7)
    'person_007'
    """
    return f"person_{person_id:03d}"


def _parse_person_ref(ref: str) -> Optional[int]:
    """Extract integer ID from an edge reference like 'person_042'.

    Returns None for non-numeric / non-standard references.
    """
    if not ref.startswith("person_"):
        return None
    num_part = ref[len("person_"):]
    if not num_part.isdigit():
        return None
    return int(num_part)


def _sanitize_cypher_value(value) -> str:
    """Format a Python value as a Cypher literal."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    # String — escape single quotes and backslashes for Cypher
    s = str(value)
    s = s.replace("\\", "\\\\")
    s = s.replace("'", "\\'")
    return f"'{s}'"


def _cypher_props(props: dict) -> str:
    """Format a dict as a Cypher property map literal.

    >>> _cypher_props({"name_zh": "杜顺", "birth_year": 557})
    "{name_zh: '杜顺', birth_year: 557}"
    """
    items = []
    for k, v in props.items():
        if v is None:
            continue  # skip nulls for cleaner output
        items.append(f"{k}: {_sanitize_cypher_value(v)}")
    return "{" + ", ".join(items) + "}"


# ---------------------------------------------------------------------------
# Data extraction from SQLite
# ---------------------------------------------------------------------------

def read_sqlite_data(db_path: Path) -> tuple[list[dict], list[dict], list[dict]]:
    """Read persons, lineage_edges, and locations from the SQLite database.

    Returns:
        (persons, edges, locations) — each a list of dicts keyed by column name.
    """
    if not db_path.exists():
        print(f"[ERROR] SQLite database not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # --- Persons ---
    columns = ["id", "source_id"] + PERSON_COLUMNS
    cursor.execute(f"SELECT {', '.join(columns)} FROM persons ORDER BY id")
    persons = [dict(row) for row in cursor.fetchall()]

    # --- Edges ---
    cursor.execute(
        "SELECT id, from_person_id, to_person_id, relation, lineage_name, note "
        "FROM lineage_edges ORDER BY id"
    )
    edges = [dict(row) for row in cursor.fetchall()]

    # --- Locations ---
    columns = ["id"] + LOCATION_COLUMNS
    cursor.execute(f"SELECT {', '.join(columns)} FROM locations ORDER BY id")
    locations = [dict(row) for row in cursor.fetchall()]

    conn.close()

    print(f"[SQLite] Read {len(persons)} persons, {len(edges)} edges, "
          f"{len(locations)} locations from {db_path.name}",
          file=sys.stderr)
    return persons, edges, locations


# ---------------------------------------------------------------------------
# Edge resolution
# ---------------------------------------------------------------------------

def resolve_edges(
    edges: list[dict], person_id_to_data: dict[int, dict],
    source_id_to_data: dict[str, dict],
) -> tuple[list[dict], list[str]]:
    """Map from_person_id / to_person_id TEXT refs to person data.

    Tries integer PK lookup first, then source_id lookup (e.g. 'person_001').

    Returns:
        (resolved_edges, warnings) — resolved_edges are those where both
        from and to resolve to a known person.  Warnings describe skipped edges.
    """
    resolved: list[dict] = []
    warnings: list[str] = []

    for edge in edges:
        from_ref = edge["from_person_id"]
        to_ref = edge["to_person_id"]

        # Resolve from
        from_data = None
        from_int = _parse_person_ref(from_ref)
        if from_int is not None and from_int in person_id_to_data:
            from_data = person_id_to_data[from_int]
        elif from_ref in source_id_to_data:
            from_data = source_id_to_data[from_ref]

        # Resolve to
        to_data = None
        to_int = _parse_person_ref(to_ref)
        if to_int is not None and to_int in person_id_to_data:
            to_data = person_id_to_data[to_int]
        elif to_ref in source_id_to_data:
            to_data = source_id_to_data[to_ref]

        if from_data is None:
            warnings.append(
                f"  SKIP edge #{edge['id']}: from_person_id={from_ref} not found"
            )
            continue

        if to_data is None:
            warnings.append(
                f"  SKIP edge #{edge['id']}: to_person_id={to_ref} not found"
            )
            continue

        relation = edge["relation"].strip().upper()
        if relation not in VALID_RELATIONS:
            warnings.append(
                f"  WARN edge #{edge['id']}: unknown relation type '{relation}', "
                f"using as-is"
            )

        resolved.append({
            "from_ref": from_data["source_id"],
            "to_ref": to_data["source_id"],
            "relation": relation,
            "lineage_name": edge.get("lineage_name"),
            "note": edge.get("note"),
        })

    return resolved, warnings


# ---------------------------------------------------------------------------
# Mode: --generate  (Cypher to stdout)
# ---------------------------------------------------------------------------

def _build_person_props(p: dict) -> dict:
    """Extract Neo4j-worthy properties from a person row."""
    person_ref = _format_person_ref(p["id"])
    props: dict[str, object] = {"person_id": person_ref}
    for col in PERSON_COLUMNS:
        v = p.get(col)
        if v is not None:
            props[col] = v
    return props


def generate_cypher(
    persons: list[dict],
    resolved_edges: list[dict],
    locations: list[dict],
) -> str:
    """Produce a self-contained Cypher script for manual import."""

    lines: list[str] = []
    lines.append("// ============================================================")
    lines.append("// Auto-generated Cypher import script")
    lines.append(f"//   {len(persons)} Person nodes")
    lines.append(f"//   {len(resolved_edges)} relationships")
    lines.append(f"//   {len(locations)} Location nodes")
    lines.append("// ============================================================")
    lines.append("")

    # --- Person nodes ---
    lines.append("// ── Persons ────────────────────────────────────────────────")
    lines.append("")
    for p in persons:
        props = _build_person_props(p)
        lines.append(f"CREATE (:Person {_cypher_props(props)});")
    lines.append("")

    # --- Location nodes ---
    lines.append("// ── Locations ──────────────────────────────────────────────")
    lines.append("")
    for loc in locations:
        props: dict[str, object] = {}
        for col in LOCATION_COLUMNS:
            v = loc.get(col)
            if v is not None:
                props[col] = v
        lines.append(f"CREATE (:Location {_cypher_props(props)});")
    lines.append("")

    # --- Relationships ---
    lines.append("// ── Relationships ─────────────────────────────────────────")
    lines.append("")
    for edge in resolved_edges:
        rel_props: dict[str, object] = {}
        if edge.get("lineage_name"):
            rel_props["lineage_name"] = edge["lineage_name"]
        if edge.get("note"):
            rel_props["note"] = edge["note"]

        prop_str = _cypher_props(rel_props)
        lines.append(
            f"MATCH (a:Person {{person_id: '{edge['from_ref']}'}}), "
            f"(b:Person {{person_id: '{edge['to_ref']}'}})\n"
            f"CREATE (a)-[:{edge['relation']} {prop_str}]->(b);"
        )
        lines.append("")

    lines.append("// ── End of import ─────────────────────────────────────────")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Mode: default — load into running Neo4j
# ---------------------------------------------------------------------------

def _try_import_neo4j():
    """Attempt to import the neo4j driver; return module or None with message."""
    try:
        from neo4j import GraphDatabase  # noqa: F401
        return GraphDatabase
    except ImportError:
        print(
            "[ERROR] The 'neo4j' Python driver is not installed.\n"
            "        Install it with:  pip install neo4j\n"
            "        Or use --generate to output Cypher for manual import.",
            file=sys.stderr,
        )
        return None


def _neo4j_person_params(p: dict) -> dict:
    """Build a parameter dict for a Person node."""
    person_ref = _format_person_ref(p["id"])
    params: dict[str, object] = {"person_id": person_ref}
    for col in PERSON_COLUMNS:
        v = p.get(col)
        if v is not None:
            params[col] = v
    return params


def load_to_neo4j(
    persons: list[dict],
    resolved_edges: list[dict],
    locations: list[dict],
    uri: str,
    user: str,
    password: str,
    database: str = "neo4j",
) -> int:
    """Load all data into a running Neo4j instance.

    Returns the number of errors (0 = success).
    """
    GraphDatabase = _try_import_neo4j()
    if GraphDatabase is None:
        return 1

    print(f"[Neo4j] Connecting to {uri} …", file=sys.stderr)
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("[Neo4j] Connection verified.", file=sys.stderr)
    except Exception as exc:
        print(f"[ERROR] Cannot connect to Neo4j at {uri}: {exc}", file=sys.stderr)
        return 1

    error_count = 0

    def _run(tx, cypher: str, params: dict | None = None):
        """Thin wrapper that runs a Cypher statement inside a transaction."""
        result = tx.run(cypher, params or {})
        return result.consume()

    try:
        with driver.session(database=database) as session:
            # --- Clear existing data ---
            print("[Neo4j] Clearing existing graph data …", file=sys.stderr)
            session.execute_write(
                _run,
                "MATCH (n) DETACH DELETE n",
            )

            # --- Create indexes ---
            print("[Neo4j] Creating indexes …", file=sys.stderr)
            session.execute_write(
                _run,
                "CREATE INDEX IF NOT EXISTS FOR (p:Person) ON (p.person_id)",
            )
            session.execute_write(
                _run,
                "CREATE INDEX IF NOT EXISTS FOR (p:Person) ON (p.name_zh)",
            )

            # --- Load Persons ---
            print(f"[Neo4j] Loading {len(persons)} persons …", file=sys.stderr)
            person_params_list = [_neo4j_person_params(p) for p in persons]
            session.execute_write(
                _run,
                textwrap.dedent("""\
                    UNWIND $rows AS row
                    CREATE (p:Person)
                    SET p = row
                """),
                {"rows": person_params_list},
            )

            # --- Load Locations ---
            print(f"[Neo4j] Loading {len(locations)} locations …", file=sys.stderr)
            loc_params_list: list[dict[str, object]] = []
            for loc in locations:
                props: dict[str, object] = {}
                for col in LOCATION_COLUMNS:
                    v = loc.get(col)
                    if v is not None:
                        props[col] = v
                loc_params_list.append(props)
            session.execute_write(
                _run,
                textwrap.dedent("""\
                    UNWIND $rows AS row
                    CREATE (l:Location)
                    SET l = row
                """),
                {"rows": loc_params_list},
            )

            # --- Load Relationships ---
            print(f"[Neo4j] Loading {len(resolved_edges)} relationships …",
                  file=sys.stderr)
            edge_params_list: list[dict[str, object]] = []
            for edge in resolved_edges:
                eparams: dict[str, object] = {
                    "from_ref": edge["from_ref"],
                    "to_ref": edge["to_ref"],
                }
                if edge.get("lineage_name"):
                    eparams["lineage_name"] = edge["lineage_name"]
                if edge.get("note"):
                    eparams["note"] = edge["note"]
                eparams["_relation"] = edge["relation"]
                edge_params_list.append(eparams)

            # We iterate per row because relationship type cannot be
            # parameterised in Cypher.
            for ep in edge_params_list:
                rel_type = ep.pop("_relation")
                cypher = (
                    f"MATCH (a:Person {{person_id: $from_ref}}), "
                    f"(b:Person {{person_id: $to_ref}}) "
                    f"CREATE (a)-[:{rel_type}]->(b)"
                )
                # Add relationship properties if present
                rel_payload = {}
                for k in ("lineage_name", "note"):
                    if k in ep:
                        rel_payload[k] = ep[k]

                if rel_payload:
                    # Add properties in a SET clause after CREATE
                    cypher = (
                        f"MATCH (a:Person {{person_id: $from_ref}}), "
                        f"(b:Person {{person_id: $to_ref}}) "
                        f"CREATE (a)-[r:{rel_type}]->(b) SET r += $props"
                    )
                    session.execute_write(
                        _run, cypher,
                        {"from_ref": ep["from_ref"],
                         "to_ref": ep["to_ref"],
                         "props": rel_payload},
                    )
                else:
                    session.execute_write(
                        _run, cypher, ep,
                    )

            # --- Summary ---
            result = session.execute_write(
                _run,
                "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS cnt "
                "ORDER BY cnt DESC",
            )
            # We cannot easily read the result here because _run returns a summary.
            # Let's do a quick read query.
            print("[Neo4j] Import complete. Node count:", file=sys.stderr)

    except Exception as exc:
        print(f"[ERROR] Neo4j import failed: {exc}", file=sys.stderr)
        error_count += 1
    finally:
        driver.close()

    return error_count


def _quick_summary(uri: str, user: str, password: str, database: str = "neo4j"):
    """Print a quick count summary after loading."""
    GraphDatabase = _try_import_neo4j()
    if GraphDatabase is None:
        return
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session(database=database) as session:
            result = session.run(
                "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS cnt "
                "ORDER BY cnt DESC"
            )
            for record in result:
                print(f"  {record['label']:>12s}: {record['cnt']:4d}", file=sys.stderr)
        driver.close()
    except Exception as exc:
        print(f"[WARN] Could not fetch summary: {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Mode: --verify
# ---------------------------------------------------------------------------

def verify_neo4j(
    uri: str, user: str, password: str, database: str = "neo4j"
) -> int:
    """Run validation Cypher queries against a Neo4j instance.

    Returns the number of queries that produced errors (0 = all clear).
    """
    GraphDatabase = _try_import_neo4j()
    if GraphDatabase is None:
        return 1

    print(f"[Neo4j] Connecting to {uri} for validation …", file=sys.stderr)
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
    except Exception as exc:
        print(f"[ERROR] Cannot connect to Neo4j at {uri}: {exc}", file=sys.stderr)
        return 1

    errors = 0

    try:
        with driver.session(database=database) as session:
            for name, cypher in VALIDATION_QUERIES.items():
                print(f"\n{'─' * 60}")
                print(f"  Query: {name}")
                cleaned = textwrap.dedent(cypher).strip()
                print(f"  Cypher: {cleaned[:100]}{'…' if len(cleaned) > 100 else ''}")
                print(f"{'─' * 60}")

                try:
                    result = session.run(cleaned)
                    records = list(result)
                    if not records:
                        print("  (no results)")
                    else:
                        # Print column headers
                        keys = records[0].keys()
                        header = "  " + " | ".join(keys)
                        print(header)
                        print("  " + "-" * (len(header) - 2))
                        for rec in records:
                            vals = "  " + " | ".join(
                                str(rec[k]) for k in keys
                            )
                            print(vals)
                        print(f"  — {len(records)} row(s)")
                except Exception as exc:
                    print(f"  [ERROR] {exc}")
                    errors += 1

    finally:
        driver.close()

    return errors


# ---------------------------------------------------------------------------
# Mode: --verify-sqlite  (graph validation via SQLite, no Neo4j needed)
# ---------------------------------------------------------------------------

# Graph validation checks — equivalent to Neo4j Cypher queries but using SQL.
SQLITE_CHECKS: list[tuple[str, str, list[tuple[str, ...]]]] = [
    (
        "node_counts",
        "SELECT 'Person' AS label, COUNT(*) AS cnt FROM persons "
        "UNION ALL SELECT 'Location', COUNT(*) FROM locations "
        "UNION ALL SELECT 'LineageEdge', COUNT(*) FROM lineage_edges "
        "UNION ALL SELECT 'PersonLocation', COUNT(*) FROM person_locations "
        "UNION ALL SELECT 'Text', COUNT(*) FROM texts "
        "UNION ALL SELECT 'Chapter', COUNT(*) FROM chapters "
        "UNION ALL SELECT 'GlossaryTerm', COUNT(*) FROM glossary "
        "ORDER BY cnt DESC",
        [],
    ),
    (
        "relation_counts",
        "SELECT relation, COUNT(*) AS cnt FROM lineage_edges "
        "GROUP BY relation ORDER BY cnt DESC",
        [],
    ),
    (
        "isolated_persons",
        "SELECT p.source_id, p.name_zh, p.dynasty FROM persons p "
        "WHERE p.source_id NOT IN (SELECT from_person_id FROM lineage_edges) "
        "AND p.source_id NOT IN (SELECT to_person_id FROM lineage_edges) "
        "ORDER BY p.dynasty, p.name_zh",
        [],
    ),
    (
        "orphan_edges",
        "SELECT e.id, e.from_person_id, e.to_person_id, e.relation "
        "FROM lineage_edges e "
        "LEFT JOIN persons pf ON e.from_person_id = pf.source_id "
        "LEFT JOIN persons pt ON e.to_person_id = pt.source_id "
        "WHERE pf.source_id IS NULL OR pt.source_id IS NULL "
        "ORDER BY e.id",
        [],
    ),
    (
        "huayan_five_patriarchs_chain",
        "WITH RECURSIVE chain AS ("
        "  SELECT from_person_id, to_person_id, 1 AS depth "
        "  FROM lineage_edges "
        "  WHERE from_person_id = 'person_001' "
        "  UNION ALL "
        "  SELECT e.from_person_id, e.to_person_id, c.depth + 1 "
        "  FROM lineage_edges e JOIN chain c ON e.from_person_id = c.to_person_id "
        "  WHERE c.depth < 10 "
        ") "
        "SELECT depth, from_person_id AS \"from\", to_person_id AS \"to\" "
        "FROM chain WHERE to_person_id = 'person_005' ORDER BY depth",
        [],
    ),
    (
        "dynasty_distribution",
        "SELECT dynasty, COUNT(*) AS cnt FROM persons "
        "WHERE dynasty IS NOT NULL AND dynasty != '' "
        "GROUP BY dynasty ORDER BY cnt DESC",
        [],
    ),
    (
        "person_locations_summary",
        "SELECT relation, COUNT(*) AS cnt FROM person_locations "
        "GROUP BY relation ORDER BY cnt DESC",
        [],
    ),
    (
        "orphan_person_locations",
        "SELECT pl.person_id, pl.location_id "
        "FROM person_locations pl "
        "LEFT JOIN persons p ON pl.person_id = p.id "
        "LEFT JOIN locations l ON pl.location_id = l.id "
        "WHERE p.id IS NULL OR l.id IS NULL",
        [],
    ),
]


def verify_sqlite(db_path: Path) -> int:
    """Run graph validation checks directly against SQLite.

    Returns the number of checks that produced errors or warnings (0 = all clear).
    """
    if not db_path.exists():
        print(f"[ERROR] SQLite database not found: {db_path}", file=sys.stderr)
        return 1

    sys.stdout.reconfigure(encoding="utf-8")
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    errors = 0

    for name, sql, _params in SQLITE_CHECKS:
        print(f"\n{'─' * 60}")
        print(f"  Check: {name}")
        print(f"{'─' * 60}")

        try:
            rows = conn.execute(sql).fetchall()
            if not rows:
                print("  (no results)")
            else:
                keys = list(rows[0].keys())
                header = "  " + " | ".join(keys)
                print(header)
                print("  " + "─" * (len(header) - 2))
                for row in rows:
                    vals = "  " + " | ".join(str(row[k]) for k in keys)
                    print(vals)
                print(f"  — {len(rows)} row(s)")

                # Specific validations
                if name == "orphan_edges" and len(rows) > 0:
                    print(f"  ⚠ {len(rows)} edge(s) reference non-existent persons")
                    errors += 1
                if name == "orphan_person_locations" and len(rows) > 0:
                    print(f"  ⚠ {len(rows)} person_location link(s) reference missing entities")
                    errors += 1
                if name == "isolated_persons":
                    # Informational only — isolated persons are expected
                    print(f"  ℹ {len(rows)} person(s) have no edges (expected for some)")
        except Exception as exc:
            print(f"  [ERROR] {exc}")
            errors += 1

    conn.close()
    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Load SQLite data (huayan.db) into Neo4j.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s                                # load to local Neo4j
              %(prog)s --generate > import.cypher     # dump Cypher script
              %(prog)s --verify                       # validate existing data
              %(prog)s --uri bolt://host:7687 --user neo4j --password pw
        """),
    )

    p.add_argument(
        "--db",
        type=Path,
        default=SQLITE_DB,
        help=f"Path to SQLite database (default: {SQLITE_DB})",
    )
    p.add_argument(
        "--uri",
        default="bolt://localhost:7687",
        help="Neo4j bolt URI (default: bolt://localhost:7687)",
    )
    p.add_argument(
        "--user",
        default="neo4j",
        help="Neo4j username (default: neo4j)",
    )
    p.add_argument(
        "--password",
        default="neo4j",
        help="Neo4j password (default: neo4j)",
    )
    p.add_argument(
        "--database",
        default="neo4j",
        help="Neo4j database name (default: neo4j)",
    )

    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--generate",
        action="store_true",
        help="Output Cypher statements to stdout instead of connecting to Neo4j",
    )
    mode.add_argument(
        "--verify",
        action="store_true",
        help="Run validation queries against a running Neo4j instance",
    )
    mode.add_argument(
        "--verify-sqlite",
        action="store_true",
        help="Run graph validation queries directly against SQLite (no Neo4j needed)",
    )

    return p


def main() -> None:
    args = build_parser().parse_args()

    # ---- Read data from SQLite ----
    persons, edges, locations = read_sqlite_data(args.db)

    # Build lookup for edge resolution (by integer PK and by source_id)
    person_id_to_data: dict[int, dict] = {}
    source_id_to_data: dict[str, dict] = {}
    for p in persons:
        person_id_to_data[p["id"]] = p
        if p.get("source_id"):
            source_id_to_data[p["source_id"]] = p

    resolved_edges, warnings = resolve_edges(edges, person_id_to_data, source_id_to_data)

    for w in warnings:
        print(f"[WARN] {w}", file=sys.stderr)

    print(
        f"[INFO] {len(persons)} persons, {len(resolved_edges)} resolved edges "
        f"(of {len(edges)} total), {len(locations)} locations",
        file=sys.stderr,
    )

    # ---- Dispatch mode ----
    if args.generate:
        cypher = generate_cypher(persons, resolved_edges, locations)
        sys.stdout.reconfigure(encoding="utf-8")
        print(cypher)
        print(
            f"\n[INFO] Cypher script written to stdout. "
            f"Paste into Neo4j Browser or run via cypher-shell.",
            file=sys.stderr,
        )
    elif args.verify:
        errs = verify_neo4j(args.uri, args.user, args.password, args.database)
        if errs:
            print(f"\n[WARN] {errs} validation query(s) had errors.", file=sys.stderr)
            sys.exit(1)
    elif args.verify_sqlite:
        errs = verify_sqlite(args.db)
        if errs:
            print(f"\n[WARN] {errs} validation check(s) failed.", file=sys.stderr)
            sys.exit(1)
    else:
        # Default: load into Neo4j
        errs = load_to_neo4j(
            persons, resolved_edges, locations,
            args.uri, args.user, args.password, args.database,
        )
        if errs:
            print("\n[ERROR] Import completed with errors.", file=sys.stderr)
            sys.exit(1)
        _quick_summary(args.uri, args.user, args.password, args.database)
        print("[OK] Data loaded successfully.", file=sys.stderr)


if __name__ == "__main__":
    main()
