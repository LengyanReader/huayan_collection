import os, unicodedata
base = r'c:\DA_Practice\huayan_collection'
RAD = {
    '\u2ef6': '日', '\u2ef7': '月', '\u2ed1': '長', '\u2ec5': '門', '\u2eda': '頁',
    '\u2edb': '風', '\u2ed8': '飛', '\u2ec3': '食', '\u2e80': '丨',
    '\u2e97': '冓', '\u2f71': '魚', '\u2f73': '鳥', '\u2f77': '鹵', '\u2f7a': '鹿',
}
def _norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(ch, ch) for ch in s)
def cjk(s):
    s = _norm(s)
    return ''.join(ch for ch in s if '\u3400' <= ch <= '\u9fff')

# key fragments from the 15 misses that need source verification
kws = [
    '遍觀一切夜摩',
    '一切夜摩',
    '一切时分天王众',
    '一切時分天王眾',
    '遍觀一切時分',
    '爾時時分天王',
    '爾時夜摩',
    '承佛威力遍觀',
]

out = []
import re
# also include T279, 80版简/繁, 60版
SRC_EXTRA = {
    'T279': cjk(re.sub(r'<[^>]+>', '', open(base + r'\data\references\cbeta\T10n0279.xml', encoding='utf-8').read())),
    'jian': cjk(open(base + r'\docs\huayanhai\义学专题\经论原典\八十华严-简-大华严寺袖珍版_1.txt', encoding='utf-8').read()),
    'fan':  cjk(open(base + r'\docs\huayanhai\义学专题\经论原典\八十华严-繁-大华严寺袖珍版_1.txt', encoding='utf-8').read()),
    's60':  cjk(open(base + r'\docs\huayanhai\义学专题\经论原典\六十华严_1.txt', encoding='utf-8').read()),
}
for tag, n in SRC_EXTRA.items():
    for kw in kws:
        nk = cjk(kw)
        i = n.find(nk)
        if i >= 0:
            out.append(f'{tag:34s} | {kw:22s} | HIT @ {i} | {repr(n[max(0,i-10):i+55])}')

CB = base + r'\data\references\cbeta_txt'
for fn in sorted(os.listdir(CB)):
    if not fn.endswith('.txt'):
        continue
    n = cjk(open(os.path.join(CB, fn), encoding='utf-8').read())
    for kw in kws:
        nk = cjk(kw)
        i = n.find(nk)
        if i >= 0:
            out.append(f'{fn[:34]:34s} | {kw:22s} | HIT @ {i} | {repr(n[max(0,i-10):i+45])}')

HAI = base + r'\docs\huayanhai\华严云海\浩瀚华严海\八十华严之01品世主妙严品'
for fn in sorted(os.listdir(HAI)):
    if not fn.endswith('.txt'):
        continue
    n = cjk(open(os.path.join(HAI, fn), encoding='utf-8').read())
    for kw in kws:
        nk = cjk(kw)
        i = n.find(nk)
        if i >= 0:
            out.append(f'HAI/{fn[:30]:30s} | {kw:22s} | HIT @ {i} | {repr(n[max(0,i-10):i+45])}')

open('scripts/_tmp_search.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok', len(out))
