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
CATALOG_PATH = ROOT / "data" / "catalog" / "complete_catalog.yaml"


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
                                       lineage_name, lineage_id, note, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (s, t, rel, ln_for_note, lineage_id, note_val, 'graph.json'))
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

        # Skip if already exists
        exists = conn.execute(
            "SELECT 1 FROM glossary WHERE source_id=?", (tid,)
        ).fetchone()
        if exists:
            imported += 1  # count as already imported
            continue

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


def import_texts(conn):
    """Import texts from complete_catalog.yaml into the texts table."""
    try:
        data = load_yaml(CATALOG_PATH)
    except Exception as e:
        print(f"Warning: Could not load complete_catalog.yaml: {e}")
        return 0, {}

    # Map source_id → inserted text rowid, for cross_ref building
    id_to_rowid = {}
    imported = 0

    # Iterate all catalog sections
    sections = [
        ('main_sutras', 'sutra'),
        ('branch_translations', 'sutra'),
        ('related_sutras', 'sutra'),
        ('treatises', 'shastra'),
        ('patriarch_works', 'commentary'),
        ('tibetan_sources', 'sutra'),
        ('modern_works', 'study'),
    ]

    for section_key, default_type in sections:
        items = data.get(section_key, [])
        if not items:
            continue
        for entry in items:
            if not isinstance(entry, dict):
                continue

            src_id = entry.get('id', '')
            title_zh = entry.get('title_zh', '')
            if not title_zh:
                continue

            title_sa = entry.get('title_sa', '')
            title_en = entry.get('title_en', '')
            title_bo = entry.get('title_bo', '')
            text_type = entry.get('type', default_type)
            sub_type = entry.get('sub_type')

            taisho_no = entry.get('taisho_no', '')
            cbeta_id = entry.get('cbeta_id', '')
            tohk_no = entry.get('tohk_no', '')

            # Author / translator lookup by name (person IDs not in catalog)
            author_name = entry.get('author', '')
            translator_name = entry.get('translator', '') or entry.get('translators', '')

            dynasty = entry.get('dynasty', '')
            date_text = entry.get('date_text', '')
            volumn_count = entry.get('volumn_count')
            chapter_count = entry.get('chapter_count')
            structure = entry.get('structure', '')
            abstract = entry.get('context_note', '')
            language = entry.get('language', 'zh')
            if section_key == 'tibetan_sources':
                language = 'bo'

            source_url = entry.get('url', '')
            in_cbeta = 1 if cbeta_id else 0

            # Determine has_tibetan / has_sanskrit from context
            has_tibetan = 0
            has_sanskrit = 0
            if title_sa:
                has_sanskrit = 1
            if section_key == 'tibetan_sources':
                has_tibetan = 1

            # yitian_status: check if listed in 义天录
            yitian_status = entry.get('yitian_status', 'not_listed')

            # Skip if already exists (title_zh + type + taisho_no)
            exists = conn.execute(
                "SELECT id FROM texts WHERE title_zh=? AND type=? AND COALESCE(taisho_no,'')=COALESCE(?,'')",
                (title_zh, text_type, taisho_no or None)
            ).fetchone()
            if exists:
                # 幂等更新：已存在行仅回填多语题名（title_sa/title_bo/title_en），
                # 便于后续批次补充英译而不重复建行。
                conn.execute(
                    "UPDATE texts SET "
                    "title_en=COALESCE(?, title_en), "
                    "title_sa=COALESCE(?, title_sa), "
                    "title_bo=COALESCE(?, title_bo) "
                    "WHERE id=?",
                    (title_en or None, title_sa or None, title_bo or None, exists[0])
                )
                if src_id:
                    id_to_rowid[src_id] = exists[0]
                continue

            conn.execute("""
                INSERT INTO texts
                (title_zh, title_bo, title_sa, title_en, type, sub_type,
                 taisho_no, cbeta_id, tohk_no, yitian_status,
                 dynasty, date_text, volumn_count, chapter_count, structure,
                 abstract, language, source_url, in_cbeta, has_tibetan, has_sanskrit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                title_zh, title_bo or None, title_sa or None, title_en or None,
                text_type, sub_type,
                taisho_no or None, cbeta_id or None, tohk_no or None, yitian_status,
                dynasty or None, date_text or None, volumn_count, chapter_count,
                structure or None, abstract or None, language, source_url or None,
                in_cbeta, has_tibetan, has_sanskrit
            ))

            rowid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            if src_id:
                id_to_rowid[src_id] = rowid
            imported += 1

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM texts").fetchone()[0]
    print(f"Texts: {imported} imported → {count} total in DB")
    return count, id_to_rowid


def import_chapters(conn, id_to_rowid):
    """Import chapter-level data for the main sutras.

    The catalog defines chapter_count per sutra but not individual chapter names.
    We populate the 39 chapters of 八十华严 (the standard version) as reference data,
    since it is the most commonly used version and the basis for the gap analysis.
    """
    # Look up the 八十华严 text rowid
    hs80_rowid = None
    for src_id, rowid in id_to_rowid.items():
        if src_id == 'text_main_002':
            hs80_rowid = rowid
            break

    if not hs80_rowid:
        # Fallback: look up by taisho_no
        row = conn.execute("SELECT id FROM texts WHERE taisho_no='T10n0279'").fetchone()
        if row:
            hs80_rowid = row[0]

    if not hs80_rowid:
        print("Chapters: skipped (八十华严 not found in texts)")
        return 0

    # 八十华严 39 chapters with cross-version comparison
    # Format: (order, title, in_60, in_tibetan, is_unique_to_zh)
    # in_60: whether this chapter exists in 六十华严 (0=absent/merged)
    # in_tibetan: whether this chapter exists in 藏文 Toh44 (0=absent)
    # is_unique_to_zh: 1 if unique to Chinese versions (not in Tibetan)
    chapters_80 = [
        (1,  "世主妙严品",          1, 1, 0),
        (2,  "如来现相品",          1, 1, 0),
        (3,  "普贤三昧品",          1, 1, 0),
        (4,  "世界成就品",          1, 1, 0),
        (5,  "华藏世界品",          1, 1, 0),
        (6,  "毗卢遮那品",          1, 1, 0),
        (7,  "如来名号品",          1, 1, 0),
        (8,  "四圣谛品",            1, 1, 0),
        (9,  "光明觉品",            1, 1, 0),
        (10, "菩萨问明品",          1, 1, 0),
        (11, "净行品",              1, 1, 0),
        (12, "贤首品",              1, 1, 0),
        (13, "升须弥山顶品",        1, 1, 0),
        (14, "须弥顶上偈赞品",      1, 1, 0),
        (15, "十住品",              1, 1, 0),
        (16, "梵行品",              1, 1, 0),
        (17, "初发心功德品",        1, 1, 0),
        (18, "明法品",              1, 1, 0),
        (19, "升夜摩天宫品",        1, 1, 0),
        (20, "夜摩宫中偈赞品",      1, 1, 0),
        (21, "十行品",              1, 1, 0),
        (22, "十无尽藏品",          1, 1, 0),
        (23, "升兜率天宫品",        1, 1, 0),
        (24, "兜率宫中偈赞品",      1, 1, 0),
        (25, "十回向品",            1, 1, 0),
        (26, "十地品",              1, 1, 0),
        (27, "十定品",              0, 1, 0),  # 六十华严无独立十定品
        (28, "十通品",              0, 1, 0),  # 六十华严无独立十通品
        (29, "十忍品",              0, 1, 0),  # 六十华严无独立十忍品
        (30, "阿僧祇品",            0, 1, 0),  # 六十华严无此品
        (31, "寿量品",              0, 1, 0),  # 六十华严无此品
        (32, "诸菩萨住处品",        0, 1, 0),  # 六十华严无此品
        (33, "佛不思议法品",        1, 1, 0),
        (34, "如来十身相海品",      1, 1, 0),
        (35, "如来随好光明功德品",  1, 1, 0),
        (36, "普贤行品",            1, 1, 0),
        (37, "如来出现品",          1, 1, 0),
        (38, "离世间品",            1, 1, 0),
        (39, "入法界品",            1, 1, 0),
    ]

    imported = 0
    for order_num, ch_title, in_60, in_tib, unique_zh in chapters_80:
        conn.execute("""
            INSERT OR REPLACE INTO chapters
            (sutra_id, title_zh, order_num, in_80huayan, in_60huayan,
             in_tibetan, is_unique_to_zh, source)
            VALUES (?, ?, ?, 1, ?, ?, ?, 'CBETA/84000')
        """, (hs80_rowid, ch_title, order_num, in_60, in_tib, unique_zh))
        imported += 1

    # 藏文独有 2 品 (汉文无对应) — use 100+ offset to avoid order_num conflicts
    unique_bo_chapters = [
        (112, "如来华严品", "Tathāgatāvataṃsaka"),
        (128, "普贤宣说品", "Samantabhadraparivarta"),
    ]
    for bo_order, bo_title, bo_sa in unique_bo_chapters:
        conn.execute("""
            INSERT OR REPLACE INTO chapters
            (sutra_id, title_zh, title_sa, order_num, in_80huayan,
             in_60huayan, in_tibetan, is_unique_to_bo, source)
            VALUES (?, ?, ?, ?, 0, 0, 1, 1, 'Toh44/84000')
        """, (hs80_rowid, bo_title, bo_sa, bo_order))
        imported += 1

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM chapters").fetchone()[0]
    print(f"Chapters: {imported} imported (八十华严 39 + 藏文独有 2) → {count} total in DB")
    return count


def import_cross_refs(conn, id_to_rowid):
    """Import cross-reference relationships from complete_catalog.yaml.

    Uses the 'related_to' and 'relation_type' fields in main_sutras,
    plus known structural relationships between texts.
    """
    try:
        data = load_yaml(CATALOG_PATH)
    except Exception as e:
        print(f"Warning: Could not load complete_catalog.yaml: {e}")
        return 0

    # Build reverse lookup: source_id → rowid (already have id_to_rowid from import_texts)
    imported = 0
    seen = set()

    def _add_ref(from_id, to_id, relation, note=''):
        """Insert a cross_ref if both texts exist and not already added."""
        nonlocal imported
        if not from_id or not to_id:
            return
        from_rowid = id_to_rowid.get(from_id)
        to_rowid = id_to_rowid.get(to_id)
        if not from_rowid or not to_rowid:
            return
        key = (from_rowid, to_rowid, relation)
        if key in seen:
            return
        seen.add(key)
        try:
            conn.execute("""
                INSERT OR IGNORE INTO cross_refs (from_text_id, to_text_id, relation, note)
                VALUES (?, ?, ?, ?)
            """, (from_rowid, to_rowid, relation, note))
            imported += 1
        except sqlite3.IntegrityError:
            pass

    # 1. Main sutra cross-refs from related_to fields
    for sutra in data.get('main_sutras', []):
        src_id = sutra.get('id', '')
        rel_type = sutra.get('relation_type', 'related')
        for target_id in sutra.get('related_to', []):
            _add_ref(src_id, target_id, rel_type, sutra.get('context_note', '')[:200] if sutra.get('context_note') else '')

    # 2. Branch translations → their corresponding main sutra chapters
    # (corresponds_to field indicates which chapter they translate)
    hs80_rowid = id_to_rowid.get('text_main_002')
    if hs80_rowid:
        for bt in data.get('branch_translations', []):
            bt_id = bt.get('id', '')
            bt_rowid = id_to_rowid.get(bt_id)
            if bt_rowid and bt.get('corresponds_to'):
                _add_ref(bt_id, 'text_main_002', 'alternate_trans',
                         f"对应: {bt.get('corresponds_to')}")

    # 3. Related sutras → main sutras (general related relationship)
    for rs in data.get('related_sutras', []):
        rs_id = rs.get('id', '')
        rs_rowid = id_to_rowid.get(rs_id)
        if rs_rowid:
            _add_ref(rs_id, 'text_main_002', 'related',
                     rs.get('context_note', '')[:200] if rs.get('context_note') else '')

    # 4. Treatises → main sutras (commentary_on relationship)
    for tr in data.get('treatises', []):
        tr_id = tr.get('id', '')
        tr_rowid = id_to_rowid.get(tr_id)
        if tr_rowid:
            _add_ref(tr_id, 'text_main_002', 'commentary_on',
                     tr.get('context_note', '')[:200] if tr.get('context_note') else '')

    # 5. Patriarch works → main sutras
    for pw in data.get('patriarch_works', []):
        pw_id = pw.get('id', '')
        pw_rowid = id_to_rowid.get(pw_id)
        if pw_rowid:
            _add_ref(pw_id, 'text_main_002', 'commentary_on',
                     pw.get('context_note', '')[:200] if pw.get('context_note') else '')

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM cross_refs").fetchone()[0]
    print(f"Cross-refs: {imported} imported → {count} total in DB")
    return count


def import_person_locations(conn):
    """Populate person_locations by reversing locations.related_persons.

    Each location's related_persons JSON array contains person source_ids.
    We create a person_locations row for each pair, inferring relation from context.
    """
    rows = conn.execute("""
        SELECT id, source_id, name_zh, related_persons, dynasty
        FROM locations WHERE related_persons IS NOT NULL AND related_persons != ''
    """).fetchall()

    imported = 0
    for loc_id, loc_source, loc_name, rp_json, dynasty in rows:
        try:
            person_ids = json.loads(rp_json) if rp_json else []
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(person_ids, list):
            continue

        for pid in person_ids:
            # Look up person's internal id by source_id
            p_row = conn.execute("SELECT id FROM persons WHERE source_id = ?", (pid,)).fetchone()
            if not p_row:
                continue
            person_db_id = p_row[0]

            # Determine relation from dynasty match
            p_dynasty = conn.execute(
                "SELECT dynasty FROM persons WHERE id = ?", (person_db_id,)
            ).fetchone()
            p_dyn = (p_dynasty[0] or '') if p_dynasty else ''
            relation = 'associated'
            if dynasty and p_dyn and dynasty in p_dyn:
                relation = 'active_in'

            try:
                conn.execute("""
                    INSERT OR IGNORE INTO person_locations
                    (person_id, location_id, relation, note)
                    VALUES (?, ?, ?, ?)
                """, (person_db_id, loc_id, relation,
                      f"据 locations.{loc_source} ({loc_name}) 关联"))
                imported += 1
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM person_locations").fetchone()[0]
    print(f"Person-locations: {imported} imported → {count} total in DB")
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

    # Texts
    t_total = conn.execute("SELECT COUNT(*) FROM texts").fetchone()[0]
    t_by_type = conn.execute("SELECT type, COUNT(*) FROM texts GROUP BY type ORDER BY COUNT(*) DESC").fetchall()
    t_with_cbeta = conn.execute("SELECT COUNT(*) FROM texts WHERE cbeta_id IS NOT NULL AND cbeta_id!=''").fetchone()[0]
    t_with_taisho = conn.execute("SELECT COUNT(*) FROM texts WHERE taisho_no IS NOT NULL AND taisho_no!=''").fetchone()[0]
    print(f"\nTexts: {t_total} total | {t_with_cbeta} with CBETA ID | {t_with_taisho} with 大正藏编号")
    for typ, cnt in t_by_type:
        print(f"  {typ}: {cnt}")

    # Chapters
    ch_total = conn.execute("SELECT COUNT(*) FROM chapters").fetchone()[0]
    ch_sutras = conn.execute("SELECT COUNT(DISTINCT sutra_id) FROM chapters").fetchone()[0]
    print(f"\nChapters: {ch_total} total (across {ch_sutras} sutras)")

    # Cross-refs
    cr_total = conn.execute("SELECT COUNT(*) FROM cross_refs").fetchone()[0]
    cr_by_rel = conn.execute("SELECT relation, COUNT(*) FROM cross_refs GROUP BY relation ORDER BY COUNT(*) DESC").fetchall()
    print(f"\nCross-refs: {cr_total} total")
    for rel, cnt in cr_by_rel:
        print(f"  {rel}: {cnt}")

    # Person-locations
    pl_total = conn.execute("SELECT COUNT(*) FROM person_locations").fetchone()[0]
    pl_by_rel = conn.execute("SELECT relation, COUNT(*) FROM person_locations GROUP BY relation ORDER BY COUNT(*) DESC").fetchall()
    pl_persons = conn.execute("SELECT COUNT(DISTINCT person_id) FROM person_locations").fetchone()[0]
    pl_locs = conn.execute("SELECT COUNT(DISTINCT location_id) FROM person_locations").fetchone()[0]
    print(f"\nPerson-locations: {pl_total} links ({pl_persons} persons × {pl_locs} locations)")
    for rel, cnt in pl_by_rel:
        print(f"  {rel}: {cnt}")

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
        conn.execute("PRAGMA foreign_keys = OFF")

    print("\n--- Importing Persons ---")
    import_persons(conn, graph, personas)

    print("\n--- Importing Locations ---")
    import_locations(conn, graph, locations)

    print("\n--- Importing Lineages & Edges ---")
    import_lineages(conn, graph, lineages)

    print("\n--- Importing Glossary ---")
    import_glossary(conn)

    print("\n--- Importing Texts ---")
    texts_count, id_to_rowid = import_texts(conn)

    print("\n--- Importing Chapters ---")
    import_chapters(conn, id_to_rowid)

    print("\n--- Importing Cross-refs ---")
    import_cross_refs(conn, id_to_rowid)

    print("\n--- Importing Person-Locations ---")
    import_person_locations(conn)

    conn.execute("PRAGMA foreign_keys = ON")
    verify_import(conn)

    conn.close()
    print(f"\nDone. Database: {DB_PATH} ({DB_PATH.stat().st_size:,} bytes)")


if __name__ == '__main__':
    main()
