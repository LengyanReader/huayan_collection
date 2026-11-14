# -*- coding: utf-8 -*-
"""extract_sutra_chapters.py — 三译按「品」抽取全文＋跨译品目对照（供悬浮对照阅读窗）

输出：
  web/demo/data/sutra/c80/p001..p039.json   八十华严 39 品（品内按卷分段）
  web/demo/data/sutra/c60/p001..p034.json   六十华严 34 品
  web/demo/data/sutra/c40/p039.json         四十华严 1 品（40 卷）
  web/demo/data/sutra/mapping.json          品目索引＋八十→六十/四十对照表

原则：品文自品题起、至下一品题前止；跨卷者按卷切段，不混入邻品正文。
"""
import io, re, sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

OUT = 'web/demo/data/sutra'
for sub in ('c80', 'c60', 'c40'):
    os.makedirs(OUT + '/' + sub, exist_ok=True)

HAN = re.compile(r'[\u3400-\u9fff]')
def cjk(s):
    return len(HAN.findall(s))

def clean_text(xml):
    """XML→阅读文本：去标签·留标点·按 <lb> 分段"""
    s = xml
    s = re.sub(r'<note[^>]*>.*?</note>', '', s, flags=re.S)
    s = re.sub(r'<anchor[^>]*/>', '', s)
    s = re.sub(r'<mulu[^>]*/>|<cb:mulu[^>]*>.*?</cb:mulu>', '', s, flags=re.S)
    s = re.sub(r'<byline[^>]*>.*?</byline>', '', s, flags=re.S)
    s = re.sub(r'<head[^>]*>(.*?)</head>', r'\n【\1】\n', s, flags=re.S)
    s = re.sub(r'<lb n="[^"]*"[^>]*/>', '\n', s)
    s = re.sub(r'<p[^>]*>', '\n', s)
    s = re.sub(r'</p>', '\n', s)
    s = re.sub(r'<milestone[^>]*/>', '', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'【\s*】', '', s)
    lines = [l.strip() for l in s.split('\n')]
    lines = [l for l in lines if l]
    paras, cur = [], ''
    for l in lines:
        cur += l
        if len(cur) >= 120 and re.search(r'[。！？』」]$', cur):
            paras.append(cur); cur = ''
    if cur:
        paras.append(cur)
    return paras

def strip_vol_end(p):
    """去段末「大方廣佛華嚴經卷第X」卷尾题（经文本身不含此句）"""
    return re.sub(r'大方廣佛華嚴經卷第?[一二三四五六七八九十百]+$', '', p).strip()

def extract_xml(fp, label, chap_re):
    raw = io.open(fp, encoding='utf-8').read()
    # 削去译本后记（六十末尾「華嚴經梵本凡十萬偈…」等，非经文）
    cuts = [p for p in (raw.find('華嚴經梵本凡十萬偈'),
                        raw.find('時吳郡內史孟顗')) if p > 0]
    if cuts:
        raw = raw[:min(cuts)]
    titles = [(int(m.group(1)), re.sub(r'^\d+\s*', '', m.group(2).strip()), m.start())
              for m in re.finditer(chap_re, raw)]
    titles.sort(key=lambda x: x[2])
    vols = [(int(m.group(1)), m.start())
            for m in re.finditer(r'<milestone n="(\d+)" unit="juan"/>', raw)]
    back = raw.find('<back>')                      # 校勘附录起点·非经文
    hard_end = back if back > 0 else len(raw)
    chapters = []
    for i, (pin, title, pos) in enumerate(titles):
        end = titles[i + 1][2] if i + 1 < len(titles) else hard_end
        body = raw[pos:end]
        v0 = max(v for v, s in vols if s < pos)
        ms = [(int(m.group(1)), m.start())
              for m in re.finditer(r'<milestone n="(\d+)" unit="juan"/>', body)]
        raw_segs = []
        if not ms:
            raw_segs.append((v0, body))
        else:
            if ms[0][1] > 0:
                raw_segs.append((v0, body[:ms[0][1]]))
            for j, (v, s) in enumerate(ms):
                e = ms[j + 1][1] if j + 1 < len(ms) else len(body)
                seg = body[s:e]
                if seg.strip():
                    raw_segs.append((v, seg))
        segs = []
        for v, seg in raw_segs:
            paras = []
            for p in clean_text(seg):
                p = strip_vol_end(p)
                if p:
                    paras.append(p)
            if paras:
                segs.append({'v': v, 'paras': paras})
        chapters.append({'p': pin, 'title': title, 'segs': segs})
    print('%s: %d 品, 品内分段 %d, CJK %d' % (
        label, len(chapters), sum(len(c['segs']) for c in chapters),
        sum(cjk(p) for c in chapters for s in c['segs'] for p in s['paras'])))
    return chapters

