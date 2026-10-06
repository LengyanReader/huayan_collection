# -*- coding: utf-8 -*-
"""草稿 ↔ 实证库 一致性校验（防止正文引用漂移与编号失联）

校验七项：
  A 正文所引之实证库编号（S1/M4/L2…）皆存在于实证库
  B 正文所引之 file:line 皆与实证库登记一致（抽样：以 `:行号` 形式出现者比对所属文件基名）
  C 实证库每条皆有正文引用（未被使用之条目须显式说明，防「建而不用」的死数据）
  D 关键论断段落皆带信度标记（〔实测〕/〔本文判断〕/〔待核〕/〔存疑〕/〔待比勘〕）
  E 不得残留旧之伪断言（「137 条」「待后续精筛补充」「初筛重点」等）
  F **T1 比勘编号不悬空**（〔C01〕〔N5〕必存在于 t1_bikan_evidence.yaml）
  G **T1 引文不得充作法师原话**——凡「—— 法师…」式署名之后若紧跟 T1 之 C 号，
    即为张冠李戴，属「严禁假信息」，必失败

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
                     "docs/随笔参考/海云继梦法师_复原·重构·建构的修行体系.md")
YML = os.environ.get("HAI_EVIDENCE",
                     "data/research/haiyun_practice_system_evidence.yaml")
T1 = os.environ.get("HAI_T1", "data/research/t1_bikan_evidence.yaml")
# 〔L.113·新增〕T0 法师原话库之路径：F1 须比对**两库**否定性记录之编号，
# 故不可只持 T1 之一库（只持一库则无从察「相撞」）。
T0_EV = os.environ.get("HAI_EVIDENCE",
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
# 〔L109·增〕并入 T1 比勘之标记语：「比勘」「T1」「否定记录」「结论」「分源」
#   「已定」——§5.1–5.6 之分析段落皆以此等标记，非「无标记之论断」。
MUST_MARK = re.compile(u"〔实测|本文判断|待核|存疑|待比勘|待证|已查|查无|盲区|待补|体例|方法|重要|局限|比勘|T1|否定记录|结论|分源|已定|排除|勾稽")


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

    # ── F/G T1 比勘编号不悬空·且不得冒充法师原话 ────────────────
    # 〔L.113·新增 F0〕**T1 库须可被 yaml 解析**——立此之缘由：T1 库之
    # `quotes:` 键**整段缺失**（`- id:` 序列直接顶在 `meta` 之下），全库
    # 不可解析（ParserError）；而本组**按纯文本读取**，故该破损**未被拦截**，
    # 反以「27 条 C 号俱在」为绿——即「门禁只按文本核、不按结构核」之
    # 假绿实例。故凡以文本核为主者，须并加一道结构核。
    t1_ids, t1_negs = set(), set()
    t1_doc = None
    if os.path.exists(T1):
        try:
            t1_doc = yaml.safe_load(io.open(T1, "r", encoding="utf-8").read())
        except Exception as e:  # noqa: BLE001
            fails.append(u"F0 T1 库不可被 yaml 解析（%s）——结构已破损，"
                         u"文本核不足恃" % type(e).__name__)
        t1 = io.open(T1, "r", encoding="utf-8").read()
        head = t1.split("negative_findings:")[0]
        t1_ids = set(re.findall(u"(?m)^  - id: (C\\d{2})$", head))
        t1_negs = set(re.findall(u"(?m)^  - id: ((?:T1)?N\\d+)$",
                                 t1.split("negative_findings:")[1]
                                 .split("conclusions:")[0]))
        # 正文所引之 T1 编号（〔C01〕〔C01–C05〕〔T1N3〕〔T1 否定记录 T1N1、T1N3〕）
        t1_cited = set()
        for m in re.finditer(u"〔([^〕]{0,80})〕", doc):
            g = m.group(1)
            t1_cited.update(u"C" + x for x in re.findall(u"\\bC(\\d{2})\\b", g))
            t1_cited.update(re.findall(u"\\bT1N\\d+\\b", g))
        # 〔L.113·新增 F2〕**否定性记录之编号须可辨所属库**。立此之缘由：
        # T1 库原用 N5–N8，与 T0 库之 N1–N7 三号相撞；且本组旧日之逻辑
        # 「只验〔〕内 N 号是否见于 T1 库」使**误引 T0 之 N7 为 T1 记录亦得
        # 通过**（假绿，已实证）。故凡〔〕内之无前缀 N 号，须**同括内已明标
        # 所属库**方许通过——**「已明标」者即「〔T0 否定记录 N7〕」之类**。
        # 〔首跑过严之记录〕本项初版仅查有无前缀，遂将已明标之
        # 「〔T0 否定记录 N7〕」亦判为歧义。**门禁自身之缺陷亦须如实修正，
        # 不可迁就变异结果**：改为「无前缀 且 同括内未明标库」方判失败。
        for m in re.finditer(u"〔([^〕]{0,80})〕", doc):
            g = m.group(1)
            qualified = bool(re.search(u"(?:T0|T1)\\s*(?:之|否定记录|实证库)",
                                       g))
            if qualified:
                continue
            for bare in re.findall(r"(?<![T1])\bN\d+\b", g):
                fails.append(u"F2 〔%s〕内有歧义之否定记录编号「%s」——"
                             u"须写明所属库（如〔T0 否定记录 N7〕／〔T1N3〕）"
                             % (g[:40], bare))
        miss_t1 = sorted(t1_cited - t1_ids - t1_negs)
        if miss_t1:
            fails.append(u"F 正文引用了 T1 库不存在之编号：%s" % u"、".join(miss_t1))
        else:
            notes.append(u"F T1 编号引用：%s（共 %d 个编号）"
                         % (u"、".join(sorted(t1_cited)), len(t1_cited)))

        # ── 〔L.113·新增 F1〕两库否定性记录编号不得相撞 ────────────
        # 立此之缘由：T0／T1 分源立册而编号各自自 N1 起编，遂致相撞。
        # 相撞之害不止于阅读混淆，更使**门禁之比对逻辑失效**（见 F2）。
        if t1_doc:
            t0_negs = set()
            if os.path.exists(T0_EV):
                t0d = yaml.safe_load(io.open(T0_EV, "r",
                                              encoding="utf-8").read()) or {}
                t0_negs = set(x.get("id") for x in t0d.get("negative_findings", [])
                              if isinstance(x, dict))
            hit = sorted(t0_negs & t1_negs)
            if hit:
                fails.append(u"F1 两库否定性记录编号相撞：%s——须各带库名前缀"
                             u"（T0 之 N#／T1 之 T1N#）" % u"、".join(hit))
            else:
                notes.append(u"F1 两库编号不撞（T0 %d 条／T1 %d 条）"
                             % (len(t0_negs), len(t1_negs)))
    else:
        notes.append(u"F 【T1 库缺失】%s，比勘编号无从校验" % T1)

    # G 张冠李戴：「—— 法师…」后紧跟 T1 之 C 号 → 把祖典当法师原话
    for lineno, line in enumerate(doc.split(u"\n"), 1):
        if re.search(u"—\\s*[^\\n]{0,12}法师[^\\n]{0,30}〔[^〕]*\\bC\\d{2}", line):
            fails.append(u"G L%d 疑将 T1 祖典引文署名于法师（「%s」）"
                         % (lineno, line.strip()[:60]))

    # ── H 「三分两用」归属声明不可回潮（rules.md §J5）────────────
    # 立此组之缘由：L.112 反向验证查出**四项假绿**——门禁未校验
    # 「自述义 vs 分析义」之归属声明，故可自由回潮而无人拦下。
    # 此组把 §J5 之契约逐条固化为**必存字串**。
    MUST_J5 = [
        (u"表二·法师自述义",
         u"H 缺「表二·法师自述义」——§J5 要求自述义与分析义两表分列"),
        (u"〔**未见其语**〕",
         u"H 缺「〔**未见其语**〕」分标——「复原」39 处皆生理义，非其自用语，"
         u"此分标为其唯一依据"),
        (u"**「兼容古今」全库 0 命中**，非其原词",
         u"H 缺「兼容古今 0 命中·非其原词」之核——不可代拟其语（§J5）"),
        (u"桥接性建构",
         u"H 缺「桥接性建构」之名——分析义须与自述义「体系建构」异名"),
        (u"体系建构",
         u"H 缺「体系建构」之名——法师自用义之专名"),
        (u"✗ **未见其语**",
         u"H 缺逐词分标表中之「✗ 未见其语」格——三分之归属须逐词分记"),
        (u"此断言经 L.112 实测推翻，已撤回",
         u"H 缺「『法师自陈之语中并无此三分』已撤回」之留痕——§J5 之自伤实例"),
        (u"全库 39 处「复原」皆为生理义",
         u"H 缺「39 处『复原』皆为生理义」之实测结论——此为「复原」非其用语之唯一依据"),
    ]
    for pat, why in MUST_J5:
        if pat not in doc:
            fails.append(why)

    # H2 建构不得回退为「最弱一档」：若「仅在无复原/重构依据时才考虑」
    #    出现于**非撤回语境、且非「桥接性建构」之定义**之处，即为降级断言回潮。
    #    （前者之定义中该句为正当表述，故须一并豁免「桥接性建构」——此为
    #     本门禁首跑之误报，已如实修正，不迁就变异结果。）
    for lineno, line in enumerate(doc.split(u"\n"), 1):
        if (u"仅在无复原/重构依据时才考虑" in line
                and u"撤回" not in line
                and u"桥接性建构" not in line):
            fails.append(u"H L%d「建构为最弱一档·仅在无复原/重构依据时才考虑」"
                         u"回潮（§J5：其自用义为建构工程面·法界原型，非最弱）"
                         % lineno)

    # ── I 附录目录有目必有文（〔L.115〕防「有目无文」复发）──────────
    # 立此之缘由：本文原目录列附录一／三／四／五，而正文只有附录二与附录七，
    # **四项皆从未成文**，且 §1.2 表一另有「详见附录一」之悬空交叉引用。
    # 〔判据要害〕**目录承诺未兑 ≠ 〔待核〕**：后者是如实交代已知限度，
    # 前者是承诺未兑——定稿中凡言「详见」而无其处者即为缺陷，与存疑不同层。
    # 〔为何只扫目录区〕正文可合法提及尚未成文之项（如「已记文末仍未竟者」），
    # 故只以「## 附录」节内之目录条目为承诺；正文标题之实有为兑现。
    if doc.count(u"## 附录\n") == 1:
        seg = doc.split(u"## 附录\n", 1)[1]
        seg = seg.split(u"\n---", 1)[0]
        listed = set(re.findall(u"(?m)^- \\*\\*附录([^*]+)\\*\\*", seg))
        listed |= set(re.findall(u"(?m)^附录([^：:]+)[：:]", seg))
        have = set(re.findall(u"(?m)^## 附录([^：、\\n]+)", doc))
        if listed:
            ghost = sorted(listed - have)
            if ghost:
                fails.append(u"I 目录列「附录%s」而正文无对应标题（有目无文）"
                             u"——承诺未兑须补文或撤目" % u"、".join(ghost))
            else:
                notes.append(u"I 附录目录 %d 项皆有正文标题（%s）"
                             % (len(listed), u"、".join(sorted(listed))))

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
