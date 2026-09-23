#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华严项目 · 自我进化引擎 (self_evolve.py)
=================================================================
一个闭环控制回路，让项目「随时间自适应」地提升适应能力：

    SENSE  感知  →  运行验证关卡 / 扫描待核存疑标记 / 侦测进度台账矛盾 /
                    (可选)链接失效 / 记录数据文件老化
    INTERPRET 解释 →  计算健康度、按「老化加权」重排优先级、
                    反馈式整定自适应阈值（问题积压↑则收紧，↓则放宽）
    ACT 行动(半自动) →  低风险记账自动做(刷新状态/登记/归档已解决)；
                    触及内容的动作(--apply 进度回填)逐项人工确认
    LEARN 学习 →  写入进化记忆(时间序列)，推算下次复核节奏，
                    输出「记忆更新」清单供 Agent 沉淀长期经验

严格遵守项目「考证优先 / 严禁假信息 / 边界自知」原则：
引擎只发现、记录、排序，绝不为消除待办而臆造或篡改研究内容。

用法:
    python scripts/self_evolve.py                 # 干跑一轮完整周期(感知+解释+记账+报告)
    python scripts/self_evolve.py --apply         # 追加：对内容类低风险动作逐项确认执行
    python scripts/self_evolve.py --check-links   # 追加：链接失效检查(联网, 规避本环境直连不通)
    python scripts/self_evolve.py --json          # 机器可读摘要输出
    python scripts/self_evolve.py --no-validators # 跳过子进程验证(离线快速预检)
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, date
from pathlib import Path

import yaml

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
CFG_PATH = ROOT / "data" / "evolution" / "evolution_config.yaml"
STATE_PATH = ROOT / "data" / "evolution" / "evolution_state.yaml"
LOG_PATH = ROOT / "data" / "evolution" / "evolution_log.yaml"
REPORT_DIR = ROOT / "docs" / "evolution"
LEDGER_MD = REPORT_DIR / "evolution_ledger.md"
PLAN_PATH = ROOT / "docs" / "next-phase-plan.md"
DB_PATH = ROOT / "data" / "catalog" / "huayan.db"


# ─────────────────────────────────────────────────────────────
# 工具
# ─────────────────────────────────────────────────────────────
def load_yaml(path, default=None):
    if not path.exists():
        return default
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=100)


def sig(*parts):
    h = hashlib.sha1("::".join(parts).encode("utf-8")).hexdigest()
    return h[:16]


# ─────────────────────────────────────────────────────────────
# 进化台账 (Evolution Ledger) —— 每次进化的显式、只追加记录
#   自动(auto) / 人工确认(human) / Agent(agent) 三类动作一律留痕，
#   供后续自我演化机制与其他机制读取。schema 稳定、seq 单调递增。
# ─────────────────────────────────────────────────────────────
LEDGER_SCHEMA = "huayan.evolution.log/v1"

# 事件类别（供其他机制过滤）：
#   cycle_run        一次周期体检总览（auto）
#   marker_register  登记新增待办（auto）
#   auto_resolve     连续缺席自动归档（auto）
#   threshold_tune   自适应阈值整定（auto）
#   cadence_set      复核节奏设定（auto）
#   progress_backfill 进度回填（human 确认执行 / declined 否决）
#   link_check       链接失效检查（auto）
#   note             人工/Agent 追加的带外进化说明（--record）


def load_log():
    d = load_yaml(LOG_PATH, default={}) or {}
    d.setdefault("schema", LEDGER_SCHEMA)
    d.setdefault("events", [])
    return d


