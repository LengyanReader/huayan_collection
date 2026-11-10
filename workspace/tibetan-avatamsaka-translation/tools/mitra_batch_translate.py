# -*- coding: utf-8 -*-
"""L.360 MITRA 三语批量试译（可续跑 · 单进程常驻 · 复读截断）。

读取 data/translation/tibetan_avatamsaka_trilingual_segments.json，
对 status != done 的段依次做 藏→汉 / 藏→英 试译，每段译完即落盘（断点可续）。

工程口径（实测所得，勿随意改）：
- CPU-only（8 物理核 / 32GB）：**必须** bf16；fp32 权重 ~35GB 会 OOM
- 加载 ~800s，生成 ~0.2 tok/s，故单次进程只加载一次、批量处理全部待译段
- 模型在长输出上会复读（冒烟实测：同句循环），故 no_repeat_ngram_size=8 + 译后周期截断
- 产物一律视为〔模型译·未校订〕，不作对勘结论
- L.380：--max-segs 默认 6（里程碑单元，链逐批续挂）；--max-new 0=按段长自适应 200–600
  （句末感知长段需要更大输出窗；meta 记 max_new 可回查）

用法：
  C:\\Users\\data\\miniconda3\\envs\\hy_py312\\python.exe -X utf8 mitra_batch_translate.py
"""
import argparse, glob, io, json, os, re, sys, time

SEG1 = 'data/translation/tibetan_avatamsaka_trilingual_segments.json'
SEGCH = 'data/translation/tibetan_avatamsaka_trilingual_segments_ch%d.json'
SEGG = 'data/translation/tibetan_avatamsaka_trilingual_segments*.json'
LOG = os.path.join(os.path.dirname(__file__), 'mitra_batch_log.txt')
MODEL = "buddhist-nlp/mitra-qwen35-translate"
MAX_NEW = 200

PROMPT_ZH = ("You are an expert translator of classical Buddhist texts. "
             "Translate the following Classical Tibetan text into Modern Chinese. "
             "The translation should be fluid and accurate. Provide your answer in Modern Chinese:\n\n")
PROMPT_EN = ("You are an expert translator of classical Buddhist texts. "
             "Translate the following Classical Tibetan text into English. "
             "Use established English Buddhist terminology. Provide your answer in English:\n\n")

_out = io.open(LOG, 'a', encoding='utf-8', buffering=1)
def log(msg):
    line = '[%s] %s' % (time.strftime('%H:%M:%S'), msg)
    _out.write(line + '\n')
    print(line)

def dedup_truncate(text):
    """周期复读截断：找出最早出现的、连续重复≥2 次的周期片段并截断。"""
    t = text.strip()
    n = len(t)
    for period in range(6, min(n // 2, 60)):
        m = re.search(r'(?P<c>.{%d})(?P=c)(?P=c)' % period, t, re.S)
        if m:
            cut = m.start() + period * 2
            return t[:cut].rstrip(), True
    return t, False

def main():
    t0 = time.time()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapter', type=int, default=None, help='只译该藏章的分文件；缺省=聚合全部段文件')
    ap.add_argument('--max-new', type=int, default=0,
                    help='0=按段长自适应 min(600,max(200,len(bo)))（L.380 句末感知长段需更大输出窗）')
    ap.add_argument('--max-segs', type=int, default=6, help='每批最多译段数（里程碑单元；0=不限）')
    args = ap.parse_args()
    files = [f.replace('\\', '/') for f in sorted(glob.glob(SEGG))]  # Windows glob 混分隔符（translation\file）→ 归一后再比对
    if args.chapter is not None:
        want = SEG1 if args.chapter == 1 else (SEGCH % args.chapter)
        files = [f for f in files if f == want]
        if not files:
            sys.exit('FATAL: 藏章%d 的 segments 数据层不存在（先跑 extract_trilingual_segments.py --chapter %d）'
                     % (args.chapter, args.chapter))
    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    log('tokenizer ready %.1fs' % (time.time() - t0))
    t1 = time.time()
    torch.set_num_threads(os.cpu_count() or 8)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, dtype=torch.bfloat16, device_map="cpu", local_files_only=True)
    model.eval()
    log('model ready %.1fs dtype=%s threads=%d' % (time.time() - t1, model.dtype, torch.get_num_threads()))

    for path in files:
        doc = json.loads(io.open(path, encoding='utf-8').read())
        todo = [s for s in doc['segments'] if s.get('status') != 'done']
        if args.max_segs > 0:
            todo = todo[:args.max_segs]
        log('file=%s 藏章%s total=%d todo=%d' % (path, (doc.get('chapter') or {}).get('tibetan_no'),
                                                 len(doc['segments']), len(todo)))

        def save():
            io.open(path, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=1))

        for s in todo:
            bo = s['bo']
            for lang, prompt, key in (('zh', PROMPT_ZH, 'zh'), ('en', PROMPT_EN, 'en')):
                if s.get(key):
                    continue
                msgs = [{"role": "user", "content": prompt + bo}]
                inputs = tok.apply_chat_template(msgs, add_generation_prompt=True,
                                                 return_dict=True, return_tensors="pt",
                                                 enable_thinking=False)
                mn = args.max_new or min(600, max(200, len(bo)))
                t2 = time.time()
                with torch.no_grad():
                    out = model.generate(**inputs, max_new_tokens=mn, do_sample=False,
                                         no_repeat_ngram_size=8,
                                         pad_token_id=tok.eos_token_id)
                raw = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
                gen, clipped = dedup_truncate(raw)
                s[key] = gen
                s[key + '_meta'] = {
                    'model': MODEL, 'engine': 'mitra-qwen35-translate 9B bf16 CPU',
                    'revisions': 0, 'schooling': '未校订',
                    'gen_s': round(time.time() - t2, 1),
                    'out_tokens': int(out.shape[1] - inputs["input_ids"].shape[1]),
                    'max_new': mn,
                    'clipped_repeat': clipped, 'ts': time.strftime('%Y-%m-%dT%H:%M:%S')}
                log('seg%d %s chars=%d gen=%.1fs max_new=%d clipped=%s :: %s' % (
                    s['no'], lang, len(gen), time.time() - t2, mn, clipped, gen[:60]))
                save()
            s['status'] = 'done'
            save()
            log('seg%d done' % s['no'])
    log('ALL DONE %.1fs' % (time.time() - t0))

if __name__ == '__main__':
    main()
