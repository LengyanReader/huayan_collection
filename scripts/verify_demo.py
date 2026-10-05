#!/usr/bin/env python3
"""Verify web/demo build output (index + 6 tab pages) structure before deployment."""
import sys
import os
import shutil
import subprocess, re
import json

# Windows console cp1252 下中文输出会 UnicodeEncodeError — 强制 UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO = os.path.join(ROOT, 'web', 'demo')
ARTICLES = os.path.join(DEMO, 'articles')

TABS = ['lineage', 'gap', 'jiaoxing', 'frontier', 'cosmology', 'spirit']
TAB_TITLES = ['法脉传承', '华严文献', '教海行云', '前沿对话', '世主妙严', '灵性仁本']
DATA_VARS = {
    'lineage': ['var GRAPH'],
    'gap': ['var GAP'],
    'jiaoxing': ['var PRACTICE_DATA'],
    'frontier': ['var FRONTIER_DATA', 'var SPIRIT_DATA'],  # 任一即可
    'cosmology': ['var COSMOLOGY_DATA', 'var SPIRIT_DATA'],
    'spirit': ['var SPIRIT_DATA'],
}

errors = 0

def fail(msg):
    global errors
    errors += 1
    print(f'  FAIL: {msg}')

def ok(msg):
    print(f'  OK:   {msg}')

# ── index.html (导航主页) ──
idx_path = os.path.join(DEMO, 'index.html')
print(f'Verifying {idx_path}\n')
if not os.path.exists(idx_path):
    fail('index.html missing')
else:
    with open(idx_path, encoding='utf-8') as f:
        idx = f.read()
    ok(f'index.html ({len(idx):,} bytes)')
    if not idx.lstrip().startswith('<!DOCTYPE html>'):
        fail('index: missing <!DOCTYPE html>')
    else:
        ok('index: starts with <!DOCTYPE html>')
    if not idx.strip().endswith('</html>'):
        fail('index: must end with </html>')
    else:
        ok('index: ends with </html>')
    for t in TABS:
        if f'tabs/{t}.html' not in idx:
            fail(f'index: missing link to tabs/{t}.html')
    ok('index: links to all 6 tab pages')
    for title in TAB_TITLES:
        if title not in idx:
            fail(f'index: missing module title "{title}"')

print()

# ── 6 个 Tab 页面 ──
for t, title in zip(TABS, TAB_TITLES):
    path = os.path.join(DEMO, 'tabs', f'{t}.html')
    print(f'Verifying tabs/{t}.html ({title})')
    if not os.path.exists(path):
        fail(f'{t}: file missing')
        continue
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # 结构
    if not html.lstrip().startswith('<!DOCTYPE html>'):
        fail(f'{t}: missing <!DOCTYPE html>')
    else:
        ok(f'{t}: DOCTYPE')
    if not html.strip().endswith('</html>'):
        fail(f'{t}: must end with </html>')
    else:
        ok(f'{t}: ends with </html>')

    # div 平衡 (此前多次空白页根因)
    opens = len(re.findall(r'<div\b', html))
    closes = html.count('</div>')
    if opens != closes:
        fail(f'{t}: div mismatch — {opens} open vs {closes} close')
    else:
        ok(f'{t}: div balanced ({opens})')

    # 数据变量已内嵌
    for var in DATA_VARS[t]:
        if var in html:
            ok(f'{t}: {var} embedded')
            break
    else:
        fail(f'{t}: missing embedded data ({DATA_VARS[t]})')

    # 侧边栏导航存在 (lineage用独立布局，无sidebar)
    if t != 'lineage':
        nav_count = html.count('nav-link')
        if nav_count >= 3:
            ok(f'{t}: sidebar nav links ({nav_count})')
        else:
            fail(f'{t}: sidebar nav links missing or too few ({nav_count})')

    # 大小合理 (>10KB)
    if len(html) < 10000:
        fail(f'{t}: size {len(html):,} too small')
    else:
        ok(f'{t}: size {len(html):,} bytes')
