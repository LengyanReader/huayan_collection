#!/usr/bin/env python3
"""fetch_cbeta_history.py — 史传部一手底本入库（CBETA TEI/P5 · G1 语料工程）

缘起（编务原则：考证优先 / 原文是什么语言就用什么 / 宁缺不伪）：
僧传画像的每一条承重断言都要能逐字回源，故须把大正藏**史传部**诸传的 CBETA
TEI/P5 原文取回本地，存作一手底本（同 `T10n0279.xml` 之规格），供逐字校勘。

通道（本会话 2026-10-17 实测，见《tasks/语料通道与文献缺口台账》§一/§九）：
  · `api.github.com/repos/cbeta-org/xml-p5/git/blobs/<sha>` 带 `Accept:
    application/vnd.github.raw` 直接返回**逐字 UTF-8 字节**（支持至 ~100 MiB）。注：
    base64-JSON 默认型在 >1 MB 会被截断，故取大书必用 raw 媒体型（已实证）。
  · `raw.githubusercontent.com` 在本环境超时，故不走直链。
  · 大正藏册五十《高僧傳》2.79 MB／《續高僧傳》6.61 MB／《宋高僧傳》2.21 MB／
    《大慈恩寺三藏法師傳》1.82 MB——**raw 媒体型可整本取回且保 TEI**（无需分卷）；
    若 raw 因体积失败，后备走 `DILA-edu/cbeta-normal-text`（一卷一檔，`--juan`）。

规矩（皆出于「宁留待核，不可失真」）：
  · **幂等**：目标文件已在盘上且字节数与 git blob 相符者，跳过、不覆盖（一手性一经改动即失）。
  · **尺寸闸**：> --max-bytes（默认 20 MB）者不整取，登记为「待分卷」，绝不半取。
  · **完整性**：每次入库记 CBETA git blob SHA 与本地内容 SHA256、字节、日期于 `INGEST_log.md`。
  · **许可**：CBETA 非营利学术用途；本脚本只新增文件、附来源，不动既有底本（见目录 README）。

用法：
  python fetch_cbeta_history.py                 # 预览（dry-run，不写盘）
  python fetch_cbeta_history.py --apply         # 整取 ≤上限 者并登记
  python fetch_cbeta_history.py --only T50n2063 --apply
  python fetch_cbeta_history.py --juan          # 大书逐卷模式（结构未展开时仅报告）

可选环境变量 GITHUB_TOKEN 以提升速率上限（未认证 60 次/时；一次整取约 5 次调用）。
"""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

API = "https://api.github.com"
REPO = "cbeta-org/xml-p5"
RAW_BASE = "https://raw.githubusercontent.com/cbeta-org/xml-p5/master"
DEST = Path(__file__).resolve().parents[1] / "data" / "references" / "cbeta"
LOG = DEST / "INGEST_log.md"
DEFAULT_BRANCH = "master"

# 史传部入库清单（经号 → 题名·册·卷·用途·关联人物轮次）。
# 字节数以本会话目录树实测为准，仅供尺寸闸预估；实际以 blob 返回为准。
TARGETS = {
    "T50n2056": dict(title="大唐故大德贈司空大辨正廣智不空三藏行狀", juan="1",
                     bytes=27520, purpose="不空行狀·一手底本", who="r1/F1"),
    "T50n2063": dict(title="比丘尼傳", juan="4", bytes=573109,
                     purpose="净检本传（卷1）·女性样本一手", who="r8"),
    "T50n2059": dict(title="高僧傳", juan="14", bytes=2794200,
                     purpose="慧远（卷6）·道安等·梁慧皎", who="r7", big=True),
    "T50n2060": dict(title="續高僧傳", juan="25", bytes=6612954,
                     purpose="玄奘(卷4)·智顗(卷17)·吉藏(卷11)·道宣", who="r1-r3", big=True),
    "T50n2061": dict(title="宋高僧傳", juan="30", bytes=2210272,
                     purpose="不空(卷1)·惠能(卷8)·鉴真(卷14)·赞宁", who="r1/r5/r6", big=True),
    "T50n2053": dict(title="大唐大慈恩寺三藏法師傳", juan="10", bytes=1816700,
                     purpose="玄奘传记·慧立彦悰", who="r2", big=True),
    "T48n2008": dict(title="六祖大師法寶壇經", juan="1", ce="48", bytes=343972,
                     verify="六祖大師", purpose="惠能义理一手底本（宗宝本·敦煌本另记）", who="r5"),
}


