# -*- coding: utf-8 -*-
"""正文引文抽取式核验：把正文的引文逐条回源到 CBETA 底本。

与 verify_quotes.py（手写 needle 抽检）不同，本脚本从**正文**抽取引文，
新增／改写引文会自动进入核验。

口径：
  · 严格项 = 以「…」开头的 blockquote 引文（声称原文者），必须逐段见于底本；
  · 提示项 = 行内「…」（≥12 字），多为术语或转述，只报告不判失败。
底本比对时只保留汉字，故标点、空格差异不影响；引文中的省略号按段切分。

    python workspace/yogacara_guide/verify_inline.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MD = ROOT / 'docs/宗派研究/瑜伽师地论导读与重点阐释.md'
SRC = {'T30n1579': ROOT / 'data/references/cbeta/T30n1579.xml',
       'T30n1580': ROOT / 'data/references/cbeta/T30n1580.xml'}


def load(xml_path):
    raw = xml_path.read_text(encoding='utf-8')
    parts = re.split(r'<cb:juan n="(\d{3})" fun="open">', raw)
    chunks, spans, pos = [], [], 0
    for i in range(1, len(parts), 2):
        n = int(parts[i])
        b = ''.join(re.findall(r'[\u4e00-\u9fff]', re.sub(r'<[^>]+>', '', parts[i + 1])))
        spans.append((n, pos, pos + len(b)))
        chunks.append(b)
        pos += len(b)
    return ''.join(chunks), spans


def cjk(s):
    return ''.join(re.findall(r'[\u4e00-\u9fff]', s))


BASES = {k: load(v) for k, v in SRC.items()}


def locate(seg):
    for name, (text, spans) in BASES.items():
        p = text.find(seg)
        if p >= 0:
            j = next((s[0] for s in spans if s[1] <= p < s[2]), None)
            return f'{name}卷{j}'
    return None


def main():
    md = MD.read_text(encoding='utf-8')
    blocks = [m.group(1).strip() for m in re.finditer(r'^> (.+)$', md, re.M)]
    strict = [b for b in blocks if b.startswith('「')]
    inline = []
    for m in re.finditer(r'「([^「」]{12,})」', md):
        s = m.group(1)
        if not any(s in b for b in strict) and s not in inline:
            inline.append(s)

    ok = fail = 0
    for q in strict:
        segs = [cjk(x) for x in re.split(r'[…]{1,}', q)]
        segs = [x for x in segs if len(x) >= 6]
        bad = []
        vols = set()
        for s in segs:
            where = locate(s)
            if where:
                vols.add(where)
            else:
                bad.append(s)
        if bad:
            fail += 1
            print(f'[FAIL] {q[:44]}…')
            for s in bad:
                print(f'        未匹配段：{s[:40]}')
        else:
            ok += 1
            print(f'[ ok ] {"、".join(sorted(vols))}  {q[:38]}…')

    print(f'\n严格引文 {len(strict)} 条：见于底本 {ok}，未匹配 {fail}')
    miss_inline = []
    for s in inline:
        parts = [cjk(x) for x in re.split(r'[…]{1,}', s)]
        parts = [x for x in parts if len(x) >= 6]
        if not parts or not all(locate(p) for p in parts):
            miss_inline.append(s)
    print(f'行内「…」{len(inline)} 条（提示，不计失败）：未匹配 {len(miss_inline)}')
    for s in miss_inline[:12]:
        print('   ·', s[:44])
    return 0 if fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
