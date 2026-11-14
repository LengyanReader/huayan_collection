/* pin_nav.js — L.473 华严经学系列·品目导航（FAB＋抽屉＋前后品底栏）
 * 数据：window.HUAYAN_NAV（build.py 生成·九会分组＋配套专文）· window.NAV_CURRENT（当前页 id）
 * 交互：点击 FAB 开抽屉；当前页金色高亮「当前」；prev/next 品快跳；ESC/点外关闭；手机全宽。
 * 品页另渲染底部「上一品/下一品」条（顺序阅读）。
 */
(function () {
  'use strict';
  if (typeof window.HUAYAN_NAV === 'undefined' || typeof window.NAV_CURRENT === 'undefined') return;
  var NAV = window.HUAYAN_NAV;
  var CUR = window.NAV_CURRENT;
  if (document.getElementById('nav-fab')) return;

  var PINS = [];
  NAV.hui.forEach(function (h) { h.items.forEach(function (p) { PINS.push(p); }); });
  var idx = -1;
  PINS.forEach(function (p, i) { if (p.id === CUR) idx = i; });
  var isPin = idx >= 0;

  /* ── 样式 ── */
  var css = document.createElement('style');
  css.textContent =
    '#nav-fab{position:fixed;right:18px;bottom:132px;z-index:1250;height:42px;padding:0 14px 0 12px;border-radius:21px;' +
    'display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(94,139,158,.8);background:rgba(31,36,42,.96);' +
    'color:#8fb8de;font-size:14px;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,.35);font-family:inherit}' +
    '#nav-fab:hover{background:rgba(52,58,66,.97);transform:translateY(-1px)}' +
    '#nav-fab .nv-ico{font-size:17px;line-height:1}' +
    '#nav-panel{position:fixed;right:0;top:0;bottom:0;width:min(46vw,520px);z-index:1300;display:none;' +
    'flex-direction:column;background:#1e222a;color:#d6d2c6;border-left:2px solid #5e8b9e;' +
    'box-shadow:-6px 0 24px rgba(0,0,0,.3)}' +
    '#nav-panel .nv-head{display:flex;align-items:center;gap:8px;padding:12px 14px;background:#2c2620;color:#e8c877}' +
    '#nav-panel .nv-head .nv-t{flex:1;font-size:.95em;font-weight:700}' +
    '#nav-panel .nv-pn{display:flex;gap:6px}' +
    '#nav-panel .nv-pn button{background:none;border:1px solid rgba(232,200,119,.5);color:#e8c877;' +
    'border-radius:8px;padding:4px 10px;cursor:pointer;font-size:.8em;font-family:inherit}' +
    '#nav-panel .nv-pn button:disabled{opacity:.4;cursor:not-allowed}' +
    '#nav-panel .nv-pn button:hover:not(:disabled){background:rgba(232,200,119,.15)}' +
    '#nav-panel .nv-close{background:none;border:none;color:#e8c877;font-size:16px;cursor:pointer}' +
    '#nav-panel .nv-body{flex:1;overflow-y:auto;padding:10px 12px 20px}' +
    '#nav-panel details{margin:0 0 8px;border:1px solid #343a45;border-radius:9px;background:#23262e}' +
    '#nav-panel details summary{cursor:pointer;list-style:none;padding:8px 12px;font-size:.88em;color:#cfc6b4;' +
    'display:flex;align-items:center;gap:6px;border-radius:9px}' +
    '#nav-panel details summary::-webkit-details-marker{display:none}' +
    '#nav-panel details summary::before{content:"▸";color:#8fb8de}' +
    '#nav-panel details[open] summary::before{content:"▾"}' +
    '#nav-panel details summary:hover{background:rgba(255,255,255,.05)}' +
    '#nav-panel .nv-grid{display:flex;flex-wrap:wrap;gap:7px;padding:6px 8px 8px}' +
    '#nav-panel a.nv-chip{display:inline-flex;align-items:center;gap:5px;border-radius:14px;padding:5px 11px;' +
    'font-size:.82em;text-decoration:none;color:#cfc6b4;border:1px solid #343a45;background:#1e222a}' +
    '#nav-panel a.nv-chip:hover{background:#2c313b;color:#fff}' +
    '#nav-panel a.nv-chip.is-cur{background:rgba(232,200,119,.18);color:#e8c877;border-color:#c9a45c;font-weight:700}' +
    '#nav-panel a.nv-chip.is-cur::after{content:"当前";font-size:.72em;color:#e8c877;' +
    'border:1px solid #c9a45c;border-radius:8px;padding:1px 5px;margin-left:2px}' +
    '#nav-panel .nv-b{font-size:.72em;color:#8a93a0;display:block;padding:4px 12px 0}' +
    '#nav-panel .nv-foot{padding:8px 14px;border-top:1px solid #343a45;font-size:.8em}' +
    '#nav-panel .nv-foot a{color:#8fb8de;text-decoration:none}' +
    '#pin-footnav{max-width:min(1500px,96vw);margin:18px auto 8px;display:flex;justify-content:space-between;gap:10px}' +
    '#pin-footnav a{flex:1;padding:10px 14px;border:1px solid var(--line,#e5ddd0);border-radius:10px;' +
    'background:var(--card,#fefdf9);color:var(--gold,#b8863c);text-decoration:none;font-size:.85em;line-height:1.5}' +
    '#pin-footnav a:hover{border-color:var(--gold,#b8863c)}' +
    '#pin-footnav .nv-dir{display:block;font-size:.78em;color:var(--text2,#7a7262)}' +
    '@media(max-width:900px){#nav-panel{width:100vw}#nav-fab{bottom:180px;right:14px}}';
  document.head.appendChild(css);

  /* ── FAB ── */
  var fab = document.createElement('button');
  fab.id = 'nav-fab';
  fab.type = 'button';
  fab.title = '品目导航：跳转任意一品或华严经学文章';
  fab.innerHTML = '<span class="nv-ico">🧭</span><span>品目导航</span>';
  document.body.appendChild(fab);

  /* ── 抽屉 ── */
  var panel = document.createElement('div');
  panel.id = 'nav-panel';
  var pn = isPin
    ? ('<div class="nv-pn">' +
       '<button id="nv-prev"' + (idx <= 0 ? ' disabled' : '') + '>◀ 上一品</button>' +
       '<button id="nv-next"' + (idx >= PINS.length - 1 ? ' disabled' : '') + '>下一品 ▶</button></div>')
    : '';
  var body = '';
  NAV.hui.forEach(function (h) {
    var hasCur = h.items.some(function (p) { return p.id === CUR; });
    var chips = h.items.map(function (p) {
      var cur = p.id === CUR ? ' is-cur' : '';
      return '<a class="nv-chip' + cur + '" href="' + p.id + '.html">' +
        p.icon + ' ' + p.no + ' 品 · ' + strip(p.title) + '</a>';
    }).join('');
    body += '<details' + (hasCur ? ' open' : '') + '><summary>' +
      '第' + '一二三四五六七八九'[h.no - 1] + '会 · ' + h.label +
      '<span style="opacity:.6">（' + h.items.length + ' 品）</span></summary>' +
      '<div class="nv-grid">' + chips + '</div></details>';
  });
  var comps = (NAV.comp || []).map(function (c) {
    var cur = c.id === CUR ? ' is-cur' : '';
    return '<a class="nv-chip' + cur + '" href="' + c.id + '.html">' + c.icon + ' ' + c.title + '</a>';
  }).join('');
  body += '<details><summary>🧭 拼读配套专文<span style="opacity:.6">（' + NAV.comp.length +
    ' 篇）</span></summary><div class="nv-grid">' + comps + '</div></details>';
  if (NAV.ext && NAV.ext.length) {
    var exts = NAV.ext.map(function (c) {
      var cur = c.id === CUR ? ' is-cur' : '';
      return '<a class="nv-chip' + cur + '" href="' + c.id + '.html">' + c.icon + ' ' + c.title + '</a>';
    }).join('');
    body += '<details><summary>📚 经学延伸<span style="opacity:.6">（' + NAV.ext.length +
      ' 篇 · 大藏对应/讲记等）</span></summary><div class="nv-grid">' + exts + '</div></details>';
  }
  body += '<span class="nv-b">数据驱动：九会分组自各品 doc 路径解析 · 与目录页「拼读速取专区」同源。</span>';

  panel.innerHTML =
    '<div class="nv-head"><span class="nv-t">🧭 品目导航</span>' + pn +
    '<button class="nv-close" title="关闭">✕</button></div>' +
    '<div class="nv-body">' + body + '</div>' +
    '<div class="nv-foot">📚 <a href="index.html">全部文章目录</a>' +
    ' · 39 品按九会 · 每页均含全文</div>';
  document.body.appendChild(panel);

  function strip(t) {
    return (t || '').replace(/^九九华严第[一二三四五六七八九十百]+品\s*/, '').replace(/之拼读$/, '');
  }
  function cnN(n) {
    var D = '一二三四五六七八九';
    if (n <= 9) return D[n - 1];
    if (n === 10) return '十';
    if (n < 20) return '十' + D[n - 11];
    if (n === 20) return '二十';
    if (n < 30) return '二十' + D[n - 21];
    if (n === 30) return '三十';
    if (n < 40) return '三十' + D[n - 31];
    return String(n);
  }

  function close() { panel.style.display = 'none'; }
  fab.addEventListener('click', function (e) {
    e.stopPropagation();
    var open = panel.style.display === 'flex';
    panel.style.display = open ? 'none' : 'flex';
    if (!open) {
      // 当前品芯片滚动进可视区
      var cur = panel.querySelector('a.nv-chip.is-cur');
      if (cur) cur.scrollIntoView({ block: 'nearest' });
    }
  });
  panel.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
  panel.querySelector('.nv-close').addEventListener('click', close);
  document.addEventListener('pointerdown', function (e) {
    if (panel.style.display !== 'flex') return;
    var t = e.target;
    if (t.closest && (t.closest('#nav-panel') || t.closest('#nav-fab'))) return;
    close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel.style.display === 'flex') close();
  });
  if (isPin) {
    var bp = document.getElementById('nv-prev'), bn = document.getElementById('nv-next');
    if (bp && idx > 0) bp.addEventListener('click', function () { location.href = PINS[idx - 1].id + '.html'; });
    if (bn && idx < PINS.length - 1) bn.addEventListener('click', function () { location.href = PINS[idx + 1].id + '.html'; });
  }

  /* ── 品页底部：上一品/下一品条 ── */
  if (isPin) {
    var bar = document.createElement('div');
    bar.id = 'pin-footnav';
    var prev = idx > 0 ? PINS[idx - 1] : null;
    var next = idx < PINS.length - 1 ? PINS[idx + 1] : null;
    bar.innerHTML =
      (prev ? '<a href="' + prev.id + '.html"><span class="nv-dir">◀ 上一品（第' +
        cnN(prev.no) + '品）</span>' + prev.icon + ' ' + strip(prev.title) + '</a>' : '<span></span>') +
      (next ? '<a href="' + next.id + '.html" style="text-align:right"><span class="nv-dir">下一品（第' +
        cnN(next.no) + '品）▶</span>' + next.icon + ' ' + strip(next.title) + '</a>' : '<span></span>');
    var main = document.querySelector('main.content');
    if (main) main.insertAdjacentElement('afterend', bar);  // 渲染器会重写 main 子树·挂在 main 之后存活
  }
})();
