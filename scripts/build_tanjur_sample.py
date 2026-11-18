#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""丹珠尔内容层抽样：八部华严论的归敬颂与规模（内容层的第一步）。

对 tanjur_qual 的八部命中，从 eTengyur 卷文件（在库）各取：
  · 部头（该 work 段的行数/字符数——规模）
  · 开头 120 字符（标题重诵＋归敬颂原文照录）
这是「内容层」的**抽样**，不是逐部对读——如实标注。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUAL = ROOT / "data" / "research" / "tanjur_qual.json"
VOLS = {3993: "vol113", 3998: "vol116", 3999: "vol116",
        4011: "vol117", 4012: "vol117", 4013: "vol117",
        4014: "vol117", 4015: "vol117"}


def main() -> int:
    texts = {v: Path(f"data/references/tibetan/derge_tengyur/{v}.txt")
             .read_text(encoding="utf-8-sig", errors="replace")
             for v in ("vol113", "vol116", "vol117")}
    data = json.loads(QUAL.read_text(encoding="utf-8"))
    n = 0
    for w in data["works"]:
        D = str(w["D"])
        vol = VOLS[w["D"]]
        t = texts[vol]
        m = re.search(r"\{D" + D + r"\}", t)
        if not m:
            continue
        nxt = re.search(r"\{D\d+\}", t[m.end():])
        end = m.end() + nxt.start() if nxt else len(t)
        seg = t[m.start():end]
        body = seg.replace("\n", " ")
        clean = re.sub(r"\[[0-9a-z.\]]+\]|#\{D\d+\}", " ", body)
        clean = re.sub(r"\s+", " ", clean).strip()
        head = clean[:150]
        w["content_sample"] = {
            "vol": vol.replace("vol", ""),
            "chars": len(clean),
            "opening": head,
        }
        n += 1
        print(f"D{D} {vol} {len(clean):>7,}字 — {head[:70]}…")
    data["meta"]["content_sample"] = {
        "date": "2026-11-19",
        "method": ("内容层抽样＝每部取部头（段内字符数）与开头 150 字符"
                   "（标题重诵＋归敬颂原文照录）；逐部对读仍未做——如实标注。"),
        "n": n,
    }
    QUAL.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    print("written", QUAL, f"({n}/8)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
