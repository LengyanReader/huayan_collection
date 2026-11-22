# -*- coding: utf-8 -*-
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
CAN = os.path.normpath(os.path.join(HERE := os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, 'data', 'references', 'cbeta'))
def load(tid):
    xml = open(os.path.join(CAN, tid + '.xml'), encoding='utf-8').read()
    chars, it = [], False
    for ch in xml:
        if ch == '<': it = True
        elif ch == '>': it = False
        elif not it: chars.append(ch)
    return ''.join(chars)
T35 = load('T35n1733'); T35S = load('T35n1735')
def ctx(text, needle, before=30, after=90, nth=0):
    i = -1
    for _ in range(nth + 1):
        i = text.find(needle, i + 1)
        if i < 0: return '(未命中)'
    return text[max(0,i-before):i+len(needle)+after].replace('\n','⏎')
print('== T35n1733 探玄记：隱密顯了俱成門 ==');  print(ctx(T35,'隱密顯了俱成門'))
print('\n== T35n1733 探玄记：祕密隱顯俱成門 =='); print(ctx(T35,'祕密隱顯俱成門'))
print('\n== T35n1733 探玄记：十玄列表起（一同時具足相應門）=='); print(ctx(T35,'一同時具足相應門',before=60,after=260))
print('\n== T35n1735 澄观疏：一同時具足相應門 =='); print(ctx(T35S,'一同時具足相應門',before=60,after=260))
print('\n== T35n1735 澄观疏：祕密隱顯俱成門 =='); print(ctx(T35S,'祕密隱顯俱成門'))
print('\n== T35n1735 澄观疏：因陀羅網境界門 =='); print(ctx(T35S,'因陀羅網境界門'))
