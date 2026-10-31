#!/usr/bin/env python3
"""
Build web/demo/ from src/ files + data/ directory.
Produces: index.html + tabs/*.html (5) + css/common.css + js/common.js

Usage (from project root):
  python web/demo/scripts/build.py
"""
import json
import html as _html
import yaml
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC = ROOT / 'web' / 'demo' / 'src'
DATA_DIR = ROOT / 'data'
OUT = ROOT / 'web' / 'demo'
TABS_OUT = OUT / 'tabs'
CSS_OUT = OUT / 'css'
JS_OUT = OUT / 'js'
ARTICLES_OUT = OUT / 'articles'

# SQLite data reader (single source of truth for graph data)
sys.path.insert(0, str(ROOT / 'scripts'))
import db_reader


def read_src(name):
    """Read a source file from src/ directory."""
    path = SRC / name
    if path.exists():
        with open(path, encoding='utf-8') as f:
            return f.read()
    return ''


def read_yaml(rel_path):
    """Read a YAML file from data/ directory."""
    path = DATA_DIR / rel_path
    if path.exists():
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f)
    return None


def read_json(rel_path):
    """Read a JSON file."""
    path = ROOT / rel_path
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def load_graph():
    """Load complete GRAPH data from SQLite (single source of truth)."""
    return db_reader.load_graph()


def load_gap():
    """Load GAP data from gap.json and gap_content.yaml."""
    gap = read_json('web/demo/gap.json')
    # Merge in gap_content
    gc = read_yaml('translation/gap_content.yaml')
    if gc:
        gap['content'] = gc
    # Merge avatamsaka studies
    avs = read_yaml('translation/avatamsaka_studies.yaml')
    if avs:
        gap['avatamsaka_studies'] = avs
    # Merge intertextual canon
    ic = read_yaml('translation/intertextual_canon.yaml')
    if ic:
        gap['intertextual_canon'] = ic
    # Merge panjiao hupan (判教互判 — 各宗派/宗教/学术/科技流派的判教与互判)
    pj = read_yaml('translation/panjiao_hupan.yaml')
    if pj:
        gap['panjiao_hupan'] = pj
    # Merge huayan masters (华严祖师 — 五祖+李通玄; 贤首/清凉国师含综述全文)
    hm = read_yaml('translation/huayan_masters.yaml')
    if hm:
        gap['huayan_masters'] = hm
        # 读取各祖师全方位文献综述 markdown, 按 master id 注入 (review_mds)
        review_mds = {}
        for m in hm.get('masters', []):
            rd = m.get('review_doc')
            if rd:
                doc_path = ROOT / rd
                if doc_path.exists():
                    with open(doc_path, encoding='utf-8') as f:
                        review_mds[m.get('id')] = f.read()
        if review_mds:
            gap['huayan_masters']['review_mds'] = review_mds
    # Merge topic studies (专题研究 — 整篇深度研究文档全文注入)
    ts = read_yaml('translation/topic_studies.yaml')
    if ts:
        gap['topic_studies'] = {k: v for k, v in ts.items() if k != 'articles'}
        gap['topic_studies']['articles'] = []
        for art in ts.get('articles', []):
            a = dict(art)
            a['doc_md'] = ''
            dp = a.get('doc')
            if dp:
                doc_path = ROOT / dp
                if doc_path.exists():
                    with open(doc_path, encoding='utf-8') as f:
                        a['doc_md'] = f.read()
            gap['topic_studies']['articles'].append(a)
    # Merge texts/chapters/cross_refs from SQLite (complete catalog)
    texts_data = db_reader.load_texts()
    if texts_data:
        gap['texts_catalog'] = texts_data
    # Merge bilingual glossary from SQLite (authoritative L1 source; 50 terms)
    gloss = db_reader.load_glossary()
    if gloss:
        gap['glossary'] = gloss
    return gap


def load_events():
    """Load all event YAML files and return merged dict."""
    import glob as _glob
    events = {}
    events_dir = DATA_DIR / 'events'
    if events_dir.exists():
        for fpath in _glob.glob(str(events_dir / '*.yaml')):
            name = os.path.splitext(os.path.basename(fpath))[0]
            data = read_yaml(f'events/{name}.yaml')
            if data:
                events[name] = data
    return events


def load_cosmology():
    """Load cosmology data from YAML files."""
    cosmo = {}
    for name in ['cosmo_layers', 'three_realms', 'art_treasures', 'heritage_critical']:
        data = read_yaml(f'cosmology/{name}.yaml')
        if data:
            cosmo[name] = data
    return cosmo


def load_practice():
    """Load practice data from YAML files."""
    practice = {}
    for name in ['cultivation_system', 'meditation_essentials',
                 'teaching_resources', 'heart_xref',
                 'youtube_playlists', 'huayan_panjiao',
                 'dushun_wujiao_zhiguan',
                 'haiyun_practice_sources',
                 'haiyun_xinfa_primary',
                 'haiyun_avatamsaka_lectures',
                 'mengcan_lectures',
                 'chan_authentic_traces',
                 'chengguan_master',
                 'haiyun_chengguan_compare',
                 'vinaya_school',
                 'faxiang_xuanji',
                  'yikong_daodi',
                   'mimi_daodi',
                    'tiantai_juejing',
'zhuandao_ziliang',
                      'sanshiqi_daopin',
                      'chan_contemplation',
                      'haiyun_wiz_catalog',
                      'haiyun_podcast_catalog',
                      'haiyun_lectures_topics']:
        data = read_yaml(f'practice/{name}.yaml')
        if data:
            practice[name] = data
    return practice


def load_frontier():
    """Load frontier data."""
    return read_yaml('frontier/frontier_dialogue.yaml') or {}


def load_spirit():
    """Load spirit data from multiple YAML files."""
    data = read_yaml('spirit/spirit_content.yaml') or {}
    # Merge environmental humanities
    eh = read_yaml('spirit/environmental_humanities.yaml')
    if eh: data['environmental_humanities'] = eh
    # Merge haiyun primary source quotes
    hp = read_yaml('spirit/haiyun_spiritual_economics_primary.yaml')
    if hp: data['haiyun_primary'] = hp
    return data


def load_bibliography():
    """Load master bibliography from data/references/bibliography.yaml.
    Returns dict with keys: sutras, books, reports, haiyun, online, meta.
    """
    return read_yaml('references/bibliography.yaml') or {}


def load_glossary():
    """Load bilingual glossary from data/references/bilingual_glossary.yaml."""
    return read_yaml('references/bilingual_glossary.yaml') or {}


def load_navigation():
    """Load site navigation spec from data/navigation.yaml (drives all sidebars)."""
    data = read_yaml('navigation.yaml') or {}
    # Handle both wrapped {'navigation': {...}} and flat {gap: {...}} formats
    if 'navigation' in data and isinstance(data['navigation'], dict):
        return data['navigation']
    return data


def _action_js(action, is_sub):
    """Render onclick JS body for a navigation action.

    action: {'type':'call','fn':..,'args':[..]} | {'type':'assign','var':..,'value':..,'call':..} | {'href':..}
    Top-level items append `,this` to call actions; sub-links do not.
    """
    if not action:
        return ''
    if action.get('type') == 'assign':
        return f"{action['var']}='{action['value']}';{action['call']}();return false"
    if 'href' in action:
        return ''
    fn = action.get('fn', '')
    args = [f"'{a}'" for a in action.get('args', [])]
    if not is_sub:
        args.append('this')
    return f"{fn}({','.join(args)});return false"


def _nav_label(item):
    """Compose a nav item label (emoji + text + optional <small> subtitle)."""
    label = item.get('label', '')
    label_sub = item.get('label_sub', '')
    if label_sub:
        label += f' <small style=font-size:0.7em;color:var(--text2)>{label_sub}</small>'
    return label


def render_sidebar(nav_spec):
    """Render sidebar HTML from a navigation spec.

    Output format matches the legacy hardcoded sidebars exactly:
    a leading newline + 4-space indentation per line.
    """
    lines = []
    heading = nav_spec.get('heading', '')
    heading_sub = nav_spec.get('heading_sub', '')
    if heading_sub:
        lines.append(f'    <h3>{heading} <small style=font-size:0.65em;color:var(--text2)>{heading_sub}</small></h3>')
    else:
        lines.append(f'    <h3>{heading}</h3>')
    for item in nav_spec.get('nav', []):
        active = ' active' if item.get('active') else ''
        label = _nav_label(item)
        action = item.get('action', {})
        if item.get('subs'):
            open_ = item.get('open')
            arrow = '▾' if open_ else '▸'
            onclick = f"if(!toggleSidebarGroup(this))return false;{_action_js(action, False)}"
            lines.append('    <div class="sidebar-group has-subs">')
            lines.append(f'    <a href="#" class="nav-link has-subs{active}" onclick="{onclick}">{label} <span class="toggle-arrow">{arrow}</span></a>')
            sub_display = ' style=display:block' if open_ else ''
            lines.append(f'    <div class="sub-links"{sub_display}>')
            for sub in item['subs']:
                sub_cls = 'sub-sub-link' if sub.get('subsub') else 'sub-link'
                sub_action = sub.get('action', {})
                if 'href' in sub_action:
                    lines.append(f'    <a href="{sub_action["href"]}" class="{sub_cls}" style="color:var(--gold)" title="独立文章页">{_nav_label(sub)} ↗</a>')
                else:
                    lines.append(f'    <a href="#" class="{sub_cls}" onclick="{_action_js(sub_action, True)}">{_nav_label(sub)}</a>')
            lines.append('    </div></div>')
        else:
            if 'href' in action:
                lines.append(f'    <div class="sidebar-group"><a href="{action["href"]}" class="nav-link{active}">{label}</a></div>')
            else:
                lines.append(f'    <div class="sidebar-group"><a href="#" class="nav-link{active}" onclick="{_action_js(action, False)}">{label}</a></div>')
    return '\n' + '\n'.join(lines)


def inject_frontier_subs(nav_spec, frontier_data, articles):
    """为前沿对话侧栏注入子目录：每个对话节的域(domain)子项 + 域内独立文章子子项。

    域与文章均读自数据源（frontier_dialogue.yaml / standalone_articles.yaml），
    不在 HTML/JS 中硬编码；域子项调用 switchFrontierDomain 高亮并滚动到对应卡片。
    """
    if not nav_spec or not frontier_data:
        return
    order = ['huayan', 'chinese', 'buddhist', 'others']
    for item in nav_spec.get('nav', []):
        act = item.get('action', {}) or {}
        key = (act.get('args') or [''])[0] if act.get('type') == 'call' else None
        if key not in order:
            continue
        sec = (frontier_data.get('sections') or {}).get(key, {}) or {}
        subs = []
        for d in sec.get('domains', []):
            did = d.get('id')
            if not did:
                continue
            subs.append({
                'label': (d.get('icon') or '') + ' ' + d.get('domain', ''),
                'action': {'type': 'call', 'fn': 'switchFrontierDomain', 'args': [key, did]},
            })
            for a in articles:
                if did in (a.get('views') or []):
                    subs.append({
                        'label': (a.get('icon') or '') + ' ' + a.get('title', a['id']),
                        'subsub': True,
                        'action': {'href': '../' + a['file']},
                    })
        if subs:
            item['subs'] = subs
            if key == 'huayan' and not item.get('open'):
                item['open'] = True


def get_bib_for_tags(bib, tags):
    """Filter bibliography entries matching any of the given tags.
    Returns a flat list of matching entries across all categories.
    """
    matches = []
    for category in ['sutras', 'books', 'reports', 'haiyun', 'online']:
        for entry in bib.get(category, []):
            entry_tags = set(entry.get('tags', []))
            if entry_tags & set(tags):
                matches.append(dict(entry, _category=category))
    return matches


# ── HTML page template ──
PAGE_TOP = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>华严宗 · {title}</title>
<link rel="stylesheet" href="../css/common.css">
</head>
<body>
<div id="page-top" style="position:sticky;top:0;z-index:100">
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>{title}</h1>
  <button id="lang-toggle" class="lang-btn" onclick="toggleSiteLang();return false" title="阅读语言：中英对照 ⇄ 仅中文">🌐 中·EN</button>
  <a href="#" onclick="heartLogin();return false" style="margin-left:auto;font-size:0.7em;color:var(--text2);text-decoration:none" title="配置GitHub Token">🔑 登录</a>
</header>
<div style="background:rgba(196,107,93,0.08);border-bottom:1px solid rgba(196,107,93,0.25);padding:6px 16px;font-size:0.72em;color:var(--red);text-align:center">
⚠️ 声明：本页面内容尚处于初始梳理阶段，在完整性、准确度、详实度、深度等方面均有不足，仅供参考；敬请多提建议，以助完善内容。
</div>
</div>
<div class="layout">
  <nav class="sidebar" id="sidebar">
    {sidebar_links}
  </nav>
  <main class="content" id="content">
  </main>
</div>
<div class="comment-box" id="cmt-{tab_id}"></div>
<script src="../js/common.js"></script>
<script>
// ═══ EMBEDDED DATA ═══
var GRAPH = {graph_json};
var GAP = {gap_json};
var EVENTS = {events_json};
var COSMO_DATA = {cosmo_json};
var PRACTICE_DATA = {practice_json};
var FRONTIER_DATA = {frontier_json};
var HEART_ARTICLES = {heart_json};
</script>
<script>
{tab_js}
</script>
<script>
{init_js}
</script>
</body>
</html>'''


def wrap_script(js_content):
    """Wrap JS content properly, handling closing script tags."""
    return js_content.replace('</script>', '<\\/script>')


def build_page(title, tab_id, sidebar_links, tab_js_name, init_call):
    """Build a single tab HTML page."""
    tab_js = read_src(f'{tab_js_name}.js')
    init_js = f'renderComments("{tab_id}");{init_call}'

    # Load all data
    graph = load_graph()
    gap = load_gap()
    events = load_events()
    cosmo = load_cosmology()
    practice = load_practice()
    frontier = load_frontier()
    heart = read_json('web/demo/gap.json')  # placeholder
    # Load HEART_ARTICLES from wechat markdown files
    import glob as _g, re as _re
    heart_articles = []
    wechat_dir = ROOT / 'docs' / 'hy_refs' / 'wechat'
    if wechat_dir.exists():
        for fpath in sorted(_g.glob(str(wechat_dir / '*.md'))):
            with open(fpath, 'r', encoding='utf-8') as f:
                text = f.read()
            title_m = _re.search(r'^# (.+)$', text, _re.MULTILINE)
            title = title_m.group(1).strip() if title_m else os.path.basename(fpath)
            # Remove frontmatter
            body = _re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=_re.MULTILINE|_re.DOTALL, count=1)
            for meta in ['来源','摘要','原文','下一篇','提取日期']:
                body = _re.sub(r'^\*\*'+meta+r'[:：].*$', '', body, flags=_re.MULTILINE)
            body = _re.sub(r'^# .+$', '', body, 1, flags=_re.MULTILINE)
            body = _re.sub(r'^\s*---\s*$', '', body, flags=_re.MULTILINE)
            body = body.strip()
            # Convert images
            body = _re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'''<div class='himg'><img src='\2' alt='\1' onclick='window.open(this.src)' title='点击查看原图'></div>''', body)
            body = _re.sub(r'\[图片\]', '', body)
            body = _re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', body)
            body = _re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', body)
            paras = [p.strip() for p in body.split('\n\n') if p.strip()]
            body = ''
            for p in paras:
                if p.startswith('<div class=') or p.startswith('<img'):
                    body += p + '\n'
                elif len(p)<80 and not p.startswith('<') and p.count('\n')==0:
                    body += '<h4>' + p + '</h4>\n'
                else:
                    body += '<p>' + p.replace('\n','<br>') + '</p>\n'
            wx_url = ''
            url_m = _re.search(r'原文[:：]\*{0,2}\s*(https?://[^\s\n]+)', text)
            if url_m: wx_url = url_m.group(1)
            heart_articles.append({'title': title, 'body': body.strip(), 'url': wx_url})

    html = PAGE_TOP.format(
        title=title,
        tab_id=tab_id,
        sidebar_links=sidebar_links,
        graph_json=json.dumps(graph, ensure_ascii=False),
        gap_json=json.dumps(gap, ensure_ascii=False),
        events_json=json.dumps(events, ensure_ascii=False),
        cosmo_json=json.dumps(cosmo, ensure_ascii=False),
        practice_json=json.dumps(practice, ensure_ascii=False),
        frontier_json=json.dumps(frontier, ensure_ascii=False),
        heart_json=json.dumps(heart_articles, ensure_ascii=False),
        tab_js=wrap_script(tab_js),
        init_js=init_call
    )
    return html


def build_famai_shell():
    """Build 法脉传承模块壳 (famai/index.html) from data/famai_subpages.yaml registry.
    Adding a new sub-page = one more registry entry (F.0 design, tasks/PLAN.md)."""
    reg = read_yaml('famai_subpages.yaml')
    if not reg:
        print('WARN famai_subpages.yaml missing - skip famai shell')
        return ''
    mod = reg.get('module', {})
    subs = reg.get('subpages', [])
    status_badge = {'live': ('已上线', 'var(--green,#3d8b5f)'),
                    'in-build': ('施工中', 'var(--gold,#b8863c)'),
                    'planned': ('規劃中', 'var(--text2)')}
    cards = ''
    for s in subs:
        zh, col = status_badge.get(s.get('status', 'planned'), status_badge['planned'])
        badge = '<span style="font-size:0.62em;padding:2px 8px;border:1px solid {};border-radius:10px;color:{}">{}</span>'.format(col, col, zh)
        inner = ('<span class="icon">{}</span>'
                 '<h3>{} <span style="font-size:0.65em;color:var(--text2);font-weight:400">{}</span> {}</h3>'
                 '<p style="font-size:0.82em">{}</p>'
                 '<div class="tag-row">{}</div>').format(
            s.get('icon', ''), s.get('title', ''), s.get('title_en', ''), badge, s.get('summary', ''),
            ''.join('<span class="tag">{}</span>'.format(t) for t in s.get('tags', [])))
        if s.get('status') == 'live':
            cards += '<a href="{}" class="card">{}</a>\n'.format(s.get('file', '#'), inner)
        else:
            cards += '<div class="card" style="opacity:0.72;cursor:default" title="批次 F.2–F.5 施工中">{}</div>\n'.format(inner)
    # 静态兜底（信息無损惯例）：注册表全字段 always-in-DOM
    reg_rows = ''
    for s in subs:
        ds = '；'.join(s.get('data_sources', []))
        reg_rows += ('<tr><td>{}</td><td>{}／{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n').format(
            s.get('id', ''), s.get('title', ''), s.get('title_en', ''),
            s.get('file', ''), s.get('status', ''), ds)
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>法脉传承 · 视角模块</title>
<link rel="stylesheet" href="../css/common.css">
<style>
.wrap{{max-width:1080px;margin:0 auto;padding:24px 20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px;margin-top:18px}}
.card{{display:block;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:12px;padding:18px 20px;text-decoration:none;color:var(--text);transition:transform .15s,box-shadow .15s}}
.card:hover{{transform:translateY(-2px);box-shadow:0 6px 18px rgba(60,40,20,.12)}}
.card h3{{color:var(--gold);margin:6px 0}}
.tag-row{{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}}
.tag{{font-size:0.68em;padding:2px 8px;border-radius:10px;background:var(--panel);border:1px solid var(--line);color:var(--text2)}}
table{{border-collapse:collapse;width:100%;font-size:0.72em}}
td,th{{border:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}}
</style>
</head>
<body>
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>🌊 {mod.get('title','法脉传承')} · 视角模块 <span style="font-size:0.55em;color:var(--text2);font-weight:400">{mod.get('title_en','')}</span></h1>
</header>
<div class="wrap">
  <p style="color:var(--text2);font-size:0.88em">{mod.get('intro','')}</p>
  <p style="color:var(--text2);font-size:0.78em;font-style:italic">{mod.get('intro_en','')}</p>
  <div class="grid">
{cards}  </div>
  <details style="margin-top:22px;font-size:0.8em">
    <summary>📇 子页注册表溯源 · Sub-page registry（<code>data/famai_subpages.yaml</code> v{reg.get('version','')} · {reg.get('last_updated','')}）——新增子页只改本表</summary>
    <table><tr><th>id</th><th>标题</th><th>文件</th><th>状态</th><th>数据源</th></tr>
{reg_rows}    </table>
  </details>
</div>
</body>
</html>'''
    famai_dir = OUT / 'famai'
    famai_dir.mkdir(exist_ok=True)
    shell_path = famai_dir / 'index.html'
    with open(shell_path, 'w', encoding='utf-8') as f:
        f.write(html)
    size = len(html.encode('utf-8'))
    print(f'OK  {shell_path} ({size:,} bytes | {len(subs)} subpages registered)')
    return size


# ══════════════ F.2 「山河法脉」底图子页 ＋ license 声明页 ══════════════
GEO_VIEW_LON = (58, 142)
GEO_VIEW_LAT = (0, 60)
GEO_CW, GEO_CH = 840, 540