# ─── 海云修行体系实证库门禁（源文档级）────────────────────────────
# 与世主妙严品门禁同理：作用于 Markdown 源文档 + YAML 实证库，非构建产物。
# 两道：①verify_haiyun_evidence.py 逐条回源（行号＋字串，信度与台账对账）
#       ②verify_haiyun_draft.py     草稿↔实证库编号一致、无伪断言回潮
# 反向验证（scripts/_verify_haiyun_reverse.py）以破坏性变异确认各项断言真能捕获
# （L109：首轮 6 项盲区——行号容差使偏移通过、下限过松使删条目通过、信度无值域、
#  否定性记录无下限——皆已修，门禁自身之缺陷亦须如实修正，不可迁就）。
_hai_gates = [('evidence', 'verify_haiyun_evidence.py'),
              ('draft', 'verify_haiyun_draft.py')]
for _tag, _fn in _hai_gates:
    _g = os.path.join(os.path.dirname(os.path.abspath(__file__)), _fn)
    if not os.path.exists(_g):
        fail('%s not found — 海云实证库门禁缺失' % _fn)
        continue
    _r = subprocess.run([sys.executable, _g], capture_output=True,
                        encoding='utf-8', errors='replace')
    _out = (_r.stdout or '')
    if _r.returncode != 0 or not _out.strip():
        for _l in [x for x in _out.splitlines() if x.strip()][-6:]:
            print('    ' + _l)
        fail('haiyun: %s 门禁失败（rc=%d）' % (_tag, _r.returncode))
    else:
        _line = [l for l in _out.splitlines() if 'ALL CHECKS PASSED' in l]
        _cnt = [l for l in _out.splitlines() if '条目：' in l]
        ok('haiyun %s: %s' % (_tag, (_cnt[0].strip() if _cnt else
                                     (_line[0].strip() if _line else 'ran'))))

_hai_rev = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '_verify_haiyun_reverse.py')
if not os.path.exists(_hai_rev):
    print('  SKIP: _verify_haiyun_reverse.py not found')
else:
    _r3 = subprocess.run([sys.executable, _hai_rev], capture_output=True,
                         encoding='utf-8', errors='replace')
    _out3 = (_r3.stdout or '')
    if _r3.returncode != 0 or not _out3.strip():
        for _l in _out3.splitlines()[-8:]:
            print('    ' + _l)
        fail('haiyun: 反向验证未全数捕获（rc=%d）' % _r3.returncode)
    else:
        _last = [l for l in _out3.splitlines() if '反向验证' in l]
        ok('haiyun: %s' % (_last[-1].strip() if _last else '反向验证 ran'))

print()

# ── 独立文章页 (articles/<id>.html) ──
print('Verifying articles/ (standalone article pages)\n')
aidx = os.path.join(ARTICLES, 'index.html')
if not os.path.exists(aidx):
    fail('articles/index.html missing')
else:
    with open(aidx, encoding='utf-8') as f:
        idx = f.read()
    if '独立文章目录' not in idx:
        fail('articles/index: missing title')
    else:
        ok('articles/index: catalog title')
    hrefs = re.findall(r'href="([^"]+\.html)"', idx)
    art_files = {h for h in hrefs if not h.startswith('../')}
    ok(f'articles/index: links to {len(art_files)} article pages')
    missing = [h for h in art_files if not os.path.exists(os.path.join(ARTICLES, h))]
    if missing:
        fail(f'articles/index: broken hrefs {missing}')
    else:
        ok('articles/index: all hrefs resolve')

# ── 「最后更新」时间带：登记源 → 产物 一一对账 ──
# 不变量：① 页面上出现的每个「最后更新：」日期必能在 YAML 注册表找到同值（禁凭空日期）；
#         ② 注册表声明 updated_at 者产物必显；③ 未注册者产物时间带须为空（不得以构建时间冒充内容更新时间）；
#         ④ 日期须为 ISO YYYY-MM-DD。
import re as _re
import yaml as _yaml
_reg = _yaml.safe_load(open(os.path.join(ROOT, 'data', 'translation', 'standalone_articles.yaml'), encoding='utf-8')) or {}
_decl = {}
for _o in (_reg.get('others') or []):
    if _o.get('updated_at'):
        _decl[_o['id']] = str(_o['updated_at'])
