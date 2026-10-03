#!/usr/bin/env python3
# scratch 校勘: verify EVERY `> **经文**` block is a verbatim CJK run of T279 (底本)
# - 经文 blocks claim 逐字回源 T279; they are NOT covered by _roll_verify.py
import re, sys, io, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RAD = {
    '\u2ef6': '日', '\u2ef7': '月', '\u2ed1': '長', '\u2ec5': '門', '\u2eda': '頁',
    '\u2edb': '風', '\u2ed8': '飛', '\u2ec3': '食', '\u2e80': '丨',
    '\u2f71': '魚', '\u2f73': '鳥', '\u2f77': '鹵', '\u2f7a': '鹿',
}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(ch, ch) for ch in s)


def cjk(s):
    s = norm(s)
    return ''.join(ch for ch in s if '\u3400' <= ch <= '\u9fff')


base = r'c:\DA_Practice\huayan_collection'
doc = open(base + r'\docs\经学文献\华严经细读_第一部_世主妙严品.md', encoding='utf-8').read().split('\n')
t279 = cjk(re.sub(r'<[^>]+>', '', open(base + r'\data\references\cbeta\T10n0279.xml', encoding='utf-8').read()))
fan = cjk(open(base + r'\docs\huayanhai\义学专题\经论原典\八十华严-繁-大华严寺袖珍版_1.txt', encoding='utf-8').read())

checked = 0
misses = []
for i, ln in enumerate(doc, 1):
    if not ln.startswith('> **经文**'):
        continue
    body = ln.split('> **经文**', 1)[1].lstrip('　 ')
    # drop editorial parentheticals and markdown emphasis
    body = re.sub(r'（[^）]*）', '', body)
    body = body.replace('**', '')
    # split into verbatim-checkable fragments on elision AND sentence/pause punctuation
    # (blocks often join 門名 + 其頌, non-adjacent in T279, via 。; each piece is verbatim)
    for seg in re.split(r'……|…|～|\.\.\.|。|，|、|；|：|！', body):
        p = cjk(seg)
        if len(p) < 7:
            continue
        checked += 1
        where = 'T279' if p in t279 else ('繁本' if p in fan else None)
        if where is None:
            misses.append((i, seg.strip()[:60]))
print('经文块回源: checked=%d  miss=%d  (against T279/繁本)' % (checked, len(misses)))
for i, m in misses:
    print('  L%-5d %s' % (i, m))