def _geo_proj(lon, lat):
    x = (lon - GEO_VIEW_LON[0]) / (GEO_VIEW_LON[1] - GEO_VIEW_LON[0]) * GEO_CW
    y = (GEO_VIEW_LAT[1] - lat) / (GEO_VIEW_LAT[1] - GEO_VIEW_LAT[0]) * GEO_CH
    return (round(x, 1), round(y, 1))


def _geo_all_pts(geom):
    def walk(g):
        t = g.get('type'); c = g.get('coordinates')
        if not c:
            return
        if t == 'Polygon':
            for ring in c:
                for pt in ring:
                    yield pt[:2]
        elif t == 'MultiPolygon':
            for poly in c:
                for ring in poly:
                    for pt in ring:
                        yield pt[:2]
        elif t == 'LineString':
            for pt in c:
                yield pt[:2]
        elif t == 'MultiLineString':
            for seg in c:
                for pt in seg:
                    yield pt[:2]
    return list(walk(geom))


def _geo_rings(geom, max_rings=12, max_pts=180):
    """只保外环（洞不显·骨架阶段），按点数抽稀。"""
    t = geom.get('type'); c = geom.get('coordinates') or []
    raw = []
    if t == 'Polygon' and c:
        raw.append(c[0])
    elif t == 'MultiPolygon':
        for poly in c[:max_rings]:
            if poly:
                raw.append(poly[0])
    out = []
    for ring in raw:
        step = max(1, len(ring) // max_pts)
        pts = [_geo_proj(p[0], p[1]) for p in ring[::step]][:max_pts + 1]
        if len(pts) >= 4:
            out.append(pts)
    return out


def _geo_lines(geom, max_pts=220):
    t = geom.get('type'); c = geom.get('coordinates') or []
    seqs = [c] if t == 'LineString' else (c if t == 'MultiLineString' else [])
    out = []
    for s in seqs:
        step = max(1, len(s) // max_pts)
        pts = [_geo_proj(p[0], p[1]) for p in s[::step]][:max_pts + 1]
        if len(pts) >= 2:
            out.append(pts)
    return out


def _geo_feature_bbox_hits_view(geom):
    pts = _geo_all_pts(geom)
    if not pts:
        return False
    lons = [p[0] for p in pts]; lats = [p[1] for p in pts]
    return not (max(lons) < GEO_VIEW_LON[0] or min(lons) > GEO_VIEW_LON[1]
                or max(lats) < GEO_VIEW_LAT[0] or min(lats) > GEO_VIEW_LAT[1])


# ── F.4 只读投影（S3 地谱卡 · S4 法脉展开 · S5 法系色块）────────────────────
# 数据皆现存 SSOT（temple_directory / lineages.json / complete_lineage_chart /
# person_trajectories），本层仅**只读投影**、不改任一 SSOT。客观传承守卫：反向边剔除。
import collections as _collections

HUAYAN_FOCUS_LINEAGES = {'lineage_hw5', 'lineage_japan', 'lineage_goryeo',
                         'lineage_huayen_lotus', 'lineage_yuexia',
                         'lineage_xianshou_gaoyuan', 'lineage_贤首宗高原法系'}
HUAYAN_BRANCH_CN = {'lineage_hw5': '华严五祖', 'lineage_japan': '日本华严',
                    'lineage_goryeo': '高丽华严', 'lineage_huayen_lotus': '华严莲社',
                    'lineage_yuexia': '月霞系', 'lineage_xianshou_gaoyuan': '高原法系',
                    'lineage_贤首宗高原法系': '高原法系'}
HUAYAN_BRANCH_COLOR = {'华严五祖': '#b8863c', '日本华严': '#8b7a9e', '高丽华严': '#6f93b4',
                       '华严莲社': '#5e8b9e', '月霞系': '#7a9ec0', '高原法系': '#c46b5d'}
HW_ORDER = {'person_001': 1, 'person_002': 2, 'person_003': 3, 'person_004': 4, 'person_005': 5}
HW_BACKBONE_ID = 'lineage_hw_patriarchs'


def _f4_is_huayan_temple(t):
    s = t.get('school') or ''
    return ('华严' in s) or ('贤首' in s) or str(t.get('id', '')).startswith('t_huayan_')


def _f4_person_meta():
    """id→(name,color) 只读自 person_trajectories（178 人）。"""
    pt = read_yaml('events/person_trajectories.yaml') or {}
    persons = pt.get('persons', pt)
    names, colors = {}, {}
    if isinstance(persons, dict):
        for pid, v in persons.items():
            if isinstance(v, dict):
                names[pid] = v.get('name')
                colors[pid] = v.get('color')
    return names, colors


def _f6_person_geo():
    """F.6a 法脉时间化：person_id → {x, y, year}（路线质心投影+中位纪年）。
       只读 person_trajectories·不添加·不臆造·无 route 者不入表。"""
    pt = read_yaml('events/person_trajectories.yaml') or {}
    persons = pt.get('persons', pt)
    geo = {}
    if not isinstance(persons, dict):
        return geo
    for pid, v in persons.items():
        route = (v or {}).get('route') or []
        pts = []
        years = []
        for s in route:
            try:
                lat = float(s.get('lat')); lng = float(s.get('lng'))
            except (TypeError, ValueError):
                continue
            if not (GEO_VIEW_LON[0] <= lng <= GEO_VIEW_LON[1] and GEO_VIEW_LAT[0] <= lat <= GEO_VIEW_LAT[1]):
                continue
            x, y = _geo_proj(lng, lat)
            pts.append((x, y))
            yr = s.get('y')
            if yr is not None:
                years.append(int(yr))
        if pts:
            cx = sum(p[0] for p in pts) / len(pts)
            cy = sum(p[1] for p in pts) / len(pts)
            med_year = sorted(years)[len(years) // 2] if years else None
            geo[pid] = {'x': round(cx, 1), 'y': round(cy, 1), 'year': med_year}
    return geo


def _f4_temples():
    """S3：华严核心要地子集（school 含华严/贤首 或 id t_huayan_ 前缀）。投影实测坐标。"""
    td = read_yaml('locations/temple_directory.yaml') or {}
    out = []
    for t in td.get('temples', []):
        if not _f4_is_huayan_temple(t):
            continue
        try:
            x, y = _geo_proj(float(t.get('lng')), float(t.get('lat')))
        except (TypeError, ValueError):
            continue
        out.append({
            'id': t.get('id'), 'name': t.get('name', ''), 'ancient': t.get('ancient_name', ''),
            'school': t.get('school', ''), 'type': t.get('type', ''), 'location': t.get('location', ''),
            'dynasty': t.get('dynasty', ''), 'founded': t.get('founded'), 'founder': t.get('founder', ''),
            'desc': t.get('description', ''), 'sig': t.get('significance', ''),
            'persons': t.get('persons') or [], 'events': t.get('events') or [],
            'source': t.get('source', ''), 'verified': t.get('verified'),
            'links': t.get('links') or [], 'lat': t.get('lat'), 'lng': t.get('lng'), 'x': x, 'y': y,
        })
    return out


def _f4_lineage():
    """S4：CBDB 式递归（华严核心支系·直系 MASTER_OF / 私淑·影响 INFLUENCED 分列）。
       守卫：剔自环 + 剔与法统次序相悖的反向边（数据自歧·各照骨干不擅改 SSOT）。"""
    names, colors = _f4_person_meta()
    lj = read_json('data/knowledge_graph/lineages.json') or {}
    adj = _collections.defaultdict(list)
    for L in lj.get('lineages', []):
        lid = L.get('id')
        if lid not in HUAYAN_FOCUS_LINEAGES:
            continue
        br = HUAYAN_BRANCH_CN.get(lid, L.get('name'))
        for e in L.get('edges', []):
            f, d, rel = e.get('from'), e.get('to'), e.get('relation')
            if not f or not d or f == d or rel not in ('MASTER_OF', 'INFLUENCED'):
                continue
            if f in HW_ORDER and d in HW_ORDER and HW_ORDER[f] > HW_ORDER[d]:
                continue  # 反向边（如 宗密→澄观）与法统相悖 → 剔出直系展开、不擅改原档
            adj[f].append({'disc': d, 'rel': rel, 'note': e.get('note', ''), 'branch': br})

    masters = [{'id': f, 'name': names[f], 'color': colors.get(f)}
               for f, lst in adj.items()
               if any(x['rel'] == 'MASTER_OF' for x in lst) and names.get(f)]
    masters.sort(key=lambda m: (HW_ORDER.get(m['id'], 99), m['id']))

    trees = {}
    for m in masters:
        res = []

        def walk(pid, depth, path):
            for e in adj.get(pid, []):
                d = e['disc']
                if d in path:
                    continue
                dn = names.get(d)
                res.append({'parent': pid, 'pname': names.get(pid), 'disc': d, 'dname': dn,
                            'dverified': bool(dn), 'rel': e['rel'], 'branch': e['branch'],
                            'depth': depth + 1, 'note': e.get('note', '')})
                if depth + 1 < 3:
                    walk(d, depth + 1, path | {d})

        walk(m['id'], 0, {m['id']})
        trees[m['id']] = res

    backbone = []
    clc = read_yaml('knowledge_graph/complete_lineage_chart.yaml') or {}
    for L in clc.get('lineages', []):
        if L.get('id') == HW_BACKBONE_ID:
            for g in L.get('generations', []):
                backbone.append({'order': g.get('order'), 'name': g.get('name'),
                                 'title': g.get('title'), 'years': g.get('years'),
                                 'note': g.get('note', '')})
            break

    seen, branches = set(), []
    for lid in HUAYAN_FOCUS_LINEAGES:
        cn = HUAYAN_BRANCH_CN.get(lid)
        if cn and cn not in seen:
            seen.add(cn)
            branches.append({'name': cn, 'color': HUAYAN_BRANCH_COLOR.get(cn, '#888888')})
    branches.sort(key=lambda b: 0 if b['name'] == '华严五祖' else 1)
    return {'masters': masters, 'trees': trees, 'branches': branches, 'backbone': backbone}


# G 系列·全法脉网络总览（G.0 只读投影·非只华严 focus 支系）
NET_RELATIONS = ('MASTER_OF', 'INFLUENCED', 'CONTEMPORARY')  # 现存三类·不臆造 TRANSMITTED_TEXT
NET_PALETTE = ['#b8863c', '#8b7a9e', '#6f93b4', '#5e8b9e', '#7a9ec0', '#c46b5d',
               '#7a9e7e', '#a6915d', '#b47fa0', '#88a48c', '#c07f6a', '#7f8fb4']


def _f_net():
    """G.0 全法脉网络只读投影：lineages.json 全部支系 → {nodes, links, branches}。
       剔自环·只画现存边·无名 id 保 null（前端标〔待核〕）·不添加·不臆造。
       节点色按所属支系（支系色 Python 单源算定·静态兜底与前端一致）。"""
    names, _colors = _f4_person_meta()
    lj = read_json('data/knowledge_graph/lineages.json') or {}
    links, nodes, branches, bseen = [], {}, [], set()
    for L in lj.get('lineages', []):
        lid = L.get('id', '')
        cn = HUAYAN_BRANCH_CN.get(lid) or L.get('name') or lid
        if cn not in bseen:
            bseen.add(cn)
            col = HUAYAN_BRANCH_COLOR.get(cn) or NET_PALETTE[len(branches) % len(NET_PALETTE)]
            branches.append({'id': lid, 'name': cn, 'color': col})
        bcol = next((b['color'] for b in branches if b['name'] == cn), '#888888')
        for e in L.get('edges', []):
            f, d, rel = e.get('from'), e.get('to'), e.get('relation')
            if not f or not d or f == d or rel not in NET_RELATIONS:
                continue
            links.append({'source': f, 'target': d, 'rel': rel, 'branch': cn,
                          'color': bcol, 'note': e.get('note', '')})
            for pid in (f, d):
                nd = nodes.setdefault(pid, {'id': pid, 'name': names.get(pid),
                                            'out': 0, 'in': 0, 'branches': []})
                if cn not in nd['branches']:
                    nd['branches'].append(cn)
            if rel == 'MASTER_OF':
                nodes[f]['out'] += 1
                nodes[d]['in'] += 1
    for nd in nodes.values():
        nd['verified'] = bool(nd['name'])
    return {'nodes': list(nodes.values()), 'links': links, 'branches': branches}


def build_shanhe_page():
    """子页 B「山河法脉」(famai/shanhe.html)：NE 物理底(PD)＋aourednik 断代色块(GPL 独立集合)
    ＋Ghost Diff＋DB 标点＋静态兜底（信息無损）。数据均实测投影，不臆造几何。"""
    import datetime
    geo = DATA_DIR / 'geo'
    man = read_yaml('geo/manifest.yaml') or {}
    if not (geo / 'historical-basemaps').exists():
        print('WARN data/geo 未入库（先跑 scripts/f2_fetch_geo.py）- skip shanhe')
        return 0

    years_out = []
    for y in (500, 600, 700, 800, 900):
        p = geo / 'historical-basemaps' / ('world_%d.geojson' % y)
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding='utf-8'))
        polities = []
        for f in d.get('features', []):
            geom = f.get('geometry') or {}
            pts = _geo_all_pts(geom)
            if not pts:
                continue
            lon = sum(q[0] for q in pts) / len(pts); lat = sum(q[1] for q in pts) / len(pts)
            if not (60 <= lon <= 138 and 0 <= lat <= 58):
                continue
            pr = f['properties'].get('BORDERPRECISION')
            polities.append({
                'n': f['properties'].get('NAME'),
                'sup': f['properties'].get('SUBJECTO') or '',
                'pr': pr if pr is not None else '',
                'rings': _geo_rings(geom),
            })
        years_out.append({'year': y, 'polities': polities})

    coast, countries = [], []
    p = geo / 'natural_earth' / 'ne_110m_coastline.geojson'
    if p.exists():
        for f in json.loads(p.read_text(encoding='utf-8')).get('features', []):
            if _geo_feature_bbox_hits_view(f.get('geometry') or {}):
                coast.append(_geo_lines(f['geometry']))
    p = geo / 'natural_earth' / 'ne_110m_admin_0_countries.geojson'
    if p.exists():
        for f in json.loads(p.read_text(encoding='utf-8')).get('features', []):
            g = f.get('geometry') or {}
            if g.get('type') in ('Polygon', 'MultiPolygon') and _geo_feature_bbox_hits_view(g):
                countries.extend(_geo_rings(g, max_rings=8, max_pts=140))

    places = []
    graph = load_graph()
    for loc in graph.get('locations', []):
        try:
            lat = float(loc.get('lat')); lng = float(loc.get('lng'))
        except (TypeError, ValueError):
            continue
        if GEO_VIEW_LON[0] <= lng <= GEO_VIEW_LON[1] and GEO_VIEW_LAT[0] <= lat <= GEO_VIEW_LAT[1]:
            x, y2 = _geo_proj(lng, lat)
            places.append({'id': loc.get('id', ''), 'n': loc.get('n', ''), 'lat': loc.get('lat'),
                           'lng': loc.get('lng'), 'tp': loc.get('tp', ''), 'dy': loc.get('dy', ''),
                           'x': x, 'y': y2})

    # F.3 S2 祖师行迹（逐字回源引文挂载·data/events/person_chronicle_citations.yaml）
    cit = read_yaml('events/person_chronicle_citations.yaml') or {}
    persons_out = []
    for pid in sorted((cit.get('persons') or {}).keys()):
        pp = cit['persons'][pid]
        sts = []
        for s in pp.get('stations', []):
            try:
                x, y2 = _geo_proj(float(s.get('lng')), float(s.get('lat')))
            except (TypeError, ValueError):
                continue
            sts.append({'index': s.get('index'), 'label': s.get('label', ''), 'yr': s.get('y'),
                        'lat': s.get('lat'), 'lng': s.get('lng'), 'x': x, 'y': y2,
                        'status': s.get('status', ''), 'quote': s.get('quote'),
                        'source': s.get('source'), 'anchor': s.get('anchor'),
                        'url': s.get('url'), 'note': s.get('note', '')})
        if sts:
            persons_out.append({'id': pid, 'name': pp.get('name', pid),
                                'person_source': pp.get('person_source', ''), 'stations': sts})

    # ── F.4 S3/S4/S5 只读投影 ──
    temples_out = _f4_temples()
    lin = _f4_lineage()
    net = _f_net()  # G.0 全法脉网络只读投影（24 支·现存边）
    _lnames, _lcolors = _f4_person_meta()
    person_geo = _f6_person_geo()  # F.6a 法脉时间化：地理质心+中位纪年

    payload = {
        'canvas': {'w': GEO_CW, 'h': GEO_CH},
        'view': {'lon': list(GEO_VIEW_LON), 'lat': list(GEO_VIEW_LAT)},
        'years': years_out,
        'base': {'coast': coast, 'countries': countries},
        'places': places,
        'persons': persons_out,
        'temples': temples_out,
        'lineage': lin,
        'lineage_net': net,
        'person_geo': person_geo,
        'meta': {'generated': str(datetime.date.today()),
                 'license_note': '断代层 aourednik/historical-basemaps (GPL-3.0 独立集合)；物理层 Natural Earth (PD)；CHGIS 依其许可仅外链'},
    }
    data_json = json.dumps(payload, ensure_ascii=False).replace('</', '<\\/')

    year_buttons = ''.join('<button class="year-btn" data-year="%d">%d</button>' % (yy['year'], yy['year'])
                           for yy in years_out)
    # F.5 S1 连续时间滑轨：min/max 取实存快照首末·value 取首快照（数据驱动·不臆造中间年代几何）
    _ymin = years_out[0]['year'] if years_out else 500
    _ymax = years_out[-1]['year'] if years_out else 900
    _y0 = _ymin
    person_options = '<option value="">— 择祖师行迹（点人溯事）—</option>' + ''.join(
        '<option value="%s">%s</option>' % (p['id'], p['name']) for p in persons_out)

    # 静态兜底（信息無损）：逐年政体表＋标点表＋层源表 always-in-DOM
    fb = ''
    for yy in years_out:
        rows = ''
        for po in sorted(yy['polities'], key=lambda q: (q['n'] is None, str(q['n']))):
            rows += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                po['n'] or '(未標名）', po['sup'] or '—', po['pr'] if po['pr'] != '' else '〔待核〕')
        fb += ('<details style="margin:6px 0"><summary>西 %d 年快照 · %d 政体（东亚区内）</summary>'
               '<table><tr><th>政体 NAME</th><th>宗主/归因</th><th>边界精度</th></tr>%s</table></details>\n'
               % (yy['year'], len(yy['polities']), rows))
    prows = ''
    for e in man.get('layers', []):
        prows += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            e.get('file', ''), e.get('license', ''), e.get('accessed', ''), str(e.get('sha256', ''))[:12])
    fb += ('<details style="margin:6px 0"><summary>层源与许可（data/geo/manifest.yaml · %d 层）</summary>'
           '<table><tr><th>文件</th><th>许可</th><th>访问日期</th><th>sha256前12</th></tr>%s</table></details>'
           % (len(man.get('layers', [])), prows))

    # 祖师行迹静态兜底（信息無损·逐字回源）：每站 label/纪年/引文/出处/页锚/URL/按语 全字段在场
    _esc = _html.escape
    for p in persons_out:
        srows = ''
        for s in p['stations']:
            if s['status'] == 'sourced':
                cite = '「%s」' % _esc(s['quote'] or '')
                src = '%s · 〔%s〕' % (_esc(s['source'] or ''), _esc(s['anchor'] or ''))
                link = '<a href="%s">%s</a>' % (_esc(s['url'] or ''), _esc(s['url'] or '')) if s.get('url') else '—'
            else:
                cite = '<span style="color:#b00">〔待核〕底本未载此站逐字句</span>'
                src = '—'
                link = '—'
            note = ('<br><small>%s</small>' % _esc(s['note'])) if s.get('note') else ''
            srows += ('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                      % (s['index'], _esc('%s（西 %s 年）' % (s['label'], s['yr'])),
                         cite, src + note, link))
        fb += ('<details style="margin:6px 0"><summary>🚶 %s · 行迹 %d 站（%s）</summary>'
               '<table><tr><th>#</th><th>站点</th><th>一手引文（繁体逐字回源）</th><th>出处·页锚·按语</th><th>底本URL</th></tr>%s</table></details>\n'
               % (_esc(p['name']), len(p['stations']), _esc(p['person_source'] or ''), srows))

    # ── F.4 S4 择师下拉（仅列有直系弟子且具 name 记录者·数据驱动）──
    lineage_options = '<option value="">— 择祖师·递归展开弟子链（S4）—</option>' + ''.join(
        '<option value="%s">%s</option>' % (m['id'], _esc(m['name'])) for m in lin['masters'])

    # ── F.4 静态兜底（信息無损·全字段逐字在场）──
    # S5 法系色块图例
    legend_chips = ''.join(
        '<span class="lg-chip" data-branch="%s"><i style="background:%s"></i>%s</span>'
        % (_esc(b['name']), _esc(b['color']), _esc(b['name'])) for b in lin['branches'])
    fb += ('<details style="margin:6px 0"><summary>🗺️ 法系分支图例（S5·色块隔离基准 · %d 支）</summary>'
           '<table><tr><th>分支</th><th>色值</th><th>直系/影响边数（本批 focus 子集）</th></tr>%s</table></details>\n'
           % (len(lin['branches']),
              ''.join('<tr><td><i style="display:inline-block;width:10px;height:10px;background:%s"></i> %s</td>'
                      '<td>%s</td><td>%d</td></tr>'
                      % (_esc(b['color']), _esc(b['name']), _esc(b['color']),
                         sum(1 for m in lin['masters'] for e in lin['trees'][m['id']] if e['branch'] == b['name']))
                      for b in lin['branches'])))

    # S4 五祖法统骨干（蒸馏自 complete_lineage_chart·客观祖统）
    _hw_note = '法藏→澄观为「私淑」（隔代影响·非直系）；本骨干表法统序次，弟子链详见各师递归。'
    fb += ('<details style="margin:6px 0"><summary>👑 华严五祖法统骨干（complete_lineage_chart · %d 世）</summary>'
           '<table><tr><th>序</th><th>名</th><th>尊号</th><th>年代</th><th>注</th></tr>%s</table>'
           '<p class="lic">%s</p></details>\n'
           % (len(lin['backbone']),
              ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                      % (g['order'], _esc(g['name']), _esc(g['title'] or '—'), _esc(g['years'] or '—'),
                         _esc(g['note'] or '')) for g in lin['backbone']),
              _esc(_hw_note)))

    # S4 逐师递归弟子链（每师一表·全字段·未具名弟子标〔待核〕）
    for m in lin['masters']:
        trows = ''
        for e in lin['trees'][m['id']]:
            dn = _esc(e['dname']) if e['dverified'] else \
                ('<span style="color:#b00">〔待核〕无 name 记录·仅见边注：%s</span>' % _esc(e['note'] or e['disc']))
            rel = '直系（师承）' if e['rel'] == 'MASTER_OF' else '私淑／影响（非直系）'
            trows += ('<tr><td>%s</td><td style="padding-left:%dem">%s → %s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                      % (e['depth'], 1 + 3 * (e['depth'] - 1), _esc(e['pname'] or e['parent']), dn,
                         rel, _esc(e['branch']), _esc(e['note'] or '')))
        fb += ('<details style="margin:6px 0"><summary>🌿 %s · 递归弟子链（直系展开·%d 节点）</summary>'
               '<table><tr><th>代</th><th>师 → 徒</th><th>传承性质</th><th>分支</th><th>依据/边注</th></tr>%s</table></details>\n'
               % (_esc(m['name']), len(lin['trees'][m['id']]), trows))

    # S3 地谱追溯卡（每要地一卡·沿革/华严事件/关联人物/信度/依据/链接 全字段）
    for t in temples_out:
        ev = '、'.join(_esc(x) for x in t['events']) or '—'
        ps = '、'.join(_esc(_lnames.get(pid) or ('〔待核〕' + str(pid))) for pid in t['persons']) or '—'
        lk = ''.join('<a href="%s" target="_blank" rel="noopener">%s</a> '
                     % (_esc(l.get('url', '')), _esc(l.get('name') or l.get('url', ''))) for l in t['links']) or '—'
        ver = '确证（堪核）' if t['verified'] == 1 else '〔待核〕传统记载'
        fb += ('<details style="margin:6px 0"><summary>⛩️ %s · %s（%s）</summary>'
               '<table>'
               '<tr><th>沿革</th><td>古称：%s ｜ 今：%s（%s）｜ 类型：%s</td></tr>'
               '<tr><th>创建/鼎盛</th><td>朝代：%s ｜ 约 %s 年 ｜ 开建：%s</td></tr>'
               '<tr><th>华严事件</th><td>%s</td></tr>'
               '<tr><th>简介</th><td>%s</td></tr>'
               '<tr><th>历史地位</th><td>%s</td></tr>'
               '<tr><th>关联人物</th><td>%s</td></tr>'
               '<tr><th>信度</th><td>%s</td></tr>'
               '<tr><th>文献依据</th><td>%s</td></tr>'
               '<tr><th>参考链接</th><td>%s</td></tr>'
               '</table></details>\n'
               % (_esc(t['name']), _esc(t['school']), _esc(t['id']),
                  _esc(t['ancient'] or t['name']), _esc(t['location']), _esc(t['dynasty'] or '—'),
                  _esc(t['type'] or '—'), _esc(t['dynasty'] or '—'), _esc(str(t['founded']) if t['founded'] is not None else '—'),
                  _esc(t['founder'] or '—'), ev, _esc(t['desc']), _esc(t['sig']), ps, ver, _esc(t['source']), lk))

    shanhe_js = read_src('shanhe.js')
    d3_js = read_src('vendor/d3.v7.min.js')  # G.0 D3 v7.9.0 UMD(MIT)·内联前置于 shanhe.js
    if 'd3' not in d3_js[:4000]:
        print('WARN vendor/d3.v7.min.js 缺失或非 UMD 构建·shanhe 页将无法用 D3 渲染')
    tmpl = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>山河法脉 · 断代山河上的法脉流传</title>
