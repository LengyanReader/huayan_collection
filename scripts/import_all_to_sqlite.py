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

        source_text = lo.get('source') or gr.get('source')

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


CHAPTERS_PATH = ROOT / "data" / "catalog" / "chapters.yaml"


def import_chapters(conn, id_to_rowid):
    """Import chapter rows for 八十华严 (39) + the 2 Tibetan-unique chapters.

    Authoritative source: data/catalog/chapters.yaml (single source of truth). It used to
    live as two hardcoded lists here (39 tuples) plus a second hardcoded title_zh->title_en
    map in backfill_chapters_title_en.py; a rebuild therefore produced rows without
    title_en that then differed from older rows, which broke de-duplication. Both are
    merged into the YAML, so one import now writes a complete, identical row set and
    re-imports are true no-ops under the UNIQUE(sutra_id, order_num) index.
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

    data = load_yaml(CHAPTERS_PATH)
    if not data or not data.get('chapters'):
        print("Chapters: skipped (chapters.yaml empty or absent)")
        return 0

    imported = 0
    for ch in data['chapters']:
        conn.execute("""
            INSERT OR REPLACE INTO chapters
            (sutra_id, title_zh, title_bo, title_sa, title_en, order_num,
             in_80huayan, in_60huayan, in_tibetan,
             is_unique_to_zh, is_unique_to_bo, source)
            VALUES (?, ?, NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (hs80_rowid, ch.get('title_zh'), ch.get('title_sa'), ch.get('title_en'),
              ch['order'], ch.get('in_80huayan', 0), ch.get('in_60huayan', 0),
              ch.get('in_tibetan', 0), ch.get('is_unique_to_zh', 0),
              ch.get('is_unique_to_bo', 0), ch.get('source')))
        imported += 1

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM chapters").fetchone()[0]
    no_en = conn.execute(
        "SELECT COUNT(*) FROM chapters WHERE title_en IS NULL OR title_en=''").fetchone()[0]
    print(f"Chapters: {imported} imported (八十华严 39 + 藏文独有 2) → {count} total in DB"
          f" | missing title_en={no_en}")
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
    """Rebuild person_locations from locations.related_persons (fully derived table).

    Each location's related_persons JSON array contains person source_ids.
    We create a person_locations row for each pair, inferring relation from context.

    The table is cleared first on purpose. It is 100% derived — every row can be
    recomputed from locations.related_persons — and it stores persons by *rowid*. Rows are
    only ever rewritten via INSERT OR REPLACE, which on a UNIQUE conflict deletes the old
    row and allocates a new rowid, so person_ids shifted on every re-import. OR IGNORE then
    could not recognise the old pairs as duplicates and appended them: the table grew by
    45 rows per run (90 -> 135 -> ... -> 360) and ended up holding 245 stale person_ids
    that no longer pointed at any person. Clearing makes the rebuild idempotent.
    """
    conn.execute("DELETE FROM person_locations")
    conn.commit()

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
    # 陈旧引用自检：person_id 必须仍存在于 persons
    live = {r[0] for r in conn.execute("SELECT id FROM persons")}
    used = {r[0] for r in conn.execute("SELECT DISTINCT person_id FROM person_locations")}
    stale = len(used - live)
    print(f"Person-locations: {imported} imported → {count} total in DB"
          f" | stale person_id={stale}")
    if stale:
        print("  !! person_locations references person rows that no longer exist")
    return count


def _ensure_unique_index(conn, table, index_name, cols):
    """Guarantee a UNIQUE index, replacing a same-named non-unique one if present.

    `CREATE UNIQUE INDEX IF NOT EXISTS` silently does NOTHING when a non-unique index of
    the same name already exists — the name check wins, uniqueness is never applied. A
    database created before an index became UNIQUE therefore keeps the non-unique one, and
    `INSERT OR REPLACE` quietly stops de-duplicating (this is what made chapters double on
    every re-import). So: drop any same-named index that is not unique, then create the
    unique one. Returns True if a replacement happened.
    """
    for row in conn.execute(f"PRAGMA index_list('{table}')"):
        # (seq, name, unique, origin, partial)
        if row[1] == index_name:
            if row[2]:
                return False
            conn.execute(f'DROP INDEX "{index_name}"')
            conn.commit()
            break
    conn.execute(f'CREATE UNIQUE INDEX "{index_name}" ON "{table}"({",".join(cols)})')
    conn.commit()
    return True


