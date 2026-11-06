# -*- coding: utf-8 -*-
"""三语专题页生成器（自包含 skip_html 页 · 承 demo 页 shell）。

数据流（全部机械派生，不手填正文）：
  data/alignment/tibetan-derge-toc.json                       45 章骨架
  data/alignment/tibetan_chinese_pin_plan_L360.json            藏章↔汉品 对应 + 进度
  data/translation/tibetan_avatamsaka_trilingual_roadmap.json  里程碑 / 会话单元 / 验收门禁
  data/translation/tibetan_avatamsaka_trilingual_segments*.json 三语段（藏逐字 / MITRA 汉·英）
  → web/demo/articles/tibetan-avatamsaka-trilingual.html

体例（用户指定）：**一段藏文 → 一段汉语 → 一段英文**，逐段三语并列；
汉/英一律 MITRA 模型译、标〔模型译·未校订〕；藏文一律德格原字形（逐字回源）。
未译段如实标〔待译〕，不占位冒充。

用法（项目根）：
  C:\\Users\\data\\miniconda3\\envs\\hy_py312\\python.exe -X utf8 ^
    workspace/tibetan-avatamsaka-translation/tools/gen_trilingual_article.py
"""
import io, json, re, glob

SHELL = 'web/demo/articles/tibetan-avatamsaka-alignment-demo.html'
OUT = 'web/demo/articles/tibetan-avatamsaka-trilingual.html'
PLAN = 'data/alignment/tibetan_chinese_pin_plan_L360.json'
ROADMAP = 'data/translation/tibetan_avatamsaka_trilingual_roadmap.json'
TOC = 'data/alignment/tibetan-derge-toc.json'
SEG_GLOB = 'data/translation/tibetan_avatamsaka_trilingual_segments*.json'
ART_ID = 'tibetan-avatamsaka-trilingual'
TITLE = '藏译华严 · 藏汉英三语对读（德格甘珠尔 Toh 44）'

plan = json.loads(io.open(PLAN, encoding='utf-8').read())
roadmap = json.loads(io.open(ROADMAP, encoding='utf-8').read())
toc = json.loads(io.open(TOC, encoding='utf-8').read())


def cell(s):
    """markdown 表格单元安全化（ASCII 竖线会破表）。"""
    return str(s).replace('|', '｜')


def load_seg_files():
    out = []
    for fn in sorted(glob.glob(SEG_GLOB)):
        d = json.loads(io.open(fn, encoding='utf-8').read())
        out.append((fn, d))
    return out

seg_files = load_seg_files()
n_chap = len(seg_files)
n_seg = sum(len(d.get('segments') or []) for _, d in seg_files)
n_done = sum(1 for _, d in seg_files for s in (d.get('segments') or []) if s.get('status') == 'done')
t = plan['totals']
mc = roadmap['measured_constraints']

# ── §2 品目规划表（45 章全量 · 含三语进度列） ──
pin_table = '\n'.join(
    '| %d | %s | %s | %s | %s | %s | %s |' % (
        r['tibetan_ch'], r['vol'], r['start_folio'],
        cell(('品%d〈%s〉' % (r['pin'], r['pin_title_zh'])) if r['pin'] and r['rule'] != '藏独有'
             else (r['pin_title_zh'] or '〔待核〕')),
        cell(r['rule'] or '—'),
        cell(r['tibetan_open_seed'][:30] + ('…' if len(r['tibetan_open_seed']) > 30 else '')),
        cell(r['trilingual_status']))
    for r in plan['chapters'])

# ── §3 里程碑总表 + 逐里程碑细目 ──
ms_rows, ms_detail = [], []
for m in roadmap['milestones']:
    sess = m['sessions']
    mach = sum(1 for g in m['gate'] if g['kind'] != 'manual')
    man = len(m['gate']) - mach
    ms_rows.append('| %s | %s | %s | %s | %d（机器 %d＋人工 %d） |' % (
        m['id'], cell(m['name']), cell(m['batch']),
        cell('；'.join('[%s] %s' % (s['no'], s.get('est', '—')) for s in sess)), mach + man, mach, man))
    det = ['### %s · %s' % (m['id'], m['name']), '',
           '- 批次：%s ｜目标：%s' % (m['batch'], m['goal']), '',
           '**会话单元**（一会话＝一单元，可中断续跑）：', '']
    for s in sess:
        det.append('- 〔单元 %s〕%s' % (s['no'], s['scope']))
        det.append('  - 负荷：%s ｜预估：%s ｜%s' % (
            s.get('load', '—'), s.get('est', '—'),
            '单会话可完成' if s.get('one_session') else '跨会话（须再拆）'))
    det += ['', '**验收门禁**：', '']
    for g in m['gate']:
        det.append('- `%s`（%s）%s' % (g['id'], '人工闸门' if g['kind'] == 'manual' else '机器判定', g['say']))
    ms_detail.append('\n'.join(det))
