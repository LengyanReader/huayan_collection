"""One-shot rebuild of FTS5 indexes for texts_fts / glossary_fts.

SQLite FTS5 external-content tables (content='xxx') store only the inverted
index, not the row data. If the source table is populated BEFORE the FTS
virtual table is created (or outside the trigger path), the index ends up
empty and MATCH returns 0 hits — even though COUNT(*) on the FTS table looks
correct. The fix is one line:

    INSERT INTO <fts_table>(<fts_table>) VALUES('rebuild');

This script is idempotent and safe to re-run.
"""
import sqlite3, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DB = "data/catalog/huayan.db"
c = sqlite3.connect(DB)

print("before rebuild:")
for name in ("texts_fts", "glossary_fts"):
    q = "'华严'" if name == "texts_fts" else "'识'"
    n_match = c.execute(f"SELECT COUNT(*) FROM {name} WHERE {name} MATCH {q}").fetchone()[0]
    n_rows = c.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f"  {name}: rows={n_rows}  MATCH-hits={n_match}")

print("running rebuild ...")
c.execute("INSERT INTO texts_fts(texts_fts) VALUES('rebuild')")
c.execute("INSERT INTO glossary_fts(glossary_fts) VALUES('rebuild')")
c.commit()

print("after rebuild:")
for name in ("texts_fts", "glossary_fts"):
    q = "'华严'" if name == "texts_fts" else "'识'"
    n_match = c.execute(f"SELECT COUNT(*) FROM {name} WHERE {name} MATCH {q}").fetchone()[0]
    n_rows = c.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f"  {name}: rows={n_rows}  MATCH-hits={n_match}")
