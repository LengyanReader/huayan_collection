#!/usr/bin/env python3
"""华严项目 — 备份恢复破坏性演练 (drill_db_restore)

证明 snapshot 真能复活被毁的 live DB：指纹对照 → 清零 live → restore →
逐表 digest 必须全等 → 恢复产物接管 live。

⚠️ 本脚本会真的把 data/catalog/huayan.db 清零(随即从快照复活)。仅当
   `python scripts/db_backup.py --verify` 刚通过时才允许运行，故须带 --force。

用法:
    python scripts/drill_db_restore.py --force
"""
import importlib.util
import shutil
import sqlite3
import sys
import io
from pathlib import Path

if __name__ == "__main__" and (sys.stdout.encoding or "").lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "catalog" / "huayan.db"
RESTORED = ROOT / "data" / "catalog" / "backups" / "huayan_restored.db"

spec = importlib.util.spec_from_file_location("db_backup", ROOT / "scripts" / "db_backup.py")
db_backup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_backup)

TABLES = ["persons", "texts", "chapters", "locations", "lineages",
          "lineage_edges", "person_locations", "cross_refs", "glossary"]


def digests(path):
    c = sqlite3.connect(str(path))
    d = {t: db_backup._table_digest(c, t) for t in TABLES}
    n = c.execute(
        "SELECT COUNT(*) FROM texts_fts WHERE texts_fts MATCH 'avatamsaka'"
    ).fetchone()[0]
    c.close()
    return d, n


def main():
    if "--force" not in sys.argv:
        print("需显式 --force(本演练会清零 live DB · 请确认快照刚 --verify 通过)")
        return 1
    if not db_backup.SNAPSHOT_PATH.exists():
        print("无快照 · 先 python scripts/db_backup.py --snapshot")
        return 1

    before, fts_before = digests(DB)
    print(f"before: texts_digest={before['texts']} fts_hits={fts_before}")

    DB.unlink()
    DB.write_bytes(b"")
    print("live DB zeroed (drill)")

    rc = db_backup.restore()
    if rc != 0:
        print("FAIL: restore 失败 · live 仍为 0 字节 · 手动跑 --restore 排查")
        return 1
    after, fts_after = digests(RESTORED)

    ok = True
    for t in TABLES:
        mark = "✅" if before[t] == after[t] else "❌"
        ok &= before[t] == after[t]
        print(f"  {t:<18} {before[t]} {after[t]} {mark}")
    print(f"FTS avatamsaka: {fts_before} -> {fts_after}")

    # 恢复产物接管 live
    shutil.copy(RESTORED, DB)
    final, fts_final = digests(DB)
    passed = final == before and fts_final == fts_before
    print(f"\nDRILL RESULT: {'PASS — snapshot 可完整复活被毁 DB' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
