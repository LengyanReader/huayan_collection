# -*- coding: utf-8 -*-
"""_e18_stats.py — L.198 P18《明法品》实测统计（数据层只出实测可得者）"""
import io, re, unicodedata
import xml.etree.ElementTree as ET
from collections import Counter

OUT = io.open('_e18_stats.txt', 'w', encoding='utf-8')
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
iC = fullC.find('明法品第十八')
kC = fullC.find('昇夜摩天宮品第十九', iC + 6)
body80 = fullC[iC:kC]

root = ET.parse('data/references/cbeta/T10n0279.xml').getroot()
tagn = Counter(); proseC = verseC = 0
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
emit('== 八十品界 CJK 总 %d · @%d-%d ==' % (len(body80), iC, kC))
emit('== 单元 tag 计 %s ==' % dict(tagn))
emit('== 长行 p CJK=%d · 重颂 lg CJK=%d（两段）==' % (proseC, verseC))

emit('\n== 十法矩阵关键词频（body80 CJK-only 计）==')
for kw in ['不放逸', '清淨', '波羅蜜', '十種', '佛子', '菩薩摩訶薩', '如來', '歡喜',
           '無盡藏', '大願', '莊嚴', '阿僧祇', '一切智', '菩提心', '精進', '法慧',
           '三寶', '說法', '增勝', '陀羅尼', '三昧', '神通']:
    emit('  %-16s %d' % (kw, body80.count(kw)))

emit('\n== 「十」数结构标记（何者為十/何等為十 列数句式）==')
for kw in ['何等為十', '何者為十', '十種法', '十種清淨', '十種願', '是為十', '令諸', '速入諸地']:
    emit('  %-12s %d' % (kw, body80.count(kw)))

# 两段偈颂句数
for lo, hi, nm in [(0, 0, '')]:
    pass
emit('\n== 重颂两段净句段（以空白分）==')
for el in root.iter():
    if el.tag.split('}')[-1] == 'lg':
        t = flat(el); tc = ONLY(t)
        pos = fullC.find(tc, iC)
        if pos < 0 or pos >= kC: continue
        segs = [s for s in re.split(r'\s{2,}', t) if ONLY(s)]
        lines = [l.strip() for l in re.split(r'[，。；：？！、\s]+', t) if ONLY(l)]
        emit('  lg@%d CJK=%d · 双空格分行=%d · 净句段=%d（均长%.1f字）' % (
            pos, len(tc), len(segs), len(lines), len(tc) / max(len(lines), 1)))

OUT.close()
print('E18_STATS done · body80=%d prose=%d verse=%d' % (len(body80), proseC, verseC))
