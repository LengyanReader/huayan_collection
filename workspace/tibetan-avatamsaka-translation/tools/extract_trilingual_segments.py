# -*- coding: utf-8 -*-
"""三语段提取器（逐字回源 · 会话单元＝一章）：从德格藏文底本切出该章开篇段落。

铁律：**绝不手打藏文**——所有藏文段自源文件字节切片而来，
并逐段以 norm()（去叶码标记＋去空白）复验可追回到原文，失败即中止。

段落口径：
- 章界 = {T44-N} … {T44-(N+1)}（德格品目标记，机器可回源；末章或跨卷时取至卷末并如实记限）
- 句读 = །（shad）切分；藏章1 的题名块（རྒྱ་གར་སྐད་དུ …）整体作第 1 段
- 正文按「整句聚合约 min_chars 字符」成段，至多 max_paras 段（默认 6 ＝ 一个里程碑单元）

产物 SSOT（数据层）：
  藏章1：data/translation/tibetan_avatamsaka_trilingual_segments.json（既有文件名保持）
  余章：data/translation/tibetan_avatamsaka_trilingual_segments_ch<N>.json
  每段 {no, kind, vol, marker, folio, char_off, bo, zh:null, en:null, status, verified}

用法（项目根）：
  C:\\Users\\data\\miniconda3\\envs\\hy_py312\\python.exe -X utf8 ^
    workspace/tibetan-avatamsaka-translation/tools/extract_trilingual_segments.py [--chapter 1] [--max-paras 6]
"""
import io, json, re, glob, sys, argparse

BASE = 'data/references/tibetan/derge_kangyur/avatamsaka'
TOC = 'data/alignment/tibetan-derge-toc.json'
OUT1 = 'data/translation/tibetan_avatamsaka_trilingual_segments.json'
OUTN = 'data/translation/tibetan_avatamsaka_trilingual_segments_ch%d.json'
MIN_CHARS = 60
FOLIO = re.compile(r'\[[0-9]+[ab](?:\.[0-9]+)?\]')


def norm(s):
    """回源复验口径：去叶码标记、去全部空白。"""
    return re.sub(r'\s+', '', FOLIO.sub('', s))


def vol_file(vol):
    hits = glob.glob('%s/%s_*' % (BASE, vol))
    if not hits:
        sys.exit('FATAL: 德格卷 %s 源文件未找到' % vol)
    return hits[0]


