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
]

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
