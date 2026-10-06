# -*- coding: utf-8 -*-
"""生成草稿附录二·原话辑录表 与 附录五·祖典比勘要点表：
两者皆自证据库直出，杜绝手工转录之笔误。

用法：python scripts/build_haiyun_appendix.py
"""
import io
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import yaml  # noqa: E402

YML = "data/research/haiyun_practice_system_evidence.yaml"
T1YML = "data/research/t1_bikan_evidence.yaml"
DOC = "docs/随笔参考/海云继梦法师_复原·重构·建构的修行体系.md"
SEC_TITLE = u"## 附录二：原话辑录表（自实证库生成）"
# 旧标题有二形（目录行「附录二：…」与正文行「## 附录二：…」），皆须容纳
SEC_LEGACY = [u"## 附录二：拼图·贯通·摸索原话辑录表（初筛）",
              u"## 附录二"]
SEC_END = u"## 附录七"

SEC5_TITLE = u"## 附录五：祖典比勘要点表（自 T1 比勘库生成）"
# 附录五同须容二形：本批新立标题，与可能残留之旧形
SEC5_LEGACY = [SEC5_TITLE, u"## 附录五"]

SEC_LABEL = {
    "strong": u"A类·强自述（拼图／摸索／补块／接线／标准作业流程）",
    "medium": u"A类·体系要素（复原、接续、改良，有自述语气）",
    "limit": u"A类·限制与警戒（划界反证）",
}


def clip(q, n=110):
    q = q.replace(u"\n", u" ")
    return q if len(q) <= n else q[:n] + u"……"


def main():
    with io.open(YML, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    out = [SEC_TITLE, u"",
           u"〔体例〕本表由 `scripts/build_haiyun_appendix.py` 自 "
           "`data/research/haiyun_practice_system_evidence.yaml` 直出，"
           u"**非手工转录**。原文以「…」节引处已在「引文」栏标出；"
           u"完整逐字原文见实证库。所有条目经 "
           "`scripts/verify_haiyun_evidence.py` 回源校验（行号＋字串双向）。", u""]

    n = 0
    for sec in ("strong", "medium", "limit"):
        out.append(u"### %s" % SEC_LABEL[sec])
        out.append(u"")
        out.append(u"| 编号 | 主题 | 出处 | 原文节引 | 判读要点 |")
        out.append(u"|------|------|------|----------|----------|")
        for it in doc.get(sec) or []:
            n += 1
            base = os.path.basename(it["src"])
            out.append(u"| **%s** | %s | `%s:%s` | %s | %s |" % (
                it["id"], it["key"], base, it["line"],
                clip(it["quote"]), clip(it.get(u"判读", u""), 60)))
        out.append(u"")

    out.append(u"### 否定性记录（经检索而查无者，与「未查」分记）")
    out.append(u"")
    out.append(u"| 编号 | 所查项 | 状态 | 结论摘要 |")
    out.append(u"|------|--------|------|----------|")
    for nf in doc.get("negative_findings") or []:
        out.append(u"| **%s** | %s | **%s** | %s |" % (
            nf["id"], nf["项"], nf["状态"], clip(nf["结论"], 80)))
    out.append(u"")
    out.append(u"〔说明〕此四项之价值与正面证据相埒：N1、N2 使本文**不代拟**"
               u"法师未曾说过之语（编务总则第 3 条·严禁假信息）；"
               u"N3 立「拼图」一词之语义边界。详见各条「检索范围」与「实际命中」。")
    out.append(u"")
    out.append(u"〔L.112 订正·不容略〕**N1／N4 之原判已就「走错／搞错」一类"
               u"撤回**，经复检补立 S11–S14（法师自述其摸索弯路之实录）、"
               u"M8（一错再错为学习必经）、L5（走错之必然性）。"
               u"故先前据 N1／N4 而作「法师未自述弯路」之断**已失效**，"
               u"本文相关处均已改正。原判一并留痕，以存其误——"
               u"**否定性结论之脆弱度高于肯定性结论**，其立须三项齐备"
               u"（检索式全文／检索范围／命中之排除依据），见 `rules.md` §J3。")
    out.append(u"")

    block = u"\n".join(out)

    with io.open(DOC, "r", encoding="utf-8") as f:
        t = f.read()

    # 旧「附录二：」目录行（无 ## 前缀）一并去掉，避免与新标题重复
    t = t.replace(u"附录二：拼图·贯通原话辑录表（file_path:line_range｜原文｜语境｜倾向｜信度）\n", u"")
    s = min([x for x in (t.find(y) for y in SEC_LEGACY) if x != -1])
    e = t.index(SEC_END)
    t = t[:s] + block + u"\n---\n\n" + build_appendix5() + u"\n---\n\n" + t[e:]
    with io.open(DOC, "w", encoding="utf-8") as f:
        f.write(t)

    print("附录二已重建：%d 条证据 ＋ %d 条否定性记录"
          % (n, len(doc.get("negative_findings") or [])))


def build_appendix5():
    """附录五·祖典比勘要点表：自 T1 比勘库 conclusions 直出。"""
    with io.open(T1YML, "r", encoding="utf-8") as f:
        t1 = yaml.safe_load(f)

    cons = t1.get("conclusions") or []
    counts = (t1.get("meta") or {}).get("counts") or {}

    out = [SEC5_TITLE, u"",
           u"〔体例〕本表由 `scripts/build_haiyun_appendix.py` 自 "
           "`data/research/t1_bikan_evidence.yaml` 之 `conclusions` 直出，"
           u"**非手工转录**；所依 C 条引文之逐字回源由 `scripts/t1_quote.py --check` 强制"
           u"（%d 条零失配），判定与理由之现行文本以该库为准。"
           u"附录二为 **T0（法师原话）**侧，本附录为 **T1（祖典注疏）**侧，二者不相混。"
           % counts.get("total", len(t1.get("quotes") or [])),
           u"", u"### 一、五节判定总表", u"",
           u"| 节 | 主题 | 判定 | 依据条目 | 附加界限 |",
           u"|---|---|---|---|---|"]

    for c in cons:
        out.append(u"| §%s | %s | %s | %s | %s |" % (
            c["sec"], c.get("topic", u""),
            c.get("判", u""),
            u"、".join(c.get("依") or []),
            clip(c.get(u"附") or u"—", 70)))

    out += [u"", u"### 二、逐节理由（全文，不节引）", u""]
    for c in cons:
        out.append(u"**§%s %s**" % (c["sec"], c.get("topic", u"")))
        out.append(u"")
        out.append(u"- **判定**：%s" % c.get("判", u""))
        out.append(u"- **理由**：%s" % (c.get(u"理由") or u"—"))
        if c.get(u"附"):
            out.append(u"- **界限**：%s" % c[u"附"])
        if c.get(u"判准"):
            out.append(u"- **判准**：%s" % c[u"判准"])
        out.append(u"")

    out.append(u"〔说明〕五节之判定**非本表所立**，而是 §5.1–5.5 正文所结之案；"
               u"本表仅将其判定、依据与理由按节汇出，以便与附录二（T0 侧）对读。"
               u"凡标〔待核〕〔待补〕者为**尚未结案**之项，不得读作已断。")
    out.append(u"")
    return u"\n".join(out)


if __name__ == "__main__":
    main()
