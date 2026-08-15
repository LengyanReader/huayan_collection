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
    # Merge avatamsaka studies
    avs = read_yaml('translation/avatamsaka_studies.yaml')
    if avs:
        gap['avatamsaka_studies'] = avs
    # Merge intertextual canon
    ic = read_yaml('translation/intertextual_canon.yaml')
    if ic:
        gap['intertextual_canon'] = ic
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
                 'faxiang_xuanji']:
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
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>{title}</h1>
  <a href="#" onclick="heartLogin();return false" style="margin-left:auto;font-size:0.7em;color:var(--text2);text-decoration:none" title="配置GitHub Token">🔑 登录</a>
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
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>🌊 法脉传承 · 时空长河</h1>
</header>

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

</div>

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
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>{title}</h1>
  <a href="#" onclick="heartLogin();return false" style="margin-left:auto;font-size:0.7em;color:var(--text2);text-decoration:none" title="配置GitHub Token">🔑 登录</a>
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
    <div class="sidebar-group"><a href="#" class="nav-link active" onclick="switchGapView('overview',this);return false">📊 差异总览</a></div>
    <div class="sidebar-group"><a href="#" class="nav-link" onclick="switchGapView('parallel',this);return false">📖 原文对读</a></div>
    <div class="sidebar-group"><a href="#" class="nav-link" onclick="switchGapView('genealogy',this);return false">🕸 文本系谱</a></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchGapView('avatamsaka_studies',this);return false">🌏 华严经学 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="gapSubNav('avatamsaka_studies','avs-origins');return false">起源与形成</a>
    <a href="#" class="sub-link" onclick="gapSubNav('avatamsaka_studies','avs-transmission');return false">翻译与流传</a>
    <a href="#" class="sub-link" onclick="gapSubNav('avatamsaka_studies','avs-structure');return false">结构关系与表法</a>
    <a href="#" class="sub-link" onclick="gapSubNav('avatamsaka_studies','avs-doctrinal');return false">义学阐释</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchGapView('intertextual',this);return false">📖 以经证经 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-tiantai');return false">天台宗</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-madhyamaka');return false">中观·三论</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-yogacara');return false">唯识·法相</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-chan');return false">禅宗</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-pureland');return false">净土宗</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-vinaya');return false">律宗</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-esoteric');return false">密宗·真言</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-kusha');return false">俱舍宗</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-chengshi');return false">成实宗</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-niepan');return false">涅槃宗</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-dilun');return false">地论宗</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-shelun');return false">摄论宗</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-tathagatagarbha');return false">如来藏系</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-other_sutras');return false">重要通经</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-dizang');return false">地藏法门</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-tibetan');return false">藏传佛教</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-theravada');return false">南传·上座部</a>
    <a href="#" class="sub-link" onclick="gapSubNav('intertextual','ic-hetuvidya');return false">因明</a>
    </div></div>
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
    <h3>🧘 教海行云</h3>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs active" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('system',this);return false">📐 修行体系 <span class="toggle-arrow">▾</span></a>
    <div class="sub-links" style=display:block>
    <a href="#" class="sub-link" onclick="jxSubNav('system','sys-stages');return false">三阶段</a>
    <a href="#" class="sub-link" onclick="jxSubNav('system','sys-blueprint');return false">四阶段蓝图</a>
    <a href="#" class="sub-link" onclick="jxSubNav('system','sys-six');return false">六科五大行法</a>
    <a href="#" class="sub-link" onclick="jxSubNav('system','sys-projects');return false">四大工程</a>
    <a href="#" class="sub-link" onclick="jxSubNav('system','sys-evolution');return false">演进脉络</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('meditation',this);return false">🗺 禅观法要 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-overview');return false">体系总览</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-paths');return false">次第道与圆融道</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-stage1');return false">资粮道</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-stage2');return false">前行</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-stage3');return false">正行</a>
    <a href="#" class="sub-sub-link" onclick="jxSubNav('meditation','med-stage3');return false">　⬦ 观照·能所分离</a>
    <a href="#" class="sub-sub-link" onclick="jxSubNav('meditation','med-stage3');return false">　⬦ 照住·能所合一</a>
    <a href="#" class="sub-sub-link" onclick="jxSubNav('meditation','med-stage3');return false">　⬦ 照见·能所双泯</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-classical');return false">古典义理地基</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-texts');return false">典籍阐释</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-verify');return false">验证机制</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-heart');return false">实修心要</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('meditation',this);return false">❤️ 心法·禅定·瑜伽 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-xinfa');return false">心法模式</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-sichenbading');return false">四禅八定</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-yoga');return false">瑜伽行法</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-three-paths');return false">三条路径总判摄</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-sanskrit-terms');return false">梵汉术语比对</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('meditation',this);return false">⚙️ 技术面·工程面 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-stage1');return false">初阶·资粮道(发心)</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-stage2');return false">二阶·前行(内摄)</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-stage3');return false">三阶·正行(等持)</a>
    <a href="#" class="sub-sub-link" onclick="jxSubNav('meditation','med-stage3');return false">　⬦ 观照·能所分离→照住→照见</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('meditation',this);return false">📐 华严判教 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-wujiao');return false">贤首五教仪</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-yicheng');return false">一乘不共别圆</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-shizong');return false">十宗</a>
    <a href="#" class="sub-link" onclick="jxSubNav('meditation','med-futian');return false">宗派比较</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('chan_traces',this);return false">🌿 禅门实迹 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="jxSubNav('chan_traces','chan-academic');return false">全球学界视角</a>
    <a href="#" class="sub-link" onclick="jxSubNav('chan_traces','chan-practice');return false">门内实修视角</a>
    <a href="#" class="sub-link" onclick="jxSubNav('chan_traces','chan-modern');return false">近现代禅门</a>
    <a href="#" class="sub-link" onclick="jxSubNav('chan_traces','chan-haiyun');return false">海云法师·禅法</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('chengguan',this);return false">🌄 成其大观 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="jxSubNav('chengguan','cg-bio');return false">生平·法脉</a>
    <a href="#" class="sub-link" onclick="jxSubNav('chengguan','cg-works');return false">著作全目</a>
    <a href="#" class="sub-link" onclick="jxSubNav('chengguan','cg-lectures');return false">讲法·译经</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('vinaya',this);return false">📏 戒律拓扑 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="jxSubNav('vinaya','vy-overview');return false">律宗总览</a>
    <a href="#" class="sub-link" onclick="jxSubNav('vinaya','vy-founders');return false">祖师谱系</a>
    <a href="#" class="sub-link" onclick="jxSubNav('vinaya','vy-classics');return false">律典要目</a>
    <a href="#" class="sub-link" onclick="jxSubNav('vinaya','vy-history');return false">发展史</a>
    <a href="#" class="sub-link" onclick="jxSubNav('vinaya','vy-practice');return false">戒律实践</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('faxiang',this);return false">🔬 法相玄机 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="jxSubNav('faxiang',x-overview');return false">名相辨析</a>
    <a href="#" class="sub-link" onclick="jxSubNav('faxiang',x-india');return false">印度渊源</a>
    <a href="#" class="sub-link" onclick="jxSubNav('faxiang',x-lineage');return false">汉传法脉</a>
    <a href="#" class="sub-link" onclick="jxSubNav('faxiang',x-doctrine');return false">核心教义</a>
    <a href="#" class="sub-link" onclick="jxSubNav('faxiang',x-decline');return false">演变式微</a>
    <a href="#" class="sub-link" onclick="jxSubNav('faxiang',x-overseas');return false">域外传播</a>
    <a href="#" class="sub-link" onclick="jxSubNav('faxiang',x-revival');return false">近代复兴</a>
    <a href="#" class="sub-link" onclick="jxSubNav('faxiang',x-practice');return false">修行界视角</a>
    <a href="#" class="sub-link" onclick="jxSubNav('faxiang',x-academic');return false">学术前沿</a>
    </div></div>
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;switchPracticeView('resources',this);return false">📡 讲法资源 <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="jxSubNav('resources','res-avatamsaka');return false">华严经讲法全目</a>
    <a href="#" class="sub-link" onclick="jxSubNav('resources','res-mengcan');return false">梦参老和尚讲法总目</a>
    <a href="#" class="sub-link" onclick="jxSubNav('resources','res-total');return false">全网总目</a>
    <a href="#" class="sub-link" onclick="jxSubNav('resources','res-books');return false">著作</a>
    <a href="#" class="sub-link" onclick="jxSubNav('resources','res-yt');return false">YouTube</a>
    <a href="#" class="sub-link" onclick="jxSubNav('resources','res-temples');return false">道场</a>
    <a href="#" class="sub-link" onclick="jxSubNav('resources','res-more');return false">检索补遗</a>
    <a href="#" class="sub-link" onclick="jxSubNav('resources','res-news');return false">最新动态</a>
    </div></div>
    '''
    jx_html = build_simple_tab_page('教海行云 · 信解行证', 'jiaoxing', sidebar_jx, 'renderPractice();', view_id='practice-view')
    jx_path = TABS_OUT / 'jiaoxing.html'
    with open(jx_path, 'w', encoding='utf-8') as f:
        f.write(jx_html)
    size = len(jx_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {jx_path} ({size:,} bytes)')

    # ── Build Tab4: Frontier (restructured) ──
    sidebar_fr = '''
    <h3>🔬 前沿对话 <small style=font-size:0.65em;color:var(--text2)>Frontier Dialogues</small></h3>
    <div class="sidebar-group"><a href="#" class="nav-link active" onclick="switchFrontierNav('huayan',this);return false">🪷 与华严的对话 <small style=font-size:0.7em;color:var(--text2)>with Huayan</small></a></div>
    <div class="sidebar-group"><a href="#" class="nav-link" onclick="switchFrontierNav('chinese',this);return false">☸ 与汉传佛教的对话 <small style=font-size:0.7em;color:var(--text2)>Chinese Buddhism</small></a></div>
    <div class="sidebar-group"><a href="#" class="nav-link" onclick="switchFrontierNav('buddhist',this);return false">🕉 与佛教的对话 <small style=font-size:0.7em;color:var(--text2)>Buddhist Traditions</small></a></div>
    <div class="sidebar-group"><a href="#" class="nav-link" onclick="switchFrontierNav('others',this);return false">🌏 跨宗教对话 <small style=font-size:0.7em;color:var(--text2)>Interreligious</small></a></div>
    <div class="sidebar-group"><a href="#" class="nav-link" onclick="switchFrontierNav('litreview',this);return false">📑 文献综述 <small style=font-size:0.7em;color:var(--text2)>Lit. Review</small></a></div>
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
    <h3>🪷 世主妙严 <small style=font-size:0.65em;color:var(--text2)>Flower Treasury Cosmos</small></h3>
    <div class="sidebar-group"><a href="#co-mandala" class="nav-link active">🌊 华藏世界海 <small style=font-size:0.7em;color:var(--text2)>Ocean of Worlds</small></a></div>
    <div class="sidebar-group"><a href="#co-tower" class="nav-link">📐 三界诸天 <small style=font-size:0.7em;color:var(--text2)>Three Realms</small></a></div>
    <div class="sidebar-group"><a href="#co-art" class="nav-link">🎨 华严艺术珍品 <small style=font-size:0.7em;color:var(--text2)>Sacred Arts</small></a></div>
    <div class="sidebar-group"><a href="#co-chant" class="nav-link">🎵 梵呗·华严字母 <small style=font-size:0.7em;color:var(--text2)>Arapacana Chant</small></a></div>
    <div class="sidebar-group"><a href="#co-sites" class="nav-link">🗺 华严古迹巡礼 <small style=font-size:0.7em;color:var(--text2)>Heritage Sites</small></a></div>
    '''
    co_html = build_simple_tab_page('世主妙严 · 华藏世界海', 'cosmology', sidebar_co, 'if(typeof renderCosmology==="function")renderCosmology();')
    co_path = TABS_OUT / 'cosmology.html'
    with open(co_path, 'w', encoding='utf-8') as f:
        f.write(co_html)
    size = len(co_html.encode('utf-8'))
    total_size += size
    file_count += 1
    print(f'OK  {co_path} ({size:,} bytes)')

    # ── Build Tab6: Spirit (new) ──
    sidebar_sp = '''
    <h3>🌱 灵性仁本 <small style=font-size:0.65em;color:var(--text2)>Spiritual Humanism</small></h3>
    <div class="sidebar-group"><a href="#" class="nav-link active" onclick="SPIRIT_ACTIVE='overview';renderSpirit();return false">🌱 总览 <small style=font-size:0.7em;color:var(--text2)>Overview</small></a></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;SPIRIT_ACTIVE='spiritual_economics';renderSpirit();return false">💎 灵性经济学 <small style=font-size:0.7em;color:var(--text2)>Spiritual Economics</small> <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="SPIRIT_ACTIVE='spiritual_economics';renderSpirit();return false">海云法师体系</a>
    <a href="#" class="sub-link" onclick="SPIRIT_ACTIVE='spiritual_economics';renderSpirit();return false">灵性GDP·三世间框架</a>
    </div></div>
    <div class="sidebar-group"><a href="#" class="nav-link" onclick="SPIRIT_ACTIVE='humanistic_economics';renderSpirit();return false">📐 仁本·人本经济学 <small style=font-size:0.7em;color:var(--text2)>Humanistic Econ</small></a></div>
    <div class="sidebar-group"><a href="#" class="nav-link" onclick="SPIRIT_ACTIVE='contemplative_traditions';renderSpirit();return false">🧘 修行传统与永续 <small style=font-size:0.7em;color:var(--text2)>Traditions & Sustainability</small></a></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;SPIRIT_ACTIVE='indigenous_knowledge';renderSpirit();return false">🌏 本土知识 <small style=font-size:0.7em;color:var(--text2)>Indigenous Knowledge</small> <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="SPIRIT_ACTIVE='indigenous_knowledge';renderSpirit();return false">二十四节气·IPBES</a>
    <a href="#" class="sub-link" onclick="SPIRIT_ACTIVE='heritage_practice';renderSpirit();return false">遗产实践·活态传承</a>
    </div></div>
    <div class="sidebar-group has-subs">
    <a href="#" class="nav-link has-subs" onclick="if(!toggleSidebarGroup(this))return false;SPIRIT_ACTIVE='env_history';renderSpirit();return false">🌿 环境人文 <small style=font-size:0.7em;color:var(--text2)>Env. Humanities</small> <span class="toggle-arrow">▸</span></a>
    <div class="sub-links">
    <a href="#" class="sub-link" onclick="SPIRIT_ACTIVE='env_history';renderSpirit();return false">人类世·环境史</a>
    <a href="#" class="sub-link" onclick="SPIRIT_ACTIVE='critical_humanities';renderSpirit();return false">批判人文·多元世界</a>
    </div></div>
    <div class="sidebar-group"><a href="#" class="nav-link" onclick="SPIRIT_ACTIVE='practice';renderSpirit();return false">🙏 澄明永续实践 <small style=font-size:0.7em;color:var(--text2)>Luminous Practice</small></a></div>
    '''
    sp_html = build_simple_tab_page('灵性仁本 · 澄明永续', 'spirit', sidebar_sp, 'if(typeof renderSpirit==="function")renderSpirit();', view_id='spirit-view')
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
