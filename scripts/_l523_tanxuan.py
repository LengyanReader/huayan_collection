# -*- coding: utf-8 -*-
"""_l523_tanxuan.py — L.523 探玄/智俨补齐批（七会品目五家窗全齐）：
①P33/P34/P35/P36 各补探玄＋智俨窗（c60 品28-31 对应·释名来意宗趣带）
②P35 新增 §6.1 六十〈佛小相光明功德品〉全引对读（异题第三例）
③P30 补探玄窗（〈阿僧祇品第二十五〉释·数系四说）
④P37 补探玄窗（〈寶王如來性起品〉释）
"""
import glob, io, json, re, sys, unicodedata

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


def ins52(md, s):
    m59 = re.search(r'^### 5\.9 新加坡白话浅释选录', md, re.M)
    assert m59
    return md[:m59.start()] + s + '\n' + md[m59.start():]


def bw(label, t, pos, stop=None, limit=340):
    w = cut(t[pos:pos + 1500], limit, stop)
    src = 'T1733' if t is T3 else 'T1732'
    return '**%s**（`%s`·L.523 补窗·%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n' % (
        label, src, han(w), w.replace('\n', ' '))


JOBS = [
    ('华严经细读_第三十三部_*.md', [
        bw('法藏《探玄記》——〈佛不思議法品第二十八〉釋名·三來意（六十品次）', T3, T3.find('佛不思議法品第二十八', 465000)),
        bw('智俨《搜玄分齊通智方軌》——〈佛不思議法品〉三身判', T2, T2.find('佛不思議法品第二十八', 103000)),
    ], '> **按语**〔本文判断〕探玄三来意判「念法悕說。非是別請」——果法深细故须念请（与 §四 念请判互证）；智俨三身判「初不思議即法身德。次相海即報身德。次小相即化身德」——**三品即三德**：本品以下相海/随好两品在三身框架中读。'),
    ('华严经细读_第三十四部_*.md', [
        bw('法藏《探玄記》——〈如來相海品第二十九〉釋名·勘梵·体性判', T3, T3.find('如來相海品第二十九', 474000)),
        bw('智俨《搜玄分齊通智方軌》——〈如來相海品〉一乘相判', T2, T2.find('如來相海品第二十九', 106000)),
    ], '> **按语**〔本文判断〕探玄勘梵「名如來十身相海品——以深廣之相在十身故」并立相义八门（智論「顯著義」）；智俨判「此文是一乘相。故如海也」——三乘三十二相/一乘相海之拣（与 §四 九十七相实测对读）。'),
    ('华严经细读_第三十五部_*.md', [
        bw('法藏《探玄記》——〈佛小相光明功德品第三十〉釋名·來意（六十品次）', T3, T3.find('佛小相光明功德品第三十', 479000)),
        bw('智俨《搜玄分齊通智方軌》——〈佛小相光明功德品〉佛自说判', T2, T2.find('佛小相光明功德品第三十', 106900)),
    ], '> **按语**〔本文判断〕探玄判「**為大相難明故辨小相**。小相復多。但論一相。一相有多時之益」——随好之益由小入深；智俨判「化身之用唯佛方窮故佛自說」——与 §四 天鼓无说而说对读：佛说/鼓说/自说三重说法相。'),
    ('华严经细读_第三十六部_*.md', [
        bw('法藏《探玄記》——〈普賢菩薩行品第三十一〉修生/平等因果组判', T3, T3.find('普賢菩薩行品第三十一', 483000)),
        bw('智俨《搜玄分齊通智方軌》——〈普賢菩薩行品〉自体因果判', T2, T2.find('普賢菩薩行品第三十一', 107800)),
    ], '> **按语**〔本文判断〕探玄组判「上來明修生因果竟。自下二品明修顯因果。亦是上明差別因果。下顯平等因果」——普贤行/性起两品为平等因果对（与 §5.2 五家组判互证）；智俨判自体因果「離性泯始終即屬此」——普贤行之体即性。'),
]

for pat, wins, ayu in JOBS:
    fp = gpat(pat)
    md = io.open(fp, encoding='utf-8').read()
    if 'L.523 补窗' in md:
        print('skip（已应用）:', pat[:14])
        continue
    sec = '\n\n'.join(wins) + '\n\n' + ayu + '\n'
    md = ins52(md, sec)
    md = add_ledger(md, '- **L.523（2026-11-22）探玄/智俨补齐批**：§5.2 补探玄窗＋智俨窗各一（c60 对应品釋名來意宗趣带·六十品次）——五家窗齐（澄观疏/演义钞/探玄/智俨/李论/合论/纂要）。')
    io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    print('done:', pat[:14])

