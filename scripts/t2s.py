#!/usr/bin/env python3
"""t2s.py — 繁→简 转换工具（偈颂/经文转录用）

用于卷二细读一类工作：CBETA（T279）为繁体，转录进正文需转简体。
两个引擎并存互校：

  zhconv  主引擎。基于 CC-CEDICT + MediaWiki 词表，**能转异体变体**
           （如「覩」→「睹」，CBETA 常见；opencc t2s 表不含此字）。
  opencc   副引擎。标准 OpenCC t2s 词表，用作交叉校勘与差异取证。

用法：
  t2s.py 字符串...            # 转标准入（中文标点保留）
  t2s.py --file juan2.xml     # 转文件（输出到 stdout）
  t2s.py --engine opencc ...  # 指定引擎
  t2s.py --diff --file x.txt  # 双引擎逐行比对，只打印不一致行（校勘用）

退出码：0 成功；2 参数/文件错误；3 引擎不可用。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _load_engine(name: str):
    """Return convert(text) -> str for the named engine, or raise ImportError."""
    if name == "zhconv":
        from zhconv import convert  # type: ignore

        return lambda s: convert(s, "zh-cn")
    if name == "opencc":
        from opencc import OpenCC  # type: ignore

        cc = OpenCC("t2s")
        return cc.convert
    raise ValueError(name)


def _diff_lines(a: str, b: str) -> list[tuple[int, str, str]]:
    """Compare two conversions line by line; return differing (lineno, zhconv, opencc)."""
    la, lb = a.splitlines(), b.splitlines()
    out: list[tuple[int, str, str]] = []
    for i in range(max(len(la), len(lb))):
        x = la[i] if i < len(la) else ""
        y = lb[i] if i < len(lb) else ""
        if x != y:
            out.append((i + 1, x, y))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description="繁→简 转换（zhconv 主 / opencc 副，双引擎可交叉校勘）",
    )
    ap.add_argument("text", nargs="*", help="待转换文本（不给则读 stdin）")
    ap.add_argument("--file", type=Path, help="输入文件（不给则读 stdin / 用 text 参数）")
    ap.add_argument("--engine", default="zhconv",
                    choices=("zhconv", "opencc"), help="转换引擎（默认 zhconv）")
    ap.add_argument("--diff", action="store_true",
                    help="双引擎逐行比对，只输出不一致行（校勘用）")
    args = ap.parse_args()

    try:
        conv = _load_engine(args.engine)
    except ImportError as exc:
        print(f"[ERROR] 引擎不可用: {exc}", file=sys.stderr)
        print("  pip install zhconv opencc-python-reimplemented", file=sys.stderr)
        sys.exit(3)

    if args.file:
        src = args.file.read_text(encoding="utf-8")
    elif args.text:
        src = " ".join(args.text)
    else:
        src = sys.stdin.read()
    if not src.strip():
        print("[ERROR] 空输入", file=sys.stderr)
        sys.exit(2)

    if args.diff:
        try:
            conv_o = _load_engine("opencc")
        except ImportError as exc:
            print(f"[ERROR] --diff 需要 opencc 引擎: {exc}", file=sys.stderr)
            sys.exit(3)
        a = _load_engine("zhconv")(src)
        b = conv_o(src)
        diffs = _diff_lines(a, b)
        if not diffs:
            print("[OK] 双引擎结果一致（无差异）")
            return
        print(f"[DIFF] {len(diffs)} 行不一致：zhconv | opencc")
        for n, x, y in diffs:
            print(f"  L{n}:")
            print(f"    zhconv: {x}")
            print(f"    opencc: {y}")
        return

    out = conv(src)
    sys.stdout.reconfigure(encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
