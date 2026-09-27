#!/usr/bin/env python3
"""华严项目 — huayan.db 快照备份/恢复/校验

背景(R1 风险): huayan.db 不入 git(正确) · 但 backfill_*.py 系列直接 UPDATE DB ·
不回写 YAML/JSON 源 · 因此 `make db-reset` 或 DB 损坏将**静默丢失全部 backfill
人工订正**。本脚本把 DB 导出为可入 git 的 SQL 文本快照 · 提供回环恢复能力。

设计要点:
  - 快照只含**普通表的 schema+数据+索引+触发器**(真实内容资产)。
  - FTS5 虚拟表是**派生数据**·不入快照·回放时重建 DDL + `rebuild` 即可
    (iterdump 对 external-content 虚拟表的输出不可回放·故不用它)。
  - 字符串/NULL 转义交给 SQLite 的 quote() 函数·生成器零手写转义。

用法:
    python scripts/db_backup.py --snapshot          # DB → data/catalog/backups/huayan_latest.sql
    python scripts/db_backup.py --verify            # 快照回放进临时库 · 与 live DB 逐表比对 + FTS 冒烟
    python scripts/db_backup.py --restore [PATH]    # 快照回放到 PATH(默认 backups/huayan_restored.db·不碰 live)

约定: 每次直接 UPDATE DB 的脚本(backfill_*/修复脚本)跑完后 · 应执行 --snapshot
并把快照与代码一起 commit · 使 DB 状态永久可复现。

事故注(2026-09-27): 本脚本第一版 restore() 在护栏比对前就 target.unlink() ·
相对路径躲过了字符串比较 · live DB 被误删且回放在 FTS 表上失败 —— 实际丢库一次。
现行版本三重防御：① restore 目标先 resolve() 再与 live 比对 · 拒绝覆盖 live；
② 回放失败不伤 live(目标永远是副本)；③ 配套 drill_db_restore.py 定期验证快照真能复活。
"""
import hashlib
import io
import sqlite3
import sys
import tempfile
from pathlib import Path

# 仅在作为脚本直接运行时包装 stdout(import 场景不重复包装·避免关闭底层缓冲)
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "catalog" / "huayan.db"
BACKUP_DIR = ROOT / "data" / "catalog" / "backups"
SNAPSHOT_PATH = BACKUP_DIR / "huayan_latest.sql"

FTS_TABLES = ("texts_fts", "glossary_fts")


def _is_virtual(row_sql):
    return (row_sql or "").lstrip().upper().startswith("CREATE VIRTUAL TABLE")


def _normal_tables(conn):
    """普通表(非虚拟表、非 shadow、非 sqlite_ 内部)。"""
    out = []
    for name, sql in conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"
    ):
        if name.startswith("sqlite_") or name in FTS_TABLES \
                or any(name.startswith(f + "_") for f in FTS_TABLES) \
                or _is_virtual(sql):
            continue
        out.append((name, sql))
    return out


def snapshot():
    """DB → SQL 文本快照(普通表 schema+数据+索引/触发器 · FTS 派生数据除外)。"""
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} 不存在")
        return 1
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    lines = ["-- huayan.db snapshot (FTS5 indexes are derived; rebuilt on replay)",
             "PRAGMA foreign_keys=OFF;",
             "BEGIN TRANSACTION;"]
    try:
        # 1) 普通表 schema + 数据(quote() 负责全部转义)
        for name, sql in _normal_tables(conn):
            lines.append(f"{sql};")
            cols = [r[1] for r in conn.execute(f'PRAGMA table_info("{name}")')]
            if not cols:
                continue
            parts = ["COALESCE(quote(\"%s\"),'NULL')" % c for c in cols]
            sel = " || ',' || ".join(parts)
            for (vals,) in conn.execute('SELECT %s FROM "%s"' % (sel, name)):
                lines.append('INSERT INTO "%s" VALUES(%s);' % (name, vals))
        # 2) FTS 虚拟表 DDL(从 sqlite_master 原文取 · 回放后 rebuild 填索引)
        for name, sql in conn.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' AND sql LIKE 'CREATE VIRTUAL TABLE%'"
        ):
            lines.append(f"{sql};")
        for f in FTS_TABLES:
            lines.append(f"INSERT INTO {f}({f}) VALUES('rebuild');")
        # 3) 索引与触发器(依赖两侧表都已建)
        for typ, name, sql in conn.execute(
            "SELECT type, name, sql FROM sqlite_master "
            "WHERE type IN ('index','trigger') AND sql IS NOT NULL "
            "AND name NOT LIKE 'sqlite_autoindex%' ORDER BY type DESC, name"
        ):
            lines.append(f"{sql};")
        lines.append("COMMIT;")
    finally:
        conn.close()
    SNAPSHOT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    size = SNAPSHOT_PATH.stat().st_size
    print(f"Snapshot written: {SNAPSHOT_PATH.relative_to(ROOT)} ({size:,} bytes, "
          f"{len(lines)} statements)")
    return 0


