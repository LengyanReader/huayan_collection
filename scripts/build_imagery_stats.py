#!/usr/bin/env python3
"""Aggregate the culture-line imagery registries (data/imagery/*_imagery.yaml)
into R-face (接受·传播) statistics for the canon-mapping article.

The per-品 registries are maintained by the 文化资产 line; formats vary slightly
across batches, so parsing is tolerant: unparseable files are counted and
reported, never silently dropped.

Usage:
  python scripts/build_imagery_stats.py
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "imagery"
OUT = ROOT / "data" / "research" / "imagery_stats.json"


def main() -> int:
    files = sorted(SRC.glob("*_imagery.yaml"))
    per_file, items, unparseable = [], [], []
    cls_total: dict[str, int] = {}
    for f in files:
        try:
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            unparseable.append({"file": f.name, "error": str(e)[:120]})
            continue
        if not isinstance(d, dict):
            unparseable.append({"file": f.name, "error": "not a mapping"})
            continue
        its = d.get("items", []) or []
        cls_file: dict[str, int] = {}
        for it in its:
            no = str(it.get("img_no", "?"))
            cls = no.split("-")[0] if "-" in no else "?"
            cls_file[cls] = cls_file.get(cls, 0) + 1
            cls_total[cls] = cls_total.get(cls, 0) + 1
        per_file.append({
            "file": f.name,
            "title": d.get("title_zh", ""),
            "items": len(its),
            "class": cls_file,
            "boundary": d.get("boundary_principle", ""),
        })
        items.extend(its)
    result = {
        "meta": {
            "date": date.today().isoformat(),
            "source": "data/imagery/*_imagery.yaml（文化资产线登记册）",
            "note": "聚合口径：files=登记册文件数，items=登记条目数；品覆盖取 img_no 前缀"
                    "（册按品组织）；格式不统一的文件如实计入 unparseable。",
        },
        "files_total": len(files),
        "parsed": len(per_file),
        "unparseable": unparseable,
        "items_total": len(items),
        "pins_covered": len(cls_total),
        "per_file": per_file,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"files {result['files_total']} parsed {result['parsed']} "
          f"unparseable {len(unparseable)} items {result['items_total']} "
          f"pins_covered {result['pins_covered']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