def _migrate_chapters_unique(conn):
    """Restore chapters to a de-duplicated, genuinely idempotent state.

    `import_chapters` uses INSERT OR REPLACE, but OR REPLACE only substitutes when a
    UNIQUE/PK conflict exists, and chapters had no UNIQUE on (sutra_id, order_num) — so
    every re-import appended a fresh copy of all rows instead of replacing them. Worse,
    the copies were not identical (title_en was filled afterwards by a second script), so
    partial de-duplication would have been ambiguous.

    chapters.yaml is now the single authoritative source, which makes a full repopulate
    deterministic. So: refuse if anything still references chapters by id, then clear the
    table and let import_chapters() rebuild it; finally enforce the UNIQUE index. Rows are
    only ever removed here — the import immediately after re-creates all of them.
    """
    have = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if 'chapters' not in have:
        return
    if not CHAPTERS_PATH.exists():
        print("!! chapters migration skipped: chapters.yaml absent, cannot verify a repopulate")
        return

    # 若仍有外键引用旧 id，则不可删除
    if 'translation_units' in have:
        tu_cols = {r[1] for r in conn.execute("PRAGMA table_info(translation_units)")}
        if 'chapter_id' in tu_cols:
            used = conn.execute(
                "SELECT COUNT(*) FROM translation_units WHERE chapter_id IS NOT NULL").fetchone()[0]
            if used:
                print(f"!! chapters migration skipped: translation_units references {used} chapter row(s)")
                return

    before = conn.execute("SELECT COUNT(*) FROM chapters").fetchone()[0]
    want = len(load_yaml(CHAPTERS_PATH).get('chapters') or [])

    if before == want:
        # 行数已对，仅确保唯一索引真正生效（快路径）
        try:
            repl = _ensure_unique_index(conn, 'chapters', 'idx_chapters_order',
                                       ['sutra_id', 'order_num'])
            print(f"Chapters idempotency: {before} rows as expected; "
                  f"{'replaced non-unique index' if repl else 'unique index already in place'}")
        except sqlite3.IntegrityError as e:
            print(f"!! chapters UNIQUE index not created ({e})")
        return

    conn.execute("DELETE FROM chapters")
    conn.commit()
    try:
        repl = _ensure_unique_index(conn, 'chapters', 'idx_chapters_order',
                                   ['sutra_id', 'order_num'])
        note = "unique index idx_chapters_order ensured" + (" (replaced non-unique)" if repl else "")
    except sqlite3.IntegrityError as e:
        note = f"index NOT created ({e})"
    print(f"Chapters idempotency: cleared {before} stale/duplicate row(s) "
          f"(authoritative source has {want}); will be repopulated from chapters.yaml; {note}")


def _ensure_article_knowledge_schema(conn):
    """Idempotently create the article-knowledge tables on an existing DB.

    The DDL's single source of truth stays data/catalog/schema.sql — this only lifts
    the `article_*` CREATE statements out of that file and runs them, so a database
    created before these tables existed gains them on the next import without the
    schema being maintained in two places. (The legacy tables carry DROP statements
    and are deliberately NOT executed here — that would erase data.)
    """
    schema_path = ROOT / "data" / "catalog" / "schema.sql"
    if not schema_path.exists():
        return
    have = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    if {'article_terms', 'article_term_links', 'article_artifacts',
        'article_assembly_classes', 'article_assembly_members'} <= have:
        # Tables all present, but a table can still predate a later column addition.
        _migrate_article_assembly_columns(conn)
        return
    wanted = ('article_terms', 'article_term_links', 'article_artifacts',
              'article_assembly_classes', 'article_assembly_members',
              'idx_article_terms', 'idx_atl_', 'idx_artifacts', 'idx_aac_', 'idx_aam_')
    stmts, buf = [], []
    for line in schema_path.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if not buf and s.startswith('CREATE ') and any(w in s for w in wanted):
            buf = [line]
        elif buf:
            buf.append(line)
        if buf and s.endswith(';'):
            stmts.append('\n'.join(buf))
            buf = []
    for stmt in stmts:
        conn.execute(stmt)
    conn.commit()
    print(f"Article-knowledge schema: applied {len(stmts)} DDL statement(s) from schema.sql")
    _migrate_article_assembly_columns(conn)


# Columns added to article_assembly_classes after the table first shipped. A database
# created earlier has the table but not these, and CREATE TABLE IF NOT EXISTS is a no-op
# for it, so they are added here rather than left to a manual rebuild.
_ASSEMBLY_NEW_COLS = (
    # Documented in data/catalog/schema.sql; kept bare here because ALTER TABLE
    # ADD COLUMN does not take a trailing comment cleanly.
    ("collective_pos", "TEXT"),
    ("vow_kind", "TEXT"),
)


def _migrate_article_assembly_columns(conn):
    """Add post-hoc columns to article_assembly_classes if they are absent."""
    if 'article_assembly_classes' not in {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}:
        return
    have = {r[1] for r in conn.execute("PRAGMA table_info(article_assembly_classes)")}
    added = 0
    for col, decl in _ASSEMBLY_NEW_COLS:
        if col not in have:
            conn.execute(f"ALTER TABLE article_assembly_classes ADD COLUMN {col} {decl}")
            added += 1
    if added:
        conn.commit()
        print(f"Article-assembly schema: added {added} column(s): "
              + ", ".join(c for c, _ in _ASSEMBLY_NEW_COLS if c not in have))


