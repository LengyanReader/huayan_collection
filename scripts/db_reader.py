import os
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
               works_links, multi_lineage, verified, source
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
            "src": r['source'] or '',
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
               related_persons, city, province, current_name, source
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
            "source": r['source'] or '',
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


def load_article_knowledge():
    """Export per-article knowledge graphs (名相·会处·术语) for the article renderer.

    Returns: {article_id: {"title": ..., "terms": [...], "links": [...]}}

    Populated by scripts/import_all_to_sqlite.py from
    data/translation/article_knowledge/*.yaml into article_terms / article_term_links.
    `grade` is the provenance level (A1 经文直证 / A2 古注明证 / B 文献转述 /
    C 单一来源待考 / D 疑讹不采用); grade D always carries status='rejected' and the
    renderer must not treat it as in-use terminology. `links` are the edges among an
    article's own terms plus edges out to the existing entity tables (chapter, location,
    term, …), which is what lets the UI offer related-node navigation.
    """
    conn = get_conn()
    have = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    if not {'article_terms', 'article_term_links'} <= have:
        conn.close()
        return {}

    trows = conn.execute("""
        SELECT article_id, term_id, term_zh, aliases, category, grade, status,
               definition_zh, definition_en, source_note, source_url, note
        FROM article_terms ORDER BY article_id, term_id
    """).fetchall()
    lrows = conn.execute("""
        SELECT article_id, from_term_id, rel, to_type, to_ref, to_label, note
        FROM article_term_links ORDER BY article_id, from_term_id, rel, to_ref
    """).fetchall()

    out = {}
    for r in trows:
        aid = r['article_id']
        art = out.setdefault(aid, {"terms": [], "links": []})
        art["terms"].append({
            "id": r['term_id'],
            "zh": r['term_zh'] or '',
            "aliases": _j_load(r['aliases']) or [],
            "category": r['category'] or '',
            "grade": r['grade'] or '',
            "status": r['status'] or '',
            "def_zh": r['definition_zh'] or '',
            "def_en": r['definition_en'] or '',
            "source": r['source_note'] or '',
            "source_url": r['source_url'] or '',
            "note": r['note'] or '',
        })
    for r in lrows:
        aid = r['article_id']
        art = out.setdefault(aid, {"terms": [], "links": []})
        art["links"].append({
            "from": r['from_term_id'],
            "rel": r['rel'] or '',
            "to_type": r['to_type'] or '',
            "to_ref": r['to_ref'] or '',
            "to_label": r['to_label'] or '',
            "note": r['note'] or '',
        })

    # Article titles come from the standalone-article registry so the UI can label the
    # panel without duplicating names here.
    try:
        import yaml
        reg = ROOT / "data" / "translation" / "standalone_articles.yaml"
        titles = {}
        if reg.exists():
            data = yaml.safe_load(reg.read_text(encoding='utf-8')) or {}
            for grp in ('sources', 'others'):
                for a in (data.get(grp) or []):
                    if isinstance(a, dict) and a.get('id'):
                        titles[a['id']] = a.get('title') or a['id']
        for aid, art in out.items():
            art["title"] = titles.get(aid, aid)
    except Exception:
        for aid, art in out.items():
            art["title"] = aid

    # 组装双向邻接：每个节点带 out（本节点发出的边）与 in（指向本节点的边），
    # 使前端渲染「关联节点」跳转时无需二次扫描，也免去前端拼字段名。
    for art in out.values():
        incoming = {t["id"]: [] for t in art["terms"]}
        for l in art["links"]:
            edge = {"rel": l["rel"], "to_type": l["to_type"],
                    "to_ref": l["to_ref"], "to_label": l["to_label"], "note": l["note"]}
            src = None
            for t in art["terms"]:
                if t["id"] == l["from"]:
                    src = t
                    break
            if src is not None:
                src.setdefault("out", []).append(dict(edge, to_label=edge["to_label"] or edge["to_ref"]))
            if l["to_type"] == "term" and l["to_ref"] in incoming:
                incoming[l["to_ref"]].append({
                    "from": l["from"], "rel": l["rel"], "to_type": l["to_type"],
                    "to_ref": l["to_ref"], "to_label": l["to_label"], "note": l["note"],
                })
        for t in art["terms"]:
            t.setdefault("in", incoming.get(t["id"], []))
            t.setdefault("out", [])

    conn.close()
    return out


