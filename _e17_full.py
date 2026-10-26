# -*- coding: utf-8 -*-
"""_e17_full.py — L.197 第十七部《初发心功德品》充实批：八十全文结构化 dump＋澄观疏窗口
   仿 _e16_full.py 范式（SKIP-tag 平文器 · CJK-only 前向游标 · 限品界防 byline 串味）
   八十品界：初發心功德品第十七 → 明法品第十八（卷第十七–十八·超长品·功德校量极大数喻）
   六十品界：初发心菩萨功德品第十三 存于六十卷九，本仓 cbeta_txt 仅入库卷一–八，故六十原文〔未入库·待核〕
   疏窗口：T1735 NFKD「初發心功德品第十七」→「明法品第十八」
"""
import io, re, unicodedata
import xml.etree.ElementTree as ET

OUT = io.open('_e17_dump.txt', 'w', encoding='utf-8')
def emit(*a):
    OUT.write(' '.join(str(x) for x in a) + '\n')

SKIP = {'note', 'rdg', 'mulu', 'pb', 'anchor', 'app'}

def clean(s):
    return re.sub(r'\s', ' ', s).strip()

def flat(el):
    acc = []
    def walk(e):
        tag = e.tag.split('}')[-1]
        if tag in SKIP:
            return
        if tag == 'lb':
            acc.append(' ')
        if e.text:
            acc.append(e.text)
        for c in e:
            walk(c)
            if c.tail:
                acc.append(c.tail)
    walk(el)
    return ''.join(acc)

def cjk(s):
    return ''.join(ch for ch in s if '\u4e00' <= ch <= '\u9fff')

ONLY = lambda s: ''.join(ch for ch in s if '\u4e00' <= ch <= '\u9fff')

acc = []
def walk(el):
    tag = el.tag.split('}')[-1]
    if tag in SKIP:
        return
    if tag == 'lb':
        acc.append(' ')
    if el.text:
        acc.append(el.text)
    for c in el:
        walk(c)
        if c.tail:
            acc.append(c.tail)
walk(ET.parse('data/references/cbeta/T10n0279.xml').getroot())
full = ''.join(acc)
fullC = ONLY(full)

# ── 八十品界（初發心功德品第十七 → 明法品第十八）──
iC = fullC.find('初發心功德品第十七')
kC = fullC.find('明法品第十八', iC + 6)
assert iC > 0 and kC > iC, (iC, kC)
emit('== 八十品界(CJK口径) @%d–%d · CJK%d ==' % (iC, kC, kC - iC))

units = []
seen = set()
root = ET.parse('data/references/cbeta/T10n0279.xml').getroot()
for el in root.iter():
    tag = el.tag.split('}')[-1]
    if tag in ('p', 'lg', 'head', 'byline'):
        t = flat(el)
        tc = ONLY(t)
        if len(tc) < 2:
            continue
        pos = fullC.find(tc, iC)
        if pos < 0 or pos >= kC or pos in seen:
            continue
        seen.add(pos)
        units.append((tag, pos, clean(t), tc))
units.sort(key=lambda u: u[1])
emit('== 八十侧单元 %d 个 ==' % len(units))
for n, (tag, pos, t, tc) in enumerate(units):
    emit('[80-%03d|%s|@%d|CJK%d] %s' % (n, tag, pos, len(tc), t))

body80 = fullC[iC:kC]
emit('== body80 len=%d ==' % len(body80))

# ── 六十侧：初发心菩萨功德品第十三在卷九，未入库 ──
emit('== 六十侧：初发心菩萨功德品第十三（卷九）本仓仅入库卷一–八，原文〔未入库·待核〕==')

# ── 澄观疏窗口（T1735·NFKD 归一·60 字标尺）──
shu = io.open('data/references/cbeta_txt/T1735_澄观_华严经疏.txt', encoding='utf-8').read()
def norm(ch):
    d = unicodedata.normalize('NFKD', ch)
    return d[0] if d else ch
nsh = ''.join(norm(c) for c in shu)
assert len(nsh) == len(shu)
a = nsh.find('初發心功德品第十七')
b = nsh.find('明法品第十八', a + 5)
assert 0 < a < b, (a, b)
emit('== 疏窗口(nsh 口径) %d–%d · 疏文长 %d ==' % (a, b, b - a))
win = nsh[a:b]
for n in range(0, len(win), 60):
    emit('[SH-%04d] %s' % (n, win[n:n+60]))

OUT.close()
print('E17_FULL done · units=%d · body80=%d · shun=%d' % (len(units), len(body80), len(win)))
