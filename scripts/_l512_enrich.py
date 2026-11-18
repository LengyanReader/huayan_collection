# -*- coding: utf-8 -*-
"""_l512_enrich.py — L.512 P30 数门通考＋P21/P22 补图（可视化强化）"""
import io, re

W = 'width="100%" style="max-width:1000px;height:auto"'

# ══ 1) P30：§四″ 数门通考＋图〇-3 ══
fp30 = 'docs/经学文献/华严经细读/第七会_普光明殿_等觉/华严经细读_第三十部_阿僧祇品.md'
md30 = io.open(fp30, encoding='utf-8').read()
GUARD_30 = '四″、数门通考' not in md30

svg_dist = '''<svg viewBox="0 0 1000 300" %s xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="24" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#7a5a28">图 〇-3　三本数法分布图——阿僧祇数门在华严三本中的安置</text>
<rect x="40" y="50" width="290" height="200" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="185" y="78" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#7a5a28">八十華嚴（T10n0279）</text>
<text x="185" y="104" text-anchor="middle" font-size="11" fill="#5a5147">獨立品〈阿僧祇品〉第三十</text>
<text x="185" y="128" text-anchor="middle" font-size="11" fill="#5a5147">心王菩薩問·佛自說</text>
<text x="185" y="152" text-anchor="middle" font-size="11" fill="#5a5147">長行 124 級數法鏈</text>
<text x="185" y="176" text-anchor="middle" font-size="11" fill="#5a5147">偈頌百二十偈·十重積數</text>
<text x="185" y="212" text-anchor="middle" font-size="10.5" fill="#8a7a5e">數之終寄不可說</text>
<rect x="355" y="50" width="290" height="200" rx="10" fill="#eef3ef" stroke="#4a8a8f"/>
<text x="500" y="78" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#2e5a5e">四十華嚴（T10n0293）</text>
<text x="500" y="104" text-anchor="middle" font-size="11" fill="#3a5147">無獨立品——數法入〈入法界品〉</text>
<text x="500" y="128" text-anchor="middle" font-size="11" fill="#3a5147">自在主童子處（善財第 13 參）</text>
<text x="500" y="152" text-anchor="middle" font-size="11" fill="#3a5147">「菩薩算法」洛叉→俱胝→阿庾多…</text>
<text x="500" y="176" text-anchor="middle" font-size="11" fill="#3a5147">法門自陳「數／名」雙舉</text>
<text x="500" y="212" text-anchor="middle" font-size="10.5" fill="#5e7a5e">昔於文殊師利所修學算數印相</text>
<rect x="670" y="50" width="290" height="200" rx="10" fill="#f1eef6" stroke="#8a6a9e"/>
<text x="815" y="78" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#5a3a7a">六十華嚴（T09n0278）</text>
<text x="815" y="104" text-anchor="middle" font-size="11" fill="#4a4154">無獨立品·無數列</text>
<text x="815" y="128" text-anchor="middle" font-size="11" fill="#4a4154">洛叉 0 見·俱胝 0 見</text>
<text x="815" y="152" text-anchor="middle" font-size="11" fill="#4a4154">阿僧祇 6 見（通名泛用）</text>
<text x="815" y="176" text-anchor="middle" font-size="11" fill="#4a4154">那由他 18 見（泛用量詞）</text>
<text x="815" y="212" text-anchor="middle" font-size="10.5" fill="#6a5a7e">數門為八十系新置之教</text>
<text x="500" y="278" text-anchor="middle" font-size="11.5" fill="#5a5147">⇒ 檢索確認（L.512·三本詞頻實測）：數法門為八十華嚴新置；四十華嚴以「參學算法」存其用；六十華嚴無之</text>
</svg>''' % W

