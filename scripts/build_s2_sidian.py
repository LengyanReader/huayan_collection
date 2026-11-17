#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S2 祀典半边：史部三书入库＋華嚴/祀典邻域扫描。

三源（Kanripo，皆为史部/诏令类一手文献）：
  · 《舊唐書》KR2a0026（後晉 劉昫）——禮儀志、本紀
  · 《唐會要》KR2m0002（宋 王溥）——祀典、尊崇道教/佛教诸卷
  · 《唐大詔令集》KR2f0010（宋 宋敏求）——诏令原文

方法：逐卷下载（并发、幂等、逐档 sha256）；全卷扫描「華嚴」并取上下文；
邻域关键词（祀／祭／廟／壇／齋／道場）用于把命中分到「祀典语境／其他」。
只报命中，不下判——判读在文章 §17.20。

Usage:
  python scripts/build_s2_sidian.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "s2_sidian.json"
BASE = "https://raw.githubusercontent.com/kanripo"

CORPORA = {
    "KR2a0026": ("jiutangshu", "《舊唐書》，後晉劉昫等撰，Kanripo KR2a0026", 188),
    "KR2m0002": ("tanghuiyao", "《唐會要》，宋王溥撰，Kanripo KR2m0002", 101),
    "KR2f0010": ("tangdazhaoling", "《唐大詔令集》，宋宋敏求輯，Kanripo KR2f0010", 110),
    "KR2m0001": ("tongdian", "《通典》，唐杜佑撰，Kanripo KR2m0001", 206),
    "KR2m0021": ("kaiyuanli", "《大唐開元禮》，唐蕭嵩等撰，Kanripo KR2m0021", 151),
    "KR2n0013": ("jinshi", "《金石錄》，宋趙明誠撰，Kanripo KR2n0013（金石樣本）", 32),
}
KW = "華嚴"
NEAR = ["祀", "祭", "廟", "壇", "齋", "道場", "寺", "度僧", "功德"]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fetch(repo: str, n: int) -> tuple[int, bytes | None, str]:
    url = f"{BASE}/{repo}/master/{repo}_{n:03d}.txt"
    req = urllib.request.Request(url, headers={"User-Agent": "huayan-fetch/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return n, r.read(), ""
    except Exception as e:  # noqa: BLE001
        return n, None, f"{type(e).__name__}: {e}"


def main() -> int:
    result = {"meta": {"date": date.today().isoformat(),
                       "purpose": "S2 祀典半边：史部三书中的華嚴邻域扫描",
                       "method": "逐卷下载（并发 8）、逐档 sha256；扫描「華嚴」并取 ±120 字上下文；"
                                 "邻域词仅作归类的辅助，不作判据。",
                       "corpora": {}},
              "hits": [], "files": {}}
    for repo, (slug, edition, nfiles) in CORPORA.items():
        d = ROOT / "data" / "references" / ("jinshi" if slug == "jinshi" else "shiji/" + slug)
        d.mkdir(parents=True, exist_ok=True)
        got, failed, meta = 0, [], {}
        todo = [n for n in range(0, nfiles)
                if not (d / f"{repo}_{n:03d}.txt").exists()]
        with ThreadPoolExecutor(max_workers=8) as ex:
            for n, data, err in ex.map(lambda n: fetch(repo, n), todo):
                if data is None:
                    failed.append({"n": n, "err": err})
                    continue
                (d / f"{repo}_{n:03d}.txt").write_bytes(data)
                got += 1
        for p in sorted(d.glob(f"{repo}_*.txt")):
            raw = p.read_bytes()
            meta[p.name] = {"bytes": len(raw), "sha256": sha256(raw)}
        result["meta"]["corpora"][repo] = {
            "slug": slug, "edition": edition, "files": len(meta),
            "downloaded": got, "failed": failed[:5]}
        result["files"].update(meta)
        # 扫描
        for p in sorted(d.glob(f"{repo}_*.txt")):
            t = p.read_text(encoding="utf-8", errors="replace")
            t = re.sub(r"<pb:[^>]*>", "", t)
            t = t.replace("¶", "").replace("\n", "")
            for m in re.finditer(KW, t):
                ctx = t[max(0, m.start() - 60):m.start() + 80]
                near = [k for k in NEAR if k in ctx]
                result["hits"].append({
                    "corpus": slug, "file": p.name, "pos": m.start(),
                    "near": near, "ctx": ctx,
                })
    result["summary"] = {
        "hits": len(result["hits"]),
        "by_corpus": {slug: sum(1 for h in result["hits"] if h["corpus"] == slug)
                      for _, (slug, _, _) in CORPORA.items()},
        "with_ritual_near": sum(1 for h in result["hits"] if h["near"]),
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=1))
    for h in result["hits"][:40]:
        print(f"  [{h['corpus']}] {h['file']} near={','.join(h['near'])} | {h['ctx'][:100]}")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
