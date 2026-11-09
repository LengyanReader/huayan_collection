# -*- coding: utf-8 -*-
"""三语专题页生成器 v0.4 · 子页架构（自包含 skip_html 页 · 承 demo 页 shell）。

数据流（全部机械派生，不手填正文）：
  data/alignment/tibetan-derge-toc.json                       45 章骨架
  data/alignment/tibetan_chinese_pin_plan_L360.json            藏章↔汉品 对应 + 进度
  data/translation/tibetan_avatamsaka_trilingual_roadmap.json  里程碑 / 会话单元 / 验收门禁
  data/translation/tibetan_avatamsaka_trilingual_segments*.json 三语段（藏逐字 / MITRA 汉·英）
  data/alignment/tibetan_zhuhuju_b[1-6].json                   对勘批（correspondence / shidu / zh80_open）
  data/alignment/avatamsaka-openings-demo.json                 藏章1 示范对勘示例层
  data/alignment/tibetan_chinese_tongyi_L354.json              同异总表（总纲 §五数据层）
  data/alignment/tibetan_shiyi_L354a.json                      开篇试译术语表
  data/alignment/tibetan_trilingual_opening_reconcile.json     开篇种子〔订正〕登记
  data/alignment/tibetan_ch_map_L352.json                      对应律 finding
  docs/经学文献/华严经学_三十九品深度研究.md                     藏独有二章法义归属（§2.3 迻录）
  → web/demo/articles/tibetan-avatamsaka-trilingual.html        总目枢纽（注册 · 四 tab）
  → web/demo/articles/tibetan-avatamsaka-trilingual-chNN.html   章子页（不注册 · 三 tab · 随翻译逐章生长）

版式（L.378 子页架构批）：内容庞大 → 总目枢纽＋章子页两级——
  hub 四 tab：总览 / 章目导航（45 章全骨架）/ 对应研究（库存文献联通）/ 工程台账（附录折叠）；
  章子页三 tab：三语对读 / 汉藏对应 / 延伸阅读；面包屑＋章间 pager＋段导航。
体例不变：汉/英一律 MITRA 模型译、标〔未校订〕；藏文德格原字形逐字回源；未译段如实标〔待译〕。

渲染器硬约束（web/demo/js/common.js，改动前必读）：
  - _mdFullToHTML 块级 passthrough 在**首个闭合标签行**截断 → div 内不得再有 </div>，
    details 不得嵌套；div/section 内文原样透出（须自行 esc），details 内文递归按 markdown 渲染。
  - _mdDocEmbed 目录取源文 ^#{2,4} 行、按序注入 mdh-N → 只用纯 markdown 标题，
    原始 HTML 里不得出现 <h2>-<h4>；附录 details 内不用 ###（改用 bold 行），免目录膨胀。
  - innerHTML 注入的 <script> 不执行、onclick 属性可执行 → 页面 JS 注入 shell </body> 前。
  - _foldDoc 把 h2 及其后内容包为 .secfold + .secfold-body（next sibling）→ 子 tab 即以 h2 为 pane，
    注入 JS 展开全部 secfold 后按 tab 显隐；hash 深链激活所在 pane。

verify_demo 不变量：章子页**不注册**于 standalone_articles.yaml → art-updated 时间带必须保持空；
  hub 注册且声明 updated_at → 由本生成器自注册表回写（口径与 build 一致）。

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
ALIGN_GLOB = 'data/alignment/tibetan_zhuhuju_b[1-6].json'
EXEMPLAR = 'data/alignment/avatamsaka-openings-demo.json'
TONGYI = 'data/alignment/tibetan_chinese_tongyi_L354.json'
SHIYI = 'data/alignment/tibetan_shiyi_L354a.json'
RECONCILE = 'data/alignment/tibetan_trilingual_opening_reconcile.json'
CHMAP = 'data/alignment/tibetan_ch_map_L352.json'
DEEP = 'docs/经学文献/华严经学_三十九品深度研究.md'
ART_ID = 'tibetan-avatamsaka-trilingual'
TITLE = '藏译华严 · 藏汉英三语对读（德格甘珠尔 Toh 44）'
TITLE_EN = 'Tibetan Avataṃsaka · Trilingual Reading Workbench (Tibetan / Chinese / English)'

plan = json.loads(io.open(PLAN, encoding='utf-8').read())
roadmap = json.loads(io.open(ROADMAP, encoding='utf-8').read())
toc = json.loads(io.open(TOC, encoding='utf-8').read())
plan_by_ch = {r['tibetan_ch']: r for r in plan['chapters']}
exemplar = (json.loads(io.open(EXEMPLAR, encoding='utf-8').read()) or {}).get('exemplar') or {}
tongyi = json.loads(io.open(TONGYI, encoding='utf-8').read())
shiyi = json.loads(io.open(SHIYI, encoding='utf-8').read())
chmap = json.loads(io.open(CHMAP, encoding='utf-8').read())
rec_by_ch = {r['tibetan_ch']: r for r in
             (json.loads(io.open(RECONCILE, encoding='utf-8').read()).get('records') or [])}
align_by_ch = {}
for _fn in sorted(glob.glob(ALIGN_GLOB)):
    _d = json.loads(io.open(_fn, encoding='utf-8').read())
    _chs = _d.get('chapters') or []
    for _c in (_chs.values() if isinstance(_chs, dict) else _chs):
        if isinstance(_c, dict) and _c.get('tibetan_ch'):
            align_by_ch.setdefault(_c['tibetan_ch'], (_fn, _c))


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
seg_fn_by_ch = {(d.get('chapter') or {}).get('tibetan_no'): fn for fn, d in seg_files}
covered = sorted(seg_by_ch)
n_chap = len(seg_files)
n_seg = sum(len(d.get('segments') or []) for _, d in seg_files)
n_done = sum(1 for _, d in seg_files for s in (d.get('segments') or []) if s.get('status') == 'done')
t = plan['totals']
mc = roadmap['measured_constraints']


def ch_url(tc):
    return '%s-ch%02d.html' % (ART_ID, tc)


def pin_label(r):
    if not r:
        return '〔待核〕'
    if r['rule'] == '藏独有':
        return '藏独有 · %s' % (r.get('pin_title_zh') or '〔待核〕')
    if r['pin']:
        return '品%d〈%s〉（%s）' % (r['pin'], r['pin_title_zh'], r['rule'])
    return '〔待核〕前段不平行'


# ── hub · 章目导航（45 章全骨架 · 按对应律分组 · 章签进度实测 · 已覆盖章链接章子页） ──
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
        tip = '%s · %s %s · %s（点击进入章子页）' % (pin_label(r), r['vol'], r['start_folio'], prog)
        return '<a class="tri-chip %s" href="%s" title="%s"><b>藏%d</b><i>%s · %s</i></a>' % (
            cls, ch_url(tc), esc(tip), tc, sub, prog)
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

# ── 章子页 · 三语对读卡片（一段藏 → 一段汉 → 一段英） ──
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


def seg_blocks_for(d):
    """一章的段导航＋三语卡片（#### 段 n 标题口径不变，门禁正则所系）。"""
    segs = d.get('segments') or []
    out = ['<div class="tri-segnav"><span class="tri-toolbar-label">段导航</span>%s</div>' % ''.join(
        '<a class="tri-segchip" href="#tri-seg-%d">段 %d</a>' % (s['no'], s['no']) for s in segs)]
    for s in segs:
        out.append('<div id="tri-seg-%d" class="tri-anchor"></div>' % s['no'])
        head = '#### 段 %d〔%s %s · %s〕%s' % (
            s['no'], s['vol'], s['folio'], s['marker'], '（题名块）' if s.get('kind') == 'title' else '')
        card = '<div class="tri-seg" data-status="%s">\n%s\n%s\n%s\n</div>' % (
            s.get('status', 'pending'),
            lang_section('tri-bo', '藏', '德格原字形 · 逐字回源', s, 'bo'),
            lang_section('tri-zh', '汉', BADGE_ZH, s, 'zh'),
            lang_section('tri-en', 'EN', BADGE_EN, s, 'en'))
        out.append(head + '\n\n' + card)
    return '\n\n'.join(out)