class Ledger:
    """把一次运行内产生的所有进化事件显式写入台账。"""

    def __init__(self):
        self.doc = load_log()
        self.events = self.doc["events"]
        self.seq = len(self.events)
        self.pending = []

    def add(self, actor, category, subject, *, action=None, before=None, after=None,
            evidence=None, rationale=None, outcome="observed", cycle=None, **extra):
        self.seq += 1
        ev = {
            "seq": self.seq,
            "ts": datetime.now().isoformat(timespec="seconds"),
            "date": date.today().isoformat(),
            "cycle": cycle,
            "actor": actor,          # auto | human | agent
            "category": category,
            "subject": subject,
            "outcome": outcome,      # observed | applied | declined | skipped
        }
        for k, v in (("action", action), ("before", before), ("after", after),
                     ("evidence", evidence), ("rationale", rationale)):
            if v is not None:
                ev[k] = v
        for k, v in extra.items():
            if v is not None:
                ev[k] = v
        self.events.append(ev)
        self.pending.append(ev)
        return ev

    def commit(self):
        # 保留最近 5000 条（台账以追加为主，超限只裁剪最旧观测类事件）
        if len(self.events) > 5000:
            self.events = self.events[-5000:]
        self.doc["events"] = self.events
        dump_yaml(LOG_PATH, self.doc)
        render_ledger_md(self.events)
        return len(self.pending)


def render_ledger_md(events):
    """把机器台账渲染成人类可读的滚动日志（按日期倒序、每次运行成组）。"""
    lines = [
        "# 进化台账 (Evolution Ledger)",
        "",
        "> 由 `scripts/self_evolve.py` 自动维护的**只追加**审计流水；权威机读源为 `data/evolution/evolution_log.yaml`。",
        "> 记录每一次进化动作——自动体检/阈值整定/自动归档，与人工确认的进度回填/否决，以及 Agent 带外记录。",
        "",
        f"共 **{len(events)}** 条事件。",
        "",
    ]
    actor_icon = {"auto": "🤖", "human": "👤", "agent": "🧠"}
    outcome_tag = {"applied": "✅执行", "declined": "⛔否决", "observed": "👁观测", "skipped": "⏭跳过"}
    by_date = {}
    for e in events:
        by_date.setdefault(e.get("date", "?"), []).append(e)
    for d in sorted(by_date, reverse=True):
        lines.append(f"## {d}")
        lines.append("")
        lines.append("| seq | 周期 | 触发 | 类别 | 对象 | 动作/变更 | 结果 | 依据/理由 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for e in by_date[d]:
            chg = e.get("action") or ""
            if e.get("before") is not None or e.get("after") is not None:
                chg = f"{e.get('before','—')} → {e.get('after','—')}".strip()
            why = e.get("rationale") or e.get("evidence") or ""
            actor = actor_icon.get(e.get("actor"), e.get("actor"))
            res = outcome_tag.get(e.get("outcome"), e.get("outcome"))
            cyc = e.get("cycle") or "—"
            cell = (lambda s: str(s).replace("|", "\\|").replace("\n", " "))
            lines.append(
                f"| {e.get('seq')} | {cyc} | {actor} | {e.get('category')} "
                f"| {cell(e.get('subject'))[:40]} | {cell(chg)[:60]} | {res} | {cell(why)[:70]} |")
        lines.append("")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    LEDGER_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def git_last_touch(relpath):
    """返回 (date|None, source) —— 以 git 最后提交时间为准，回退文件 mtime。"""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", relpath],
            cwd=ROOT, capture_output=True, text=True, timeout=8,
        )
        ts = out.stdout.strip()
        if ts.isdigit():
            return date.fromtimestamp(int(ts)), "git"
    except Exception:
        pass
    p = ROOT / relpath
    if p.exists():
        return date.fromtimestamp(p.stat().st_mtime), "mtime"
    return None, "none"


def expand_targets(cfg):
    """按 include/exclude glob 收集待扫描文件集合。"""
    files = set()
    for pat in cfg["scan"]["include"]:
        for p in ROOT.glob(pat):
            if p.is_file():
                files.add(p.relative_to(ROOT).as_posix())
    excl = set()
    for pat in cfg["scan"]["exclude"]:
        for p in ROOT.glob(pat):
            if p.is_file():
                excl.add(p.relative_to(ROOT).as_posix())
        # pathlib 的尾缀 `/**` 不匹配目录直属文件（如 data/evolution/** 命中为空）——
        # 显式按「子树前缀」剔除，使排除表达如预期生效（防引擎自扫描基因组/台账）。
        if pat.endswith("/**"):
            prefix = pat[:-3].rstrip("/")
            excl |= {f for f in files if f == prefix or f.startswith(prefix + "/")}
    return sorted(files - excl)