_ts = _yaml.safe_load(open(os.path.join(ROOT, 'data', 'translation', 'topic_studies.yaml'), encoding='utf-8')) or {}
for _a in (_ts.get('articles') or []):
    if _a.get('id') and _a.get('updated_at'):
        _decl[_a['id']] = str(_a['updated_at'])
_badfmt = {k: v for k, v in _decl.items() if not _re.fullmatch(r'\d{4}-\d{2}-\d{2}', v)}
if _badfmt:
    fail(f'articles updated_at: 非 ISO 日期 {sorted(_badfmt)}')
else:
    ok(f'articles updated_at: {_len if False else len(_decl)} 条声明皆为 ISO YYYY-MM-DD')
_orph, _miss = [], []
for _id, _v in sorted(_decl.items()):
    _p = os.path.join(ARTICLES, _id + '.html')
    if not os.path.exists(_p):
        _miss.append(_id + '(page absent)')
        continue
    _h = open(_p, encoding='utf-8').read()
    _m = _re.search(r'<span class="art-updated">(.*?)</span>', _h, _re.S)
    _shown = (_m.group(1).strip() if _m else '')
    if _v not in _shown:
        _miss.append(f'{_id}(声明 {_v} / 产物 {_shown or "空"})')
for _obj in sorted(os.listdir(ARTICLES)):
    if not _obj.endswith('.html') or _obj == 'index.html':
        continue
    _id = _obj[:-5]
    if _id in _decl:
        continue
    _h = open(os.path.join(ARTICLES, _obj), encoding='utf-8').read()
    for _d in _re.findall(r'<span class="art-updated">([^<]*最后更新[^<]*)</span>', _h):
        if _d.strip():
            _orph.append(f'{_id}:{_d.strip()}')
if _orph:
    fail(f'articles updated_at: 未注册却显时间 {_orph}')
else:
    ok('articles updated_at: 无未注册而显时间者')
if _miss:
    fail(f'articles updated_at: 声明与产物不符 {_miss}')
else:
    ok(f'articles updated_at: {_len if False else len(_decl)} 条声明与产物一一对账')