toolbar = ('<div class="tri-toolbar"><span class="tri-toolbar-label">三语排列</span>'
           '<button type="button" class="tri-btn is-on" data-lay="stack" onclick="__triLayout(\'stack\')">堆叠 · 一段三语</button>'
           '<button type="button" class="tri-btn" data-lay="cols" onclick="__triLayout(\'cols\')">并排 · 三栏对读</button>'
           '<span class="tri-toolbar-note">并排在窄屏自动回退堆叠 · 选择记忆在本机 · 段标题可点击折叠</span></div>')

# ── hub · 工程台账 tab（附录 · 默认折叠；details 内文递归 markdown，不用 ### 标题免目录膨胀） ──
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


# ── 章子页 · 汉藏对应 tab（库存对勘素材机械接入；bo_open 错切字段不展示） ──


def quote_section(cls, tag, sub, text, lang):
    """CBETA / 对勘引文块（非 MITRA badge 区；多行 section passthrough，闭合标签独占一行）。"""
    return ('<section class="tri-quote %s">\n'
            '<p class="tri-head"><span class="tri-tag">%s</span><span class="tri-sub">%s</span></p>\n'
            '<blockquote class="tri-text" lang="%s">%s</blockquote>\n'
            '</section>') % (cls, tag, esc(sub), lang, esc(text))


def corr_table(rows):
    out = ['| 目 | 八十（T10n0279） | 六十（T09n0278） | 藏（德格 Toh 44） |', '|---|---|---|---|']
    for r in rows:
        out.append('| %s | %s | %s | %s |' % tuple(cell(x) for x in r))
    return '\n'.join(out)


