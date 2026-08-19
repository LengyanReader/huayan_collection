#!/usr/bin/env python3
"""
华严项目 — 多源数据导入 SQLite (零信息损失版)
从 graph.json + personas.json + locations.json + lineages.json + glossary.yaml
合并导入到 huayan.db，保留所有字段。

用法: python scripts/import_all_to_sqlite.py [--verify-only]
"""

import json
import sqlite3
import sys
import os
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "catalog" / "huayan.db"

GRAPH_PATH = ROOT / "web" / "demo" / "graph.json"
PERSONAS_PATH = ROOT / "data" / "knowledge_graph" / "personas.json"
LINEAGES_PATH = ROOT / "data" / "knowledge_graph" / "lineages.json"
LOCATIONS_PATH = ROOT / "data" / "knowledge_graph" / "locations.json"
GLOSSARY_PATH = ROOT / "data" / "translation" / "glossary.yaml"


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def load_yaml(path):
    import yaml
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def normalize_relation(r):
    """Normalize relation values to standard form."""
    m = {"MASTER": "MASTER_OF", "INFLUENCE": "INFLUENCED", "STUDIED_UNDER": "INFLUENCED"}
    return m.get(r, r)


def j(v):
    """Serialize value to JSON TEXT for storage (None stays None)."""
    if v is None:
        return None
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return v


