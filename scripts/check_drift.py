#!/usr/bin/env python3
"""R3 · 双份派生 JSON 漂移检查 (docs/ vs web/demo/)

背景：graph.json/gap.json 在 docs/ 与 web/demo/ 各有一份。生产链
(import_all_to_sqlite / export_sqlite_to_json / test_pipeline / audit_classify)
全部读写 web/demo/ 那份；docs/ 那份无任何代码引用，属遗留副本，已观测到漂移
(docs: nodes=92/edges=96 vs demo: nodes=95/edges=98)。

本脚本只报警不删改：
    python scripts/check_drift.py          # 逐对比对 · 漂移则 exit 1
删除/同步 docs/ 副本属数据处置决定，留给维护者（见 harness/concerns.md §7）。
"""
import hashlib
import io
import json
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAIRS = [
    ("docs/graph.json", "web/demo/graph.json"),
    ("docs/gap.json", "web/demo/gap.json"),
]


def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def summarize(p: Path):
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return {k: (len(v) if isinstance(v, list) else "-") for k, v in d.items()}
    except Exception as e:
        return f"ERR {e}"


drift = 0
for a_rel, b_rel in PAIRS:
    a, b = ROOT / a_rel, ROOT / b_rel
    if not a.exists() or not b.exists():
        print(f"MISSING  {a_rel} exists={a.exists()}  {b_rel} exists={b.exists()}")
        drift += 1
        continue
    ha, hb = sha(a), sha(b)
    if ha == hb:
        print(f"SYNCED   {a_rel} == {b_rel}  ({ha[:12]})")
    else:
        drift += 1
        print(f"DRIFT    {a_rel} ({ha[:12]}) != {b_rel} ({hb[:12]})")
        print(f"         docs: {summarize(a)}")
        print(f"         demo: {summarize(b)}")
        print("         权威=web/demo(生产链所系) · docs 副本处置待维护者定")

print(f"\ncheck_drift: {len(PAIRS) - drift}/{len(PAIRS)} pairs synced")
sys.exit(1 if drift else 0)