def corr_pane(tc):
    d = seg_by_ch.get(tc) or {}
    segs = d.get('segments') or []
    parts = []
    if tc == 1 and exemplar:
        ex = exemplar
        parts += ['**三本开篇对照**（L.203 示范对勘 · 库存示例层）', '',
                  quote_section('tri-qbo', '藏', '德格 Toh 44-1 · 叶码 %s（示例层自记）' % ex.get('folio', '?'),
                                ex.get('tibetan', ''), 'bo'),
                  quote_section('tri-qzh', '八十', ex.get('chinese_80_source', ''), ex.get('chinese_80', ''), 'zh'),
                  quote_section('tri-qzh', '六十', ex.get('chinese_60_source', ''), ex.get('chinese_60', ''), 'zh'),
                  '', '**对勘发现**（示例层 collation_findings 原文迻录）', '']
        parts += ['- ' + f for f in (ex.get('collation_findings') or [])]
        parts += ['', '> 〔口径〕本示例出自《藏汉英对读 · 初探》页之旧示例层（英文 IITB 词典辅助、汉译 MITRA 旧译程），'
                  '与本专题 MITRA 9B 译程**非同一引擎批次**；藏文与两汉译祖本引文逐字回源口径不变。']
        return '\n'.join(parts)
    ac = align_by_ch.get(tc)
    if not ac:
        return ('〔未竟〕本章汉藏对应素材待对勘批覆盖后机械接入（当前库存：b1–b6 逐段对读批）；'
                '不臆造对应条目。对应律口径见总目「对应研究」tab。')
    fn, c = ac
    parts += ['**开篇对照**（本专题 seg1 × 对勘批开篇）', '']
    if segs:
        s1 = segs[0]
        parts.append(quote_section('tri-qbo', '藏', '本专题 seg1 · 德格 %s %s（逐字回源复验）' % (
            s1.get('vol'), s1.get('folio')), s1.get('bo', ''), 'bo'))
    if c.get('zh80_open'):
        parts.append(quote_section('tri-qzh', '八十', '对勘批 %s · %s 开篇（T10n0279 逐字回源）' % (
            fn.split('/')[-1], c.get('pin', '?')), c['zh80_open'], 'zh'))
    else:
        parts.append('> 〔口径〕本批对勘条目无 `zh80_open` 字段 → 只列对应表与识读，不臆造开篇引文。')
    if c.get('correspondence'):
        parts += ['', '**名相对应表**（对勘批 correspondence 原文迻录）', '', corr_table(c['correspondence'])]
    if c.get('shidu'):
        parts += ['', '> ' + c['shidu']]
    rec = rec_by_ch.get(tc)
    if rec:
        body = ['**判定**：%s' % rec.get('verdict', ''), '',
                '**观察**：%s' % rec.get('observation', ''), '', '**证据**（≥2 条独立佐证）：', '']
        body += ['- ' + e for e in (rec.get('evidence') or [])]
        body += ['', '**后续**：%s' % rec.get('followup', ''), '',
                 '**机器检查**：`%s`' % rec.get('machine_check', '')]
        parts += ['', fold('🧭 开篇种子〔订正〕登记（L.361 · 证据留痕）', '\n'.join(body))]
        parts += ['', '> 〔口径〕对勘批 `bo_open` 字段经 L.361 订正登记判为旧偏移错切，本页**不展示**该字段；'
                  '藏文开篇一律以本专题逐字复验 seg1 为准。订正不改对勘批 SSOT（各照底本·铁律）。']
    return '\n'.join(parts)


# ── 章子页 · 延伸阅读 tab（专篇互链＋试译迻录＋数据源清单） ──
READ_MORE = {
    1: ('shizhu-miaoyan.html', '九九华严第一品〈世主妙严品〉拼读专篇',
        '第一会·菩提场：本专题藏章1 开篇所对应的汉译本品'),
    14: ('huayan-guangmingjue-pin.html', '九九华严第九品〈光明觉品〉拼读专篇',
         '第二会·普光明殿：藏章14 对应汉品9（差5）'),
    15: ('huayan-wenming-pin.html', '九九华严第十品〈菩萨问明品〉拼读专篇',
         '第二会·普光明殿：藏章15 对应汉品10（差5）'),
}


def links_pane(tc):
    parts = ['**本仓专篇与总纲**', '']
    rm = READ_MORE.get(tc)
    if rm:
        parts.append('- [%s](%s) — %s' % (rm[1], rm[0], rm[2]))
    parts.append('- [华严经引读 · 系列总纲（§五 藏汉对应总表）](huayan-series-outline.html)')
    parts.append('- [华严经学 · 三十九品深度研究](huayan-studies.html) — 藏独有二章之法义归属见 §2.3')
    if tc in (14, 15):
        parts.append('- [九九华严第七品〈如来名号品〉拼读专篇](rulai-minghao.html) — 名号异文同型参看')
    sy = (shiyi.get('chapters') or {}).get(str(tc))
    if sy:
        parts += ['', '**开篇试译**（L.354a 术语表 · 〔本文试译〕）', '', '> ' + sy]
    parts += ['', '**数据源清单**（本页内容全部机械派生自下列库存）', '']
    parts.append('- 三语段数据层：`%s`' % seg_fn_by_ch.get(tc, SEG_GLOB))
    if tc in align_by_ch:
        parts.append('- 对勘批：`%s`' % align_by_ch[tc][0])
    if tc in rec_by_ch:
        parts.append('- 开篇订正登记：`%s`' % RECONCILE)
    if sy:
        parts.append('- 试译术语表：`%s`' % SHIYI)
    if tc == 1:
        parts.append('- 示范对勘示例层：`%s`' % EXEMPLAR)
    parts.append('- 品目规划表：`%s`' % PLAN)
    return '\n'.join(parts)