def import_article_knowledge(conn):
    """Populate article_terms / article_term_links from data/translation/article_knowledge/*.yaml.

    Each YAML file is one standalone article's knowledge graph: its 名相/会处/术语 nodes
    (with provenance grade A1/A2/B/C/D) plus the edges among them and out to the existing
    entity tables. Idempotent: a file's rows are replaced wholesale, so re-running never
    duplicates. Grade D (疑讹·不见于经与历代注疏) is stored with status='rejected' —
    the renderer shows it struck through and never treats it as in-use terminology.
    """
    import glob
    _ensure_article_knowledge_schema(conn)
    ak_dir = ROOT / "data" / "translation" / "article_knowledge"
    if not ak_dir.exists():
        print("Article-knowledge: source dir absent, skipped")
        return 0

    files = sorted(glob.glob(str(ak_dir / "*.yaml")))
    n_terms = n_links = 0
    for fp in files:
        data = load_yaml(fp)
        if not isinstance(data, dict):
            print(f"  !! {Path(fp).name}: not a mapping, skipped")
            continue
        article_id = data.get('article_id') or Path(fp).stem
        terms = data.get('terms') or []
        links = data.get('links') or []

        # 幂等：先清该篇旧行（外键关，故顺序无碍）
        conn.execute("DELETE FROM article_term_links WHERE article_id = ?", (article_id,))
        conn.execute("DELETE FROM article_terms WHERE article_id = ?", (article_id,))

        for t in terms:
            tid = t.get('term_id')
            if not tid or not t.get('term_zh'):
                print(f"  !! {Path(fp).name}: term missing term_id/term_zh, skipped: {tid}")
                continue
            grade = (t.get('grade') or 'C').upper()
            status = t.get('status') or ('rejected' if grade == 'D' else 'used')
            aliases = t.get('aliases') or []
            conn.execute("""
                INSERT INTO article_terms
                (article_id, term_id, term_zh, aliases, category, grade, status,
                 definition_zh, definition_en, source_note, source_url, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (article_id, tid, t.get('term_zh'),
                  j(aliases) if aliases else None,
                  t.get('category'), grade, status,
                  t.get('definition_zh'), t.get('definition_en'),
                  t.get('source_note') or t.get('source'),
                  t.get('source_url'), t.get('note')))
            n_terms += 1

        known = {t.get('term_id') for t in terms}
        for l in links:
            f = l.get('from_term_id')
            if f not in known:
                print(f"  !! {Path(fp).name}: link from unknown term '{f}', skipped")
                continue
            conn.execute("""
                INSERT OR IGNORE INTO article_term_links
                (article_id, from_term_id, rel, to_type, to_ref, to_label, note)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (article_id, f, l.get('rel') or 'see_also',
                  l.get('to_type') or 'term', l.get('to_ref') or '',
                  l.get('to_label'), l.get('note')))
            n_links += 1

    conn.commit()
    n_files = conn.execute("SELECT COUNT(DISTINCT article_id) FROM article_terms").fetchone()[0]
    print(f"Article-knowledge: {n_files} article(s), {n_terms} terms, {n_links} links imported")
    return n_terms


