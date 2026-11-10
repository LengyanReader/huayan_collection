# -*- coding: utf-8 -*-
"""三语专题里程碑门禁检查器（machine 项实测判定 · manual 项只登记不代判）。

铁律口径：「完成」是被观察到的状态。
- PASS   判定条件在现存数据上实测成立
- FAIL   数据存在但条件不成立（阻塞当前里程碑）
- PENDING 前提数据尚未产生（对应里程碑未开工）——**绝不冒充 PASS**
- MANUAL_PENDING 人工闸门项，须人工在 tasks/PROGRESS.md 留证据行
- 退出码：仅当 --milestone 指定里程碑（默认 M0）内出现 FAIL 时非零

用法（项目根）：
  C:\\Users\\data\\miniconda3\\envs\\hy_py312\\python.exe -X utf8 ^
    workspace/tibetan-avatamsaka-translation/tools/check_trilingual_gates.py [--milestone M0|all]
"""
import io, json, re, glob, argparse, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

RM = 'data/translation/tibetan_avatamsaka_trilingual_roadmap.json'
PLAN = 'data/alignment/tibetan_chinese_pin_plan_L360.json'
PAGE = 'web/demo/articles/tibetan-avatamsaka-trilingual.html'
PAGE_GLOB = 'web/demo/articles/tibetan-avatamsaka-trilingual*.html'
YAMLREG = 'data/translation/standalone_articles.yaml'
ART_ID = 'tibetan-avatamsaka-trilingual'
SEG_GLOB = 'data/translation/tibetan_avatamsaka_trilingual_segments*.json'
ALIGN_GLOB = 'data/alignment/tibetan_zhuhuju_b[1-6].json'
FOLIO = re.compile(r'\[[0-9]+[ab](?:\.[0-9]+)?\]')


def norm(s):
    return re.sub(r'\s+', '', FOLIO.sub('', s or ''))


def jload(p):
    return json.loads(io.open(p, encoding='utf-8').read()) if glob.glob(p) else None


def segs_by_chapter():
    by = {}
    for fn in glob.glob(SEG_GLOB):
        d = jload(fn)
        tc = (d.get('chapter') or {}).get('tibetan_no')
        by.setdefault(tc, []).extend(d.get('segments') or [])
    return by


def alignment_open():
    """{藏章号: bo_open}（对勘批既有开篇种子，用于 opening_matches_alignment）。"""
    out = {}
    for fn in glob.glob(ALIGN_GLOB):
        d = jload(fn) or {}
        ch = d.get('chapters') or []
        for v in (ch.values() if isinstance(ch, dict) else ch):
            if isinstance(v, dict) and v.get('tibetan_ch') and v.get('bo_open'):
                out.setdefault(v['tibetan_ch'], norm(v['bo_open']))
    return out


CTX = {}


# ── machine 谓词：返回 (status, info) ──
def p_segments_all_verified():
    sb = CTX['segs']
    if not sb:
        return 'PENDING', '尚无 segments 数据层'
    allseg = [s for v in sb.values() for s in v]
    unver = [s['no'] for s in allseg if not s.get('verified')]
    broken = [s['no'] for s in allseg
              if bool(s.get('zh') and s.get('en')) != (s.get('status') == 'done')]
    if unver or broken:
        return 'FAIL', '未复验段=%s；双语/status 不一致段=%s' % (unver, broken)
    done = sum(1 for s in allseg if s.get('status') == 'done')
    return 'PASS', '章=%d 段=%d（已译 %d）全部逐字复验通过·双语与状态一致' % (len(sb), len(allseg), done)


def p_plan_totals_closed():
    pl = CTX['plan']
    if not pl:
        return 'PENDING', '规划表未派生'
    t = pl['totals']
    s = t['verified_pairs'] + t['tibetan_only'] + t['front_unparallel']
    if s != t['tibetan_chapters']:
        return 'FAIL', '分项和 %d ≠ 45（%s）' % (s, t)
    return 'PASS', '%s · conflicts=%d 条已留痕' % (t, len(pl.get('conflicts') or []))


