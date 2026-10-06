# -*- coding: utf-8 -*-
"""《九九華嚴》OCR 立册门禁（L.111）

门禁目的：防止 `data/research/jj_huayan_lectures.yaml` 之「待校定」身份
被无声摘除、防止实测数字与源脱钩、防止出处失效、并把「既有语料未覆盖」
与「两源不一致」之混淆钉死。

七道校验：
  A  结构：立册存在且可解析，必备顶层键齐备
  B  实测对账：**重跑** jj_ocr_audit 之实测函数，逐集与 YAML 数字比对
            （**不信任** .tmp_jj_audit.json——临时产物不得成为事实来源）
  C  出处可点：src 文件存在、video_id 非空 11 位、url 含该 id（编务总则七）
  D  校定状态诚实：calibration 非「待校定」时，**必须**带 calibration_evidence
            且证据文件存在——防无凭据摘除「待校」
  E  U1 硬规则：T0 一手栈（T0_ROOT）**不得**覆盖本路径，OCR 稿不得充逐字依据
  F  否定记录：必备字段齐备；N-JJ1 必含「不可」限定（防「无命中」被读作「一致」）
  G  禁用表述：不得出现「已校定／完整无误／逐字无误／两源一致」等越界断言
  H  月份自洽：period 描述须覆盖逐集 title 所载之月份

反向验证（须如期失败，防门禁自身失效）：
  python scripts/verify_jj_lectures.py --mutate drop_calibration
  python scripts/verify_jj_lectures.py --mutate falsify_number
  python scripts/verify_jj_lectures.py --mutate break_url
  python scripts/verify_jj_lectures.py --mutate admit_t0
  python scripts/verify_jj_lectures.py --mutate soften_neg
  python scripts/verify_jj_lectures.py --mutate shout_verified
  python scripts/verify_jj_lectures.py --mutate drop_ep
  python scripts/verify_jj_lectures.py --mutate month_drift
"""
import argparse
import importlib.util
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

LIB = "data/research/jj_huayan_lectures.yaml"
AUDIT = "scripts/jj_ocr_audit.py"
T0_GUARD = "scripts/verify_haiyun_evidence.py"
TOP_KEYS = ["meta", "measured", "episodes_detail", "negative_findings",
            "limits", "usage_rules", "conclusions"]
NEG_FIELDS = ["id", "key", "probe", "result", "判读"]
# 〔L.111·自纠〕初版禁词过窄（只挡「已校定」），实测漏掉「逐字无误」
#   「完整无误」——越界断言并不只一种说法。故改为**按义族**列，且每族皆须命中。
# 〔L.111·自纠三·结构性修正〕初版为**单一禁词表 + 40 字语境豁免**，两处失效：
#   ① 假阴性——豁免窗口过宽（「不得手录」恰落在 40 字内，遂使「已校定」被豁免）；
#   ② 假阳性——「须回 T1 祖典或已校定之讲记」中对**他种材料**的合法提及被误杀。
#   根因：试图以**关键词窗口猜语义**。故改为**按字段性质分层**，不再猜：
#     HARD 禁词：任何位置皆不可出现（连「引用他人已校定」亦不得写此六词）；
#     STATE 禁词（「已校定／已核校」）：只在**断言字段**（meta.*／calibration／
#       conclusions[].判）裸禁——此三处必是**对本稿本身**之陈述；
#       规则/理由/判读/限度等**散文字段**合法提及他种材料之状态，予以豁免。
#   分层依据是**字段在本册中之角色**，可核对、可复跑，不依赖自然语言启发式。
BANNED_HARD = [
    ("完整无误", "完整性越界断言"),
    ("逐字无误", "逐字可靠性越界断言"),
    ("逐字可靠", "逐字可靠性越界断言"),
    ("两源一致", "无互证语料而宣称一致"),
    ("完全一致", "无互证语料而宣称一致"),
    ("无遗漏", "完整性越界断言"),
]
BANNED_STATE = [("已校定", "待校状态被摘除"), ("已核校", "待校状态被摘除")]
ASSERT_SCALARS = []   # 运行期填充：meta.* 之值 + 逐集 calibration + conclusions[].判