# ── hub · 对应研究 tab（对应律＋同异总表＋深度研究迻录＋库存文献联通地图） ──
deep_md = io.open(DEEP, encoding='utf-8').read()
deep_bullets = []
for _name in ('如来华严品', '普贤宣说品'):
    _m = re.search(r'(?m)^- \*\*《%s》\*\*.*$' % _name, deep_md)
    if not _m:
        raise SystemExit('FATAL: 深度研究缺《%s》条目（口径漂移，勿静默产出）' % _name)
    deep_bullets.append(_m.group(0))

LIT_MAP = [
    ('系列总纲 §五', '藏汉对应总表（同异总表之 hub）', '[系列总纲](huayan-series-outline.html)'),
    ('三十九品深度研究', '品目·批注·版本对照；藏独有二章法义归属（§2.3）', '[深度研究](huayan-studies.html)'),
    ('世主妙严品拼读专篇', '汉品1（藏章1 开篇对应）', '[世主妙严品](shizhu-miaoyan.html)'),
    ('光明觉品拼读专篇', '汉品9（藏章14 · 差5）', '[光明觉品](huayan-guangmingjue-pin.html)'),
    ('菩萨问明品拼读专篇', '汉品10（藏章15 · 差5）', '[菩萨问明品](huayan-wenming-pin.html)'),
    ('如来名号品拼读专篇', '汉品7 · 名号异文同型参看', '[如来名号品](rulai-minghao.html)'),
    ('八十/六十品次-体量矩阵', '两汉译品次体量对照', '[品次-体量矩阵](huayan-80-60-matrix.html)'),
    ('对勘批 b1–b6', '逐段对读数据层（correspondence / shidu）', '`data/alignment/tibetan_zhuhuju_b[1-6].json`'),
    ('同异总表 L.354 / 试译 L.354a', '同异条目 · 开篇试译术语表', '`tibetan_chinese_tongyi_L354.json` · `tibetan_shiyi_L354a.json`'),
    ('开篇订正登记 L.361', 'bo_open 错切之〔订正〕留痕', '`tibetan_trilingual_opening_reconcile.json`'),
]

corr_parts = ['**对应律总览**（机器实证 · 非臆测）', '',
              '- **藏章 14–31 ＝ 汉品 9–26**（序号差 5，逐章平行）— 证据：对勘批 b1–b4 ＋ L.352 重勘覆写',
              '- **藏章 33–38 ＝ 汉品 27–32**、**藏章 39–45 ＝ 汉品 33–39**（序号差 6）— 证据：b5 / b6（L.357 章末自题定章收官）',
              '- **藏章 11〈如来华严〉· 藏章 32〈普贤宣说〉＝ 藏独有**（无汉文平行品；藏32 归属仍〔待核〕）',
              '- **藏章 1–10、12–13 ↔ 汉品 1–8 区间：章界不平行**〔待核〕（L.352 finding）',
              '', '> ' + chmap['finding'], '',
              '**同异总表**（L.354b · 系列总纲 §五之数据层，原文迻录）', '',
              '*同（%d 条）*：' % len(tongyi['same']), '']
corr_parts += ['- ' + s for s in tongyi['same']]
corr_parts += ['', '*异（%d 条）*：' % len(tongyi['diff']), '']
corr_parts += ['- ' + s for s in tongyi['diff']]
corr_parts += ['', '**藏独有二章 · 法义归属**（《华严经学·三十九品深度研究》§2.3 原文迻录）', '']
corr_parts += deep_bullets
corr_parts += ['', '**库存文献联通地图**（本页与各章子页之素材皆出于此）', '',
               '| 文献 / 数据 | 内容 | 入口 |', '|---|---|---|']
corr_parts += ['| %s | %s | %s |' % tuple(cell(x) for x in row) for row in LIT_MAP]
corr_hub = '\n'.join(corr_parts)

# ── hub · 总览 tab（实测统计＋当前批次＋已建章子页卡片） ──
stats_html = ('<div class="tri-stats">'
              '<span class="tri-stat"><b>%d</b>藏章全骨架</span>'
              '<span class="tri-stat"><b>%d</b>章子页已建</span>'
              '<span class="tri-stat"><b>%d</b>切段总数</span>'
              '<span class="tri-stat"><b>%d</b>段已试译</span>'
              '</div>') % (t['tibetan_chapters'], n_chap, n_seg, n_done)
