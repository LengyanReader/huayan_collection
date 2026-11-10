#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe MITRA's official prompt template on a short Tibetan span.

Usage:
  C:\\Users\\data\\miniconda3\\envs\\hy_py312\\python.exe -X utf8 probe_mitra_official.py
"""

import json
import re
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = 'buddhist-nlp/mitra-qwen35-translate'
SEG = 'data/translation/tibetan_avatamsaka_trilingual_segments_ch16.json'
HEADER = ("You are an expert translator of classical Asian languages. In your translation, "
          "make sure to use proper IAST diacritics if Sanskrit terms occur, but also translate "
          "Sanskrit terms into English if English is the target language. The translation "
          "should be fluid and accurate.")


def main():
    doc = json.load(open(SEG, encoding='utf-8'))
    bo = doc['segments'][0]['bo'][:60]
    target = 'Modern Chinese'
    prompt = (f"{HEADER}\nHere is a piece of text to translate: {bo}\n"
              f"Provide only the translation, without any explanation or additional information. "
              f"Provide your translation in {target}:")
    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    torch.set_num_threads(torch.get_num_threads() or 8)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map='cpu', local_files_only=True)
    model.eval()
    text = tok.apply_chat_template([{'role': 'user', 'content': prompt}],
                                   tokenize=False, add_generation_prompt=True, enable_thinking=False)
    ids = tok(text, return_tensors='pt')
    t0 = time.time()
    with torch.no_grad():
        out = model.generate(**ids, max_new_tokens=60, do_sample=False)
    raw = tok.decode(out[0][ids['input_ids'].shape[1]:], skip_special_tokens=True).strip()
    print('SOURCE:', bo)
    print('RAW:', repr(raw))
    print('CJK:', len(re.findall(r'[\u3400-\u9fff]', raw)), 'TIB:', len(re.findall(r'[\u0F00-\u0FFF]', raw)))
    print('LATIN:', len(re.findall(r'[A-Za-z]', raw)), 'SECONDS:', round(time.time() - t0, 1))


if __name__ == '__main__':
    main()