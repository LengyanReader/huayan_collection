# -*- coding: utf-8 -*-
"""L.138 · 《九九華嚴》讲记校勘工作台 · 独立文章页构建器

用法：python scripts/build_jj_collation_page.py
读入：data/research/jj_huayan_lectures.yaml + jj_huayan_collation.yaml
      docs/经学文献/海云讲记_九九华严/README.md + episodes/ep01.md
产出：web/demo/articles/jj-huayan-collation.html（自包含 · 数据 inline · 无外部依赖）
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

import yaml

M = yaml.safe_load(io.open("data/research/jj_huayan_lectures.yaml", encoding="utf-8").read())
C = yaml.safe_load(io.open("data/research/jj_huayan_collation.yaml", encoding="utf-8").read())

# Merge
episodes = []
for cm in C["episodes"]:
    ep = cm["ep"]
    md = next((x for x in M["episodes_detail"] if x["ep"] == ep), {})
    episodes.append({
        "ep": ep,
        "segment": cm["segment"],
        "topic": cm["topic_zh"],
        "anchor_pin": cm.get("anchor_pin"),
        "anchor_juan": cm.get("anchor_juan"),
        "anchor_cbeta": cm.get("anchor_cbeta"),
        "collation_status": cm["collation_status"],
        "cross_ref": cm.get("cross_ref_series") or [],
        "notes": cm.get("notes", ""),
        "cues": md.get("cues"),
        "han": md.get("han_chars"),
        "coverage": round(md.get("coverage", 0) * 100, 1),
        "pipe": md.get("pipe_cues"),
        "declared_sec": md.get("declared_sec"),
        "video_id": md.get("video_id"),
        "url": md.get("url"),
        "calibration": md.get("calibration"),
    })

# Markdown to simple HTML (only for embedded Ep1 doc + README)
def md_to_html(md):
    # Escape first
    md = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Code blocks ```...```
    md = re.sub(r"```([\s\S]*?)```", lambda m: "<pre><code>" + m.group(1) + "</code></pre>", md)
    # Headings
    md = re.sub(r"^###### (.+)$", r"<h6>\1</h6>", md, flags=re.M)
    md = re.sub(r"^##### (.+)$", r"<h5>\1</h5>", md, flags=re.M)
    md = re.sub(r"^#### (.+)$", r"<h4>\1</h4>", md, flags=re.M)
    md = re.sub(r"^### (.+)$", r"<h3>\1</h3>", md, flags=re.M)
    md = re.sub(r"^## (.+)$", r"<h2>\1</h2>", md, flags=re.M)
    md = re.sub(r"^# (.+)$", r"<h1>\1</h1>", md, flags=re.M)
    # Horizontal rules
    md = re.sub(r"^---$", "<hr>", md, flags=re.M)
    # Blockquotes
    md = re.sub(r"^&gt; (.+)$", r"<blockquote>\1</blockquote>", md, flags=re.M)
    # Bold
    md = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", md)
    # Inline code
    md = re.sub(r"`([^`]+)`", r"<code>\1</code>", md)
    # Tables: |a|b|c|
    def table_repl(m):
        rows = [ln.strip() for ln in m.group(0).splitlines() if ln.strip().startswith("|")]
        if not rows:
            return m.group(0)
        out = ['<table class="md-table">']
        for i, row in enumerate(rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            if all(re.match(r"^:?-+:?$", c or "-") for c in cells):
                continue  # skip separator row
            tag = "th" if i == 0 else "td"
            out.append("<tr>" + "".join("<%s>%s</%s>" % (tag, c, tag) for c in cells) + "</tr>")
        out.append("</table>")
        return "\n".join(out)
    md = re.sub(r"(^(\|.*\|)\n)+", table_repl, md, flags=re.M)
    # Lists (simple)
    md = re.sub(r"^(\d+)\. (.+)$", r"<li><strong>\1.</strong> \2</li>", md, flags=re.M)
    md = re.sub(r"^- (.+)$", r"<li>\1</li>", md, flags=re.M)
    # Paragraphs: wrap lines that aren't already tags
    def para_repl(m):
        ln = m.group(1)
        if ln.strip().startswith("<") or not ln.strip():
            return ln
        return "<p>" + ln + "</p>"
    md = re.sub(r"^(.*)$", lambda m: para_repl(m), md, flags=re.M)
    return md


readme_md = io.open("docs/经学文献/海云讲记_九九华严/README.md", encoding="utf-8").read()
ep01_md = io.open("docs/经学文献/海云讲记_九九华严/episodes/ep01.md", encoding="utf-8").read()
ep02_path = "docs/经学文献/海云讲记_九九华严/episodes/ep02.md"
ep02_md = io.open(ep02_path, encoding="utf-8").read() if os.path.exists(ep02_path) else ""

DATA_JSON = json.dumps(episodes, ensure_ascii=False)
MEASURED_JSON = json.dumps(M.get("measured", {}), ensure_ascii=False)
README_HTML = md_to_html(readme_md)
EP01_HTML = md_to_html(ep01_md)
EP02_HTML = md_to_html(ep02_md) if ep02_md else ""

TEMPLATE = r"""<!DOCTYPE html>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>九九华严 · 讲记校勘工作台 · 独立文章</title>
<link rel="stylesheet" href="../css/common.css">
<style>
:root { --jj-teal: #4a8a8f; --jj-warn: #b48a5a; --jj-ok: #5c8d5c; }
.jj-hero { background: linear-gradient(135deg, rgba(74,138,143,0.10), rgba(94,139,158,0.06));
  padding: 22px 24px; border-radius: 10px; border: 1px solid var(--line); margin: 12px 0 18px; }
.jj-hero h1 { margin: 0 0 6px; color: var(--jj-teal); font-size: 1.5em; }
.jj-hero .sub { color: var(--text2); font-size: 0.9em; line-height: 1.6; }
.jj-hero .badges { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 8px; }
.badge { padding: 3px 10px; border-radius: 12px; font-size: 0.72em; background: rgba(74,138,143,0.14);
  color: var(--jj-teal); border: 1px solid rgba(74,138,143,0.28); }
.badge-warn { background: rgba(180,138,90,0.14); color: var(--jj-warn); border-color: rgba(180,138,90,0.32); }
.badge-ok { background: rgba(92,141,92,0.14); color: var(--jj-ok); border-color: rgba(92,141,92,0.32); }

.jj-toolbar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center;
  padding: 8px 0; margin: 8px 0 12px; border-bottom: 1px solid var(--line); }
