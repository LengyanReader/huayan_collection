# -*- coding: utf-8 -*-
"""verify_imagery.py — 图像著录一致性校验（凡例九「源头治理」之实施）

强制三条不变量：
  1. 文中每一张 doc-img 都必须在 data/imagery/*.yaml 登记表内（无著录之图不得出现）；
  2. 登记表每一项都必须在文中出现，且图号／缩略图／授权／登记号逐一相符（登记表不得虚列）；
  3. 分类不得拔高——A 类（依本经之像）非空时，每项须有 evidence 字段说明「本经而作」之据；
     B／C 类之图注须含「边界」二字，明示其不可等同之处。

用法：
    python scripts/verify_imagery.py            # 离线校验（默认）
    python scripts/verify_imagery.py --online   # 另加 Commons 可达性（HEAD 200）
"""
import io, os, re, sys, collections, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

DOC = os.path.join(ROOT, "docs", "经学文献", "华严经细读_第一部_世主妙严品.md")
REG = os.path.join(ROOT, "data", "imagery", "shizhu_miaoyan_imagery.yaml")

import yaml

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--online", action="store_true", help="另作 Commons 可达性检查")
    a = ap.parse_args()

    errs, warns, notes = [], [], []
    doc = io.open(DOC, encoding="utf-8").read()
    Y = yaml.safe_load(io.open(REG, encoding="utf-8"))
    IM = Y["imagery"]

    # ---- 0. 登记表自身完整性 ----
    need = ("id", "kind", "kind_label", "figure_no", "title_zh", "title_en", "era_zh",
            "location_zh", "license_zh", "license_en", "author_zh", "thumb_url",
            "source_page", "relevance_zh", "relevance_en")
    for it in IM:
        for k in need:
            if not str(it.get(k) or "").strip():
                errs.append("登记表 %s：字段 %s 为空" % (it.get("id", "?"), k))
    if len({i["id"] for i in IM}) != len(IM):
        errs.append("登记表存在重复 id")
    if len({i["thumb_url"] for i in IM}) != len(IM):
        errs.append("登记表存在重复 thumb_url")
    if len({i["figure_no"] for i in IM}) != len(IM):
        errs.append("登记表存在重复图号")
    # 图号须为裸「N-M」：若含「图 」前缀，渲染模板再补一字即成「图 图 N-M」
    # L.102：卷三至卷五（4-x／5-x／6-x）入册，故放宽至 1—6 章（原为 1-2）
    FIGPAT = r"[1-6]-\d+"
    for it in IM:
        if not re.fullmatch(FIGPAT, str(it["figure_no"]).strip()):
            errs.append("登记表 %s 之 figure_no 非裸「N-M」式：%r"
                        % (it["id"], it["figure_no"]))

    # ---- 0b. 四类框架（内容／名相／行动／象征）之声明与取值 ----
    TD = Y.get("typology_definitions") or {}
    if not TD:
        errs.append("登记表缺 typology_definitions——凡例六「边界自知」："
                    "入册之图须能自述其属「内容／名相／行动／象征」何类，不得只言『配图』")
    else:
        for k in ("内容", "名相", "行动", "象征"):
            if not str(TD.get(k) or "").strip():
                errs.append("typology_definitions 缺「%s」之定义（四类须齐备）" % k)
        TYP = set(TD)
        for it in IM:
            if not str(it.get("typology") or "").strip():
                errs.append("登记表 %s 缺 typology 字段（内容／名相／行动／象征）"
                            % it["id"])
            elif it["typology"] not in TYP:
                errs.append("登记表 %s 之 typology=%r 不在四类之内（%s）"
                            % (it["id"], it["typology"], "／".join(sorted(TYP))))
    notes.append("四类框架：%s（各图须自报其类）"
                 % "／".join("%s %d" % (k, sum(1 for i in IM
                                              if i.get("typology") == k))
                             for k in ("内容", "名相", "行动", "象征")))

    # ---- 0c. 否定性记录：未配图之组须载明「未查」或「查无」，不可留白 ----
    NEG = Y.get("negative_findings") or []
    if not NEG:
        warns.append("登记表缺 negative_findings——未能配图之组须留否定性记录，"
                     "以免「查无此图」与「未查」不可辨（凡例六）")
    else:
        for nf in NEG:
            for k in ("section", "motif_zh", "status", "query_terms", "note_zh"):
                if not str(nf.get(k) or "").strip():
                    errs.append("否定性记录 %s：字段 %s 为空"
                                % (nf.get("motif_zh", "?"), k))
            if nf.get("status") not in ("未查", "查无"):
                errs.append("否定性记录 %s 之 status=%r 须为「未查」或「查无」"
                            "（%s）" % (nf.get("motif_zh"), nf.get("status"),
                                       nf.get("section")))
        notes.append("否定性记录 %d 条（未查／查无各须注明检索词）" % len(NEG))

    # ---- 1. A 类不得无据（防拔高） ----
    for it in IM:
        if it["kind"] == "A" and not str(it.get("evidence") or "").strip():
            errs.append("登记表 %s 标为 A（依本经之像）却无 evidence 字段说明依据"
                        "——凡例九「严禁假信息」：不能证明「为本经而作」者应归 B/C" % it["id"])

    # ---- 2. 文中 doc-img ⊆ 登记表 ----
    doc_imgs = re.findall(r'<img class="doc-img" src="([^"]+)"', doc)
    reg_urls = {i["thumb_url"]: i for i in IM}
    for u in doc_imgs:
        if u not in reg_urls:
            errs.append("文中图片未著录：%s" % u[:110])
    notes.append("文中 doc-img %d 张，登记表 %d 项" % (len(doc_imgs), len(IM)))

    # ---- 3. 登记表各项 ⊆ 文中，且图号／授权相符 ----
    for it in IM:
        n = doc.count(it["thumb_url"])
        if n == 0:
            errs.append("登记表 %s 之图未出现于正文" % it["id"])
        elif n > 1:
            errs.append("登记表 %s 之图在正文出现 %d 次（应 1 次）" % (it["id"], n))
        else:
            blk = re.search(r'<img class="doc-img" src="' + re.escape(it["thumb_url"]) + r'".*?</figure>',
                            doc, re.S)
            blk = blk.group(0) if blk else ""
            if it["figure_no"] not in blk:
                errs.append("正文图注未含图号「%s」（%s）" % (it["figure_no"], it["id"]))
            if it["license_zh"] not in blk:
                errs.append("正文图注未含授权「%s」（%s）" % (it["license_zh"], it["id"]))
            if it["id"] not in blk:
                errs.append("正文图注未回指登记号（%s）" % it["id"])
            if it["kind"] in ("B", "C") and "边界" not in blk:
                errs.append("%s 属 %s 类，图注未见「边界」声明" % (it["id"], it["kind"]))

    # ---- 4. 图号连续无缺（逐章；L.102 由 1-2 两章泛化至各章皆验） ----
    byc = collections.defaultdict(list)
    for c, n in re.findall(r"图 (\d+)-(\d+)　", doc):
        byc[c].append(int(n))
    for c in sorted(byc):
        ns = sorted(byc[c])
        if ns != list(range(1, len(ns) + 1)):
            errs.append("第 %s 分图图号不连续：%s" % (c, ns))
    if not byc:
        errs.append("全文未见「图 N-M　」式图注")
    notes.append("图号：%s（共 %d）" % (
        " ／ ".join("%s-%s" % (c, ",".join(map(str, sorted(byc[c]))))
                    for c in sorted(byc)),
        sum(len(v) for v in byc.values())))

    # ---- 4b. 逐图图注之图号须「恰一处」，且不得出现「图 图」重字 ----
    for it in IM:
        pat = "图 %s　" % it["figure_no"]
        n = doc.count(pat)
        if n != 1:
            errs.append("图注「%s」在全文出现 %d 处（应恰 1 处）" % (pat, n))
    for m in re.finditer(r"图\s+图\s*[1-6]-\d+", doc):
        errs.append("图号重字「%s」——渲染模板与登记表图号重复加了「图」" % m.group(0))

    # ---- 4c. A 类为 0 时，须留下检索与否决记录（否则「查无此图」与「未查」不可辨） ----
    nA = sum(1 for i in IM if i["kind"] == "A")
    if nA == 0:
        if "十.4" not in doc or "否决" not in doc:
            errs.append("A 类为 0 件，然文中未见「十.4」A 类检索与否决记录"
                        "——须载明检索方式与逐条否决理由，方能区分「查无」与「未查」")
        else:
            notes.append("A 类 0 件，已留检索与否决记录（十.4）")

    # ---- 4d. 未配图之组，文中须有对应之否定性记录（十.5）----
    if NEG:
        if "十.5" not in doc or "查无" not in doc:
            errs.append("登记表载有 %d 条否定性记录，然文中未见「十.5」未配图组之"
                        "「未查／查无」记录——凡例六：信息边界须自述，"
                        "「查无此图」与「未查」不可混同" % len(NEG))
        else:
            notes.append("未配图组已留否定性记录（十.5），%d 条" % len(NEG))

    # ---- 5. 图注所指之登记册须真实存在 ----
    if "〔▲实证文物与图像登记〕" in doc:
        if "附录十" not in doc:
            errs.append("图注指向〔▲实证文物与图像登记〕，但文中无附录十")
    else:
        warns.append("文中未见〔▲实证文物与图像登记〕标记")

    # ---- 6. 诚实性：不得出现「本经专像／依本经」之类拔高措辞而无据 ----
    for it in IM:
        if it["kind"] != "A":
            blk = re.search(r'<img class="doc-img" src="' + re.escape(it["thumb_url"]) + r'".*?</figure>',
                            doc, re.S)
            if blk and re.search(r"本经(之)?专像(?!)", blk.group(0)):
                if "非本经之专像" not in blk.group(0):
                    errs.append("%s 之图注出现「本经专像」而未自我否定" % it["id"])

    # ---- 7. 统计（供台账登记） ----
    kc = collections.Counter(i["kind"] for i in IM)
    lc = collections.Counter(i["license_en"] for i in IM)
    print("── 图像著录校验 ──────────────────────────────")
    for x in notes:
        print("  · " + x)
    print("  · 分类 A/B/C：%s" % "、".join("%s %d" % (k, kc.get(k, 0)) for k in "ABC"))
    print("  · 授权：%s" % "、".join("%s %d" % (k, v) for k, v in lc.most_common()))

    # ---- 8. 可选：Commons 可达性 ----
    if a.online:
        import urllib.request, time
        UA = {"User-Agent": "huayan-collection-imagery/1.0 (educational; local)"}
        print("── 在线可达性 ────────────────────────────────")
        bad = 0
        for it in IM:
            for k in ("thumb_url", "source_page"):
                for att in range(3):
                    try:
                        rq = urllib.request.Request(it[k], headers=UA, method="HEAD")
                        with urllib.request.urlopen(rq, timeout=35) as r:
                            print("  %-4s %-32s %s" % (r.status, it["id"], k)); break
                    except Exception as e:
                        if "429" in str(e) and att < 2:
                            time.sleep(3); continue
                        print("  ERR  %-32s %s -> %s" % (it["id"], k, e)); bad += 1; break
                time.sleep(1.0)
        if bad:
            errs.append("在线检查：%d 项不可达" % bad)

    for w in warns:
        print("  ! WARN  " + w)
    if errs:
        print("── 结果 ────────────────────────────────────")
        for e in errs:
            print("  ✗ " + e)
        print("\nFAILED：%d 项" % len(errs))
        return 1
    print("\nALL CHECKS PASSED（%d 项著录一致）" % len(IM))
    return 0

if __name__ == "__main__":
    sys.exit(main())
