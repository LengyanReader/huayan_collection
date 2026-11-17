#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批次取文（s7）：P 面三格＋D4＋C 面扩样＋D5 补样。

  CBETA  T45n1866 華嚴一乘教義分齊章（法藏）      → D4 教义对立
  CBETA  T19n1020 字輪瑜伽儀軌（不空）             → P2 仪轨化
  CBETA  T19n1021 華嚴經心陀羅尼（實叉難陀）       → P3 陀罗尼化
  Kanripo KR5e0040 無上祕要（存 68 檔）            → D5 内核共享第二部道经
  Kanripo KR5d0019 周易參同契分章通真義（彭曉）    → C 面扩样·道教丹道
  GRETIL  Pātañjala-yoga-sūtra（corpustei 明文）   → C 面扩样·印度瑜伽

入库规则照 `data/references/README.md`：登记 `external_manifest.json`。幂等。
"""
import hashlib
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_CBETA = "https://raw.githubusercontent.com/cbeta-org/xml-p5/master"
BASE_KR = "https://raw.githubusercontent.com/kanripo"
MANIFEST = ROOT / "data" / "references" / "external_manifest.json"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fetch(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "huayan-fetch/1.0"})
    return urllib.request.urlopen(req, timeout=timeout).read()


JOBS = [
    # (id, url, local relative path)
    ("T45n1866", f"{BASE_CBETA}/T/T45/T45n1866.xml", "data/references/cbeta/T45n1866.xml"),
    ("T19n1020", f"{BASE_CBETA}/T/T19/T19n1020.xml", "data/references/cbeta/T19n1020.xml"),
    ("T19n1021", f"{BASE_CBETA}/T/T19/T19n1021.xml", "data/references/cbeta/T19n1021.xml"),
]
# GRETIL yoga（明文）
JOBS.append(("yogasutra",
             "https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations"
             "/plaintext/sa_pataJjali-yogasUtra.txt",
             "data/references/sanskrit/yoga_sutra.txt"))


def main() -> int:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = man.setdefault("files", {})
    ok = fail = 0

    for cid, url, dst in JOBS:
        p = ROOT / dst
        if p.exists():
            print("exists", cid)
            continue
        try:
            raw = fetch(url)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
            files[cid] = {"path": dst, "url": url, "bytes": len(raw),
                          "sha256": sha256(raw), "retrieved": "2026-11-18",
                          "note": f"s7 批次 · {cid}"}
            ok += 1
            print("OK", cid, f"{len(raw):,}B")
        except Exception as e:  # noqa: BLE001
            fail += 1
            print("FAIL", cid, str(e)[:100])

    # Kanripo 多档：先列目录再逐档取
    for cid, repo, dst_dir, note in (
        ("KR5e0040", "KR5e0040", "data/references/daozang_wushang", "無上祕要（Kanripo KR5e0040，存 68 檔）"),
        ("KR5d0019", "KR5d0019", "data/references/daozang_cantongqi", "周易參同契分章通真義（漢彭曉，Kanripo KR5d0019）"),
    ):
        d = ROOT / dst_dir
        d.mkdir(parents=True, exist_ok=True)
        import urllib.request as u
        import json as j
        api = f"https://api.github.com/repos/kanripo/{repo}/contents"
        names = [x["name"] for x in j.loads(
            u.Request(api, headers={"User-Agent": "huayan-fetch/1.0"})
            and u.urlopen(u.Request(api, headers={"User-Agent": "huayan-fetch/1.0"}), timeout=60).read())
            if x["name"].endswith(".txt")]
        for name in sorted(names):
            p = d / name
            if p.exists():
                continue
            url = f"{BASE_KR}/{repo}/master/{name}"
            try:
                raw = fetch(url)
                p.write_bytes(raw)
                key = f"{cid}_{name[:-4]}"
                files[key] = {"path": f"{dst_dir}/{name}", "url": url,
                              "bytes": len(raw), "sha256": sha256(raw),
                              "retrieved": "2026-11-18", "note": note}
                ok += 1
                time.sleep(0.3)
            except Exception as e:  # noqa: BLE001
                fail += 1
                print("FAIL", name, str(e)[:80])
        print(f"{cid}: {len(names)} files done ({dst_dir})")

    man["meta"]["updated"] = "2026-11-18"
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")
    print(f"ok={ok} fail={fail}; manifest={len(files)}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
