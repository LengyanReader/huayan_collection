# -*- coding: utf-8 -*-
"""_l520_probe.py — P31/P32 六源窗锚勘样（只打印）"""
import io, re, sys, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
HAN = re.compile(r'[\u3400-\u9fff]')


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


SRC = {'智俨T1732': 'data/references/cbeta_txt/T1732_智俨_搜玄记.txt',
       '演义钞T1736': 'data/references/cbeta_txt/T1736_澄观_随疏演义钞.txt',
       '李论T1739': 'data/references/cbeta_txt/T1739_李通玄_新华严经论.txt',
       '纂要B0002': 'data/references/cbeta_txt/B0002_疏论纂要_epub提取本.txt',
       '探玄T1733': 'data/references/cbeta_txt/T1733_法藏_探玄记.txt'}
texts = {k: norm(p) for k, p in SRC.items()}

JOBS = [
    ('P31 壽量品', '壽量品', ['壽量品', '如來壽量品'], ['T1732@99473'], 30),
    ('P32 菩薩住處品', '菩薩住處品', ['菩薩住處品', '住處品'], [], 26),
]
for label, main, alts, fixed, show in JOBS:
    print('═' * 20, label)
    for k, t in texts.items():
        ps = sorted(set([m.start() for v in alts for m in re.finditer(re.escape(v), t)]))
        print('── %s · %d 锚: %s' % (k, len(ps), ps[:8]))
        use = ps[:2] if not fixed else ps[:1]
        for p in use:
            w = cut(t[p:p + 1200])
            print('  [%s@%d] %d字: %s' % (k.split('T')[-1], p, len(HAN.findall(w)), w.replace('\n', ' ')[:show]))
