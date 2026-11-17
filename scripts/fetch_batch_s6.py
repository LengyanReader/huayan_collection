#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批次取文：金光明两本（T16n0663/0664）＋清凉传三书（T51n2098/99/2100）。

入库规则照 `data/references/README.md`：一手文本底本入 `data/references/cbeta/`，
登记 `external_manifest.json`（url+bytes+sha256+retrieved+note）。幂等。
"""
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://raw.githubusercontent.com/cbeta-org/xml-p5/master"
MANIFEST = ROOT / "data" / "references" / "external_manifest.json"

TARGETS = [
    ("T16n0663", "T/T16/T16n0663.xml", "data/references/cbeta/T16n0663.xml",
     "CBETA xml-p5 · T16n0663 · 金光明經（北涼曇無讖譯，四卷）"),
    ("T16n0664", "T/T16/T16n0664.xml", "data/references/cbeta/T16n0664.xml",
     "CBETA xml-p5 · T16n0664 · 合部金光明經（隋釋寶貴合，八卷）"),
    ("T51n2098", "T/T51/T51n2098.xml", "data/references/cbeta/T51n2098.xml",
     "CBETA xml-p5 · T51n2098 · 古清涼傳（唐慧祥，二卷）"),
    ("T51n2099", "T/T51/T51n2099.xml", "data/references/cbeta/T51n2099.xml",
     "CBETA xml-p5 · T51n2099 · 廣清涼傳（宋延一，三卷）"),
    ("T51n2100", "T/T51/T51n2100.xml", "data/references/cbeta/T51n2100.xml",
     "CBETA xml-p5 · T51n2100 · 續清涼傳（宋張商英，二卷）"),
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = man.setdefault("files", {})
    for cid, rel, dst, note in TARGETS:
        p = ROOT / dst
        if p.exists():
            print("exists", dst)
            continue
        try:
            req = urllib.request.Request(f"{BASE}/{rel}",
                                         headers={"User-Agent": "huayan-fetch/1.0"})
            raw = urllib.request.urlopen(req, timeout=180).read()
        except Exception as e:  # noqa: BLE001
            print("FAIL", rel, str(e)[:120])
            continue
        p.write_bytes(raw)
        files[cid] = {"path": dst, "url": f"{BASE}/{rel}", "bytes": len(raw),
                      "sha256": sha256(raw), "retrieved": "2026-11-17", "note": note}
        print("OK", dst, len(raw), "bytes")
    man["meta"]["updated"] = "2026-11-17"
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")
    print("manifest entries now", len(files))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