milestone_table = '\n'.join(ms_rows)
milestone_detail = '\n\n'.join(ms_detail)
sched_notes = '\n'.join('- ' + s for s in roadmap.get('scheduling_notes', []))

# 会话口径总表：L.360 批量实测（seg1 zh 200 tokens / 4597.8 s）后，各里程碑会话单元的真实粒度
gran_rows = []
for m in roadmap['milestones']:
    for s in m['sessions']:
        if s.get('one_session'):
            continue
        gran_rows.append('| %s | %s ｜%s｜ | %s | %s |' % (
            m['id'], s['no'], cell(s['scope']), cell(s.get('load', '—')), cell(s.get('est', '—'))))
granularity_note = ''
if gran_rows:
    granularity_note = ('\n> **实测后的诚实口径**：会话＝*编排*单元（切段/启动/落盘确认/重生页面，单会话内可完成）；'
                        '机时按 L.360 W1 全量实测 ≈30–50 min/段（双语），一章 6 段 ≈ 3.5–5 h **单长会话后台续跑**'
                        '（`status!=done` 自动续），算力按用户决策逐点推进不冒进；'
                        '下表单元仍非单会话可完成，粒度已按实测改标：\n\n'
                        '| 里程碑 | 会话单元 | 负荷 | 实测预估 |\n|---|---|---|---|\n' + '\n'.join(gran_rows))

# ── §4 三语段（一段藏 → 一段汉 → 一段英） ──
blocks = []
for fn, d in seg_files:
    ch = (d.get('chapter') or {})
    tc = ch.get('tibetan_no')
    blocks.append('### 藏章%s（德格 %s · 起叶 %s）· 对应：%s' % (
        tc, ch.get('derge_vol'), ch.get('start_folio'), cell(ch.get('chinese_correspondence'))))
    for s in d.get('segments') or []:
        bo = cell(s['bo'])
        blk = ['', '#### 段 %d〔%s %s · %s〕%s' % (
            s['no'], s['vol'], s['folio'], s['marker'], '（题名块）' if s['kind'] == 'title' else ''), '',
            '**藏（德格原字形·逐字回源）**', '', '> ' + bo, '']
        if s.get('zh'):
            mt = s.get('zh_meta') or {}
            blk += ['**汉（MITRA 模型译·未校订）**', '', '> ' + cell(s['zh']).replace('\n', ' ').strip(), '',
                    '> 〔引擎 %s · 生成 %ss · 输出 %s tokens · 复读截断 %s〕' % (
                        mt.get('engine', 'mitra-qwen35-translate'), mt.get('gen_s', '?'),
                        mt.get('out_tokens', '?'), '是' if mt.get('clipped_repeat') else '否'), '']
        else:
            blk += ['**汉**', '', '> 〔待译 · 该段尚未产出（作业进行中／属后续会话）〕', '']
        if s.get('en'):
            mt = s.get('en_meta') or {}
            blk += ['**EN (MITRA model translation · unproofed)**', '',
                    '> ' + cell(s['en']).replace('\n', ' ').strip(), '',
                    '> 〔engine %s · %ss · %s tokens · repeat-clipped %s〕' % (
                        mt.get('engine', 'mitra-qwen35-translate'), mt.get('gen_s', '?'),
                        mt.get('out_tokens', '?'), 'yes' if mt.get('clipped_repeat') else 'no'), '']
        else:
            blk += ['**EN**', '', '> 〔pending · not yet produced〕', '']
        blocks.append('\n'.join(blk))
seg_blocks = '\n\n'.join(blocks)

cf = roadmap.get('conflicts') or plan.get('conflicts') or []
cf_lines = '\n'.join('> - 藏章%d：%s（早期实证 品%s → 现记 品%s）' % (
    c['tibetan_ch'], c['note'], c.get('dropped'), c.get('kept')) for c in cf) \
    or '> - 无（派生过程中无配对冲突）'

