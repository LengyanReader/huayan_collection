# -*- coding: utf-8 -*-
"""在 T30n1579/T1580 中检索关键义理锚点，输出 juan + 原文上下文（含标点）。"""
import re, sys, os

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

def load(tid):
    xml = open(os.path.join(HERE, 'xml', tid + '.xml'), encoding='utf-8').read()
    juan_pos = [(m.start(), m.group(1)) for m in re.finditer(r'<cb:juan[^>]*n="(\d+)"', xml)]
    chars, pmap, intag = [], [], False
    for i, ch in enumerate(xml):
        if ch == '<':
            intag = True
        elif ch == '>':
            intag = False
        elif not intag:
            chars.append(ch); pmap.append(i)
    return ''.join(chars), pmap, juan_pos

def juan_at(pmap, juan_pos, plain_pos):
    x = pmap[plain_pos]
    cur = None
    for p, n in juan_pos:
        if p <= x: cur = n
        else: break
    return cur

TEXT, PMAP, JPOS = load('T30n1579')
TEXT2, PMAP2, JPOS2 = load('T30n1580')

QUERIES = [
 ('五识身自性', '云何五識身相應地'),
 ('意地门', '云何意地'),
 ('阿赖耶识问', '云何阿賴耶識'),
 ('阿赖耶识体', '阿賴耶識自性'),
 ('八证起', '云何建立阿賴耶識'),
 ('三自性', '云何三種自性'),
 ('九种心住', '云何九種心住'),
 ('四种所缘', '云何四種所緣境事'),
 ('四寻思', '云何菩薩於法假立尋思'),
 ('有余依', '云何有餘依地'),
 ('无余依', '云何無餘依地'),
 ('摄释五相', '云何攝釋'),
 ('菩萨地四持', '云何菩薩地'),
 ('十三住', '云何十三住'),
 ('种子', '云何種子'),
 ('转依', '云何轉依'),
 ('所知障', '云何所知障'),
 ('三摩呬多', '云何三摩呬多地'),
 ('静虑爱味', '愛味相應靜慮'),
 ('闻所成', '云何聞所成地'),
 ('思所成', '云何思所成地'),
 ('修所成', '云何修所成地'),
 ('独觉五相', '云何獨覺地'),
 ('菩萨四持名', '四持瑜伽處'),
 ('真实义离言', '離言說相'),
 ('摩呾理迦', '摩呾理迦'),
 ('调伏事', '調伏事'),
 ('本母事', '本母事'),
]
print('===== T30n1579 =====')
for label, q in QUERIES:
    hits = [m.start() for m in re.finditer(re.escape(q), TEXT)]
    if not hits:
        print('[MISS] %-14s %s' % (label, q)); continue
    h = hits[0]
    ctx = TEXT[max(0, h - 30):h + 90].replace('\n', '')
    print('[ ok ] %-14s j%-3s hits=%-3d %s' % (label, juan_at(PMAP, JPOS, h), len(hits), ctx))

print('\n===== T30n1580 (瑜伽师地论释) =====')
for q in ['就初立名', '十七地', '瑜伽師地']:
    hits = [m.start() for m in re.finditer(re.escape(q), TEXT2)]
    if hits:
        h = hits[0]
        print('[ ok ] %-10s %s' % (q, TEXT2[max(0, h - 40):h + 80].replace('\n', '')))
    else:
        print('[MISS]', q)