def load_article_artifacts():
    """Export per-article artwork/relic/archaeology registers for the article renderer.

    Returns: {article_id: {"title": ..., "items": [...]}}

    Populated by scripts/import_all_to_sqlite.py from
    data/translation/article_artifacts/*.yaml into article_artifacts.
    Only status='confirmed' rows are meant to surface in the UI; pending/rejected stay
    in the database as an auditable candidate register until a human has compared them
    against the text (registration precedes display).
    """
    conn = get_conn()
    have = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    if 'article_artifacts' not in have:
        conn.close()
        return {}

    rows = conn.execute("""
        SELECT article_id, artifact_id, title_zh, title_en, era, location, category,
               grade, status, relevance_zh, relevance_en, href, thumb_url,
               source_note, license, note
        FROM article_artifacts ORDER BY article_id, grade, category, artifact_id
    """).fetchall()

    out = {}
    for r in rows:
        aid = r['article_id']
        art = out.setdefault(aid, {"items": []})
        art["items"].append({
            "id": r['artifact_id'],
            "title": r['title_zh'] or '',
            "title_en": r['title_en'] or '',
            "era": r['era'] or '',
            "location": r['location'] or '',
            "category": r['category'] or '',
            "grade": r['grade'] or '',
            "status": r['status'] or '',
            "relevance": r['relevance_zh'] or '',
            "relevance_en": r['relevance_en'] or '',
            "href": r['href'] or '',
            "thumb": r['thumb_url'] or '',
            "source": r['source_note'] or '',
            "license": r['license'] or '',
            "note": r['note'] or '',
        })

    try:
        import yaml
        reg = ROOT / "data" / "translation" / "standalone_articles.yaml"
        titles = {}
        if reg.exists():
            data = yaml.safe_load(reg.read_text(encoding='utf-8')) or {}
            for grp in ('sources', 'others'):
                for a in (data.get(grp) or []):
                    if isinstance(a, dict) and a.get('id'):
                        titles[a['id']] = a.get('title') or a['id']
        for aid, art in out.items():
            art["title"] = titles.get(aid, aid)
    except Exception:
        for aid, art in out.items():
            art["title"] = aid

    conn.close()
    return out


def load_article_assembly():
    """Export per-article 会众结构 (class × member × domain × vow) for the article renderer.

    Returns: {article_id: {"title": ..., "classes": [...]}}

    Populated by scripts/import_all_to_sqlite.py from
    data/translation/*_assembly.yaml into article_assembly_classes/members.

    `n_named` counts the members the sutra names outright and is NOT the size of the
    class, which the sutra gives only as 微塵數／無量; `count_expr` preserves the sutra's
    own phrasing. The renderer must not present n_named as a headcount.
    """
    conn = get_conn()
    have = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    if not {'article_assembly_classes', 'article_assembly_members'} <= have:
        conn.close()
        return {}

    crows = conn.execute("""
        SELECT article_id, cls_idx, cat_zh, group_key, group_zh, realm, count_expr,
               leader_zh, n_named, domain_zh, collective_zh, collective_pos, vow_kind,
               vow_zh, punct_variant, glyph_variant, source_note
        FROM article_assembly_classes ORDER BY article_id, cls_idx
    """).fetchall()
    mrows = conn.execute("""
        SELECT article_id, cls_idx, member_idx, member_zh, is_leader
        FROM article_assembly_members ORDER BY article_id, cls_idx, member_idx
    """).fetchall()

    members = {}
    for r in mrows:
        members.setdefault((r['article_id'], r['cls_idx']), []).append({
            "i": r['member_idx'],
            "name": r['member_zh'] or '',
            "is_leader": 1 if r['is_leader'] else 0,
        })

    out = {}
    for r in crows:
        aid = r['article_id']
        art = out.setdefault(aid, {"classes": []})
        art["classes"].append({
            "idx": r['cls_idx'],
            "cat": r['cat_zh'] or '',
            "group": r['group_key'] or '',
            "group_zh": r['group_zh'] or '',
            "realm": r['realm'] or '',
            "count_expr": r['count_expr'] or '',
            "leader": r['leader_zh'] or '',
            "n_named": r['n_named'] or 0,
            "domain": r['domain_zh'] or '',
            "collective": r['collective_zh'] or '',
            "collective_pos": r['collective_pos'] or '',
            "vow_kind": r['vow_kind'] or '',
            "vow": r['vow_zh'] or '',
            "punct_variant": r['punct_variant'] or '',
            "glyph_variant": r['glyph_variant'] or '',
            "source": r['source_note'] or '',
            "members": members.get((aid, r['cls_idx']), []),
        })

    _attach_article_titles(out, conn)
    conn.close()
    return out


