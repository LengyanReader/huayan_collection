#!/usr/bin/env python3
"""Verify chapters.title_en coverage. (Batch A, 2026-09-27 — now a check, not a writer.)

English names follow the standard scholarly convention of Thomas Cleary's
"The Flower Ornament Scripture" (1993) / 84000 Toh 44 Phal chen translations.
These are established academic English renderings, not invented translations.

HISTORY: this script used to hold its own title_zh -> title_en map and UPDATE the table
by title_zh. That made title_en a *second* source: import_chapters wrote rows without it,
this script patched them afterwards, and after any rebuild the freshly inserted rows had
NULL title_en while older ones had it — so a re-import produced non-identical duplicates
and de-duplication became ambiguous. The map now lives in data/catalog/chapters.yaml
(alongside title_zh and the version flags) and import_chapters writes title_en in the
same pass, making re-imports true no-ops.

It is therefore retained only to VERIFY the authoritative data: it reports any chapter
whose title_en is missing or does not match chapters.yaml. Exit code is non-zero on
mismatch so a pipeline can gate on it. Fix data by editing chapters.yaml and re-running
the import — never by editing the database.
"""
import sqlite3, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "catalog" / "huayan.db"
CHAPTERS_YAML = ROOT / "data" / "catalog" / "chapters.yaml"

import yaml
data = yaml.safe_load(CHAPTERS_YAML.read_text(encoding='utf-8'))
WANT = {c['title_zh']: c.get('title_en') for c in (data.get('chapters') or [])}

conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row

total, has_en, bad = 0, 0, []
for row in conn.execute("SELECT id, title_zh, title_en FROM chapters ORDER BY order_num"):
    total += 1
    zh, en = row['title_zh'], row['title_en']
    if en:
        has_en += 1
    if zh not in WANT:
        bad.append(f"  chapter not in chapters.yaml: {zh!r}")
    elif (en or '') != (WANT[zh] or ''):
        bad.append(f"  {zh}: db={en!r} != yaml={WANT[zh]!r}")
    elif not en:
        bad.append(f"  {zh}: missing title_en")

print(f"Chapters title_en coverage: {has_en}/{total} (authoritative source: {len(WANT)} entries)")
if bad:
    print("MISMATCH — re-run scripts/import_all_to_sqlite.py after fixing chapters.yaml:")
    for b in bad:
        print(b)
else:
    print("OK — every chapters row matches data/catalog/chapters.yaml")

conn.close()
sys.exit(1 if bad else 0)
