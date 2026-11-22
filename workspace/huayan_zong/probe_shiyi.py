# -*- coding: utf-8 -*-
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
CAN = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, 'data', 'references', 'cbeta'))
xml = open(os.path.join(CAN, 'T35n1733.xml'), encoding='utf-8').read()
chars, it = [], False
for ch in xml:
    if ch == '<': it = True
    elif ch == '>': it = False
    elif not it: chars.append(ch)
t = ''.join(chars)
PUNCT = set('，。、；：？！「」『』（）《》〈〉……—－· \u3000\n\r\t')
np_ = lambda s: ''.join(c for c in s if c not in PUNCT)
nt = np_(t)
i = nt.find(np_('就初門中有十義具足'))
print('十义段（剥标点后 %d 起，展 300 字）：' % i)
print(nt[i:i+300])
