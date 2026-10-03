# -*- coding: utf-8 -*-
"""_bold_60.py — 把每条「六十本原文」bullet 里的晋译 `「」` 引用整体加粗(**「…」**)。
标记置于引号外, 不在 「」内部加粗。仅处理以 `- **六十本原文：**` 开头的行,
故 〔本文判断〕/对照 里的评论性 `「」` 不受影响。幂等: 已加粗者(前面紧跟 **)跳过。
"""
import re
import os

BASE = r'c:\DA_Practice\huayan_collection'
P = os.path.join(BASE, 'docs', '经学文献', '华严经细读_第一部_世主妙严品.md')
PRE = '- **六十本原文：**'


def bold_line(line):
    out = []
    i = 0
    n = len(line)
    changed = False
    while i < n:
        if line[i] == '「':
            j = line.find('」', i)
            if j < 0:
                out.append(line[i])
                i += 1
                continue
            # 已加粗? 前紧邻 '**' 且后紧邻 '**'
            quoted = line[i:j + 1]
            if ''.join(out).endswith('**') and line[j + 1:j + 3] == '**':
                out.append(quoted)
            else:
                out.append('**' + quoted + '**')
                changed = True
            i = j + 1
        else:
            out.append(line[i])
            i += 1
    return ''.join(out), changed


def main():
    lines = open(P, encoding='utf-8').read().split('\n')
    cnt = 0
    for k, ln in enumerate(lines):
        if ln.startswith(PRE):
            new, ch = bold_line(ln)
            if ch:
                lines[k] = new
                cnt += 1
    open(P, 'w', encoding='utf-8').write('\n'.join(lines))
    print('bolded 六十本原文 lines =', cnt)


if __name__ == '__main__':
    main()