def import_article_artifacts(conn):
    """Populate article_artifacts from data/translation/article_artifacts/*.yaml.

    One YAML per standalone article: the artworks, relics, murals and archaeological
    material that bear on that article's subject, each registered row-by-row with a
    provenance grade, a display status, a relevance statement, a mandatory href
    (the original object record, never a hot-linked bulk scan) and a mandatory
    licence/attribution line. Idempotent: a file's rows are replaced wholesale.

    Registration precedes display: status=pending rows are stored and auditable but the
    renderer leaves them out until a human has compared them against the text, so an
    unverified candidate can never reach the page as fact.
    """
    import glob
    _ensure_article_knowledge_schema(conn)
    ar_dir = ROOT / "data" / "translation" / "article_artifacts"
    if not ar_dir.exists():
        print("Article-artifacts: source dir absent, skipped")
        return 0

    files = sorted(glob.glob(str(ar_dir / "*.yaml")))
    n_art = 0
    for fp in files:
        data = load_yaml(fp)
        if not isinstance(data, dict):
            print(f"  !! {Path(fp).name}: not a mapping, skipped")
            continue
        article_id = data.get('article_id') or Path(fp).stem
        items = data.get('items') or []

        # 幂等：先清该篇旧行
        conn.execute("DELETE FROM article_artifacts WHERE article_id = ?", (article_id,))

        for a in items:
            aid = a.get('artifact_id')
            if not aid or not a.get('title_zh'):
                print(f"  !! {Path(fp).name}: item missing artifact_id/title_zh, skipped: {aid}")
                continue
            grade = (a.get('grade') or 'C').upper()
            status = a.get('status') or ('rejected' if grade == 'D' else 'pending')
            if status not in ('confirmed', 'pending', 'rejected'):
                print(f"  !! {Path(fp).name}: bad status '{status}', treated as pending: {aid}")
                status = 'pending'
            # 版权与溯源底线：出处与许可必填，链接必填或如实标注〔无链接〕
            href = a.get('href') or ''
            src = a.get('source_note') or ''
            lic = a.get('license') or ''
            if not src:
                print(f"  !! {Path(fp).name}: source_note missing, marked pending: {aid}")
                status = 'pending'
            if not lic:
                print(f"  !! {Path(fp).name}: license missing, marked pending: {aid}")
                status = 'pending'
            if not href:
                print(f"  !! {Path(fp).name}: href missing, recorded as 〔无链接〕: {aid}")
            conn.execute("""
                INSERT OR IGNORE INTO article_artifacts
                (article_id, artifact_id, title_zh, title_en, era, location, category,
                 grade, status, relevance_zh, relevance_en, href, thumb_url,
                 source_note, license, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (article_id, aid, a.get('title_zh'), a.get('title_en'),
                  a.get('era'), a.get('location'), a.get('category'),
                  grade, status, a.get('relevance_zh'), a.get('relevance_en'),
                  href, a.get('thumb_url'), src, lic, a.get('note')))
            n_art += 1

    conn.commit()
    n_files = conn.execute("SELECT COUNT(DISTINCT article_id) FROM article_artifacts").fetchone()[0]
    print(f"Article-artifacts: {n_files} article(s), {n_art} item(s) imported")
    return n_art


def import_article_assembly(conn):
    """Populate article_assembly_classes/members from data/translation/*_assembly.yaml.

    The assembly lists of a 品 (e.g. 世主妙严品 vol.1) are the substrate for EDA on that
    assembly: the class name, the number expression the text actually uses, every member it
    names outright, the domain it presides over, and the collective vow of the block.

    The distinction that matters and is easy to lose: `n_named` counts the members the sutra
    lists by name; it is NOT the size of the class, which the sutra gives only as 微塵數／無量.
    Conflating the two is how a deck of named figures gets promoted into a headcount.

    The vow is captured per block, bounded by that class's own 「如是等而為上首」 marker, so a
    long vow can never bleed into its neighbour. Idempotent: a file's rows are replaced
    wholesale.
    """
    import glob
    _ensure_article_knowledge_schema(conn)
    asm_glob = str(ROOT / "data" / "translation" / "*_assembly.yaml")
    files = sorted(glob.glob(asm_glob))
    if not files:
        print("Article-assembly: source absent, skipped")
        return 0

    n_cls = n_mem = 0
    for fp in files:
        data = load_yaml(fp)
        if not isinstance(data, dict):
            print(f"  !! {Path(fp).name}: not a mapping, skipped")
            continue
        article_id = data.get('article') or Path(fp).stem.replace('_assembly', '')
        classes = data.get('classes') or []
        src = data.get('source_note') or data.get('source') or 'T10n0279'

        # 幂等：先清该篇旧行（无外键约束，顺序无碍）
        conn.execute("DELETE FROM article_assembly_members WHERE article_id = ?", (article_id,))
        conn.execute("DELETE FROM article_assembly_classes WHERE article_id = ?", (article_id,))

        for c in classes:
            cat = c.get('cat')
            if not cat or 'n_named' not in c:
                print(f"  !! {Path(fp).name}: class missing cat/n_named, skipped: {cat}")
                continue
            members = c.get('members') or []
            # 守恒：n_named 必须等于实列成员数，否则该类不可信
            if len(members) != c['n_named']:
                print(f"  !! {Path(fp).name}: {cat} n_named={c['n_named']} "
                      f"but {len(members)} member(s) listed, using listed count")
                c['n_named'] = len(members)
            conn.execute("""
                INSERT OR REPLACE INTO article_assembly_classes
                (article_id, cls_idx, cat_zh, group_key, group_zh, realm, count_expr,
                 leader_zh, n_named, domain_zh, collective_zh, collective_pos, vow_kind,
                 vow_zh, punct_variant, glyph_variant, source_note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (article_id, c.get('idx', n_cls), cat, c.get('group') or '',
                  c.get('group_zh'), c.get('realm'), c.get('count_expr'),
                  c.get('leader'), c['n_named'], c.get('domain'), c.get('collective'),
                  c.get('collective_pos'), c.get('vow_kind'),
                  c.get('vow'), c.get('punct_variant'), c.get('glyph_variant'), src))
            n_cls += 1
            for j, m in enumerate(members, start=1):
                conn.execute("""
                    INSERT OR REPLACE INTO article_assembly_members
                    (article_id, cls_idx, member_idx, member_zh, is_leader)
                    VALUES (?, ?, ?, ?, ?)
                """, (article_id, c.get('idx', n_cls - 1), j, m, 1 if j == 1 else 0))
                n_mem += 1

    conn.commit()
    # 自洽：各类 n_named 之和须等于成员表行数
    s = conn.execute("SELECT COALESCE(SUM(n_named),0) FROM article_assembly_classes").fetchone()[0]
    m = conn.execute("SELECT COUNT(*) FROM article_assembly_members").fetchone()[0]
    if s != m:
        print(f"  !! Article-assembly: class n_named sum {s} != member rows {m}")
    print(f"Article-assembly: {n_cls} class(es), {n_mem} member(s) imported "
          f"(n_named sum {s} == member rows {m})")
    return n_cls


_EDA_TABLES = ('article_eda_docs', 'article_eda_morphemes', 'article_eda_member_segs',
               'idx_aem_', 'idx_aems_')


# Fields of the generated EDA `classes` block that are the EDITOR's analysis rather than
# a statement of the sutra. Everything else (cat aside, which is the join label) is a sutra
# fact and is therefore served from article_assembly_* so it is stated in exactly one place.
_EDA_CLASS_KEEP = ('idx', 'cat', 'n_char_total', 'len_hist', 'head_hist', 'tailch_hist',
                   'domain_hist', 'domain_top', 'top_morphemes', 'top_pairs',
                   'n_word_hits', 'n_unsegmented')
_EDA_MEMBER_KEEP = ('i', 'n_char', 'head', 'tailch', 'segs', 'segs_char_only',
                    'domains', 'n_word', 'n_unsegmented', 'n_unsegmented_char_only',
                    'zhu_object')


def _project_eda_classes(classes):
    """Keep only the analysis half of the generated per-class block."""
    out = []
    for c in classes:
        keep = {k: c[k] for k in _EDA_CLASS_KEEP if k in c}
        keep['members'] = [{k: mm[k] for k in _EDA_MEMBER_KEEP if k in mm}
                           for mm in (c.get('members') or [])]
        out.append(keep)
    return out


def _ensure_article_eda_schema(conn):
    """Idempotently create the EDA tables on an existing DB.

    Same approach — and the same restraint — as _ensure_article_knowledge_schema: lift
    only the EDA `CREATE` statements out of data/catalog/schema.sql and run those, so
    the schema has a single source of truth. Executing schema.sql wholesale would run
    its `DROP TABLE IF EXISTS persons/texts/…` statements and destroy the database, so
    the extraction is not optional here.
    """
    schema_path = ROOT / "data" / "catalog" / "schema.sql"
    if not schema_path.exists():
        return
    have = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    if set(_EDA_TABLES[:3]) <= have:
        return
    stmts, buf = [], []
    for line in schema_path.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if not buf and s.startswith('CREATE ') and any(w in s for w in _EDA_TABLES):
            buf = [line]
        elif buf:
            buf.append(line)
        if buf and s.endswith(';'):
            stmts.append('\n'.join(buf))
            buf = []
    for stmt in stmts:
        conn.execute(stmt)
    conn.commit()
    print(f"Article-EDA schema: applied {len(stmts)} DDL statement(s) from schema.sql")


def import_article_eda(conn):
    """Populate the article EDA group from data/translation/*_eda.yaml.

    Source: scripts/miaoyan_eda.py, which derives every number from
    data/translation/miaoyan_assembly.yaml (the sutra facts) plus a hand-compiled
    morpheme lexicon. Nothing here is invented downstream: this step only moves the
    generated document into SQLite so that db_reader/build can serve it without the
    frontend ever reading YAML.

    Two shapes are stored on purpose:
      * article_eda_docs.payload_json — the whole rendered document (heat matrix, morph
        matrix, graphs, per-class member segmentation), because the renderer needs it
        whole and re-assembling it from rows would only invite drift;
      * article_eda_morphemes / article_eda_member_segs — the same analysis normalised,
        so SQL can audit it (e.g. 「sum(n) == metrics.tokens_total」) and so a future
        generator can be checked against what shipped.

    Idempotent: a file's rows are replaced wholesale.
    """
    import glob
    _ensure_article_eda_schema(conn)
    files = sorted(glob.glob(str(ROOT / "data" / "translation" / "*_eda.yaml")))
    files = [f for f in files if not f.endswith("_eda_lexicon.yaml")]
    if not files:
        print("Article-EDA: source absent, skipped")
        return 0

    n_doc = n_mor = n_seg = 0
    for fp in files:
        data = load_yaml(fp)
        if not isinstance(data, dict) or 'metrics' not in data:
            print(f"  !! {Path(fp).name}: no metrics, skipped")
            continue
        article_id = data.get('article') or Path(fp).stem.replace('_eda', '')

        conn.execute("DELETE FROM article_eda_member_segs WHERE article_id = ?", (article_id,))
        conn.execute("DELETE FROM article_eda_morphemes  WHERE article_id = ?", (article_id,))
        conn.execute("DELETE FROM article_eda_docs       WHERE article_id = ?", (article_id,))

        # payload = whole document minus the two pieces served elsewhere:
        #   * classes are projected to analysis-only (below) so sutra facts (name, vow,
        #     count_expr, domain) live in exactly ONE place — article_assembly_*;
        #   * the per-member segmentation is also normalised into article_eda_member_segs.
        eda_classes = _project_eda_classes(data.get('classes') or [])
        payload = {k: v for k, v in data.items() if k != 'classes'}
        payload['eda_classes'] = eda_classes
        conn.execute("""
            INSERT OR REPLACE INTO article_eda_docs
            (article_id, source, source_url, generated_by, method_json, metrics_json, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (article_id, data.get('source'), data.get('source_url'),
              data.get('generated_by'), j(data.get('method')), j(data.get('metrics')),
              j(payload)))
        n_doc += 1

        for rank, m in enumerate(data.get('morph_freq') or [], start=1):
            conn.execute("""
                INSERT OR REPLACE INTO article_eda_morphemes
                (article_id, zh, n, n_char_only, seg_mode, domain, confidence,
                 gloss, gloss_en, rank)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (article_id, m.get('zh', ''), m.get('n', 0), m.get('n_char_only', 0),
                  m.get('mode', 'char'), m.get('domain', 'unassigned'), m.get('c', 'low'),
                  m.get('gloss', ''), m.get('gloss_en', ''), rank))
            n_mor += 1

        # 逐类逐名写入切分结果；类目本身仍以 article_assembly_* 为准，此处只存分析
        for c in data.get('classes') or []:
            ci = c.get('idx', 0)
            for mm in c.get('members') or []:
                for seq, t in enumerate(mm.get('segs') or [], start=1):
                    conn.execute("""
                        INSERT OR REPLACE INTO article_eda_member_segs
                        (article_id, cls_idx, member_idx, seq, token, seg_mode,
                         known, domain, confidence)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (article_id, ci, mm.get('i', 0), seq, t.get('zh', ''),
                          t.get('mode', 'char'), 1 if t.get('known') else 0,
                          t.get('domain', 'unassigned'), t.get('c', 'low')))
                    n_seg += 1

    conn.commit()
    # 自洽：词素频次合计须等于 metrics.tokens_total
    for (aid,) in conn.execute("SELECT article_id FROM article_eda_docs").fetchall():
        s = conn.execute(
            "SELECT COALESCE(SUM(n),0) FROM article_eda_morphemes WHERE article_id = ?",
            (aid,)).fetchone()[0]
        mj = conn.execute(
            "SELECT metrics_json FROM article_eda_docs WHERE article_id = ?",
            (aid,)).fetchone()[0]
        try:
            want = (json.loads(mj) if mj else {}).get('tokens_total')
        except Exception:
            want = None
        if want is not None and s != want:
            print(f"  !! Article-EDA: {aid} morpheme sum {s} != metrics.tokens_total {want}")
    print(f"Article-EDA: {n_doc} doc(s), {n_mor} morpheme row(s), {n_seg} segment row(s) imported")
    return n_doc


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

    # Article knowledge graph（名相·会处·术语 + 边）
    ak_arts = conn.execute("SELECT COUNT(DISTINCT article_id) FROM article_terms").fetchone()[0]
    ak_terms = conn.execute("SELECT COUNT(*) FROM article_terms").fetchone()[0]
    ak_links = conn.execute("SELECT COUNT(*) FROM article_term_links").fetchone()[0]
    ak_grades = conn.execute(
        "SELECT grade, COUNT(*) FROM article_terms GROUP BY grade ORDER BY grade").fetchall()
    ak_no_def = conn.execute(
        "SELECT COUNT(*) FROM article_terms WHERE definition_zh IS NULL OR definition_zh=''").fetchone()[0]
    ak_bad_grade = conn.execute(
        "SELECT COUNT(*) FROM article_terms WHERE grade NOT IN ('A1','A2','B','C','D')").fetchone()[0]
    # D 级必须为 rejected（铁律：D 级不采用）
    ak_d_bad = conn.execute(
        "SELECT COUNT(*) FROM article_terms WHERE grade='D' AND status<>'rejected'").fetchone()[0]
    # 边不得悬空（from_term_id 必为同篇之术语）
    ak_dangling = conn.execute("""
        SELECT COUNT(*) FROM article_term_links l
        WHERE NOT EXISTS (SELECT 1 FROM article_terms t
                          WHERE t.article_id = l.article_id AND t.term_id = l.from_term_id)
    """).fetchone()[0]
    print(f"\nArticle knowledge: {ak_arts} article(s) | {ak_terms} terms | {ak_links} links")
    print("  grades: " + ", ".join(f"{g}={c}" for g, c in ak_grades))
    print(f"  no_definition={ak_no_def} | bad_grade={ak_bad_grade} | D_not_rejected={ak_d_bad} | dangling_edges={ak_dangling}")
    if ak_bad_grade or ak_d_bad or ak_dangling:
        print("  !! Article-knowledge integrity problem (see counts above)")

    # Article assembly（会众结构：类 × 成员 × 所主 × 誓愿）
    have_asm = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    if {'article_assembly_classes', 'article_assembly_members'} <= have_asm:
        aa_arts = conn.execute("SELECT COUNT(DISTINCT article_id) FROM article_assembly_classes").fetchone()[0]
        aa_cls = conn.execute("SELECT COUNT(*) FROM article_assembly_classes").fetchone()[0]
        aa_mem = conn.execute("SELECT COUNT(*) FROM article_assembly_members").fetchone()[0]
        aa_sum = conn.execute("SELECT COALESCE(SUM(n_named),0) FROM article_assembly_classes").fetchone()[0]
        aa_grp = conn.execute(
            "SELECT group_key, COUNT(*) FROM article_assembly_classes GROUP BY group_key ORDER BY 2 DESC").fetchall()
        aa_nvow = conn.execute(
            "SELECT COUNT(*) FROM article_assembly_classes WHERE vow_zh IS NULL OR vow_zh=''").fetchone()[0]
        # 每类必有上首，且上首必须是该类首名成员
        aa_nolead = conn.execute(
            "SELECT COUNT(*) FROM article_assembly_classes WHERE leader_zh IS NULL OR leader_zh=''").fetchone()[0]
        aa_badlead = conn.execute("""
            SELECT COUNT(*) FROM article_assembly_classes c
            WHERE c.leader_zh <> (SELECT m.member_zh FROM article_assembly_members m
                                  WHERE m.article_id=c.article_id AND m.cls_idx=c.cls_idx
                                    AND m.member_idx=1)
        """).fetchone()[0]
        # 成员不得悬空（每成员必属本篇已存在的类）
        aa_orphan = conn.execute("""
            SELECT COUNT(*) FROM article_assembly_members m
            WHERE NOT EXISTS (SELECT 1 FROM article_assembly_classes c
                              WHERE c.article_id=m.article_id AND c.cls_idx=m.cls_idx)
        """).fetchone()[0]
        # 结句不得以数词开头（数词混入结句是早期抽取之失，须防复现）
        aa_numleak = conn.execute("""
            SELECT COUNT(*) FROM article_assembly_classes
            WHERE vow_zh LIKE '其數%' OR vow_zh LIKE '不可思議數%' OR vow_zh LIKE '不思議數%'
               OR vow_zh LIKE '有無量數%' OR vow_zh LIKE '不可稱數%' OR vow_zh LIKE '%微塵數%'
        """).fetchone()[0]
        # 有集总词者必须记其位置
        aa_nopos = conn.execute(
            "SELECT COUNT(*) FROM article_assembly_classes "
            "WHERE collective_zh IS NOT NULL AND collective_zh<>'' "
            "AND (collective_pos IS NULL OR collective_pos='')").fetchone()[0]
        aa_kind = conn.execute(
            "SELECT vow_kind, COUNT(*) FROM article_assembly_classes GROUP BY vow_kind").fetchall()
        print(f"\nArticle assembly: {aa_arts} article(s) | {aa_cls} classes | {aa_mem} members")
        print("  groups: " + ", ".join(f"{g}={c}" for g, c in aa_grp))
        print("  vow kinds: " + ", ".join(f"{k or 'NULL'}={c}" for k, c in aa_kind))
        print(f"  n_named_sum={aa_sum} (must equal members={aa_mem}) | no_vow={aa_nvow} | "
              f"no_leader={aa_nolead} | leader_mismatch={aa_badlead} | orphan_members={aa_orphan}")
        print(f"  vow_leaks_count_expr={aa_numleak} | collective_without_pos={aa_nopos}")
        if (aa_sum != aa_mem or aa_orphan or aa_badlead or aa_nolead
                or aa_nvow or aa_numleak or aa_nopos):
            print("  !! Article-assembly integrity problem (see counts above)")

    # Article EDA（名号构词法析构：编辑性分析，非经文事实）
    have_eda = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    if {'article_eda_docs', 'article_eda_morphemes', 'article_eda_member_segs'} <= have_eda:
        ed_docs = conn.execute("SELECT COUNT(*) FROM article_eda_docs").fetchone()[0]
        ed_mor = conn.execute("SELECT COUNT(*) FROM article_eda_morphemes").fetchone()[0]
        ed_seg = conn.execute("SELECT COUNT(*) FROM article_eda_member_segs").fetchone()[0]
        ed_unknown = conn.execute(
            "SELECT COUNT(*) FROM article_eda_member_segs WHERE known=0").fetchone()[0]
        ed_noconf = conn.execute(
            "SELECT COUNT(*) FROM article_eda_morphemes WHERE confidence IS NULL OR confidence=''").fetchone()[0]
        ed_nodom = conn.execute(
            "SELECT COUNT(*) FROM article_eda_morphemes WHERE domain IS NULL OR domain=''").fetchone()[0]
        ed_nomethod = conn.execute(
            "SELECT COUNT(*) FROM article_eda_docs WHERE method_json IS NULL OR method_json=''").fetchone()[0]
        # 词素频次合计须等于 metrics.tokens_total（否则分析文档与规范化表脱节）
        ed_badsum = 0
        for (aid, mj) in conn.execute(
                "SELECT article_id, metrics_json FROM article_eda_docs").fetchall():
            s = conn.execute(
                "SELECT COALESCE(SUM(n),0) FROM article_eda_morphemes WHERE article_id=?",
                (aid,)).fetchone()[0]
            try:
                want = (json.loads(mj) if mj else {}).get('tokens_total')
            except Exception:
                want = None
            if want is not None and s != want:
                ed_badsum += 1
        # 切分段不得指向不存在的成员
        ed_orphan = conn.execute("""
            SELECT COUNT(*) FROM article_eda_member_segs s
            WHERE NOT EXISTS (SELECT 1 FROM article_assembly_members m
                              WHERE m.article_id=s.article_id AND m.cls_idx=s.cls_idx
                                AND m.member_idx=s.member_idx)
        """).fetchone()[0]
        print(f"\nArticle EDA: {ed_docs} doc(s) | {ed_mor} morpheme row(s) | {ed_seg} segment row(s)")
        print(f"  unsegmented_tokens={ed_unknown} | no_confidence={ed_noconf} | no_domain={ed_nodom}")
        print(f"  doc_without_method={ed_nomethod} | morpheme_sum_mismatch={ed_badsum} | orphan_segments={ed_orphan}")
        if ed_badsum or ed_orphan or ed_nomethod or ed_noconf or ed_nodom:
            print("  !! Article-EDA integrity problem (see counts above)")

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
    _migrate_chapters_unique(conn)
    import_chapters(conn, id_to_rowid)

    print("\n--- Importing Cross-refs ---")
    import_cross_refs(conn, id_to_rowid)

    print("\n--- Importing Person-Locations ---")
    import_person_locations(conn)

    print("\n--- Importing Article Knowledge Graph ---")
    import_article_knowledge(conn)

    print("\n--- Importing Article Artifacts ---")
    import_article_artifacts(conn)

    print("\n--- Importing Article Assembly (会众结构) ---")
    import_article_assembly(conn)

    print("\n--- Importing Article EDA (名号构词法析构) ---")
    import_article_eda(conn)

    conn.execute("PRAGMA foreign_keys = ON")

    # ---------------------------------------------------------------
    # Safety net: rebuild FTS5 inverted index
    # ---------------------------------------------------------------
    # FTS5 external-content tables (content='xxx') store ONLY the
    # inverted index — row data stays in the source table. AFTER INSERT
    # triggers populate the index as rows land in texts/glossary, but any
    # path that bypasses triggers (ATTACH, bulk .import, direct rowid
    # manipulation, historical DB that added FTS virtual tables AFTER the
    # source data was already loaded) will silently leave the index empty.
    # Symptom: COUNT(*) on FTS table looks right, but MATCH returns 0.
    # Rebuild is cheap + idempotent → always run as final step.
    # ---------------------------------------------------------------
    print("\n--- Rebuilding FTS5 indexes (safety net) ---")
    conn.execute("INSERT INTO texts_fts(texts_fts) VALUES('rebuild')")
    conn.execute("INSERT INTO glossary_fts(glossary_fts) VALUES('rebuild')")
    conn.commit()
    for t in ("texts_fts", "glossary_fts"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {n} rows indexed")
    hit = conn.execute(
        "SELECT COUNT(*) FROM texts_fts WHERE texts_fts MATCH 'avatamsaka'"
    ).fetchone()[0]
    print(f"  sanity MATCH 'avatamsaka': {hit} hit(s)")

    verify_import(conn)

    conn.close()
    print(f"\nDone. Database: {DB_PATH} ({DB_PATH.stat().st_size:,} bytes)")


if __name__ == '__main__':
    main()