for obj in sorted(os.listdir(ARTICLES)):
    if not obj.endswith('.html') or obj == 'index.html':
        continue
    path = os.path.join(ARTICLES, obj)
    with open(path, encoding='utf-8') as f:
        html = f.read()
    checks = [
        ('DOCTYPE', html.lstrip().startswith('<!DOCTYPE html>')),
        ('ends </html>', html.strip().endswith('</html>')),
        ('ARTICLE embedded', 'var ARTICLE =' in html),
        # 独立文章页分两种形式：doc 驱动（内嵌 doc_md + renderArticle）或数据驱动
        # （内嵌 PRACTICE_DATA / GAP_DATA 数据源 + 自包含渲染脚本，正文单存于 YAML，
        #  如 chan-traces → renderChanTraces；avatamsaka-studies / panjiao → renderDynTopics；
        #  海云讲法全库 → renderWizLibrary）
        ('doc_md embedded', '"doc_md"' in html or 'var PRACTICE_DATA' in html or 'var GAP_DATA' in html),
        ('renderer inlined', 'function renderArticle' in html
            or 'function renderChanTraces' in html
            or 'function renderDynTopics' in html
            or 'function renderWizLibrary' in html),
        ('common.css', '../css/common.css' in html),
    ]
    bad = [c[0] for c in checks if not c[1]]
    # 会众名号 EDA 页：数据与调用在页面内，渲染器本体在 js/common.js（外链共享），故分处检查。
    # 分源之要：经文事实（ARTICLE_ASSEMBLY）须与编辑性析构（ARTICLE_EDA）并存且页面明言之。
    if 'var ARTICLE_EDA' in html:
        eda_checks = [
            ('ARTICLE_ASSEMBLY (经文事实)', 'var ARTICLE_ASSEMBLY' in html),
            ('renderArticleEDA 调用', "renderArticleEDA('#article-eda" in html),
            ('edaGo 入口', 'function edaGo' in html),
            ('剖面节容器', 'id="article-eda"' in html),
        ]
        bad += [c[0] for c in eda_checks if not c[1]]
        # 渲染器要件（声明/群组/热力）落在外链 js/common.js
        cjs_path = os.path.join(DEMO, 'js', 'common.js')
        cjs = open(cjs_path, encoding='utf-8').read() if os.path.exists(cjs_path) else ''
        for label, token in (('renderArticleEDA 渲染器', 'function renderArticleEDA'),
                             ('方法与限度声明', '切分方法与限度'),
                             ('体例声明（编辑性析构）', '编辑性析构'),
                             ('群组纵深', '群组纵深'),
                             ('热力矩阵', '热力矩阵')):
            if token not in cjs:
                bad.append(f'js/common.js 缺 {label}')
        # 交互面板默认折叠壳（panel-fold）：文本分析层/会众名号剖面/叙事动画须纳入可折叠 <details>，
        # 由 _foldShellHtml 生成，内容渲染入壳内 *-inner 容器；页首另设「全页折叠/展开」一对统管。
        pf_checks = [
            ('_foldShellHtml 折叠壳', "class=\"fold panel-fold\"" in cjs),
            ('EDA 折叠壳内渲染', "renderArticleEDA('#article-eda-inner')" in html),
            ('BI 折叠壳内渲染', "_foldShellHtml('bi-report-inner'" in html),
            ('叙事动画折叠壳内渲染', "renderMiaoyanNarrative('#article-narrative-inner')" in html),
            ('全页折叠控件', 'function _installPageBar' in cjs or '_installPageBar' in cjs),
        ]
        bad += [c[0] for c in pf_checks if not c[1]]

    # 文本分析层：内嵌 ARTICLE_BI + article.js 内的 renderArticleBI。
    # schema 契约：校验「产物实际内嵌之 JSON」含渲染器所读之全部键路径——
    # 前端零硬编码，故键名笔误会静默渲染不出内容（而非报错），必以契约卡住。
    if 'var ARTICLE_BI' in html:
        bi_checks = [
            ('renderArticleBI 渲染器', 'function renderArticleBI' in html),
            ('biGo 入口', 'function biGo' in html),
            ('BI 入口按钮', 'onclick="biGo()"' in html),
            ('BI 节容器', 'id="bi-report"' in html),
        ]
        bad += [c[0] for c in bi_checks if not c[1]]
        # 锚定 </script>：BI 脚本仅一条赋值语句，故取「贪婪至最后一个 };」即全量 JSON
        # （不可用 };\n 或非贪婪 —— JSON 字符串值内可能含 `};` 之形）
        m = re.search(r'var ARTICLE_BI = (\{.*?\});</script>', html, re.S)
        if not m:
            bad.append('ARTICLE_BI JSON 无法定位')
        else:
            try:
                bi = json.loads(m.group(1))
            except Exception as e:
                bi = None
                bad.append(f'ARTICLE_BI JSON 解析失败({e.__class__.__name__})')
            if bi is not None:
                # (路径, 期望类型) —— 与 renderArticleBI 所读键一一对应
                contract = [
                    ('scorecard.items', list), ('funnel.track_names.stages', list),
                    ('funnel.track_tokens.stages', list), ('funnel.grades', dict),
                    ('funnel.conversion.tokens_per_name', (int, float)),
                    ('domain_landscape.rows', list), ('domain_landscape.concentration.hhi', (int, float)),
                    ('crosstab.groups', list), ('crosstab.domains', list), ('crosstab.matrix', list),
                    ('similarity.names', list), ('similarity.matrix', list),
                    ('clustering.clusters', list), ('clustering.curve', list),
                    ('pca.points', list), ('pca.explained', list),
                    ('pareto.series', list), ('network.top_pagerank', list),
                    ('network.truncation.n_used_edges', (int, float)),
                    ('ordinal.segments', list), ('ordinal.z', (int, float)),
                    ('quality.robustness', list), ('executive.findings', list),
                ]
                missing = []
                for path, typ in contract:
                    cur = bi
                    for k in path.split('.'):
                        if isinstance(cur, dict) and k in cur:
                            cur = cur[k]
                        else:
                            cur = None
                            break
                    if not isinstance(cur, typ) or (typ is list and not cur):
                        missing.append(path)
                if missing:
                    bad.append(f'ARTICLE_BI 契约缺键 {missing}')
                else:
                    ok(f'articles/{obj}: BI schema 契约 {len(contract)} 键路径齐备')
    if bad:
        fail(f'articles/{obj}: missing {", ".join(bad)}')
    else:
        ok(f'articles/{obj} ({len(html):,} bytes, all checks)')

