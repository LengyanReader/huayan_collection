# -*- coding: utf-8 -*-
"""阶段二·底本处理：从德格版 Toh 44 (035-038) 机械提取藏译 45 品 TOC + 底本 sha256 台账。

原则（承本仓铁律）：
- 逐字回源：品目标记 {T44-N}、叶码 [Na.b]、藏文开篇种子，均由真实文本字节提取，不臆造。
- 汉藏品名对应「需人工比对」：仅登记结构性事实（藏 45 品 vs 八十 39 品 vs 六十 34 品），
  逐品对应一律标 alignment_status="待核"，不代立论。
- 机器只观察：本脚本只提取 / 记录 / 排序，不改写任何实质内容。

输出：data/alignment/tibetan-derge-toc.json
"""
import io, glob, os, re, json, hashlib

BASE = 'data/references/tibetan/derge_kangyur/avatamsaka'
CBETA = {
    'T10n0279': 'data/references/cbeta/T10n0279.xml',   # 八十华严
    'T09n0278': 'data/references/cbeta/T09n0278.xml',   # 六十华严
}
OUT = 'data/alignment/tibetan-derge-toc.json'


def sha256(path):
    return hashlib.sha256(io.open(path, 'rb').read()).hexdigest()


def clean(seg):
    seg = re.sub(r'\[[0-9]+[ab](?:\.[0-9]+)?\]', '', seg)     # 去叶码标记
    seg = re.sub(r'\{T44(?:-\d+)?\}', '', seg)                 # 去 Tohoku 标记
    seg = seg.replace('༄༅༅།', '').replace('༄༅།', '').replace('༑', '')
    seg = re.sub(r'\s+', ' ', seg).strip()
    return seg


def prev_folio(txt, pos):
    ms = list(re.finditer(r'\[(\d+[ab](?:\.\d+)?)\]', txt[:pos]))
    return ms[-1].group(1) if ms else ''


def _cn2int(s):
    d = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7,
         '八': 8, '九': 9, '十': 10, '百': 100}
    total, num = 0, 0
    for ch in s:
        v = d.get(ch, 0)
        if ch == '十':
            total += (num or 1) * 10; num = 0
        elif ch == '百':
            total += (num or 1) * 100; num = 0
        else:
            num = v
    return total + num


def last_pin(path):
    """从 CBETA XML 实测「品第N」最大序号的品题，用作品数的可回源证据（排除「明本作…」异文注）。"""
    x = io.open(path, encoding='utf-8', errors='replace').read()
    best, best_n = '', -1
    for n in re.findall(r'[\u4e00-\u9fff]{2,12}品第[一二三四五六七八九十百]+', x):
        if '明本作' in n or n.startswith('明本'):
            continue
        m = re.search(r'第([一二三四五六七八九十百]+)$', n)
        if not m:
            continue
        k = _cn2int(m.group(1))
        if k > best_n:
            best_n, best = k, n
    return best


def main():
    # 1. 底本 sha256 / 体量台账（德格 4 卷 + CBETA 对照本）
    base_texts = []
    for f in sorted(glob.glob(BASE + '/0*.txt')):
        b = io.open(f, 'rb').read()
        base_texts.append({
            'file': os.path.relpath(f, 'data/references/tibetan').replace('\\', '/'),
            'vol': os.path.basename(f)[:3],
            'bytes': len(b),
            'sha256': hashlib.sha256(b).hexdigest(),
            'role': '藏文主底本 (Toh 44)',
        })
    for sig, p in CBETA.items():
        if os.path.exists(p):
            b = io.open(p, 'rb').read()
            base_texts.append({
                'file': os.path.relpath(p, 'data/references').replace('\\', '/'),
                'siglum': sig, 'bytes': len(b),
                'sha256': hashlib.sha256(b).hexdigest(),
                'role': '汉文对勘本',
            })

    # 2. 藏译 45 品 TOC（机械提取 · 逐字回源）
    entries = []
    for f in sorted(glob.glob(BASE + '/0*.txt')):
        vol = os.path.basename(f)[:3]
        txt = io.open(f, encoding='utf-8', errors='replace').read()
        for m in re.finditer(r'\{T44-(\d+)\}', txt):
            n = int(m.group(1))
            seg = clean(txt[m.end():m.end() + 260])
            entries.append({
                'no': n, 'vol': vol,
                'start_folio': prev_folio(txt, m.start()),
                'tibetan_open': seg[:90],
                'alignment_status': '待核',   # 汉藏逐品对应需人工比对
            })
    entries.sort(key=lambda e: e['no'])

    doc = {
        'toh': '44',
        'title': 'བུདྡྷ་ཨ་བ་ཏང་ས་ཀ / 大方广佛华严经（德格版 Kangyur）',
        'extracted_by': 'workspace/tibetan-avatamsaka-translation/tools/extract_tibetan_toc.py',
        'note': '品目标记 {T44-N} 与叶码、藏文开篇种子均由德格 .txt 逐字回源提取；'
                '汉藏逐品对应一律标〔待核〕，仅结构性事实可先行陈述。',
        'structural_facts': {
            'tibetan_chapters': len(entries),
            'chinese_80_chapters': 39,   # T10n0279 八十华严·品题实测末=入法界品第三十九
            'chinese_80_last_pin': last_pin(CBETA['T10n0279']),
            'chinese_60_chapters': 34,   # T09n0278 六十华严·品题实测末=法界品第三十四
            'chinese_60_last_pin': last_pin(CBETA['T09n0278']),
            'bam_po_total': 115,
            'derge_vols': ['035', '036', '037', '038'],
        },
        'base_texts': base_texts,
        'toc': entries,
    }
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=2))
    print('WROTE', OUT, '· toc=%d · base_texts=%d · ch80=%d ch60=%d'
          % (len(entries), len(base_texts),
             sum(1 for e in base_texts if e.get('siglum', '').startswith('T1')),
             sum(1 for e in base_texts if e.get('siglum', '').startswith('T0'))))


if __name__ == '__main__':
    main()
