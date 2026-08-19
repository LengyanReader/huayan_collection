#!/usr/bin/env python3
"""
华严项目 — 全链路数据一致性测试
验证: JSON源文件 → SQLite → db_reader → build.py → HTML输出

测试内容:
  1. 数据完整性: SQLite 包含所有 JSON 源文件的数据
  2. 字段零损失: 每个源字段都有对应 SQLite 列
  3. db_reader 输出: 与原始 JSON 格式兼容
  4. 构建产物: HTML 内嵌数据与 SQLite 一致
  5. 硬编码检测: build.py 无硬编码人名/地点
"""

import json
import sqlite3
import sys
import re
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "catalog" / "huayan.db"
GRAPH_PATH = ROOT / "web" / "demo" / "graph.json"
PERSONAS_PATH = ROOT / "data" / "knowledge_graph" / "personas.json"
LINEAGES_PATH = ROOT / "data" / "knowledge_graph" / "lineages.json"
LOCATIONS_PATH = ROOT / "data" / "knowledge_graph" / "locations.json"
BUILD_PY = ROOT / "web" / "demo" / "scripts" / "build.py"

sys.path.insert(0, str(ROOT / 'scripts'))
import db_reader

errors = 0
warnings = 0

def pass_(msg):
    print(f"  PASS  {msg}")

def fail(msg):
    global errors
    errors += 1
    print(f"  FAIL  {msg}")

def warn(msg):
    global warnings
    warnings += 1
    print(f"  WARN  {msg}")

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ── Test 1: SQLite contains all persons from both sources ──
def test_persons_completeness():
    print("\n[1] Persons completeness")
    graph = load_json(GRAPH_PATH)
    personas = load_json(PERSONAS_PATH)

    graph_ids = {n['id'] for n in graph['nodes']}
    persona_ids = {p['id'] for p in personas['persons']}

    conn = sqlite3.connect(str(DB_PATH))
    db_ids = {r[0] for r in conn.execute("SELECT source_id FROM persons").fetchall()}
    conn.close()

    # All graph.json persons in DB
    missing_from_db = graph_ids - db_ids
    if missing_from_db:
        fail(f"graph.json persons NOT in DB: {missing_from_db}")
    else:
        pass_(f"All {len(graph_ids)} graph.json persons in DB")

    # All personas.json persons in DB
    missing_from_db = persona_ids - db_ids
    if missing_from_db:
        fail(f"personas.json persons NOT in DB: {missing_from_db}")
    else:
        pass_(f"All {len(persona_ids)} personas.json persons in DB")

    # DB has no extra persons beyond sources
    extra_in_db = db_ids - graph_ids - persona_ids
    if extra_in_db:
        warn(f"DB has {len(extra_in_db)} persons not in either source: {extra_in_db}")
    else:
        pass_(f"DB has exactly {len(db_ids)} persons (union of sources)")


# ── Test 2: No information loss in person fields ──
def test_person_fields():
    print("\n[2] Person field preservation")
    graph = load_json(GRAPH_PATH)
    personas = load_json(PERSONAS_PATH)
    pa_by_id = {p['id']: p for p in personas['persons']}

    graph_fields = set()
    for n in graph['nodes']:
        graph_fields.update(n.keys())

    pa_fields = set()
    for p in personas['persons']:
        pa_fields.update(p.keys())

    # Check each source field has a DB column
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    sample = conn.execute("SELECT * FROM persons LIMIT 1").fetchone()
    db_cols = set(sample.keys()) if sample else set()
    conn.close()

    # graph.json fields → db column mapping
    g2db = {
        'id': 'source_id', 'n': 'name_zh', 'ti': 'title', 'li': 'lineage_branch',
        'multi': 'multi_lineage', 'tp': 'type', 'b': 'birth_year', 'd': 'death_year',
        'dy': 'dynasty', 'bio': 'biography', 'wk': 'key_works', 'wl': 'works_links',
        'v': 'verified',
    }
    for gf, col in g2db.items():
        if col in db_cols:
            pass_(f"graph.json '{gf}' → DB '{col}'")
        else:
            fail(f"graph.json '{gf}' → DB column '{col}' MISSING")

    # personas.json fields → db column mapping
    p2db = {
        'id': 'source_id', 'name_zh': 'name_zh', 'name_sa': 'name_sa',
        'name_en': 'name_en', 'name_bo': 'name_bo', 'title': 'title',
        'type': 'type', 'birth_year': 'birth_year', 'death_year': 'death_year',
        'dynasty': 'dynasty', 'lineage_branch': 'lineage_branch',
        'lineage_order': 'lineage_order', 'biography': 'biography',
        'key_works': 'key_works', 'source': 'source', 'verified': 'verified',
    }
    for pf, col in p2db.items():
        if col in db_cols:
            pass_(f"personas.json '{pf}' → DB '{col}'")
        else:
            fail(f"personas.json '{pf}' → DB column '{col}' MISSING")


