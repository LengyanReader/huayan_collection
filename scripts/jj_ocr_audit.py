# -*- coding: utf-8 -*-
"""《九九華嚴》2026 講座 OCR 重建稿之**质量实测**（L.111 立·**集数自动发现**）

〔立此工具之由〕交付者已自述五条瑕疵（片头乱码／幻燈片以「 | 」拼接／
时间码 ±1s／简繁混排／仅影像层还原）。然「自述」不等于「实测」——
本工具把每一条**量化**，使「校订状态」有**可复现之实数**支撑，
而非一句「待校定」了事。

**实测五项**
  1 内部一致性：md／srt／html 三份产物之字幕条数是否相符（可复跑性）
  2 覆盖率：末时间戳 vs html 声明之时长（漏尾检测）
  3 污染率：片头乱码段（前 40s，依自述可弃）／幻燈片「 | 」拼接／
    拉丁字母混入／纯拉丁条目
  4 简繁混排：简体专用字出现之条目数
  5 跨源互证：与 `docs/huayanhai/` 之《九九華嚴》摘录逐句命中率

用法：python scripts/jj_ocr_audit.py [--json]
"""
import io
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

D = "docs/hy_refs/sub_extract/delivery"
# 〔体例〕md 之行为：  `[00:00:04–00:00:05]` 會員 | 區
#   —— 时间码**外加反引号**，且分隔符为 en/em dash 或连字符，三者皆须容。
CUE_MD = re.compile(r"^`\[(\d\d):(\d\d):(\d\d)[\u2013\u2014-]"
                    r"(\d\d):(\d\d):(\d\d)\]`\s*(.+)$")
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
LATIN = re.compile(r"[A-Za-z]")
# 简体专用字表（**抽样集，非全量**；本工具只判「有无混排」，不作简繁转换，
#故不需 OpenCC。集内含交付者自述之两个实例「现在」「国」，用以自校——
# **若此二实例不被命中，则本表失效**，此为内置自检。
SIMP_CHARS = ("现国这个们来对时会说过还东车马长门问题实现学讲记华严经"
              "说来时间万与开关无书汉语东车马长门体边过达还动务头们")
SIMP = re.compile("[" + "".join(sorted(set(SIMP_CHARS))) + "]")
HEAD_GARBAGE_S = 40   # 依交付者自述：片頭 0–40s 可整段丟棄

# 〔内置自检〕交付者自述之混排实例必须被命中，否则本工具之 SIMP 表失效，
#     「简繁混排 N 条」这一实测数即不可信。宁可使工具失败，不发不可信之数。
SIMP_SELFCHECK = ("过去、现在、未来", "国")


def sec(h, m, s):
    return int(h) * 3600 + int(m) * 60 + int(s)


def cues_of_md(path):
    out = []
    for ln in io.open(path, encoding="utf-8"):
        m = CUE_MD.match(ln.rstrip("\n"))
        if m:
            out.append((sec(m.group(1), m.group(2), m.group(3)),
                        sec(m.group(4), m.group(5), m.group(6)),
                        m.group(7).strip()))
    return out


def cues_of_srt(path):
    n = 0
    for ln in io.open(path, encoding="utf-8", errors="replace"):
        if re.match(r"^\d\d:\d\d:\d\d,\d\d\d --> ", ln):
            n += 1
    return n


def cues_of_html(path):
    return len(re.findall(r"<td class='t'>", io.open(
        path, encoding="utf-8", errors="replace").read()))


def declared(path):
    """html 之 meta：時長 mm:ss（N 秒）"""
    h = io.open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"時長\s*(\d\d):(\d\d)（(\d+) 秒）", h)
    if m:
        return sec("0", m.group(1), m.group(2)), int(m.group(3))
    m = re.search(r"(\d\d):(\d\d)（(\d+) 秒）", h)
    if m:
        return sec("0", m.group(1), m.group(2)), int(m.group(3))
    return None, None


def title_of(path):
    h = io.open(path, encoding="utf-8", errors="replace").read()
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    return re.sub(r"\s*·\s*硬字幕 OCR 重建報告\s*$", "", t.group(1)).strip() if t else ""


def video_id_of(path):
    """〔L.111·自纠〕初版只认 `youtu.be/`，而交付者 HTML 用 `youtube.com/watch?v=`，
    遂**静默返回空串**——立册遂生成 `url: ...watch?v=`（无效链接）而无人察觉。
    故：一并列两种形态，且**空 ID 直接失败**——依编务总则七「引用可点·出处可溯」，
    空链接即不合格著录，宁可工具报错，不可发不可信之数。"""
    h = io.open(path, encoding="utf-8", errors="replace").read()
    for pat in (r"youtube\.com/watch\?v=([A-Za-z0-9_\-]+)",
                r"youtu\.be/([A-Za-z0-9_\-]+)"):
        m = re.search(pat, h)
        if m:
            return m.group(1)
    raise SystemExit("【缺 YouTube ID】%s —— 无法著录可点出处，工具中止。"
                     "（不可静默留空）" % path)