def p_page_trilingual_order():
    dm = CTX.get('all_doc_md')
    if dm is None:
        return 'PENDING', '页面未生成'
    # v0.4 子页架构：三语段在章子页（#### 段 n，卡片内 tri-bo→tri-zh→tri-en 三色块依序）
    missing = [tc for tc in CTX['segs']
               if not glob.glob('web/demo/articles/%s-ch%02d.html' % (ART_ID, tc))]
    if missing:
        return 'FAIL', '章子页缺失（数据层有段而页面未生成）：%s' % missing
    blocks = re.findall(r'#### 段 \d+[\s\S]*?(?=\n#### 段 \d+|\n### |\n## |\Z)', dm)
    if not blocks:
        return 'FAIL', '页面对读区无三语段'
    bad = [i + 1 for i, b in enumerate(blocks)
           if not (b.find('tri-bo') >= 0 and b.find('tri-zh') > b.find('tri-bo')
                   and b.find('tri-en') > b.find('tri-zh'))]
    if bad:
        return 'FAIL', '段序非 藏→汉→英：%s' % bad
    unmarked = [i + 1 for i, b in enumerate(blocks)
                if ('MITRA 模型译' in b and '未校订' not in b)
                or ('model translation' in b and 'unproofed' not in b)]
    if unmarked:
        return 'FAIL', '模型译缺〔未校订〕标注：%s' % unmarked
    return 'PASS', '%d 个三语段序正确·模型译标注齐全（hub＋%d 章子页合扫）' % (len(blocks), len(CTX['segs']))


def p_registered_skip_html():
    try:
        import yaml
    except Exception as e:
        return 'PENDING', '无 PyYAML：%s' % e
    d = None
    if glob.glob(YAMLREG):
        d = yaml.safe_load(io.open(YAMLREG, encoding='utf-8'))
    if not d:
        return 'PENDING', '注册表未读'
    ents = [o for o in (d.get('others') or []) if o.get('id') == ART_ID]
    if not ents:
        return 'FAIL', 'standalone_articles.yaml 未登记 %s' % ART_ID
    e = ents[0]
    if not e.get('skip_html'):
        return 'FAIL', '该条目缺 skip_html: true（build 会覆写自包含页）'
    dup = [x['id'] for x in d.get('others', []) if x.get('group') == e.get('group')
           and x.get('order_in_group') == e.get('order_in_group') and x['id'] != ART_ID]
    if dup:
        return 'FAIL', '同组 order_in_group=%s 与 %s 冲突' % (e.get('order_in_group'), dup)
    return 'PASS', '已登记（group=%s order=%s skip_html=true·用号无冲突）' % (e.get('group'), e.get('order_in_group'))


def _coverage(rule, need):
    pl, sb = CTX['plan'], CTX['segs']
    if not pl:
        return 'PENDING', '规划表未派生'
    want = [c['tibetan_ch'] for c in pl['chapters'] if c['rule'] == rule]
    missing, short = [], []
    for tc in want:
        v = sb.get(tc) or []
        don = [s for s in v if s.get('status') == 'done' and s.get('verified')]
        if not v:
            missing.append(tc)
        elif len(don) < need:
            short.append('%d(%d/%d)' % (tc, len(don), need))
    if missing or short:
        return 'FAIL' if not missing or len(missing) < len(want) else 'PENDING', '缺章=%s 未足量=%s' % (missing, short)
    return 'PASS', '%s 段 %d 章均各 ≥%d 已译复验段' % (rule, len(want), need)


def p_chapter_coverage_diff5():
    return _coverage('差5', 6)


def p_chapter_coverage_diff6():
    return _coverage('差6', 6)


def p_opening_matches_alignment():
    sb, opens = CTX['segs'], CTX['align']
    if not opens:
        return 'PENDING', '对勘批 bo_open 种子未读'
    if not sb:
        return 'PENDING', '无 segments'
    rec_p = 'data/alignment/tibetan_trilingual_opening_reconcile.json'
    fixed = {}
    if glob.glob(rec_p):
        rc = jload(rec_p) or {}
        fixed = {r['tibetan_ch']: r for r in (rc.get('records') or [])
                 if r.get('tibetan_ch') and len(r.get('evidence') or []) >= 2}
    bad, corrected = [], []
    for tc, v in sb.items():
        if tc not in opens or not v:
            continue
        head = norm(v[0]['bo'])[:24]
        if head and head not in opens[tc] and opens[tc][:24] not in head:
            (corrected if tc in fixed else bad).append(tc)
    if bad:
        return 'FAIL', '首段与对勘批开篇不衔接（须出〔订正〕）：%s' % bad
    if corrected:
        return 'PASS', '已覆盖章首段均衔接；不一致章已登〔订正〕（证据≥2）：%s' % corrected
    return 'PASS', '已覆盖章首段均与 b*.json bo_open 衔接'