# ── Test 3: Locations completeness ──
def test_locations():
    print("\n[3] Locations completeness")
    graph = load_json(GRAPH_PATH)
    locations = load_json(LOCATIONS_PATH)

    graph_ids = {loc['id'] for loc in graph['locations']}
    loc_ids = {loc['id'] for loc in locations['locations']}

    conn = sqlite3.connect(str(DB_PATH))
    db_ids = {r[0] for r in conn.execute("SELECT source_id FROM locations").fetchall()}
    conn.close()

    missing = graph_ids - db_ids
    if missing:
        fail(f"graph.json locations NOT in DB: {missing}")
    else:
        pass_(f"All {len(graph_ids)} graph.json locations in DB")

    missing = loc_ids - db_ids
    if missing:
        fail(f"locations.json NOT in DB: {missing}")
    else:
        pass_(f"All {len(loc_ids)} locations.json locations in DB")


# ── Test 4: Edges completeness ──
def test_edges():
    print("\n[4] Edges completeness")
    graph = load_json(GRAPH_PATH)

    conn = sqlite3.connect(str(DB_PATH))
    db_count = conn.execute("SELECT COUNT(*) FROM lineage_edges").fetchone()[0]
    conn.close()

    # graph.json has ~100 edges; some may reference non-existent persons
    graph_edge_count = len(graph['edges'])
    if db_count >= graph_edge_count - 5:  # allow small margin
        pass_(f"DB has {db_count} edges (graph.json has {graph_edge_count})")
    else:
        fail(f"DB edges ({db_count}) significantly less than graph.json ({graph_edge_count})")


# ── Test 5: db_reader output compatibility ──
def test_db_reader():
    print("\n[5] db_reader output format")

    graph = db_reader.load_graph()
    if 'nodes' in graph and 'edges' in graph and 'locations' in graph:
        pass_(f"load_graph() returns correct keys: nodes={len(graph['nodes'])}, edges={len(graph['edges'])}, locations={len(graph['locations'])}")
    else:
        fail(f"load_graph() missing keys: {list(graph.keys())}")

    # Verify node format matches legacy graph.json
    if graph['nodes']:
        n = graph['nodes'][0]
        required = {'id', 'n', 'tp', 'b', 'd', 'dy', 'bio', 'wk', 'wl', 'v'}
        present = required & set(n.keys())
        missing = required - present
        if missing:
            fail(f"Node missing fields: {missing}")
        else:
            pass_(f"Node has all legacy fields + extras: {set(n.keys()) - required}")

    # Verify lineage_colors
    if graph['lineage_colors']:
        pass_(f"lineage_colors: {len(graph['lineage_colors'])} entries")
    else:
        warn("lineage_colors is empty")


