#!/usr/bin/env python3
"""cbeta_extract.py — 从 CBETA TEI/P5 XML 抽取指定本传的**净读文本**，供综述逐句回源。

背景：`data/references/cbeta/*.xml` 是逐字一手底本，但满布 <lb>/<pb>/<anchor>/<cb:*>
等结构标签，不便通读。本工具按「起标记 →（止标记／行数窗）」切出目标段落，剥标签
还原文字，把 CBETA 每行约二十字的断行**缝合为连续正文**（中文不插空格），并在原
<p> 起处保留换行，便于人读与引用定位。

只读不改：本脚本绝不写回 .xml（一手性一经改动即失）。抽取结果默认打到 stdout；
--out 可另存为工作稿（属临时件，勿入库）。

规矩（承《data/references/cbeta/README.md》契约）：
  · CBETA 原文为**繁体**，起／止标记须用繁体正字（如 釋玄奘／那提）。
  · 抽取仅供回源比对，引文入页面时须逐字照录原文，不得改写。

用法：
  python cbeta_extract.py data/references/cbeta/T50n2060.xml \
      --start 釋玄奘 --end 釋那提
  python cbeta_extract.py FILE --start REGEX --max-lines 400 [--out work.txt]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TAG = re.compile(r"<[^>]*>")
# <p ...> 起处视作段界（还原段落感）
P_OPEN = re.compile(r"<p[\s>]")

sys.stdout.reconfigure(encoding="utf-8")


def clean_line(line: str) -> str:
    """剥掉所有标签，保留文字节点。anchor/pb/milestone 等自闭合标签无内容，自然滤除。"""
    # 段界用换行占位（<p> 处），再统一剥标签
    marked = P_OPEN.sub("\u0000<p ", line)
    txt = TAG.sub("", marked)
    # \u0000 标记位转成换行；其余 CBETA 断行缝合为空（中文连续）
    return txt


def extract(path: Path, start: str, end: str | None, max_lines: int):
    lines = path.read_text(encoding="utf-8").splitlines()
    # 先逐行剥标签得净文（CBETA 用 <anchor>/<lb> 等把字拆开，故标记须在净文上匹配，
    # 而非原始 XML 行），再据此定起止。
    cleaned = [clean_line(l) for l in lines]
    si = None
    for i, c in enumerate(cleaned):
        flat = c.replace("\u0000", "")
        if re.search(start, flat):
            si = i
            break
    if si is None:
        raise SystemExit(f"未找到起标记 {start!r}（注意 CBETA 为繁体，须用正字）")
    out = []
    count = 0
    for j in range(si, len(cleaned)):
        flat = cleaned[j].replace("\u0000", "")
        if end and count > 0 and re.search(end, flat):
            break
        out.append(cleaned[j])
        count += 1
        if count >= max_lines:
            break
    # 缝合：每原始行是一条 CBETA 断行；段界处出换行，其余直接相接
    text = "".join(out)
    text = text.replace("\u0000", "\n")
    # 归并多余空白与孤行
    text = re.sub(r"[ \t]+", "", text)
    text = re.sub(r"\n{2,}", "\n", text).strip()
    return text, count


def main():
    ap = argparse.ArgumentParser(description="CBETA TEI → 本传净读文本抽取（只读）")
    ap.add_argument("file", help="XML 路径（如 data/references/cbeta/T50n2060.xml）")
    ap.add_argument("--start", required=True, help="起标记（正则，繁体正字）")
    ap.add_argument("--end", help="止标记（正则，exclusive）")
    ap.add_argument("--max-lines", type=int, default=4000, help="最多扫过的原始行数")
    ap.add_argument("--out", help="另存工作稿路径（默认打到 stdout）")
    a = ap.parse_args()

    path = Path(a.file)
    if not path.exists():
        raise SystemExit(f"文件不存在：{path}")
    text, nl = extract(path, a.start, a.end, a.max_lines)
    head = f"# {path.name} · 起于 {a.start!r} · 扫过 {nl} 行 · {len(text)} 字\n\n"
    body = head + text + "\n"
    if a.out:
        Path(a.out).write_text(body, encoding="utf-8")
        print(f"已写出 {a.out}（{len(text)} 字，扫过 {nl} 行）")
    else:
        print(body)


if __name__ == "__main__":
    main()
