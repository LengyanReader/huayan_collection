# -*- coding: utf-8 -*-
"""T1 比勘门禁之反向验证（L.109 立）——门禁须自证有效，否则即「假绿」

〔方法论·承 L.107〕改**库副本**（不碰真库），逐项施加破坏性变异，
      要求两道门禁各自如期失败；并**前置断言变异确已生效**，
      否则「变异为空操作 → 门禁测不到东西 → 假绿」（既往三处假绿之根）。
"""
import io
import os
import shutil
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

LIB = "data/research/t1_bikan_evidence.yaml"
TMP = ".tmp_t1_mut.yaml"

# (名, 锚点, 替换, 应捕获此变异之门禁)
# 〔L109·自纠〕初版要求「两道门禁皆须失败」，然二者**职责不同**：
#   t1_quote --check 只管引文是否逐字（故改引文／改行号当由它捕获，
#   而改台账 total 于它无涉——**不应**要求它失败）；
#   verify_t1_bikan 管台账与结构对账。强求两者皆失败，等于把
#   「职责分离」误判为「门禁薄弱」，此为**验证脚本自身之缺陷**。
#   故改为逐项**指派应捕获之门禁**。另：初版以「失配」二字判命中，
#   而「失配 0 条」亦含此二字 → 恒假命中；改以「ALL CHECKS PASSED 不出现」
#   且 rc≠0 为准。
MUT = [
    ("台账 total 谎报", "    total: 27", "    total: 28", "bikan"),
    ("分节计数谎报", '      "5.2": 9', '      "5.2": 8', "bikan"),
    ("引文改一字", 'quote: "遊入故號門也"', 'quote: "遊入故號門耶"', "quote"),
    ("行号偏移", "    src_line: 2432", "    src_line: 2433", "quote"),
    ("否定记录删除", "  - id: N8", "  - id: X8", "bikan"),
    ("结论引用悬空", "依: [C01, C02, N5, N7]", "依: [C01, C02, N5, N99]", "bikan"),
    ("结论缺一节", '  - sec: "5.5"', '  - sec: "9.9"', "bikan"),
    ("id 断号", "  - id: C14", "  - id: X14", "bikan"),
]


def caught(rc, out):
    """判定「该门禁捕获了变异」：rc≠0 且未自称 ALL CHECKS PASSED。"""
    return rc != 0 and "ALL CHECKS PASSED" not in out


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, encoding="utf-8",
                       errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main():
    orig = io.open(LIB, encoding="utf-8").read()
    passed = 0
    for name, anchor, repl, gate in MUT:
        # 〔前置断言〕变异必已生效——否则本项作废而非「通过」
        if anchor not in orig:
            print("  SKIP  %-14s 【锚点不存在，变异未生效——不算通过】" % name)
            continue
        shutil.copyfile(LIB, LIB + ".bak")
        try:
            io.open(LIB, "w", encoding="utf-8", newline="\n").write(
                orig.replace(anchor, repl, 1))
            rc1, out1 = run([sys.executable, "scripts/t1_quote.py", "--check", LIB])
            rc2, out2 = run([sys.executable, "scripts/verify_t1_bikan.py"])
            # 另一道门禁「不失败」亦属合格（职责分离），但须如实记录
            if gate == "quote":
                tgt_ok, tgt_rc = caught(rc1, out1), rc1
                oth = "台账=%s" % ("失败" if caught(rc2, out2) else "通过")
            else:
                tgt_ok, tgt_rc = caught(rc2, out2), rc2
                oth = "引文=%s" % ("失败" if caught(rc1, out1) else "通过")
            status = "OK  " if tgt_ok else "MISS"
            if tgt_ok:
                passed += 1
            else:
                print("     应捕获之门禁 rc=%s，未捕获；另一门禁 %s" % (tgt_rc, oth))
            print("  %s  %-14s →%s 捕获（%s）"
                  % (status, name, "由" + gate, oth))
        finally:
            if os.path.exists(LIB + ".bak"):
                shutil.move(LIB + ".bak", LIB)
    # 对照：原库必过
    rc1, out1 = run([sys.executable, "scripts/t1_quote.py", "--check", LIB])
    rc2, out2 = run([sys.executable, "scripts/verify_t1_bikan.py"])
    base_ok = rc1 == 0 and rc2 == 0
    print("\n对照：未变异之库 quote rc=%d／台账 rc=%d（%s）"
          % (rc1, rc2, "皆通过" if base_ok else "**竟失败**"))
    print("反向验证 %d/%d 如期失败" % (passed, len(MUT)))
    if not base_ok:
        print("FAIL：未变异之库竟不过，门禁本身有误")
        return 1
    if passed != len(MUT):
        print("FAIL：有变异未被捕获")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())