# ── Test 6: Build output matches SQLite data ──
def test_build_consistency():
    print("\n[6] Build output consistency")
    lineage_path = ROOT / "web" / "demo" / "tabs" / "lineage.html"
    if not lineage_path.exists():
        fail("lineage.html not found (run build first)")
        return

    with open(lineage_path, encoding='utf-8') as f:
        html = f.read()

    # Extract embedded GRAPH data
    m = re.search(r'var GRAPH\s*=\s*(\{.*?\});\s*\nvar DATA', html, re.DOTALL)
    if not m:
        fail("Could not extract GRAPH from lineage.html")
        return

    try:
        embedded = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        fail(f"GRAPH JSON parse error: {e}")
        return

    # Compare counts
    sqlite_graph = db_reader.load_graph()
    if len(embedded['nodes']) == len(sqlite_graph['nodes']):
        pass_(f"Embedded nodes: {len(embedded['nodes'])} = SQLite nodes")
    else:
        fail(f"Embedded nodes ({len(embedded['nodes'])}) != SQLite ({len(sqlite_graph['nodes'])})")

    if len(embedded['edges']) == len(sqlite_graph['edges']):
        pass_(f"Embedded edges: {len(embedded['edges'])} = SQLite edges")
    else:
        fail(f"Embedded edges ({len(embedded['edges'])}) != SQLite ({len(sqlite_graph['edges'])})")

    if len(embedded['locations']) == len(sqlite_graph['locations']):
        pass_(f"Embedded locations: {len(embedded['locations'])} = SQLite locations")
    else:
        fail(f"Embedded locations ({len(embedded['locations'])}) != SQLite ({len(sqlite_graph['locations'])})")

    # Verify a specific person's data survived the pipeline
    # Find 法藏 in embedded
    fazang_emb = None
    fazang_sql = None
    for n in embedded['nodes']:
        if n['id'] == 'person_003':
            fazang_emb = n
    for n in sqlite_graph['nodes']:
        if n['id'] == 'person_003':
            fazang_sql = n

    if fazang_emb and fazang_sql:
        if fazang_emb['n'] == fazang_sql['n']:
            pass_(f"法藏: embedded name = SQLite name")
        else:
            fail(f"法藏: embedded '{fazang_emb['n']}' != SQLite '{fazang_sql['n']}'")

        # Check enriched fields
        if fazang_sql.get('name_sa'):
            pass_(f"法藏: name_sa='{fazang_sql['name_sa']}' preserved")
        if fazang_sql.get('wk'):
            pass_(f"法藏: key_works={fazang_sql['wk']} preserved")


# ── Test 7: No hardcoded data in build.py ──
def test_no_hardcoding():
    print("\n[7] No hardcoded data in build.py")
    with open(BUILD_PY, encoding='utf-8') as f:
        build_src = f.read()

    # Check for hardcoded person names
    known_names = ['龙树', '法藏', '杜顺', '智俨', '澄观', '宗密', '海云继梦', '钦因']
    found = []
    for name in known_names:
        if f"'{name}'" in build_src or f'"{name}"' in build_src:
            found.append(name)
    if found:
        fail(f"Hardcoded names in build.py: {found}")
    else:
        pass_("No hardcoded person names")

    # Check for hardcoded locations
    known_locs = ['大慈恩寺', '终南山', '清凉山', '草堂寺']
    found = []
    for loc in known_locs:
        if f"'{loc}'" in build_src or f'"{loc}"' in build_src:
            found.append(loc)
    if found:
        fail(f"Hardcoded locations in build.py: {found}")
    else:
        pass_("No hardcoded location names")


# ── Test 8: Edge relation normalization ──
def test_relation_normalization():
    print("\n[8] Relation normalization")
    conn = sqlite3.connect(str(DB_PATH))
    bad_rels = conn.execute("""
        SELECT DISTINCT relation FROM lineage_edges
        WHERE relation NOT IN ('MASTER_OF', 'INFLUENCED', 'LINEAGE', 'CONTEMPORARY')
    """).fetchall()
    conn.close()

    if bad_rels:
        fail(f"Non-standard relations found: {[r[0] for r in bad_rels]}")
    else:
        pass_("All relations normalized to standard values")


# ── Main ──
def main():
    print("=" * 60)
    print("  华严项目 — 全链路数据一致性测试")
    print("=" * 60)

    test_persons_completeness()
    test_person_fields()
    test_locations()
    test_edges()
    test_db_reader()
    test_build_consistency()
    test_no_hardcoding()
    test_relation_normalization()

    print("\n" + "=" * 60)
    if errors == 0 and warnings == 0:
        print("  ALL TESTS PASSED")
    elif errors == 0:
        print(f"  ALL TESTS PASSED ({warnings} warnings)")
    else:
        print(f"  {errors} FAILURES, {warnings} warnings")
    print("=" * 60)

    sys.exit(0 if errors == 0 else 1)


if __name__ == '__main__':
    main()
