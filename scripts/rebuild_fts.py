"""One-shot rebuild of FTS5 indexes for texts_fts / glossary_fts.

SQLite FTS5 external-content tables (content='xxx') store only the inverted
index, not the row data. If the source table is populated BEFORE the FTS
virtual table is created (or outside the trigger path), the index ends up
empty and MATCH returns 0 hits — even though COUNT(*) on the FTS table looks
correct. The fix is one line:

    INSERT INTO <fts_table>(<fts_table>) VALUES('rebuild');

This script is idempotent and safe to re-run.

Honest scope note (2026-09-26): this project's `MATCH '华严' → 0 hits` case
was originally attributed to an empty index, but a Latin probe (`avatamsaka`)
showed the index was healthy all along — the real culprit is the default
unicode61 tokenizer treating continuous CJK as ONE token, so a 2-char CJK
query can't substring-match a longer title token. This script was a NO-OP
for that case. Retained as (a) defensive tool for future bypass-trigger
import paths, (b) sanity smoke test. The functional CJK fix lives in
`db_reader.search_texts/glossary` LIKE fallback.
"""
import sqlite3, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DB = "data/catalog/huayan.db"
c = sqlite3.connect(DB)

print("before rebuild:")
for name, probe in (("texts_fts", "avatamsaka"), ("glossary_fts", "prajna")):
    n_match = c.execute(
        f"SELECT COUNT(*) FROM {name} WHERE {name} MATCH ?", (probe,)
    ).fetchone()[0]
    n_rows = c.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f"  {name}: rows={n_rows}  MATCH {probe!r}={n_match} hit(s)")

print("running rebuild ...")
c.execute("INSERT INTO texts_fts(texts_fts) VALUES('rebuild')")
c.execute("INSERT INTO glossary_fts(glossary_fts) VALUES('rebuild')")
c.commit()

print("after rebuild:")
for name, probe in (("texts_fts", "avatamsaka"), ("glossary_fts", "prajna")):
    n_match = c.execute(
        f"SELECT COUNT(*) FROM {name} WHERE {name} MATCH ?", (probe,)
    ).fetchone()[0]
    n_rows = c.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f"  {name}: rows={n_rows}  MATCH {probe!r}={n_match} hit(s)")

print("\nnote: CJK queries may still return 0 via MATCH due to unicode61 default")
print("       treating continuous CJK as ONE token. db_reader.search_* 已内置")
print("       LIKE 兑底·面向中文的搜索行为仍可用。")
