/* 华严经群关系网络 · 内嵌交互渲染器（无外部依赖）
   由 build.py 注入：window.DAZANG_GRAPH + 本脚本。
   挂载点：<div id="dazang-graph-inline"></div>
*/
(function () {
  'use strict';

  var TYPE_NAME = {version:"版本", pin:"品", tib:"藏章", text:"异译", cluster:"簇", commentary:"注疏", work:"经论", canon_class:"部类", commentary_hub:"合计"};
  var TYPE_COLOR = {version:"#8b5e34", pin:"#b5651d", tib:"#4f6f52", text:"#2f5d7c", cluster:"#7a6a9a", commentary:"#2f5d7c", work:"#4f6f52", canon_class:"#a87900", commentary_hub:"#b03a2e"};
  var TYPE_R = {version:13, pin:5, tib:3.2, text:4.6, cluster:10, commentary:9, work:8, canon_class:7, commentary_hub:14};
  var EDGE_NAME = {contains:"contains", contains_60:"contains_60", parallel:"parallel", translation:"translation", related:"related", belongs:"belongs", unique:"unique", survives:"survives", sums_to:"sums_to", cites:"cites", cites_class:"cites_class"};
  var EDGE_GROUP = {contains:"structural", contains_60:"structural", belongs:"structural", unique:"structural", survives:"structural", parallel:"parallel", translation:"translation", related:"related", sums_to:"citation", cites:"citation", cites_class:"citation"};
  var EDGE_COLOR = {contains:"#8b5e34", contains_60:"#2f5d7c", parallel:"#bab2a3", translation:"#b5651d", related:"#b03a2e", belongs:"rgba(120,110,90,.30)", unique:"#b03a2e", survives:"#b03a2e", sums_to:"#2f5d7c", cites:"#4f6f52", cites_class:"#a87900"};
  var EDGE_DASH = {contains_60:[5,4], related:[4,3], survives:[2,3]};
  var CSS = ''
    + '#dazang-graph-inline{position:relative;border:1px solid var(--line,#d8d0c0);border-radius:8px;background:#fbf8f1;margin:1.2rem 0;overflow:hidden}'
    + '#dazang-graph-inline.dg-full{position:fixed;inset:12px;z-index:9999;margin:0;box-shadow:0 18px 60px rgba(0,0,0,.35)}'
    + '#dazang-graph-inline .dg-bar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:7px 10px;border-bottom:1px solid #e4dccb;font-size:.72rem;background:rgba(255,255,255,.55)}'
    + '#dazang-graph-inline .dg-bar .dg-g{display:flex;align-items:center;gap:4px;padding-right:8px;border-right:1px solid #e4dccb}'
    + '#dazang-graph-inline .dg-bar .dg-g:last-child{border-right:0}'
    + '#dazang-graph-inline button{font:inherit;font-size:.72rem;padding:2px 7px;border:1px solid #d8d0c0;background:#fff;color:#2b2b2b;border-radius:4px;cursor:pointer}'
    + '#dazang-graph-inline button:hover{border-color:#8b5e34}'
    + '#dazang-graph-inline button.on{background:#8b5e34;color:#fff;border-color:#8b5e34}'
    + '#dazang-graph-inline label.dg-chk{display:inline-flex;align-items:center;gap:3px;color:#6b6b6b;cursor:pointer}'
    + '#dazang-graph-inline input[type=search]{font:inherit;font-size:.72rem;padding:2px 7px;border:1px solid #d8d0c0;border-radius:4px;background:#fff;color:#2b2b2b;width:140px}'
    + '#dazang-graph-inline .dg-body{display:flex;height:560px}'
    + '#dazang-graph-inline .dg-stage{position:relative;flex:1 1 auto;min-width:0}'
    + '#dazang-graph-inline canvas{display:block;width:100%;height:100%;cursor:grab;touch-action:none}'
    + '#dazang-graph-inline canvas.dragging{cursor:grabbing}'
    + '#dazang-graph-inline .dg-side{flex:0 0 250px;border-left:1px solid #e4dccb;padding:10px 12px;overflow:auto;background:rgba(255,255,255,.55);font-size:.74rem}'
    + '#dazang-graph-inline .dg-side h4{font-size:.78rem;margin:.1rem 0 .4rem}'
    + '#dazang-graph-inline .dg-side .dg-meta{color:#6b6b6b;font-size:.7rem;line-height:1.6}'
    + '#dazang-graph-inline .dg-side .dg-edge{display:block;width:100%;text-align:left;margin:2px 0;padding:2px 3px;border:0;background:transparent;color:#2b2b2b;cursor:pointer;font-size:.7rem}'
    + '#dazang-graph-inline .dg-side .dg-edge:hover{background:rgba(139,94,52,.08)}'
    + '#dazang-graph-inline .dg-tip{position:absolute;pointer-events:none;display:none;max-width:320px;padding:5px 8px;background:#fff;border:1px solid #d8d0c0;border-radius:5px;box-shadow:0 3px 14px rgba(0,0,0,.12);font-size:.7rem;z-index:20;line-height:1.5}'
    + '#dazang-graph-inline .dg-legend{position:absolute;left:8px;bottom:8px;background:rgba(255,255,255,.9);border:1px solid #e4dccb;border-radius:5px;padding:4px 7px;font-size:.62rem;color:#6b6b6b;line-height:1.7;max-width:420px}'
    + '#dazang-graph-inline .dg-legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:3px;vertical-align:-1px}'
    + '#dazang-graph-inline .dg-stats{position:absolute;right:8px;bottom:8px;background:rgba(255,255,255,.9);border:1px solid #e4dccb;border-radius:5px;padding:4px 7px;font-size:.64rem;color:#6b6b6b}'
    + '@media(max-width:760px){#dazang-graph-inline .dg-body{flex-direction:column;height:640px}#dazang-graph-inline .dg-side{flex:0 0 180px;border-left:0;border-top:1px solid #e4dccb}}';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];
    });
  }

  function mount() {
    var host = document.getElementById('dazang-graph-inline');
    if (!host || !window.DAZANG_GRAPH) return;
    if (host.getAttribute('data-mounted') === '1' && host.querySelector('canvas')) return;
    host.setAttribute('data-mounted', '1');

    var G = window.DAZANG_GRAPH;
    var nodes = G.nodes.map(function (n, i) {
      return Object.assign({}, n, {i:i, x:0, y:0, vx:0, vy:0, r:TYPE_R[n.type] || 5, color:n.color || TYPE_COLOR[n.type] || '#888'});
    });
    var byId = new Map(nodes.map(function (n) { return [n.id, n]; }));
    var edges = G.edges.map(function (e) {
      return Object.assign({}, e, {s:byId.get(e.source), t:byId.get(e.target)});
    });
    var adj = new Map(nodes.map(function (n) { return [n.id, []]; }));
    edges.forEach(function (e) { adj.get(e.source).push(e); adj.get(e.target).push(e); });

    host.innerHTML =
      '<style>' + CSS + '</style>'
      + '<div class="dg-bar">'
      + '<div class="dg-g" id="dg-modes"><span style="color:#6b6b6b">视图</span>'
      + '<button data-mode="layered" class="on">分层</button><button data-mode="force">力导向</button><button data-mode="citation">引用</button></div>'
      + '<div class="dg-g" id="dg-layers">'
      + '<label class="dg-chk"><input type="checkbox" value="version" checked>版本</label>'
      + '<label class="dg-chk"><input type="checkbox" value="pin" checked>品</label>'
      + '<label class="dg-chk"><input type="checkbox" value="tib" checked>藏章</label>'
      + '<label class="dg-chk"><input type="checkbox" value="text" checked>异译</label>'
      + '<label class="dg-chk"><input type="checkbox" value="cluster" checked>簇</label>'
      + '<label class="dg-chk"><input type="checkbox" value="citation">注疏</label></div>'
      + '<div class="dg-g" id="dg-etypes">'
      + '<label class="dg-chk"><input type="checkbox" value="structural" checked>结构</label>'
      + '<label class="dg-chk"><input type="checkbox" value="parallel" checked>平行</label>'
      + '<label class="dg-chk"><input type="checkbox" value="translation" checked>异译</label>'
      + '<label class="dg-chk"><input type="checkbox" value="related" checked>关联</label>'
      + '<label class="dg-chk"><input type="checkbox" value="citation">引用</label></div>'
      + '<div class="dg-g"><input type="search" id="dg-q" placeholder="搜索品／T号／藏章…">'
      + '<button id="dg-labels" class="on">标签</button><button id="dg-fit">适配</button><button id="dg-reset">重置</button><button id="dg-full">展开</button></div>'
      + '</div>'
      + '<div class="dg-body"><div class="dg-stage"><canvas></canvas><div class="dg-tip"></div><div class="dg-legend"></div><div class="dg-stats"></div></div>'
      + '<aside class="dg-side"><h4>节点详情</h4><div class="dg-meta" id="dg-detail">点击节点查看：类型、编号、相邻边与证据级别。</div><div id="dg-neighbors"></div></aside></div>';

    var cv = host.querySelector('canvas'), ctx = cv.getContext('2d');
    var stage = host.querySelector('.dg-stage'), tip = host.querySelector('.dg-tip');
    var detail = host.querySelector('#dg-detail'), neighbors = host.querySelector('#dg-neighbors');
    var statsEl = host.querySelector('.dg-stats'), qEl = host.querySelector('#dg-q');
    var view = {k:1, x:0, y:0}, W = 900, H = 560, dpr = Math.min(window.devicePixelRatio || 1, 2);
    var mode = 'layered', showLabels = true, simAlpha = 1;
    var layers = new Set(['version','pin','tib','text','cluster']);
    var egroups = new Set(['structural','parallel','translation','related']);
    var hover = null, selected = null, dragNode = null, dragStart = null, dragMoved = false;

    function visibleNode(n) {
      if (mode === 'citation') return ['commentary','work','canon_class','commentary_hub'].indexOf(n.type) >= 0;
      if (['commentary','work','canon_class','commentary_hub'].indexOf(n.type) >= 0) return layers.has('citation');
      return layers.has(n.type);
    }
    function visibleEdge(e) { return visibleNode(e.s) && visibleNode(e.t) && egroups.has(EDGE_GROUP[e.type]); }

    function initPositions() {
      if (mode === 'layered') {
        var pins = nodes.filter(function (n) { return n.type === 'pin'; }).sort(function (a,b) { return +a.id.split(':')[1] - +b.id.split(':')[1]; });
        var tibs = nodes.filter(function (n) { return n.type === 'tib'; }).sort(function (a,b) { return +a.id.split(':')[1] - +b.id.split(':')[1]; });
        var texts = nodes.filter(function (n) { return n.type === 'text'; }).sort(function (a,b) { return a.id.localeCompare(b.id); });
        nodes.filter(function (n) { return n.type === 'version'; }).forEach(function (n,i) { n.x = 90; n.y = 110 + i*105; });
        nodes.filter(function (n) { return n.type === 'cluster'; }).forEach(function (n,i) { n.x = 260; n.y = 120 + i*62; });
        pins.forEach(function (n,i) { n.x = 380; n.y = 60 + i*22.5; });
        tibs.forEach(function (n,i) { n.x = 650; n.y = 60 + i*19.5; });
        texts.forEach(function (n,i) { n.x = 900; n.y = 60 + i*30; });
      } else if (mode === 'citation') {
        nodes.filter(function (n) { return n.type === 'commentary'; }).forEach(function (n,i) { n.x = 150; n.y = 180 + i*95; });
        nodes.filter(function (n) { return n.type === 'work'; }).forEach(function (n,i) { n.x = 840; n.y = 120 + i*92; });
        nodes.filter(function (n) { return n.type === 'canon_class'; }).forEach(function (n,i) { n.x = 180 + i*125; n.y = 740; });
        var hub = nodes.find(function (n) { return n.type === 'commentary_hub'; });
        if (hub) { hub.x = 510; hub.y = 420; }
      } else {
        var vis = nodes.filter(visibleNode);
        vis.forEach(function (n,i) {
          var a = 2*Math.PI*i/Math.max(vis.length,1);
          n.x = 500 + 330*Math.cos(a); n.y = 460 + 310*Math.sin(a); n.vx = 0; n.vy = 0;
        });
      }
    }

    function simulate(steps) {
      var vis = nodes.filter(visibleNode), es = edges.filter(visibleEdge), k = 130;
      for (var s=0; s<steps; s++) {
        simAlpha = Math.max(0.02, simAlpha*0.985);
        for (var i=0; i<vis.length; i++) {
          var a = vis[i];
          for (var j=i+1; j<vis.length; j++) {
            var b = vis[j], dx=a.x-b.x, dy=a.y-b.y, d2=dx*dx+dy*dy+1;
            if (d2 > 90000) continue;
            var f = (1.9*k*k/d2)*simAlpha, d=Math.sqrt(d2);
            a.vx += dx/d*f; a.vy += dy/d*f; b.vx -= dx/d*f; b.vy -= dy/d*f;
          }
        }
        es.forEach(function (e) {
          var dx=e.s.x-e.t.x, dy=e.s.y-e.t.y, d=Math.hypot(dx,dy)+.01, f=d*d/k*0.055*simAlpha;
          e.s.vx -= dx/d*f; e.s.vy -= dy/d*f; e.t.vx += dx/d*f; e.t.vy += dy/d*f;
        });
        if (mode === 'force') {
          var cs = nodes.filter(function (n) { return n.type === 'cluster'; });
          cs.forEach(function (n,i) {
            var a = 2*Math.PI*i/Math.max(cs.length,1), tx = 500+180*Math.cos(a), ty = 460+180*Math.sin(a);
            n.vx += (tx-n.x)*.012; n.vy += (ty-n.y)*.012;
          });
        }
        vis.forEach(function (n) {
          n.vx += (500-n.x)*0.0016; n.vy += (460-n.y)*0.0016;
          n.x += n.vx*0.55; n.y += n.vy*0.55; n.vx *= 0.82; n.vy *= 0.82;
          n.x = Math.min(980, Math.max(20, n.x)); n.y = Math.min(900, Math.max(30, n.y));
        });
      }
      for (var r=0; r<40; r++) {
        var moved = false;
        for (var i2=0; i2<vis.length; i2++) {
          for (var j2=i2+1; j2<vis.length; j2++) {
            var a2=vis[i2], b2=vis[j2], dx2=a2.x-b2.x, dy2=a2.y-b2.y, d3=Math.hypot(dx2,dy2);
            var md = (a2.r+b2.r)+8;
            if (d3 < md) { moved = true; if (d3 < .01) { dx2=1; dy2=0; d3=1; } var p=(md-d3)/2; a2.x+=dx2/d3*p; a2.y+=dy2/d3*p; b2.x-=dx2/d3*p; b2.y-=dy2/d3*p; }
          }
        }
        if (!moved) break;
      }
      draw();
    }

    function draw() {
      W = Math.max(320, stage.clientWidth); H = Math.max(320, stage.clientHeight);
      if (cv.width !== Math.floor(W*dpr) || cv.height !== Math.floor(H*dpr)) { cv.width = Math.floor(W*dpr); cv.height = Math.floor(H*dpr); }
      ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,W,H);
      ctx.fillStyle = '#fbf8f1'; ctx.fillRect(0,0,W,H);
      ctx.save(); ctx.translate(view.x, view.y); ctx.scale(view.k, view.k);
      var visE = edges.filter(visibleEdge), visN = nodes.filter(visibleNode);
      var focus = hover || selected;
      var nbr = focus ? new Set([focus.id].concat(adj.get(focus.id).map(function (e) { return e.source === focus.id ? e.target : e.source; }))) : null;
      visE.forEach(function (e) {
        if (!e.s || !e.t) return;
        var dim = nbr && !(nbr.has(e.source) && nbr.has(e.target));
        ctx.globalAlpha = dim ? 0.10 : 0.72;
        ctx.strokeStyle = EDGE_COLOR[e.type] || '#999';
        ctx.lineWidth = (e.type === 'cites' ? Math.max(.7, Math.min(4.5, e.weight/170)) : e.type === 'cites_class' ? Math.max(.7, (e.weight||0)*18) : 0.9) / Math.max(view.k, .7);
        ctx.setLineDash(EDGE_DASH[e.type] || []);
        var mx = (e.s.x+e.t.x)/2;
        ctx.beginPath(); ctx.moveTo(e.s.x,e.s.y); ctx.bezierCurveTo(mx,e.s.y,mx,e.t.y,e.t.x,e.t.y); ctx.stroke();
      });
      ctx.setLineDash([]); ctx.globalAlpha = 1;
      visN.forEach(function (n) {
        var isFocus = focus && (n.id === focus.id || (nbr && nbr.has(n.id)));
        var dim = focus && !isFocus;
        ctx.globalAlpha = dim ? 0.22 : 1;
        ctx.beginPath(); ctx.arc(n.x,n.y,n.r,0,2*Math.PI); ctx.fillStyle = n.color; ctx.fill();
        if (isFocus) { ctx.strokeStyle = '#b03a2e'; ctx.lineWidth = 2/Math.max(view.k,.6); ctx.stroke(); }
        if (['version','cluster','commentary','work','canon_class'].indexOf(n.type) >= 0) {
          ctx.globalAlpha = dim ? 0.2 : 0.95; ctx.fillStyle = '#2b2b2b';
          ctx.font = (n.type === 'cluster' ? '8.5px' : '9.5px') + " 'Noto Serif SC','Songti SC',serif";
          ctx.textAlign = 'center';
          ctx.fillText(n.label.length > 22 ? n.label.slice(0,22) + '…' : n.label, n.x, n.y - n.r - 4);
        }
        if (showLabels && (view.k > 1.15 || n.type === 'pin' || n.type === 'tib' || n.type === 'text')) {
          ctx.globalAlpha = dim ? 0.18 : 0.8; ctx.fillStyle = n.type === 'text' ? '#2f5d7c' : '#6b6b6b';
          ctx.font = "7px 'Noto Serif SC','Songti SC',serif"; ctx.textAlign = 'left';
          var lab = n.type === 'pin' ? n.id.split(':')[1] : n.type === 'tib' ? n.id.split(':')[1] : n.label.split(' ')[0];
          ctx.fillText(lab, n.x + n.r + 2, n.y + 2);
        }
        ctx.globalAlpha = 1;
      });
      ctx.restore();
      statsEl.textContent = '可见 ' + visN.length + ' 节点 · ' + visE.length + ' 边　缩放 ' + view.k.toFixed(2) + '×';
    }

    function pick(ev) {
      var r = cv.getBoundingClientRect();
      var x = (ev.clientX - r.left - view.x)/view.k, y = (ev.clientY - r.top - view.y)/view.k;
      var best = null, bd = 1e9;
      nodes.forEach(function (n) {
        if (!visibleNode(n)) return;
        var d = Math.hypot(n.x-x, n.y-y);
        if (d < n.r + 10 && d < bd) { best = n; bd = d; }
      });
      return best;
    }

    function showTip(ev, n) {
      if (!n) { tip.style.display = 'none'; return; }
      var r = stage.getBoundingClientRect();
      tip.innerHTML = '<b>' + esc(n.label) + '</b><br>' + (TYPE_NAME[n.type] || n.type) + ' · 度 ' + adj.get(n.id).length + (n.grade ? ' · ' + n.grade : '') + (n.sub ? '<br>' + esc(n.sub) : '');
      tip.style.display = 'block';
      tip.style.left = Math.min(stage.clientWidth - 340, ev.clientX - r.left + 12) + 'px';
      tip.style.top = Math.min(stage.clientHeight - 30, ev.clientY - r.top + 12) + 'px';
    }

    function select(n) {
      selected = n;
      if (!n) { detail.textContent = '点击节点查看：类型、编号、相邻边与证据级别。'; neighbors.innerHTML = ''; return; }
      detail.innerHTML = '<b>' + esc(n.label) + '</b><br>' + (TYPE_NAME[n.type] || n.type) + ' · ' + n.id + (n.sub ? '<br>' + esc(n.sub) : '');
      var es = adj.get(n.id).slice().sort(function (a,b) { return a.type.localeCompare(b.type); });
      neighbors.innerHTML = '<div class="dg-meta" style="margin-top:6px">相邻边（' + es.length + '）</div>';
      es.forEach(function (e) {
        var other = e.source === n.id ? e.t : e.s;
        var btn = document.createElement('button');
        btn.className = 'dg-edge';
        btn.innerHTML = '<span style="color:' + EDGE_COLOR[e.type] + '">■</span> ' + EDGE_NAME[e.type] + ' → ' + esc(other.label) + ' <span style="color:#999">' + (e.grade || '') + '</span>';
        btn.onclick = function () { select(other); centerOn(other); };
        neighbors.appendChild(btn);
      });
    }
    function centerOn(n) { view.k = Math.max(view.k, 1.5); view.x = W/2 - n.x*view.k; view.y = H/2 - n.y*view.k; draw(); }

    function fit() {
      var vis = nodes.filter(visibleNode);
      if (!vis.length) return;
      var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
      vis.forEach(function (n) { x0=Math.min(x0,n.x); y0=Math.min(y0,n.y); x1=Math.max(x1,n.x); y1=Math.max(y1,n.y); });
      var pad = 40;
      var k = Math.min((W-2*pad)/Math.max(x1-x0,1), (H-2*pad)/Math.max(y1-y0,1));
      view.k = Math.max(0.18, Math.min(2.8, k));
      view.x = W/2 - (x0+x1)/2*view.k; view.y = H/2 - (y0+y1)/2*view.k;
      draw();
    }

    function setMode(m) {
      mode = m;
      host.querySelectorAll('#dg-modes button').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-mode') === m); });
      if (m === 'citation') {
        layers.add('citation'); egroups.add('citation');
        host.querySelector('#dg-layers input[value="citation"]').checked = true;
        host.querySelector('#dg-etypes input[value="citation"]').checked = true;
      }
      initPositions();
      if (m === 'force') { simAlpha = 1; simulate(220); }
      selected = null; select(null); fit();
    }

    function syncFilters() {
      layers = new Set(Array.from(host.querySelectorAll('#dg-layers input:checked')).map(function (x) { return x.value; }));
      egroups = new Set(Array.from(host.querySelectorAll('#dg-etypes input:checked')).map(function (x) { return x.value; }));
      if (mode === 'citation') { layers = new Set(['commentary','work','canon_class','commentary_hub']); egroups = new Set(['citation']); }
      draw();
    }

    host.querySelectorAll('#dg-modes button').forEach(function (b) { b.onclick = function () { setMode(b.getAttribute('data-mode')); }; });
    host.querySelectorAll('#dg-layers input,#dg-etypes input').forEach(function (x) { x.onchange = syncFilters; });
    host.querySelector('#dg-labels').onclick = function (e) { showLabels = !showLabels; e.currentTarget.classList.toggle('on', showLabels); draw(); };
    host.querySelector('#dg-fit').onclick = fit;
    host.querySelector('#dg-reset').onclick = function () {
      view = {k:1,x:0,y:0}; layers = new Set(['version','pin','tib','text','cluster']); egroups = new Set(['structural','parallel','translation','related']);
      host.querySelectorAll('#dg-layers input').forEach(function (x) { x.checked = layers.has(x.value); });
      host.querySelectorAll('#dg-etypes input').forEach(function (x) { x.checked = egroups.has(x.value); });
      qEl.value = ''; selected = null; select(null); setMode('layered');
    };
    host.querySelector('#dg-full').onclick = function (e) { host.classList.toggle('dg-full'); e.currentTarget.classList.toggle('on', host.classList.contains('dg-full')); setTimeout(function () { draw(); fit(); }, 30); };
    qEl.addEventListener('input', function () {
      var q = qEl.value.trim().toLowerCase();
      if (!q) { selected = null; select(null); draw(); return; }
      var hit = nodes.find(function (n) { return visibleNode(n) && (n.label.toLowerCase().indexOf(q) >= 0 || n.id.toLowerCase().indexOf(q) >= 0); });
      if (hit) { select(hit); centerOn(hit); }
    });

    cv.addEventListener('mousemove', function (ev) {
      if (dragNode) {
        dragMoved = true;
        var r = cv.getBoundingClientRect();
        dragNode.x = (ev.clientX-r.left-view.x)/view.k; dragNode.y = (ev.clientY-r.top-view.y)/view.k; draw(); return;
      }
      if (dragStart && dragStart.moved) {
        var dx = ev.clientX-dragStart.x, dy = ev.clientY-dragStart.y;
        view.x += dx; view.y += dy; dragStart.x = ev.clientX; dragStart.y = ev.clientY; draw(); return;
      }
      var n = pick(ev);
      if (n !== hover) { hover = n; showTip(ev,n); draw(); } else showTip(ev,n);
    });
    cv.addEventListener('mousedown', function (ev) {
      var n = pick(ev);
      if (n && mode === 'force') { dragNode = n; dragMoved = false; cv.classList.add('dragging'); }
      else dragStart = {x:ev.clientX, y:ev.clientY, moved:false};
    });
    window.addEventListener('mousemove', function (ev) { if (dragStart && (Math.abs(ev.clientX-dragStart.x) > 2 || Math.abs(ev.clientY-dragStart.y) > 2)) dragStart.moved = true; });
    cv.addEventListener('mouseup', function (ev) {
      if (dragNode) { var n = dragNode; dragNode = null; cv.classList.remove('dragging'); if (!dragMoved) select(n); return; }
      if (dragStart && !dragStart.moved) select(pick(ev));
      dragStart = null;
    });
    cv.addEventListener('mouseleave', function () { hover = null; showTip(null); draw(); });
    cv.addEventListener('wheel', function (ev) {
      ev.preventDefault();
      var r = cv.getBoundingClientRect(), mx = ev.clientX-r.left, my = ev.clientY-r.top;
      var wx = (mx-view.x)/view.k, wy = (my-view.y)/view.k;
      var k2 = Math.max(0.18, Math.min(4, view.k*(ev.deltaY < 0 ? 1.12 : 0.89)));
      view.x = mx-wx*k2; view.y = my-wy*k2; view.k = k2; draw();
    }, {passive:false});

    host.querySelector('.dg-legend').innerHTML =
      Object.keys(TYPE_NAME).filter(function (k) { return k !== 'commentary_hub'; }).map(function (k) {
        return '<i style="background:' + TYPE_COLOR[k] + '"></i>' + TYPE_NAME[k];
      }).join(' ')
      + '<br><span style="color:#8b5e34">━ contains</span> <span style="color:#2f5d7c">┅ contains_60</span> <span style="color:#bab2a3">━ parallel</span> <span style="color:#b5651d">━ translation</span> <span style="color:#b03a2e">┅ related</span> <span style="color:#4f6f52">━ cites</span>';

    initPositions();
    setMode('layered');
    draw(); fit();

    // Do not redraw synchronously inside ResizeObserver: resizing the canvas
    // re-triggers the observer and Chrome reports
    // "ResizeObserver loop completed with undelivered notifications".
    var roFrame = null, lastSize = '';
    function resizeDraw() {
      if (roFrame) return;
      roFrame = requestAnimationFrame(function () {
        roFrame = null;
        var size = stage.clientWidth + 'x' + stage.clientHeight;
        if (size === lastSize) return;
        lastSize = size;
        draw();
      });
    }
    if (window.ResizeObserver) {
      lastSize = stage.clientWidth + 'x' + stage.clientHeight;
      new ResizeObserver(resizeDraw).observe(stage);
    } else {
      window.addEventListener('resize', resizeDraw);
    }
  }

  function boot() {
    mount();
    var root = document.getElementById('article-root');
    if (root && window.MutationObserver) {
      var pending = null;
      new MutationObserver(function () {
        var host = document.getElementById('dazang-graph-inline');
        if (!host || host.querySelector('canvas')) return;
        host.setAttribute('data-mounted', '0');
        if (pending) clearTimeout(pending);
        pending = setTimeout(mount, 30);
      }).observe(root, {childList:true, subtree:true});
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();