# -*- coding: utf-8 -*-
"""test_infra.py — B1 · 基础设施自证测试（防"工具自己烂掉"）

覆盖三块曾真实出过事故/盲区的层面：
  1. check_drift 漂移检出（合成夹具 · 决定/缺失/同步三态）
  2. db_backup 快照回环 + live-DB 护栏（v1 曾因 restore 先 unlink 毁库 · 此测试即墓碑）
  3. db_reader 搜索两层策略（CJK LIKE 兑底 + 拉丁 FTS 主路）

live-DB 相关用例在缺 data/catalog/huayan.db 时自动 skip（如全新 clone 未构建）。
"""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


cd = _load("check_drift", "scripts/check_drift.py")
dbb = _load("db_backup", "scripts/db_backup.py")

DB = ROOT / "data" / "catalog" / "huayan.db"
needs_db = pytest.mark.skipif(not DB.exists(), reason="live DB 未构建")


# ---------- 1. check_drift ----------

def _mkpair(tmp, rel, content_a, content_b):
    a = tmp / "docs" / rel
    b = tmp / "web" / "demo" / rel
    for p in (a, b):
        p.parent.mkdir(parents=True, exist_ok=True)
    if content_a is not None:
        a.write_text(content_a, encoding="utf-8")
    if content_b is not None:
        b.write_text(content_b, encoding="utf-8")


def test_drift_synthetic_three_states(tmp_path):
    _mkpair(tmp_path, "gap.json", '{"x":1}', '{"x":1}')      # 同步
    _mkpair(tmp_path, "index.html", "<html>a</html>", "<html>b</html>")  # 漂移
    _mkpair(tmp_path, "js/common.js", "1", None)              # 单侧缺失
    synced, results = cd.collect(tmp_path)
    states = {r["state"] for r in results}
    assert "DRIFT" in states and "MISSING" in states
    assert "gap.json" not in " ".join(r["pair"] for r in results)  # 同步对不进结果
    assert synced + len(results) == len(cd.MIRROR_PAIRS)


def test_drift_main_exit_codes(tmp_path):
    _mkpair(tmp_path, "gap.json", "{}", "{}")
    assert cd.main(["--root", str(tmp_path)]) == 0            # 全同步 → 0
    _mkpair(tmp_path, "gap.json", "{}", '{"a":2}')
    assert cd.main(["--root", str(tmp_path), "--json"]) == 1  # 漂移 → 1


def test_drift_real_repo_is_consistent_count():
    """真仓库巡检必须无异常且计数自洽（现状含已知漂移·处置定前不断言 0）。"""
    synced, results = cd.collect(ROOT)
    assert synced + len(results) == len(cd.MIRROR_PAIRS)


# ---------- 2. db_backup ----------

@needs_db
def test_snapshot_verify_roundtrip():
    assert dbb.snapshot() == 0
    assert dbb.verify() == 0, "快照回环+FTS 冒烟必须逐表 digest 一致"


@needs_db
def test_restore_guard_refuses_live_db(tmp_path):
    """护栏：restore 指到 live DB 必须拒绝且不动 live（v1 事故的墓碑测试）。"""
    before = DB.read_bytes()
    rc = dbb.restore(DB)
    assert rc == 1, "对 live DB 的 restore 必须被护栏拒绝"
    assert DB.read_bytes() == before, "live DB 字节必须分毫未动"


@needs_db
def test_restore_to_copy_rebuilds_identical(tmp_path):
    """restore 到副本 → 与 live 逐表 digest 一致（备份真能用）。"""
    target = tmp_path / "restored.db"
    assert dbb.restore(target) == 0
    import sqlite3
    live = sqlite3.connect(DB)
    copy = sqlite3.connect(target)
    tables = [t for (t,) in live.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'texts_fts%' AND name NOT LIKE 'glossary_fts%' "
        "AND sql NOT LIKE 'CREATE VIRTUAL TABLE%'")]
    for t in tables:
        assert dbb._table_digest(live, t) == dbb._table_digest(copy, t), t
    live.close(); copy.close()


# ---------- 3. db_reader 搜索两层策略 ----------

@needs_db
def test_search_cjk_like_fallback():
    from db_reader import search_texts
    hits = search_texts("华严")
    assert len(hits) > 0, "CJK 词必须经 LIKE 兑底命中（unicode61 单 token 顽疾）"


@needs_db
def test_search_latin_fts_primary():
    from db_reader import search_texts
    hits = search_texts("avatamsaka")
    assert len(hits) > 0, "拉丁词应走 FTS5 MATCH 主路"


@needs_db
def test_search_glossary_cjk():
    from db_reader import search_glossary
    assert len(search_glossary("法界")) > 0
