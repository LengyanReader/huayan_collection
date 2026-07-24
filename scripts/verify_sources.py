#!/usr/bin/env python3
"""
华严项目 — 信息来源可靠性验证脚本
用法:
  python scripts/verify_sources.py              # 检查所有文件
  python scripts/verify_sources.py --json       # JSON 格式输出
  python scripts/verify_sources.py --fixme      # 输出需要修复的具体条目
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

# --- 配置 ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# 模糊来源关键词（被认为是不可回溯的）
VAGUE_SOURCE_PATTERNS = [
    "近现代佛教史料",
    "当代佛教资料",
    "当代佛教资料（华严莲社）",
    "当代佛教资料（2024年）",
    "华严莲社资料",
    "华严莲社资料（2024年）",
    "网络资料",
    "大华严寺法脉资料",
    "大华严寺法脉资料（2024年）",
    "华严莲社美国分会资料",
    "日本佛教史",
    "学术研究",  # 太泛
    "待查",
    "待确认",
]

# 被认为是可靠的一级来源关键词
PRIMARY_PATTERNS = [
    "《宋高僧传》",
    "《续高僧传》",
    "《高僧传》",
    "《佛祖统纪》",
    "《佛祖历代通载》",
    "《大明高僧传》",
    "《补续高僧传》",
    "《新续高僧传》",
    "《龙树菩萨传》",
    "大正藏",
    "CBETA",
    "T0",  # 大正藏编号
    "T2",  # 大正藏编号
]


def classify_source(source_str: str) -> str:
    """将 source 字符串分类为 T1/T2/T3/T0"""
    if not source_str or source_str.strip() == "":
        return "T0"

    # 检查是否为模糊来源
    for pattern in VAGUE_SOURCE_PATTERNS:
        if pattern in source_str:
            return "T3"

    # 检查是否为一级来源
    for pattern in PRIMARY_PATTERNS:
        if pattern in source_str:
            return "T1"

    # 包含 URL 或学术关键词 → T2
    if "http" in source_str or "研究" in source_str or "论文" in source_str:
        return "T2"

    # 包含书名号 → 至少 T2
    if "《" in source_str:
        return "T1"

    return "T3"


def check_personas():
    """检查 personas.json"""
    path = DATA_DIR / "knowledge_graph" / "personas.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    persons = data["persons"]
    results = {
        "file": "personas.json",
        "total": len(persons),
        "tiers": Counter(),
        "missing_source": [],
        "vague_source": [],
        "missing_verified": [],
        "no_alt_source": [],
    }

    for p in persons:
        tier = classify_source(p.get("source", ""))
        results["tiers"][tier] += 1

        if tier == "T0":
            results["missing_source"].append(f"  {p['id']}: {p['name_zh']}")
        elif tier == "T3":
            results["vague_source"].append(f"  {p['id']}: {p['name_zh']} → \"{p.get('source','')}\"")

        if "verified" not in p:
            results["missing_verified"].append(f"  {p['id']}: {p['name_zh']}")

    return results


def check_lineages():
    """检查 lineages.json 的边是否有双向验证"""
    path = DATA_DIR / "knowledge_graph" / "lineages.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    edges = []
    for lin in data["lineages"]:
        for e in lin["edges"]:
            if e.get("from") != e.get("to"):  # 排除自引用
                edges.append(e)

    results = {
        "file": "lineages.json",
        "total_edges": len(edges),
        "with_note": sum(1 for e in edges if e.get("note")),
        "without_note": [f"  {e['from']} → {e['to']} ({e['relation']})" for e in edges if not e.get("note")],
    }
    return results


def check_locations():
    """检查 locations.json 的 source 质量"""
    path = DATA_DIR / "knowledge_graph" / "locations.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    locs = data["locations"]
    results = {
        "file": "locations.json",
        "total": len(locs),
        "tiers": Counter(),
        "without_source": [],
    }

    for loc in locs:
        tier = classify_source(loc.get("source", ""))
        results["tiers"][tier] += 1
        if tier == "T0":
            results["without_source"].append(f"  {loc['id']}: {loc['name_zh']}")

    return results


def score_tier(tier: str) -> int:
    """将 tier 转换为分数"""
    return {"T1": 3, "T2": 2, "T3": 1, "T0": 0}.get(tier, 0)


def compute_overall_score(all_results: list) -> int:
    """计算总体可验证性评分 (0-100)"""
    if not all_results:
        return 0

    total_points = 0
    max_points = 0

    for r in all_results:
        if "tiers" in r:
            for tier, count in r["tiers"].items():
                total_points += score_tier(tier) * count
                max_points += 3 * count  # 满分 = 全部 T1
        elif "total_edges" in r:
            max_edge = r["total_edges"]
            total_points += score_tier("T2") * r.get("with_note", 0)
            max_points += 3 * max_edge

    if max_points == 0:
        return 0
    return int(total_points / max_points * 100)


def main():
    json_output = "--json" in sys.argv
    show_fixme = "--fixme" in sys.argv

    all_results = []
    all_results.append(check_personas())
    all_results.append(check_lineages())
    all_results.append(check_locations())

    score = compute_overall_score(all_results)

    if json_output:
        print(json.dumps({"score": score, "results": all_results, "timestamp": datetime.now().isoformat()}, ensure_ascii=False, indent=2, default=str))
        return

    # --- 人类可读输出 ---
    print("=" * 60)
    print("  华严项目 — 信息来源可靠性验证报告")
    print(f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    for r in all_results:
        print(f"\n── {r['file']} ──")
        if "total" in r:
            print(f"  总记录: {r['total']}")
        if "tiers" in r:
            print(f"  T1 (一级史料):   {r['tiers'].get('T1', 0)}")
            print(f"  T2 (二级学术):   {r['tiers'].get('T2', 0)}")
            print(f"  T3 (三级记述):   {r['tiers'].get('T3', 0)}")
            print(f"  T0 (待确认):     {r['tiers'].get('T0', 0)}")
        if "total_edges" in r:
            print(f"  总边数: {r['total_edges']}")
            print(f"  有 note 注释: {r['with_note']}")
            print(f"  缺 note:     {len(r.get('without_note', []))}")

        if show_fixme:
            for key in ["missing_source", "vague_source", "missing_verified", "no_alt_source", "without_note", "without_source"]:
                items = r.get(key, [])
                if items:
                    label = key.replace("_", " ").title()
                    print(f"\n  ⚠ {label} ({len(items)}):")
                    for item in items[:5]:  # 最多显示5条
                        print(item)
                    if len(items) > 5:
                        print(f"  ... 还有 {len(items) - 5} 条")

    print(f"\n{'=' * 60}")
    print(f"  总体可验证性评分: {score}/100")
    if score >= 80:
        print("  评级: ✅ 良好 — 大部分记录可追溯到可靠来源")
    elif score >= 60:
        print("  评级: ⚠ 中等 — 需要改进模糊来源")
    elif score >= 40:
        print("  评级: 🟠 不足 — 大量记录缺乏可靠溯源")
    else:
        print("  评级: 🔴 严重 — 必须优先补全来源信息")
    print("=" * 60)


if __name__ == "__main__":
    main()
