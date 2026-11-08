# -*- coding: utf-8 -*-
"""三语专题页生成器 v0.3 · 对读工作台（自包含 skip_html 页 · 承 demo 页 shell）。

数据流（全部机械派生，不手填正文）：
  data/alignment/tibetan-derge-toc.json                       45 章骨架
  data/alignment/tibetan_chinese_pin_plan_L360.json            藏章↔汉品 对应 + 进度
  data/translation/tibetan_avatamsaka_trilingual_roadmap.json  里程碑 / 会话单元 / 验收门禁
  data/translation/tibetan_avatamsaka_trilingual_segments*.json 三语段（藏逐字 / MITRA 汉·英）
  → web/demo/articles/tibetan-avatamsaka-trilingual.html

版式（L.377 设计批 · 用户确认 Elevated）：阅读优先——
  ① 45 章章目导航（按对应律分组 · 章签带实测进度 · 已覆盖章可点击直达）；
  ② 三语对读卡片（一段藏→一段汉→一段英 · 默认堆叠，可切三栏并排，选择记忆本机）；
  ③ 工程台账（体例/规划表/里程碑/复现/未竟）默认折叠于附录。
体例不变：汉/英一律 MITRA 模型译、标〔未校订〕；藏文德格原字形逐字回源；未译段如实标〔待译〕。

渲染器硬约束（web/demo/js/common.js，改动前必读）：
  - _mdFullToHTML 块级 passthrough 在**首个闭合标签行**截断 → div 内不得再有 </div>，
    details 不得嵌套；div/section 内文原样透出（须自行 esc），details 内文递归按 markdown 渲染。
  - _mdDocEmbed 目录取源文 ^#{2,4} 行、按序注入 mdh-N → 只用纯 markdown 标题，
    原始 HTML 里不得出现 <h2>-<h4>；附录 details 内不用 ###（改用 bold 行），免目录膨胀。
  - innerHTML 注入的 <script> 不执行、onclick 属性可执行 → 页面 JS 注入 shell </body> 前。
  - _foldDoc 默认全折叠（.is-folded + .secfold-body）→ 注入 JS 展开阅读区、附录保持折叠。

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
plan_by_ch = {r['tibetan_ch']: r for r in plan['chapters']}


def cell(s):
    """markdown 表格单元安全化（ASCII 竖线会破表）。"""
    return str(s).replace('|', '｜')


def esc(s):
    """原始 HTML 上下文（div/section passthrough 内文不经渲染器转义，须自行转义）。"""
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def load_seg_files():
    out = []
    for fn in sorted(glob.glob(SEG_GLOB)):
        d = json.loads(io.open(fn, encoding='utf-8').read())
        out.append((fn, d))
    out.sort(key=lambda x: (x[1].get('chapter') or {}).get('tibetan_no') or 0)
    return out


seg_files = load_seg_files()
seg_by_ch = {(d.get('chapter') or {}).get('tibetan_no'): d for _, d in seg_files}
n_chap = len(seg_files)
n_seg = sum(len(d.get('segments') or []) for _, d in seg_files)
n_done = sum(1 for _, d in seg_files for s in (d.get('segments') or []) if s.get('status') == 'done')
t = plan['totals']
mc = roadmap['measured_constraints']


def pin_label(r):
    if not r:
        return '〔待核〕'
    if r['rule'] == '藏独有':
        return '藏独有 · %s' % (r.get('pin_title_zh') or '〔待核〕')
    if r['pin']:
        return '品%d〈%s〉（%s）' % (r['pin'], r['pin_title_zh'], r['rule'])
    return '〔待核〕前段不平行'


# ── ① 章目导航（45 章全骨架 · 按对应律分组 · 章签进度实测） ──
NAV_GROUPS = [
    ('差5', '藏章 14–31 ＝ 汉品 9–26 · 逐章平行已实证（对勘批 b1–b4＋L.352 覆写）'),
    ('差6', '藏章 33–45 ＝ 汉品 27–39 · 逐章平行已实证（b5/b6·L.357 章末自题定章）'),
    ('藏独有', '藏章 11 / 32 · 无汉文平行品（藏32 归属仍〔待核〕）'),
    ('前段不平行', '藏章 1–10、12–13 ↔ 汉品 1–8 区间 · 章界不平行〔待核〕（L.352 finding）'),
]


def chip(tc):
    r = plan_by_ch.get(tc)
    d = seg_by_ch.get(tc)
    if r['rule'] == '藏独有':
        sub = '独有'
    elif r['pin']:
        sub = '品%d' % r['pin']
    else:
        sub = '待核'
    if d:
        segs = d.get('segments') or []
        don = sum(1 for s in segs if s.get('status') == 'done')
        prog = '%d/%d' % (don, len(segs))
        cls = 'tri-done' if don == len(segs) and segs else ('tri-part' if don else 'tri-todo')
        tip = '%s · %s %s · %s（点击直达对读区）' % (pin_label(r), r['vol'], r['start_folio'], prog)
        return '<a class="tri-chip %s" href="#tri-ch-%d" title="%s"><b>藏%d</b><i>%s · %s</i></a>' % (
            cls, tc, esc(tip), tc, sub, prog)
    prog = r.get('trilingual_status') or '未启动'
    tip = '%s · %s %s · %s' % (pin_label(r), r['vol'], r['start_folio'], prog)
    return '<span class="tri-chip tri-todo" title="%s"><b>藏%d</b><i>%s · 未启动</i></span>' % (
        esc(tip), tc, sub)


nav_parts = ['<div class="tri-nav">']
for rule, desc in NAV_GROUPS:
    chs = [r['tibetan_ch'] for r in plan['chapters'] if r['rule'] == rule]
    nav_parts.append('<p class="tri-nav-group">%s <small>%s</small></p>' % (rule, esc(desc)))
    nav_parts.append('<p class="tri-chips">%s</p>' % ''.join(chip(tc) for tc in sorted(chs)))
nav_parts.append('</div>')
nav_html = '\n'.join(nav_parts)

# ── ② 三语对读卡片（一段藏 → 一段汉 → 一段英） ──
BADGE_ZH = 'MITRA 模型译 · 未校订'
BADGE_EN = 'MITRA model translation · unproofed'


def bo_display(s):
    bo = s.get('bo') or ''
    if s.get('kind') == 'verse' or '།།' in bo:
        # 偈颂分行预留：数据层不动，仅排版按 shad 断行（当前各段皆长行，此枝休眠）
        return '<br>'.join(esc(x) for x in re.split(r'(?<=།)\s*', bo) if x.strip())
    return esc(bo)


def meta_fold(mt, lang):
    if not mt:
        return ''
    if lang == 'zh':
        summary = '译程元数据'
        l1 = '引擎 %s · 生成 %ss · 输出 %s tokens · 复读截断 %s' % (
            mt.get('engine', '?'), mt.get('gen_s', '?'), mt.get('out_tokens', '?'),
            '是' if mt.get('clipped_repeat') else '否')
        l2 = '模型 %s · revisions %s · 校订状态 %s · %s' % (
            mt.get('model', '?'), mt.get('revisions', '?'), mt.get('schooling', '未校订'), mt.get('ts', '?'))
    else:
        summary = 'generation metadata'
        l1 = 'engine %s · %ss · %s tokens · repeat-clipped %s' % (
            mt.get('engine', '?'), mt.get('gen_s', '?'), mt.get('out_tokens', '?'),
            'yes' if mt.get('clipped_repeat') else 'no')
        l2 = 'model %s · revisions %s · schooling %s · %s' % (
            mt.get('model', '?'), mt.get('revisions', '?'), mt.get('schooling', 'unproofed'), mt.get('ts', '?'))
    return '<details class="tri-meta"><summary>%s</summary><p>%s<br>%s</p></details>' % (
        summary, esc(l1), esc(l2))


def lang_section(cls, tag, sub, s, lang):
    val = s.get(lang)
    if val:
        text = bo_display(s) if lang == 'bo' else esc(str(val).replace('\n', ' ').strip())
        body = '<blockquote class="tri-text" lang="%s">%s</blockquote>' % (lang, text)
        meta = '' if lang == 'bo' else meta_fold(s.get(lang + '_meta'), lang)
    else:
        sub = '待译 · 尚未产出' if lang == 'zh' else 'pending · not yet produced'
        note = ('〔待译 · 该段尚未产出（作业进行中／属后续会话）〕' if lang == 'zh'
                else '〔pending · not yet produced〕')
        body = '<blockquote class="tri-text tri-pending">%s</blockquote>' % note
        meta = ''
    head = '<p class="tri-head"><span class="tri-tag">%s</span><span class="tri-sub">%s</span></p>' % (
        tag, esc(sub))
    return '<section class="tri-lang %s">%s%s%s</section>' % (cls, head, body, meta)


blocks = []
for fn, d in seg_files:
    ch = (d.get('chapter') or {})
    tc = ch.get('tibetan_no')
    segs = d.get('segments') or []
    don = sum(1 for s in segs if s.get('status') == 'done')
    blocks.append('<div id="tri-ch-%d" class="tri-anchor"></div>' % tc)
    blocks.append('### 藏章%d（德格 %s · 起叶 %s）· 对应：%s' % (
        tc, ch.get('derge_vol'), ch.get('start_folio'), pin_label(plan_by_ch.get(tc))))
    blocks.append('> **进度：%d/%d 段已试译**（数据层实测）· %s' % (
        don, len(segs), cell(ch.get('chinese_correspondence') or '')))
    for s in segs:
        head = '#### 段 %d〔%s %s · %s〕%s' % (
            s['no'], s['vol'], s['folio'], s['marker'], '（题名块）' if s.get('kind') == 'title' else '')
        card = '<div class="tri-seg" data-status="%s">\n%s\n%s\n%s\n</div>' % (
            s.get('status', 'pending'),
            lang_section('tri-bo', '藏', '德格原字形 · 逐字回源', s, 'bo'),
            lang_section('tri-zh', '汉', BADGE_ZH, s, 'zh'),
            lang_section('tri-en', 'EN', BADGE_EN, s, 'en'))
        blocks.append(head + '\n\n' + card)
seg_blocks = '\n\n'.join(blocks)

toolbar = ('<div class="tri-toolbar"><span class="tri-toolbar-label">三语排列</span>'
           '<button type="button" class="tri-btn is-on" data-lay="stack" onclick="__triLayout(\'stack\')">堆叠 · 一段三语</button>'
           '<button type="button" class="tri-btn" data-lay="cols" onclick="__triLayout(\'cols\')">并排 · 三栏对读</button>'
           '<span class="tri-toolbar-note">并排在窄屏自动回退堆叠 · 选择记忆在本机 · 段标题可点击折叠</span></div>')

# ── ③ 附录（工程台账 · 默认折叠；details 内文递归 markdown，不用 ### 标题免目录膨胀） ──
pin_table = '\n'.join(
    '| %d | %s | %s | %s | %s | %s | %s |' % (
        r['tibetan_ch'], r['vol'], r['start_folio'],
        cell(('品%d〈%s〉' % (r['pin'], r['pin_title_zh'])) if r['pin'] and r['rule'] != '藏独有'
             else (r['pin_title_zh'] or '〔待核〕')),
        cell(r['rule'] or '—'),
        cell(r['tibetan_open_seed'][:30] + ('…' if len(r['tibetan_open_seed']) > 30 else '')),
        cell(r['trilingual_status']))
    for r in plan['chapters'])

ms_rows, ms_detail = [], []
for m in roadmap['milestones']:
    sess = m['sessions']
    mach = sum(1 for g in m['gate'] if g['kind'] != 'manual')
    man = len(m['gate']) - mach
    ms_rows.append('| %s | %s | %s | %s | %d（机器 %d＋人工 %d） |' % (
        m['id'], cell(m['name']), cell(m['batch']),
        cell('；'.join('[%s] %s' % (s['no'], s.get('est', '—')) for s in sess)), mach + man, mach, man))
    det = ['**%s · %s**' % (m['id'], m['name']), '',
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

cf = roadmap.get('conflicts') or plan.get('conflicts') or []
cf_lines = '\n'.join('> - 藏章%d：%s（早期实证 品%s → 现记 品%s）' % (
    c['tibetan_ch'], c['note'], c.get('dropped'), c.get('kept')) for c in cf) \
    or '> - 无（派生过程中无配对冲突）'


def fold(summary, body):
    # details 首行/闭合行必须独占一行（渲染器 inner=raw.slice(1,-1)）；不得嵌套 details
    return '<details class="tri-appx">\n<summary>%s</summary>\n\n%s\n\n</details>' % (summary, body)


appx_style = fold('📐 体例与硬约束', """| 项 | 口径 |
|---|---|
| 段制 | 一段藏文 → 一段汉语 → 一段英文；段为最小对齐单位 |
| 藏文来源 | 自德格底本 `{T44-N}…{T44-N+1}` 区间**字节切片**，逐段 norm() 复验可追回原文；**绝不手打藏文** |
| 切段规则 | %s |
| 汉 / 英 | MITRA 9B（bf16 · CPU · greedy）模型译，**未校订**；长输出复读已作 n-gram 禁用 + 周期截断 |
| 品目对应 | 只用已机器实证的对应；未实证一律〔待核〕，不代立论 |
| 完成判定 | 里程碑门禁为被观察到的证据；未全绿不得称完成 |
| 版式 | v0.3（L.377 设计批）：阅读优先——章目导航＋三语卡片在前，工程台账折叠于附录；默认堆叠、可切并排；偈颂分行与术语悬停为预留位（数据层未动） |

