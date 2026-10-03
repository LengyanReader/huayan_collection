# -*- coding: utf-8 -*-
import re
p = r'c:\DA_Practice\huayan_collection\docs\huayanhai\义学专题\经论原典\六十华严_1.txt'
txt = open(p, encoding='utf-8').read()
# 限定〈世间净眼品〉天众区: 卷一开头 ~ 持国乾闼婆(八部始)
a = txt.find('善海摩醯首罗')
b = txt.find('持国乾闼婆王')
seg = txt[a:b]
lines = seg.split('\n')
out = ['天众区 %d..%d\n' % (a, b)]
# 组首: 复有X天[王/子]。 / 尔时X。…遍观/观察Y天众
for i, ln in enumerate(lines):
    s = ln.strip().replace(' ', '')
    if not s:
        continue
    mh = re.match(r'^(?:复有)?(.{2,12}?(?:天王|天子|大梵天|天))。于(.{2,40}?)法门', s)
    mo = re.search(r'(?:遍观|观察)(.{2,14}?天众)', s)
    if mo:
        out.append('  OBS @%d  %s' % (i, mo.group(1)))
    if mh:
        out.append('HEAD @%d  %s  |  立门: %s' % (i, mh.group(1), mh.group(2)[:24]))
open(r'c:\DA_Practice\huayan_collection\scripts\_60sky_scan.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('lines in seg', len(lines))
