#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三幅系统总览图（图14–16）的 SVG 生成函数。

  图14 七面×三十四算子覆盖热力格（挂 §17.4 审计后）
  图15 十二典×華嚴对应径向图（挂 §17.48 后）
  图16 复现与验证管线（挂 §16.1）

数据全部来自已入库 JSON：relation_ontology／substantive_correspondence／
c_deepen／external_manifest／门禁计数。此模块只被 build_dazang_article.py
导入（提供 fig_coverage / fig_radial / fig_pipeline 三个函数）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = "#2b2b2b"
MUTED = "#666666"
PAPER = "#fbf8f1"
GREEN = "#4f6f52"
GOLD = "#b8860b"
BLUE = "#2f5d7c"
BROWN = "#8b5e34"
RED = "#b03a2e"

FACET_NAME = {"T": "文本关系", "M": "文本史", "S": "社会史", "D": "教义",
              "P": "修行实践", "C": "跨典藏", "R": "接受传播"}
STATUS_FILL = {"done": "#cfe3cf", "partial": "#f3e3bd", "none": "#e8cfcf"}
STATUS_LABEL = {"done": "已做", "partial": "部分", "none": "未做"}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace("|", "／"))


def svg(w, h, title, desc, body):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-labelledby="t" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'style="max-width:{w}px;margin:1.2rem auto;display:block">'
            f'<title>{esc(title)}</title><desc>{esc(desc)}</desc>'
            f'<rect width="{w}" height="{h}" fill="{PAPER}" rx="8"/>' + body + "</svg>")


def txt(x, y, s, size=12, fill=INK, anchor="start", weight="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" '
            f'font-family="\'Noto Serif SC\',\'Songti SC\',serif">{esc(s)}</text>')


def fig_coverage(ontology):
    """图14 七面×三十四算子覆盖热力格。"""
    ops = ontology["operators"]
    facets = {}
    for o in ops:
        facets.setdefault(o["facet"], []).append(o)
    order = ["T", "M", "S", "D", "P", "C", "R"]
    cell_w, cell_h, x0, y0 = 52, 26, 96, 46
    b = [txt(x0 - 8, 24, "图例：", 11, MUTED)]
    for i, st in enumerate(("done", "partial", "none")):
        x = x0 - 8 + i * 96
        b.append(f'<rect x="{x}" y="14" width="26" height="14" rx="3" '
                 f'fill="{STATUS_FILL[st]}" stroke="#999" sw="0.5"/>')
        b.append(txt(x + 32, 25, STATUS_LABEL[st], 11, MUTED))
    for r, f in enumerate(order):
        group = facets.get(f, [])
        y = y0 + r * cell_h
        b.append(txt(6, y + 17, f"{f} {FACET_NAME[f]}", 11, BROWN, weight="bold"))
        for c, o in enumerate(group):
            x = x0 + c * cell_w
            fill = STATUS_FILL[o["status"]]
            b.append(f'<rect x="{x}" y="{y}" width="{cell_w - 6}" height="{cell_h - 6}" '
                     f'rx="4" fill="{fill}" stroke="#a09478" stroke-width="0.6"/>')
            b.append(txt(x + (cell_w - 6) / 2, y + 12, o["id"], 9.5, INK,
                         anchor="middle", weight="bold"))
            zh = o.get("zh", "")
            b.append(txt(x + (cell_w - 6) / 2, y + 21.5, zh[:5], 7.5, MUTED,
                         anchor="middle"))
    w = x0 + max(len(g) for g in facets.values()) * cell_w + 16
    h = y0 + len(order) * cell_h + 34
    b.append(txt(8, h - 12, "色块＝算子状态（绿 已做／黄 部分／红 未做）；格子内为算子号与名称。"
                 "数据由 relation_ontology.json 生成，手改无效。", 10, MUTED))
    return svg(w, h, "图15　七面×三十四算子覆盖热力格",
               "七面各算子的实测状态总览：绿已做、黄部分、红未做", "".join(b))