tongkao = '''### 四″、数门通考——华严数法的经典分布与义涵四维（L.512·检索确认）

> **体例**：本节承 §四′ 数义深考，回答两个问题：①华严三本中，数法门如何分布？②经典内外，「数」还有哪些面向？分布为**程序实测**（三本数词密度检索），义涵属〔本文判断〕层。

**A. 三本分布实测**（词频：全文检索·去空白）

| 本 | 洛叉 | 俱胝 | 阿庾多 | 那由他 | 阿僧祇 | 不可說 | 独立数品 |
|---|---|---|---|---|---|---|---|
| 八十 `T10n0279` | 71（〈阿僧祇品〉内） | 82 | 45 | 443 | 341 | 933 | **〈阿僧祇品〉品30** |
| 四十 `T10n0293` | 4 | 16 | 6 | 69 | 140 | 327 | 无——数法入〈入法界品〉 |
| 六十 `T09n0278` | **0** | **0** | **0** | 18（泛用） | 6（泛用） | 26（泛用） | 无 |

''' + '''<figure>
''' + svg_dist + '''
<figcaption style="font-size:.78em;color:var(--text2);line-height:1.85;max-width:760px;margin:6px auto 0"><b>图 〇-3　三本数法分布图。</b>八十华严将数法门**独立置品**（心王问·佛自说）；四十华严以「参学算法」存其用（自在主童子·数名双举）；六十华严无此数门——数法为八十系新置之教。</figcaption>
</figure>

**B. 四十华严·自在主童子「菩萨算法」**（`T10n0293`·善财第 13 参·照录）：

> ……善男子！我又善知一切聲論、音聲、語言、內外、因起、名字、訓釋普遍無窮，假使帝釋於梵王所，聽受聲明，盡其天壽，足滿千歲，亦不能知聲論邊際，我一念頃，以此算法，悉能了知，盡其源底。「善男子！彼復教我菩薩算法，所謂：百千為一洛叉；一百洛叉為一俱胝；俱胝俱胝為一阿庾多；阿庾多阿庾多為一那由他；那由他那由他為一頻婆羅；頻婆羅頻婆羅為一矜羯羅；……
>
> 「善男子！我昔曾於文殊師利童子所，修學算、數、印、相等法，即得悟入一切工巧神通智門。……我唯知此一切工巧大神通智光明法門，如諸菩薩摩訶薩，**能知一切諸眾生數，及知一切諸眾生名；能知一切法品類數，及知一切法品類名；能知三世諸時劫數，及知三世諸時劫名；能知一切諸如來數，及知一切諸如來名；能知一切諸菩薩數，及知一切諸菩薩名**……

**通考要点**（〔本文判断〕）：

1. **三本三安置**——八十**独立置品**（心王问·佛自说·数之终寄不可说）；四十以「参学算法」存其用（数门入行门：算法是善知识所教之**工巧**）；六十无此门。三本对读：数法门为八十华严教理新置之明确标志，而其**实用层**（菩萨算法）在四十的参学历程中保存。
2. **数名双举**——自在主童子法门自陈，五组皆「數／名」双举（眾生數·名／法品類數·名／時劫數·名／如來數·名／菩薩數·名）：**数量与名称是心王把握世界的两翼**——数（量）与名（相）双运，正与本品的问者「心王」呼应：数门即心门，名门亦心门。
3. **学算处＝文殊**——自在主自陈「昔曾於文殊師利童子所，修學算、數、印、相等法」：数法的**师承归于文殊**（大智）；本品问者心王、能数之智皆属文殊系——数门即智门。
4. **跨经转引**（据疏钞转引·非本库直证）：澄观疏引《俱舍》「以洛叉為億則俱胝當兆」之数系异说；《大智度論》「菩薩以般若波羅蜜為母、般舟三昧為父」（念佛众行先——澄观引证本品前置之由）；《瓔珞本業經》「初地一念無相法身成就百萬阿僧祇功德」（§5.2 演义钞已引）；《勝鬘經》「無明住地佛位方終」（李论判本品与〈隨好品〉为佛位内无明·§5.2 已引）。
5. **数义四维**（承 §四′ 十节）：**数即德**（寄數顯德分齊——澄观宗趣）／**数即位**（位位增胜·倍倍變＝行布之尺）／**数即心**（數不離心·心王问／自在主学算于文殊）／**数即教**（黄帝 23·小乘 60·华严 124——数系即判教之尺）。〔本文判断〕四维合读：华严之数是「德·位·心·教」四合一的表法系统，阿僧祇品是其总纲，自在主童子是其行用，〈光明覺品〉疏是其小学注脚。

'''
if GUARD_30:
    m5 = re.search(r'\n## 五、注疏选要', md30)
    assert m5
    md30 = md30[:m5.start()+1] + tongkao + '\n' + md30[m5.start()+1:]
    io.open(fp30, 'w', encoding='utf-8', newline='').write(md30)