def chapter_bounds(ch):
    """返回 (源文件, 章起点内容位, 下一标记是否在本文件)。"""
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
    ap.add_argument('--max-paras', type=int, default=6)
    ap.add_argument('--min-chars', type=int, default=MIN_CHARS)
    ap.add_argument('--dry-run', action='store_true', help='只切段与复验，不写数据层（既有译文在跑时安全）')
    a = ap.parse_args()
    ch, MAX_PARAS, MINC = a.chapter, a.max_paras, a.min_chars

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

    parts = [re.sub(r'\s+', ' ', s).strip() for s in ch1c.split('།') if s.strip()]
    # 首个含字母（音节文字）的句读段：跳过纯 Ornament 起首（保持与既有 藏章1 数据层同形，幂等可续）
    ts = next((i for i, s in enumerate(parts) if re.search(r'[\u0F40-\u0FBC]', s)), 0)
    # 正文起点：藏章1 有题名块（起句འདི་སྐད），余章从首个实质句读段起
    body0 = ts
    if ch == 1:
        for i, s in enumerate(parts):
            if s.startswith('འདི་'):
                body0 = i
                break
        else:
            sys.exit('FATAL: 藏章1 未定位正文起句འདི་སྐད（口径变化？勿手打，需人工核查）')

    def cut(p_from, p_to_last, c_from):
        s1 = ch1c.index(parts[p_from], c_from)
        s2 = ch1c.index(parts[p_to_last], s1) + len(parts[p_to_last])
        return ch1c[s1:s2] + '།'

    seg_slices = []
    c0 = ch1c.index(parts[ts])
    if ch == 1:
        seg_slices.append(('title', cut(ts, body0 - 1, c0)))
        p = body0
    else:
        p = ts
    cstart = c0
    acc = 0
    while p < len(parts) and len(seg_slices) < MAX_PARAS:
        q = p
        while acc < MINC and q + 1 < len(parts):
            acc += len(parts[q])
            q += 1
        cstart = ch1c.index(parts[p], cstart)
        seg_slices.append(('body', cut(p, q, cstart)))
        acc = 0
        p = q + 1

    out_segs, cursor = [], 0
    for k, (kind, bo) in enumerate(seg_slices[:MAX_PARAS]):
        npos = nmap.find(norm(bo), cursor)
        if npos < 0:
            sys.exit('FATAL: 段 %d 无法逐字追回源文件：%s' % (k + 1, bo[:60]))
        cursor = npos + len(norm(bo))
        out_segs.append({'no': k + 1, 'kind': kind, 'vol': ent['vol'], 'marker': 'T44-%d' % ch,
                         'folio': folio_for(npos), 'char_off': noff[npos],
                         'bo': bo, 'zh': None, 'en': None, 'status': 'pending', 'verified': True})

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

    doc = {
        'id': 'tibetan_avatamsaka_trilingual_segments_ch%d' % ch,
        'batch_created': 'L.360' if ch == 1 else '〔本段所属批次见 PROGRESS〕',
        'date': '2026-11-06' if ch == 1 else None,
        'source_file': src.replace('\\', '/'),
        'chapter_boundary': '{T44-%d}…{T44-%d}%s' % (ch, ch + 1,
                              '' if has_next else '（下一标记不在本卷文件内 → 取至卷末，〔跨卷未合并〕）'),
        'grounding_rule': '藏文段一律自德格底本 {T44-%d} 区间字节切片提取并逐段 norm() 复验；绝不手打' % ch,
        'segmentation_rule': ('题名块整体为段1；' if ch == 1 else '') +
                             '正文按 shad（།）整句聚合，每段约≥%d 字；本单元共 %d 段' % (MINC, len(out_segs)),
        'translation_engine': 'buddhist-nlp/mitra-qwen35-translate（9B, bf16, CPU）· 输出〔模型译·未校订〕',
        'chapter': {'tibetan_no': ch, 'derge_vol': ent['vol'], 'start_folio': ent['start_folio'],
                    'chinese_correspondence': corr},
        'ch_stats': {'raw_chars': len(ch1), 'clean_chars': len(ch1c), 'sentence_count': len(parts)},
        'segments': out_segs,
    }
    out = OUT1 if ch == 1 else (OUTN % ch)
    if a.dry_run:
        same = 'n/a'
        if glob.glob(out):
            old = json.loads(io.open(out, encoding='utf-8').read())
            same = [s['bo'] for s in old.get('segments', [])] == [s['bo'] for s in out_segs]
        print('DRY-RUN 藏章%d：%d 段 · 与既有数据层同形=%s · 章正文 %s 字符 / %d 句读' % (
            ch, len(out_segs), same, len(ch1c), len(parts)))
        for s in out_segs:
            print(' [%d] %s folio=%s len=%d :: %s…' % (s['no'], s['kind'], s['folio'], len(s['bo']), s['bo'][:36]))
        return
    # 已译段保留（幂等续跑：同段号 bo 一致则继承 zh/en/status）
    if glob.glob(out):
        old = json.loads(io.open(out, encoding='utf-8').read())
        prev = {s['bo']: s for s in old.get('segments', [])}
        for s in doc['segments']:
            o = prev.get(s['bo'])
            if o:
                for kk in ('zh', 'en', 'zh_meta', 'en_meta', 'status'):
                    if o.get(kk) is not None:
                        s[kk] = o[kk]
    if doc['date'] is None:
        doc['date'] = '2026-11-06'
    io.open(out, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=1))
    done = sum(1 for s in doc['segments'] if s.get('status') == 'done')
    print('OK 藏章%d -> %s | %d 段（已译 %d）| 章正文 %s 字符 / %d 句读' % (
        ch, out, len(out_segs), done, doc['ch_stats']['clean_chars'], doc['ch_stats']['sentence_count']))
    for s in doc['segments']:
        print(' [%d] %s folio=%s len=%d' % (s['no'], s['kind'], s['folio'], len(s['bo'])))


if __name__ == '__main__':
    main()