m2_parts = []
for _tc in (14, 15):
    _dd = seg_by_ch.get(_tc)
    if _dd:
        _ss = _dd.get('segments') or []
        m2_parts.append('藏%d %d/%d' % (_tc, sum(1 for s in _ss if s.get('status') == 'done'), len(_ss)))
    else:
        m2_parts.append('藏%d 未启动' % _tc)
m2_line = ' · '.join(m2_parts)
chcards = []
for tc in covered:
    r = plan_by_ch.get(tc) or {}
    ss = seg_by_ch[tc].get('segments') or []
    don = sum(1 for s in ss if s.get('status') == 'done')
    pct = int(round(100.0 * don / len(ss))) if ss else 0
    chcards.append(
        '<div class="tri-chcard">\n'
        '<p class="tri-chcard-main"><b>藏章%d</b><span class="tri-chcard-pin">%s</span></p>\n'
        '<p class="tri-chcard-prog"><span class="tri-prog"><i style="width:%d%%"></i></span><span>%d/%d 段已试译</span></p>\n'
        '<p class="tri-chcard-go"><a href="%s">进入对读 →</a></p>\n'
        '</div>' % (tc, esc(pin_label(r)), pct, don, len(ss), ch_url(tc)))
overview = '\n\n'.join([
    stats_html,
    '**当前批次**：M2 差5 跨段开篇（%s）；藏章1 开篇 6 段已全译（M0 收官）。章子页随翻译推进逐章生长——'
    '每章子页含「三语对读 / 汉藏对应 / 延伸阅读」三 tab。' % m2_line,
    '\n'.join(chcards)])


def tabs_bar(labels):
    btns = ['<button type="button" class="tri-tab%s" onclick="__triTab(%d)">%s</button>' % (
        ' is-on' if i == 0 else '', i, lb) for i, lb in enumerate(labels)]
    return '<div class="tri-tabs" role="tablist">\n' + '\n'.join(btns) + '\n</div>'


appx_style = fold('📐 体例与硬约束', """| 项 | 口径 |
|---|---|
| 段制 | 一段藏文 → 一段汉语 → 一段英文；段为最小对齐单位 |
| 藏文来源 | 自德格底本 `{T44-N}…{T44-N+1}` 区间**字节切片**，逐段 norm() 复验可追回原文；**绝不手打藏文** |
| 切段规则 | %s |
| 汉 / 英 | MITRA 9B（bf16 · CPU · greedy）模型译，**未校订**；长输出复读已作 n-gram 禁用 + 周期截断 |
| 品目对应 | 只用已机器实证的对应；未实证一律〔待核〕，不代立论 |
| 完成判定 | 里程碑门禁为被观察到的证据；未全绿不得称完成 |
| 版式 | v0.4（L.378 子页架构批）：总目枢纽＋章子页（随翻译逐章生长）；页内子 tab 分区；三语卡片默认堆叠、可切并排；偈颂分行与术语悬停为预留位（数据层未动） |

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
# ④ 重生成本专题（总目枢纽＋全部章子页）
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
- 〔待核·M5〕藏章14 藏文残字混入（L.379 全段扫描实测）：段1/3 汉译中段、段1–6 英译末尾均有藏文残字（疑解码/复读残留）；数据层原样保留，校订线双轨处理，本批不改。
- 〔待核·M5〕藏章14 段5/6 汉译语义漂移（L.379 落盘验收实测）：起首合本品（百億如來涅槃/須彌山王·四百億諸天），中段以后飘入般若系「善現對曰」问答与「十種法」枚举 boilerplate；英译起首合本品、末尾藏文残字。归 M5 校订线。
- 〔待核·M5〕藏章15 段1：汉译起首误系《佛說大毘盧遮那成佛神變加持經》经题（他经），疑模型错译；该段 status=pending（英译未产出），归 M5 校订线。
- 〔未竟·设计〕术语悬停释义（`.tri-term[data-gloss]` 样式已预留，术语库待 M6 产出后接线）。
- 〔未竟·设计〕章子页「汉藏对应」tab 素材随库存对勘批机械接入：b1/b2 含 `zh80_open` 开篇对照，b3/b4/b6 无该字段者只显对应表与识读；未覆盖章如实标〔未竟〕。""")

HUB_MD = """# %s

> **本页任务**：把德格甘珠尔《大方广佛华严经》（Toh 44，藏文 45 章 / 115 bam po）**逐段译为三语并列**——
> 一段藏文（德格原字形，逐字回源）→ 一段汉语 → 一段英文（后二者由本地模型 `buddhist-nlp/mitra-qwen35-translate` 9B 试译）。
> 汉 / 英译文一律**〔模型译·未校订〕**，只作工作草稿，不作引文、不替代 CBETA 祖本文字。
> **版式 v0.4**：总目枢纽（本页）＋章子页（%d 个已建，随翻译推进逐章生长）；页内子 tab 分区，工程台账折叠于「工程台账」tab。

%s

## 一、总览

%s

## 二、章目导航（45 章全骨架）

%s

> 〔口径〕分组依机器实证对应律；章签数字＝已试译段/切段总数（数据层实测）。亮色章签点击进入该章子页，灰色＝未启动（子页随翻译推进逐章生成）。全量规划表见「工程台账」tab。

## 三、对应研究（库存文献联通）

%s

## 四、工程台账与路线

%s

%s

%s

%s

%s
""" % (TITLE, n_chap, tabs_bar(['总览', '章目导航', '对应研究', '工程台账']), overview, nav_html, corr_hub,
       appx_style, appx_plan, appx_roadmap, appx_repro, appx_todo)


