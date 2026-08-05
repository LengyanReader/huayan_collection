#!/usr/bin/env python3
"""
华严项目 — SQLite 数据导入/导出脚本
用法:
  python scripts/export_sqlite_to_json.py --import    # JSON/YAML → SQLite
  python scripts/export_sqlite_to_json.py --export    # SQLite → JSON/YAML
  python scripts/export_sqlite_to_json.py --verify    # 验证数据完整性
"""

import json
import yaml
import sqlite3
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "catalog" / "huayan.db"
GRAPH_PATH = ROOT / "web" / "demo" / "graph.json"
GLOSSARY_PATH = ROOT / "data" / "translation" / "glossary.yaml"
PERSONAS_OUT = ROOT / "data" / "knowledge_graph" / "personas.json"
LINEAGES_OUT = ROOT / "data" / "knowledge_graph" / "lineages.json"
LOCATIONS_OUT = ROOT / "data" / "knowledge_graph" / "locations.json"


def import_graph_to_sqlite():
    """从 graph.json 导入 persons, edges, locations 到 SQLite"""
    with open(GRAPH_PATH, encoding='utf-8') as f:
        graph = json.load(f)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    # --- Import persons ---
    conn.execute("DELETE FROM persons")
    for n in graph['nodes']:
        conn.execute("""
            INSERT INTO persons (source_id, name_zh, type, birth_year, death_year, dynasty,
                                 biography, lineage_branch, verified, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '从graph.json导入')
        """, (
            n['id'],
            n['n'],
            n.get('tp', 'practitioner'),
            n.get('b'),
            n.get('d'),
            n.get('dy', ''),
            n.get('bio', ''),
            n.get('li') if n.get('li') != 'null' else None,
            n.get('v', 0)
        ))

    # --- Import locations ---
    conn.execute("DELETE FROM locations")
    for loc in graph['locations']:
        conn.execute("""
            INSERT INTO locations (name_zh, lat, lng, type, dynasty, description, related_persons, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, '从graph.json导入')
        """, (
            loc['n'],
            loc.get('lat'),
            loc.get('lng'),
            loc.get('tp', 'temple'),
            loc.get('dy', ''),
            loc.get('ds', ''),
            json.dumps(loc.get('ps', []), ensure_ascii=False) if loc.get('ps') else None,
        ))

    # --- Import edges ---
    conn.execute("DELETE FROM lineage_edges")
    for e in graph['edges']:
        conn.execute("""
            INSERT INTO lineage_edges (from_person_id, to_person_id, relation, lineage_name)
            VALUES (?, ?, ?, ?)
        """, (e['s'], e['t'], e.get('r', 'MASTER'), e.get('li', '')))

    conn.commit()

    # Verify
    p_count = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    e_count = conn.execute("SELECT COUNT(*) FROM lineage_edges").fetchone()[0]
    l_count = conn.execute("SELECT COUNT(*) FROM locations").fetchone()[0]
    conn.close()

    print(f"Imported: {p_count} persons | {e_count} edges | {l_count} locations -> {DB_PATH}")
    return p_count, e_count, l_count


def import_glossary_to_sqlite():
    """从 glossary.yaml 导入术语到 SQLite"""
    with open(GLOSSARY_PATH, encoding='utf-8') as f:
        glossary = yaml.safe_load(f)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("DELETE FROM glossary")

    terms = glossary.get('terms', glossary) if isinstance(glossary, dict) else glossary
    if isinstance(terms, dict):
        terms = list(terms.values())

    count = 0
    for t in terms:
        if not isinstance(t, dict):
            continue
        conn.execute("""
            INSERT INTO glossary (term_sa, term_bo, term_zh, term_en, category)
            VALUES (?, ?, ?, ?, 'doctrine')
        """, (
            t.get('sa', ''),
            t.get('bo_wylie', ''),
            t.get('zh', ''),
            t.get('en', '')
        ))
        count += 1

    conn.commit()
    conn.close()
    print(f"Imported: {count} glossary terms → {DB_PATH}")
    return count