def gh(url: str):
    """GET a GitHub API URL → parsed JSON (with optional token for higher limits)."""
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "huayan-collection-g1-ingest")
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def gh_raw(url: str, expect: int = 0, tries: int = 4):
    """GET with `Accept: application/vnd.github.raw` → raw bytes (blobs up to ~100 MiB).
    长连接偶发 IncompleteRead（本环境实测 6.6 MB 会中途断），故**重试 + 长度校验**：
    若带 expect 字节且取回不足，视为不完整，退避重试。"""
    last = None
    for n in range(tries):
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github.raw")
        req.add_header("User-Agent", "huayan-collection-g1-ingest")
        tok = os.environ.get("GITHUB_TOKEN")
        if tok:
            req.add_header("Authorization", "Bearer " + tok)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            if expect and len(data) < expect:
                last = f"IncompleteRead({len(data):,}/{expect:,})"
                time.sleep(2 * (n + 1))
                continue
            return data
        except (http.client.HTTPException, urllib.error.URLError,
                ConnectionError, TimeoutError) as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(2 * (n + 1))
    raise RuntimeError(f"raw 取回失败（{tries} 次）：{last}")


_TREE_CACHE = {}   # tree_sha -> {path: entry}


def _tree(sha):
    if sha not in _TREE_CACHE:
        data = gh(f"{API}/repos/{REPO}/git/trees/{sha}")
        _TREE_CACHE[sha] = {e["path"]: e for e in data.get("tree", [])}
    return _TREE_CACHE[sha]


def resolve_tree(prefix):
    """Walk tree SHAs down a path like ['T','T50'] → dict {name: entry} of the leaf tree."""
    entries = _tree(DEFAULT_BRANCH)
    for seg in prefix:
        e = entries.get(seg)
        if not e or "sha" not in e:
            return {}
        entries = _tree(e["sha"])
    return entries


def find_blob(sig):
    """Locate <sig>.xml under the 册 T50 tree → (blob_sha, size)."""
    name = f"{sig}.xml"
    # xml-p5 顶层以「T」分册；T50 在册目录下。逐级 walk（失败再试单层）。
    for prefix in (["T", "T50"], ["T50"]):
        leaf = resolve_tree(prefix)
        hit = leaf.get(name)
        if hit and hit.get("type") == "blob":
            return hit["sha"], int(hit.get("size", 0))
    raise LookupError(f"未在 T50 目录树中找到 {name}（通道或已变更，须按台账 §一 重定位）")


def fetch_blob_text(blob_sha, expect=0):
    # 用 raw 媒体型直接取原始字节（非 base64 JSON）→ 支持大书且保 TEI。
    return gh_raw(f"{API}/repos/{REPO}/git/blobs/{blob_sha}", expect=expect)  # bytes, verbatim


def git_blob_sha(data: bytes) -> str:
    """按 git 自身算法从内容算 blob SHA-1：sha1('blob <len>\\0' + data)。"""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def raw_get(url, expect=0, tries=4):
    """从 raw.githubusercontent 直取逐字字节（api.github 限流时的后备通道）。
    带重试 + 长度校验（同 gh_raw），expect 非零且取回不足视为不完整。"""
    last = None
    for n in range(tries):
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "huayan-collection-g1-ingest")
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            if expect and len(data) < expect:
                last = f"IncompleteRead({len(data):,}/{expect:,})"
                time.sleep(2 * (n + 1))
                continue
            return data
        except (http.client.HTTPException, urllib.error.URLError,
                ConnectionError, TimeoutError) as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(2 * (n + 1))
    raise RuntimeError(f"raw 取回失败（{tries} 次）：{last}")


def log_row(sig, meta, blob_sha, nbytes, status, fname):
    """Append/refresh one row in INGEST_log.md keyed by 经号."""
    today = date.today().isoformat()
    row = (f"| {sig} | {meta['title']} | 册{meta.get('ce','50')} 卷{meta.get('juan','?')} | "
           f"{nbytes:,} | `{blob_sha[:10]}` | {today} | {status} | `{fname}` |\n")
    header = ("# CBETA 史传部入库日志（G1·fetch_cbeta_history.py 自动生成）\n\n"
              "> 一手 TEI/P5 逐字底本。勿擅改本目录内 .xml——一经改动即失一手性。\n"
              "> 通道：`api.github.com` git blob（详见台账 §一）。许可：CBETA 非营利用途，请保留说明。\n\n"
              "| 经号 | 题名 | 册卷 | 字节 | git-blob-SHA | 取回日期 | 状态 | 文件 |\n"
              "|---|---|---|---|---|---|---|---|\n")
    lines = []
    if LOG.exists():
        lines = [l for l in LOG.read_text(encoding="utf-8").splitlines(True)
                 if not l.startswith(f"| {sig} ")]
    body = "".join(lines) if lines else header
    if "| 经号 |" not in body:
        body = header + body
    body += row
    LOG.write_text(body, encoding="utf-8")


