#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cbeta_id_audit.py — G2「经号校勘闸」：逐条校勘页面上的 CBETA 经号。

缘起（项目红线：逐字回源 / 宁缺不伪）：页面以「裸号」（省略册号，如 T1733、X0368）
引用经号者众，无从机械核验其「藏·册·号」是否自洽、是否在盘、题名是否相符。
本闸把这件事做成**可复跑、可举证、三态判定**的仪器。

定论三态（M3：三态 + 弃权；不逼二选一）：
  · 通过   —— 形态规范、官方目录树有此「册·号」、本地有底本、题名相符
  · 应订正 —— 能机械定出唯一规范式（多为「裸号」补册），或与官方树冲突
  · 待核   —— 无法唯一确定（跨册同号 / 官方树无此号 / 通道不可用）→ **绝不猜**

证据链（每一态必附证据，M4）：
  ① 形态自洽：经号自身语法 <藏><册>n<号>
  ② 官方目录树：`cbeta-org/xml-p5` 递归树 → 号↔册（SSOT·记 tree sha 与取数日）
  ③ 本地底本：`data/references/cbeta/*.xml` TEI 头 → 藏/册/号/题名/作者/卷数（逐字回源）
  ④ 页锚：`_p####x` 是否见于底本 `<pb n="####x">`

只读不改：绝不写回页面或底本。GitHub 通道复用 `fetch_cbeta_history.py`（M6：连接而非重造）。

用法：
  python scripts/cbeta_id_audit.py --build-index            # 取官方树 → 缓存 号↔册
  python scripts/cbeta_id_audit.py --selftest               # 验证「验证器」（已知对/错样例）
  python scripts/cbeta_id_audit.py                          # 出校勘表（TSV）
  python scripts/cbeta_id_audit.py --fetch-titles           # 为「未在盘」者补题名证据
环境：经代理 `--proxy http://127.0.0.1:7890`（或已设 HTTPS_PROXY）。GITHUB_TOKEN 可提额。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import fetch_cbeta_history as cb  # noqa: E402  （复用 gh / gh_raw / 常量）

DEFAULT_PAGES = ROOT / "docs" / "草稿" / "高僧传" / "僧传画像"
DEFAULT_CBETA = ROOT / "data" / "references" / "cbeta"
DEFAULT_WORK = Path(os.environ.get("TEMP", ".")) / "opencode" / "g2_cache"

# 经号形态：<藏><册>n<号>[A-Z]? （册/ n 可缺 → 裸号），尾可挂页锚 _p####x
TOKEN = re.compile(
    r"\b(?P<canon>[TXJAB])(?:(?P<vol>\d{2,3})n)?(?P<no>\d{3,4})(?P<suf>[A-Za-z]?)"
    r"(?:_p(?P<pg>\d{4})(?P<col>[a-c]))?\b"
)
FILENAME = re.compile(r"^([A-Z]+)(\d+)n(\w+)\.xml$")


def nkey(canon: str, no: str) -> str:
    """号归一：去前导零（数字号）；含字母者（如 a001）原样。"""
    return f"{canon}:{no.lstrip('0') if no.isdigit() else no}"

TEI = {
    "canon": re.compile(r'<idno type="canon">([^<]+)</idno>'),
    "vol": re.compile(r'<idno type="vol">([^<]+)</idno>'),
    "no": re.compile(r'<idno type="no">([^<]+)</idno>'),
    "title": re.compile(r'<title level="m"[^>]*>([^<]+)</title>'),
    "author": re.compile(r"<author>([^<]*)</author>"),
    "extent": re.compile(r"<extent>([^<]*)</extent>"),
}


def read_head(path: Path, nbytes: int = 200_000) -> str:
    with path.open("rb") as f:
        return f.read(nbytes).decode("utf-8", "replace")


def parse_tei(text: str) -> dict:
    out = {}
    for k, rx in TEI.items():
        m = rx.search(text)
        out[k] = (m.group(1).strip() if m else None)
    return out


