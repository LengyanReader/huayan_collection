"""R6 · `catalog init` CLI 测试：临时路径 / 安全模式 / live 不误删.

可 pytest 收集，也可 `python scripts/test_cli_catalog.py` 直跑。
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

PY = sys.executable
ROOT = Path(__file__).resolve().parent.parent


def run_cli(args, expect_rc=0):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run(
        [PY, "-c", "from src.cli.main import cli; cli(standalone_mode=True)", *args],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=env)
    assert p.returncode == expect_rc, f"rc={p.returncode}\n{p.stdout}\n{p.stderr}"
    return p


def test_catalog_init_temp_path():
    tdb = Path(tempfile.mkdtemp()) / "t.db"
    p = run_cli(["catalog", "init", "--db", str(tdb)])
    assert tdb.exists() and tdb.stat().st_size > 0
    assert "Tables (21)" in p.stdout  # schema.sql 全 21 表建齐


def test_if_missing_never_deletes():
    tdb = Path(tempfile.mkdtemp()) / "t.db"
    run_cli(["catalog", "init", "--db", str(tdb)])
    mtime = tdb.stat().st_mtime_ns
    p = run_cli(["catalog", "init", "--db", str(tdb), "--if-missing"])
    assert "已存在" in p.stdout
    assert tdb.stat().st_mtime_ns == mtime, "--if-missing 竟改写了已存在的库"


@pytest.mark.skipif(
    not (ROOT / "data" / "catalog" / "huayan.db").exists(),
    reason="live DB 不存在(CI 全链重建前) · 跳过")
def test_if_missing_noop_on_live():
    live = ROOT / "data" / "catalog" / "huayan.db"
    size_before = live.stat().st_size
    run_cli(["catalog", "init", "--if-missing"])
    assert live.stat().st_size == size_before, "live DB 被 --if-missing 动了"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
