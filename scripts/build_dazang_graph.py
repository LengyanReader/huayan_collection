#!/usr/bin/env python3
"""Build a typed Huayan canon graph and render three deterministic views.

Graph layers:
  version  (T278 / T279 / T293 / Toh 44 / Sanskrit survivals)
  pin      (39 chapters of T279)
  tib      (45 chapters of Toh 44)
  text     (T280-T309 別生 / 眷屬, T293 treated as version)
  cluster  (12 content clusters + 藏文独有)
  commentary / work / canon-class (citation subgraph)

Views:
  1. spine      layered topological alignment (versions → pins → tib → texts)
  2. radial     cluster-gravity network (force layout, deterministic)
  3. citations  commentary → works / canon classes

Output: data/research/huayan_dazang_graph.json
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "research" / "dazang_mapping_verification.json"
TOC = ROOT / "data" / "alignment" / "tibetan-derge-toc.json"
OUT = ROOT / "data" / "research" / "huayan_dazang_graph.json"

INK = "#2b2b2b"
MUTED = "#6b6b6b"
LINE = "#d8d0c0"
PAPER = "#fbf8f1"
BROWN = "#8b5e34"
RED = "#b03a2e"
BLUE = "#2f5d7c"
GREEN = "#4f6f52"
GOLD = "#a87900"
PURPLE = "#7a6a9a"

CLUSTER_ORDER = [
    "初会六品", "名号·光明觉", "净行", "十住", "十地", "十定", "寿量",
    "佛不思议", "普贤行愿", "如来出现", "离世间", "入法界", "其余",
]
CLUSTER_PINS = {
    "初会六品": [1, 2, 3, 4, 5, 6],
    "名号·光明觉": [7, 9],
    "净行": [11],
    "十住": [15],
    "十地": [26],
    "十定": [27],
    "寿量": [31],
    "佛不思议": [33],
    "普贤行愿": [36],
    "如来出现": [37],
    "离世间": [38],
    "入法界": [39],
    "其余": [8, 10, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 32, 34, 35],
}
# article tables group 初会六品 inside 「其余」; the graph splits it for layout only.
CLUSTER_COLOR = {
    "初会六品": "#8c6a4a", "名号·光明觉": "#b06a4a", "净行": "#4f6f52",
    "十住": "#2f5d7c", "十地": "#8b5e34", "十定": "#7a6a9a", "寿量": "#a87900",
    "佛不思议": "#b03a2e", "普贤行愿": "#4a7a8c", "如来出现": "#6b8e6b",
    "离世间": "#9a6a8a", "入法界": "#3f6f8f", "其余": "#9a9a9a",
    "藏文独有": "#b03a2e",
}

MANUAL_PIN = {
    "T10n0296": [36], "T10n0297": [36], "T10n0299": [15],
    "T10n0300": [33], "T10n0301": [33], "T10n0302": [37],
    "T10n0303": [37], "T10n0304": [37], "T10n0305": [37],
    "T10n0306": [37], "T10n0307": [26], "T10n0308": [26],
    "T10n0309": [15],
}
SPECIAL_TIB = {"T10n0298": 32}

WORKS = [
    ("瑜伽师地论", 669), ("大般涅槃经", 585), ("大智度论", 538),
    ("成唯识论", 507), ("摄大乘论", 371),
]
CLASSES = [
    ("瑜伽部", 0.27), ("释经论部", 0.20), ("经集部", 0.09),
    ("涅槃部", 0.08), ("般若部", 0.05), ("毗昙部", 0.05),
]
COMMENTARIES = [
    ("T1732 搜玄记", "智俨", 95), ("T1733 探玄记", "法藏", 1580),
    ("T1735 华严经疏", "澄观", 1667), ("T1736 演义钞", "澄观", 4363),
]


def esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=10, fill=INK, anchor="start", weight="normal", rotate=None):
    r = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="\'Noto Serif SC\',\'Songti SC\',serif"{r}>{esc(s)}</text>')


def rect(x, y, w, h, fill="none", stroke=LINE, rx=3, sw=1, op=1):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')


def line(x1, y1, x2, y2, stroke=LINE, sw=1, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}" opacity="{op}"{d}/>')


def curve(x1, y1, x2, y2, stroke=LINE, sw=1, dash=None, op=0.8):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    mx = (x1 + x2) / 2
    return (f'<path d="M{x1:.1f},{y1:.1f} C{mx:.1f},{y1:.1f} {mx:.1f},{y2:.1f} {x2:.1f},{y2:.1f}" '
            f'fill="none" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"{d}/>')


def svg(w, h, title, desc, body):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-labelledby="t" '
            f'xmlns="http://www.w3.org/2000/svg" style="max-width:{w}px;margin:1.2rem auto;display:block">'
            f'<title>{esc(title)}</title><desc>{esc(desc)}</desc>'
            f'<rect width="{w}" height="{h}" fill="{PAPER}" rx="8"/>' + body + "</svg>")


def tib_for_pin(n: int) -> list[int]:
    if n <= 4:
        return [n]
    if n == 5:
        return [5, 6, 7, 8, 9]
    if n == 6:
        return [10]
    if 7 <= n <= 26:
        return [n + 5]
    return [n + 6]


def build_graph() -> dict:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    toc = json.loads(TOC.read_text(encoding="utf-8"))
    rows = data["mapping_60_80"]["rows"]
    nodes: list[dict] = []
    edges: list[dict] = []

    def node(i, typ, label, **kw):
        nodes.append({"id": i, "type": typ, "label": label, **kw})

    def edge(s, t, typ, grade="A", weight=1, **kw):
        edges.append({"source": s, "target": t, "type": typ, "grade": grade, "weight": weight, **kw})

    versions = [
        ("V:T278", "T278 晋译", "60 卷 · 34 品"),
        ("V:T279", "T279 唐译", "80 卷 · 39 品"),
        ("V:T293", "T293 四十华严", "40 卷 · 入法界"),
        ("V:Toh44", "Toh 44 藏译", "45 章 · 115 包"),
        ("V:Sanskrit", "梵本", "全经佚 · 四单品存"),
    ]
    for i, lab, sub in versions:
        node(i, "version", lab, sub=sub)

    for i, r in enumerate(rows, 1):
        node(f"P:{i}", "pin", f"{i} {r['p80']}", assembly=r["assembly"], p60=r["p60"])
        edge("V:T279", f"P:{i}", "contains")
        if r["p60"]:
            edge("V:T278", f"P:{i}", "contains_60", weight=1)
    edge("V:T293", "P:39", "contains")
    edge("V:T293", "P:36", "contains_part", grade="B")
    for p in (26, 31, 36, 39):
        edge("V:Sanskrit", f"P:{p}", "survives", grade="A/B")

    for j in range(1, len(toc["toc"]) + 1):
        node(f"T:{j}", "tib", f"藏{j}", vol=toc["toc"][j - 1].get("vol"))
        edge("V:Toh44", f"T:{j}", "contains")
    for i in range(1, 40):
        for j in tib_for_pin(i):
            edge(f"P:{i}", f"T:{j}", "parallel", grade="A")

    for name, pins in CLUSTER_PINS.items():
        node(f"C:{name}", "cluster", name, color=CLUSTER_COLOR[name], count=len(pins))
        for p in pins:
            edge(f"P:{p}", f"C:{name}", "belongs")
    node("C:藏文独有", "cluster", "藏文独有", color=CLUSTER_COLOR["藏文独有"], count=2)
    edge("T:11", "C:藏文独有", "unique")
    edge("T:32", "C:藏文独有", "unique")

    pin_cluster = {p: c for c, ps in CLUSTER_PINS.items() for p in ps}
    for x in data["catalog_32"]:
        t = x["taisho"]
        if t == "T10n0293":
            continue
        node(f"X:{t}", "text", f"{t.replace('T10n0', 'T')} {x['title_cbeta']}", juan=x["juan_cbeta"], cjk=x.get("cjk_body", x["cjk"]))
        pins = x["xref"].get("T279") or MANUAL_PIN.get(t, [])
        grade = "A" if x["xref"].get("T279") else "B/C"
        etype = "translation" if (x["xref"].get("T279") or t in ("T10n0296", "T10n0297")) else "related"
        for p in pins:
            edge(f"P:{p}", f"X:{t}", etype, grade=grade)
            edge(f"X:{t}", f"C:{pin_cluster[p]}", "belongs", grade=grade)
        if t in SPECIAL_TIB:
            edge(f"X:{t}", f"T:{SPECIAL_TIB[t]}", "related", grade="B")
            edge(f"X:{t}", "C:藏文独有", "belongs", grade="B")

    node("M:ALL", "commentary_hub", "四部注疏合计", value=7705)
    for name, person, n in COMMENTARIES:
        node(f"M:{name}", "commentary", name, person=person, value=n)
        edge(f"M:{name}", "M:ALL", "sums_to", weight=n, grade="B")
    for w, n in WORKS:
        node(f"W:{w}", "work", w, value=n)
        edge("M:ALL", f"W:{w}", "cites", weight=n, grade="B")
    for c, v in CLASSES:
        node(f"K:{c}", "canon_class", c, value=v)
        edge("M:ALL", f"K:{c}", "cites_class", weight=v, grade="B")

    stats = {
        "nodes": len(nodes),
        "edges": len(edges),
        "by_node": {k: sum(1 for n in nodes if n["type"] == k) for k in sorted({n["type"] for n in nodes})},
        "by_edge": {k: sum(1 for e in edges if e["type"] == k) for k in sorted({e["type"] for e in edges})},
    }
    return {"meta": {"source": "dazang_mapping_verification.json + tibetan-derge-toc.json", "access_date": data["meta"]["access_date"]}, "nodes": nodes, "edges": edges, "stats": stats}


def render_spine(g: dict) -> str:
    rows = [n for n in g["nodes"] if n["type"] == "pin"]
    rows.sort(key=lambda n: int(n["id"].split(":")[1]))
    tibs = sorted([n for n in g["nodes"] if n["type"] == "tib"], key=lambda n: int(n["id"].split(":")[1]))
    texts = sorted([n for n in g["nodes"] if n["type"] == "text"], key=lambda n: n["id"])
    W, H = 1120, 1010
    top, gap = 64, 23
    ypin = {int(n["id"].split(":")[1]): top + i * gap for i, n in enumerate(rows)}
    ytib = {int(n["id"].split(":")[1]): top + i * (23 * 39 / 45) for i, n in enumerate(tibs)}
    ytxt = {n["id"]: top + i * 31 for i, n in enumerate(texts)}
    b = []
    b.append(txt(30, 30, "图7　经群分层拓扑：版本 → 39 品 → 45 藏章 → 30 部异译", 15, INK, weight="bold"))
    b.append(txt(30, 48, "实线＝containment／parallel／translation；虚线＝存疑或特例。色带＝十二簇；红圈＝藏文独有二章；红叉＝六十无十定。", 10, MUTED))

    # cluster bands
    for c, pins in CLUSTER_PINS.items():
        ys = [ypin[p] for p in pins if p in ypin]
        if not ys:
            continue
        y0, y1 = min(ys) - 8, max(ys) + 8
        b.append(rect(332, y0, 18, max(y1 - y0, 14), fill=CLUSTER_COLOR[c], stroke="none", op=0.55, rx=2))
        if len(pins) <= 2:
            b.append(txt(358, (y0 + y1) / 2 + 3, c, 8, CLUSTER_COLOR[c], rotate=-90))
        else:
            b.append(txt(358, (y0 + y1) / 2 + 3, f"{c}（{len(pins)}）", 8, CLUSTER_COLOR[c], rotate=-90))

    # version boxes + brackets
    vpos = {"V:T279": 110, "V:T278": 220, "V:T293": 330, "V:Toh44": 440, "V:Sanskrit": 550}
    for v, y in vpos.items():
        n = next(x for x in g["nodes"] if x["id"] == v)
        b.append(rect(30, y - 22, 170, 44, fill="#fff", stroke=BROWN if v != "V:Sanskrit" else RED, sw=1.2))
        b.append(txt(38, y - 6, n["label"], 10, INK, weight="bold"))
        b.append(txt(38, y + 9, n["sub"], 8, MUTED))
    # containment brackets
    def bracket(ybox, first, last, color, label, dash=None):
        b.append(line(200, ybox, 228, ybox, color, 1.1))
        b.append(line(228, ypin[first], 228, ypin[last], color, 1.4, dash=dash))
        for p in (first, last):
            b.append(line(228, ypin[p], 322, ypin[p], color, 0.8, dash=dash))
        b.append(txt(232, (ypin[first] + ypin[last]) / 2 - 4, label, 8, color))
    bracket(110, 1, 39, BROWN, "39 品")
    bracket(220, 1, 39, BLUE, "34 品／60 卷（十定缺）", dash="4 3")
    bracket(330, 39, 39, GREEN, "入法界")
    bracket(440, 1, 39, GREEN, "45 章")
    for p in (26, 31, 36, 39):
        b.append(line(200, 550, 228, 550, RED, 0.9, dash="2 3"))
        b.append(line(228, 550, 228, ypin[p], RED, 0.7, dash="2 3"))
        b.append(line(228, ypin[p], 322, ypin[p], RED, 0.8, dash="2 3"))
        b.append(f'<circle cx="228" cy="{ypin[p]:.1f}" r="2.5" fill="{RED}"/>')

    # pins
    for n in rows:
        p = int(n["id"].split(":")[1])
        y = ypin[p]
        b.append(f'<circle cx="330" cy="{y:.1f}" r="3.2" fill="{BROWN}"/>')
        b.append(txt(324, y + 3, f"{p}", 7, MUTED, anchor="end"))
        if p in (1, 6, 26, 27, 39):
            b.append(txt(312, y - 4, n["label"][:18], 7, INK, anchor="end"))
    # ten-ding gap marker
    b.append(f'<circle cx="330" cy="{ypin[27]:.1f}" r="7" fill="none" stroke="{RED}" stroke-width="1.1"/>')
    b.append(txt(340, ypin[27] + 3, "六十无", 7, RED))

    # tib nodes and parallel edges
    for i in range(1, 40):
        for j in tib_for_pin(i):
            b.append(curve(333, ypin[i], 552, ytib[j], "#b9b2a4", 0.7, op=0.55))
    for n in tibs:
        j = int(n["id"].split(":")[1])
        y = ytib[j]
        col = RED if j in (11, 32) else GREEN
        b.append(f'<circle cx="556" cy="{y:.1f}" r="3" fill="{col}"/>')
        b.append(txt(562, y + 2, str(j), 6, MUTED))
        if j in (11, 32):
            b.append(f'<circle cx="556" cy="{y:.1f}" r="8" fill="none" stroke="{RED}" stroke-width="1.2"/>')
            b.append(txt(570, y + 2, "汉无", 7, RED, weight="bold"))

    # text nodes and translation edges
    pin_to_y = {int(n["id"].split(":")[1]): ypin[int(n["id"].split(":")[1])] for n in rows}
    for n in texts:
        y = ytxt[n["id"]]
        edges = [e for e in g["edges"] if e["target"] == n["id"] and e["type"] in ("translation", "related")]
        grade = edges[0]["grade"] if edges else "B/C"
        col = RED if grade == "B/C" else "#b5651d"
        for e in edges:
            p = int(e["source"].split(":")[1])
            b.append(curve(333, pin_to_y[p], 820, y, col, 0.8, dash="3 3" if grade == "B/C" else None, op=0.65))
        b.append(f'<circle cx="824" cy="{y:.1f}" r="2.6" fill="{col}"/>')
        b.append(txt(830, y + 3, n["label"][:34], 7.2, INK))
    # unique tib → T298
    b.append(curve(560, ytib[32], 820, ytxt["X:T10n0298"], RED, 0.9, dash="3 3"))

    # legend
    ly = 930
    legend = [("contains / parallel / translation", BROWN), ("related（B/C，虚线）", RED), ("藏文独有", RED)]
    for i, (lab, col) in enumerate(legend):
        b.append(line(30 + i * 260, ly, 70 + i * 260, ly, col, 1.3, dash="3 3" if i else None))
        b.append(txt(76 + i * 260, ly + 3, lab, 8, MUTED))
    b.append(txt(30, 972, "纵轴按品次／章次顺序；T278 的 34 品与 T279 的 39 品为「同一行」对齐，不是一一编号。", 8, MUTED))
    b.append(txt(30, 988, "T293 只含入法界（品39）与卷40 普贤行（挂品36）；梵本四项存于品26/31/36/39。", 8, MUTED))
    return svg(W, H, "图7 经群分层拓扑", "版本、品、藏章、异译的分层对应网络", "".join(b))


def render_radial(g: dict) -> str:
    nodes = {n["id"]: n for n in g["nodes"]}
    clusters = [n for n in g["nodes"] if n["type"] == "cluster"]
    pins = sorted([n for n in g["nodes"] if n["type"] == "pin"], key=lambda n: int(n["id"].split(":")[1]))
    texts = sorted([n for n in g["nodes"] if n["type"] == "text"], key=lambda n: n["id"])

    # deterministic initial positions: clusters on a circle, pins in their sector
    pos: dict[str, list[float]] = {}
    cx, cy, R = 470, 470, 900
    ncl = len(clusters)
    for i, c in enumerate(clusters):
        ang = 2 * math.pi * i / ncl - math.pi / 2
        pos[c["id"]] = [cx + 120 * math.cos(ang), cy + 120 * math.sin(ang)]
    for i, p in enumerate(pins):
        num = int(p["id"].split(":")[1])
        cl = next(c["id"] for c in clusters if num in CLUSTER_PINS.get(c["label"], []))
        ci = [c["id"] for c in clusters].index(cl)
        sector = 2 * math.pi / ncl
        local = [q for q in CLUSTER_PINS[nodes[cl]["label"]]]
        k = local.index(num)
        ang = 2 * math.pi * ci / ncl - math.pi / 2 + sector * (k + 0.5) / max(len(local), 1) * 0.8 - sector * 0.4
        r = 250 + (k % 2) * 38
        pos[p["id"]] = [cx + r * math.cos(ang), cy + r * math.sin(ang)]
    anchor = {}
    for t in texts:
        anchor[t["id"]] = next((e["source"] for e in g["edges"] if e["target"] == t["id"] and e["type"] in ("translation", "related") and e["source"].startswith("P:")), None)
    groups: dict[str, list[str]] = {}
    for t in texts:
        groups.setdefault(anchor[t["id"]] or "none", []).append(t["id"])
    for key, members in groups.items():
        if key == "none":
            for i, tid in enumerate(members):
                ang = -1.9 if tid == "X:T10n0298" else 2 * math.pi * i / max(len(members), 1)
                pos[tid] = [cx + 385 * math.cos(ang), cy + 385 * math.sin(ang)]
            continue
        base = pos[key]
        ang0 = math.atan2(base[1] - cy, base[0] - cx)
        for j, tid in enumerate(members):
            ang = ang0 + (j - (len(members) - 1) / 2) * 0.11
            pos[tid] = [cx + 375 * math.cos(ang), cy + 375 * math.sin(ang)]

    # force relaxation: clusters anchored, pins/texts movable
    ids = list(pos)
    fixed = {c["id"] for c in clusters}
    k = 160.0
    for it in range(220):
        temp = max(1.0, 14.0 * (1 - it / 220))
        disp = {i: [0.0, 0.0] for i in ids}
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                ia, ib = ids[a], ids[b]
                dx = pos[ia][0] - pos[ib][0]
                dy = pos[ia][1] - pos[ib][1]
                d2 = dx * dx + dy * dy + 1
                if d2 > 90000:
                    continue
                f = 1.9 * k * k / d2
                d = math.sqrt(d2)
                ux, uy = dx / d, dy / d
                disp[ia][0] += ux * f; disp[ia][1] += uy * f
                disp[ib][0] -= ux * f; disp[ib][1] -= uy * f
        for e in g["edges"]:
            if e["type"] not in ("belongs", "translation", "related"):
                continue
            a, bb = e["source"], e["target"]
            if a not in pos or bb not in pos:
                continue
            dx = pos[a][0] - pos[bb][0]; dy = pos[a][1] - pos[bb][1]
            d = math.sqrt(dx * dx + dy * dy) + 0.01
            f = d * d / k
            ux, uy = dx / d, dy / d
            disp[a][0] -= ux * f * 0.08; disp[a][1] -= uy * f * 0.08
            disp[bb][0] += ux * f * 0.08; disp[bb][1] += uy * f * 0.08
        for i in ids:
            if i in fixed:
                continue
            dx, dy = disp[i]
            d = math.sqrt(dx * dx + dy * dy) + 0.01
            pos[i][0] += dx / d * min(d, temp)
            pos[i][1] += dy / d * min(d, temp)
            pos[i][0] = min(max(pos[i][0], 70), 870)
            pos[i][1] = min(max(pos[i][1], 80), 830)

    for _ in range(60):
        moved = False
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                ia, ib = ids[a], ids[b]
                dx = pos[ia][0] - pos[ib][0]
                dy = pos[ia][1] - pos[ib][1]
                d = math.hypot(dx, dy)
                mind = 16 if (ia in fixed or ib in fixed) else 12.5
                if d < mind:
                    moved = True
                    ux, uy = (dx / d, dy / d) if d > 0.01 else (1.0, 0.0)
                    push = (mind - d) / 2
                    if ia not in fixed:
                        pos[ia][0] += ux * push; pos[ia][1] += uy * push
                    if ib not in fixed:
                        pos[ib][0] -= ux * push; pos[ib][1] -= uy * push
        if not moved:
            break
        for i in ids:
            if i in fixed:
                continue
            pos[i][0] = min(max(pos[i][0], 70), 870)
            pos[i][1] = min(max(pos[i][1], 80), 830)

    b = []
    b.append(txt(24, 28, "图8　簇—品—异译关系网：簇为引力中心，品与异译为卫星", 15, INK, weight="bold"))
    b.append(txt(24, 46, "节点 82：14 布局簇（12 内容簇＋初会六品＋藏文独有）＋39 品＋29 异译；边＝belongs／translation／related。力导向布局为确定性（无随机）。", 9.5, MUTED))
    # cluster halo + edges first
    for c in clusters:
        x, y = pos[c["id"]]
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="58" fill="{CLUSTER_COLOR[c["label"]]}" opacity="0.07"/>')
    for e in g["edges"]:
        if e["type"] not in ("belongs", "translation", "related"):
            continue
        a, bb = e["source"], e["target"]
        if a not in pos or bb not in pos:
            continue
        x1, y1 = pos[a]; x2, y2 = pos[bb]
        if a.startswith("C:") or bb.startswith("C:"):
            b.append(line(x1, y1, x2, y2, CLUSTER_COLOR[nodes[a if a.startswith("C:") else bb]["label"]], 0.5, op=0.45))
        else:
            b.append(line(x1, y1, x2, y2, RED if e["type"] == "related" else "#b5651d", 0.7, dash="3 3" if e["type"] == "related" else None, op=0.55))
    for c in clusters:
        x, y = pos[c["id"]]
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{CLUSTER_COLOR[c["label"]]}" stroke="#fff" stroke-width="1"/>')
        b.append(txt(x, y + 3, str(c["count"]), 8, "#fff", anchor="middle", weight="bold"))
        lx, ly = x, y - 18
        b.append(txt(lx, ly, c["label"], 8.5, CLUSTER_COLOR[c["label"]], anchor="middle", weight="bold"))
    for p in pins:
        x, y = pos[p["id"]]
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.1" fill="{BROWN}" opacity="0.9"/>')
        b.append(txt(x + 4, y + 2, p["id"].split(":")[1], 6, MUTED))
    for t in texts:
        x, y = pos[t["id"]]
        col = BLUE if t["id"] != "X:T10n0298" else RED
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{col}"/>')
        b.append(txt(x + 4, y + 2, t["label"].split(" ")[0], 6.2, MUTED))
    b.append(txt(24, 860, "读图：越靠近簇心的品，越属于该簇；外侧为单行异译。虚线＝B/C 级关联（待梵藏对读）。", 9, MUTED))
    return svg(940, 880, "图8 簇—品—异译关系网", "以十二簇为引力中心的关系网络", "".join(b))


def render_citations() -> str:
    W, H = 940, 600
    b = []
    b.append(txt(24, 28, "图9　注疏中的大藏：四部注疏 → 被引经论／部类", 15, INK, weight="bold"))
    b.append(txt(24, 46, "种子报告数据（B）：7,705 次书名号引用；本图只展示前五被引与六部类，不是全集。", 9.5, MUTED))
    cx, cy = 470, 300
    b.append(f'<circle cx="{cx}" cy="{cy}" r="44" fill="#fff" stroke="{BROWN}" stroke-width="1.4"/>')
    b.append(txt(cx, cy - 4, "四部注疏", 10, INK, anchor="middle", weight="bold"))
    b.append(txt(cx, cy + 12, "7,705", 13, BROWN, anchor="middle", weight="bold"))
    # commentaries left
    ys = [90, 190, 290, 390]
    for (name, person, n), y in zip(COMMENTARIES, ys):
        b.append(rect(30, y - 24, 170, 48, fill="#fff", stroke=BLUE, sw=1.1))
        b.append(txt(38, y - 8, name, 9, INK, weight="bold"))
        b.append(txt(38, y + 7, f"{person} · {n:,}", 8, MUTED))
        b.append(curve(200, y, cx - 44, cy, BLUE, max(0.6, n / 2200), op=0.55))
    # works right
    wys = [80, 160, 240, 320, 400]
    for (w, n), y in zip(WORKS, wys):
        b.append(rect(730, y - 20, 180, 40, fill="#fff", stroke=GREEN, sw=1.1))
        b.append(txt(738, y - 5, w, 9, INK, weight="bold"))
        b.append(txt(738, y + 9, f"{n:,}", 8, MUTED))
        b.append(curve(cx + 44, cy, 730, y, GREEN, max(0.7, n / 220), op=0.55))
    # classes bottom
    cxs = [120, 270, 420, 570, 720, 860]
    for (c, v), x in zip(CLASSES, cxs):
        b.append(rect(x - 58, 500, 116, 38, fill="#fff", stroke=GOLD, sw=1))
        b.append(txt(x, 515, c, 8.5, INK, anchor="middle", weight="bold"))
        b.append(txt(x, 530, f"{v:.0%}", 8, MUTED, anchor="middle"))
        b.append(curve(cx, cy + 44, x, 500, GOLD, max(0.7, v * 20), op=0.55))
    b.append(txt(24, 570, "注：部类百分比为四部注疏的平均占比近似值（种子 B）；「瑜伽部 24–31%」取中值 27%。", 8.5, RED))
    b.append(txt(24, 586, "读法：线宽＝引用量或占比；蓝色＝注疏自身体量；绿色＝被引经论；金色＝被引部类。", 8.5, MUTED))
    return svg(W, H, "图9 注疏引用网络", "四部注疏与被引经论、部类的二部图", "".join(b))


def main() -> int:
    g = build_graph()
    OUT.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(g["stats"], ensure_ascii=False, indent=2))
    print(f"written {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())