def load_article_eda():
    """Export per-article 名号构词法 EDA (editorial segmentation analysis).

    Returns: {article_id: {"title": ..., "source": ..., "method": {...}, "metrics": {...},
                           "payload": {...}}}

    Populated by scripts/import_all_to_sqlite.py from data/translation/*_eda.yaml
    (generated by scripts/miaoyan_eda.py) into article_eda_docs / _morphemes / _member_segs.

    ⚠ This is **editorial analysis, not sutra fact**. The segmentation is a chosen
    method, `domain` is one normalising reading rather than a gloss of every sense, and
    `confidence` marks how firm each reading is. The renderer must surface `method` and
    the unassigned/low-confidence counts rather than presenting the matrices as findings
    of the text. Sutra facts live in load_article_assembly() and must not be sourced here:
    `eda_classes` deliberately omits names, count expressions, domains and vows for that
    reason, so the two loaders are meant to be joined on `idx`/`i`.
    """
    conn = get_conn()
    have = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    if 'article_eda_docs' not in have:
        conn.close()
        return {}

    rows = conn.execute("""
        SELECT article_id, source, source_url, generated_by,
               method_json, metrics_json, payload_json
        FROM article_eda_docs ORDER BY article_id
    """).fetchall()

    out = {}
    for r in rows:
        out[r['article_id']] = {
            "source": r['source'] or '',
            "source_url": r['source_url'] or '',
            "generated_by": r['generated_by'] or '',
            "method": _j_load(r['method_json']) or {},
            "metrics": _j_load(r['metrics_json']) or {},
            "payload": _j_load(r['payload_json']) or {},
        }

    # Per-article morpheme rows carry the glosses; the payload's morph_freq is the
    # ranked list. Merge the glosses on so the renderer need not hold two tables.
    mrows = conn.execute("""
        SELECT article_id, zh, n, n_char_only, seg_mode, domain, confidence,
               gloss, gloss_en, rank
        FROM article_eda_morphemes ORDER BY article_id, rank
    """).fetchall()
    glosses = {}
    for r in mrows:
        glosses.setdefault(r['article_id'], {})[r['zh']] = {
            "n": r['n'] or 0,
            "n_char_only": r['n_char_only'] or 0,
            "mode": r['seg_mode'] or 'char',
            "domain": r['domain'] or 'unassigned',
            "c": r['confidence'] or 'low',
            "gloss": r['gloss'] or '',
            "gloss_en": r['gloss_en'] or '',
        }
    for aid, doc in out.items():
        doc["morphemes"] = glosses.get(aid, {})
        # Per-class analysis, joined to the sutra facts by the caller. `eda_classes` holds
        # only the editorial half (segmentation + histograms); class names, count
        # expressions, domains and vows come from load_article_assembly() so that no sutra
        # fact is stated twice. Join key is `idx` (class) and `i` (member within class).
        doc["eda_classes"] = (doc.get("payload") or {}).get("eda_classes") or []

    _attach_article_titles(out, conn)
    conn.close()
    return out


def _attach_article_titles(out, conn=None):
    """Fill in each article's display title from the standalone-article registry.

    Article titles are not duplicated into the feature tables; the registry is the one
    place a title is stated, so the panels label themselves from it.
    """
    try:
        import yaml
        reg = ROOT / "data" / "translation" / "standalone_articles.yaml"
        titles = {}
        if reg.exists():
            data = yaml.safe_load(reg.read_text(encoding='utf-8')) or {}
            for grp in ('sources', 'others'):
                for a in (data.get(grp) or []):
                    if isinstance(a, dict) and a.get('id'):
                        titles[a['id']] = a.get('title') or a['id']
        for aid, art in out.items():
            art["title"] = titles.get(aid, aid)
    except Exception:
        for aid, art in out.items():
            art["title"] = aid


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