def ingest(sig, meta, apply_, max_bytes, raw=False):
    fname = f"{sig}.xml"
    path = DEST / fname
    if raw:
        vol = sig.split("n")[0]            # T48n2008 -> T48
        est = meta["bytes"]
        if path.exists():
            local = path.stat().st_size
            if local and abs(local - est) <= 4096:
                print(f"  ✓ {sig} 已在库且字节相符（{local:,} B）→ 幂等跳过")
                return "exists"
        if not apply_:
            print(f"  ⬇(raw) {sig} {meta['title']}：预估 {est:,} B（dry-run 未下载）")
            return "fetch"
        text = raw_get(f"{RAW_BASE}/T/{vol}/{fname}", expect=est)
        blob_sha = git_blob_sha(text)
        mk = meta.get("verify", "")
        if mk and mk.encode("utf-8") not in text:
            raise RuntimeError(f"{sig}：内容未含校验串「{mk}」（疑错经，拒入库）")
        sha256 = hashlib.sha256(text).hexdigest()
        print(f"  ⬇(raw) {sig} {meta['title']}：{len(text):,} B · blob={blob_sha[:10]} · SHA256={sha256[:12]}…")
        DEST.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text)
        log_row(sig, meta, blob_sha, len(text), f"已入库(raw) sha256:{sha256[:12]}", fname)
        return "fetch"
    blob_sha, size = find_blob(sig)
    est = size or meta["bytes"]
    if est > max_bytes:
        status = f"⏸ 超阈（{est:,} B > {max_bytes:,}；跑 --juan 后备）"
        print(f"  ⏸ {sig} {meta['title']}：{est:,} B → {status}")
        if apply_:
            log_row(sig, meta, blob_sha or "-", est, "待分卷", fname + "（未落盘）")
        return "skip"
    if path.exists():
        local = path.stat().st_size
        if local and abs(local - est) <= 4096:
            print(f"  ✓ {sig} 已在库且字节相符（{local:,} B）→ 幂等跳过")
            return "exists"
    if not apply_:
        print(f"  ⬇ {sig} {meta['title']}：预估 {est:,} B（dry-run 未下载）")
        return "fetch"
    text = fetch_blob_text(blob_sha, expect=est)
    sha256 = hashlib.sha256(text).hexdigest()
    print(f"  ⬇ {sig} {meta['title']}：{len(text):,} B · SHA256={sha256[:12]}…")
    DEST.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text)
    log_row(sig, meta, blob_sha, len(text), f"已入库 sha256:{sha256[:12]}", fname)
    return "fetch"


def juan_mode():
    print("分卷模式：大书须走 `DILA-edu/cbeta-normal-text`（一卷一檔，default_branch=main）。")
    print("  该仓库逐卷路径本会话尚未展开〔台账 §一 待核〕；展开后本模式按卷拼接并登记。")
    for sig, m in TARGETS.items():
        if m.get("big"):
            print(f"  ⏸ {sig} {m['title']}（{m['juan']} 卷）→ 待 cbeta-normal-text 结构确认")


def main():
    ap = argparse.ArgumentParser(description="CBETA 史传部一手底本入库")
    ap.add_argument("--apply", action="store_true", help="实际写盘（默认 dry-run）")
    ap.add_argument("--only", help="仅处理指定经号（如 T50n2063）")
    ap.add_argument("--max-bytes", type=int, default=20_000_000,
                    help="整取字节上限（raw 媒体型可支持至 ~100 MiB；默认 20 MB）")
    ap.add_argument("--juan", action="store_true", help="大书逐卷模式（报告）")
    ap.add_argument("--raw", action="store_true",
                    help="走 raw.githubusercontent 直取（api.github 限流时的后备；路径 T/<册>/<sig>.xml）")
    a = ap.parse_args()

    print("=" * 56)
    print("  G1 · 史传部 CBETA TEI/P5 入库" + ("  [APPLY]" if a.apply else "  [dry-run]"))
    print("=" * 56)
    if a.juan:
        juan_mode()
        return
    todo = {a.only: TARGETS[a.only]} if a.only else TARGETS
    tally = {"fetch": 0, "exists": 0, "skip": 0}
    for sig, meta in todo.items():
        tally[ingest(sig, meta, a.apply, a.max_bytes, raw=a.raw)] += 1
    print("-" * 56)
    print(f"取回 {tally['fetch']} · 已在库 {tally['exists']} · 待分卷 {tally['skip']}")
    if not a.apply and tally["fetch"]:
        print("（dry-run：加 --apply 方落盘并写 INGEST_log.md）")


if __name__ == "__main__":
    main()
