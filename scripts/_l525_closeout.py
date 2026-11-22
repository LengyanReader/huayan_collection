# -*- coding: utf-8 -*-
"""_l525_closeout.py — L.525 清账批：
①P25 §2.3a ③④⑤余文补入（c80/p025.json tc 切片 13888-17930·两次挂账闭账）
②P17/P18 藏译对照待勘指针
"""
import glob, io, json, re, sys

sys.stdout.reconfigure(encoding='utf-8')
HAN = re.compile(r'[\u3400-\u9fff]')


def han(s):
    return len(HAN.findall(s))


def gpat(pat):
    g = glob.glob('docs/经学文献/华严经细读/**/' + pat, recursive=True)
    assert g, pat
    return g[0]


# ══ ① P25 余文 ══
fp = gpat('华严经细读_第二十五部_*.md')
md = io.open(fp, encoding='utf-8').read()
assert 'L.525 余文' not in md
d = json.load(open('web/demo/data/sutra/c80/p025.json', encoding='utf-8'))
paras = [p for s in d['segs'] for p in s['paras']]
tc = re.sub(r'\s+', '', '\n'.join(paras))
i_stop = tc.find('於此明了善迴向。') + len('於此明了善迴向。')
i_end = tc.find('云何為菩薩摩訶薩隨順堅固一切善根迴向')
assert 0 < i_stop < i_end
spans = []
off = 0
for p in paras:
    n = len(re.sub(r'\s+', '', p))
    spans.append((off, off + n))
    off += n
cont = [p for p, (a, b) in zip(paras, spans) if b > i_stop and a < i_end]
cont_han = sum(han(p) for p in cont)
print('余文切片:', cont_han, '字·', len(cont), '段')

# 定位 md 内尾块（§2.3a 尾·2.5 前的区域）
i_note = md.find('（回向③④⑤余文待 L.264b 全引）')
assert i_note > 0
i_block = md.rfind('大方廣佛華嚴經卷第二十四', 0, i_note)
assert 0 < i_block < i_note
i_note_end = i_note + len('（回向③④⑤余文待 L.264b 全引）')
new = ('> **〔L.525 余文补入〕**：③④⑤与⑥之间经文自此无缺——以下自 `c80/p025.json` 程序切片照录（%d 字·底本卷家具照录·承 §2.5 体例）；原「待 L.264b 全引」注闭账。\n\n'
       % cont_han + '\n\n'.join(cont) + '\n')
md = md[:i_block] + new + md[i_note_end:]
ml = re.search(r'^## 九[、　]台账[^\n]*\n', md, re.M)
assert ml
md = md[:ml.end()] + '- **L.525（2026-11-22）清账批**：§2.3a 尾「③④⑤余文待 L.264b 全引」**闭账**——余文 %d 字自 `c80/p025.json` 程序切片照录补入（tc %d-%d·至⑥开章·含底本卷家具·承 §2.5 体例）；本品①-⑩经文自此**全序无缺**。\n' % (cont_han, i_stop, i_end) + md[ml.end():]
io.open(fp, 'w', encoding='utf-8', newline='').write(md)
print('① P25 余文补入 ✓ (%d 字)' % cont_han)

# ══ ② P17/P18 藏译指针 ══
for pat in ['华严经细读_第十七部_*.md', '华严经细读_第十八部_*.md']:
    fp = gpat(pat)
    md = io.open(fp, encoding='utf-8').read()
    if 'L.525 藏译待勘' in md:
        print('skip:', pat[:12])
        continue
    m6 = re.search(r'^## 六[、　]', md, re.M)
    assert m6, pat
    md = md[:m6.start()] + '\n> **藏译对照待勘（L.525）**：本品藏译对应章（Phal chen le\u02bcu 次第）未勘〔未竟〕——补前不对录音/影像外源臆引（体例同 `P16` §六）。\n' + md[m6.start():]
    ml = re.search(r'^## 九[、　]台账[^\n]*\n', md, re.M)
    if ml:
        md = md[:ml.end()] + '- **L.525（2026-11-22）清账批**：藏译对照待勘指针（体例同 P16·不臆引）。\n' + md[ml.end():]
    io.open(fp, 'w', encoding='utf-8', newline='').write(md)
    print('② 藏译指针:', pat[:12])
print('L.525 done')
