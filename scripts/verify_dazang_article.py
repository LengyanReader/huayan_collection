#!/usr/bin/env python3
"""Gate for the canon-mapping article page: content, figures, and data consistency."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "web" / "demo" / "articles" / "huayan-dazang-mapping.html"
DATA = ROOT / "data" / "research" / "dazang_mapping_verification.json"
SRC = ROOT / "docs" / "经学文献" / "华严经与大藏经对应研究.md"


def fail(msg: str) -> None:
    print(f"FAIL  {msg}")
    raise SystemExit(1)


def ok(msg: str) -> None:
    print(f"PASS  {msg}")


def main() -> int:
    for p in (PAGE, DATA, SRC):
        if not p.exists():
            fail(f"missing {p.relative_to(ROOT)}")

    html = PAGE.read_text(encoding="utf-8")
    m = re.search(r"var ARTICLE = (\{.*?\});", html, re.S)
    if not m:
        fail("var ARTICLE not found")
    try:
        art = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        fail(f"ARTICLE JSON invalid: {e}")
    md = art.get("doc_md", "")
    data = json.loads(DATA.read_text(encoding="utf-8"))
    src = SRC.read_text(encoding="utf-8")

    ok(f"page loaded: {len(html):,} bytes; doc_md {len(md):,} chars")
    if md != src:
        fail("doc_md differs from source markdown")
    ok("doc_md equals source markdown")

    bare = re.findall(r"<!--GEN:(?!start:|end:)[a-z_0-9]+-->", md)
    if bare:
        fail(f"unresolved placeholders: {bare[:3]}")
    ok("no unresolved placeholders")

    figures = re.findall(r"<title>(图\d+)", md)
    want = [f"图{i}" for i in range(1, 14)]
    if figures != want:
        fail(f"figure sequence {figures}")
    if md.count("<svg") != 13:
        fail(f"svg count {md.count('<svg')} != 13")
    ok("13 figures in order 图1–图13")

    def rows_between(start: str, end: str) -> int:
        a = md.find(start)
        if a < 0:
            return -1
        b = md.find(end, a)
        if b < 0:
            b = len(md)
        return len(re.findall(r"^\|", md[a:b], re.M)) - 2

    mapping = rows_between("| # | 八十华严 | 六十华严 |", "\n\n")
    if mapping != len(data["mapping_60_80"]["rows"]):
        fail(f"mapping rows {mapping} != {len(data['mapping_60_80']['rows'])}")
    ok(f"mapping table rows: {mapping}")

    catalog = len(re.findall(r"^\| T\d{3} \|.*\| (别生|大本|眷属) \|", md, re.M))
    if catalog != 30:
        fail(f"catalog rows {catalog} != 30")
    ok("catalog table rows: 30")

    ranges = len(re.findall(r"^\| \d{1,4}–\d{1,4} \|", md, re.M))
    if ranges != len(data["section_ranges"]):
        fail(f"section ranges {ranges} != {len(data['section_ranges'])}")
    ok(f"section range rows: {ranges}")

    claims = len(re.findall(r"^\| V\d\d \|", md, re.M))
    if claims != len(data["claims"]):
        fail(f"claims {claims} != {len(data['claims'])}")
    ok(f"claim rows: {claims}")

    enrich_path = ROOT / "data" / "research" / "dazang_enrichment.json"
    enrich = json.loads(enrich_path.read_text(encoding="utf-8"))
    checks = [
        ("forty", r"^\| L\.\d+", len(enrich["forty"]["batches"])),
        ("bhumi", r"^\| (初地|二地|三地|四地|五地|六地|七地|八地|九地|十地)[^|]*\| [A-Za-z]", len(enrich["bhumi"])),
        ("tib45", r"^\| \d{1,2} \| 03[5-8] \|", len(enrich["tib45"])),
        ("mentions", r"^\| (瑜伽論|涅槃經|智度論|成唯識論|攝大乘論|瓔珞經|寶性論) \|", len(enrich["mentions"]["rows"])),
    ]
    for name, pat, want in checks:
        got = len(re.findall(pat, md, re.M))
        if got != want:
            fail(f"{name} table rows {got} != {want}")
    ok("enrichment tables: 40/十地/45章/注疏 rows match JSON")

    for i, block in enumerate(re.findall(r"<svg.*?</svg>", md, re.S), 1):
        try:
            ET.fromstring(block)
        except ET.ParseError as e:
            fail(f"figure {i} is not well-formed XML: {e}")
    ok("13 SVG blocks are well-formed XML")

    graph_path = ROOT / "data" / "research" / "huayan_dazang_graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    ids = {n["id"] for n in graph["nodes"]}
    dangling = [e for e in graph["edges"] if e["source"] not in ids or e["target"] not in ids]
    if dangling:
        fail(f"dangling graph edges: {dangling[:3]}")
    types = graph["stats"]["by_node"]
    if types.get("pin") != 39 or types.get("tib") != 45 or types.get("text") != 29 or types.get("cluster") != 14:
        fail(f"graph node counts {types}")
    if graph["stats"]["nodes"] != len(graph["nodes"]) or graph["stats"]["edges"] != len(graph["edges"]):
        fail("graph stats mismatch")
    belongs = {e["source"] for e in graph["edges"] if e["type"] == "belongs" and e["source"].startswith("P:")}
    if len(belongs) != 39:
        fail(f"pins without cluster: {39 - len(belongs)}")
    ok(f"graph integrity: {graph['stats']['nodes']} nodes / {graph['stats']['edges']} edges, 0 dangling")

    if 'id="dazang-graph-inline"' not in md:
        fail("article missing inline graph container")
    if "var DAZANG_GRAPH" not in html:
        fail("page missing DAZANG_GRAPH data")
    inline_js = (ROOT / "web" / "demo" / "src" / "dazang_graph_inline.js").read_text(encoding="utf-8")
    for key in ["function mount()", "dg-bar", 'data-mode="force"', 'data-mode="citation"', "MutationObserver"]:
        if key not in inline_js:
            fail(f"inline renderer missing {key}")
    if re.search(r"https?://", inline_js):
        fail("inline renderer references external resources")
    if "new ResizeObserver(function () { draw(); })" in inline_js:
        fail("synchronous ResizeObserver redraw (feedback loop)")
    if "requestAnimationFrame" not in inline_js:
        fail("ResizeObserver redraw is not frame-coalesced")
    if "huayan-dazang-graph.html" in md:
        fail("standalone graph link still present")
    if not re.search(r'"nodes":\s*148', html):
        fail("inline graph data not embedded")
    ok(f"inline graph: data embedded + renderer mounted ({len(inline_js):,} bytes)")

    for key in ["613,191", "507,687", "265,368", "阙一品", "十明", "十通", "Toh 44-31", "第 31 章"]:
        if key not in md:
            fail(f"missing key fact: {key}")
    ok("key verified facts present")

    for bad in ["undefined", "NaN", "None"]:
        if re.search(rf"\b{bad}\b", md):
            fail(f"rendered artifact contains {bad}")
    ok("no undefined/NaN/None artifacts")

    print("=" * 40)
    print("ALL Dazang article checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())