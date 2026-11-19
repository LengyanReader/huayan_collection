# -*- coding: utf-8 -*-
"""《般若空宗三论中观全方位研究》引文回源核验。
底本：T30n1564（中论·canonical）、T45n1852（三论玄义）、T45n1854（二谛义）、T45n1858（肇论）。
访问日期：2026-11-20。"""
import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CAN = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, 'data', 'references', 'cbeta'))
WS = os.path.join(HERE, 'xml')
PUNCT = set('，。、；：？！「」『』（）《》〈〉……—－·“”‘’ \u3000\n\r\t()[]')

def load(tid, canonical=False):
    p = os.path.join(CAN, tid + '.xml')
    xml = open(p, encoding='utf-8').read()
    jp = [(m.start(), m.group(1)) for m in re.finditer(r'<cb:juan[^>]*n="(\d+)"', xml)]
    chars, pm, it = [], [], False
    for i, ch in enumerate(xml):
        if ch == '<': it = True
        elif ch == '>': it = False
        elif not it: chars.append(ch); pm.append(i)
    return ''.join(chars), pm, jp

def juan_of(pm, jp, p):
    x = pm[p]; cur = None
    for q, n in jp:
        if q <= x: cur = n
        else: break
    return cur

def np(s):
    return ''.join(ch for ch in s if ch not in PUNCT)

def find_ctx(text, needle, before=16, after=28):
    hn, nn = np(text), np(needle)
    idx = hn.find(nn)
    if idx < 0: return None
    pos = [i for i, ch in enumerate(text) if ch not in PUNCT]
    if idx >= len(pos): return None
    s = pos[idx]; e = pos[min(idx + len(nn) - 1, len(pos) - 1)] + 1
    return text[max(0, s - before):min(len(text), e + after)].replace('\n', '⏎')

T1564, PM1, JP1 = load('T30n1564', canonical=True)
T1852, PM2, JP2 = load('T45n1852')
T1854, PM4, JP4 = load('T45n1854')
T1858, PM8, JP8 = load('T45n1858')
T1585, PM5, JP5 = load('T31n1585', canonical=True)

QUOTES = [
 ('T30n1564', '八不偈', '不生亦不滅，不常亦不斷，不一亦不異，不來亦不出'),
 ('T30n1564', '三是偈(无字形)', '眾因緣生法，我說即是無'),
 ('T30n1564', '三是偈(空字形-查异文)', '我說即是空'),
 ('T30n1564', '空亦复空', '大聖說空法，為離諸見故'),
 ('T30n1564', '有空义', '以有空義故，一切法得成'),
 ('T45n1852', '玄义归敬', '不生不滅'),
 ('T45n1852', '玄义二大门', '一破邪、二顯正'),
 ('T45n1852', '义唯二辙', '義唯二轍：一曰顯正、二曰破邪'),
 ('T45n1854', '十重对开善', '初則二諦大意、最後二諦同異'),
 ('T45n1854', '教二谛', '於教二諦'),
 ('T45n1854', '山门相承', '山門相承'),
 ('T45n1858', '不真空', '不真空論'),
 ('T45n1858', '物不迁', '物不遷論'),
 ('T45n1858', '般若无知', '般若無知論'),
 ('T45n1858', '非有非无', '非有非無'),
 ('T45n1858', '即色', '即色'),
 ('T31n1585', '三无性偈', '即依此三性，立彼三無性'),
 ('T31n1585', '唯识实性', '此諸法勝義，亦即是真如'),
 ('T31n1585', '遍计空则依他见', '未達遍計所執性空，不如實知依他有'),
 ('T31n1585', '种子更互为因', '任持種子，與一切法更互為因'),
 ('T31n1585', '大圆镜智', '如大圓鏡，現眾色像'),
 ('T31n1585', '平等性智', '觀一切法，自、他有情，悉皆平等'),
 ('T31n1585', '无性趣寂', '無性有情不能窮底，故說「甚深」'),
 ('T31n1585', '凡即无性', '「凡」即無性，「愚」即趣寂'),
]

total = ok = 0
cur_tid = None
for tid, label, q in QUOTES:
    if tid != cur_tid:
        cur_tid = tid
        print('=' * 70)
        print('##', tid)
    total += 1
    text, pm, jp = {'T30n1564': (T1564, PM1, JP1), 'T45n1852': (T1852, PM2, JP2),
                    'T45n1854': (T1854, PM4, JP4), 'T45n1858': (T1858, PM8, JP8), 'T31n1585': (T1585, PM5, JP5)}[tid]
    ctx = find_ctx(text, q)
    if ctx is None:
        print('  [MISS] %-18s %s' % (label, q))
    else:
        ok += 1
        j = None
        hn, pmf = np(text), None
        # 简易 juan
        hn_idx = np(text).find(np(q))
        pos_list = [i for i, ch in enumerate(text) if ch not in PUNCT]
        if hn_idx < len(pos_list):
            x = pos_list[hn_idx]
            for qq, nn in jp:
                if qq <= x: j = nn
                else: break
        print('  [ ok ] %-18s j%-4s %s' % (label, j, q))
        print('         …%s…' % ctx)
print('=' * 70)
print('TOTAL %d  OK %d  MISS %d' % (total, ok, total - ok))
