# -*- coding: utf-8 -*-
"""_split_60.py — 把 25 组「六十本对读」从单段密排改为三项分列:
  - 六十本原文：(晋译引文, 以 逐字照录）为界)
  - 对照八十本：(对照分析)
  - 〔本文判断〕(若有)
切分只认 `逐字照录）` 与 `〔本文判断〕` 两个「」外标记; 无 逐字照录） 者不改。
`「」` 逐字引文/经号不动。dry=仅打印样例, 不写文件。
"""
import re
import os

BASE = r'c:\DA_Practice\huayan_collection'
P = os.path.join(BASE, 'docs', '经学文献', '华严经细读_第一部_世主妙严品.md')
HDR = '**六十本对读**'
END60 = '逐字照录）'
JUDGE = '〔本文判断〕'


def convert(line):
    if HDR not in line:
        return None
    body = line.split(HDR, 1)[1].lstrip('\u3000 ：:')
    i = body.find(END60)
    if i < 0:
        return None  # 无稳定边界, 保持原样
    end = i + len(END60)
    if body[end:end + 1] == '。':
        end += 1
    part60 = body[:end]
    rest = body[end:]
    j = rest.find(JUDGE)
    cmp_ = rest[:j] if j >= 0 else rest
    judge = rest[j:] if j >= 0 else None
    # 清理对照段前导的破折号/标点/冗余"对照"
    c = cmp_.strip('\u3000 \n')
    while c[:1] in ('—', '。', '：', '、', '；', '，'):
        c = c.lstrip('—')
        c = c.lstrip('\u3000 。：、，；')
    if c.startswith('对照'):
        c = c[len('对照'):].lstrip('\u3000 ：:')
    cmp_ = c
    bullets = ['- **六十本原文：**' + part60, '- **对照八十本：**' + cmp_]
    if judge:
        bullets.append('- ' + judge.rstrip())
    return HDR + '\n\n' + '\n'.join(bullets)


def main(dry=True):
    lines = open(P, encoding='utf-8').read().split('\n')
    changed = 0
    result = []
    samples = {}
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith(HDR):
            nxt = lines[i + 1] if i + 1 < len(lines) else ''
            if nxt.lstrip().startswith('- ') or nxt.lstrip().startswith('**六十本'):
                result.append(ln)  # 已分列
                i += 1
                continue
            new = convert(ln)
            if new is None:
                result.append(ln)
                samples.setdefault('SKIP', ln[:60])
            else:
                result.append(new)
                changed += 1
                if len(samples) < 3 and 'SKIP' not in samples:
                    samples['S%d' % changed] = new
            i += 1
            continue
        result.append(ln)
        i += 1
    if not dry:
        open(P, 'w', encoding='utf-8').write('\n'.join(result))
    report = ['dry=%s changed=%d' % (dry, changed)]
    for k, v in samples.items():
        report.append('==== %s ====' % k)
        report.append(v)
    open(os.path.join(BASE, 'scripts', '_split60_preview.txt'), 'w', encoding='utf-8').write('\n'.join(report))
    print('changed=', changed)


if __name__ == '__main__':
    import sys
    main(dry=('--apply' not in sys.argv))
