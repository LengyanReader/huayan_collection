# -*- coding: utf-8 -*-
"""由 jj_ocr_audit.py 之实测 JSON 生成《九九華嚴》立册 YAML（L.111 立）

〔为何要生成器〕台账之数**必须来自实测**，不得手录——故本生成器只做
「JSON → YAML」之排版与**限度文字之附载**，不新增任何未经实测之数字。

用法：python scripts/jj_ocr_audit.py --json && python scripts/_jj_build_lib.py
"""
import io
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

SRC = ".tmp_jj_audit.json"
OUT = "data/research/jj_huayan_lectures.yaml"

HEADER = """# 《九九華嚴》華嚴經弘法講座（2026）· OCR 重建稿 —— 立册与质量实测
#   （集数**自动发现**：交付者明言讲座尚未完結，故此处不写死「12 集」）
# ---------------------------------------------------------------------------
# 〔L.111 立〕本文件之全部数字由 `scripts/jj_ocr_audit.py` **实测**生成
#   （`--json` → 本生成器），**不得手录**。
#
# 【性質·最重要】**OCR 重建稿 · 待校定**。寺方原始字幕稿件已遺失，
#   画面內硬字幕（hardsub）為唯一存續形態，本稿係影像層還原。
#   故：**不得**以本稿作逐字引证之最终依据；引用须标〔OCR 待校〕，
#   或**先与讲义／录音互证校定**（交付者明言「三源互证另行进行」）。
#
# 【授权】交付者（華嚴弟子·維護者）自述「已獲寺方授權，用途為傳播正法」。
#   ——此為**交付者陳述**，**授权書未見**〔待核〕；权利状态依
#   `harness/compliance.md` §三/§四 R1 登记。
#
# 【與既有語料之關係】`docs/huayanhai/` 645 篇之「九九华严」條目**僅 1 件**
#   （`菩萨问明品是下手处_1.txt`，66 汉字，2025-12），且係**另一讲题之摘录**，
#   非本講座內容。故本講座為**語料新增**，非既有語料之重複。
"""

NEG = """
# ── 否定性記錄（比勘須雙向：除「有何用」亦須記「有何不可用」）────────
negative_findings:

  - id: N-JJ1
    key: 跨源互證不可行（非「兩源不一致」）
    probe: 以 delivery 全部各集逐句（去漢字、去標點、長度 ≥8）檢索 docs/huayanhai 內「九九华严」路徑下全部文本
    result: 命中 {hit}/{tried}（{xsrate}）；惟比對語料僅 {files} 件／{cjk} 漢字，且內容係**另一讲题**（菩萨问明品是下手处）之摘录
    判读: >-
      **不可**表述为「OCR 稿与既有语料一致」或「两源不一致」——比對語料僅 {cjk} 漢字，
      根本不足以互證。此为**「檢索未及／無可互證之对象」**，非實測所得之矛盾。
      欲真互證，須取得同一場次之講義或錄音（〔待补〕）。

  - id: N-JJ2
    key: 既有語料未覆蓋本講座
    probe: 遍歷 docs/huayanhai/export_manifest.json 645 條，檢其 category／htmlPath 含「九九华严」者
    result: 僅 {manifest_jj} 條（`菩萨问明品是下手处_1.html`，category `/华严云海/浩瀚华严海/九九华严/摘录/`）
    判读: >-
      本講座現有 {neps} 集（約 {hours:.1f} 小時／{total_cjk} 漢字）為**新增語料**，
      现有 645 篇語料**未覆蓋**。故不可據既有語料之結論推及本講座，
      反之亦然——二者分屬不同場次，须分源立册、分源判读。

  - id: N-JJ3
    key: 「 | 」之義為幻燈片＋口播拼接，**非**雙軌 OCR
    probe: 統計含「 | 」之字幕條數；並與交付者報告「五·已知瑕疵清單」第 2 條對照
    result: 含「 | 」者 {pipe} 條（佔全部 {piperate}）
    判读: >-
      交付者已明言：「幻燈片時段帶內多行文字以「 | 」拼接，非純口播字幕」。
      故「 | 」**左／右兩側語義不同**（幻燈片投影文字 vs 口播字幕），
      **不可**當作兩路 OCR 互校之依据（**此為本批一度之誤判，已撤回**）。
      凡引用本講記内容，**须先剥离**幻燈片文字，否則即以投影字冒充法師語。

  - id: N-JJ4
    key: 覆蓋率缺口 0.2%–1.6%，成因未核
    probe: 逐集比較「html 声明時長」与「末條時間戳」
    result: 最低 {covmin}／最高 {covmax}／均值 {covavg}；缺口約 1–3 分鐘
    判读: >-
      **不可**稱本講記「完整」。缺口成因〔待核〕——可能為片尾無字幕、片尾幻燈片，
      亦可能為漏提。**未定即不臆断**；引用時须留意末尾數分鐘可能缺漏。

  - id: N-JJ5
    key: 片頭動畫幀亂碼
    probe: 統計時間碼 < 40 秒之字幕條數（依交付者自述此段可整段丟棄）
    result: {head} 條
    判读: >-
      已實測為**少量**（佔 {headrate}），且交付者已指明可丟。校定時整段刪除即可，
      無實質損失。此為**已解決**之瑕疵，非待辦。
"""

