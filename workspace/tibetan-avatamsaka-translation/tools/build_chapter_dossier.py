#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""章翻译简报生成器（L.519 · dossier/L2 层）：每章自动装配翻译知识包，
喂给 M5 校订者（或获授权的更强模型）一包在手、上下文齐全。

数据全部来自既有权威层（只读装配，不造内容）：
  - pin_plan_L360      ：章↔品配对（pin/title/rule/evidence/卷叶）
  - segments ch*.json  ：翻译进度（done/needs_retry/pending·段号）
  - L.354a 试译        ：人工公式译锚点（藏→现代汉语·术语注）
  - drift_review_L379  ：模型退化三型逐段清单（m5_action 在场）
  - term_candidates_L519：本章高频候选（计数·来自已译段）
  - ancestor_crosscheck_L519：祖本勘验状态与分歧计数
  - c80 分品文本       ：祖本品题＋卷次
  - 品专篇（39 篇）    ：路径定位（品旨/科判取窗〔待取〕）

产出：data/translation/tibetan_avatamsaka_dossier_L519.json
Usage:
  hy_py312 python -X utf8 build_chapter_dossier.py
"""

import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PLAN = os.path.join(ROOT, 'data/alignment/tibetan_chinese_pin_plan_L360.json')
SEG_GLOB = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_trilingual_segments*.json')
SHIYI = os.path.join(ROOT, 'data/alignment/tibetan_shiyi_L354a.json')
DRIFT = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_drift_review_L379.json')
TERMS = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_term_candidates_L519.json')
XC = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_ancestor_crosscheck_L519.json')
C80 = os.path.join(ROOT, 'web/demo/data/sutra/c80/p%03d.json')
DOCS = os.path.join(ROOT, 'docs/经学文献/华严经细读')
OUT = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_dossier_L519.json')

CNUM = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八',
        9: '九', 10: '十', 11: '十一', 12: '十二', 13: '十三', 14: '十四',
        15: '十五', 16: '十六', 17: '十七', 18: '十八', 19: '十九', 20: '二十'}


def pin_article(pin):
    """品专篇路径（部号=品号·39 篇 1:1）。"""
    pat = os.path.join(DOCS, '*', '*_第%s部_*.md' % CNUM.get(pin, str(pin)))
    hits = glob.glob(pat)
    return os.path.relpath(hits[0], ROOT) if len(hits) == 1 else (hits or None)


def main():
    plan = json.load(io.open(PLAN, encoding='utf-8'))
    rows = plan.get('chapters') or plan.get('plan') or plan
    if isinstance(rows, dict):
        rows = list(rows.values())
    by_ch = {r.get('tibetan_ch'): r for r in rows if isinstance(r, dict)}
    shiyi = json.load(io.open(SHIYI, encoding='utf-8'))
    drift = json.load(io.open(DRIFT, encoding='utf-8'))
    drift_by_ch = {}
    for s in (drift.get('segments') or []):
        drift_by_ch.setdefault(str(s.get('chapter')), []).append(
            {'seg': s.get('seg'), 'flaw_types': s.get('flaw_types'),
             'm5_action': s.get('m5_action')})
    terms = json.load(io.open(TERMS, encoding='utf-8'))
    xc = json.load(io.open(XC, encoding='utf-8'))
    xc_by_ch = {str(r.get('ch')): r for r in xc.get('chapters', [])}

    segs_by_ch = {}
    for fn in sorted(glob.glob(SEG_GLOB)):
        d = json.load(io.open(fn, encoding='utf-8'))
        ch = (d.get('chapter') or {}).get('tibetan_no')
        if ch:
            segs_by_ch.setdefault(str(ch), []).extend(d.get('segments') or [])

    out = {'id': 'tibetan_avatamsaka_dossier_L519', 'date': '2026-11-22',
           'batch': 'L.519',
           'nature': '〔机器装配〕全部字段回指权威层；空缺如实标〔缺〕，不造内容',
           'style_guide': 'workspace/tibetan-avatamsaka-translation/docs/STYLE-GUIDE-v1.md',
           'chapters': {}}

    for ch in sorted(segs_by_ch, key=int):
        row = by_ch.get(int(ch)) or {}
        segs = segs_by_ch[ch]
        done = [s for s in segs if s.get('status') == 'done']
        pin = row.get('pin')
        # 章级术语候选（本章出现的，按计数排）
        cand = [t for t in (terms.get('candidates', {}).get('trigrams', [])
                            + terms.get('candidates', {}).get('bigrams', []))
                if ch in [str(c) for c in t.get('chapters', [])]]
        xc_rec = xc_by_ch.get(ch) or {}
        d = {
            'tibetan_ch': int(ch),
            'pin': pin,
            'pin_title': xc_rec.get('pin_title') or row.get('pin_title_zh') or '〔缺〕',
            'rule': row.get('rule'),
            'pairing_evidence': row.get('evidence'),
            'derge_vol_folio': '%s %s' % (row.get('vol'), row.get('start_folio')),
            'progress': {'total': len(segs), 'done': len(done),
                         'needs_retry': sum(1 for s in segs if s.get('status') == 'needs_retry'),
                         'pending': sum(1 for s in segs if s.get('status') == 'pending'),
                         'done_seg_nos': [s['no'] for s in done]},
            'trilingual_status': row.get('trilingual_status'),
            'human_trial_L354a': shiyi.get('chapters', {}).get(ch) or '〔缺〕',
            'drift_flags_L379': drift_by_ch.get(ch) or [],
            'term_candidates': [{'bo': t['bo'], 'count': t['count']} for t in cand[:20]],
            'ancestor': {'source': '八十 T10n0279 分品文本 c80/p%03d.json' % pin if pin else None,
                         'crosscheck_status': xc_rec.get('status'),
                         'crosscheck_flags': {
                             'num_token_diffs': len((xc_rec.get('screens') or {}).get('num_tokens', [])),
                             'names_new_only': len((xc_rec.get('screens') or {}).get('names_new_only', [])),
                             'list_density': (xc_rec.get('screens') or {}).get('list_density')},
                         } if pin else {'note': '前段不平行——归 M8 定界后配对'},
            'pin_article': pin_article(pin) if pin else None,
            'pin_article_note': '品旨/来意/宗趣取窗〔待取窗·下批〕',
        }
        out['chapters'][ch] = d

    with io.open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('落盘 %s（%d 章）' % (OUT, len(out['chapters'])))
    for ch, d in out['chapters'].items():
        print('藏章%s ↔ 品%s《%s》 | %s | 进度 %d/%d | 漂移标 %d | 术语候选 %d | 专篇 %s'
              % (ch, d.get('pin'), d.get('pin_title'), d.get('rule'),
                 d['progress']['done'], d['progress']['total'],
                 len(d['drift_flags_L379']), len(d['term_candidates']),
                 '√' if d.get('pin_article') else '缺'))


if __name__ == '__main__':
    main()
