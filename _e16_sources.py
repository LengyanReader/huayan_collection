# -*- coding: utf-8 -*-
"""_e16_sources.py — L.196 P16《梵行品》五家祖典窗口收割"""
import io, unicodedata

def norm(ch):
    d = unicodedata.normalize('NFKD', ch)
    return d[0] if d else ch

OUT = io.open('_e16_sources.txt', 'w', encoding='utf-8')
def emit(*a):
    OUT.write(' '.join(str(x) for x in a) + '\n')

# 1. 澄观 T1735
shu = io.open('data/references/cbeta_txt/T1735_澄观_华严经疏.txt', encoding='utf-8').read()
nsh = ''.join(norm(c) for c in shu)
a = nsh.find('梵行品第十六')
b = nsh.find('初發心功德品第十七', a + 5)
win = nsh[a:b]
emit('== 澄观 T1735 @%d-%d · nsh len=%d ==' % (a, b, len(win)))
emit('  四门·来意六义·释名·宗趣·释文')
emit('  head: %s' % win[:120])
emit('  tail: %s' % win[-80:])
emit()

# 2. 法藏 T1733 (梵行品第十二·卷十一)
t133 = io.open('data/references/cbeta_txt/T1733_法藏_探玄记.txt', encoding='utf-8').read()
n133 = ''.join(norm(c) for c in t133)
p133 = n133.find('梵行品第十二')
# find next品 boundary
p133_end = n133.find('初發心菩薩功德品第十三', p133 + 6)
if p133_end < 0:
    p133_end = p133 + 3000
seg133 = n133[p133:p133_end]
emit('== 法藏 T1733 @%d-%d · len=%d ==' % (p133, p133_end, len(seg133)))
emit('  head: %s' % seg133[:120])
emit()

# 3. 智俨 T1732 (梵行品第十二·搜玄记)
t132 = io.open('data/references/cbeta_txt/T1732_智俨_搜玄记.txt', encoding='utf-8').read()
n132 = ''.join(norm(c) for c in t132)
p132 = n132.find('梵行品第十二')
p132_end = n132.find('發心功德品第十三', p132 + 6)
if p132_end < 0:
    p132_end = p132 + 2000
seg132 = n132[p132:p132_end]
emit('== 智俨 T1732 @%d-%d · len=%d ==' % (p132, p132_end, len(seg132)))
emit('  head: %s' % seg132[:120])
emit()

# 4. 慧苑 X0221 (梵行品第十六·刊定记)
tx21 = io.open('data/references/cbeta_txt/X0221_慧苑_续华严略疏刊定记.txt', encoding='utf-8').read()
nx21 = ''.join(norm(c) for c in tx21)
# skip first hit (catalog)
p21_cat = nx21.find('梵行品第十六')
p21 = nx21.find('梵行品第十六', p21_cat + 5)
p21_end = nx21.find('初發心功德品第十七', p21 + 6)
if p21_end < 0:
    p21_end = p21 + 3000
seg21 = nx21[p21:p21_end]
emit('== 慧苑 X0221 @%d-%d · len=%d ==' % (p21, p21_end, len(seg21)))
emit('  head: %s' % seg21[:120])
emit()

# 5. 李通玄 T1739 (梵行品第十六·新华严经论)
t739 = io.open('data/references/cbeta_txt/T1739_李通玄_新华严经论.txt', encoding='utf-8').read()
n739 = ''.join(norm(c) for c in t739)
p739 = n739.find('梵行品第十六')
p739_end = n739.find('初發心功德品第十七', p739 + 6)
if p739_end < 0:
    p739_end = p739 + 5000
seg739 = n739[p739:p739_end]
emit('== 李通玄 T1739 @%d-%d · len=%d ==' % (p739, p739_end, len(seg739)))
emit('  head: %s' % seg739[:120])
emit()

# 6. 李通玄 X0223 (梵行品第十六·合论·第三hit=专段)
tx23 = io.open('data/references/cbeta_txt/X0223_李通玄_华严经合论.txt', encoding='utf-8').read()
nx23 = ''.join(norm(c) for c in tx23)
# find the substantive segment (3rd hit)
pos = nx23.find('梵行品第十六')
pos = nx23.find('梵行品第十六', pos + 5)
pos = nx23.find('梵行品第十六', pos + 5)
p723 = pos
p723_end = nx23.find('初發心功德品第十七', p723 + 6)
if p723_end < 0:
    p723_end = p723 + 5000
seg723 = nx23[p723:p723_end]
emit('== 李通玄 X0223 @%d-%d · len=%d ==' % (p723, p723_end, len(seg723)))
emit('  head: %s' % seg723[:120])

OUT.close()
print('E16_SOURCES done · 6 families')
