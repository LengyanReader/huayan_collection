#!/usr/bin/env python3
"""
F.2 断代底图数据受控下载器（B＋A 路线·用户 2026-10-30 R4 显式授权）

入库两层（均只下载点名文件·CHGIS 依其 license 禁再分发·恒外链不入库）：
  A 层  aourednik/historical-basemaps（GPL-3.0·独立集合＋LICENSE 随仓）
        world_{500,600,700,800,900}.geojson —— 百年一份世界政体快照
  B 层  Natural Earth（public domain）
        ne_110m_land / ne_110m_coastline / ne_110m_admin_0_countries —— 现代物理/政区底图

行为：目标文件已存在且 sha256 与 manifest 一致 → 跳过；否则下载并刷新
     data/geo/manifest.yaml（url·license·访问日期·sha256·bytes）。
幂等·可复核：python scripts/f2_fetch_geo.py [--force]
"""

import hashlib
import sys
import urllib.request
from datetime import date
from pathlib import Path

import yaml

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
GEO = ROOT / "data" / "geo"
UA = {"User-Agent": "huayan-collection F.2 controlled fetch (non-commercial)"}

AOUR = "https://raw.githubusercontent.com/aourednik/historical-basemaps/master"
NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson"

FILES = [
    # (相对路径, url, license, note)
    ("historical-basemaps/LICENSE", f"{AOUR}/LICENSE",
     "GPL-3.0（数据集合独立保留 GPL 声明·不传染 MIT 代码组件）", "随仓 GPL 全文"),
    ("historical-basemaps/index.json", f"{AOUR}/index.json",
     "GPL-3.0", "年份↔文件↔政体名索引（离线核对用）"),
] + [
    (f"historical-basemaps/world_{y}.geojson", f"{AOUR}/geojson/world_{y}.geojson",
     "GPL-3.0", f"{y} 年世界政体快照·示意底图〔学术精度待核〕")
    for y in (500, 600, 700, 800, 900)
] + [
    (f"natural_earth/{n}.geojson", f"{NE}/{n}.geojson",
     "Public Domain", pd_note)
    for n, pd_note in (
        ("ne_110m_land", "110m 陆地多边形（现代海岸线）"),
        ("ne_110m_coastline", "110m 海岸线（描绘层）"),
        ("ne_110m_admin_0_countries", "110m 现代国界（方位参考·非历史断代）"),
    )
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    force = "--force" in sys.argv
    GEO.mkdir(parents=True, exist_ok=True)
    man_path = GEO / "manifest.yaml"
    old = {}
    if man_path.exists():
        old = {e["file"]: e for e in (yaml.safe_load(man_path.read_text(encoding="utf-8")) or {}).get("layers", [])}

    entries, changed = [], []
    for rel, url, lic, note in FILES:
        p = GEO / rel
        if p.exists() and not force and old.get(rel, {}).get("sha256") == sha256(p):
            e = dict(old[rel])
        elif p.exists() and not force and rel not in old and p.stat().st_size > 0:
            # manifest 缺席但文件系本轮刚取回：重计算纳采，避免断链后整批重拉
            e = {"file": rel, "url": url, "license": lic, "note": note,
                 "accessed": date.today().isoformat(),
                 "sha256": sha256(p), "bytes": p.stat().st_size}
            entries.append(e)
            print(f"RECOMP {e['bytes']:>9,} B  sha256:{e['sha256'][:12]}  {rel}")
            continue
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r, open(p, "wb") as f:
                f.write(r.read())
            e = {
                "file": rel, "url": url, "license": lic, "note": note,
                "accessed": date.today().isoformat(),
                "sha256": sha256(p), "bytes": p.stat().st_size,
            }
            changed.append(rel)
        entries.append(e)
        print(f"{'FRESH' if rel in changed else 'HELD '} {e['bytes']:>9,} B  sha256:{e['sha256'][:12]}  {rel}")

    man_path.write_text(
        yaml.safe_dump({"generated": date.today().isoformat(), "layers": entries,
                        "policy": "CHGIS=禁再分发·仅外链（Harvard Dataverse）；OHM=ODbL 后置；"
                                  "aourednik=GPL-3.0 独立集合；Natural Earth=PD。"},
                       allow_unicode=True, sort_keys=False),
        encoding="utf-8")
    print(f"manifest -> {man_path}  ({len(changed)} fresh / {len(entries)} total)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
