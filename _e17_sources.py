# -*- coding: utf-8 -*-
"""_e17_sources.py — L.197 P17《初发心功德品》五家祖典窗口收割（跳过品目目录命中）"""
import io, unicodedata

def norm(ch):
    d = unicodedata.normalize('NFKD', ch)
    return d[0] if d else ch

OUT = io.open('_e17_sources.txt', 'w', encoding='utf-8')
def emit(*a):
    OUT.write(' '.join(str(x) for x in a) + '\n')

# 1. 澄观 T1735（疏窗主源·已在 _e17_dump）
shu = io.open('data/references/cbeta_txt/T1735_澄观_华严经疏.txt', encoding='utf-8').read()
nsh = ''.join(norm(c) for c in shu)
a = nsh.find('初發心功德品第十七')
b = nsh.find('明法品第十八', a + 5)
win = nsh[a:b]
emit('== 澄观 T1735 @%d-%d · nsh len=%d ==' % (a, b, len(win)))
emit('  head: %s' % win[:140])
emit('  tail: %s' % win[-90:])
emit()

# 2. 法藏 T1733 探玄记（六十品题 發心菩薩功德品第十三·跳过卷首目录@217）
t133 = ''.join(norm(c) for c in io.open('data/references/cbeta_txt/T1733_法藏_探玄记.txt', encoding='utf-8').read())
p133_cat = t133.find('發心菩薩功德品')
p133 = t133.find('發心菩薩功德品', p133_cat + 6)   # 第二命中=专段
p133_end = t133.find('明法品第十四', p133 + 6)
if p133_end < 0:
    p133_end = p133 + 4000
seg133 = t133[p133:p133_end]
emit('== 法藏 T1733 @%d-%d · len=%d ==' % (p133, p133_end, len(seg133)))
emit('  head: %s' % seg133[:140])
emit('  tail: %s' % seg133[-60:])
emit()

# 3. 智俨 T1732 搜玄记（现存仅及前段·本品无窗口）
t132 = ''.join(norm(c) for c in io.open('data/references/cbeta_txt/T1732_智俨_搜玄记.txt', encoding='utf-8').read())
p132 = t132.find('發心功德品')
emit('== 智俨 T1732 搜玄记 · 發心功德品 命中=%d（现存卷不覆此品·缺口）==' % p132)
emit()

# 4. 慧苑 X0221 刊定记（八十品题·跳过卷首目录@321）
tx21 = ''.join(norm(c) for c in io.open('data/references/cbeta_txt/X0221_慧苑_续华严略疏刊定记.txt', encoding='utf-8').read())
p21_cat = tx21.find('初發心功德品第十七')
p21 = tx21.find('初發心功德品第十七', p21_cat + 5)   # 第二命中=专段
p21_end = tx21.find('明法品第十八', p21 + 6)
if p21_end < 0:
    p21_end = p21 + 4000
seg21 = tx21[p21:p21_end]
emit('== 慧苑 X0221 @%d-%d · len=%d ==' % (p21, p21_end, len(seg21)))
emit('  head: %s' % seg21[:140])
emit('  tail: %s' % seg21[-60:])
emit()

# 5. 李通玄 T1739 新华严经论
t739 = ''.join(norm(c) for c in io.open('data/references/cbeta_txt/T1739_李通玄_新华严经论.txt', encoding='utf-8').read())
p739 = t739.find('初發心功德品第十七')
p739_end = t739.find('明法品第十八', p739 + 6)
if p739_end < 0:
    p739_end = p739 + 5000
seg739 = t739[p739:p739_end]
emit('== 李通玄 T1739 @%d-%d · len=%d ==' % (p739, p739_end, len(seg739)))
emit('  head: %s' % seg739[:140])
emit('  tail: %s' % seg739[-60:])
emit()

# 6. 李通玄 X0223 合论（跳过卷首目录·取专段命中@324670）
tx23 = ''.join(norm(c) for c in io.open('data/references/cbeta_txt/X0223_李通玄_华严经合论.txt', encoding='utf-8').read())
# 目录命中在 <1000，专段在 >300000
p723 = tx23.find('初發心功德品第十七', 300000)
p723_end = tx23.find('明法品第十八', p723 + 6)
if p723_end < 0:
    p723_end = p723 + 5000
seg723 = tx23[p723:p723_end]
emit('== 李通玄 X0223 @%d-%d · len=%d ==' % (p723, p723_end, len(seg723)))
emit('  head: %s' % seg723[:140])
emit('  tail: %s' % seg723[-60:])

OUT.close()
print('E17_SOURCES done · 6 families probed')
