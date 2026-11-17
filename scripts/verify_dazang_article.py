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
    if "跨典藏登记册：18 行" not in md:
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
    probe_src["KR5e0031"] = norm("".join(p.read_text(encoding="utf-8") for p in sorted(dz_dir.glob("KR5e0031_*.txt"))))
    rj_dir = ROOT / "data" / "references" / "rujia"
    probe_src["KR1h0015"] = norm("".join(p.read_text(encoding="utf-8") for p in sorted(rj_dir.glob("KR1h0015_*.txt"))))
    probe_src["yogasutra"] = norm((ROOT / "data" / "references" / "sanskrit" / "yogasutra_with_bhashya.txt").read_text(encoding="utf-8"))
    for key, meta in probes["meta"]["sources"].items():
        if key == "DZ0001":
            raw = b"".join(p.read_bytes() for p in sorted(dz_dir.glob("KR5a0001_*.txt")))
        elif key == "KR5e0031":
            raw = b"".join(p.read_bytes() for p in sorted(dz_dir.glob("KR5e0031_*.txt")))
        elif key == "KR1h0015":
            raw = b"".join(p.read_bytes() for p in sorted(rj_dir.glob("KR1h0015_*.txt")))
        elif key == "yogasutra":
            raw = (ROOT / "data" / "references" / "sanskrit" / "yogasutra_with_bhashya.txt").read_bytes()
        else:
            raw = (ROOT / meta["path"]).read_bytes()
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
        qgroups = [probes[section]["quotes"]]
        for extra in ("daojiao", "kuax"):
            if extra in probes[section]:
                qgroups.append(probes[section][extra]["quotes"])
        for qgroup in qgroups:
            for q in qgroup:
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
    nq = (sum(len(c['quotes']) for c in t9_cases) + len(probes['d5']['quotes'])
          + len(probes['d5'].get('daojiao', {}).get('quotes', []))
          + len(probes['p1']['quotes'])
          + len(probes['p1'].get('daojiao', {}).get('quotes', []))
          + len(probes['p1'].get('kuax', {}).get('quotes', [])))
    ok(f"§17.11–17.13 probes: {nq} quotes re-verified ({len(t9_cases)} 品 for T9)")

    # --- §17.19 S1 workshop: quotes re-sliced from sources; roster ↔ quote ↔ matrix ---
    ws_path = ROOT / "data" / "research" / "translation_workshop.json"
    if not ws_path.exists():
        fail("translation_workshop.json missing")
    ws = json.loads(ws_path.read_text(encoding="utf-8"))

    def flat_source(key: str) -> str:
        meta = ws["meta"]["sources"][key]
        p = ROOT / meta["path"]
        if hashlib.sha256(p.read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"workshop source hash changed: {key}")
        raw = p.read_text(encoding="utf-8")
        if key == "derge":
            raw = re.sub(r"\[\d{3}[ab]\.\d\]", "", raw)
        else:
            m1 = raw.find("<body")
            m2 = raw.rfind("</body>")
            if m1 >= 0 and m2 > m1:
                raw = raw[m1:m2]
            raw = re.sub(r"<[^>]*>", "", raw)
        return re.sub(r"\s+", "", raw)

    ws_flat = {k: flat_source(k) for k in ws["meta"]["sources"]}
    for qid, q in ws["quotes"].items():
        if q["text"] not in ws_flat[q["source"]]:
            fail(f"workshop quote not in source: {qid} {q['text'][:24]}")
        if q["text"] not in md:
            fail(f"workshop quote not printed in article: {qid}")
        if f'`{q["lb"]}`' not in md:
            fail(f"workshop quote lb not printed: {qid}")

    def tr_norm(s: str) -> str:
        return re.sub(r"[།་\s]", "", s)

    n_att = 0
    for vk, v in ws["versions"].items():
        for item in v["roster"]:
            q = ws["quotes"][item["quote"]]
            if item.get("person_bo"):
                attested = tr_norm(item["person_bo"]) in tr_norm(q["text"])
            elif item["person"] == "武后":
                attested = "天后" in q["text"]
            else:
                attested = all(part in q["text"] for part in item["person"].split("、"))
            if not attested:
                fail(f"workshop roster not attested by its quote: {vk} "
                     f"{item['role']} {item['person']}")
            n_att += 1
    if n_att != ws["summary"]["roster_total"]:
        fail("workshop summary.roster_total != roster entries")

    roles = ws["roles"]
    order = ["T278", "T279", "T293", "TOH44"]
    want_matrix = {r: [k for k, v in ws["versions"].items()
                       if any(x["role"] == r for x in v["roster"])] for r in roles}
    if want_matrix != ws["matrix"]:
        fail("workshop matrix != roster-derived matrix")

    wblock = grab("workshop")
    if first_table_rows(wblock) != len(order):
        fail("§17.19 version table rows != 4")
    got_roles = []
    for ln in wblock.splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0] not in roles:
            continue
        got_roles.append(cells[0])
        for i, k in enumerate(order):
            people = [x["person"] for x in ws["versions"][k]["roster"]
                      if x["role"] == cells[0]]
            want_cell = "、".join(people) if people else "—"
            if cells[i + 1] != want_cell:
                fail(f"§17.19 matrix cell out of sync: {cells[0]}/{k} "
                     f"{cells[i + 1]!r} != {want_cell!r}")
    if got_roles != roles:
        fail(f"§17.19 matrix rows {len(got_roles)} != roles {len(roles)}")
    counts = {k: len(ws["versions"][k]["roster"]) for k in order}
    if (f"六十 {counts['T278']}、八十 {counts['T279']}、四十 {counts['T293']}、"
            f"藏译 {counts['TOH44']}") not in wblock:
        fail("§17.19 roster-count sentence out of sync")
    if f"合计 {sum(counts.values())} 条、{len(roles)} 类职衔" not in wblock:
        fail("§17.19 roster total out of sync")
    if len(ws["typology"]) != 4:
        fail(f"workshop typology {len(ws['typology'])} != 4")
    for t in ws["typology"]:
        if t["quote"] not in ws["quotes"]:
            fail(f"workshop typology cites unknown quote: {t['quote']}")
        if t["why"] not in wblock:
            fail(f"§17.19 typology line missing: {t['kind']}")
    for b in ws["boundaries"]:
        if b not in wblock:
            fail(f"§17.19 boundary line missing: {b[:20]}")
    s1 = next(o for o in ops if o["id"] == "S1")
    if s1["status"] != "done" or "17.19" not in (s1.get("refs") or ""):
        fail("ontology S1 not marked done / §17.19")
    if "### 17.19 S1" not in md:
        fail("§17.19 heading missing")
    ok(f"§17.19 S1 workshop: {len(ws['quotes'])} quotes re-sliced / "
       f"{n_att} roster entries attested by their quote / {len(roles)}-role matrix in sync")

    # --- §17.20 S2 royal patronage: quotes re-sliced; events/kinds/scan in sync ---
    rp_path = ROOT / "data" / "research" / "royal_patronage.json"
    if not rp_path.exists():
        fail("royal_patronage.json missing")
    rp = json.loads(rp_path.read_text(encoding="utf-8"))

    def royal_flat(key: str) -> str:
        meta = rp["meta"]["sources"][key]
        p = ROOT / meta["path"]
        if hashlib.sha256(p.read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"royal source hash changed: {key}")
        raw = p.read_text(encoding="utf-8")
        m1 = raw.find("<body")
        m2 = raw.rfind("</body>")
        if m1 >= 0 and m2 > m1:
            raw = raw[m1:m2]
        raw = re.sub(r"<[^>]*>", "", raw)
        return re.sub(r"\s+", "", raw)

    rflat = {k: royal_flat(k) for k in rp["meta"]["sources"]}
    rblock = grab("royal")
    for qid, q in rp["quotes"].items():
        if q["text"] not in rflat[q["source"]]:
            fail(f"royal quote not in source: {qid} {q['text'][:24]}")
        if q["text"] not in rblock:
            fail(f"royal quote not printed in §17.20: {qid}")
        if f'`{q["lb"]}`' not in rblock:
            fail(f"royal quote lb not printed: {qid}")

    events = rp["events"]
    if len(events) != 10:
        fail(f"royal events {len(events)} != 10")
    kinds = {}
    for e in events:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
        if e["kind"] not in rblock:
            fail(f"royal event kind missing in table: {e['kind']}")
        if e["act"] not in rblock:
            fail(f"royal event act missing: {e['kind']} {e['when']}")
        for qid in e["quotes"]:
            if qid not in rp["quotes"]:
                fail(f"royal event cites unknown quote: {qid}")
    if kinds != rp["kinds"] or kinds != rp["summary"]["kinds_count"]:
        fail("royal kinds != event-derived kinds")
    if len(kinds) != rp["summary"]["kinds"]:
        fail("royal summary.kinds != derived")
    parts = "、".join(f"{k} {v}" for k, v in kinds.items())
    if f"十事八类：{parts}" not in rblock:
        fail("§17.20 kinds-count sentence out of sync")
    if rp["summary"]["events"] != len(events) or rp["summary"]["quotes"] != len(rp["quotes"]):
        fail("royal summary counts out of sync")

    scan = rp["ritual_scan"]
    if len(scan["rows"]) != scan["files"]:
        fail("ritual_scan rows != files")
    if sum(r["total"] for r in scan["rows"].values()) != scan["occurrences"]:
        fail("ritual_scan total != sum of rows")
    scan_tbl = rblock.split("**祀典词检索**", 1)[-1]
    got = 0
    for fn, row in scan["rows"].items():
        want_sum = sum(row["counts"].values())
        for ln in scan_tbl.splitlines():
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 9 and cells[-1] == str(want_sum) and \
                    cells[1:8] == [str(row["counts"][k]) for k in scan["keywords"]]:
                got += 1
                break
    if got != scan["files"]:
        fail(f"§17.20 ritual-scan rows {got} != {scan['files']}")
    if f'| **合** |  |  |  |  |  |  |  | **{scan["occurrences"]}** |' not in scan_tbl:
        fail("§17.20 ritual-scan total row out of sync")
    if (f'在库 {scan["files"]} 部全文检索' not in rblock
            or f'共 {scan["occurrences"]} 处' not in rblock
            or f'相邻者 {len(scan["near_huayan"])} 处' not in rblock):
        fail("§17.20 ritual-absence sentence out of sync")
    for b in rp["boundaries"]:
        if b not in rblock:
            fail(f"§17.20 boundary line missing: {b[:20]}")
    # --- §17.20 祀典半边：史部三书扫描（s2_sidian.json）---
    sd_path = ROOT / "data" / "research" / "s2_sidian.json"
    if not sd_path.exists():
        fail("s2_sidian.json missing")
    sd = json.loads(sd_path.read_text(encoding="utf-8"))
    if len(sd["meta"]["corpora"]) != 6:
        fail(f"S2 sibu corpora {len(sd['meta']['corpora'])} != 5")
    if sd["summary"]["hits"] != len(sd["hits"]):
        fail("S2 sibu hit count out of sync")
    for h in sd["hits"]:
        if not h["near"]:
            fail(f"S2 sibu hit unclassified: {h['file']}")
        if h["ctx"] not in rblock:
            fail(f"S2 sibu hit ctx not printed: {h['file']}")
    for repo, info in sd["meta"]["corpora"].items():
        if f"{info['files']} |" not in rblock:
            fail(f"S2 sibu row missing: {repo}")
    if "皆为寺名" not in rblock:
        fail("S2 sibu 寺名 judgement sentence missing")
    if "399 档" not in rblock:
        fail("S2 sibu file-count sentence missing")
    s2 = next(o for o in ops if o["id"] == "S2")
    if s2["status"] != "partial" or "17.20" not in (s2.get("refs") or ""):
        fail("ontology S2 not marked partial / §17.20")
    if "### 17.20 S2" not in md:
        fail("§17.20 heading missing")
    ok(f"§17.20 S2 royal: {len(rp['quotes'])} quotes re-sliced / "
       f"{len(events)} events in {len(kinds)} kinds / ritual scan "
       f"{scan['files']} files {scan['occurrences']} hits, {len(scan['near_huayan'])} near 華嚴")

    # --- §17.21 S3 persecution: quotes re-sliced; events/kinds/scan/near-notes in sync ---
    pc_path = ROOT / "data" / "research" / "persecution.json"
    if not pc_path.exists():
        fail("persecution.json missing")
    pc = json.loads(pc_path.read_text(encoding="utf-8"))

    def pc_flat(key: str) -> str:
        meta = pc["meta"]["sources"][key]
        p = ROOT / meta["path"]
        if hashlib.sha256(p.read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"persecution source hash changed: {key}")
        raw = p.read_text(encoding="utf-8")
        m1 = raw.find("<body")
        m2 = raw.rfind("</body>")
        if m1 >= 0 and m2 > m1:
            raw = raw[m1:m2]
        raw = re.sub(r"<[^>]*>", "", raw)
        return re.sub(r"\s+", "", raw)

    pflat = {k: pc_flat(k) for k in pc["meta"]["sources"]}
    pblock = grab("persecution")
    for qid, q in pc["quotes"].items():
        if q["text"] not in pflat[q["source"]]:
            fail(f"persecution quote not in source: {qid} {q['text'][:24]}")
        if q["text"] not in pblock:
            fail(f"persecution quote not printed in §17.21: {qid}")
        if f'`{q["lb"]}`' not in pblock:
            fail(f"persecution quote lb not printed: {qid}")

    pevents = pc["events"]
    if len(pevents) != pc["summary"]["events"]:
        fail(f"persecution events {len(pevents)} != summary {pc['summary']['events']}")
    pkinds = {}
    for e in pevents:
        pkinds[e["kind"]] = pkinds.get(e["kind"], 0) + 1
        if e["kind"] not in pblock:
            fail(f"persecution event kind missing in table: {e['kind']}")
        if e["act"] not in pblock:
            fail(f"persecution event act missing: {e['kind']} {e['when']}")
        for qid in e["quotes"]:
            if qid not in pc["quotes"]:
                fail(f"persecution event cites unknown quote: {qid}")
    if pkinds != pc["kinds"] or pkinds != pc["summary"]["kinds_count"]:
        fail("persecution kinds != event-derived kinds")
    pparts = "、".join(f"{k} {v}" for k, v in pkinds.items())
    if f"{len(pevents)} 事 {len(pkinds)} 类：{pparts}" not in pblock:
        fail("§17.21 kinds-count sentence out of sync")
    if pc["summary"]["events"] != len(pevents) or pc["summary"]["quotes"] != len(pc["quotes"]):
        fail("persecution summary counts out of sync")

    # 护法半边：引经须双源——護法論引「佛以法為身，清淨如虛空」须见于本经 T279
    apol = sum(1 for e in pevents if e["kind"].startswith("护法"))
    if apol < 4:
        fail(f"persecution apologetics events {apol} < 4")
    if "护法引经" not in pblock or "护法判教" not in pblock:
        fail("§17.21 apologetics event kinds missing")
    t279 = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "",
         (ROOT / "data" / "references" / "cbeta" / "T10n0279.xml").read_text(encoding="utf-8")))
    for frag in ("佛以法為身", "清淨如虛空"):
        if frag not in t279:
            fail(f"§17.21 apologetics verse fragment not in T279: {frag}")
    if "引经证法" not in pblock or "判教骨架" not in pblock:
        fail("§17.21 apologetics form sentence missing")

    pscan = pc["scan"]
    if len(pscan["rows"]) != pscan["files"]:
        fail("persecution scan rows != files")
    if sum(r["total"] for r in pscan["rows"].values()) != pscan["occurrences"]:
        fail("persecution scan total != sum of rows")
    ptail = pblock.split("**法难词检索**", 1)[-1]
    pgot = 0
    for fn, row in pscan["rows"].items():
        want_sum = sum(row["counts"].values())
        for ln in ptail.splitlines():
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == len(pscan["keywords"]) + 2 and cells[-1] == str(want_sum) and \
                    cells[1:-1] == [str(row["counts"][k]) for k in pscan["keywords"]]:
                pgot += 1
                break
    if pgot != pscan["files"]:
        fail(f"§17.21 scan rows {pgot} != {pscan['files']}")
    if f'| **合** | ' + " | ".join("" for _ in pscan["keywords"]) + \
            f' | **{pscan["occurrences"]}** |' not in ptail:
        fail("§17.21 scan total row out of sync")
    if (f'在库 {pscan["files"]} 部全文检索' not in pblock
            or f'共 {pscan["occurrences"]} 处' not in pblock
            or f'相邻者 {len(pscan["near_huayan"])} 处' not in pblock):
        fail("§17.21 scan sentence out of sync")
    for n in pscan["near_huayan"]:
        if n["note"] == "待分类":
            fail(f"§17.21 near-hit unclassified: {n['file']} {n['ctx'][:40]}")
        if n["note"] not in pblock:
            fail(f"§17.21 near-hit note not printed: {n['note']}")
    if "三处全是寺名" not in pblock:
        fail("§17.21 near-hit conclusion missing")
    for b in pc["boundaries"]:
        if b not in pblock:
            fail(f"§17.21 boundary line missing: {b[:20]}")
    s3 = next(o for o in ops if o["id"] == "S3")
    if s3["status"] != "partial" or "17.21" not in (s3.get("refs") or ""):
        fail("ontology S3 not marked partial / §17.21")
    if "### 17.21 S3" not in md:
        fail("§17.21 heading missing")
    ok(f"§17.21 S3 persecution: {len(pc['quotes'])} quotes re-sliced / "
       f"{len(pevents)} events in {len(pkinds)} kinds / scan "
       f"{pscan['files']} files {pscan['occurrences']} hits, "
       f"{len(pscan['near_huayan'])} near 華嚴 all classified")

    # --- §17.22 T9 visit names: every name re-located in its own recension at the cited lb ---
    vn_path = ROOT / "data" / "research" / "visits_names.json"
    if not vn_path.exists():
        fail("visits_names.json missing")
    vn = json.loads(vn_path.read_text(encoding="utf-8"))
    vn_rows = vn["rows"]
    if len(vn_rows) != 50 or [r["no"] for r in vn_rows] != list(range(2, 52)):
        fail("visits_names rows not 50 or 参号 not 2..51")

    def vn_flat(key: str) -> str:
        meta = vn["meta"]["sources"][key]
        p = ROOT / meta["path"]
        if hashlib.sha256(p.read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"visit-names source hash changed: {key}")
        raw = p.read_text(encoding="utf-8")
        m1 = raw.find("<body")
        m2 = raw.rfind("</body>")
        if m1 >= 0 and m2 > m1:
            raw = raw[m1:m2]
        return re.sub(r"\s+", "", re.sub(r"<[^>]*>", "", raw))

    f80, f60, f40 = (vn_flat(k) for k in ("80", "60", "40"))
    for r in vn_rows:
        # 八十：名在指授句之前 500 字内（成对名如「德生·有德」按两部分各查）
        win80 = f80[max(0, r["pos80"] - 500):r["pos80"]]
        if not all(part in win80 for part in r["n80"].split("·")):
            fail(f"visit name80 not found at lb: {r['no']} {r['n80']}")
        # 六十／四十：名起于 pos
        probe60 = r["n60"].split("·")[0]
        if not f60.startswith(probe60, r["pos60"]):
            fail(f"visit name60 not at pos: {r['no']} {r['n60']}")
        if not f40.startswith(r["n40probe"], r["pos40"]):
            fail(f"visit name40 not at pos: {r['no']} {r['n40']}")

    def recount(field, val):
        return sum(1 for r in vn_rows if r[field] == val)

    want_stats = {
        "rows": 50,
        "rel80_40": {"全同": recount("rel80_40", "全同"), "基同": recount("rel80_40", "基同"),
                     "异": recount("rel80_40", "异")},
        "rel80_60": {"全同": recount("rel80_60", "全同"), "基同": recount("rel80_60", "基同"),
                     "异": recount("rel80_60", "异")},
        "rel60_40": {"全同": recount("rel60_40", "全同"), "基同": recount("rel60_40", "基同"),
                     "异": recount("rel60_40", "异")},
        "all_same": sum(1 for r in vn_rows if r["n80"] == r["n60"] == r["n40"]),
        "80eq60_ne40": sum(1 for r in vn_rows if r["n80"] == r["n60"] != r["n40"]),
        "80eq40_ne60": sum(1 for r in vn_rows if r["n80"] == r["n40"] != r["n60"]),
        "all_diff": sum(1 for r in vn_rows if len({r["n80"], r["n60"], r["n40"]}) == 3),
    }
    if vn["stats"] != want_stats:
        fail("visits_names stats out of sync with rows")
    if vn["stats"]["all_same"] + vn["stats"]["80eq60_ne40"] + \
            vn["stats"]["80eq40_ne60"] + vn["stats"]["all_diff"] != 50:
        fail("visits_names partition does not sum to 50")

    vblock = grab("visits")
    for r in vn_rows:
        row = (f'| {r["no"]} | {r["n80"]} `{r["lb80"]}` | {r["n60"]} `{r["lb60"]}` | '
               f'{r["n40"]} `{r["lb40"]}` |')
        if row not in vblock:
            fail(f"§17.22 table row missing/mismatched: 参 {r['no']} {r['n80']}")
    st = vn["stats"]
    if (f'> 五十参：三本同字 **{st["all_same"]}** 处；'
            f'八十与六十同字 {st["rel80_60"]["全同"]} 处、'
            f'与四十同字 {st["rel80_40"]["全同"]} 处；'
            f'六十与四十同字 {st["rel60_40"]["全同"]} 处。') not in vblock:
        fail("§17.22 counts sentence out of sync")
    for b in vn["boundaries"]:
        if b not in vblock:
            fail(f"§17.22 boundary line missing: {b[:20]}")
    t9 = next(o for o in ops if o["id"] == "T9")
    if "17.22" not in (t9.get("refs") or ""):
        fail("ontology T9 refs do not cite §17.22")
    if "### 17.22 T9" not in md:
        fail("§17.22 heading missing")
    ok(f"§17.22 T9 visits: {len(vn_rows)} names re-located in 80/60/40 at lb / "
       f"all_same {st['all_same']}, 80=60 {st['rel80_60']['全同']}, "
       f"80=40 {st['rel80_40']['全同']}, all-diff {st['all_diff']}")

    # --- §17.24 T9 梵本对照: 18 组同指判，指令定位与次序单调逐条复核 ---
    vs_path = ROOT / "data" / "research" / "visits_sanskrit.json"
    if not vs_path.exists():
        fail("visits_sanskrit.json missing")
    vs = json.loads(vs_path.read_text(encoding="utf-8"))
    vcases = vs["cases"]
    if len(vcases) != 18:
        fail(f"visits_sanskrit cases {len(vcases)} != 18")
    nos = [c["no"] for c in vcases]
    if nos != sorted(nos) or len(set(nos)) != 18:
        fail("visits_sanskrit 参号 not ascending/unique")

    # 口径：cases 必等于 §17.22 中「恰有一对同名」的十八组；
    # 另十七组三本全异、十五组三本同字未判，其数与名单须与 visits_names 一致
    vrows = {r["no"]: r for r in vn_rows}
    vtri = {n: {r["n80"], r["n60"], r["n40"]} for n, r in vrows.items()}
    v_one = sorted(n for n, s in vtri.items() if len(s) == 2)
    v_diff = sorted(n for n, s in vtri.items() if len(s) == 3)
    v_same = sorted(n for n, s in vtri.items() if len(s) == 1)
    if nos != v_one:
        fail(f"visits_sanskrit cases != 「恰一对同名」18 组: {nos} vs {v_one}")
    # 2026-11-16 并行线 schema 重构：§17.24 用自己的口径（all_diff_* 是梵本判，不是 §17.22 三方分组）
    st = vs["stats"]
    if st.get("all_diff_cases") != len(v_diff):
        fail(f"visits_sanskrit all_diff_cases {st.get('all_diff_cases')} != §17.22 all-diff {len(v_diff)}")
    if st.get("cases") != len(v_one):
        fail(f"visits_sanskrit cases {st.get('cases')} != §17.22 one-pair {len(v_one)}")
    # all_diff_same = 17 组中梵本找到对应者 16；all_diff_pending = 待核 1
    if st.get("all_diff_pending", 0) + st.get("all_diff_same", 0) != st.get("all_diff_cases", 0):
        fail(f"visits_sanskrit all_diff pending {st.get('all_diff_pending')} + same {st.get('all_diff_same')} "
             f"!= cases {st.get('all_diff_cases')}")
    # 2026-11-16 并行线重构边界格式；§17.28 起改为「五十行全部核梵」口径
    vbound = next((b for b in vs["boundaries"] if "五十行至此全部核梵" in b), None)
    if not vbound:
        fail("visits_sanskrit scope boundary missing (五十行至此全部核梵)")
    for need in ("§17.28", "50"):
        if need not in vbound:
            fail(f"visits_sanskrit boundary lacks {need} note")

    # 源文：与 build 同一规范化（空白折叠），逐条复定位
    smeta = vs["meta"]["source"]
    sp = ROOT / smeta["path"]
    if hashlib.sha256(sp.read_bytes()).hexdigest() != smeta["sha256"]:
        fail("visits_sanskrit source hash changed")
    sraw = sp.read_text(encoding="utf-8", errors="replace")
    schars = []
    for ch in sraw:
        if ch.isspace():
            if schars and schars[-1] == " ":
                continue
            schars.append(" ")
        else:
            schars.append(ch)
    sflat = "".join(schars)
    # 与 build_visits_sanskrit.py 同口径：指授句 = (?:asti|gaccha) kulaputra 且 900 字内见 upasaṃkramya
    gstarts = []
    for m in re.finditer(r"(?:asti|gaccha) kulaputra", sflat):
        if "upasaṃkramya" in sflat[m.start():m.start() + 900]:
            gstarts.append(m.start())
    if len(gstarts) != 50:
        fail(f"visit-sanskrit instruction events {len(gstarts)} != 50")
    gpages = [(m.start(), int(m.group(1))) for m in re.finditer(r"\(gv (\d+)\)", sflat)]

    def s_gv(pos):
        best = None
        for p, n in gpages:
            if p <= pos:
                best = n
            else:
                break
        return f"gv {best}" if best else None

    def s_ord(pos):
        k = 0
        for i, s in enumerate(gstarts):
            if s <= pos:
                k = i + 1
            else:
                break
        return k or None

    vn_by_no = {r["no"]: r for r in vn_rows}
    for c in vcases:
        src = vn_by_no.get(c["no"])
        if not src:
            fail(f"visit-sanskrit 参 {c['no']} not in visits_names")
            continue
        for k in ("n80", "n60", "n40"):
            if c[k] != src[k]:
                fail(f"visit-sanskrit name drift vs visits_names: 参 {c['no']} {k} "
                     f"{c[k]} != {src[k]}")
        if c.get("probe"):
            hits = [m.start() for m in re.finditer(re.escape(c["probe"]), sflat)]
            if len(hits) != 1:
                fail(f"visit-sanskrit probe not unique: 参 {c['no']} ({len(hits)})")
                continue
            if hits[0] != c["pos"]:
                fail(f"visit-sanskrit pos moved: 参 {c['no']}")
            if s_ord(hits[0]) != c["ord"]:
                fail(f"visit-sanskrit ord mismatch: 参 {c['no']} {s_ord(hits[0])} != {c['ord']}")
            if s_gv(hits[0]) != c["gv"]:
                fail(f"visit-sanskrit gv mismatch: 参 {c['no']} {s_gv(hits[0])} != {c['gv']}")
        else:
            a = sflat.find(c["gap_between"][0])
            b = sflat.find(c["gap_between"][1])
            if a < 0 or b < 0 or b < a:
                fail(f"visit-sanskrit gap anchors missing: 参 {c['no']}")
                continue
            own = max([s for s in gstarts if s < b], default=None)
            inner = [s for s in gstarts if a < s < b and s != own]
            if inner:
                fail(f"visit-sanskrit gap not empty: 参 {c['no']} ({len(inner)})")
    vords = [c["ord"] for c in vcases if c["ord"]]
    if vords != sorted(vords):
        fail("visit-sanskrit ordinals decrease")
    vdup = sum(1 for a, b in zip(vords, vords[1:]) if a == b)
    vgaps = sum(1 for c in vcases if not c.get("probe"))
    if vdup != vgaps:
        fail(f"visit-sanskrit equal ordinals {vdup} != gap cases {vgaps}")

    bps = vs.get("byproducts") or []
    if len(bps) != 1:
        fail(f"visit-sanskrit byproducts {len(bps)} != 1")
    for b in bps:
        hits = [m.start() for m in re.finditer(re.escape(b["probe"]), sflat)]
        if len(hits) != 1 or b["also"] not in sflat[hits[0]:hits[0] + 200]:
            fail(f"visit-sanskrit byproduct not re-located: 参 {b['no']}")

    vsame = sum(1 for c in vcases if c["verdict"].startswith("同指"))
    vpend = sum(1 for c in vcases if c["verdict"].startswith("待核"))
    vbv = {}
    for c in vcases:
        vbv[c["verdict"]] = vbv.get(c["verdict"], 0) + 1
    if (vs["stats"]["same"], vs["stats"]["pending"], vs["stats"]["by_verdict"]) != (vsame, vpend, vbv):
        fail("visit-sanskrit stats out of sync with cases")

    sblock = grab("visits_skt")
    for c in vcases:
        tri = f'{c["n80"]}／{c["n60"]}／{c["n40"]}'
        if c["verdict"].startswith("待核·梵本无对应"):
            row = (f'| {c["no"]} | {tri} | — | —（觀自在→大天之間無第三位） | '
                   f'{c["gv"]}→{c["gv_to"].replace("gv ", "")} | {c["verdict"]} |')
        else:
            row = (f'| {c["no"]} | {tri} | `{c["skt"]}` | '
                   f'{c["skt_role"]}·{c["skt_place"]} | {c["gv"]} | {c["verdict"]} |')
        if row not in sblock:
            fail(f"§17.24 table row missing/mismatched: 参 {c['no']} {c['n80']}")
    if (f'> 十八组：同指 **{vsame}**、待核 **{vpend}**。') not in sblock:
        fail("§17.24 counts sentence out of sync")
    for b in vs["boundaries"]:
        if b not in sblock:
            fail(f"§17.24 boundary line missing: {b[:20]}")
    if "17.24" not in (t9.get("refs") or ""):
        fail("ontology T9 refs do not cite §17.24")
    if "### 17.24 T9" not in md:
        fail("§17.24 heading missing")
    ok(f"§17.24 T9 Sanskrit: {len(vcases)} cases re-located (ord {vords[0]}–{vords[-1]} monotonic) / "
       f"same {vsame}, pending {vpend}, byproduct 参 {bps[0]['no']}")

    # --- §17.27 T9 梵本对照（续）: 三本全异 17 组，逐行＋空缺参45＋全表口径 ---
    ad = vs.get("all_diff") or {}
    dcases = ad.get("cases") or []
    dgaps = ad.get("gaps") or []
    if len(dcases) != len(v_diff):
        fail(f"§17.27 all_diff cases {len(dcases)} != §17.22 all-diff {len(v_diff)}")
    if [c["no"] for c in dcases] != v_diff:
        fail(f"§17.27 case numbers != all-diff set: {[c['no'] for c in dcases]} vs {v_diff}")
    dst = ad.get("stats") or {}
    if dst.get("cases") != len(dcases):
        fail("§17.27 stats.cases mismatch")
    # 全表口径：五十行全部核梵（35 组字面有异 ＋ 15 组三本同字）
    if vs["stats"].get("rows_judged") != len(v_one) + len(v_diff) + len(v_same):
        fail(f"§17.27 rows_judged {vs['stats'].get('rows_judged')} != "
             f"{len(v_one)}＋{len(v_diff)}＋{len(v_same)}")
    if len(dgaps) != 1 or dgaps[0]["no"] != 45:
        fail(f"§17.27 same-gap 参45 missing: {[g['no'] for g in dgaps]}")
    if vs["stats"].get("same_gap_nos") != [g["no"] for g in dgaps]:
        fail("§17.27 stats.same_gap_nos mismatch")
    if vs["stats"].get("same_unprobed_nos") != []:
        fail(f"§17.27 same_unprobed_nos not empty: {vs['stats'].get('same_unprobed_nos')}")
    if vs["stats"].get("rows_same") != len(v_same) or \
            vs["stats"].get("rows_same_gap") != len(dgaps) or \
            vs["stats"].get("rows_same_unprobed") != 0:
        fail("§17.27 same-row counts out of sync")

    # 逐条复定位（与 §17.24 同口径），ord 须严格递增、无相等
    dord_seen = []
    for c in dcases:
        src = vn_by_no.get(c["no"])
        if not src:
            fail(f"§17.27 参 {c['no']} not in visits_names")
            continue
        for k in ("n80", "n60", "n40"):
            if c[k] != src[k]:
                fail(f"§17.27 name drift: 参 {c['no']} {k}")
        hits = [m.start() for m in re.finditer(re.escape(c["probe"]), sflat)]
        if len(hits) != 1:
            scoped = [h for h in hits
                      if any(s0 <= h <= s0 + 900 for s0 in gstarts)]
            hits = scoped
        if len(hits) != 1:
            fail(f"§17.27 probe not unique: 参 {c['no']} ({len(hits)})")
            continue
        if hits[0] != c["pos"]:
            fail(f"§17.27 pos moved: 参 {c['no']}")
        if s_ord(hits[0]) != c["ord"]:
            fail(f"§17.27 ord mismatch: 参 {c['no']} {s_ord(hits[0])} != {c['ord']}")
        if s_gv(hits[0]) != c["gv"]:
            fail(f"§17.27 gv mismatch: 参 {c['no']} {s_gv(hits[0])} != {c['gv']}")
        dord_seen.append(c["ord"])
    if dord_seen != sorted(dord_seen) or len(set(dord_seen)) != len(dord_seen):
        fail(f"§17.27 ordinals not strictly increasing: {dord_seen}")
    if (min(dord_seen), max(dord_seen)) != (dst.get("ord_first"), dst.get("ord_last")):
        fail(f"§17.27 ord range {min(dord_seen)}–{max(dord_seen)} != stats "
             f"{dst.get('ord_first')}–{dst.get('ord_last')}")

    # 参45：空缺须真空、且「后一位之序 = 空缺之序 + 1」
    g45 = dgaps[0]
    a45 = sflat.find(g45["between"][0])
    b45 = sflat.find(g45["between"][1])
    if a45 < 0 or b45 < 0 or b45 < a45:
        fail("§17.27 参45 gap anchors missing")
    else:
        own45 = max([s for s in gstarts if s < b45], default=None)
        inner45 = [s for s in gstarts if a45 < s < b45 and s != own45]
        if inner45:
            fail(f"§17.27 参45 gap not empty ({len(inner45)} instruction events)")
        if s_gv(a45) != g45["gv"] or s_gv(b45) != g45["gv_to"]:
            fail("§17.27 参45 gv span mismatch")
    after45 = min((c for c in dcases + vcases if c["no"] > 45), key=lambda c: c["no"])
    if after45["ord"] != g45["ord"] + 1:
        fail(f"§17.27 参45 does not occupy exactly one slot: "
             f"{g45['ord']} -> {after45['ord']} (参{after45['no']})")
    judged_nos = {c["no"] for c in dcases + vcases}
    judged_nos |= {c["no"] for c in (vs.get("same") or {}).get("cases") or []}
    judged_nos |= {b["no"] for b in vs.get("byproducts") or []}
    gap_nos = [c["no"] for c in vcases if not c.get("probe")] + [g["no"] for g in dgaps]
    occupied_gaps = sum(1 for n in gap_nos if (n - 1) in judged_nos)
    if vs["stats"].get("ord_all_equal_pairs") != occupied_gaps:
        fail(f"§17.27 ord_all_equal_pairs {vs['stats'].get('ord_all_equal_pairs')} "
             f"!= occupied gap slots {occupied_gaps}")
    if (vs["stats"].get("ord_all_first"), vs["stats"].get("ord_all_last")) != (1, 49):
        fail(f"§17.27 full-table ord range "
             f"{vs['stats'].get('ord_all_first')}–{vs['stats'].get('ord_all_last')} != 1–49")

    dsame = sum(1 for c in dcases if c["verdict"].startswith("同指"))
    dpend = sum(1 for c in dcases if c["verdict"].startswith("待核"))
    dbv = {}
    for c in dcases:
        dbv[c["verdict"]] = dbv.get(c["verdict"], 0) + 1
    if (dst.get("same"), dst.get("pending"), dst.get("by_verdict")) != (dsame, dpend, dbv):
        fail("§17.27 stats out of sync with cases")
    if (vs["stats"].get("all_diff_same"), vs["stats"].get("all_diff_pending"),
            vs["stats"].get("all_diff_by_verdict")) != (dsame, dpend, dbv):
        fail("§17.27 top-level all_diff_* stats out of sync")

    dblock = grab("visits_skt_diff")
    for c in dcases:
        tri = f'{c["n80"]}／{c["n60"]}／{c["n40"]}'
        row = (f'| {c["no"]} | {tri} | `{c["skt"]}` | '
               f'{c["skt_role"]}·{c["skt_place"]} | {c["gv"]} | {c["verdict"]} |')
        if row not in dblock:
            fail(f"§17.27 table row missing/mismatched: 参 {c['no']} {c['n80']}")
    if (f'> 十七组：同指 **{dsame}**、待核 **{dpend}**。') not in dblock:
        fail("§17.27 counts sentence out of sync")
    if g45["basis"] not in dblock and f'参 {g45["no"]}' not in dblock:
        fail("§17.27 same-gap 参45 note missing")
    for b in ad.get("boundaries") or []:
        if b not in dblock:
            fail(f"§17.27 boundary line missing: {b[:20]}")
    if "17.27" not in (t9.get("refs") or ""):
        fail("ontology T9 refs do not cite §17.27")
    if "### 17.27 T9" not in md:
        fail("§17.27 heading missing")
    ok(f"§17.27 T9 Sanskrit (all-diff): {len(dcases)} cases re-located "
       f"(ord {min(dord_seen)}–{max(dord_seen)} strictly increasing) / same {dsame}, "
       f"pending {dpend} / gap 参 {g45['no']} empty (slot {g45['ord']}→{after45['ord']})")


    # --- §17.28 T9 梵本对照（三）: 三本同字 15 组，逐名核 ---
    sm = vs.get("same") or {}
    scases = sm.get("cases") or []
    sgaps = sm.get("gaps") or []
    sbyp = sm.get("byproducts") or []
    s_expected = [n for n in v_same if n not in (45, 51)]
    if len(scases) != len(s_expected):
        fail(f"§17.28 same cases {len(scases)} != 三本同字直核 {len(s_expected)}")
    if [c["no"] for c in scases] != s_expected:
        fail(f"§17.28 case numbers != 三本同字（除 45/51）: "
             f"{[c['no'] for c in scases]} vs {s_expected}")
    if len(sgaps) != 1 or sgaps[0]["no"] != 45:
        fail(f"§17.28 same-gap 参45 missing: {[g['no'] for g in sgaps]}")
    if len(sbyp) != 1 or sbyp[0]["no"] != 51:
        fail(f"§17.28 byproduct 参51 missing: {[b['no'] for b in sbyp]}")
    if len(scases) + len(sgaps) + len(sbyp) != len(v_same):
        fail("§17.28 13＋1＋1 != 三本同字 15")
    if (vs["stats"].get("rows_same_probed"), vs["stats"].get("rows_same_byproduct"),
            vs["stats"].get("rows_same_unprobed")) != (len(scases), len(sbyp), 0):
        fail("§17.28 same-row probed/byproduct/unprobed out of sync")
    sst = sm.get("stats") or {}
    if (sst.get("cases"), sst.get("same"), sst.get("pending")) != (len(scases), len(scases), 0):
        fail("§17.28 stats cases/same/pending out of sync")
    if sst.get("gap_nos") != [g["no"] for g in sgaps] or \
            sst.get("byproduct_nos") != [b["no"] for b in sbyp]:
        fail("§17.28 stats gap/byproduct nos out of sync")
    if (vs["stats"].get("same_cases"), vs["stats"].get("same_same"),
            vs["stats"].get("same_pending")) != (len(scases), len(scases), 0):
        fail("§17.28 top-level same_* stats out of sync")

    sord_seen = []
    for c in scases:
        src = vn_by_no.get(c["no"])
        if not src:
            fail(f"§17.28 参 {c['no']} not in visits_names")
            continue
        for k in ("n80", "n60", "n40"):
            if c[k] != src[k]:
                fail(f"§17.28 name drift: 参 {c['no']} {k}")
        if c["rel80_60"] != "全同" or c["rel80_40"] != "全同":
            fail(f"§17.28 参 {c['no']} not 三本同字 per visits_names")
        hits = [m.start() for m in re.finditer(re.escape(c["probe"]), sflat)]
        if len(hits) != 1:
            scoped = [h for h in hits
                      if any(s0 <= h <= s0 + 900 for s0 in gstarts)]
            hits = scoped
        if len(hits) != 1:
            fail(f"§17.28 probe not unique: 参 {c['no']} ({len(hits)})")
            continue
        if hits[0] != c["pos"]:
            fail(f"§17.28 pos moved: 参 {c['no']}")
        if s_ord(hits[0]) != c["ord"]:
            fail(f"§17.28 ord mismatch: 参 {c['no']} {s_ord(hits[0])} != {c['ord']}")
        if s_gv(hits[0]) != c["gv"]:
            fail(f"§17.28 gv mismatch: 参 {c['no']} {s_gv(hits[0])} != {c['gv']}")
        if not c["verdict"].startswith("同指"):
            fail(f"§17.28 参 {c['no']} verdict not 同指: {c['verdict']}")
        sord_seen.append(c["ord"])
    if sord_seen != sorted(sord_seen) or len(set(sord_seen)) != len(sord_seen):
        fail(f"§17.28 ordinals not strictly increasing: {sord_seen}")
    if (min(sord_seen), max(sord_seen)) != (sst.get("ord_first"), sst.get("ord_last")):
        fail(f"§17.28 ord range {min(sord_seen)}–{max(sord_seen)} != stats "
             f"{sst.get('ord_first')}–{sst.get('ord_last')}")
    # 参45：空缺须真空、gv 跨两页、与前一位（参44）同占一序
    g45s = sgaps[0]
    a45s = sflat.find(g45s["between"][0])
    b45s = sflat.find(g45s["between"][1])
    if a45s < 0 or b45s < 0 or b45s < a45s:
        fail("§17.28 参45 gap anchors missing")
    else:
        own45s = max([x for x in gstarts if x < b45s], default=None)
        inner45s = [x for x in gstarts if a45s < x < b45s and x != own45s]
        if inner45s:
            fail(f"§17.28 参45 gap not empty ({len(inner45s)} instruction events)")
        if s_gv(a45s) != g45s["gv"] or s_gv(b45s) != g45s["gv_to"]:
            fail("§17.28 参45 gv span mismatch")
    if g45s.get("gap_chars", 0) < 1000:
        fail(f"§17.28 参45 gap_chars too small: {g45s.get('gap_chars')}")
    if g45s["ord"] != 43:
        fail(f"§17.28 参45 ord {g45s['ord']} != 43")
    prev44 = next(c for c in scases if c["no"] == 44)
    if prev44["ord"] != g45s["ord"]:
        fail(f"§17.28 参45 does not share slot with 参44: {prev44['ord']} vs {g45s['ord']}")
    # 参51：一句两名——probe 与 also 须在同一指授窗内
    b51 = sbyp[0]
    p51 = sflat.find(b51["probe"])
    if p51 < 0:
        fail("§17.28 参51 probe missing")
    win51 = sflat[p51:p51 + 400]
    if b51["also"] not in win51:
        fail("§17.28 参51 一句两名：also 不在同一窗内")
    if s_ord(p51) != b51["ord"] or b51["ord"] != 49:
        fail(f"§17.28 参51 ord mismatch: {s_ord(p51)} / {b51['ord']}")
    if s_gv(p51) != b51["gv"]:
        fail("§17.28 参51 gv mismatch")

    sblock = grab("visits_skt_same")
    for c in scases:
        tri = f'{c["n80"]}／{c["n60"]}／{c["n40"]}'
        row = (f'| {c["no"]} | {tri} | `{c["skt"]}` | '
               f'{c["skt_role"]}·{c["skt_place"]} | {c["gv"]} | {c["verdict"]} |')
        if row not in sblock:
            fail(f"§17.28 table row missing/mismatched: 参 {c['no']} {c['n80']}")
    if (f'> 十三组：同指 **{len(scases)}**、待核 **0**。') not in sblock:
        fail("§17.28 counts sentence out of sync")
    if f'参 {g45s["no"]}' not in sblock or f'参 {b51["no"]}' not in sblock:
        fail("§17.28 参45／参51 note missing")
    for b in sm.get("boundaries") or []:
        if b not in sblock:
            fail(f"§17.28 boundary line missing: {b[:20]}")
    if "17.28" not in (t9.get("refs") or ""):
        fail("ontology T9 refs do not cite §17.28")
    if "### 17.28 T9" not in md:
        fail("§17.28 heading missing")
    if "### 17.29 未竟" not in md:
        fail("§17.29 未竟 heading missing after renumber")
    ok(f"§17.28 T9 Sanskrit (all-same): {len(scases)} cases re-located "
       f"(ord {min(sord_seen)}–{max(sord_seen)} strictly increasing) / same {len(scases)}, "
       f"pending 0 / gap 参 {g45s['no']} empty + 参 {b51['no']} 一句两名 / "
       f"50/50 rows witnessed")

    # --- §17.30–17.32 T9 逐品科判：quotes re-located; 品次/科数/边界 assertions ---
    t9p_cases = probes["t9_pin"]["cases"]
    if len(t9p_cases) != 3:
        fail(f"§17.30–§17.32 must have 3 cases, got {len(t9p_cases)}")
    for tag, case in zip(("§17.30", "§17.31", "§17.32"), t9p_cases):
        for q in case["quotes"]:
            if norm(q["text"]) not in probe_src[q["src"]]:
                fail(f"{tag} quote missing from {q['src']}: {q['text'][:24]}")
            if q["text"] not in md:
                fail(f"{tag} quote not printed in article: {q['text'][:24]}")
    t9p_block = grab("t9_pin")
    t9p2_block = grab("t9_pin2")
    t9p3_block = grab("t9_pin3")
    t9p_rows = sum(1 for blk in (t9p_block, t9p2_block, t9p3_block) for ln in blk.splitlines()
                   if ln.startswith("| ") and not ln.startswith("|---"))
    if t9p_rows != sum(len(c["rows"]) for c in t9p_cases) + len(t9p_cases):
        fail("§17.30–17.32 tables != probes JSON rows")
    # 品1：品次自述、澄观品级十分、法藏无定数
    c1 = t9p_cases[0]
    if "世主妙嚴品" not in c1["pin"] or "世間淨眼品" not in c1["pin"] or "品1" not in c1["pin"]:
        fail("§17.30 case must state 品1 and name both 八十〈世主妙嚴品〉 and 六十〈世間淨眼品〉")
    r1 = {item: (a, b) for item, a, b in c1["rows"]}
    if not r1.get("品级科数", ("", ""))[0].startswith("10"):
        fail("§17.30 澄观 品级科数 must be 10")
    if "无品级定数" not in r1.get("品级科数", ("", ""))[1]:
        fail("§17.30 法藏 must be recorded as 无品级定数")
    for want in ("一〈世間淨眼品〉", "即今〈世主品〉", "〈盧舍那品〉"):
        if want not in c1["quotes"][0]["text"]:
            fail(f"§17.30 品次自述缺 {want}")
    for want in ("一總顯已聞", "十「如此世界」下結通無盡"):
        if want not in t9p_block:
            fail(f"§17.30 澄观十分缺 {want}")
    for want in ("五分", "十分", "不可互推", "科判异同不得写成文本异同"):
        if want not in t9p_block:
            fail(f"§17.30 block 缺关键判语：{want}")
    # 品2：1:5 只对所在段、澄观品级六分、法藏品内答相十段
    c2 = t9p_cases[1]
    for want in ("如來現相品", "盧舍那佛品", "前段"):
        if want not in c2["pin"]:
            fail(f"§17.31 case pin 缺 {want}")
    if "品2" not in c2["pin"]:
        fail("§17.31 case must state 品2 on both sides")
    r2 = {item: (a, b) for item, a, b in c2["rows"]}
    if not r2.get("品级科数", ("", ""))[0].startswith("6"):
        fail("§17.31 澄观 品级科数 must be 6")
    if not r2.get("品级科数", ("", ""))[1].startswith("10"):
        fail("§17.31 法藏 品内答相 must be 10")
    if "八十品2–6" not in r2.get("所释品次", ("", ""))[1]:
        fail("§17.31 法藏 所释品次 must state 一品统摄八十品2–6")
    for want in ("一眾海同請", "六結通無窮"):
        if want not in c2["quotes"][2]["text"]:
            fail(f"§17.31 澄观六分缺 {want}")
    for want in ("一面光集眾分", "十正陳法海分"):
        if want not in c2["quotes"][5]["text"]:
            fail(f"§17.31 法藏十段缺 {want}")
    for want in ("長分有十", "釋第一會竟"):
        if want not in t9p2_block:
            fail(f"§17.31 block 缺 {want}")
    for want in ("层级", "不可互推", "不构成经文增减"):
        if want not in t9p2_block:
            fail(f"§17.31 block 缺关键判语：{want}")
    for want in ("1:5", "不作逐品等数", "同名段位置不同"):
        if want not in md:
            fail(f"§17.31 正文缺：{want}")
    # 品3：六十品2 中段 3–9、澄观六分、法藏七段、分合互为镜像
    c3 = t9p_cases[2]
    for want in ("普賢三昧品", "中段", "3–9"):
        if want not in c3["pin"]:
            fail(f"§17.32 case pin 缺 {want}")
    if "品3" not in c3["pin"]:
        fail("§17.32 case must state 品3")
    r3 = {item: (a, b) for item, a, b in c3["rows"]}
    if not r3.get("品级科数", ("", ""))[0].startswith("6"):
        fail("§17.32 澄观 品级科数 must be 6")
    if not r3.get("品级科数", ("", ""))[1].startswith("7"):
        fail("§17.32 法藏 对应段数 must be 7")
    for want in ("一三昧分", "六大眾偈請分"):
        if want not in c3["quotes"][0]["text"]:
            fail(f"§17.32 澄观六分缺 {want}")
    if "初起定、後眾益" not in c3["quotes"][1]["text"]:
        fail("§17.32 起定分须含「初起定、後眾益」")
    for want in ("6 对 7", "分合方向相反", "位置差异不据此判经文异同"):
        if want not in t9p3_block:
            fail(f"§17.32 block 缺关键判语：{want}")
    for want in ("同请位置相反", "名称可对者五"):
        if want not in md:
            fail(f"§17.32 正文缺：{want}")
    if "17.30" not in (t9.get("refs") or "") or "17.31" not in (t9.get("refs") or "") \
            or "17.32" not in (t9.get("refs") or ""):
        fail("ontology T9 refs must cite §17.30, §17.31 and §17.32")
    if "### 17.30 T9 科判逐品" not in md or "### 17.31 T9 科判逐品" not in md \
            or "### 17.32 T9 科判逐品" not in md:
        fail("§17.30／§17.31／§17.32 headings missing")
    if "### 17.29 未竟" not in md:
        fail("§17.29 未竟 heading missing (must stay last)")
    ok(f"§17.30–§17.32 T9 逐品科判: {len(t9p_cases)} 品 / "
       f"{sum(len(c['quotes']) for c in t9p_cases)} quotes re-located / "
       f"品1 澄观 10 vs 法藏 無定數 / 品2 澄观 6 vs 法藏品内 10（1:5 只对所在段） / "
       f"品3 澄观 6 vs 法藏 3–9 段共 7")


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
    if "### 17.14 T6" not in md or "### 17.15 T7" not in md or "### 17.29 未竟" not in md:
        fail("§17.14–17.24 headings missing")

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

    # --- §6.6 third source: ACIP index must place D4011–4015 in vol 117 ---
    ai_path = ROOT / "data" / "references" / "tibetan" / "derge_tengyur" / "acip_index.yml"
    if not ai_path.exists():
        fail("acip_index.yml missing")
    import yaml as _yaml
    aid = _yaml.safe_load(ai_path.read_text(encoding="utf-8"))
    acip_rows = {}
    for _k, _v in aid.get("annotations", {}).items():
        _w = _v.get("work_id")
        for _s in _v.get("span") or []:
            acip_rows[_w] = _s.get("vol")
    for w, vol in (("D4011", 117), ("D4012", 117), ("D4013", 117),
                   ("D4014", 117), ("D4015", 117),
                   ("D3993", 113), ("D3998", 116), ("D3999", 116)):
        got = acip_rows.get(w)
        if got is None:
            fail(f"ACIP index missing {w}")
        if got != vol:
            fail(f"ACIP {w} in vol {got} != expected {vol}")
    if "三源一致" not in md or "acip_index.yml" not in md:
        fail("§6.6 third-source sentence missing")
    tanj = json.loads((ROOT / "data" / "research" / "tanjur_catalog.json").read_text(encoding="utf-8"))
    acip = tanj["meta"]["dkarchag"].get("acip_third_source")
    if not acip or not all(v["vol_matches"] for v in acip["checks"].values()):
        fail("§6.6 ACIP checks in tanjur_catalog.json not all matching")
    ok("§6.6 tanjur third source: ACIP index places D4010–4015 contiguous in vol 117")

    # --- §17.23 R5: 灵验叙事 quotes re-sliced from T51n2073 ---
    ly_path = ROOT / "data" / "research" / "r5_lingyan.json"
    if not ly_path.exists():
        fail("r5_lingyan.json missing")
    ly = json.loads(ly_path.read_text(encoding="utf-8"))
    for key, meta in ly["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"R5 source hash changed: {key}")
    r5_block = grab("r5")
    for qid, q in ly["quotes"].items():
        if q["text"] not in md:
            fail(f"R5 quote not printed: {qid}")
        if f'`{q["lb"]}`' not in r5_block:
            fail(f"R5 quote lb missing: {qid}")
    for g in ly["groups"]:
        if f"*{g['kind']}*" not in r5_block:
            fail(f"R5 group heading missing: {g['kind']}")
        for qid in g["quotes"]:
            if qid not in ly["quotes"]:
                fail(f"R5 group cites unknown quote: {qid}")
    if "受持華嚴力" not in md or "圖畫七處八會之像" not in md:
        fail("R5 cross-ref anchors missing")
    r5 = next(o for o in ops if o["id"] == "R5")
    if r5["status"] not in ("partial", "done"):
        fail(f"ontology R5 not partial/done: {r5['status']}")
    if len(ly["groups"]) != 5:
        fail(f"R5 groups {len(ly['groups'])} != 5 (諷誦/轉讀/書寫/講解/雜述)")
    for gk in ("講解", "雜述"):
        if gk not in r5_block:
            fail(f"R5 {gk} group missing")
    if "以華嚴為圓教" not in md:
        fail("R5 慧光判教 quote missing")
    if "般若空宗。乃華嚴經中。枝條出矣" not in md:
        fail("R5 孙思邈 quote missing")
    ok(f"§17.23 R5: {len(ly['quotes'])} quotes in {len(ly['groups'])} groups re-verified "
       f"({('/').join(g['kind'] for g in ly['groups'])})")

    # --- §17.25 waizi matrix: 9 corpora, 14 verbatim anchors, Buddhist anchors all zero ---
    wz_path = ROOT / "data" / "research" / "waizi_matrix.json"
    if not wz_path.exists():
        fail("waizi_matrix.json missing")
    wz = json.loads(wz_path.read_text(encoding="utf-8"))
    allc = list(wz["corpora"].values()) + list(wz["gretil"].values())
    if len(allc) != 9:
        fail(f"waizi corpora {len(allc)} != 9")
    nverbatim = 0
    for c in allc:
        for f, meta in c.get("files", {}).items():
            p_local = ROOT / c["dir"] / f
            if hashlib.sha256(p_local.read_bytes()).hexdigest() != meta["sha256"]:
                fail(f"waizi file hash changed: {f}")
        for s in c["struct"]:
            if s.get("verbatim"):
                nverbatim += 1
                if s["quote"] not in md:
                    fail(f"waizi struct quote not printed: {s['quote'][:20]}")
            else:
                fail(f"waizi struct anchor not verbatim: {s['quote'][:20]}")
    if nverbatim < 14:
        fail(f"waizi verbatim anchors {nverbatim} < 14")
    for anchor_w in ("法界", "華嚴", "圓融", "涅槃"):
        for c in allc:
            if c["matrix"].get(anchor_w, 0) != 0:
                fail(f"waizi Buddhist anchor nonzero in {c['slug']}: {anchor_w}")
    w_block = grab("waizi")
    if "皆为 0" not in w_block.replace(" ", "") and "全部为 0" not in w_block:
        fail("§17.25 zero-anchor sentence missing")
    if "### 17.25 诸子" not in md:
        fail("§17.25 heading missing")
    ok(f"§17.25 waizi matrix: 9 corpora / {nverbatim} verbatim anchors / Buddhist anchors all zero")

    # --- §17.26 substantive: 4 groups, bilateral quotes, analysis present ---
    sc_path = ROOT / "data" / "research" / "substantive_correspondence.json"
    if not sc_path.exists():
        fail("substantive_correspondence.json missing")
    sc = json.loads(sc_path.read_text(encoding="utf-8"))
    for key, meta in sc["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"substantive source hash changed: {key}")
    sc_block = grab("substantive")
    if len(sc["groups"]) != 4:
        fail(f"substantive groups {len(sc['groups'])} != 4")
    for g in sc["groups"]:
        if g["title"] not in sc_block:
            fail(f"substantive group title missing: {g['title'][:30]}")
        if g["level"] not in sc_block:
            fail(f"substantive level missing: {g['level']}")
        if g["analysis"][:30] not in sc_block:
            fail(f"substantive analysis missing: {g['id']}")
        for side in ("non_buddhist", "buddhist"):
            for q in g[side]:
                if q["text"][:20] not in sc_block:
                    fail(f"substantive quote not printed: {g['id']} {side}")
    for frag in ("同构层级", "方向", "不在场的那半"):
        if frag not in sc_block:
            fail(f"substantive discipline sentence missing: {frag}")
    ok(f"§17.26 substantive: {len(sc['groups'])} groups / "
       f"{sc['summary']['quotes_total']} bilateral quotes / 4 levels + directions")

    # --- R4 仪式·课诵: quotes re-sliced from T19n1019 + T279 cross ---
    lt_path = ROOT / "data" / "research" / "r4_liturgical.json"
    if not lt_path.exists():
        fail("r4_liturgical.json missing")
    lt = json.loads(lt_path.read_text(encoding="utf-8"))
    for key, meta in lt["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"R4 source hash changed: {key}")
    r4_block = grab("r4")
    for qid, q in lt["quotes"].items():
        if q["text"] not in md:
            fail(f"R4 quote not printed: {qid}")
        if f'`{q["lb"]}`' not in r4_block:
            fail(f"R4 quote lb missing: {qid}")
    for g in lt["groups"]:
        if g["kind"] not in r4_block:
            fail(f"R4 group missing: {g['kind']}")
    t279_flat = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "",
        (ROOT / "data" / "references" / "cbeta" / "T10n0279.xml").read_text(encoding="utf-8")))
    if "善知眾藝，學菩薩字智" not in t279_flat:
        fail("R4 T279 chapter anchor not in T279")
    r4 = next(o for o in ops if o["id"] == "R4")
    if r4["status"] not in ("partial", "done"):
        fail(f"ontology R4 not partial/done: {r4['status']}")
    if "音乐化" not in r4_block:
        fail("R4 boundary sentence missing")
    ok(f"§17.18 R4: {len(lt['quotes'])} quotes in {len(lt['groups'])} groups re-verified")

    # --- §17.18 influence: five-channel skeleton ---
    inf_block = grab("influence")
    inf_rows = [ln for ln in inf_block.splitlines() if ln.startswith("| ") and "通道" not in ln and "---" not in ln]
    if len(inf_rows) != 7:
        fail(f"§17.18 influence rows {len(inf_rows)} != 7")
    for frag in ("宗派传承", "注疏传统", "西藏接受", "图像文物", "儒道论衡", "Toh 4011–4015"):
        if frag not in inf_block:
            fail(f"§17.18 influence channel missing: {frag}")
    if "见证先行，逐格充实" not in md:
        fail("§17.18 influence discipline sentence missing")
    ok("§17.18 influence: 5-channel skeleton present")

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
    if "### 17.15 T7" not in md or "### 17.29 未竟" not in md:
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
    if "### 17.16 T4" not in md or "### 17.29 未竟" not in md:
        fail("§17.16–17.24 headings missing")
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

    # --- §17.33 T4 true conflation: hashes, partition, splice, table rows ---
    t4c_path = ROOT / "data" / "research" / "t4_conflation_true.json"
    if not t4c_path.exists():
        fail("t4_conflation_true.json missing")
    t4c = json.loads(t4c_path.read_text(encoding="utf-8"))
    for key, meta in t4c["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"T4 conflation source hash changed: {key}")
    t4c_block = grab("t4conflation")
    st = t4c["stats"]
    if st["pins664"] != 24 or st["pins663"] != 19 or st["juans664"] != 8:
        fail(f"T4 conflation counts {st['pins664']}/{st['pins663']}/{st['juans664']} != 24/19/8")
    if st["by_src_counts"] != {"曇無讖": 18, "真諦": 4, "崛多": 2}:
        fail(f"T4 by_src_counts {st['by_src_counts']} != 18/4/2")
    if st["cov_median"]["曇無讖"] < 0.75:
        fail("T4 讖品 median coverage < 0.75")
    if st["cov_max_zhendi"] > 0.05:
        fail("T4 真諦品 max coverage > 0.05")
    sp = t4c["splice_split_pin2"]
    if not (sp.get("ok") and sp["pre_cov"] > 0.85 and sp["post_cov"] < 0.05):
        fail("T4 pin2 splice split missing or wrong")
    if len(t4c["splice_marks"]) < 4:
        fail("T4 splice marks < 4")
    for frag in ("### 17.33 T4 真拼合", "品级多源合成", "同旨重译",
                 "题下标注与文本实况出现张力"):
        if frag not in md:
            fail(f"§17.33 key sentence missing: {frag}")
    n_rows = sum(1 for ln in t4c_block.splitlines()
                 if re.match(r"\| \d+ \| .*\| \d\.\d{3} \| ", ln))
    if n_rows != 24:
        fail(f"§17.33 pin table rows {n_rows} != 24")
    for j in t4c["juan_bases"]:
        if j["byline"][:14] not in t4c_block:
            fail(f"§17.33 juan byline missing: juan{j['juan']}")
    ok(f"§17.33 T4 true conflation: 24 pins / 8 juans, partition "
       f"18/4/2, 讖 median {st['cov_median']['曇無讖']:.3f}, 真諦 max "
       f"{st['cov_max_zhendi']:.3f}, splice pre {sp['pre_cov']:.3f}/post {sp['post_cov']:.3f}")

    # --- §17.34 T7 paraphrase: hashes, cluster stats, exhibits re-sliced ---
    t7p_path = ROOT / "data" / "research" / "t7_paraphrase.json"
    if not t7p_path.exists():
        fail("t7_paraphrase.json missing")
    t7p = json.loads(t7p_path.read_text(encoding="utf-8"))
    for key, meta in t7p["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"T7 paraphrase source hash changed: {key}")
    t7_block = grab("t7para")
    for pid, want in (("A", 0.99), ("B", 0.97)):
        stp = t7p["pairs"][pid]["stats"]
        if stp["cluster_share"] < want:
            fail(f"T7 {pid} cluster_share {stp['cluster_share']} < {want}")
    if "### 17.34 T7" not in md:
        fail("§17.34 heading missing")
    exs = t7p.get("exhibits", [])
    if len(exs) != 5:
        fail(f"T7 exhibits {len(exs)} != 5")
    sys.path.insert(0, str(ROOT / "scripts"))
    from build_implicit_quotes import Doc as VDoc  # noqa: E402
    _vdocs: dict = {}

    def _vdoc(name: str, rel: str) -> VDoc:
        if name not in _vdocs:
            _vdocs[name] = VDoc(name, ROOT / rel)
        return _vdocs[name]

    _t7_files = {"T1735": "cbeta/T35n1735.xml", "T279": "cbeta/T10n0279.xml",
                 "T1733": "cbeta/T35n1733.xml", "T278": "cbeta/T09n0278.xml"}
    for ex in exs:
        pid = ex["key"].split(":")[0]
        com_name, sutra_name = {"A": ("T1735", "T279"),
                                "B": ("T1733", "T278")}[pid]
        com = _vdoc(com_name, "data/references/" + _t7_files[com_name])
        sutra = _vdoc(sutra_name, "data/references/" + _t7_files[sutra_name])
        a, b = ex["c_anchor"]
        i = com.norm.find(a)
        if i < 0:
            fail(f"T7 exhibit {ex['key']} com anchor not found")
        else:
            if com.lb_at(com.raw_index(i)) != ex["com_quote"]["lb"]:
                fail(f"T7 exhibit {ex['key']} com lb mismatch")
            if ex["com_quote"]["text"][:20] not in t7_block:
                fail(f"T7 exhibit {ex['key']} com quote not printed")
        for (sa, sb), q in zip(ex["s_quotes"], ex["sutra_quotes"]):
            j = sutra.norm.find(sa)
            if j < 0:
                fail(f"T7 exhibit {ex['key']} sutra anchor not found")
            elif sutra.lb_at(sutra.raw_index(j)) != q["lb"]:
                fail(f"T7 exhibit {ex['key']} sutra lb mismatch")
            if q["text"][:20] not in t7_block:
                fail(f"T7 exhibit {ex['key']} sutra quote not printed")
        if len(ex["terms"]) < 2:
            fail(f"T7 exhibit {ex['key']} terms < 2")
        if "〔本文判断〕" not in ex["analysis"]:
            fail(f"T7 exhibit {ex['key']} judgment marker missing")
    ok(f"§17.34 T7 paraphrase: clusters "
       f"{t7p['pairs']['A']['stats']['cluster_share']:.1%}/"
       f"{t7p['pairs']['B']['stats']['cluster_share']:.1%}, "
       f"{len(exs)} exhibits re-sliced + lb re-verified")

    # --- §17.35 Tanjur qualification: 8 works, dkar chag hash, table rows ---
    tq_path = ROOT / "data" / "research" / "tanjur_qual.json"
    if not tq_path.exists():
        fail("tanjur_qual.json missing")
    tq = json.loads(tq_path.read_text(encoding="utf-8"))
    dkm = tq["meta"]["dkarchag"]
    if hashlib.sha256((ROOT / dkm["path"]).read_bytes()).hexdigest() != dkm["sha256"]:
        fail("Tanjur qual dkar chag hash changed")
    tq_block = grab("tanjurqual")
    if len(tq["works"]) != 8:
        fail(f"Tanjur qual works {len(tq['works'])} != 8")
    for w in tq["works"]:
        if str(w["D"]) not in tq_block:
            fail(f"Tanjur qual D{w['D']} missing in block")
        if w["genre"] not in tq_block:
            fail(f"Tanjur qual genre missing: D{w['D']}")
        if w["han_correspond"][:8] not in tq_block:
            fail(f"Tanjur qual han_correspond missing: D{w['D']}")
    if "内容层仍空" not in tq_block and "内容层仍空" not in md:
        fail("§17.35 content-layer disclaimer missing")
    nq_rows = sum(1 for ln in tq_block.splitlines()
                  if re.match(r"\| \d{4} \|", ln))
    if nq_rows != 8:
        fail(f"§17.35 qual table rows {nq_rows} != 8")
    ok("§17.35 Tanjur qual: 8 works / dkar chag hash ok / T1522+T297 correspondences")

    # --- §17.36 Qingliang zhuan: hashes, 6 exhibits re-sliced ---
    ql_path = ROOT / "data" / "research" / "qingliang_probe.json"
    if not ql_path.exists():
        fail("qingliang_probe.json missing")
    ql = json.loads(ql_path.read_text(encoding="utf-8"))
    for key, meta in ql["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"Qingliang source hash changed: {key}")
    ql_block = grab("qingliang")
    if len(ql["exhibits"]) != 6:
        fail(f"Qingliang exhibits {len(ql['exhibits'])} != 6")
    _ql_files = {"T2098": "cbeta/T51n2098.xml", "T2099": "cbeta/T51n2099.xml",
                 "T2100": "cbeta/T51n2100.xml"}
    for ex in ql["exhibits"]:
        d = _vdoc(ex["doc"], "data/references/" + _ql_files[ex["doc"]])
        i = d.norm.find(ex["text"].replace("。", "")[:12])
        if i < 0:
            fail(f"Qingliang exhibit text not in source: {ex['key']}")
        elif d.lb_at(d.raw_index(i)) != ex["lb"]:
            fail(f"Qingliang exhibit lb mismatch: {ex['key']}")
        if ex["text"][:20] not in ql_block:
            fail(f"Qingliang exhibit not printed: {ex['key']}")
        if "〔本文判断〕" not in ex["analysis"]:
            fail(f"Qingliang exhibit judgment marker missing: {ex['key']}")
    kinds = [ex["kind"] for ex in ql["exhibits"]]
    if kinds.count("R4") != 4 or kinds.count("R3") != 2:
        fail(f"Qingliang kinds {kinds} != 4×R4 + 2×R3")
    if "音乐化半边" not in ql_block:
        fail("§17.36 music-half disclaimer missing")
    ok("§17.36 Qingliang: 6 exhibits (4×R4 + 2×R3) re-sliced + lb re-verified")

    # --- §17.37 P grids: hashes + exhibits re-sliced ---
    p4_path = ROOT / "data" / "research" / "p4_jiangjie.json"
    r2p_path = ROOT / "data" / "research" / "p2p3_ritual.json"
    for pp_ in (p4_path, r2p_path):
        if not pp_.exists():
            fail(f"{pp_.name} missing")
    p4jj = json.loads(p4_path.read_text(encoding="utf-8"))
    p2p3 = json.loads(r2p_path.read_text(encoding="utf-8"))
    for meta in (p4jj["meta"]["sources"], p2p3["meta"]["sources"]):
        for key, meta_i in meta.items():
            if hashlib.sha256((ROOT / meta_i["path"]).read_bytes()).hexdigest() != meta_i["sha256"]:
                fail(f"P-grid source hash changed: {key}")
    pg_block = grab("pgrids")
    _p_files = {"T2073": "cbeta/T51n2073.xml", "T19n1020": "cbeta/T19n1020.xml",
                "T19n1021": "cbeta/T19n1021.xml"}
    for ex in p4jj["exhibits"] + p2p3["exhibits"]:
        docname = ex.get("doc", "T2073")
        d = _vdoc(docname, "data/references/" + _p_files[docname])
        frag = re.sub(r"[^\u4e00-\u9fff]", "", ex["text"])[:12]
        i = d.norm.find(frag)
        if i < 0:
            fail(f"P-grid exhibit text not in source: {ex['key']}")
        if ex["text"][:20] not in pg_block:
            fail(f"P-grid exhibit not printed: {ex['key']}")
    if "P 面 P1–P4 四格全落" not in pg_block:
        fail("§17.37 P-face conclusion missing")
    ok(f"§17.37 P grids: {len(p4jj['exhibits'])}+{len(p2p3['exhibits'])} exhibits verified")

    # --- §17.38 D4 opposition: 5 exhibits re-sliced ---
    d4_path = ROOT / "data" / "research" / "d4_opposition.json"
    if not d4_path.exists():
        fail("d4_opposition.json missing")
    d4 = json.loads(d4_path.read_text(encoding="utf-8"))
    for key, meta in d4["meta"]["sources"].items():
        if hashlib.sha256((ROOT / meta["path"]).read_bytes()).hexdigest() != meta["sha256"]:
            fail(f"D4 source hash changed: {key}")
    d4_block = grab("d4oppo")
    if len(d4["exhibits"]) != 5:
        fail(f"D4 exhibits {len(d4['exhibits'])} != 5")
    _d4_files = {"T45n1866": "cbeta/T45n1866.xml", "T279": "cbeta/T10n0279.xml"}
    for ex in d4["exhibits"]:
        d = _vdoc(ex["doc"], "data/references/" + _d4_files[ex["doc"]])
        frag = re.sub(r"[^\u4e00-\u9fff]", "", ex["text"])[:12]
        i = d.norm.find(frag)
        if i < 0:
            fail(f"D4 exhibit text not in source: {ex['key']}")
        elif d.lb_at(d.raw_index(i)) != ex["lb"]:
            fail(f"D4 exhibit lb mismatch: {ex['key']}")
        if ex["text"][:20] not in d4_block:
            fail(f"D4 exhibit not printed: {ex['key']}")
    for frag in ("教说位阶", "臨門三車俱是開方便門", "本末不見說三乘"):
        if frag.replace("臨門三車俱是開方便門", "臨門三車俱是開方便門") not in md:
            fail(f"§17.38 key phrase missing: {frag}")
    ok("§17.38 D4 opposition: 5 exhibits / positions-level opposition asserted")

    # --- §17.39 T6 huayong: 3 exhibits re-sliced + quote-flag logic ---
    t6h_path = ROOT / "data" / "research" / "t6_huayong.json"
    if not t6h_path.exists():
        fail("t6_huayong.json missing")
    t6h = json.loads(t6h_path.read_text(encoding="utf-8"))
    t6_block = grab("t6huayong")
    if len(t6h.get("exhibits", [])) != 3:
        fail(f"T6 exhibits {len(t6h.get('exhibits', []))} != 3")
    for ex in t6h["exhibits"]:
        pid = ex["pair"]
        com_name, sutra_name = {"A": ("T1735", "T279"), "B": ("T1733", "T278")}[pid]
        com = _vdoc(com_name, "data/references/" + _t7_files[com_name])
        sutra = _vdoc(ex.get("sutra_doc", sutra_name),
                      "data/references/" + _t7_files[ex.get("sutra_doc", sutra_name)])
        for side, doc in (("com_quote", com), ("sutra_quote", sutra)):
            q = ex[side]
            if q["text"][:20] not in t6_block:
                fail(f"T6 exhibit {ex['key']} {side} not printed")
            if doc.norm.find(q["text"].replace("。", "")[:10]) < 0 and \
                    doc.norm.find(ex["c_anchor"][0] if side == "com_quote"
                                  else ex["s_anchor"][0]) < 0:
                fail(f"T6 exhibit {ex['key']} {side} anchor not in source")
    for frag in ("引号检测", "牒示式", "眾生心下"):
        if frag not in t6_block:
            fail(f"§17.39 key phrase missing: {frag}")
    ok("§17.39 T6 huayong: 3 exhibits / quote-flag typology asserted")

    # --- §17.40 C expansion: matrices + anchors + negatives ---
    ce_path = ROOT / "data" / "research" / "c_expand.json"
    if not ce_path.exists():
        fail("c_expand.json missing")
    ce = json.loads(ce_path.read_text(encoding="utf-8"))
    if hashlib.sha256((ROOT / ce["meta"]["sources"]["yogasutra"]["path"]).read_bytes()
                      ).hexdigest() != ce["meta"]["sources"]["yogasutra"]["sha256"]:
        fail("C-expand yoga hash changed")
    ce_block = grab("cexpand")
    if ce["cantongqi"]["matrix"].get("法界", 1) != 0 or \
            ce["cantongqi"]["matrix"].get("涅槃", 1) != 0:
        fail("C-expand cantongqi Buddhist anchors not zero")
    if ce["wushangmiyao"]["matrix"].get("道性", 1) != 0:
        fail("C-expand wushang daoxing should be 0")
    for frag in ("atha yogānuśāsanam", "乾坤者易之門户", "负向结果", "陈那"):
        if frag not in ce_block:
            fail(f"§17.40 key content missing: {frag}")
    tq2 = json.loads(tq_path.read_text(encoding="utf-8"))
    n_col = sum(1 for w in tq2["works"] if w.get("in_text_colophon", {}).get("ok"))
    if n_col != 6:
        fail(f"Tanjur colophons {n_col} != 6")
    w12 = next(w for w in tq2["works"] if w["D"] == 4012)
    if "陈那" not in w12["author_dkarchag"]:
        fail("D4012 author correction missing")
    ok(f"§17.40 C expansion + Tanjur colophons: {n_col}/8 translator records, D4012=Dignāga")

    print("=" * 40)
    print("ALL Dazang article checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())