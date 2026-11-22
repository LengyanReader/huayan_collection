# -*- coding: utf-8 -*-
import os, re, sys, hashlib, shutil
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
SRC = os.path.join(ROOT, 'workspace', 'huayan_zong', 'xml', 'T48n2015.xml')
CAN = os.path.join(ROOT, 'data', 'references', 'cbeta')
DST = os.path.join(CAN, 'T48n2015.xml')
assert os.path.exists(SRC), SRC
data = open(SRC, 'rb').read()
assert b'</TEI>' in data[-40:], 'tail check fail'
sha = hashlib.sha256(data).hexdigest()[:12]
shutil.copyfile(SRC, DST)
print('copied ->', DST, len(data), 'B sha256:%s' % sha)

# INGEST_log
p = os.path.join(CAN, 'INGEST_log.md')
s = open(p, encoding='utf-8').read()
add = '''
## L.513h · 华严宗密底本入库（2026-11-22）

> raw.githubusercontent.com/cbeta-org/xml-p5@master（T/T48/ 分卷夹路径）直取；为《华严宗全方位研究》（新篇）「经是佛语，禅是佛意」句与禅教一致节回源底本。许可：CBETA 非营利用途。

| 经号 | 题名 | 册 | 字节 | 取回日期 | 状态 | 文件 |
|---|---|---|---|---|---|---|
| T48n2015 | 禪源諸詮集都序（唐宗密撰·四卷） | 册48 | 310,554 | 2026-11-22 | 已入库 sha256:%s | `T48n2015.xml` |
''' % sha
assert 'L.513h' not in s
s = s.rstrip('\n') + '\n' + add
open(p, 'w', encoding='utf-8').write(s)
print('INGEST_log +L.513h')

# README
p = os.path.join(CAN, 'README.md')
s = open(p, encoding='utf-8').read()
anchor = '| `T45n1866.xml` | `T1866` | 《華嚴一乘教義分齊章》四卷（唐法藏撰）——五教（小/始/終/頓/圓）十宗（我法俱有宗起）判释原文 | CBETA TEI/P5·raw·`2026-11-22` |'
row = '\n| `T48n2015.xml` | `T2015` | 《禪源諸詮集都序》四卷（唐宗密撰）——「經是佛語，禪是佛意」＋以教三種證禪三宗（息妄修心/泯絕無寄/直明心性）原文 | CBETA TEI/P5·raw·`2026-11-22` |'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + row, 1)
open(p, 'w', encoding='utf-8').write(s)
print('README +T48n2015 row')