def audit_one(ep):
    md = os.path.join(D, "ep%02d.md" % ep)
    ht = os.path.join(D, "ep%02d.html" % ep)
    st = os.path.join(D, "ep%02d.srt" % ep)
    cs = cues_of_md(md)
    n_md, n_srt, n_html = len(cs), cues_of_srt(st), cues_of_html(ht)
    last = cs[-1][1] if cs else 0
    d_ms, d_sec = declared(ht)

    head = [c for c in cs if c[0] < HEAD_GARBAGE_S]
    pipe = [c for c in cs if "|" in c[2]]
    latin = [c for c in cs if LATIN.search(c[2])]
    latin_only = [c for c in cs if c[2] and not HAN.search(c[2])]
    simp = [c for c in cs if SIMP.search(c[2])]
    short = [c for c in cs if len(HAN.findall(c[2])) <= 2]

    return {
        "ep": ep,
        "title": title_of(ht),
        "video_id": video_id_of(ht),
        "cues": n_md, "cues_srt": n_srt, "cues_html": n_html,
        "consistent": n_md == n_srt == n_html,
        "declared_sec": d_sec, "covered_sec": last,
        "coverage": round(last / d_sec, 4) if d_sec else None,
        "han_chars": sum(len(HAN.findall(c[2])) for c in cs),
        "head_garbage_cues": len(head),
        "pipe_cues": len(pipe),
        "latin_cues": len(latin),
        "latin_only_cues": len(latin_only),
        "simp_cues": len(simp),
        "short_cues": len(short),
        "pollution_rate": round(
            (len(head) + len(latin_only) + len(short)) / n_md, 4) if n_md else None,
    }


def discover_eps():
    """〔L.111·依交付者「後續會持續更新」之指示〕**自动发现集数**，不固化 12。
    初版硬编码 `range(1, 13)`——交付者已明言讲座**尚未完結**，故集数必变；
    硬编码将使新增集次**静默漏测**（而输出仍显示「12 集」之全绿假象）。
    三种产物须**集集齐备**，缺一即中止——宁可不测，不可假装测全。
    """
    eps = sorted({int(m.group(1))
                  for fn in os.listdir(D)
                  for m in [re.match(r"^ep(\d+)\.(md|srt|html)$", fn)] if m})
    if not eps:
        raise SystemExit("【无交付物】%s 下未找到任何 epNN.{md,srt,html}" % D)
    for e in eps:
        for ext in ("md", "srt", "html"):
            if not os.path.exists(os.path.join(D, "ep%02d.%s" % (e, ext))):
                raise SystemExit("【交付物不齐】ep%02d 缺 .%s —— 三产物须齐备，"
                                 "不可只测其一而宣称覆盖。" % (e, ext))
    gaps = [x for x in range(1, max(eps) + 1) if x not in eps]
    if gaps:
        raise SystemExit("【集号不连续】缺 ep%s —— 编号须连续，"
                         "否则「共 N 集」之实数将不可信。"
                         % "、".join("%02d" % g for g in gaps))
    return eps


def cross_source():
    """跨源互证：delivery 逐句是否见于 hyuanyanhai 之九九華嚴材料

    〔L.111·自纠〕初版用 `glob.glob('docs/huayanhai/**/*九九华严*/*.txt', recursive=True)`
    ——然本仓库该路径为**混合分隔符**（`docs/huayanhai\\华严云海\\…\\九九华严\\摘录\\…`），
    glob 匹配不到，致 corpus 为空而**静默返回 0 命中**，形似「跨源零重叠」之结论。
    实则根本没找到文件。改 `os.walk`，且**必回 rate 键**，使「未找到」与「零重叠」
    在输出上可区分——此即 L.107「空数据不得呈现为实测结论」之原则。
    """
    corpus = ""
    files = []
    for root, _dirs, fns in os.walk("docs/huayanhai"):
        if "九九华严" not in root:
            continue
        for fn in fns:
            if fn.lower().endswith((".txt", ".md")):
                files.append(os.path.join(root, fn))
                corpus += io.open(os.path.join(root, fn), encoding="utf-8",
                                  errors="replace").read()
    corpus = HAN.sub("", corpus)
    hit = tried = 0
    if corpus:
        for ep in discover_eps():
            for _, _, txt in cues_of_md(os.path.join(D, "ep%02d.md" % ep)):
                t = HAN.sub("", txt)
                if len(t) < 8:
                    continue
                tried += 1
                if t in corpus:
                    hit += 1
    return {"files": len(files), "corpus_chars": len(corpus),
            "hit": hit, "tried": tried,
            "found": bool(corpus),
            "rate": round(hit / tried, 5) if tried else None}


