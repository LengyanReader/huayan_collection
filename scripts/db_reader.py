#!/usr/bin/env python3
"""
华严项目 — SQLite 数据读取模块
供 build.py 调用，从 huayan.db 读取数据并转换为前端所需格式。

职责:
  1. 读取 SQLite → 返回 graph.json 兼容格式 (nodes/edges/locations)
  2. 读取 SQLite → 返回 personas/lineages/locations JSON 格式
  3. 提供查询接口 (按ID查人物、按法系过滤等)

不修改数据，不硬编码任何内容。
"""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "catalog" / "huayan.db"


def get_conn():
    """Get a connection to huayan.db with foreign keys enabled."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _j_load(v):
    """Load JSON TEXT back to Python object, pass through if not JSON."""
    if v is None:
        return None
    if isinstance(v, (list, dict)):
        return v
    try:
        return json.loads(v)
    except (json.JSONDecodeError, TypeError):
        return v


def load_graph():
    """Build graph.json-compatible dict from SQLite.

    Returns: {"nodes": [...], "edges": [...], "locations": [...], "lineage_colors": {...}}
    Compatible with existing lineage.js, build.py, and frontend code.
    """
    conn = get_conn()

    # --- Nodes (persons) ---
    rows = conn.execute("""
        SELECT source_id, name_zh, name_bo, name_sa, name_en, name_ja,
               alt_names, title, type, birth_year, death_year, dynasty,
               biography, lineage_branch, lineage_order, key_works,
               works_links, multi_lineage, verified
        FROM persons ORDER BY id
    """).fetchall()

    nodes = []
    for r in rows:
        kw = _j_load(r['key_works'])
        wl = _j_load(r['works_links'])
        ml = _j_load(r['multi_lineage'])
        an = _j_load(r['alt_names'])

        nodes.append({
            "id": r['source_id'],
            "n": r['name_zh'],
            "ti": r['title'] or '',
            "li": r['lineage_branch'],
            "multi": ml if ml else [],
            "tp": r['type'] or 'practitioner',
            "b": r['birth_year'],
            "d": r['death_year'],
            "dy": r['dynasty'] or '',
            "bio": (r['biography'] or '')[:150],
            "wk": kw if kw else [],
            "wl": wl if wl else {},
            "v": r['verified'] or 0,
            # Extra fields (not in legacy graph.json but available for enriched rendering)
            "name_sa": r['name_sa'],
            "name_en": r['name_en'],
            "name_bo": r['name_bo'],
            "name_ja": r['name_ja'],
            "alt_names": an,
            "biography_full": r['biography'] or '',
            "lineage_order": r['lineage_order'],
        })

    # --- Edges ---
    rows = conn.execute("""
        SELECT from_person_id, to_person_id, relation, lineage_name, note
        FROM lineage_edges ORDER BY id
    """).fetchall()

    edges = []
    for r in rows:
        edges.append({
            "s": r['from_person_id'],
            "t": r['to_person_id'],
            "r": r['relation'] or 'MASTER_OF',
            "li": r['lineage_name'] or 'null',
        })

    # --- Locations ---
    rows = conn.execute("""
        SELECT source_id, name_zh, lat, lng, type, dynasty, description,
               related_persons, city, province, current_name
        FROM locations ORDER BY id
    """).fetchall()

    locations = []
    for r in rows:
        rp = _j_load(r['related_persons'])
        locations.append({
            "id": r['source_id'],
            "n": r['name_zh'],
            "lat": r['lat'],
            "lng": r['lng'],
            "tp": r['type'] or 'temple',
            "dy": r['dynasty'] or '',
            "ds": (r['description'] or '')[:120],
            "ps": rp if rp else [],
            # Extra fields
            "city": r['city'],
            "province": r['province'],
            "current_name": r['current_name'],
        })

    # --- Lineage colors ---
    rows = conn.execute("SELECT name, color FROM lineages WHERE color IS NOT NULL").fetchall()
    lineage_colors = {r['name']: r['color'] for r in rows}

    conn.close()

    return {
        "nodes": nodes,
        "edges": edges,
        "locations": locations,
        "lineage_colors": lineage_colors,
    }


def load_personas():
    """Export persons in personas.json v0.2.0 format.

    Returns: {"version": "0.2.0", "persons": [...]}
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT source_id, name_zh, name_sa, name_en, name_bo, name_ja,
               alt_names, title, type, birth_year, death_year, dynasty,
               lineage_branch, lineage_order, biography, key_works,
               works_links, source, verified
        FROM persons ORDER BY id
    """).fetchall()

    persons = []
    for r in rows:
        persons.append({
            "id": r['source_id'],
            "name_zh": r['name_zh'],
            "name_sa": r['name_sa'],
            "name_en": r['name_en'],
            "name_bo": r['name_bo'],
            "name_ja": r['name_ja'],
            "alt_names": _j_load(r['alt_names']),
            "title": r['title'],
            "type": r['type'] or 'practitioner',
            "birth_year": r['birth_year'],
            "death_year": r['death_year'],
            "dynasty": r['dynasty'] or '',
            "lineage_branch": r['lineage_branch'],
            "lineage_order": r['lineage_order'],
            "biography": r['biography'] or '',
            "key_works": _j_load(r['key_works']),
            "works_links": _j_load(r['works_links']),
            "source": r['source'],
            "verified": r['verified'] or 0,
        })

    conn.close()
    return {"version": "0.2.0", "persons": persons}


def load_lineages():
    """Export lineages in lineages.json v0.2.0 format.

    Returns: {"version": "0.2.0", "lineages": [...]}
    """
    conn = get_conn()

    lg_rows = conn.execute("""
        SELECT id, source_id, name, description, period
        FROM lineages ORDER BY id
    """).fetchall()

    lineages = []
    for lg in lg_rows:
        edge_rows = conn.execute("""
            SELECT from_person_id, to_person_id, relation, note
            FROM lineage_edges WHERE lineage_id = ? ORDER BY id
        """, (lg['id'],)).fetchall()

        edges = []
        for e in edge_rows:
            edges.append({
                "from": e['from_person_id'],
                "to": e['to_person_id'],
                "relation": e['relation'],
                "note": e['note'] or '',
            })

        lineages.append({
            "id": lg['source_id'],
            "name": lg['name'],
            "description": lg['description'] or '',
            "period": lg['period'] or '',
            "edges": edges,
        })

    conn.close()
    return {"version": "0.2.0", "lineages": lineages}


def load_locations():
    """Export locations in locations.json v0.2.0 format.

    Returns: {"version": "0.2.0", "locations": [...]}
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT source_id, name_zh, current_name, lat, lng, type,
               dynasty, city, province, description, related_persons, source
        FROM locations ORDER BY id
    """).fetchall()

    locations = []
    for r in rows:
        locations.append({
            "id": r['source_id'],
            "name_zh": r['name_zh'],
            "current_name": r['current_name'],
            "lat": r['lat'],
            "lng": r['lng'],
            "type": r['type'] or 'temple',
            "dynasty": r['dynasty'] or '',
            "city": r['city'],
            "province": r['province'],
            "description": r['description'] or '',
            "related_persons": _j_load(r['related_persons']) or [],
            "source": r['source'],
        })

    conn.close()
    return {"version": "0.2.0", "locations": locations}


def load_glossary():
    """Export glossary in glossary.yaml-compatible format.

    Returns: list of term dicts.
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT source_id, term_sa, term_bo_wylie, term_bo_unicode,
               term_zh, term_en, category, definition_zh, definition_en,
               alt_translations
        FROM glossary ORDER BY id
    """).fetchall()

    terms = []
    for r in rows:
        terms.append({
            "id": r['source_id'],
            "category": r['category'] or 'doctrine',
            "sa": r['term_sa'] or '',
            "sa_iast": r['term_sa'] or '',
            "bo_wylie": r['term_bo_wylie'] or '',
            "bo_unicode": r['term_bo_unicode'] or '',
            "zh": r['term_zh'] or '',
            "en": r['term_en'] or '',
            "definition_zh": r['definition_zh'] or '',
            "definition_en": r['definition_en'] or '',
            "alt_translations": _j_load(r['alt_translations']) or {},
        })

    conn.close()
    return terms


def load_texts():
    """Export texts, chapters, and cross_refs from SQLite.

    Returns: {"texts": [...], "chapters": [...], "cross_refs": [...]}
    """
    conn = get_conn()

    # --- Texts ---
    rows = conn.execute("""
        SELECT id, title_zh, title_bo, title_sa, title_en, type, sub_type,
               taisho_no, cbeta_id, tohk_no, yitian_status, dynasty,
               date_text, volumn_count, chapter_count, structure, abstract,
               language, source_url, in_cbeta, has_tibetan, has_sanskrit
        FROM texts ORDER BY id
    """).fetchall()

    texts = []
    for r in rows:
        texts.append({
            "id": r['id'],
            "title_zh": r['title_zh'] or '',
            "title_bo": r['title_bo'] or '',
            "title_sa": r['title_sa'] or '',
            "title_en": r['title_en'] or '',
            "type": r['type'] or 'sutra',
            "sub_type": r['sub_type'] or '',
            "taisho_no": r['taisho_no'] or '',
            "cbeta_id": r['cbeta_id'] or '',
            "tohk_no": r['tohk_no'] or '',
            "yitian_status": r['yitian_status'] or 'not_listed',
            "dynasty": r['dynasty'] or '',
            "date_text": r['date_text'] or '',
            "volumn_count": r['volumn_count'],
            "chapter_count": r['chapter_count'],
            "structure": r['structure'] or '',
            "abstract": r['abstract'] or '',
            "language": r['language'] or 'zh',
            "source_url": r['source_url'] or '',
            "in_cbeta": r['in_cbeta'] or 0,
            "has_tibetan": r['has_tibetan'] or 0,
            "has_sanskrit": r['has_sanskrit'] or 0,
        })

    # --- Chapters ---
    rows = conn.execute("""
        SELECT id, sutra_id, title_zh, title_bo, title_sa, title_en,
               order_num, in_60huayan, in_80huayan, in_40huayan,
               in_tibetan, is_unique_to_bo, is_unique_to_zh, content_diff
        FROM chapters ORDER BY sutra_id, order_num
    """).fetchall()

    chapters = []
    for r in rows:
        chapters.append({
            "id": r['id'],
            "sutra_id": r['sutra_id'],
            "title_zh": r['title_zh'] or '',
            "title_bo": r['title_bo'] or '',
            "title_sa": r['title_sa'] or '',
            "title_en": r['title_en'] or '',
            "order_num": r['order_num'],
            "in_60huayan": r['in_60huayan'] or 0,
            "in_80huayan": r['in_80huayan'] or 0,
            "in_40huayan": r['in_40huayan'] or 0,
            "in_tibetan": r['in_tibetan'] or 0,
            "is_unique_to_bo": r['is_unique_to_bo'] or 0,
            "is_unique_to_zh": r['is_unique_to_zh'] or 0,
            "content_diff": r['content_diff'] or '',
        })

    # --- Cross-refs ---
    rows = conn.execute("""
        SELECT from_text_id, to_text_id, relation, note
        FROM cross_refs ORDER BY id
    """).fetchall()

    cross_refs = []
    for r in rows:
        cross_refs.append({
            "from": r['from_text_id'],
            "to": r['to_text_id'],
            "relation": r['relation'] or '',
            "note": r['note'] or '',
        })

    conn.close()
    return {"texts": texts, "chapters": chapters, "cross_refs": cross_refs}


def get_person_by_id(source_id):
    """Get a single person by source_id. Returns dict or None."""
    conn = get_conn()
    r = conn.execute("""
        SELECT * FROM persons WHERE source_id = ?
    """, (source_id,)).fetchone()
    conn.close()
    if not r:
        return None
    return dict(r)


def get_edges_for_person(source_id):
    """Get all edges (in or out) for a person."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM lineage_edges
        WHERE from_person_id = ? OR to_person_id = ?
        ORDER BY id
    """, (source_id, source_id)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_persons_by_lineage(lineage_name):
    """Get all persons in a given lineage branch."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT source_id, name_zh, type, dynasty
        FROM persons WHERE lineage_branch = ?
        ORDER BY lineage_order
    """, (lineage_name,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_stats():
    """Get database statistics."""
    conn = get_conn()
    stats = {}
    stats['persons'] = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    stats['edges'] = conn.execute("SELECT COUNT(*) FROM lineage_edges").fetchone()[0]
    stats['locations'] = conn.execute("SELECT COUNT(*) FROM locations").fetchone()[0]
    stats['lineages'] = conn.execute("SELECT COUNT(*) FROM lineages").fetchone()[0]
    stats['glossary'] = conn.execute("SELECT COUNT(*) FROM glossary").fetchone()[0]
    stats['texts'] = conn.execute("SELECT COUNT(*) FROM texts").fetchone()[0]
    stats['chapters'] = conn.execute("SELECT COUNT(*) FROM chapters").fetchone()[0]
    stats['isolated_persons'] = conn.execute("""
        SELECT COUNT(*) FROM persons p
        WHERE NOT EXISTS (SELECT 1 FROM lineage_edges e
                          WHERE e.from_person_id = p.source_id
                             OR e.to_person_id = p.source_id)
    """).fetchone()[0]
    conn.close()
    return stats


def export_all_json(output_dir):
    """Export all SQLite data to JSON files (for build.py backward compatibility).

    Writes:
      - graph.json
      - personas.json
      - lineages.json
      - locations.json
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    graph = load_graph()
    with open(out / 'graph.json', 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"  graph.json: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges, {len(graph['locations'])} locations")

    personas = load_personas()
    with open(out / 'personas.json', 'w', encoding='utf-8') as f:
        json.dump(personas, f, ensure_ascii=False, indent=2)
    print(f"  personas.json: {len(personas['persons'])} persons")

    lineages = load_lineages()
    with open(out / 'lineages.json', 'w', encoding='utf-8') as f:
        json.dump(lineages, f, ensure_ascii=False, indent=2)
    print(f"  lineages.json: {len(lineages['lineages'])} lineages")

    locations = load_locations()
    with open(out / 'locations.json', 'w', encoding='utf-8') as f:
        json.dump(locations, f, ensure_ascii=False, indent=2)
    print(f"  locations.json: {len(locations['locations'])} locations")