def export_sqlite_to_json():
    """从 SQLite 导出 persons, edges, locations 到 JSON"""
    conn = sqlite3.connect(str(DB_PATH))

    # Export persons
    rows = conn.execute("""
        SELECT id, name_zh, type, birth_year, death_year, dynasty, biography,
               lineage_branch, lineage_order, verified, source
        FROM persons ORDER BY id
    """).fetchall()

    persons_list = []
    for r in rows:
        persons_list.append({
            "id": f"person_{r[0]:04d}",
            "name_zh": r[1],
            "type": r[2] or "practitioner",
            "birth_year": r[3],
            "death_year": r[4],
            "dynasty": r[5] or "",
            "biography": r[6] or "",
            "lineage_branch": r[7],
            "lineage_order": r[8],
            "verified": r[9] or 0,
            "source": r[10] or "",
        })

    # Export locations
    loc_rows = conn.execute("""
        SELECT id, name_zh, lat, lng, type, dynasty, description, related_persons, source
        FROM locations ORDER BY id
    """).fetchall()

    locations_list = []
    for r in loc_rows:
        rp = r[7]
        if isinstance(rp, str):
            try:
                rp = json.loads(rp)
            except:
                rp = []
        locations_list.append({
            "id": f"loc_{r[0]:03d}",
            "name_zh": r[1],
            "lat": r[2],
            "lng": r[3],
            "type": r[4] or "temple",
            "dynasty": r[5] or "",
            "description": r[6] or "",
            "related_persons": rp or [],
            "source": r[8] or "",
        })

    # Export edges
    edge_rows = conn.execute("""
        SELECT from_person_id, to_person_id, relation, lineage_name
        FROM lineage_edges ORDER BY id
    """).fetchall()

    edges_list = []
    for r in edge_rows:
        edges_list.append({
            "from": r[0],
            "to": r[1],
            "relation": r[2] or "MASTER",
        })

    # Group edges by lineage
    lineage_map = {}
    for e in edges_list:
        lin = "default"
        for er in edge_rows:
            if er[0] == e['from'] and er[1] == e['to']:
                lin = er[3] or "default"
                break
        if lin not in lineage_map:
            lineage_map[lin] = []
        lineage_map[lin].append(e)

    lineages_output = {
        "version": "0.2.0",
        "lineages": [{"name": k, "edges": v} for k, v in lineage_map.items()]
    }

    # Write outputs
    with open(PERSONAS_OUT, 'w', encoding='utf-8') as f:
        json.dump({"version": "0.2.0", "last_updated": "2026-08-05",
                    "persons": persons_list}, f, ensure_ascii=False, indent=2)
    with open(LINEAGES_OUT, 'w', encoding='utf-8') as f:
        json.dump(lineages_output, f, ensure_ascii=False, indent=2)
    with open(LOCATIONS_OUT, 'w', encoding='utf-8') as f:
        json.dump({"version": "0.2.0", "locations": locations_list}, f, ensure_ascii=False, indent=2)

    conn.close()
    print(f"Exported: {len(persons_list)} persons → {PERSONAS_OUT}")
    print(f"Exported: {len(edges_list)} edges → {LINEAGES_OUT}")
    print(f"Exported: {len(locations_list)} locations → {LOCATIONS_OUT}")

    # Also export updated graph.json for build.py
    with open(GRAPH_PATH, encoding='utf-8') as f:
        old_graph = json.load(f)

    lineage_colors = old_graph.get('lineage_colors', {})

    # Build nodes in old format for compatibility
    nodes_out = []
    for r in rows:
        nodes_out.append({
            "id": f"person_{r[0]:04d}",
            "n": r[1],
            "dy": r[5] or "",
            "ti": "",
            "li": r[7] if r[7] else "null",
            "multi": [],
            "tp": r[2] or "practitioner",
            "b": r[3],
            "d": r[4],
            "bio": (r[6] or "")[:150],
            "wk": [],
            "wl": {},
            "v": r[9] or 0
        })

    locs_out = []
    for r in loc_rows:
        rp = r[7]
        if isinstance(rp, str):
            try: rp = json.loads(rp)
            except: rp = []
        locs_out.append({
            "id": f"loc_{r[0]:03d}",
            "n": r[1],
            "lat": r[2],
            "lng": r[3],
            "tp": r[4] or "temple",
            "dy": r[5] or "",
            "ds": (r[6] or "")[:120],
            "ps": rp or []
        })

    with open(GRAPH_PATH, 'w', encoding='utf-8') as f:
        json.dump({
            "nodes": nodes_out,
            "edges": [{"s": e['from'], "t": e['to'], "r": e['relation'],
                        "li": "default"} for e in edges_list],
            "locations": locs_out,
            "lineage_colors": lineage_colors
        }, f, ensure_ascii=False)
    print(f"Updated: {GRAPH_PATH}")


def verify_data():
    """验证 SQLite 数据完整性"""
    conn = sqlite3.connect(str(DB_PATH))
    print("=" * 50)
    print("  SQLite 数据完整性报告")
    print("=" * 50)

    # Person counts
    p_total = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    p_verified = conn.execute("SELECT COUNT(*) FROM persons WHERE verified=1").fetchone()[0]
    p_null_dates = conn.execute("SELECT COUNT(*) FROM persons WHERE birth_year IS NULL AND death_year IS NULL").fetchone()[0]
    print(f"\nPersons: {p_total} total | {p_verified} verified | {p_null_dates} missing dates")

    # Edge counts
    e_total = conn.execute("SELECT COUNT(*) FROM lineage_edges").fetchone()[0]
    e_rels = conn.execute("""
        SELECT relation, COUNT(*) FROM lineage_edges GROUP BY relation
    """).fetchall()
    print(f"Edges: {e_total} total")
    for rel, cnt in e_rels:
        print(f"  {rel}: {cnt}")

    # Location counts
    l_total = conn.execute("SELECT COUNT(*) FROM locations").fetchone()[0]
    l_no_coords = conn.execute("SELECT COUNT(*) FROM locations WHERE lat IS NULL OR lng IS NULL").fetchone()[0]
    print(f"Locations: {l_total} total | {l_no_coords} missing coordinates")

    # Glossary
    g_total = conn.execute("SELECT COUNT(*) FROM glossary").fetchone()[0]
    print(f"Glossary: {g_total} terms")

    # Isolated persons (no edges) - match on source_id
    isolated = conn.execute("""
        SELECT COUNT(*) FROM persons p
        WHERE NOT EXISTS (SELECT 1 FROM lineage_edges e WHERE e.from_person_id = p.source_id
                          OR e.to_person_id = p.source_id)
    """).fetchone()[0]
    print(f"Connectivity: {isolated} isolated persons (no edges)")

    conn.close()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == '--import':
        print("Importing data → SQLite...")
        import_graph_to_sqlite()
        import_glossary_to_sqlite()
        verify_data()

    elif cmd == '--export':
        print("Exporting SQLite → JSON...")
        export_sqlite_to_json()

    elif cmd == '--verify':
        verify_data()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