def extract_40(fp):
    t = io.open(fp, encoding='utf-8', errors='ignore').read()
    # 削去经末进上表／元代校勘劝缘题记（非经文）；取最早标记
    cuts = [p for p in (t.find('南天竺烏茶國'), t.find('大昭慶寺前住持')) if p > 0]
    if cuts:
        t = t[:min(cuts)]
    marks = [(m.start(), m.group(1))
             for m in re.finditer(r'大方廣佛華嚴經卷第([一二三四五六七八九十百]+)', t)]
    CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    def cn2n(s):
        if s in CN:
            return CN[s]
        if s.startswith('十'):
            return 10 + (CN[s[1]] if len(s) > 1 and s[1] in CN else 0)
        if '十' in s:
            a, _, b = s.partition('十')
            v = CN[a] * 10 if a else 10
            if b:
                v += CN.get(b, 0)
            return v
        if s.startswith('百'):
            v = 100
            rest = s[1:]
            if rest and rest[0] in CN and rest[0] != '十':
                v += CN[rest[0]] * 10 if '十' in rest else CN.get(rest[0], 0)
                if '十' in rest:
                    seg2 = rest.split('十')[-1]
                    if seg2 and seg2[0] in CN:
                        v += CN[seg2[0]]
            return v
        return 0
    marks = [(pos, cn2n(cn)) for pos, cn in marks]
    starts = [marks[i][0] for i in range(0, len(marks), 2)]
    segs = []
    for i, pos in enumerate(starts):
        n = i + 1
        end = starts[i + 1] if i + 1 < len(starts) else len(t)
        seg = t[pos:end]
        paras = [p.strip() for p in re.split(r'\n+', seg)
                 if p.strip() and not re.match(r'^大方廣佛華嚴經卷第', p.strip())]
        paras = [re.sub(r'\s+', '', p) for p in paras]
        joined = ''.join(p for p in paras if p)
        sents = re.split(r'(?<=[。！？；」』])', joined)
        paras, cur = [], ''
        for s_ in sents:
            cur += s_
            if len(cur) >= 160:
                paras.append(cur); cur = ''
        if cur:
            paras.append(cur)
        if paras:
            segs.append({'v': n, 'paras': paras})
    ch = {'p': 39, 'title': '入法界品', 'segs': segs}
    print('四十: 1 品, %d 卷段, CJK %d' % (len(segs), sum(cjk(p) for s in segs for p in s['paras'])))
    return [ch]

# ---------- 八十 ----------
c80 = extract_xml('data/references/cbeta/T10n0279.xml', '八十',
                  r'<cb:mulu level="1" n="(\d+)" type="品">([^<]*)</cb:mulu>')
# ---------- 六十 ----------
c60 = extract_xml('data/references/cbeta/T09n0278.xml', '六十',
                  r'<cb:mulu level="1" n="(\d+)" type="品">([^<]*)</cb:mulu>')
# ---------- 四十 ----------
c40 = extract_40('data/references/cbeta_txt/T10n0293.txt')

for tag, chs in (('c80', c80), ('c60', c60), ('c40', c40)):
    for ch in chs:
        fp = '%s/%s/p%03d.json' % (OUT, tag, ch['p'])
        json.dump(ch, io.open(fp, 'w', encoding='utf-8'), ensure_ascii=False,
                  separators=(',', ':'))
    print(tag, 'files:', len(os.listdir('%s/%s' % (OUT, tag))))

# ---------- 跨译品目对照（八十品号 → 六十品号；0＝六十阙）----------
X60 = {1: 1,
       2: 2, 3: 2, 4: 2, 5: 2, 6: 2,           # 六十〈盧舍那佛品〉统摄八十品2–6
       7: 3, 8: 4, 9: 5, 10: 6, 11: 7, 12: 8, 13: 9, 14: 10, 15: 11,
       16: 12, 17: 13, 18: 14, 19: 15, 20: 16, 21: 17, 22: 18, 23: 19,
       24: 20, 25: 21, 26: 22,
       27: 0,                                   # 六十阙〈十定品〉（译本差异）
       28: 23,                                  # 六十〈十明品〉＝八十〈十通品〉
       29: 24, 30: 25, 31: 26, 32: 27, 33: 28, 34: 29, 35: 30, 36: 31,
       37: 32, 38: 33, 39: 34}
assert len(X60) == 39
X40 = {39: 39}

notes = {
    '2': {'60': '六十译〈盧舍那佛品〉统摄八十品2–6（开合不同·如实）'},
    '3': {'60': '六十译〈盧舍那佛品〉统摄八十品2–6（开合不同·如实）'},
    '4': {'60': '六十译〈盧舍那佛品〉统摄八十品2–6（开合不同·如实）'},
    '5': {'60': '六十译〈盧舍那佛品〉统摄八十品2–6（开合不同·如实）'},
    '6': {'60': '六十译〈盧舍那佛品〉统摄八十品2–6（开合不同·如实）'},
    '27': {'60': '六十译阙〈十定品〉（译本差异·如实）'},
    '28': {'60': '六十译〈十明品〉与八十〈十通品〉名异实同'},
    '39': {'40': '四十华严即〈入法界品〉全译（四十卷）'},
}

def ch_index(chs, tag):
    return {str(ch['p']): {'file': ('%s/p%03d.json' % (tag, ch['p'])),
                           'title': ch['title'],
                           'vols': [s['v'] for s in ch['segs']]}
            for ch in chs}

mapping = {
    'v80': ch_index(c80, 'c80'),
    'v60': ch_index(c60, 'c60'),
    'v40': ch_index(c40, 'c40'),
    'x60': {str(k): v for k, v in X60.items()},
    'x40': {str(k): v for k, v in X40.items()},
    'notes': notes,
}
json.dump(mapping, io.open(OUT + '/mapping.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('mapping.json ✓  x60:', len(X60), ' x40:', len(X40))