# ── Tab 页内「独立文章页」入口条链接解析检查 ──
chip_errors = 0
for t in TABS:
    if t == 'lineage':
        continue
    with open(os.path.join(DEMO, 'tabs', f'{t}.html'), encoding='utf-8') as f:
        html = f.read()
    for href in re.findall(r'href="../articles/([^"]+\.html)"', html):
        if not os.path.exists(os.path.join(ARTICLES, href)):
            fail(f'tabs/{t}.html: chip href broken -> articles/{href}')
            chip_errors += 1
if chip_errors == 0:
    ok('tabs: all article-chip hrefs resolve')

# ── gap 侧栏「华严祖师 / 专题研究」→ 直接进入独立文章页 ──
gap_path = os.path.join(DEMO, 'tabs', 'gap.html')
with open(gap_path, encoding='utf-8') as f:
    gp_html = f.read()
gp_need = ['../articles/master-dushun.html', '../articles/master-zhiyan.html',
           '../articles/master-fazang.html', '../articles/master-chengguan.html',
           '../articles/master-zongmi.html', '../articles/master-litongxuan.html',
           '../articles/master-mengcan.html', '../articles/zhenwei.html']
gp_missing = [h for h in gp_need if h not in gp_html]
if gp_missing:
    fail(f'gap sidebar: missing direct article links {gp_missing}')
else:
    ok('gap sidebar: 8 article entries link straight to standalone pages')
if 'articlePageHref' not in gp_html:
    fail('gap: articlePageHref helper missing')
else:
    ok('gap: articlePageHref helper present')

print()

# ─── 构建产物 JS 语法校验（node --check）──────────────────────────────
# 说明：JS 语法错误不会令本脚本的字符串检查失败，却会使整份 common.js 不执行、
#       全站交互（含语言开关）失效，故须独立校验。node 缺失时跳过并如实标注。
print('Verifying built JavaScript syntax')
_js_dir = os.path.join(DEMO, 'js')
_js_files = sorted(f for f in os.listdir(_js_dir) if f.endswith('.js')) if os.path.isdir(_js_dir) else []
_node = shutil.which('node')
if not _node:
    print('  SKIP: node not found — JS syntax check skipped')
elif not _js_files:
    fail('js/: no built JavaScript files found')