# ══ P35 §6.1 异题全引对读 ══
fp35 = gpat('华严经细读_第三十五部_*.md')
md35 = io.open(fp35, encoding='utf-8').read()
if 'L.523 异题' not in md35:
    d6 = json.load(open('web/demo/data/sutra/c60/p030.json', encoding='utf-8'))
    t6 = re.sub(r'\s+', '', '\n'.join(x for s in d6['segs'] for x in s['paras']))
    sec61 = '''### 6.1 六十华严（`T0278`〈佛小相光明功德品〉第三十·全引对读）

> **异题第三例（L.523）**：六十〈佛小相光明功德品〉＝八十〈隨好光明功德品〉——「小相／隨好」异题同品（前二例：〈壽命品〉＝〈壽量品〉·〈心王菩薩問阿僧祇品〉题式异）；六十〈如來相海品〉＝八十〈十身相海品〉（探玄勘梵本同名）。

**六十·全引**（`c60/p030.json`·%d 字·照录）：

> %s

**对照要点**（〔本文判断〕）：①六十题「小相」就形立名、八十题「隨好」随大相立名——一形一饰，所指同一（探玄：「依前大相流出形好故次來也」）；②「佛自说」两译同（智俨：「化身之用唯佛方窮故」）；③八十增广处待逐段勘〔未竟〕。

''' % (han(t6), t6)
    m6 = re.search(r'^## 六、文本对读', md35, re.M)
    assert m6
    md35 = md35[:m6.start()] + sec61 + '\n' + md35[m6.start():]
    md35 = add_ledger(md35, '- **L.523（2026-11-22）异题批**：新增 §6.1 六十〈佛小相光明功德品〉全引对读——**异题第三例**（小相/隨好·一形一饰所指同一）；探玄「依前大相流出形好」即两品相承之据。')
    io.open(fp35, 'w', encoding='utf-8', newline='').write(md35)
    print('P35 §6.1 异题对读 ✓')

# ══ P30 探玄窗 ══
fp30 = gpat('华严经细读_第三十部_*.md')
md30 = io.open(fp30, encoding='utf-8').read()
if 'L.523 补窗' not in md30:
    w = cut(T3[T3.find('阿僧祇品第二十五', 461000):461202 + 1700], 430, '約圓教辨也。')
    assert '數至六十重' in w
    s = ('**法藏《探玄記》——〈阿僧祇品第二十五〉釋名·來意·宗趣·数系四说**（`T1733`·六十品次·L.523 补窗）**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
         '> **按语**〔本文判断〕探玄释名「心王菩薩是能問人。**表數法依心**」——数门即心门之六十印证；宗趣「一能數之數。二所數之德」；**数系四说**（俱舍六十重約小乘／智論數過十重……）为 §四′ 三「数的系统比较」（黄帝23/小乘60/华严124）之**论据源**——小乘六十出自《俱舍》、华严百二十四倍倍變与之对照，判教之尺由此坐实。\n' % (han(w), w.replace('\n', ' ')))
    m59 = re.search(r'^### 5\.9 新加坡白话浅释选录', md30, re.M)
    assert m59
    md30 = md30[:m59.start()] + s + '\n' + md30[m59.start():]
    md30 = add_ledger(md30, '- **L.523（2026-11-22）补窗批**：§5.2 补探玄窗（〈阿僧祇品第二十五〉六十品次·釋名「表數法依心」·宗趣能所二数·**数系四说**——俱舍/智論为 §四′ 数系比较论据源）——五家窗齐。')
    io.open(fp30, 'w', encoding='utf-8', newline='').write(md30)
    print('P30 探玄窗 ✓')

# ══ P37 探玄窗 ══
fp37 = gpat('华严经细读_第三十七部_*.md')
md37 = io.open(fp37, encoding='utf-8').read()
if 'L.523 补窗' not in md37:
    w = cut(T3[T3.find('寶王如來性起品', 487000):487104 + 1400])
    assert '性起' in w
    s = ('**法藏《探玄記》——〈寶王如來性起品〉释（六十品次·L.523 补窗）**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
         '> **按语**〔本文判断〕探玄性起品释与 §6.1 六十对读直通——贤首宗「性起」题之本据层；与 §5.2 智俨「性者體。起者現在心地」并读：二祖释同品而探玄存六十旧题（寶王）。\n' % (han(w), w.replace('\n', ' ')))
    m59 = re.search(r'^### 5\.9 新加坡白话浅释选录', md37, re.M)
    assert m59
    md37 = md37[:m59.start()] + s + '\n' + md37[m59.start():]
    md37 = add_ledger(md37, '- **L.523（2026-11-22）补窗批**：§5.2 补探玄窗（〈寶王如來性起品〉六十品次释）——五家窗齐。')
    io.open(fp37, 'w', encoding='utf-8', newline='').write(md37)
    print('P37 探玄窗 ✓')
print('L.523 done')
