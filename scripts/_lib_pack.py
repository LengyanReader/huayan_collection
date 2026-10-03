# -*- coding: utf-8 -*-
"""_lib_pack.py — 为卷三 retrofit 各组批量取出 澄观/法藏/李通玄 语料窗口，
写入 scripts/_pack.txt（UTF-8）。每组每源尝试多个候选锚点，命中即取。
"""
import re
import os
import unicodedata

BASE = r'c:\DA_Practice\huayan_collection'
CB = os.path.join(BASE, 'data', 'references', 'cbeta_txt')
RAD = {'\u2ed1': '長', '\u2ec5': '門', '\u2eda': '頁', '\u2edb': '風', '\u2f71': '魚', '\u2f73': '鳥'}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(ch, ch) for ch in s)


def load(fn):
    t = open(os.path.join(CB, fn), encoding='utf-8').read()
    t = re.sub(r'<<<PAGE \d+>>>', '', t)
    return norm(re.sub(r'\s+', '', t))


SRC = {
    '澄观': load('T1735_澄观_华严经疏.txt'),
    '法藏': load('T1733_法藏_探玄记.txt'),
    '李通玄': load('X0223_李通玄_华严经合论.txt'),
}

# 组号 -> [(候选锚点...)]  用 上首名/类目词，优先命中“释颂/义判”体
GROUPS = {
    '4.3 乾闼婆': ['法樂', '乾闥', '尋香'],
    '4.4 鸠盘荼': ['鳩槃荼', '怨害', '斗諍'],
    '4.5 龙': ['毘婁博叉', '龍王', '興雲'],
    '4.6 夜叉': ['毘沙門', '夜叉', '輕捷'],
    '4.7 摩睺罗伽': ['摩睺', '大腹'],
    '4.9 迦楼罗': ['迦樓羅', '妙翅'],
    '4.10 阿修罗': ['阿修羅', '憍慢'],
    '4.11 主昼': ['示現宮殿', '主晝神十'],
    '4.13 主方': ['遍住一切', '主方神'],
    '4.14 主空': ['淨光普照', '主空神'],
    '4.15 主风': ['無礙光明主風', '主風神'],
}
AFTER = 320


def win(t, key, after=AFTER):
    i = t.find(key)
    if i < 0:
        return None
    return t[i:i + after]


out = []
for g, keys in GROUPS.items():
    out.append('\n\n########## %s ##########' % g)
    for sname, t in SRC.items():
        seg = None
        used = None
        for k in keys:
            seg = win(t, k)
            if seg:
                used = k
                break
        out.append('---- %s [%s] ----\n%s' % (sname, used or 'MISS', seg or '(未命中)'))
open(os.path.join(BASE, 'scripts', '_pack.txt'), 'w', encoding='utf-8').write(''.join(out))
print('wrote scripts/_pack.txt', sum(len(x) for x in out), 'chars')
