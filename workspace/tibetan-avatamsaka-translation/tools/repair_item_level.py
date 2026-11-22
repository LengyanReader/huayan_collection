#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""条目级修复器（L.519）：把「子单元仍过长/截断」的段再降到条目（item）粒度，
单次模型装载逐条目翻译 zh+en，全部条目完成后按规则拼装回子单元与段。

背景：ch18 seg5 子单元级重试两度 12 字截断（2026-11-14／11-21），台账结论
「不能再靠整段/术语 prompt 盲跑，需条目级」。本器是 repair_subunit 的下一层：
- 切分：shad（།）优先；无 shad 的长句按 --joint 显式句法接点切（接点留痕）；
- 每条目独立生成（官方 prompt＋术语表注入，复用 repair_trilingual_segment）；
- 逐条目留痕 bo/zh/en/raw/clean（含 gen_s——补子单元线机时台账缺口）；
- 不覆盖历史：子单元旧 zh_clean 存入 prev_attempt（双轨可回溯）；
- 拼装规则（M4.3 合并留痕）：shad 清单条目→「，」连接、句号收尾；en 空格
  连接。规则记入 *_compose 供 M5 校订。

Usage:
  python repair_item_level.py --chapter 18 --seg 5 \
    --joint "མཐོང་ནས" --glossary "པོག་རེ=靠墊;..." [--only lang] [--dry-run]
