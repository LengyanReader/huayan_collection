#!/usr/bin/env python3
# scratch: verify 「」 quotes on 六十本对读/诸家强调 lines against sources
# sources now include 祖师大德 CBETA extracts (疏/钞/探玄记/搜玄记/新论/合论) + 海云五卷讲记
import re, sys, io, os, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# CBETA PDF 注入的康熙部首/中日韩 radicals 补充块的异形字 → 正字（NFKC 未覆盖者，fail-safe 兜底）
RAD = {
    '\u2ef6': '日', '\u2ef7': '月', '\u2ed1': '長', '\u2ec5': '門', '\u2eda': '頁',
    '\u2edb': '風', '\u2ed8': '飛', '\u2ec3': '食', '\u2ec5': '門', '\u2e80': '丨',
    '\u2e97': '冓', '\u2f71': '魚', '\u2f73': '鳥', '\u2f77': '鹵', '\u2f7a': '鹿',
}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(ch, ch) for ch in s)


def cjk(s):
    s = norm(s)
    return ''.join(ch for ch in s if '\u3400' <= ch <= '\u9fff')


base = r'c:\DA_Practice\huayan_collection'
doc = open(base + r'\docs\经学文献\华严经细读_第一部_世主妙严品.md', encoding='utf-8').read()
t279 = cjk(re.sub(r'<[^>]+>', '', open(base + r'\data\references\cbeta\T10n0279.xml', encoding='utf-8').read()))
jian = cjk(open(base + r'\docs\huayanhai\义学专题\经论原典\八十华严-简-大华严寺袖珍版_1.txt', encoding='utf-8').read())
fan = cjk(open(base + r'\docs\huayanhai\义学专题\经论原典\八十华严-繁-大华严寺袖珍版_1.txt', encoding='utf-8').read())
s60 = cjk(open(base + r'\docs\huayanhai\义学专题\经论原典\六十华严_1.txt', encoding='utf-8').read())

HAI_DIR = base + r'\docs\huayanhai\华严云海\浩瀚华严海\八十华严之01品世主妙严品'
hai = cjk(''.join(
    open(os.path.join(HAI_DIR, f), encoding='utf-8').read()
    for f in sorted(os.listdir(HAI_DIR)) if f.endswith('.txt')
))

CB = base + r'\data\references\cbeta_txt'
SRC = {'T279': t279, '简本': jian, '繁本': fan, '六十': s60, '海云': hai}
for fn in os.listdir(CB):
    if fn.endswith('.txt'):
        SRC[fn.split('_')[0]] = cjk(open(os.path.join(CB, fn), encoding='utf-8').read())

lines = doc.split('\n')
checked = 0
misses = []
for ln in lines:
    if not (ln.startswith('**六十本对读**') or ln.startswith('**诸家强调')):
        continue
    tag = ln[:14]
    for frag in re.findall(r'「([^」]+)」', ln):
        # split on joiners I used editorially
        for part in re.split(r'……|…|／|、|（', frag):
            p = cjk(part)
            if len(p) < 4:
                continue
            checked += 1
            if not any(p in v for v in SRC.values()):
                misses.append((tag, part[:40]))
with open(base + r'\scripts\_roll_misses.txt', 'w', encoding='utf-8') as f:
    f.write('checked=%d misses=%d  SRC=%s\n' % (checked, len(misses), ','.join(SRC)))
    for t, m in misses:
        f.write('MISS %s :: %s\n' % (t, m))
print(open(base + r'\scripts\_roll_misses.txt', encoding='utf-8').read().splitlines()[0])