else:
    for _f in _js_files:
        _p = os.path.join(_js_dir, _f)
        _r = subprocess.run([_node, '--check', _p], capture_output=True, text=True)
        if _r.returncode != 0:
            _msg = (_r.stderr or '').strip().splitlines()
            fail(f'js/{_f}: syntax error — {_msg[0] if _msg else "parse failed"}')
        else:
            ok(f'js/{_f}: syntax OK')

    # BI 渲染器冒烟测试（node）：renderArticleBI 纯拼字符串、不触 DOM，故可在 node 中实跑。
    # 仅 --check 语法不足以证其可运行 —— 键名笔误、类型误判皆为静默失败（渲染不出内容而不报错）。
    _smoke = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verify_bi_render.js')
    if not _node:
        print('  SKIP: node not found — BI render smoke test skipped')
    elif not os.path.exists(_smoke):
        print('  SKIP: verify_bi_render.js not found')
    else:
        for _t in sorted(os.listdir(ARTICLES)):
            if not _t.endswith('.html') or _t == 'index.html':
                continue
            _p = os.path.join(ARTICLES, _t)
            if 'var ARTICLE_BI' not in open(_p, encoding='utf-8').read():
                continue
            _r = subprocess.run([_node, _smoke, _p], capture_output=True, text=True)
            if _r.returncode != 0:
                fail(f'articles/{_t}: BI render — {(_r.stderr or "").strip().splitlines()[-1]}')
            else:
                ok(f'articles/{_t}: BI render — {(_r.stdout or "").strip()}')

    # 叙事动画播放器冒烟测试（node）：MiaoyanNarrative 触 DOM/Canvas，故以最小
    # DOM+Canvas 桩实跑，驱动播放/暂停/步进/跳拍/进度/倍速/图层诸控件，并校验环位
    # 口径（一点=一类，全图 40 类 == assembly 之 40 类／414 名）。
    # --check 仅能证语法，不能证「按钮真的绑了、画布真的出图、旁白随拍切换」。
    _nsmoke = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'verify_narrative_render.js')
    if not _node:
        print('  SKIP: node not found — narrative render smoke test skipped')
    elif not os.path.exists(_nsmoke):
        print('  SKIP: verify_narrative_render.js not found')
    else:
        for _t in sorted(os.listdir(ARTICLES)):
            if not _t.endswith('.html') or _t == 'index.html':
                continue
            _p = os.path.join(ARTICLES, _t)
            if 'var MIAOYAN_NARR' not in open(_p, encoding='utf-8').read():
                continue
            _r = subprocess.run([_node, _nsmoke, _p], capture_output=True,
                                encoding='utf-8', errors='replace')
            if _r.returncode != 0 or not (_r.stdout or '').strip():
                # stdout 空亦计失败：非 ASCII 输出遇 locale 解码失败时 rc 仍为 0，
                # 若只验 rc 会出现「显示 OK 而无任何证据」的假绿。
                _msg = (_r.stderr or _r.stdout or 'no output (rc=%d)' % _r.returncode)
                fail(f'articles/{_t}: narrative render — {_msg.strip().splitlines()[-1]}')
            else:
                ok(f'articles/{_t}: narrative render — {(_r.stdout or "").strip()}')

    # 要点导览门禁（node）：MiaoyanKeypoints 触 DOM/Canvas，故以最小 DOM+Canvas 桩实跑。
    # 与叙事门禁分工：那一路证曼荼罗六环，此一路证 8 要点之内挂正文（#article-kp）——
    # 故须先证 markdown 未吞占位（正文内挂载之前提），再证数据不变量（要点号连续/四层
    # 注册/point_at 落在单位圆上/判断者必附 judgment_zh/引文逐字见于 T279），末驱控件。
    # 皆以页面内联之源码/数据为准；改桩只会「测不到东西」。
    _ksmoke = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'verify_keypoints_render.js')
    _common_js = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'web', 'demo', 'js', 'common.js')
    _cbeta_t279 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               'data', 'references', 'cbeta', 'T10n0279.xml')
    if not _node:
        print('  SKIP: node not found — keypoints render gate skipped')
    elif not os.path.exists(_ksmoke):
        print('  SKIP: verify_keypoints_render.js not found')
    else:
        for _t in sorted(os.listdir(ARTICLES)):
            if not _t.endswith('.html') or _t == 'index.html':
                continue
            _p = os.path.join(ARTICLES, _t)
            if 'var MIAOYAN_KP' not in open(_p, encoding='utf-8').read():
                continue
            _r = subprocess.run([_node, _ksmoke, _p, _common_js, _cbeta_t279],
                                capture_output=True, encoding='utf-8', errors='replace')
            if _r.returncode != 0 or not (_r.stdout or '').strip():
                _msg = (_r.stderr or _r.stdout or 'no output (rc=%d)' % _r.returncode)
                fail(f'articles/{_t}: keypoints render — {_msg.strip().splitlines()[-1]}')
            else:
                ok(f'articles/{_t}: keypoints render — {(_r.stdout or "").strip()}')

    # 会众全景流程门禁（node）：MiaoyanFlow 触 DOM，故以最小 DOM 桩实跑。与要点/叙事门禁分工：
    # 此一路证「详版全景流程图」之不损——四十类之类名/上首/全成员名号/本愿原文，
    # 既须逐字见于渲染产物（折叠亦在 DOM），亦须逐字见于 CBETA T10n0279（回源）；
    # 末驱检索/展开/折叠/跳转/目录诸控件。
    _fsmoke = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'verify_flow_render.js')
    if not _node:
        print('  SKIP: node not found — flow render gate skipped')
    elif not os.path.exists(_fsmoke):
        print('  SKIP: verify_flow_render.js not found')
    else:
        for _t in sorted(os.listdir(ARTICLES)):
            if not _t.endswith('.html') or _t == 'index.html':
                continue
            _p = os.path.join(ARTICLES, _t)
            _c = open(_p, encoding='utf-8').read()
            if 'var ARTICLE_ASSEMBLY' not in _c or 'function renderMiaoyanFlow' not in _c:
                continue
            _r = subprocess.run([_node, _fsmoke, _p, _common_js, _cbeta_t279],
                                capture_output=True, encoding='utf-8', errors='replace')
            if _r.returncode != 0 or not (_r.stdout or '').strip():
                _msg = (_r.stderr or _r.stdout or 'no output (rc=%d)' % _r.returncode)
                fail(f'articles/{_t}: flow render — {_msg.strip().splitlines()[-1]}')
            else:
                ok(f'articles/{_t}: flow render — {(_r.stdout or "").strip()}')