"""

import argparse
import os
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
        f.write(line.rstrip() + '\n')  # 行尾 rstrip——git diff --check 卫生（:: + 空 cleaned 会留尾空格）
    try:
        print(line, flush=True)
    except Exception:
        pass  # cp1252 控制台打印藏文可失败——写日志已先行，进程不可中断（L.512 教训）


def split_items(bo, joints):
    """shad 优先切；无 shad（或切后仍单条）按 joints 字面接点切。接点留在前一条目。"""
    bo = bo or ''
    parts = [p for p in bo.split('།') if p.strip()]
    if len(parts) > 1:
        return [(p.strip() + '།') for p in parts if p.strip()], 'shad'
    for j in joints or []:
        k = bo.find(j)
        if k > 0 and k + len(j) < len(bo):
            a = bo[:k + len(j)].strip()
            b = bo[k + len(j):].strip().lstrip('་ ')  # 剥除接点后游离 tsheg/空白
            return [x for x in (a, b) if x], 'joint:' + j
    return [bo.strip()], 'whole'


def compose_zh(items):
    """条目→「，」连接、句号收尾；中间条目尾标点剥除。"""
    vals = []
    for it in items:
        v = (it.get('zh') or '').strip()
        if v:
            vals.append(v)
    if not vals:
        return ''
    for i in range(len(vals) - 1):
        vals[i] = vals[i].rstrip('，。；：、')
    return '，'.join(vals).rstrip('，。；') + '。'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapter', type=int, required=True)
    ap.add_argument('--seg', type=int, required=True)
    ap.add_argument('--joint', action='append', default=[],
                    help='无 shad 长句的字面接点（可多次；接点保留于前条目）')
    ap.add_argument('--glossary', default='', help='术语表（注入官方 prompt）')
    ap.add_argument('--glossary-src', default='L.354a术语表+11-14供物表',
                    help='术语来源登记')
    ap.add_argument('--only', choices=['zh', 'en'], default='', help='只译单语（调试）')
    ap.add_argument('--subunit', type=int, default=0, help='只处理指定子单元（1 起·调试探针）')
    ap.add_argument('--item', type=int, default=0, help='只处理子单元内指定条目（1 起·调试探针）')
    ap.add_argument('--sample', action='store_true',
                    help='采样解码（temperature/top_p 扰动）——治贪心退化路径')
    ap.add_argument('--temperature', type=float, default=0.8)
    ap.add_argument('--max-new', type=int, default=150)
    ap.add_argument('--time-limit', type=int, default=300, help='单条目墙钟上限（秒）')
    ap.add_argument('--dry-run', action='store_true', help='只打印切分计划不装载模型')
    args = ap.parse_args()

    path, doc = R.load_doc(args.chapter)
    s = next((x for x in doc['segments'] if int(x['no']) == args.seg), None)
    if not s:
        sys.exit('segment not found')
    subs = s.get('subunits') or [{'bo': s['bo']}]

    # ── 切分计划（先全部算好；条目结构挂 subunit['items']）──
    for si, sub in enumerate(subs, 1):
        items, how = split_items(sub.get('bo'), args.joint)
        sub['items'] = [{'bo': b} for b in items]
        log('切分计划 sub%d (%s): %d 条目' % (si, how, len(items)))
        for k, b in enumerate(items, 1):
            log('   item%d (%d chars): %s' % (k, len(b), b[:56]))
    if args.dry_run:
        return

    langs = [args.only] if args.only else ['zh', 'en']
    need = [si for si, sub in enumerate(subs, 1)
            if any(not it.get(l) for it in sub['items'] for l in langs)]
    if not need:
        log('seg%d 条目已齐，无需生成' % args.seg)
        return

    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, dtype=torch.bfloat16, device_map='cpu',
        local_files_only=True, low_cpu_mem_usage=True)
    model.eval()
    log('模型装载完成 (%.0fs)，开始条目生成' % (time.time() - t0))

    gen_s_total = 0.0
    for si in need:
        if args.subunit and si != args.subunit:
            continue
        sub = subs[si - 1]
        for ii, it in enumerate(sub['items'], 1):
            if args.item and ii != args.item:
                continue
            for lang in langs:
                if it.get(lang):
                    continue
                prompt = R.build_prompt(it['bo'], 'Modern Chinese' if lang == 'zh' else 'English')
                if args.glossary:
                    prompt = prompt.replace(
                        'Provide only the translation',
                        'Use this terminology consistently: ' + args.glossary
                        + ' Provide only the translation')
                inputs = tok.apply_chat_template(
                    [{'role': 'user', 'content': prompt}],
                    add_generation_prompt=True, return_dict=True,
                    return_tensors='pt', enable_thinking=False)
                t1 = time.time()

                class _Limit(StoppingCriteria):
                    def __call__(self, input_ids, scores, **kwargs):
                        return (time.time() - t1) > args.time_limit

                with torch.no_grad():
                    out = model.generate(
                        **inputs, max_new_tokens=args.max_new,
                        do_sample=bool(args.sample),
                        temperature=args.temperature if args.sample else None,
                        top_p=0.9 if args.sample else None,
                        no_repeat_ngram_size=8, pad_token_id=tok.eos_token_id,
                        stopping_criteria=StoppingCriteriaList([_Limit()]))
                gen_s = round(time.time() - t1, 1)
                gen_s_total += gen_s
                raw = tok.decode(out[0][inputs['input_ids'].shape[1]:],
                                 skip_special_tokens=True)
                cleaned, complete, trimmed = R.clean(raw, lang)
                ok, why = R.validate(cleaned, lang)
                it[lang] = cleaned if (complete and ok) else ''
                it[lang + '_raw'] = raw
                it[lang + '_clean'] = {
                    'method': 'item-level-official-prompt', 'complete': bool(complete and ok),
                    'trimmed': trimmed, 'validation': why, 'gen_s': gen_s,
                    'decode': ('sample t=%.1f' % args.temperature) if args.sample else 'greedy',
                    'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
                }
                log('sub%d item %s: raw=%d cleaned=%d complete=%s (%s) gen=%.0fs :: %s'
                    % (si, lang, len(raw), len(cleaned), complete and ok, why, gen_s, cleaned[:60]))
        # ── 子单元拼装（规则留痕；旧 zh_clean 存 prev_attempt 不覆盖历史）──
        its = sub['items']
        zh_vals = [x.get('zh') for x in its]
        en_vals = [x.get('en') for x in its]
        if all(zh_vals):
            sub['zh'] = compose_zh(its) if len(its) > 1 else zh_vals[0]
            sub['zh_compose'] = 'shad-list→，。' if len(its) > 1 else 'direct'
        if all(en_vals):
            sub['en'] = ' '.join(en_vals)
            sub['en_compose'] = 'space-join' if len(its) > 1 else 'direct'
        prev = sub.get('zh_clean') or {}
        zc = dict(prev) if prev.get('method') == 'item-level-official-prompt' else {}
        if prev and prev.get('method') != 'item-level-official-prompt':
            zc['prev_attempt'] = prev
        zc.update({'method': 'item-level-official-prompt', 'items': len(its),
                   'ts': time.strftime('%Y-%m-%dT%H:%M:%S')})
        sub['zh_clean'] = zc
        s['subunits'] = subs

    # ── 段级拼装：全部子单元双语齐才置 done ──
    all_ok = all(u.get('zh') and u.get('en') for u in subs)
    if all_ok:
        s['zh'] = '\n'.join(u['zh'] for u in subs)
        s['en'] = ' '.join(u['en'] for u in subs)
        s['status'] = 'done'
    meta = {'model': MODEL, 'engine': 'mitra-qwen35-translate 9B bf16 CPU',
            'method': 'item-level-official-prompt', 'glossary_src': args.glossary_src,
            'gen_s_total': round(gen_s_total, 1),
            'ts': time.strftime('%Y-%m-%dT%H:%M:%S')}
    if all_ok or gen_s_total:
        s['zh_meta'] = dict(s.get('zh_meta') or {}, **meta)
        s['en_meta'] = dict(s.get('en_meta') or {}, **meta)
    R.save_doc(path, doc)
    log('seg%d 条目级完成：status=%s gen_s_total=%.1fs' % (args.seg, s['status'], gen_s_total))


if __name__ == '__main__':
    main()
