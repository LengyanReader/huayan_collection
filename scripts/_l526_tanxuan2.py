# -*- coding: utf-8 -*-
"""_l526_tanxuan2.py — L.526 探玄补齐批二（会4-5·异题第四~七例）：
P19/P21/P22/P23/P25/P29 补探玄窗（c60 品15/17/18/19/21/24 对应带·P29 兼智俨窗）
"""
import glob, io, re, sys, unicodedata

sys.stdout.reconfigure(encoding='utf-8')
HAN = re.compile(r'[\u3400-\u9fff]')


def han(s):
    return len(HAN.findall(s))


def norm(p):
    t = io.open(p, encoding='utf-8').read()
    return unicodedata.normalize('NFKC', re.sub(r'<<<PAGE \d+>>>', '', t))


def cut(raw, limit=340, stop=None):
    if stop:
        i = raw.find(stop)
        if i > 0:
            return raw[:i + len(stop)]
    acc = 0
    for k, ch in enumerate(raw):
        if HAN.match(ch):
            acc += 1
        if acc >= limit and ch in '。；':
            return raw[:k + 1]
    return raw[:limit]


def gpat(pat):
    g = glob.glob('docs/经学文献/华严经细读/**/' + pat, recursive=True)
    assert g, pat
    return g[0]


T3 = norm('data/references/cbeta_txt/T1733_法藏_探玄记.txt')
T2 = norm('data/references/cbeta_txt/T1732_智俨_搜玄记.txt')


def add_ledger(md, text):
    ml = re.search(r'^## 九[、　]台账[^\n]*\n', md, re.M)
    assert ml
    return md[:ml.end()] + text + '\n' + md[ml.end():]


def bw(label, t, pos, stop=None, limit=340):
    w = cut(t[pos:pos + 1500], limit, stop)
    src = 'T1733' if t is T3 else 'T1732'
    return '**%s**（`%s`·L.526 补窗·%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n' % (
        label, src, han(w), w.replace('\n', ' '))


JOBS = [
    ('华严经细读_第十九部_*.md', [
        bw('法藏《探玄記》——〈夜摩天宮自在品第十五〉釋名（六十品次·蘇夜摩=善時分）', T3, T3.find('夜摩天宮自在品第十五', 173000)),
    ], '> **按语**〔本文判断〕探玄释名引《大集經》「觀赤蓮華開是晝。青蓮華開是夜」——时分天之无日月知时（承 §四′ 时分天判·宜适其时）；会名三门（夜摩天會／功德林會／十行會）与 §5.9 会名三义互证。'),
    ('华严经细读_第二十一部_*.md', [
        bw('法藏《探玄記》——〈十行品第十七〉釋名·來意（六十题「功德華聚」）', T3, T3.find('十行品第十七', 179000)),
    ], '> **按语**〔本文判断〕探玄释名「十度利潤體名功德……眾行交飾如華聚。又德是行體。華是行用。聚是行相」——**异题第四例**（六十〈功德華聚菩薩十行品〉＝八十〈十行品〉）：题名即十行结构之缩写（德体·华用·聚相）；「此是功德林之異名。如下金剛幢迴向品相似」——说主题名之通例（行主功德林·向主金刚幢）。'),
    ('华严经细读_第二十二部_*.md', [
        bw('法藏《探玄記》——〈十無盡藏品第十八〉釋名·无尽三义·來意五义', T3, T3.find('十無盡藏品第十八', 205000)),
    ], '> **按语**〔本文判断〕探玄释名立**无尽三义**（含攝蘊積出生名藏／一一各攝一切行相／一一皆能出生果德無有窮竭）——与 §四′ 体五用五及 L.512 图〇-2 对读：无尽非量词而是结构义。'),
    ('华严经细读_第二十三部_*.md', [
        bw('法藏《探玄記》——〈昇兜率天一切寶殿品第十九〉會名·品名（六十题「一切寶殿」）', T3, T3.find('昇兜率天一切寶殿品第十九', 212000)),
    ], '> **按语**〔本文判断〕**异题第五例**（六十〈昇兜率天一切寶殿品〉＝八十〈昇兜率天宮品〉）；探玄会名三门（兜率天會／金剛幢會／十迴向會）＋「赴此喜足天者**表世間行滿故也**。一切寶者表攝行多門」——兜率=知足=世间行满之位（承 §四′ 第三叠位义）。'),
    ('华严经细读_第二十五部_*.md', [
        bw('法藏《探玄記》——〈金剛幢菩薩迴向品第二十一〉釋名·來意（六十题带说主）', T3, T3.find('金剛幢菩薩迴向品第二十一', 221000)),
    ], '> **按语**〔本文判断〕**异题第六例**（六十〈金剛幢菩薩迴向品〉＝八十〈十回向品〉——题带说主）；探玄释名「**迴已善根向於三處**」——三处即众生/菩提/实际（承 §四′ 三向并运之古据）；「德成無壞喻號金剛。獨出世間舉幢以表」——金刚幢之名即回向体（坚固不坏·高显标相）。'),
    ('华严经细读_第二十九部_*.md', [
        bw('法藏《探玄記》——〈十忍品〉答位配对·定忍明辨（六十品次）', T3, T3.find('十忍品答', 102000), None, 340),
        bw('智俨《搜玄分齊通智方軌》——〈十忍品二十四〉忍义·约位判', T2, T2.find('十忍品二十四', 101000)),
    ], '> **按语**〔本文判断〕探玄判「觀心納理為忍。止心不散為定。止觀無礙唯是一心」——定忍配对（承 P27/P29 邻品关系之古据）并及十明品答、兜沙译名、梵网计会之辩；智俨「**忍者境與神會情諦可也**」＋约位判（前二加行摄·無生忍正體攝·約位音聲三地已還順忍四五六十地……）——十忍的行位配属表。另：六十于十忍前有〈十明品〉第二十三独立品（八十并入〈佛不思議法品〉十明节）——**品目分合异例**。'),
]

for pat, wins, ayu in JOBS:
    fp = gpat(pat)
    md = io.open(fp, encoding='utf-8').read()
    if 'L.526 补窗' in md:
        print('skip:', pat[:14])
        continue
    sec = '\n\n'.join(wins) + '\n\n' + ayu + '\n'
    m59 = re.search(r'^### 5\.9 新加坡白话浅释选录', md, re.M)
    assert m59, pat
    md = md[:m59.start()] + sec + '\n' + md[m59.start():]
    md = add_ledger(md, '- **L.526（2026-11-22）探玄补齐批二**：§5.2 补探玄窗（c60 对应品釋名來意宗趣带·六十品次）——**异题第四至六例**（功德華聚＝十行·一切寶殿＝昇兜率·金剛幢迴向＝十回向）＋十明品分合异例记。')
    io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    print('done:', pat[:14])
print('L.526 done')
