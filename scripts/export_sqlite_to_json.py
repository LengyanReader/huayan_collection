#!/usr/bin/env python3
"""
华严项目 — SQLite 数据导入/导出脚本 (v0.2.0)
用法:
  python scripts/export_sqlite_to_json.py --import    # JSON/YAML → SQLite (多源合并)
  python scripts/export_sqlite_to_json.py --export    # SQLite → JSON (db_reader)
  python scripts/export_sqlite_to_json.py --verify    # 数据完整性报告
  python scripts/export_sqlite_to_json.py --init      # 初始化空数据库
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

# Ensure scripts/ is importable
sys.path.insert(0, str(ROOT / 'scripts'))


def init_database():
    """Initialize huayan.db from schema.sql."""
    import import_all_to_sqlite
    schema_path = ROOT / "data" / "catalog" / "schema.sql"
    if DB_PATH.exists():
        os.remove(DB_PATH)
    conn = sqlite3.connect(str(DB_PATH))
    with open(schema_path, encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print(f"Initialized {DB_PATH}")


def import_data():
    """Import data from all JSON/YAML sources into SQLite."""
    import import_all_to_sqlite
    # Reuse the comprehensive import script
    old_argv = sys.argv
    sys.argv = ['import_all_to_sqlite.py']
    try:
        import_all_to_sqlite.main()
    finally:
        sys.argv = old_argv


def export_data():
    """Export SQLite data to JSON files using db_reader."""
    import db_reader

    kg_dir = ROOT / "data" / "knowledge_graph"
    demo_dir = ROOT / "web" / "demo"

    print("Exporting SQLite → JSON files...")

    # Export graph.json (for build.py compatibility)
    graph = db_reader.load_graph()
    with open(demo_dir / 'graph.json', 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"  {demo_dir / 'graph.json'}: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges, {len(graph['locations'])} locations")

    # Export personas.json
    personas = db_reader.load_personas()
    with open(kg_dir / 'personas.json', 'w', encoding='utf-8') as f:
        json.dump(personas, f, ensure_ascii=False, indent=2)
    print(f"  {kg_dir / 'personas.json'}: {len(personas['persons'])} persons")

    # Export lineages.json
    lineages = db_reader.load_lineages()
    with open(kg_dir / 'lineages.json', 'w', encoding='utf-8') as f:
        json.dump(lineages, f, ensure_ascii=False, indent=2)
    print(f"  {kg_dir / 'lineages.json'}: {len(lineages['lineages'])} lineages")

    # Export locations.json
    locations = db_reader.load_locations()
    with open(kg_dir / 'locations.json', 'w', encoding='utf-8') as f:
        json.dump(locations, f, ensure_ascii=False, indent=2)
    print(f"  {kg_dir / 'locations.json'}: {len(locations['locations'])} locations")

    # Export glossary
    glossary = db_reader.load_glossary()
    print(f"  Glossary: {len(glossary)} terms (still in YAML as primary)")


def verify_data():
    """Print data integrity report."""
    import import_all_to_sqlite
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} does not exist")
        sys.exit(1)
    conn = sqlite3.connect(str(DB_PATH))
    import_all_to_sqlite.verify_import(conn)
    conn.close()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == '--init':
        init_database()

    elif cmd == '--import':
        print("Importing data → SQLite (multi-source merge)...")
        import_data()

    elif cmd == '--export':
        export_data()

    elif cmd == '--verify':
        verify_data()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == '__main__':
    main()
