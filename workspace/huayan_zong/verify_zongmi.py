# -*- coding: utf-8 -*-
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
xml = open(os.path.join('xml', 'T48n2015.xml'), encoding='utf-8').read()
chars, it = [], False
for ch in xml:
    if ch == '<': it = True
    elif ch == '>': it = False
    elif not it: chars.append(ch)
t = ''.join(chars)
PUNCT = set('，。、；：？！「」『』（）《》〈〉……—－· \u3000\n\r\t')
np_ = lambda s: ''.join(c for c in s if c not in PUNCT)
nt = np_(t)
for needle in ['經是佛語，禪是佛意', '禪是佛意', '教禪一致', '經律', '三宗']:
    i = nt.find(np_(needle))
    if i >= 0:
        print('[ok] %s' % needle)
        print('     …%s…' % nt[max(0,i-20):i+len(np_(needle))+40])
    else:
        print('[MISS] %s' % needle)
