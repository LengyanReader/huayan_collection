# -*- coding: utf-8 -*-
"""quote_koushu.py — 僧传画像 ✓ 引文回盘校勘扫描（引文面闸·v2 按檔归属版）。

v2 改动：① 逐檔建索引（命中可报所在檔）；② 全片段未命中时按「·/＝/＋/、」二次
切分，各 ≥4 字子段全命中者记 split-hit；③ 行内声明经号(T####/X####)与命中檔比对，
命中但不在声明源=「attr?」（错挂史源候选），全檔皆无=「MISS」。
只读不改页；报告落 tasks/。用法：python scripts/quote_koushu.py [--min 6]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIRS = [ROOT / "data/references/cbeta", ROOT / "data/references/cbeta_txt"]
PAGE_DIR = ROOT / "docs" / "草稿" / "高僧传" / "僧传画像" / "portraits"
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
TAG = re.compile(r"<[^>]*>")
QUOTE = re.compile(r"「([^」]{4,400})」")
SPLIT = re.compile(r"…|／|\.\.\.|\\n")
SPLIT2 = re.compile(r"[·＝=＋+]")
SIGLA = re.compile(r"([TX])(?:\d{2})?n?(\d{4})")

try:
    from zhconv import convert as _zc
    def tol(s):  # 折叠为简体重叠空间（校「引文抄成简体」型失配）
        return _zc(s, "zh-cn")
except Exception:  # zhconv 不可用则退化为恒等（不误报 SIMPL）
    def tol(s):
        return s


def norm(s: str) -> str:
    return "".join(CJK.findall(s))


def file_num(name):
    # T50n2061.xml → 2061；T1733_法藏_探玄记.txt → 1733（入库命名变体）
    m = re.search(r"n(\d{4})", name) or re.search(r"(\d{4})", name)
    return m.group(1) if m else "-"


def load_index():
    idx = []  # (label, nnum, text_strict, text_loose)
    for d in CORPUS_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.iterdir()):
            if f.suffix.lower() not in (".xml", ".txt") or not f.is_file():
                continue
            raw = f.read_text(encoding="utf-8", errors="ignore")
            if f.suffix.lower() == ".xml":
                raw = TAG.sub("", raw)
            t = norm(raw)
            idx.append((f.name, file_num(f.name), t, tol(t)))
    return idx


def find(frag, idx):
    return [lab for lab, _, text, _l in idx if frag in text]


def findl(frag, idx):
    f2 = tol(frag)
    return [lab for lab, _, _t, loose in idx if f2 in loose]


def nnum(lab):
    return file_num(lab) if lab != "-" else lab


def check_page(path: Path, idx, min_len):
    corpus_nums = {num for _, num, _, _ in idx if num != "-"}
    rows = []
    n = nh = nsplit = nl = 0
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        decl = {b for a, b in SIGLA.findall(line)}
        nodisk = decl - corpus_nums
        if nodisk and "✓" in line:
            rows.append((i, "NODISK✓", "声明经号未入库:" + ",".join(sorted(nodisk)), "-", ""))
        for q in QUOTE.findall(line):
            for frag in SPLIT.split(q):
                f = norm(frag)
                if len(f) < min_len:
                    continue
                n += 1
                hits = find(f, idx)
                if hits:
                    nh += 1
                    if decl and not ({nnum(h) for h in hits} & decl):
                        rows.append((i, "attr?", frag[:52], ",".join(sorted(hits))[:40],
                                     ",".join(sorted(decl))))
                    continue
                looselab = findl(f, idx)
                if looselab:
                    nl += 1
                    mark = "✓" if "✓" in line else ("◐" if "◐" in line else "-")
                    rows.append((i, "LOOSE" + mark, frag[:52],
                                 ",".join(sorted(looselab))[:40], ""))
                    continue
                subs = [norm(s) for s in SPLIT2.split(frag)]
                subs = [s for s in subs if len(s) >= 4]
                if subs and all(find(s, idx) for s in subs):
                    nsplit += 1
                    hs = {x for s in subs for x in find(s, idx)}
                    if decl and not ({nnum(h) for h in hs} & decl):
                        rows.append((i, "attr-s?", frag[:52], ",".join(sorted(hs))[:40],
                                     ",".join(sorted(decl))))
                    continue
                mark = "✓" if "✓" in line else ("◐" if "◐" in line else "-")
                # 引文 vs 评述标签判分：CJK≥10 视为引文，否则标签（不入库判）
                kind = ("MISS" if len(f) >= 10 else "label") + mark
                rows.append((i, kind, frag[:52],
                             "-".join(sorted(decl)) or "-", ""))
    return rows, n, nh, nsplit, nl


def main():
    args = sys.argv[1:]
    min_len = int(args[args.index("--min") + 1]) if "--min" in args else 6
    idx = load_index()
    print(f"[index] {len(idx)} 檔 · {sum(len(x[2]) for x in idx):,} 字")
    out = ROOT / "docs" / "草稿" / "高僧传" / "僧传画像" / "tasks" / "校勘_引文回盘_首轮.md"
    lines = ["# 校勘扫描 · 引文回盘（v2 归属版）", "",
             f"- 判准：「…」引文按省略号切段·≥{min_len} 汉字整段子串；未命中再按 ·＝＋ 切分各≥4段子查",
             "- MISS✓＝标✓而未回源（**最高风险**）；attr?＝命中但不在行内声明经号（错挂史源候选）；MISS◐/-＝单源待核类引用（次要）", ""]
    tot = 0
    for p in sorted(x for x in PAGE_DIR.glob("*.html")):
        rows, n, nh, ns, nl = check_page(p, idx, min_len)
        tot += len(rows)
        lines.append(f"## {p.name} — 片段 {n} · 整段命中 {nh} · 拆分命中 {ns} · 简折命中 {nl} · 待核 {len(rows)}")
        if rows:
            lines.append("| 行 | 类 | 片段 | 声明/命中檔 | |")
            lines.append("|---|---|---|---|---|")
            for i, kind, frag, a, b in rows:
                lines.append(f"| {i} | {kind} | {frag} | {a}{b} | |")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[done] 待核合计 {tot} · 报告：{out}")


if __name__ == "__main__":
    main()