<link rel="stylesheet" href="../css/common.css">
<style>
.wrap{max-width:1200px;margin:0 auto;padding:18px 20px}
#ctl{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:10px 0}
.year-btn{border:1px solid var(--line);background:var(--card);color:var(--text);border-radius:14px;padding:4px 14px;cursor:pointer;font-size:0.85em}
.year-btn.active{background:var(--gold);color:#fff;border-color:var(--gold)}
#map-row{display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap}
#map-box{flex:3;min-width:340px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:8px}
#map-svg{width:100%;height:auto;display:block;background:#f4efe5;border-radius:8px}
#info-panel{flex:1;min-width:260px;border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:var(--card);min-height:180px;font-size:0.86em}
#info-panel h4{margin:0 0 8px;color:var(--gold)}#info-panel .yr{font-size:0.7em;color:var(--text2);font-weight:400}
#info-panel .lic{font-size:0.78em;color:var(--text2);border-top:1px dashed var(--line);padding-top:8px;margin-top:10px}
table{border-collapse:collapse;width:100%;font-size:0.78em}td,th{border:1px solid var(--line);padding:3px 7px;text-align:left}
details{font-size:0.9em}summary{cursor:pointer;color:var(--text2)}
#fallback{margin-top:20px}
#person-bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:4px 0}
#person-select{border:1px solid var(--line);background:var(--card);color:var(--text);border-radius:10px;padding:5px 10px;font-size:0.86em;max-width:260px}
.st-btn{border:1px solid var(--line);background:var(--card);color:var(--text);border-radius:10px;width:34px;height:30px;cursor:pointer;font-size:1.1em;line-height:1}
.st-btn:disabled{opacity:0.35;cursor:default}
#st-ind{font-size:0.82em;color:var(--text2);min-width:70px}
#person-hint{font-size:0.74em;color:var(--text2)}
.cite-card{border-left:3px solid var(--gold);padding:8px 10px;margin:8px 0;background:var(--panel);border-radius:0 8px 8px 0;font-size:0.9em}
.cite-card .q{color:var(--text);line-height:1.6}
.cite-card .src{font-size:0.82em;color:var(--text2);margin-top:6px}
.cite-card .pend{color:#b00;font-size:0.86em}
.cite-card .note{font-size:0.8em;color:var(--text2);margin-top:4px;font-style:italic}
#lineage-bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:4px 0}
#lineage-select{border:1px solid var(--line);background:var(--card);color:var(--text);border-radius:10px;padding:5px 10px;font-size:0.86em;max-width:280px}
#legend{display:flex;gap:8px;flex-wrap:wrap}
.lg-chip{display:inline-flex;align-items:center;gap:5px;border:1px solid var(--line);border-radius:12px;padding:2px 10px;font-size:0.78em;cursor:pointer;background:var(--card)}
.lg-chip i{width:11px;height:11px;border-radius:2px;display:inline-block}
.lg-chip.dim{opacity:0.35}
#lineage-hint{font-size:0.74em;color:var(--text2)}
#lineage-box{margin-top:6px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:8px 12px}
#lineage-svg{width:100%;height:auto;display:block;background:#f6f1e7;border-radius:8px}
.lg-edge{stroke-width:1.6;fill:none}
.lg-edge.inf{stroke-dasharray:5,3}
.lg-node.dim,.lg-edge.dim{opacity:0.15}
.lg-node text{font-size:11px;fill:#3a2f1e}
.lg-root text{font-weight:bold}
/* ══ F.5 视觉持平批 · 羊皮纸美术方向 + 交互打磨（对标 jiangshan-map·clean-room）══ */
:root{--parch:#f3ecdd;--ink:#3a2f1e;--ink2:#6b5a3a;--verm:#a83a24;--gold2:#b8863c}
body{background:
  radial-gradient(ellipse at 18% 8%, rgba(201,178,132,.16), transparent 52%),
  radial-gradient(ellipse at 84% 96%, rgba(150,128,88,.14), transparent 50%),
  repeating-linear-gradient(0deg, rgba(120,100,60,.022) 0 2px, transparent 2px 4px),
  var(--parch)}
.wrap{font-family:"Songti SC","STSong","Noto Serif CJK SC","Source Han Serif SC","SimSun",Georgia,"Times New Roman",serif;color:var(--ink)}
.wrap h1,.wrap h2,.wrap h3,.wrap h4{font-weight:600;letter-spacing:.02em}
#gs{position:relative;margin:8px 0 2px;max-width:360px}
#gs-input{width:100%;box-sizing:border-box;border:1px solid var(--line);border-radius:18px;
  padding:6px 14px 6px 30px;font:inherit;font-size:.9em;background:rgba(255,252,244,.8);color:var(--ink);
  box-shadow:inset 0 1px 2px rgba(120,100,60,.12);transition:box-shadow .2s,border-color .2s}
#gs-input:focus{outline:none;border-color:var(--gold2);box-shadow:0 0 0 3px rgba(184,134,60,.18)}
#gs-input::before{content:"🔍"}
#gs-drop{position:absolute;z-index:40;left:0;right:0;top:105%;background:#fffcf4;
  border:1px solid var(--line);border-radius:10px;box-shadow:0 8px 22px rgba(80,60,20,.22);max-height:280px;overflow:auto}
#gs-drop .it{padding:7px 13px;font-size:.85em;cursor:pointer;border-bottom:1px solid rgba(120,100,60,.12);display:flex;gap:8px;align-items:center}
#gs-drop .it:last-child{border-bottom:none}
#gs-drop .it:hover,#gs-drop .it.sel{background:rgba(184,134,60,.16)}
#gs-drop .tag{font-size:.78em;color:var(--ink2);border:1px solid var(--line);border-radius:8px;padding:0 6px;margin-left:auto}
#tl-bar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:10px 0 4px;
  background:rgba(255,252,244,.55);border:1px solid var(--line);border-radius:12px;padding:8px 14px}
.tl-cap{font-size:.8em;color:var(--ink2)}
#tl-range{flex:1;min-width:220px;height:6px;-webkit-appearance:none;appearance:none;border-radius:4px;
  background:linear-gradient(90deg,var(--gold2),var(--verm));outline:none;cursor:pointer}
#tl-range::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;
  background:var(--verm);border:2px solid #fff;box-shadow:0 1px 4px rgba(80,40,10,.4);transition:transform .12s}
#tl-range::-webkit-slider-thumb:hover{transform:scale(1.18)}
#tl-range::-moz-range-thumb{width:16px;height:16px;border-radius:50%;background:var(--verm);border:2px solid #fff;cursor:pointer}
.tl-year{font-size:1.05em;font-weight:700;color:var(--verm);min-width:52px;text-align:center}
.tl-meta{font-size:.76em;color:var(--ink2)}
#tip{position:fixed;z-index:60;pointer-events:none;background:rgba(58,47,30,.94);color:#f5eeda;
  font-size:.72em;line-height:1.5;padding:5px 9px;border-radius:7px;max-width:250px;box-shadow:0 4px 14px rgba(0,0,0,.32)}
