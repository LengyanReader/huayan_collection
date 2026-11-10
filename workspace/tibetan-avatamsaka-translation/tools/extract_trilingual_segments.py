# -*- coding: utf-8 -*-
"""三语段提取器（逐字回源 · 句末感知 · 全章无损）：从德格藏文底本切出整章段落。

铁律：**绝不手打藏文**——所有藏文段自源文件字节切片而来，
并逐段以 norm()（去叶码标记＋去空白）复验可追回到原文，失败即中止。

段落口径（L.380 起，用户裁决：保证语句完整＋分段连贯＋不丢内容）：
- 章界 = {T44-N} … {T44-(N+1)}（德格品目标记，机器可回源；末章或跨卷时取至卷末并如实记限）
- 句读 = shad 串（། / །། / ། །）切分；起首纯符号段（无字母）不入段（与藏章1 同口径）
- 句末感知收段：累积 ≥min_chars 且遇句末（终结助词 ཏོ/སོ/ནོ/ངོ/འོ/དོ/མོ/ལོ/ཡིན/ཡོད/མེད
  或双 shad）才收段（boundary=final）；超 max_chars 仍未句末，允许在非续读 shad 处软收
  （boundary=soft）；绝不以续读（དང/ཏེ/ནས/གྱིས…）收尾；章末如实标 boundary=tail
- 整章切到底（--max-paras 0=不限，默认）；数据层先保全章，译文逐批补（未译段 pending）
- --continue：已译章旧段原样保留（旧译不丢），自末段尾续切至章末；旧段间若因旧口径
  漏掉双 shad 之第二 shad，仅容忍纯 shad 缺口并计数（标点级，非内容），余者一律 FATAL
- 连续性自检：各段 norm() 拼接 == 自段1起至章末之 norm()（无缺口无重叠），失败即中止

产物 SSOT（数据层）：
  藏章1：data/translation/tibetan_avatamsaka_trilingual_segments.json（既有文件名保持）
  余章：data/translation/tibetan_avatamsaka_trilingual_segments_ch<N>.json
  每段 {no, kind, vol, marker, folio, char_off, bo, zh:null, en:null, status, verified}
  新段另带 boundary（final/soft/tail）；doc 带 full_chapter 标记

用法（项目根）：
  C:\\Users\\data\\miniconda3\\envs\\hy_py312\\python.exe -X utf8 ^
    workspace/tibetan-avatamsaka-translation/tools/extract_trilingual_segments.py ^
    [--chapter 1] [--max-paras 0] [--continue] [--dry-run]
"""
import io, json, re, glob, sys, argparse, time

BASE = 'data/references/tibetan/derge_kangyur/avatamsaka'
TOC = 'data/alignment/tibetan-derge-toc.json'
OUT1 = 'data/translation/tibetan_avatamsaka_trilingual_segments.json'
OUTN = 'data/translation/tibetan_avatamsaka_trilingual_segments_ch%d.json'
MIN_CHARS = 60
MAX_CHARS = 400
FOLIO = re.compile(r'\[[0-9]+[ab](?:\.[0-9]+)?\]')
SHAD_RUN = re.compile(r'((?:།[ \t]*)+)')
# 句末终结助词（rdzogs tshig）＋判断/存在动词句末；rstrip tsheg 后判定
FINALS = ('ཏོ', 'སོ', 'ནོ', 'ངོ', 'འོ', 'དོ', 'མོ', 'ལོ', 'ཡིན', 'ཡོད', 'མེད')
# 续读/非句末（软收亦不许在此收尾）；单音节助词另列（须带 tsheg，免误伤 ལྡན/བསྟན 等词尾）
CONT = ('དང', 'ཏེ', 'སྟེ', 'ནས', 'གྱིས', 'གིས', 'ཀྱིས', 'ཞིང', 'ཅིང', 'ཤིང',
        'བས', 'པས', 'ཞེས', 'ཅེས', 'ཞེ', 'ཅེ', 'གྱི', 'གི', 'ཀྱི', 'འི', 'ཕྱིར',
        'ཏུ', 'སུ', 'རུ', 'དུ')
CONT_SYL = ('ན', 'ལ')


def norm(s):
    """回源复验口径：去叶码标记、去全部空白。"""
    return re.sub(r'\s+', '', FOLIO.sub('', s))


