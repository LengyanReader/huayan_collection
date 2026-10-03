# -*- coding: utf-8 -*-
"""_js_pack.py — 经首(卷一 序分/道场庄严/成正觉)四家评述取窗口。
锚点用 NFKC+RAD 归一后检索(同 _roll_verify)。输出 scripts/_js_out.txt。
"""
import re
import os
import unicodedata

BASE = r'c:\DA_Practice\huayan_collection'
YD = os.path.join(BASE, 'docs', 'huayanhai', '义学专题', '经论原典')
HAI_DIR = os.path.join(BASE, 'docs', 'huayanhai', '华严云海', '浩瀚华严海', '八十华严之01品世主妙严品')
CB = os.path.join(BASE, 'data', 'references', 'cbeta_txt')
RAD = {
    '\u2ef6': '日', '\u2ef7': '月', '\u2ed1': '長', '\u2ec5': '門', '\u2eda': '頁',
    '\u2edb': '風', '\u2ed8': '飛', '\u2ec3': '食', '\u2e80': '丨', '\u2e97': '冓',
    '\u2f71': '魚', '\u2f73': '鳥', '\u2f77': '鹵', '\u2f7a': '鹿',
}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(ch, ch) for ch in s)


SRC = {}


def load(key):
    if key == '海云首':
        ps = [os.path.join(HAI_DIR, '01华严经经首_1.txt')]
    elif key == '六十':
        ps = [os.path.join(YD, '六十华严_1.txt')]
    else:
        ps = [os.path.join(CB, f) for f in os.listdir(CB) if f.startswith(key + '_')]
    txt = ''.join(open(p, encoding='utf-8').read() for p in ps)
    txt = re.sub(r'<<<PAGE \d+>>>', '', txt)
    txt = re.sub(r'\s+', '', txt)
    return norm(txt)


def get(key):
    if key not in SRC:
        SRC[key] = load(key)
    return SRC[key]


# (标签, 源key, [锚点候选], before, after)
SPECS = [
    # —— 澄观 十门分别（释品由致）——
    ('澄观·十门总标', 'T1735', ['將將釋此品', '十門', '略舉十門', '十義門'], 40, 900),
    ('澄观·释题目', 'T1735', ['世主妙嚴品', '釋世主', '依教', '辨體'], 40, 700),
    ('澄观·序分开首', 'T1735', ['如是我聞', '一時佛在', '摩竭提'], 40, 600),
    ('澄观·道场庄严', 'T1735', ['菩提場', '莊嚴', '其地堅固', '道場'], 30, 500),
    # —— 法藏 探玄记 开卷 ——
    ('法藏·十门/释名', 'T1733', ['十門', '略以十門', '將欲釋經', '釋题名', '解释', '十種'], 40, 900),
    ('法藏·如是我闻', 'T1733', ['如是我聞', '如是我', '依處', '說人'], 40, 600),
    ('法藏·成正觉', 'T1733', ['始成正覺', '成正覺', '盧舍那'], 30, 500),
    # —— 李通玄 合论 ——
    ('李通玄·释题目', 'X0223', ['何故名為大方廣', '大者無方', '釋經題目', '世主妙嚴者'], 40, 800),
    ('李通玄·如是我闻', 'X0223', ['如是我聞', '如是我', '一時'], 40, 500),
    ('李通玄·成正觉/菩提场', 'X0223', ['菩提場', '成正覺', '摩竭'], 30, 600),
    # —— 海云 经首讲记 ——
    ('海云首·释经题', '海云首', ['大方广佛华严经', '经题', '题目'], 20, 500),
    ('海云首·如是我闻', '海云首', ['如是我闻', '一时'], 20, 400),
    ('海云首·信位/所信因果', '海云首', ['信', '所信因果', '澄观'], 20, 400),
    ('海云首·道场庄严', '海云首', ['道场', '菩提场', '庄严', '摩尼'], 20, 400),
    ('海云首·世界严净', '海云首', ['华藏世界', '世界', '卢舍那'], 20, 400),
    # —— 六十本 经首对照 ——
    ('六十本·序分开首', '六十', ['如是我闻', '一时佛在', '摩竭提国'], 20, 400),
    ('六十本·道场庄严', '六十', ['其地', '菩提树', '师子座', '道场'], 20, 400),
]


def main():
    out = []
    for label, key, anchors, before, after in SPECS:
        t = get(key)
        hit = None
        for a in anchors:
            i = t.find(norm(a))
            if i >= 0:
                hit = (a, t[max(0, i - before): i + after])
                break
        out.append('\n\n########## %s [%s] ##########\n%s' % (
            label, hit[0] if hit else 'MISS', hit[1] if hit else '(未命中)'))
    open(os.path.join(BASE, 'scripts', '_js_out.txt'), 'w', encoding='utf-8').write(''.join(out))
    print('wrote scripts/_js_out.txt', sum(len(x) for x in out), 'chars')


if __name__ == '__main__':
    main()
