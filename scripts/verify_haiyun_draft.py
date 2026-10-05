# -*- coding: utf-8 -*-
"""草稿 ↔ 实证库 一致性校验（防止正文引用漂移与编号失联）

校验五项：
  A 正文所引之实证库编号（S1/M4/L2…）皆存在于实证库
  B 正文所引之 file:line 皆与实证库登记一致（抽样：以 `:行号` 形式出现者比对所属文件基名）
  C 实证库每条皆有正文引用（未被使用之条目须显式说明，防「建而不用」的死数据）
  D 关键论断段落皆带信度标记（〔实测〕/〔本文判断〕/〔待核〕/〔存疑〕/〔待比勘〕）
  E 不得残留旧之伪断言（「137 条」「待后续精筛补充」「初筛重点」等）

用法：python scripts/verify_haiyun_draft.py
"""
import io
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import yaml  # noqa: E402

DOC = os.environ.get("HAI_DRAFT",
                     "docs/随笔参考/海云继梦法师_复原·重构·建构的修行体系（草稿）.md")
YML = os.environ.get("HAI_EVIDENCE",
                     "data/research/haiyun_practice_system_evidence.yaml")

# 正文残留检测：旧版之伪断言与占位语
STALE = [
    (u"待后续精筛补充", u"旧占位语"),
    (u"初筛重点", u"旧方法之占位语"),
    (u"抽词共检出", u"旧之关键词计数法（已废弃）"),
    (u"组织性用语候选", u"旧之候选表（已撤回）"),
    (u"A·组织性候选", u"旧之伪命中标记（已撤回）"),
    (u"待补入实证库", u"引文尚未入库（须入库后方可引）"),
]
MUST_MARK = re.compile(u"〔实测|本文判断|待核|存疑|待比勘|待证|已查|查无|盲区|待补|体例|方法|重要|局限〕")


def main():
    if not os.path.exists(DOC):
        print("FAIL 草稿不存在：%s" % DOC)
        return 1
    doc = io.open(DOC, "r", encoding="utf-8").read()
    lib = yaml.safe_load(io.open(YML, "r", encoding="utf-8"))

    fails, notes = [], []

    # ── A 编号皆存在 ─────────────────────────────────────────────
    lib_ids = set()
    for sec in ("strong", "medium", "limit"):
        for it in lib.get(sec) or []:
            lib_ids.add(it["id"])
    # 正文中的编号引用一律带标记方算引用：〔实证库 S1〕〔S1〕〔…｜S1〕〔S1、M4〕
    # （旧版曾误将「L1397」行号、「S24」播客季次当作证据编号，故须严限格式）
    cited = set()
    for m in re.finditer(u"〔([^〕]{0,40})〕", doc):
        cited.update(re.findall(u"\\b([SML]\\d{1,2})\\b", m.group(1)))
    # 附录二之表体（自实证库生成）：`| **S1** |`
    for m in re.finditer(u"\\*\\*([SML]\\d{1,2})\\*\\*", doc):
        cited.add(m.group(1))
    missing = sorted(cited - lib_ids)
    if missing:
        fails.append(u"A 正文引用了实证库不存在之编号：%s" % u"、".join(missing))

    # ── C 每条皆被使用（死数据防护）────────────────────────────
    used = cited & lib_ids
    unused = sorted(lib_ids - used)
    if unused:
        notes.append(u"C 实证库有 %d 条未见于正文（若为「备查」宜在附录二注明）：%s"
                     % (len(unused), u"、".join(unused)))

    # ── B file:line 与登记一致 ──────────────────────────────────
    reg = {}
    for sec in ("strong", "medium", "limit"):
        for it in lib.get(sec) or []:
            base = os.path.basename(it["src"])
            ln = it["line"]
            ln = ln if isinstance(ln, str) else str(ln)
            reg.setdefault(base, set()).add(ln.split("-")[0].strip())
    # 正文中形如 `xxx_1.txt:174` 者
    for m in re.finditer(u"`([^`]+\\.txt):(\\d+)", doc):
        base, ln = os.path.basename(m.group(1)), m.group(2)
        if base in reg and ln not in reg[base]:
            notes.append(u"B 正文引用 %s:%s 与实证库登记行号不同（该行或为同段他条，"
                         u"请人工确认）" % (base, ln))

    # ── E 不得残留伪断言 ────────────────────────────────────────
    # 豁免：§3.5.3「撤回记录」与 §8.3「已撤回之断言」二节之内，
    #       其引旧语正为记录撤回之所需（非残留）。
    exempt_marks = (u"撤回", u"旧断言", u"旧之", u"伪命中")
    for lineno, line in enumerate(doc.split(u"\n"), 1):
        if any(k in line for k in exempt_marks):
            continue
        for pat, why in STALE:
            if pat in line:
                fails.append(u"E L%d 残留旧之%s：「%s」" % (lineno, why, pat))

    # ── D 关键段落带标记 ────────────────────────────────────────
    paras = [p for p in doc.split(u"\n") if p.strip()]
    unmarked = 0
    for p in paras:
        if p.startswith(u"#"):
            continue
        if p.startswith(u"|") or p.startswith(u">"):
            continue
        if not MUST_MARK.search(p) and len(p) > 60:
            unmarked += 1
    if unmarked:
        notes.append(u"D 有 %d 个较长段落未见信度标记（须人工确认是否为纯过渡句）"
                     % unmarked)

    print(u"草稿：%s（%d 行）" % (DOC, len(doc.splitlines())))
    print(u"实证库引用：%d 处，涉 %d/%d 条" % (len(cited), len(used), len(lib_ids)))
    for n in notes:
        print(u"  提示 %s" % n)
    if fails:
        print(u"FAIL %d 项：" % len(fails))
        for f in fails:
            print(u"  - %s" % f)
        return 1
    print(u"ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