def p_progress_column_synced():
    dm, pl, sb = CTX['doc_md'], CTX['plan'], CTX['segs']
    if dm is None or not pl:
        return 'PENDING', '页面或规划表未生成'
    if '三语进度' not in dm:
        return 'FAIL', '页面品目表缺「三语进度」列'
    bad = []
    for line in dm.splitlines():
        m = re.match(r'\|\s*(\d+)\s*\|.*\|\s*(未启动|开篇\d+段已试译)\s*\|\s*$', line)
        if m:
            tc, shown = int(m.group(1)), m.group(2)
            n = sum(1 for s in (sb.get(tc) or []) if s.get('status') == 'done')
            want = '未启动' if n == 0 else '开篇%d段已试译' % n
            if shown != want:
                bad.append('藏%d:页面%s≠数据%s' % (tc, shown, want))
    if bad:
        return 'FAIL', '；'.join(bad[:6])
    return 'PASS', '页面进度列与数据层计数一致'


def p_evidence_cited():
    pl = CTX['plan']
    if not pl:
        return 'PENDING', '规划表未派生'
    rows = [c for c in pl['chapters'] if c['rule'] == '差6']
    noev = [c['tibetan_ch'] for c in rows if not (c.get('evidence') or '').strip() or c['evidence'] == '待核']
    if noev:
        return 'FAIL', '差6 段无证据行：%s' % noev
    return 'PASS', '差6 段 %d 章均有 evidence 行（b5/b6·L.357）' % len(rows)


def p_unique_chapters_unpaired():
    pl, dm = CTX['plan'], CTX['doc_md']
    if not pl or dm is None:
        return 'PENDING', '规划表或页面未生成'
    bad = []
    for tc in (11, 32):
        r = next((c for c in pl['chapters'] if c['tibetan_ch'] == tc), None)
        if not r or r['rule'] != '藏独有' or r['pin']:
            bad.append(tc)
    if bad:
        return 'FAIL', '藏独有章被强行配对或标记丢失：%s' % bad
    if '藏独有' not in dm:
        return 'FAIL', '页面未显示『藏独有』口径'
    return 'PASS', '藏11/藏32 在数据层与页面均保持『藏独有·不配对』'


def p_page_selfcontained():
    files = sorted(glob.glob(PAGE_GLOB))
    if not files:
        return 'PENDING', '页面未生成'
    for fn in files:
        h = io.open(fn, encoding='utf-8').read()
        ext = re.findall(r'(?:src|href)="(https?://[^"]+)"', h)
        if ext:
            return 'FAIL', '%s 存在外部依赖资源：%s' % (fn.split('/')[-1], ext[:3])
        if '藏' not in h or not re.search(r'var ARTICLE = \{', h):
            return 'FAIL', '%s 页面无 ARTICLE 块' % fn.split('/')[-1]
    return 'PASS', '%d 页均自包含（仅站内相对路径）· ARTICLE 在位' % len(files)


