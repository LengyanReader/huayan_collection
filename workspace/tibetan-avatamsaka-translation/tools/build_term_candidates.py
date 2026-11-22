#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""章级术语预提取器（L.519 · M6 提前开工的第一步）。

机器只做「观察与候选」，不判释义——术语确认走 M6.3 人工门禁
（抽样 10 条判定释义与华严义理相容）。产出：
data/translation/tibetan_avatamsaka_term_candidates_L519.json
  - seeds.covered / seeds.missed : 既有术语库（glossary.yaml 50 条＋L.354a 内联表）
    在已译章藏文中的命中情况（覆盖检查）
  - candidates.bigrams / unigrams : 已译章藏文高频词候选（计数＋出现章，不在种子内）
  - per_chapter : 各章候选分布

方法注：分词按 tsheg（་）切；虚词停用词表为起步集（标注〔起步集〕）；
候选≠术语，须人工确认后经 glossary 升版接入 prompt 与 M5 扫描。

Usage:
  hy_py312 python -X utf8 build_term_candidates.py [--min-count 4] [--top 60]
"""

import argparse
import collections
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SEG_GLOB = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_trilingual_segments*.json')
GLOSS = os.path.join(ROOT, 'data/translation/glossary.yaml')
SHIYI = os.path.join(ROOT, 'data/alignment/tibetan_shiyi_L354a.json')
OUT = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_term_candidates_L519.json')

# 虚词/语法成分停用词（起步集·单音节为主；后缀形式以 tsheg 连接形式匹配）
STOP = set("""དེ དེ་དག ལ ཡི དང ལས ནི ཀྱི གྱི འི སུ ཏུ རུ དུ ཅེས ཞེས བཞིན
རྣམས ཐམས་ཅད ཡང མ མི རབ ཤིན་ཏུ ལྟར བཞུགས གནས ཡོད འགྱུར བྱེད བྱས
ཚད ལ་ ནས ནས་ཀྱང གྱིས ཀྱིས པ བ འ ག ཅིང ཅིག ཞིང བར བྱ བྱ་ ལགས སོ
མཐོང གཤེགས གསུང སྨྲས ཐོས ཉན འཇིག རྟེན ཁམས དུས དེའི དེ་ལ""".split())

TSEGSPLIT = re.compile(r'་+')


def tokens(bo):
    """按 tsheg 切音节（藏文词内以 tsheg 连接，空格只在短语边界）；shad/空白清理。"""
    bo = re.sub(r'[\u0F0D\u0F0E\u0F0F\u0F11\u0F14\s]+', ' ', bo or '')  # །།༑༎|. 等
    toks = []
    for chunk in bo.split(' '):
        for p in chunk.split('་'):
            p = p.strip()
            if p:
                toks.append(p)
    return toks


def load_glossary_terms():
    """glossary.yaml → {bo_unicode(去尾 shad): {zh, wylie, id, src}}。"""
    terms = {}
    try:
        import yaml  # hy_py312 环境有 PyYAML
        y = yaml.safe_load(io.open(GLOSS, encoding='utf-8'))
        for t in (y.get('terms') or []):
            bo = (t.get('bo_unicode') or '').replace('།', '').strip(' ')
            if bo:
                terms[bo] = {'zh': t.get('zh'), 'wylie': t.get('bo_wylie'),
                             'id': t.get('id'), 'src': 'glossary.yaml'}
    except ImportError:
        print('〔警告〕无 PyYAML——glossary.yaml 跳过，仅用 L.354a（G0.4 同因）')
    return terms


def load_shiyi_terms():
    d = json.load(io.open(SHIYI, encoding='utf-8'))
    terms = {}
    for pair in (d.get('note') or '').split('·'):
        if '=' in pair:
            bo, zh = pair.split('=', 1)
            bo = bo.strip().replace('།', '').strip(' ')
            if bo:
                terms[bo] = {'zh': zh.strip(), 'wylie': None, 'id': None,
                             'src': 'L.354a'}
    return terms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min-count', type=int, default=4)
    ap.add_argument('--bigram-min', type=int, default=2)
    ap.add_argument('--top', type=int, default=60)
    args = ap.parse_args()

    seeds = {}
    g = load_glossary_terms()
    sy = load_shiyi_terms()
    print('种子来源：glossary.yaml %d 条 · L.354a %d 条' % (len(g), len(sy)))
    for t in (g, sy):
        for k, v in t.items():
            seeds.setdefault(k, v)
    print('种子术语 %d 条（去重后）' % len(seeds))

    # ── 已译章 corpus（章→已译段 bo 拼接）──
    corpus = {}
    for fn in sorted(glob.glob(SEG_GLOB)):
        d = json.load(io.open(fn, encoding='utf-8'))
        ch = (d.get('chapter') or {}).get('tibetan_no')
        if not ch:
            continue
        bo_all = ' '.join(s.get('bo') or '' for s in (d.get('segments') or [])
                          if s.get('status') == 'done')
        if bo_all:
            corpus[str(ch)] = corpus.get(str(ch), '') + ' ' + bo_all
    print('已译章：%s' % sorted(corpus))

    # ── 种子覆盖检查 ──
    all_bo = ' '.join(corpus.values())
    covered, missed = [], []
    for bo, meta in sorted(seeds.items()):
        hit = all_bo.count(bo)
        (covered if hit else missed).append(dict(bo=bo, zh=meta.get('zh'),
                                                 wylie=meta.get('wylie'), src=meta.get('src'),
                                                 count=hit))
    print('种子命中 %d / 未命中 %d' % (len(covered), len(missed)))

    # ── 高频候选 ──
    uni = collections.Counter()
    bi = collections.Counter()
    tri = collections.Counter()
    bi_ch = collections.defaultdict(set)
    tri_ch = collections.defaultdict(set)
    uni_ch = collections.defaultdict(set)
    for ch, bo in corpus.items():
        toks = tokens(bo)
        cleaned = [t for t in toks if t not in STOP]
        for t in cleaned:
            uni[t] += 1
            uni_ch[t].add(ch)
        for a, b in zip(cleaned, cleaned[1:]):
            bg = a + '་' + b
            bi[bg] += 1
            bi_ch[bg].add(ch)
        for a, b, c2 in zip(cleaned, cleaned[1:], cleaned[2:]):
            tg = a + '་' + b + '་' + c2
            tri[tg] += 1
            tri_ch[tg].add(ch)

    def pack(c, chmap, minc):
        return [dict(bo=k, count=v, chapters=sorted(chmap[k]))
                for k, v in c.most_common(None) if v >= minc]

    bigrams = pack(bi, bi_ch, args.bigram_min)[:args.top]
    trigrams = pack(tri, tri_ch, args.bigram_min)[:args.top]
    unigrams = [dict(bo=k, count=v, chapters=sorted(uni_ch[k]))
                for k, v in uni.most_common(args.top * 2) if v >= args.min_count][:args.top]

    out = {
        'id': 'tibetan_avatamsaka_term_candidates_L519',
        'date': '2026-11-22', 'batch': 'L.519',
        'nature': '〔机器观察〕候选与覆盖，非术语定案——确认走 M6.3 人工门禁',
        'method': 'tsheg 切分＋停用词〔起步集〕过滤；种子=glossary.yaml(50)＋L.354a 内联表；'
                  '范围=已译段（ch1·ch14–18·done）',
        'gap_note': 'glossary.yaml 50 条中仅 13 条带 bo_unicode——缺 37 条藏文字形，'
                    '为 M6 实测缺口（2026-11-22 本器发现）',
        'seeds': {'covered': covered, 'missed': missed},
        'candidates': {'bigrams': bigrams, 'trigrams': trigrams, 'unigrams': unigrams},
    }
    with io.open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('落盘 %s' % OUT)
    print('trigram 候选前 12：%s' % [x['bo'] for x in trigrams[:12]])
    print('bigram 候选前 15：%s' % [x['bo'] for x in bigrams[:15]])
    print('unigram 候选前 15：%s' % [x['bo'] for x in unigrams[:15]])
    print('种子未命中前 10：%s' % [x['bo'] for x in missed[:10]])


if __name__ == '__main__':
    main()
