#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate one sub-unit of an over-long segment, then compose when all parts are complete.

Usage:
  python repair_subunit.py --chapter 18 --seg 3 --part 1 --lang zh --max-new 250
"""

import argparse
import json
import os
import re
import sys
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repair_trilingual_segment as R

MODEL = 'buddhist-nlp/mitra-qwen35-translate'
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repair_log.txt')


def log(msg):
    line = '[%s] %s' % (time.strftime('%H:%M:%S'), msg)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    print(line)


def split_n(bo, n):
    shads = [i + 1 for i, c in enumerate(bo or '') if c == '།']
    if n < 2 or not shads:
        return [bo or '']
    bounds = []
    for k in range(1, n):
        t = len(bo) * k // n
        b = min(shads, key=lambda p: abs(p - t))
        if b not in bounds:
            bounds.append(b)
    bounds.sort()
    cuts = [0] + bounds + [len(bo)]
    return [bo[cuts[i]:cuts[i + 1]].strip() for i in range(len(cuts) - 1) if bo[cuts[i]:cuts[i + 1]].strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapter', type=int, required=True)
    ap.add_argument('--seg', type=int, required=True)
    ap.add_argument('--part', type=int, required=True)
    ap.add_argument('--lang', choices=['zh', 'en'], required=True)
    ap.add_argument('--max-new', type=int, default=250)
    ap.add_argument('--parts', type=int, default=0, help='分几段（0=沿用/2）')
    ap.add_argument('--keep-zh', action='store_true', help='仅重译英文，保留已有中文')
    ap.add_argument('--time-limit', type=int, default=900, help='单次生成墙钟上限（秒）')
    args = ap.parse_args()

    path, doc = R.load_doc(args.chapter)
    s = next((x for x in doc['segments'] if int(x['no']) == args.seg), None)
    if not s:
        sys.exit('segment not found')
    if args.keep_zh:
        parts = s.get('en_parts')
        if not parts:
            parts = [{'bo': x} for x in split_n(s['bo'], args.parts or 3)]
            s['en_parts'] = parts
    else:
        parts = s.get('subunits')
        if not parts:
            n = args.parts or 2
            splitter = (lambda b: split_n(b, n)) if n > 2 else R.split_subunits
            parts = [{'bo': x} for x in splitter(s['bo'])]
            s['subunits'] = parts
    if args.part < 1 or args.part > len(parts):
        sys.exit('bad part')
    part = parts[args.part - 1]
    source = part['bo']

    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map='cpu', local_files_only=True)
    model.eval()
    prompt = R.build_prompt(source, 'Modern Chinese' if args.lang == 'zh' else 'English')
    inputs = tok.apply_chat_template([{'role': 'user', 'content': prompt}],
                                     add_generation_prompt=True, return_dict=True,
                                     return_tensors='pt', enable_thinking=False)

    t0 = time.time()

    class _Limit(StoppingCriteria):
        def __call__(self, input_ids, scores, **kwargs):
            return (time.time() - t0) > args.time_limit

    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=min(args.max_new, 300), do_sample=False,
                             no_repeat_ngram_size=8, pad_token_id=tok.eos_token_id,
                             stopping_criteria=StoppingCriteriaList([_Limit()]))
    raw = tok.decode(out[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    cleaned, complete, trimmed = R.clean(raw, args.lang)
    ok, why = R.validate(cleaned, args.lang)
    part[args.lang] = cleaned if (complete and ok) else ''
    part[args.lang + '_raw'] = raw
    part[args.lang + '_clean'] = {
        'method': 'subunit-official-prompt', 'complete': bool(complete and ok),
        'trimmed': trimmed, 'validation': why, 'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
    }
    if args.keep_zh:
        all_ok = all(p.get('en') for p in parts)
        s['en'] = ' '.join(p['en'] for p in parts) if all_ok else ''
        if s.get('zh') and all_ok:
            s['status'] = 'done'
        else:
            s['status'] = 'needs_retry' if not (complete and ok) else 'partial'
        s['en_parts'] = parts
    else:
        all_ok = all(p.get('zh') and p.get('en') for p in parts)
        s['zh'] = '\n'.join(p['zh'] for p in parts) if all_ok else ''
        s['en'] = ' '.join(p['en'] for p in parts) if all_ok else ''
        s['status'] = 'done' if all_ok else ('needs_retry' if not (complete and ok) else 'partial')
        s['subunits'] = parts
    R.save_doc(path, doc)
    log('seg%d part%d %s: raw=%d cleaned=%d complete=%s (%s); composed=%s' %
        (args.seg, args.part, args.lang, len(raw), len(cleaned), complete and ok, why, all_ok))
    log('--- cleaned ---\n%s' % cleaned)


if __name__ == '__main__':
    main()