> 〔诚实边界〕汉 / 英译文一律视为**〔模型译·未校订〕**，只作工作草稿；**不**等同于本仓既有的 CBETA 祖本引文（祖本引文另按 T10n0279 繁体逐字回源，见〈藏汉英对读 · 初探〉页）。""" % roadmap['scope_note'])

appx_plan = fold('🗂 结构事实与 45 章品目规划表', """藏文 **%d 章** ／ 八十汉译 **39 品** ／ 六十汉译 **34 品**。
对应统计：**已实证逐章平行 %d 对** · **藏独有 %d 章** · **前段章界不平行 %d 章（〔待核〕）**。

对应律（机器实证所得，非臆测）：

- **藏章 14–31 ＝ 汉品 9–26**（序号差 5，逐章平行）— 证据：对勘批 b1–b4 ＋ L.352 重勘覆写
- **藏章 33–38 ＝ 汉品 27–32**、**藏章 39–45 ＝ 汉品 33–39**（序号差 6）— 证据：b5 / b6（L.357 章末自题定章收官）
- **藏章 11〈如来华严〉· 藏章 32〈普贤宣说〉＝ 藏独有**（无汉文平行品；藏32 归属仍〔待核〕）
- **藏章 1–10、12–13 ↔ 汉品 1–8 区间：章界不平行**〔待核〕（L.352 finding：不平行限于前段）

