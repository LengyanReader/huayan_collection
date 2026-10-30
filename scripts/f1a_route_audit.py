#!/usr/bin/env python3
"""
F.1a — 行迹路径逐站引文覆盖审计（observe-only·非门禁）

对象: data/events/person_trajectories.yaml（S2「点人溯事」行迹层数据源）
目的: 量化「站级引文回源」缺口基线，供「山河法脉」F.3 交互批据此补源。
铁律: 只读·不改数据·不编造。缺口如实报告，不臆测填充。

用法: python scripts/f1a_route_audit.py
退出码: 恒为 0（审计观察，非通过/失败门禁）。
"""

import sys
from collections import Counter
from pathlib import Path

import yaml

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TRAJ_PATH = ROOT / "data" / "events" / "person_trajectories.yaml"

# 站级引文回源字段候选（当前数据结构中不存在→命中数即覆盖数）
STOP_CITE_KEYS = {"source", "citation", "cite", "quote", "ref", "reference", "note"}


def main() -> int:
    if not TRAJ_PATH.exists():
        print(f"[F1a] MISSING: {TRAJ_PATH}")
        return 0

    data = yaml.safe_load(TRAJ_PATH.read_text(encoding="utf-8")) or {}
    persons = {k: v for k, v in data.items() if isinstance(v, dict)}

    n_persons = len(persons)
    with_route = {k: v for k, v in persons.items() if v.get("route")}
    n_route = len(with_route)
    stops = [s for v in with_route.values() for s in (v.get("route") or []) if isinstance(s, dict)]
    n_stops = len(stops)

    # 人物级 source / verified 覆盖
    p_src = sum(1 for v in with_route.values() if str(v.get("source", "")).strip())
    p_ver = sum(1 for v in with_route.values() if v.get("verified") in (True, "true", "yes", 1))

    # 站级字段命中统计
    stop_keys = Counter(k for s in stops for k in s.keys())
    stop_cited = sum(1 for s in stops if any(k in s for k in STOP_CITE_KEYS))

    print("=" * 60)
    print("F.1a 行迹路径逐站引文覆盖审计")
    print(f"源文件: {TRAJ_PATH.relative_to(ROOT)}")
    print("=" * 60)
    print(f"人物总数               : {n_persons}")
    print(f"有 route 的人物        : {n_route}")
    print(f"路径站点总数           : {n_stops}")
    print(f"  站点字段分布         : {dict(stop_keys)}")
    print("-" * 60)
    print(f"人物级 有 source       : {p_src}/{n_route}"
          f"  ({100*p_src/n_route:.1f}%)" if n_route else "无 route 人物")
    print(f"人物级 有 verified     : {p_ver}/{n_route}"
          f"  ({100*p_ver/n_route:.1f}%)" if n_route else "")
    print(f"站级 逐站引文(任一字段): {stop_cited}/{n_stops}"
          f"  ({100*stop_cited/n_stops:.1f}%)" if n_stops else "")
    print("-" * 60)
    if stop_cited == 0 and n_stops:
        print("[缺口] 站级引文回源 = 0/{}：S2「点人溯事」每站引文卡片须自本批起逐站补源".format(n_stops))
        print("       (人物级 source/verified 可作 F.3 补源的起点，非终点)")
    unverified = [k for k, v in with_route.items() if v.get("verified") not in (True, "true", "yes", 1)]
    if unverified:
        print(f"[待核] 无 verified 的行迹人物 {len(unverified)} 位(节选前10): {unverified[:10]}")
    print("=" * 60)
    print("审计完成（observe-only·未改动任何数据）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
