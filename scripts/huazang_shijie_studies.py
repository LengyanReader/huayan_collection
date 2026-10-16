#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
huazang_shijie_studies.py — 第五品《華藏世界品》數據科學層（L1–L4）復算腳本

口徑（與第五部 §七 各表一致，可一命令復算）：
  * 底本    : data/references/cbeta/T10n0279.xml（八十華嚴，繁體原字形）
  * 範圍    : 品題 <head>「華藏世界品第五之一」起，至次品題 <head>「毘盧遮那品第六」止。
              本品佔卷八至卷十（品內分「之一／之二／之三」三段）。
  * 剝校勘  : 完全剔除 <note>…</note> 與 <app>…</app>（連同其內文字）；
              並剝 CBETA 結構標記 <cb:juan>、<byline>、<cb:mulu>，以免卷題
              「大方廣佛華嚴經卷第N」與譯人題混入字數。
  * 計數    : 再剝一切標籤；**並壓除所有空白**（XML 排版換行會把
              「佛號」等連字切成「佛\n號」，不壓除則少計），僅計 CJK(3400–9FFF)。
              此為本腳本與初稿第一版之差異，特記以免回退。
  * 依賴    : 僅標準庫（無 numpy / networkx），純 Python 可復算。

用法: python scripts/huazang_shijie_studies.py
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


def analyse():
    xml = open(XML, encoding='utf-8').read()
    a = xml.find('華藏世界品第五之一')
    b = xml.find('毘盧遮那品第六')
    span = xml[a:b]

    text = plain(span)                       # 標籤＋空白全剝，未 NFKC
    i1 = text.find('華藏世界品第五之一')
    i2 = text.find('華藏世界品第五之二')
    i3 = text.find('華藏世界品第五之三')
    seg_txt = {'p5_1': text[i1:i2], 'p5_2': text[i2:i3], 'p5_3': text[i3:]}
    pin = '華藏世界品第五之一華藏世界品第五之二華藏世界品第五之三'

    out = {}
    allcjk = cjk_only(text)
    freq = Counter(allcjk)
    slope, R = ols_zipf(allcjk)
    out['L1'] = dict(
        cjk_total=len(allcjk), cjk_net=len(allcjk) - len(cjk_only(pin)),
        unique=len(freq), H=round(entropy(allcjk), 4),
        zipf_slope=round(slope, 4), zipf_R=round(R, 4),
        sent_ends=len(re.findall(r'[。！？]', text)),
        p_blocks=len(re.findall(r'<p\b', span)), lg_groups=len(re.findall(r'<lg\b', span)),
        l_lines=len(re.findall(r'<l>', span)), verses=len(re.findall(r'<l>', span)) // 2,
        top15=freq.most_common(15))

    def tagslice(h1, h2):
        s = span.find(h1); e = span.find(h2) if h2 else len(span)
        return span[s:e]
    segdef = [('p5_1', '華藏世界品第五之一', '華藏世界品第五之二'),
              ('p5_2', '華藏世界品第五之二', '華藏世界品第五之三'),
              ('p5_3', '華藏世界品第五之三', None)]
    out['seg'] = {}
    for nm, h1, h2 in segdef:
        t = seg_txt[nm]; tg = tagslice(h1, h2)
        out['seg'][nm] = dict(cjk=len(cjk_only(t)), sent_ends=len(re.findall(r'[。！？]', t)),
                              p=len(re.findall(r'<p\b', tg)), lg=len(re.findall(r'<lg\b', tg)),
                              l=len(re.findall(r'<l>', tg)))

    out['motifs'] = {k: text.count(k) for k in
                     ['一一', '一切', '世界海', '世界種', '香水海', '香水河', '大輪圍山',
                      '大蓮華', '微塵', '微塵數', '佛剎微塵數', '不可說', '周匝圍遶',
                      '各各', '莊嚴', '清淨', '光明', '摩尼', '佛號', '此上過',
                      '如天帝網', '純一清淨', '毘盧遮那', '普賢', '法界', '虛空']}

    # L2 名相枚舉之計量
    ring = []
    for m in re.finditer(r'次有香水海，名：([^；，。]{2,20})', text):
        y = m.group(1)
        win = text[m.end():m.end() + 130]
        mw = re.search(r'世界種.{0,10}?名：([^，。；]{2,24})', win)
        ring.append((y, mw.group(1) if mw else '?'))
    # 之二＝索引 0-9（十方環）；之三＝索引 10 起（外圍）
    central = re.search(r'最中央香水海，名：([^，；。]{2,12})', text)
    czhong = re.search(r'最中央香水海.*?世界種.{0,10}?名：([^，。；]{2,24})', text)
    out['L2'] = dict(
        central_sea=central.group(1) if central else None,
        central_zhong=czhong.group(1) if czhong else None,
        n_seas_ring=seg_txt['p5_2'].count('次有香水海'),    # 之二＝十方環香水海數（10）
        n_seas_outer=seg_txt['p5_3'].count('次有香水海'),   # 之三＝外圍香水海數（89）
        n_seas_total=text.count('次有香水海'),              # 99
        n_zuijin=text.count('最近輪圍山'),                  # 9（第五段闕一）
        seas_ring=ring[:10],
        seas_outer=ring[10:],
        wang_haohao=text.count('佛號：'), wang_fohao=text.count('佛號'),
        qi_fo=text.count('其佛即是'),
        world_approx=text.count('佛號：') + text.count('其佛即是'),
        ci_shang_guo=text.count('此上過'),
        zhouza=text.count('周匝圍遶'),
        n_zhong_20=text.count('二十佛剎微塵數世界'),
        n_zhong_10=text.count('十佛剎微塵數世界'),
        ci_shang_10=text.count('此上過十佛剎微塵數世界'),
        yu_suopo=text.count('與娑婆世界齊等'),
        yu_jingangchuang=text.count('與金剛幢世界齊等'),
        numerals={n: text.count(n) for n in
                  ['一佛剎微塵數', '二佛剎微塵數', '三佛剎微塵數', '四佛剎微塵數',
                   '五佛剎微塵數', '六佛剎微塵數', '七佛剎微塵數', '八佛剎微塵數',
                   '九佛剎微塵數', '十佛剎微塵數', '十一佛剎微塵數', '十二佛剎微塵數',
                   '十三佛剎微塵數', '十四佛剎微塵數', '十五佛剎微塵數', '十六佛剎微塵數',
                   '十七佛剎微塵數', '十八佛剎微塵數', '十九佛剎微塵數', '二十佛剎微塵數']})

    # L3 方位與關係
    out['L3'] = {
        'dirs': {d: text.count('香水海' + d) for d in ['東', '南', '西', '北', '右旋', '外']},
        'kinds': {k: text.count(k) for k in
                  ['依', '形', '住', '圍遶', '彌覆', '為際', '為體', '齊等', '最下方', '最上方']}}

    # L4 自似與如幻
    out['L4'] = {k: text.count(k) for k in
                 ['一一', '一一塵中', '一一微塵', '一一毛孔', '一毛孔', '塵中',
                  '如影', '如幻', '如夢', '如鏡', '如天帝網', '因陀羅網', '帝網',
                  '無來無去', '不一不異', '一即一切', '遞相接連', '成世界網']}
    return out


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(json.dumps(analyse(), ensure_ascii=False, indent=1))
