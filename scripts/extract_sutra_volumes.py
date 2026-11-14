# -*- coding: utf-8 -*-
"""extract_sutra_volumes.py — 三译全本按卷抽取＋品卷映射生成（供悬浮对照阅读窗）"""
import io, re, sys, json, os
sys.stdout.reconfigure(encoding='utf-8')
OUT = 'web/demo/data/sutra'
os.makedirs(OUT + '/v80', exist_ok=True)
os.makedirs(OUT + '/v60', exist_ok=True)
os.makedirs(OUT + '/v40', exist_ok=True)

def clean_text(xml):
    """XML→阅读文本：去标签·留标点·按 <lb> 分段"""
    s = xml
    s = re.sub(r'<note[^>]*>.*?</note>', '', s, flags=re.S)
    s = re.sub(r'<anchor[^>]*/>', '', s)
    s = re.sub(r'<mulu[^>]*/>|<cb:mulu[^>]*>.*?</cb:mulu>', '', s, flags=re.S)
    s = re.sub(r'<byline[^>]*>.*?</byline>', '', s, flags=re.S)
    s = re.sub(r'<head[^>]*>(.*?)</head>', r'\n【\1】\n', s, flags=re.S)
    s = re.sub(r'<lb n="[^"]*"[^>]*/>', '\n', s)          # 每行断
    s = re.sub(r'<p[^>]*>', '\n', s)
    s = re.sub(r'</p>', '\n', s)
    s = re.sub(r'<milestone[^>]*/>', '', s)
    s = re.sub(r'<[^>]+>', '', s)                          # 其余标签
    s = re.sub(r'【\s*】', '', s)
    lines = [l.strip() for l in s.split('\n')]
    lines = [l for l in lines if l]
    # 合并过短行成段（句号/问号/叹号后断）
    paras, cur = [], ''
    for l in lines:
        cur += l
        if len(cur) >= 120 and re.search(r'[。！？』」]$', cur):
            paras.append(cur); cur = ''
    if cur:
        paras.append(cur)
    return paras

def split_volumes(xml, unit='juan'):
    ms = list(re.finditer(r'<milestone n="(\d+)" unit="%s"/>' % unit, xml))
    vols = {}
    for i, m in enumerate(ms):
        n = int(m.group(1))
        end = ms[i+1].start() if i+1 < len(ms) else len(xml)
        vols[n] = xml[m.start():end]
    return vols

# ---------- 八十（T10n0279）----------
raw80 = io.open('data/references/cbeta/T10n0279.xml', encoding='utf-8').read()
v80 = split_volumes(raw80)
print('八十卷数:', len(v80))
# 品题定位（cb:mulu type="品" level="1"）
pin80 = {}
for m in re.finditer(r'<cb:mulu level="1" n="(\d+)" type="品">[^<]*</cb:mulu>', raw80):
    pin = int(m.group(1))
    # 找该位置所在卷（之前的最近 milestone）
    vol = max(v for v, s in ((int(mm.group(1)), mm.start()) for mm in re.finditer(r'<milestone n="(\d+)" unit="juan"/>', raw80)) if s < m.start())
    pin80.setdefault(pin, []).append(vol)
print('八十品→卷:', {k: v for k, v in sorted(pin80.items())})

for n, seg in v80.items():
    body = seg[seg.find('>')+1:] if '>' in seg[:200] else seg
    paras = clean_text(body)
    json.dump({'v': n, 'paras': paras}, io.open('%s/v80/j%03d.json' % (OUT, n), 'w', encoding='utf-8'),
              ensure_ascii=False)
print('v80 卷文件:', len(os.listdir(OUT + '/v80')))

# ---------- 六十（T09n0278）----------
raw60 = io.open('data/references/cbeta/T09n0278.xml', encoding='utf-8').read()
v60 = split_volumes(raw60)
print('六十卷数:', len(v60))
pin60 = {}
for m in re.finditer(r'<cb:mulu level="1" n="(\d+)" type="品">[^<]*</cb:mulu>', raw60):
    pin = int(m.group(1))
    vol = max(v for v, s in ((int(mm.group(1)), mm.start()) for mm in re.finditer(r'<milestone n="(\d+)" unit="juan"/>', raw60)) if s < m.start())
    pin60.setdefault(pin, []).append(vol)
print('六十品→卷:', {k: v for k, v in sorted(pin60.items())})
for n, seg in v60.items():
    paras = clean_text(seg)
    json.dump({'v': n, 'paras': paras}, io.open('%s/v60/j%03d.json' % (OUT, n), 'w', encoding='utf-8'),
              ensure_ascii=False)
print('v60 卷文件:', len(os.listdir(OUT + '/v60')))

# ---------- 四十（T10n0293 txt·无卷标→按「卷第N」切）----------
t293 = io.open('data/references/cbeta_txt/T10n0293.txt', encoding='utf-8', errors='ignore').read()
marks = [(m.start(), m.group(1)) for m in re.finditer(r'大方廣佛華嚴經卷第([一二三四五六七八九十百]+)', t293)]
CN = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
def cn2n(s):
    # 简单中文数字（≤120）
    if s in CN: return CN[s]
    if s.startswith('十'): return 10 + (CN[s[1]] if len(s) > 1 and s[1] in CN else 0)
    if '十' in s:
        a, _, b = s.partition('十')
        v = CN[a]*10 if a else 10
        if b: v += CN.get(b, 0)
        return v
    if s.startswith('百'):
        v = 100
        rest = s[1:]
        if rest and rest[0] in CN and rest[0] != '十':
            v += CN[rest[0]]*10 if '十' in rest else CN.get(rest[0], 0)
            if '十' in rest:
                seg2 = rest.split('十')[-1]
                if seg2 and seg2[0] in CN: v += CN[seg2[0]]
        return v
    return 0
marks = [(pos, cn2n(cn)) for pos, cn in marks]
print('四十卷标:', len(marks), marks[:5], marks[-2:])
# 每卷两标（卷首含译者行＋卷尾回指）——偶位为卷首、奇位为卷尾
starts = [marks[i][0] for i in range(0, len(marks), 2)]
vols40 = {}
for i, pos in enumerate(starts):
    n = i + 1
    end = starts[i + 1] if i + 1 < len(starts) else len(t293)
    seg = t293[pos:end]
    paras = [p.strip() for p in re.split(r'\n+', seg) if p.strip() and not re.match(r'^大方廣佛華嚴經卷第', p.strip())]
    paras = [re.sub(r'\s+', '', p) for p in paras]
    paras = [p for p in paras if p]
    # 无换行长文→按句读切分（每 3 句一段·便于阅读滚动）
    joined = ''.join(paras)
    sents = re.split(r'(?<=[。！？；」』])', joined)
    paras, cur = [], ''
    for s_ in sents:
        cur += s_
        if len(cur) >= 160:
            paras.append(cur); cur = ''
    if cur:
        paras.append(cur)
    vols40[n] = paras
for n, paras in vols40.items():
    json.dump({'v': n, 'paras': paras}, io.open('%s/v40/j%03d.json' % (OUT, n), 'w', encoding='utf-8'),
              ensure_ascii=False)
print('v40 卷文件:', len(os.listdir(OUT + '/v40')))

# ---------- 映射 JSON ----------
mapping = {
    'v80': {str(k): v for k, v in sorted(pin80.items())},
    'v60': {str(k): v for k, v in sorted(pin60.items())},
    'v40': {'39': list(range(1, 41))},
}
json.dump(mapping, io.open(OUT + '/mapping.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('mapping.json ✓')
