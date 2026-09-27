"""R6 tests for `catalog init` CLI: temp-path, idempotent safe mode, no clobber."""
import subprocess, sys, tempfile, os
from pathlib import Path

PY = sys.executable
ROOT = Path(__file__).resolve().parent.parent
ok = True

def run(args, expect_rc=0, label=""):
    global ok
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([PY, "-c",
        "from src.cli.main import cli; cli(standalone_mode=True)", *args],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=env)
    passed = p.returncode == expect_rc
    ok &= passed
    print(f"{'PASS' if passed else 'FAIL'} {label} (rc={p.returncode})")
    if not passed:
        print(p.stdout[-300:], p.stderr[-500:])
    return p

tmp = Path(tempfile.mkdtemp())
tdb = tmp / "t.db"

p = run(["catalog", "init", "--db", str(tdb)], label="init --db 临时路径")
assert tdb.exists() and tdb.stat().st_size > 0, "临时库未建"
n_tables = "Tables (21)" in p.stdout
print(("PASS " if n_tables else "FAIL ") + "schema 21 表建齐")
ok &= n_tables

p = run(["catalog", "init", "--db", str(tdb), "--if-missing"], label="--if-missing 已存在跳过(不删)")
print(("PASS " if "已存在" in p.stdout else "FAIL ") + "安全模式输出跳过")
ok &= "已存在" in p.stdout

# 默认路径护栏验证：--if-missing 对 live 无破坏（live 存在时应跳过）
live = ROOT / "data" / "catalog" / "huayan.db"
size_before = live.stat().st_size
p = run(["catalog", "init", "--if-missing"], label="live 存在时 --if-missing 无操作")
print(("PASS " if live.stat().st_size == size_before else "FAIL ") + "live DB 未被碰")
ok &= live.stat().st_size == size_before

print("\nR6 CLI TEST:", "ALL PASS" if ok else "HAS FAILURES")
sys.exit(0 if ok else 1)
