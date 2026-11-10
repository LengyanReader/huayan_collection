#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repair one trilingual segment at a time, with sentence-completeness enforcement.

Modes:
  --clean-only   strip model meta / Tibetan residue / incomplete tail, no model load
  (default)      retranslate one language with a strict prompt, then clean + validate

The data layer keeps the raw model output (`zh_raw` / `en_raw`) and exposes only a
sentence-complete cleaned string in `zh` / `en`. A segment that still ends mid-sentence
is marked `needs_retry` and is NOT counted as done.

Usage:
  python tools/repair_trilingual_segment.py --chapter 16 --seg 1 --clean-only
  python tools/repair_trilingual_segment.py --chapter 16 --seg 2 --lang zh --max-new 800
"""

import argparse
import io
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SEG1 = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_trilingual_segments.json')
SEGCH = os.path.join(ROOT, 'data/translation/tibetan_avatamsaka_trilingual_segments_ch%d.json')
MODEL = 'buddhist-nlp/mitra-qwen35-translate'
LOG = os.path.join(HERE, 'repair_log.txt')

HEADER = (
    "You are an expert translator of classical Asian languages. In your translation, "
    "make sure to use proper IAST diacritics if Sanskrit terms occur, but also translate "
    "Sanskrit terms into English if English is the target language. The translation "
    "should be fluid and accurate."
)


def build_prompt(source, target):
    return (f"{HEADER}\nHere is a piece of text to translate: {source}\n"
            f"Provide only the translation, without any explanation or additional information. "
            f"Provide your translation in {target}:")


_meta = re.compile(r'^\s*(#\s*\d+\.|#\s*(藏文|中文|英文|现代汉语|英语|text|sent_id|sent_counter|sent_subcounter)\s*=|藏文转写\s*$|现代汉语翻译\s*$|英语翻译\s*$)')
_conll = re.compile(r'(?m)^\d+	|# sent_id\s*=|# text\s*=')
_tib = re.compile(r'[\u0F00-\u0FFF]+')


def log(msg):
    line = '[%s] %s' % (time.strftime('%H:%M:%S'), msg)
    with io.open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    print(line)


def is_frame(bo):
    tail = (bo or '').strip()[-40:]
    return ('སྨྲས' in tail) or ('ཞེས' in tail)


def clean(text, lang, frame=False):
    """Return (cleaned, complete, trimmed). Keeps only complete sentences."""
    raw = text or ''
    lines = []
    for line in raw.splitlines():
        if _meta.match(line):
            continue
        lines.append(line)
    t = '\n'.join(lines)
    t = _tib.sub('', t)
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n{3,}', '\n\n', t).strip()
    t = re.sub(r'^["“”\']+|["“”\']+$', '', t).strip()
    if lang == 'en':
        t = re.sub(r';\s*', '; ', t)
    if not t:
        return '', False, bool(raw)

    if lang == 'zh':
        ends = '。！？；' + ('：' if frame else '')
        parts = re.split(r'(?<=[。！？；：])' if frame else r'(?<=[。！？；])', t)
    else:
        ends = '.!?;' + (':' if frame else '')
        parts = re.split(r'(?<=[.!?;:])\s+' if frame else r'(?<=[.!?;])\s+', t)

    complete_parts = [p for p in parts if p.strip() and p.strip()[-1] in ends]
    tail = parts[-1].strip() if parts else ''
    incomplete = bool(tail and tail[-1] not in ends)
    cleaned = ''.join(complete_parts).strip()
    return cleaned, not incomplete and bool(cleaned), cleaned != t.strip()


def validate(text, lang, frame=False):
    if not text:
        return False, 'empty'
    if _tib.search(text):
        return False, 'tibetan residue'
    if _conll.search(text):
        return False, 'CoNLL/Sanskrit annotation'
    ends = ('。！？；' + ('：' if frame else '')) if lang == 'zh' else ('.!?;' + (':' if frame else ''))
    if text.strip()[-1] not in ends:
        return False, 'no terminal punctuation'
    return True, 'ok'


def load_doc(chapter):
    path = SEG1 if chapter == 1 else (SEGCH % chapter)
    if not os.path.exists(path):
        sys.exit('missing %s' % path)
    return path, json.loads(io.open(path, encoding='utf-8').read())


def save_doc(path, doc):
    io.open(path, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=1))


def clean_only(path, doc, seg_no):
    s = next((x for x in doc['segments'] if int(x['no']) == seg_no), None)
    if not s:
        sys.exit('segment %d not found' % seg_no)
    changed = False
    for lang in ('zh', 'en'):
        raw = s.get(lang + '_raw2') or s.get(lang + '_raw') or s.get(lang) or ''
        if not raw:
            continue
        frame = is_frame(s.get('bo'))
        cleaned, complete, trimmed = clean(raw, lang, frame=frame)
        ok, why = validate(cleaned, lang, frame=frame)
        s[lang + '_raw'] = raw
        s[lang] = cleaned
        s[lang + '_clean'] = {
            'method': 'meta+residue+sentence-trim-v1',
            'complete': bool(complete and ok),
            'trimmed': trimmed,
            'validation': why,
            'frame': frame,
            'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        if not (complete and ok):
            s['status'] = 'needs_retry'
            s[lang] = ''
        changed = True
        log('seg%d %s: raw=%d cleaned=%d complete=%s trimmed=%s (%s)' %
            (seg_no, lang, len(raw), len(cleaned), complete and ok, trimmed, why))
    if changed:
        zh_ok = bool(s.get('zh')) and (s.get('zh_clean') or {}).get('complete')
        en_ok = bool(s.get('en')) and (s.get('en_clean') or {}).get('complete')
        if zh_ok and en_ok:
            s['status'] = 'done'
        elif zh_ok or en_ok:
            s['status'] = 'partial'
        save_doc(path, doc)
    return s


def retranslate(path, doc, seg_no, lang, max_new):
    s = next((x for x in doc['segments'] if int(x['no']) == seg_no), None)
    if not s:
        sys.exit('segment %d not found' % seg_no)
    bo = s['bo']
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    torch.set_num_threads(os.cpu_count() or 8)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map='cpu', local_files_only=True)
    model.eval()
    log('model ready %.1fs' % (time.time() - t0))
    prompt = build_prompt(bo, 'Modern Chinese' if lang == 'zh' else 'English')
    msgs = [{'role': 'user', 'content': prompt}]
    inputs = tok.apply_chat_template(msgs, add_generation_prompt=True, return_dict=True,
                                     return_tensors='pt', enable_thinking=False)
    t1 = time.time()
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new, do_sample=False,
                             no_repeat_ngram_size=8, pad_token_id=tok.eos_token_id)
    raw = tok.decode(out[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    frame = is_frame(bo)
    cleaned, complete, trimmed = clean(raw, lang, frame=frame)
    ok, why = validate(cleaned, lang, frame=frame)
    if lang not in s or not s.get(lang + '_raw'):
        s[lang + '_raw'] = s.get(lang) or ''
    s[lang + '_raw2'] = raw
    s[lang] = cleaned
    s[lang + '_meta'] = {
        'model': MODEL, 'engine': 'mitra-qwen35-translate 9B bf16 CPU',
        'revisions': 1, 'schooling': '未校订',
        'prompt_version': 'mitra-official-user-turn-v1',
        'gen_s': round(time.time() - t1, 1),
        'out_tokens': int(out.shape[1] - inputs['input_ids'].shape[1]),
        'max_new': max_new, 'clipped_repeat': False,
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
    }
    bo_chars = len(re.sub(r'\s', '', bo))
    out_chars = len(re.sub(r'\s', '', cleaned))
    ratio = round(out_chars / max(bo_chars, 1), 3)
    bo_units = bo.count('།')
    out_units = len(re.findall(r'[。！？；]' if lang == 'zh' else r'[.!?;]', cleaned))
    coverage = {
        'bo_chars': bo_chars, 'out_chars': out_chars, 'ratio': ratio,
        'bo_shad_units': bo_units, 'out_sentence_units': out_units,
    }
    review = (not (complete and ok)) or (not frame and (out_chars < 8 or ratio < 0.12 or out_units < max(1, bo_units // 2)))
    s[lang + '_clean'] = {
        'method': 'official-mitra-prompt+meta/residue/sentence-trim-v1',
        'complete': bool(complete and ok),
        'trimmed': trimmed,
        'validation': why,
        'coverage': coverage,
        'frame': frame,
        'needs_review': review,
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
    }
    if not (complete and ok):
        s['status'] = 'needs_retry'
        s[lang] = ''
    elif review:
        s['status'] = 'needs_review'
    else:
        s['status'] = 'done'

    save_doc(path, doc)
    log('seg%d %s: raw=%d cleaned=%d complete=%s (%s)' % (seg_no, lang, len(raw), len(cleaned), complete and ok, why))
    log('--- cleaned ---\n%s' % cleaned)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapter', type=int, required=True)
    ap.add_argument('--seg', type=int, required=True)
    ap.add_argument('--lang', choices=['zh', 'en'])
    ap.add_argument('--clean-only', action='store_true')
    ap.add_argument('--max-new', type=int, default=800)
    args = ap.parse_args()
    path, doc = load_doc(args.chapter)
    if args.clean_only:
        clean_only(path, doc, args.seg)
    else:
        if not args.lang:
            sys.exit('--lang required unless --clean-only')
        retranslate(path, doc, args.seg, args.lang, args.max_new)


if __name__ == '__main__':
    main()