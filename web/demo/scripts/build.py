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
    """Build Tab1: 法脉传承 (standalone, Canvas+Leaflet, layout preserved)."""
    graph = load_graph()
    events = load_events()
    graph_json = json.dumps(graph, ensure_ascii=False)

    # Build data.js content
    data_js_content = f'''
var GRAPH = {graph_json};
var DATA = GRAPH;
var nodeMap = {{}};
if(DATA && DATA.nodes) DATA.nodes.forEach(function(n){{nodeMap[n.id]=n;}});
var GAP = {{}};
var HEART_ARTICLES = [];
var selectedId = null, selectedId2 = null, hoveredId = null, searchQuery = "";
var map = null, mapMain = null, mapMini = null;
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

    # Inject events data as JS globals inside lineage.js replacement
    events_js = ''
    for name, data in events.items():
        events_js += f'var {name.upper()} = {json.dumps(data, ensure_ascii=False)};\n'

    # Build clean standalone page
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<title>华严宗 · 法脉传承</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<link rel="stylesheet" href="../css/common.css">
<style>
#search-bar{{display:flex;gap:6px;padding:6px 12px;background:var(--panel);border-bottom:1px solid var(--line);align-items:center}}
#search-bar input{{border:1px solid var(--line);border-radius:14px;padding:5px 12px;font-size:0.8em;background:var(--card);color:var(--text);width:220px;outline:none}}
#main-row{{display:flex;flex:1;min-height:0}}
#tl-panel{{flex:1;position:relative;background:var(--panel);overflow-y:auto;overflow-x:hidden;min-width:0;cursor:grab}}
#tl-panel canvas{{display:block;position:absolute;top:0;left:0}}
#side{{flex:1;display:flex;flex-direction:column;min-width:200px;border-left:1px solid var(--line)}}
#map-main-wrap{{position:relative;overflow:hidden;flex:1}}
#map-main,#map-mini{{width:100%;height:100%}}
#info-popup{{position:fixed;z-index:999;background:var(--card);border:1px solid var(--gold);border-radius:10px;padding:12px 16px;font-size:0.82em;max-width:360px;max-height:70vh;overflow-y:auto;color:var(--text);box-shadow:0 8px 30px rgba(60,40,20,0.18);display:none}}
#info-popup h3{{color:var(--gold);font-size:1.05em;margin-bottom:4px}}
#info-popup .close-btn{{position:absolute;top:4px;right:8px;cursor:pointer;color:var(--text2);font-size:1.1em}}
#controls{{background:var(--panel);padding:6px 12px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;border-top:1px solid var(--line)}}
#controls button{{padding:4px 12px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.73em;transition:all 0.2s}}
#controls button:hover{{background:#f0ebe0;color:var(--text);border-color:var(--gold)}}
#controls button.active{{background:var(--gold);color:#fff;border-color:var(--gold)}}
#tl-tooltip{{position:absolute;background:var(--card);color:var(--text);padding:10px 14px;border-radius:8px;font-size:0.82em;pointer-events:none;opacity:0;transition:opacity 0.15s;max-width:300px;z-index:100;box-shadow:0 4px 14px rgba(60,40,20,0.14);border:1px solid var(--line)}}
#tl-tooltip h3{{color:var(--gold);margin-bottom:3px}}
#resize-handle{{width:5px;cursor:col-resize;background:var(--line);transition:background 0.2s;flex-shrink:0}}#resize-handle:hover,#resize-handle.active{{background:var(--gold)}}
.map-ancient .leaflet-tile-pane{{filter:sepia(0.7) hue-rotate(-15deg) saturate(0.4) brightness(0.85) contrast(1.1)}}
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
  #info-popup{{position:fixed;max-width:94vw;max-height:50vh;font-size:0.72em;left:3vw!important;top:10vh!important}}
}}
</style>
</head>
<body>
<header id="header">
  <a href="../index.html" class="back-link">&larr; 总览</a>
  <h1>🌊 法脉传承 · 时空长河</h1>
  <div style="font-size:0.68em;color:var(--text2);margin-left:auto">滚轮缩放 | 拖拽平移 | Shift+点击双人对比</div>
</header>

<div id="search-bar">
  <input type="text" id="search-input" placeholder="🔍 检索人物、地点…">
  <span id="anim-status" style="flex:1;font-size:0.7em;color:var(--gold);margin:0 8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;opacity:0;transition:opacity 0.3s"></span>
  <span id="stats-bar" style="font-size:0.68em;color:var(--text2);margin-left:auto"></span>
</div>

<div id="main-row">
  <div id="tl-panel"><canvas id="tl-canvas"></canvas><div id="tl-tooltip"></div></div>
  <div id="resize-handle" title="拖拽调节地图宽度"></div>
  <div id="side">
    <div id="map-main-wrap">
      <div id="map-main"></div>
      <div id="map-overlay" style="position:absolute;bottom:50px;left:10px;right:10px;z-index:500;background:rgba(254,253,249,0.94);border:2px solid var(--gold);border-radius:10px;padding:10px 14px;font-size:0.78em;line-height:1.5;display:none;pointer-events:none;box-shadow:0 4px 16px rgba(60,40,20,0.18)"></div>
      <div id="map-mini-wrap" style="position:absolute;bottom:10px;right:10px;width:180px;height:130px;border:2px solid var(--gold);border-radius:6px;overflow:hidden;z-index:600;box-shadow:0 4px 16px rgba(60,40,20,0.25);background:#fdfaf3">
        <div id="map-mini"></div>
        <button id="mini-terrain-btn" onclick="toggleMiniTerrain()" style="position:absolute;bottom:2px;right:2px;z-index:700;font-size:7px;padding:1px 4px;border:1px solid var(--line);border-radius:3px;background:var(--card);color:var(--text2);cursor:pointer">🗻 地形</button>
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
  <button id="ancient-btn" onclick="toggleAncient()">🏯 古今</button>
  <span id="speed-row" style="font-size:0.7em;color:var(--text2)">⏱<input type="range" id="anim-speed" min="5" max="40" value="15" step="1"><span id="speed-label">1×</span></span>
  <button id="route-info-btn" style="border:1px solid var(--blue);color:var(--blue);font-size:0.75em" onclick="toggleRouteInfo()">ℹ️ 路线</button>
  <button id="anim-btn" style="border:1px solid var(--green);color:var(--green)" onclick="toggleAnim()">▶ 播放</button>
  <button id="reset-btn" style="margin-left:auto;border:1px solid var(--gold);color:var(--gold)">↺ 重置</button>
</div>

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


def build_simple_tab_page(title, tab_id, sidebar_html, render_call, view_id=None):
    """Build a tab page with sidebar layout using existing JS rendering."""
    if view_id is None:
        view_id = f'{tab_id}-view'
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
    <a href="#gv-overview" class="nav-link active" data-section="gv-overview">📊 差异总览</a>
    <a href="#gv-parallel" class="nav-link" data-section="gv-parallel">📖 原文对读</a>
    <a href="#gv-genealogy" class="nav-link" data-section="gv-genealogy">🕸 文本系谱</a>
    '''
    gap_html = build_simple_tab_page('华严文献 · 雅思渊才', 'gap', sidebar_gap, 'if(typeof renderGap==="function")renderGap();')
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
    <a href="#pv-system" class="nav-link active" data-section="pv-system">📐 修行体系</a>
    <a href="#pv-meditation" class="nav-link" data-section="pv-meditation">🗺 禅观法要</a>
    <a href="#pv-heart" class="nav-link" data-section="pv-heart">❤️ 实修心要</a>
    <a href="#pv-resources" class="nav-link" data-section="pv-resources">📡 讲法资源</a>
    '''
    jx_html = build_simple_tab_page('华严教行 · 修行体系', 'jiaoxing', sidebar_jx, 'renderPractice();', view_id='practice-view')
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
    <a href="#fv-dialogue" class="nav-link active" data-section="fv-dialogue">🔬 跨界对话</a>
    <a href="#fv-litreview" class="nav-link" data-section="fv-litreview">📑 文献综述</a>
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
    <a href="#" class="nav-link active" onclick="document.getElementById('cosmo-canvas').scrollIntoView({behavior:'smooth'});return false">🌊 华藏世界海</a>
    <a href="#" class="nav-link" onclick="document.getElementById('cosmo-tower').scrollIntoView({behavior:'smooth'});return false">📐 三界诸天</a>
    <a href="#" class="nav-link">🎨 艺术珍品</a>
    <a href="#" class="nav-link">🎵 梵呗字母</a>
    <a href="#" class="nav-link">🗺 古迹巡礼</a>
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
