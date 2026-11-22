# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
MD = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, 'docs', '宗派研究', '华严宗全方位研究.md'))
s = open(MD, encoding='utf-8').read()
a = 'X03n0221 慧苑刊定记、X04n0223 合论；本批新入 T45n1866 教义分齐章）'
b = 'X03n0221 慧苑刊定记、X04n0223 合论；本批新入 T45n1866 教义分齐章、T48n2015 禅源诸诠集都序）'
assert s.count(a) == 1, s.count(a)
s = s.replace(a, b, 1)
open(MD, 'w', encoding='utf-8').write(s)
print('patch2 ok: 说明补 T48n2015')
