#!/usr/bin/env python3
"""Build complete demo HTML from data files."""
import json, yaml, sys

# ── Load data ──
base = 'c:/DA_Practice/huayan_collection'
with open(f'{base}/data/knowledge_graph/personas.json', encoding='utf-8') as f:
    personas = json.load(f)
with open(f'{base}/data/knowledge_graph/lineages.json', encoding='utf-8') as f:
    lineages = json.load(f)
with open(f'{base}/data/knowledge_graph/locations.json', encoding='utf-8') as f:
    locations = json.load(f)
with open(f'{base}/data/translation/diff_matrix.yaml', encoding='utf-8') as f:
    diff = yaml.safe_load(f)

# ── Nodes ──
nodes = []
for p in personas['persons']:
    nodes.append({'id':p['id'],'n':p['name_zh'],'dy':p.get('dynasty',''),'ti':p.get('title','') or '',
                  'li':p.get('lineage_branch'),'tp':p.get('type','practitioner'),
                  'b':p.get('birth_year'),'d':p.get('death_year'),
                  'bio':(p.get('biography','')or'')[:150],'wk':(p.get('key_works')or[])[:2]})

# ── Edges ──
edges = []
for lin in lineages['lineages']:
    for e in lin['edges']:
        if e['from']==e['to']: continue
        r = e['relation']
        if r not in ('MASTER_OF','INFLUENCED','LINEAGE','CONTEMPORARY'): r='MASTER'
        edges.append({'s':e['from'],'t':e['to'],'r':r,'li':lin['name']})

# ── Locations ──
locs = []
for loc in locations['locations']:
    locs.append({'id':loc['id'],'n':loc['name_zh'],'lat':loc['lat'],'lng':loc['lng'],
                 'tp':loc.get('type','temple'),'dy':loc.get('dynasty',''),
                 'ds':(loc.get('description','')or'')[:120],'ps':loc.get('related_persons',[])})
locs.append({'id':'l_h','n':'南投大华严寺','lat':23.92,'lng':120.88,'tp':'temple','dy':'当代','ds':'海云继梦导师。普贤乘根本道场。','ps':['person_042']})
locs.append({'id':'l_f','n':'台北福慧寺','lat':24.98,'lng':121.42,'tp':'temple','dy':'当代','ds':'钦因长老住持。','ps':['person_041','person_043']})

# ── Colors ──
colors = {'华严五祖':'#b8863c','华严莲社':'#5e8b9e','月霞系':'#7a9ec0','李通玄系':'#c8893e','高丽华严':'#6d9a6e','日本华严':'#8b7a9e','贤首宗高原法系':'#c46b5d','临济宗':'#d48476','慈舟系':'#8b7a9e','译师':'#a09080','印度源流':'#9e8b6e','当代学者':'#b0a898','null':'#b0a898'}

GRAPH = json.dumps({'nodes':nodes,'edges':edges,'locations':locs,'lineage_colors':colors}, ensure_ascii=False)

# ── GAP data ──
gap_chs = []
for ch in diff.get('chapters',[]):
    dt = ch.get('diff_type','')
    if dt in ('A','B','C'):
        gap_chs.append({'bo':ch.get('order'),'z80':ch.get('order_zh_80'),'ti':ch.get('title_zh',''),
                        'sa':ch.get('title_sa',''),'tp':dt,'sm':(ch.get('diff_summary','')or'')[:150]})

GAP = json.dumps({'vs':[{'n':'藏文德格版 (Toh 44)','c':45,'v':'4册','t':'胜友、智军','p':'9世纪初'},{'n':'汉文八十华严 (T10n0279)','c':39,'v':'80卷','t':'实叉难陀','p':'699年'},{'n':'汉文六十华严 (T09n0278)','c':34,'v':'60卷','t':'佛驮跋陀罗','p':'420年'},{'n':'汉文四十华严 (T10n0293)','c':1,'v':'40卷','t':'般若','p':'798年'}],'sm':{'A':2,'B':3,'C':3,'D':1,'E':32},'cs':gap_chs,'wn':['⚠ 《最胜问菩萨十住除垢断结经》(T0309): 法藏明确判为非十住品亦非十地品']}, ensure_ascii=False)

