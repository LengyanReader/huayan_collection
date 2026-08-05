#!/usr/bin/env python3
"""
Build web/demo/ from src/ files + data/ directory.
Produces: index.html + tabs/*.html (5) + css/common.css + js/common.js

Usage (from project root):
  python web/demo/scripts/build.py
"""
import json
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
    """Load complete GRAPH data from graph.json (already merged by SQLite export)."""
    return read_json('web/demo/graph.json')


def load_gap():
    """Load GAP data from gap.json and gap_content.yaml."""
    gap = read_json('web/demo/gap.json')
    # Merge in gap_content
    gc = read_yaml('translation/gap_content.yaml')
    if gc:
        gap['content'] = gc
    return gap


def load_events():
    """Load all event YAML files and return merged dict."""
    events = {}
    event_files = [
        'key_events', 'anim_waypoints', 'transmission_story',
        'theory_stages', 'practice_stages', 'geo_flow',
        'era_brackets', 'other_schools', 'loc_ancient', 'dynasty_boundaries'
    ]
    for name in event_files:
        data = read_yaml(f'events/{name}.yaml')
        if data:
            events[name] = data
    return events


def load_cosmology():
    """Load cosmology data from YAML files."""
    cosmo = {}
    for name in ['cosmo_layers', 'three_realms', 'art_treasures']:
        data = read_yaml(f'cosmology/{name}.yaml')
        if data:
            cosmo[name] = data
    return cosmo


def load_practice():
    """Load practice data from YAML files."""
    practice = {}
    for name in ['cultivation_system', 'meditation_essentials',
                 'teaching_resources', 'heart_xref']:
        data = read_yaml(f'practice/{name}.yaml')
        if data:
            practice[name] = data
    return practice


def load_frontier():
    """Load frontier data."""
    return read_yaml('frontier/frontier_dialogue.yaml') or {}


# ── HTML page template ──
PAGE_TOP = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>华严宗 · {title}</title>
<link rel="stylesheet" href="../css/common.css">
</head>
<body>
<header id="header">
  <a href="../index.html" class="back-link">&larr; 总览</a>
  <h1>{title}</h1>
</header>
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
    # Actually load HEART from the old build
    heart_articles = []
    wechat_dir = DATA_DIR / 'hy_refs' / 'wechat'
    if wechat_dir.exists():
        heart_articles = []  # Will be populated from existing data

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


def build_lineage_page():
    """Build Tab1: 法脉传承 (layout preserved, single-page structure)."""
    # Tab1 is special - it uses Canvas + Leaflet and needs its original layout
    template_top = read_src('template_top.html')
    data_js = read_src('data.js')
    lineage_js = read_src('lineage.js')
    init_js = read_src('init.js')
    template_bot = read_src('template_bottom.html')

    # Build GRAPH data (same as old build.py but without hardcoded data)
    graph = load_graph()
    gap = load_gap()
    events = load_events()
    heart_articles = read_json('web/demo/gap.json')  # placeholder

    graph_json = json.dumps(graph, ensure_ascii=False)
    gap_json = json.dumps(gap, ensure_ascii=False)
    heart_json = json.dumps(heart_articles, ensure_ascii=False)

    data_js = data_js.replace('__GRAPH__', graph_json)
    data_js = data_js.replace('__GAP__', gap_json)
    data_js = data_js.replace('__HEART__', heart_json)

    # Strip stray leading chars
    def clean(s):
        while s and s[0] not in '<':
            s = s[1:]
        return s

    gap_js = read_src('gap.js')
    practice_js = read_src('practice.js')
    frontier_js = read_src('frontier.js')
    cosmology_js = read_src('cosmology.js')

    # Only Tab1 content, other tabs removed
    # Keep the HTML structure but modify tab buttons to only show lineage
    # For now, keep full structure (single HTML still works for lineage tab)
    html = clean(template_top) + data_js + lineage_js + gap_js + practice_js + frontier_js + cosmology_js + init_js + clean(template_bot)

    # Rename 华严行法 -> 华严教行 in the HTML
    html = html.replace('华严行法', '华严教行')

    return html