配对冲突记录（派生过程中如实保留，不静默取舍）：

%s

**章节品目规划表（德格 45 章全量）**

| 藏章 | 卷 | 起始叶码 | 对应汉品（八十） | 对应律 | 藏文开篇（德格原字形·节选） | 三语进度 |
|---|---|---|---|---|---|---|
%s

> 〔口径〕「对应汉品」= 对勘批机械收集＋L.352 覆写所得；对应律「—」= 前段未定界〔待核〕；「三语进度」= 数据层实测计数。全量种子见 `%s`，派生表见 `%s`。""" % (
    t['tibetan_chapters'], t['verified_pairs'], t['tibetan_only'], t['front_unparallel'],
    cf_lines, pin_table, TOC, PLAN))

appx_roadmap = fold('🛤 里程碑路线与验收门禁', """拆解决策口径：

1. **一会话＝一编排单元**：单元尺寸由实测吞吐反推——%s；「一章开篇 6 段」为最小**工作**单元（会话内完成切段/启动/落盘确认，翻译机时后台续跑跨会话）。
2. **证据分层**：先译已实证平行段（差5 → 差6），前段（章界未定）刻意置后，避免产出无法对齐的孤立译文。
3. **门禁两类**：`机器判定` 由 `tools/check_trilingual_gates.py` 实测（能判则判，前提数据缺失判 PENDING，**不冒充 PASS**）；`人工闸门` 须在 `tasks/PROGRESS.md` 留证据行方得通过。
4. **成本上限可见**：%s token/s、%ss 冷加载（热加载 %ss）——规模判断一律以实测为准，不估算冒充实测。

