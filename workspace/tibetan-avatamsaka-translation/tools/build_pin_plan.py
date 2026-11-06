# -*- coding: utf-8 -*-
"""L.360 藏章 ↔ 汉品 品目规划表构建器（机器派生，不手填）。

输入（全部为既有 SSOT）：
- data/alignment/tibetan-derge-toc.json           45 章骨架（卷/叶码/开篇种子）
- data/alignment/tibetan_zhuhuju_b1..b6.json      逐章对勘所得 (pin ↔ tibetan_ch)
- data/alignment/tibetan_ch_map_L352.json         藏28-31 重勘（覆写早期误配）
- data/catalog/chapters.yaml                      品名 / Cleary 英题 / 三本有无
- data/translation/tibetan_avatamsaka_trilingual_segments.json  三语段进度

输出：data/alignment/tibetan_chinese_pin_plan_L360.json
派生口径：证据覆写顺序 b1-b6 → L.352 correction；冲突即记 conflicts（不静默取舍）。
未达逐章实证者一律 correspondence='待核'，不臆造对应。
"""
import io, json, re, glob, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # Windows cp437 控制台下防 UnicodeEncodeError（仅显示层）

TOC = 'data/alignment/tibetan-derge-toc.json'
OUT = 'data/alignment/tibetan_chinese_pin_plan_L360.json'
SEG = 'data/translation/tibetan_avatamsaka_trilingual_segments.json'

# 1) 45 章骨架
toc = json.loads(io.open(TOC, encoding='utf-8').read())
rows = {e['no']: {'tibetan_ch': e['no'], 'vol': e['vol'], 'start_folio': e['start_folio'],
                  'tibetan_open_seed': re.sub(r'\s+', ' ', e['tibetan_open']).strip()[:48],
                  'pin': None, 'pin_title_zh': None, 'pin_title_en': None,
                  'evidence': '待核', 'rule': None} for e in toc['toc']}

# 2) 逐章对勘所得 pairs
pairs, conflicts = {}, []
for fn in sorted(glob.glob('data/alignment/tibetan_zhuhuju_b[1-6].json')):
    d = json.loads(io.open(fn, encoding='utf-8').read())
    src = fn.split('/')[-1]
    got = []
    ch = d.get('chapters') or []
    it = ch.values() if isinstance(ch, dict) else ch
    for v in it:
        if isinstance(v, dict) and v.get('pin') and v.get('tibetan_ch'):
            got.append((int(re.sub(r'\D', '', v['pin'])), v['tibetan_ch'], src + ' 章条目'))
    for v in (d.get('mapping') or []):
        if v.get('pin') and v.get('tibetan_ch'):
            got.append((int(v['pin']), v['tibetan_ch'], src + ' mapping'))
    for pin, tc, whence in got:
        if tc in rows and rows[tc]['pin'] not in (None, pin):
            conflicts.append({'tibetan_ch': tc, 'kept': rows[tc]['pin'], 'dropped': pin, 'note': whence})
        if tc in rows and rows[tc]['pin'] is None:
            rows[tc]['pin'] = pin
            rows[tc]['evidence'] = whence
        elif tc in rows:
            rows[tc]['evidence'] += ' + ' + whence

# 3) L.352 重勘覆写（后期实证优先）
m352 = json.loads(io.open('data/alignment/tibetan_ch_map_L352.json', encoding='utf-8').read())
for c in m352['correction']:
    tc = c['tibetan_ch']
    mm = re.search(r'品\s*(\d+)', c['new'])
    pin = int(mm.group(1)) if mm else None
    if pin:
        if tc in rows and rows[tc]['pin'] and rows[tc]['pin'] != pin:
            conflicts.append({'tibetan_ch': tc, 'dropped': rows[tc]['pin'],
                              'kept': pin, 'note': 'L.352 correction 覆写'})
        rows[tc]['pin'] = pin
        rows[tc]['evidence'] = 'L.352 重勘（%s）' % c['evidence'][:40]

# 4) 藏独有二章（chapters.yaml is_unique_to_bo）
import yaml
cat = yaml.safe_load(io.open('data/catalog/chapters.yaml', encoding='utf-8'))
names = {c['order']: c for c in cat['chapters'] if c['order'] <= 39}
unique_bo = [c for c in cat['chapters'] if c.get('is_unique_to_bo')]
ub = {c['title_zh']: c for c in unique_bo}
# 藏11〈如来华严〉= 藏独有（L.354/L.357 结构观察）；藏32〈普贤宣说〉= 藏独有（b5 mapping pin:null）
for tc, key in ((11, '如来华严品'), (32, '普贤宣说品')):
    rows[tc]['rule'] = '藏独有'
    rows[tc]['pin_title_zh'] = '（藏独有·%s）' % key
    rows[tc]['pin_title_en'] = ub[key]['title_en'] + ' (Tibetan-only)'