if __name__ == '__main__':
    import sys
    if '--stats' in sys.argv:
        s = get_stats()
        for k, v in s.items():
            print(f"  {k}: {v}")
    elif '--export' in sys.argv:
        idx = sys.argv.index('--export')
        out = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else str(ROOT / 'web' / 'demo')
        print(f"Exporting SQLite → {out}")
        export_all_json(out)
    elif '--verify' in sys.argv:
        graph = load_graph()
        print(f"Graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges, {len(graph['locations'])} locations")
        print(f"Lineage colors: {len(graph['lineage_colors'])}")
        # Verify no data loss: count unique fields
        has_sa = sum(1 for n in graph['nodes'] if n.get('name_sa'))
        has_en = sum(1 for n in graph['nodes'] if n.get('name_en'))
        has_wk = sum(1 for n in graph['nodes'] if n.get('wk'))
        has_wl = sum(1 for n in graph['nodes'] if n.get('wl'))
        has_ml = sum(1 for n in graph['nodes'] if n.get('multi'))
        has_ti = sum(1 for n in graph['nodes'] if n.get('ti'))
        print(f"  name_sa: {has_sa}, name_en: {has_en}, title: {has_ti}")
        print(f"  key_works: {has_wk}, works_links: {has_wl}, multi_lineage: {has_ml}")
    else:
        print("Usage: python scripts/db_reader.py [--stats|--export DIR|--verify]")