def import_persons(conn, graph, personas):
    """Import persons from graph.json (superset) + personas.json (richer fields)."""
    # Build lookup from personas.json
    pa_by_id = {}
    for p in personas.get('persons', []):
        pa_by_id[p['id']] = p

    # Build lookup from graph.json nodes
    gr_by_id = {}
    for n in graph.get('nodes', []):
        gr_by_id[n['id']] = n

    # All person IDs (union of both sources)
    all_ids = sorted(set(list(pa_by_id.keys()) + list(gr_by_id.keys())),
                     key=lambda x: (x.split('_')[0], x.split('_')[-1]))

    imported = 0
    skipped = 0
    for pid in all_ids:
        gr = gr_by_id.get(pid, {})
        pa = pa_by_id.get(pid, {})

        # Prefer personas.json for richer text fields, graph.json for broad coverage
        name_zh = pa.get('name_zh') or gr.get('n', '')
        if not name_zh:
            skipped += 1
            continue

        # Name fields (only in personas.json for most)
        name_sa = pa.get('name_sa')
        name_en = pa.get('name_en')
        name_bo = pa.get('name_bo')
        name_ja = pa.get('name_ja')

        # alt_names from personas.json
        alt_names = j(pa.get('alt_names'))

        # title from graph.json (ti) or personas.json (title)
        title = pa.get('title') or gr.get('ti')

        # type
        ptype = pa.get('type') or gr.get('tp', 'practitioner')

        # dates: prefer graph.json if personas has null but graph doesn't
        birth_year = pa.get('birth_year') if pa.get('birth_year') is not None else gr.get('b')
        death_year = pa.get('death_year') if pa.get('death_year') is not None else gr.get('d')

        # dynasty
        dynasty = pa.get('dynasty') or gr.get('dy', '')

        # biography: prefer longer text
        bio_pa = pa.get('biography', '') or ''
        bio_gr = gr.get('bio', '') or ''
        biography = bio_pa if len(bio_pa) >= len(bio_gr) else bio_gr

        # lineage
        lineage_branch = pa.get('lineage_branch') or gr.get('li')
        if lineage_branch == 'null':
            lineage_branch = None
        lineage_order = pa.get('lineage_order')

        # key_works: merge from both sources
        kw_pa = pa.get('key_works', [])
        kw_gr = gr.get('wk', [])
        key_works_list = kw_pa if kw_pa else kw_gr
        key_works = j(key_works_list) if key_works_list else None

        # works_links (only in personas.json)
        works_links = j(pa.get('works_links'))

        # multi_lineage (only in graph.json)
        multi = gr.get('multi', [])
        multi_lineage = j(multi) if multi else None

        # source (only in personas.json)
        source_text = pa.get('source')

        # verified
        verified = pa.get('verified', 0)
        if verified is None:
            verified = gr.get('v', 0) or 0

        conn.execute("""
            INSERT OR REPLACE INTO persons
            (source_id, name_zh, name_bo, name_sa, name_en, name_ja, alt_names,
             title, type, birth_year, death_year, dynasty, biography,
             lineage_branch, lineage_order, key_works, works_links, multi_lineage,
             source, verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pid, name_zh, name_bo, name_sa, name_en, name_ja, alt_names,
            title, ptype, birth_year, death_year, dynasty, biography,
            lineage_branch, lineage_order, key_works, works_links, multi_lineage,
            source_text, verified or 0
        ))
        imported += 1

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    print(f"Persons: {imported} imported ({skipped} skipped) → {count} total in DB")
    return count


def import_locations(conn, graph, locations_data):
    """Import locations from graph.json (superset) + locations.json (richer fields)."""
    # Build lookups
    loc_by_id = {}
    for loc in locations_data.get('locations', []):
        loc_by_id[loc['id']] = loc

    gr_by_id = {}
    for loc in graph.get('locations', []):
        gr_by_id[loc['id']] = loc

    all_ids = sorted(set(list(loc_by_id.keys()) + list(gr_by_id.keys())))

    imported = 0
    for lid in all_ids:
        gr = gr_by_id.get(lid, {})
        lo = loc_by_id.get(lid, {})

        name_zh = lo.get('name_zh') or gr.get('n', '')
        if not name_zh:
            continue

        current_name = lo.get('current_name')
        lat = gr.get('lat') if gr.get('lat') is not None else lo.get('lat')
        lng = gr.get('lng') if gr.get('lng') is not None else lo.get('lng')
        ltype = gr.get('tp') or lo.get('type', 'temple')
        dynasty = gr.get('dy') or lo.get('dynasty', '')
        city = lo.get('city')
        province = lo.get('province')

        # description: prefer longer
        desc_lo = lo.get('description', '') or ''
        desc_gr = gr.get('ds', '') or ''
        description = desc_lo if len(desc_lo) >= len(desc_gr) else desc_gr

        # related_persons: merge from both
        rp_gr = gr.get('ps', [])
        rp_lo = lo.get('related_persons', [])
        rp_all = sorted(set(rp_gr + rp_lo))
        related_persons = j(rp_all) if rp_all else None

        source_text = lo.get('source')

        conn.execute("""
            INSERT OR REPLACE INTO locations
            (source_id, name_zh, current_name, lat, lng, type, dynasty,
             city, province, description, related_persons, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lid, name_zh, current_name, lat, lng, ltype, dynasty,
            city, province, description, related_persons, source_text
        ))
        imported += 1

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM locations").fetchone()[0]
    print(f"Locations: {imported} imported → {count} total in DB")
    return count