rows[11]['evidence'] = 'chapters.yaml is_unique_to_bo + L.354 结构观察'
rows[32]['evidence'] = 'b5 mapping pin:null「普贤行段·归属待核」'

# 5) 品名回填 + 对应律（rule）标注
for tc, r in rows.items():
    if r['pin'] and r['rule'] != '藏独有':
        c = names.get(r['pin'])
        if c:
            r['pin_title_zh'] = c['title_zh']
            r['pin_title_en'] = c['title_en']
            r['in_60huayan'] = c.get('in_60huayan')
        r['rule'] = '差%d' % (tc - r['pin'])
    elif r['rule'] is None:
        r['rule'] = '前段不平行'
        r['pin_title_zh'] = None
        r['evidence'] = '藏1-10/12-13 与品1-8 章界不平行（L.352 finding：不平行限于前段）〔待核〕'

# 6) 三语翻译进度（聚合 藏章1 主文件 + 后续每章分文件 tibetan_avatamsaka_trilingual_segments_*.json）
done_by_ch = {}
for fn in sorted(glob.glob('data/translation/tibetan_avatamsaka_trilingual_segments*.json')):
    d2 = json.loads(io.open(fn, encoding='utf-8').read())
    tc2 = (d2.get('chapter') or {}).get('tibetan_no')
    if tc2 is None:
        continue
    done_by_ch[tc2] = done_by_ch.get(tc2, 0) + sum(1 for s in d2.get('segments', []) if s.get('status') == 'done')
for tc, r in rows.items():
    n = done_by_ch.get(tc, 0)
    r['trilingual_done_segments'] = n
    r['trilingual_status'] = ('开篇%d段已试译' % n) if n else '未启动'

# 7) 翻译波次规划（依对应律分层：先已实证平行段，后待核段）
waves = [
    {'wave': 'W1', 'scope': '藏章1 开篇 6 段', 'chapters': [1],
     'why': '体例验证段·L.203 已示范对勘（藏×八十×六十逐字回源）', 'batch': 'L.360'},
    {'wave': 'W2', 'scope': '藏章14–31（对应律「差5」段，= 品9–26）',
     'chapters': sorted(tc for tc in rows if rows[tc]['rule'] == '差5'),
     'why': '逐章一对一对应已机器实证（b1–b4 + L.352 覆写），可直接三语并列',
     'batch': 'L.361 起（每章开篇 6 段）'},
    {'wave': 'W3', 'scope': '藏章33–45（对应律「差6」段，= 品27–39）',
     'chapters': sorted(tc for tc in rows if rows[tc]['rule'] == '差6'),
     'why': '藏汉对读六批 L.357 收官实证；入法界品（藏45=品39）篇幅最大，须分段排产',
     'batch': '待 W2 后'},
    {'wave': 'W4', 'scope': '藏章1–10、12–13（前段·章界不平行）',
     'chapters': sorted(tc for tc in rows if rows[tc]['rule'] == '前段不平行'),
     'why': '须先做人工段界比对（藏12 章 vs 汉 8 品），未定界前只译不配对〔待核〕',
     'batch': '待 W3 后'},
    {'wave': 'W5', 'scope': '藏独有 藏章11〈如来华严〉· 藏章32〈普贤宣说〉',
     'chapters': [11, 32],
     'why': '无汉文平行品，须另建术语表并单独立校勘线；藏32 归属仍〔待核〕',
     'batch': '待 W3 后'},
]

doc = {
    'id': 'tibetan_chinese_pin_plan_L360',
    'batch': 'L.360',
    'date': '2026-11-06',
    'derived_from': [TOC, 'data/alignment/tibetan_zhuhuju_b1..b6.json',
                     'data/alignment/tibetan_ch_map_L352.json', 'data/catalog/chapters.yaml', SEG],
    'derivation_rule': 'pairs 自对勘批机械收集；L.352 correction 覆写早期误配；冲突记入 conflicts 不静默取舍；'
                       '未达逐章实证者 correspondence 保持〔待核〕',
    'totals': {
        'tibetan_chapters': len(rows),
        'verified_pairs': sum(1 for r in rows.values() if r['pin'] and r['rule'] != '藏独有'),
        'tibetan_only': sum(1 for r in rows.values() if r['rule'] == '藏独有'),
        'front_unparallel': sum(1 for r in rows.values() if r['rule'] == '前段不平行'),
    },
    'conflicts': conflicts,
    'waves': waves,
    'chapters': [rows[k] for k in sorted(rows)],
}
io.open(OUT, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=1))
print('OK -> %s' % OUT)
print(json.dumps(doc['totals'], ensure_ascii=False))
print('conflicts=%d' % len(conflicts))
for c in conflicts:
    print('  ', json.dumps(c, ensure_ascii=True))
for tc in (1, 11, 14, 28, 32, 33, 39, 45):
    r = rows[tc]
    print('藏%d %s pin=%s rule=%s ev=%s' % (tc, r['start_folio'], r['pin'], r['rule'], (r['evidence'] or '')[:34]))