def search_texts(query: str, limit: int = 20):
    """FTS5 全文检索 texts（title_zh/bo/sa/en + abstract + dynasty + date_text）。

    两层策略：
      1) FTS5 MATCH（对 Latin 与 整串 CJK 词都能快命）
      2) 若 CJK 查询且 MATCH 无命中 →回退 LIKE（兼容 unicode61 把连续 CJK 归一 token 导致的子串不能默认命的问题）
    返回 [{id, title_zh, title_en, dynasty, date_text, snip, score}]
    """
    q = (query or '').strip()
    if not q:
        return []
    has_cjk = any('\u4e00' <= c <= '\u9fff' for c in q)
    match_expr = f'"{q}"' if has_cjk else q
    conn = get_conn()
    rows = conn.execute(
        """SELECT t.id, t.title_zh, t.title_en, t.dynasty, t.date_text,
                  snippet(texts_fts, 4, '[', ']', '…', 20) AS snip,
                  bm25(texts_fts) AS score
           FROM texts_fts
           JOIN texts t ON t.id = texts_fts.rowid
           WHERE texts_fts MATCH ?
           ORDER BY score
           LIMIT ?""",
        (match_expr, limit)
    ).fetchall()
    if not rows and has_cjk:
        like = f'%{q}%'
        rows = conn.execute(
            """SELECT id, title_zh, title_en, dynasty, date_text,
                      substr(COALESCE(abstract,''), 1, 120) AS snip,
                      0 AS score
               FROM texts
               WHERE title_zh LIKE ? OR title_en LIKE ?
                    OR COALESCE(abstract,'') LIKE ? OR dynasty LIKE ?
               ORDER BY id LIMIT ?""",
            (like, like, like, like, limit)
        ).fetchall()
    return [dict(r) for r in rows]


def search_glossary(query: str, limit: int = 20):
    """FTS5 全文检索 glossary（term_zh/sa/bo/en + definition_zh/en）·CJK 同 texts 两层策略。"""
    q = (query or '').strip()
    if not q:
        return []
    has_cjk = any('\u4e00' <= c <= '\u9fff' for c in q)
    match_expr = f'"{q}"' if has_cjk else q
    conn = get_conn()
    rows = conn.execute(
        """SELECT g.id, g.term_zh, g.term_sa, g.term_bo, g.term_en,
                  snippet(glossary_fts, 4, '[', ']', '…', 20) AS snip,
                  bm25(glossary_fts) AS score
           FROM glossary_fts
           JOIN glossary g ON g.id = glossary_fts.rowid
           WHERE glossary_fts MATCH ?
           ORDER BY score
           LIMIT ?""",
        (match_expr, limit)
    ).fetchall()
    if not rows and has_cjk:
        like = f'%{q}%'
        rows = conn.execute(
            """SELECT id, term_zh, term_sa, term_bo, term_en,
                      substr(COALESCE(definition_zh,''), 1, 120) AS snip,
                      0 AS score
               FROM glossary
               WHERE term_zh LIKE ? OR term_en LIKE ? OR term_sa LIKE ?
                    OR COALESCE(definition_zh,'') LIKE ? OR COALESCE(definition_en,'') LIKE ?
               ORDER BY id LIMIT ?""",
            (like, like, like, like, like, limit)
        ).fetchall()
    return [dict(r) for r in rows]


if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
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
    elif '--search' in sys.argv:
        idx = sys.argv.index('--search')
        q = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ''
        if not q:
            print("Need query. Usage: python scripts/db_reader.py --search 华严")
            sys.exit(1)
        tt = search_texts(q, limit=10)
        gl = search_glossary(q, limit=10)
        print(f"=== TEXTS · {q} · {len(tt)} hit(s) ===")
        for r in tt:
            head = f"  [{r['id']:>3}] {(r.get('title_zh') or '').strip()}"
            meta = ' · '.join(x for x in [r.get('dynasty') or '', r.get('title_en') or ''] if x)
            if meta:
                head += f"  ({meta})"
            print(head)
            if r.get('snip'):
                print(f"        {r['snip']}")
        print(f"\n=== GLOSSARY · {q} · {len(gl)} hit(s) ===")
        for r in gl:
            terms = ' / '.join(x for x in [r.get('term_zh') or '', r.get('term_sa') or '', r.get('term_en') or ''] if x)
            print(f"  [{r['id']:>3}] {terms}")
            if r.get('snip'):
                print(f"        {r['snip']}")
    else:
        print("Usage: python scripts/db_reader.py [--stats|--export DIR|--verify|--search QUERY]")








def load_article_bi() -> dict[str, any]:
    articles = {}
    return articles