def chapter_md(tc):
    r = plan_by_ch.get(tc) or {}
    d = seg_by_ch[tc]
    ch = d.get('chapter') or {}
    segs = d.get('segments') or []
    don = sum(1 for s in segs if s.get('status') == 'done')
    if r.get('pin'):
        title = '藏章%d · 品%d〈%s〉 — 三语对读' % (tc, r['pin'], r['pin_title_zh'])
    else:
        title = '藏章%d · 汉译开篇对应（章界〔待核〕） — 三语对读' % tc
    crumbs = ('<div class="tri-crumbs"><a href="%s.html">← 返回总目</a><span class="tri-crumbs-sep">／</span>'
              '<b>藏章%d</b><span class="tri-crumbs-rule">%s</span></div>') % (
                  ART_ID, tc, esc(r.get('rule') or '〔待核〕'))
    lead = ('> **德格 %s · 起叶 %s** ｜ 对应：%s ｜ **进度：%d/%d 段已试译**（数据层实测）\n'
            '> %s') % (ch.get('derge_vol'), ch.get('start_folio'), pin_label(r), don, len(segs),
                       ch.get('chinese_correspondence') or '')
    idx = covered.index(tc)
    prev_a = ('<a href="%s">← 藏章%d</a>' % (ch_url(covered[idx - 1]), covered[idx - 1])) if idx > 0 else ''
    next_a = ('<a href="%s">藏章%d →</a>' % (ch_url(covered[idx + 1]), covered[idx + 1])) if idx < len(covered) - 1 else ''
    pager = '<div class="tri-pager">%s<a href="%s.html">返回总目</a>%s</div>' % (prev_a, ART_ID, next_a)
    md = """# %s

%s

%s

%s

%s

## 一、三语对读

%s

%s

> 〔诚实边界〕以上仅覆盖本章**开篇**，非全品；未译段如实标〔待译〕。模型译未经人工校订，不作引文使用，不得替代 CBETA 祖本文字。

## 二、汉藏对应

%s

## 三、延伸阅读

%s
""" % (title, crumbs, lead, pager, tabs_bar(['三语对读', '汉藏对应', '延伸阅读']),
       toolbar, seg_blocks_for(d), corr_pane(tc), links_pane(tc))
    return title, md


CSS = """/* ── 三语对读工作台（L.378 · gen v0.4 子页架构） ── */
.tri-anchor{scroll-margin-top:96px}
.tri-tabs{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0 6px;padding:6px;border:1px solid var(--line);border-radius:10px;background:rgba(94,139,158,.05)}
.tri-tab{border:1px solid transparent;background:transparent;color:var(--text2);border-radius:7px;padding:5px 16px;font-size:.8em;cursor:pointer}
.tri-tab.is-on{border-color:var(--gold);color:var(--gold);background:rgba(184,134,60,.10);font-weight:700}
.tri-crumbs{font-size:.78em;margin:8px 0;color:var(--text2)}
.tri-crumbs a{color:var(--blue);text-decoration:none}
.tri-crumbs-sep{margin:0 8px;opacity:.5}
.tri-crumbs-rule{margin-left:8px;opacity:.7}
.tri-pager{display:flex;gap:10px;justify-content:space-between;flex-wrap:wrap;margin:10px 0;font-size:.78em}
.tri-pager a{color:var(--blue);text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:3px 10px}
.tri-pager a:hover{border-color:var(--gold);color:var(--gold)}
.tri-stats{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0}
.tri-stat{border:1px solid var(--line);border-radius:8px;padding:6px 14px;font-size:.75em;color:var(--text2);background:rgba(94,139,158,.04)}
.tri-stat b{display:block;font-size:1.5em;color:var(--gold)}
.tri-chcard{border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:8px 0;background:rgba(94,139,158,.03)}
.tri-chcard-main{margin:0 0 4px;font-size:.85em}
.tri-chcard-pin{margin-left:10px;color:var(--text2);font-size:.85em}
.tri-chcard-prog{margin:0 0 4px;font-size:.75em;color:var(--text2);display:flex;align-items:center;gap:8px}
.tri-prog{display:inline-block;width:120px;height:6px;border-radius:3px;background:rgba(94,139,158,.15);overflow:hidden}
.tri-prog i{display:block;height:100%;background:var(--gold)}
.tri-chcard-go{margin:0;font-size:.78em}
.tri-chcard-go a{color:var(--blue);text-decoration:none;font-weight:700}
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
.tri-segnav{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin:10px 0;font-size:.75em}
.tri-segchip{border:1px solid var(--line);border-radius:6px;padding:2px 10px;color:var(--text2);text-decoration:none}
.tri-segchip:hover{border-color:var(--gold);color:var(--gold)}
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
.tri-quote{margin:8px 0;padding-left:10px;border-left:3px solid var(--line)}
.tri-quote.tri-qbo{border-left-color:var(--gold)}
.tri-quote.tri-qzh{border-left-color:var(--blue)}
.tri-quote .tri-tag{color:var(--text2)}
.tri-quote.tri-qbo .tri-tag{color:var(--gold)}
.tri-quote.tri-qzh .tri-tag{color:var(--blue)}
.tri-cols .tri-seg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;align-items:start}
.tri-cols .tri-lang{margin-top:0}
@media (max-width:960px){.tri-cols .tri-seg{grid-template-columns:1fr}}
.tri-appx{margin:8px 0}
.tri-term[data-gloss]{border-bottom:1px dotted var(--gold);cursor:help;position:relative}
.tri-term[data-gloss]:hover::after{content:attr(data-gloss);position:absolute;left:0;top:100%;z-index:50;background:rgba(31,36,42,.96);color:#fff;padding:4px 10px;border-radius:6px;font-size:.85em;white-space:nowrap}
"""

