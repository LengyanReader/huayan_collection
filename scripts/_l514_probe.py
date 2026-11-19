# -*- coding: utf-8 -*-
"""_l514_probe.py — P26 逐地澄观疏窗试取（只打印·校验章题带）"""
import re, unicodedata, sys

sys.stdout.reconfigure(encoding='utf-8')
t = open('data/references/cbeta_txt/T1735_澄观_华严经疏.txt', encoding='utf-8').read()
t = re.sub(r'<<<PAGE \d+>>>', '', t)
t = unicodedata.normalize('NFKC', t)

v34 = t.find('大方廣佛華嚴經疏卷第三十四')
band_end = t.find('十定品', 500000)  # 十地品疏之后下一品·带宽界实测
print('band 卷三十四 @%d · 十定品 @%d' % (v34, band_end))
assert 0 < v34 < band_end
v41 = band_end

NAMES = ['歡喜地', '離垢地', '發光地', '焰慧地', '難勝地', '現前地', '遠行地', '不動地', '善慧地', '法雲地']
HAN = re.compile(r'[\u3400-\u9fff]')
cur = v34
for i, nm in enumerate(NAMES):
    p = t.find(nm, cur)
    assert p > 0 and p < v41, (nm, p)
    raw = t[p:p + 1500]
    raw = raw[:raw.find('CBETA 贊助')] if 'CBETA 贊助' in raw else raw
    acc = 0
    for k, ch in enumerate(raw):
        if HAN.match(ch):
            acc += 1
        if acc >= 380 and ch in '。；':
            raw = raw[:k + 1]
            break
    print('\n════════ 地%d %s @%d（%d 字）════════' % (i + 1, nm, p, len(HAN.findall(raw))))
    print(raw.replace('\n', ' ')[:1600])
    cur = p + 1