def load_audit():
    """复用 jj_ocr_audit 之实测函数——**同一份实现**，不复制逻辑"""
    spec = importlib.util.spec_from_file_location("jj_ocr_audit", AUDIT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutate", default="")
    args = ap.parse_args()

    fails = []
    if not os.path.exists(LIB):
        print("【缺立册】%s" % LIB)
        return 1
    text = io.open(LIB, encoding="utf-8").read()
    if args.mutate:
        text, ok = mutate(text, args.mutate)
        if not ok:
            print("【变异未生效】%s —— 变异器自身失效，测试无意义"
                  % args.mutate)
            return 2
    y = yaml.safe_load(text)

    # A 结构
    for k in TOP_KEYS:
        if k not in y:
            fails.append("A 缺顶层键 %s" % k)
    if fails:
        for f in fails:
            print(f)
        return 1

    # B 实测对账（重跑，不信 tmp JSON）
    A = load_audit()
    # 〔L.111·依交付者「後續會持續更新」〕集数**自动发现**——
    #   门禁不写死「12 集」，而是要求台账集集数 == 目录实测集数。
    #   故交付者一旦新增 ep13，门禁**立即**报「台账漏收」，而非静默通过。
    eps_found = A.discover_eps()
    neps_found = len(eps_found)
    rows = {r["ep"]: r for r in [A.audit_one(e) for e in eps_found]}
    det = y["episodes_detail"]
    if neps_found != y["meta"].get("episodes"):
        fails.append("B meta.episodes %s ≠ 目录实测 %d 集 —— **台账漏收新集**，"
                     "请重跑 jj_ocr_audit → _jj_build_lib"
                     % (y["meta"].get("episodes"), neps_found))
    got = sorted(d["ep"] for d in det)
    if got != sorted(eps_found):
        missing = [e for e in eps_found if e not in got]
        extra = [e for e in got if e not in eps_found]
        fails.append("B 逐集台账与目录实数不符：缺 %s／多余 %s"
                     % (missing or "无", extra or "无"))
    if len(det) != neps_found:
        fails.append("B 逐集条目数 %d ≠ 实测 %d" % (len(det), neps_found))
    for d in det:
        r = rows.get(d["ep"])
        if r is None:
            fails.append("B ep%02d 无实测对应" % d["ep"])
            continue
        for k_yaml, k_meas in (("cues", "cues"), ("han_chars", "han_chars"),
                               ("pipe_cues", "pipe_cues"),
                               ("declared_sec", "declared_sec"),
                               ("covered_sec", "covered_sec")):
            if d[k_yaml] != r[k_meas]:
                fails.append("B ep%02d %s 台账 %s ≠ 实测 %s"
                             % (d["ep"], k_yaml, d[k_yaml], r[k_meas]))
        if abs(d["coverage"] - r["coverage"]) > 1e-6:
            fails.append("B ep%02d coverage 台账 %.4f ≠ 实测 %.4f"
                         % (d["ep"], d["coverage"], r["coverage"]))
    m = y["measured"]
    for k, v in y["meta"].items():
        ASSERT_SCALARS.append(("meta.%s" % k, v))
    for d in det:
        ASSERT_SCALARS.append(("ep%02d.calibration" % d["ep"],
                               d.get("calibration", "")))
    for c in y["conclusions"]:
        for k, v in c.items():
            ASSERT_SCALARS.append(("conclusion[%s].%s" % (c.get("topic", "?"), k), v))
    tot_han = sum(r["han_chars"] for r in rows.values())
    if m["total_han_chars"] != tot_han:
        fails.append("B measured.total_han_chars %s ≠ 实测 %d"
                     % (m["total_han_chars"], tot_han))
    tot_cues = sum(r["cues"] for r in rows.values())
    if m["total_cues"] != tot_cues:
        fails.append("B measured.total_cues %s ≠ 实测 %d"
                     % (m["total_cues"], tot_cues))
    for k_meas, k_yaml in (("pipe_cues", "pipe_cues"),
                           ("simp_cues", "simp_cues"),
                           ("latin_cues", "latin_cues"),
                           ("latin_only_cues", "latin_only_cues"),
                           ("head_garbage_cues", "head_garbage_cues")):
        tot = sum(r[k_meas] for r in rows.values())
        if m[k_yaml] != tot:
            fails.append("B measured.%s %s ≠ 实测 %d"
                         % (k_yaml, m[k_yaml], tot))

    # C 出处可点
    for d in det:
        if not os.path.exists(d["src"]):
            fails.append("C ep%02d src 不存在：%s" % (d["ep"], d["src"]))
        vid = str(d["video_id"])
        if not re.match(r"^[A-Za-z0-9_-]{11}$", vid):
            fails.append("C ep%02d video_id 无效：%r" % (d["ep"], vid))
        if vid and vid not in d["url"]:
            fails.append("C ep%02d url 未含 video_id：%s" % (d["ep"], d["url"]))
        if not d["declared_sec"]:
            fails.append("C ep%02d declared_sec 为 0" % d["ep"])

    # D 校定状态诚实
    if "待校定" not in str(y["meta"].get("nature", "")):
        fails.append("D meta.nature 不再声明「待校定」—— 本册自我定性被摘除")
    for d in det:
        cal = d.get("calibration", "")
        if cal != "待校定":
            ev = d.get("calibration_evidence")
            if not ev or not os.path.exists(ev):
                fails.append("D ep%02d calibration=%r 却无有效 "
                             "calibration_evidence —— 疑似无凭据摘除「待校」"
                             % (d["ep"], cal))

    # E U1 硬规则：T0 一手栈不得覆盖本路径
    t0 = ""
    for ln in io.open(T0_GUARD, encoding="utf-8"):
        mm = re.match(r'^T0_ROOT\s*=\s*"([^"]+)"', ln.strip())
        if mm:
            t0 = mm.group(1)
    if not t0:
        fails.append("E 未能从 %s 读出 T0_ROOT" % T0_GUARD)
    elif det and det[0]["src"].startswith(t0 + "/"):
        fails.append("E U1 失效：OCR 稿已被纳入 T0 一手栈 %s —— 逐字不可靠之"
                     "材料不得充逐字依据" % t0)
    if det and "verify_haiyun_evidence" not in text:
        fails.append("E 立册未声明与 verify_haiyun_evidence 之分工（U1）")

    # F 否定记录
    negs = y["negative_findings"]
    for n in negs:
        for f in NEG_FIELDS:
            if f not in n or not str(n[f]).strip():
                fails.append("F %s 缺字段 %s" % (n.get("id", "?"), f))
    ids = [n["id"] for n in negs]
    for req in ("N-JJ1", "N-JJ3"):
        if req not in ids:
            fails.append("F 缺必备否定记录 %s" % req)
    for n in negs:
        if n["id"] == "N-JJ1" and "不可" not in n["判读"]:
            fails.append("F N-JJ1 缺「不可」限定 —— 「0 命中」不得被读作"
                         "「两源一致」，实为无可互证之对象")

    # G 禁用表述（按字段性质分层，见 BANNED_HARD / BANNED_STATE 之说明）
    for word, why in BANNED_HARD:
        if word in text:
            fails.append("G 出现越界断言「%s」（%s）——无论何种字段皆不可出现"
                         % (word, why))
    for word, why in BANNED_STATE:
        for label, val in ASSERT_SCALARS:
            if word in str(val):
                fails.append("G 断言字段 %s 出现「%s」（%s）"
                             % (label, word, why))

    # H 月份自洽
    months = set()
    for d in det:
        mm = re.search(r"#(\d+)月", d["title"])
        if mm:
            months.add(int(mm.group(1)))
    period = y["meta"]["period"]
    for mo in sorted(months):
        if "#%d月" % mo not in period and "%d月" % mo not in period:
            fails.append("H period 未覆盖实测月份 #%d月" % mo)

    if fails:
        print("【门禁失败】%d 项" % len(fails))
        for f in fails:
            print("  ✗ " + f)
        return 1
    print("ALL CHECKS PASSED（L.111 九九華嚴 OCR 立册）")
    print("  A 结构 %d 键｜B 实测对账 %d 集（目录发现＝台账集数）／%d 汉字"
          "｜C 出处 %d 条可点链接"
          % (len(TOP_KEYS), neps_found, m["total_han_chars"], len(det)))
    print("  D 校定状态 %d 集皆「待校定」｜E T0 限栈=%s（不含本路径）｜"
          "F 否定记录 %d 条｜G 禁词 %d 族｜H 月份 %s"
          % (len(det), t0, len(negs),
             len(BANNED_HARD) + len(BANNED_STATE),
             sorted(months) if months else "—"))
    return 0


def mutate(text, kind):
    """变异器：返回 (新文本, 是否生效)。**生效为 False 时上层即中止**——
    「变异是空操作」曾多次导致门禁假绿（L.106/107），故此处以返回码防之。"""
    if kind == "drop_calibration":
        # 〔L.111·自纠〕初版正则 `calibration:\s*待校定` 未容引号，而生成器写的是
        #   `calibration: "待校定"` —— 变异空操作，rc=2 由反假绿机制正确报出。
        pat = re.compile(r'^(\s*calibration:\s*)["\']?待校定["\']?\s*$', re.M)
        if not pat.search(text):
            return text, False
        return pat.sub(r'\g<1>"已校定"', text), True
    if kind == "falsify_number":
        pat = re.compile(r'^(\s*cues:\s*)1728\s*$', re.M)
        if not pat.search(text):
            return text, False
        return pat.sub(r'\g<1>1700', text), True
    if kind == "break_url":
        pat = re.compile(r'watch\?v=[A-Za-z0-9_-]{11}')
        if not pat.search(text):
            return text, False
        return pat.sub("watch?v=", text), True
    if kind == "admit_t0":
        old = "src: \"docs/hy_refs/sub_extract/delivery/ep01.md\""
        if old not in text:
            return text, False
        return text.replace(
            old, "src: \"docs/huayanhai/华严云海/浩瀚华严海/九九华严/摘录/x.md\""), True
    if kind == "soften_neg":
        # 〔L.111·自纠〕初版以「N-JJ1 起 900 字」为窗，致「不可」先命中
        #   `key` 字段（「跨源互證不可行」）而非 `判读` —— 变异打在无关处，
        #   门禁如期通过，构成**假绿**。故改为**定位该条之 判读 块**再改。
        #   〔二次〕块边界亦曾取错（`>-\n` 之后即断，遂 blk 只剩「判读: >-」）。
        i = text.find("N-JJ1")
        if i < 0:
            return text, False
        j = text.find("判读:", i)
        if j < 0:
            return text, False
        k = text.find("\n  - id:", j)
        if k < 0:
            k = len(text)
        blk = text[j:k]
        if "不可" not in blk:
            return text, False
        return text[:j] + blk.replace("不可", "可以", 1) + text[k:], True
    if kind == "shout_verified":
        # 〔L.111·自纠〕初版 replace 全篇首个同串，落点为**文件头注释**内的
        #   「OCR 重建稿 · 待校定」——注释不进 YAML，门禁自是无从察觉，
        #   遂 rc=0 假绿。故改为**定点改 meta.nature**，即真正之断言字段。
        old = 'nature: "OCR 重建稿 · 待校定'
        if old not in text:
            return text, False
        return text.replace(old, 'nature: "OCR 重建稿 · 已校定', 1), True
    if kind == "drop_ep":
        pat = re.compile(r"  - ep: 7\n(?:    .*\n)+", re.M)
        if not pat.search(text):
            return text, False
        return pat.sub("", text), True
    if kind == "month_drift":
        if "#7月" not in text:
            return text, False
        return text.replace("#7月", "#9月", 1), True
    return text, False


def y_ok(text):
    return "OCR 重建稿 · 待校定" in text


if __name__ == "__main__":
    sys.exit(main())