def fig_radial(groups_all):
    """图15 十二典×華嚴对应径向图。groups_all＝[(名称, 条数, 方向类), ...]"""
    cx, cy, r = 340, 250, 170
    n = len(groups_all)
    b = [f'<circle cx="{cx}" cy="{cy}" r="64" fill="#fff" stroke="{BROWN}" stroke-width="2"/>',
         txt(cx, cy - 6, "華嚴", 16, BROWN, anchor="middle", weight="bold"),
         txt(cx, cy + 16, "T279 为坐标", 10, MUTED, anchor="middle")]
    for i, (name, cnt, kind) in enumerate(groups_all):
        ang = -90 + i * (360 / n)
        x = cx + r * 0.86 * __import__("math").cos(ang * 3.1415926 / 180)
        y = cy + r * 0.86 * __import__("math").sin(ang * 3.1415926 / 180)
        color = RED if kind == "移植" else BLUE
        mx = cx + r * 0.5 * __import__("math").cos(ang * 3.1415926 / 180)
        my = cy + r * 0.5 * __import__("math").sin(ang * 3.1415926 / 180)
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{color}" '
                 f'stroke-width="{1.2 + min(cnt, 6) * 0.45}" opacity="0.55"/>')
        b.append(f'<circle cx="{mx}" cy="{my}" r="11" fill="#fff" stroke="{color}" '
                 f'stroke-width="1.2"/>')
        b.append(txt(mx, my + 4, str(cnt), 10, color, anchor="middle", weight="bold"))
        lx = cx + (r + 34) * __import__("math").cos(ang * 3.1415926 / 180)
        ly = cy + (r + 34) * __import__("math").sin(ang * 3.1415926 / 180)
        anchor = "middle"
        if lx > cx + 30:
            anchor = "start"
        elif lx < cx - 30:
            anchor = "end"
        b.append(txt(lx, ly + 4, f"{name}（{cnt}条）", 11.5, INK, anchor=anchor))
    b.append(txt(20, 20, "线宽＝双侧引文条数；红＝移植接收（佛教→道教），蓝＝平行发展", 10.5, MUTED))
    b.append(txt(20, 470, "数据：§17.26 四组＋§17.48 八组＋§17.40 形式层（共 12 典、47 条双侧引文）",
                 10.5, MUTED))
    return svg(680, 490, "图16　十二典×華嚴对应径向图",
               "中心为華嚴，周围十二典各以引文条数连线，红移植蓝平行", "".join(b))


def fig_pipeline(stats):
    """图16 复现与验证管线。stats＝dict(sources, probes, jsons, gates, chars, figs)"""
    stages = [
        ("一手语料", f"{stats['sources']} 档", "CBETA XML · 卍续藏 · Kanripo\nGRETIL · 84000 · 德格 eTengyur", BLUE),
        ("探针脚本", f"{stats['probes']} 部", "scripts/build_* · 每个论断一个探针\n起止锚切片 · 词级计数", GREEN),
        ("数据层", f"{stats['jsons']} 份", "data/research/*.json\n全部机器生成 · 手改无效", BROWN),
        ("门禁", f"{stats['gates']} 组", "verify_dazang_article.py\n含负向测试（篡改即 FAIL）", GOLD),
        ("文章", f"{stats['chars']}", "36.6 万字 · 52 小节 · 16 图\n内嵌交互图 · 全部可回源", RED),
    ]
    x, y, bw, bh = 24, 70, 200, 110
    b = []
    for i, (name, num, sub, color) in enumerate(stages):
        x = 24 + i * 252
        b.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="8" '
                 f'fill="#fff" stroke="{color}" stroke-width="1.6"/>')
        b.append(txt(x + 16, y + 28, name, 14, color, weight="bold"))
        b.append(txt(x + 16, y + 58, num, 19, INK, weight="bold"))
        for j, line in enumerate(sub.split("\n")):
            b.append(txt(x + 16, y + 82 + j * 16, line, 9.5, MUTED))
        if i < len(stages) - 1:
            ax = x + bw + 6
            b.append(f'<line x1="{ax}" y1="{y + bh / 2}" x2="{ax + 38}" '
                     f'y2="{y + bh / 2}" stroke="{MUTED}" stroke-width="1.6" '
                     f'marker-end="url(#arrow)"/>')
    b.append('<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
             'refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" '
             f'fill="{MUTED}"/></marker></defs>')
    b.append(txt(24, 30, "每个论断的来路：语料 → 探针 → 数据 → 门禁 → 文章（任一环可独立重跑）",
                 12, INK, weight="bold"))
    return svg(1290, 210, "图14　复现与验证管线",
               "一手语料到成文的五段管线与计数", "".join(b))
