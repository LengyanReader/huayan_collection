#!/usr/bin/env python3
"""
华严项目 — 信息来源可靠性审计（SQLite 权威源）

以 data/catalog/huayan.db 为唯一数据源，对所有人/传承边/文档做来源分级审计：
  T1 一级史料（高僧传/大正藏CBETA/付法师资记等）→ 🟢
  T2 二级学术（专著/论文/专题数据库）            → 🟡
  T3 三级记述（官网/百科/口述/网络，不可直接回溯） → 🟠
  T0 无来源 / 模糊来源（近现代佛教史料等）        → 🔴 存疑

用法:
  python scripts/verify_sources.py                # 打印报告
  python scripts/verify_sources.py --json         # JSON 输出
  python scripts/verify_sources.py --out docs/source-audit-report.md  # 写审计报告
  python scripts/verify_sources.py --fixme        # 打印需修复条目
"""

import json
import re
import sys
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "catalog" / "huayan.db"
DOCS_DIR = PROJECT_ROOT / "docs"
YAML_TARGETS = [
    ("translation", "huayan_masters.yaml"),
    ("translation", "topic_studies.yaml"),
    ("translation", "standalone_articles.yaml"),
]

# 不可直接回溯的模糊来源（含这些词则 T3，根本不交代出处则 T0）
VAGUE_PATTERNS = [
    "网", "百度百科", "官网", "维基",
    "近现代佛教史料", "当代佛教资料", "日本佛教史", "学术研究",
    "华严莲社", "大华严寺法脉资料", "资料（2024", "资料", "口述", "传记类网络",
    "待查", "待确认", "存疑", "凤凰网",
]

# 一级史料（高僧传系/大正藏/祖师传记/教史/经律论原典）
PRIMARY_PATTERNS = [
    "《宋高僧传》", "《续高僧传》", "《高僧传》", "《大明高僧传》",
    "《补续高僧传》", "《新续高僧传》", "《景新续高僧传》",
    "《佛祖统纪》", "《佛祖历代通载》", "《佛祖正传古今捷录》",
    "《付法师资记》", "《贤首宗付法师资记》",
    "《法藏和尚传》", "《华严经传记》", "《华严经感应略记》",
    "大正藏", "CBETA", "T87", "卍续藏", "《高丽史》",
    "《佛国记》", "《法显传》", "《大唐西域记》", "《往五天竺国传》",
    "《御请来目录》", "《长阿含经》", "《大慈恩寺三藏法师传》",
    "《皇唐嵩岳少林寺碑》", "《全唐文》", "《旧唐书》", "《新唐书》",
]

T2_PATTERNS = ["http", "论文", "专著", "《华严学研究》", "固安法源寺", "《中国佛教寺院大观》"]


def classify_source(s: str) -> str:
    """T0 无来源 / T1 一级史料 / T2 学术 / T3 模糊三级记述"""
    s = (s or "").strip()
    if not s:
        return "T0"
    for p in PRIMARY_PATTERNS:
        if p in s:
            return "T1"
    for p in VAGUE_PATTERNS:
        if p in s:
            return "T3"
    if "http" in s or "论文" in s or "研究" in s:
        return "T2"
    if "《" in s:  # 有具体文献名但非一级史料 → 至少二级
        return "T2"
    return "T3"


def audit_persons(cur):
    rows = cur.execute(
        "SELECT id, name_zh, source, verified FROM persons ORDER BY id").fetchall()
    tiers = Counter()
    missing, vague, unverified = [], [], []
    for pid, name, source, verified in rows:
        tier = classify_source(source)
        tiers[tier] += 1
        if tier == "T0":
            missing.append((pid, name, source))
        elif tier == "T3":
            vague.append((pid, name, source))
        if not verified:
            unverified.append((pid, name))
    return {
        "file": "persons (SQLite)",
        "total": len(rows),
        "tiers": dict(tiers),
        "missing": missing, "vague": vague, "unverified": unverified,
    }


def audit_edges(cur):
    rows = cur.execute(
        "SELECT id, from_person_id, to_person_id, relation, COALESCE(source,'') FROM lineage_edges ORDER BY id").fetchall()
    no_source = [(r[1], r[2], r[3]) for r in rows if not r[4].strip()]
    return {
        "file": "lineage_edges (SQLite)",
        "total": len(rows),
        "no_source": no_source,
    }


def audit_locations(cur):
    rows = cur.execute(
        "SELECT id, source_id, name_zh, COALESCE(source,''), type FROM locations ORDER BY id").fetchall()
    tiers = Counter()
    no_source = [(r[1], r[2], r[4]) for r in rows if classify_source(r[3]) == "T0"]
    for r in rows:
        tiers[classify_source(r[3])] += 1
    return {"file": "locations (SQLite)", "total": len(rows), "tiers": dict(tiers),
            "no_source": no_source}


