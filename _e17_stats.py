# -*- coding: utf-8 -*-
"""_e17_stats.py — L.197 P17《初发心功德品》实测统计（数据层只出实测可得者）"""
import io, re, unicodedata
import xml.etree.ElementTree as ET

OUT = io.open('_e17_stats.txt', 'w', encoding='utf-8')
def emit(*a):
    OUT.write(' '.join(str(x) for x in a) + '\n')

SKIP = {'note', 'rdg', 'mulu', 'pb', 'anchor', 'app'}
def flat(el):
    acc = []
    def walk(e):
        tag = e.tag.split('}')[-1]
        if tag in SKIP: return
        if tag == 'lb': acc.append(' ')
        if e.text: acc.append(e.text)
        for c in e:
            walk(c)
            if c.tail: acc.append(c.tail)
    walk(el)
    return ''.join(acc)
ONLY = lambda s: ''.join(ch for ch in s if '\u4e00' <= ch <= '\u9fff')

acc = []
def walk(el):
    tag = el.tag.split('}')[-1]
    if tag in SKIP: return
    if tag == 'lb': acc.append(' ')
    if el.text: acc.append(el.text)
    for c in el:
        walk(c)
        if c.tail: acc.append(c.tail)
walk(ET.parse('data/references/cbeta/T10n0279.xml').getroot())
fullC = ONLY(''.join(acc))
iC = fullC.find('初發心功德品第十七')
kC = fullC.find('明法品第十八', iC + 6)
body80 = fullC[iC:kC]

# units by tag
root = ET.parse('data/references/cbeta/T10n0279.xml').getroot()
from collections import Counter
tagn = Counter()
proseC = verseC = 0
for el in root.iter():
    tag = el.tag.split('}')[-1]
    if tag in ('p', 'lg', 'head', 'byline'):
        t = flat(el); tc = ONLY(t)
        if len(tc) < 2: continue
        pos = fullC.find(tc, iC)
        if pos < 0 or pos >= kC: continue
        tagn[tag] += 1
        if tag == 'lg': verseC += len(tc)
        elif tag == 'p': proseC += len(tc)
emit('== 八十品界 CJK 总 %d ==' % len(body80))
emit('== 单元 tag 计 %s ==' % dict(tagn))
emit('== 长行 p CJK=%d · 重颂 lg CJK=%d ==' % (proseC, verseC))

# 校量数喻频次
emit('\n== 数量级 / 校量喻词频（body80 CJK-only 计）==')
for kw in ['阿僧祇', '那由他', '优波尼沙陀', '優波尼沙陀', '百分不及一', '千分不及一',
           '歌羅分', '算分', '諭分', '不可說不可說', '無量', '無邊', '微塵數',
           '發菩提心', '發阿耨多羅三藐三菩提心', '初發心', '佛子', '天帝', '法慧']:
    emit('  %-24s %d' % (kw, body80.count(kw)))

# 十难 / 震动三遍 / 十方
emit('\n== 结构标记 ==')
for kw in ['難說', '難知', '難分別', '難信解', '難證', '難行', '難通達', '難思惟', '難度量', '難趣入']:
    emit('  十難 %-8s %d' % (kw, body80.count(kw)))
for kw in ['遍動', '等遍動', '六種震動', '十方', '同名', '清淨心如來']:
    emit('  結界 %-10s %d' % (kw, body80.count(kw)))

# 偈颂句数（lg 内 以空格分隔·七言为主）
lg_text = ''
for el in root.iter():
    if el.tag.split('}')[-1] == 'lg':
        t = flat(el); tc = ONLY(t)
        if len(tc) > 3000 and tc in body80:
            lg_text = t
lines = [l.strip() for l in re.split(r'[，。；：？！、\s]+', lg_text) if ONLY(l)]
emit('\n== 重颂 lg：CJK=%d · 净句段计=%d（七言为主·均长=%.1f）==' % (
    len(ONLY(lg_text)), len(lines), len(ONLY(lg_text)) / max(len(lines), 1)))

OUT.close()
print('E17_STATS done · body80=%d prose=%d verse=%d' % (len(body80), proseC, verseC))
