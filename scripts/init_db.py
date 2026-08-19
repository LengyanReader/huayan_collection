#!/usr/bin/env python3
"""Initialize huayan.db from schema.sql"""
import sqlite3, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "catalog" / "huayan.db"
SCHEMA_PATH = ROOT / "data" / "catalog" / "schema.sql"

if DB_PATH.exists():
    os.remove(DB_PATH)
    print(f"Removed old {DB_PATH}")

conn = sqlite3.connect(str(DB_PATH))
with open(SCHEMA_PATH, encoding='utf-8') as f:
    conn.executescript(f.read())

tables = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
).fetchall()]
print(f"Created {DB_PATH}")
print(f"Tables ({len(tables)}): {tables}")
conn.close()
