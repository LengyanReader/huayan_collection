/* sutra_panel.js — 三译对照悬浮阅读窗（六十/八十/四十·品目对照＋品内按卷全文）
 * L.467：按品取全文；八十↔六十↔四十 依跨译品目表取对应品，不再按品号硬套。
 * L.468：窗口可缩放（左缘拖宽）·可移动（拖标题浮窗·双击回停靠）·随点随现（点面板外即收）。
 */
(function () {
  'use strict';
  var PIN = (typeof SUTRA_PANEL_PIN === 'number') ? SUTRA_PANEL_PIN : null;
  if (!PIN || PIN < 1 || PIN > 39) return;
  if (document.getElementById('sp-fab')) return;

  /* 卷/品目录：优先读构建期生成的 mapping.js（<script> 不受 file:// fetch 限制） */
  var MAPPING = (window.SUTRA_MAPPING && typeof window.SUTRA_MAPPING === 'object') ? window.SUTRA_MAPPING : null;
  var mappingPromise = null;
  function loadMapping(force) {
    if (MAPPING && !force) return Promise.resolve(MAPPING);
    if (mappingPromise && !force) return mappingPromise;
    mappingPromise = fetch('../data/sutra/mapping.json').then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (m) { MAPPING = m; return m; });
    return mappingPromise;
  }
  loadMapping().catch(function () { /* 打开面板时再提示并允许重试 */ });

  var TRANS = { '80': '八十', '60': '六十', '40': '四十' };

  /* 八十品号 → 本译对应品：80 直取；60/40 走 mapping.x60 / x40 */
  function chapFor(pin, trans) {
    if (!MAPPING) return null;
    var x, table;
    if (trans === '80') return (MAPPING.v80 || {})[String(pin)] || null;
    x = (MAPPING['x' + trans] || {})[String(pin)];
    if (!x) return null;
    table = MAPPING['v' + trans] || {};
    return table[String(x)] || null;
  }
  function tabWhy(trans) {
    if (trans === '40') return '四十华严仅〈入法界品〉（唐·般若译），本品无四十译本';
    if (trans === '60' && PIN === 27) return '六十译阙〈十定品〉（译本差异·如实）';
    return '本译无对应品';
  }
  function volText(ch) {
    if (!ch || !ch.vols || !ch.vols.length) return '';
    return ch.vols.length > 1
      ? ('卷' + ch.vols[0] + '–' + ch.vols[ch.vols.length - 1])
      : ('卷' + ch.vols[0]);
  }

  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function isMobileWin() { return window.innerWidth <= 900; }
  function defaultW() { return Math.round(Math.min(window.innerWidth * 0.46, 700)); }

  /* ── 入口按钮 ── */
  var fabEl = null;
  function buildFab() {
    if (fabEl) return fabEl;
    var fab = document.createElement('button');
    fab.id = 'sp-fab';
    fab.type = 'button';
    fab.title = '打开三译对照阅读窗（八十／六十／四十原文）';
    fab.setAttribute('aria-label', '打开三译对照阅读窗');
    fab.innerHTML = '<span class="sp-fab-ico">📖</span><span class="sp-fab-label">原文对照</span>';
    document.body.appendChild(fab);
    fab.addEventListener('click', function () { hideHint(); toggle(); });
    fabEl = fab;
    maybeHint();
    if (window.localStorage && localStorage.getItem('sp-open') === '1') toggle();
    return fab;
  }
  function maybeHint() {
    try { if (localStorage.getItem('sp-hint') === '1') return; } catch (e) { return; }
    if (document.getElementById('sp-hint')) return;
    var h = document.createElement('div');
    h.id = 'sp-hint';
    h.innerHTML = '点这里对照 <b>六十 / 八十 / 四十</b> 原文';
    h.addEventListener('click', hideHint);
    document.body.appendChild(h);
    try { localStorage.setItem('sp-hint', '1'); } catch (e) {}
    setTimeout(hideHint, 15000);
  }
  function hideHint() {
    var h = document.getElementById('sp-hint');
    if (h && h.parentNode) h.parentNode.removeChild(h);
  }

  /* ── 状态与位置记忆 ── */
  var panel = null;
  var state = { trans: '80', vol: null, loaded: {}, segOffsets: {}, chapter: null };
  var SKEY = 'sp2:' + PIN;
  function loadPos() { try { return JSON.parse(localStorage.getItem(SKEY) || 'null'); } catch (e) { return null; } }
  function savePos() {
    try {
      var rec = loadPos() || { scroll: {} };
      rec.trans = state.trans;
      rec.vol = state.vol;
      rec.scroll = rec.scroll || {};
      var box = panel && panel.querySelector('.sp-body');
      rec.scroll[state.trans] = box ? Math.round(box.scrollTop) : 0;
      rec.ts = Date.now();
      localStorage.setItem(SKEY, JSON.stringify(rec));
    } catch (e) {}
  }

  /* ── 窗口形态：宽 / 浮窗位置（跨页共用 'sp-win'）── */
  var WINKEY = 'sp-win';
  function loadWin() { try { return JSON.parse(localStorage.getItem(WINKEY) || 'null'); } catch (e) { return null; } }
  function saveWin() {
    if (!panel) return;
    try {
      var r = panel.getBoundingClientRect();
      var rec = {
        w: Math.round(panel.offsetWidth),
        float: panel.classList.contains('is-float'),
        x: Math.round(r.left), y: Math.round(r.top),
        ts: Date.now()
      };
      localStorage.setItem(WINKEY, JSON.stringify(rec));
    } catch (e) {}
  }
  function enterFloatAt(left, top) {
    panel.classList.add('is-float');
    panel.style.right = 'auto';
    panel.style.bottom = 'auto';
    left = clamp(left, 8, Math.max(8, window.innerWidth - 220));
    top = clamp(top, 0, Math.max(0, window.innerHeight - 160));
    panel.style.left = left + 'px';
    panel.style.top = top + 'px';
    panel.style.height = (window.innerHeight - top) + 'px';
  }
  function dockPanel() {
    panel.classList.remove('is-float');
    panel.style.left = '';
    panel.style.top = '';
    panel.style.height = '';
    panel.style.right = '';
    panel.style.bottom = '';
  }
  function applyWin() {
    var rec = loadWin();
    var w = (rec && rec.w) ? clamp(rec.w, 300, Math.min(1100, window.innerWidth - 40)) : defaultW();
    panel.style.width = w + 'px';
    if (rec && rec.float && isFinite(rec.x) && isFinite(rec.y)
        && rec.x > -40 && rec.x < window.innerWidth && rec.y > -40 && rec.y < window.innerHeight) {
      enterFloatAt(rec.x, rec.y);
    } else {
      dockPanel();
    }
  }

  function ensurePanel() {
    if (panel) return panel;
    panel = document.createElement('div');
    panel.id = 'sp-panel';
    panel.innerHTML =
      '<div class="sp-resize" title="拖动调宽；双击恢复默认宽"></div>' +
      '<div class="sp-head" title="拖动标题可移动窗口；双击回到右侧停靠">' +
      '  <span class="sp-title">三译对照 · 本品经文全文</span>' +
      '  <a class="sp-cbeta" target="_blank" rel="noopener" title="在 CBETA 线上阅读">CBETA ↗</a>' +
      '  <button class="sp-close" title="关闭">✕</button>' +
      '</div>' +
      '<div class="sp-tabs">' +
      '  <button data-t="80">八十 T0279</button>' +
      '  <button data-t="60">六十 T0278</button>' +
      '  <button data-t="40">四十 T0293</button>' +
      '</div>' +
      '<div class="sp-meta"><span class="sp-chap">—</span><span class="sp-note"></span></div>' +
      '<div class="sp-bar">' +
      '  <label>卷</label><select class="sp-vol"></select>' +
      '  <span class="sp-hint">品内全文·按卷分段</span>' +
      '</div>' +
      '<div class="sp-body"><div class="sp-text">加载中…</div></div>';
    document.body.appendChild(panel);
    panel.querySelector('.sp-close').addEventListener('click', function () { toggle(); });
    panel.querySelectorAll('.sp-tabs button').forEach(function (b) {
      b.addEventListener('click', function () { switchTab(b.getAttribute('data-t')); });
    });
    panel.querySelector('.sp-vol').addEventListener('change', function (e) {
      state.vol = parseInt(e.target.value, 10);
      scrollToVol(state.vol);
      setCBeta(state.vol);
      savePos();
    });
    var st = panel.querySelector('.sp-body'), stTimer = null;
    st.addEventListener('scroll', function () {
      if (stTimer) return;
      stTimer = setTimeout(function () {
        stTimer = null;
        syncVolFromScroll();
        savePos();
      }, 500);
    }, { passive: true });

    /* ── L.468 窗口化：拖标题移动 / 拖左缘调宽 / 双击回停靠 ── */
    var head = panel.querySelector('.sp-head');
    var rz = panel.querySelector('.sp-resize');
    var drag = null;
    head.addEventListener('pointerdown', function (e) {
      if (isMobileWin() || drag) return;
      if (e.target.closest && e.target.closest('a,button')) return;   // CBETA/关闭保持原生
      var r = panel.getBoundingClientRect();
      if (!panel.classList.contains('is-float')) enterFloatAt(r.left, r.top);
      var r2 = panel.getBoundingClientRect();
      drag = { mode: 'move', id: e.pointerId, dx: e.clientX - r2.left, dy: e.clientY - r2.top };
      try { head.setPointerCapture(e.pointerId); } catch (_) {}
      e.preventDefault();
    });
    rz.addEventListener('pointerdown', function (e) {
      if (isMobileWin() || drag) return;
      drag = { mode: 'size', id: e.pointerId, right: panel.getBoundingClientRect().right };
      try { rz.setPointerCapture(e.pointerId); } catch (_) {}
      e.preventDefault();
    });
    panel.addEventListener('pointermove', function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      if (drag.mode === 'move') {
        var top = clamp(e.clientY - drag.dy, 0, Math.max(0, window.innerHeight - 160));
        var left = clamp(e.clientX - drag.dx, 8, Math.max(8, window.innerWidth - 220));
        panel.style.left = left + 'px';
        panel.style.top = top + 'px';
        panel.style.height = (window.innerHeight - top) + 'px';
      } else {
        var w = clamp(drag.right - e.clientX, 300, Math.min(1100, window.innerWidth - 40));
        panel.style.width = w + 'px';
      }
    });
    panel.addEventListener('pointerup', function (e) {
      if (drag && e.pointerId === drag.id) { drag = null; saveWin(); }
    });
    panel.addEventListener('pointercancel', function () { drag = null; });
    head.addEventListener('dblclick', function (e) {
      if (e.target.closest && e.target.closest('a,button')) return;
      dockPanel();
      saveWin();
    });
    rz.addEventListener('dblclick', function (e) {
      e.preventDefault();
      panel.style.width = defaultW() + 'px';
      saveWin();
    });

    /* ── 随点随现：点面板外（正文／空白处）即收起；面板内与入口钮除外 ── */
    document.addEventListener('pointerdown', function (e) {
      if (!(panel && panel.style.display === 'flex')) return;
      if (drag) return;
      var t = e.target;
      if (t.closest && (t.closest('#sp-panel') || t.closest('#sp-fab') || t.closest('#sp-hint'))) return;
      toggle();
    });

    applyWin();
    return panel;
  }

  function renderTabs() {
    panel.querySelectorAll('.sp-tabs button').forEach(function (b) {
      var t = b.getAttribute('data-t');
      var ch = chapFor(PIN, t);
      b.disabled = !ch;
      b.className = (t === state.trans) ? 'sp-on' : '';
      b.title = ch ? ('对应：' + ch.title + '（' + volText(ch) + '）') : tabWhy(t);
    });
  }

  function renderMeta(ch) {
    var chapEl = panel.querySelector('.sp-chap');
    var noteEl = panel.querySelector('.sp-note');
    if (ch) {
      chapEl.textContent = TRANS[state.trans] + '〈' + ch.title + '〉 · ' + volText(ch);
    } else {
      chapEl.textContent = TRANS[state.trans] + ' · 无对应品';
    }
    var notes = (MAPPING && MAPPING.notes) ? MAPPING.notes[String(PIN)] : null;
    noteEl.textContent = (notes && notes[state.trans]) || '';
  }

  function switchTab(trans) {
    if (!chapFor(PIN, trans)) return;
    savePos();
    state.trans = trans;
    state.vol = null;
    renderTabs();
    loadChapter();
  }

  function showMapError() {
    var box = panel.querySelector('.sp-text');
    box.textContent = '';
    var p = document.createElement('p');
    p.textContent = (location.protocol === 'file:')
      ? '当前是直接打开本地 HTML 文件（file://），品目索引未能加载。请通过站点地址（http/https）访问本站。'
      : '品目索引加载失败：请检查 data/sutra/mapping.json 是否存在，或稍后重试。';
    box.appendChild(p);
    var a = document.createElement('a');
    a.href = '#';
    a.textContent = '重试';
    a.style.cssText = 'color:#7a5a28;text-decoration:underline';
    a.addEventListener('click', function (ev) {
      ev.preventDefault();
      box.textContent = '正在重试…';
      loadMapping(true).then(function () { renderTabs(); loadChapter(); }).catch(showMapError);
    });
    box.appendChild(a);
  }

  function loadChapter() {
    var box = panel.querySelector('.sp-text');
    if (!MAPPING) {
      box.textContent = '正在加载品目…';
      loadMapping().then(function () {
        if (panel && panel.style.display === 'flex') { renderTabs(); loadChapter(); }
      }).catch(showMapError);
      return;
    }
    var ch = chapFor(PIN, state.trans);
    renderMeta(ch);
    if (!ch) {
      box.textContent = tabWhy(state.trans);
      setCBeta(1);
      return;
    }
    var key = state.trans + ':' + ch.file;
    if (state.loaded[key]) { renderChapter(state.loaded[key]); return; }
    box.textContent = '加载中…';
    fetch('../data/sutra/' + ch.file)
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (d) {
        state.loaded[key] = d;
        renderChapter(d);
      })
      .catch(function () { showVolError(); });
  }

  function showVolError() {
    var box = panel.querySelector('.sp-text');
    box.textContent = '';
    var p = document.createElement('p');
    p.textContent = (location.protocol === 'file:')
      ? '当前是直接打开本地 HTML 文件（file://），浏览器禁止读取品文数据。请通过站点地址（http/https）访问，例如在本目录运行 python -m http.server 后打开 http://127.0.0.1:8000/。'
      : '品文加载失败：请检查 data/sutra 品文文件是否存在，或稍后重试。';
    box.appendChild(p);
    var a = document.createElement('a');
    a.href = '#';
    a.textContent = '重试';
    a.style.cssText = 'color:#7a5a28;text-decoration:underline';
    a.addEventListener('click', function (ev) {
      ev.preventDefault();
      state.loaded = {};
      loadChapter();
    });
    box.appendChild(a);
  }

  function renderChapter(d) {
    var box = panel.querySelector('.sp-text');
    state.chapter = d;
    box.innerHTML = '';
    d.segs.forEach(function (seg) {
      var h = document.createElement('div');
      h.className = 'sp-volh';
      h.id = 'sp-vol-' + seg.v;
      h.textContent = '卷第' + seg.v;
      box.appendChild(h);
      seg.paras.forEach(function (t) {
        var el = document.createElement('p');
        el.textContent = t;
        box.appendChild(el);
      });
    });
    var sel = panel.querySelector('.sp-vol');
    sel.innerHTML = '';
    d.segs.forEach(function (seg) {
      var o = document.createElement('option');
      o.value = seg.v;
      o.textContent = '卷 ' + seg.v;
      sel.appendChild(o);
    });
    state.segOffsets = {};
    state.vol = null;
    setTimeout(function () {
      var body = panel.querySelector('.sp-body');
      var base = body.getBoundingClientRect().top - body.scrollTop;
      d.segs.forEach(function (seg) {
        var h = document.getElementById('sp-vol-' + seg.v);
        if (h) state.segOffsets[seg.v] = Math.round(h.getBoundingClientRect().top - base);
      });
      var rec = loadPos();
      var want = (rec && rec.scroll && rec.scroll[state.trans] != null) ? rec.scroll[state.trans] : 0;
      body.scrollTop = want;
      syncVolFromScroll();
      setTimeout(function () {
        if (Math.abs(body.scrollTop - want) > 24 && want > 0) body.scrollTop = want;
      }, 300);
    }, 30);
  }

  function scrollToVol(v) {
    var body = panel.querySelector('.sp-body');
    var top = state.segOffsets[v];
    if (typeof top === 'number') body.scrollTop = top;
  }

  function syncVolFromScroll() {
    if (!state.chapter) return;
    var body = panel.querySelector('.sp-body');
    var y = body.scrollTop + 24, cur = state.chapter.segs[0].v;
    state.chapter.segs.forEach(function (seg) {
      if (state.segOffsets[seg.v] != null && state.segOffsets[seg.v] <= y) cur = seg.v;
    });
    state.vol = cur;
    var sel = panel.querySelector('.sp-vol');
    if (sel && String(sel.value) !== String(cur)) sel.value = cur;
    setCBeta(cur);
  }

  function cbetaUrl(trans, vol) {
    var nn = ('00' + vol).slice(-3);
    var tid = { '80': 'T10n0279', '60': 'T09n0278', '40': 'T0293' }[trans];
    return 'https://cbetaonline.dila.edu.tw/zh/' + tid + '_' + nn;
  }

  function setCBeta(vol) {
    var a = panel.querySelector('.sp-cbeta');
    var v = vol || (state.vol || 1);
    a.href = cbetaUrl(state.trans, v);
  }

  function toggle() {
    if (panel && panel.style.display === 'flex') {
      savePos();
      saveWin();
      panel.style.display = 'none';
      if (window.localStorage) localStorage.setItem('sp-open', '0');
      return;
    }
    ensurePanel();
    var rec = loadPos();
    if (rec && rec.trans && chapFor(PIN, rec.trans)) state.trans = rec.trans;
    panel.style.display = 'flex';
    if (window.localStorage) localStorage.setItem('sp-open', '1');
    renderTabs();
    loadChapter();
  }

  // ESC 关闭
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel && panel.style.display === 'flex') toggle();
  });

  // 样式注入
  var css = document.createElement('style');
  css.textContent =
    '#sp-fab{position:fixed;right:18px;bottom:84px;z-index:1250;height:42px;padding:0 14px 0 12px;border-radius:21px;' +
    'display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(184,134,60,.75);background:rgba(31,36,42,.96);' +
    'color:#e8c877;font-size:14px;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,.35);font-family:inherit}' +
    '#sp-fab:hover{background:rgba(52,58,66,.97);transform:translateY(-1px)}' +
    '#sp-fab .sp-fab-ico{font-size:18px;line-height:1}' +
    '#sp-fab .sp-fab-label{font-size:13px;letter-spacing:.02em}' +
    '#sp-hint{position:fixed;right:18px;bottom:134px;z-index:1251;max-width:240px;padding:9px 12px;border-radius:9px;' +
    'background:#fbf3df;color:#5c4a28;border:1px solid #d9c18a;font-size:12px;line-height:1.5;' +
    'box-shadow:0 4px 14px rgba(0,0,0,.2);cursor:pointer}' +
    '#sp-hint b{color:#8a5a18}' +
    '@media(max-width:640px){#sp-fab{bottom:76px;right:14px}#sp-hint{right:14px;bottom:126px}}' +
    '#sp-panel{position:fixed;right:0;top:0;bottom:0;width:min(46vw,700px);z-index:1300;display:none;' +
    'flex-direction:column;background:#faf6ee;color:#2f2a22;border-left:2px solid #b8863c;' +
    'box-shadow:-6px 0 24px rgba(0,0,0,.25)}' +
    '#sp-panel.is-float{box-shadow:0 10px 38px rgba(0,0,0,.4);border:1px solid #b8863c}' +
    '.sp-resize{position:absolute;left:0;top:0;bottom:0;width:9px;cursor:col-resize;z-index:3;touch-action:none}' +
    '.sp-resize:hover{background:rgba(184,134,60,.3)}' +
    '#sp-panel .sp-head{display:flex;align-items:center;gap:10px;padding:10px 14px;background:#2c2620;color:#e8c877;' +
    'cursor:move;user-select:none;-webkit-user-select:none;touch-action:none}' +
    '#sp-panel .sp-head a,#sp-panel .sp-head button{cursor:pointer}' +
    '#sp-panel .sp-head .sp-title{flex:1;font-size:.95em}' +
    '#sp-panel .sp-head .sp-cbeta{color:#8fb8de;font-size:.8em;text-decoration:none}' +
    '#sp-panel .sp-head .sp-close{background:none;border:none;color:#e8c877;font-size:16px;cursor:pointer}' +
    '#sp-panel .sp-tabs{display:flex;gap:6px;padding:8px 12px 0;background:#efe8da}' +
    '#sp-panel .sp-tabs button{padding:6px 14px;border:1px solid #c9b48a;background:#f6efe1;cursor:pointer;font-size:.85em;border-radius:6px 6px 0 0}' +
    '#sp-panel .sp-tabs button.sp-on{background:#fbf8f2;font-weight:bold;color:#7a5a28}' +
    '#sp-panel .sp-tabs button:disabled{opacity:.45;cursor:not-allowed}' +
    '#sp-panel .sp-meta{display:flex;gap:10px;flex-wrap:wrap;padding:6px 14px;background:#f3ecdd;' +
    'border-top:1px solid #e3d9c6;font-size:.76em;color:#6b5a3a;line-height:1.5}' +
    '#sp-panel .sp-meta .sp-chap{font-weight:bold;color:#7a5a28}' +
    '#sp-panel .sp-meta .sp-note{color:#a0522d}' +
    '#sp-panel .sp-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;background:#fbf8f2;border-top:1px solid #e3d9c6}' +
    '#sp-panel .sp-bar select{flex:0 0 auto}' +
    '#sp-panel .sp-bar .sp-hint{font-size:.72em;color:#8a7a5a}' +
    '#sp-panel .sp-body{flex:1;overflow-y:auto;background:#fbf8f2}' +
    '#sp-panel .sp-text{padding:12px 18px;line-height:2.05;font-size:.95em;font-family:serif;white-space:pre-wrap;text-align:justify}' +
    '#sp-panel .sp-text .sp-volh{margin:18px 0 6px;padding:4px 0 4px 10px;border-left:3px solid #b8863c;' +
    'font-family:inherit;font-size:.9em;font-weight:bold;color:#7a5a28;background:#f3ecdd;position:sticky;top:0;z-index:1}' +
    '@media(max-width:900px){#sp-panel{width:100vw}.sp-resize{display:none}#sp-panel .sp-head{cursor:default}}';
  document.head.appendChild(css);

  // 置末启动：确保 state/函数均已初始化（sp-open=1 时会立即 toggle）
  buildFab();
})();
