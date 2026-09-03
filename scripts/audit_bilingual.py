#!/usr/bin/env python3
"""Audit bilingual (EN/SA/BO) coverage across all SQLite tables."""
import sqlite3
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "catalog" / "huayan.db"

def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row

    # === TEXTS ===
    print("=== TEXTS ===")
    texts = conn.execute("SELECT id, title_zh, title_en, title_sa, title_bo FROM texts ORDER BY id").fetchall()
    n = len(texts)
    has_en = sum(1 for t in texts if t["title_en"])
    has_sa = sum(1 for t in texts if t["title_sa"])
    has_bo = sum(1 for t in texts if t["title_bo"])
    print(f"  Total: {n}  |  title_en: {has_en}/{n}  |  title_sa: {has_sa}/{n}  |  title_bo: {has_bo}/{n}")

    print("  [MISSING title_en]")
    for t in texts:
        if not t["title_en"]:
            print(f"    id={t['id']}: {t['title_zh']}")
    print("  [MISSING title_sa]")
    for t in texts:
        if not t["title_sa"]:
            print(f"    id={t['id']}: {t['title_zh']}")
    print("  [MISSING title_bo]")
    for t in texts:
        if not t["title_bo"]:
            print(f"    id={t['id']}: {t['title_zh']}")
    print("  [HAS title_sa]")
    for t in texts:
        if t["title_sa"]:
            print(f"    id={t['id']}: {t['title_zh']} => {t['title_sa']}")
    print("  [HAS title_bo]")
    for t in texts:
        if t["title_bo"]:
            print(f"    id={t['id']}: {t['title_zh']} => {t['title_bo']}")

    # === CHAPTERS ===
    print("\n=== CHAPTERS ===")
    ch = conn.execute("""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN title_en != '' AND title_en IS NOT NULL THEN 1 ELSE 0 END) as has_en,
               SUM(CASE WHEN title_sa != '' AND title_sa IS NOT NULL THEN 1 ELSE 0 END) as has_sa,
               SUM(CASE WHEN title_bo != '' AND title_bo IS NOT NULL THEN 1 ELSE 0 END) as has_bo
        FROM chapters""").fetchone()
    print(f"  Total: {ch['total']}  |  title_en: {ch['has_en']}/{ch['total']}  |  title_sa: {ch['has_sa']}/{ch['total']}  |  title_bo: {ch['has_bo']}/{ch['total']}")

    print("  [MISSING title_en] (sample)")
    rows = conn.execute("SELECT id, sutra_id, title_zh FROM chapters WHERE title_en IS NULL OR title_en = '' LIMIT 20").fetchall()
    for r in rows:
        print(f"    ch#{r['id']} (sutra {r['sutra_id']}): {r['title_zh']}")
    print("  [MISSING title_sa] (sample)")
    rows = conn.execute("SELECT id, sutra_id, title_zh FROM chapters WHERE title_sa IS NULL OR title_sa = '' LIMIT 20").fetchall()
    for r in rows:
        print(f"    ch#{r['id']} (sutra {r['sutra_id']}): {r['title_zh']}")

    # === PERSONS ===
    print("\n=== PERSONS ===")
    p = conn.execute("""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN name_en != '' AND name_en IS NOT NULL THEN 1 ELSE 0 END) as has_en,
               SUM(CASE WHEN name_sa != '' AND name_sa IS NOT NULL THEN 1 ELSE 0 END) as has_sa,
               SUM(CASE WHEN name_bo != '' AND name_bo IS NOT NULL THEN 1 ELSE 0 END) as has_bo,
               SUM(CASE WHEN name_ja != '' AND name_ja IS NOT NULL THEN 1 ELSE 0 END) as has_ja
        FROM persons""").fetchone()
    print(f"  Total: {p['total']}  |  EN: {p['has_en']}/{p['total']}  |  SA: {p['has_sa']}/{p['total']}  |  BO: {p['has_bo']}/{p['total']}  |  JA: {p['has_ja']}/{p['total']}")

    print("  [MISSING name_en]")
    rows = conn.execute("SELECT source_id, name_zh FROM persons WHERE name_en IS NULL OR name_en = '' ORDER BY id").fetchall()
    for r in rows:
        print(f"    {r['source_id']}: {r['name_zh']}")

    # === LOCATIONS ===
    print("\n=== LOCATIONS (no name_en column — all need EN if desired) ===")
    locs = conn.execute("SELECT source_id, name_zh, current_name FROM locations ORDER BY id").fetchall()
    print(f"  Total: {len(locs)} (locations table has no name_en column)")

    # === GLOSSARY ===
    print("\n=== GLOSSARY ===")
    g = conn.execute("""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN term_en != '' AND term_en IS NOT NULL THEN 1 ELSE 0 END) as has_en,
               SUM(CASE WHEN definition_en != '' AND definition_en IS NOT NULL THEN 1 ELSE 0 END) as has_def,
               SUM(CASE WHEN definition_zh != '' AND definition_zh IS NOT NULL THEN 1 ELSE 0 END) as has_def_zh
        FROM glossary""").fetchone()
    print(f"  Total: {g['total']}  |  term_en: {g['has_en']}/{g['total']}  |  def_en: {g['has_def']}/{g['total']}  |  def_zh: {g['has_def_zh']}/{g['total']}")

    print("  [MISSING definition_en]")
    rows = conn.execute("SELECT source_id, term_zh, term_en FROM glossary WHERE definition_en IS NULL OR definition_en = '' ORDER BY id").fetchall()
    for r in rows:
        print(f"    {r['source_id']}: {r['term_zh']} / {r['term_en']}")

    # === LINEAGES ===
    print("\n=== LINEAGES ===")
    rows = conn.execute("SELECT source_id, name FROM lineages ORDER BY id").fetchall()
    for r in rows:
        print(f"  {r['source_id']}: {r['name']}")

    # === SUMMARY ===
    print("\n=== BILINGUAL GAP SUMMARY ===")
    print(f"  texts title_en gap: {n - has_en}")
    print(f"  texts title_sa gap: {n - has_sa}")
    print(f"  texts title_bo gap: {n - has_bo}")
    print(f"  chapters title_en gap: {ch['total'] - ch['has_en']}")
    print(f"  chapters title_sa gap: {ch['total'] - ch['has_sa']}")
    print(f"  chapters title_bo gap: {ch['total'] - ch['has_bo']}")
    print(f"  persons name_en gap: {p['total'] - p['has_en']}")
    print(f"  persons name_sa gap: {p['total'] - p['has_sa']}")
    print(f"  locations name_en gap: {len(missing_en)}")
    print(f"  glossary definition_en gap: {g['total'] - g['has_def']}")

    conn.close()

if __name__ == "__main__":
    main()