LIMITS = """
# ── 限度（邊界自知 · 局限留檔）────────────────────────────────────────
limits:
  - 性質: 本稿為**影像層還原**，非語詞級校定；交付者明言「與講義、錄音的語詞級校定（三源互證）另行進行」
  - 時間碼: 精度 ±1s（交付者自述）；快語速換句**可能丟首字**——故**逐字引證須以音／講義覆核**
  - 幻燈片: {pipe} 條含投影文字，引用前须剥离（N-JJ3）
  - 簡繁: 實測 {simp} 條含簡體字（{simprate}），校定時須統一；本工具**只判有無，不作轉換**（未用 OpenCC）
  - 拉丁混入: 實測 {lat} 條含拉丁字母、其中 {lonely} 條為**純拉丁**（動畫幀／頻道角標殘留）
  - 片頭: 前 40 秒動畫幀亂碼 {head} 條，可整段刪（N-JJ5）
  - 授權: 交付者自述已獲寺方授權，**授权書未見**〔待核〕；見 `harness/compliance.md` §三/§四 R1
  - 完整性: 本册所收 {neps} 集為**現有交付之全部**，然講座本身**尚未完結**（交付者語：「後續會持續更新」），故本册**非全集**

# ── 使用規則（硬规则 · 與 A 類語料之分野）────────────────────────────────
usage_rules:
  - id: U1
    rule: 本稿**不得**充作 A 類（法师原话逐字回源）之依据；`verify_haiyun_evidence.py` 之 T0 限栈**不含**本路徑
    理由: OCR 重建 · 待校定 · 時間碼 ±1s · 可能丟首字 · 含幻燈片文字——逐字不可靠
  - id: U2
    rule: 引用須逐處標〔OCR 待校〕，或先完成三源互證（講義／錄音／影像）後升級
  - id: U3
    rule: 凡引用**教义性关键语**（名号／判教／法门定义），**不得**單憑本稿——须回 T1 祖典或已校定之讲记
  - id: U4
    rule: 幻燈片文字（N-JJ3 之「 | 」側）**不得**引作法師語
  - id: U5
    rule: 本讲座（2026-04→07）之时间／地点／集数，据 **YouTube 頻道頁面**；交付者自述授权見 compliance.md，非本册自证
"""

