#!/usr/bin/env python3
"""quote_from_cbeta.py — 把文稿中的经文引文回填为 CBETA 原字形（繁体·异体·罕字）

缘起（编务原则：原文是什么语言就用什么，简体与英文只作说明性语言）：
中文经卷的「原文」即 CBETA 所录字形。凡引经一律照原字形，不作简繁转换，
方能保住异体（覩/睹）、罕字（𢔌）、专名正体（毘盧遮那）等一经转换即失的信息。

本工具不是简繁转换器，而是**回源对齐器**：
  1. 取出文中标记为经文的引文块（默认 `> **经文**`）；
  2. 以「由经证经」得到的简→繁字表（见 cbeta_s2t.py，由 T279 自身反推）
     作候选，在 CBETA 纯文本的**汉字投影**中定位同段；
  3. 逐字对齐后，用 CBETA 原字替换文稿中的字（**保留作者的标点、括号与按语**）；
  4. 定位失败或不稳定者**整块**保留原样并列为待核，绝不猜补、绝不半改。

四条不肯让步的规矩（皆出于「宁留待核，不可失真」）：
  · **整块全对齐才动手**：只换「对得上的字串」会让同一段引文半繁半简，
    读者无从判断哪几字是经文原貌，比原本更坏。
  · **只取字形，不改用字**：回源换回的正是 CBETA 自己的字，与底本用字一致；
    但凡定位不上（如作者转述、意译、按语）即整块弃用，不作「顺手订正」。
  · **标点不参与比对**：各本标点不一（本文「复次持国乾闼婆王」／CBETA「復次，
    持國乾闥婆王」），故只取汉字投影比对，另存下标表以便回映原字。
  · **歧义字折叠只在匹配期**：干可作乾/幹/干，一字多形无法唯一定位，故折叠后比对，
    落笔仍取 CBETA 原字；折叠不及者宁可不改。

用法：
  quote_from_cbeta.py <文稿.md> [--xml T279.xml] [--marker 经文] [--apply]

默认 dry-run：只报告将改之处与待核清单；--apply 才写回。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cbeta_s2t
from cbeta_s2t import CJK, CbetaS2T

def _default_xml() -> Path:
    """CBETA XML 优先取环境变量，其次取本篇旁置之资料目录，最后回退旧临时路径。"""
    env = os.environ.get("CBETA_T279_XML")
    if env:
        return Path(env)
    local = Path(__file__).resolve().parent.parent / "data" / "references" / "cbeta" / "T10n0279.xml"
    if local.exists():
        return local
    return Path(r"C:\Users\data\AppData\Local\Temp\opencode\t10n0279.xml")


DEFAULT_XML = _default_xml()

# 本项目各文稿的「底本统一体字」：文稿凡例（如《世主妙严品》凡例七）已声明
# 者，视为遵底本而非待核。值为「底本用字 → 经中对应正字」之可能集。
BASE_VARIANTS = {
    "华严经细读_第一部_世主妙严品.md": {
        "琉": "瑠", "疏": "踈", "晖": "輝", "览": "覽",
        "遍": "徧", "睹": "覩", "阎": "閻", "闲": "閑",
    },
}

_proj_cache: dict = {}


def sutra_text(xml: Path) -> str:
    raw = xml.read_text(encoding="utf-8")
    return re.sub(r"<[^>]+>", "", raw).replace("\n", "")


def cjk_projection(sutra: str):
    """(汉字投影串, 原字下标表)。

    标点各本不一，若连标点一并比对则处处不合；故只取汉字成串比对，
    另存下标表以便回映 CBETA 原字。投影动辄数十万字，只建一次。
    """
    key = id(sutra)
    if key not in _proj_cache:
        chars, idx = [], []
        for i, ch in enumerate(sutra):
            if CJK.match(ch):
                chars.append(ch)
                idx.append(i)
        _proj_cache[key] = ("".join(chars), idx)
    return _proj_cache[key]


def fold_map(eng: CbetaS2T) -> dict:
    """歧义字折叠表：每个歧义字的经中诸形，一律折到「其中最常见者」。

    只用于匹配（阿脩羅之脩与修行之修、乾/幹/干、鹹/咸…），不用于落笔；
    落笔一律取 CBETA 原字，故折叠不影响回填结果的正确性。
    缓存以字表条数为键——字表随取用而增长，若按对象缓存，折叠表会停在
    「只见过前几个字」的旧快照上，害得本该折叠的字依旧对不上。
    """
    key = ("fold", id(eng), len(eng.table))
    if key not in _proj_cache:
        table = {}
        for c, rec in eng.table.items():
            forms = rec.get("forms")
            if not forms or len(forms) < 2:
                continue
            counts = rec.get("counts") or {f: eng.counts.get(f, 0) for f in forms}
            canon = max(forms, key=lambda f: counts.get(f, 0))
            for f in forms:
                if f != canon:
                    table[f] = canon
            # 简体键字本身亦须折到同一代表字，否则候选串里留着「发」，
            # 而经中投影已折成「發」，永远对不上
            if c != canon:
                table[c] = canon
        _proj_cache[key] = table
    return _proj_cache[key]


def folded_proj(proj: str, table: dict) -> str:
    key = ("fproj", id(proj), len(table))
    if key not in _proj_cache:
        _proj_cache[key] = proj.translate(str.maketrans(table)) if table else proj
    return _proj_cache[key]


def align(query: str, sutra: str, eng: CbetaS2T):
    """Locate `query` (a simplified CJK run) in the 繁体 sutra.

    Returns (ok, cbeta_span, note). `cbeta_span` is CBETA's own text covering the
    same run, spliced back character-for-character. 候选字表由 T279 反推，
    故定位成功即等于「该段经文在 CBETA 中逐字如此」，无须再作相似度猜测——
    定位不上便是有出入，如实上报。
    """
    cand = eng.convert(query).translate(str.maketrans(fold_map(eng)))
    if not cand:
        return False, "", "空串"
    proj, idx = cjk_projection(sutra)
    p = folded_proj(proj, fold_map(eng)).find(cand)
    if p < 0:
        return False, "", "未定位"
    if len(cand) != len(query):
        return False, "", "长度不符"
    return True, "".join(sutra[idx[p + k]] for k in range(len(cand))), ""


def fix_block(text: str, sutra: str, eng: CbetaS2T, exempt: dict | None = None):
    """Re-source one 经文 block to CBETA glyphs, or leave it wholly untouched.

    `exempt` 为「底本用字 → 经中正字」之对应（文稿凡例已声明者，如《世主妙严
    品》凡例七之「瑠璃→琉璃、踈→疏、輝→晖、徧→遍、覩→睹」）。凡全句之 CJK
    字串与经中仅此等体字之差者，判为「遵底本」，保留底本写法，不算待核。
    """
    runs, cur = [], []
    for ch in text:
        if CJK.match(ch):
            cur.append(ch)
        else:
            if cur:
                runs.append("".join(cur))
            cur = []
    if cur:
        runs.append("".join(cur))

    ex_map = {}
    for base_ch, cbeta_chs in (exempt or {}).items():
        for c in cbeta_chs:
            ex_map[base_ch] = c
    ex_tr = str.maketrans(ex_map) if ex_map else {}

    bad, mapping, kept = [], [], []
    for q in runs:
        ok, span, note = align(q, sutra, eng)
        if ok and len(span) == len(q):
            mapping.append(span)
            kept.append(False)
            continue
        # 底本统一体字：先按凡例把底本用字换回经中正字，再定位一次；
        # 能定位即证「除体字外逐字无异」，判为遵底本，保留底本写法。
        if ex_tr:
            ok2, span2, note2 = align(q.translate(ex_tr), sutra, eng)
            if ok2 and len(span2) == len(q.translate(ex_tr)):
                mapping.append(q)
                kept.append(True)
                continue
        bad.append((q, note2 if ex_tr and note2 != "未定位" else note))
        mapping.append(q)
        kept.append(True)
    if bad:
        return text, {"applied": False, "aligned": False, "runs": len(runs),
                      "chars": 0, "unmatched": bad}

    # 逐字重建：CJK 字按其所属字串的对应位取 CBETA 原字，非 CJK 一律原样
    out, ri, ci = [], 0, 0
    for ch in text:
        if CJK.match(ch):
            span = mapping[ri]
            out.append(span[ci])
            ci += 1
            if ci >= len(span):
                ri += 1
                ci = 0
        else:
            out.append(ch)
    fixed = "".join(out)
    return fixed, {"applied": fixed != text, "aligned": True, "runs": len(runs),
                   "chars": sum(1 for a, b in zip(text, fixed) if a != b), "unmatched": []}


def quote_blocks(lines, marker: str):
    """Yield (start_lineno, block_lines) for scripture quotes.

    只认严格标记行（`> **经文**`）；其后连续的 `>` 引用行（含空行）视为同一块，
    直至非引用行。
    """
    other = re.compile(r"^\s*>\s*\*\*" + re.escape(marker) + r"\*\*")
    cur = re.compile(r"^\s*>\s*\*\*" + re.escape(marker) + r"\*\*")
    i = 0
    while i < len(lines):
        if cur.match(lines[i]):
            start = i + 1
            block = [lines[i]]
            j = i + 1
            while j < len(lines):
                if lines[j].strip() == ">" or other.match(lines[j]) or lines[j].lstrip().startswith(">"):
                    block.append(lines[j])
                    j += 1
                else:
                    break
            yield start, block
            i = j
        else:
            i += 1


def main() -> None:
    ap = argparse.ArgumentParser(description="经文引文回填 CBETA 原字形")
    ap.add_argument("doc", type=Path, help="待处理文稿（Markdown）")
    ap.add_argument("--xml", type=Path, default=DEFAULT_XML, help="CBETA T279 XML")
    ap.add_argument("--marker", default="经文", help="经文块标记（默认「经文」）")
    ap.add_argument("--exempt", default=None,
                    help="底本统一体字（JSON：{\"底本字\":\"经中正字\"}）；缺省依文稿名取内置表")
    ap.add_argument("--apply", action="store_true", help="写回文件（默认只报告）")
    args = ap.parse_args()

    exempt = args.exempt if args.exempt is not None else BASE_VARIANTS.get(args.doc.name, {})
    if isinstance(exempt, str):
        if exempt.strip():
            exempt = json.loads(exempt)
        else:
            exempt = {}

    sutra = sutra_text(args.xml)
    eng = CbetaS2T(sutra)
    lines = args.doc.read_text(encoding="utf-8").splitlines(keepends=True)

    blocks = list(quote_blocks(lines, args.marker))
    # 先把引文里出现的字全部问过经中，折叠表才建得全（修/脩、乾/幹之类
    # 要靠「同字多形皆见于经」才判得为歧义；字表未全则折叠表缺项）
    for _, block in blocks:
        for ch in "".join(block):
            if CJK.match(ch):
                eng.resolve(ch)

    head = re.compile(r"^(\s*>\s*\*\*" + re.escape(args.marker) + r"\*\*)")
    changed_blocks = aligned_blocks = tot_runs = tot_chars = 0
    skipped = []
    for start, block in reversed(blocks):
        # 标记本身（「**经文**」）是标签而非经文，须排除在回填之外
        m = head.match(block[0])
        prefix = block[0][:m.end()] if m else ""
        rest = [(block[0][m.end():] if m else block[0])] + block[1:]
        new_block, st = fix_block("".join(rest), sutra, eng, exempt)
        if st["applied"]:
            changed_blocks += 1
            tot_runs += st["runs"]
            tot_chars += st["chars"]
            lines[start - 1:start - 1 + len(block)] = [prefix + new_block]
        elif st["aligned"]:
            # 已回源、字串相符而本无须改字（如作者原已照 CBETA 原字抄录）
            aligned_blocks += 1
        else:
            skipped.append((start, st["unmatched"]))
    if args.apply:
        args.doc.write_text("".join(lines), encoding="utf-8")
    done = changed_blocks + aligned_blocks
    print(f"[{'APPLY' if args.apply else 'DRY-RUN'}] {args.doc.name}")
    print(f"  经文块 {len(blocks)}：回源定位 {done}（改字 {changed_blocks}｜原已合 {aligned_blocks}）"
          f"｜整块待核 {len(skipped)}"
          f"｜回填 CJK 字串 {tot_runs}｜实际换字 {tot_chars}")
    if skipped:
        print("  ── 整块待核（未改动；须作者亲自订正后重跑）")
        for ln, bad in skipped:
            print(f"    L{ln}")
            for q, note in bad:
                print(f"        [{note}] {q}")
    else:
        print("  待核 0：全部引文均已回源定位")
    n = eng.save()
    if n:
        print(f"  字表新增 {n} 字 → {eng.map_path.name}")


if __name__ == "__main__":
    main()