doc_md = f"""# {TITLE}

> **本页任务**：把德格甘珠尔《大方广佛华严经》（Toh 44，藏文 45 章 / 115 bam po）**逐段译为三语并列**——
> 一段藏文（德格原字形，逐字回源）→ 一段汉语 → 一段英文（后二者由本地模型 `buddhist-nlp/mitra-qwen35-translate` 9B 试译）；
> 并把后续路线拆成**里程碑 → 单会话工作量 → 验收门禁**三层，使每一层都可被观察、可被复算。
> 汉 / 英译文一律视为**〔模型译·未校订〕**，只作工作草稿；**不**等同于本仓既有的 CBETA 祖本引文（祖本引文另按 T10n0279 繁体逐字回源，见〈藏汉英对读 · 初探〉页）。

## 0. 体例与硬约束

| 项 | 口径 |
|---|---|
| 段制 | 一段藏文 → 一段汉语 → 一段英文；段为最小对齐单位 |
| 藏文来源 | 自德格底本 `{{T44-N}}…{{T44-N+1}}` 区间**字节切片**，逐段 norm() 复验可追回原文；**绝不手打藏文** |
| 切段规则 | {roadmap['scope_note']} |
| 汉 / 英 | MITRA 9B（bf16 · CPU · greedy）模型译，**未校订**；长输出复读已作 n-gram 禁用 + 周期截断 |
| 品目对应 | 只用已机器实证的对应；未实证一律〔待核〕，不代立论 |
| 完成判定 | 门禁（§3）为被观察到的证据；未全绿不得称完成 |

## 1. 结构事实（可回源）

藏文 **{t['tibetan_chapters']} 章** ／ 八十汉译 **39 品** ／ 六十汉译 **34 品**。
本批派生的对应统计：**已实证逐章平行 {t['verified_pairs']} 对** · **藏独有 {t['tibetan_only']} 章** · **前段章界不平行 {t['front_unparallel']} 章（〔待核〕）**。

对应律（机器实证所得，非臆测）：

- **藏章 14–31 ＝ 汉品 9–26**（序号差 5，逐章平行）— 证据：对勘批 b1–b4 ＋ L.352 重勘覆写
- **藏章 33–38 ＝ 汉品 27–32**、**藏章 39–45 ＝ 汉品 33–39**（序号差 6）— 证据：b5 / b6（L.357 章末自题定章收官）
- **藏章 11〈如来华严〉· 藏章 32〈普贤宣说〉＝ 藏独有**（无汉文平行品；藏32 归属仍〔待核〕）
- **藏章 1–10、12–13 ↔ 汉品 1–8 区间：章界不平行**〔待核〕（L.352 finding：不平行限于前段）

配对冲突记录（派生过程中如实保留，不静默取舍）：

{cf_lines}

## 2. 章节品目规划表（德格 45 章全量）

| 藏章 | 卷 | 起始叶码 | 对应汉品（八十） | 对应律 | 藏文开篇（德格原字形·节选） | 三语进度 |
|---|---|---|---|---|---|---|
{pin_table}

> 〔口径〕「对应汉品」= 对勘批机械收集＋L.352 覆写所得；对应律「—」= 前段未定界〔待核〕；「三语进度」= 数据层实测计数。全量种子见 `{TOC}`，派生表见 `{PLAN}`。

## 3. 后续路线：里程碑 → 会话单元 → 验收门禁

拆解决策口径：

1. **一会话＝一编排单元**：单元尺寸由实测吞吐反推——{mc['session_unit_cost_estimate']}；「一章开篇 6 段」为最小**工作**单元（会话内完成切段/启动/落盘确认，翻译机时后台续跑跨会话）。
2. **证据分层**：先译已实证平行段（差5 → 差6），前段（章界未定）刻意置后，避免产出无法对齐的孤立译文。
3. **门禁两类**：`机器判定` 由 `tools/check_trilingual_gates.py` 实测（能判则判，前提数据缺失判 PENDING，**不冒充 PASS**）；`人工闸门` 须在 `tasks/PROGRESS.md` 留证据行方得通过。
4. **成本上限可见**：{mc['gen_throughput_tok_per_s']} token/s、{mc['cold_load_s']}s 冷加载（热加载 {mc['warm_load_s']}s）——规模判断一律以实测为准，不估算冒充实测。

| 里程碑 | 名称 | 批次 | 会话单元（预估） | 验收门禁 |
|---|---|---|---|---|
{milestone_table}

> 顺序：{ ' → '.join(roadmap.get('ordering', [])) }。排产说明：
{sched_notes}
{granularity_note}

### 3.1 逐里程碑细目

{milestone_detail}

## 4. 已产出三语段（{n_chap} 章 · {n_seg} 段 · 其中 {n_done} 段已试译）

{seg_blocks}

> 〔诚实边界〕以上仅覆盖各章**开篇**，非全品；未译段如实标〔待译〕。模型译未经人工校订，不作引文使用，不得替代 CBETA 祖本文字。

## 5. 复现与续跑

```text
# ① 逐字回源切段（一会话一章；--dry-run 可先复验不写数据层）
python workspace/tibetan-avatamsaka-translation/tools/extract_trilingual_segments.py --chapter 1 --max-paras 6
# ② 品目规划表派生（45 章 · 含三语进度列）
python workspace/tibetan-avatamsaka-translation/tools/build_pin_plan.py
# ③ MITRA 批量试译（可续跑：只处理 status != done 的段）
python workspace/tibetan-avatamsaka-translation/tools/mitra_batch_translate.py --chapter 1
# ④ 重生成本页
python workspace/tibetan-avatamsaka-translation/tools/gen_trilingual_article.py
# ⑤ 里程碑门禁（machine 项实测判定）
python workspace/tibetan-avatamsaka-translation/tools/check_trilingual_gates.py --milestone M0
```

运行环境（实测口径）：`hy_py312` · torch CPU-only（{mc['hardware']}）· **必须** bf16 加载（{mc['must_bf16']}）·
生成 {mc['gen_throughput_tok_per_s']} token/s（≈{mc['gen_seconds_per_token']} s/token）· {mc['repeat_risk']}。

## 6. 未竟（按里程碑）

- 〔未竟·M0〕藏章1 开篇其余段（单章正文实测 188,713 字符／约 3,914 句读）；本批只取 6 段。
- 〔未竟·M1〕吞吐标定表与算力决策（含人工闸门）。
- 〔未竟·M2/M3/M4〕差5、差6 两跨段与入法界品的逐章开篇三语。
- 〔未竟·M5〕人工校订：模型译升格为可引用译文（须双轨保留原译）。
- 〔未竟·M6〕三语术语库；〔未竟·M7〕藏独有二章；〔未竟·M8〕前段章界比对。
- 〔待核〕偈颂分行对齐（藏文 `།།` 七言颂与汉译偈组对应）。
"""