def _replay_to_temp():
    """快照回放进临时 DB · 返回 (conn, tmp_path)。"""
    sql = SNAPSHOT_PATH.read_text(encoding="utf-8")
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    conn = sqlite3.connect(tmp.name)
    conn.executescript(sql)
    conn.commit()
    return conn, Path(tmp.name)


def _table_digest(conn, table):
    h = hashlib.sha256()
    try:
        cur = conn.execute(f'SELECT * FROM "{table}" ORDER BY rowid')
    except sqlite3.OperationalError:
        return "ERR"
    for row in cur:
        h.update(repr(row).encode("utf-8"))
    return h.hexdigest()[:16]


def verify():
    """回环校验：快照回放库 vs live 库 · 逐普通表指纹 + FTS 冒烟命中。"""
    if not SNAPSHOT_PATH.exists():
        print(f"ERROR: 无快照 {SNAPSHOT_PATH} · 先 --snapshot")
        return 1
    live = sqlite3.connect(str(DB_PATH))
    snap, tmp = _replay_to_temp()
    rc = 0
    try:
        tables = [n for n, _ in _normal_tables(live)]
        ok = fail = 0
        print(f"{'TABLE':<22} {'LIVE':>6} {'SNAP':>6}  DIGEST       MATCH")
        for t in tables:
            lc = live.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
            sc = snap.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
            ld, sd = _table_digest(live, t), _table_digest(snap, t)
            match = ld == sd
            ok += match
            fail += (not match)
            print(f"  {t:<20} {lc:>6} {sc:>6}  {ld}  {'✅' if match else '❌'}")
        # FTS 冒烟：回放库重建后的索引必须可用
        hit = snap.execute(
            "SELECT COUNT(*) FROM texts_fts WHERE texts_fts MATCH 'avatamsaka'"
        ).fetchone()[0]
        fts_ok = hit > 0
        print(f"\nFTS smoke on replay DB: MATCH 'avatamsaka' = {hit} hit(s) "
              f"{'✅' if fts_ok else '❌'}")
        print(f"verify: {ok}/{len(tables)} tables identical", end="")
        if fail or not fts_ok:
            print(f" — ❌ {fail} table mismatch(es), fts_ok={fts_ok}")
            rc = 1
        else:
            print(" + FTS ✅ — 快照可完整重现 live DB")
        return rc
    finally:
        live.close()
        snap.close()
        tmp.unlink(missing_ok=True)


def restore(target=None):
    """快照回放为新 DB 文件。绝不覆盖 live(需人工搬移)。"""
    if not SNAPSHOT_PATH.exists():
        print(f"ERROR: 无快照 {SNAPSHOT_PATH}")
        return 1
    if target is None:
        target = BACKUP_DIR / "huayan_restored.db"
    target = Path(target)
    if target.resolve() == DB_PATH.resolve():
        print("ERROR: 拒绝直接覆盖 live DB · 请先自行备份再指定其他路径")
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()
    conn = sqlite3.connect(str(target))
    conn.executescript(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    conn.commit()
    n = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    conn.close()
    print(f"Restored → {target} ({n} tables)")
    print("如需接管 live: 先手动备份现 db · 再复制替换 data/catalog/huayan.db")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    cmd = args[0]
    if cmd == "--snapshot":
        sys.exit(snapshot())
    elif cmd == "--verify":
        sys.exit(verify())
    elif cmd == "--restore":
        sys.exit(restore(args[1] if len(args) > 1 else None))
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