# ─────────────────────────────────────────────────────────────
# SENSE 感知
# ─────────────────────────────────────────────────────────────
def sense_validators(cfg, enabled=True):
    results = []
    if not enabled:
        return results
    for v in cfg.get("validators", []):
        cmd = [sys.executable if a == "python" else a for a in v["cmd"]]
        rec = {"id": v["id"], "weight": v.get("weight", 0), "passed": False,
               "score": None, "note": ""}
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        try:
            out = subprocess.run(cmd, cwd=ROOT, capture_output=True,
                                  text=True, encoding="utf-8", timeout=180,
                                  env=env, stdin=subprocess.DEVNULL)
            blob = (out.stdout or "") + (out.stderr or "")
            if v.get("json_score_key"):
                try:
                    data = json.loads(out.stdout[out.stdout.index("{"):out.stdout.rindex("}") + 1])
                    rec["score"] = data.get(v["json_score_key"])
                    rec["passed"] = rec["score"] is not None
                except Exception:
                    rec["note"] = "json解析失败"
            elif v.get("pass_regex"):
                rec["passed"] = bool(re.search(v["pass_regex"], blob))
            if out.returncode != 0 and rec["score"] is None:
                rec["passed"] = False
                rec["note"] = (rec["note"] + f" exit={out.returncode}").strip()
        except FileNotFoundError:
            rec["note"] = "脚本缺失"
        except subprocess.TimeoutExpired:
            rec["note"] = "超时"
        results.append(rec)
    return results


def sense_markers(cfg, ref_date):
    """扫描 include 文件中的待办/存疑标记 → items 列表。"""
    targets = expand_targets(cfg)
    items = []
    compiled = []
    for m in cfg["markers"]:
        if m.get("word_bound"):
            rx = re.compile(r"\b" + re.escape(m["token"]) + r"\b")
        else:
            rx = re.compile(re.escape(m["token"]))
        compiled.append((m, rx))
    for rel in targets:
        try:
            text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for ln, line in enumerate(text.splitlines(), 1):
            for m, rx in compiled:
                if rx.search(line):
                    snippet = line.strip()[:120]
                    items.append({
                        "signature": sig(rel, m["token"], re.sub(r"\s+", " ", snippet)),
                        "file": rel, "line": ln, "token": m["token"],
                        "kind": m["kind"], "severity": m["severity"],
                        "note": m.get("note", ""), "snippet": snippet,
                    })
    return items


def sense_link_rot(cfg, items):
    lc = cfg.get("link_check", {})
    if not lc.get("enabled"):
        return []
    import urllib.request
    import urllib.error
    urls = {}
    for it in items:
        for u in re.findall(r"https?://[^\s)\"'`]+", it["snippet"]):
            urls.setdefault(u.rstrip(".,;]"), it["file"])
    broken, unreachable_hosts = [], set(lc.get("allow_unreachable_hosts", []))
    for u in list(urls)[:60]:  # 限量避免长阻塞
        host = re.sub(r"^https?://", "", u).split("/")[0]
        try:
            req = urllib.request.Request(u, method="HEAD",
                                         headers={"User-Agent": lc.get("user_agent", "evolution")})
            with urllib.request.urlopen(req, timeout=lc.get("timeout_sec", 6)) as r:
                code = r.status
            if code >= 400:
                broken.append({"url": u, "file": urls[u], "status": code})
        except urllib.error.HTTPError as e:
            broken.append({"url": u, "file": urls[u], "status": e.code})
        except Exception:
            if not any(h in host for h in unreachable_hosts):
                broken.append({"url": u, "file": urls[u], "status": "timeout"})
    return broken


def sense_stale_progress(validators):
    """侦测进度台账矛盾：P0 表仍标 🔴待实施，但管线已全绿 → 陈旧。"""
    green = bool(validators) and all(v["passed"] for v in validators)
    stale = []
    if not green or not PLAN_PATH.exists():
        return stale
    text = PLAN_PATH.read_text(encoding="utf-8")
    m = re.search(r"###\s*P0.*?(?=\n###\s|\n---)", text, re.DOTALL)
    block = m.group(0) if m else ""
    for row in re.findall(r"^\|\s*\*\*(.+?)\*\*.*?🔴\s*待实施.*$", block, re.MULTILINE):
        stale.append(row.strip())
    return stale


