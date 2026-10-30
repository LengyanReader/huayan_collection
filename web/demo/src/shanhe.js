/* shanhe.js — 「山河法脉」子页渲染器（F.2 底图骨架·famai/shanhe.html 专用·standalone）
   数据契约：注入的全局 SHANHE = {
     canvas:{w,h}, view:{lon:[min,max],lat:[min,max]},
     years:[{year, polities:[{n,sup,pr, rings:[[[x,y],…],…]}]}],   // 坐标已由 Python 投影为画布坐标
     base:{coast:[rings], countries:[rings]},
     places:[{id,n,lat,lng,tp,dy,x,y}],
     meta:{generated, license_note}
   } 静态兜底表（信息無损）在 DOM 中先行存在，本脚本只做增强。 */
(function () {
  var S = window.SHANHE;
  if (!S) return;
  var svg = document.getElementById('map-svg');
  var gBase = document.getElementById('g-base');
  var gPoly = document.getElementById('g-polity');
  var gGhost = document.getElementById('g-ghost');
  var gPlace = document.getElementById('g-place');
  var panel = document.getElementById('info-panel');
  var cur = S.years.length ? S.years[0].year : null;

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

  /* ── 启动 ── */
  drawBase();
  refresh();
  drawPlaces();
})();
