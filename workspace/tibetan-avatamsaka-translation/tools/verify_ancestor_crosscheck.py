#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""祖本对照勘验器 MVP（L.519）：以汉祖本（八十 T10n0279 分品文本）为「独立译本」，
对已译段做机器初筛——**只出分歧清单，不作对错裁决**（M0.4：机器观察，人定实质）。

原理：31/45 藏章有汉平行品＝同经异译的独立 rendering（M4.10 §3 跨来源互证）。
对齐锚：b 文件 correspondence 的汉开篇锚句（G2.2 已验 bo_open 衔接）→ 祖本全文
定位 → 取「近似窗」（窗长=已译段 zh 总 CJK × 1.5，窗对应为近似，如实标注）。

初筛三面（每面只计数/列差集，裁决标〔待人工裁决〕）：
  A 数词多集差：新译 vs 祖本窗的数词词元计数（十千/萬/俱胝/那由他…）
  B 名目密度：顿号/分号计数差（清单段漏项的粗筛）
  C 专名差集：新译有而祖本窗无的 专名（菩萨/如来/三昧 等后缀词元）

产出：data/translation/tibetan_avatamsaka_ancestor_crosscheck_L519.json
适用范围：rule=差5/差6 已译章（ch14–18；ch1 前段不平行归 M8，如实跳过）。

Usage:
  hy_py312 python -X utf8 verify_ancestor_crosscheck.py [--window-margin 1.5]
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
PLAN = os.path.join(ROOT, 'data/alignment/tibetan_chinese_pin_plan_L360.json')
SEG_GLOB = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_trilingual_segments*.json')
ALIGN_GLOB = os.path.join(ROOT, 'data/alignment/tibetan_zhuhuju_b?.json')
C80 = os.path.join(ROOT, 'web/demo/data/sutra/c80/p%03d.json')
OUT = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_ancestor_crosscheck_L519.json')

CJK = re.compile(r'[\u3400-\u9fff]')
NUM_TOKEN = re.compile(r'(十千|俱胝|那由他|阿僧祇|恒河沙|百亿|千亿|万亿|無量|无数|百万|千万|[一二三四五六七八九十百千萬億]+)')
NAME_TOKEN = re.compile(r'([\u3400-\u9fff]{2,8}?)(菩薩|菩萨|如來|如来|天子|天女|三昧|夜叉|天王|比丘|佛)')
HEADER = re.compile(r'【[^】]*】')


def cjk_count(s):
    return len(CJK.findall(s or ''))


def load_ancestor(pin):
    """祖本全文（去品题头）＋逐卷结构。"""
    d = json.load(io.open(C80 % pin, encoding='utf-8'))
    paras = []
    for seg in d.get('segs') or []:
        for p in (seg.get('paras') or []):
            paras.append(HEADER.sub('', p))
    return {'title': d.get('title'), 'text': ''.join(paras),
            'vols': [seg.get('v') for seg in (d.get('segs') or [])]}


def load_align_anchor(ch):
    for fn in sorted(glob.glob(ALIGN_GLOB)):
        d = json.load(io.open(fn, encoding='utf-8'))
        chs = d.get('chapters') or []
        vals = chs.values() if isinstance(chs, dict) else chs
        for v in vals:
            if isinstance(v, dict) and v.get('tibetan_ch') == ch:
                anchor = v.get('zh80_open') or ''
                corr = v.get('correspondence') or []
                if not anchor and corr and len(corr[0]) > 1:
                    a = corr[0][1] or ''
                    anchor = a.strip('「」')
                return {'src': os.path.basename(fn), 'anchor': anchor,
                        'correspondence': corr}
    return None