def load_article_bi() -> dict[str, any]:
    articles = {}
    p_list = os.path.join(ROOT, 'data', 'translation', 'standalone_articles.yaml')
    if os.path.exists(p_list):
        try:
            with open(p_list, 'r', encoding='utf-8') as f:
                lst = yaml.safe_load(f) or {}
            for k in ('sources', 'others'):
                for a in lst.get(k, []):
                    if isinstance(a, str):
                        aid = a
                    elif isinstance(a, dict):
                        aid = a.get('id')
                    else:
                        aid = None
                    if aid:
                        articles[aid] = {}
        except Exception:
            pass
    articles.setdefault('shizhu-miaoyan', {})
    db_path = os.path.join(ROOT, 'data', 'catalog', 'huayan.db')
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('SELECT article_id, payload_json, method_json, metrics_json, source, source_url, generated_by FROM article_bi_docs')
            for r in cur.fetchall():
                aid = r['article_id']
                if aid in articles:
                    payload = {}
                    try:
                        payload = json.loads(r['payload_json']) if r['payload_json'] else {}
                    except Exception:
                        payload = {}
                    articles[aid] = payload
            conn.close()
        except Exception:
            pass
    if 'shizhu-miaoyan' in articles and not articles['shizhu-miaoyan']:
        p2 = os.path.join(ROOT, 'data', 'translation', 'miaoyan_bi.yaml')
        if os.path.exists(p2):
            try:
                with open(p2, 'r', encoding='utf-8') as f2:
                    d = yaml.safe_load(f2) or {}
                articles['shizhu-miaoyan'] = d
            except Exception:
                pass
    return articles



def load_miaoyan_narrative():
    import os, yaml
    DATA_DIR = os.path.join(ROOT, 'data')
    p = os.path.join(DATA_DIR, 'narrative', 'miaoyan_narrative.yaml')
    if not os.path.exists(p): return {}
    with open(p, encoding='utf-8') as f2:
        y = yaml.safe_load(f2) or {}
    beats = y.get('beats') or []
    beats_sorted = sorted(beats, key=lambda x: (x.get('order') if x.get('order') is not None else 999))
    y['beats'] = beats_sorted
    return y


def _load_narrative_library(kind):
    """按文章 id 归集的叙事／分镜库（通用，供任意独立文章页复用）。

    扫 `data/narrative/*_<kind>.yaml`，以各文件 `meta.article` 为键。
    未标 `meta.article` 者不入册（避免全局单例误挂到别篇）。
    narrative 之 beats 依 order 排序；storyboard 交渲染器自排，不加干预。
    """
    import glob as _glob, yaml as _yaml
    lib = {}
    d = os.path.join(ROOT, 'data', 'narrative')
    if not os.path.isdir(d):
        return lib
    for p in sorted(_glob.glob(os.path.join(d, '*_%s.yaml' % kind))):
        try:
            with open(p, encoding='utf-8') as f:
                y = _yaml.safe_load(f) or {}
        except Exception:
            continue
        aid = (y.get('meta') or {}).get('article')
        if not aid:
            continue
        if kind == 'narrative':
            beats = y.get('beats') or []
            y['beats'] = sorted(beats, key=lambda x: (x.get('order') if x.get('order') is not None else 999))
        lib[aid] = y
    return lib


def load_narrative_library():
    """按文章 id 索引的叙事动画库（data/narrative/*_narrative.yaml）。"""
    return _load_narrative_library('narrative')


def load_storyboard_library():
    """按文章 id 索引的分镜库（data/narrative/*_storyboard.yaml）。"""
    return _load_narrative_library('storyboard')


def load_miaoyan_keypoints():
    """一品要点导览（data/narrative/miaoyan_keypoints.yaml）。

    要点一律依 `idx` 排序，不依赖 YAML 书写次序——重排文件不应改变编次。
    （注：字段名取 `idx` 而非 `no`——YAML 1.1 会将裸 `no` 解析为布尔键 False。）
    实算要点数与总时长，供页面与校验器共用同一口径（免两处各算一遍而生歧）。
    """
    import os, yaml
    DATA_DIR = os.path.join(ROOT, 'data')
    p = os.path.join(DATA_DIR, 'narrative', 'miaoyan_keypoints.yaml')
    if not os.path.exists(p): return {}
    with open(p, encoding='utf-8') as f2:
        y = yaml.safe_load(f2) or {}
    kps = y.get('keypoints') or []
    kps = sorted(kps, key=lambda x: (x.get('idx') if x.get('idx') is not None else 999))
    y['keypoints'] = kps
    y['keypoint_count'] = len(kps)
    y['duration_total_s'] = sum(k.get('duration_s') or 0 for k in kps)
    return y