| 里程碑 | 名称 | 批次 | 会话单元（预估） | 验收门禁 |
|---|---|---|---|---|
%s

> 顺序：%s。排产说明：
%s
%s

**逐里程碑细目**

%s""" % (mc['session_unit_cost_estimate'], mc['gen_throughput_tok_per_s'], mc['cold_load_s'],
         mc['warm_load_s'], milestone_table, ' → '.join(roadmap.get('ordering', [])),
         sched_notes, granularity_note, milestone_detail))

appx_repro = fold('🔁 复现与续跑', """```text
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

运行环境（实测口径）：`hy_py312` · torch CPU-only（%s）· **必须** bf16 加载（%s）·
生成 %s token/s（≈%s s/token）· %s。""" % (mc['hardware'], mc['must_bf16'],
                                       mc['gen_throughput_tok_per_s'], mc['gen_seconds_per_token'],
                                       mc['repeat_risk']))

appx_todo = fold('⏳ 未竟与待核', """- 〔未竟·M0〕藏章1 开篇其余段（单章正文实测 188,713 字符／约 3,914 句读）；本批只取 6 段。
- 〔未竟·M1〕吞吐标定表与算力决策（含人工闸门）。
- 〔未竟·M2/M3/M4〕差5、差6 两跨段与入法界品的逐章开篇三语。
- 〔未竟·M5〕人工校订：模型译升格为可引用译文（须双轨保留原译）。
- 〔未竟·M6〕三语术语库；〔未竟·M7〕藏独有二章；〔未竟·M8〕前段章界比对。
- 〔待核〕偈颂分行对齐（藏文 `།།` 七言颂与汉译偈组对应；页面已留分行排版枝，数据层当前无偈颂段）。
- 〔待核·M5〕藏章14 段1：汉译中段、英译末尾混入藏文残字（疑解码/复读残留）；数据层原样保留，校订线双轨处理，本批不改。
- 〔待核·M5〕藏章15 段1：汉译起首误系《佛說大毘盧遮那成佛神變加持經》经题（他经），疑模型错译；该段 status=pending（英译未产出），归 M5 校订线。
- 〔未竟·设计〕术语悬停释义（`.tri-term[data-gloss]` 样式已预留，术语库待 M6 产出后接线）。""")

doc_md = """# %s

> **本页任务**：把德格甘珠尔《大方广佛华严经》（Toh 44，藏文 45 章 / 115 bam po）**逐段译为三语并列**——
> 一段藏文（德格原字形，逐字回源）→ 一段汉语 → 一段英文（后二者由本地模型 `buddhist-nlp/mitra-qwen35-translate` 9B 试译）。
> 汉 / 英译文一律**〔模型译·未校订〕**，只作工作草稿，不作引文、不替代 CBETA 祖本文字。
> **版式 v0.3**：阅读优先——章目导航与三语对读在前；工程台账（体例 / 规划表 / 里程碑 / 复现 / 未竟）默认折叠于附录。

## 一、章目导航（45 章全骨架）

%s

> 〔口径〕分组依机器实证对应律；章签数字＝已试译段/切段总数（数据层实测）。亮色章签可点击直达对读区，灰色＝未启动。全量规划表见附录「结构事实与 45 章品目规划表」。

## 二、三语对读（%d 章 · %d 段 · 已试译 %d 段）

%s

%s

> 〔诚实边界〕以上仅覆盖各章**开篇**，非全品；未译段如实标〔待译〕。模型译未经人工校订，不作引文使用，不得替代 CBETA 祖本文字。〔质量待核〕藏章14/15 个别段译文有藏文残留/疑似错译，已如实保留，详见附录「未竟与待核」。

<div id="tri-appendix" class="tri-anchor"></div>

## 附录 · 工程台账与路线

%s

%s

%s

%s

%s
""" % (TITLE, nav_html, n_chap, n_seg, n_done, toolbar, seg_blocks,
       appx_style, appx_plan, appx_roadmap, appx_repro, appx_todo)

# 附录 h2 的 mdh 序号（_mdDocEmbed 按源文 ^#{2,4} 顺序编号）→ 注入 JS 精确识别附录子树
ap_pos = doc_md.index('\n## 附录')
AP_MDH = 'mdh-%d' % (len(re.findall(r'(?m)^#{2,4}\s', doc_md[:ap_pos])) + 1)

CSS = """/* ── 三语对读工作台（L.377 · gen v0.3） ── */
.tri-anchor{scroll-margin-top:96px}
.tri-nav{margin:10px 0}
.tri-nav-group{font-size:.8em;font-weight:700;color:var(--gold);margin:12px 0 6px}
.tri-nav-group small{font-weight:400;color:var(--text2)}
.tri-chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 4px}
.tri-chip{display:inline-flex;flex-direction:column;align-items:center;min-width:64px;padding:4px 8px;border:1px solid var(--line);border-radius:8px;font-size:.72em;line-height:1.5;text-decoration:none;color:var(--text2);background:rgba(94,139,158,.04)}
.tri-chip b{font-size:1.05em;color:var(--text)}
.tri-chip i{font-style:normal;font-size:.9em;opacity:.8}
a.tri-chip:hover{border-color:var(--gold);color:var(--gold)}
.tri-chip.tri-done{border-color:var(--blue);background:rgba(94,139,158,.10)}
.tri-chip.tri-part{border-color:var(--gold);background:rgba(184,134,60,.08)}
.tri-chip.tri-todo{opacity:.55}
.tri-toolbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:10px 0;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:rgba(94,139,158,.05);font-size:.78em}
.tri-toolbar-label{font-weight:700;color:var(--gold)}
.tri-btn{border:1px solid var(--line);background:transparent;color:var(--text2);border-radius:6px;padding:3px 12px;font-size:1em;cursor:pointer}
.tri-btn.is-on{border-color:var(--gold);color:var(--gold);background:rgba(184,134,60,.10);font-weight:700}
.tri-toolbar-note{opacity:.65;font-size:.92em}
.tri-seg{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:8px 0 14px;background:rgba(94,139,158,.03)}
.tri-seg[data-status="pending"]{border-style:dashed}
.tri-lang{margin:8px 0;padding-left:10px;border-left:3px solid var(--line)}
.tri-lang.tri-bo{border-left-color:var(--gold)}
.tri-lang.tri-zh{border-left-color:var(--blue)}
.tri-lang.tri-en{border-left-color:#9a7fb8}
.tri-head{margin:0 0 4px;font-size:.72em;color:var(--text2)}
.tri-tag{display:inline-block;font-weight:700;border:1px solid currentColor;border-radius:4px;padding:0 6px;margin-right:8px}
.tri-bo .tri-tag{color:var(--gold)}
.tri-zh .tri-tag{color:var(--blue)}
.tri-en .tri-tag{color:#9a7fb8}
.tri-text{margin:0;padding:6px 10px;border:none;background:transparent;font-size:.85em;line-height:1.9;white-space:pre-line;overflow-wrap:break-word}
.tri-text[lang="bo"]{font-family:'Noto Serif Tibetan','Noto Sans Tibetan','Microsoft Himalaya','Kailasa','Tibetan Machine Uni',serif;line-height:2.3;font-size:.95em}
.tri-text[lang="en"]{font-family:Georgia,'Times New Roman',serif}
.tri-pending{opacity:.55;font-style:italic}
.tri-meta{margin:4px 0 0;font-size:.7em;color:var(--text2)}
.tri-meta summary{cursor:pointer;opacity:.7}
.tri-meta p{margin:4px 0;padding:4px 10px;background:rgba(94,139,158,.06);border-radius:6px;line-height:1.7}
.tri-cols .tri-seg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;align-items:start}
.tri-cols .tri-lang{margin-top:0}
@media (max-width:960px){.tri-cols .tri-seg{grid-template-columns:1fr}}
.tri-appx{margin:8px 0}
.tri-term[data-gloss]{border-bottom:1px dotted var(--gold);cursor:help;position:relative}
.tri-term[data-gloss]:hover::after{content:attr(data-gloss);position:absolute;left:0;top:100%;z-index:50;background:rgba(31,36,42,.96);color:#fff;padding:4px 10px;border-radius:6px;font-size:.85em;white-space:nowrap}
"""

JS = """/* ── 三语对读工作台（L.377 · gen v0.3） ── */
window.__triLayout = function (mode) {
  var root = document.getElementById('article-full');
  if (!root) return;
  var cols = (mode === 'cols');
  root.classList.toggle('tri-cols', cols);
  try { localStorage.setItem('triLayout', cols ? 'cols' : 'stack'); } catch (e) {}
  var btns = document.querySelectorAll('.tri-btn[data-lay]');
  for (var i = 0; i < btns.length; i++) {
    btns[i].classList.toggle('is-on', btns[i].getAttribute('data-lay') === (cols ? 'cols' : 'stack'));
  }
};
(function () {
  var AP = '__AP_MDH__';
  function init() {
    var root = document.getElementById('article-full');
    if (!root || !root.querySelector('.secfold')) return false;
    var ap = document.getElementById(AP);
    if (!ap) return false;
    var apBody = ap.nextElementSibling;
    var hs = root.querySelectorAll('.secfold');
    for (var i = 0; i < hs.length; i++) {
      var h = hs[i];
      if (h === ap || (apBody && apBody.contains(h))) continue;
      h.classList.remove('is-folded');
      h.setAttribute('aria-expanded', 'true');
    }
    // 窄屏页头换行可高达 200px+，固定 scroll-margin 会把锚点藏进页头 → 按实高同步
    function syncGap() {
      var top = document.getElementById('page-top');
      var gap = (top ? top.offsetHeight : 0) + 12;
      var as = document.querySelectorAll('.tri-anchor');
      for (var i = 0; i < as.length; i++) as[i].style.scrollMarginTop = gap + 'px';
    }
    syncGap();
    window.addEventListener('resize', syncGap);
    var lay = 'stack';
    try { lay = localStorage.getItem('triLayout') || 'stack'; } catch (e) {}
    window.__triLayout(lay);
    root.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a.tri-chip[href^="#"]') : null;
      if (!a) return;
      var el = document.getElementById(a.getAttribute('href').slice(1));
      if (!el) return;
      e.preventDefault();
      if (window._reveal) window._reveal(el);
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (history.replaceState) history.replaceState(null, '', a.getAttribute('href'));
    });
    return true;
  }
  function poll(n) { if (init()) return; if (n > 0) setTimeout(function () { poll(n - 1); }, 120); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { poll(20); });
  else poll(20);
})();
""".replace('__AP_MDH__', AP_MDH)

# ── 注入自包含页（shell 承 demo 页；页头两处硬编码标题随之替换） ──
html = io.open(SHELL, encoding='utf-8').read()
m = re.search(r'var ARTICLE = (\{.*?\n\});', html, re.S)
if not m:
    raise SystemExit('FATAL: shell ARTICLE 块未找到')
obj = json.loads(m.group(1))
obj['id'] = ART_ID
obj['file'] = 'articles/%s.html' % ART_ID
obj['title'] = TITLE
obj['title_en'] = 'Tibetan Avataṃsaka · Trilingual Reading Workbench (Tibetan / Chinese / English)'
obj['title_sub'] = ('德格甘珠尔 Toh 44 · 45 章导航（差5/差6 逐章平行已实证 · 藏独有 2 章 · 前段〔待核〕）· '
                    '一段藏→一段汉→一段英 · MITRA 9B 本地模型译·未校订 · '
                    '里程碑 %d 个 / 验收门禁 %d 项（附录折叠）' % (
                        len(roadmap['milestones']), sum(len(x['gate']) for x in roadmap['milestones'])))
obj['version'] = ('v0.3 · 对读工作台（L.377 设计批：45 章导航＋三语卡片＋堆叠/并排切换＋工程附录折叠）'
                  '· 已试译 %d/%d 段' % (n_done, n_seg))
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
page = pre + block + html[m.end():]
if page.count('</head>') != 1 or page.count('</body>') != 1:
    raise SystemExit('FATAL: shell 注入点不唯一（</head>=%d </body>=%d）' % (
        page.count('</head>'), page.count('</body>')))
page = page.replace('</head>', '<style>\n' + CSS + '</style>\n</head>', 1)
page = page.replace('</body>', '<script>\n' + JS + '</script>\n</body>', 1)
io.open(OUT, 'w', encoding='utf-8').write(page)
print('OK %s | doc_md %d chars | 章 %d 段 %d（已试译 %d）| 导航章签 %d | 附录 fold 5 | AP=%s | CSS/JS 已注入' % (
    OUT, len(doc_md), n_chap, n_seg, n_done, len(plan['chapters']), AP_MDH))