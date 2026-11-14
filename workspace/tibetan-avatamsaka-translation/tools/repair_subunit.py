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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapter', type=int, required=True)
    ap.add_argument('--seg', type=int, required=True)
    ap.add_argument('--part', type=int, required=True)
    ap.add_argument('--lang', choices=['zh', 'en'], required=True)
    ap.add_argument('--max-new', type=int, default=250)
    args = ap.parse_args()

    path, doc = R.load_doc(args.chapter)
    s = next((x for x in doc['segments'] if int(x['no']) == args.seg), None)
    if not s:
        sys.exit('segment not found')
    parts = s.get('subunits')
    if not parts:
        parts = [{'bo': x} for x in R.split_subunits(s['bo'])]
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
            return (time.time() - t0) > 900

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