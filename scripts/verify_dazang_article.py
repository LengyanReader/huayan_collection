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
    if f"已做 {total['done']} 个、部分 {total['partial']} 个、未做 {total['none']} 个" not in md:
        fail(f"§17.1 prose counts out of sync: expected 已做 {total['done']} / 部分 {total['partial']} / 未做 {total['none']}")
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
    t9_cases = probes["t9"]["cases"]
    for case in t9_cases:
        for q in case["quotes"]:
            if norm(q["text"]) not in probe_src[q["src"]]:
                fail(f"t9 quote missing from {q['src']}: {q['text'][:24]}")
            if q["text"] not in md:
                fail(f"t9 quote not printed in article: {q['text'][:24]}")
    for section in ("d5", "p1"):
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

    t9_grab = grab("t9")
    t9_table_rows = sum(1 for ln in t9_grab.splitlines() if ln.startswith("| ") and not ln.startswith("|---"))
    if t9_table_rows != sum(len(c["rows"]) for c in t9_cases) + len(t9_cases):
        fail("§17.11 tables != probes JSON rows")
    if first_table_rows(grab("d5")) != len(probes["d5"]["rows"]):
        fail("§17.12 table rows != probes JSON")
    if first_table_rows(grab("p1")) != len(probes["p1"]["rows"]):
        fail("§17.13 table rows != probes JSON")
    if len(probes["p1"]["rows"]) != 10:
        fail("P1 must have ten stages")
    nq = sum(len(c['quotes']) for c in t9_cases) + len(probes['d5']['quotes']) + len(probes['p1']['quotes'])
    ok(f"§17.11–17.13 probes: {nq} quotes re-verified ({len(t9_cases)} 品 for T9)")

    # --- §17.14 T6: every example must be a substring of BOTH texts, at the cited line ---
    imp_path = ROOT / "data" / "research" / "implicit_quotes.json"
    if not imp_path.exists():
        fail("implicit_quotes.json missing")
    imp = json.loads(imp_path.read_text(encoding="utf-8"))
    def cjk(text: str) -> str:
        return re.sub(r"[^\u4e00-\u9fff]", "", text)

    imp_src = {}
    for key, meta in imp["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"T6 source hash changed: {key}")
        imp_src[key] = cjk((ROOT / meta["path"]).read_text(encoding="utf-8"))
    md_cjk = cjk(md)
    for pid in imp["pairs"]:
        p = imp["pairs"][pid]
        st = p["stats"]
        if st["marked"]["hits"] + st["unmarked"]["hits"] != st["hits"]:
            fail(f"T6 {pid}: marked + unmarked != hits")
        if st["marked"]["chars"] + st["unmarked"]["chars"] != st["matched_chars"]:
            fail(f"T6 {pid}: char sums do not add up")
        if len(p["sweep"]) != len(imp["meta"]["sweep"]):
            fail(f"T6 {pid}: sweep incomplete")
        for e in p["examples_unmarked"]:
            q = cjk(e["text"])
            if q not in imp_src[p["commentary"]] or q not in imp_src[p["sutra"]]:
                fail(f"T6 {pid}: example not found in both texts: {e['text'][:20]}")
            if q not in md_cjk:
                fail(f"T6 {pid}: example not printed in article: {e['text'][:20]}")
            if not imp_src[p["commentary"]].count(q):
                fail(f"T6 {pid}: empty example")
    if "### 17.14 T6" not in md or "### 17.15 T7" not in md or "### 17.18 未竟" not in md:
        fail("§17.14–17.18 headings missing")

    def rows_in(block: str) -> list[str]:
        lines = block.splitlines()
        start = next(i for i, ln in enumerate(lines) if ln.startswith("|"))
        out = []
        for ln in lines[start:]:
            if not ln.startswith("|"):
                break
            out.append(ln)
        return out

    t6_block = grab("t6")
    t6_rows = rows_in(t6_block)
    if len(t6_rows) - 2 != len(imp["pairs"]):
        fail("§17.14 first table rows != pairs in JSON")
    sweep_rows = [ln for ln in t6_block.splitlines() if re.match(r"^\| \d+ \|", ln)]
    if len(sweep_rows) != len(imp["meta"]["sweep"]):
        fail("§17.14 sweep table rows != meta.sweep")
    ok(f"§17.14 T6: {sum(len(p['examples_unmarked']) for p in imp['pairs'].values())} examples re-verified in both texts")

    # --- §4.6 source map: 39-品 master table must match the underlying JSONs ---
    sm_block = grab("source_map")
    sm_rows = [ln for ln in sm_block.splitlines() if re.match(r"^\| \d+ \|", ln)]
    mapping_rows = data["mapping_60_80"]["rows"]
    if len(sm_rows) != len(mapping_rows):
        fail(f"§4.6 source map rows {len(sm_rows)} != mapping rows {len(mapping_rows)}")
    tib_rows = json.loads((ROOT / "data" / "research" / "dazang_enrichment.json")
                          .read_text(encoding="utf-8"))["tib45"]
    tib_by_pin: dict[str, list[int]] = {}
    for r in tib_rows:
        tib_by_pin.setdefault(str(r["pin"]), []).append(r["no"])
    for i, row_ln in enumerate(sm_rows, 1):
        cells = [c.strip() for c in row_ln.split("|")]
        if cells[1] != str(i):
            fail(f"§4.6 row {i} numbering broken")
        if cells[2] != mapping_rows[i - 1]["p80"]:
            fail(f"§4.6 row {i} 品名 out of sync: {cells[2]}")
        want_tib = "、".join(str(n) for n in tib_by_pin.get(str(i), [])) or "—"
        if cells[4] != want_tib:
            fail(f"§4.6 row {i} 藏章 out of sync: {cells[4]} != {want_tib}")
        if mapping_rows[i - 1]["branch"].strip() and cells[5] == "—":
            fail(f"§4.6 row {i} 别译 dropped")
    if "藏译拆为章 5–9" not in sm_block or "聖堅本 25 参→彌勒自数 110" not in sm_block:
        fail("§4.6 growth marks missing")
    if "Daśabhūmika 存" not in sm_block or "Gaṇḍavyūha 存" not in sm_block:
        fail("§4.6 Sanskrit marks missing")
    hanwu = [r["no"] for r in tib_rows if str(r["pin"]) == "汉无"]
    if f"{len(hanwu)} 章汉无" not in sm_block:
        fail("§4.6 completion line out of sync")
    ok(f"§4.6 source map: {len(sm_rows)} 品 rows synced (藏章/别译/梵本/增长)")

    # --- §2.8 growth: timeline table and growth markers ---
    gr_block = grab("growth")
    gr_rows = [ln for ln in gr_block.splitlines()
               if ln.startswith("| ") and "译本" not in ln and "---" not in ln]
    if len(gr_rows) != 5:
        fail(f"§2.8 growth timeline rows {len(gr_rows)} != 5")
    for frag in ("聖堅〈入法界〉单品", "388–408", "420", "695–699", "798", "25 参",
                 "62 颂", "乌荼王本", "45 章·115 包"):
        if frag not in gr_block and frag not in md:
            fail(f"§2.8 growth figure missing: {frag}")
    if "单品先行" not in md or "判读纪律" not in md or "演變線" not in md and "演变线" not in md:
        fail("§2.8 growth prose missing")
    ok("§2.8 growth: 5-row timeline + 单品先行/入法界个案/判读纪律 present")

    # --- §6.3 Tanjur: dkar chag entries must be verbatim substrings of vol213 ---
    tanjur_block = grab("tanjur")
    dk_path = ROOT / "data" / "references" / "tibetan" / "derge_tengyur" / "vol213_dkarchag.txt"
    if not dk_path.exists():
        fail("tanjur dkar chag missing")
    dk_norm = re.sub(r"\[[0-9]+[xab](?:\.\d+)?\]|#|\{[^}]*\}", "",
                     dk_path.read_text(encoding="utf-8").replace("\n", " "))
    dk_nospace = re.sub(r"\s+", "", dk_norm)
    tanjur_titles = re.findall(r"^\| Toh \d+ \| (འཕགས་པ[^\n]*?|ཀུན་དུ[^\n]*?) \|", tanjur_block, re.M)
    if len(tanjur_titles) < 5:
        fail(f"§6.3 tanjur rows {len(tanjur_titles)} < 5")
    for t in tanjur_titles[:5]:          # 行愿表（5 列）：题名回源 dkar chag
        if re.sub(r"\s+", "", t) not in dk_nospace:
            fail(f"§6.3 tanjur title not verbatim in dkar chag: {t[:40]}")
    for t in tanjur_titles[5:]:          # 十地表（3 列）：题名回源卷文件
        tt = re.sub(r"\s+", "", t)
        if not any(tt in re.sub(r"\s+", "", re.sub(r"\[[^\]]*\]|#", "",
                (ROOT / "data" / "references" / "tibetan" / "derge_tengyur" / f"vol{v}.txt")
                .read_text(encoding="utf-8")))
                for v in ("113", "116")):
            fail(f"§6.3 十地 title not verbatim in volumes: {t[:40]}")
    for frag in ("ཀླུ་སྒྲུབ", "ཕྱོགས་ཀྱི་གླང་པོ", "དབྱིག་གཉེན", "443b"):
        if frag not in tanjur_block:
            fail(f"§6.3 tanjur column missing: {frag}")
    ok(f"§6.3 tanjur: {len(tanjur_titles)} 行愿讚释 entries verbatim in dkar chag")

    # --- §6.6 Toh numbers: eTengyur vol117 must carry {D4011}–{D4015} ---
    v117 = (ROOT / "data" / "references" / "tibetan" / "derge_tengyur" / "vol117.txt")
    if not v117.exists():
        fail("eTengyur vol117 missing")
    v117t = v117.read_text(encoding="utf-8")
    for no in range(4011, 4016):
        if f"{{D{no}}}" not in v117t:
            fail(f"vol117 missing {{D{no}}} mark")
    for no in ("Toh 4011", "Toh 4012", "Toh 4013", "Toh 4014", "Toh 4015"):
        if no not in md:
            fail(f"§6.6 Toh number missing in article: {no}")
    ok("§6.6 tanjur: Toh 4011–4015 double-sourced (vol117 {D} marks + dkar chag order)")

    # --- §17.15 T7: 品级长度比、引用率、节略用语、锚点链 ---
    t7_path = ROOT / "data" / "research" / "paraphrase_probe.json"
    if not t7_path.exists():
        fail("paraphrase_probe.json missing")
    t7 = json.loads(t7_path.read_text(encoding="utf-8"))
    for key, meta in t7["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"T7 source hash changed: {key}")
    for pid in t7["pairs"]:
        p = t7["pairs"][pid]
        st = p["stats"]
        if sum(st["markers_by_type"].values()) != st["markers_total"]:
            fail(f"T7 {pid}: marker counts do not add up")
        if sum(r["quoted_chars"] for r in p["pins"]) != st["quoted_chars"]:
            fail(f"T7 {pid}: per-品 quoted chars != total")
        if sum(r["quoted_hits"] for r in p["pins"]) != st["hits"]:
            fail(f"T7 {pid}: per-品 hit counts != total")
        if sum(r["sutra_chars"] for r in p["pins"]) != st["sutra_chars"]:
            fail(f"T7 {pid}: per-品 sutra chars != total")
        q = cjk(st["max_hit_head"])
        if q not in imp_src[p["commentary"]] or q not in imp_src[p["sutra"]]:
            fail(f"T7 {pid}: longest hit not found in both texts")
        if q not in md_cjk:
            fail(f"T7 {pid}: longest hit not printed in article")
        for e in p["examples"]:
            ec = cjk(e["ctx"])
            if ec not in md_cjk:
                fail(f"T7 {pid}: example not printed: {e['lb']}")
            if ec not in imp_src[p["commentary"]]:
                fail(f"T7 {pid}: example not found in commentary: {e['lb']}")
    a, b = t7["pairs"]["A"]["stats"], t7["pairs"]["B"]["stats"]
    if a["chain_spans_ge_120"] or b["chain_spans_ge_120"]:
        if "无一跨 120 字" in md:
            fail("T7: article claims no chain >= 120 but JSON has one")
    elif "无一跨 120 字" not in md:
        fail("T7: article should state that no chain spans 120")
    if f"{a['chain_max_span']}／{b['chain_max_span']} 字" not in md:
        fail("T7: chain span sentence out of sync")
    c = t7["pairs"]["C"]["stats"]
    for frag in (f"长比 {c['length_ratio']:.2f}、引用率中位 {c['quoted_share_median']:.2%}",
                 f"链最长 {c['chain_max_span']} 字"):
        if frag not in md:
            fail(f"T7: C judgement figure missing: {frag}")
    t7_block = grab("t7")
    t7_tables = [ln for ln in t7_block.splitlines() if ln.startswith("| 对 |")]
    if len(t7_tables) != 3:
        fail("§17.15 should print three tables with a 对 column")
    star = [ln for ln in t7_block.splitlines() if ln.startswith("| **合** |")]
    if len(star) != 1 or any(f"**{t7['pairs'][pid]['stats']['markers_total']}**" not in star[0]
                             for pid in t7["pairs"]):
        fail("§17.15 marker total row out of sync")
    if "### 17.15 T7" not in md or "### 17.18 未竟" not in md:
        fail("§17.15–17.16 headings missing")
    ok(f"§17.15 T7: {'+'.join(str(t7['pairs'][pid]['stats']['markers_total']) for pid in t7['pairs'])} 节略用语, "
       f"{sum(len(p['examples']) for p in t7['pairs'].values())} 例 re-verified")

    # --- §17.16 T4: screen / partition / controls must be reproduced by the article ---
    t4_path = ROOT / "data" / "research" / "conflation_probe.json"
    if not t4_path.exists():
        fail("conflation_probe.json missing")
    t4 = json.loads(t4_path.read_text(encoding="utf-8"))
    t4_src = {}

    def src_of(key: str) -> str:
        if key not in t4_src:
            path = ROOT / t4["meta"]["sources"][key]["path"]
            t4_src[key] = imp_src[key] if key in imp_src else cjk(path.read_text(encoding="utf-8"))
        return t4_src[key]

    for key, meta in t4["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"T4 source hash changed: {key}")

    def tables_of(block: str) -> list[list[str]]:
        out, cur = [], []
        for ln in block.splitlines():
            if ln.startswith("|"):
                cur.append(ln)
            elif cur:
                if len(cur) > 1:
                    out.append(cur)
                cur = []
        if len(cur) > 1:
            out.append(cur)
        return out

    t4_block = grab("t4")
    t4_tables = tables_of(t4_block)
    screen_t = next(t for t in t4_tables if "分块检验" in t[0])
    base_t = next(t for t in t4_tables if "甲 12 字串见于乙" in t[0])
    part_t = next(t for t in t4_tables if "分离度" in t[0])
    exh_t = next(t for t in t4_tables if "`lb`" in t[0])
    if len(screen_t) - 2 != len(t4["screen"]):
        fail("§17.16 screen table rows != JSON")
    if len(base_t) - 2 != len(t4["baselines"]):
        fail("§17.16 baseline table rows != JSON")
    if len(part_t) - 2 != len(t4["partition"]) + 1:
        fail("§17.16 partition table rows != JSON (+1 正控)")

    for r in t4["screen"]:
        line = next((ln for ln in screen_t[2:] if ln.startswith(f"| {r['id']} |")), None)
        if line is None:
            fail(f"T4 screen row missing: {r['id']}")
        if f"{r['cov']['T278']:.2%}" not in line or f"{r['cov']['T279']:.2%}" not in line:
            fail(f"T4 screen coverage out of sync: {r['id']}")
    for r in t4["baselines"]:
        if f"{r['coverage']:.2%}" not in base_t[[ln for ln in base_t].index(
                next(ln for ln in base_t[2:] if ln.startswith(f"| {r['label']} |")))]:
            fail(f"T4 baseline coverage out of sync: {r['label']}")

    pos = t4["controls"]["positive"]
    if not pos["pass"]:
        fail("T4 positive control did not pass; the detector cannot see a seam")
    if pos["result"]["recovered_error"] > t4["meta"]["block_chars"]:
        fail("T4 positive control split error exceeds one block")
    pos_line = next(ln for ln in part_t[2:] if ln.startswith("| 正控（植入） |"))
    if f"{pos['result']['separation']:+.1%}" not in pos_line:
        fail("T4 positive-control separation out of sync")
    if f"误差 {pos['result']['recovered_error']} 字" not in md:
        fail("T4 positive-control sentence out of sync")

    for r in t4["partition"]:
        line = next((ln for ln in part_t[2:] if ln.startswith(f"| {r['id']} |")), None)
        if line is None:
            fail(f"T4 partition row missing: {r['id']}")
        bs = r["best_split"]
        if bs["split_char"] is None:
            if "— | — | — | 不通过" not in line:
                fail(f"T4 {r['id']}: empty split not printed as dashes")
        elif f"{bs['separation']:+.1%}" not in line:
            fail(f"T4 {r['id']}: separation out of sync")
        if r["pass"] != bs["pass"]:
            fail(f"T4 {r['id']}: pass flag inconsistent with split")

    if t4["verdict"]["passed"]:
        fail(f"T4: {t4['verdict']['passed']} passed, but the article claims none")
    if "无一部可通过分块来源分离检验" not in md:
        fail("T4: verdict sentence missing")
    x223 = next((r for r in t4["partition"] if r["id"] == "X223"), None)
    if x223 is None:
        fail("T4: X223 helun candidate missing")
    for hid in ("X223", "X240a", "X240b"):
        hr = next((r for r in t4["partition"] if r["id"] == hid), None)
        if hr is None or "helun" not in hr:
            fail(f"T4: helun candidate missing: {hid}")
        if hr["pass"]:
            fail(f"T4: {hid} unexpectedly passes two-segment separation (逐段嵌入不该有切点)")
        hl = hr["helun"]
        row = next((ln for ln in md.splitlines()
                    if ln.startswith(f"| {hid} |") and len(ln.split("|")) == 12), None)
        if row is None:
            fail(f"T4: helun table row missing: {hid}")
        cells = [c.strip() for c in row.split("|")]
        want = [str(hr["blocks"]), str(hl["labels"]["经块"]), str(hl["labels"]["义块"]),
                str(hl["labels"]["双高"]), str(hl["transitions"]), str(hl["longest_run"]),
                f"{hl['cov_overall'][hr['sources'][0]]:.1%}／{hl['cov_overall'][hr['sources'][1]]:.1%}",
                f"{hr['best_split']['separation']:+.1%}"]
        got = cells[3:11]
        if got != want:
            fail(f"T4: helun row out of sync: {hid} got={got} want={want}")
    if "逐段嵌入" not in md or "两段拼合" not in md:
        fail("T4: helun form wording missing")
    thr = t4["meta"]["thresholds"]
    if (f"两侧各≥{thr['min_side_share']:.0%}篇幅" not in md
            or f"各自≥{thr['side_coverage']:.0%}覆盖" not in md
            or f"压过交叉配对≥{thr['separation']:.0%}" not in md):
        fail("T4 threshold sentence out of sync")

    shown = 0
    for r in t4["partition"]:
        b = r["best_block"]
        if not b:
            continue
        shown += 1
        h = cjk(b["head"])
        if h not in src_of(r["id"]):
            fail(f"T4 {r['id']}: exhibit head not in candidate")
        if h not in src_of(b["source"]):
            fail(f"T4 {r['id']}: exhibit head not in source {b['source']}")
        if h not in md_cjk:
            fail(f"T4 {r['id']}: exhibit head not printed")
    if len(exh_t) - 2 != shown:
        fail("§17.16 exhibit rows != JSON")

    t293 = next(r for r in t4["targeted"] if r["a"] == "T293" and r["b"] == "T297")
    if f"{t293['coverage']:.2%}" not in md:
        fail("T4 targeted (卷40 vs 願讚) number missing")
    if "### 17.16 T4" not in md or "### 17.18 未竟" not in md:
        fail("§17.16–17.18 headings missing")
    ok(f"§17.16 T4: {len(t4['screen'])} screened / {len(t4['partition'])} partitioned / "
       f"{shown} exhibits re-verified; no candidate passes")

    # --- §17.17 T9 末会: departure-mark counts, unique anchors, name pairs ---
    eg_path = ROOT / "data" / "research" / "endgame_probe.json"
    if not eg_path.exists():
        fail("endgame_probe.json missing")
    eg = json.loads(eg_path.read_text(encoding="utf-8"))
    eg_src = {}
    for key, meta in eg["meta"]["sources"].items():
        p = ROOT / meta["path"]
        if hashlib.sha256(p.read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"endgame source hash changed: {key}")
        eg_src[key] = cjk(p.read_text(encoding="utf-8"))

    eg_block = grab("endgame")

    def eg_row(lb: str) -> list[str]:
        for ln in eg_block.splitlines():
            if ln.startswith("|") and f"`{lb}`" in ln:
                return [c.strip() for c in ln.split("|")]
        fail(f"endgame scale row missing: {lb}")

    for key, lb in (("T279", "0319a05"), ("T278", "0676a05"), ("T293", "0661a01")):
        cells = eg_row(lb)
        t, kd = eg["texts"][key], eg["summary"]["kinds"][key]
        if (cells[3] != f"{t['chars']:,}" or cells[4] != str(t["marks"])
                or cells[5] != str(kd["参末"]) or cells[6] != str(kd["会众散"])):
            fail(f"endgame scale row out of sync: {key}")
    if "### 17.17 T9 末会" not in md:
        fail("§17.17 heading missing")
    for key in ("T279", "T278", "T293"):
        if eg["summary"]["marks"][key] != eg["texts"][key]["marks"]:
            fail(f"endgame summary/texts mark count disagree: {key}")
        if (eg["summary"]["kinds"][key]["参末"] + eg["summary"]["kinds"][key]["会众散"]
                != eg["texts"][key]["marks"]):
            fail(f"endgame kinds do not sum to marks: {key}")
    ok("§17.17 scale rows: 48/45/52 marks, 参末/会众散 split matches JSON")

    want_pairs = [r for rows in (eg["pivot"]["T278"], eg["pivot"]["T293"], eg["reverse"])
                  for r in rows if r["cls"] in ("同一处", "邻近")]
    got_pairs = [ln for ln in eg_block.splitlines()
                 if re.match(r"^\| (八十→(六十|四十)|四十→八十) \| `\d", ln)]
    if len(got_pairs) != len(want_pairs):
        fail(f"endgame anchor rows {len(got_pairs)} != JSON {len(want_pairs)}")
    for r in want_pairs:
        if f"`{r['lb']}`" not in md:
            fail(f"endgame anchor lb missing: {r['lb']}")
    checked = 0
    for akey, rows in (("T279", eg["pivot"]["T278"]), ("T279", eg["pivot"]["T293"]),
                       ("T293", eg["reverse"])):
        for r in rows:
            if r["cls"] in ("同一处", "邻近"):
                tail = cjk(r["ctx"])[-10:]
                if len(tail) >= 6 and tail not in eg_src[akey]:
                    fail(f"endgame anchor ctx not in source: {r['lb']} {tail}")
                checked += 1
    ok(f"§17.17 anchors: {len(want_pairs)} rows, {checked} ctx re-verified in sources")

    for ln in eg_block.splitlines():
        mm = re.match(r"^\| (八十→六十|八十→四十|四十→八十) \| (\d+) \| (\d+) \| (\d+) "
                      r"\| (\d+) \| (\d+) \| (\d+) \|", ln)
        if not mm:
            continue
        name = mm.group(1)
        if name == "八十→六十":
            rows_, tally = eg["pivot"]["T278"], eg["summary"]["pivot_to_60"]
        elif name == "八十→四十":
            rows_, tally = eg["pivot"]["T293"], eg["summary"]["pivot_to_40"]
        else:
            rows_, tally = eg["reverse"], eg["summary"]["reverse_40_to_80"]
        if (int(mm.group(2)) != len(rows_)
                or int(mm.group(3)) != tally.get("同一处", 0)
                or int(mm.group(4)) != tally.get("邻近", 0)
                or int(mm.group(5)) != tally.get("漂移", 0)
                or int(mm.group(6)) != tally.get("复见", 0)
                or int(mm.group(7)) != tally.get("无锚", 0)):
            fail(f"endgame tally row out of sync: {name}")
    ok("endgame tally rows match JSON (incl. 复见 tier)")

    npr = [ln for ln in eg_block.splitlines()
           if ln.startswith("| 八十↔") and ln.count("|") == 5]
    if len(npr) != 2:
        fail("endgame name-pair rows missing")
    for ln, key in zip(npr, ("name_pairs_60", "name_pairs_40")):
        cells = [c.strip() for c in ln.split("|")]
        if (cells[2] != str(eg["summary"][key]["proper"])
                or cells[3] != str(eg["summary"][key]["generic"])):
            fail(f"endgame name-pair row out of sync: {key}")
    for q in eg["variant_example"]["quotes"]:
        if cjk(q["text"]) not in eg_src[q["key"]]:
            fail(f"endgame variant quote not in source: {q['key']} {q['text']}")
    n_q = len(eg["variant_example"]["quotes"])
    gv = eg["variant_example"].get("sanskrit")
    if not gv:
        fail("endgame variant_example missing Sanskrit evidence")
    gv_path = ROOT / gv["source"]
    if hashlib.sha256(gv_path.read_bytes()).hexdigest() != gv["sha256"]:
        fail("endgame Sanskrit source hash changed")
    gv_flat = " ".join(gv_path.read_text(encoding="utf-8").split())
    for q in gv["quotes"]:
        if " ".join(q["text"].split()) not in gv_flat:
            fail(f"endgame Sanskrit quote not in source: {q['text'][:40]}")
    ok(f"endgame name pairs + {n_q} variant quotes + {len(gv['quotes'])} Sanskrit quotes re-verified")

    # --- §17.17 链式对齐：表行 ↔ JSON 逐格对账；离群引文回源；语族计数与「非善財」断言 ---
    ch_lbl = {"八十→六十": "to_60", "八十→四十": "to_40", "四十→八十": "rev_40_80"}
    ch_rows = {}
    for ln in eg_block.splitlines():
        m = re.match(r"^\| (八十→六十|八十→四十|四十→八十)（链） \| (\d+) \| (\d+) \| (\d+) "
                     r"\| (\d+) \| (\d+) \| ([\d,—]+) \| ([\d,]+) \|$", ln)
        if m:
            ch_rows[m.group(1)] = [m.group(i) for i in range(2, 9)]
    if len(ch_rows) != 3:
        fail(f"endgame chain table rows {len(ch_rows)} != 3")
    n_ch = 0
    for label, key in ch_lbl.items():
        cells = ch_rows[label]
        c, rows_ = eg["summary"]["chain"][key], eg["chain"][key]["rows"]
        t = c["tally"]
        want = [len(rows_), t.get("同一处", 0), t.get("邻近", 0), t.get("漂移", 0),
                t.get("无链", 0)]
        if [int(x) for x in cells[:5]] != want:
            fail(f"endgame chain row out of sync: {label} {cells[:5]} != {want}")
        if cells[5] not in (str(c["median"]), "—"):
            fail(f"endgame chain median out of sync: {label}")
        if int(cells[6].replace(",", "")) != c["anchors"]:
            fail(f"endgame chain anchor count out of sync: {label}")
        if sum(want[1:]) != want[0]:
            fail(f"endgame chain tiers do not sum to marks: {label}")
        n_ch += 1
    # 离群点表：方向/两侧 lb/距 与 JSON 同序同值，引文（去标点）回源
    out_rows = []
    for ln in eg_block.splitlines():
        m = re.match(r"^\| (八十→六十|八十→四十|四十→八十)（链） \| `([0-9a-z]+)` "
                     r"\| `([0-9a-z]+)` \| ([\d,]+) \|", ln)
        if m:
            out_rows.append((m.group(1), m.group(2), m.group(3),
                             int(m.group(4).replace(",", ""))))
    if len(out_rows) != len(eg["chain_outliers"]):
        fail(f"endgame outlier rows {len(out_rows)} != JSON {len(eg['chain_outliers'])}")
    n_oq = 0
    for (label, alb, blb, dist), o in zip(out_rows, eg["chain_outliers"]):
        if (label != {v: k for k, v in ch_lbl.items()}[o["dir"]]
                or alb != o["a"]["lb"] or blb != o["b"]["lb"] or dist != o["dist"]):
            fail(f"endgame outlier row out of sync: {alb}")
        for side in ("a", "b"):
            q = cjk(o[side]["text"])
            if not q or q not in eg_src[o[side]["key"]]:
                fail(f"endgame outlier quote not in source: {o[side]['key']} {alb}")
            n_oq += 1
    # 语族表：三项计数与非善財数
    fam_rows = {}
    for ln in eg_block.splitlines():
        m = re.match(r"^\| (八十|六十|四十) \| (\d+) \| (\d+) \| (\d+) \| (\d+) "
                     r"\| (\d+) \| (\d+) \|", ln)
        if m:
            fam_rows[m.group(1)] = [int(m.group(i)) for i in range(2, 8)]
    if len(fam_rows) != 3:
        fail(f"endgame family table rows {len(fam_rows)} != 3")
    for nm, key in (("八十", "T279"), ("六十", "T278"), ("四十", "T293")):
        f = eg["family"][key]
        k = f["kinds"]
        want = [k.get("辭退", 0), k.get("辭去", 0), k.get("而退", 0),
                k.get("匝…而去", 0), f["total"], f["total"] - f["before_shancai"]]
        if fam_rows[nm] != want:
            fail(f"endgame family row out of sync: {nm} {fam_rows[nm]} != {want}")
        if sum(fam_rows[nm][:4]) != fam_rows[nm][4]:
            fail(f"endgame family kinds do not sum: {nm}")
        if len(f["not_before_lb"]) != f["total"] - f["before_shancai"]:
            fail(f"endgame family non-Shancai lb count mismatch: {nm}")
    if eg["family"]["T279"]["total"] == 53:
        if set(eg["family"]["T279"]["not_before_lb"]) != {"0330c19", "0330c26", "0411a13"}:
            fail("endgame family T279: 非善財三处 lb 与断言不符")
        if "53 不可用作「五十三参」的证成" not in eg_block:
            fail("endgame family: 53→五十三参 boundary statement missing")
    ok(f"endgame chain: {n_ch} directions / {n_oq} outlier quotes re-verified; "
       f"family 53/51/54 with 3 non-Shancai marks asserted")

    # 师名谱系：八十↔六十 五十参分类计数
    pair60 = json.loads((ROOT / "data/research/huayan_80_60_pairwise.json")
                        .read_text(encoding="utf-8"))
    npc = pair60["stats"]["name_counter"]
    m = re.search(r"^\| 八十↔六十 \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$",
                  eg_block, re.M)
    if not m:
        fail("endgame name-genealogy row missing")
    got = [int(x) for x in m.groups()]
    want = [pair60["stats"]["total"], npc.get("全同", 0), npc.get("义近", 0),
            npc.get("基同增衔", 0), npc.get("异", 0)]
    if got != want:
        fail(f"endgame name-genealogy row out of sync: {got} != {want}")
    ok(f"endgame name genealogy: 80↔60 {want} (全同/义近/基同增衔/异)")

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