print('1 P30 数门通考+图〇-3 done')

# ══ 2) P21 十行品：图〇-2 十度增广图 ══
fp21 = 'docs/经学文献/华严经细读/第四会_夜摩天宫_差别因果周/华严经细读_第二十一部_十行品.md'
md21 = io.open(fp21, encoding='utf-8').read()
GUARD_21 = '图 〇-2　十行与十波罗蜜对照' not in md21
svg21 = '''<figure>
<svg viewBox="0 0 1000 380" %s xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#7a5a28">图 〇-2　十行与十波罗蜜对照·六度增广为十度图</text>
<text x="80" y="52" font-size="11" font-weight="bold" fill="#7a5a28">行位</text>
<text x="330" y="52" font-size="11" font-weight="bold" fill="#7a5a28">所对波罗蜜</text>
<text x="620" y="52" font-size="11" font-weight="bold" fill="#7a5a28">增广脉络</text>
'''
rows = [
 ('1 歡喜行', '布施', '六度之一'),
 ('2 饒益行', '持戒', '六度之二'),
 ('3 無違逆行', '忍辱', '六度之三'),
 ('4 無屈撓行', '精進', '六度之四'),
 ('5 無癡亂行', '禪定', '六度之五'),
 ('6 善現行', '般若', '六度之六'),
 ('7 無著行', '方便', '六度＋方便（七）'),
 ('8 願行', '願', '＋願（八）'),
 ('9 善法行', '力', '＋力（九）'),
 ('10 真實行', '智', '＋智（十）——六度增广成十度'),
]
y = 76
for i, (a, b, c) in enumerate(rows):
    fill = '#f6efe1' if i < 6 else '#e8f0e8'
    md21_svg_line = '<rect x="60" y="%d" width="220" height="24" rx="5" fill="%s" stroke="#b8863c"/><text x="80" y="%d" font-size="11" fill="#5a5147">%s</text><rect x="310" y="%d" width="220" height="24" rx="5" fill="#f6efe1" stroke="#b8863c"/><text x="330" y="%d" font-size="11" fill="#5a5147">%s</text><text x="620" y="%d" font-size="10.5" fill="#8a7a5e">%s</text>' % (y, fill, y+16, a, y, y+16, b, y+16, c)
    svg21 += md21_svg_line + '\n'
    y += 28
svg21 += '<text x="500" y="368" text-anchor="middle" font-size="11" fill="#5a5147">前六行＝六度本位；后四行增广方便·願·力·智——十行即十波罗蜜之行位化（智俨：歡喜者施…十真實者得智順理）</text>\n</svg>\n<figcaption style="font-size:.78em;color:var(--text2);line-height:1.85;max-width:760px;margin:6px auto 0"><b>图 〇-2　十行与十波罗蜜对照·六度增广为十度图。</b>配 §5.9 释名与 §5.2 智俨释——十行非另有法体，即十波罗蜜之行位化；前六度承本位，后四度增广涉有化物之用。</figcaption>\n</figure>'
blk21 = '### 〇之二.2 图 〇-2　十度增广图（十行与十波罗蜜对照）\n\n' + svg21
m2 = re.search(r'\n### 〇之二\.2 ', md21) if GUARD_21 else None
assert (m2 or not GUARD_21)
if GUARD_21:
    md21 = md21[:m2.start()+1] + blk21 + '\n' + md21[m2.start()+1:]
    io.open(fp21, 'w', encoding='utf-8', newline='').write(md21)
