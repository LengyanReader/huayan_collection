# -*- coding: utf-8 -*-
"""生成草稿附录二·原话辑录表：自实证库直出，杜绝手工转录之笔误。

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
DOC = "docs/随笔参考/海云继梦法师_复原·重构·建构的修行体系（草稿）.md"
SEC_TITLE = u"## 附录二：原话辑录表（自实证库生成）"
# 旧标题有二形（目录行「附录二：…」与正文行「## 附录二：…」），皆须容纳
SEC_LEGACY = [u"## 附录二：拼图·贯通·摸索原话辑录表（初筛）",
              u"## 附录二"]
SEC_END = u"## 附录七"

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

    block = u"\n".join(out)

    with io.open(DOC, "r", encoding="utf-8") as f:
        t = f.read()

    e = t.index(SEC_END)
    s = min(t.index(x) for x in SEC_LEGACY if x in t)
    # 旧「附录二：」目录行（无 ## 前缀）一并去掉，避免与新标题重复
    t = t.replace(u"附录二：拼图·贯通原话辑录表（file_path:line_range｜原文｜语境｜倾向｜信度）\n", u"")
    s = min([x for x in (t.find(y) for y in SEC_LEGACY) if x != -1])
    e = t.index(SEC_END)
    t = t[:s] + block + u"\n---\n\n" + t[e:]
    with io.open(DOC, "w", encoding="utf-8") as f:
        f.write(t)

    print("附录二已重建：%d 条证据 ＋ %d 条否定性记录"
          % (n, len(doc.get("negative_findings") or [])))


if __name__ == "__main__":
    main()