def import_lineages(conn, graph, lineages_data):
    """Import lineages metadata + edges."""
    # Import lineage metadata — clear first to avoid ID churn
    conn.execute("DELETE FROM lineage_edges")
    conn.execute("DELETE FROM lineages")

    lineage_colors = graph.get('lineage_colors', {})
    lineage_meta = {}
    for lg in lineages_data.get('lineages', []):
        lineage_meta[lg['name']] = lg

    # Also extract lineage names from graph.json edges
    edge_lineage_names = set()
    for e in graph.get('edges', []):
        ln = e.get('li', '')
        if ln and ln != 'null':
            edge_lineage_names.add(ln)

    # Build full set of lineage names
    all_lineage_names = sorted(set(list(lineage_meta.keys()) + list(edge_lineage_names)))

    lineage_id_map = {}
    for name in all_lineage_names:
        meta = lineage_meta.get(name, {})
        lid = meta.get('id') or f'lineage_{name}'
        desc = meta.get('description', '')
        period = meta.get('period', '')
        color = lineage_colors.get(name)

        conn.execute("""
            INSERT INTO lineages (source_id, name, description, period, color)
            VALUES (?, ?, ?, ?, ?)
        """, (lid, name, desc, period, color))

        row = conn.execute("SELECT id FROM lineages WHERE name=?", (name,)).fetchone()
        lineage_id_map[name] = row[0]

    conn.commit()

    # Collect all person IDs known to DB
    known_persons = set()
    for row in conn.execute("SELECT source_id FROM persons").fetchall():
        known_persons.add(row[0])

    # Build edge note lookup from lineages.json
    edge_notes = {}
    for lg in lineages_data.get('lineages', []):
        lg_name = lg['name']
        for e in lg.get('edges', []):
            key = (e['from'], e['to'], e.get('relation', 'MASTER_OF'))
            edge_notes[key] = (e.get('note', ''), lg_name)

    # Import edges from graph.json (primary, has lineage_name per edge)
    imported = 0
    skipped = 0
    seen = set()
    for e in graph.get('edges', []):
        s = e['s']
        t = e['t']

        # Skip edges referencing non-existent persons
        if s not in known_persons or t not in known_persons:
            skipped += 1
            continue

        rel = normalize_relation(e.get('r', 'MASTER_OF'))
        ln_graph = e.get('li', '')

        # Try to get note from lineages.json
        key = (s, t, rel)
        note_val = ''
        ln_for_note = ln_graph
        if key in edge_notes:
            note_val, ln_from_json = edge_notes[key]
            if not ln_for_note or ln_for_note == 'null':
                ln_for_note = ln_from_json

        # Try broader match (relation might differ slightly)
        if not note_val:
            for (fs, ft, fr), (n, ln) in edge_notes.items():
                if fs == s and ft == t:
                    note_val = n
                    if not ln_for_note or ln_for_note == 'null':
                        ln_for_note = ln
                    break

        if not ln_for_note or ln_for_note == 'null':
            ln_for_note = None

        lineage_id = lineage_id_map.get(ln_for_note)

        edge_key = (s, t, rel, ln_for_note or '')
        if edge_key in seen:
            continue
        seen.add(edge_key)

        conn.execute("""
            INSERT INTO lineage_edges (from_person_id, to_person_id, relation,
                                       lineage_name, lineage_id, note)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (s, t, rel, ln_for_note, lineage_id, note_val))
        imported += 1

    # Also import edges from lineages.json that aren't in graph.json
    graph_edge_keys = set()
    for e in graph.get('edges', []):
        graph_edge_keys.add((e['s'], e['t'], normalize_relation(e.get('r', 'MASTER_OF'))))

    for lg in lineages_data.get('lineages', []):
        lg_name = lg['name']
        for e in lg.get('edges', []):
            rel = normalize_relation(e.get('relation', 'MASTER_OF'))
            key = (e['from'], e['to'], rel)
            if key not in graph_edge_keys:
                if e['from'] not in known_persons or e['to'] not in known_persons:
                    skipped += 1
                    continue
                edge_key = (e['from'], e['to'], rel, lg_name)
                if edge_key not in seen:
                    seen.add(edge_key)
                    lineage_id = lineage_id_map.get(lg_name)
                    conn.execute("""
                        INSERT INTO lineage_edges (from_person_id, to_person_id, relation,
                                                   lineage_name, lineage_id, note, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (e['from'], e['to'], rel, lg_name, lineage_id,
                          e.get('note', ''), f'lineages.json:{lg_name}'))
                    imported += 1

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM lineage_edges").fetchone()[0]
    lg_count = conn.execute("SELECT COUNT(*) FROM lineages").fetchone()[0]
    if skipped:
        print(f"  (skipped {skipped} edges referencing unknown persons)")
    print(f"Lineages: {lg_count} metadata entries imported")
    print(f"Edges: {imported} imported → {count} total in DB")
    return count


def import_glossary(conn):
    """Import glossary from glossary.yaml."""
    try:
        data = load_yaml(GLOSSARY_PATH)
    except Exception as e:
        print(f"Warning: Could not load glossary.yaml: {e}")
        return 0

    terms = data.get('terms', data) if isinstance(data, dict) else data
    if isinstance(terms, dict):
        terms = list(terms.values())

    imported = 0
    for idx, t in enumerate(terms):
        if not isinstance(t, dict):
            continue

        tid = t.get('id', f'glossary_{idx+1:03d}')
        category = t.get('category', 'doctrine')
        sa = t.get('sa') or t.get('sa_iast', '')
        bo_wylie = t.get('bo_wylie', '')
        bo_unicode = t.get('bo_unicode', '')
        zh = t.get('zh', '')
        en = t.get('en', '')
        def_zh = t.get('definition_zh', '')
        def_en = t.get('definition_en', '')

        # alt_translations: merge zh and en lists
        alt_zh = t.get('alt_translations', {}).get('zh', []) if isinstance(t.get('alt_translations'), dict) else []
        alt_en = t.get('alt_translations', {}).get('en', []) if isinstance(t.get('alt_translations'), dict) else []
        alt_all = {}
        if alt_zh:
            alt_all['zh'] = alt_zh
        if alt_en:
            alt_all['en'] = alt_en
        alt_trans = j(alt_all) if alt_all else None

        conn.execute("""
            INSERT INTO glossary
            (source_id, term_sa, term_bo, term_bo_wylie, term_bo_unicode,
             term_zh, term_en, category, definition_zh, definition_en,
             alt_translations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tid, sa, bo_unicode, bo_wylie, bo_unicode,
            zh, en, category, def_zh, def_en, alt_trans
        ))
        imported += 1

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM glossary").fetchone()[0]
    print(f"Glossary: {imported} imported → {count} total in DB")
    return count


def verify_import(conn):
    """Comprehensive verification of imported data."""
    print("\n" + "=" * 60)
    print("  数据完整性验证报告")
    print("=" * 60)

    # Persons
    p_total = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    p_verified = conn.execute("SELECT COUNT(*) FROM persons WHERE verified=1").fetchone()[0]
    p_no_bio = conn.execute("SELECT COUNT(*) FROM persons WHERE biography IS NULL OR biography=''").fetchone()[0]
    p_no_dates = conn.execute("SELECT COUNT(*) FROM persons WHERE birth_year IS NULL AND death_year IS NULL").fetchone()[0]
    p_no_lineage = conn.execute("SELECT COUNT(*) FROM persons WHERE lineage_branch IS NULL").fetchone()[0]
    p_with_title = conn.execute("SELECT COUNT(*) FROM persons WHERE title IS NOT NULL AND title!=''").fetchone()[0]
    p_with_kw = conn.execute("SELECT COUNT(*) FROM persons WHERE key_works IS NOT NULL").fetchone()[0]
    p_with_wl = conn.execute("SELECT COUNT(*) FROM persons WHERE works_links IS NOT NULL").fetchone()[0]
    p_with_ml = conn.execute("SELECT COUNT(*) FROM persons WHERE multi_lineage IS NOT NULL").fetchone()[0]
    p_with_sa = conn.execute("SELECT COUNT(*) FROM persons WHERE name_sa IS NOT NULL AND name_sa!=''").fetchone()[0]
    p_with_en = conn.execute("SELECT COUNT(*) FROM persons WHERE name_en IS NOT NULL AND name_en!=''").fetchone()[0]
    print(f"\nPersons: {p_total} total")
    print(f"  verified={p_verified}, no_bio={p_no_bio}, no_dates={p_no_dates}, no_lineage={p_no_lineage}")
    print(f"  with_title={p_with_title}, key_works={p_with_kw}, works_links={p_with_wl}, multi_lineage={p_with_ml}")
    print(f"  name_sa={p_with_sa}, name_en={p_with_en}")

    # Locations
    l_total = conn.execute("SELECT COUNT(*) FROM locations").fetchone()[0]
    l_no_coords = conn.execute("SELECT COUNT(*) FROM locations WHERE lat IS NULL OR lng IS NULL").fetchone()[0]
    l_with_city = conn.execute("SELECT COUNT(*) FROM locations WHERE city IS NOT NULL AND city!=''").fetchone()[0]
    print(f"\nLocations: {l_total} total | {l_no_coords} missing coords | {l_with_city} with city")

    # Lineages
    lg_total = conn.execute("SELECT COUNT(*) FROM lineages").fetchone()[0]
    print(f"\nLineages: {lg_total} metadata entries")

    # Edges
    e_total = conn.execute("SELECT COUNT(*) FROM lineage_edges").fetchone()[0]
    e_rels = conn.execute("SELECT relation, COUNT(*) FROM lineage_edges GROUP BY relation ORDER BY COUNT(*) DESC").fetchall()
    print(f"\nEdges: {e_total} total")
    for rel, cnt in e_rels:
        print(f"  {rel}: {cnt}")

    # Glossary
    g_total = conn.execute("SELECT COUNT(*) FROM glossary").fetchone()[0]
    g_with_sa = conn.execute("SELECT COUNT(*) FROM glossary WHERE term_sa IS NOT NULL AND term_sa!=''").fetchone()[0]
    g_with_en = conn.execute("SELECT COUNT(*) FROM glossary WHERE term_en IS NOT NULL AND term_en!=''").fetchone()[0]
    print(f"\nGlossary: {g_total} terms | {g_with_sa} with Sanskrit | {g_with_en} with English")

    # Connectivity
    isolated = conn.execute("""
        SELECT COUNT(*) FROM persons p
        WHERE NOT EXISTS (SELECT 1 FROM lineage_edges e
                          WHERE e.from_person_id = p.source_id
                             OR e.to_person_id = p.source_id)
    """).fetchone()[0]
    print(f"\nConnectivity: {isolated} isolated persons (no edges)")

    # Orphan edges (reference non-existent persons)
    orphans = conn.execute("""
        SELECT COUNT(*) FROM lineage_edges e
        WHERE NOT EXISTS (SELECT 1 FROM persons p WHERE p.source_id = e.from_person_id)
           OR NOT EXISTS (SELECT 1 FROM persons p WHERE p.source_id = e.to_person_id)
    """).fetchone()[0]
    print(f"Orphan edges: {orphans} (reference missing persons)")

    print("\n" + "=" * 60)
    return p_total, e_total, l_total, g_total


def main():
    verify_only = '--verify-only' in sys.argv

    if verify_only:
        if not DB_PATH.exists():
            print(f"ERROR: {DB_PATH} does not exist. Run without --verify-only first.")
            sys.exit(1)
        conn = sqlite3.connect(str(DB_PATH))
        verify_import(conn)
        conn.close()
        return

    print("Loading data sources...")
    graph = load_json(GRAPH_PATH)
    personas = load_json(PERSONAS_PATH)
    lineages = load_json(LINEAGES_PATH)
    locations = load_json(LOCATIONS_PATH)

    print(f"  graph.json: {len(graph.get('nodes', []))} nodes, {len(graph.get('edges', []))} edges, {len(graph.get('locations', []))} locations")
    print(f"  personas.json: {len(personas.get('persons', []))} persons")
    print(f"  lineages.json: {len(lineages.get('lineages', []))} lineages")
    print(f"  locations.json: {len(locations.get('locations', []))} locations")

    # Init DB if needed
    if not DB_PATH.exists():
        print("\nDatabase not found, initializing from schema.sql...")
        schema_path = ROOT / "data" / "catalog" / "schema.sql"
        conn = sqlite3.connect(str(DB_PATH))
        with open(schema_path, encoding='utf-8') as f:
            conn.executescript(f.read())
    else:
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("PRAGMA foreign_keys = ON")

    print("\n--- Importing Persons ---")
    import_persons(conn, graph, personas)

    print("\n--- Importing Locations ---")
    import_locations(conn, graph, locations)

    print("\n--- Importing Lineages & Edges ---")
    import_lineages(conn, graph, lineages)

    print("\n--- Importing Glossary ---")
    import_glossary(conn)

    verify_import(conn)

    conn.close()
    print(f"\nDone. Database: {DB_PATH} ({DB_PATH.stat().st_size:,} bytes)")


if __name__ == '__main__':
    main()