print('2 P21 图〇-2 done')

# ══ 3) P22 十无尽藏品：图〇-2 十藏体用图 ══
fp22 = 'docs/经学文献/华严经细读/第四会_夜摩天宫_差别因果周/华严经细读_第二十二部_十无尽藏品.md'
md22 = io.open(fp22, encoding='utf-8').read()
GUARD_22 = '图 〇-2　十藏体用图' not in md22
svg22 = '''<figure>
<svg viewBox="0 0 1000 340" %s xmlns="http://www.w3.org/2000/svg" font-family="serif">
<text x="500" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#7a5a28">图 〇-2　十藏体用图——体五·用五·融通随相</text>
<rect x="60" y="46" width="400" height="150" rx="10" fill="#f6efe1" stroke="#b8863c"/>
<text x="260" y="72" text-anchor="middle" font-size="12" font-weight="bold" fill="#7a5a28">以體立名（五藏）</text>
<text x="260" y="100" text-anchor="middle" font-size="11.5" fill="#5a5147">念藏·慧藏·信藏·慚藏·愧藏</text>
<text x="260" y="128" text-anchor="middle" font-size="10.5" fill="#8a7a5e">心淨為信·制止為戒·崇敬為慚</text>
<text x="260" y="150" text-anchor="middle" font-size="10.5" fill="#8a7a5e">輕拒為愧·參教廣聞為聞·決擇為慧…</text>
<text x="260" y="176" text-anchor="middle" font-size="10.5" fill="#8a7a5e">——內明之五，以「性」為本</text>
<rect x="540" y="46" width="400" height="150" rx="10" fill="#eef3ef" stroke="#4a8a8f"/>
<text x="740" y="72" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e5a5e">以用立名（五藏）</text>
<text x="740" y="100" text-anchor="middle" font-size="11.5" fill="#3a5147">戒藏·聞藏·施藏·持藏·辯藏</text>
<text x="740" y="128" text-anchor="middle" font-size="10.5" fill="#5e7a5e">克己為施·任持所記為持</text>
<text x="740" y="150" text-anchor="middle" font-size="10.5" fill="#5e7a5e">巧宣所持為辯——外化之五，以「行」為用</text>
<text x="740" y="176" text-anchor="middle" font-size="10.5" fill="#5e7a5e">（隨相：前九自利·後一辯藏利他）</text>
<rect x="300" y="220" width="400" height="90" rx="10" fill="#f1eef6" stroke="#8a6a9e"/>
<text x="500" y="248" text-anchor="middle" font-size="12" font-weight="bold" fill="#5a3a7a">融通：十種藏皆順法界而修</text>
<text x="500" y="274" text-anchor="middle" font-size="10.5" fill="#6a5a7e">法界體性本自清淨離過——體用五五相即·一藏攝十藏</text>
<text x="500" y="296" text-anchor="middle" font-size="10.5" fill="#6a5a7e">（§5.9 新加坡釋名·§5.2 智俨同判）</text>
</svg>
<figcaption style="font-size:.78em;color:var(--text2);line-height:1.85;max-width:760px;margin:6px auto 0"><b>图 〇-2　十藏体用图。</b>十藏分「体五（信惭愧念慧）·用五（戒闻施持辩）」——配 §5.2 智俨释与 §5.9 新加坡释名；融通门：十藏皆顺法界，随相门前九自利、后一利他。</figcaption>
</figure>''' % W
blk22 = '### 〇之二.2 图 〇-2　十藏体用图（体五用五·融通随相）\n\n' + svg22
m2 = re.search(r'\n### 〇之二\.2 ', md22) if GUARD_22 else None
assert (m2 or not GUARD_22)
if GUARD_22:
    md22 = md22[:m2.start()+1] + blk22 + '\n' + md22[m2.start()+1:]
    io.open(fp22, 'w', encoding='utf-8', newline='').write(md22)
print('3 P22 图〇-2 done')