def gh_head(url: str, nbytes: int = 8192, tries: int = 3) -> bytes:
    """只读文件头部（TEI 头在前 8 KB 内即可），避免整取数 MB 大书。"""
    last = None
    for n in range(tries):
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github.raw")
        req.add_header("User-Agent", "huayan-collection-g2")
        tok = os.environ.get("GITHUB_TOKEN")
        if tok:
            req.add_header("Authorization", "Bearer " + tok)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read(nbytes)
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            last = f"{type(e).__name__}: {e}"
    raise RuntimeError(f"取头部失败（{tries} 次）：{last}")


def raw_head(path: str, nbytes: int = 8192, tries: int = 3) -> bytes:
    """经 raw.githubusercontent.com 只读文件头（**不受 API 速率限制**，本会话实测可用）。
    失败再退 api.github.com（受 60 次/时限制）。"""
    try:
        return gh_head(f"{cb.RAW_BASE}/{path}", nbytes, tries=1)
    except Exception:
        return gh_head(f"{cb.API}/repos/{cb.REPO}/contents/{path}", nbytes, tries=tries)



# ---------------------------------------------------------------- 官方目录树
def build_index(work: Path, proxy: str | None) -> dict:
    if proxy:
        os.environ["HTTPS_PROXY"] = os.environ["HTTP_PROXY"] = proxy
    url = f"{cb.API}/repos/{cb.REPO}/git/trees/{cb.DEFAULT_BRANCH}?recursive=1"
    tree = cb.gh(url)
    idx: dict[str, list] = {}
    for e in tree.get("tree", []):
        m = FILENAME.match(Path(e["path"]).name)
        if not m:
            continue
        canon, vol, no = m.groups()
        idx.setdefault(nkey(canon, no), []).append([vol, e["path"], e["sha"]])
    data = {
        "_meta": {"source": f"{cb.REPO}@tree:{tree.get('sha')}",
                  "fetched": date.today().isoformat(),
                  "n_files": sum(len(v) for v in idx.values()),
                  "truncated": bool(tree.get("truncated"))},
        "by_no": idx,
    }
    work.mkdir(parents=True, exist_ok=True)
    (work / "cbeta_tree_index.json").write_text(
        json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def load_index(work: Path, proxy: str | None) -> dict:
    f = work / "cbeta_tree_index.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return build_index(work, proxy)


# ---------------------------------------------------------------- 本地底本
def local_canon(cbeta: Path) -> dict:
    """(canon,no)→文件名；并解析各底本 TEI 头。"""
    by_key, headers = {}, {}
    for p in sorted(cbeta.glob("*.xml")):
        m = FILENAME.match(p.name)
        if not m:
            continue
        canon, vol, no = m.groups()
        by_key[nkey(canon, no)] = p
        headers[p.name] = parse_tei(read_head(p))
    return by_key, headers


# ---------------------------------------------------------------- 收集 token
def collect(pages: Path) -> dict:
    files = [pages / "index.html", pages / "monolith.html"]
    files += sorted((pages / "portraits").glob("*.html"))
    hits: dict[str, dict] = {}
    for f in files:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        for m in TOKEN.finditer(text):
            tok = m.group(0)
            # 排除项目自用编号（J1–J6 / A1 / B1–B5 / C1–C6 一类 <3 位且无 n 者）
            if not m.group("vol") and len(m.group("no")) < 3:
                continue
            d = hits.setdefault(tok, {"n": 0, "files": {}, "kind": None,
                                      "canon": m.group("canon"), "vol": m.group("vol"),
                                      "no": m.group("no"), "suf": m.group("suf"),
                                      "pg": m.group("pg"), "col": m.group("col")})
            d["n"] += 1
            d["files"][f.name] = d["files"].get(f.name, 0) + 1
            d["kind"] = "规范式" if m.group("vol") else "裸号"
    return hits


# ---------------------------------------------------------------- 判定
def judge(tok: str, d: dict, idx: dict, by_key: dict, headers: dict,
          titles: dict) -> dict:
    canon, vol, no, suf = d["canon"], d["vol"], d["no"], d["suf"]
    key = nkey(canon, no + suf)
    cands = idx["by_no"].get(key, [])

    # ① 官方树查无此号（若仅「号+后缀」缺失而「号」在 → 后缀疑衍）
    if not cands:
        base = idx["by_no"].get(nkey(canon, no)) if suf else None
        if base:
            bvols = sorted({x[0] for x in base})
            return dict(verdict="应订正", tag="后缀疑衍",
                        proposed=f"{canon}{bvols[0]}n{no}", vol=",".join(bvols),
                        onhand="", title=(titles.get(nkey(canon, no), {}) or {}).get("title") or "",
                        note=f"官方树有 {canon}{bvols[0]}n{no} 而无 {canon}n{no}{suf}；后缀「{suf}」疑衍")
        return dict(verdict="待核", tag="官方树无此号",
                    proposed="-", vol="-", onhand="", title="",
                    note=f"{canon} 号 {no}{suf} 不在 xml-p5 目录树内（跨藏别或讹号，须人工）")

    vols = sorted({c[0] for c in cands})
    # ② 规范式：册号须与官方树一致
    if vol:
        if vol.lstrip("0") not in [v.lstrip("0") for v in vols]:
            return dict(verdict="应订正", tag="册号与官方树不符", proposed=f"{canon}{vols[0]}n{no}{suf}",
                        vol=",".join(vols), onhand="", title="",
                        note=f"页作 册{vol}，官方树作 册{'/'.join(vols)}")
        resolved_vol = vol
    else:
        if len(vols) > 1:
            return dict(verdict="待核", tag="跨册同号", proposed="-", vol=",".join(vols),
                        onhand="", title="",
                        note=f"号 {no} 见于多册（{'/'.join(vols)}），须人工定册")
        resolved_vol = vols[0]

    proposed = f"{canon}{resolved_vol}n{no}{suf}"
    lk = by_key.get(nkey(canon, no + suf))
    onhand = lk.name if lk else ""
    h = headers.get(onhand, {}) if onhand else {}
    # ③ 题名证据（本地头优先→缓存标题）
    title = h.get("title") or (titles.get(key, {}) or {}).get("title") or ""
    tsrc = "本地TEI" if h.get("title") else ("缓存" if title else "")
    if not title:
        title, tsrc = "", ""
    # ④ 页锚证据：CBETA 页锚可作 <pb n="0280a"> 或行锚 <lb n="0280a26">，二者皆算「在」
    anchor = ""
    if d.get("pg") and lk:
        full = lk.read_text(encoding="utf-8", errors="replace")
        pg = f'{d["pg"]}{d["col"]}'
        if re.search(rf'n="{pg}"', full):
            anchor = "锚在（pb 页锚）"
        elif re.search(rf'n="{pg}\d+"', full):
            anchor = "锚在（lb 行锚）"
        else:
            anchor = "锚缺"

    if lk:
        verdict, tag = "通过", "在盘·规范"
        note = f"底本 {onhand}；{tsrc}题名《{title}》" if title else f"底本 {onhand}"
        if anchor:
            note += f"；页锚 {d['pg']}{d['col']} {anchor}"
        if anchor == "锚缺":
            verdict, tag = "待核", "页锚不存"
        if not vol:
            verdict, tag = "应订正", "裸号→补册（可核）"
            note = f"页作裸号，规范式 {proposed}；底本 {onhand}" + (f"；题名《{title}》" if title else "")
    else:
        # 规范式且册号已对官方树、或裸号→补册：经号本身成立；「未在盘」只记于 在盘 列
        verdict, tag = ("应订正", "裸号→补册（未在盘）") if not vol else ("通过", "号正确·未在盘（登记待取）")
        note = f"规范式 {proposed}；题名{('《'+title+'》') if title else '未取'}；底本未入库（登记待取）"
    return dict(verdict=verdict, tag=tag, proposed=proposed, vol=resolved_vol,
                onhand=onhand, title=title, note=note)


_STOP = {"出处", "依据", "待核", "待采", "见于", "根据", "按语", "考异", "条目", "出处考",
         "按", "说", "考", "乙", "甲", "丙", "丁"}


def _claims(prefix: str) -> list:
    """从前缀取『页内所题书名』候选：① 最近一个《…》 ② 紧邻其前的中文词（3–12 字）。"""
    out = []
    bs = re.findall(r"《([^》]{1,60})》", prefix)
    if bs:
        out.append(bs[-1].strip())
    m = re.search(r"(?:[·\s、,，]|</[^>]*>)*([一-鿿]{3,12})\s*$", prefix)
    if m and m.group(1) not in _STOP:
        out.append(m.group(1))
    return out


def screen(pages: Path, idx: dict, by_key: dict, headers: dict, titles: dict,
           win: int = 70, minlcs: int = 2) -> list:
    """软门候选：页内**所题书名** vs 经号的**官方题名**（简→繁归一后取最长公共子串）。

    与「逐次出现」不同：只在**出现冲突证据**时才报——即该号近旁确有可辨书名、而它与官方题名
    几乎不相交（LCS < minlcs）。无书名证据者不报（不臆断）。宁多报勿漏报，**每条须回源复核**。
    只扫分册页与 index（不扫生成物 monolith，避免重复）。
    """
    import difflib
    try:
        import zhconv
        def tr(s):
            return zhconv.convert(s, "zh-hant")
    except Exception:
        def tr(s):
            return s
    flagged = []
    for f in [pages / "index.html"] + sorted((pages / "portraits").glob("*.html")):
        if not f.exists():
            continue
        text = re.sub(r"<[^>]+>", " ", f.read_text(encoding="utf-8"))
        for m in TOKEN.finditer(text):
            if not m.group("vol") and len(m.group("no")) < 3:
                continue
            r = judge(m.group(0), {"canon": m.group("canon"), "vol": m.group("vol"),
                                   "no": m.group("no"), "suf": m.group("suf"),
                                   "pg": m.group("pg"), "col": m.group("col")},
                      idx, by_key, headers, titles)
            title = r.get("title")
            if not title:
                continue
            t = tr(re.sub(r"\s+", "", title))
            best, bestc = None, -1
            for c in _claims(text[max(0, m.start() - win): m.start()]):
                w = tr(re.sub(r"\s+", "", c))
                lcs = difflib.SequenceMatcher(None, w, t, autojunk=False)\
                    .find_longest_match(0, len(w), 0, len(t)).size
                if lcs > bestc:
                    best, bestc = c, lcs
            if best is None:
                continue                      # 无书名证据 → 不臆断、不报
            if bestc < minlcs:
                flagged.append((f.name, m.group(0), r["proposed"], bestc, title, best))
    return flagged


def main():
    ap = argparse.ArgumentParser(description="G2 经号校勘闸")
    ap.add_argument("--pages", type=Path, default=DEFAULT_PAGES)
    ap.add_argument("--cbeta", type=Path, default=DEFAULT_CBETA)
    ap.add_argument("--work", type=Path, default=DEFAULT_WORK)
    ap.add_argument("--proxy", default=None)
    ap.add_argument("--build-index", action="store_true")
    ap.add_argument("--fetch-titles", action="store_true")
    ap.add_argument("--probe", nargs="+", metavar="ID",
                    help="按号验证若干经号（T1852 / T42n1824 / X531）：raw 通道取题名，不受 API 限额")
    ap.add_argument("--screen", action="store_true",
                    help="软门筛选：经号近旁书名 vs 官方题名（候选误号，须回源复核）")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", type=Path, default=None,
                    help="输出文件（UTF-8·LF）；不给则打到 stdout（经重定向易受 shell 编码影响）")
    a = ap.parse_args()
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        sys.stdout = a.out.open("w", encoding="utf-8", newline="\n")
    if a.proxy:
        os.environ["HTTPS_PROXY"] = os.environ["HTTP_PROXY"] = a.proxy

    if a.build_index:
        d = build_index(a.work, a.proxy)
        print(f"[索引] {d['_meta']['source']}  {d['_meta']['n_files']} 檔  "
              f"truncated={d['_meta']['truncated']}")
        return

    idx = load_index(a.work, a.proxy)
    by_key, headers = local_canon(a.cbeta)

    if a.probe:
        print("经号\t官方册\t题名\t标题来源")
        for tok in a.probe:
            m = TOKEN.search(tok)
            if not m:
                print(f"{tok}\t-\t（无法解析）\t-")
                continue
            canon, no, suf = m.group("canon"), m.group("no"), m.group("suf")
            key = nkey(canon, no + suf)
            cands = idx["by_no"].get(key)
            if not cands:
                print(f"{tok}\t-\t官方树无此号\t-")
                continue
            vols = sorted({c[0] for c in cands})
            path = cands[0][1]
            try:
                t = parse_tei(raw_head(path).decode("utf-8", "replace"))["title"]
                src = "raw"
            except Exception as e:
                t, src = None, f"失败:{type(e).__name__}"
            print(f"{canon}{no}{suf}\t{'/'.join(vols)}\t{t or '未取'}\t{src}")
        return

    hits = collect(a.pages)
    tf = a.work / "cbeta_titles.json"
    titles = json.loads(tf.read_text(encoding="utf-8")) if tf.exists() else {}

    if a.selftest:
        # 验证「验证器」：已知对（T50n2054 在盘）/ 已知错（T50n9999 无此号）/ 裸号（T0279）
        cases = {"T50n2054": None, "T50n9999": None, "T0279": None}
        for t in cases:
            m = TOKEN.search(t)
            dd = {"canon": m.group("canon"), "vol": m.group("vol"), "no": m.group("no"),
                  "suf": m.group("suf"), "n": 1, "files": {}}
            r = judge(t, dd, idx, by_key, headers, titles)
            print(f"  selftest {t:12s} → {r['verdict']:4s} [{r['tag']}] {r['note']}")
        return

    if a.screen:
        # 软门筛选：须先有题名证据（raw 通道补取，不受 API 限额）
        need = {k for k in {nkey(d["canon"], d["no"] + d["suf"]) for d in hits.values()}
                if k not in by_key and k not in titles}
        for k in sorted(need):
            c = idx["by_no"].get(k)
            if c:
                try:
                    titles[k] = parse_tei(raw_head(c[0][1]).decode("utf-8", "replace"))
                except Exception as e:
                    titles[k] = {"title": None, "error": str(e)}
        flags = screen(a.pages, idx, by_key, headers, titles)
        print("页\t页内经号\t建议规范式\tLCS\t官方题名\t页内所题书名")
        for row in flags:
            print("\t".join(str(x) for x in row))
        print(f"\n# 候选误号 {len(flags)} 项（须逐条回源复核）", file=sys.stderr)
        return

    # 补题名：未在盘且官方树定册者
    if a.fetch_titles:
        need = {}
        for tok, d in hits.items():
            key = nkey(d["canon"], d["no"] + d["suf"])
            if key in by_key or key in titles:
                continue
            c = idx["by_no"].get(key)
            if c and len({x[0] for x in c}) == 1:
                need[key] = c[0][2]
        print(f"[题名] 待取 {len(need)} 部（只读头部 8 KB · raw 通道）", file=sys.stderr)
        for key, sha in need.items():
            path = idx["by_no"][key][0][1]
            try:
                titles[key] = parse_tei(raw_head(path).decode("utf-8", "replace"))
            except Exception as e:
                titles[key] = {"title": None, "error": str(e)}
        a.work.mkdir(parents=True, exist_ok=True)
        tf.write_text(json.dumps(titles, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[题名] 缓存 → {tf}", file=sys.stderr)

    rows = []
    for tok, d in sorted(hits.items(), key=lambda kv: (-kv[1]["n"], kv[0])):
        r = judge(tok, d, idx, by_key, headers, titles)
        pages = ",".join(sorted(d["files"]))
        rows.append((tok, d["kind"], d["n"], pages, r))

    order = {"应订正": 0, "待核": 1, "通过": 2}
    rows.sort(key=lambda x: (order[x[4]["verdict"]], -x[2]))
    tally = {"通过": 0, "应订正": 0, "待核": 0}
    print("经号\t形态\t次数\t页\t定论\t子类\t建议规范式\t官方册\t在盘底本\t题名\t说明")
    for tok, kind, n, pages, r in rows:
        tally[r["verdict"]] += 1
        print("\t".join([tok, kind, str(n), pages, r["verdict"], r["tag"],
                         r["proposed"], str(r["vol"]), r["onhand"],
                         r["title"] or "", r["note"]]))
    print(f"\n# 合计：通过 {tally['通过']} · 应订正 {tally['应订正']} · 待核 {tally['待核']}"
          f"（共 {len(rows)} 种；索引 {idx['_meta']['source']}）", file=sys.stderr)


if __name__ == "__main__":
    main()