# ─── 世主妙严品专书门禁（源文档级）────────────────────────────────────
# 前述诸门禁皆作用于**构建产物**（页面/JS）。本门禁作用于**Markdown 源文档**
# 《华严经细读_第一部_世主妙严品.md》之学术正确性：实测口径、旧数回潮、引文回源
# （含海云讲记逐字）、来源声明自洽。凡经此门禁，故其成果不因重建而失效。
# 内含反向验证（scripts/_verify_shizhu_reverse.py）：以破坏性变异确认各断言真能捕获，
# 否则「全绿」不足为凭（L106 已立之原则）。
_shizhu = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verify_shizhu.py')
_shizhu_rev = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '_verify_shizhu_reverse.py')
if not os.path.exists(_shizhu):
    fail('verify_shizhu.py not found — 世主妙严品专书门禁缺失')
else:
    _r = subprocess.run([sys.executable, _shizhu], capture_output=True,
                        encoding='utf-8', errors='replace')
    _tail = [l for l in (_r.stdout or '').splitlines() if l.strip()][-6:]
    if _r.returncode != 0 or not (_r.stdout or '').strip():
        for _l in _tail:
            print('    ' + _l)
        fail('shizhu: 专书门禁失败（rc=%d）' % _r.returncode)
    else:
        _line = [l for l in (_r.stdout or '').splitlines() if 'ALL CHECKS PASSED' in l]
        ok('shizhu: 专书门禁 — %s' % (_line[0].strip() if _line else 'ran'))
    if os.path.exists(_shizhu_rev):
        _r2 = subprocess.run([sys.executable, _shizhu_rev], capture_output=True,
                             encoding='utf-8', errors='replace')
        _last = [l for l in (_r2.stdout or '').splitlines() if '反向验证' in l]
        if _r2.returncode != 0 or not (_r2.stdout or '').strip():
            for _l in (_r2.stdout or '').splitlines()[-6:]:
                print('    ' + _l)
            fail('shizhu: 反向验证未全数捕获（rc=%d）' % _r2.returncode)
        else:
            ok('shizhu: 反向验证 — %s' % (_last[-1].strip() if _last else 'ran'))
    else:
        print('  SKIP: _verify_shizhu_reverse.py not found')

print()

print('=' * 40)
if errors == 0:
    print('✅ ALL CHECKS PASSED')
    sys.exit(0)
else:
    print(f'❌ {errors} ERROR(S) FOUND')
    sys.exit(1)
