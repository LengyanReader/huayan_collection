# -*- coding: utf-8 -*-
"""_reorder_jia.py — 把每组「诸家强调」的分列 bullet 按四家时代先后重排:
  法藏(643) → 李通玄(687) → 澄观(738) → 海云继梦(今)
只重排 - bullet 行的顺序, 不改任何 `「」` 内容/经号。幂等: 已按此序者不动。
"""
import re
import os

BASE = r'c:\DA_Practice\huayan_collection'
P = os.path.join(BASE, 'docs', '经学文献', '华严经细读_第一部_世主妙严品.md')
HDR = '**诸家强调**'


def era_key(bullet):
    b = bullet[2:]
    if '法藏' in b[:12]:
        return 0
    if '李通玄' in b[:12]:
        return 1
    if '澄观' in b[:12] or '唐·澄观' in b[:12]:
        return 2
    if '海云继梦' in b[:12]:
        return 3
    return 9  # 未识之家置于末尾(理论不应出现)


def main():
    lines = open(P, encoding='utf-8').read().split('\n')
    out = []
    i = 0
    reordered = 0
    while i < len(lines):
        ln = lines[i]
        out.append(ln)
        if ln.startswith(HDR):
            # 收集其后: 允许一个空行 + 连续 - bullet
            j = i + 1
            block = []
            if j < len(lines) and lines[j].strip() == '':
                block.append('')
                j += 1
            bullets = []
            while j < len(lines) and lines[j].startswith('- '):
                bullets.append(lines[j])
                j += 1
            if bullets:
                order = [era_key(b) for b in bullets]
                if order != sorted(order):  # 未有序才重排(stable)
                    bullets = sorted(bullets, key=era_key)
                    reordered += 1
                out.extend(block)
                out.extend(bullets)
            else:
                out.extend(block)
            i = j
            continue
        i += 1
    open(P, 'w', encoding='utf-8').write('\n'.join(out))
    print('reordered blocks =', reordered)


if __name__ == '__main__':
    main()