def build_simple_tab_page(title, tab_id, sidebar_html, render_call):
    """Build a tab page with sidebar layout using existing JS rendering."""
    graph = load_graph()
    gap = load_gap()
    events = load_events()
    cosmo = load_cosmology()
    practice = load_practice()
    frontier = load_frontier()

    # Build inline data script
    data_script = f'''
var GRAPH = {json.dumps(graph, ensure_ascii=False)};
var GAP = {json.dumps(gap, ensure_ascii=False)};
var EVENTS = {json.dumps(events, ensure_ascii=False)};
var COSMO_DATA = {json.dumps(cosmo, ensure_ascii=False)};
var PRACTICE_DATA = {json.dumps(practice, ensure_ascii=False)};
var FRONTIER_DATA = {json.dumps(frontier, ensure_ascii=False)};
var HEART_ARTICLES = {{}};
var DATA = GRAPH;
var nodeMap = {{}};
if(DATA && DATA.nodes) DATA.nodes.forEach(function(n){{nodeMap[n.id]=n;}});
'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>华严宗 · {title}</title>
<link rel="stylesheet" href="../css/common.css">
</head>
<body>
<header id="header">
  <a href="../index.html" class="back-link">&larr; 总览</a>
  <h1>{title}</h1>
</header>
<div class="layout">
  <nav class="sidebar" id="sidebar">
    {sidebar_html}
  </nav>
  <main class="content" id="content">
    <div id="{tab_id}-view"></div>
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
  {render_call}
  renderComments('{tab_id}');
}})();
</script>
</body>
</html>'''

    # Rename practice->jiaoxing in content
    html = html.replace('华严行法', '华严教行')
    html = html.replace('renderPractice()', 'renderJiaoxing()')
    html = html.replace('switchPracticeView', 'switchJiaoxingView')
    html = html.replace('pv-nav', 'jv-nav')

    return html


def main():
    # Ensure output directories
    TABS_OUT.mkdir(parents=True, exist_ok=True)
    CSS_OUT.mkdir(parents=True, exist_ok=True)
    JS_OUT.mkdir(parents=True, exist_ok=True)

    total_size = 0
    file_count = 0

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

    # ── Build Tab2: Gap (restructured layout) ──
    sidebar_gap = '''
    <h3>📜 华严文献</h3>
    <a href="#overview" class="nav-link active" data-section="overview">📊 差异总览</a>
    <a href="#parallel" class="nav-link" data-section="parallel">📖 原文对读</a>
    <a href="#genealogy" class="nav-link" data-section="genealogy">🕸 文本系谱</a>
    <a href="#references" class="nav-link" data-section="references">📚 参考文献</a>
    '''
    gap_html = build_simple_tab_page('华严文献 · 汉藏差异', 'gap', sidebar_gap, 'if(typeof renderGap==="function")renderGap();')
    gap_path = TABS_OUT / 'gap.html'
    with open(gap_path, 'w', encoding='utf-8') as f:
        f.write(gap_html)
    size = len(gap_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {gap_path} ({size:,} bytes)')

    # ── Build Tab3: Jiaoxing (renamed, restructured) ──
    sidebar_jx = '''
    <h3>🧘 华严教行</h3>
    <a href="#system" class="nav-link active" data-section="system">📐 修行体系</a>
    <a href="#meditation" class="nav-link" data-section="meditation">🗺 禅观法要</a>
    <a href="#heart" class="nav-link" data-section="heart">❤️ 实修心要</a>
    <a href="#resources" class="nav-link" data-section="resources">📡 讲法资源</a>
    '''
    jx_html = build_simple_tab_page('华严教行 · 修行体系', 'jiaoxing', sidebar_jx, 'if(typeof renderPractice==="function")renderPractice();')
    jx_path = TABS_OUT / 'jiaoxing.html'
    with open(jx_path, 'w', encoding='utf-8') as f:
        f.write(jx_html)
    size = len(jx_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {jx_path} ({size:,} bytes)')

    # ── Build Tab4: Frontier (restructured) ──
    sidebar_fr = '''
    <h3>🔬 前沿对话</h3>
    <a href="#dialogue" class="nav-link active" data-section="dialogue">🔬 跨界对话</a>
    <a href="#litreview" class="nav-link" data-section="litreview">📑 文献综述</a>
    '''
    fr_html = build_simple_tab_page('前沿对话 · 跨界研究', 'frontier', sidebar_fr, 'if(typeof renderFrontier==="function")renderFrontier();')
    fr_path = TABS_OUT / 'frontier.html'
    with open(fr_path, 'w', encoding='utf-8') as f:
        f.write(fr_html)
    size = len(fr_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {fr_path} ({size:,} bytes)')

    # ── Build Tab5: Cosmology (restructured) ──
    sidebar_co = '''
    <h3>🪷 世主妙严</h3>
    <a href="#mandala" class="nav-link active" data-section="mandala">🌊 华藏世界海</a>
    <a href="#tower" class="nav-link" data-section="tower">📐 三界诸天</a>
    <a href="#art" class="nav-link" data-section="art">🎨 艺术珍品</a>
    <a href="#chant" class="nav-link" data-section="chant">🎵 梵呗字母</a>
    <a href="#sites" class="nav-link" data-section="sites">🗺 古迹巡礼</a>
    '''
    co_html = build_simple_tab_page('世主妙严 · 华藏世界海', 'cosmology', sidebar_co, 'if(typeof renderCosmology==="function")renderCosmology();')
    co_path = TABS_OUT / 'cosmology.html'
    with open(co_path, 'w', encoding='utf-8') as f:
        f.write(co_html)
    size = len(co_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {co_path} ({size:,} bytes)')

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

    print(f'\nTotal: {file_count} files | {total_size:,} bytes')


if __name__ == '__main__':
    main()