JS = """/* ── 三语对读工作台（L.378 · gen v0.4 子页架构） ── */
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
window.__triTab = function (i) {
  var root = document.getElementById('article-full');
  if (!root) return;
  // shell 另渲一个裸 h2 页题（无 secfold）→ pane 只取 h2.secfold
  var hs = root.querySelectorAll('h2.secfold');
  for (var j = 0; j < hs.length; j++) {
    var on = (j === i);
    if (on) { hs[j].classList.remove('is-folded'); hs[j].setAttribute('aria-expanded', 'true'); }
    hs[j].style.display = on ? '' : 'none';
    var b = hs[j].nextElementSibling;
    if (b && b.classList.contains('secfold-body')) b.style.display = on ? '' : 'none';
  }
  var btns = document.querySelectorAll('.tri-tab');
  for (var k = 0; k < btns.length; k++) btns[k].classList.toggle('is-on', k === i);
  try { localStorage.setItem('__PAGE_KEY__', String(i)); } catch (e) {}
};
(function () {
  function paneOf(el) {
    var root = document.getElementById('article-full');
    if (!root) return -1;
    var hs = root.querySelectorAll('h2.secfold');
    for (var i = 0; i < hs.length; i++) {
      if (el === hs[i]) return i;
      var b = hs[i].nextElementSibling;
      if (b && b.classList.contains('secfold-body') && b.contains(el)) return i;
    }
    return -1;
  }
  function fromHash() {
    var h = location.hash.slice(1);
    if (!h) return -1;
    var el = document.getElementById(h);
    return el ? paneOf(el) : -1;
  }
  function init() {
    var root = document.getElementById('article-full');
    if (!root || !root.querySelector('.secfold') || !root.querySelector('h2') || !root.querySelector('.tri-tabs')) return false;
    var hs = root.querySelectorAll('.secfold');
    for (var i = 0; i < hs.length; i++) {
      hs[i].classList.remove('is-folded');
      hs[i].setAttribute('aria-expanded', 'true');
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
    var tab = fromHash();
    if (tab < 0) {
      try { tab = parseInt(localStorage.getItem('__PAGE_KEY__') || '0', 10) || 0; } catch (e) { tab = 0; }
    }
    if (tab >= root.querySelectorAll('h2.secfold').length) tab = 0;
    window.__triTab(tab);
    root.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
      if (!a) return;
      var el = document.getElementById(a.getAttribute('href').slice(1));
      if (!el) return;
      e.preventDefault();
      var p = paneOf(el);
      if (p >= 0) window.__triTab(p);
      if (window._reveal) window._reveal(el);
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (history.replaceState) history.replaceState(null, '', a.getAttribute('href'));
    });
    window.addEventListener('hashchange', function () {
      var p = fromHash();
      if (p >= 0) window.__triTab(p);
    });
    return true;
  }
  function poll(n) { if (init()) return; if (n > 0) setTimeout(function () { poll(n - 1); }, 120); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { poll(20); });
  else poll(20);
})();
"""

# ── 注入自包含页（shell 承 demo 页；页头两处硬编码标题随之替换） ──
shell_html = io.open(SHELL, encoding='utf-8').read()


