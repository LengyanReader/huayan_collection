# -*- coding: utf-8 -*-
"""_e18_sources.py — L.198 P18《明法品》五家祖典窗口收割（跳过品目目录命中）"""
import io, unicodedata

def norm(ch):
    d = unicodedata.normalize('NFKD', ch)
    return d[0] if d else ch
NN = lambda p: ''.join(norm(c) for c in io.open(p, encoding='utf-8').read())

OUT = io.open('_e18_sources.txt', 'w', encoding='utf-8')
def emit(*a):
    OUT.write(' '.join(str(x) for x in a) + '\n')

def harvest(tag, path, start_marker, end_markers, skip_first=0, min_pos=0):
    if isinstance(end_markers, str):
        end_markers = [end_markers]
    n = NN(path)
    pos = min_pos
    for _ in range(skip_first + 1):
        pos = n.find(start_marker, pos + 1)
    end = -1
    for em in end_markers:
        q = n.find(em, pos + len(start_marker))
        if q >= 0 and (end < 0 or q < end):
            end = q
    if end < 0:
        end = pos + 4000
    seg = n[pos:end]
    emit('== %s @%d-%d · len=%d ==' % (tag, pos, end, len(seg)))
    emit('  head: %s' % seg[:140])
    emit('  tail: %s' % seg[-70:])
    emit()
    return seg

base = 'data/references/cbeta_txt/'
# 1. 澄观 T1735（疏窗主源）
harvest('澄观 T1735', base + 'T1735_澄观_华严经疏.txt', '明法品第十八', ['升夜摩天宮品第十九', '昇夜摩天宮品第十九'])
# 2. 法藏 T1733（六十品题 明法品第十四·首命中即专段·次品题 昇夜摩天宮自在品第十五）
harvest('法藏 T1733', base + 'T1733_法藏_探玄记.txt', '明法品第十四', '昇夜摩天宮')
# 3. 智俨 T1732（六十品题 明法品第十四·首命中即专段·本品有文非缺口）
harvest('智俨 T1732', base + 'T1732_智俨_搜玄记.txt', '明法品第十四', '夜摩')
# 4. 慧苑 X0221（八十品题·跳过卷首目录@331·取专段@195786·次品题 升夜摩天…）
harvest('慧苑 X0221', base + 'X0221_慧苑_续华严略疏刊定记.txt', '明法品第十八', ['昇夜摩天', '升夜摩天'], skip_first=1)
# 5. 李通玄 T1739
harvest('通玄 T1739', base + 'T1739_李通玄_新华严经论.txt', '明法品第十八', ['昇夜摩天宮品第十九', '升夜摩天宮品第十九'])
# 6. 李通玄 X0223 合论（目录命中 <1000·专段 >300000@339294）
harvest('合论 X0223', base + 'X0223_李通玄_华严经合论.txt', '明法品第十八', '昇夜摩天宮', min_pos=300000)

OUT.close()
print('E18_SOURCES done · 6 families harvested')
