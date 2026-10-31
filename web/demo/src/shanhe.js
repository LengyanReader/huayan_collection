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
  var tlRange = document.getElementById('tl-range');
  var tlYear = document.getElementById('tl-year');
  var tlMeta = document.getElementById('tl-meta');
  var tip = document.getElementById('tip');
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
          pth.setAttribute('fill', 'none'); pth.setAttribute('stroke', '#a83a24');
          pth.setAttribute('stroke-width', 1); pth.setAttribute('stroke-dasharray', '5,3');
          pth.setAttribute('opacity', 0.7);
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
    /* F.5 断代淡入过渡：整层 opacity 复位→下一帧升回（CSS #g-polity transition 承接） */
    gPoly.style.opacity = 0;
    requestAnimationFrame(function () { gPoly.style.opacity = 1; });
    updateTimeline();
  }
  function updateTimeline() {
    if (!tlRange) return;
    var d = yearData(cur), n = d ? d.polities.length : 0;
    if (tlYear) tlYear.textContent = cur;
    if (tlMeta) tlMeta.textContent = '依 ' + cur + ' 年最近断代快照 · 区内 ' + n + ' 政体 · 帝号/年号〔待核·断代底图未含〕';
    if (document.activeElement !== tlRange) tlRange.value = cur;   /* 外部改年代时吸附滑轨；拖拽中不打断 */
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
    if (BS.sel) parts.push('sel=' + encodeURIComponent(BS.sel));
    if (BS.view && BS.view !== 'tree') parts.push('view=' + encodeURIComponent(BS.view));
    var url = location.pathname + (parts.length ? ('?' + parts.join('&')) : '') + location.hash;
    try { history.replaceState(null, '', url); } catch (e) {}
  }

  var sel = document.getElementById('person-select');
  if (sel) sel.addEventListener('change', function () { selectPerson(this.value); });
  var pbtn = document.getElementById('st-prev'), nbtn = document.getElementById('st-next');
  if (pbtn) pbtn.addEventListener('click', function () { step(-1); });
  if (nbtn) nbtn.addEventListener('click', function () { step(1); });
  document.addEventListener('keydown', function (e) {
    if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;  /* F.5 搜索框内不劫持按键 */
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
      r.setAttribute('data-name', t.name); r.setAttribute('data-tp', '华严要地 · 点击开地谱卡');
      r.setAttribute('data-dy', t.dynasty || '');
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
  var collapseSet = {}, linZoom = null, linG = null, fullVB = null, lastLayout = [];
  var BS = { sel: null, view: 'tree' }, TREE_PARENT = {};
  var ROWH = 34, CWp = 190, PADL = 40, PADR = 200, PADV = 30;
  function metaOf(id) {
    var m = (window.__LIN_META || {})[id];
    return m || { name: null, verified: true, rel: null, branch: '华严五祖' };
  }
  function renderTree(mid) {
    if (!lSvg) return;
    var DS = window.d3;
    if (!DS) { lSvg.innerHTML = '<text x="14" y="20" fill="#b00" font-size="12">D3 未加载·法脉树不可用（静态兜底见下方无损表）</text>'; return; }
    linCur = mid || null; isoBranch = null;
    var svgS = DS.select(lSvg);
    linG = svgS.select('g.lin-g');
    if (linG.empty()) linG = svgS.append('g').attr('class', 'lin-g');
    if (!mid) {
      linG.selectAll('*').remove(); svgS.attr('viewBox', '0 0 900 60');
      linG.append('text').attr('x', 14).attr('y', 32).attr('font-size', 13).attr('fill', '#8a7a5a')
        .text('择祖师后展开其 N 代弟子链（直系＝实线／私淑·影响＝虚线·点节点重定根·⊖ 收展分支·滚轮缩放/拖拽平移·双击复位）');
      return;
    }
    /* —— 只读构树（单父·按首见父边·自环/环守卫·不擅改 SSOT）—— */
    var edges = LIN.trees[mid] || [], mrec = findMaster(mid);
    var NAME = {}, VER = {}, parentOf = {}, chEdge = {}, kids = {};
    NAME[mid] = mrec ? mrec.name : mid; VER[mid] = true;
    edges.forEach(function (e) {
      if (e.parent === e.disc) return;
      if (e.pname) NAME[e.parent] = e.pname;
      if (e.dname) NAME[e.disc] = e.dname;
      if (!(e.disc in VER)) VER[e.disc] = !!e.dverified;
      if (!(e.disc in parentOf)) { parentOf[e.disc] = e.parent; chEdge[e.disc] = { rel: e.rel, branch: e.branch }; }
    });
    Object.keys(parentOf).forEach(function (d) { var p = parentOf[d]; (kids[p] = kids[p] || []).push(d); });
    TREE_PARENT = parentOf;   /* G.4 选择总线：当前子树父链·供 bsReveal 展开祖先 */
    window.__LIN_META = {};
    Object.keys(NAME).concat([mid]).forEach(function (id) {
      window.__LIN_META[id] = { name: (id in NAME) ? NAME[id] : null, verified: (id in VER) ? VER[id] : true,
        rel: chEdge[id] ? chEdge[id].rel : null, branch: chEdge[id] ? chEdge[id].branch : '华严五祖' };
    });
    function buildNode(id) {
      var o = { id: id };
      var ch = collapseSet[id] ? [] : (kids[id] || []);
      if (ch.length) o.children = ch.map(buildNode);
      return o;
    }
    var root = DS.hierarchy(buildNode(mid));
    DS.tree().nodeSize([ROWH, CWp])(root);
    var nodes = root.descendants(), links = root.links();
    var sx = function (n) { return n.y; }, sy = function (n) { return n.x; };
    lastLayout = nodes.map(function (n) { return { id: n.data.id, x: sx(n), y: sy(n), branch: metaOf(n.data.id).branch }; });

    /* —— 连线（elbow 折线·直系实线／私淑·影响虚线·支系色）—— */
    var edgeSel = linG.selectAll('path.lg-edge').data(links, function (d) { return d.target.data.id; });
    edgeSel.exit().transition().duration(300).style('opacity', 0).remove();
    var edgeEnter = edgeSel.enter().append('path')
      .attr('class', function (d) { return 'lg-edge' + (metaOf(d.target.data.id).rel === 'INFLUENCED' ? ' inf' : ''); })
      .attr('data-branch', function (d) { return metaOf(d.target.data.id).branch; })
      .attr('stroke', function (d) { return BRANCH_COLOR[metaOf(d.target.data.id).branch] || '#888'; })
      .attr('fill', 'none').style('opacity', 0);
    edgeSel = edgeEnter.merge(edgeSel);
    edgeSel.transition().duration(450).style('opacity', 0.85)
      .attr('d', function (d) {
        var px = sx(d.source), py = sy(d.source), cx = sx(d.target), cy = sy(d.target), mx = (px + cx) / 2;
        return 'M' + px + ',' + py + 'L' + mx + ',' + py + 'L' + mx + ',' + cy + 'L' + cx + ',' + cy;
      });

    /* —— 节点（圆+名·root 加粗·未具名〔待核〕·⊖/⊕ 折叠钮·点节点重定根·悬停邻域高亮）—— */
    var nodeSel = linG.selectAll('g.lg-node').data(nodes, function (d) { return d.data.id; });
    nodeSel.exit().transition().duration(250).style('opacity', 0).remove();
    var nodeEnter = nodeSel.enter().append('g')
      .attr('transform', function (d) { return 'translate(' + sx(d) + ',' + sy(d) + ')'; })
      .style('cursor', 'pointer').style('opacity', 0);
    nodeEnter.append('circle').attr('stroke', '#fff').attr('stroke-width', 1);
    nodeEnter.append('text').attr('class', 'lg-label').attr('x', 9).attr('y', 4).attr('font-size', 11);
    nodeEnter.append('text').attr('class', 'lg-tog').attr('x', -15).attr('y', 4).attr('font-size', 12)
      .attr('fill', '#7a6a4a').style('cursor', 'pointer');
    nodeSel = nodeEnter.merge(nodeSel);
    /* 重定根后深度会变：class/root/circle 一律在合并集上重绘（不只在 enter），否则新根丢 .lg-root */
    nodeSel.attr('class', function (d) { return 'lg-node' + (d.depth === 0 ? ' lg-root' : ''); })
      .attr('data-id', function (d) { return d.data.id; })
      .attr('data-branch', function (d) { return metaOf(d.data.id).branch; });
    nodeSel.select('circle')
      .attr('r', function (d) { return d.depth === 0 ? 6 : 4.5; })
      .attr('fill', function (d) { return d.depth === 0 ? '#c0392b' : (BRANCH_COLOR[metaOf(d.data.id).branch] || '#8d5a2b'); });
    nodeSel.select('.lg-label')
      .attr('fill', function (d) { return metaOf(d.data.id).verified ? '#3a2f1e' : '#b00'; })
      .text(function (d) { var m = metaOf(d.data.id); return (m.name || d.data.id) + (m.verified ? '' : '〔待核〕'); });
    nodeSel.select('.lg-tog')
      .style('display', function (d) { return (kids[d.data.id] && kids[d.data.id].length) ? null : 'none'; })
      .text(function (d) { return collapseSet[d.data.id] ? '⊕' : '⊖'; });
    nodeSel.transition().duration(450).style('opacity', 1)
      .attr('transform', function (d) { return 'translate(' + sx(d) + ',' + sy(d) + ')'; });
    nodeSel.on('click', function (ev, d) {
      ev.stopPropagation();
      if (d.data.id !== linCur) { renderTree(d.data.id); setSel(d.data.id); }
      bsSelect(d.data.id, 'tree');
    });
    nodeSel.select('.lg-tog').on('click', function (ev, d) {
      ev.stopPropagation();
      collapseSet[d.data.id] = !collapseSet[d.data.id];
      renderTree(linCur);
    });
    nodeSel.on('mouseenter', function (ev, d) { hiNeighbor(d); }).on('mouseleave', clearHi);

    /* —— 视口 fit + 缩放平移 —— */
    var minx = 1e9, miny = 1e9, maxx = -1e9, maxy = -1e9;
    nodes.forEach(function (n) { var X = sx(n), Y = sy(n); if (X < minx) minx = X; if (X > maxx) maxx = X; if (Y < miny) miny = Y; if (Y > maxy) maxy = Y; });
    fullVB = (minx - PADL) + ' ' + (miny - PADV) + ' ' + (maxx - minx + PADL + PADR) + ' ' + (maxy - miny + 2 * PADV);
    svgS.attr('viewBox', fullVB);
    if (!linZoom) {
      linZoom = DS.zoom().scaleExtent([0.3, 5]).on('zoom', function (ev) { linG.attr('transform', ev.transform); });
      svgS.call(linZoom).on('dblclick.zoom', null);
      svgS.on('dblclick', resetView);
    } else {
      svgS.call(linZoom.transform, DS.zoomIdentity);
    }
    applyIsolate(); syncURL(); renderLinGeo(mid); bsApply();
  }
  function resetView() {
    if (!lSvg || !window.d3) return;
    var svgS = d3.select(lSvg);
    if (fullVB) svgS.attr('viewBox', fullVB);
    if (linZoom) svgS.transition().duration(350).call(linZoom.transform, d3.zoomIdentity);
  }
  function hiNeighbor(d) {
    if (!linG) return;
    var kin = {};
    d.ancestors().forEach(function (a) { kin[a.data.id] = 1; });
    d.descendants().forEach(function (n) { kin[n.data.id] = 1; });
    linG.selectAll('g.lg-node').style('opacity', function (n) { return kin[n.data.id] ? 1 : 0.16; });
    linG.selectAll('path.lg-edge').style('opacity', function (l) { return (kin[l.source.data.id] && kin[l.target.data.id]) ? 0.9 : 0.1; });
  }
  function clearHi() {
    if (!linG) return;
    linG.selectAll('g.lg-node').style('opacity', 1);
    linG.selectAll('path.lg-edge').style('opacity', 0.85);
    applyIsolate();
  }
  function applyIsolate() {
    if (!lSvg) return;
    var ns = lSvg.querySelectorAll('.lg-node'), es = lSvg.querySelectorAll('.lg-edge'), k;
    for (k = 0; k < ns.length; k++) ns[k].classList.toggle('dim', !!isoBranch && ns[k].getAttribute('data-branch') !== isoBranch);
    for (k = 0; k < es.length; k++) es[k].classList.toggle('dim', !!isoBranch && es[k].getAttribute('data-branch') !== isoBranch);
  }
  function zoomBranch(bname) {
    if (!lSvg || !linCur) return;
    resetView();
    if (!bname) return;
    var pts = lastLayout.filter(function (p) { return p.branch === bname; });
    if (!pts.length) return;
    var minx = 1e9, miny = 1e9, maxx = -1e9, maxy = -1e9;
    pts.forEach(function (p) { if (p.x < minx) minx = p.x; if (p.x > maxx) maxx = p.x; if (p.y < miny) miny = p.y; if (p.y > maxy) maxy = p.y; });
    lSvg.setAttribute('viewBox', (minx - PADL) + ' ' + (miny - PADV) + ' ' + (maxx - minx + PADL + PADR) + ' ' + (maxy - miny + 2 * PADV));
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
  if (lsel) lsel.addEventListener('change', function () { renderTree(this.value || null); renderRadial(this.value || null); });
  var tbt = document.getElementById('temple-toggle');
  if (tbt) tbt.addEventListener('change', function () { if (gTemple) gTemple.style.display = tbt.checked ? '' : 'none'; });

  /* ══ F.6a 法脉时间化：S4 树铺底图（地理质心+弧形师承边+分支色） ══ */
  var gLinGeo = document.getElementById('g-linmap');
  var lgeoTgl = document.getElementById('lingeo-toggle');
  var PGEO = S.person_geo || {};
  function renderLinGeo(mid) {
    if (!gLinGeo) return;
    while (gLinGeo.firstChild) gLinGeo.removeChild(gLinGeo.firstChild);
    if (!mid || !lgeoTgl || !lgeoTgl.checked) { if (gLinGeo) gLinGeo.style.display = 'none'; return; }
    gLinGeo.style.display = '';
    var edges = LIN.trees[mid] || [];
    var mrec = findMaster(mid);
    var nodes = {}; nodes[mid] = { id: mid, name: mrec ? mrec.name : mid, branch: '华严五祖' };
    edges.forEach(function (e) {
      if (!nodes[e.parent]) nodes[e.parent] = { id: e.parent, name: e.pname || e.parent, branch: e.branch };
      if (!nodes[e.disc]) nodes[e.disc] = { id: e.disc, name: e.dname || null, branch: e.branch };
    });
    // draw edges as arcs
    edges.forEach(function (e) {
      var pf = PGEO[e.parent], pt = PGEO[e.disc];
      if (!pf || !pt) return;
      var mx = (pf.x + pt.x) / 2, my = (pf.y + pt.y) / 2 - Math.abs(pt.x - pf.x) * 0.18;
      var col = BRANCH_COLOR[e.branch] || '#888';
      var path = el('path', { d: 'M' + pf.x + ',' + pf.y + ' Q' + mx + ',' + my + ' ' + pt.x + ',' + pt.y,
        'class': 'lm-edge' + (e.rel === 'INFLUENCED' ? ' inf' : ''), stroke: col, 'data-branch': e.branch });
      gLinGeo.appendChild(path);
    });
    // draw nodes
    Object.keys(nodes).forEach(function (k) {
      var n = nodes[k], g = PGEO[k]; if (!g) return;
      var gg = el('g', { 'class': 'lm-node', 'data-branch': n.branch, 'data-id': k });
      var isRoot = (k === mid);
      gg.appendChild(el('circle', { cx: g.x, cy: g.y, r: isRoot ? 7 : 4.5,
        fill: BRANCH_COLOR[n.branch] || '#8d5a2b', stroke: '#fff', 'stroke-width': isRoot ? 2 : 1.2 }));
      var tx = el('text', { x: g.x + 8, y: g.y + 3, 'font-size': isRoot ? 11 : 9 });
      tx.textContent = (n.name || k) + (g.year ? ' (' + g.year + ')' : '');
      gg.appendChild(tx);
      gg.style.cursor = 'pointer';
      gg.addEventListener('click', (function (nid) { return function () { if (nid !== linCur) { renderTree(nid); setSel(nid); renderLinGeo(nid); } bsSelect(nid, 'map'); }; })(k));
      gLinGeo.appendChild(gg);
    });
    bsApply();
  }
  if (lgeoTgl) lgeoTgl.addEventListener('change', function () { renderLinGeo(linCur); });

  /* ══ G.2 全法脉网络总览（d3-force 力导向·80 点/97 边·只画现存边·零臆造）══
     节点半径＝直系出度·色＝所属支系·实线=师承/虚线=影响/淡线=同期·拖拽·缩放·邻域高亮·点节点聚焦直系子网络 */
  var NET = S.lineage_net || { nodes: [], links: [], branches: [] };
  var nSvg = document.getElementById('lineage-net-svg');
  var NET_BCOL = {}; (NET.branches || []).forEach(function (b) { NET_BCOL[b.name] = b.color; });
  var NET_ADJ = {}, NET_CHILD = {};
  (NET.links || []).forEach(function (l) {
    (NET_ADJ[l.source] = NET_ADJ[l.source] || {})[l.target] = 1;
    (NET_ADJ[l.target] = NET_ADJ[l.target] || {})[l.source] = 1;
    if (l.rel === 'MASTER_OF') (NET_CHILD[l.source] = NET_CHILD[l.source] || {})[l.target] = 1;
  });
  function netSubtree(id) { var seen = {}, st = [id]; while (st.length) { var c = st.pop(); if (seen[c]) continue; seen[c] = 1; var ch = NET_CHILD[c] || {}; for (var k in ch) st.push(k); } return seen; }
  var netSim = null, netG = null, netNodeSel = null, netLinkSel = null, netZoom = null, netFocus = null;
  var NW = 960, NH = 620;
  function netRad(d) { return 4 + Math.sqrt(d.out || 0) * 2.4; }
  function netCol(d) { return NET_BCOL[(d.branches || [])[0]] || '#8d5a2b'; }
  function netDraw() {
    if (!netLinkSel || !netNodeSel) return;
    netLinkSel.attr('x1', function (l) { return l.source.x; }).attr('y1', function (l) { return l.source.y; })
      .attr('x2', function (l) { return l.target.x; }).attr('y2', function (l) { return l.target.y; });
    netNodeSel.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
  }
  function netTipHtml(d) {
    var nm = d.name || ('〔待核〕' + d.id), br = (d.branches || []).join('·');
    return '<b>' + esc(nm) + '</b><br>支系：' + esc(br || '—') +
      '<br>直系弟子出度 ' + (d.out || 0) + ' · 受法入度 ' + (d.in || 0) +
      (d.verified ? '' : '<br><span style="color:#e0a">未具名·仅见边注〔待核〕</span>');
  }
  function applyFocus() {
    if (!netNodeSel) return;
    if (!netFocus) { netNodeSel.classed('dim', false); netLinkSel.classed('dim', false); return; }
    var sub = netSubtree(netFocus);
    netNodeSel.classed('dim', function (n) { return !sub[n.id]; });
    netLinkSel.classed('dim', function (l) { return !(sub[l.source.id] && sub[l.target.id]); });
  }
  function renderNet() {
    if (!nSvg) return;
    var DS = window.d3;
    if (!DS) { nSvg.innerHTML = '<text x="14" y="24" font-size="12" fill="#b00">D3 未加载·网络图不可用（静态兜底边表见下方）</text>'; return; }
    netFocus = null;
    var svgS = DS.select(nSvg);
    svgS.selectAll('*').remove();
    netG = svgS.append('g').attr('class', 'net-g');
    var nodes = (NET.nodes || []).map(function (n) { return Object.assign({}, n); });
    var links = (NET.links || []).map(function (l) { return Object.assign({}, l); });
    if (!netSim) {
      netSim = DS.forceSimulation()
        .force('link', DS.forceLink().id(function (d) { return d.id; })
          .distance(function (l) { return l.rel === 'MASTER_OF' ? 46 : (l.rel === 'INFLUENCED' ? 72 : 96); }).strength(0.5))
        .force('charge', DS.forceManyBody().strength(-150).distanceMax(300))
        .force('center', DS.forceCenter(NW / 2, NH / 2))
        .force('x', DS.forceX(NW / 2).strength(0.05))
        .force('y', DS.forceY(NH / 2).strength(0.09))
        .force('collide', DS.forceCollide().radius(function (d) { return netRad(d) + 6; }));
    }
    netLinkSel = netG.append('g').selectAll('line.net-link').data(links).enter().append('line')
      .attr('class', function (l) { return 'net-link' + (l.rel === 'INFLUENCED' ? ' inf' : (l.rel === 'CONTEMPORARY' ? ' contemp' : '')); })
      .attr('stroke', function (l) { return l.color || '#999'; })
      .attr('data-branch', function (l) { return l.branch; })
      .attr('data-rel', function (l) { return l.rel; });
    netNodeSel = netG.append('g').selectAll('g.net-node').data(nodes).enter().append('g')
      .attr('class', 'net-node').attr('data-branch', function (d) { return (d.branches || [])[0] || ''; })
      .attr('data-id', function (d) { return d.id; })
      .call(DS.drag()
        .on('start', function (ev, d) { var np = document.getElementById('net-phys'); if (np && np.checked && !ev.active) netSim.alphaTarget(0.25).restart(); d.fx = d.x; d.fy = d.y; })
        .on('drag', function (ev, d) { d.fx = ev.x; d.fy = ev.y; var np = document.getElementById('net-phys'); if (np && !np.checked) { d.x = ev.x; d.y = ev.y; netDraw(); } })
        .on('end', function (ev, d) { var np = document.getElementById('net-phys'); if (np && np.checked) { if (!ev.active) netSim.alphaTarget(0); d.fx = null; d.fy = null; } else { d.x = d.fx; d.y = d.fy; netDraw(); } }));
    netNodeSel.append('circle').attr('r', netRad).attr('fill', netCol).attr('stroke', '#fff').attr('stroke-width', 1);
    netNodeSel.append('text').attr('class', 'net-label').attr('x', function (d) { return netRad(d) + 3; }).attr('y', 3)
      .text(function (d) { return (d.name || d.id) + (d.verified ? '' : '〔待核〕'); });
    netNodeSel.on('mouseenter', function (ev, d) {
      var nb = NET_ADJ[d.id] || {};
      netNodeSel.classed('dim', function (n) { return !(n.id === d.id || nb[n.id]); });
      netLinkSel.classed('dim', function (l) { return !(l.source.id === d.id || l.target.id === d.id); });
      showTip(netTipHtml(d), ev.clientX, ev.clientY);
    }).on('mousemove', function (ev) { var t = tip; if (t && !t.hidden) { var r = t.getBoundingClientRect(); showTip(t.innerHTML, ev.clientX - 14, ev.clientY - 14); } })
      .on('mouseleave', function () { hideTip(); applyFocus(); })
      .on('click', function (ev, d) { ev.stopPropagation(); netFocus = (netFocus === d.id ? null : d.id); applyFocus(); bsSelect(d.id, 'net'); });
    netSim.nodes(nodes);
    netSim.force('link').links(links);
    netSim.on('tick', netDraw);
    netSim.alpha(1).restart();
    if (!netZoom) {
      netZoom = DS.zoom().scaleExtent([0.3, 4]).on('zoom', function (ev) { netG.attr('transform', ev.transform); });
      svgS.call(netZoom);
    }
    var nl = document.getElementById('net-labels');
    netNodeSel.selectAll('text.net-label').style('display', (nl && nl.checked) ? null : 'none');
    bsApply();
  }
  (function wireNet() {
    var nb = document.getElementById('net-reset');
    if (nb) nb.addEventListener('click', function () {
      netFocus = null; applyFocus();
      if (nSvg && window.d3 && netZoom) window.d3.select(nSvg).transition().duration(300).call(netZoom.transform, window.d3.zoomIdentity);
    });
    var nl = document.getElementById('net-labels');
    if (nl) nl.addEventListener('change', function () {
      if (netNodeSel) netNodeSel.selectAll('text.net-label').style('display', nl.checked ? null : 'none');
    });
    var np = document.getElementById('net-phys');
    if (np) np.addEventListener('change', function () {
      if (!netSim) return;
      if (np.checked) netSim.alpha(0.3).restart();
      else { netSim.stop(); (netSim.nodes() || []).forEach(function (d) { d.fx = d.x; d.fy = d.y; }); }
    });
  })();

  /* ═ G.3 放射式·时间轴法脉（d3.tree radial）══
     圆心＝择定祖师·半径＝代际·角度按代际均分或公元纪年·环刻度＝世代·直系实线/影响虚线 */
  var rSvg = document.getElementById('lineage-radial-svg');
  var RCEN = 380, RRR = 320, rdG = null, rdZoom = null, rdCur = null;
  function rdYearMode() { var y = document.getElementById('rd-angle-year'); return !!(y && y.checked); }
  function yearOf(id) { var g = PGEO[id]; return (g && g.year != null) ? g.year : null; }
  function renderRadial(mid) {
    if (!rSvg) return;
    var DS = window.d3;
    if (!DS) { rSvg.innerHTML = '<text x="14" y="24" font-size="12" fill="#b00">D3 未加载·放射图不可用（静态兜底见下方 S4 弟子链表）</text>'; return; }
    rdCur = mid || null;
    var svgS = DS.select(rSvg);
    svgS.selectAll('*').remove();
    rdG = svgS.append('g').attr('class', 'rd-g');
    if (!mid) {
      rdG.append('text').attr('text-anchor', 'middle').attr('y', 4).attr('font-size', 13).attr('fill', '#8a7a5a')
        .text('择祖师后以其为圆心展开放射法脉（半径＝代际·点节点重定根·⊖ 收展·滚轮缩放）');
      return;
    }
    /* —— 只读构树（与 G.1 同一守卫：单父·自环跳·环不擅改 SSOT）—— */
    var edges = LIN.trees[mid] || [], mrec = findMaster(mid);
    var NAME = {}, VER = {}, parentOf = {}, chEdge = {}, kids = {};
    NAME[mid] = mrec ? mrec.name : mid; VER[mid] = true;
    edges.forEach(function (e) {
      if (e.parent === e.disc) return;
      if (e.pname) NAME[e.parent] = e.pname;
      if (e.dname) NAME[e.disc] = e.dname;
      if (!(e.disc in VER)) VER[e.disc] = !!e.dverified;
      if (!(e.disc in parentOf)) { parentOf[e.disc] = e.parent; chEdge[e.disc] = { rel: e.rel, branch: e.branch }; }
    });
    Object.keys(parentOf).forEach(function (d) { (kids[parentOf[d]] = kids[parentOf[d]] || []).push(d); });
    function rmeta(id) { return { name: (id in NAME) ? NAME[id] : null, verified: (id in VER) ? VER[id] : true, rel: chEdge[id] ? chEdge[id].rel : null, branch: chEdge[id] ? chEdge[id].branch : '华严五祖' }; }
    function rcol(id) { return BRANCH_COLOR[rmeta(id).branch] || '#8d5a2b'; }
    function build(id) { var o = { id: id }; var ch = collapseSet[id] ? [] : (kids[id] || []); if (ch.length) o.children = ch.map(build); return o; }
    var root = DS.hierarchy(build(mid));
    DS.tree().size([2 * Math.PI, RRR]).separation(function (a, b) { return a.parent === b.parent ? 1 : 2.2; })(root);
    var maxD = root.height || 1;
    /* —— 角度：代际均分（tree.x）或纪年映射（scaleLinear 年→角·无纪年继承父角·不插值）—— */
    var ymode = rdYearMode(), ys = null;
    if (ymode) {
      var yrs = root.descendants().map(function (n) { return yearOf(n.data.id); }).filter(function (v) { return v != null; });
      if (yrs.length >= 2 && DS.max(yrs) > DS.min(yrs)) ys = DS.scaleLinear().domain([DS.min(yrs), DS.max(yrs)]).range([0, 2 * Math.PI]);
    }
    root.eachBefore(function (n) {
      n.rdR = n.y;
      if (ys) { var yy = yearOf(n.data.id); n.rdA = (yy != null) ? ys(yy) : (n.depth === 0 ? 0 : n.parent.rdA); }
      else n.rdA = n.x;
    });
    var nodes = root.descendants(), links = root.links();
    function rpx(n) { return n.rdR * Math.sin(n.rdA); }
    function rpy(n) { return -n.rdR * Math.cos(n.rdA); }
    /* —— 世代导环 + 刻度（纪年模式加年代辐条）—— */
    var ringG = rdG.append('g').attr('class', 'rd-rings');
    for (var g = 1; g <= maxD; g++) {
      var rr = (g / maxD) * RRR;
      ringG.append('circle').attr('class', 'rd-ring').attr('r', rr);
      ringG.append('text').attr('class', 'rd-rlabel').attr('x', 3).attr('y', -rr - 1).text(g + '代');
    }
    if (ys) {
      var tks = ys.ticks ? ys.ticks(6) : [];
      tks.forEach(function (yr) {
        var a = ys(yr), sx = Math.sin(a) * RRR, sy = -Math.cos(a) * RRR;
        ringG.append('line').attr('class', 'rd-tick').attr('x1', 0).attr('y1', 0).attr('x2', sx * 0.55).attr('y2', sy * 0.55);
        ringG.append('text').attr('class', 'rd-rlabel').attr('x', sx * 1.06).attr('y', sy * 1.06).attr('text-anchor', 'middle').text(yr);
      });
    }
    /* —— 连线（linkRadial 直系实线/影响虚线/支系色）—— */
    var linkGen = DS.linkRadial().angle(function (d) { return d.rdA; }).radius(function (d) { return d.rdR; });
    var lk = rdG.append('g').selectAll('path.rd-link').data(links).enter().append('path')
      .attr('class', function (d) { return 'rd-link' + (rmeta(d.target.data.id).rel === 'INFLUENCED' ? ' inf' : ''); })
      .attr('stroke', function (d) { return rcol(d.target.data.id); })
      .attr('data-branch', function (d) { return rmeta(d.target.data.id).branch; })
      .attr('d', linkGen);
    /* —— 节点（圆+水平名·root 加粗·未具名〔待核〕·⊖/⊕ 折叠·点重定根·悬停直系链高亮）—— */
    var nd = rdG.append('g').selectAll('g.rd-node').data(nodes).enter().append('g')
      .attr('class', function (d) { return 'rd-node' + (d.depth === 0 ? ' rd-root' : ''); })
      .attr('data-id', function (d) { return d.data.id; })
      .attr('data-branch', function (d) { return rmeta(d.data.id).branch; })
      .attr('transform', function (d) { return 'translate(' + rpx(d) + ',' + rpy(d) + ')'; })
      .style('cursor', 'pointer');
    nd.append('circle').attr('r', function (d) { return d.depth === 0 ? 6 : 4; }).attr('fill', function (d) { return d.depth === 0 ? '#c0392b' : rcol(d.data.id); }).attr('stroke', '#fff').attr('stroke-width', 1);
    var showL = document.getElementById('rd-labels'); showL = !showL || showL.checked;
    nd.append('text').attr('class', 'rd-label')
      .attr('text-anchor', function (d) { return Math.sin(d.rdA) >= 0 ? 'start' : 'end'; })
      .attr('x', function (d) { return Math.sin(d.rdA) >= 0 ? 6 : -6; }).attr('y', 3)
      .style('display', showL ? null : 'none')
      .attr('fill', function (d) { return rmeta(d.data.id).verified ? '#3a2f1e' : '#b00'; })
      .text(function (d) { var m = rmeta(d.data.id); return (m.name || d.data.id) + (m.verified ? '' : '〔待核〕'); });
    nd.append('text').attr('class', 'rd-tog').attr('y', 4).attr('text-anchor', 'middle').attr('font-size', 11).attr('fill', '#7a6a4a').style('cursor', 'pointer')
      .style('display', function (d) { return (kids[d.data.id] && kids[d.data.id].length) ? null : 'none'; })
      .attr('x', function (d) { return d.depth === 0 ? 0 : (Math.sin(d.rdA) >= 0 ? -9 : 9); })
      .text(function (d) { return collapseSet[d.data.id] ? '⊕' : '⊖'; });
    nd.on('click', function (ev, d) { ev.stopPropagation(); if (d.data.id !== linCur) { renderTree(d.data.id); setSel(d.data.id); renderRadial(d.data.id); } bsSelect(d.data.id, 'radial'); });
    nd.select('.rd-tog').on('click', function (ev, d) { ev.stopPropagation(); collapseSet[d.data.id] = !collapseSet[d.data.id]; renderTree(linCur); renderRadial(linCur); });
    nd.on('mouseenter', function (ev, d) { var kin = {}; d.ancestors().forEach(function (a) { kin[a.data.id] = 1; }); d.descendants().forEach(function (n) { kin[n.data.id] = 1; }); nd.classed('dim', function (n) { return !kin[n.data.id]; }); lk.classed('dim', function (l) { return !(kin[l.source.data.id] && kin[l.target.data.id]); }); })
      .on('mouseleave', function () { nd.classed('dim', false); lk.classed('dim', false); });
    /* —— 缩放平移（初变中位归入 zoom transform·保确定性）—— */
    if (!rdZoom) { rdZoom = DS.zoom().scaleExtent([0.4, 4]).on('zoom', function (ev) { rdG.attr('transform', ev.transform); }); svgS.call(rdZoom).on('dblclick.zoom', null); }
    svgS.call(rdZoom.transform, DS.zoomIdentity.translate(RCEN, RCEN));
    bsApply();
  }
  (function wireRadial() {
    var rb = document.getElementById('radial-reset');
    if (rb) rb.addEventListener('click', function () { Object.keys(collapseSet).forEach(function (k) { delete collapseSet[k]; }); renderTree(linCur); renderRadial(linCur); });
    ['rd-angle-gen', 'rd-angle-year'].forEach(function (idv) { var el2 = document.getElementById(idv); if (el2) el2.addEventListener('change', function () { renderRadial(rdCur); }); });
    var rl = document.getElementById('rd-labels');
    if (rl) rl.addEventListener('change', function () { if (rSvg) { var ts = rSvg.querySelectorAll('text.rd-label'); for (var k = 0; k < ts.length; k++) ts[k].style.display = rl.checked ? null : 'none'; } });
  })();

  /* ══ G.4 四视图联动·选择总线（任一选中→弟子树/放射/网络/地理同步高亮该人及其一阶邻域）══ */
  function bsRelated(id) { var s = {}; if (!id) return s; s[id] = 1; var nb = NET_ADJ[id] || {}; for (var k in nb) s[k] = 1; return s; }
  function bsStatus(id) {
    var st = document.getElementById('bs-status'); if (!st) return;
    if (!id) { st.textContent = '选择总线：点任一视图节点→四视图同步高亮该师及其一阶邻域；再点同一节点或空白处取消。'; return; }
    var nb = NET_ADJ[id] || {}, cnt = 0; for (var k in nb) cnt++;
    var nm = (PNAME[id] || (window.__LIN_META && window.__LIN_META[id] && window.__LIN_META[id].name) || id);
    st.innerHTML = '已选：<b>' + esc(nm) + '</b>（' + esc(id) + '）·一阶邻域 ' + cnt + ' 人·四视图已联动高亮（再点取消）';
  }
  function bsApply() {
    var rel = bsRelated(BS.sel);
    var conts = ['#lineage-svg', '#lineage-radial-svg', '#lineage-net-svg', '#g-linmap'];
    conts.forEach(function (c) {
      var svg = document.querySelector(c); if (!svg) return;
      var ns = svg.querySelectorAll('[data-id]');
      for (var i = 0; i < ns.length; i++) {
        var node = ns[i], d = node.getAttribute('data-id');
        node.classList.toggle('bs-hl', !!BS.sel && d === BS.sel);
        node.classList.toggle('bs-neighbor', !!BS.sel && d !== BS.sel && !!rel[d]);
      }
    });
    bsStatus(BS.sel);
  }
  function bsReveal(id) { if (!id || !TREE_PARENT[id]) return false; var changed = false, cur = id; while (cur) { if (collapseSet[cur]) { delete collapseSet[cur]; changed = true; } cur = TREE_PARENT[cur]; } return changed; }
  function bsSelect(id, view) {
    if (view) BS.view = view;
    if (!id) { bsClear(); return; }
    if (BS.sel === id) { BS.sel = null; }
    else {
      BS.sel = id;
      if (bsReveal(id)) { if (linCur) renderTree(linCur); if (rdCur) renderRadial(rdCur); }
    }
    bsApply(); syncURL();
  }
  function bsClear() { BS.sel = null; bsApply(); syncURL(); }
  (function wireBusGlobal() {
    var nrs = document.getElementById('net-reset'); if (nrs) nrs.addEventListener('click', bsClear);
    var rrs = document.getElementById('radial-reset'); if (rrs) rrs.addEventListener('click', bsClear);
    ['#lineage-svg', '#lineage-radial-svg', '#lineage-net-svg'].forEach(function (sid) {
      var s = document.getElementById(sid.slice(1)); if (s) s.addEventListener('click', function (ev) { if (!(ev.target.closest && ev.target.closest('[data-id]'))) bsClear(); });
    });
    var ls2 = document.getElementById('lineage-select');
    if (ls2) ls2.addEventListener('change', function () { if (this.value) bsSelect(this.value, 'tree'); });
  })();

  /* ══ F.5 视觉持平：连续时间滑轨 · hover tooltip · 全局搜索（/ 聚焦）══ */
  if (tlRange) tlRange.addEventListener('input', function () {
    var snap = nearestSnapshot(parseInt(this.value, 10));
    if (snap != null) { cur = snap; refresh(); }
  });
  function showTip(html, x, y) {
    if (!tip) return; tip.innerHTML = html; tip.hidden = false;
    var pad = 14, w = tip.offsetWidth, h = tip.offsetHeight, L = x + pad, T = y + pad;
    if (L + w > window.innerWidth) L = x - w - pad;
    if (T + h > window.innerHeight) T = y - h - pad;
    tip.style.left = L + 'px'; tip.style.top = T + 'px';
  }
  function hideTip() { if (tip) tip.hidden = true; }
  if (svg) svg.addEventListener('mousemove', function (ev) {
    var t = ev.target, nm = t.getAttribute && t.getAttribute('data-name');
    if (!nm) { hideTip(); return; }
    var line = '<b>' + esc(nm) + '</b>', dy = t.getAttribute('data-dy'), tp = t.getAttribute('data-tp');
    if (dy) line += '<br>' + esc(dy);
    if (tp) line += (dy ? ' · ' : '<br>') + esc(tp);
    var yr = t.getAttribute('data-year'); if (yr) line += '<br>' + esc(yr) + ' 年快照';
    var sup = t.getAttribute('data-sup'); if (sup != null) line += '<br>宗主／归因：' + esc(sup || '—');
    var pr = t.getAttribute('data-pr'); if (pr != null) line += '<br>边界精度 ' + (pr === '' ? '〔待核〕' : esc(pr) + '/3');
    showTip(line, ev.clientX, ev.clientY);
  });
  if (svg) svg.addEventListener('mouseleave', hideTip);
  (function initSearch() {
    var gi = document.getElementById('gs-input'), gd = document.getElementById('gs-drop');
    if (!gi || !gd) return;
    var idx = [];
    PERSONS.forEach(function (p) { idx.push({ kind: '祖师行迹', name: p.name, go: function () { var s = document.getElementById('person-select'); if (s) s.value = p.id; selectPerson(p.id); } }); });
    TEMPLES.forEach(function (t) { idx.push({ kind: '要地', name: t.name, go: function () { var s = document.getElementById('temple-toggle'); if (s && !s.checked) { s.checked = true; if (gTemple) gTemple.style.display = ''; } selectTemple(t.id); } }); });
    (LIN.masters || []).forEach(function (m) { idx.push({ kind: '法师·法脉', name: m.name, go: function () { renderTree(m.id); setSel(m.id); } }); });
    var hits = [], sel = -1;
    function match(q) { return q ? idx.filter(function (it) { return it.name && it.name.indexOf(q) >= 0; }) : []; }
    function render() {
      if (!hits.length) { gd.hidden = true; return; }
      gd.innerHTML = hits.map(function (it, i) {
        return '<div class="it' + (i === sel ? ' sel' : '') + '" data-i="' + i + '"><span>' + esc(it.name) + '</span><span class="tag">' + esc(it.kind) + '</span></div>';
      }).join('');
      gd.hidden = false;
    }
    function choose(i) { if (i < 0 || i >= hits.length) return; hits[i].go(); gi.value = hits[i].name; gd.hidden = true; sel = -1; }
    gi.addEventListener('input', function () { hits = match(this.value.trim()); sel = hits.length ? 0 : -1; render(); });
    gi.addEventListener('focus', function () { var q = gi.value.trim(); hits = q ? match(q) : idx.slice(0, 15); sel = hits.length ? 0 : -1; render(); });
    gi.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); sel = Math.min(sel + 1, hits.length - 1); render(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); sel = Math.max(sel - 1, 0); render(); }
      else if (e.key === 'Enter') { e.preventDefault(); choose(sel >= 0 ? sel : 0); }
      else if (e.key === 'Escape') { gd.hidden = true; gi.blur(); }
    });
    gd.addEventListener('click', function (e) { var d = e.target.closest ? e.target.closest('.it') : null; if (d) choose(parseInt(d.getAttribute('data-i'), 10)); });
    document.addEventListener('click', function (e) { if (!(e.target.closest && e.target.closest('#gs'))) gd.hidden = true; });
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== gi && !/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName || '')) { e.preventDefault(); gi.focus(); gi.select(); }
    });
  })();

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
  renderNet();   /* G.2 全法脉网络总览 */
  renderRadial(linCur);   /* G.3 放射式·时间轴法脉（随 S4 当前祖师）*/

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
    if (q.master && findMaster(q.master)) { renderTree(q.master); setSel(q.master); renderRadial(q.master); }
    /* G.4 深链复位：选择总线 sel + 激活视图 view（零坐标·仅语义） */
    if (q.view) BS.view = q.view;
    if (q.sel) { BS.sel = q.sel; if (bsReveal(q.sel)) { if (linCur) renderTree(linCur); if (rdCur) renderRadial(rdCur); } bsApply(); }
    if (q.view) { var vmap = { tree: 'lineage-box', radial: 'radial-box', net: 'net-box', map: 'lineage-box' }; var ve = document.getElementById(vmap[q.view] || ''); if (ve && ve.scrollIntoView) ve.scrollIntoView({ block: 'start' }); }
  })();
})();

