/* shanhe.js — 「山河法脉」子页渲染器（F.2 底图骨架·famai/shanhe.html 专用·standalone）
   数据契约：注入的全局 SHANHE = {
     canvas:{w,h}, view:{lon:[min,max],lat:[min,max]},
     years:[{year, polities:[{n,sup,pr, rings:[[[x,y],…],…]}]}],   // 坐标已由 Python 投影为画布坐标
     base:{coast:[rings], countries:[rings]},
     places:[{id,n,lat,lng,tp,dy,x,y}],
     persons:[{id,name,person_source,stations:[{index,label,yr,lat,lng,x,y,status,quote,source,anchor,url,note}]}],
     meta:{generated, license_note}
   } 静态兜底表（信息無损）在 DOM 中先行存在，本脚本只做增强。
   F.3 S2「点人溯事」：择祖师→行迹折线＋逐站 ‹›/空格推进→每站一手引文卡（CBETA 繁体逐字回源·
   pending 站显〔待核〕）；S6 零坐标深链 ?person=<id>&station=<idx>（&year=<公元>），URL 不含经纬度。 */

(function () {
  var S = window.SHANHE;
  if (!S) return;
  var svg = document.getElementById('map-svg');
  var gBase = document.getElementById('g-base');
  var gPoly = document.getElementById('g-polity');
  var gGhost = document.getElementById('g-ghost');
  var gPlace = document.getElementById('g-place');
  var gPerson = document.getElementById('g-person');
  var panel = document.getElementById('info-panel');
  var PERSONS = S.persons || [];
  var TEMPLES = S.temples || [];
  var LIN = S.lineage || { masters: [], trees: {}, branches: [], backbone: [] };
  var gTemple = document.getElementById('g-temple');
  var lSvg = document.getElementById('lineage-svg');
  var cur = S.years.length ? S.years[0].year : null;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }


  /* ── 坐标 → path 串 ── */
  function ringPath(r) {
    var d = '';
    for (var i = 0; i < r.length; i++) {
      d += (i ? 'L' : 'M') + r[i][0].toFixed(1) + ',' + r[i][1].toFixed(1);
    }
    return d + 'Z';
  }
  function el(name, attrs) {
    var e = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }

  /* ── 政体配色（按名哈希·稳定色板·低饱和贴合纸色系） ── */
  var PAL = ['#b8863c', '#7a9e7e', '#8d7ba6', '#c07f6a', '#6f93b4', '#a6915d',
             '#88a48c', '#b47fa0', '#7f8fb4', '#c09a6f'];
  function hue(nm) {
    var h = 0, s = String(nm || '?');
    for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) % 9973;
    return PAL[h % PAL.length];
  }

  /* ── 物理底图（NE·PD） ── */
  function drawBase() {
    var i, j, r, p;
    for (i = 0; i < S.base.countries.length; i++) {
      r = S.base.countries[i];
      p = el('path', { d: ringPath(r), fill: 'none', stroke: '#c9c2b6', 'stroke-width': 0.6, 'stroke-dasharray': '3,2' });
      gBase.appendChild(p);
    }
    for (i = 0; i < S.base.coast.length; i++) {
      for (j = 0; j < S.base.coast[i].length; j++) {
        r = S.base.coast[i][j];
        p = el('path', { d: ringPath(r), fill: '#efe9dd', stroke: '#a99e88', 'stroke-width': 0.8 });
        gBase.appendChild(p);
      }
    }
  }

  /* ── 断代政体色块层 ── */
  function yearData(y) {
    for (var i = 0; i < S.years.length; i++) if (S.years[i].year === y) return S.years[i];
    return null;
  }
  function drawYear(y, target, ghostMode) {
    var d = yearData(y);
    if (!d) return;
    target.innerHTML = '';
    for (var i = 0; i < d.polities.length; i++) {
      var po = d.polities[i];
      for (var j = 0; j < po.rings.length; j++) {
        var pth = el('path', { d: ringPath(po.rings[j]) });
        if (ghostMode) {
          pth.setAttribute('fill', 'none'); pth.setAttribute('stroke', '#555');
          pth.setAttribute('stroke-width', 0.7); pth.setAttribute('stroke-dasharray', '4,3');
          pth.setAttribute('opacity', 0.55);
        } else {
          pth.setAttribute('fill', hue(po.n)); pth.setAttribute('fill-opacity', 0.42);
          pth.setAttribute('stroke', hue(po.n)); pth.setAttribute('stroke-width', 1);
          pth.setAttribute('data-name', po.n || '(未標名）');
          pth.setAttribute('data-sup', po.sup || ''); pth.setAttribute('data-pr', po.pr || '');
          pth.setAttribute('data-year', y);
          pth.style.cursor = 'pointer';
          pth.addEventListener('click', onPolity);
        }
        target.appendChild(pth);
      }
    }
  }
  function onPolity(ev) {
    var t = ev.target;
    var pr = t.getAttribute('data-pr');
    var prTxt = pr ? ('边界精度 ' + pr + '/3') : '精度未標〔待核〕';
    panel.innerHTML = '<h4>' + t.getAttribute('data-name') + ' <span class="yr">' + t.getAttribute('data-year') +
      ' 年快照</span></h4>' +
      '<p>宗主／归因：' + (t.getAttribute('data-sup') || '—') + '</p>' +
      '<p>' + prTxt + '</p>' +
      '<p class="lic">几何来源 aourednik/historical-basemaps（GPL-3.0 独立集合）·示意底图·学术精度待核。<a href="license.html">层源与许可 →</a></p>';
  }

  /* ── 仓内实地标点（DB locations·30） ── */
  function drawPlaces() {
    for (var i = 0; i < S.places.length; i++) {
      var p = S.places[i];
      var c = el('circle', { cx: p.x, cy: p.y, r: 3.2, fill: '#3d5a80', stroke: '#fff', 'stroke-width': 1 });
      c.setAttribute('data-name', p.n); c.setAttribute('data-dy', p.dy || '');
      c.setAttribute('data-tp', p.tp || ''); c.setAttribute('data-ll', p.lat + ',' + p.lng);
      c.style.cursor = 'pointer';
      c.addEventListener('click', onPlace);
      gPlace.appendChild(c);
      var tx = el('text', { x: p.x + 4.5, y: p.y + 3, 'font-size': 8.5, fill: '#4a4033' });
      tx.textContent = p.n;
      gPlace.appendChild(tx);
    }
  }
  function onPlace(ev) {
    var t = ev.target;
    panel.innerHTML = '<h4>' + t.getAttribute('data-name') + ' <span class="yr">' + t.getAttribute('data-dy') + '</span></h4>' +
      '<p>类型：' + t.getAttribute('data-tp') + ' · 坐标：' + t.getAttribute('data-ll') + '</p>' +
      '<p class="lic">仓内实证库 data/catalog/huayan.db · locations 表（lat/lng 实测全填）</p>';
  }

  /* ── 控件 ── */
  var ghostOn = false, showPlaces = true;
  function refresh() {
    drawYear(cur, gPoly, false);
    if (ghostOn) {
      var idx = -1;
      for (var i = 0; i < S.years.length; i++) if (S.years[i].year === cur) idx = i;
      if (idx > 0) drawYear(S.years[idx - 1].year, gGhost, true);
      else gGhost.innerHTML = '';
    } else gGhost.innerHTML = '';
    var btns = document.querySelectorAll('.year-btn');
    for (var k = 0; k < btns.length; k++) btns[k].className = 'year-btn' + (String(btns[k].getAttribute('data-year')) === String(cur) ? ' active' : '');
  }
  document.querySelectorAll('.year-btn').forEach(function (b) {
    b.addEventListener('click', function () { cur = parseInt(b.getAttribute('data-year'), 10); refresh(); });
  });
  var gb = document.getElementById('ghost-toggle');
  if (gb) gb.addEventListener('change', function () { ghostOn = gb.checked; refresh(); });
  var pb = document.getElementById('place-toggle');
  if (pb) pb.addEventListener('change', function () { showPlaces = pb.checked; gPlace.style.display = showPlaces ? '' : 'none'; });

  /* ── F.3 S2 祖师行迹（点人溯事·逐站推进·引文卡·S6 零坐标 URL） ── */
  var pCur = null, stCur = 0;   // pCur=person id；stCur=当前站点 index
  function findPerson(id) { for (var i = 0; i < PERSONS.length; i++) if (PERSONS[i].id === id) return PERSONS[i]; return null; }
  function indexOfStation(p, idx) { for (var i = 0; i < p.stations.length; i++) if (p.stations[i].index === idx) return i; return 0; }
  function nearestSnapshot(y) {
    var ys = S.years.map(function (d) { return d.year; }).sort(function (a, b) { return a - b; });
    var best = ys.length ? ys[0] : null;
    for (var i = 0; i < ys.length; i++) if (ys[i] <= y) best = ys[i];
    return best;
  }
  function drawRoute() {
    if (!gPerson) return;
    gPerson.innerHTML = '';
    var p = findPerson(pCur);
    if (!p) return;
    var sts = p.stations, dpath = '';
    for (var i = 0; i < sts.length; i++) dpath += (i ? 'L' : 'M') + sts[i].x + ',' + sts[i].y;
    gPerson.appendChild(el('path', { d: dpath, fill: 'none', stroke: '#8d5a2b', 'stroke-width': 1.6, 'stroke-dasharray': '5,3', opacity: 0.75 }));
    for (var i = 0; i < sts.length; i++) {
      var s = sts[i], on = (s.index === stCur);
      var fill = s.status === 'sourced' ? (on ? '#c0392b' : '#8d5a2b') : '#9a9a9a';
      var c = el('circle', { cx: s.x, cy: s.y, r: on ? 5.5 : 3.6, fill: fill, stroke: '#fff', 'stroke-width': 1 });
      c.style.cursor = 'pointer';
      c.setAttribute('data-idx', s.index);
      c.addEventListener('click', function () { selectStation(parseInt(this.getAttribute('data-idx'), 10)); });
      gPerson.appendChild(c);
      var tx = el('text', { x: s.x + 6, y: s.y - 5, 'font-size': on ? 10 : 8.5, fill: on ? '#c0392b' : '#6b5a3a', 'font-weight': on ? 'bold' : 'normal' });
      tx.textContent = (i + 1) + '. ' + s.label;
      gPerson.appendChild(tx);
    }
  }
  function card(p, s) {
    var head = '<h4>' + esc(p.name) + ' <span class="yr">' + esc(s.label) + ' · 西 ' + esc(s.yr) + ' 年</span></h4>';
    var body;
    if (s.status === 'sourced') {
      body = '<div class="cite-card"><div class="q">「' + esc(s.quote) + '」</div>' +
        '<div class="src">出处：' + esc(s.source) + ' · 大正页锚 〔' + esc(s.anchor) + '〕' +
        (s.url ? (' · <a href="' + esc(s.url) + '" target="_blank" rel="noopener">回源底本 →</a>') : '') + '</div>' +
        (s.note ? ('<div class="note">' + esc(s.note) + '</div>') : '') + '</div>';
    } else {
      body = '<div class="cite-card"><div class="pend">〔待核〕本传未载此站逐字句' +
        (s.note ? ('：' + esc(s.note)) : '') + '</div></div>';
    }
    return head + body + '<p class="lic">一手引文＝CBETA 底本繁体逐字回源（miss=0）·异文／底本自歧各照底本、不统一。</p>';
  }
  function showCard() {
    var p = findPerson(pCur);
    if (!p) return;
    var s = null;
    for (var i = 0; i < p.stations.length; i++) if (p.stations[i].index === stCur) s = p.stations[i];
    if (!s) s = p.stations[0];
    panel.innerHTML = card(p, s);
    var pos = indexOfStation(p, s.index);
    var ind = document.getElementById('st-ind');
    if (ind) ind.textContent = '第 ' + (pos + 1) + '/' + p.stations.length + ' 站';
    var pv = document.getElementById('st-prev'), nx = document.getElementById('st-next');
    if (pv) pv.disabled = pos <= 0;
    if (nx) nx.disabled = pos >= p.stations.length - 1;
    if (s.yr != null) { cur = nearestSnapshot(parseInt(s.yr, 10)); refresh(); }
  }
  function selectStation(idx) { if (!findPerson(pCur)) return; stCur = idx; drawRoute(); showCard(); syncURL(); }
  function step(delta) {
    var p = findPerson(pCur); if (!p) return;
    var pos = Math.max(0, Math.min(p.stations.length - 1, indexOfStation(p, stCur) + delta));
    stCur = p.stations[pos].index; drawRoute(); showCard(); syncURL();
  }
  function selectPerson(id) {
    pCur = id || null;
    var p = findPerson(pCur);
    stCur = p ? p.stations[0].index : 0;
    drawRoute();
    if (p) showCard();
    syncURL();
  }
  function syncURL() {   // S6：零坐标深链——仅记语义参数，不含经纬度
    var parts = [];
    if (pCur) { parts.push('person=' + encodeURIComponent(pCur)); parts.push('station=' + encodeURIComponent(stCur)); }
    if (linCur) parts.push('master=' + encodeURIComponent(linCur));
    if (templeCur) parts.push('temple=' + encodeURIComponent(templeCur));
    var url = location.pathname + (parts.length ? ('?' + parts.join('&')) : '') + location.hash;
    try { history.replaceState(null, '', url); } catch (e) {}
  }

  var sel = document.getElementById('person-select');
  if (sel) sel.addEventListener('change', function () { selectPerson(this.value); });
  var pbtn = document.getElementById('st-prev'), nbtn = document.getElementById('st-next');
  if (pbtn) pbtn.addEventListener('click', function () { step(-1); });
  if (nbtn) nbtn.addEventListener('click', function () { step(1); });
  document.addEventListener('keydown', function (e) {
    if (!pCur) return;
    if (e.code === 'Space') { e.preventDefault(); step(1); }
    else if (e.key === 'ArrowRight') step(1);
    else if (e.key === 'ArrowLeft') step(-1);
  });

  /* ══ F.4 S3 地谱追溯卡（华严要地·点击→沿革/华严事件/人物/信度/依据）══ */
  var BRANCH_COLOR = {};
  (LIN.branches || []).forEach(function (b) { BRANCH_COLOR[b.name] = b.color; });
  var PNAME = {};
  (LIN.masters || []).forEach(function (m) { PNAME[m.id] = m.name; });
  Object.keys(LIN.trees || {}).forEach(function (mid) {
    (LIN.trees[mid] || []).forEach(function (e) { if (e.pname) PNAME[e.parent] = e.pname; if (e.dname) PNAME[e.disc] = e.dname; });
  });
  var templeCur = null;
  function findTemple(id) { for (var i = 0; i < TEMPLES.length; i++) if (TEMPLES[i].id === id) return TEMPLES[i]; return null; }
  function drawTemples() {
    if (!gTemple) return;
    gTemple.innerHTML = '';
    for (var i = 0; i < TEMPLES.length; i++) {
      var t = TEMPLES[i], on = (t.id === templeCur), s = on ? 6 : 4.2;
      var r = el('rect', { x: t.x - s, y: t.y - s, width: 2 * s, height: 2 * s, fill: on ? '#c0392b' : '#7a5a2e',
        stroke: '#fff', 'stroke-width': 1, transform: 'rotate(45 ' + t.x + ' ' + t.y + ')' });
      r.style.cursor = 'pointer';
      r.addEventListener('click', (function (id) { return function () { selectTemple(id); }; })(t.id));
      gTemple.appendChild(r);
      var tx = el('text', { x: t.x + 8, y: t.y - 6, 'font-size': 8.5, fill: on ? '#c0392b' : '#6b5a3a' });
      tx.textContent = t.name; gTemple.appendChild(tx);
    }
  }
  function templeCard(t) {
    var ev = (t.events && t.events.length) ? t.events.map(esc).join('、') : '—';
    var ps = (t.persons && t.persons.length) ? t.persons.map(function (id) { return esc(PNAME[id] || ('〔待核〕' + id)); }).join('、') : '—';
    var lk = (t.links || []).map(function (l) { return '<a href="' + esc(l.url) + '" target="_blank" rel="noopener">' + esc(l.name || l.url) + '</a>'; }).join(' ') || '—';
    var ver = (t.verified === 1) ? '确证（堪核）' : '〔待核〕传统记载';
    return '<h4>⛩ ' + esc(t.name) + ' <span class="yr">' + esc(t.school) + '</span></h4>' +
      '<p><b>沿革</b>：古称 ' + esc(t.ancient || t.name) + ' ｜ 今 ' + esc(t.location) + '（' + esc(t.dynasty || '—') + '）· ' + esc(t.type || '—') + '</p>' +
      '<p><b>创建/鼎盛</b>：约 ' + esc(t.founded == null ? '—' : t.founded) + ' 年 · 开建 ' + esc(t.founder || '—') + '</p>' +
      '<p><b>华严事件</b>：' + ev + '</p><p>' + esc(t.desc) + '</p>' +
      '<p><b>历史地位</b>：' + esc(t.sig) + '</p><p><b>关联人物</b>：' + ps + '</p>' +
      '<p><b>信度</b>：' + ver + ' ｜ <b>依据</b>：' + esc(t.source) + '</p>' +
      '<p class="src">参考：' + lk + '</p>' +
      '<p class="lic">地谱卡＝现存道场名录（temple_directory.yaml）逐字摘要＋信度标·只读投影。沿革/事件属综述（非逐字回源）；一手逐字引文见「点人溯事」S2。</p>';
  }
  function selectTemple(id) {
    templeCur = id || null;
    var t = findTemple(templeCur);
    if (t) { panel.innerHTML = templeCard(t); if (t.founded != null) { var yy = nearestSnapshot(Math.round(t.founded)); if (yy != null) { cur = yy; refresh(); } } }
    drawTemples(); syncURL();
  }

  /* ══ F.4 S4 法脉递归弟子树（分层 dendrogram）＋ S5 法系色块隔离/zoom ══ */
  var linCur = null, isoBranch = null;
  function findMaster(id) { for (var i = 0; i < LIN.masters.length; i++) if (LIN.masters[i].id === id) return LIN.masters[i]; return null; }
  function branchOf(nodeId, mid) {
    var es = LIN.trees[mid] || [];
    for (var i = 0; i < es.length; i++) if (es[i].disc === nodeId) return es[i].branch;
    return '华严五祖';
  }
  function setSel(id) { var s = document.getElementById('lineage-select'); if (s) s.value = id || ''; }
  function renderTree(mid) {
    if (!lSvg) return;
    while (lSvg.firstChild) lSvg.removeChild(lSvg.firstChild);
    linCur = mid || null; isoBranch = null;
    if (!mid) { lSvg.setAttribute('viewBox', '0 0 900 60'); var tip = el('text', { x: 14, y: 32, 'font-size': 13, fill: '#8a7a5a' }); tip.textContent = '择祖师后展开其 N 代弟子链（直系＝实线／私淑·影响＝虚线）'; lSvg.appendChild(tip); syncURL(); return; }
    var edges = LIN.trees[mid] || [];
    var mrec = findMaster(mid);
    var nodes = {}; nodes[mid] = { id: mid, name: mrec ? mrec.name : mid, depth: 0, verified: true };
    edges.forEach(function (e) {
      if (!nodes[e.parent]) nodes[e.parent] = { id: e.parent, name: e.pname || e.parent, depth: e.depth - 1, verified: true };
      if (!nodes[e.disc] || nodes[e.disc].depth > e.depth) nodes[e.disc] = { id: e.disc, name: e.dname || null, depth: e.depth, verified: e.dverified };
    });
    var byDepth = {}, maxD = 0;
    Object.keys(nodes).forEach(function (k) { var n = nodes[k]; (byDepth[n.depth] = byDepth[n.depth] || []).push(n); if (n.depth > maxD) maxD = n.depth; });
    var CW = 170, rowH = 30, y = 26;
    for (var d = 0; d <= maxD; d++) { var arr = byDepth[d] || []; for (var j = 0; j < arr.length; j++) { arr[j].y = y; y += rowH; } if (arr.length) y += 6; }
    var height = Math.max(60, y + 8), width = 24 + (maxD + 1) * CW + 220;
    var gE = el('g', {}), gN = el('g', {});
    edges.forEach(function (e) {
      var pn = nodes[e.parent], dn = nodes[e.disc]; if (!pn || !dn) return;
      var x1 = 24 + pn.depth * CW, x2 = 24 + dn.depth * CW, col = BRANCH_COLOR[e.branch] || '#888';
      var path = el('path', { d: 'M' + x1 + ',' + pn.y + ' C' + (x1 + CW / 2) + ',' + pn.y + ' ' + (x2 - CW / 2) + ',' + dn.y + ' ' + x2 + ',' + dn.y,
        stroke: col, 'class': 'lg-edge' + (e.rel === 'INFLUENCED' ? ' inf' : ''), 'data-branch': e.branch, 'stroke-opacity': 0.8 });
      gE.appendChild(path);
    });
    Object.keys(nodes).forEach(function (k) {
      var n = nodes[k], x = 24 + n.depth * CW;
      var gg = el('g', { 'class': 'lg-node' + (n.depth === 0 ? ' lg-root' : ''), 'data-branch': branchOf(n.id, mid) });
      gg.appendChild(el('circle', { cx: x, cy: n.y, r: n.depth === 0 ? 6 : 4.5, fill: n.depth === 0 ? '#c0392b' : (BRANCH_COLOR[branchOf(n.id, mid)] || '#8d5a2b'), stroke: '#fff', 'stroke-width': 1 }));
      var tx = el('text', { x: x + 9, y: n.y + 4, 'font-size': 11, fill: n.verified ? '#3a2f1e' : '#b00' });
      tx.textContent = (n.name || n.id) + (n.verified ? '' : '〔待核〕');
      gg.appendChild(tx); gg.style.cursor = 'pointer';
      gg.addEventListener('click', (function (nid) { return function () { if (nid !== linCur) { renderTree(nid); setSel(nid); } }; })(n.id));
      gN.appendChild(gg);
    });
    lSvg.appendChild(gE); lSvg.appendChild(gN);
    var vb = '0 0 ' + width + ' ' + height;
    lSvg.setAttribute('viewBox', vb); lSvg.setAttribute('data-full', vb);
    applyIsolate(); syncURL();
  }
  function applyIsolate() {
    if (!lSvg) return;
    var ns = lSvg.querySelectorAll('.lg-node'), es = lSvg.querySelectorAll('.lg-edge'), k;
    for (k = 0; k < ns.length; k++) ns[k].classList.toggle('dim', !!isoBranch && ns[k].getAttribute('data-branch') !== isoBranch);
    for (k = 0; k < es.length; k++) es[k].classList.toggle('dim', !!isoBranch && es[k].getAttribute('data-branch') !== isoBranch);
  }
  function zoomBranch(bname) {
    if (!lSvg || !linCur) return;
    var els = lSvg.querySelectorAll('.lg-node,.lg-edge'), minx = 1e9, miny = 1e9, maxx = -1e9, maxy = -1e9, hit = false;
    for (var k = 0; k < els.length; k++) {
      if (els[k].getAttribute('data-branch') !== bname) continue;
      var bb; try { bb = els[k].getBBox(); } catch (e) { continue; }
      hit = true; minx = Math.min(minx, bb.x); miny = Math.min(miny, bb.y);
      maxx = Math.max(maxx, bb.x + bb.width); maxy = Math.max(maxy, bb.y + bb.height);
    }
    if (!hit) { if (lSvg.getAttribute('data-full')) lSvg.setAttribute('viewBox', lSvg.getAttribute('data-full')); return; }
    var pad = 26;
    lSvg.setAttribute('viewBox', (minx - pad) + ' ' + (miny - pad) + ' ' + (maxx - minx + 2 * pad) + ' ' + (maxy - miny + 2 * pad));
  }
  (function wireLegend() {
    var chips = document.querySelectorAll('.lg-chip');
    for (var k = 0; k < chips.length; k++) {
      (function (c) {
        var b = c.getAttribute('data-branch');
        c.addEventListener('mouseenter', function () { isoBranch = b; applyIsolate(); });
        c.addEventListener('mouseleave', function () { isoBranch = null; applyIsolate(); });
        c.addEventListener('click', function () { zoomBranch(b); });
      })(chips[k]);
    }
  })();
  var lsel = document.getElementById('lineage-select');
  if (lsel) lsel.addEventListener('change', function () { renderTree(this.value || null); });
  var tbt = document.getElementById('temple-toggle');
  if (tbt) tbt.addEventListener('change', function () { if (gTemple) gTemple.style.display = tbt.checked ? '' : 'none'; });

  /* ── 启动 ── */
  drawBase();
  refresh();
  drawPlaces();
  drawTemples();
  (function initLineage() {
    if (LIN.masters && LIN.masters.length) {
      var def = findMaster('person_003') ? 'person_003' : LIN.masters[0].id;
      renderTree(def); setSel(def);
    }
  })();

  /* ── S6 深链初始化：读 URL 参数 person/station/year/master/temple（零坐标） ── */
  (function initFromURL() {
    var q = {};
    location.search.replace(/^\?/, '').split('&').forEach(function (kv) {
      if (!kv) return; var i = kv.indexOf('=');
      q[decodeURIComponent(kv.slice(0, i))] = decodeURIComponent(kv.slice(i + 1));
    });
    if (q.year) { var yy = nearestSnapshot(parseInt(q.year, 10)); if (yy != null && !isNaN(yy)) { cur = yy; refresh(); } }
    if (sel && q.person && findPerson(q.person)) {
      var p = findPerson(q.person);
      sel.value = q.person; pCur = q.person;
      stCur = p.stations[0].index;
      if (q.station != null) for (var i = 0; i < p.stations.length; i++) if (String(p.stations[i].index) === String(q.station)) stCur = p.stations[i].index;
      drawRoute(); showCard();
    }
    if (q.temple && findTemple(q.temple)) selectTemple(q.temple);
    if (q.master && findMaster(q.master)) { renderTree(q.master); setSel(q.master); }
  })();
})();

