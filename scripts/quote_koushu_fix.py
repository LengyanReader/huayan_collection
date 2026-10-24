# -*- coding: utf-8 -*-
"""quote_koushu_fix.py — 校勘落改①：把页内「抄成简体/异体」的引文按盘内原字形回填。

规则：仅处理「strict 未命中、folded(t2s) 命中」的片段；取命中处 strict 原文切片，
与片段逐位对字（CJK→CJK 一对一），把页中该片段的每个 CJK 字符替换为盘内原字，
非 CJK（标点、括号、<strong> 等标签）原样保留。多檔切片不一/长度不齐/仅能落在
非声明源者 → 不动，旗为 MANUAL。默认 dry-run 出预览；--write 才写页（先留 .koukai.bak）。
用法：python scripts/quote_koushu_fix.py [--page bukong.html] [--write]
"""
import re
import sys
import shutil
from pathlib import Path
from zhconv import convert as _zc

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIRS = [ROOT / "data/references/cbeta", ROOT / "data/references/cbeta_txt"]
PAGE_DIR = ROOT / "docs" / "草稿" / "高僧传" / "僧传画像" / "portraits"
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
TAG = re.compile(r"<[^>]*>")
QUOTE = re.compile(r"「([^」]{4,400})」")
SPLIT = re.compile(r"…|／|\.\.\.|\\n")
SIGLA = re.compile(r"([TX])(?:\d{2})?n?(\d{4})")


def norm(s):
    return "".join(CJK.findall(s))


def fold(s):
    return _zc(s, "zh-cn")


def foldstr(s):
    # 逐字折叠：与 per-char 前缀偏移严格一致（zhconv 词表整体转换可能变长导致错位）
    return "".join(fold(c) for c in s)


def load():
    files = []
    for d in CORPUS_DIRS:
        for f in sorted(d.iterdir()):
            if f.suffix.lower() in (".xml", ".txt") and f.is_file():
                raw = f.read_text(encoding="utf-8", errors="ignore")
                if f.suffix.lower() == ".xml":
                    raw = TAG.sub("", raw)
                strict = norm(raw)
                pieces = [len(fold(c)) for c in strict]
                offs, acc = [], 0
                for ln_ in pieces:
                    offs.append(acc)
                    acc += ln_
                offs.append(acc)
                loose = "".join(fold(c) for c in strict)
                m = re.search(r"n(\d{4})", f.name) or re.search(r"(\d{4})", f.name)
                files.append((f.name, m.group(1) if m else "-", strict, loose, offs))
    return files


def locate(folded, files):
    """返回候选 {(num, strict_slice): label}，strict↔loose 以前缀偏移对齐。"""
    import bisect
    out = {}
    L = len(folded)
    for lab, num, strict, loose, offs in files:
        start = 0
        while True:
            p = loose.find(folded, start)
            if p < 0:
                break
            i = bisect.bisect_right(offs, p) - 1
            j = i
            while offs[j] - offs[i] < L and j < len(strict):
                j += 1
            sl = strict[i:j]
            if "".join(fold(c) for c in sl) == folded:  # 逐位一致性守卫
                out.setdefault((num, sl), lab)
            start = p + 1
    return out


def patch_line(line, files, fixes, manual, line_no):
    decl = {b for _, b in SIGLA.findall(line)}

    def outer(mq):
        return "「" + sub_quote_inner(mq.group(1)) + "」"

    def sub_quote_inner(txt):
        for seg in SPLIT.split(txt):
            b = [c for c in seg if CJK.match(c)]
            if len(b) < 6:
                continue
            ftxt = "".join(fold(c) for c in b)
            cands = locate(ftxt, files)
            if not cands:
                continue
            slis = {sl for (_, sl) in cands}
            prefer = {sl for (n, sl) in cands if n in decl} or slis
            if len(prefer) > 1:
                manual.append((line_no, "".join(b)[:40], "多解:" + "|".join(x[:8] for x in list(prefer)[:3])))
                continue
            sl = next(iter(prefer))
            # 逐位替换：seg 中的 CJK 依次换成 sl 原字
            it = iter(sl)
            new = "".join((next(it) if CJK.match(c) else c) for c in seg)
            if new != seg:
                txt = txt.replace(seg, new, 1)
                fixes.append((line_no, seg[:36], "→", new[:36]))
        return txt

    return QUOTE.sub(outer, line)


def main():
    args = sys.argv[1:]
    write = "--write" in args
    only = args[args.index("--page") + 1] if "--page" in args else None
    files = load()
    print(f"[corpus] {len(files)} 檔")
    pages = [PAGE_DIR / only] if only else sorted(PAGE_DIR.glob("*.html"))
    preview, tot_fix, tot_man = [], 0, 0
    for p in pages:
        lines = p.read_text(encoding="utf-8").splitlines()
        fixes, manual, newline = [], [], []
        for ln, line in enumerate(lines, 1):

            newline.append(patch_line(line, files, fixes, manual, ln))
        rel = p.name
        preview.append(f"## {rel} — 回填 {len(fixes)} · 需人工 {len(manual)}")
        for f in fixes:
            preview.append(f"| L{f[0]} | {f[1]} {f[2]} {f[3]} |")
        for mm in manual:
            preview.append(f"| L{mm[0]} | MANUAL {mm[1]} {mm[2]} |")
        tot_fix += len(fixes)
        tot_man += len(manual)
        if write and fixes:
            bak = p.with_suffix(p.suffix + ".koukai.bak")
            if not bak.exists():
                shutil.copy2(p, bak)
            p.write_text("\n".join(newline), encoding="utf-8")
    out = ROOT / "docs" / "草稿" / "高僧传" / "僧传画像" / "tasks" / "校勘_字形回填_预览.md"
    header = ["# 校勘 · 引文字形回填预览（盘内原字逐位替换）", "",
              f"- 模式：{'WRITE(已落盘)' if write else 'DRY-RUN'}", ""]
    out.write_text("\n".join(header + preview), encoding="utf-8")
    print(f"[done] 回填 {tot_fix} · 人工 {tot_man} · 预览：{out}")


if __name__ == "__main__":
    main()
