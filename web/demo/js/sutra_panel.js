/* sutra_panel.js — 三译对照悬浮阅读窗（八十/六十/四十·卷文本仓内自足＋CBETA 外链） */
(function () {
  'use strict';
  var PIN = (typeof SUTRA_PANEL_PIN === 'number') ? SUTRA_PANEL_PIN : null;
  if (!PIN || PIN < 1 || PIN > 39) return;
  if (document.getElementById('sp-fab')) return;

  var MAPPING = null;
  fetch('../data/sutra/mapping.json').then(function (r) { return r.json(); }).then(function (m) {
    MAPPING = m; buildFab();
  }).catch(function () { /* mapping 缺失则不显示入口 */ });

  function volsFor(pin, trans) {
    if (!MAPPING) return null;
    var key = 'v' + trans;
    var table = MAPPING[key] || {};
    return table[String(pin)] || null;
  }

  function buildFab() {
    var fab = document.createElement('button');
    fab.id = 'sp-fab';
    fab.title = '三译对照阅读窗（八十／六十／四十）';
    fab.innerHTML = '📖';
    document.body.appendChild(fab);
    fab.addEventListener('click', function () { toggle(); });
    if (window.localStorage && localStorage.getItem('sp-open') === '1') toggle();
  }

  var panel = null, state = { trans: '80', vol: null, loaded: {} };
  var SKEY = 'sp:' + PIN;
  function loadPos() { try { return JSON.parse(localStorage.getItem(SKEY) || 'null'); } catch (e) { return null; } }
  function savePos() {
    try {
      var rec = loadPos() || { scroll: {} };
      rec.trans = state.trans; rec.vol = state.vol;
      rec.scroll = rec.scroll || {};
      if (state.vol != null) {
        var box = panel && panel.querySelector('.sp-body');
        rec.scroll[state.trans + '/' + state.vol] = box ? Math.round(box.scrollTop) : 0;
      }
      rec.ts = Date.now();
      localStorage.setItem(SKEY, JSON.stringify(rec));
    } catch (e) {}
  }

  function ensurePanel() {
    if (panel) return panel;
    panel = document.createElement('div');
    panel.id = 'sp-panel';
    panel.innerHTML =
      '<div class="sp-head">' +
      '  <span class="sp-title">三译对照 · 本品经文全文</span>' +
      '  <a class="sp-cbeta" target="_blank" rel="noopener" title="在 CBETA 线上阅读">CBETA ↗</a>' +
      '  <button class="sp-close" title="关闭">✕</button>' +
      '</div>' +
      '<div class="sp-tabs">' +
      '  <button data-t="80">八十 T0279</button>' +
      '  <button data-t="60">六十 T0278</button>' +
      '  <button data-t="40">四十 T0293</button>' +
      '</div>' +
      '<div class="sp-bar">' +
      '  <label>卷</label><select class="sp-vol"></select>' +
      '  <span class="sp-hint">卷内全文·滚动阅读</span>' +
      '</div>' +
      '<div class="sp-body"><div class="sp-text">加载中…</div></div>';
    document.body.appendChild(panel);
    panel.querySelector('.sp-close').addEventListener('click', function () { toggle(); });
    panel.querySelectorAll('.sp-tabs button').forEach(function (b) {
      b.addEventListener('click', function () { switchTab(b.getAttribute('data-t')); });
    });
    panel.querySelector('.sp-vol').addEventListener('change', function (e) {
      savePos();
      state.vol = parseInt(e.target.value, 10);
      loadVol();
    });
    var st = panel.querySelector('.sp-body'), stTimer = null;
    if (st) st.addEventListener('scroll', function () {
      if (stTimer) return;
      stTimer = setTimeout(function () { stTimer = null; savePos(); }, 500);
    }, { passive: true });
    return panel;
  }

  function switchTab(trans) {
    savePos();
    state.trans = trans;
    renderTabs();
    fillVols();
  }

  function renderTabs() {
    panel.querySelectorAll('.sp-tabs button').forEach(function (b) {
      var t = b.getAttribute('data-t');
      var has = volsFor(PIN, t);
      b.disabled = !has;
      b.className = (t === state.trans) ? 'sp-on' : '';
    });
  }

  function fillVols() {
    var sel = panel.querySelector('.sp-vol');
    var vols = volsFor(PIN, state.trans) || [];
    sel.innerHTML = '';
    if (!vols.length) {
      sel.innerHTML = '<option>—（本译无本品独立卷）</option>';
      panel.querySelector('.sp-text').textContent = '此译本无本品独立卷（藏汉章界差异·如实）。';
      setCBeta();
      return;
    }
    vols.forEach(function (v) {
      var o = document.createElement('option');
      o.value = v; o.textContent = '卷 ' + v;
      sel.appendChild(o);
    });
    if (vols.indexOf(state.vol) >= 0) {
      sel.value = state.vol;
    } else {
      state.vol = vols[0];
      sel.value = state.vol;
    }
    setCBeta();
    loadVol();
  }

  function cbetaUrl(trans, vol) {
    var nn = ('00' + vol).slice(-3);
    var tid = { '80': 'T10n0279', '60': 'T09n0278', '40': 'T0293' }[trans];
    return 'https://cbetaonline.dila.edu.tw/zh/' + tid + '_' + nn;
  }

  function setCBeta() {
    var a = panel.querySelector('.sp-cbeta');
    a.href = cbetaUrl(state.trans, state.vol || 1);
  }

  function loadVol() {
    var box = panel.querySelector('.sp-text');
    var key = state.trans + '/' + state.vol;
    if (state.loaded[key]) { renderParas(state.loaded[key]); return; }
    box.textContent = '加载中…';
    fetch('../data/sutra/v' + state.trans + '/j' + ('00' + state.vol).slice(-3) + '.json')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        state.loaded[key] = d.paras;
        renderParas(d.paras);
        var rec = loadPos();
        var top = rec && rec.scroll ? rec.scroll[key] : 0;
        if (top) setTimeout(function () { var sb = panel.querySelector('.sp-body'); if (sb) sb.scrollTop = top; }, 60);
      })
      .catch(function () { box.textContent = '加载失败（data/sutra 卷文件缺失）'; });
  }

  function renderParas(paras) {
    var box = panel.querySelector('.sp-text');
    box.innerHTML = '';
    paras.forEach(function (p) {
      var el = document.createElement('p');
      el.textContent = p;
      box.appendChild(el);
    });
    box.scrollTop = 0;
  }

  function toggle() {
    if (panel && panel.style.display === 'flex') {
      savePos();
      panel.style.display = 'none';
      if (window.localStorage) localStorage.setItem('sp-open', '0');
      return;
    }
    ensurePanel();
    var rec = loadPos();
    if (rec) { if (rec.trans) state.trans = rec.trans; if (rec.vol) state.vol = rec.vol; }
    panel.style.display = 'flex';
    if (window.localStorage) localStorage.setItem('sp-open', '1');
    renderTabs();
    fillVols();
  }

  // ESC 关闭
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel && panel.style.display === 'flex') toggle();
  });

  // 样式注入
  var css = document.createElement('style');
  css.textContent =
    '#sp-fab{position:fixed;right:18px;bottom:64px;z-index:1200;width:52px;height:52px;border-radius:50%;' +
    'border:1px solid rgba(184,134,60,.7);background:rgba(31,36,42,.95);color:#e8c877;font-size:24px;cursor:pointer;' +
    'box-shadow:0 4px 16px rgba(0,0,0,.35)}' +
    '#sp-fab:hover{background:rgba(52,58,66,.96)}' +
    '#sp-panel{position:fixed;right:0;top:0;bottom:0;width:min(46vw,700px);z-index:1199;display:none;' +
    'flex-direction:column;background:#faf6ee;color:#2f2a22;border-left:2px solid #b8863c;' +
    'box-shadow:-6px 0 24px rgba(0,0,0,.25)}' +
    '#sp-panel .sp-head{display:flex;align-items:center;gap:10px;padding:10px 14px;background:#2c2620;color:#e8c877}' +
    '#sp-panel .sp-head .sp-title{flex:1;font-size:.95em}' +
    '#sp-panel .sp-head .sp-cbeta{color:#8fb8de;font-size:.8em;text-decoration:none}' +
    '#sp-panel .sp-head .sp-close{background:none;border:none;color:#e8c877;font-size:16px;cursor:pointer}' +
    '#sp-panel .sp-tabs{display:flex;gap:6px;padding:8px 12px 0;background:#efe8da}' +
    '#sp-panel .sp-tabs button{padding:6px 14px;border:1px solid #c9b48a;background:#f6efe1;cursor:pointer;font-size:.85em;border-radius:6px 6px 0 0}' +
    '#sp-panel .sp-tabs button.sp-on{background:#fbf8f2;font-weight:bold;color:#7a5a28}' +
    '#sp-panel .sp-tabs button:disabled{opacity:.45;cursor:not-allowed}' +
    '#sp-panel .sp-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;background:#fbf8f2;border-top:1px solid #e3d9c6}' +
    '#sp-panel .sp-bar select{flex:0 0 auto}' +
    '#sp-panel .sp-bar .sp-hint{font-size:.72em;color:#8a7a5a}' +
    '#sp-panel .sp-body{flex:1;overflow-y:auto;background:#fbf8f2}' +
    '#sp-panel .sp-text{padding:12px 18px;line-height:2.05;font-size:.95em;font-family:serif;white-space:pre-wrap;text-align:justify}' +
    '@media(max-width:900px){#sp-panel{width:100vw}}';
  document.head.appendChild(css);
})();
