#!/usr/bin/env python3
"""
check_drift.py — R3 · 双份派生数据一致性检查器（v2 · 全站点面）

背景：同一份数据存在两处拷贝——
  - web/demo/            = Pages 线上站点（权威 · 根 index.html redirect 至此）
  - docs/ 下的站点面      = 历史遗留镜像（index/css/js/tabs/json · 研究 .md 不在此列·是活跃资产）
2026-09-27 核查：除 gap.json 外**全部漂移**（tabs 650KB vs 3.8MB · graph 55KB vs 133KB）。
本工具只报告、不删改（§I10）；处置（同步/退役）待维护者定。

用法：
  python scripts/check_drift.py             # 人读报告
  python scripts/check_drift.py --json      # 机读
退出码：0=全部同步；1=存在漂移或缺拷贝（verify-data 中为非阻塞告警）
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (docs 侧相对路径, demo 侧相对路径)——两两镜像对
MIRROR_PAIRS = [
    ("index.html", "index.html"),
    ("css/common.css", "css/common.css"),
    ("js/common.js", "js/common.js"),
    ("gap.json", "gap.json"),
    ("graph.json", "graph.json"),
] + [(f"tabs/{t}.html", f"tabs/{t}.html") for t in
     ("cosmology", "frontier", "gap", "jiaoxing", "lineage", "spirit")]


def sha256(b):
    return hashlib.sha256(b).hexdigest()[:16]


def json_shape(p):
    """JSON 结构摘要：键/元素数量漂移定位用。"""
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return f"<parse error: {e}>"
    if isinstance(d, dict):
        return "{" + ", ".join(f"{k}:{len(v) if isinstance(v, list) else '?'}"
                               for k, v in d.items()) + "}"
    if isinstance(d, list):
        return f"[{len(d)} items]"
    return type(d).__name__


def diff_pair(root, a_rel, b_rel):
    """比对一对镜像文件。返回 None(同步) 或 结果字典。"""
    a = root / "docs" / a_rel
    b = root / "web" / "demo" / b_rel
    label = f"docs/{a_rel}  ↔  web/demo/{b_rel}"
    if not a.exists() and not b.exists():
        return None
    if not a.exists() or not b.exists():
        side = "docs" if not a.exists() else "web/demo"
        return {"pair": label, "state": "MISSING", "detail": f"{side} 侧缺拷贝"}
    ha, hb = sha256(a.read_bytes()), sha256(b.read_bytes())
    if ha == hb:
        return None
    detail = f"hash 不一致 ({ha} vs {hb}) · 字节 {a.stat().st_size} vs {b.stat().st_size}"
    if a_rel.endswith(".json"):
        detail += f" | A={json_shape(a)} | B={json_shape(b)}"
    return {"pair": label, "state": "DRIFT", "detail": detail}


def collect(root=ROOT):
    """全对巡检 → (同步数, 漂移结果列表)。"""
    results = [r for r in (diff_pair(root, a, b) for a, b in MIRROR_PAIRS) if r]
    synced = len(MIRROR_PAIRS) - len(results)
    return synced, results


def main(argv=None):
    ap = argparse.ArgumentParser(description="双份派生数据一致性检查（报告模式）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--root", type=Path, default=ROOT, help="仓库根（测试可注入临时结构）")
    a = ap.parse_args(argv)

    synced, results = collect(a.root)
    if a.json:
        print(json.dumps({"synced": synced, "total": len(MIRROR_PAIRS),
                          "drift": results}, ensure_ascii=False))
    else:
        print("=== 双份派生数据巡检（docs 镜像 ↔ web/demo 权威 · 只报警不阻塞）===")
        for r in results:
            print(f"  {r['state']:8} {r['pair']}")
            print(f"           {r['detail']}")
        if not results:
            print(f"  SYNCED   全部 {synced} 对一致")
        else:
            print(f"\n汇总：{synced}/{len(MIRROR_PAIRS)} 同步 · {len(results)} 待处置"
                  "（权威=web/demo · 处置方式待维护者定·见 harness/concerns.md §7）")
    return 1 if results else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
