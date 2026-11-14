#!/usr/bin/env python3
"""Build the Tanjur catalog: extract work headers from the Esukhia eTengyur
(mdo-sde / sūtra-commentary section, Derge vols 113–122) and pull out the
works whose titles relate to the Avataṃsaka.

Sources: Esukhia/derge-tengyur (Digital Derge Tengyur). Each volume file is
folio-prefixed text; every work starts with {D####} + Sanskrit/Tibetan title.

Usage:
  python scripts/build_tanjur_catalog.py            # download missing + extract
  python scripts/build_tanjur_catalog.py --dry-run  # probe only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TDIR = ROOT / "data" / "references" / "tibetan" / "derge_tengyur"
OUT = ROOT / "data" / "research" / "tanjur_catalog.json"

BASE = "https://raw.githubusercontent.com/Esukhia/derge-tengyur/master/text"
VOL_NOS = list(range(113, 123))          # mdo-sde section, 10 volumes
API = ("https://api.github.com/repos/Esukhia/derge-tengyur/contents/"
       "text?per_page=100")

# 华严相关题名关键词（藏文转写）
KEYS = {
    "sdong po bkod": "华严·树严（入法界/华严）",
    "phal po chen": "华严（phal po che）",
    "phal chen": "华严（phal chen）",
    "sa bcu": "十地",
    "bzang po smon lam": "行愿",
    "bzang spyod smon lam": "行愿",
}

WORK_RE = re.compile(r"\[([0-9]+[ab](?:\.\d+)?)\]\{D(\d+)\}([^\n]+)")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fetch(url: str) -> bytes:
    p = urllib.parse.urlsplit(url)
    url2 = urllib.parse.urlunsplit(
        (p.scheme, p.netloc, urllib.parse.quote(p.path), p.query, p.fragment))
    req = urllib.request.Request(url2, headers={"User-Agent": "huayan-fetch/1.0"})
    with urllib.request.urlopen(req, timeout=240) as r:
        return r.read()


def volume_urls() -> dict[int, str]:
    req = urllib.request.Request(API, headers={"User-Agent": "huayan-fetch/1.0"})
    entries = json.loads(urllib.request.urlopen(req, timeout=60).read())
    out = {}
    for it in entries:
        m = re.match(r"(\d+)_", it["name"])
        if m and int(m.group(1)) in VOL_NOS:
            out[int(m.group(1))] = it["download_url"]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    TDIR.mkdir(parents=True, exist_ok=True)
    urls = volume_urls()
    if len(urls) != len(VOL_NOS):
        print(f"x 预期 {len(VOL_NOS)} 卷，API 只见 {len(urls)} 卷")
        return 1

    volumes = {}
    for no in VOL_NOS:
        dest = TDIR / f"vol{no:03d}.txt"
        if dest.exists() and dest.stat().st_size > 100_000:
            data = dest.read_bytes()
            print(f"  · vol{no:03d} 已在库 {len(data):,} B")
        else:
            if args.dry_run:
                print(f"  ⬇ vol{no:03d}（dry-run 跳过写入）")
                continue
            print(f"  ⬇ vol{no:03d} …", flush=True)
            data = fetch(urls[no])
            dest.write_bytes(data)
        volumes[no] = {"path": str(dest.relative_to(ROOT)).replace("\\", "/"),
                       "bytes": len(data), "sha256": sha256(data)}

    works, huayan = [], []
    for no in sorted(volumes):
        text = (ROOT / volumes[no]["path"]).read_text(encoding="utf-8")
        parts = re.split(r"\{D(\d+)\}", text)
        for i in range(1, len(parts) - 1, 2):
            dno = int(parts[i])
            seg = parts[i + 1][:400].replace("#", "").strip()
            if not seg:
                continue
            mt = re.search(r"བོད་སྐད་དུ།(.+?)(?:། |།|$)", seg, re.S)
            tib = re.sub(r"\s+", " ", mt.group(1)).strip() if mt else seg[:120]
            sans = re.sub(r"\s+", " ", seg.split("བོད་སྐད་དུ")[0]
                          .replace("༄༅༅", "").strip(" །"))[:150]
            folio_m = re.match(r"\[([0-9]+[ab](?:\.\d+)?)\]", parts[i + 1])
            work = {"D": dno, "vol": no,
                    "folio": folio_m.group(1) if folio_m else "?",
                    "title_tib": tib[:150], "title_sans": sans}
            works.append(work)
            blob = tib + " " + sans
            hit = next((zh for k, zh in KEYS.items() if k in blob), None)
            if hit:
                work["topic"] = hit
                huayan.append(work)

    # --- dkar chag（目录卷 213）：行愿讚释线等华严相关条目 ---
    DK = TDIR / "vol213_dkarchag.txt"
    dkarchag = {}
    if DK.exists():
        raw = DK.read_text(encoding="utf-8").replace("\n", " ")
        folio_at = [(m.start(), m.group(1)) for m in
                    re.finditer(r"\[(\d+[ab](?:\.\d+)?)\]", raw)]
        folio_at.append((len(raw), "?"))

        def folio_of(pos: int) -> str:
            for p, f in folio_at:
                if p > pos:
                    return f
            return "?"

        entries = []
        for kw, zh in (("བཟང་པོ་སྤྱོད་པ", "行愿讚释"),
                       ("སྡོང་པོ་བཀོད་པ", "华严·树严"),
                       ("ཕལ་ཆེན", "phal chen")):
            for m in re.finditer(kw, raw):
                s, e = max(0, m.start() - 60), m.start() + 320
                ctx = raw[s:e]
                if "མཛད་པ" not in ctx and "འགྱུར" not in ctx:
                    continue
                if not ctx.rstrip().endswith("།") and "འགྱུར" not in ctx:
                    continue
                entries.append({"kw": kw, "topic": zh, "folio": folio_of(m.start()),
                                "text": re.sub(r"\[[0-9xab.]+\]|\{[^}]*\}", "", ctx).strip()})
        dkarchag = {"source": str(DK.relative_to(ROOT)).replace("\\", "/"),
                    "sha256": sha256(DK.read_bytes()),
                    "entries": entries}

    result = {
        "meta": {
            "date": date.today().isoformat(),
            "source": "Esukhia/derge-tengyur（Digital Derge Tengyur）",
            "scope": f"经释部（མདོ་སྡེ）Derge 卷 {VOL_NOS[0]}–{VOL_NOS[-1]}＋目录卷 213",
            "keywords": KEYS,
            "note": "题录=各论 {D####} 头行原文截取（README：{DX} 即 Tohoku 号，转写不完整故稀疏）；"
                    "dkar chag 条目为题名＋作者＋译者原样截取；关键词覆盖之外的题名仍待逐条判读。",
            "volumes": volumes,
            "dkarchag": dkarchag,
        },
        "works_total": len(works),
        "huayan": huayan,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"works={len(works)}  huayan-related={len(huayan)}")
    for w in huayan:
        print(f"  D{w['D']} vol{w['vol']} {w['topic']}: {w['title'][:70]}")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