def is_final(text, shads):
    if shads.count('།') >= 2:
        return True
    return text.rstrip('་').endswith(FINALS)


def is_cont(text):
    t = text.rstrip('་')
    if t.endswith(CONT):
        return True
    return any(t == s or t.endswith('་' + s) for s in CONT_SYL)


def vol_file(vol):
    hits = glob.glob('%s/%s_*' % (BASE, vol))
    if not hits:
        sys.exit('FATAL: 德格卷 %s 源文件未找到' % vol)
    return hits[0]


def chapter_bounds(ch):
    """返回 (源文件, 全文, 章起点内容位, 章终点内容位, 下一标记是否在本文件, toc 条目)。"""
    toc = json.loads(io.open(TOC, encoding='utf-8').read())
    ent = next((e for e in toc['toc'] if e['no'] == ch), None)
    if not ent:
        sys.exit('FATAL: toc 无藏章 %d' % ch)
    f = vol_file(ent['vol'])
    raw = io.open(f, encoding='utf-8').read()
    tag = '{T44-%d}' % ch
    if tag not in raw:
        sys.exit('FATAL: 文件 %s 内无标记 %s（章界口径变化，需人工核查）' % (f, tag))
    a = raw.index(tag) + len(tag)
    nxt = '{T44-%d}' % (ch + 1)
    b = raw.index(nxt) if nxt in raw else len(raw)
    return f, raw, a, b, (nxt in raw), ent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapter', type=int, default=1)
    ap.add_argument('--max-paras', type=int, default=0, help='0=整章切到底（默认）；>0 限新切段数')
    ap.add_argument('--min-chars', type=int, default=MIN_CHARS)
    ap.add_argument('--max-chars', type=int, default=MAX_CHARS, help='软收上限（句末未至时）')
    ap.add_argument('--continue', dest='cont', action='store_true',
                    help='已译章续切：旧段原样保留，自末段尾续切至章末')
    ap.add_argument('--dry-run', action='store_true', help='只切段与复验，不写数据层（既有译文在跑时安全）')
    a = ap.parse_args()
    ch, MAX_PARAS, MINC, MAXC = a.chapter, a.max_paras, a.min_chars, a.max_chars

    src, raw, beg, end, has_next, ent = chapter_bounds(ch)
    ch1 = raw[beg:end]
    ch1c = re.sub(r'[ \t\r\n]+', ' ', FOLIO.sub('', ch1)).strip()
    src_norm = norm(ch1)
    # norm→原文位置映射：整段跳过叶码标记（与 FOLIO.sub 口径一致）
    skip = set()
    for m in FOLIO.finditer(ch1):
        skip.update(range(m.start(), m.end()))
    nchars, noff = [], []
    for i, c in enumerate(ch1):
        if i in skip or c.isspace():
            continue
        nchars.append(c)
        noff.append(i)
    nmap = ''.join(nchars)
    assert nmap == src_norm, 'norm 双口径不一致（叶码标记跳过逻辑有误）'

    def folio_for(np_):
        orig = noff[min(np_, len(noff) - 1)]
        last = None
        for fm in FOLIO.finditer(ch1, 0, orig):
            last = fm
        return last.group(0) if last else ent['start_folio']

    # shad 串感知切分：parts = (text, shads)；双 shad（含其间空白）整体随前段
    toks = SHAD_RUN.split(ch1c)
    parts = []
    for i in range(0, len(toks) - 1, 2):
        t = toks[i].strip()
        if t:
            parts.append((t, toks[i + 1]))
    if toks[-1].strip():
        parts.append((toks[-1].strip(), ''))
    # 各 part 在 ch1c 的字节区间 [s,e)（含随段 shad 串；顺序游标定位）
    spans, c = [], 0
    for t, sh in parts:
        s = ch1c.index(t, c)
        e = s + len(t)
        m = re.match(r'[ \t]*(?:།[ \t]*)*', ch1c[e:])
        run = m.group(0) if m else ''
        if run.count('།') != sh.count('།'):
            sys.exit('FATAL: shad 串口径不一致 @%d（%s…）' % (s, t[:30]))
        e += len(run)
        spans.append((s, e))
        c = e
    # 首个含字母（音节文字）的句读段：跳过纯 Ornament 起首（与既有数据层同口径）
    ts = next((i for i, (t, _) in enumerate(parts) if re.search(r'[ཀ-ྼ]', t)), 0)
    # 正文起点：藏章1 有题名块（起句འདི་སྐད），余章从首个实质句读段起
    body0 = ts
    if ch == 1 and not a.cont:
        for i, (t, _) in enumerate(parts):
            if t.startswith('འདི་'):
                body0 = i
                break
        else:
            sys.exit('FATAL: 藏章1 未定位正文起句འདི་སྐད（口径变化？勿手打，需人工核查）')

    out = OUT1 if ch == 1 else (OUTN % ch)
    old_segs, old_doc = [], None
    p = body0
    if a.cont:
        if not glob.glob(out):
            sys.exit('FATAL: --continue 需既有数据层：%s 不存在' % out)
        old_doc = json.loads(io.open(out, encoding='utf-8').read())
        old_segs = old_doc.get('segments') or []
        if not old_segs:
            sys.exit('FATAL: --continue 既有数据层无段')
        last_bo = old_segs[-1]['bo']
        pos = ch1c.find(last_bo)
        if pos < 0:
            sys.exit('FATAL: 旧末段无法在章正文定位（口径变化？勿手打，需人工核查）')
        resume = pos + len(last_bo)
        p = next((i for i, (s, _) in enumerate(spans) if s >= resume), len(parts))

    # 句末感知聚段：final=句末收段；soft=超上限非续读处软收；tail=章末如实收
    new_slices = []  # (kind, bo, boundary)
    if ch == 1 and not a.cont and body0 > ts:
        new_slices.append(('title', ch1c[spans[ts][0]:spans[body0 - 1][1]], 'final'))
    while p < len(parts) and (MAX_PARAS <= 0 or len(new_slices) < MAX_PARAS):
        q, acc, boundary = p, 0, 'tail'
        while True:
            acc += len(parts[q][0])
            if acc >= MINC and is_final(*parts[q]):
                boundary = 'final'
                break
            if q + 1 >= len(parts):
                boundary = 'tail'
                break
            if acc >= MAXC and not is_cont(parts[q][0]):
                boundary = 'soft'
                break
            q += 1
        new_slices.append(('body', ch1c[spans[p][0]:spans[q][1]], boundary))
        p = q + 1

    # 逐段 norm() 复验：pos==cursor 严合；--continue 旧段仅容忍纯 shad 缺口（计数留痕）
    out_segs, cursor, shad_gaps = [], 0, 0
    all_bo = [(s['bo'], None) for s in old_segs] + [(b, bd) for _, b, bd in new_slices]
    for k, (bo, bd) in enumerate(all_bo):
        nbo = norm(bo)
        npos = nmap.find(nbo, cursor)
        if npos < 0:
            sys.exit('FATAL: 段 %d 无法逐字追回源文件：%s' % (k + 1, bo[:60]))
        gap = nmap[cursor:npos]
        if gap and k > 0:
            if a.cont and not gap.strip('།'):
                shad_gaps += 1
            else:
                sys.exit('FATAL: 段 %d 前有内容缺口/重叠（%d 字：%s…）' % (
                    k + 1, len(gap), gap[:30]))
        cursor = npos + len(nbo)
        if k < len(old_segs):
            out_segs.append(old_segs[k])
        else:
            kind = new_slices[k - len(old_segs)][0]
            out_segs.append({'no': k + 1, 'kind': kind, 'vol': ent['vol'], 'marker': 'T44-%d' % ch,
                             'folio': folio_for(npos), 'char_off': noff[npos],
                             'bo': bo, 'zh': None, 'en': None, 'status': 'pending',
                             'verified': True, 'boundary': bd})
    full = MAX_PARAS <= 0 or p >= len(parts)
    if full and cursor != len(nmap):
        sys.exit('FATAL: 章末未覆尽（余 %d norm 字；不丢内容口径，需人工核查）' % (len(nmap) - cursor))

    # 该章汉藏对应（只取既有实证，不新立判断）
    corr, plan_p = '〔待核〕', 'data/alignment/tibetan_chinese_pin_plan_L360.json'
    try:
        pl = json.loads(io.open(plan_p, encoding='utf-8').read())
        r = next((c for c in pl['chapters'] if c['tibetan_ch'] == ch), None)
        if r:
            corr = ('品%d〈%s〉（对应律 %s）·证据：%s' % (r['pin'], r['pin_title_zh'], r['rule'], r['evidence'])) \
                if r.get('pin') and r['rule'] not in ('藏独有', '前段不平行') \
                else '%s · 证据：%s' % (r['rule'], r['evidence'])
    except Exception:
        pass

    rule = ('题名块整体为段1；' if ch == 1 and not a.cont else '') + \
           ('L.380 句末感知：累积≥%d 字遇句末（终结助词/双shad）收段，超 %d 字非续读处软收，'
            '绝不以续读收尾；整章切到底共 %d 段；段拼接 norm 逐字对账无缺口' % (MINC, MAXC, len(out_segs)))
    if a.cont:
        rule += '；旧段1–%d 原样保留（旧译不丢），自旧末段尾续切' % len(old_segs)
        if shad_gaps:
            rule += '；旧口径纯 shad 缺口 %d 处（标点级，非内容，如实计数）' % shad_gaps
    doc = {
        'id': 'tibetan_avatamsaka_trilingual_segments_ch%d' % ch,
        'batch_created': 'L.360' if ch == 1 else '〔本段所属批次见 PROGRESS〕',
        'date': '2026-11-06' if ch == 1 else time.strftime('%Y-%m-%d'),
        'source_file': src.replace('\\', '/'),
        'chapter_boundary': '{T44-%d}…{T44-%d}%s' % (ch, ch + 1,
                              '' if has_next else '（下一标记不在本卷文件内 → 取至卷末，〔跨卷未合并〕）'),
        'grounding_rule': '藏文段一律自德格底本 {T44-%d} 区间字节切片提取并逐段 norm() 复验；绝不手打' % ch,
        'segmentation_rule': rule,
        'full_chapter': bool(full),
        'translation_engine': 'buddhist-nlp/mitra-qwen35-translate（9B, bf16, CPU）· 输出〔模型译·未校订〕',
        'chapter': {'tibetan_no': ch, 'derge_vol': ent['vol'], 'start_folio': ent['start_folio'],
                    'chinese_correspondence': corr},
        'ch_stats': {'raw_chars': len(ch1), 'clean_chars': len(ch1c), 'sentence_count': len(parts)},
        'segments': out_segs,
    }
    if a.cont:
        doc['continued'] = {'batch': 'L.380', 'date': time.strftime('%Y-%m-%d'),
                            'old_segs': len(old_segs), 'shad_gaps': shad_gaps}
        for kk in ('batch_created', 'date'):
            if old_doc.get(kk):
                doc[kk] = old_doc[kk]
    if a.dry_run:
        print('DRY-RUN 藏章%d：%d 段（旧 %d＋新 %d）· full_chapter=%s · 章正文 %s 字符 / %d 句读' % (
            ch, len(out_segs), len(old_segs), len(new_slices), full, len(ch1c), len(parts)))
        for s in out_segs[len(old_segs):]:
            print(' [%d] %s folio=%s len=%d boundary=%s :: …%s' % (
                s['no'], s['kind'], s['folio'], len(s['bo']), s.get('boundary', '-'), s['bo'][-24:]))
        return
    # 已译段保留（幂等续跑：同段号 bo 一致则继承 zh/en/status）
    if glob.glob(out) and not a.cont:
        old = json.loads(io.open(out, encoding='utf-8').read())
        prev = {s['bo']: s for s in old.get('segments', [])}
        for s in doc['segments']:
            o = prev.get(s['bo'])
            if o:
                for kk in ('zh', 'en', 'zh_meta', 'en_meta', 'status'):
                    if o.get(kk) is not None:
                        s[kk] = o[kk]
    io.open(out, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=1))
    done = sum(1 for s in doc['segments'] if s.get('status') == 'done')
    print('OK 藏章%d -> %s | %d 段（已译 %d）· full_chapter=%s | 章正文 %s 字符 / %d 句读' % (
        ch, out, len(out_segs), done, full, doc['ch_stats']['clean_chars'], doc['ch_stats']['sentence_count']))
    for s in out_segs:
        print(' [%d] %s folio=%s len=%d boundary=%s' % (
            s['no'], s['kind'], s['folio'], len(s['bo']), s.get('boundary', '旧段')))


if __name__ == '__main__':
    main()