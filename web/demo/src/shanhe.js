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
    var qs = '';
    if (pCur) qs = 'person=' + encodeURIComponent(pCur) + '&station=' + encodeURIComponent(stCur);
    var url = location.pathname + (qs ? ('?' + qs) : '') + location.hash;
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

  /* ── 启动 ── */
  drawBase();
  refresh();
  drawPlaces();

  /* ── S6 深链初始化：读 URL 参数 person/station/year（零坐标） ── */
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
  })();
})();