def p_cost_table_grounded():
    """M1 G1.1：标定表每个数字可指到来源字段（meta/log），无估算冒充实测。"""
    rm = jload(RM)
    mc = rm.get('measured_constraints') or {}
    cp = rm.get('compute_policy') or {}
    need = ('gen_seconds_per_token', 'batch_measured_seg1_zh', 'batch_final_W1',
            'session_unit_cost_estimate')
    miss = [k for k in need if not mc.get(k)]
    if miss:
        return 'FAIL', '标定表缺来源键：%s' % miss
    if not cp.get('statement'):
        return 'PENDING', '算力决策尚未入账（compute_policy.statement 缺）'
    allseg = [s for v in CTX['segs'].values() for s in v]
    done = [s for s in allseg if s.get('status') == 'done']
    if not done:
        return 'PENDING', '无已译段可标定'
    nomet = [s['no'] for s in done
             if not ((s.get('zh_meta') or {}).get('gen_s')
                     and (s.get('en_meta') or {}).get('gen_s'))]
    if nomet:
        return 'FAIL', '已译段缺 *_meta.gen_s（数字无来源可指）：%s' % nomet
    # 逐批对账：每个 batch_final_* 声明键按 batch_scopes 圈定段集，
    # 总量只与同批 Σmeta 比对（多章落盘后全局求和会拿 W1总量对全部段，口径错误）。
    scopes = mc.get('batch_scopes') or {}
    keys = [k for k in mc if k.startswith('batch_final_')]
    if not keys:
        return 'FAIL', '标定表无 batch_final_* 实测键'
    msgs = []
    for k in keys:
        sc = scopes.get(k)
        if not sc:
            return 'FAIL', '%s 缺 batch_scopes 圈定（总量无对账范围）' % k
        segs = CTX['segs'].get(sc['chapter']) or []
        if sc.get('segs'):
            segs = [s for s in segs if s['no'] in sc['segs']]
        segs = [s for s in segs if s.get('status') == 'done']
        m = re.search(r'总机时\s*([0-9.]+)s', mc[k])
        if not m:
            return 'FAIL', '%s 未声明总机时（数字无来源可指）' % k
        if not segs:
            return 'FAIL', '%s 圈定段集无已译段' % k
        stated = float(m.group(1))
        ssum = sum(s['zh_meta']['gen_s'] + s['en_meta']['gen_s'] for s in segs)
        if abs(stated - ssum) / stated > 0.05:
            return 'FAIL', '%s 总机时 %.1fs 与圈定 Σmeta %.1fs 偏差>5%%' % (k, stated, ssum)
        msgs.append('%s %.1f vs Σmeta %.1f s（差 %.2f%%）' % (k, stated, ssum,
                                                          100 * (stated - ssum) / stated))
    return 'PASS', ('标定表键齐·%d 段 meta 逐数可指·逐批对账：%s'
                    % (len(done), '；'.join(msgs)))


def p_ab_translation_recorded():
    """M1 G1.2：提速候选若采纳，须留同段新旧对照记录于数据层。"""
    cp = jload(RM).get('compute_policy') or {}
    if 'ab_candidates_adopted' not in cp:
        return 'PENDING', '算力决策未入账（ab_candidates_adopted 缺）'
    if not cp['ab_candidates_adopted']:
        return ('PASS', '未采纳提速候选（决策=本机 CPU 逐点推进）→ 无新旧对照义务；'
                        '日后采纳须补 tibetan_avatamsaka_*ab*.json 数据层')
    ab = [p for p in glob.glob('data/translation/tibetan_avatamsaka_*ab*.json')]
    if not ab:
        return 'FAIL', '提速候选标记已采纳，但数据层无同段新旧对照记录'
    return 'PASS', '提速候选已采纳且有对照：%s' % [p.split('/')[-1] for p in ab]


def p_segment_continuity():
    """G2.5：段拼接无损——逐段 norm 衔接无内容缺口；full_chapter 者须覆至章末。

    旧口径（未续切/continued 章）容忍纯 shad 缺口（双 shad 第二 shad 曾被旧提取器漏掉，
    标点级非内容，如实计数）；新切全章（full_chapter 且无 continued）严合零缺口。
    """
    sb = CTX['segs']
    if not sb:
        return 'PENDING', '无 segments'
    import extract_trilingual_segments as ex
    fails, partial, full, notes = [], [], [], []
    for fn in sorted(glob.glob(SEG_GLOB)):
        d = jload(fn)
        tc = (d.get('chapter') or {}).get('tibetan_no')
        segs = d.get('segments') or []
        if not tc or not segs:
            continue
        legacy = bool(d.get('continued')) or not d.get('full_chapter')
        try:
            _, raw, a, b, _, _ = ex.chapter_bounds(tc)
        except SystemExit as e:
            fails.append('藏%s 章界读取失败：%s' % (tc, e))
            continue
        src = ex.norm(raw[a:b])
        cur = src.find(ex.norm(segs[0]['bo']))
        if cur < 0:
            fails.append('藏%d 段1 无法回源' % tc)
            continue
        ok, sg = True, 0
        for s in segs:
            n = ex.norm(s['bo'])
            pos = src.find(n, cur)
            if pos < 0:
                fails.append('藏%d 段%d 无法回源' % (tc, s['no']))
                ok = False
                break
            gap = src[cur:pos]
            if gap:
                if legacy and not gap.strip('།'):
                    sg += 1
                else:
                    fails.append('藏%d 段%d 前内容缺口/重叠 %d 字' % (tc, s['no'], len(gap)))
                    ok = False
                    break
            cur = pos + len(n)
        if not ok:
            continue
        if sg:
            notes.append('藏%d 纯shad缺口%d处（旧口径标点级）' % (tc, sg))
        if cur == len(src):
            full.append(tc)
        elif d.get('full_chapter'):
            fails.append('藏%d 标 full_chapter 但余 %d 字未覆' % (tc, len(src) - cur))
        else:
            partial.append(tc)
    if fails:
        return 'FAIL', '；'.join(fails[:6])
    tail = ('；' + '；'.join(notes)) if notes else ''
    if partial:
        return 'PENDING', '段衔接无内容缺口但未覆至章末（待续切）：%s；已全章 %s%s' % (partial, full, tail)
    return 'PASS', '%d 章段拼接逐字无内容缺口·均覆至章末：%s%s' % (len(full), full, tail)


