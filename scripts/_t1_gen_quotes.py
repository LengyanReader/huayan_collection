# -*- coding: utf-8 -*-
"""生成 t1_bikan_evidence.yaml 之引文块（L.109 立·构建器，保留以备重跑）

〔体例〕引文**一律经 t1_quote.cut() 程序抽取**，不手录。

〔L109·坑·务必守〕**不得**用 shell 重定向（`python … > frag`）取本脚本输出——
PowerShell / cmd 会按 locale（cp1252）重编码 stdout，中文与繁体逐字成乱码
（实测「初列四諦…」→「σê¥σêùσ¢¢…」），而 key/sec 等写在 .py 源码里者
不受影响，于是**半本文件坏、半本完好，肉眼极易漏过**。
故此处**由 Python 自己写文件**（显式 UTF-8 + newline）。

用法：python scripts/_t1_gen_quotes.py [输出路径]
     默认 .tmp_t1_quotes.frag
"""
import io
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, "scripts")
import t1_quote as Q  # noqa: E402

# (id, 节, code, line, a, b)
SPEC = [
    ("C01", "5.1", "T1732", 2764, 5, 22),
    ("C02", "5.1", "T1732", 2921, 13, 28),
    ("C03", "5.2", "T1735", 7206, 18, 29),
    ("C04", "5.2", "T1735", 7207, 1, 18),
    ("C05", "5.2", "T1735", 7207, 19, 27),
    ("C06", "5.2", "T1733", 18320, 8, 17),
    ("C07", "5.2", "X0223", 1205, 6, 30),
    ("C08", "5.2", "X0223", 1206, 1, 17),
    ("C09", "5.2", "X0223", 1923, 3, 12),
    ("C10", "5.2", "X0223", 1923, 15, 20),
    ("C11", "5.2", "X0223", 1913, 13, 30),
    ("C12", "5.3", "T1735", 2432, 15, 20),
    ("C13", "5.3", "T1735", 2434, 4, 12),
    ("C14", "5.3", "T1735", 2439, 17, 30),
    ("C15", "5.3", "T1735", 2440, 10, 19),
    ("C16", "5.3", "T1735", 2441, 1, 8),
    ("C17", "5.3", "X0223", 7065, 11, 29),
    ("C18", "5.4", "T1735", 908, 4, 13),
    ("C19", "5.4", "T1735", 909, 4, 30),
    ("C20", "5.4", "T1735", 910, 1, 30),
    ("C21", "5.4", "T1735", 911, 1, 30),
    ("C22", "5.4", "T1735", 912, 1, 26),
    ("C23", "5.4", "T1736", 3807, 14, 24),
    ("C24", "5.5", "X0223", 4531, 22, 30),
    ("C25", "5.5", "X0223", 4532, 1, 12),
    ("C26", "5.5", "X0223", 5647, 22, 29),
    ("C27", "5.5", "X0223", 5648, 1, 3),
]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else ".tmp_t1_quotes.frag"
    buf = []
    for bid, sec, c, l, a, b in SPEC:
        q = Q.cut(c, l, a, b)
        if '"' in q:
            raise SystemExit("quote 含双引号，YAML 需转义：%s" % bid)
        buf.append('  - id: %s\n    sec: "%s"\n    code: %s\n'
                   '    src_line: %d\n    quote: "%s"\n'
                   % (bid, sec, c, l, q))
    txt = "".join(buf)
    io.open(path, "w", encoding="utf-8", newline="\n").write(txt)
    # 自校：写后重读，若含 mojibake 特征序列即失败（不靠肉眼）
    back = io.open(path, encoding="utf-8").read()
    if back != txt:
        raise SystemExit("【写后回读不一致】疑编码受损：%s" % path)
    for probe in ("四諦", "解脫", "普賢", "威儀"):
        if probe not in back:
            raise SystemExit("【繁体串缺失·疑乱码】%s 无「%s」" % (path, probe))
    print("已写 %s（%d 条，%d 字节；写后回读一致，繁体自校通过）"
          % (path, len(SPEC), len(back.encode("utf-8"))))


if __name__ == "__main__":
    main()
