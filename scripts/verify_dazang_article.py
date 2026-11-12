#!/usr/bin/env python3
"""Gate for the canon-mapping article page: content, figures, and data consistency."""

from __future__ import annotations

import hashlib
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

    # --- semantic anchors: chapter -> pin must equal the Derge colophon mapping ---
    expect_tib = {}
    for n in range(1, 46):
        if 1 <= n <= 4:
            v = n
        elif 5 <= n <= 9:
            v = 5
        elif n == 10:
            v = 6
        elif n in (11, 32):
            v = None
        elif 12 <= n <= 31:
            v = n - 5
        else:
            v = n - 6
        expect_tib[n] = v

    tib_rows = re.findall(r"^\| (\d{1,2}) \| 0\d\d \| [0-9ab.]+ \| ([^|]+?) \| [^|]+ \|$", md, re.M)
    if len(tib_rows) != 45:
        fail(f"tib45 semantic rows {len(tib_rows)} != 45")
    wrong = []
    for no, pin_txt in tib_rows:
        m = re.search(r"品(\d+)", pin_txt)
        got = int(m.group(1)) if m else None
        if got != expect_tib[int(no)]:
            wrong.append((int(no), pin_txt.strip(), expect_tib[int(no)]))
    if wrong:
        fail(f"chapter->pin mismatch (colophon mapping): {wrong[:5]}")
    ok("tib45 chapter->pin matches Derge colophons (45/45)")

    # --- forty-huayan batches must track the live JSON files ---
    batch_files = sorted((ROOT / "data" / "research").glob("huayan_80_40_duikandu_b*.json"))
    live_windows = sum(len(json.loads(p.read_text(encoding="utf-8")).get("windows", [])) for p in batch_files)
    if len(enrich["forty"]["batches"]) != len(batch_files) or enrich["forty"]["windows_total"] != live_windows:
        fail(f"forty stale: {len(enrich['forty']['batches'])}/{enrich['forty']['windows_total']} "
             f"vs live {len(batch_files)}/{live_windows}")
    if re.search(r"10 批[、 ]*62", md):
        fail("stale forty counts (10 批 62 窗) still in prose")
    pairs = set(re.findall(r"(\d+) 批[、 ]*(\d+) (?:个对照)?窗", md))
    allowed = {(str(len(batch_files)), str(live_windows)), ("16", "92")}  # 16/92 是 v1.2 历史记述
    bad_pairs = pairs - allowed
    if bad_pairs:
        fail(f"forty window counts out of sync with live data: {sorted(bad_pairs)}")
    zero_rows = re.findall(r"^\| (L\.\d+[^|]*)\| [^|]+ \| 0 \|", md, re.M)
    if zero_rows:
        fail(f"forty table shows a bare 0 window count: {zero_rows}")
    if "不以「窗口」记录" not in md:
        fail("forty table footnote about non-window batches missing")
    ok(f"forty batches: {len(batch_files)} batches / {live_windows} windows")

    # --- catalog: pin definition + T293 docNumber coverage ---
    if "「品」= 该文本自标的品题数" not in md:
        fail("catalog pin-column definition missing")
    if re.search(r"^\| T287 \|.*\| 4 \|", md, re.M):
        fail("T287 pin count regressed to 4 (type=pin string count)")
    if "39 入法界品、36 普賢行品" not in md:
        fail("T293 xref missing the Fasc.1-39 (pin 39) segment")
    ok("catalog: pin column defined; T293 xref complete")

    # --- no stale cross-section state ---
    if "是否为此品别译，〔待核〕" in md:
        fail("§4.3 still says T300/T301 pending while §12.6 has decided")
    ok("no contradictory pending-state left")

    # --- §17 cross-canon registry: table == JSON, and grades must match witnesses ---
    reg = json.loads((ROOT / "data" / "research" / "canon_registry.json").read_text(encoding="utf-8"))
    rows_json = reg.get("rows", [])
    tbl = re.findall(r"^\| ([^|]*?) \| ([^|]*?) \| ([^|]*?) \| ([^|]*?) \| ([^|]*?) \| ([^|]*?) \| ([ABC]) \|$", md, re.M)
    if len(tbl) != len(rows_json):
        fail(f"§17 registry rows {len(tbl)} != JSON {len(rows_json)}")
    seen = {(r[1].strip(), r[6]) for r in tbl}
    for r in rows_json:
        if (r["canon"], r["grade"]) not in seen:
            fail(f"§17 registry row missing or mis-graded: {r['canon']} / {r['grade']}")
        w = r["witness_local"].strip()
        if r["grade"] == "A" and ("無" in w or "仅二手" in w or "僅二手" in w):
            fail(f"§17 grade A without first-hand witness: {r['canon']}")
        if r["grade"] == "B" and w.startswith("無") and "題錄" not in w and "题录" not in w:
            fail(f"§17 grade B with no witness and no bibliographic record: {r['canon']}")
    if "相似不是证据，见证才是证据" not in md:
        fail("§17 red-line sentence missing")
    if "跨典藏登记册：17 行" not in md:
        fail("§16 data table lacks canon_registry.json row")
    ok(f"§17 registry: {len(rows_json)} rows, grades consistent with witnesses")

    # --- §17.3/17.4 relation ontology: facets, operators, coverage must agree with the text ---
    ont_path = ROOT / "data" / "research" / "relation_ontology.json"
    if not ont_path.exists():
        fail("relation_ontology.json missing")
    ont = json.loads(ont_path.read_text(encoding="utf-8"))
    facets, ops = ont["facets"], ont["operators"]
    fids = [f["id"] for f in facets]
    if len(facets) != 7 or len(set(fids)) != 7:
        fail(f"ontology facets {len(facets)} != 7")
    if len(ops) < 34 or len({o["id"] for o in ops}) != len(ops):
        fail(f"ontology operators {len(ops)} (<34) or duplicated ids")
    verdicts = set(ont["meta"]["verdicts"])
    statuses = set(ont["meta"]["status_legend"])
    for o in ops:
        if o["facet"] not in fids:
            fail(f"operator {o['id']} has unknown facet {o['facet']}")
        if not o["min_evidence"].strip() or not o["forbidden"].strip():
            fail(f"operator {o['id']} lacks min_evidence/forbidden")
        if o["verdict"] not in verdicts:
            fail(f"operator {o['id']} has unknown verdict {o['verdict']}")
        if o["status"] not in statuses:
            fail(f"operator {o['id']} has unknown status {o['status']}")
        if o["status"] == "done" and not o.get("refs"):
            fail(f"operator {o['id']} marked done but cites no section")
    def gen_block(key: str) -> str:
        s = md.find(f"<!--GEN:start:{key}-->")
        e = md.find(f"<!--GEN:end:{key}-->", s + 1)
        if s < 0 or e < 0:
            fail(f"§17 GEN block missing: {key}")
        return md[s:e]

    op_md = gen_block("operators")
    audit_md = gen_block("audit")
    op_rows = re.findall(r"^\| ([MTDPRSC]\d+) ", op_md, re.M)
    if sorted(op_rows) != sorted(o["id"] for o in ops):
        fail(f"§17.3 operator table rows {len(op_rows)} != ontology {len(ops)}")
    total = {"done": 0, "partial": 0, "none": 0}
    for f in facets:
        mine = [o for o in ops if o["facet"] == f["id"]]
        c = {k: sum(1 for o in mine if o["status"] == k) for k in total}
        for k in total:
            total[k] += c[k]
        pat = (rf"^\| {f['id']} \| [^|]+ \| {len(mine)} \| {c['done']} \| {c['partial']} "
               rf"\| {c['none']} \| (\d+)% \|")
        m = re.search(pat, audit_md, re.M)
        if not m:
            fail(f"§17.4 audit row for facet {f['id']} missing or miscounted")
        want = round((c["done"] + 0.5 * c["partial"]) / len(mine) * 100)
        if int(m.group(1)) != want:
            fail(f"§17.4 facet {f['id']} coverage {m.group(1)}% != {want}%")
    score = total["done"] + 0.5 * total["partial"]
    m = re.search(rf"^\| \*\*合\*\* \| — \| \*\*{len(ops)}\*\* \| \*\*{total['done']}\*\* "
                  rf"\| \*\*{total['partial']}\*\* \| \*\*{total['none']}\*\* \| \*\*(\d+)%\*\*", audit_md, re.M)
    if not m:
        fail("§17.4 audit total row missing or miscounted")
    want = round(score / len(ops) * 100)
    if int(m.group(1)) != want:
        fail(f"§17.4 total coverage {m.group(1)}% != {want}%")
    per = "＋".join(f"{f['id']}{sum(1 for o in ops if o['facet'] == f['id'])}" for f in facets)
    if f"共 {len(ops)} 个（{per}）" not in md:
        fail(f"§17.3 facet-count sentence out of sync: expected 共 {len(ops)} 个（{per}）")
    if f"加权 {score:g}/{len(ops)}" not in md:
        fail(f"§17.4 prose coverage out of sync: expected 加权 {score:g}/{len(ops)}")
    ok(f"§17.3–17.4 ontology: {len(facets)} facets / {len(ops)} operators, audit {score:g}/{len(ops)} = {want}%")

    # --- §4.5 edge types must each be assigned a facet (checked after the graph loads) ---
    emap = ont.get("graph_edges", {})
    graph = json.loads((ROOT / "data" / "research" / "huayan_dazang_graph.json").read_text(encoding="utf-8"))
    graph_types = {e["type"] for e in graph["edges"]}
    if set(emap) != graph_types:
        fail(f"edge->facet map {sorted(emap)} != graph edge types {sorted(graph_types)}")
    edge_rows = re.findall(r"^\| `([a-z_0-9]+)` \| [^|]+ \| [^|]+ \| [^|]+ \| ([MTDPRSC]) \| [^|]+ \|$", md, re.M)
    if len(edge_rows) != len(emap):
        fail(f"§4.5 edge table rows {len(edge_rows)} != {len(emap)}")
    for name, facet in edge_rows:
        if emap.get(name, {}).get("facet") != facet:
            fail(f"§4.5 edge {name} facet {facet} != ontology {emap.get(name)}")
    if "| 边型 | 方向 | 含义 | 线型 | 面 | 级 |" not in md:
        fail("§4.5 edge table lacks the facet column")
    ok(f"§4.5 edge facets: {len(edge_rows)} edge types mapped")

    # --- §17.11–17.13 probes: every quote must still be present in its source ---
    probes_path = ROOT / "data" / "research" / "cross_canon_probes.json"
    if not probes_path.exists():
        fail("cross_canon_probes.json missing")
    probes = json.loads(probes_path.read_text(encoding="utf-8"))

    def norm(text: str) -> str:
        text = re.sub(r"<pb:[^>]*>", "", text)
        text = re.sub(r"<lb[^>]*/>", "", text)
        text = re.sub(r"<pb[^>]*/>", "", text)
        text = re.sub(r"<anchor[^>]*/>", "", text)
        text = re.sub(r"<[^>]+>", "", text)
        return re.sub(r"\s+", "", text.replace("¶", ""))

    probe_files = {"T1735": "T35n1735.xml", "T1733": "T35n1733.xml", "T279": "T10n0279.xml"}
    probe_src = {}
    for key, fn in probe_files.items():
        probe_src[key] = norm((ROOT / "data" / "references" / "cbeta" / fn).read_text(encoding="utf-8"))
    dz_dir = ROOT / "data" / "references" / "daozang"
    probe_src["DZ0001"] = norm("".join(p.read_text(encoding="utf-8") for p in sorted(dz_dir.glob("KR5a0001_*.txt"))))
    for key, meta in probes["meta"]["sources"].items():
        raw = (b"".join(p.read_bytes() for p in sorted(dz_dir.glob("KR5a0001_*.txt")))
               if key == "DZ0001" else (ROOT / meta["path"]).read_bytes())
        if hashlib.sha256(raw).hexdigest() != meta["sha256"]:
            fail(f"probe source hash changed: {key}")
    for section in ("t9", "d5", "p1"):
        for q in probes[section]["quotes"]:
            if norm(q["text"]) not in probe_src[q["src"]]:
                fail(f"{section} quote missing from {q['src']}: {q['text'][:24]}")
            if q["text"] not in md:
                fail(f"{section} quote not printed in article: {q['text'][:24]}")
    if "### 17.11 T9" not in md or "### 17.12 D5" not in md or "### 17.13 P1" not in md:
        fail("§17.11–17.13 probe headings missing")

    def first_table_rows(block: str) -> int:
        lines = block.splitlines()
        start = next(i for i, ln in enumerate(lines) if ln.startswith("|"))
        n = 0
        for ln in lines[start:]:
            if not ln.startswith("|"):
                break
            n += 1
        return max(0, n - 2)

    def grab(key: str) -> str:
        s = md.find(f"<!--GEN:start:{key}-->")
        e = md.find(f"<!--GEN:end:{key}-->", s + 1)
        return md[s:e]

    if first_table_rows(grab("t9")) != len(probes["t9"]["rows"]):
        fail("§17.11 table rows != probes JSON")
    if first_table_rows(grab("d5")) != len(probes["d5"]["rows"]):
        fail("§17.12 table rows != probes JSON")
    if first_table_rows(grab("p1")) != len(probes["p1"]["rows"]):
        fail("§17.13 table rows != probes JSON")
    if len(probes["p1"]["rows"]) != 10:
        fail("P1 must have ten stages")
    ok(f"§17.11–17.13 probes: {len(probes['t9']['quotes']) + len(probes['d5']['quotes']) + len(probes['p1']['quotes'])} quotes re-verified")

    # --- §17.8 external witnesses: every manifest file must exist with the recorded hash ---
    mf = ROOT / "data" / "references" / "external_manifest.json"
    if not mf.exists():
        fail("external_manifest.json missing")
    man = json.loads(mf.read_text(encoding="utf-8"))
    bad = []
    for k, v in man["files"].items():
        p = ROOT / v["path"]
        if not p.exists():
            bad.append(f"{k}: missing")
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h != v["sha256"]:
            bad.append(f"{k}: sha256 {h[:8]} != {v['sha256'][:8]}")
    if bad:
        fail(f"external witness mismatch: {bad[:3]}")
    if "本批新入库的见证" not in md:
        fail("§17.8 witness table missing")
    ok(f"§17.8 external witnesses: {len(man['files'])} files hash-verified")

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