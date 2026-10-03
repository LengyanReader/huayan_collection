# -*- coding: utf-8 -*-
"""_lib_seg.py — 从抽取语料中取出「规范化后可逐字照录」的连续片段。

用法: python scripts/_lib_seg.py <SRC_KEY> <检索词> [before] [after] [occ]
  SRC_KEY: 海云 | 六十 | 繁本 | 简本 | T1735 | T1736 | T1733 | T1732 | T1739 | X0223
输出以 NFKC+部首归一、去除页面标记与空白后的连续文本，供「」引文照录
（与 _roll_verify.py 的归一化规则一致，故照录即可回源）。
"""
import re
import os
import sys
import unicodedata

BASE = r'c:\DA_Practice\huayan_collection'
RAD = {
    '\u2ef6': '日', '\u2ef7': '月', '\u2ed1': '長', '\u2ec5': '門', '\u2eda': '頁',
    '\u2edb': '風', '\u2ed8': '飛', '\u2ec3': '食', '\u2e80': '丨', '\u2e97': '冓',
    '\u2f71': '魚', '\u2f73': '鳥', '\u2f77': '鹵', '\u2f7a': '鹿',
}
HAI_DIR = os.path.join(BASE, 'docs', 'huayanhai', '华严云海', '浩瀚华严海', '八十华严之01品世主妙严品')
YD = os.path.join(BASE, 'docs', 'huayanhai', '义学专题', '经论原典')
CB = os.path.join(BASE, 'data', 'references', 'cbeta_txt')

FILES = {
    '六十': [os.path.join(YD, '六十华严_1.txt')],
    '简本': [os.path.join(YD, '八十华严-简-大华严寺袖珍版_1.txt')],
    '繁本': [os.path.join(YD, '八十华严-繁-大华严寺袖珍版_1.txt')],
    '海云': [os.path.join(HAI_DIR, f) for f in sorted(os.listdir(HAI_DIR)) if f.endswith('.txt')],
    'T1735': [os.path.join(CB, 'T1735_澄观_华严经疏.txt')],
    'T1736': [os.path.join(CB, 'T1736_澄观_随疏演义钞.txt')],
    'T1733': [os.path.join(CB, 'T1733_法藏_探玄记.txt')],
    'T1732': [os.path.join(CB, 'T1732_法藏_搜玄记.txt')],
    'T1739': [os.path.join(CB, 'T1739_李通玄_新华严经论.txt')],
    'X0223': [os.path.join(CB, 'X0223_李通玄_华严经合论.txt')],
}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(ch, ch) for ch in s)


def load(key):
    txt = ''.join(open(p, encoding='utf-8').read() for p in FILES[key])
    txt = re.sub(r'<<<PAGE \d+>>>', '', txt)
    txt = re.sub(r'\s+', '', txt)  # 去空白/换行（与 cjk 归一化方向一致）
    return norm(txt)


def main():
    key = sys.argv[1]
    q = norm(re.sub(r'\s+', '', sys.argv[2]))
    before = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    after = int(sys.argv[4]) if len(sys.argv) > 4 else 260
    occ = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    t = load(key)
    start = -1
    for _ in range(occ):
        start = t.find(q, start + 1)
    if start < 0:
        print('NOT FOUND in %s' % key)
        return
    print('[%s occ=%d len=%d]' % (key, occ, len(t)))
    print(t[max(0, start - before): start + len(q) + after])


if __name__ == '__main__':
    main()