def audit_docs():
    """docs/*.md 的存疑/待考标注覆盖率"""
    results = []
    for p in sorted(DOCS_DIR.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        markers = len(re.findall(r"存疑|待考|待核|疑点|存异说|一说般", text))
        citations = text.count("CBETA") + text.count("T[0-9]") + text.count("T[0-9]{1,2}n")
        results.append({"file": p.name, "markers": markers, "citations": citations})
    return results


def score(tiers):
    pts = sum({"T1": 3, "T2": 2, "T3": 1}.get(t, 0) * c for t, c in tiers.items())
    mx = 3 * sum(tiers.values())
    return int(pts / mx * 100) if mx else 0


def main():
    json_out = "--json" in sys.argv
    out_md = None
    if "--out" in sys.argv:
        out_md = Path(sys.argv[sys.argv.index("--out") + 1])
    show_fixme = "--fixme" in sys.argv

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    persons = audit_persons(cur)
    edges = audit_edges(cur)
    locations = audit_locations(cur)
    docs = audit_docs()
    con.close()

    p_missing = len(persons["missing"])
    p_vague = len(persons["vague"])
    p_unver = len(persons["unverified"])
    e_no_src = len(edges["no_source"])
    pct_missing = 100.0 * p_missing / persons["total"]
    pct_edges = 100.0 * e_no_src / edges["total"]
    score_val = score(persons["tiers"])
    doc_nomark = [d["file"] for d in docs if d["markers"] == 0]

    report = {
        "generated": datetime.now().isoformat(timespec="minutes"),
        "persons": persons,
        "edges": edges,
        "docs": {"total": len(docs), "without_doubt_marker": doc_nomark, "list": docs},
        "score_persons": score_val,
        "pct_persons_without_source": round(pct_missing, 1),
        "pct_edges_without_source": round(pct_edges, 1),
    }
    if json_out:
        report["locations"] = locations
        print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
        return

    print("=" * 60)
    print("  华严项目 — 信息来源可靠性审计（SQLite 权威源）")
    print("  生成时间: %s" % datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 60)
    print("\n── persons ──")
    print("  总人数: %d" % persons["total"])
    for t in ("T1", "T2", "T3", "T0"):
        print("  %s (%s): %3d" % (t, {"T1": "一级史料", "T2": "二级学术", "T3": "三级记述", "T0": "无/模糊"}[t], persons["tiers"].get(t, 0)))
    print("  ├ 无来源 T0       : %d (%.1f%%)" % (p_missing, pct_missing))
    print("  ├ 模糊来源 T3     : %d" % p_vague)
    print("  └ 未核实 verified : %d" % p_unver)
    print("\n── lineage_edges ──")
    print("  总边数: %d | 缺 source: %d (%.1f%%)" % (edges["total"], e_no_src, pct_edges))
    print("\n── locations ──")
    print("  总数: %d | 缺来源: %d" % (locations["total"], len(locations["no_source"])))
    for t in ("T1", "T2", "T3", "T0"):
        print("  %s: %3d" % (t, locations["tiers"].get(t, 0)))
    print("\n── docs 存疑标注覆盖率 ──")
    for d in docs:
        flag = "  ⚠ 无存疑标注" if d["markers"] == 0 else ""
        print("  %-34s 存疑x%-3d citex%-3d%s" % (d["file"], d["markers"], d["citations"], flag))
    print("\n  人物来源评分: %d/100  (T1=3分/T0=0分)" % score_val)

    if show_fixme:
        print("\n── 需修复条目 ──")
        print("  persons 无来源 (%d):" % p_missing)
        for pid, name, s in persons["missing"][:30]:
            print("    %s  %s" % (name, pid))
        print("  persons 模糊来源 (%d):" % p_vague)
        for pid, name, s in persons["vague"][:30]:
            print("    %s  [%s]" % (name, s))
        print("  edges 无来源 (前20/%d):" % e_no_src)
        for f, t, rel in edges["no_source"][:20]:
            print("    %s → %s  (%s)" % (f, t, rel))

    print("\n" + "=" * 60)

    if out_md:
        lines = [
            "# 信息来源可靠性审计报告",
            "",
            "> 生成时间：%s · 数据源：SQLite `data/catalog/huayan.db` · 由 `scripts/verify_sources.py` 自动产出，" % report["generated"],
            "> 结论仅供人工核校参考；T0/T3 项即需补充第一手来源或标注存疑。",
            "",
            "## 总览",
            "",
            "| 对象 | 总数 | 缺来源 | 占比 | 备注 |",
            "|------|------|--------|------|------|",
            "| persons | %d | %d | %.1f%% | 评分 %d/100 |" % (persons["total"], p_missing, pct_missing, score_val),
            "| lineage_edges | %d | %d | %.1f%% | — |" % (edges["total"], e_no_src, pct_edges),
            "| docs   | %d | 无存疑标注 %d 篇 | — | — |" % (len(docs), len(doc_nomark)),
            "",
            "## persons 需补来源（T0）",
            "",
        ]
        for pid, name, s in persons["missing"]:
            lines.append("- [ ] `%s` %s　（无来源）" % (pid, name))
        lines += ["", "## persons 模糊来源（T3，需细化到具体文献）", ""]
        for pid, name, s in persons["vague"]:
            lines.append("- [ ] `%s` %s　`%s`" % (pid, name, s))
        lines += ["", "## lineage_edges 缺来源", ""]
        for f, t, rel in edges["no_source"]:
            lines.append("- [ ] %s → %s　(%s)" % (f, t, rel))
        lines += ["", "## locations 缺来源", ""]
        for lid, name, tp in locations["no_source"]:
            lines.append("- [ ] `%s` %s（%s）" % (lid, name, tp))
        lines += ["", "## docs 无存疑标注", ""]
        for f in doc_nomark:
            lines.append("- [ ] %s　（全篇无「存疑/待考」标注，需复核是否存在不确定内容）" % f)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("  已写报告 → %s" % out_md)


if __name__ == "__main__":
    main()