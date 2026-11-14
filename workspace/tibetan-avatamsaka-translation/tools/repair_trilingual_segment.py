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
    tail = (bo or '').strip()[-25:]
    return bool(re.search(r'(སྨྲས་སོ|ཞེས་སོ|སྨྲས་པ|ཞེས་པ)\s*།?\s*།?\s*$', tail))


TIB_UNITS = {'གཅིག': 1, 'གཉིས': 2, 'གསུམ': 3, 'བཞི': 4, 'ལྔ': 5,
             'དྲུག': 6, 'བདུན': 7, 'བརྒྱད': 8, 'དགུ': 9}


def tib_num(s):
    tens = 0
    if 'ཉི་ཤུ' in s or 'ཉེར་' in s:
        tens = 20
    elif 'སུམ་ཅུ' in s:
        tens = 30
    elif 'བཅུ' in s or 'བཅྭོ' in s:
        tens = 10
    unit = next((v for k, v in TIB_UNITS.items() if k in s), 0)
    return tens + unit if tens else unit


def cn_num(n):
    d = '〇一二三四五六七八九'
    if 0 < n < 10:
        return d[n]
    if n == 10:
        return '十'
    if 10 < n < 20:
        return '十' + d[n % 10]
    if n % 10 == 0 and n < 100:
        return d[n // 10] + '十'
    if n < 100:
        return d[n // 10] + '十' + d[n % 10]
    return str(n)


TITLE_RE = re.compile(r'^(.*?བམ་པོ་[^།]*།)\s*(.*)$', re.S)


def split_title(bo):
    m = TITLE_RE.match(bo or '')
    return (m.group(1), m.group(2)) if m else ('', bo or '')


def split_subunits(bo, n=2):
    pos = [i + 1 for i, c in enumerate(bo or '') if c == '།']
    if not pos:
        return [bo or '']
    mid = len(bo) // 2
    idx = min(pos, key=lambda p: abs(p - mid))
    parts = [(bo or '')[:idx].strip(), (bo or '')[idx:].strip()]
    return [p for p in parts if p]


def is_title_block(bo):
    title, body = split_title(bo)
    return bool(title and not body.strip())


def title_block_translation(bo):
    m = re.search(r'བམ་པོ་([^།]+)', bo or '')
    n = tib_num(m.group(1)) if m else 0
    zh = '《大方廣佛華嚴經》' + (('第%s包' % cn_num(n)) if n else '')
    en = 'The Mahāvaipulya Sūtra, Buddhāvataṃsaka' + ((', bam po %d' % n) if n else '') + '.'
    return zh, en, n


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
        t = re.sub(r'([!?])(?=[A-Z])', r'\1 ', t)
        if t.count('"') % 2 == 1:
            t = t.replace('"', '')
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
    if s.get('merged_into'):
        return s
    if is_title_block(s.get('bo')):
        zh, en, n = title_block_translation(s['bo'])
        s['kind'] = 'title'
        s['zh'] = zh
        s['en'] = en
        for lang in ('zh', 'en'):
            s[lang + '_meta'] = {
                'model': 'none', 'engine': 'canonical-title-block',
                'method': 'title-formula+bam-po', 'prompt_version': 'none',
                'bam_po': n, 'schooling': '规范译名', 'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
            }
            s[lang + '_clean'] = {
                'method': 'canonical-title-block', 'complete': True,
                'trimmed': False, 'validation': 'ok', 'frame': False,
                'needs_review': False, 'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
            }
        s['status'] = 'done'
        save_doc(path, doc)
        log('seg%d title-block: bam po %s -> %s / %s' % (seg_no, n, zh, en))
        return s
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
        bo = s.get('bo') or ''
        bo_chars = len(re.sub(r'\s', '', bo))
        out_chars = len(re.sub(r'\s', '', cleaned))
        ratio = round(out_chars / max(bo_chars, 1), 3)
        bo_units = bo.count('།')
        out_units = len(re.findall(r'[。！？；]' if lang == 'zh' else r'[.!?;]', cleaned))
        merged = (s.get('window') or [0, 0])[1] > s['no']
        verse = ('། །' in (s.get('bo') or ''))
        review = (not (complete and ok)) or (not frame and (out_chars < 8 or ratio < 0.12 or ((not merged and not verse) and out_units < max(1, bo_units // 2))))
        s[lang + '_clean'] = {
            'method': 'meta+residue+sentence-trim-v1',
            'complete': bool(complete and ok),
            'trimmed': trimmed,
            'validation': why,
            'frame': frame,
            'coverage': {'bo_chars': bo_chars, 'out_chars': out_chars, 'ratio': ratio,
                         'bo_shad_units': bo_units, 'out_sentence_units': out_units},
            'needs_review': review,
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
        review = bool((s.get('zh_clean') or {}).get('needs_review') or (s.get('en_clean') or {}).get('needs_review'))
        if review:
            s['status'] = 'needs_review'
        elif zh_ok and en_ok:
            s['status'] = 'done'
        elif zh_ok or en_ok:
            s['status'] = 'partial'
        save_doc(path, doc)
    return s


def compose_title(s):
    title, _ = split_title(s.get('bo') or '')
    tzh, ten, n = title_block_translation(title)
    s['zh'] = tzh + ((' ' + s['body_zh']) if s.get('body_zh') else '')
    s['en'] = ten + ((' ' + s['body_en']) if s.get('body_en') else '')
    s['kind'] = 'title'
    s['bam_po'] = n


def retranslate(path, doc, seg_no, lang, max_new, window=1, time_limit=900):
    s = next((x for x in doc['segments'] if int(x['no']) == seg_no), None)
    if not s:
        sys.exit('segment %d not found' % seg_no)
    idx = doc['segments'].index(s)
    win = doc['segments'][idx:idx + max(1, window)]
    bo = '\n'.join(x['bo'] for x in win) if len(win) > 1 else s['bo']
    s['window'] = [seg_no, win[-1]['no']]
    s['bo_merged'] = bo
    title_prefix, body_text = split_title(bo)
    source = body_text if title_prefix else bo
    if len(win) == 1 and is_title_block(bo):
        zh, en, n = title_block_translation(bo)
        s['kind'] = 'title'
        s['zh'] = zh
        s['en'] = en
        for lang in ('zh', 'en'):
            s[lang + '_meta'] = {
                'model': 'none', 'engine': 'canonical-title-block',
                'method': 'title-formula+bam-po', 'prompt_version': 'none',
                'bam_po': n, 'schooling': '规范译名', 'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
            }
            s[lang + '_clean'] = {
                'method': 'canonical-title-block', 'complete': True,
                'trimmed': False, 'validation': 'ok', 'frame': False,
                'needs_review': False, 'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
            }
        s['status'] = 'done'
        save_doc(path, doc)
        log('seg%d title-block: bam po %s -> %s / %s' % (seg_no, n, zh, en))
        return
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    torch.set_num_threads(os.cpu_count() or 8)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map='cpu', local_files_only=True)
    model.eval()
    log('model ready %.1fs' % (time.time() - t0))
    prompt = build_prompt(source, 'Modern Chinese' if lang == 'zh' else 'English')
    msgs = [{'role': 'user', 'content': prompt}]
    inputs = tok.apply_chat_template(msgs, add_generation_prompt=True, return_dict=True,
                                     return_tensors='pt', enable_thinking=False)
    t1 = time.time()

    class _TimeLimit(StoppingCriteria):
        def __init__(self, start, limit):
            self.start, self.limit = start, limit

        def __call__(self, input_ids, scores, **kwargs):
            return (time.time() - self.start) > self.limit

    max_new = min(max_new, 400)
    criteria = StoppingCriteriaList([_TimeLimit(t1, time_limit)])
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new, do_sample=False,
                             no_repeat_ngram_size=8, pad_token_id=tok.eos_token_id,
                             stopping_criteria=criteria)
    raw = tok.decode(out[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    frame = is_frame(source)
    cleaned, complete, trimmed = clean(raw, lang, frame=frame)
    ok, why = validate(cleaned, lang, frame=frame)
    if lang not in s or not s.get(lang + '_raw'):
        s[lang + '_raw'] = s.get(lang) or ''
    s[lang + '_raw2'] = raw
    if title_prefix:
        s['body_' + lang] = cleaned
        if cleaned:
            compose_title(s)
    else:
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
    bo_chars = len(re.sub(r'\s', '', source))
    out_chars = len(re.sub(r'\s', '', cleaned))
    ratio = round(out_chars / max(bo_chars, 1), 3)
    bo_units = source.count('།')
    out_units = len(re.findall(r'[。！？；]' if lang == 'zh' else r'[.!?;]', cleaned))
    coverage = {
        'bo_chars': bo_chars, 'out_chars': out_chars, 'ratio': ratio,
        'bo_shad_units': bo_units, 'out_sentence_units': out_units,
    }
    merged = len(win) > 1
    verse = ('། །' in source)
    review = (not (complete and ok)) or (not frame and (out_chars < 8 or ratio < 0.12 or ((not merged and not verse) and out_units < max(1, bo_units // 2))))
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
        if title_prefix:
            s['body_' + lang] = ''
            compose_title(s)
        else:
            s[lang] = ''
    elif review:
        s['status'] = 'needs_review'
    else:
        zh_src = s.get('body_zh') if title_prefix else s.get('zh')
        en_src = s.get('body_en') if title_prefix else s.get('en')
        zh_ok = bool(zh_src) and (s.get('zh_clean') or {}).get('complete')
        en_ok = bool(en_src) and (s.get('en_clean') or {}).get('complete')
        s['status'] = 'done' if (zh_ok and en_ok) else 'partial'

    if len(win) > 1:
        for x in win[1:]:
            x['status'] = s['status']
            x['merged_into'] = seg_no
            x['zh'] = ''
            x['en'] = ''
            x['zh_clean'] = {'method': 'merged-into', 'complete': True,
                             'merged_into': seg_no, 'needs_review': False}
            x['en_clean'] = {'method': 'merged-into', 'complete': True,
                             'merged_into': seg_no, 'needs_review': False}
    save_doc(path, doc)
    log('seg%d %s: window=%d raw=%d cleaned=%d complete=%s (%s)' %
        (seg_no, lang, len(win), len(raw), len(cleaned), complete and ok, why))
    log('--- cleaned ---\n%s' % cleaned)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapter', type=int, required=True)
    ap.add_argument('--seg', type=int, required=True)
    ap.add_argument('--lang', choices=['zh', 'en'])
    ap.add_argument('--clean-only', action='store_true')
    ap.add_argument('--max-new', type=int, default=800)
    ap.add_argument('--window', type=int, default=1, help='合并 1–N 段为一个译句单元（偈颂跨行）')
    ap.add_argument('--time-limit', type=int, default=900, help='单次生成墙钟上限（秒）')
    args = ap.parse_args()
    path, doc = load_doc(args.chapter)
    if args.clean_only:
        clean_only(path, doc, args.seg)
    else:
        if not args.lang:
            sys.exit('--lang required unless --clean-only')
        retranslate(path, doc, args.seg, args.lang, args.max_new, args.window, args.time_limit)


if __name__ == '__main__':
    main()
