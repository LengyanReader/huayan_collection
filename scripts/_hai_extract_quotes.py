# -*- coding: utf-8 -*-
"""海云继梦法师修行体系研究·原话抽取器

用途：从 docs/huayanhai/ 645 篇讲记中抽取「自述性」原话候选，输出带
file_path:line_start-line_end 的可溯证据，供文章正文引用。

设计要点（遵 harness 深度研究规范）：
1. 自述优先：只保留主语指向法师自身（我/我们/法师自述语气）的语境。
2. 可溯：行号而非字符偏移，便于复核。
3. 不臆断：只抽取，不判定；判定由人工按语境完成。

用法：
  python scripts/_hai_extract_quotes.py --kind self  --top 40
  python scripts/_hai_extract_quotes.py --kind weave --top 30
  python scripts/_hai_extract_quotes.py --kind revise --top 30
"""
import argparse
import json
import os
import re
import sys

# Windows 控制台默认 cp1252/cp936，中文输出会抛 UnicodeEncodeError。
# 统一改用 UTF-8 缓冲输出（stdout/stderr 皆然），此为既有脚本同一坑的复现。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

BASE = "docs/huayanhai"
MANIFEST = os.path.join(BASE, "export_manifest.json")

# ── 词表 ────────────────────────────────────────────────────────────
KIND_PATTERNS = {
    # 过程性自述：摸索/曲折/边修边讲/调整…
    "self": re.compile(
        r"(摸索|探索|曲折|走弯路|走错|犯过错|犯过错误|有过错误|失误|"
        r"边修边讲|边讲边修|边体会|边理顺|边走边拼|边学边讲|"
        r"调整|修订|修正|改变说法|说法改变)"
    ),
    # 组织性思路：拼图/贯通/串起/打通
    "weave": re.compile(
        r"(拼图|拼起来|拼起来|串起来|串起|贯通|融会贯通|打通|贯串|"
        r"连起来|连接起来|接起来|一以贯之)"
    ),
    # 体系整体性称谓
    "system": re.compile(
        r"(整个体系|这个体系|华严.{0,4}体系|修行体系|.{0,4}体系.{0,4}完成|"
        r"大体理顺|基本理顺|基本能走通|走通|定型|成熟了|完成)"
    ),
}

# 自述语气标记（须命中其一，方进入候选）
SELF_MARKERS = re.compile(
    r"(我们[^。！？]{0,12}(讲|学|修|做|整理|理顺|体会|体认|发现)|"
    r"我[^。！？]{0,12}(讲|学|修|做|整理|理顺|体会|体认|发现|走|试)|"
    r"法师[^。！？]{0,12}(讲|说|提|指出|强调)|"
    r"当年|那时候|起初|最初|一开始|后来才发现|回头看|"
    r"所以我|因此我|我才|我就|我们才)"
)

# 排除语境：纯教理定义、他人转述（避免把经义当自述）
EXCLUDE_MARKERS = re.compile(
    r"(所谓|例如|譬如|就像|经云|经中云|菩萨云|论云|祖师云|问曰|答曰|"
    r"瑜伽|唯识|中观|论文|学者|研究)"
)


def iter_files():
    """依 manifest 列出实际存在的讲记文件（txt 优先，其次 html）。"""
    if not os.path.exists(MANIFEST):
        sys.exit("manifest 不存在：%s" % MANIFEST)
    with open(MANIFEST, "r", encoding="utf-8") as f:
        items = json.load(f)
    for it in items:
        for key in ("txtPath", "htmlPath"):
            rel = it.get(key) or ""
            if not rel:
                continue
            fp = os.path.join(BASE, rel)
            if os.path.exists(fp):
                yield fp
                break


def extract(pattern, need_self=True, ctx_chars=180):
    """抽取命中段，返回 (file, line_start, line_end, kw, context)。"""
    seen = set()
    out = []
    for fp in iter_files():
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        if not text.strip():
            continue
        lines = text.splitlines()
        for m in pattern.finditer(text):
            # 字符偏移 → 行号（二分定位，避免逐行累加）
            off = m.start()
            lo, hi = 0, len(lines)
            while lo < hi:
                mid = (lo + hi) // 2
                if sum(len(l) + 1 for l in lines[:mid]) <= off:
                    lo = mid + 1
                else:
                    hi = mid
            li = lo
            ctx_start = max(0, off - ctx_chars)
            ctx_end = min(len(text), m.end() + ctx_chars)
            ctx = text[ctx_start:ctx_end].replace("\r", " ").replace("\n", " ")
            ctx = re.sub(r"\s+", " ", ctx).strip()

            if need_self and not SELF_MARKERS.search(ctx):
                continue
            if EXCLUDE_MARKERS.search(ctx):
                continue
            key = (fp, li // 8, m.group(1))
            if key in seen:
                continue
            seen.add(key)
            out.append(
                {
                    "file": fp.replace("\\", "/"),
                    "line_start": li + 1,
                    "line_end": min(len(lines), li + 3),
                    "kw": m.group(1),
                    "ctx": ctx,
                }
            )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", default="self",
                    choices=["self", "weave", "system"])
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--no-self", action="store_true",
                    help="关闭自述语气要求（用于统计总量分布）")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    rows = extract(KIND_PATTERNS[args.kind],
                   need_self=not args.no_self)

    # 按关键词出现频次排序（同词多处出现者优先，便于看稳定表述）
    from collections import Counter
    kwc = Counter(r["kw"] for r in rows)
    rows.sort(key=lambda r: -kwc[r["kw"]])

    lines = [
        "# 抽取结果 kind=%s  总候选=%d  （自述语气=%s）"
        % (args.kind, len(rows), "开" if not args.no_self else "关"),
        "",
        "## 关键词频次分布",
    ]
    for kw, c in kwc.most_common():
        lines.append("- %s：%d" % (kw, c))
    lines.append("")
    lines.append("## 候选明细（最多 %d 条）" % args.top)
    for i, r in enumerate(rows[: args.top], 1):
        lines.append("")
        lines.append("%d. `%s:%d-%d` 〔%s〕" % (
            i, r["file"], r["line_start"], r["line_end"], r["kw"]))
        lines.append("   > %s" % r["ctx"])

    text = "\n".join(lines)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("written -> %s（%d 字符）" % (args.out, len(text)))
    else:
        print(text)


if __name__ == "__main__":
    main()