def main():
    # 〔内置自检〕先证 SIMP 表可用，再谈「混排 N 条」之实测数
    for probe in SIMP_SELFCHECK:
        if not SIMP.search(probe):
            print("【内置自检失败】SIMP 表未命中交付者自述实例「%s」——"
                  "「简繁混排」实测数不可信，工具中止。" % probe)
            return 1
    eps = discover_eps()
    rows = [audit_one(e) for e in eps]
    xs = cross_source()

    print("《九九華嚴》華嚴經弘法講座 2026 · %d 集 OCR 重建稿 质量实测" % len(eps))
    print("來源：大华严寺官方 YouTube（@huayen-world）· 台北國際會議中心 · 2026-04→07")
    print("產出性質：OCR 重建稿·**待校定**（寺方原始字幕稿已遺失）\n")
    hdr = ("ep", "字幕条", "md/srt/html", "声明时长", "覆蓋至", "覆盖率",
           "汉字", "片头", "拼接", "拉丁", "纯拉丁", "简混", "短句", "污染率")
    print("%-4s %6s %12s %8s %8s %7s %7s %5s %5s %5s %6s %5s %5s %7s"
          % hdr)
    print("-" * 118)
    KEYMAP = {"cues": "cues", "han": "han_chars",
              "head": "head_garbage_cues", "pipe": "pipe_cues",
              "lat": "latin_cues", "lonly": "latin_only_cues",
              "simp": "simp_cues", "sh": "short_cues"}
    T = dict(cues=0, han=0, head=0, pipe=0, lat=0, lonly=0, simp=0, sh=0)
    for r in rows:
        print("%-4d %6d %12s %8s %8s %6.1f%% %7d %5d %5d %5d %6d %5d %5d %6.2f%%"
              % (r["ep"], r["cues"],
                 "%d/%d/%d%s" % (r["cues"], r["cues_srt"], r["cues_html"],
                                  "" if r["consistent"] else "✗"),
                 "%d:%02d" % (r["declared_sec"] // 60, r["declared_sec"] % 60)
                 if r["declared_sec"] else "—",
                 "%d:%02d" % (r["covered_sec"] // 60, r["covered_sec"] % 60),
                 100.0 * r["coverage"] if r["coverage"] else 0,
                 r["han_chars"], r["head_garbage_cues"], r["pipe_cues"],
                 r["latin_cues"], r["latin_only_cues"], r["simp_cues"],
                 r["short_cues"], 100.0 * r["pollution_rate"]))
        # 〔L.111·自纠〕初版以 `r["%s_cues" % k]` 拼键，然 T 之键名与 r 之键名
        #   并不对应（lat↔latin、lonly↔latin_only、sh↔short、head↔head_garbage），
        #   遂 KeyError。改为**显式映射**——不得以「拼字符串」代替对账。
        # 〔L.111·自纠二〕此段曾被误置于 for 循环之外，遂合计＝**末集**之数
        #   而非总和，且输出看似合理——**正是「静默错算」之典型**。
        for k in T:
            T[k] += r[KEYMAP[k]]
    print("-" * 118)
    print("合计 字幕 %d 条／汉字 %d／片头可弃 %d／幻燈片拼接 %d／含拉丁 %d"
          "／纯拉丁 %d／简繁混排 %d／短句(≤2字) %d"
          % (T["cues"], T["han"], T["head"], T["pipe"], T["lat"], T["lonly"],
             T["simp"], T["sh"]))
    ncons = len([r for r in rows if r["consistent"]])
    print("md/srt/html 条数相符：%d/%d 集" % (ncons, len(rows)))
    covs = [r["coverage"] for r in rows if r["coverage"]]
    print("覆盖率：最低 %.1f%%／最高 %.1f%%／均值 %.1f%%"
          % (100 * min(covs), 100 * max(covs), 100 * sum(covs) / len(covs)))
    if xs["found"]:
        print("\n〔跨源互证〕与 hyuanyanhai《九九華嚴》材料（%d 件／%d 汉字）"
              "之逐句命中：%d/%d（%.3f%%）"
              % (xs["files"], xs["corpus_chars"], xs["hit"], xs["tried"],
                 100 * xs["rate"] if xs["rate"] else 0))
    else:
        print("\n〔跨源互证〕**未找到** hyuanyanhai 之《九九華嚴》材料——"
              "此为「检索未及」，**不得**表述为「跨源零重叠」之实测结论。")

    if "--json" in sys.argv:
        out = {"episodes": rows, "cross_source": xs, "totals": T}
        io.open(".tmp_jj_audit.json", "w", encoding="utf-8", newline="\n").write(
            json.dumps(out, ensure_ascii=False, indent=1))
        print("\n已写 .tmp_jj_audit.json（供立册生成器消费，避免手填）")
    return 0


if __name__ == "__main__":
    sys.exit(main())