# ── 注入自包含页（shell 承 demo 页；页头两处硬编码标题随之替换） ──
html = io.open(SHELL, encoding='utf-8').read()
m = re.search(r'var ARTICLE = (\{.*?\n\});', html, re.S)
if not m:
    raise SystemExit('FATAL: shell ARTICLE 块未找到')
obj = json.loads(m.group(1))
obj['id'] = ART_ID
obj['file'] = 'articles/%s.html' % ART_ID
obj['title'] = TITLE
obj['title_en'] = 'Tibetan Avataṃsaka · Trilingual (Tibetan / Chinese / English) Working Page with Milestone Plan'
obj['title_sub'] = ('德格甘珠尔 Toh 44 · 45 章品目规划机器派生（差5 / 差6 逐章平行已实证 · 藏独有 2 章 · 前段〔待核〕）· '
                    '一段藏→一段汉→一段英 · MITRA 9B 本地模型译·未校订 · '
                    '后续路线拆为 %d 个里程碑 / 单会话工作量 / %d 项验收门禁' % (
                        len(roadmap['milestones']), sum(len(x['gate']) for x in roadmap['milestones'])))
obj['version'] = 'v0.2 · 里程碑化路线（M0–M9）＋ W1 三语段（藏章1 开篇 %d/%d 段已试译）' % (n_done, n_seg)
obj['icon'] = '🕻'
obj['doc'] = ''
obj['doc_md'] = doc_md
obj['meta'] = ('底本：德格甘珠尔《大方广佛华严经》Toh 44（035-038）\n'
               '切段与翻译工作区：workspace/tibetan-avatamsaka-translation/\n'
               '数据层：' + PLAN + ' · ' + ROADMAP + ' · ' + SEG_GLOB)
pre = html[:m.start()]
pre = pre.replace('<title>藏汉英对读 · 大方广佛华严经（德格藏文本）初探 — 独立文章</title>',
                  '<title>%s — 独立文章</title>' % TITLE, 1)
pre = pre.replace('<h1>藏汉英对读 · 大方广佛华严经（德格藏文本）初探</h1>',
                  '<h1>%s</h1>' % TITLE, 1)
# 「最后更新」时间带：skip_html 页不经 build 注入 → 由本生成器自注册表声明回写
# （verify_demo 不变量②：注册表声明 updated_at 者产物必显；口径与 build 一致）
import yaml as _yaml
_regd = _yaml.safe_load(io.open('data/translation/standalone_articles.yaml', encoding='utf-8')) or {}
_upd = next(str(o['updated_at']) for o in (_regd.get('others') or [])
            if o.get('id') == ART_ID and o.get('updated_at'))
pre = pre.replace('<span class="art-updated"></span>',
                  '<span class="art-updated">📝 最后更新：%s</span>' % _upd, 1)
if _upd not in pre:
    raise SystemExit('FATAL: shell 的 art-updated 空位未命中（口径漂移，勿静默产出不符声明的页面）')
block = 'var ARTICLE = ' + json.dumps(obj, ensure_ascii=False, indent=2) + ';'
io.open(OUT, 'w', encoding='utf-8').write(pre + block + html[m.end():])
print('OK %s | doc_md %d chars | 章 %d 段 %d（已试译 %d）| 规划行 %d | 里程碑 %d · 门禁 %d' % (
    OUT, len(doc_md), n_chap, n_seg, n_done, len(plan['chapters']),
    len(roadmap['milestones']), sum(len(x['gate']) for x in roadmap['milestones'])))
