# -*- coding: utf-8 -*-
"""test_audit_consistency.py — B2 checker 自证（合成夹具 · 不碰真 docs）"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "audit_consistency", ROOT / "scripts/audit_consistency.py")
ac = importlib.util.module_from_spec(spec)
sys.modules["audit_consistency"] = ac
spec.loader.exec_module(ac)


def _mk(tmp, name, text):
    p = tmp / name
    p.write_text(text, encoding="utf-8")
    return p


def test_pending_ledger_counts(tmp_path):
    f = _mk(tmp_path, "a.md", "首〔待核〕…再一处【待核】…[待核]三型都应数\n干净行\n")
    led = ac.pending_ledger([f])
    assert sum(led.values()) == 3, "三书写变体都应收数"


def test_cbeta_format_rules(tmp_path):
    f = _mk(tmp_path, "b.md", "\n".join([
        "合法正编：《金刚经》T08n0235",
        "合法史传：《景德传灯录》T51n2076",
        "合法补编：《续古摘钞》T85n2837",
        "越界卷号：T99n1234",
        "编号非四位：T08n235",
        "卷号未补零：《华严经》T9n0279",
    ]))
    total, fmt, _ = ac.cbeta_audit([f])
    reasons = " ".join(w for *_, w in fmt)
    assert total == 6
    assert "越出大正藏全藏" in reasons
    assert "非 4 位" in reasons
    assert "未补零" in reasons
    assert sum(1 for r in fmt if "越出" in r[3]) == 1, "51/85 等合法卷不应误报"


def test_cbeta_conflict_candidates(tmp_path):
    f = _mk(tmp_path, "c.md", "\n".join([
        "《原人论》T45n1886 又《原人论》T45n1884",   # 一名多号(候选)
        "《一号多名》T46n1900 又《另一名字》T46n1900",  # 一号多名(候选)
    ]))
    _, _, conf = ac.cbeta_audit([f])
    assert "原人论" in conf["same_title_multi_siglas"]
    assert "T46n1900" in conf["same_sigla_multi_titles"]