# ── Build HTML ──
html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>华严宗 · 法脉全景</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
:root{--bg:#f6f2e8;--panel:#fdfaf3;--card:#fefdf9;--gold:#b8863c;--blue:#5e8b9e;--green:#7d9a6e;--red:#c46b5d;--text:#3d3427;--text2:#7a7262;--line:#e5ddd0}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);overflow:hidden;height:100vh;display:flex;flex-direction:column}
#header{background:linear-gradient(135deg,#e8e0d2,#efe6d8);padding:8px 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}
#header h1{font-size:1.1em;color:var(--gold);font-weight:600}
#header .sub{font-size:0.7em;color:var(--text2)}
#tabs{display:flex;background:var(--panel);border-bottom:1px solid var(--line);padding:0 14px}
#tabs button{padding:10px 20px;border:none;background:none;color:var(--text2);cursor:pointer;font-size:0.85em;border-bottom:3px solid transparent;transition:all 0.25s;font-weight:500}
#tabs button:hover{color:var(--text)}
#tabs button.active{color:var(--gold);border-bottom-color:var(--gold);font-weight:600}
.tab-content{display:none;flex:1;overflow:hidden}
.tab-content.active{display:flex;flex-direction:column}
#search-bar{display:flex;gap:6px;padding:6px 12px;background:var(--panel);border-bottom:1px solid var(--line);align-items:center}
#search-bar input{border:1px solid var(--line);border-radius:14px;padding:5px 12px;font-size:0.8em;background:var(--card);color:var(--text);width:220px;outline:none}
#main-row{display:flex;flex:1;min-height:0}
#tl-panel{flex:1;position:relative;background:var(--panel);overflow:hidden;min-width:0;cursor:grab}
#tl-panel canvas{display:block;position:absolute;top:0;left:0}
#side{width:380px;display:flex;flex-direction:column;min-width:240px;border-left:1px solid var(--line)}
#map-wrap{flex:1;min-height:200px;position:relative}
#map{width:100%;height:100%}
#info-box{background:var(--panel);border-top:1px solid var(--line);padding:14px 16px;font-size:0.82em;min-height:150px;overflow-y:auto;color:var(--text)}
#info-box .empty{text-align:center;color:var(--text2);padding-top:20px}
#info-box h3{color:var(--gold);font-size:1.1em;margin-bottom:4px}
#controls{background:var(--panel);padding:6px 12px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;border-top:1px solid var(--line)}
#controls button{padding:4px 12px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.73em;transition:all 0.2s}
#controls button:hover{background:#f0ebe0;color:var(--text);border-color:var(--gold)}
#controls button.active{background:var(--gold);color:#fff;border-color:var(--gold)}
#tl-tooltip{position:absolute;background:var(--card);color:var(--text);padding:10px 14px;border-radius:8px;font-size:0.82em;pointer-events:none;opacity:0;transition:opacity 0.15s;max-width:300px;z-index:100;box-shadow:0 4px 14px rgba(60,40,20,0.14);border:1px solid var(--line)}
#tl-tooltip h3{color:var(--gold);margin-bottom:3px}
.leaflet-popup-content{font-size:0.85em;color:var(--text)}
.leaflet-popup-content b{color:var(--gold)}
#gap-view,#practice-view{flex:1;background:var(--bg);overflow-y:auto;padding:22px 26px}
.section{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:16px;width:100%}
.section h2{color:var(--gold);font-size:1.05em;margin-bottom:6px}
.v-table{width:100%;border-collapse:collapse;font-size:0.82em}
.v-table th{background:linear-gradient(180deg,#f5efe4,#efe6d8);color:var(--text);padding:8px 10px;text-align:left;font-weight:600}
.v-table td{padding:7px 10px;border-bottom:1px solid var(--line)}
.badge{padding:2px 8px;border-radius:10px;font-size:0.7em;font-weight:600}
.bA{color:var(--red)} .bB{color:#c8893e} .bC{color:#a08020} .bD{color:var(--blue)} .bE{color:var(--green)}
.miss{color:var(--red);font-weight:600}
.tag{display:inline-block;padding:2px 8px;border-radius:10px;font-size:0.78em;font-weight:600;margin:2px 4px}
.stage-box{border-left:4px solid var(--gold);padding:8px 14px;margin:8px 0;background:rgba(200,150,60,0.04);border-radius:0 8px 8px 0;font-size:0.85em;line-height:1.7}
.stage-box b{color:var(--gold)}
@media(max-width:768px){body{overflow:auto}#header h1{font-size:0.9em}#header .sub{display:none}#main-row{flex-direction:column}#tl-panel{height:50vh;min-height:300px}#side{width:100%!important;flex-direction:row}#map-wrap{height:30vh}#controls button{font-size:0.65em}}
</style>
</head>
<body>

<div id="header"><div><h1>华严宗部文献与修行资料</h1><span class="sub">贤首宗法脉传承 (557–2024) &nbsp;|&nbsp; 藏汉华严经差异总览</span></div></div>

<div id="tabs">
  <button data-tab="practice">🧘 华严行法</button>
  <button class="active" data-tab="lineage">🌊 法脉传承</button>
  <button data-tab="gap">📜 汉藏差异</button>
</div>

<div id="tab-practice" class="tab-content"><div id="practice-view"></div></div>

<div id="tab-lineage" class="tab-content active">
  <div id="search-bar"><input type="text" id="search-input" placeholder="🔍 检索人物、地点…"><span style="font-size:0.7em;color:var(--text2)">点击人物寿命条 | 滚轮缩放 | 拖拽平移</span></div>
  <div id="main-row">
    <div id="tl-panel"><canvas id="tl-canvas"></canvas><div id="tl-tooltip"></div></div>
    <div id="side">
      <div id="map-wrap"><div id="map"></div></div>
      <div id="info-box"><div class="empty">👆 点击时间轴上的人物寿命条</div></div>
    </div>
  </div>
  <div id="controls">
    <span style="font-size:0.7em;color:var(--text2)">法系:</span>
    <button class="active" data-filter="all">全部</button>
    <button data-filter="华严五祖">五祖</button>
    <button data-filter="贤首宗高原法系">高原法系</button>
    <button data-filter="华严莲社">华严莲社</button>
    <button data-filter="月霞系">月霞系</button>
    <button id="reset-btn" style="margin-left:auto;border:1px solid var(--gold);color:var(--gold)">↺ 重置</button>
  </div>
</div>

<div id="tab-gap" class="tab-content"><div id="gap-view"></div></div>

<script>
// ═══ DATA ═══
var GRAPH = __GRAPH__;
var GAP = __GAP__;
var DATA=GRAPH, map=null, selectedId=null, searchQuery="";
var tl={canvas:null,ctx:null,W:0,H:0,ox:0,oy:0,scale:1,minX:100,maxX:2060,rows:[],hitRects:[],drag:false,lastX:0};
var nodeMap={}; DATA.nodes.forEach(function(n){nodeMap[n.id]=n;});

// ═══ HELPERS ═══
function getPersonLocs(pid){return DATA.locations.filter(function(l){return (l.ps||[]).indexOf(pid)>=0;});}
function buildTimelineRows(){
  var order=["华严五祖","李通玄系","日本华严","高丽华严","贤首宗高原法系","月霞系","华严莲社","慈舟系","临济宗","译师","印度源流","当代学者"];
  var rows={}; order.forEach(function(l,i){rows[l]=i;});
  var rd=order.map(function(l){return {lineage:l,ps:[],y:0,color:DATA.lineage_colors[l]||"#b0a898"};});
  DATA.nodes.forEach(function(n){
    var ri=rows[n.li]!==undefined?rows[n.li]:order.length;
    if(!rd[ri])rd[ri]={lineage:n.li||"other",ps:[],y:0,color:DATA.lineage_colors[n.li]||"#b0a898"};
    rd[ri].ps.push(n);
  });
  tl.rows=rd.filter(function(r){return r.ps.length>0;});
}
buildTimelineRows();

// ═══ CANVAS ═══
function resizeTL(){var p=document.getElementById("tl-panel");tl.W=p.clientWidth;tl.H=p.clientHeight;tl.canvas=document.getElementById("tl-canvas");tl.canvas.width=tl.W;tl.canvas.height=tl.H;tl.canvas.style.width=tl.W+"px";tl.canvas.style.height=tl.H+"px";tl.ctx=tl.canvas.getContext("2d");}
function tX(y){return (y-tl.minX)*tl.scale+tl.ox;}

function drawTL(hlId){
  var ctx=tl.ctx,W=tl.W,H=tl.H;if(!ctx)return;ctx.clearRect(0,0,W,H);var rh=H/Math.max(tl.rows.length,1);
  [{n:"唐",s:618,e:907,c:"rgba(200,160,80,0.08)"},{n:"宋",s:960,e:1279,c:"rgba(150,170,190,0.08)"},{n:"明",s:1368,e:1644,c:"rgba(160,150,140,0.06)"},{n:"清",s:1644,e:1912,c:"rgba(150,140,130,0.06)"},{n:"近现代",s:1912,e:1949,c:"rgba(200,150,140,0.1)"},{n:"当代",s:1949,e:2026,c:"rgba(150,190,190,0.1)"}].forEach(function(d){var x=tX(d.s),x2=tX(d.e);if(x2>0&&x<W){ctx.fillStyle=d.c;ctx.fillRect(Math.max(0,x),0,Math.min(W,x2-x),H);}});
  ctx.strokeStyle="#e8e0d0";ctx.lineWidth=0.5;
  for(var y=200;y<=2050;y+=100){var x=tX(y);if(x>=0&&x<=W){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}}
  tl.rows.forEach(function(r,i){r.y=(i*rh+rh*0.5);var y2=r.y;if(i%2===0){ctx.fillStyle="rgba(255,255,255,0.3)";ctx.fillRect(0,y2-rh/2,W,rh);}ctx.fillStyle=r.color;ctx.font="bold 11px Microsoft YaHei";ctx.fillText(r.lineage,6,y2-rh/2+14);});
  tl.hitRects=[];var ds=25,isSearch=searchQuery.length>0;
  tl.rows.forEach(function(r,ri){var y2=r.y;r.ps.forEach(function(p){
    var b=p.b||(p.d?p.d-ds:null),d=p.d||(p.b?p.b+ds:null);if(!b&&!d)return;
    var bx=tX(b||d-10),dx=tX(d||b+10),bh=Math.min(rh*0.5,20),by=y2-bh/2;
    var isHL=p.id===hlId,matches=!isSearch||p.n.indexOf(searchQuery)>=0;
    if(isSearch&&!matches)ctx.globalAlpha=0.12;else if(hlId&&!isHL)ctx.globalAlpha=0.2;else ctx.globalAlpha=1;
    if(isHL){ctx.shadowColor="#b8863c";ctx.shadowBlur=14;}
    ctx.fillStyle=isHL?"#c46b5d":(r.color+"DD");var rx=Math.max(0,bx),rw=Math.max(6,dx-rx);
    ctx.beginPath();ctx.moveTo(rx+4,by);ctx.lineTo(rx+rw-4,by);ctx.quadraticCurveTo(rx+rw,by,rx+rw,by+4);ctx.lineTo(rx+rw,by+bh-4);ctx.quadraticCurveTo(rx+rw,by+bh,rx+rw-4,by+bh);ctx.lineTo(rx+4,by+bh);ctx.quadraticCurveTo(rx,by+bh,rx,by+bh-4);ctx.lineTo(rx,by+4);ctx.quadraticCurveTo(rx,by,rx+4,by);ctx.closePath();ctx.fill();
    ctx.shadowColor="transparent";ctx.shadowBlur=0;ctx.globalAlpha=1;
    if(!isSearch||matches){ctx.fillStyle=isHL?"#c46b5d":"#5c5040";ctx.font=(isHL?"bold ":"")+(isHL?12:10)+"px Microsoft YaHei";ctx.fillText(p.n,rx+rw+4,by+bh*0.72);}
    tl.hitRects.push({x:rx,y:by,w:rw,h:bh,person:p});
  });});
  tl.hitRects.forEach(function(hr){var p=hr.person;
    DATA.edges.filter(function(e){return e.s===p.id&&(e.r==="MASTER"||e.r==="LINEAGE");}).forEach(function(e){var tHR=tl.hitRects.find(function(h){return h.person.id===e.t;});if(!tHR)return;var isHL=p.id===hlId||e.t===hlId;ctx.strokeStyle=isHL?"#b8863c":"#d5cdc0";ctx.lineWidth=isHL?2:1;ctx.globalAlpha=isHL?1:0.45;ctx.setLineDash(e.r==="LINEAGE"?[5,4]:[]);ctx.beginPath();var sx=hr.x+hr.w,sy=hr.y+hr.h/2,ex=tHR.x,ey=tHR.y+tHR.h/2;ctx.moveTo(sx,sy);ctx.bezierCurveTo(sx+(ex-sx)*0.4,sy,ex-(ex-sx)*0.4,ey,ex,ey);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;});
  });
  ctx.fillStyle="#a09080";ctx.font="10px Microsoft YaHei";
  for(var y=200;y<=2000;y+=100){var x=tX(y);if(x>=0&&x<=W)ctx.fillText(y,x-12,H-8);}
  [{y:420,l:"六十华严译出",c:"#b8863c"},{y:699,l:"八十华严译出",c:"#b8863c"},{y:845,l:"唐武宗灭佛",c:"#c46b5d"},{y:1085,l:"义天入宋求法",c:"#6d9a6e"},{y:1914,l:"华严大学创立",c:"#5e8b9e"},{y:1952,l:"华严莲社创社",c:"#5e8b9e"},{y:2008,l:"钦因传衣钵",c:"#c46b5d"}].forEach(function(ev){var x=tX(ev.y);if(x<0||x>W)return;ctx.fillStyle=ev.c;ctx.font="bold 9px Microsoft YaHei";ctx.fillText("▸ "+ev.l,x,18);});
}

// ═══ MAP ═══
function initMap(){
  if(map){map.invalidateSize();return;}
  if(typeof L==="undefined"){document.getElementById("map").innerHTML="<div style=display:flex;align-items:center;justify-content:center;height:100%;color:var(--text2)>🗺 地图未加载</div>";return;}
  map=L.map("map",{zoomControl:true}).setView([33,110],4);
  L.tileLayer("https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",{subdomains:["1","2","3","4"],maxZoom:18}).addTo(map);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{subdomains:["a","b","c"],maxZoom:19,opacity:0.5}).addTo(map);
  var mc={temple:"#b8863c",mountain:"#7d9a6e",region:"#c46b5d"};
  DATA.locations.forEach(function(loc){
    var names=(loc.ps||[]).map(function(pid){var n=nodeMap[pid];return n?n.n:"";}).filter(Boolean).join("、");
    var m=L.circleMarker([loc.lat,loc.lng],{radius:9,fillColor:mc[loc.tp]||"#b0a898",color:"#fff",weight:2,fillOpacity:0.9});
    m.addTo(map).bindPopup("<b>"+loc.n+"</b><br>"+(loc.dy||"")+"<br>"+(loc.ds||"")+(names?"<br>👤 "+names:""));
    m._ld=loc;m.on("click",function(){if(loc.ps&&loc.ps.length>0)selectPerson(loc.ps[0]);});
  });
}

// ═══ SELECTION ═══
function selectPerson(id){
  selectedId=id;drawTL(id);
  var p=nodeMap[id];if(!p)return;
  var lc=DATA.lineage_colors[p.li]||"#b0a898";
  var locs=getPersonLocs(id),locHTML="";
  locs.forEach(function(l){locHTML+="📍 "+l.n+"<br>";});
  var teachers=DATA.edges.filter(function(e){return e.t===id&&e.r==="MASTER";}).map(function(e){return nodeMap[e.s];}).filter(Boolean);
  var students=DATA.edges.filter(function(e){return e.s===id&&e.r==="MASTER";}).map(function(e){return nodeMap[e.t];}).filter(Boolean);
  var tch=teachers.length?"⬆ 师承: "+teachers.map(function(t){return t.n;}).join("、")+"<br>":"";
  var std=students.length?"⬇ 传法: "+students.map(function(t){return t.n;}).join("、")+"<br>":"";
  document.getElementById("info-box").innerHTML="<h3>"+p.n+"</h3>"
    +"<span class=tag style=background:"+lc+"20;color:"+lc+">"+(p.li||"—")+"</span> "
    +"<span class=tag style=background:rgba(0,0,0,0.04)>"+(p.tp||"—")+"</span><br>"
    +"📅 "+(p.dy||"?")+" · "+(p.b||"?")+"–"+(p.d||"?")+"<br>"
    +"🏛 "+(p.ti||"")+"<br>"
    +locHTML+tch+std
    +(p.bio?"<div style=color:var(--text2);line-height:1.5;margin-top:4px>"+p.bio+"</div>":"")
    +(p.wk&&p.wk.length?"📖 "+p.wk.join(" · "):"");
  if(map&&locs.length>0){var loc=locs[0];map.flyTo([loc.lat,loc.lng],locs.length===1?10:8,{duration:0.8});}
}
function clearSelection(){selectedId=null;drawTL(null);document.getElementById("info-box").innerHTML="<div class=empty>👆 点击时间轴上的人物寿命条</div>";}

// ═══ INTERACTION ═══
function onWheel(e){e.preventDefault();var p=document.getElementById("tl-panel");var r=p.getBoundingClientRect();var mx=e.clientX-r.left;var before=(mx-tl.ox)/tl.scale;tl.scale*=e.deltaY<0?1.12:0.89;tl.scale=Math.max(0.12,Math.min(6,tl.scale));tl.ox=mx-before*tl.scale;drawTL(selectedId);}
function onMD(e){if(e.target.tagName==="CANVAS"){tl.drag=true;tl.lastX=e.clientX;}}
function onMM(e){
  if(!tl.drag){
    var p=document.getElementById("tl-panel"),r=p.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
    var hit=tl.hitRects.find(function(h){return mx>=h.x&&mx<=h.x+h.w&&my>=h.y&&my<=h.y+h.h;});
    var tip=document.getElementById("tl-tooltip");
    if(hit){var pp=hit.person;tip.style.opacity="1";tip.innerHTML="<h3>"+pp.n+"</h3>"+(pp.ti||"")+" · "+pp.dy+" · "+(pp.b||"?")+"–"+(pp.d||"?");tip.style.left=(e.pageX+14)+"px";tip.style.top=(e.pageY-20)+"px";}
    else{tip.style.opacity="0";}
    return;
  }
  var dx=e.clientX-tl.lastX;tl.ox+=dx;tl.lastX=e.clientX;drawTL(selectedId);
}
function onMU(){tl.drag=false;}
function onClick(e){
  if(tl.drag||Math.abs(e.clientX-tl.lastX)>3)return;
  var p=document.getElementById("tl-panel"),r=p.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  var hit=tl.hitRects.find(function(h){return mx>=h.x&&mx<=h.x+h.w&&my>=h.y&&my<=h.y+h.h;});
  if(hit){selectPerson(hit.person.id);}else{clearSelection();}
}

// ═══ TABS ═══
document.getElementById("tabs").addEventListener("click",function(e){
  if(e.target.tagName!=="BUTTON")return;
  document.querySelectorAll("#tabs button").forEach(function(b){b.classList.remove("active");});
  e.target.classList.add("active");
  document.querySelectorAll(".tab-content").forEach(function(t){t.classList.remove("active");});
  document.getElementById("tab-"+e.target.dataset.tab).classList.add("active");
  if(e.target.dataset.tab==="lineage"){setTimeout(function(){resizeTL();drawTL(selectedId);if(map)map.invalidateSize();},200);}
});

// ═══ GAP TAB ═══
function renderGap(){
  var gv=document.getElementById("gap-view");if(!gv)return;
  var h="<h2 style=color:var(--gold)>📜 版本对照</h2><div class=section><table class=v-table><tr><th>版本</th><th>品目</th><th>卷/册</th><th>译者</th><th>年代</th></tr>";
  GAP.vs.forEach(function(v){h+="<tr><td>"+v.n+"</td><td style=font-weight:700;color:var(--gold)>"+v.c+"</td><td>"+v.v+"</td><td>"+v.t+"</td><td>"+v.p+"</td></tr>";});
  h+="</table></div>";
  var ds={A:{i:"🔴",l:"藏文独有品目",c:"#c46b5d",d:"汉文三译完全缺失"},B:{i:"🟠",l:"内容实质性参差",c:"#c8893e",d:"同名品内容有显著差异"},C:{i:"🟡",l:"结构/开合不同",c:"#a08020",d:"品目序号名称开合不同"},D:{i:"🔵",l:"品目级微小差异",c:"#5e8b9e",d:"个别段落不同"},E:{i:"🟢",l:"汉藏基本对应",c:"#7d9a6e",d:"32品大致一致"}};
  h+="<h2 style=color:var(--gold)>📊 差异分布 (藏文45品 vs 汉文39品)</h2><div class=section style=display:flex;gap:10px;flex-wrap:wrap>";
  ["A","B","C","D","E"].forEach(function(t){var d=ds[t];h+="<span style=flex:1;min-width:130px;background:var(--card);border-radius:10px;padding:14px;text-align:center;border:1px solid var(--line);border-left:3px solid "+d.c+"><div style=font-size:1.3em>"+d.i+"</div><div style=font-size:2em;font-weight:700;color:"+d.c+">"+(GAP.sm[t]||0)+"</div><div style=font-weight:600>"+d.l+"</div><div style=font-size:0.8em;color:var(--text2)>"+d.d+"</div></span>";});
  h+="</div>";
  h+="<h2 style=color:var(--gold)>📋 逐品差异详情</h2><div class=section><table class=v-table><tr><th>藏文#</th><th>八十华严#</th><th>品名</th><th>类型</th><th>差异说明</th></tr>";
  GAP.cs.forEach(function(ch){var b="badge b"+ch.tp;h+="<tr><td>"+(ch.bo||"—")+"</td><td>"+(ch.z80||"<span class=miss>✗</span>")+"</td><td>"+ch.ti+(ch.sa?" <span style=font-size:0.8em;color:var(--text2)>"+ch.sa+"</span>":"")+"</td><td><span class='"+b+"'>"+ch.tp+"</span></td><td style=font-size:0.8em>"+(ch.sm||"")+"</td></tr>";});
  h+="</table></div>";
  h+="<h2 style=color:var(--gold)>🗺 对译优先级</h2><div class=section><p><b style=color:#c46b5d>P0</b> Ch.11 如来华严品 · Ch.28 普贤宣说品 — 汉文全缺</p><p><b style=color:#c8893e>P1</b> Ch.27 十地品 · Ch.40 离世间品 — 内容参差</p></div>";
  GAP.wn.forEach(function(w){h+="<div style=background:rgba(196,107,93,0.05);border:1px solid rgba(196,107,93,0.2);border-radius:8px;padding:8px 12px;margin:4px 0;font-size:0.8em;color:var(--red)>"+w+"</div>";});
  gv.innerHTML=h;
}

// ═══ PRACTICE TAB ═══
function renderPractice(){
  var pv=document.getElementById("practice-view");if(!pv)return;
  pv.innerHTML="<div class=section><h2>🧘 华严行法 — 修行蓝图</h2><p style=line-height:1.8>参考大华严寺海云继梦和上所立 <b>普贤乘华严宗</b> 修行体系。以华严禅法为核心，透过<b>心法工程</b>止住安心、令真心起作用。</p></div>"
  +"<div class=section><h2>📐 修行三阶段</h2>"
  +"<div class=stage-box><b>一、资粮道 — 发心工程</b><br>三门必修: 人格健康、出离心、菩提心。技术面: 纯化禅(动→静)→象限转移→瞬间定。工程面: 心性培养+戒律基础。</div>"
  +"<div class=stage-box><b>二、前行 — 内摄工程（界内定）</b><br>核心: 安那般那数息观(数·随·止·观·还·净)。四种观法: 唯心识观→真如实现→毗婆舍那→奢摩他。禅定次第: 四天王定(初信)→忉利定(二信)→欲界定→色界定→无色界定。</div>"
  +"<div class=stage-box><b>三、正行 — 等持工程（界外定）</b><br>前半程: 三摩呬多(Samāhita)。后半程: 三摩钵底(Samāpatti)。究竟: 三摩地(Samādhi)。依杜顺法界三观，透过海印三昧呈现华严境界。</div>"
  +"</div>"
  +"<div class=section><h2>📊 十信法门·前行对应</h2><table class=v-table><tr><th>信位</th><th>禅定</th><th>法位</th><th>观法</th><th>关键检验</th></tr>"
  +"<tr><td>初信</td><td>四天王定</td><td>煖法</td><td>唯心识观·自省三业</td><td>觉醒生命意义</td></tr>"
  +"<tr><td>二信</td><td>忉利定</td><td>顶法</td><td>观妄念所由生</td><td>确认菩提心·收心工程</td></tr>"
  +"<tr><td>三信</td><td>欲界定</td><td>忍法</td><td>轻安三相</td><td>菩提心稳定·摄众共修</td></tr>"
  +"<tr><td>四信</td><td>未到定</td><td>世第一法</td><td>安般守意</td><td>置心风门·心不散乱</td></tr>"
  +"<tr><td>五~十信</td><td>色界·无色界定</td><td>—</td><td>奢摩他·毗婆舍那</td><td>舍妄念→入界外定</td></tr>"
  +"</table></div>"
  +"<div class=section><h2>🎯 核心禅法</h2><p style=line-height:1.8><b>根本行法:</b> 安那般那(Ānāpāna)数息观—六妙门(数·随·止·观·还·净)。<b>置心一处:</b> 端身正坐，置心风门；使心不乱，若心他缘，摄心令返。<b>参禅金三角:</b> 置心一处·放下着·吸闭吐。<b>法界三观:</b> 真空绝相观→理事无碍观→周遍含融观。<b>东山法门:</b> 海云继梦复兴失传八百余年的身—息—心观行次第。</p><p style=color:var(--gold);margin-top:8px><b>海云法语:</b> 「听经就是要你去实践！知道不算，做到才算。」— 禅是自在的境界。</p></div>"
  +"<div class=section><h2>📖 讲法资源</h2><p style=line-height:1.8>🎙 Apple Podcast/Spotify: 普贤乘华严宗 | 🌐 大华严寺: huayenworld.org</p><p style=font-size:0.82em;color:var(--text2)><b>系列讲法(23个系列):</b> S3 华严禅行法 · S8 禅与入定 · S9 东山法门与禅宗的特色 · S2 华严经教与行法</p><p style=font-size:0.82em;color:var(--text2)><b>核心著作:</b> 《迈向佛陀的境界》《禅，怎么参？》《煖身：华严禅修入门》《禅修正行》</p></div>"
  +"<div class=section><h2>🏛 相关道场</h2><p style=line-height:1.8>📍 南投大华严寺 — 海云继梦导师·普贤乘根本道场<br>📍 台北福慧寺 — 钦因长老·高原法系在台道场<br>📍 台北华严莲社 — 贤度法师·华严专宗学院</p></div>";
}

// ═══ INIT ═══
resizeTL();
drawTL(null);
initMap();
renderGap();
renderPractice();

// Events
document.getElementById("search-input").addEventListener("input",function(){searchQuery=this.value.trim();drawTL(selectedId);});
var panel=document.getElementById("tl-panel");
panel.addEventListener("wheel",onWheel,{passive:false});
panel.addEventListener("mousedown",onMD); panel.addEventListener("mousemove",onMM);
panel.addEventListener("mouseup",onMU); panel.addEventListener("mouseleave",onMU);
panel.addEventListener("click",onClick);
panel.addEventListener("touchstart",function(e){if(e.touches.length===1){tl.drag=true;tl.lastX=e.touches[0].clientX;}e.preventDefault();},{passive:false});
panel.addEventListener("touchmove",function(e){if(tl.drag){var dx=e.touches[0].clientX-tl.lastX;tl.ox+=dx;tl.lastX=e.touches[0].clientX;drawTL(selectedId);}e.preventDefault();},{passive:false});
panel.addEventListener("touchend",function(){tl.drag=false;});

// Controls
document.getElementById("reset-btn").addEventListener("click",function(){clearSelection();searchQuery="";document.getElementById("search-input").value="";tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);if(map)map.setView([33,110],4);});
document.querySelectorAll("#controls button[data-filter]").forEach(function(btn){btn.addEventListener("click",function(){
  document.querySelectorAll("#controls button[data-filter]").forEach(function(b){b.classList.remove("active");});
  btn.classList.add("active");
  var lin=btn.dataset.filter;
  if(lin==="all"){clearSelection();return;}
  var ids=DATA.nodes.filter(function(n){return n.li===lin;}).map(function(n){return n.id;});
  if(ids.length>0)selectPerson(ids[0]);
});});

// Final: set viewport & draw
tl.ox=20; tl.scale=(tl.W-40)/(tl.maxX-tl.minX); drawTL(null);
</script>
</body>
</html>'''

html = html.replace('__GRAPH__', GRAPH).replace('__GAP__', GAP)

with open(f'{base}/web/demo/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Built: {len(html):,} bytes')
print(f'Nodes: {len(nodes)}, Edges: {len(edges)}, Locs: {len(locs)}')
print(f'OK')