def screens(new_zh, anc_win):
    out = {}
    # A 数词多集
    n_num = collections.Counter(NUM_TOKEN.findall(new_zh or ''))
    a_num = collections.Counter(NUM_TOKEN.findall(anc_win or ''))
    keys = set(n_num) | set(a_num)
    out['num_tokens'] = [{'tok': k, 'new': n_num.get(k, 0), 'anc': a_num.get(k, 0)}
                         for k in sorted(keys, key=lambda x: -(n_num[x] + a_num[x]))
                         if n_num.get(k, 0) != a_num.get(k, 0)]
    # B 名目密度
    out['list_density'] = {'new_dun': (new_zh or '').count('、'),
                           'anc_dun': (anc_win or '').count('、'),
                           'new_semi': (new_zh or '').count('；'),
                           'anc_semi': (anc_win or '').count('；')}
    # C 专名差集
    n_names = set(NAME_TOKEN.findall(new_zh or ''))
    a_names = set(NAME_TOKEN.findall(anc_win or ''))
    out['names_new_only'] = sorted('%s%s' % t for t in (n_names - a_names))
    out['names_anc_only'] = sorted('%s%s' % t for t in (a_names - n_names))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--window-margin', type=float, default=1.5)
    args = ap.parse_args()

    plan = json.load(io.open(PLAN, encoding='utf-8'))
    rows = plan.get('chapters') or plan.get('plan') or plan
    if isinstance(rows, dict):
        rows = list(rows.values())
    by_ch = {r.get('tibetan_ch'): r for r in rows if isinstance(r, dict)}

    segs_by_ch = {}
    for fn in sorted(glob.glob(SEG_GLOB)):
        d = json.load(io.open(fn, encoding='utf-8'))
        ch = (d.get('chapter') or {}).get('tibetan_no')
        if ch:
            segs_by_ch.setdefault(ch, []).extend(d.get('segments') or [])

    out = {'id': 'tibetan_avatamsaka_ancestor_crosscheck_L519',
           'date': '2026-11-22', 'batch': 'L.519',
           'nature': '〔机器初筛〕只列分歧不作裁决；窗对应为近似（窗长=已译 zh CJK×%.1f）；'
                     '裁决〔待人工〕' % args.window_margin,
           'chapters': []}
    for ch in sorted(segs_by_ch):
        row = by_ch.get(ch) or {}
        rule = row.get('rule') or ''
        if rule not in ('差5', '差6'):
            out['chapters'].append({'ch': ch, 'rule': rule, 'status': 'skip',
                                    'note': '前段不平行/藏独有——归 M7/M8 专批，不配对'})
            continue
        pin = row.get('pin')
        anc = load_ancestor(pin)
        align = load_align_anchor(ch)
        done = [s for s in segs_by_ch[ch] if s.get('status') == 'done']
        new_zh = '\n'.join(s.get('zh') or '' for s in done)
        text = anc['text']
        anchor = (align or {}).get('anchor') or ''
        # 锚两级回退：全锚（可能带品题前缀）→ 正文锚（「爾時」起）
        pos = text.find(anchor) if anchor else -1
        anchor_form = 'full' if pos >= 0 else ''
        if pos < 0 and anchor:
            k = anchor.find('爾時')
            if k > 0:
                body = anchor[k:]
                pos = text.find(body)
                anchor_form = 'body(爾時起)' if pos >= 0 else ''
                anchor = body
        rec = {'ch': ch, 'pin': pin, 'pin_title': anc['title'], 'rule': rule,
               'align_src': (align or {}).get('src'),
               'anchor': anchor[:40], 'anchor_form': anchor_form,
               'ancestor_vols': anc['vols'],
               'done_segs': [s['no'] for s in done],
               'new_zh_cjk': cjk_count(new_zh)}
        if pos < 0:
            rec.update({'status': 'anchor-miss',
                        'note': '锚句未命中祖本全文〔待查〕——correspondence 措辞与分品文本或异'})
        else:
            win = max(int(cjk_count(new_zh) * args.window_margin), 300)
            anc_win = text[pos:pos + win]
            rec.update({'status': 'screened', 'anchor_pos': pos,
                        'window_len': win,
                        'screens': screens(new_zh, anc_win)})
        out['chapters'].append(rec)

    with io.open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('落盘 %s' % OUT)
    for r in out['chapters']:
        if r.get('status') == 'screened':
            s = r['screens']
            print('ch%s(品%s %s)：数词差 %d 项·顿号 %d↔%d·新译独有专名 %d %s'
                  % (r['ch'], r['pin'], r['pin_title'], len(s['num_tokens']),
                     s['list_density']['new_dun'], s['list_density']['anc_dun'],
                     len(s['names_new_only']), s['names_new_only'][:6]))
        else:
            print('ch%s：%s (%s)' % (r['ch'], r.get('status'), r.get('note', '')))


if __name__ == '__main__':
    main()
