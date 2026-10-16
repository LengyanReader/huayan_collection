#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sjcj_puxian_studies.py — 第三品《普贤三昧品》/ 第四品《世界成就品》数据科学层（L1–L4）复算脚本

口径（与 §7 各表一致，可一命令复算）：
  * 底本      : data/references/cbeta/T10n0279.xml（八十华严，繁体原字形）
  * 范围      : 品题 <head> 起，至次品题 <head>（或卷末）止（「品界口径」）。
                品三 = [卷七开 : 品四题]；品四 = [品四题 : 卷八开]。
  * 剥校勘    : 完全剔除 <note>…</note> 与 <app>…</app>（连同其内文字），
                再剥一切标签与空白，仅计 CJK(3400–9FFF)。
  * 输出      : L1 语言统计（CJK/独字/熵/Zipf/句末/颂）+ L2/L3/L4 图元计数。
  * 依赖      : 仅标准库（无 numpy / networkx），纯 Python 可复算。
数据用法：本脚本只产出计数（实测读数），判读属〔本文判断〕，不作义理之证。

用法: python scripts/sjcj_puxian_studies.py        （打印 JSON）
"""
import re, io, sys, json, math, unicodedata
from collections import Counter

BASE = r'c:\DA_Practice\huayan_collection'
XML = BASE + r'\data\references\cbeta\T10n0279.xml'

# CBETA 偶见 Kangxi 部首/相容字符，归一为正字
RAD = {'\u2ef6': '日', '\u2ef7': '月', '\u2ed1': '長', '\u2ec5': '門', '\u2eda': '頁',
       '\u2edb': '風', '\u2ed8': '飛', '\u2ec3': '食'}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(RAD.get(c, c) for c in s)


def strip_apparatus(s):
    """完全剔除校勘层（note/app 含其内文字）。"""
    s = re.sub(r'<note\b.*?</note>', '', s, flags=re.S)
    s = re.sub(r'<app\b.*?</app>', '', s, flags=re.S)
    return s


def cjk_only(s):
    return ''.join(c for c in norm(s) if '\u3400' <= c <= '\u9fff')


def ols_zipf(chars):
    """Zipf：log-rank vs log-freq OLS，返回 (斜率, R)。"""
    freq = Counter(chars)
    items = sorted(freq.values(), reverse=True)
    xs = [math.log(i + 1) for i in range(len(items))]
    ys = [math.log(v) for v in items]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    slope = sxy / sxx
    R = sxy / math.sqrt(sxx * syy)
    return slope, R


def entropy(chars):
    freq = Counter(chars)
    N = len(chars)
    return -sum((v / N) * math.log2(v / N) for v in freq.values())


# ---------------------------------------------------------------- 主流程
def analyse():
    xml = open(XML, encoding='utf-8').read()
    j7 = re.search(r'<cb:juan n="007" fun="open">', xml)
    j8 = re.search(r'<cb:juan n="008" fun="open">', xml)
    vol7 = xml[j7.start():j8.start()]

    # 品界（剥校勘后定位品题文本；位置取**未归一**文本，以免 NFKC 改易全角标点）
    stripped = re.sub(r'<[^>]+>', '', strip_apparatus(vol7))   # 未 NFKC
    p3 = stripped.find('普賢三昧品第三')
    p4 = stripped.find('世界成就品第四')

    seg3 = stripped[p3:p4]            # 品三（含品题）
    seg4 = stripped[p4:]              # 品四（含品题）至卷末

    out = {}
    for name, pin, seg in (('puxian', '普賢三昧品第三', seg3),
                           ('shijie', '世界成就品第四', seg4)):
        cjk = cjk_only(seg)
        freq = Counter(cjk)
        slope, R = ols_zipf(cjk)
        # 颂：剥标签后的段落无法再计 <lg>/<l>，故在标签态上单独统计
        out[name] = dict(
            cjk_total=len(cjk),
            cjk_net=len(cjk) - len(cjk_only(pin)),
            unique=len(freq),
            H=round(entropy(cjk), 4),
            zipf_slope=round(slope, 4),
            zipf_R=round(R, 4),
            # 句末标点：。！？（全角）——于**未 NFKC** 之剥校勘文本上计
            sent_ends=len(re.findall(r'[。！？]', seg)),
            top12=[(c, v) for c, v in freq.most_common(12)],
            motifs={k: seg.count(k) for k in
                    ['一一', '一切', '三昧', '海雲', '摩尼王雲', '世界海', '海', '塵',
                     '微塵', '微塵數', '入', '起', '現', '遍', '滿', '中', '含',
                     '無量', '無邊', '差別', '無差別', '佛', '諸佛', '如是等',
                     '或', '故', '以']},
        )
    # 颂（标签态）：品三 = 卷七开→品四题；品四 = 品四题→卷八开（均在**标签态** vol7 上定位）
    p4_tag = vol7.find('世界成就品第四')          # 标签态偏移（品题文本内含于 <head>）
    for name, span in (('puxian', vol7[:p4_tag]),
                       ('shijie', vol7[p4_tag:])):
        lgs = re.findall(r'<lg\b[^>]*>(.*?)</lg>', span, flags=re.S)
        out[name]['lg_groups'] = len(lgs)
        out[name]['l_lines'] = sum(len(re.findall(r'<l>', g)) for g in lgs)
        out[name]['verses'] = out[name]['l_lines'] // 2
    return out


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    res = analyse()
    print(json.dumps(res, ensure_ascii=False, indent=1))
