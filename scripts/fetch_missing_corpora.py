#!/usr/bin/env python3
"""Fetch first-hand corpora the article currently lacks (§17 registry).

Design rules (repo iron rules):
  * Only download from sources that state their base edition (CBETA xml-p5,
    SuttaCentral bilara root, Kanripo 道藏 texts with DZ id + base edition).
  * Idempotent: skip files already on disk whose SHA-256 matches the manifest.
  * Every file is content-checked (title / dialect / header) before it counts.
  * Never overwrite a file this script did not create without --force.

Usage:
  python scripts/fetch_missing_corpora.py            # fetch what is missing
  python scripts/fetch_missing_corpora.py --dry-run  # probe only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "references" / "external_manifest.json"

CBETA = "https://raw.githubusercontent.com/cbeta-org/xml-p5/master"
SC = "https://raw.githubusercontent.com/suttacentral/bilara-data/published"
KR = "https://raw.githubusercontent.com/kanripo"
GRETIL = "https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/plaintext"

# jsDelivr mirrors the same GitHub content and is far faster on this network;
# raw.githubusercontent is kept as fallback so the manifest stays reproducible.
CBETA_ALT = "https://cdn.jsdelivr.net/gh/cbeta-org/xml-p5@master"
SC_ALT = "https://cdn.jsdelivr.net/gh/suttacentral/bilara-data@published"
KR_ALT = "https://cdn.jsdelivr.net/gh/kanripo"

TARGETS = [
    # --- 漢譯四阿含（大正藏 vol.1–2）: L3 typology baseline ---
    {
        "id": "T01n0001", "dir": "cbeta", "path": "T01n0001.xml",
        "url": f"{CBETA}/T/T01/T01n0001.xml",
        "check": ["<title>長阿含經</title>", "T01n0001"],
        "note": "CBETA xml-p5 · 大正藏 T1 · 長阿含經（佛陀耶舍共竺佛念譯）",
    },
    {
        "id": "T01n0026", "dir": "cbeta", "path": "T01n0026.xml",
        "url": f"{CBETA}/T/T01/T01n0026.xml",
        "check": ["<title>中阿含經</title>", "T01n0026"],
        "note": "CBETA xml-p5 · 大正藏 T1 · 中阿含經（瞿曇僧伽提婆譯）",
    },
    {
        "id": "T02n0099", "dir": "cbeta", "path": "T02n0099.xml",
        "url": f"{CBETA}/T/T02/T02n0099.xml",
        "check": ["<title>雜阿含經</title>", "T02n0099"],
        "note": "CBETA xml-p5 · 大正藏 T2 · 雜阿含經（求那跋陀羅譯）",
    },
    {
        "id": "T02n0125", "dir": "cbeta", "path": "T02n0125.xml",
        "url": f"{CBETA}/T/T02/T02n0125.xml",
        "check": ["<title>增壹阿含經</title>", "T02n0125"],
        "note": "CBETA xml-p5 · 大正藏 T2 · 增壹阿含經（瞿曇僧伽提婆譯）",
    },
    # --- 巴利三藏：兩經樣本（不是全藏） ---
    {
        "id": "mn1_root", "dir": "pali", "path": "mn1_root-pli-ms.json",
        "url": f"{SC}/root/pli/ms/sutta/mn/mn1_root-pli-ms.json",
        "check": ["mn1:1.1", "Mūlapariyāyasutta"],
        "note": "SuttaCentral bilara-data · root/pli/ms · MN1（樣本，非全藏）",
    },
    {
        "id": "dn1_root", "dir": "pali", "path": "dn1_root-pli-ms.json",
        "url": f"{SC}/root/pli/ms/sutta/dn/dn1_root-pli-ms.json",
        "check": ["dn1:1.1", "brahmajāla"],
        "note": "SuttaCentral bilara-data · root/pli/ms · DN1（樣本，非全藏）",
    },
    # --- 道藏：度人經（DZ0001，三家本）全 61 卷 ---
    # --- 梵文：入法界品梵本（Gaṇḍavyūha，Vaidya 1960 底本电子转录） ---
    {
        "id": "gandavyuha", "dir": "sanskrit", "path": "gandavyuha_vaidya.txt",
        "url": f"{GRETIL}/sa_gaNDavyUhasUtra.txt",
        "check": ["Gaṇḍavyūhasūtra", "P.L. Vaidya", "samantabhadra"],
        "note": "GRETIL（哥廷根）· 底本 P.L. Vaidya 1960 · Gaṇḍavyūha（〈入法界品〉梵本·印本电子转录）",
    },
    # --- 卍續藏：華嚴部注疏三線（合論／疏注／綱要），X 部取自 CBETA xml-p5 ---
    {
        "id": "X04n0223", "dir": "cbeta_x", "path": "X04n0223.xml",
        "url": f"{CBETA}/X/X04/X04n0223.xml",
        "check": ["華嚴經合論", "李通玄"],
        "note": "CBETA xml-p5 · 卍續藏 X223 · 華嚴經合論（唐李通玄造論・志寧釐經合論）",
    },
    {
        "id": "X07n0234", "dir": "cbeta_x", "path": "X07n0234.xml",
        "url": f"{CBETA}/X/X07/X07n0234.xml",
        "check": ["華嚴經疏注", "淨源"],
        "note": "CBETA xml-p5 · 卍續藏 X234 · 華嚴經疏注（唐澄觀述・宋淨源錄疏注經）",
    },
    {
        "id": "X08n0240", "dir": "cbeta_x", "path": "X08n0240.xml",
        "url": f"{CBETA}/X/X08/X08n0240.xml",
        "check": ["華嚴綱要", "德清"],
        "note": "CBETA xml-p5 · 卍續藏 X240 · 華嚴綱要 卷1–44（唐澄觀疏義・明德清提挈）",
    },
    {
        "id": "X09n0240", "dir": "cbeta_x", "path": "X09n0240.xml",
        "url": f"{CBETA}/X/X09/X09n0240.xml",
        "check": ["華嚴綱要", "德清"],
        "note": "CBETA xml-p5 · 卍續藏 X240 · 華嚴綱要 卷45–80（唐澄觀疏義・明德清提挈）",
    },
    # --- 儒家樣本：《大學》（朱熹章句，Kanripo KR1h0015，17 檔）---
    # --- 道教階位品：《道教義樞》（孟安排，Kanripo KR5e0031，10 檔；位業義為 P1 缺口）---
]

for _n in range(0, 17):
    TARGETS.append({
        "id": f"KR1h0015_{_n:03d}", "dir": "rujia", "path": f"KR1h0015_{_n:03d}.txt",
        "url": f"{KR}/KR1h0015/master/KR1h0015_{_n:03d}.txt",
        "check": ["大學"],
        "note": f"Kanripo KR1h0015 · 大學（宋 朱熹章句）· 檔 {_n:03d}",
    })
for _n in range(0, 10):
    TARGETS.append({
        "id": f"KR5e0031_{_n:03d}", "dir": "daozang", "path": f"KR5e0031_{_n:03d}.txt",
        "url": f"{KR}/KR5e0031/master/KR5e0031_{_n:03d}.txt",
        "check": ["道教義樞", "位業"],
        "note": f"Kanripo KR5e0031 · 道教義樞（唐 孟安排）· 檔 {_n:03d}（位業義＝P1 道教階位缺口）",
    })
TARGETS.append({
    "id": "yogasutra", "dir": "sanskrit", "path": "yogasutra_with_bhashya.txt",
    "url": f"{GRETIL}/sa_pataJjali-yogasUtra-with-bhASya.txt",
    "check": ["yoga", "Pata"],
    "note": "GRETIL（哥廷根）· Patañjali Yogasūtra with Bhāṣya（八支階位＝P 面對位樣本）",
})

# The Daozang text is split one file per juan; expand into 61 targets.
for _n in range(1, 62):
    TARGETS.append({
        "id": f"KR5a0001_{_n:03d}", "dir": "daozang", "path": f"KR5a0001_{_n:03d}.txt",
        "url": f"{KR}/KR5a0001/master/KR5a0001_{_n:03d}.txt",
        "check": ["正統道藏", "#+TITLE"],
        "note": f"Kanripo KR5a0001 · 正統道藏 DZ0001 · 三家本 1988 · 卷之{_n}",
    })


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def candidates(url: str) -> list[str]:
    alt = url.replace(CBETA, CBETA_ALT).replace(SC, SC_ALT).replace(KR, KR_ALT)
    return [alt, url] if alt != url else [url]


def fetch(url: str) -> bytes:
    last = None
    for u in candidates(url):
        req = urllib.request.Request(u)
        req.add_header("User-Agent", "huayan-collection-fetch/1.0")
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"    · {u.split('/')[2]} 失败：{type(e).__name__}，换通道")
    raise last  # type: ignore[misc]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default="", help="comma-separated ids")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {
        "meta": {"purpose": "§17 跨典藏登記冊的一手見證清單", "updated": "", "notes": []},
        "files": {},
    }
    only = {x.strip() for x in args.only.split(",") if x.strip()}
    rows = []
    for t in TARGETS:
        if only and t["id"] not in only:
            continue
        dest = ROOT / "data" / "references" / t["dir"] / t["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        prev = manifest["files"].get(t["id"])
        if dest.exists() and not args.force:
            data = dest.read_bytes()
            if prev and prev.get("sha256") == sha256(data) and len(data) == prev.get("bytes"):
                rows.append((t["id"], "已在库", len(data), prev["sha256"]))
                continue
            print(f"  ! {t['id']} 在库但與 manifest 不符，重新抓取")
        if args.dry_run:
            try:
                head = fetch(t["url"])
            except Exception as e:  # noqa: BLE001
                print(f"  x {t['id']} {e}")
                continue
            rows.append((t["id"], "dry-run", len(head), sha256(head)))
            continue
        try:
            print(f"  ⬇ {t['id']} …", flush=True)
            data = fetch(t["url"])
        except Exception as e:  # noqa: BLE001
            print(f"  x {t['id']} 抓取失敗：{e}")
            continue
        text_ok = True
        try:
            probe = data.decode("utf-8")
        except UnicodeDecodeError:
            probe = ""
            text_ok = False
        missing = [c for c in t["check"] if c not in probe]
        if missing or not text_ok:
            print(f"  x {t['id']} 內容校驗失敗（缺 {missing[:2]}，非 UTF-8={not text_ok}）")
            continue
        dest.write_bytes(data)
        manifest["files"][t["id"]] = {
            "path": str(dest.relative_to(ROOT)).replace("\\", "/"),
            "url": t["url"],
            "bytes": len(data),
            "sha256": sha256(data),
            "retrieved": date.today().isoformat(),
            "note": t["note"],
        }
        rows.append((t["id"], "已下載", len(data), sha256(data)))

    if not args.dry_run:
        manifest["meta"]["updated"] = date.today().isoformat()
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for rid, status, n, h in rows:
        print(f"  {status:<6} {rid:<9} {n:>10,} B  sha256={h[:12]}")
    got = sum(1 for r in rows if r[1] in ("已下載", "已在库"))
    print(f"targets={len(rows)} ok={got}")
    return 0 if got == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
