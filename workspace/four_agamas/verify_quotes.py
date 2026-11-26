#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""《四阿含与南传佛教》回归核验：结构计数、直接引文、引注闭合。

用法：python workspace/four_agamas/verify_quotes.py
退出码 0 = 全绿；1 = 有 FAIL。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DOC = os.path.join(ROOT, 'docs', '宗派研究', '四阿含与南传佛教.md')
CBETA = os.path.join(ROOT, 'data', 'references', 'cbeta')

# 结构计数：文件 -> (jing 数, pin 数)
EXPECTED = {
    'T01n0001.xml': (30, 12),
    'T01n0026.xml': (222, 21),
    'T02n0099.xml': (1355, 0),
    'T02n0125.xml': (472, 52),
}

# 正文直接引文（保留 CBETA 繁体原字形）-> 所属文件
QUOTES = [
    ('此《長阿含》四分四誦，合三十經以為一部。', 'T01n0001.xml'),
    ('凡有五誦', 'T01n0026.xml'),
    ('都十八品', 'T01n0026.xml'),
    ('有二百二十二經', 'T01n0026.xml'),
    ('分為六十卷', 'T01n0026.xml'),
    ('合上下部，四百七十二經。', 'T02n0125.xml'),
    ('父母為東方，師長為南方，妻婦為西方，親黨為北方，僮僕為下方，沙門、婆羅門、諸高行者為上方。', 'T01n0001.xml'),
    ('未可拔箭，我應先知彼人如是姓、如是名、如是生', 'T01n0026.xml'),
    ('此非義相應，非法相應，非梵行本，不趣智、不趣覺、不趣涅槃', 'T01n0026.xml'),
    ('苦、苦習、苦滅、苦滅道跡，我一向說', 'T01n0026.xml'),
    ('此有故彼有，此起故彼起', 'T02n0099.xml'),
    ('當觀色無常。如是觀者，則為正觀。正觀者，則生厭離；厭離者，喜貪盡；喜貪盡者，說心解脫。', 'T02n0099.xml'),
    ('於色當正思惟，觀色無常如實知', 'T02n0099.xml'),
    ('菩薩發意趣大乘', 'T02n0125.xml'),
    ('人尊說六度無極', 'T02n0125.xml'),
    ('具足六波羅蜜', 'T02n0125.xml'),
    ('住不放逸之地', 'T02n0125.xml'),
    ('未生善法，求方便令生', 'T02n0125.xml'),
    ('已生善法，求方便令增多', 'T02n0125.xml'),
    ('已生弊惡法，求方便令滅', 'T02n0125.xml'),
    ('已生弊惡法，求方便令不生，心不遠離，恒欲令滅', 'T02n0125.xml'),
]


def plain(fn):
    raw = open(os.path.join(CBETA, fn), encoding='utf-8').read()
    return re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', raw))


def main():
    fails = []
    text = open(DOC, encoding='utf-8').read()
    print(f'DOC {os.path.relpath(DOC, ROOT)} | {len(text):,} chars')

    print('\n[1] 结构计数')
    for fn, (jing, pin) in EXPECTED.items():
        raw = open(os.path.join(CBETA, fn), encoding='utf-8').read()
        got = (len(re.findall(r'<cb:div[^>]*type="jing"', raw)),
               len(re.findall(r'<cb:div[^>]*type="pin"', raw)))
        ok = got == (jing, pin)
        print(f'  {"OK  " if ok else "FAIL"} {fn}: jing={got[0]} pin={got[1]} (expect {jing}/{pin})')
        if not ok:
            fails.append(f'{fn} 结构计数 {got} != {(jing, pin)}')

    print('\n[2] 直接引文逐字回源')
    corpus = {}
    for _, fn in QUOTES:
        corpus.setdefault(fn, plain(fn))
    for q, fn in QUOTES:
        ok = re.sub(r'\s+', '', q) in corpus[fn]
        print(f'  {"OK  " if ok else "FAIL"} [{fn}] {q[:34]}{"…" if len(q) > 34 else ""}')
        if not ok:
            fails.append(f'引文未命中: {q[:40]}')

    print('\n[3] 引注闭合')
    ids = set(re.findall(r'<a id="([^"]+)"', text))
    refs = re.findall(r'href="#([^"]+)"', text)
    missing = sorted({r for r in refs if r not in ids})
    print(f'  ids={len(ids)} links={len(refs)} missing={len(missing)}')
    if missing:
        fails.append(f'缺失锚点: {missing}')

    print('\n[4] 篇内序号')
    heads = re.findall(r'^## (.+)$', text, re.M)
    print('  ' + ' | '.join(h[:12] for h in heads))
    if len(heads) != 12:
        fails.append(f'章标题数 {len(heads)} != 12')

    print('\n' + ('ALL CHECKS PASSED' if not fails else 'FAILED:\n  ' + '\n  '.join(fails)))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
