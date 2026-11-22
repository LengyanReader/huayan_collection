# -*- coding: utf-8 -*-
"""_l521_p14p16.py — L.521 P14+P16 补窗批：
①P14 须弥顶上偈赞品：+5.1′ 演义钞窗（一切慧偈·中论引）＋5.4′ 道霈窗（四门·助化赞扬）
②P16 梵行品：+5.1′ 演义钞窗（六来意·行位相对）＋5.4′ 道霈窗（四门·位位成佛不由他悟）＋净行品姊妹互链＋藏译待勘指针
"""
import glob, io, re, sys, unicodedata

sys.stdout.reconfigure(encoding='utf-8')
HAN = re.compile(r'[\u3400-\u9fff]')


def han(s):
    return len(HAN.findall(s))


def norm(p):
    t = io.open(p, encoding='utf-8').read()
    return unicodedata.normalize('NFKC', re.sub(r'<<<PAGE \d+>>>', '', t))


def cut(raw, limit=340):
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

# ══ ① P14 ══
fp14 = gpat('华严经细读_第十四部_*.md')
md = io.open(fp14, encoding='utf-8').read()
if 'L.521 补窗' not in md:
    w6 = cut(T6[T6.find('須彌頂上偈讚品', 529000):530178 + 1300])
    assert '一切慧菩薩' in w6
    wb = cut(TB[TB.find('須彌頂上偈讚品第十四', 459000):460163 + 1300])
    assert '助化讚揚' in wb
    s51 = ('### 5.1′ 澄观《隨疏演義鈔》窗（`T1736`·L.521 补窗）\n\n'
           '**演义钞窗·一切慧偈逐偈释**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
           '> **按语**〔本文判断〕演义钞于本品逐偈释一切慧菩萨「一切法無生。一切法無滅。若能如是解。諸佛常現前」，并以《中論》〈四諦品〉末「若見因緣法則為能見佛」会通——**偈赞品的般若底色**：赞佛德即观因缘。\n\n' % (han(w6), w6.replace('\n', ' ')))
    s54 = ('### 5.4′ 道霈《華嚴經疏論纂要》窗（`B0002`·L.521 补窗）\n\n'
           '**纂要窗·四门（来意·释名·宗趣＋【论】）**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
           '> **按语**〔本文判断〕纂要判「將演住門。先陳體性。性即佛智。先讚如來」——**赞者先陈住体**（佛智），正说（十住·品15）随之；兼收【论】「法慧等十箇菩薩各以自己當位隨位進修之法還自以偈讚——令信終菩薩倣之悟入」：偈赞即行法的示范式。\n\n' % (han(wb), wb.replace('\n', ' ')))
    m52 = re.search(r'^### 5\.2 法藏《大方[广廣]佛华[严嚴]经探玄[记記]》', md, re.M)
    assert m52
    md = md[:m52.start()] + s51 + '\n' + md[m52.start():]
    m59 = re.search(r'^### 5\.9 新加坡白话浅释选录', md, re.M)
    assert m59
    md = md[:m59.start()] + s54 + '\n' + md[m59.start():]
    ml = re.search(r'^## 九、台账[^\n]*\n', md, re.M)
    assert ml
    md = md[:ml.end()] + '- **L.521（2026-11-22）补窗批**：新增 §5.1′ 演义钞窗（一切慧偈逐偈释·中论「若見因緣法則為能見佛」会通）＋§5.4′ 道霈窗（四门·「將演住門先陳體性性即佛智」·【论】当位偈讚令信終倣之悟入）——会3 品目五家窗自此齐（澄观疏/演义钞/探玄/李论/合论/纂要）。\n' + md[ml.end():]
    io.open(fp14, 'w', encoding='utf-8', newline='').write(md)
    print('① P14 两窗＋台账 ✓')

# ══ ② P16 ══
fp16 = gpat('华严经细读_第十六部_*.md')
md = io.open(fp16, encoding='utf-8').read()
if 'L.521 补窗' not in md:
    w6 = cut(T6[T6.find('梵行品第十六', 494000):495647 + 1400])
    assert '初來意有六者' in w6
    wb = cut(TB[TB.find('梵行品第十六', 505000):506223 + 1400])
    assert '位位成佛' in wb
    s51 = ('### 5.1′ 澄观《隨疏演義鈔》窗（`T1736`·L.521 补窗）\n\n'
           '**演义钞窗·六来意**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
           '> **按语**〔本文判断〕演义钞六来意以四对判本品——行位相对（前虽有行意在位故）·通别相对（十住别修·梵行通修）·道俗相对（本品别显出家所行）·随相实相对（「於身無所取。於修無所著……知一切法即心自性」）——**梵行＝位中之通行**：十住各别行之上的共通观法。\n\n' % (han(w6), w6.replace('\n', ' ')))
    s54 = ('### 5.4′ 道霈《華嚴經疏論纂要》窗（`B0002`·L.521 补窗）\n\n'
           '**纂要窗·四门六来意**（%d 字·程序抽取逐字回源·句界截断）：\n\n> %s\n\n'
           '> **按语**〔本文判断〕纂要同源六来意而加按——「別顯初住成佛。則類前諸位。**位位成佛。不由他悟之相**」：梵行一品即初住成佛之示范——与 §5.3″′ 品级讲记（梵行清净）对读。\n\n' % (han(wb), wb.replace('\n', ' ')))
    m52 = re.search(r'^### 5\.2 法藏《大方[广廣]佛华[严嚴]经探玄[记記]》', md, re.M)
    assert m52
    md = md[:m52.start()] + s51 + '\n' + md[m52.start():]
    m59 = re.search(r'^### 5\.9 新加坡白话浅释选录', md, re.M)
    assert m59
    md = md[:m59.start()] + s54 + '\n' + md[m59.start():]
    # 姊妹品互链（§三 末）
    m4 = re.search(r'^## 四、义理要点', md, re.M)
    assert m4
    lnk = ('\n> **L.521 姊妹品互链**：〈淨行品〉（`P11`·141 净行·日用随事发愿）与本品（梵行·观心十义）同答「云何而行」——**净行是事上行，梵行是理上观**；净行以愿转事、梵行以观净心，两轮相承（P11 §5.3 系列可互参）。\n')
    md = md[:m4.start()] + lnk + md[m4.start():]
    # 藏译待勘指针（§六）
    m6x = re.search(r'^## 六[、　]文本对读', md, re.M)
    if m6x:
        md = md[:m6x.start()] + '\n> **藏译对照待勘（L.521）**：本品藏译对应章（Phal chen le\u02bcu 次第）未勘〔未竟〕——补前不对录音/影像外源臆引。\n' + md[m6x.start():]
    ml = re.search(r'^## 九、台账[^\n]*\n', md, re.M)
    assert ml
    md = md[:ml.end()] + '- **L.521（2026-11-22）补窗批**：新增 §5.1′ 演义钞窗（六来意·四对行位相对·「知一切法即心自性」）＋§5.4′ 道霈窗（「位位成佛不由他悟之相」）＋净行品姊妹互链（P11·事上行/理上观）＋藏译对照待勘指针。\n' + md[ml.end():]
    io.open(fp16, 'w', encoding='utf-8', newline='').write(md)
    print('② P16 两窗＋互链＋藏译指针＋台账 ✓')
print('L.521 done')
