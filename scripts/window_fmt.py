# -*- coding: utf-8 -*-
"""window_fmt.py — 窗体规范 v2 引擎（L.528）

对长单行 blockquote（'> ' 开头·汉字>200·非按语行）做两步改造：
  ①科目界标：句首的 釋名/來意/宗趣/釋文 前插【釋名】【來意】【宗趣】【釋文】（插入字符·不动原文）
  ②按句义分段：每段 ≤150 汉字；段界优先落在界标处
硬校验：去空白并剥离【】后，改造前后逐字全等——保证「不改一字」（断言失败即回滚该行）。

幂等性：界标插入后其前字符为'】'，不满足句首前瞻——二次运行自然零改动。
【疏】【論】原文括注保持不动。
可读规范（本引擎即规范本体·后续取窗管线沿用）：长引文必须分段+界标；本引擎与
web/demo/scripts/rufajie_can_lib.py 的 _fmt_quote 同逻辑（can 页生成时直接套用）。
"""
import re

HAN = re.compile(r'[\u3400-\u9fff]')
CAT = {'釋名': '【釋名】', '來意': '【來意】', '宗趣': '【宗趣】', '釋文': '【釋文】'}
MARK_RE = re.compile(r'(?<=[。；！？」』])([初二三四五六七八九十]{1,2}?)(釋名|來意|宗趣|釋文)')
SENT_RE = re.compile(r'[^。；！？」』]*[。；！？」』]|[^。；！？」』]+$')
LIMIT = 150


def canon(s):
    s = re.sub(r'【[^】]*】', '', s)   # 界标整块移除（括内文字系新增·不计守恒）
    return re.sub(r'[\s>]', '', s)


def add_marks(t):
    def f(m):
        return CAT[m.group(2)] + m.group(0)
    return MARK_RE.sub(f, t)




def soft_split(sent, limit=200):
    """超长句在 ，、 处软切；全无标点的 OCR 联句则定距硬切（纯断行·守恒）。"""
    if len(HAN.findall(sent)) <= limit:
        return [sent]
    if not re.search(r'[，、]', sent):
        return [sent[i:i+120] for i in range(0, len(sent), 120)]
    parts = re.findall(r'[^，、]*[，、]|[^，、]+$', sent)
    out = []
    cur = ''
    for p in parts:
        if cur and len(HAN.findall(cur)) >= limit:
            out.append(cur)
            cur = ''
        cur += p
    if cur:
        out.append(cur)
    return out


def para_split(t, limit=LIMIT):
    sents = []
    for s in SENT_RE.findall(t):
        sents.extend(soft_split(s, limit=LIMIT))
    paras = []
    cur = ''
    for s in sents:
        if cur and (len(HAN.findall(cur)) >= limit or s.startswith('【')):
            paras.append(cur)
            cur = ''
        cur += s
    if cur.strip():
        paras.append(cur)
    return paras


def fmt_line(line):
    """输入单行（含 '> ' 前缀），返回多行 blockquote 文本（或原行）。"""
    if not line.startswith('> ') or line.startswith('> **'):
        return line, 0, 0
    text = line[2:]
    if len(HAN.findall(text)) < 200:
        return line, 0, 0
    marked = add_marks(text)
    paras = para_split(marked)
    joined = '\n> '.join(paras)
    assert canon(text) == canon(joined), 'fmt_line 硬校验失败：不改一字被违反'
    return '\n'.join('> ' + p for p in paras), 1, len(marked) - len(text)


def fmt_file(path, apply=True):
    """对单文件全部合格行改造；返回 (行数·界标数·写否)。"""
    import io
    md = io.open(path, encoding='utf-8').read()
    out = []
    n_lines = n_marks = 0
    for line in md.split('\n'):
        new, hit, mk = fmt_line(line)
        if hit:
            n_lines += 1
            n_marks += mk
        out.append(new)
    if apply and n_lines:
        io.open(path, 'w', encoding='utf-8', newline='').write('\n'.join(out))
    return n_lines, n_marks


if __name__ == '__main__':
    import sys, glob
    sys.stdout.reconfigure(encoding='utf-8')
    apply = '--apply' in sys.argv
    pats = [a for a in sys.argv[1:] if a != '--apply'] or ['docs/经学文献/华严经细读/*/华严经细读_第*部_*.md']
    tot_l = tot_m = 0
    for pat in pats:
        for fp in sorted(glob.glob(pat, recursive=True)):
            nl, nm_ = fmt_file(fp, apply)
            if nl:
                tot_l += nl
                tot_m += nm_
                print('%-42s %3d 行 · 界标 %3d' % (fp[-42:], nl, nm_))
    print('合计 %d 行 · 界标 %d（apply=%s）' % (tot_l, tot_m, apply))