def sense_file_age(cfg, ref_date):
    stale_days = cfg["temporal"]["file_stale_days"]["value"]
    out = []
    for rel in expand_targets(cfg):
        d, src = git_last_touch(rel)
        if d is None:
            continue
        age = (ref_date - d).days
        if age >= stale_days:
            out.append({"file": rel, "last_touch": d.isoformat(), "age_days": age, "source": src})
    out.sort(key=lambda x: -x["age_days"])
    return out[:20]


# ─────────────────────────────────────────────────────────────
# INTERPRET 解释 / 优先级 / 自适应整定
# ─────────────────────────────────────────────────────────────
def effective_window(cfg, state):
    base = cfg["temporal"]["escalation_window_days"]
    return state.get("adaptive", {}).get("escalation_window_days", base["value"])


def age_weight(cfg, window, age_days):
    ec = cfg["temporal"]["escalation_window_days"]
    gain = ec.get("gain", 0.5)
    cap = ec.get("max_multiplier", 4.0)
    tiers = age_days // max(1, window)
    return min(cap, (1 + gain) ** tiers)


def interpret(cfg, state, items, validators):
    ref_date = state["_ref_date"]
    window = effective_window(cfg, state)

    # 与历史 registry 合并，计算 age
    reg = state.get("registry", {})
    for it in items:
        entry = reg.get(it["signature"])
        if entry and entry.get("first_seen"):
            first = date.fromisoformat(entry["first_seen"])
        else:
            first = ref_date
        age = (ref_date - first).days
        it["age_days"] = age
        it["time_mult"] = round(age_weight(cfg, window, age), 2)
        it["priority"] = round(it["severity"] * it["time_mult"], 2)

    open_items = sorted(items, key=lambda x: (-x["priority"], -x["severity"], x["file"]))
    high_backlog = sum(1 for it in open_items if it["severity"] >= 4)

    # 健康度（透明扣分模型）
    score = 100.0
    detail = []
    for v in validators:
        if not v["passed"]:
            pen = v["weight"] * 40
            score -= pen
            detail.append(f"验证 {v['id']} 未通过 −{pen:.0f}")
        elif v.get("score") is not None:
            pen = (100 - v["score"]) / 100 * v["weight"] * 40
            score -= pen
            detail.append(f"来源评分 {v['score']}/100 −{pen:.1f}")
    sev_count = {}
    for it in open_items:
        sev_count[it["severity"]] = sev_count.get(it["severity"], 0) + 1
    score -= sev_count.get(5, 0) * 1.0
    score -= sev_count.get(4, 0) * 0.5
    score -= sev_count.get(3, 0) * 0.2
    detail.append(f"待订正 {sev_count.get(5,0)} / 待核存疑 {sev_count.get(4,0)} / 待考 {sev_count.get(3,0)}")

    # 反馈式阈值整定
    ctl = cfg["temporal"]["controller"]
    new_window = window
    tune = "维持"
    if high_backlog > ctl["tolerance_high"]:
        new_window = max(ctl["clamp_min"], window - ctl["adjust_step_days"])
        tune = "收紧"
    elif high_backlog < ctl["tolerance_low"]:
        new_window = min(ctl["clamp_max"], window + ctl["adjust_step_days"])
        tune = "放宽"

    # 复核节奏
    cad = cfg["cadence"]
    if new_window < cad["baseline_days"]:
        recommended = max(cad["min_days"], cad["baseline_days"] // 2)
    elif high_backlog <= ctl["tolerance_low"]:
        recommended = min(cad["max_days"], cad["baseline_days"] + 7)
    else:
        recommended = cad["baseline_days"]

    return {
        "health": round(max(0.0, min(100.0, score)), 1),
        "health_detail": detail,
        "open_items": open_items,
        "high_backlog": high_backlog,
        "sev_count": sev_count,
        "window_before": window,
        "window_after": new_window,
        "tune": tune,
        "recommended_cadence_days": recommended,
    }


# ─────────────────────────────────────────────────────────────
# ACT 行动（半自动）
# ─────────────────────────────────────────────────────────────
def act_registry(state, items, ref_date, grace_cycles):
    """登记/刷新/归档：确定性、纯派生的记账（自动执行）。"""
    reg = state.setdefault("registry", {})
    seen = set()
    added = resolved = 0
    for it in items:
        s = it["signature"]
        seen.add(s)
        e = reg.get(s)
        if e:
            e["last_seen"] = ref_date.isoformat()
            e["absent_cycles"] = 0
            e["seen_count"] = e.get("seen_count", 1) + 1
            # 刷新派生字段：config 为可变基因组，kind/severity 调整应传导至已有项
            e["kind"] = it["kind"]
            e["severity"] = it["severity"]
            if it.get("note"):
                e["note"] = it["note"]
            if e.get("status") == "resolved":
                e["status"] = "open"
        else:
            reg[s] = {"file": it["file"], "token": it["token"], "kind": it["kind"],
                      "severity": it["severity"], "snippet": it["snippet"],
                      "first_seen": ref_date.isoformat(), "last_seen": ref_date.isoformat(),
                      "seen_count": 1, "absent_cycles": 0, "status": "open"}
            added += 1
    for s, e in reg.items():
        if s not in seen and e.get("status") == "open":
            e["absent_cycles"] = e.get("absent_cycles", 0) + 1
            if e["absent_cycles"] > grace_cycles:
                e["status"] = "resolved"
                e["resolved_date"] = ref_date.isoformat()
                resolved += 1
    return added, resolved


def act_autofix_stale_progress(stale, ref_date, confirm_cb, ledger=None, cycle=None, evidence=""):
    """进度回填（内容类·逐项确认）：P0 🔴待实施 → ✅已完成(进化引擎核证)。
    无论执行还是否决，均向台账显式留痕（actor=human）。"""
    applied = []
    if not stale or not PLAN_PATH.exists():
        return applied
    text = PLAN_PATH.read_text(encoding="utf-8")
    m = re.search(r"###\s*P0.*?(?=\n###\s|\n---)", text, re.DOTALL)
    if not m:
        return applied
    block = m.group(0)
    new_block = block
    for row in stale:
        label = f"**{row}**"
        pattern = re.compile(r"(\|\s*" + re.escape(label) + r".*?)🔴\s*待实施")
        if pattern.search(new_block):
            ok = confirm_cb(f"进度回填 next-phase-plan P0 「{row}」 🔴待实施 → ✅已完成(进化引擎核证 {ref_date})")
            if ok:
                new_block = pattern.sub(lambda x: x.group(1) + f"✅ 已完成·进化引擎核证{ref_date.isoformat()}", new_block, count=1)
                applied.append(row)
            if ledger is not None:
                ledger.add("human", "progress_backfill", f"P0 {row}",
                           before="🔴 待实施", after="✅ 已完成·进化引擎核证" + ref_date.isoformat(),
                           evidence=evidence, outcome="applied" if ok else "declined",
                           rationale="管线全绿佐证·人工逐项确认" if ok else "人工否决，保留待核实",
                           cycle=cycle)
    if new_block != block:
        PLAN_PATH.write_text(text.replace(block, new_block, 1), encoding="utf-8")
    return applied


# ─────────────────────────────────────────────────────────────
# 报告输出
# ─────────────────────────────────────────────────────────────
def write_reports(cfg, state, interp, validators, stale, aged, link_broken, ref_date):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = ref_date.isoformat()

    lines = [
        f"# 自我进化 · 健康度报告 {stamp}",
        "",
        f"> 由 `scripts/self_evolve.py` 自动生成 · 周期 #{state.get('cycle_count',0)} · 数据源为派生观测，非研究内容",
        "",
        "## 总览",
        "",
        f"- **健康度**: {interp['health']}/100",
        f"- 高优先级积压(sev≥4): **{interp['high_backlog']}** 项",
        f"- 自适应阈值 escalation_window: {interp['window_before']} → **{interp['window_after']}** 天 ({interp['tune']})",
        f"- 建议下次复核: **{interp['recommended_cadence_days']}** 天后 ({next_review_date(ref_date, interp['recommended_cadence_days'])})",
        "",
        "### 健康度扣分明细",
        "",
    ]
    for d in interp["health_detail"]:
        lines.append(f"- {d}")
    lines += ["", "### 验证关卡", "", "| 关卡 | 结果 | 评分 | 备注 |", "|---|---|---|---|"]
    for v in validators:
        lines.append(f"| {v['id']} | {'✅ 通过' if v['passed'] else '❌ 未过'} | {v.get('score','—')} | {v.get('note','')} |")
    if not validators:
        lines.append("| (本次跳过) | — | — | --no-validators |")

    if stale:
        lines += ["", "### ⚠ 进度台账矛盾（管线全绿但标未实施）", ""]
        for s in stale:
            lines.append(f"- {s}")

    if link_broken:
        lines += ["", f"### 链接失效 ({len(link_broken)})", ""]
        for b in link_broken:
            lines.append(f"- `{b['file']}` → {b['url']}  (status {b['status']})")

    if aged:
        lines += ["", f"### 久未触碰文件 (≥{cfg['temporal']['file_stale_days']['value']}天)", "",
                  "| 文件 | 最后触碰 | 距今天数 |", "|---|---|---|"]
        for a in aged:
            lines.append(f"| {a['file']} | {a['last_touch']} | {a['age_days']} |")

    (REPORT_DIR / f"health_{stamp}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (REPORT_DIR / "health_latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # next_actions 梯队
    na = [f"# 下一步待办梯队（进化引擎排序）{stamp}", "",
          "> 按「严重度 × 老化加权」排序；kind=boundary 者为边界自知(不强行处理)。", "",
          "| 优先级 | 严重度 | 龄(天) | 类型 | 标记 | 文件:行 |",
          "|---|---|---|---|---|---|"]
    for it in interp["open_items"][:60]:
        na.append(f"| {it['priority']} | {it['severity']} | {it['age_days']} | {it['kind']} | {it['token']} | `{it['file']}:{it['line']}` |")
    na += ["", "## 明细（前 25 条）", ""]
    for it in interp["open_items"][:25]:
        na.append(f"- **[{it['priority']}] {it['file']}:{it['line']}** {it['token']} — {it['snippet']}")
    na += ["", "## 记忆更新提示（供 Agent 沉淀长期经验）", "",
           f"- 当前健康度 {interp['health']}/100，高优先积压 {interp['high_backlog']}。",
           f"- 自适应阈值本轮{interp['tune']}至 {interp['window_after']} 天窗口——若连续多轮同向调整，说明积压结构性，应立项专项清理。",
           "- 若出现新的验证关卡失败或进度台账矛盾，作为 common_pitfalls 记入长期记忆。"]
    (REPORT_DIR / f"next_actions_{stamp}.md").write_text("\n".join(na) + "\n", encoding="utf-8")
    (REPORT_DIR / "next_actions.md").write_text("\n".join(na) + "\n", encoding="utf-8")


def next_review_date(ref_date, days):
    from datetime import timedelta
    return (ref_date + timedelta(days=days)).isoformat()


# ─────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="华严项目自我进化引擎")
    ap.add_argument("--apply", action="store_true", help="对内容类低风险动作(进度回填)逐项确认执行")
    ap.add_argument("--check-links", action="store_true", help="启用链接失效检查(联网)")
    ap.add_argument("--no-validators", action="store_true", help="跳过子进程验证关卡")
    ap.add_argument("--json", action="store_true", help="输出机器可读摘要")
    ap.add_argument("--reference-date", default=None, help="可复现实验的基准日 YYYY-MM-DD")
    ap.add_argument("--record", metavar="CATEGORY", default=None,
                    help="向台账追加一条带外进化事件(不跑周期)；供人工/Agent 记录重型动作")
    ap.add_argument("--actor", default="human", choices=["auto", "human", "agent"], help="--record 的触发主体")
    ap.add_argument("--subject", default="", help="--record 的对象")
    ap.add_argument("--note", default="", help="--record 的动作/理由说明")
    ap.add_argument("--outcome", default="applied", choices=["applied", "observed", "declined", "skipped"], help="--record 的结果")
    ap.add_argument("--ledger", action="store_true", help="打印进化台账摘要后退出")
    args = ap.parse_args()

    if args.ledger:
        log = load_log()
        evs = log["events"]
        print(f"进化台账：共 {len(evs)} 条事件（权威源 data/evolution/evolution_log.yaml）")
        for e in evs[-15:]:
            print(f"  #{e.get('seq')} {e.get('date')} [c{e.get('cycle')}] "
                  f"{e.get('actor')}/{e.get('category')}/{e.get('outcome')} — {e.get('subject')}")
        return

    if args.record:
        led = Ledger()
        led.add(args.actor, args.record, args.subject or args.record,
                action=args.note or None, outcome=args.outcome)
        n = led.commit()
        print(f"已追加 {n} 条进化事件至台账 → {LOG_PATH.relative_to(ROOT)}；同步 {LEDGER_MD.relative_to(ROOT)}")
        return

    cfg = load_yaml(CFG_PATH)
    if not cfg:
        print("缺少配置 data/evolution/evolution_config.yaml")
        sys.exit(1)
    if args.check_links:
        cfg.setdefault("link_check", {})["enabled"] = True

    state = load_yaml(STATE_PATH, default={}) or {}
    state.setdefault("schema", "huayan.evolution.state/v1")
    state.setdefault("registry", {})
    state.setdefault("history", [])
    state.setdefault("adaptive", {})

    rd = cfg["temporal"].get("reference_date", "auto")
    if args.reference_date:
        ref_date = date.fromisoformat(args.reference_date)
    elif rd and rd != "auto":
        ref_date = date.fromisoformat(str(rd))
    else:
        ref_date = date.today()
    state["_ref_date"] = ref_date
    led = Ledger()

    # SENSE
    validators = sense_validators(cfg, enabled=not args.no_validators)
    items = sense_markers(cfg, ref_date)
    link_broken = sense_link_rot(cfg, items)
    stale = sense_stale_progress(validators)
    aged = sense_file_age(cfg, ref_date)

    # INTERPRET
    interp = interpret(cfg, state, items, validators)

    # ACT — 自动记账（低风险派生动作）
    grace = 2
    for a in cfg.get("autofix", {}).get("allow", []):
        if a["id"] == "prune_resolved":
            grace = a.get("grace_cycles", 2)
    added, resolved = act_registry(state, items, ref_date, grace)

    applied_fix = []
    green = bool(validators) and all(v["passed"] for v in validators)
    v_ev = "管线" + ("全绿" if green else "未全绿") + ": " + ",".join(
        f"{v['id']}={'✅' if v['passed'] else '❌'}" for v in validators) if validators else "(验证跳过)"
    if args.apply and stale:
        def confirm_cb(msg):
            try:
                ans = input(f"[进化·确认] {msg} ? [y/N] ").strip().lower()
            except EOFError:
                ans = "n"  # 非交互/无 stdin → 保守回退为不执行
            return ans in ("y", "yes")
        applied_fix = act_autofix_stale_progress(
            stale, ref_date, confirm_cb, ledger=led,
            cycle=state.get("cycle_count", 0) + 1, evidence=v_ev)

    # LEARN — 更新自适应阈值 + 历史时间序列
    state.setdefault("adaptive", {})["escalation_window_days"] = interp["window_after"]
    state["cycle_count"] = state.get("cycle_count", 0) + 1
    state["last_run"] = datetime.now().isoformat(timespec="seconds")
    state["history"].append({
        "date": ref_date.isoformat(), "health": interp["health"],
        "open": len(interp["open_items"]), "high_backlog": interp["high_backlog"],
        "sev5": interp["sev_count"].get(5, 0), "sev4": interp["sev_count"].get(4, 0),
        "window": interp["window_after"], "added": added, "resolved": resolved,
        "stale_progress": len(stale),
        "validators": {v["id"]: v["passed"] for v in validators},
    })
    state["history"] = state["history"][-200:]  # 保留最近 200 轮
    dump_yaml(STATE_PATH, state)

    # LEARN — 向进化台账显式登记本次自动动作（人工回填事件已在 act 内追加）
    cyc = state["cycle_count"]
    led.add("auto", "cycle_run", f"周期 #{cyc} 体检总览", cycle=cyc, outcome="observed",
            after=f"health={interp['health']} open={len(interp['open_items'])} high={interp['high_backlog']}",
            evidence=v_ev,
            rationale="新增 %d·归档 %d·台账矛盾 %d" % (added, resolved, len(stale)))
    if added:
        led.add("auto", "marker_register", f"登记新增待办 {added} 项", cycle=cyc, outcome="applied",
                rationale="扫描 include 文件命中的待核/存疑/待订正标记")
    if resolved:
        led.add("auto", "auto_resolve", f"自动归档已解决 {resolved} 项", cycle=cyc, outcome="applied",
                evidence=f"连续 >{grace} 周期未再出现", rationale="标记已从源头消失→销账")
    if interp["window_after"] != interp["window_before"]:
        led.add("auto", "threshold_tune", "escalation_window_days",
                before=interp["window_before"], after=interp["window_after"],
                cycle=cyc, outcome="applied",
                rationale="高优先积压 %d vs 带限[%d,%d]→%s" % (
                    interp["high_backlog"], cfg["temporal"]["controller"]["tolerance_low"],
                    cfg["temporal"]["controller"]["tolerance_high"], interp["tune"]))
    led.add("auto", "cadence_set", "next_review", cycle=cyc, outcome="applied",
            after=f"+{interp['recommended_cadence_days']}d → {next_review_date(ref_date, interp['recommended_cadence_days'])}",
            rationale="据积压与阈值推算复核节奏")
    if link_broken:
        led.add("auto", "link_check", f"链接失效 {len(link_broken)} 条", cycle=cyc, outcome="observed",
                rationale="; ".join(b["url"] for b in link_broken[:5]))
    n_led = led.commit()

    write_reports(cfg, state, interp, validators, stale, aged, link_broken, ref_date)

    # 控制台摘要
    if args.json:
        print(json.dumps({
            "date": ref_date.isoformat(), "health": interp["health"],
            "open": len(interp["open_items"]), "high_backlog": interp["high_backlog"],
            "window": f"{interp['window_before']}→{interp['window_after']} ({interp['tune']})",
            "recommended_cadence_days": interp["recommended_cadence_days"],
            "added": added, "resolved": resolved,
            "stale_progress": stale, "applied_fix": applied_fix,
            "ledger_events_added": n_led,
            "validators": {v["id"]: v["passed"] for v in validators},
        }, ensure_ascii=False, indent=1))
        return

    print("=" * 62)
    print("  华严项目 · 自我进化引擎  —  周期 #%d  (%s)" % (state["cycle_count"], ref_date))
    print("=" * 62)
    print(f"  健康度        : {interp['health']}/100")
    print(f"  扫描标记      : 未解决 {len(interp['open_items'])} 项 (新增 {added} · 归档 {resolved})")
    print(f"  高优先积压    : {interp['high_backlog']} 项 (sev≥4)")
    print(f"  自适应阈值    : {interp['window_before']} → {interp['window_after']} 天  [{interp['tune']}]")
    print(f"  建议复核节奏  : {interp['recommended_cadence_days']} 天后")
    if validators:
        stat = " ".join(f"{v['id']}={'✅' if v['passed'] else '❌'}" for v in validators)
        print(f"  验证关卡      : {stat}")
    if stale:
        print(f"  ⚠ 进度台账矛盾 : {len(stale)} 项 " + ("(已回填)" if applied_fix else "(--apply 可回填)"))
    if link_broken:
        print(f"  链接失效      : {len(link_broken)}")
    print("-" * 62)
    print(f"  报告 → docs/evolution/health_{ref_date.isoformat()}.md")
    print(f"  梯队 → docs/evolution/next_actions.md")
    print(f"  台账 → data/evolution/evolution_log.yaml (本次 +{n_led} 事件) / docs/evolution/evolution_ledger.md")
    print(f"  记忆 → data/evolution/evolution_state.yaml")
    if not args.apply:
        print("  (干跑模式；加 --apply 可对进度台账逐项确认回填)")
    print("=" * 62)


if __name__ == "__main__":
    main()