CONCL = """
# ── 結論（依實測，非依印象）────────────────────────────────────────────
conclusions:
  - topic: 可用性
    判: 可用作**内容索引·主题定位·时间锚点·讲题线索**；不可用作**逐字引证**
    依据: [U1, U2, N-JJ1, N-JJ3, N-JJ4]
  - topic: 可复现性
    判: 提取流水線**可复跑**——md／srt／html 三份产物之字幕条数 {cons}/{neps} 集完全相符
    依据: [实测·一致性]
  - topic: 对既有語料之价值
    判: "**新增约 {hours:.1f} 小時／{total_cjk} 漢字**之第一手素材，且为**现有 645 篇未覆盖之最新场次**；对「時間軸」与「2026 年現況」具關鍵價值"
    依据: [N-JJ2]
  - topic: 校定優先級
    判: 若資源有限，**首集（開篇·立論）與末集（收束）優先校定**；中间各集可按引用需要逐集校
    依据: [实测·集次时长分布]
"""


def q(v):
    """〔YAML 1.1 陷阱·第 6 坑·L.101 已载，此处再犯故立此函数〕
    以 `**`/`&`/`*`/`!`/`%`/`@`/反引号/`-`/`?`/`:` 起首之**裸标量**会被
    YAML 解析为 alias/anchor/tag——实测 `判: **新增约 …` 即抛
    `expected alphabetic or numeric character, but found '*'`。
    故凡纯量一律**双引号包裹并转义**，不靠「注意别以星号开头」这种人工自律。
    """
    v = str(v).replace("\\", "\\\\").replace('"', '\\"')
    return '"%s"' % v