def inject_page(art_id, title, title_en, sub, version, doc_md, meta, with_updated):
    m = re.search(r'var ARTICLE = (\{.*?\n\});', shell_html, re.S)
    if not m:
        raise SystemExit('FATAL: shell ARTICLE 块未找到')
    obj = json.loads(m.group(1))
    obj['id'] = art_id
    obj['file'] = 'articles/%s.html' % art_id
    obj['title'] = title
    obj['title_en'] = title_en
    obj['title_sub'] = sub
    obj['version'] = version
    obj['icon'] = '🕻'
    obj['doc'] = ''
    obj['doc_md'] = doc_md
    obj['meta'] = meta
    pre = shell_html[:m.start()]
    pre = pre.replace('<title>藏汉英对读 · 大方广佛华严经（德格藏文本）初探 — 独立文章</title>',
                      '<title>%s — 独立文章</title>' % title, 1)
    pre = pre.replace('<h1>藏汉英对读 · 大方广佛华严经（德格藏文本）初探</h1>',
                      '<h1>%s</h1>' % title, 1)
    if with_updated:
        # 「最后更新」时间带：skip_html 页不经 build 注入 → 由本生成器自注册表声明回写
        # （verify_demo 不变量②：注册表声明 updated_at 者产物必显；口径与 build 一致）
        import yaml as _yaml
        _regd = _yaml.safe_load(io.open('data/translation/standalone_articles.yaml', encoding='utf-8')) or {}
        _upd = next(str(o['updated_at']) for o in (_regd.get('others') or [])
                    if o.get('id') == art_id and o.get('updated_at'))
        pre = pre.replace('<span class="art-updated"></span>',
                          '<span class="art-updated">📝 最后更新：%s</span>' % _upd, 1)
        if _upd not in pre:
            raise SystemExit('FATAL: shell 的 art-updated 空位未命中（口径漂移，勿静默产出不符声明的页面）')
    # 章子页不注册 → art-updated 保持空（verify_demo 不变量③）
    block = 'var ARTICLE = ' + json.dumps(obj, ensure_ascii=False, indent=2) + ';'
    page = pre + block + shell_html[m.end():]
    if page.count('</head>') != 1 or page.count('</body>') != 1:
        raise SystemExit('FATAL: shell 注入点不唯一（</head>=%d </body>=%d）' % (
            page.count('</head>'), page.count('</body>')))
    page = page.replace('</head>', '<style>\n' + CSS + '</style>\n</head>', 1)
    page = page.replace('</body>', '<script>\n' + JS.replace('__PAGE_KEY__', 'triTab:' + art_id) + '</script>\n</body>', 1)
    return page


hub_sub = ('德格甘珠尔 Toh 44 · 总目枢纽（45 章导航按对应律分组 · 章子页 %d 个 · 对应研究联通库存文献）· '
           '一段藏→一段汉→一段英 · MITRA 9B 本地模型译·未校订 · '
           '里程碑 %d 个 / 验收门禁 %d 项（工程台账 tab 折叠）' % (
               n_chap, len(roadmap['milestones']), sum(len(x['gate']) for x in roadmap['milestones'])))
hub_ver = ('v0.4 · 子页架构（L.378：hub 四 tab＋章子页三 tab＋对应研究联通库存文献）'
           '· 已试译 %d/%d 段' % (n_done, n_seg))
hub_meta = ('底本：德格甘珠尔《大方广佛华严经》Toh 44（035-038）\n'
            '切段与翻译工作区：workspace/tibetan-avatamsaka-translation/\n'
            '数据层：' + PLAN + ' · ' + ROADMAP + ' · ' + SEG_GLOB)
io.open(OUT, 'w', encoding='utf-8').write(inject_page(
    ART_ID, TITLE, TITLE_EN, hub_sub, hub_ver, HUB_MD, hub_meta, True))
print('OK %s | doc_md %d chars | 章 %d 段 %d（已试译 %d）| 导航章签 %d | hub 四 tab | 附录 fold 5' % (
    OUT, len(HUB_MD), n_chap, n_seg, n_done, len(plan['chapters'])))

for tc in covered:
    title, md = chapter_md(tc)
    r = plan_by_ch.get(tc) or {}
    ch = (seg_by_ch[tc].get('chapter') or {})
    ss = seg_by_ch[tc].get('segments') or []
    don = sum(1 for s in ss if s.get('status') == 'done')
    sub = '德格 %s · 起叶 %s · %s · 已试译 %d/%d 段 · MITRA 9B 模型译〔未校订〕' % (
        ch.get('derge_vol'), ch.get('start_folio'), pin_label(r), don, len(ss))
    ver = 'v0.4 · 章子页（L.378 子页架构）· 三语对读 / 汉藏对应 / 延伸阅读'
    meta = ('底本：德格甘珠尔《大方广佛华严经》Toh 44（035-038）\n'
            '本章数据层：' + seg_fn_by_ch.get(tc, SEG_GLOB) + '\n'
            '总目：articles/%s.html' % ART_ID)
    fn = 'web/demo/articles/%s' % ch_url(tc)
    io.open(fn, 'w', encoding='utf-8').write(inject_page(
        '%s-ch%02d' % (ART_ID, tc), title,
        'Tibetan Avataṃsaka · Chapter %d Trilingual Reading (Tibetan / Chinese / English)' % tc,
        sub, ver, md, meta, False))
    print('OK %s | doc_md %d chars | 段 %d（已试译 %d）| 章子页三 tab | art-updated 空（不注册）' % (
        fn, len(md), len(ss), don))