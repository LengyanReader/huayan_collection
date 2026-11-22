# -*- coding: utf-8 -*-
"""_l522_shengpin.py — L.522 升会/偈赞小品收尾批：
①P13 升须弥山顶：+5.1′ 演义钞窗＋5.4′ 道霈窗
②P19 昇夜摩天宫：+演义钞窗（会仪贯通判）＋5.10 立节＋升叠互链
③P20 夜摩宫中偈赞：+演义钞窗（十行建立五义·起信引）＋偈赞叠互链
④P24 兜率宫中偈赞：+演义钞窗（幢五义·刊定七义）＋5.10 立节＋叠互链
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


T6 = norm('data/references/cbeta_txt/T1736_澄观_随疏演义钞.txt')
TB = norm('data/references/cbeta_txt/B0002_疏论纂要_epub提取本.txt')
M59 = re.compile(r'^### 5\.9 新加坡白话浅释选录', re.M)


def win(label, src, pos, stop=None, limit=340):
    t = T6 if src == 'T1736' else TB
    w = cut(t[pos:pos + 1400], limit, stop)
    return ('**%s**（`%s`·L.522 补窗）****' % (label, src)) .replace('**（', '（').replace('）****', '）') + \
        ('（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n' % (han(w), w.replace('\n', ' ')))


def add_ledger(md, text):
    ml = re.search(r'^## 九[、　]台账[^\n]*\n', md, re.M)
    assert ml
    return md[:ml.end()] + text + '\n' + md[ml.end():]


# ══ ① P13 ══
fp = gpat('华严经细读_第十三部_*.md')
md = io.open(fp, encoding='utf-8').read()
if 'L.522 补窗' not in md:
    w6 = cut(T6[T6.find('升須彌山頂品第十三', 460000):460923 + 1300])
    assert '品名須彌' in w6
    wb = cut(TB[TB.find('升須彌山頂品第十三', 452000):452819 + 1400])
    assert '四門分別' in wb
    s51 = ('### 5.1′ 澄观《隨疏演義鈔》窗（`T1736`·L.522 补窗）\n\n'
           '**演义钞窗·品名表位释**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
           '> **按语**〔本文判断〕演义钞释品名「須彌」——妙高表位：七金山七重圍繞而須彌處中，**十住之位即妙高之体**；并出「妙有十義」通释——升会之「处」全转为教具。\n\n' % (han(w6), w6.replace('\n', ' ')))
    s54 = ('### 5.4′ 道霈《華嚴經疏論纂要》窗（`B0002`·L.522 补窗）\n\n'
           '**纂要窗·四门（会来·品来·释名）**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
           '> **按语**〔本文判断〕纂要判双来意——「前品說信究竟。此品趣後說住」：信（品11-12）为住之方便、本品入正位；会名三门（忉利天會／法慧菩薩會／十住會）皆依主釋——与 §5.9 新加坡来意对读。\n\n' % (han(wb), wb.replace('\n', ' ')))
    m52 = re.search(r'^### 5\.2 法藏《大方[广廣]佛华[严嚴]经探玄[记記]》', md, re.M)
    assert m52, 'P13 5.2'
    md = md[:m52.start()] + s51 + '\n' + md[m52.start():]
    m59 = M59.search(md)
    assert m59
    md = md[:m59.start()] + s54 + '\n' + md[m59.start():]
    md = add_ledger(md, '- **L.522（2026-11-22）补窗批**：新增 §5.1′ 演义钞窗（品名妙高表位·妙有十義）＋§5.4′ 道霈窗（双来意·信为住之方便）——五家窗齐。')
    io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    print('① P13 ✓')

# ══ ② P19 ══
fp = gpat('华严经细读_第十九部_*.md')
md = io.open(fp, encoding='utf-8').read()
if 'L.522 补窗' not in md:
    w6 = cut(T6[T6.find('夜摩天宮品第十九', 526000):527021 + 1200], 340, '餘義多同須彌頂品。')
    assert '通上三會' in w6
    s = ('**澄观《隨疏演義鈔》·演义钞窗（会仪贯通判）**（`T1736`·L.522 补窗）**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
         '> **按语**〔本文判断〕演义钞判「則而演說法通上三會」——第三會不離前二會而昇忉利·今加不離須彌頂上而法慧說十住：**升会即加会**——每一会承前会之法而加说新法，三会法一贯（承 §四′ 升四义之「不离前会而升」）。\n' % (han(w6), w6.replace('\n', ' ')))
    m59 = M59.search(md)
    assert m59
    md = md[:m59.start()] + s + '\n' + md[m59.start():]
    # 5.10 立节（包裹既有宣化窗）
    ix = md.find('**宣化上人《華嚴經淺釋》')
    assert ix > 0
    md = md[:ix] + '### 5.10 宣化上人《華嚴經淺釋》限量选段\n\n> **来源与纪律**：宣化上人《大方廣佛華嚴經淺釋》（法界佛教总会在线文本 DRBA）。**限量引用**（每章 ≤2 段·句界截断）；浅释口语照录，讲者之误只标不改。\n\n' + md[ix:]
    md = add_ledger(md, '- **L.522（2026-11-22）补窗批**：新增演义钞窗（「演說法通上三會」会仪贯通判——升会即加会）＋5.10 立节（宣化窗自 L.504 批既有·本批立节）；升叠互链（品13→19→23）。')
    # 升叠互链
    m4 = re.search(r'^## 四[、　]', md, re.M)
    assert m4
    md = md[:m4.start()] + '\n> **L.522 升叠互链**：升会三叠（品13 忉利·品19 夜摩·品23 兜率）——「不离而升」一式三叠，`P13`／`P23` 可对读。\n' + md[m4.start():]
    io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    print('② P19 ✓')

# ══ ③ P20 ══
fp = gpat('华严经细读_第二十部_*.md')
md = io.open(fp, encoding='utf-8').read()
if 'L.522 补窗' not in md:
    w6 = cut(T6[T6.find('夜摩宮中偈讚品第二十', 527000):527127 + 1300])
    assert '表十行建立' in w6
    s = ('**澄观《隨疏演義鈔》·演义钞窗（十行建立五义）**（`T1736`·L.522 补窗）**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
         '> **按语**〔本文判断〕演义钞判本品「表十行建立故」五义——「於法性無修之中而起修故」居首（无修而修·十行之纲领），并引《起信論》「以知法性無慳貪故。隨順修行檀波羅蜜等」——**性德起修**的起信式论证；「庇映者。一一行門與慈悲俱。普蔭一切」——行行相映。\n' % (han(w6), w6.replace('\n', ' ')))
    m59 = M59.search(md)
    assert m59
    md = md[:m59.start()] + s + '\n' + md[m59.start():]
    m4 = re.search(r'^## 四[、　]', md, re.M)
    assert m4
    md = md[:m4.start()] + '\n> **L.522 偈赞叠互链**：偈赞三叠（品14→品20→品24）——每会正说前先陈体性（`P14`／`P24` 对读）；本品偈赞所陈即十行体性（品21 正说随之）。\n' + md[m4.start():]
    md = add_ledger(md, '- **L.522（2026-11-22）补窗批**：新增演义钞窗（十行建立五义·起信「性德起修」引·庇映慈悲）＋偈赞叠互链（品14→20→24）。§四 本体已厚（4.1 觉林偈）不重写。')
    io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    print('③ P20 ✓')

# ══ ④ P24 ══
fp = gpat('华严经细读_第二十四部_*.md')
md = io.open(fp, encoding='utf-8').read()
if 'L.522 补窗' not in md:
    w6 = cut(T6[T6.find('兜率宮中偈讚品第二十四', 604000):604919 + 1300])
    assert '幢者略有五義' in w6
    s = ('**澄观《隨疏演義鈔》·演义钞窗（幢五义·刊定七义）**（`T1736`·L.522 补窗）**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
         '> **按语**〔本文判断〕演义钞释「幢」五义（高出·建立·歸向·摧殄·等）而勘《刊定記》七义略其二——「修戒定慧如帝釋幢不移轉故」（涅槃引）：**幢＝行法之不动相**——回向位之幢（金刚幢领衔·品25 说主）正是坚固不坏之表（承 §四′ 金刚幢领衔系）。\n' % (han(w6), w6.replace('\n', ' ')))
    m59 = M59.search(md)
    assert m59
    md = md[:m59.start()] + s + '\n' + md[m59.start():]
    ix = md.find('**宣化上人《華嚴經淺釋》')
    assert ix > 0
    md = md[:ix] + '### 5.10 宣化上人《華嚴經淺釋》限量选段\n\n> **来源与纪律**：宣化上人《大方廣佛華嚴經淺釋》（法界佛教总会在线文本 DRBA）。**限量引用**（每章 ≤2 段·句界截断）；浅释口语照录，讲者之误只标不改。\n\n' + md[ix:]
    m4 = re.search(r'^## 四[、　]', md, re.M)
    assert m4
    md = md[:m4.start()] + '\n> **L.522 叠互链**：偈赞三叠（品14→品20→品24·`P14`／`P20` 对读）＋升叠（品13→19→品23·本品第三叠·`P19` 对读）——两叠在本品交汇：偈赞承升会而来。\n' + md[m4.start():]
    md = add_ledger(md, '- **L.522（2026-11-22）补窗批**：新增演义钞窗（幢五义·刊定七义勘略·帝釋幢不移轉——幢即行法不动相）＋5.10 立节＋两叠互链（偈赞叠×升叠在本品交汇）。')
    io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    print('④ P24 ✓')
print('L.522 done')