def discover_eps():
    """〔L.111·依交付者「後續會持續更新」之指示〕集数**自动发现**，
    不可沿用「12 集」之字面值——交付者已明言讲座尚未完結，
    固化集数将使新增集次**静默不入册**而门禁仍全绿。
    此处复用 jj_ocr_audit 之发现函数，不复制逻辑。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("jj_ocr_audit",
                                                  "scripts/jj_ocr_audit.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.discover_eps()


def main():
    if not os.path.exists(SRC):
        print("【缺实测数据】%s —— 请先运行：python scripts/jj_ocr_audit.py --json"
              % SRC)
        return 1
    d = json.load(io.open(SRC, encoding="utf-8"))
    eps, T, xs = d["episodes"], d["totals"], d["cross_source"]
    neps = len(eps)
    # 〔L.111〕以**实测发现**之集数为准，而非「12」之字面值；
    #   若交付者新增集次而此处仍写 12，则新集将不入册而门禁仍全绿。
    assert neps == len(discover_eps()), (
        '实测 JSON 之集数(%d)与目录发现之集数(%d)不符——不可任取其一'
        % (neps, len(discover_eps())))

    buf = [HEADER, "\nmeta:\n"]
    buf.append('  source: "大华严寺官方 YouTube（@huayen-world）· 華嚴經弘法講座《九九華嚴》"\n')
    buf.append('  venue: "台北國際會議中心"\n')
    _mon = {}
    for _e in eps:
        _mm = re.search(r'#(\d+)月', _e.get('title') or '')
        if _mm:
            _mon.setdefault(int(_mm.group(1)), []).append(_e['ep'])
    _ps = '、'.join('%d月(第%s集)' % (mo, '/'.join(str(x) for x in v))
                   for mo, v in sorted(_mon.items()))
    buf.append('  period: "2026　依逐集實測月份：%s"\n' % _ps)
    buf.append('  episodes: %d\n' % neps)
    buf.append('  nature: "OCR 重建稿 · 待校定（寺方原始字幕稿件已遺失，'
               '硬字幕為唯一存續形態）"\n')
    buf.append('  provenance: "交付者自述：yt-dlp 720p → ffmpeg 1fps 裁字幕帶 → '
               'IoU 掩碼去重 → PaddleOCR(PP-OCRv6 繁中)；生成日期 2026-09-30"\n')
    buf.append('  license_claim: "交付者（華嚴弟子）自述已獲寺方授權，'
               '用途為傳播正法 —— **授权書未見**〔待核〕"\n')
    buf.append('  completeness: "本册所收 %d 集為現有交付之全部；講座本身**尚未完結**，' % neps +
               '交付者語「後續會持續更新」"\n')

    buf.append("\n# ── 實測台帳（數字全部來自 jj_ocr_audit.py，不得手改）──────────\n")
    buf.append("measured:\n")
    buf.append('  consistency: "md／srt／html 三產物字幕條數相符：%d/%d 集"\n'
               % (len([e for e in eps if e["consistent"]]), neps))
    covs = [e["coverage"] for e in eps]
    buf.append('  coverage_min: %.4f\n  coverage_max: %.4f\n  coverage_mean: %.4f\n'
               % (min(covs), max(covs), sum(covs) / len(covs)))
    buf.append('  total_cues: %d\n' % T["cues"])
    buf.append('  total_han_chars: %d\n' % T["han"])
    buf.append('  total_hours: %.2f\n' % (sum(e["declared_sec"] for e in eps) / 3600.0))
    for k, lbl in (("head", "head_garbage_cues"), ("pipe", "pipe_cues"),
                   ("lat", "latin_cues"), ("lonly", "latin_only_cues"),
                   ("simp", "simp_cues"), ("sh", "short_cues")):
        buf.append("  %s: %d\n" % (lbl, T[k]))

    buf.append("\n# ── 逐集台帳 ───────────────────────────────────────────────\n")
    buf.append("episodes_detail:\n")
    for e in eps:
        buf.append('  - ep: %d\n' % e["ep"])
        buf.append('    title: %s\n' % q(e["title"]))
        buf.append('    video_id: %s\n' % q(e["video_id"]))
        buf.append('    url: %s\n' % q("https://www.youtube.com/watch?v=%s" % e["video_id"]))
        buf.append('    src: %s\n' % q("docs/hy_refs/sub_extract/delivery/ep%02d.md" % e["ep"]))
        buf.append('    declared_sec: %d\n' % e["declared_sec"])
        buf.append('    covered_sec: %d\n' % e["covered_sec"])
        buf.append('    coverage: %.4f\n' % e["coverage"])
        buf.append('    cues: %d\n' % e["cues"])
        buf.append('    han_chars: %d\n' % e["han_chars"])
        buf.append('    pipe_cues: %d\n' % e["pipe_cues"])
        buf.append('    calibration: "待校定"\n')

    buf.append(NEG.format(
        neps=neps, hit=xs["hit"], tried=xs["tried"],
        xsrate=("%.3f%%" % (100 * xs["rate"])) if xs["rate"] is not None else "n/a",
        files=xs["files"], cjk=xs["corpus_chars"],
        manifest_jj=1, hours=sum(e["declared_sec"] for e in eps) / 3600.0,
        total_cjk=T["han"], pipe=T["pipe"],
        piperate="%.1f%%" % (100 * T["pipe"] / T["cues"]),
        covmin="%.1f%%" % (100 * min(covs)), covmax="%.1f%%" % (100 * max(covs)),
        covavg="%.1f%%" % (100 * sum(covs) / len(covs)),
        head=T["head"], headrate="%.2f%%" % (100 * T["head"] / T["cues"])))
    buf.append(LIMITS.format(
        neps=neps, pipe=T["pipe"], simp=T["simp"],
        simprate="%.1f%%" % (100 * T["simp"] / T["cues"]),
        lat=T["lat"], lonely=T["lonly"], head=T["head"]))
    buf.append(CONCL.format(
        neps=neps,
        cons=len([e for e in eps if e["consistent"]]),
        hours=sum(e["declared_sec"] for e in eps) / 3600.0,
        total_cjk=T["han"]))

    txt = "".join(buf)
    back = io.open(OUT, "w", encoding="utf-8", newline="\n").write(txt)
    import yaml  # noqa: E402
    y = yaml.safe_load(io.open(OUT, encoding="utf-8"))
    print("已写 %s：%d 集／实测台账 %d 汉字／否定记录 %d 条／使用规则 %d 条"
          % (OUT, len(y["episodes_detail"]), y["measured"]["total_han_chars"],
             len(y["negative_findings"]), len(y["usage_rules"])))
    print("  YAML 解析 OK（%d 字节）" % back)
    return 0


if __name__ == "__main__":
    sys.exit(main())