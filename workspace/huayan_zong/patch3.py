# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
MD = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, 'docs', '宗派研究', '华严宗全方位研究.md'))
s = open(MD, encoding='utf-8').read()
a = '主张「经是佛语，禅是佛意」'
b = '主张「經是佛語，禪是佛意」（T48n2015，已核）'
assert s.count(a) == 1
s = s.replace(a, b, 1)
open(MD, 'w', encoding='utf-8').write(s)
print('patch3 ok: 宗密句繁体照底本')
