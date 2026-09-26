#!/usr/bin/env python3
"""Audit 行文与文体 (§I) across authored research docs.

Enforces harness/rules.md §I:
  I2 加粗只留表格 / 加粗密度  —— 正文 `**…**` 每千字密度（阈值默认 9.5，承 L.㊽ 指标）
  I4 不用套话·反 AI 腔        —— 命中空转连接词/翻译腔短语计数

v1 为**报告模式**（exit 0，不作门禁），先建立基线。文言残留(I5)/CJK-in-EN 泄漏为
〔启发式·待细化〕，本版仅**粗扫 CJK-in-Latin 段落**给线索，不据此判定违规（宁缺不伪）。

用法:
  python scripts/audit_style.py                 # 审默认语料（docs 顶层 *.md + web/demo/articles/*.md）
  python scripts/audit_style.py <path> [...]    # 审指定文件/目录
  python scripts/audit_style.py --bold-max 9.5  # 调加粗密度阈值
"""
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# 空转连接词 / 翻译腔 / AI 腔（软命中，按次数给线索）
CLICHE = [
    "首先，", "其次，", "再次，", "最后，", "总而言之", "综上所述",
    "值得注意的是", "不难发现", "毋庸置疑", "在当今社会", "与此同时",
    "在某种程度上", "众所周知", "一言以蔽之",
]

CJK = re.compile(r"[\u4e00-\u9fff]")
BOLD = re.compile(r"\*\*([^*\n]+?)\*\*")
# CJK-in-Latin 粗扫：一行以拉丁字母为主(>=40 连续字母词场景)却夹带单个 CJK → 疑英译正文混入中文
SUSPECT_MIX = re.compile(r"[A-Za-z]{4,}\s*[\u4e00-\u9fff]\s*[A-Za-z]{4,}")


# 项目过程/元文档（非研究正文，§I 不适用）——承 F9“排除自指”精神，不计入默认语料
META_EXCLUDE = {
    "architecture.md", "tech-stack.md", "next-phase-plan.md", "engineering-workflow.md",
    "knowledge-management.md", "reference-management.md", "translation-guide.md",
    "bilingual-annotation-design.md", "visualization-research.md",
    "scalable-text-architecture.md", "source-audit-report.md", "verification-framework.md",
    "multilingual-alignment.md", "gap-analysis.md",
}


def default_targets():
    files = [f for f in sorted((ROOT / "docs").glob("*.md"))  # 顶层研究文档，不含 huayanhai/ 等子树
             if f.name not in META_EXCLUDE]
    files += sorted((ROOT / "web" / "demo" / "articles").glob("*.md"))
    return [f for f in files if f.is_file()]


def iter_md(paths):
    for p in paths:
        if p.is_dir():
            yield from sorted(p.rglob("*.md"))
        elif p.suffix.lower() == ".md":
            yield p


def strip_frontmatter_and_fences(text):
    # 去代码块，避免把 ```mermaid / ```bash 里的 ** 误计
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    # 去表格行（§I2 允许加粗出现在表格）
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("|")]
    return "\n".join(lines)


def analyze(path, bold_max):
    raw = path.read_text(encoding="utf-8", errors="replace")
    body = strip_frontmatter_and_fences(raw)
    cjk_n = len(CJK.findall(body))
    prose = body
    # 加粗只留正文（已去表格）——此处统计正文残留加粗
    bold_n = len(BOLD.findall(prose))
    density = (bold_n / (cjk_n / 1000.0)) if cjk_n >= 200 else None
    cliche = {w: prose.count(w) for w in CLICHE if prose.count(w) > 0}
    total_cliche = sum(cliche.values())
    mix_hits = len(SUSPECT_MIX.findall(prose))
    return {
        "file": path,
        "cjk": cjk_n,
        "bold": bold_n,
        "density": density,
        "over_bold": (density is not None and density > bold_max),
        "cliche": cliche,
        "cliche_total": total_cliche,
        "mix_hits": mix_hits,
    }


def main(argv):
    bold_max = 9.5
    args = [a for a in argv[1:]]
    rest = []
    i = 0
    while i < len(args):
        if args[i] == "--bold-max" and i + 1 < len(args):
            bold_max = float(args[i + 1]); i += 2
        else:
            rest.append(args[i]); i += 1

    paths = [Path(a) for a in rest] if rest else default_targets()
    results = []
    for p in iter_md(paths):
        try:
            results.append(analyze(p, bold_max))
        except Exception as e:  # noqa: BLE001
            print(f"  [SKIP] {p}: {e}")

    print("=== STYLE AUDIT (§I) ===")
    print(f"  扫描文件: {len(results)}  |  加粗密度阈值: {bold_max}/千字  |  模式: 报告(非门禁)\n")

    over = [r for r in results if r["over_bold"]]
    clich = [r for r in results if r["cliche_total"] > 0]

    print("--- I2 加粗密度超标 (正文加粗 > 阈值) ---")
    if not over:
        print("  ✅ 无")
    for r in sorted(over, key=lambda x: -x["density"]):
        print(f"  ⚠ {r['density']:5.2f}/千字  bold={r['bold']:3d}  cjk={r['cjk']:5d}  {r['file'].name}")

    print("\n--- I4 套话/翻译腔命中 (Top 15) ---")
    if not clich:
        print("  ✅ 无")
    for r in sorted(clich, key=lambda x: -x["cliche_total"])[:15]:
        detail = ", ".join(f"{k}×{v}" for k, v in sorted(r["cliche"].items(), key=lambda kv: -kv[1]))
        print(f"  ⚠ {r['cliche_total']:3d}  {r['file'].name}  [{detail}]")

    mix = [r for r in results if r["mix_hits"] > 0]
    print("\n--- CJK-in-Latin 粗扫线索 (启发式·待细化, 不据此判定) ---")
    if not mix:
        print("  无可疑命中")
    for r in sorted(mix, key=lambda x: -x["mix_hits"])[:15]:
        print(f"  · {r['mix_hits']:3d}  {r['file'].name}")

    print("\n=== SUMMARY ===")
    print(f"  files={len(results)}  over_bold={len(over)}  with_cliche={len(clich)}  mix_suspect={len(mix)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