.jj-toolbar button { padding: 5px 12px; font-size: 0.78em; border-radius: 6px;
  border: 1px solid var(--line); background: transparent; color: var(--text1); cursor: pointer; }
.jj-toolbar button.active { background: var(--jj-teal); color: #fff; border-color: var(--jj-teal); }

table.jj-eps { width: 100%; border-collapse: collapse; font-size: 0.82em; margin-top: 6px; }
table.jj-eps th { text-align: left; padding: 8px 10px; background: rgba(74,138,143,0.10);
  border-bottom: 2px solid var(--jj-teal); color: var(--text1); font-weight: 600; }
table.jj-eps td { padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
table.jj-eps tr:hover td { background: rgba(74,138,143,0.05); cursor: pointer; }
.seg-tag { display: inline-block; padding: 1px 8px; border-radius: 10px; font-size: 0.85em; }
.seg-玄談 { background: rgba(148,132,182,0.16); color: #7a5fa0; }
.seg-宏觀華嚴經 { background: rgba(212,164,80,0.16); color: #a07028; }
.seg-正行 { background: rgba(92,141,92,0.18); color: #3d6d3d; }
.stag-未啟 { color: var(--text2); }
.stag-待校 { color: var(--jj-warn); }
.stag-試點精校 { color: var(--jj-teal); font-weight: 600; }
.stag-已校 { color: var(--jj-ok); font-weight: 600; }

.jj-detail { margin-top: 20px; padding: 16px 20px; background: rgba(74,138,143,0.05);
  border-left: 3px solid var(--jj-teal); border-radius: 6px; }
.jj-detail h2 { color: var(--jj-teal); margin-top: 0; font-size: 1.15em; }
.jj-detail .kv { display: grid; grid-template-columns: 120px 1fr; gap: 4px 12px; font-size: 0.85em; margin: 8px 0 12px; }
.jj-detail .kv .k { color: var(--text2); }
.jj-detail .kv .v { color: var(--text1); }

.doc-panel { margin-top: 14px; padding: 12px 16px; background: rgba(255,255,255,0.4);
  border: 1px solid var(--line); border-radius: 8px; max-height: 720px; overflow-y: auto; }
.doc-panel h1 { font-size: 1.35em; color: var(--jj-teal); border-bottom: 2px solid var(--jj-teal); padding-bottom: 4px; }
.doc-panel h2 { font-size: 1.05em; color: var(--text1); margin-top: 22px; padding-left: 8px; border-left: 3px solid var(--jj-teal); }
.doc-panel h3 { font-size: 0.98em; color: var(--text1); margin-top: 16px; }
.doc-panel code { background: rgba(74,138,143,0.10); padding: 1px 5px; border-radius: 3px; font-size: 0.9em; }
.doc-panel pre { background: rgba(31,36,42,0.05); padding: 10px 12px; border-radius: 6px;
  overflow-x: auto; font-size: 0.82em; }
.doc-panel blockquote { border-left: 3px solid var(--jj-warn); padding: 6px 12px; margin: 8px 0;
  background: rgba(180,138,90,0.06); color: var(--text1); font-size: 0.9em; }
.doc-panel ul, .doc-panel ol { padding-left: 22px; }
.doc-panel .md-table { width: 100%; border-collapse: collapse; font-size: 0.82em; margin: 8px 0; }
.doc-panel .md-table th, .doc-panel .md-table td { border: 1px solid var(--line); padding: 4px 8px; text-align: left; vertical-align: top; }
.doc-panel .md-table th { background: rgba(74,138,143,0.10); }
.doc-panel hr { border: none; border-top: 1px dashed var(--line); margin: 16px 0; }

.tabbar { display: flex; gap: 4px; margin: 20px 0 0; border-bottom: 1px solid var(--line); }
.tabbar button { background: transparent; border: none; padding: 8px 14px; font-size: 0.85em;
  cursor: pointer; color: var(--text2); border-bottom: 2px solid transparent; }
.tabbar button.active { color: var(--jj-teal); border-bottom-color: var(--jj-teal); }
.tab-panel { display: none; }
.tab-panel.active { display: block; }

.footer-note { margin: 30px 0 12px; padding: 12px 16px; font-size: 0.75em; color: var(--text2);
  border-top: 1px dashed var(--line); }
</style>
</head>
<body>
<div id="page-top" style="position:sticky;top:0;z-index:100">
<header id="header">
  <a href="../index.html" class="back-link">&larr; Home</a>
  <h1>九九华严 · 讲记校勘工作台</h1>
  <span class="art-updated"></span>
  <button id="share-link" class="share-btn" onclick="copyPageLink();return false" title="复制本页独立地址">🔗 分享地址</button>
  <span style="margin-left:auto;font-size:0.7em;color:var(--text2);text-decoration:none">📄 独立文章页 · L.138</span>
</header>
<div style="background:rgba(180,138,90,0.10);border-bottom:1px solid rgba(180,138,90,0.30);padding:6px 16px;font-size:0.72em;color:var(--jj-warn);text-align:center">
⚠️ 本页为 <strong>OCR 重建稿之校订工作台</strong>·非定稿。所有引讲者口语均标〔OCR 待校〕；如需逐字引证·请先与讲义/录音互证。
</div>
<div style="padding:5px 16px;border-bottom:1px solid var(--line);font-size:0.76em;display:flex;gap:16px;align-items:center;background:rgba(94,139,158,0.06);flex-wrap:wrap">
  <a href="javascript:history.back()" style="color:var(--blue);text-decoration:none;font-weight:600">← 返回上一步</a>
  <span style="opacity:0.45">|</span>
  <a href="haiyun-lectures.html" style="color:var(--blue);text-decoration:none">相关：海云讲法 · 645 篇全库 reader ›</a>
  <span style="margin-left:auto;opacity:0.75;color:var(--text2)"><a href="../index.html" style="color:var(--text2);text-decoration:none">首页 ›</a></span>
</div>
</div>

<main class="content content-article" id="article-root">

<div class="jj-hero">
  <h1>《九九華嚴》2026 讲座 · 讲记校勘工作台</h1>
  <div class="sub">海雲繼夢法師 · 台北國際會議中心 · 依八十華嚴三十九品次第 · 官方 YouTube @huayen-world 硬字幕 OCR 重建 · 三源互证</div>
  <div class="badges" id="hero-badges"></div>
</div>

<div class="tabbar">
  <button class="active" data-tab="overview">📊 概览·14 集</button>
  <button data-tab="pilot">✒️ Ep 1 精校</button>
  <button data-tab="ep02">✒️ Ep 2 精校</button>
  <button data-tab="protocol">📖 凡例·体例</button>
</div>

<section id="tab-overview" class="tab-panel active">
  <div class="jj-toolbar">
    <span style="font-size:0.82em;color:var(--text2)">筛选：</span>
    <button class="fbtn active" data-fseg="all">全部</button>
    <button class="fbtn" data-fseg="玄談">玄談</button>
    <button class="fbtn" data-fseg="宏觀華嚴經">宏觀華嚴經</button>
    <button class="fbtn" data-fseg="正行">正行</button>
    <span style="width:16px"></span>
    <button class="fbtn active" data-fstat="all">全状态</button>
    <button class="fbtn" data-fstat="試點精校">試點精校</button>
    <button class="fbtn" data-fstat="待校">待校</button>
  </div>
  <div style="overflow-x:auto">
    <table class="jj-eps">
      <thead><tr>
        <th>集</th><th>segment</th><th>主题 / 品目 anchor</th>
        <th>状态</th><th>cues</th><th>汉字</th><th>覆盖</th><th>pipe</th><th>时长</th>
      </tr></thead>
      <tbody id="eps-body"></tbody>
    </table>
  </div>
  <div id="detail-holder"></div>
</section>

<section id="tab-pilot" class="tab-panel">
  <div class="doc-panel">
    <div id="ep01-body">__EP01_HTML__</div>
  </div>
</section>

<section id="tab-ep02" class="tab-panel">
  <div class="doc-panel">
    <div id="ep02-body">__EP02_HTML__</div>
  </div>
</section>

<section id="tab-protocol" class="tab-panel">
  <div class="doc-panel">
    <div id="readme-body">__README_HTML__</div>
  </div>
</section>

<div class="footer-note">
  <strong>数据源</strong>：
  <code>data/research/jj_huayan_lectures.yaml</code>（实测·自动生成）·
  <code>data/research/jj_huayan_collation.yaml</code>（编辑判断·人定）·
  <code>docs/经学文献/海云讲记_九九华严/episodes/ep01.md</code>（试点校订稿）·
  <code>docs/hy_refs/sub_extract/delivery/ep01.md … ep14.md</code>（OCR 初稿·不入 git）。
  <br><strong>批次</strong>：L.138 · 建立工作台骨架 + Ep 1 试点 · 后续 Ep 2–14 依 segment 分批。
</div>

</main>

<div id="share-toast" style="position:fixed;left:50%;bottom:36px;transform:translateX(-50%);background:rgba(31,36,42,0.96);color:#fff;padding:10px 18px;border-radius:8px;font-size:0.82em;display:none;z-index:999"></div>

<script src="../js/common.js"></script>
<script>
const EPISODES = __DATA_JSON__;
const MEASURED = __MEASURED_JSON__;

function fmtDur(sec){ if(!sec) return '—'; const h=Math.floor(sec/3600), m=Math.floor((sec%3600)/60); return h ? (h+'h'+String(m).padStart(2,'0')+'m') : (m+'m'); }

function renderBadges(){
  const b = document.getElementById('hero-badges');
  const total = EPISODES.length;
  const xuan = EPISODES.filter(e=>e.segment==='玄談').length;
  const hong = EPISODES.filter(e=>e.segment==='宏觀華嚴經').length;
  const zheng = EPISODES.filter(e=>e.segment==='正行').length;
  const pilot = EPISODES.filter(e=>e.collation_status==='試點精校').length;
  const cues = EPISODES.reduce((s,e)=>s+(e.cues||0),0);
  const han = MEASURED.total_han_chars || EPISODES.reduce((s,e)=>s+(e.han||0),0);
  b.innerHTML =
    '<span class="badge">共 '+total+' 集</span>'+
    '<span class="badge" style="background:rgba(148,132,182,0.16);color:#7a5fa0;border-color:rgba(148,132,182,0.30)">玄談 '+xuan+'</span>'+
    '<span class="badge" style="background:rgba(212,164,80,0.16);color:#a07028;border-color:rgba(212,164,80,0.30)">宏觀 '+hong+'</span>'+
    '<span class="badge" style="background:rgba(92,141,92,0.16);color:#3d6d3d;border-color:rgba(92,141,92,0.30)">正行 '+zheng+'</span>'+
    '<span class="badge badge-ok">試點精校 '+pilot+'</span>'+
    '<span class="badge">'+cues.toLocaleString()+' cues · '+han.toLocaleString()+' 汉字</span>';
}

let curFseg = 'all', curFstat = 'all';
function renderTable(){
  const tb = document.getElementById('eps-body');
  const rows = EPISODES.filter(e =>
    (curFseg==='all'||e.segment===curFseg) &&
    (curFstat==='all'||e.collation_status===curFstat)
  );
  tb.innerHTML = rows.map(e => {
    const segCls = 'seg-'+e.segment.replace(/\s/g,'');
    const stagCls = 'stag-'+e.collation_status;
    const anchor = e.anchor_pin ? ('<br><span style="color:var(--jj-teal);font-size:0.85em">▸ '+e.anchor_pin+' · '+e.anchor_juan+'</span>') : '';
    return '<tr data-ep="'+e.ep+'">'+
      '<td><strong>Ep '+String(e.ep).padStart(2,'0')+'</strong></td>'+
      '<td><span class="seg-tag '+segCls+'">'+e.segment+'</span></td>'+
      '<td>'+e.topic+anchor+'</td>'+
      '<td><span class="'+stagCls+'">'+e.collation_status+'</span></td>'+
      '<td>'+(e.cues||'—')+'</td>'+
      '<td>'+(e.han?e.han.toLocaleString():'—')+'</td>'+
      '<td>'+(e.coverage?e.coverage.toFixed(1)+'%':'—')+'</td>'+
      '<td>'+(e.pipe||'—')+'</td>'+
      '<td>'+fmtDur(e.declared_sec)+'</td>'+
    '</tr>';
  }).join('');
  Array.from(tb.querySelectorAll('tr')).forEach(tr => {
    tr.addEventListener('click', () => showDetail(parseInt(tr.dataset.ep,10)));
  });
}

function showDetail(ep){
  const e = EPISODES.find(x=>x.ep===ep);
  const holder = document.getElementById('detail-holder');
  if(!e){ holder.innerHTML=''; return; }
  const cross = e.cross_ref && e.cross_ref.length
    ? '<ul>'+e.cross_ref.map(p=>'<li><code>'+p+'</code></li>').join('')+'</ul>'
    : '<span style="color:var(--text2)">（无）</span>';
  const link = e.url ? ' <a href="'+e.url+'" target="_blank" rel="noopener" style="color:var(--jj-teal)">▶ 官方视频</a>' : '';
  holder.innerHTML =
    '<div class="jj-detail">'+
      '<h2>Ep '+String(e.ep).padStart(2,'0')+' · '+e.segment+' · '+e.collation_status+link+'</h2>'+
      '<div class="kv">'+
        '<div class="k">主题</div><div class="v">'+e.topic+'</div>'+
        '<div class="k">品目 anchor</div><div class="v">'+(e.anchor_pin||'—')+(e.anchor_juan?(' · '+e.anchor_juan):'')+'</div>'+
        '<div class="k">CBETA 回源</div><div class="v">'+(e.anchor_cbeta||'—')+'</div>'+
        '<div class="k">video_id</div><div class="v"><code>'+(e.video_id||'—')+'</code></div>'+
        '<div class="k">实测</div><div class="v">'+(e.cues||'—')+' cues · '+(e.han?e.han.toLocaleString():'—')+' 汉字 · 覆盖 '+(e.coverage?e.coverage.toFixed(1)+'%':'—')+' · pipe '+(e.pipe||'—')+' · '+fmtDur(e.declared_sec)+'</div>'+
        '<div class="k">细读 cross_ref</div><div class="v">'+cross+'</div>'+
        '<div class="k">按语</div><div class="v">'+(e.notes||'—')+'</div>'+
      '</div>'+
    '</div>';
  holder.scrollIntoView({behavior:'smooth', block:'nearest'});
}

document.querySelectorAll('.tabbar button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tabbar button').forEach(x=>x.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(x=>x.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-'+btn.dataset.tab).classList.add('active');
  });
});

document.querySelectorAll('.fbtn').forEach(btn => {
  btn.addEventListener('click', () => {
    if(btn.dataset.fseg !== undefined){
      document.querySelectorAll('.fbtn[data-fseg]').forEach(x=>x.classList.remove('active'));
      btn.classList.add('active');
      curFseg = btn.dataset.fseg;
    } else {
      document.querySelectorAll('.fbtn[data-fstat]').forEach(x=>x.classList.remove('active'));
      btn.classList.add('active');
      curFstat = btn.dataset.fstat;
    }
    renderTable();
  });
});

function copyPageLink(){
  var url = window.location.href;
  var toast = document.getElementById('share-toast');
  function done(msg, ok){
    toast.textContent = msg;
    toast.style.background = ok ? 'rgba(31,36,42,0.96)' : 'rgba(180,80,60,0.96)';
    toast.style.display = 'block';
    setTimeout(()=>{toast.style.display='none';}, 2200);
  }
  if(navigator.clipboard && window.isSecureContext){
    navigator.clipboard.writeText(url).then(()=>done('已复制本页地址', true), ()=>done('复制失败', false));
  } else {
    var t = document.createElement('textarea');
    t.value = url; t.style.position='fixed'; t.style.opacity='0';
    document.body.appendChild(t); t.select();
    try{ document.execCommand('copy'); done('已复制本页地址', true); }
    catch(e){ done('复制失败', false); }
    document.body.removeChild(t);
  }
}

renderBadges();
renderTable();
</script>
</body>
</html>
"""

out = (TEMPLATE
       .replace("__DATA_JSON__", DATA_JSON)
       .replace("__MEASURED_JSON__", MEASURED_JSON)
       .replace("__EP01_HTML__", EP01_HTML)
       .replace("__EP02_HTML__", EP02_HTML)
       .replace("__README_HTML__", README_HTML))

io.open("web/demo/articles/jj-huayan-collation.html", "w", encoding="utf-8", newline="\n").write(out)
_cjk = lambda s: len(re.findall(r"[\u4e00-\u9fff]", s))
print("已生成 web/demo/articles/jj-huayan-collation.html · %d bytes · %d 集 · Ep1 %d 漢字 · Ep2 %d 漢字 · README %d 漢字" % (
    len(out.encode("utf-8")), len(episodes), _cjk(ep01_md), _cjk(ep02_md), _cjk(readme_md)))
