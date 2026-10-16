#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""名号层 Zipf 复算 —— 纯标准库（无 numpy / networkx）。

取代 `scripts/_analysis_miaoyan.py` 之 `zipf_names_morpheme`（该脚本因 import numpy /
networkx 而本机不可跑，故旧测被标「未存脚本」）。本脚本以纯标准库复算：名号层之
字符 Zipf（原注称「名号语素」，实为**名号诸字**之字频——`[ch for nm in names for ch in nm]`）。

语料：`scripts/_assembly.json` 之 40 类 414 名（T279 已核），**与经文文本层无关**，
故不受文本切片污染之影响。口径与 `_analysis_miaoyan.py` 一致：
  norm = NFKC + RAD 造字映射；cjk = 只留 U+3400–U+9FFF；Zipf = log-log 拟合斜率取负。

用法：  python scripts/miaoyan_names.py
"""
import io, sys, json, math, unicodedata
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'c:\DA_Practice\huayan_collection'
RAD = {'\u2ef6': '日', '\u2ef7': '月', '\u2ed1': '長', '\u2ec5': '門',
       '\u2eda': '頁', '\u2edb': '風', '\u2ed8': '飛', '\u2ec3': '食'}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(c, c) for c in s)


def cjk(s):
    return ''.join(c for c in norm(s) if '\u3400' <= c <= '\u9fff')


def zipf(series):
    """log-log Zipf：R = Pearson(log rank, log freq)；exponent = -slope（同 numpy.polyfit 次数 1）。"""
    c = Counter(series)
    items = sorted(c.values(), reverse=True)
    n = len(items)
    r = [math.log(i + 1) for i in range(n)]
    f = [math.log(x) for x in items]
    mr = sum(r) / n
    mf = sum(f) / n
    cov = sum((r[i] - mr) * (f[i] - mf) for i in range(n))
    sr = sum((x - mr) ** 2 for x in r)
    sf = sum((y - mf) ** 2 for y in f)
    R = cov / math.sqrt(sr * sf)
    slope = cov / sr
    return dict(types=n, tokens=int(sum(items)), zipf_R=round(R, 4),
                exponent=round(-slope, 3))


def ent(series):
    """Shannon 熵（bit），与 _analysis_miaoyan.py 之 ent() 同式。"""
    c = Counter(series)
    N = sum(c.values())
    H = -sum((v / N) * math.log2(v / N) for v in c.values())
    return round(H, 3)


def main():
    asm = json.load(open(BASE + r'\scripts\_assembly.json', encoding='utf-8'))
    classes = asm['classes']
    names = [cjk(m['name']) for c in classes for m in c.get('members', []) if m.get('name')]
    morph_freq = [ch for nm in names for ch in nm]
    res = zipf(morph_freq)
    res['H_bit'] = ent(morph_freq)
    res['n_names'] = len(names)
    res['distinct_names'] = len(set(names))
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
