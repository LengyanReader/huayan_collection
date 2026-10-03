# -*- coding: utf-8 -*-
"""_split_jia.py — 把 25 组「诸家强调」从行内四家挤一段改为分列(每家一个 bullet)。
只动结构分隔符(；与全角空格　)与海云标签加粗，`「」` 逐字引文/经号/括注一律不动。
仅处理以 **诸家强调** 起头的整行；幂等：已是分列(下一行以 - 开头)则跳过。
"""
import re
import os

BASE = r'c:\DA_Practice\huayan_collection'
P = os.path.join(BASE, 'docs', '经学文献', '华严经细读_第一部_世主妙严品.md')

# 前三家(注释/探玄/合论)以粗体标签定位, 各仅出现一次
MASTER = re.compile(
    r'\*\*(?:唐·)?澄观《(?:华严经)?疏》\*\*'
    r'|\*\*法藏《探玄记》\*\*'
    r'|\*\*李通玄《合论》\*\*'
)
HAI = '海云继梦'
HDR = '**诸家强调**'


def convert(line):
    body = line[len(HDR):].lstrip('\u3000 ')
    # 边界: 前三家粗体标签 + 海云「起始」(末家之后首个 海云继梦, 其括注不再切)
    bounds = [m.start() for m in MASTER.finditer(body)]
    last_master_end = max((m.end() for m in MASTER.finditer(body)), default=-1)
    h = body.find(HAI, last_master_end + 1)
    if h >= 0:
        bounds.append(h)
    bounds = sorted(set(bounds))
    if not bounds:
        return None
    pre = body[:bounds[0]].strip('\uff1b\u3000 ')
    segs = []
    for k, b in enumerate(bounds):
        end = bounds[k + 1] if k + 1 < len(bounds) else len(body)
        seg = body[b:end].strip().rstrip('\uff1b\u3000 ')
        segs.append(seg)
    if pre:
        segs[0] = pre + segs[0]
    # 海云段: 把前导 海云继梦 加粗, 与其余三家标签对称
    out = []
    for s in segs:
        if s.startswith(HAI):
            s = '**' + HAI + '**' + s[len(HAI):]
        out.append('- ' + s)
    return HDR + '\n\n' + '\n'.join(out)


def main():
    lines = open(P, encoding='utf-8').read().split('\n')
    changed = 0
    result = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith(HDR):
            nxt = lines[i + 1] if i + 1 < len(lines) else ''
            if nxt.lstrip().startswith('- '):
                result.append(ln)  # 已分列, 幂等跳过
                i += 1
                continue
            new = convert(ln)
            if new is None:
                result.append(ln)
            else:
                result.append(new)
                changed += 1
            i += 1
            continue
        result.append(ln)
        i += 1
    open(P, 'w', encoding='utf-8').write('\n'.join(result))
    print('converted blocks =', changed)


if __name__ == '__main__':
    main()
