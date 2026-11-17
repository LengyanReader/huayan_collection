#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""丹珠尔华严八命中题记扫描（题录层再加深：卷内译场记）。

eTengyur 正文每部论末有译场题记（「…རྫོགས་སོ།། རྒྱ་གར་གྱི་མཁན་པོ X དང་།
ཞུ་ཆེན་གྱི་ལོ་ཙཱ་བ Y བསྒྱུར…」），位于下一部论的 {D####} 标记之前。
对八条命中（D3993/3998/3999/4011–4015）各取其题记原句，
并入 `tanjur_qual.json`（新增 `in_text_colophon` 字段）。

只照录原文＋位置，不转译作断言。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUAL = ROOT / "data" / "research" / "tanjur_qual.json"
VOLS = {"3993": ("vol113", 113), "3998": ("vol116", 116), "3999": ("vol116", 116),
        "4011": ("vol117", 117), "4012": ("vol117", 117), "4013": ("vol117", 117),
        "4014": ("vol117", 117), "4015": ("vol117", 117)}

COLOPHON_RE = re.compile(
    r"[^#\n]{0,40}(?:མཁན་པོ|ལོ་ཙཱ་བ)[#\s]{0,6}[^#\n]{0,60}(?:[#\s]{0,6}[^#\n]{0,60})*?"
    r"(?:བསྒྱུར|ཞུས|འགྱུར)[^#\n]{0,70}")


def main() -> int:
    texts = {v: Path(f"data/references/tibetan/derge_tengyur/{v}.txt")
             .read_text(encoding="utf-8-sig", errors="replace")
             for v in ("vol113", "vol116", "vol117")}
    data = json.loads(QUAL.read_text(encoding="utf-8"))
    n_ok = 0
    for w in data["works"]:
        D = str(w["D"])
        if D not in VOLS:
            continue
        volname, volno = VOLS[D]
        t = texts[volname]
        m = re.search(r"\{D" + D + r"\}", t)
        if not m:
            w["in_text_colophon"] = {"ok": False, "note": "work head not found"}
            continue
        nxt = re.search(r"\{D\d+\}", t[m.end():])
        end = m.end() + nxt.start() if nxt else len(t)
        seg = t[m.start():end]
        # 简化提取：找部末「རྫོགས་སོ」之后到段尾（下一部 {D} 之前）的译场套式
        cm = None
        tail = seg[-420:]
        if re.search(r"མཁན་པོ|ལོ་ཙཱ་བ", tail) and \
                re.search(r"བསྒྱུར|ཞུས|འགྱུར", tail):
            i = min([p for p in (tail.find("མཁན་པོ"), tail.find("ལོ་ཙཱ་བ"),
                                  tail.find("རྫོགས་སོ"))
                     if p >= 0] or [0])
            cm = tail[max(0, i - 10):].replace("\n", " ") \
                                       .replace("#", "").strip()
        if not cm:
            # 作者记（…མཛད་པ་རྫོགས་སོ）有、译场记无——照录作者句
            am = re.search(r"[^\n]{0,120}མཛད་པ་རྫོགས་སོ[^#\n]{0,10}", tail)
            if am:
                w["in_text_colophon"] = {
                    "ok": False, "vol": volno,
                    "author_colophon": am.group(0)
                                       .replace("\n", " ").replace("#", "").strip(),
                    "note": "author-only colophon (no translator formula)"}
                print(f"D{D} [{volname}]: author-only …{w['in_text_colophon']['author_colophon'][:70]}…")
            else:
                w["in_text_colophon"] = {"ok": False, "vol": volno,
                                         "note": "no translator formula in segment"}
            continue
        w["in_text_colophon"] = {"ok": True, "vol": volno, "text": cm}
        n_ok += 1
        print(f"D{D} [{volname}]: …{cm[:90]}…")
    # D4012 造者校正：卷内题记「སློབ་དཔོན་ཕྱོགས་ཀྱི་གླང་པོས་མཛད」（陈那造）
    for w in data["works"]:
        if w["D"] == 4012:
            w["author_dkarchag"] = (
                "སློབ་དཔོན་ཕྱོགས་ཀྱི་གླང་པོས་མཛད（陈那造）——eTengyur 卷内题记"
                "（vol117）直接证据；dkar chag 216b.5 条目群内萨班诸作为同簇他书，"
                "先前据邻近条目的归属判读据此更正〔本文判断〕")
            w["author_correction"] = "dkar chag 邻近条目判读 → 卷内题记直证：陈那（Dignāga）"
    data["meta"]["colophon_scan"] = {
        "date": "2026-11-18",
        "method": ("eTengyur 正文部末译场题记（མཁན་པོ/ལོ་ཙཱ་བ/བསྒྱུར 套式），"
                   "取命中八部论各自段内的末条译记，照录原文。"),
        "n_ok": n_ok,
    }
    QUAL.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    print("written", QUAL, f"({n_ok}/8)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