#tip b{color:#f0c674}
/* 断代过渡动画：整层淡入 */
#g-polity{transition:opacity .45s ease}
@keyframes nodeIn{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:scale(1)}}
.lg-node circle{transform-box:fill-box;transform-origin:center;animation:nodeIn .4s ease}
.lg-edge{transition:opacity .3s}
.lg-node{transition:opacity .3s}
/* 响应式断点 */
@media(max-width:820px){#map-row{flex-direction:column}#map-box,#info-panel{flex:none;width:100%;min-width:0}
  #info-panel{min-height:120px}#gs{max-width:none}}
@media(max-width:560px){.wrap{padding:12px}h1{font-size:1.25em}#ctl,#person-bar,#lineage-bar{font-size:.86em}
  #tl-bar{gap:8px;padding:6px 10px}}
/* F.6a 法脉地理 overlay */
#g-linmap .lm-node circle{stroke:#fff;stroke-width:1.5;cursor:pointer}
#g-linmap .lm-node text{font-size:9px;fill:var(--ink);paint-order:stroke;stroke:#f3ecdd;stroke-width:2px}
#g-linmap .lm-edge{fill:none;stroke-width:1.4;stroke-opacity:.7}
#g-linmap .lm-edge.inf{stroke-dasharray:4,3}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <a href="index.html" class="back-link">&larr; 法脉传承模块</a>
    <h1>⛰️ 山河法脉 <span style="font-size:0.5em;color:var(--text2);font-weight:400">Mountains &amp; Rivers · Dharma on the Historical Map</span></h1>
    <div id="gs"><input id="gs-input" type="search" placeholder="🔍 搜祖师 / 要地 / 法师 · 按 / 聚焦" autocomplete="off"><div id="gs-drop" hidden></div></div>
  </header>
  <div id="tl-bar">
    <span class="tl-cap">时间轴</span>
    <input type="range" id="tl-range" min="__YMIN__" max="__YMAX__" step="1" value="__Y0__">
    <span id="tl-year" class="tl-year">__Y0__</span>
    <span id="tl-meta" class="tl-meta"></span>
  </div>

  <div id="ctl">
    __YEAR_BUTTONS__
    <label style="font-size:0.82em"><input type="checkbox" id="ghost-toggle"> 叠加前一时段轮廓（Ghost Diff）</label>
    <label style="font-size:0.82em"><input type="checkbox" id="place-toggle" checked> 仓内实地标点（DB locations · __N_PLACES__）</label>
    <label style="font-size:0.82em"><input type="checkbox" id="temple-toggle" checked> ⛩️ 华严要地·地谱卡（S3 · __N_TEMPLES__）</label>
    <label style="font-size:0.82em"><input type="checkbox" id="lingeo-toggle"> 🌐 法脉地理（S4 树铺底图·F.6a）</label>
    <a href="license.html" style="margin-left:auto;font-size:0.8em">层源与许可 →</a>
  </div>
  <div id="person-bar">
    <select id="person-select">__PERSON_OPTIONS__</select>
    <button class="st-btn" id="st-prev" title="上一站">‹</button>
    <button class="st-btn" id="st-next" title="下一站">›</button>
    <span id="st-ind"></span>
    <span id="person-hint">选中后：‹ › 或空格逐站推进·每站一手引文逐字回源</span>
  </div>
  <div id="lineage-bar">
    <select id="lineage-select">__LINEAGE_OPTIONS__</select>
    <span id="legend">__LEGEND__</span>
    <span id="lineage-hint">S4 择师递归展弟子链（直系＝实线／私淑·影响＝虚线）·S5 悬停图例隔离色块、点击 zoom</span>
  </div>
  <div id="map-row">
    <div id="map-box">
      <svg id="map-svg" viewBox="0 0 __CW__ __CH__" xmlns="http://www.w3.org/2000/svg">
        <g id="g-base"></g><g id="g-polity"></g><g id="g-ghost"></g><g id="g-place"></g><g id="g-person"></g><g id="g-temple"></g><g id="g-linmap" style="display:none"></g>
      </svg>

      <p style="font-size:0.72em;color:var(--text2);margin:6px 4px 2px">断代色块为<b>示意底图</b>（aourednik 百年快照·GPL-3.0 独立集合·学术精度待核）；
      唐代 700 年快照疑承旧隋界〔待核〕；CHGIS（禁再分发）仅外链：<a href="https://dataverse.harvard.edu/dataverse/chgis_v6">Harvard Dataverse</a>。</p>
    </div>
    <div id="info-panel"><h4>点击政体或标点</h4><p>政体=断代示意层（GPL·待核）；蓝点=仓内实证地名（DB 实测坐标）；⛩=华严要地（S3 地谱卡）。</p></div>
  </div>
  <div id="lineage-box">
    <h3 style="font-size:1em;margin:14px 0 4px">法脉展开 · 递归弟子树（S4/S5）</h3>
    <svg id="lineage-svg" viewBox="0 0 900 360" xmlns="http://www.w3.org/2000/svg"></svg>
    <p style="font-size:0.74em;color:var(--text2)">直系师承＝实线；私淑／隔代影响＝虚线（依客观传承·不并置同等）。〔待核〕＝person_trajectories 无 name 记录、仅见边注，不臆造。数据源 lineages.json＋complete_lineage_chart.yaml（只读投影·未改 SSOT）。</p>
  </div>
  <div id="fallback">
    <h3 style="font-size:1em">静态兜底 · 全字段无损在场（信息無损惯例）</h3>
    __FALLBACK__
  </div>
</div>
<div id="tip" hidden></div>
<script>var SHANHE = __DATA_JSON__;</script>
<script>__D3_JS__</script>
<script>__SHANHE_JS__</script>
</body>
</html>'''
    html = (tmpl.replace('__YEAR_BUTTONS__', year_buttons)
                .replace('__YMIN__', str(_ymin)).replace('__YMAX__', str(_ymax)).replace('__Y0__', str(_y0))
                .replace('__N_PLACES__', str(len(places)))
                .replace('__N_TEMPLES__', str(len(temples_out)))
                .replace('__PERSON_OPTIONS__', person_options)
                .replace('__LINEAGE_OPTIONS__', lineage_options)
                .replace('__LEGEND__', legend_chips)
                .replace('__CW__', str(GEO_CW)).replace('__CH__', str(GEO_CH))
                .replace('__FALLBACK__', fb)
                .replace('__DATA_JSON__', data_json)
                .replace('__D3_JS__', d3_js)
                .replace('__SHANHE_JS__', shanhe_js))
    famai_dir = OUT / 'famai'
    famai_dir.mkdir(exist_ok=True)
    path = famai_dir / 'shanhe.html'
    path.write_text(html, encoding='utf-8')
    size = len(html.encode('utf-8'))
    npoly = sum(len(yy['polities']) for yy in years_out)
    nstn = sum(len(p['stations']) for p in persons_out)
    nedge = sum(len(v) for v in lin['trees'].values())
    print('OK  %s (%s bytes | %d 年·%d 政体·%d 标点·%d 祖师/%d 站·要地 %d·法脉 %d 师/%d 边/%d 支·网络 %d 点/%d 边/%d 支·coast %d/countries %d)' % (
        path, format(size, ','), len(years_out), npoly, len(places),
        len(persons_out), nstn, len(temples_out), len(lin['masters']), nedge, len(lin['branches']),
        len(net['nodes']), len(net['links']), len(net['branches']),
        len(coast), len(countries)))
    return size


def build_famai_license_page():
    """famai/license.html — 数据层许可声明页（由 data/geo/manifest.yaml 生成·可复核）。"""
    man = read_yaml('geo/manifest.yaml')
    if not man:
        print('WARN data/geo/manifest.yaml missing - skip license page')
        return 0
    rows = ''
    for e in man.get('layers', []):
        rows += ('<tr><td>{}</td><td><a href="{}">{}</a></td><td>{}</td><td>{}</td>'
                 '<td>{}</td><td>{}</td></tr>').format(
            e.get('file', ''), e.get('url', ''), e.get('url', '').split('/')[2],
            e.get('license', ''), e.get('accessed', ''), format(e.get('bytes', 0), ','),
            str(e.get('sha256', ''))[:16])
    html = '''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>层源与许可 · 法脉传承模块</title><link rel="stylesheet" href="../css/common.css">
<style>body{max-width:1000px;margin:0 auto;padding:26px 22px}
table{border-collapse:collapse;width:100%;font-size:0.8em}td,th{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
.note{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 18px;font-size:0.88em;margin:16px 0}</style></head>
<body>
<a href="index.html">&larr; 法脉传承模块</a>
<h1>层源与许可声明 · Provenance &amp; Licenses</h1>
<p class="note"><b>非商用声明</b>：本项目为人文书读与数字人文研究用途，非商业。各数据层按上游许可分层管理：
<a href="https://github.com/aourednik/historical-basemaps">aourednik/historical-basemaps</a> = <b>GPL-3.0</b>（作独立数据集合入库·其 LICENSE 全文随仓
<code>data/geo/historical-basemaps/LICENSE</code>·不与本仓 MIT 代码组件混许可）；
<a href="https://www.naturalearthdata.com/">Natural Earth</a> = <b>Public Domain</b>（无需许可）；
<a href="https://chgis.fas.harvard.edu/data/chgis/v6/">CHGIS V6</a> 官方许可「free for academic research, no commercial use, resale, or
<b>redistribution</b> permitted」——故其原始数据<b>不入库、不分发</b>，仅作外链引用；
<a href="https://www.openhistoricalmap.org/">OpenHistoricalMap</a> = ODbL（覆盖评估中·暂未接入）。
<b>代码依赖</b>：<a href="https://github.com/d3/d3">D3.js v7.9.0</a>（<b>ISC 许可</b>·本地 vendor <code>web/demo/src/vendor/d3.v7.min.js</code>·内联前置于页面脚本·无 CDN/离线可用）——仅用于法脉可视化，与本仓内容数据层无关。
若未来商业化，须先移除/替换 GPL 层并重审全部上游条款。断代几何为<b>示意底图</b>，学术精度逐项待核。</p>
<table><tr><th>文件</th><th>来源域</th><th>许可</th><th>访问日期</th><th>字节</th><th>sha256 前16</th></tr>
__ROWS__</table>
<p style="font-size:0.75em;color:var(--text2)">溯源 SSOT：<code>data/geo/manifest.yaml</code>（受控下载器 <code>scripts/f2_fetch_geo.py</code> 生成·幂等可复核）·本批裁定见 <code>.harness/decisions.md</code> #12</p>
</body></html>'''.replace('__ROWS__', rows)
    path = OUT / 'famai' / 'license.html'
    path.write_text(html, encoding='utf-8')
    size = len(html.encode('utf-8'))
    print('OK  %s (%s bytes | %d layers declared)' % (path, format(size, ','), len(man.get('layers', []))))
    return size


def build_lineage_page():
    """Build Tab1: 法脉传承 (standalone, Canvas+Leaflet, layout preserved)."""
    graph = load_graph()
    events = load_events()
    bib = load_bibliography()
    glossary = load_glossary()
    graph_json = json.dumps(graph, ensure_ascii=False)

    # Build data.js content
    data_js_content = f'''
var GRAPH = {graph_json};
var DATA = GRAPH;
var BIBLIOGRAPHY = {json.dumps(bib, ensure_ascii=False)};
var BILINGUAL_GLOSSARY = {json.dumps(glossary, ensure_ascii=False)};
var nodeMap = {{}};
if(DATA && DATA.nodes) DATA.nodes.forEach(function(n){{nodeMap[n.id]=n;}});
var GAP = {{}};
var HEART_ARTICLES = [];
var selectedId = null, selectedId2 = null, hoveredId = null, searchQuery = "";
var map = null, mapMain = null;
var tl = {{canvas:null, ctx:null, W:0, H:0, ox:0, oy:0, scale:1,
         minX:100, maxX:2060, rows:[], hitRects:[],
         drag:false, lastX:0}};
'''

    lineage_js = read_src('lineage.js')
    init_js = read_src('init.js')
    # Protect other-tab render calls -- they don't exist in standalone lineage page
    init_js = init_js.replace('renderGap();', 'try{renderGap();}catch(e){}')
    init_js = init_js.replace('renderPractice();', 'try{renderPractice();}catch(e){}')
    init_js = init_js.replace('renderFrontier();', 'try{renderFrontier();}catch(e){}')

    # Inject events data as JS globals
    events_js = ''
    for name, data in events.items():
        events_js += f'var {name.upper()} = {json.dumps(data, ensure_ascii=False)};\n'
    # Also inject temple directory
    temple_data = read_yaml('locations/temple_directory.yaml')
    if temple_data:
        events_js += f'var TEMPLE_DIRECTORY = {json.dumps(temple_data, ensure_ascii=False)};\n'

    # Build clean standalone page
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<title>华严宗 · 法脉传承</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<link rel="stylesheet" href="../css/common.css">
<style>
#search-bar{{display:flex;gap:6px;padding:6px 12px;background:var(--panel);border-bottom:1px solid var(--line);align-items:center;position:relative}}
#search-bar input{{border:1px solid var(--line);border-radius:14px;padding:5px 12px;font-size:0.8em;background:var(--card);color:var(--text);width:220px;outline:none}}
#main-row{{display:flex;flex:1;min-height:65vh}}
#tl-panel{{flex:1;position:relative;background:var(--panel);overflow-y:auto;overflow-x:hidden;min-width:220px;cursor:grab}}
#tl-panel canvas{{display:block;position:absolute;top:0;left:0}}
#side{{flex:3;display:flex;flex-direction:column;min-width:300px;border-left:1px solid var(--line)}}
#map-main-wrap{{position:relative;overflow:hidden;flex:1;min-height:50vh}}
#map-main{{width:100%;height:100%}}
#info-popup{{position:fixed;z-index:999;background:rgba(254,253,249,0.88);backdrop-filter:blur(4px);border:1px solid rgba(184,134,60,0.5);border-radius:10px;padding:8px 12px;font-size:0.72em;max-width:280px;max-height:45vh;overflow-y:auto;color:var(--text);box-shadow:0 4px 16px rgba(60,40,20,0.12);display:none}}
.anim-popup .leaflet-popup-content-wrapper{{background:rgba(254,253,249,0.85)!important;backdrop-filter:blur(3px);border-radius:8px;box-shadow:0 2px 8px rgba(60,40,20,0.1);padding:6px 10px}}
.anim-popup .leaflet-popup-content{{margin:0;font-size:0.7em;line-height:1.4;max-width:200px}}
.anim-popup .leaflet-popup-tip{{background:rgba(254,253,249,0.85)!important}}
#info-popup h3{{color:var(--gold);font-size:0.92em;margin-bottom:3px}}
#info-popup .close-btn{{position:absolute;top:2px;right:6px;cursor:pointer;color:var(--text2);font-size:0.95em}}
#controls{{background:var(--panel);padding:6px 12px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;border-top:1px solid var(--line)}}
#controls button{{padding:4px 12px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.73em;transition:all 0.2s}}
#controls button:hover{{background:#f0ebe0;color:var(--text);border-color:var(--gold)}}
#controls button.active{{background:var(--gold);color:#fff;border-color:var(--gold)}}
#tl-tooltip{{position:absolute;background:var(--card);color:var(--text);padding:10px 14px;border-radius:8px;font-size:0.82em;pointer-events:none;opacity:0;transition:opacity 0.15s;max-width:300px;z-index:100;box-shadow:0 4px 14px rgba(60,40,20,0.14);border:1px solid var(--line)}}
#tl-tooltip h3{{color:var(--gold);margin-bottom:3px}}
#resize-handle{{width:5px;cursor:col-resize;background:var(--line);transition:background 0.2s;flex-shrink:0}}#resize-handle:hover,#resize-handle.active{{background:var(--gold)}}
.map-ancient .leaflet-tile-pane{{filter:sepia(0.7) hue-rotate(-15deg) saturate(0.4) brightness(0.85) contrast(1.1)}}
.filter-parchment .leaflet-tile-pane{{filter:sepia(0.7) saturate(0.45) brightness(0.9) contrast(1.05)}}
.filter-silver .leaflet-tile-pane{{filter:grayscale(0.9) contrast(1.15) brightness(0.95)}}
.filter-indigo .leaflet-tile-pane{{filter:hue-rotate(-30deg) saturate(0.55) brightness(0.95) contrast(1.05)}}
.filter-amber .leaflet-tile-pane{{filter:sepia(0.5) saturate(0.9) contrast(1.1) brightness(1.0) hue-rotate(-5deg)}}
.filter-twilight .leaflet-tile-pane{{filter:grayscale(0.15) brightness(0.72) contrast(1.12) saturate(0.45)}}
#map-vignette{{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:600;background:radial-gradient(ellipse at center,transparent 62%,rgba(40,24,10,0.22) 100%);border-radius:inherit}}
.filter-btn-active{{background:var(--gold)!important;color:#fff!important;border-color:var(--gold)!important}}
@media(max-width:768px){{
  body{{overflow:auto;height:auto}}
  #header{{position:sticky;padding:6px 10px}}
  #header h1{{font-size:0.85em}}
  #search-bar{{flex-wrap:wrap;gap:3px;padding:4px 6px}}
  #search-bar input{{width:120px;font-size:0.7em;padding:3px 8px}}
  #main-row{{flex:none;flex-direction:column}}
  #tl-panel{{height:300px;flex:none;touch-action:pan-x}}
  #side{{width:100%!important;height:350px;flex:none;min-width:0!important}}
  #resize-handle{{display:none}}
  #controls{{flex-wrap:wrap;gap:2px;padding:4px 5px}}
  #controls button{{padding:3px 6px;font-size:0.6em;border-radius:8px}}
  #info-popup{{position:fixed;max-width:90vw;max-height:35vh;font-size:0.68em;left:5vw!important;top:8vh!important;background:rgba(254,253,249,0.85)}}
}}
</style>
</head>
<body>
<div id="page-top" style="position:sticky;top:0;z-index:100">
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>🌊 法脉传承 · 时空长河</h1>
  <button id="lang-toggle" class="lang-btn" style="margin-left:auto" onclick="toggleSiteLang();return false" title="阅读语言：中英对照 ⇄ 仅中文">🌐 中·EN</button>
</header>
<div style="background:rgba(196,107,93,0.08);border-bottom:1px solid rgba(196,107,93,0.25);padding:6px 16px;font-size:0.72em;color:var(--red);text-align:center">
⚠️ 声明：本页面内容尚处于初始梳理阶段，在完整性、准确度、详实度、深度等方面均有不足，仅供参考；敬请多提建议，以助完善内容。
</div>
</div>

<div id="search-bar">
  <input type="text" id="search-input" placeholder="🔍 检索人物、地点…" autocomplete="off">
<div id="search-suggest" style="position:absolute;top:100%;left:0;z-index:1000;background:rgba(254,253,249,0.95);border:1px solid var(--line);border-radius:0 0 8px 8px;max-height:180px;overflow-y:auto;display:none;width:260px;box-shadow:0 4px 12px rgba(0,0,0,0.1)"></div>
  <span id="anim-status" style="flex:1;font-size:0.7em;color:var(--gold);margin:0 8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;opacity:0;transition:opacity 0.3s"></span>
  <span id="stats-bar" style="font-size:0.68em;color:var(--text2);margin-left:auto"></span>
</div>

<div id="main-row">
  <div id="tl-panel"><canvas id="tl-canvas"></canvas><div id="tl-tooltip"></div></div>
  <div id="resize-handle" title="拖拽调节地图宽度"></div>
  <div id="side">
    <div id="map-main-wrap">
      <div id="map-main"></div>
	      <div id="map-vignette"></div>
      <div id="route-info" style="display:none;position:absolute;bottom:8px;left:8px;right:8px;background:rgba(254,253,249,0.9);border:1px solid var(--line);border-radius:6px;padding:6px 10px;font-size:0.68em;color:var(--text2);z-index:500;line-height:1.5">
        🪷 <span style=color:#c46b5d>佛教·华严</span> <span style=color:#e08040>南亚</span> <span style=color:#b8863c>儒家</span> <span style=color:#7d9a6e>道家</span> <span style=color:#5e8b9e>西方</span> <span style=color:#4a9e8e>伊斯兰</span> <span style=color:#c8893e>非洲</span> <span style=color:#d48476>美洲</span> <span style=color:#8b7a9e>大洋洲</span> — 彩色路线代表全球文明传统的传播与交融
      </div>
    </div>
  </div>
</div>

<div id="info-popup"><span class="close-btn" onclick="document.getElementById('info-popup').style.display='none'">&times;</span><div id="info-popup-content"></div></div>

<div id="progress-bar" style="background:var(--panel);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:2px 12px;display:flex;align-items:center;gap:6px">
  <button onclick="animJump(-1)" style="padding:0 4px;font-size:0.7em;border:1px solid var(--line);border-radius:8px;background:var(--card);cursor:pointer">◀</button>
  <span id="prog-year" style="font-size:0.65em;color:var(--gold);min-width:45px;text-align:center">-600年</span>
  <input type="range" id="anim-progress" min="-1500" max="2030" value="-600" step="5" style="flex:1;accent-color:var(--gold);height:8px">
  <button onclick="animJump(1)" style="padding:0 4px;font-size:0.7em;border:1px solid var(--line);border-radius:8px;background:var(--card);cursor:pointer">▶</button>
</div>

<div id="controls">
  <span style="font-size:0.7em;color:var(--text2)">法系:</span>
  <button class="active" data-filter="all">全部</button>
  <button data-filter="华严五祖">五祖</button>
  <button data-filter="贤首宗高原法系">高原法系</button>
  <button data-filter="华严莲社">华严莲社</button>
  <button data-filter="月霞系">月霞系</button>
  <span style="font-size:0.7em;color:var(--text2);margin-left:8px">书签:</span>
  <button data-bookmark="557,841">五祖时代</button>
  <button data-bookmark="1000,1120">高丽传入</button>
  <button data-bookmark="1850,2026">近现代</button>
  <span style="font-size:0.7em;color:var(--text2);margin-left:8px">图层:</span>
  <button class="active" data-layer="theory" onclick="toggleLayer('theory')">理</button>
  <button class="active" data-layer="practice" onclick="toggleLayer('practice')">修</button>
  <button class="active" data-layer="geo" onclick="toggleLayer('geo')">地</button>
  <button class="active" data-layer="edges" onclick="toggleLayer('edges')">传</button>
  <button class="active" data-layer="events" onclick="toggleLayer('events')">事</button>
  <span style="font-size:0.7em;color:var(--text2);margin-left:8px">底图:</span>
  <button id="basemap-btn" onclick="cycleBasemap()" title="切换底图: 现代/卫星/地形">🗺 现代</button>
  <button id="ancient-btn" onclick="toggleAncient()">🏯 古今</button>
  <button id="filter-btn" onclick="cycleFilter()" style="border:1px solid var(--blue);color:var(--blue);font-size:0.73em" title="循环切换地图滤镜预设">🎨 无</button>
  <span id="speed-row" style="font-size:0.7em;color:var(--text2)">⏱<input type="range" id="anim-speed" min="5" max="40" value="35" step="1"><span id="speed-label">1×</span></span>
  <button id="roster-btn" style="border:1px solid var(--green);color:var(--green);font-size:0.75em" onclick="toggleRoster()">📋 名录</button>
  <button id="temple-btn" style="border:1px solid var(--gold);color:var(--gold);font-size:0.75em" onclick="toggleTempleDir()">🏛 道场</button>
  <button id="route-info-btn" style="border:1px solid var(--blue);color:var(--blue);font-size:0.75em" onclick="toggleRouteInfo()">ℹ️ 路线</button>
  <button id="anim-btn" style="border:1px solid var(--green);color:var(--green);font-weight:600;font-size:0.8em;padding:4px 16px" onclick="toggleAnim()">▶ 播放</button>
  <button id="anim-stop-btn" style="border:1px solid var(--red);color:var(--red);font-weight:600;font-size:0.8em;padding:4px 12px;display:none" onclick="stopAnim()">⏹</button>
  <span id="route-legend" style="margin-left:auto;font-size:0.60em;color:var(--text2);line-height:1.4;opacity:0.75">
    🪷 <span style=color:#c46b5d>佛教</span> <span style=color:#e08040>南亚</span> <span style=color:#b8863c>儒家</span> <span style=color:#7d9a6e>道家</span> <span style=color:#5e8b9e>西方</span> <span style=color:#4a9e8e>伊斯兰</span> <span style=color:#c8893e>非洲</span> <span style=color:#d48476>美洲</span> <span style=color:#8b7a9e>大洋洲</span>
  </span>
  <button id="reset-btn" style="border:1px solid var(--gold);color:var(--gold)">↺ 重置</button>
</div>

<div id="roster-modal" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;z-index:2000;background:rgba(0,0,0,0.3);justify-content:center;align-items:center">
<div style="background:var(--card);border-radius:12px;padding:16px;max-width:700px;max-height:75vh;overflow-y:auto;width:90vw;box-shadow:0 8px 40px rgba(0,0,0,0.2)">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
<h3 style="color:var(--gold);font-size:1em">📋 人物名录 (共<span id=roster-count></span>位)</h3>
<button onclick="document.getElementById('roster-modal').style.display='none'" style="border:none;background:none;font-size:1.2em;cursor:pointer;color:var(--text2)">&times;</button>
</div>
<div id="roster-content"></div></div></div>

<div id="mini-maps-grid" style="display:flex;gap:6px;margin:6px 14px;height:110px;flex-shrink:0;overflow-x:auto"></div>

<div class="comment-box" id="cmt-lineage"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="../js/common.js"></script>
<script>
{data_js_content}
{events_js}
</script>
<script>
{wrap_script(lineage_js)}
</script>
<script>
{wrap_script(init_js)}
</script>
</body>
</html>'''

    html = html.replace('华严行法', '华严教行')
    return html


def build_simple_tab_page(title, tab_id, sidebar_html, render_call, view_id=None, articles=None):
    """Build a tab page with sidebar layout using existing JS rendering."""
    if articles is None:
        articles = []
    if view_id is None:
        view_id = f'{tab_id}-view'
    graph = load_graph()
    gap = load_gap()
    events = load_events()
    cosmo = load_cosmology()
    practice = load_practice()
    frontier = load_frontier()

    # Load heart articles
    import glob as _g2, re as _re2
    heart_articles = []
    wechat_dir2 = ROOT / 'docs' / 'hy_refs' / 'wechat'
    if wechat_dir2.exists():
        for fpath in sorted(_g2.glob(str(wechat_dir2 / '*.md'))):
            with open(fpath, 'r', encoding='utf-8') as f:
                text = f.read()
            ht_m = _re2.search(r'^# (.+)$', text, _re2.MULTILINE)
            ht_title = ht_m.group(1).strip() if ht_m else os.path.basename(fpath)
            body = _re2.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=_re2.MULTILINE|_re2.DOTALL, count=1)
            for meta in ['来源','摘要','原文','下一篇','提取日期']:
                body = _re2.sub(r'^\*\*'+meta+r'[:：].*$', '', body, flags=_re2.MULTILINE)
            body = _re2.sub(r'^# .+$', '', body, 1, flags=_re2.MULTILINE)
            body = _re2.sub(r'^\s*---\s*$', '', body, flags=_re2.MULTILINE).strip()
            body = _re2.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'''<div class='himg'><img src='\2' alt='\1' onclick='window.open(this.src)'></div>''', body)
            body = _re2.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', body)
            body = _re2.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', body)
            paras = [p.strip() for p in body.split('\n\n') if p.strip()]
            body = ''
            for p in paras:
                if p.startswith('<div class='): body += p + '\n'
                elif len(p)<80 and not p.startswith('<') and p.count('\n')==0: body += '<h4>'+p+'</h4>\n'
                else: body += '<p>'+p.replace('\n','<br>')+'</p>\n'
            wx_url = ''
            url_m = _re2.search(r'原文[:：]\*{0,2}\s*(https?://[^\s\n]+)', text)
            if url_m: wx_url = url_m.group(1)
            heart_articles.append({'title': ht_title, 'body': body.strip(), 'url': wx_url})

    haiyun_res = read_yaml('practice/haiyun_resources.yaml') or {}
    spirit = load_spirit()
    bib = load_bibliography()
    glossary = load_glossary()

    # Build inline data script
    articles_lite = [{'id': a['id'], 'title': a.get('title', a['id']), 'file': a['file'],
                      'icon': a.get('icon', '📄'), 'views': a.get('views', [])} for a in articles]
    data_script = f'''
var HAIYUN_RESOURCES = {json.dumps(haiyun_res, ensure_ascii=False)};
var GRAPH = {json.dumps(graph, ensure_ascii=False)};
var GAP = {json.dumps(gap, ensure_ascii=False)};
var EVENTS = {json.dumps(events, ensure_ascii=False)};
var COSMO_DATA = {json.dumps(cosmo, ensure_ascii=False)};
var PRACTICE_DATA = {json.dumps(practice, ensure_ascii=False)};
var FRONTIER_DATA = {json.dumps(frontier, ensure_ascii=False)};
var SPIRIT_DATA = {json.dumps(spirit, ensure_ascii=False)};
var BIBLIOGRAPHY = {json.dumps(bib, ensure_ascii=False)};
var BILINGUAL_GLOSSARY = {json.dumps(glossary, ensure_ascii=False)};
var HEART_ARTICLES = {json.dumps(heart_articles, ensure_ascii=False)};
var ARTICLES = {json.dumps(articles_lite, ensure_ascii=False)};
var DATA = GRAPH;
var nodeMap = {{}};
if(DATA && DATA.nodes) DATA.nodes.forEach(function(n){{nodeMap[n.id]=n;}});
'''

    html = f'''<!DOCTYPE html>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>华严宗 · {title}</title>
<link rel="stylesheet" href="../css/common.css">
</head>
<body>
<div id="page-top" style="position:sticky;top:0;z-index:100">
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>{title}</h1>
  <button id="lang-toggle" class="lang-btn" onclick="toggleSiteLang();return false" title="阅读语言：中英对照 ⇄ 仅中文">🌐 中·EN</button>
  <a href="#" onclick="heartLogin();return false" style="margin-left:auto;font-size:0.7em;color:var(--text2);text-decoration:none" title="配置GitHub Token">🔑 登录</a>
</header>
<div style="background:rgba(196,107,93,0.08);border-bottom:1px solid rgba(196,107,93,0.25);padding:6px 16px;font-size:0.72em;color:var(--red);text-align:center">
⚠️ 声明：本页面内容尚处于初始梳理阶段，在完整性、准确度、详实度、深度等方面均有不足，仅供参考；敬请多提建议，以助完善内容。
</div>
</div>
<div class="layout">
  <nav class="sidebar" id="sidebar">
    {sidebar_html}
  </nav>
  <main class="content" id="content">
    <div id="{view_id}"></div>
  </main>
</div>
<div class="comment-box" id="cmt-{tab_id}"></div>
<button class="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="回到顶部">&uarr;</button>

<script src="../js/common.js"></script>
<script>
{data_script}
</script>
<script>
{wrap_script(read_src(tab_id + '.js') if tab_id != 'jiaoxing' else read_src('practice.js'))}
</script>
<script>
(function(){{
  try{{ {render_call} }}catch(e){{console.error(e);}}
  try{{ renderComments('{tab_id}'); }}catch(e){{console.error(e);}}
}})();
</script>
</body>
</html>'''

    # Rename practice->jiaoxing in display text only (NOT function names)
    html = html.replace('华严行法', '华严教行')
    # Keep renderPractice/switchPracticeView/pv-nav function names intact
    # since practice.js defines them

    return html


def load_standalone_articles():
    """Expand the standalone-articles registry (data/translation/standalone_articles.yaml)
    into the full article catalog. Each entry: {id, file, title, title_sub, icon, version,
    meta, doc, doc_md, back:{tab,view,label}, views:[...]}.

    Sources:
      - topic_studies   → every 专题研究 article (id = article id)
      - huayan_masters  → every master carrying a review_doc (id = master-<id>)
      - others          → explicit full-document articles registered in the YAML
    """
    reg = read_yaml('translation/standalone_articles.yaml') or {}
    articles = []

    # ① 专题研究 (data/translation/topic_studies.yaml)
    ts = read_yaml('translation/topic_studies.yaml') or {}
    for art in ts.get('articles', []):
        if not art.get('id'):
            continue
        # 默认返回文献页·专题研究，并在 gap 侧栏挂入口；
        # 允许 YAML 通过 `views` 追加其他选项卡目录入口（如前沿对话某域），
        # 通过 `back` 覆盖返回链接——默认视图恒保留，不因此丢失文献页入口。
        ts_views = ['topic-' + art['id']]
        for v in (art.get('views') or []):
            if v not in ts_views:
                ts_views.append(v)
        ts_back = art.get('back') or {
            'tab': 'gap', 'view': 'topic-' + art['id'], 'label': '华严文献 · 专题研究'}
        articles.append({
            'id': art['id'],
            'file': 'articles/%s.html' % art['id'],
            'title': art.get('title', art['id']),
            'title_sub': art.get('title_sub', ''),
            'icon': art.get('icon', '📌'),
            'group': art.get('group', ''),
            'family': art.get('family', ''),
            'order_in_group': art.get('order_in_group'),
            'version': art.get('version', ''),
            'meta': art.get('meta', ''),
            'doc': art.get('doc', ''),
            'updated_at': art.get('updated_at', ''),
            'back': ts_back,
            'views': ts_views,
        })

    # ② 华严祖师 (data/translation/huayan_masters.yaml — 含 review_doc 者)
    hm = read_yaml('translation/huayan_masters.yaml') or {}
    for m in hm.get('masters', []):
        if not m.get('review_doc') or not m.get('id'):
            continue
        articles.append({
            'id': 'master-' + m['id'],
            'file': 'articles/master-%s.html' % m['id'],
            'title': m.get('name', m['id']),
            'title_sub': ('华严祖师 · ' + m['role']) if m.get('role') else '华严祖师',
            'icon': '🧑',
            'group': m.get('group', ''),
            'family': 'masters',
            'order_in_group': m.get('order_in_group'),
            'version': '',
            'meta': '',
            'doc': m['review_doc'],
            'back': {'tab': 'gap', 'view': 'master-' + m['id'], 'label': '华严文献 · 华严祖师'},
            'views': ['master-' + m['id']],
        })

    # ③ 其他整篇文档（各 Tab 由完整 docs/*.md 支撑的专题/子tab）
    for o in reg.get('others', []):
        if not o.get('id'):
            continue
        articles.append({
            'id': o['id'],
            'file': 'articles/%s.html' % o['id'],
            'title': o.get('title', o['id']),
            'title_sub': o.get('title_sub', ''),
            'icon': o.get('icon', '📄'),
            'group': o.get('group', ''),
            'family': o.get('family', ''),
            'order_in_group': o.get('order_in_group'),
            'version': o.get('version', ''),
            'meta': o.get('meta', ''),
            'doc': o.get('doc', ''),
            # 数据驱动独立页：指向 PRACTICE_DATA（默认）或 GAP（data_pool: gap）内的数据源键
            # （如 chan_authentic_traces / avatamsaka_studies / panjiao_hupan），
            # 由 build_articles 内嵌完整数据 + 自包含渲染脚本生成，正文单源存于 YAML
            'data_source': o.get('data_source', ''),
            'data_pool': o.get('data_pool', 'practice'),
            # skip_html: true → 该 id 的 HTML 由项目内其他专项脚本生成（如 jj-huayan-collation
            # 由 scripts/build_jj_collation_page.py 生成），build.py 只登记 index 卡片入口，
            # 不再重复生成同名 .html，避免两个来源互相覆盖。
            'skip_html': bool(o.get('skip_html', False)),
            # 内容最后更新时间：仅登记「内容实质变更」之日，未登记则页头不显时间带
            #（不得以构建时间冒充内容更新时间——二者性质不同）。
            'updated_at': o.get('updated_at', ''),
            'back': o.get('back') or {},
            'views': o.get('views', [o['id']]),
        })

    # Load full markdown for every article
    for a in articles:
        a['doc_md'] = ''
        if a.get('doc'):
            dp = ROOT / a['doc']
            if dp.exists():
                with open(dp, encoding='utf-8') as f:
                    a['doc_md'] = f.read()
            else:
                print(f'  ! standalone article {a["id"]}: doc not found: {a["doc"]}')
    return articles


# 数据驱动独立页的渲染脚本：与 practice.js 中 renderChanTraces() 同构的演示层代码
# （纯展示逻辑，正文一律来自 YAML 的 chan_authentic_traces，实现「单源数据」）。此处为
# 脚本常量 + 页面内联调用；如需同步更新，仅改此处与 practice.js 两处（二者皆为生成产出源）。
CHAN_TRACES_RENDER = r'''function renderChanTraces() {
  var ct = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.chan_authentic_traces) ? PRACTICE_DATA.chan_authentic_traces : null;
  if (!ct || !ct.sections) return '';
  function md(s) {
    return String(s||'')
      .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
      .replace(/(^|[^*])\*([^*]+?)\*(?!\*)/g, '$1<i>$2</i>');
  }
  var h = '';
  ct.sections.forEach(function(sec) {
    h += '<div class=section id=chan-' + sec.id.replace('chan_','') + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title;
    if (sec.title_en) h += '<span class="en-line" style="font-size:0.62em;display:block;color:var(--text2);margin-top:2px">' + sec.title_en + '</span>';
    h += '</h2>';
    if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + md(sec.intro) + '</p>';
    if (sec.intro_en) h += '<p class="en-line" style="white-space:pre-line;font-size:0.78em;color:var(--text2);line-height:1.8"><span style="color:var(--gold);font-weight:600">📖 </span>' + sec.intro_en + '</p>';
    if (sec.topics) {
      sec.topics.forEach(function(t, idx) {
        h += '<div class="wu-door" id=ct-' + sec.id + '-' + idx + ' onclick="this.classList.toggle(\'open\')">';
        h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
        if (t.title_en) h += '<div class="en-line" style="font-size:0.62em;color:var(--text2);margin-left:18px;margin-bottom:4px">' + t.title_en + '</div>';
        h += '<div class=body>';
        h += '<p style=font-size:0.8em;line-height:1.8;white-space:pre-line>' + md(t.body) + '</p>';
        if (t.en_body) h += '<div class="en-line" style="white-space:pre-line;font-size:0.82em;color:var(--text2);border-top:1px dashed var(--line);margin-top:6px;padding-top:6px"><span style="color:var(--gold);font-weight:600">📖 </span>' + md(t.en_body) + '</div>';
        if (t.links) {
          Object.keys(t.links).forEach(function(k) {
            h += '<a href="' + t.links[k] + '" target=_blank style="font-size:0.72em;color:var(--blue)">🔗 ' + k + '</a> ';
          });
        }
        if (t.source) h += '<p style=font-size:0.68em;color:var(--text2);margin-top:4px">📎 ' + md(t.source) + '</p>';
        h += '</div></div>';
      });
    }
    h += '</div>';
  });
  if (ct.references) {
    h += '<details style=font-size:0.72em;margin-top:8px><summary>📚 参考文献（分级 · 🔗 可回查）</summary>'
       + (window.renderRefList ? renderRefList(ct.references) : '') + '</details>';
  }
  h += '<div class=section id=chan-diagrams><h2>📊 禅宗法脉传承</h2>';
  h += '<table class=v-table style=font-size:0.75em><tr><th>时期</th><th>人物</th><th>贡献</th></tr>';
  h += '<tr><td>印度</td><td>佛陀二十八代→菩提达摩</td><td>灵山拈花·教外别传</td></tr>';
  h += '<tr><td>隋</td><td>慧可→僧璨→道信→弘忍</td><td>二祖至五祖·东山法门</td></tr>';
  h += '<tr><td>唐</td><td>神秀(北宗) 慧能(南宗)</td><td>南北分宗</td></tr>';
  h += '<tr><td>晚唐五代</td><td>马祖·石头→临济·曹洞·沩仰·云门·法眼</td><td>五家七宗</td></tr>';
  h += '<tr><td>宋</td><td>大慧宗杲(看话) 宏智正觉(默照)</td><td>两大法门</td></tr>';
  h += '<tr><td>明清</td><td>永明延寿→云栖袾宏→蕅益智旭</td><td>禅净合流</td></tr>';
  h += '<tr><td>近现代</td><td>虚云(兼祧五宗) 来果 铃木大拙</td><td>传统坚守·西传</td></tr>';
  h += '<tr><td>当代</td><td>净慧(生活禅) 圣严 一行禅师</td><td>现代体系化</td></tr>';
  h += '</table></div>';
  return h;
}
'''

# ═══ 海云法师讲法全库渲染脚本 ═══
# 供独立页 articles/haiyun-lectures.html 使用（practice 池, data_source=haiyun_wiz_catalog）。
# 与 practice.js 中 renderWizLibrary() 同构的演示层代码；正文一律按需加载 docs/huayanhai/<cat>/<title>.txt。
# 数据来自 data/practice/haiyun_wiz_catalog.yaml（由 wiz 导出清单 export_manifest.json 数据驱动生成，无虚构条目）。
# 如需同步更新，仅改此处与 practice.js 两处（二者皆为生成产出源）。
WIZ_LIB_RENDER = r'''function esc(s){ return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function fmtChars(n){ n = Number(n) || 0; if (n >= 1e8) return (n / 1e8).toFixed(2) + ' 亿字'; if (n >= 1e4) return (n / 1e4).toFixed(1) + ' 万字'; if (n >= 1e3) return (n / 1e3).toFixed(1) + ' 千字'; return n + ' 字'; }
function fmtBytes(n){ n = Number(n) || 0; if (n >= 1e6) return (n / 1e6).toFixed(1) + ' MB'; if (n >= 1e3) return (n / 1e3).toFixed(0) + ' KB'; return n + ' B'; }
function fmtDate(ms){ if (!ms) return ''; var d = new Date(ms), p = function(x){ return (x < 10 ? '0' : '') + x; }; return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()); }
function renderWizLibrary() {
  var cat = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.haiyun_wiz_catalog) ? PRACTICE_DATA.haiyun_wiz_catalog : null;
  if (!cat || !cat.notes || !cat.notes.length) return '';
  var WIZ_BASE = '../../../docs/huayanhai';
  function buildTree(notes){
    var root = {name: '', children: {}, notes: []};
    notes.forEach(function(n){
      var cats = String(n.cat || '未分类').split('/').filter(function(c){ return c && c.trim(); });
      var node = root;
      cats.forEach(function(c){ if (!node.children[c]) node.children[c] = {name: c, children: {}, notes: []}; node = node.children[c]; });
      node.notes.push(n);
    });
    return root;
  }
  window.wzTree = buildTree(cat.notes);
  window.wzAll = cat.notes;
  window.wzNotes = {};
  cat.notes.forEach(function(n){ window.wzNotes[n.guid] = n; });
  function wzFolderCount(node){ var c = node.notes.length; Object.keys(node.children).forEach(function(k){ c += wzFolderCount(node.children[k]); }); return c; }
  function wzTreeHTML(node, dep){
    var keys = Object.keys(node.children), h = '';
    if (dep > 0) {
      h += '<div class="wz-folder" onclick="wzToggle(this)"><span class="wz-arrow">▶</span> 📁 ' + esc(node.name) + ' <span style="color:var(--text2);font-size:0.82em">(' + wzFolderCount(node) + ')</span></div>';
    }
    h += '<div class="wz-sub" style="' + (dep > 0 ? 'display:none' : '') + '">';
    keys.sort().forEach(function(k){ h += wzTreeHTML(node.children[k], dep + 1); });
    (node.notes || []).forEach(function(n){
      h += '<div class="wz-note" id="wzn-' + n.guid + '" style="cursor:pointer;padding:3px 6px;border-radius:5px" onclick="wzOpen(\'' + n.guid + '\')">📄 ' + esc(n.title) + '<span style="color:var(--text2);font-size:0.82em"> · ' + fmtChars(n.len) + ' · ' + fmtDate(n.modified) + '</span></div>';
    });
    h += '</div>';
    return h;
  }
  var h = '';
  // ── file:// 协议检测：浏览器禁止读取本地正文 ──
  if (location.protocol === 'file:') {
    h += '<div class="section" id="hl-filemode" style="border-left:4px solid #d98a00;background:rgba(217,138,0,.08)"><h2>🔒 检测到 file:// 打开方式</h2><p style="font-size:0.78em;color:var(--text2);line-height:1.9">浏览器会阻止 <code>file://</code> 下按需读取正文（点击篇目将报 <b>Failed to fetch</b>），目录、检索与课题总览仍正常可用。请在<b>仓库根目录</b>运行 <code>python -m http.server</code>，然后访问 <code>http://127.0.0.1:8000/web/demo/tabs/jiaoxing.html</code>（独立文章页为 <code>.../web/demo/articles/haiyun-lectures.html</code>）；或将整仓部署到 GitHub Pages（<code>docs/huayanhai/</code> 相对路径自动解析）。</p></div>';
  }
  // ── 总览 ──
  h += '<div class="section" id="hl-overview" style="border-left:4px solid var(--gold)"><h2>📚 海云讲法 · 公开资料</h2>';
  h += '<p style="font-size:0.74em;color:var(--text2);margin:4px 0 0">🔗 本页可分享/收藏的独立地址：<a href="' + (location.href.indexOf('/articles/') >= 0 ? 'haiyun-lectures.html' : '../articles/haiyun-lectures.html') + '" style="color:var(--blue);text-decoration:underline">海云讲法 · 公开资料（独立页）</a> · 访问后可用页顶「分享地址」按钮一键复制。</p>';
  h += '<p style="font-size:0.78em;color:var(--text2);line-height:1.9">' + esc(cat.subtitle || '') + '。全库共 <b style="color:var(--gold)">' + cat.totals.count + '</b> 篇、<b style="color:var(--gold)">' + cat.totals.folders_top + '</b> 个一级目录，文本合计 <b style="color:var(--gold)">' + fmtChars(cat.totals.chars) + '</b>（html 原件 ' + fmtBytes(cat.totals.size) + '）。正文按需加载，支持关键词检索与目录导航，点篇即读。</p>';
  if ((cat.shortcuts || []).length) {
    h += '<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:8px;font-size:0.76em"><span style="color:var(--text2)">🎯 主要讲法方向：</span>';
    cat.shortcuts.forEach(function(s){
      h += '<span class="topic-card" style="cursor:pointer;padding:6px 10px" onclick="wzJump(\'' + esc(s.root) + '\')"><b style="color:var(--gold)">' + esc(s.label) + '</b> <span style="color:var(--text2)">' + s.count + ' 篇</span></span>';
    });
    h += '</div>';
  }
  h += '</div>';
  // 去重：原独立「🎯 主要讲法方向 · 快捷入口」区块已删除——其一级目录卡片行与下方「目录·检索」树重复；三个重点讲法方向改为行内内嵌于本总览。
  // ── 目录·检索 + 阅读器（双栏：左目录 右正文；点篇即阅，无需下滑跳转）──
  h += '<div class="section" id="hl-browse" style="border-left:4px solid var(--gold)"><h2>🔍 目录 · 检索</h2>';
  h += '<p style="font-size:0.74em;color:var(--text2);line-height:1.7">点击左侧篇目，正文即刻在右侧阅读（目录自动展开、当前篇高亮）；输入关键词即输即搜。窄屏时自动上下排列。</p>';
  h += '<div style="display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap">';
  h += '<div style="flex:1 1 320px;min-width:250px;max-width:540px">';
  h += '<input id="wz-q" type="search" placeholder="输入关键词检索篇目（标题 / 目录）…" oninput="wzFilter(this.value)" style="width:100%;padding:8px 12px;border:1px solid var(--line);border-radius:8px;font-size:0.9em;background:var(--card);color:var(--text)">';
  h += '<div id="wz-count" style="font-size:0.74em;color:var(--text2);margin:6px 0"></div>';
  h += '<div id="wz-tree" style="font-size:0.8em">' + wzTreeHTML(window.wzTree, 0) + '</div>';
  h += '<div id="wz-results" style="display:none;font-size:0.8em"></div>';
  h += '</div>';
  h += '<div style="flex:2 1 420px;min-width:290px;position:sticky;top:8px">';
  h += '<div id="hl-reader" style="max-height:78vh;overflow-y:auto;border-left:3px solid var(--gold);padding:2px 0 12px 14px;font-size:0.88em;line-height:1.95;min-height:120px;color:var(--text2)">📖 阅读区域 — 点击左侧目录或检索结果中的任意篇目，正文将在此显示。</div>';
  h += '</div></div></div>';
  // ── 课题多源总览（经/教/行/密/生活 · 每题聚合全库/播客/视频/门户/书目）──
  h += renderLecturesTopics();
  // ── 播客全季目录（S1-S24 · 387 集真实 RSS）──
  h += renderPodcastCatalog();
  // ── 说明 ──
  h += '<div class="section" id="hl-hint" style="border-left:4px solid var(--line)"><h2>⚠️ 阅读与部署说明</h2>';
  h += '<p style="font-size:0.76em;color:var(--text2);line-height:1.9">📌 <b>数据来源与持久化：</b>本全库源于 wiz.cn 账号 huayanhai 全部 ' + cat.totals.count + ' 篇笔记（' + esc(cat.generated || '') + ' 全量导出），html 原件保真存档于 <code>docs/huayanhai/</code>，正文为按需加载的 txt 抽取本（LF，可由 html 确定性复现）。所有目录、计数与快捷方式均来自导出清单（数据驱动），<b>未加入任何未经验证的条目</b>。</p>';
  h += '<p style="font-size:0.76em;color:var(--text2);line-height:1.9">🌍 <b>本地浏览：</b>若以 <code>file://</code> 直接打开，浏览器安全策略会阻止按需加载正文。请在仓库根目录运行 <code>python -m http.server</code> 后访问 <code>web/demo/tabs/jiaoxing.html</code>，或将整仓部署到 GitHub Pages（<code>../../../docs/huayanhai/</code> 相对路径自动解析）。</p>';
  h += '</div>';
  return h;
}
function wzToggle(el){
  var sub = el.nextElementSibling, arrow = el.querySelector('.wz-arrow');
  if (!sub || sub.className !== 'wz-sub') return;
  var open = sub.style.display !== 'none';
  sub.style.display = open ? 'none' : 'block';
  if (arrow) arrow.textContent = open ? '▶' : '▼';
}
function wzJump(root){
  var q = document.getElementById('wz-q');
  if (q) { q.value = root; wzFilter(root); }
  var b = document.getElementById('hl-browse');
  if (b) b.scrollIntoView({behavior: 'smooth', block: 'start'});
}
function wzFilter(q){
  q = String(q || '').trim();
  var tree = document.getElementById('wz-tree'), res = document.getElementById('wz-results'), cnt = document.getElementById('wz-count');
  if (!tree || !res || !cnt) return;
  if (!q) { res.style.display = 'none'; tree.style.display = 'block'; cnt.textContent = ''; return; }
  var ql = q.toLowerCase();
  var hits = (window.wzAll || []).filter(function(n){
    return (String(n.title || '').toLowerCase().indexOf(ql) >= 0) || (String(n.cat || '').toLowerCase().indexOf(ql) >= 0);
  });
  tree.style.display = 'none'; res.style.display = 'block';
  cnt.textContent = hits.length ? ('命中 ' + hits.length + ' 篇') : '未命中，请尝试其他关键词（支持目录名，如「玄谈」「离世间品」「地藏」）。';
  var h = '';
  hits.forEach(function(n){
    h += '<div class="wz-note" style="padding:7px 10px;margin:4px 0;background:var(--card);border:1px solid var(--line);border-radius:8px;cursor:pointer" onclick="wzOpen(\'' + n.guid + '\')">📄 <b>' + esc(n.title) + '</b><span style="color:var(--text2)"> <span style="color:var(--gold);font-size:0.85em">' + esc(n.cat) + '</span> · ' + fmtChars(n.len) + ' · ' + fmtDate(n.modified) + '</span></div>';
  });
  res.innerHTML = h;
}
function wzOpen(guid){
  var n = window.wzNotes && window.wzNotes[guid];
  var rd = document.getElementById('hl-reader');
  if (!n || !rd) return;
  rd.style.display = 'block';
  rd.innerHTML = '<h2>📖 载入中…</h2><p style="color:var(--text2);font-size:0.78em">' + esc(n.title) + ' · ' + esc(n.cat) + '</p>';
  rd.scrollIntoView({behavior: 'smooth', block: 'start'});
  var url = '../../../docs/huayanhai/' + n.txt.split('/').map(function(seg){ return encodeURIComponent(seg); }).join('/');
  fetch(url).then(function(r){ if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); }).then(function(text){
    var body = String(text || '').replace(/^\uFEFF/, '');
    body = body.replace(/^#[^\n]*\n?/, '');
    var paras = body.split(/\n{2,}/).map(function(p){ return esc(p).replace(/\n/g, '<br>'); }).filter(function(p){ return p.replace(/<br>/g, '').trim(); });
    var all = window.wzAll || [], idx = -1;
    for (var i = 0; i < all.length; i++) { if (all[i].guid === guid) { idx = i; break; } }
    var h = '<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:4px"><h2 style="margin:0">📖 ' + esc(n.title) + '</h2></div>';
    h += '<p style="font-size:0.72em;color:var(--text2);margin-bottom:8px">📁 ' + esc(n.cat) + ' · ' + fmtChars(n.len) + ' · 更新 ' + fmtDate(n.modified) + '</p>';
    h += '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;font-size:0.78em">';
    h += '<button onclick="wzBack()" style="cursor:pointer;padding:5px 14px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--blue)">← 目录</button>';
    if (idx > 0) h += '<button onclick="wzOpen(\'' + all[idx - 1].guid + '\')" style="cursor:pointer;padding:5px 14px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--blue)">↑ 上一篇</button>';
    if (idx >= 0 && idx < all.length - 1) h += '<button onclick="wzOpen(\'' + all[idx + 1].guid + '\')" style="cursor:pointer;padding:5px 14px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--blue)">↓ 下一篇</button>';
    h += '<button onclick="window.scrollTo({top:0,behavior:\'smooth\'})" style="cursor:pointer;padding:5px 14px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--text2)">⬆ 顶部</button>';
    h += '</div>';
    h += '<div style="border-left:3px solid var(--gold);padding-left:16px">' + paras.join('') + '</div>';
    h += '<p style="font-size:0.68em;color:var(--text2);margin-top:10px">📎 原文存档：<code>docs/huayanhai/' + esc(n.txt) + '</code></p>';
    rd.innerHTML = h;
    wzMarkActive(guid);
  }).catch(function(err){
    rd.innerHTML = '<h2>⚠️ 载入失败</h2><p style="color:var(--text2);font-size:0.8em;line-height:1.8">无法按需加载正文（' + esc(String((err && err.message) || err)) + '）。若以 <code>file://</code> 打开会受浏览器安全策略限制；请在仓库根目录运行 <code>python -m http.server</code>，或访问 GitHub Pages 部署版本。</p>';
  });
}
function wzMarkActive(guid){
  var notes = document.querySelectorAll('.wz-note');
  for (var i = 0; i < notes.length; i++) { notes[i].style.background = ''; notes[i].style.borderLeft = ''; }
  var el = document.getElementById('wzn-' + guid);
  if (!el) return;
  el.style.background = 'rgba(212,175,55,.12)';
  el.style.borderLeft = '3px solid var(--gold)';
  var p = el.parentElement;
  while (p && p !== document.body) {
    if (p.classList && p.classList.contains('wz-sub')) {
      if (p.style.display === 'none') p.style.display = 'block';
      var f = p.previousElementSibling;
      if (f && f.querySelector) { var a = f.querySelector('.wz-arrow'); if (a && a.textContent === '▶') a.textContent = '▼'; }
    }
    p = p.parentElement;
  }
}
function wzBack(){ var b = document.getElementById('hl-browse'); if (b) b.scrollIntoView({behavior: 'smooth', block: 'start'}); }

// ═══ 课题多源总览（PRACTICE_DATA.haiyun_lectures_topics）：40 课题×五类，每题聚合权威多源头 ═══
function renderLecturesTopics() {
  var tp = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.haiyun_lectures_topics) ? PRACTICE_DATA.haiyun_lectures_topics : null;
  if (!tp || !tp.groups) return '';
  var h = '';
  h += '<div class="section" id="hl-topics" style="border-left:4px solid var(--blue)"><h2>🧭 课题多源总览 — 经 / 教 / 行 / 密 / 生活</h2>';
  if (tp.meta && tp.meta.note) h += '<p style="font-size:0.74em;color:var(--text2);line-height:1.8">' + esc(tp.meta.note) + '</p>';
  if (tp.meta && tp.meta.title_en) h += '<p class="en-line" style="font-size:0.72em;color:var(--text2);font-style:italic">📖 ' + esc(tp.meta.title_en) + '</p>';
  tp.groups.forEach(function(g) {
    h += '<h3 style="color:var(--gold);margin:16px 0 6px">' + esc(g.title) + (g.title_en ? ' <span class="en-line" style="font-size:0.6em;color:var(--text2);font-weight:400">(' + esc(g.title_en) + ')</span>' : '') + ' <span style="font-size:0.6em;color:var(--text2);font-weight:400">' + (g.topics || []).length + ' 题</span></h3>';
    (g.topics || []).forEach(function(t) {
      h += '<div class="topic-card" style="font-size:0.76em;margin:8px 0">';
      h += '<b>' + esc(t.title) + '</b>';
      if (t.title_en) h += ' <span class="en-line" style="color:var(--text2);font-weight:400;font-style:italic">(' + esc(t.title_en) + ')</span>';
      if (t.desc) h += '<div style="color:var(--text2);line-height:1.7;margin:3px 0">' + esc(t.desc) + '</div>';
      if (t.desc_en) h += '<div class="en-line" style="color:var(--text2);line-height:1.7;font-size:0.92em">📖 ' + esc(t.desc_en) + '</div>';
      h += '<div style="margin-top:5px">';
      (t.wiz || []).forEach(function(f) {
        h += '<span style="display:inline-block;margin:2px 3px;padding:3px 9px;border:1px solid var(--line);border-radius:12px;font-size:0.85em;cursor:pointer;color:var(--blue);background:var(--card);white-space:nowrap" onclick="wzJump(\'' + String(f).replace(/'/g, '&#39;') + '\')">📄 全库「' + esc(f) + '」</span>';
      });
      (t.podcast || []).forEach(function(s) {
        h += '<span style="display:inline-block;margin:2px 3px;padding:3px 9px;border:1px solid var(--line);border-radius:12px;font-size:0.85em;cursor:pointer;color:var(--gold);background:var(--card);white-space:nowrap" onclick="wzPodSeason(' + s + ')">🎧 播客 S' + s + '</span>';
      });
      (t.yt || []).forEach(function(y) {
        h += '<a href="' + esc(y.url) + '" target="_blank" style="display:inline-block;margin:2px 3px;padding:3px 9px;border:1px solid var(--line);border-radius:12px;font-size:0.85em;color:var(--blue);background:var(--card);text-decoration:none;white-space:nowrap">▶️ ' + esc(y.name) + '</a>';
      });
      if (t.yt_q) h += '<a href="https://www.youtube.com/results?search_query=' + encodeURIComponent(t.yt_q) + '" target="_blank" style="display:inline-block;margin:2px 3px;padding:3px 9px;border:1px solid var(--line);border-radius:12px;font-size:0.85em;color:var(--blue);background:var(--card);text-decoration:none;white-space:nowrap">▶️ YouTube 搜索</a>';
      (t.bl || []).forEach(function(b) {
        h += '<a href="' + esc(b.url) + '" target="_blank" style="display:inline-block;margin:2px 3px;padding:3px 9px;border:1px solid var(--line);border-radius:12px;font-size:0.85em;color:var(--blue);background:var(--card);text-decoration:none;white-space:nowrap">📺 B站 · ' + esc(b.name) + '</a>';
      });
      if (t.bl_q) h += '<a href="https://search.bilibili.com/all?keyword=' + encodeURIComponent(t.bl_q) + '" target="_blank" style="display:inline-block;margin:2px 3px;padding:3px 9px;border:1px solid var(--line);border-radius:12px;font-size:0.85em;color:var(--blue);background:var(--card);text-decoration:none;white-space:nowrap">📺 B站 搜索</a>';
      (t.web || []).forEach(function(w) {
        h += '<a href="' + esc(w.url) + '" target="_blank" style="display:inline-block;margin:2px 3px;padding:3px 9px;border:1px solid var(--line);border-radius:12px;font-size:0.85em;color:var(--blue);background:var(--card);text-decoration:none;white-space:nowrap">🌐 ' + esc(w.name) + '</a>';
      });
      h += '</div>';
      if (t.books && t.books.length) h += '<div style="margin-top:4px;font-size:0.9em;color:var(--text2)">📚 ' + t.books.map(function(b) { return esc(b); }).join(' · ') + '</div>';
      h += '</div>';
    });
  });
  h += '</div>';
  return h;
}

// ═══ 播客全季目录（PRACTICE_DATA.haiyun_podcast_catalog）：S1-S24 · 387 集真实 RSS 目录 ═══
function renderPodcastCatalog() {
  var pc = (typeof PRACTICE_DATA !== 'undefined' && PRACTICE_DATA.haiyun_podcast_catalog) ? PRACTICE_DATA.haiyun_podcast_catalog : null;
  if (!pc || !pc.seasons || !pc.episodes) return '';
  window.wzPod = pc; window.wzPodAll = pc.episodes;
  var h = '';
  h += '<div class="section" id="hl-podcast" style="border-left:4px solid var(--gold)"><h2>🎧 播客全季目录 — 海雲繼夢說華嚴 · ' + (pc.meta && pc.meta.episode_count ? pc.meta.episode_count : pc.episodes.length) + ' 集</h2>';
  if (pc.meta) {
    h += '<p style="font-size:0.74em;color:var(--text2);line-height:1.8">📻 ' + esc(pc.meta.title_zh || '') + (pc.meta.title_en ? ' <span class="en-line">(' + esc(pc.meta.title_en) + ')</span>' : '') + ' · ' + esc(pc.meta.creator_zh || '') + ' · ' + esc(pc.meta.language || '');
    if (pc.meta.alt_title_zh) h += '<br>🗂 同名既有条目：' + esc(pc.meta.alt_title_zh) + (pc.meta.alt_title_en ? ' <span class="en-line">(' + esc(pc.meta.alt_title_en) + ')</span>' : '');
    h += '</p>';
    h += '<p style="font-size:0.72em">';
    [['Apple 播客（现名「海雲繼夢說華嚴」）', pc.meta.apple_url], ['Apple（既有条目「普賢乘華嚴宗」）', pc.meta.apple_url_au], ['Spotify', pc.meta.spotify_url], ['RSS 源', pc.meta.rss_url]].forEach(function(pair) {
      if (pair[1]) h += '<a href="' + esc(pair[1]) + '" target="_blank" style="color:var(--blue);margin-right:12px">🔗 ' + pair[0] + '</a>';
    });
    h += '</p>';
    if (pc.meta.season_note) h += '<p style="font-size:0.7em;color:var(--text2);line-height:1.7">📌 ' + esc(pc.meta.season_note) + '</p>';
  }
  h += '<div style="display:flex;gap:6px;flex-wrap:wrap;font-size:0.73em;margin:8px 0">';
  h += '<span style="padding:4px 10px;border:1px solid var(--line);border-radius:14px;cursor:pointer;color:var(--blue);background:var(--card)" onclick="wzPodAll()">全部 ' + pc.episodes.length + ' 集</span>';
  pc.seasons.forEach(function(s) {
    h += '<span style="padding:4px 10px;border:1px solid var(--line);border-radius:14px;cursor:pointer;color:var(--blue);background:var(--card);white-space:nowrap" onclick="wzPodSeason(' + s.s + ')">S' + s.s + ' ' + esc(s.title) + ' <span style="color:var(--text2);font-size:0.85em">(' + s.count + ')</span></span>';
  });
  h += '</div>';
  h += '<input id="wz-pq" type="search" placeholder="在播客目录内检索（标题关键词，如 玄谈 / 药师 / 會後問答）…" oninput="wzPodFilter(this.value)" style="width:100%;max-width:480px;padding:7px 12px;border:1px solid var(--line);border-radius:8px;font-size:0.85em;background:var(--card);color:var(--text)">';
  h += '<div id="wz-pcount" style="font-size:0.72em;color:var(--text2);margin:6px 0"></div>';
  var last = pc.seasons[pc.seasons.length - 1];
  window.wzPodCur = last ? last.s : 0;
  h += '<div id="wz-podlist">' + wzPodListHTML(window.wzPodCur, '') + '</div>';
  h += '<p style="font-size:0.7em;color:var(--text2);line-height:1.7;margin-top:4px">💡 列表默认展示<b>最新季 S' + window.wzPodCur + '</b>（' + esc(last ? last.title : '') + '，当前进行中的《九九华严讲座》）；点击上方季名或输入关键词即可筛选；单集标题可直达官方单集页。数据来自官方 RSS（anchor.fm），含标题、日期与时长。</p>';
  h += '</div>';
  return h;
}
function wzPodListHTML(s, q) {
  var all = window.wzPodAll || [];
  var ql = String(q || '').trim().toLowerCase();
  var list = all.filter(function(e) {
    if (s && e.s !== s) return false;
    if (ql) { var tt = String(e.t || '').toLowerCase() + ' ' + String(e.e || '').toLowerCase(); if (tt.indexOf(ql) < 0) return false; }
    return true;
  });
  if (!list.length) return '<p style="font-size:0.75em;color:var(--text2)">（无匹配单集）</p>';
  var rows = list.map(function(e) {
    return '<tr><td style="white-space:nowrap;font-weight:600">S' + e.s + '</td><td><a href="' + esc(e.u) + '" target="_blank" style="color:var(--blue)">' + esc(e.t) + '</a></td><td style="white-space:nowrap">' + esc(e.d) + '</td><td style="white-space:nowrap">' + e.m + ' 分</td></tr>';
  }).join('');
  return '<table class="v-table" style="font-size:0.72em;width:100%"><tr><th style="text-align:left">季</th><th style="text-align:left">单集标题</th><th style="text-align:left">日期</th><th style="text-align:left">时长</th></tr>' + rows + '</table>';
}
function wzPodSeason(s) {
  window.wzPodCur = s;
  var el = document.getElementById('wz-podlist');
  if (el) el.innerHTML = wzPodListHTML(s, '');
  var c = document.getElementById('wz-pcount');
  if (c) c.textContent = 'S' + s + ' 季 · 共 ' + ((window.wzPodAll || []).filter(function(e) { return e.s === s; }).length) + ' 集';
  var p = document.getElementById('hl-podcast');
  if (p) p.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
function wzPodAll() {
  window.wzPodCur = 0;
  var el = document.getElementById('wz-podlist');
  if (el) el.innerHTML = wzPodListHTML(0, '');
  var c = document.getElementById('wz-pcount');
  if (c) c.textContent = '全部季 · 共 ' + (window.wzPodAll || []).length + ' 集';
  var p = document.getElementById('hl-podcast');
  if (p) p.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
function wzPodFilter(q) {
  var el = document.getElementById('wz-podlist');
  if (el) el.innerHTML = wzPodListHTML(window.wzPodCur || 0, q);
}
'''

# 通用数据驱动独立页渲染脚本：处理「sections + topics」schema（vatamsaka_studies / panjiao_hupan
# 等 gap 数据源共用），生成折叠门布局 + 中英对照 + 出处/链接 + 参考文献。演示层代码，正文单存于 YAML。
GAP_TOPICS_RENDER = r'''function _dynMDInline(s) {
  return String(s||'')
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/(^|[^*])\*([^*]+?)\*(?!\*)/g, '$1<i>$2</i>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target=_blank style="color:var(--blue)">$1</a>');
}
// Markdown 管道表 → <table class="dyn-tbl">：首个非分隔行为表头，|---| 分隔行丢弃
function _dynRenderTable(rows) {
  var cells = rows.map(function(r){
    return r.replace(/^\s*\|/,'').replace(/\|\s*$/,'').split('|').map(function(c){return c.trim();});
  });
  var isSep = function(cs){ return cs.length>0 && cs.every(function(c){return /^:?-{2,}:?$/.test(c);}); };
  var head = cells[0] || [], body;
  if (isSep(head)) { head = []; body = cells.filter(function(cs){return !isSep(cs);}); }
  else { body = cells.slice(1).filter(function(cs){return !isSep(cs);}); }
  var h = '<table class="dyn-tbl">';
  if (head.length) h += '<thead><tr>' + head.map(function(c){return '<th>'+_dynMDInline(c)+'</th>';}).join('') + '</tr></thead>';
  h += '<tbody>' + body.map(function(cs){return '<tr>' + cs.map(function(c){return '<td>'+_dynMDInline(c)+'</td>';}).join('') + '</tr>';}).join('') + '</tbody></table>';
  return h;
}
// CJK 重排：源文多为定宽硬换行，pre-line 会照原样断行致句中断裂（「佛光即法界/全体」），
// 行末的。！？多因定宽截断而非段落结束，故不能当换行信号。规则：只有「真空行 / 结构行（·【（[①-㊿
// 数字. ═══ ** label: 起首）」才另起新行，其余换行一律视为软折行并入上一行（体-体不补空格，涉拉丁则补
// 一空格）。重排后仍走 pre-line，于是段落自然按容器宽度折行。
function _dynStartsNew(t) {
  return /^[·【〔\[]/.test(t) || /^[(（][0-9一二三四五六七八九十]{1,3}[)）]/.test(t) || /^\*\*/.test(t) || /^[\u2460-\u24ff\u3251-\u32bf]/.test(t)
    || /^\d+[\.、)]/.test(t) || /═/.test(t) || /^[\u4e00-\u9fffA-Za-z0-9]{1,6}[:：]/.test(t);
}
function _dynReflowLines(lines) {
  var res = [], cur = null, prev = '';
  function pushCur(){ if (cur !== null) { res.push(cur); cur = null; } }
  lines.forEach(function(raw){
    var t = raw.replace(/\s+$/, '');
    if (t.trim() === '') { pushCur(); if (prev !== '') res.push(''); prev = ''; return; }
    var body = t.replace(/^\s+/, '');
    if (cur === null || _dynStartsNew(body)) { pushCur(); cur = t; }
    else {
      var a = cur.replace(/\s+$/, '');
      var cjk = /[\u4e00-\u9fff、）」』]$/.test(a) && /^[\u4e00-\u9fff、（「『]/.test(body);
      cur = a + (cjk ? '' : ' ') + body;
    }
    prev = t;
  });
  pushCur();
  return res.join('\n');
}
// 块级：连续的 | 行成组转表，其余文字重排后走内联格式化（换行留经容器 pre-line 处理）
function _dynMD(s) {
  var lines = String(s||'').split('\n');
  var out = [], text = [], tbl = [];
  function flushText(){ if(text.length){ out.push(_dynMDInline(_dynReflowLines(text))); text=[]; } }
  function flushTbl(){ if(tbl.length){ out.push(_dynRenderTable(tbl)); tbl=[]; } }
  lines.forEach(function(ln){
    if (/^\s*\|.*\|\s*$/.test(ln)) { flushText(); tbl.push(ln); }
    else if (tbl.length && /^\s*$/.test(ln)) { /* 表内空行忽略 */ }
    else { flushTbl(); text.push(ln); }
  });
  flushText(); flushTbl();
  return out.join('\n');
}
function _dynSectionLink(sec) { return 'avs-dyn-' + sec.id; }
function _dynTopicLink(sec, i) { return 'avs-topic-' + sec.id + '-' + i; }
// mode: 'article' = zhenwei 式连续全文（华严经学等，全展开可读）；默认 'doors' = 折叠门（判教互判等）
function renderDynTopics(data, mode) {
  if (!data || !data.sections) return '';
  var isArticle = (mode === 'article');
  var art = (typeof ARTICLE !== 'undefined') ? ARTICLE : {};
  var icon = data.icon || art.icon || '📌';
  var title = data.title || art.title || '';
  var subtitle = data.title_sub || art.title_sub || '';
  var backTab = art.back && art.back.tab ? '../tabs/' + art.back.tab + '.html' : '';
  var backLabel = (art.back && art.back.label) || '';
  var h = '';
  if (isArticle) {
    // ── 面包屑 ──
    h += '<div style="font-size:0.74em;color:var(--text2);margin-bottom:12px;">';
    h += '<a href="../index.html" style="color:var(--blue);text-decoration:none">主页</a> › ';
    h += '<a href="index.html" style="color:var(--blue);text-decoration:none">独立文章目录</a>';
    if (backTab) h += ' › <a href="' + backTab + '" style="color:var(--blue);text-decoration:none">' + backLabel + '</a>';
    h += '</div>';
    // ── 页头横幅 ──
    h += '<div style="background:linear-gradient(120deg,rgba(184,134,60,0.12),rgba(94,139,158,0.08));border:1px solid var(--line);border-radius:12px;padding:20px 22px;margin-bottom:16px;">';
    h += '  <div style="font-size:0.76em;color:var(--text2);letter-spacing:0.5px">📄 独立文章页 · 数据驱动全文（全量展开）</div>';
    h += '  <h2 data-skip-toc="1" style="color:var(--gold);margin:6px 0 4px">' + icon + ' ' + title + '</h2>';
    if (subtitle) h += '  <div style="font-size:0.85em;color:var(--text2)">' + subtitle + '</div>';
    if (data.intro) h += '  <p style="font-size:0.8em;color:var(--text2);line-height:1.8;white-space:pre-line;margin:10px 0 0">' + _dynMD(data.intro) + '</p>';
    h += '</div>';
    // ── 自动目录（含逐题锚点） ──
    h += '<div class="section" data-chrome="1"><h2>🧭 本文目录</h2>';
    h += '<div style="column-width:250px;column-gap:26px;font-size:0.8em;line-height:1.85">';
    data.sections.forEach(function(sec){
      h += '<div style="padding:2px 0"><a href="#' + _dynSectionLink(sec) + '" style="color:var(--gold);text-decoration:none;font-weight:600">' + (sec.icon||'') + ' ' + sec.title + '</a> <span style="color:var(--text2);font-size:0.85em">(' + ((sec.topics||[]).length) + '题)</span></div>';
      (sec.topics||[]).forEach(function(t,i){
        h += '<div style="padding-left:16px"><a href="#' + _dynTopicLink(sec,i) + '" style="color:var(--text2);text-decoration:none">· ' + t.title + '</a></div>';
      });
    });
    if (data.references) h += '<div style="padding:2px 0"><a href="#avs-dyn-refs" style="color:var(--gold);text-decoration:none;font-weight:600">📚 参考文献</a></div>';
    h += '</div></div>';
    // ── 全文（标题层级：节=h2 / 题=h3，平级兄弟，交 _foldDoc 逐级折叠展开）──
    h += '<div class="section" style="border-left:4px solid var(--gold)" id="article-full"><h2 data-skip-toc="1" style="color:var(--gold)">📄 ' + title + ' · 全文</h2>';
    data.sections.forEach(function(sec){
      h += '<h2 id="' + _dynSectionLink(sec) + '" style="color:var(--gold);border-bottom:1px solid var(--line);padding-bottom:6px;margin-top:18px;font-size:1.08em">' + (sec.icon||'📌') + ' ' + sec.title + ' <span style="font-size:0.6em;color:var(--text2);font-weight:400">(' + ((sec.topics||[]).length) + '题)</span></h2>';
      if (sec.title_en) h += '<div class="en-line" style="font-size:0.74em;color:var(--text2);font-style:italic">' + sec.title_en + '</div>';
      if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + _dynMD(sec.intro) + '</p>';
      if (sec.intro_en) h += '<div class="en-line" style="font-size:0.78em;color:var(--text2);line-height:1.8;white-space:pre-line">📖 ' + _dynMD(sec.intro_en) + '</div>';
      (sec.topics||[]).forEach(function(t,i){
        h += '<h3 id="' + _dynTopicLink(sec,i) + '" style="margin:14px 0 4px;padding-left:12px;border-left:3px solid rgba(94,139,158,0.25);color:var(--blue);font-size:1em;font-weight:600">' + (i+1) + '. ' + t.title;
        if (t.title_en) h += ' <span class="en-line" style="color:var(--text2);font-weight:400;font-style:italic;font-size:0.82em">(' + t.title_en + ')</span>';
        h += '</h3>';
        h += '<div style="font-size:0.8em;line-height:1.8;white-space:pre-line;margin-top:4px;padding-left:12px">' + _dynMD(t.body) + '</div>';
        if (t.en_body) h += '<div class="en-line" style="font-size:0.78em;color:var(--text2);line-height:1.8;white-space:pre-line;margin-top:6px;padding-left:12px">📖 ' + _dynMD(t.en_body) + '</div>';
        var srcs = t.sources || (t.source ? [t.source] : []);
        if (srcs.length) {
          h += '<div style="font-size:0.7em;color:var(--text2);margin-top:6px;padding-left:12px">📎 ';
          srcs.forEach(function(s,si){ h += (si>0?'<br>':'') + _dynMD(s); });
          h += '</div>';
        }
        if (t.links) {
          h += '<div style="font-size:0.7em;margin-top:2px;padding-left:12px">';
          Object.keys(t.links).forEach(function(k){ h += '<a href="' + t.links[k] + '" target=_blank style="color:var(--blue)">🔗 ' + k + '</a> '; });
          h += '</div>';
        }
      });
    });
    h += '</div>';
    if (data.references) {
      h += '<div class="section" id="avs-dyn-refs"><h2>📚 参考文献</h2>' + (window.renderRefList ? renderRefList(data.references, {fmt: _dynMD}) : '');
      h += '</div>';
    }
    // ── 页脚 ──
    h += '<div style="margin-top:18px;padding-top:10px;border-top:1px solid var(--line);font-size:0.74em;color:var(--text2)">';
    h += '<a href="index.html" style="color:var(--blue);text-decoration:none">📚 返回独立文章目录</a>';
    if (backTab) h += ' · <a href="' + backTab + '" style="color:var(--blue);text-decoration:none">' + backLabel + '</a>';
    h += '</div>';
    return h;
  }
  // ── 折叠门布局（panjiao 等，默认） ──
  h += '<div style="font-size:0.74em;margin:4px 0 10px;color:var(--text2);display:flex;flex-wrap:wrap;gap:3px 12px">';
  data.sections.forEach(function(sec){ h += '<a href="#' + _dynSectionLink(sec) + '" style="color:var(--blue);text-decoration:none;white-space:nowrap">' + (sec.icon||'') + sec.title + '</a>'; });
  if (data.references) h += '<a href="#avs-dyn-refs" style="color:var(--blue);text-decoration:none;white-space:nowrap">📚 参考文献</a>';
  h += '</div>';
  data.sections.forEach(function(sec) {
    h += '<div class=section id=' + _dynSectionLink(sec) + '>';
    h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title + ' <span style="font-size:0.62em;color:var(--text2);font-weight:400">(' + ((sec.topics||[]).length) + '题)</span></h2>';
    if (sec.title_en) h += '<div class="en-line" style="font-size:0.74em;color:var(--text2);font-style:italic;margin:-4px 0 6px">' + sec.title_en + '</div>';
    if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8;white-space:pre-line">' + _dynMD(sec.intro) + '</p>';
    if (sec.intro_en) h += '<div class="en-line" style="font-size:0.78em;color:var(--text2);line-height:1.8;white-space:pre-line">📖 ' + _dynMD(sec.intro_en) + '</div>';
    (sec.topics||[]).forEach(function(t, i) {
      var doOpen = (sec.topics[0]===t && i===0) ? ' open' : '';
      h += '<div class="wu-door' + doOpen + '" onclick="this.classList.toggle(\'open\')"><span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
      if (t.title_en) h += ' <span class="en-line" style="color:var(--text2);font-weight:400;font-style:italic;font-size:0.8em">(' + t.title_en + ')</span>';
      h += '<div class=body><div style="font-size:0.8em;line-height:1.8;white-space:pre-line">' + _dynMD(t.body) + '</div>';
      if (t.en_body) h += '<div class="en-line" style="font-size:0.78em;color:var(--text2);line-height:1.8;white-space:pre-line;margin-top:6px">📖 ' + _dynMD(t.en_body) + '</div>';
      var srcs = t.sources || (t.source ? [t.source] : []);
      if (srcs.length) {
        h += '<div style="font-size:0.7em;color:var(--text2);margin-top:6px">📎 ';
        srcs.forEach(function(s,si){ h += (si>0?'<br>':'') + _dynMD(s); });
        h += '</div>';
      }
      if (t.links) {
        h += '<div style="font-size:0.7em;margin-top:2px">';
        Object.keys(t.links).forEach(function(k){ h += '<a href="' + t.links[k] + '" target=_blank style="color:var(--blue)">🔗 ' + k + '</a> '; });
        h += '</div>';
      }
      h += '</div></div>';
    });
    h += '</div>';
  });
  if (data.references) {
    h += '<div class=section id=avs-dyn-refs><h2>📚 参考文献</h2>' + (window.renderRefList ? renderRefList(data.references, {fmt: _dynMD}) : '');
    h += '</div>';
  }
  return h;
}
'''

SHARE_JS = '''<script>
function copyPageLink(){
  var url = window.location.href;
  var toast = document.getElementById('share-toast');
  function done(msg, ok){
    if(toast){ toast.textContent = msg; toast.style.display='block'; setTimeout(function(){ toast.style.display='none'; }, 2600); }
    return ok;
  }
  function fallback(u){
    var ta = document.createElement('textarea'); ta.value = u; ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); done('✅ 本页独立地址已复制：' + u, true); }
    catch(e){ done('📋 请手动复制地址：' + u, false); }
    document.body.removeChild(ta);
  }
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(url).then(function(){ done('✅ 本页独立地址已复制：' + url, true); },
      function(){ fallback(url); });
  } else {
    fallback(url);
  }
}
</script>
'''

# F.6b 文本→深链：细读文章祖师名自动链接至 shanhe.html（progressive enhancement·不动源文）
def _f6b_deeplink_map():
    """从 person_trajectories + lineages 动态生成 name-variant→person_id 映射。"""
    pt = read_yaml('events/person_trajectories.yaml') or {}
    persons = pt.get('persons', pt)
    lj = read_json('data/knowledge_graph/lineages.json') or {}
    # collect all person_ids in 华严 focus lineages
    hv_ids = set()
    for L in lj.get('lineages', []):
        lid = L.get('id', '')
        if any(kw in (L.get('name', '') + lid) for kw in ('华严', '贤首', 'huayan')):
            for e in L.get('edges', []):
                hv_ids.add(e.get('from')); hv_ids.add(e.get('to'))
    # build name→id from trajectories (name field often has "名·描述" → take part before ·)
    mapping = {}
    if isinstance(persons, dict):
        for pid, v in persons.items():
            if pid not in hv_ids:
                continue
            nm = (v or {}).get('name', '')
            if not nm:
                continue
            # primary name (before ·)
            primary = nm.split('·')[0].strip()
            if primary and len(primary) >= 2:
                mapping[primary] = pid
    # Add well-known aliases from backbone (data-driven from complete_lineage_chart)
    clc = read_yaml('knowledge_graph/complete_lineage_chart.yaml') or {}
    for L in clc.get('lineages', []):
        if L.get('id') == HW_BACKBONE_ID:
            for g in L.get('generations', []):
                gn = g.get('name', '')
                gid = g.get('person_id', '')
                if gn and gid and len(gn) >= 2:
                    mapping[gn] = gid
                # title aliases (清涼/賢首/圭峰 etc.)
                title = g.get('title', '')
                if title and gid and len(title) >= 2:
                    mapping[title] = gid
            break
    # manually curated aliases that appear in articles but not in name/title fields
    _extra = {'賢首': 'person_003', '康藏法藏': 'person_003',
              '雲華': 'person_002', '澄觀': 'person_004', '清涼': 'person_004',
              '義天': 'person_010', '義湘': 'person_061', '元曉': 'person_060',
              '審祥': 'person_050', '實叉難陀': 'person_007', '佛陀跋陀罗': 'person_006',
              '應慈': 'person_031', '續法': 'person_080', '淨源': 'person_011'}
    mapping.update(_extra)
    return mapping

LIN_DEEPLINK_JS_TMPL = '''<script>
(function(){
  var MAP = __DEEPLINK_MAP__;
  var NAMES = Object.keys(MAP).sort(function(a,b){return b.length-a.length;});
  var BASE = '../famai/shanhe.html';
  function skip(node){
    var p = node.parentElement;
    while(p && p !== document.body){
      var tag = p.tagName;
      if(tag==='A'||tag==='CODE'||tag==='PRE'||tag==='BLOCKQUOTE') return true;
      var cls = p.getAttribute ? (p.getAttribute('class')||'') : '';
      if(/\\b(q|quote|cite-card|lic)\\b/.test(cls)) return true;
      p = p.parentElement;
    }
    return false;
  }
  function linkify(){
    var root = document.getElementById('article-root');
    if(!root) return;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
    var edits = [];
    var tn;
    while((tn = walker.nextNode())){
      if(skip(tn)) continue;
      var text = tn.textContent;
      for(var i=0;i<NAMES.length;i++){
        var nm = NAMES[i], pos = text.indexOf(nm);
        if(pos < 0) continue;
        edits.push({node:tn, name:nm, pid:MAP[nm], pos:pos});
        break;
      }
    }
    for(var j=edits.length-1;j>=0;j--){
      var e = edits[j];
      var t = e.node.textContent;
      var idx = t.indexOf(e.name);
      if(idx < 0) continue;
      var before = t.slice(0, idx), after = t.slice(idx + e.name.length);
      var a = document.createElement('a');
      a.href = BASE + '?master=' + e.pid;
      a.className = 'lin-deeplink';
      a.title = '在山河法脉地图中展开 ' + e.name;
      a.textContent = e.name;
      var frag = document.createDocumentFragment();
      if(before) frag.appendChild(document.createTextNode(before));
      frag.appendChild(a);
      if(after) frag.appendChild(document.createTextNode(after));
      e.node.parentNode.replaceChild(frag, e.node);
    }
    if(edits.length) console.log('[lin-deeplink] linked %d mentions' % edits.length);
  }
  if(document.readyState==='complete') setTimeout(linkify,100);
  else window.addEventListener('load', function(){ setTimeout(linkify,100); });
})();
</script>
<style>
.lin-deeplink{color:var(--gold,#b8863c);text-decoration:none;border-bottom:1px dashed var(--gold,#b8863c);cursor:pointer;font-weight:600}
.lin-deeplink:hover{color:var(--red,#a83a24);border-bottom-color:var(--red,#a83a24)}
</style>
'''

def build_articles(articles):
    """Emit one standalone static page per full article (web/demo/articles/<id>.html)
    plus a catalog index (web/demo/articles/index.html). Returns total bytes written."""
    practice = load_practice()
    gap = load_gap()
    article_bi = db_reader.load_article_bi()
    try:
        ds_lib = db_reader.load_data_science()
    except Exception as e:
        print(f'  ! data-science layer unavailable: {e}')
        ds_lib = {}
    try:
        narr_lib = db_reader.load_narrative_library()
    except Exception as e:
        print(f'  ! narrative library unavailable: {e}')
        narr_lib = {}
    try:
        sb_lib = db_reader.load_storyboard_library()
    except Exception as e:
        print(f'  ! storyboard library unavailable: {e}')
        sb_lib = {}
    try:
        article_knowledge = db_reader.load_article_knowledge()
    except Exception as e:
        print(f'  ! article knowledge graph unavailable: {e}')
        article_knowledge = {}
    try:
        article_artifacts = db_reader.load_article_artifacts()
    except Exception as e:
        print(f'  ! article artifacts register unavailable: {e}')
        article_artifacts = {}
    # 世主妙严品会众：EDA（词素切分/群组剖面等，编辑性析构）与 assembly（经文事实，40 类/414 名）。
    # 两者皆自 SQLite 读取、按文章 id 内嵌；缺席则该篇不注入，页面照常渲染正文。
    try:
        article_eda = db_reader.load_article_eda()
    except Exception as e:
        print(f'  ! article EDA unavailable: {e}')
        article_eda = {}
    try:
        article_assembly = db_reader.load_article_assembly()
    except Exception as e:
        print(f'  ! article assembly unavailable: {e}')
        article_assembly = {}
    ARTICLES_OUT.mkdir(parents=True, exist_ok=True)
    article_js = read_src('article.js')
    common_css_rel = '../css/common.css'
    total = 0
    count = 0

    # F.6b: generate deeplink JS once (data-driven from trajectories + lineages)
    _dl_map = _f6b_deeplink_map()
    _dl_json = json.dumps(_dl_map, ensure_ascii=False)
    LIN_DEEPLINK_JS = LIN_DEEPLINK_JS_TMPL.replace('__DEEPLINK_MAP__', _dl_json)

    for a in articles:
        if a.get('skip_html'):
            # HTML 由专项脚本生成，build.py 只在 index 登记卡片入口，跳过页面写入
            continue
        payload = {k: a.get(k) for k in ('id', 'file', 'title', 'title_sub', 'icon', 'version', 'meta', 'doc', 'doc_md', 'data_source', 'data_pool', 'back', 'updated_at')}
        title = a.get('title', a['id'])
        ds = a.get('data_source', '')
        pool = a.get('data_pool', 'practice')
        if ds:
            # 数据驱动独立页：内嵌完整数据源（正文单存于 YAML）+ 自包含渲染脚本。
            # pool=practice → PRACTICE_DATA（如 chan_authentic_traces，用 CHAN_TRACES_RENDER）；
            # pool=gap      → GAP_DATA（如 avatamsaka_studies / panjiao_hupan，用通用 GAP_TOPICS_RENDER）。
            if pool == 'gap':
                sub = {ds: gap.get(ds)}
                data_script = ('var GAP_DATA = %s;\n'
                               'var ARTICLE = %s;'
                               % (json.dumps(sub, ensure_ascii=False),
                                  json.dumps({'id': a['id'], 'title': title,
                                              'icon': a.get('icon'), 'title_sub': a.get('title_sub'),
                                              'data_source': ds, 'back': a.get('back')},
                                             ensure_ascii=False)))
                # 华严经学独立页采用 zhenwei 式连续全文布局（标题层级节h2/题h3）；其余 gap 数据驱动页保持折叠门
                dyn_mode = "'article'" if a['id'] == 'avatamsaka-studies' else "'doors'"
                render_script = (GAP_TOPICS_RENDER
                                 + ('\ndocument.getElementById("article-root").innerHTML = renderDynTopics(GAP_DATA[ARTICLE.data_source], %s);' % dyn_mode))
                if a['id'] == 'avatamsaka-studies':
                    # 全文渲染后就地启用站点既有章节折叠机制：节/题标题逐级可单点收展，
                    # 页首一套「全部折叠/全部展开」（_foldDoc 逐级包裹 + _installPageBar 页面级控件）。
                    # foldDefault:false → 默认展开，保留本页「全文可读」身份，折叠按需。
                    render_script += ("\nif(window._foldDoc){ _foldDoc('#article-full', {noBar:true, foldDefault:false}); }"
                                      + "\nif(window._installPageBar){ _installPageBar({rootSel:'#article-root', mountSel:'#article-full'}); }")
            else:
                if ds == 'haiyun_wiz_catalog':
                    # 海云讲法·公开资料独立页：必须与教行页同源同量——文档库 + 40 课题 + 播客全季 全量内嵌
                    sub = {'haiyun_wiz_catalog': practice.get('haiyun_wiz_catalog'),
                           'haiyun_lectures_topics': practice.get('haiyun_lectures_topics'),
                           'haiyun_podcast_catalog': practice.get('haiyun_podcast_catalog')}
                else:
                    sub = {ds: practice.get(ds)}
                data_script = ('var PRACTICE_DATA = %s;\n'
                               'var ARTICLE = %s;'
                               % (json.dumps(sub, ensure_ascii=False),
                                  json.dumps({'id': a['id'], 'title': title,
                                              'icon': a.get('icon'), 'title_sub': a.get('title_sub'),
                                              'data_source': ds, 'back': a.get('back')},
                                             ensure_ascii=False)))
                if ds == 'haiyun_wiz_catalog':
                    # 海云讲法全库独立页：目录·检索 + 按需加载 txt 全文阅读器
                    render_script = (WIZ_LIB_RENDER
                                     + '\nrenderWizLibrary();'
                                     + '\ndocument.getElementById("article-root").innerHTML = renderWizLibrary();')
                else:
                    render_script = (CHAN_TRACES_RENDER
                                     + '\nrenderChanTraces();'
                                     + '\ndocument.getElementById("article-root").innerHTML = renderChanTraces();')
            scripts = ('<script>\n' + data_script + '\n</script>\n'
                       '<script>\n' + wrap_script(render_script) + '\n</script>')
            doc_chars = sum(len(t.get('body') or '')
                            for s in (sub.get(ds) or {}).get('sections', [])
                            for t in s.get('topics', []))
        else:
            data_script = 'var ARTICLE = %s;' % json.dumps(payload, ensure_ascii=False)
            # 交互渲染器按「本文实际所含数据」注入（不再绑定 shizhu-miaoyan 单一 id）：
            #   assembly(40 类会众) → 会众全景流程图；narrative/storyboard → 连环画·信息图。
            # 数据缺席则该篇不注入该渲染器，页面照常渲染正文。
            extra_js = ''
            _asm_here = article_assembly.get(a['id']) if isinstance(article_assembly, dict) else None
            if _asm_here and _asm_here.get('classes'):
                extra_js += ('\n<script>\n' + wrap_script(read_src('miaoyan_flow.js')) + '\n</script>')
            # 连环画式分镜信息图（静态零 Canvas，方案 B）：叙事/分镜任一在场即注入，
            # 数据（MIAOYAN_NARR / MIAOYAN_SB）仍各自内嵌，由 story_comic.js 读取渲染。
            if (narr_lib.get(a['id']) or {}).get('beats') or (sb_lib.get(a['id']) or {}).get('acts'):
                extra_js += ('\n<script>\n' + wrap_script(read_src('story_comic.js')) + '\n</script>')
            if (ds_lib.get(a['id']) or {}).get('linguistic'):
                extra_js += '\n<script>\n' + wrap_script(read_src('data_science.js')) + '\n</script>'
            scripts = ('<script>\n' + data_script + '\n</script>\n'
                       '<script>\n' + wrap_script(article_js) + '\n</script>' + extra_js)
            doc_chars = len(a.get('doc_md', ''))
        graph = article_knowledge.get(a['id'])
        if graph:
            scripts = ('<script>var ARTICLE_GRAPH = %s;</script>\n' % json.dumps(graph, ensure_ascii=False)) + scripts
        arts = article_artifacts.get(a['id'])
        if arts:
            # 仅注册页内嵌 confirmed 条目（pending/rejected 留库待审，不入页面）
            confirmed = [it for it in arts['items'] if it.get('status') == 'confirmed']
            if confirmed:
                scripts = ('<script>var ARTICLE_ARTIFACTS = %s;</script>\n'
                           % json.dumps({'title': arts.get('title'), 'items': confirmed},
                                        ensure_ascii=False)) + scripts
        # 经文事实在前、EDA 析构在后：先注 assembly，使 EDA 可就地回链类名与成员原名
        asm = article_assembly.get(a['id'])
        if asm and asm.get('classes'):
            scripts = ('<script>var ARTICLE_ASSEMBLY = %s;</script>\n'
                       % json.dumps(asm, ensure_ascii=False)) + scripts
        eda = article_eda.get(a['id'])
        if eda:
            scripts = ('<script>var ARTICLE_EDA = %s;</script>\n'
                       % json.dumps(eda, ensure_ascii=False)) + scripts
            a['_eda'] = True
        bi = article_bi.get(a['id'])
        if bi:
            scripts = ('<script>var ARTICLE_BI = %s;</script>\n' % json.dumps(bi, ensure_ascii=False)) + scripts
        # 叙事动画 / 分镜：按文章 id 内嵌（全局单例 MIAOYAN_NARR/MIAOYAN_SB，逐页独立，互不相撞）
        _narr = narr_lib.get(a['id'])
        if _narr and _narr.get('beats'):
            scripts = ('<script>var MIAOYAN_NARR = %s;</script>\n' % json.dumps(_narr, ensure_ascii=False)) + scripts
        _sb = sb_lib.get(a['id'])
        if _sb and _sb.get('acts'):
            scripts = ('<script>var MIAOYAN_SB = %s;</script>\n' % json.dumps(_sb, ensure_ascii=False)) + scripts
        # 数据科学层（四视角）：按文章 id 内嵌 ARTICLE_DS（data/translation/*_studies.yaml）
        _rls = ds_lib.get(a['id'])
        if _rls and _rls.get('linguistic'):
            scripts = ('<script>var ARTICLE_DS = %s;</script>\n' % json.dumps(_rls, ensure_ascii=False)) + scripts
        # （要点导览已行除：不再注入 MIAOYAN_KP，数据层仍存而不入页面。）
        _b = a.get('back') or {}
        back_tab = _b.get('tab') or 'index'
        back_label = _b.get('label') or '导航主页'
        back_href = ('../tabs/%s.html' % back_tab) if back_tab != 'index' else '../index.html'
        updated_at = ('\U0001F4DD 最后更新：' + a['updated_at']) if a.get('updated_at') else ''
        html = f'''<!DOCTYPE html>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>华严宗 · {title} · 独立文章</title>
<link rel="stylesheet" href="{common_css_rel}">
</head>
<body>
<div id="page-top" style="position:sticky;top:0;z-index:100">
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>{title}</h1>
  <span class="art-updated">{updated_at}</span>
  <button id="share-link" class="share-btn" onclick="copyPageLink();return false" title="复制本页独立地址，点击即可直达">🔗 分享地址</button>
  <button id="lang-toggle" class="lang-btn" onclick="toggleSiteLang();return false" title="阅读语言：中英对照 ⇄ 仅中文">🌐 中·EN</button>
  <span style="margin-left:auto;font-size:0.7em;color:var(--text2);text-decoration:none">📄 独立文章页</span>
</header>
<div style="background:rgba(196,107,93,0.08);border-bottom:1px solid rgba(196,107,93,0.25);padding:6px 16px;font-size:0.72em;color:var(--red);text-align:center">
⚠️ 声明：本站内容尚处于初始梳理阶段，在完整性、准确度、详实度、深度等方面均有不足，仅供参考；敬请多提建议，以助完善内容。
</div>
<div style="padding:5px 16px;border-bottom:1px solid var(--line);font-size:0.76em;display:flex;gap:16px;align-items:center;background:rgba(94,139,158,0.06);flex-wrap:wrap">
  <a href="javascript:history.back()" style="color:var(--blue);text-decoration:none;font-weight:600">← 返回上一步</a>
  <span style="opacity:0.45">|</span>
  <a href="{back_href}" style="color:var(--blue);text-decoration:none">返回到：{back_label} ›</a>
  <span style="margin-left:auto;opacity:0.75;color:var(--text2)"><a href="../index.html" style="color:var(--text2);text-decoration:none">首页 ›</a></span>
</div>
</div>
<main class="content content-article" id="article-root"></main>
<div id="share-toast" style="position:fixed;left:50%;bottom:36px;transform:translateX(-50%);background:rgba(31,36,42,0.96);color:#fff;padding:10px 18px;border-radius:8px;font-size:0.82em;display:none;z-index:999;box-shadow:0 4px 16px rgba(0,0,0,0.3)"></div>

<script src="../js/common.js"></script>
{SHARE_JS}
{LIN_DEEPLINK_JS}
{scripts}
</body>
</html>'''
        path = ARTICLES_OUT / (a['id'] + '.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        size = len(html.encode('utf-8'))
        total += size
        count += 1
        print(f'OK  {path} ({size:,} bytes | {doc_chars:,} doc chars)' + (' | DATA-DRIVEN' if ds else ''))

    # ── 目录页 (index) ──
    # 分组依数据源字段（standalone_articles.yaml 之 group / group_order / group_icons），
    # 不在本处硬编码任何分组名或次序；文章无 group 者归「其他」。
    reg = read_yaml('translation/standalone_articles.yaml') or {}
    gspec = {g['key']: g for g in (reg.get('group_order') or []) if g.get('key')}
    gicons = dict(reg.get('group_icons') or {})
    fallback = '其他'

    def _doc_label(p):
        """文章目录卡只显示源文件名，不暴露 docs/ 下的目录结构
        （分类目录调整时版式不受影响，路径变动亦不致改写版式）"""
        return (p or '').replace('\\', '/').rsplit('/', 1)[-1]

    def _card(a):
        back_link = ''
        if a.get('back', {}).get('tab'):
            back_link = ('<a href="../tabs/%s.html" style="color:var(--text2);font-size:0.78em">返回 %s</a>'
                         % (a['back']['tab'], a['back'].get('label', a['back']['tab'])))
        if a.get('data_source'):
            meta_desc = (f'数据驱动页 · 全 YAML 渲染 · <code>{a["data_source"]}.yaml</code>'
                         if a.get('data_source') and not a.get('doc') else
                         f'全文 {len(a.get("doc_md","")):,} 字 · <code>{_doc_label(a.get("doc",""))}</code>')
        else:
            meta_desc = f'全文 {len(a.get("doc_md","") ):,} 字 · <code>{_doc_label(a.get("doc",""))}</code>'
        return f'''<div style="display:flex;flex-direction:column;gap:6px;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:10px;padding:14px 16px">
<div><a href="{a['id'] + '.html'}" style="color:var(--gold);font-weight:700;font-size:1.02em;text-decoration:none">{a.get('icon','📄')} {a.get('title','')} ↗</a></div>
{"<div style='font-size:0.75em;color:var(--text2)'>" + a.get('title_sub','') + "</div>" if a.get('title_sub') else ''}
<div style="font-size:0.72em;color:var(--text3,var(--text2))">{meta_desc}</div>
<div style="display:flex;gap:14px;font-size:0.75em"><a href="../tabs/{a['back']['tab']}.html" style="color:var(--blue);text-decoration:none">栏目: {a['back'].get('label','')}</a> {back_link}</div>
</div>'''

    buckets = {}
    for a in articles:
        buckets.setdefault(a.get('group') or fallback, []).append(a)

    # 组内排序：优先依 order_in_group（None 沉尾·保持自然登记序）；
    # 无 order_in_group 者维持 YAML/注入先后（华严祖师 YAML 已按法脉 杜顺→智俨→法藏→澄观→宗密→李通玄→梦参 登记）。
    for _k in buckets:
        buckets[_k] = sorted(
            buckets[_k],
            key=lambda x: (x.get('order_in_group') is None,
                           x.get('order_in_group') if x.get('order_in_group') is not None else 0))

    # 次序：先依 group_order 声明之组，余者（未声明之组／兜底组）依首见追加
    order = [g['key'] for g in (reg.get('group_order') or []) if g.get('key')]
    for k in buckets:
        if k not in order:
            order.append(k)
    order = [k for k in order if buckets.get(k)]

    sections = []
    for gi, key in enumerate(order):
        items = buckets[key]
        icon = gicons.get(key) or (gspec.get(key, {}) or {}).get('icon') or '📂'
        summary = (gspec.get(key, {}) or {}).get('summary') or ''
        cards = ''.join(_card(a) for a in items)
        summary_html = (f'<div style="font-size:0.74em;color:var(--text2);margin-top:2px">{summary}</div>'
                        if summary else '')
        sections.append(f'''<section id="grp-{gi}" style="margin-top:{8 if gi == 0 else 26}px">
<div style="display:flex;align-items:baseline;gap:10px;border-bottom:1px solid var(--line);padding-bottom:6px;margin-bottom:12px;flex-wrap:wrap">
<span style="font-size:1.12em;font-weight:700;color:var(--gold)">{icon} {key}</span>
<span style="font-size:0.74em;color:var(--text3,var(--text2))">{len(items)} 篇</span>
{summary_html}
</div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px">
{cards}
</div>
</section>''')

    nav = ' · '.join(
        '<a href="#grp-%d" style="color:var(--blue);text-decoration:none">%s %s(%d)</a>'
        % (gi, gicons.get(k) or gspec.get(k, {}).get('icon') or '📂', k, len(buckets[k]))
        for gi, k in enumerate(order))

    n_groups = len(order)
    idx_html = f'''<!DOCTYPE html>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>华严宗 · 独立文章目录</title>
<link rel="stylesheet" href="../css/common.css">
</head>
<body>
<div id="page-top" style="position:sticky;top:0;z-index:100">
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>📚 独立文章目录</h1>
</header>
<div style="background:rgba(196,107,93,0.08);border-bottom:1px solid rgba(196,107,93,0.25);padding:6px 16px;font-size:0.72em;color:var(--red);text-align:center">
⚠️ 声明：本站内容尚处于初始梳理阶段，在完整性、准确度、详实度、深度等方面均有不足，仅供参考；敬请多提建议，以助完善内容。
</div>
<div style="background:rgba(94,139,158,0.06);border-bottom:1px solid rgba(94,139,158,0.2);padding:5px 16px;font-size:0.7em;color:var(--blue);text-align:center">
共 {count} 篇完整文章 · 分 {n_groups} 组 · 每篇均含整篇 doc 全文 · 由 build.py 依 data/translation/standalone_articles.yaml 生成
</div>
<div style="padding:7px 16px;font-size:0.78em;line-height:1.9;border-bottom:1px solid var(--line)">
{nav}
</div>
</div>
<main class="content" id="article-root">
{''.join(sections)}
<div style="margin-top:26px;text-align:center">
<a href="../index.html" style="color:var(--blue);font-size:0.8em">← 返回导航主页</a> ·
<a href="../tabs/gap.html" style="color:var(--blue);font-size:0.8em">华严文献</a> ·
<a href="../tabs/jiaoxing.html" style="color:var(--blue);font-size:0.8em">华严教行</a>
</div>
</main>
</body>
</html>'''
    idx_path = ARTICLES_OUT / 'index.html'
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(idx_html)
    size = len(idx_html.encode('utf-8'))
    total += size
    count += 1
    print(f'OK  {idx_path} ({size:,} bytes | {len(articles)} articles | {n_groups} groups: '
          + ', '.join('%s=%d' % (k, len(buckets[k])) for k in order) + ')')
    return total



def main():
    # Ensure output directories
    TABS_OUT.mkdir(parents=True, exist_ok=True)
    CSS_OUT.mkdir(parents=True, exist_ok=True)
    JS_OUT.mkdir(parents=True, exist_ok=True)

    nav = load_navigation()

    total_size = 0
    file_count = 0

    # ── Build standalone article pages (每一篇完整文章的独立地址) ──
    articles = load_standalone_articles()
    total_size += build_articles(articles)
    file_count += len(articles) + 1

    # ── Build Tab1: Lineage (preserve original layout) ──
    lineage_html = build_lineage_page()
    lineage_path = TABS_OUT / 'lineage.html'
    with open(lineage_path, 'w', encoding='utf-8') as f:
        f.write(lineage_html)
    size = len(lineage_html.encode('utf-8'))
    total_size += size
    file_count += 1
    graph = load_graph()
    print(f'OK  {lineage_path} ({size:,} bytes | {len(graph.get("nodes",[]))} persons | {len(graph.get("edges",[]))} edges)')

    # ── Build 法脉传承模块壳 (famai/index.html · registry-driven) ──
    famai_size = build_famai_shell()
    if famai_size:
        total_size += famai_size
        file_count += 1

    # ── Build 子页B「山河法脉」＋层源许可声明页 (F.2) ──
    sh_size = build_shanhe_page()
    if sh_size:
        total_size += sh_size
        file_count += 1
    li_size = build_famai_license_page()
    if li_size:
        total_size += li_size
        file_count += 1

    # ── Build Tab2: Gap (restructured layout) ──
    gap_spec = nav.get('gap', {})
    gap_html = build_simple_tab_page(
        gap_spec.get('title', '华严文献'),
        'gap',
        render_sidebar(gap_spec),
        gap_spec.get('render', 'if(typeof renderGap==="function")renderGap();'),
        view_id=gap_spec.get('view_id', 'gap-view'),
        articles=articles)
    gap_path = TABS_OUT / 'gap.html'
    with open(gap_path, 'w', encoding='utf-8') as f:
        f.write(gap_html)
    size = len(gap_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {gap_path} ({size:,} bytes)')

    # ── Build Tab3: Jiaoxing (renamed, restructured) ──
    jx_spec = nav.get('jiaoxing', {})
    jx_html = build_simple_tab_page(
        jx_spec.get('title', '教海行云'),
        'jiaoxing',
        render_sidebar(jx_spec),
        jx_spec.get('render', 'renderPractice();'),
        view_id=jx_spec.get('view_id', 'practice-view'),
        articles=articles)
    jx_path = TABS_OUT / 'jiaoxing.html'
    with open(jx_path, 'w', encoding='utf-8') as f:
        f.write(jx_html)
    size = len(jx_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {jx_path} ({size:,} bytes)')

    # ── Build Tab4: Frontier (restructured) ──
    fr_spec = nav.get('frontier', {})
    inject_frontier_subs(fr_spec, load_frontier(), articles)
    fr_html = build_simple_tab_page(
        fr_spec.get('title', '前沿对话'),
        'frontier',
        render_sidebar(fr_spec),
        fr_spec.get('render', 'if(typeof renderFrontier==="function")renderFrontier();'),
        view_id=fr_spec.get('view_id', 'frontier-view'),
        articles=articles)
    fr_path = TABS_OUT / 'frontier.html'
    with open(fr_path, 'w', encoding='utf-8') as f:
        f.write(fr_html)
    size = len(fr_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {fr_path} ({size:,} bytes)')

    # ── Build Tab5: Cosmology (restructured) ──
    co_spec = nav.get('cosmology', {})
    co_html = build_simple_tab_page(
        co_spec.get('title', '世主妙严'),
        'cosmology',
        render_sidebar(co_spec),
        co_spec.get('render', 'if(typeof renderCosmology==="function")renderCosmology();'),
        view_id=co_spec.get('view_id', 'cosmology-view'),
        articles=articles)
    co_path = TABS_OUT / 'cosmology.html'
    with open(co_path, 'w', encoding='utf-8') as f:
        f.write(co_html)
    size = len(co_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {co_path} ({size:,} bytes)')

    # ── Build Tab6: Spirit (new) ──
    sp_spec = nav.get('spirit', {})
    sp_html = build_simple_tab_page(
        sp_spec.get('title', '灵性仁本'),
        'spirit',
        render_sidebar(sp_spec),
        sp_spec.get('render', 'if(typeof renderSpirit==="function")renderSpirit();'),
        view_id=sp_spec.get('view_id', 'spirit-view'),
        articles=articles)
    sp_path = TABS_OUT / 'spirit.html'
    with open(sp_path, 'w', encoding='utf-8') as f:
        f.write(sp_html)
    size = len(sp_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {sp_path} ({size:,} bytes)')

    # ── Copy/WRITE shared CSS ──
    common_css = read_src('common.css')
    if not common_css:
        # Use CSS extracted from template_top as fallback
        common_css = '''/* Common CSS will be built by agent - see src/common.css */'''
    css_path = CSS_OUT / 'common.css'
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(common_css)
    size = len(common_css.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {css_path} ({size:,} bytes)')

    # ── Copy/WRITE shared JS ──
    common_js = read_src('common.js')
    if not common_js:
        common_js = '''// Common JS will be built by agent - see src/common.js'''
    js_path = JS_OUT / 'common.js'
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(common_js)
    size = len(common_js.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {js_path} ({size:,} bytes)')

    # ── Build index.html with dynamic stats ──
    graph = load_graph()
    temple_data = read_yaml('locations/temple_directory.yaml')
    traj_data = read_yaml('events/person_trajectories.yaml')
    traj_count = sum(1 for k, v in traj_data.items() if k.startswith('person_') and isinstance(v, dict) and 'route' in v) if traj_data else 0
    temple_count = len(temple_data.get('temples', [])) if temple_data else 0
    glossary_data = read_yaml('translation/glossary.yaml')
    glossary_count = len(glossary_data.get('terms', [])) if glossary_data else 0

    with open(OUT / 'index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    index_html = index_html.replace('__STAT_PERSONS__', str(len(graph.get('nodes', []))))
    index_html = index_html.replace('__STAT_EDGES__', str(len(graph.get('edges', []))))
    index_html = index_html.replace('__STAT_TEMPLES__', str(temple_count))
    index_html = index_html.replace('__STAT_TABS__', '6')
    index_html = index_html.replace('__STAT_GLOSSARY__', str(glossary_count))

    index_path = OUT / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    size = len(index_html.encode('utf-8'))
    total_size += size
    file_count += 1
    node_count = len(graph.get('nodes', []))
    edge_count = len(graph.get('edges', []))
    print(f'OK  {index_path} ({size:,} bytes | {node_count} persons | {temple_count} temples | {glossary_count} glossary)')

    print(f'\nTotal: {file_count} files | {total_size:,} bytes')


if __name__ == '__main__':
    main()