PREDICATES = {
    'segments_all_verified': p_segments_all_verified,
    'plan_totals_closed': p_plan_totals_closed,
    'page_trilingual_order': p_page_trilingual_order,
    'registered_skip_html': p_registered_skip_html,
    'chapter_coverage_diff5': p_chapter_coverage_diff5,
    'chapter_coverage_diff6': p_chapter_coverage_diff6,
    'opening_matches_alignment': p_opening_matches_alignment,
    'progress_column_synced': p_progress_column_synced,
    'evidence_cited': p_evidence_cited,
    'unique_chapters_unpaired': p_unique_chapters_unpaired,
    'page_selfcontained': p_page_selfcontained,
    'cost_table_grounded': p_cost_table_grounded,
    'ab_translation_recorded': p_ab_translation_recorded,
    'segment_continuity': p_segment_continuity,
}


def page_doc_md():
    if not glob.glob(PAGE):
        return None
    h = io.open(PAGE, encoding='utf-8').read()
    m = re.search(r'var ARTICLE = (\{.*?\n\});', h, re.S)
    if not m:
        return None
    return json.loads(m.group(1)).get('doc_md', '')


def all_pages_doc_md():
    """hub＋全部章子页之 doc_md 合扫（三语段序门禁所系；品目表/藏独有门禁仍只看 hub）。"""
    files = sorted(glob.glob(PAGE_GLOB))
    if not files:
        return None
    out = []
    for fn in files:
        h = io.open(fn, encoding='utf-8').read()
        m = re.search(r'var ARTICLE = (\{.*?\n\});', h, re.S)
        if m:
            out.append(json.loads(m.group(1)).get('doc_md', ''))
    return '\n\n'.join(out) if out else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--milestone', default='M0', help='M0…M9 或 all')
    a = ap.parse_args()
    if not glob.glob(RM):
        print('FAIL roadmap 数据层缺失：%s' % RM)
        return 1
    rm = jload(RM)
    CTX.update(plan=jload(PLAN), segs=segs_by_chapter(), align=alignment_open(),
               doc_md=page_doc_md(), all_doc_md=all_pages_doc_md())
    blockers = 0
    for ms in rm['milestones']:
        if a.milestone != 'all' and ms['id'] != a.milestone:
            continue
        print('== 里程碑 %s · %s（%s）' % (ms['id'], ms['name'], ms['batch']))
        for g in ms['gate']:
            if g['kind'] == 'manual':
                st, info = 'MANUAL_PENDING', g['say']
            else:
                fn = PREDICATES.get(g['check'])
                if fn is None:
                    st, info = 'PENDING', '判定函数未实现（里程碑未开工）：%s' % g['check']
                else:
                    st, info = fn()
            if st == 'FAIL' and (a.milestone == 'all' or ms['id'] == a.milestone):
                if a.milestone == ms['id']:
                    blockers += 1
            print('  [%-14s] %s :: %s' % (st, g['id'], info))
    print('-- 当前里程碑 FAIL=%d（PENDING/MANUAL 不计阻塞）' % blockers)
    return 1 if blockers else 0


if __name__ == '__main__':
    sysexit = main()
    raise SystemExit(sysexit)
