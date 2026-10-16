#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pilu_shena_studies.py — 第六品《毘盧遮那品》數據科學層（L1–L4）復算腳本

口徑（與第六部 §七 各表一致，可一命令復算）：
  * 底本    : data/references/cbeta/T10n0279.xml（八十華嚴，繁體原字形）
  * 範圍    : 品題 <head>「毘盧遮那品第六」起，至次品題 <head>「如來名號品第七」止。
              本品佔卷第十一（一品一卷）。
  * 剝校勘  : 完全剔除 <note>…</note> 與 <app>…</app>（連同其內文字）；
              並剝 CBETA 結構標記 <cb:juan>、<byline>、<cb:mulu>，以免卷題
              「大方廣佛華嚴經卷第N」與譯人題混入字數。
  * 計數    : 再剝一切標籤；**並壓除所有空白**（XML 排版換行會把
              「佛號」等連字切成「佛\n號」，不壓除則少計），僅計 CJK(3400–9FFF)。
  * 偈頌    : 以 <l> 行計，兩行（＝4 句）為一頌（與李通玄「兩行為一頌」合）。
  * 依賴    : 僅標準庫（無 numpy / networkx），純 Python 可復算。

用法: python scripts/pilu_shena_studies.py
"""
import re, io, sys, json, math, unicodedata
from collections import Counter

BASE = r'c:\DA_Practice\huayan_collection'
XML = BASE + r'\data\references\cbeta\T10n0279.xml'

RAD = {'\u2ef6': '日', '\u2ef7': '月', '\u2ed1': '長', '\u2ec5': '門', '\u2eda': '頁',
       '\u2edb': '風', '\u2ed8': '飛', '\u2ec3': '食'}


def norm(s):
    return ''.join(RAD.get(c, c) for c in unicodedata.normalize('NFKC', s))


def strip_apparatus(s):
    s = re.sub(r'<note\b.*?</note>', '', s, flags=re.S)
    s = re.sub(r'<app\b.*?</app>', '', s, flags=re.S)
    s = re.sub(r'<cb:juan\b.*?</cb:juan>', '', s, flags=re.S)
    s = re.sub(r'<byline\b.*?</byline>', '', s, flags=re.S)
    s = re.sub(r'<cb:mulu\b.*?</cb:mulu>', '', s, flags=re.S)
    return s


def plain(span):
    """標籤全剝＋空白全壓（計數用）。"""
    s = re.sub(r'<[^>]+>', '', strip_apparatus(span))
    return re.sub(r'\s+', '', s)


def cjk_only(s):
    return ''.join(c for c in norm(s) if '\u3400' <= c <= '\u9fff')


def ols_zipf(chars):
    freq = Counter(chars)
    items = sorted(freq.values(), reverse=True)
    xs = [math.log(i + 1) for i in range(len(items))]
    ys = [math.log(v) for v in items]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / sxx, sxy / math.sqrt(sxx * syy)


def entropy(chars):
    freq = Counter(chars)
    N = len(chars)
    return -sum((v / N) * math.log2(v / N) for v in freq.values())


PIN = '毘盧遮那品第六'
NEXT = '如來名號品第七'

# 四佛次第（本事故之骨架；依 T1735 科判）
FOB = {
    'b1': ('其第一佛，號：一切功德山須彌勝雲', '有佛出世，名：波羅蜜善眼莊嚴王'),
    'b2': ('有佛出世，名：波羅蜜善眼莊嚴王', '第三如來出現於世，名：最勝功德海'),
    'b3': ('第三如來出現於世，名：最勝功德海', '復有佛出，號：名稱普聞蓮華眼幢'),
    'b4': ('復有佛出，號：名稱普聞蓮華眼幢', None),
}


def analyse():
    xml = open(XML, encoding='utf-8').read()
    a = xml.find(PIN)
    b = xml.find(NEXT)
    span = xml[a:b]

    text = plain(span)
    out = {}

    # L1 語言統計
    allcjk = cjk_only(text)
    freq = Counter(allcjk)
    slope, R = ols_zipf(allcjk)
    l_lines = len(re.findall(r'<l>', span))
    out['L1'] = dict(
        cjk_total=len(allcjk), cjk_net=len(allcjk) - len(cjk_only(PIN)),
        unique=len(freq), H=round(entropy(allcjk), 4),
        zipf_slope=round(slope, 4), zipf_R=round(R, 4),
        sent_ends=len(re.findall(r'[。！？]', text)),
        p_blocks=len(re.findall(r'<p\b', span)), lg_groups=len(re.findall(r'<lg\b', span)),
        l_lines=l_lines, verses=l_lines // 2,
        lb=len(re.findall(r'<lb\b', span)), pb=len(re.findall(r'<pb\b', span)),
        caesura=len(re.findall(r'<caesura/>', span)),
        note=len(re.findall(r'<note\b', span)), app=len(re.findall(r'<app\b', span)),
        top15=freq.most_common(15))

    # 長行 vs 偈頌 CJK 分計
    verses_html = re.findall(r'<lg\b.*?</lg>', span, re.S)
    vt = ''.join(plain(v) for v in verses_html)
    rest = span
    for v in verses_html:
        rest = rest.replace(v, '\x00')
    pt = ''.join(plain(x) for x in rest.split('\x00'))
    out['L1']['cjk_verse'] = len(cjk_only(vt))
    out['L1']['cjk_prose'] = len(cjk_only(pt))

    # 四佛分段：以「剝標籤後之字序」對回原始 span 位置（標記常跨 <lb>，不可直接 find）
    def align(span_s):
        """回傳 (plain_no_ws, spans) —— spans[k] 為第 k 個 plain 字在 span_s 之起點。"""
        buf, sp = [], []
        i, n = 0, len(span_s)
        while i < n:
            if span_s[i] == '<':
                j = span_s.find('>', i)
                i = j + 1 if j >= 0 else i + 1
                continue
            c = span_s[i]
            if not c.isspace():
                buf.append(c); sp.append(i)
            i += 1
        return ''.join(buf), sp

    ptxt, pmap = align(strip_apparatus(span))
    assert ptxt == text, 'align mismatch: %d vs %d' % (len(ptxt), len(text))
    base = strip_apparatus(span)
    out['seg'] = {}
    bounds = {}
    for nm, (h1, h2) in FOB.items():
        i = text.find(h1)
        bounds[nm] = (i, text.find(h2) if h2 else len(text))
    for nm in FOB:
        i, j = bounds[nm]
        if i < 0:
            out['seg'][nm] = None
            continue
        si, sj = pmap[i], (pmap[j] if j < len(text) else len(base))
        tg_span = base[si:sj]
        t = text[i:j]
        nl = len(re.findall(r'<l>', tg_span))
        out['seg'][nm] = dict(
            cjk=len(cjk_only(t)), sent_ends=len(re.findall(r'[。！？]', t)),
            p=len(re.findall(r'<p\b', tg_span)), lg=len(re.findall(r'<lg\b', tg_span)),
            l=nl, verses=nl // 2)

    # L2 名相枚舉之計量
    out['L2'] = dict(
        n_fo=len(re.findall(r'[號号]：([^。」，、；）]{2,22})', text)),   # 名號「…：X」計
        buddhas=[m.group(1) for m in re.finditer(
            r'(?:有佛出世，名：|其第一佛，號：|如來出現於世，名：|復有佛出，號：)([^。，；]{2,18})', text)],
        sutras=[m.group(1) for m in re.finditer(r'說([\u4e00-\u9fff]{4,20})修多羅', text)],
        cities=[m.group(1) for m in re.finditer(r'次有[\u4e00-\u9fff]{1,4}城，名[曰：]([^；，。]{2,12})', text)],
        n_cities=len(re.findall(r'次有[\u4e00-\u9fff]{1,4}城，名[曰：]', text)),
        n_sanmei=text.count('三昧'), n_tuoluoni=text.count('陀羅尼'),
        n_boluomi=text.count('波羅蜜'), n_shentong=text.count('神通'),
        n_biancai=text.count('辯才'), n_zhiguang=text.count('智光明'),
        n_famen=text.count('法門'), n_dizhong=text.count('法光'),
        xutuo_luo=text.count('修多羅'),
        n_weichen=text.count('微塵數'),
        n_xiangshui=text.count('香水海'), n_shijiehai=text.count('世界海'),
        n_xumi_ding=text.count('須彌山頂') + text.count('須彌山上'),
        n_baiwan_yi=text.count('百萬億那由他'),
        n_nauto=text.count('那由他'),
        numerals={n: text.count(n) for n in
                  ['十須彌山微塵數', '五十億歲', '十千法門', '三萬七千人', '五百人',
                   '六萬大臣', '七十七百千億那由他', '六十八千億須彌山頂',
                   '二萬五千', '恒河沙數小劫', '二小劫', '一百年']})

    # L3 關係·次第
    roles = ['大威光太子', '大威光菩薩', '大威光童子', '大威光王子',
             '大威光轉輪聖王', '大威光於此命終', '大威光為上首', '喜見善慧王',
             '福吉祥', '妙見', '慧力', '離垢福德幢']
    out['L3'] = dict(
        roles={r: text.count(r) for r in roles},
        awakes={k: text.count(k) for k in
                ['見佛光明', '證得', '即得', '得三昧', '得陀羅尼', '獲', '發菩提心', '承事供養']},
        places={k: text.count(k) for k in
                ['摩尼華枝輪大林', '焰光明大城', '寶華遍照', '香摩尼金剛',
                 '華蘂焰輪', '須彌山', '勝音世界', '普門淨光明']},
        who={k: text.count(k) for k in ['普賢菩薩', '諸佛子', '爾時', '時，彼佛', '時，彼如來']})

    # L4 自似·因·願
    out['L4'] = {k: text.count(k) for k in
                 ['往昔', '宿世', '本因', '因', '果', '願', '大願', '普賢',
                  '剎海', '嚴淨', '承事供養', '發菩提心', '成佛', '當得', '當成',
                  '一一', '一切', '無量', '不可思議', '不可說']}
    return out


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(json.dumps(analyse(), ensure_ascii=False, indent=1))
