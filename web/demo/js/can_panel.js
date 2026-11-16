/* can_panel.js — L.497 入法界品·参读浮窗
 * 仅在《入法界品之拼读》主页启用（window.RUFAJIE_CAN_PAGE===true）。
 * 参读窗＝不离开主页读任一参的六层深读内容（fetch data/rufajie_can/<key>.md·_mdDocEmbed 渲染）。
 * 接入点：①主页内所有指向 huayan-rufajie-can-* 的链接（速查芯片/身份检索/★直达/参节头）点击即开窗；
 *         ②内嵌行历图详情卡（embed 模式 postMessage）；③左上 FAB。
 * 窗内：上一参/下一参、「独立页 ↗」（可离开）、ESC/点外关闭。
 * 数据：build.py 发射 data/rufajie_can/{index,01..54}.md + meta.js（window.RUFAJIE_CAN_META）。
 */
(function () {
  'use strict';
  if (window.RUFAJIE_CAN_PAGE !== true || typeof window._mdDocEmbed !== 'function') return;
  if (document.getElementById('canp-fab')) return;

  var META = null;          // [{k,no,t}]·index 在首
  var CUR = null;           // 当前 key
  var Cache = {};           // key -> md 文本

  /* ── 样式 ── */
  var css = document.createElement('style');
  css.textContent =
    '#canp-fab{position:fixed;right:18px;bottom:184px;z-index:1250;height:42px;padding:0 14px 0 12px;border-radius:21px;' +
    'display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(201,162,39,.75);background:rgba(31,28,22,.96);' +
    'color:#e8c877;font-size:14px;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,.35);font-family:inherit}' +
    '#canp-fab:hover{background:rgba(52,46,36,.97);transform:translateY(-1px)}' +
    '#canp-panel{position:fixed;right:0;top:0;bottom:0;width:min(48vw,620px);z-index:1300;display:none;' +
    'flex-direction:column;background:#fffdf8;color:#3a3226;border-left:2px solid #c9a45c;' +
    'box-shadow:-6px 0 24px rgba(0,0,0,.25)}' +
    '#canp-panel .cp-head{display:flex;align-items:center;gap:8px;padding:10px 12px;background:#2c2620;color:#e8c877;flex-wrap:wrap}' +
    '#canp-panel .cp-t{flex:1;font-size:.92em;font-weight:700;min-width:180px}' +
    '#canp-panel .cp-btns{display:flex;gap:6px;flex-wrap:wrap}' +
    '#canp-panel .cp-btns button,#canp-panel .cp-btns a{background:none;border:1px solid rgba(232,200,119,.5);color:#e8c877;' +
    'border-radius:8px;padding:4px 9px;cursor:pointer;font-size:.8em;font-family:inherit;text-decoration:none;display:inline-block}' +
    '#canp-panel .cp-btns button:hover,#canp-panel .cp-btns a:hover{background:rgba(232,200,119,.15)}' +
    '#canp-panel .cp-btns button:disabled{opacity:.4;cursor:not-allowed}' +
    '#canp-panel .cp-body{flex:1;overflow-y:auto;padding:14px 18px 24px;font-size:.92em;line-height:1.95}' +
    '#canp-panel .cp-body h1{font-size:1.25em;margin:2px 0 10px;color:var(--gold,#b8863c)}' +
    '#canp-panel .cp-body h2{font-size:1.1em;margin:18px 0 8px;border-bottom:1px solid rgba(184,134,60,.35);padding-bottom:4px}' +
    '#canp-panel .cp-body h3{font-size:1em;margin:14px 0 6px;color:#7a5a28}' +
    '#canp-panel .cp-body blockquote{margin:8px 0;padding:8px 12px;background:rgba(184,134,60,.07);border-left:3px solid rgba(184,134,60,.5);line-height:1.95}' +
    '#canp-panel .cp-body table{border-collapse:collapse;width:100%;font-size:.88em;margin:8px 0}' +
    '#canp-panel .cp-body td,#canp-panel .cp-body th{border:1px solid rgba(127,127,127,.3);padding:4px 7px;text-align:left;vertical-align:top}' +
    '#canp-panel .cp-body a{color:var(--blue,#4a8a8f)}' +
    '#canp-panel .cp-body details{margin:6px 0;border:1px solid rgba(127,127,127,.25);border-radius:8px;padding:4px 8px}' +
    '#canp-panel .cp-body summary{cursor:pointer;font-weight:600;color:#7a5a28}' +
    '#canp-panel .cp-loading{color:var(--text2,#7a7262);font-size:.85em;padding:18px 0}' +
    '@media(max-width:900px){#canp-panel{width:100vw}#canp-fab{bottom:236px;right:14px}}';
  document.head.appendChild(css);

  /* ── FAB ── */
  var fab = document.createElement('button');
  fab.id = 'canp-fab';
  fab.type = 'button';
  fab.title = '参读窗：不离开本页读任一参的六层深读内容';
  fab.innerHTML = '<span>🧭</span><span>参读窗</span>';
  document.body.appendChild(fab);

  /* ── 窗体 ── */
  var panel = document.createElement('div');
  panel.id = 'canp-panel';
  panel.innerHTML =
    '<div class="cp-head">' +
    '<span class="cp-t" id="cp-title">参读窗</span>' +
    '<span class="cp-btns">' +
    '<button id="cp-prev" title="上一参">◀ 上一参</button>' +
    '<button id="cp-next" title="下一参">下一参 ▶</button>' +
    '<a id="cp-page" class="canp-open-page" title="在独立文章页打开（可收藏/分享）">独立页 ↗</a>' +
    '<button id="cp-close" title="关闭">✕</button>' +
    '</span></div>' +
    '<div class="cp-body" id="cp-body"><div class="cp-loading">从速查网格、行历图或任一参链接打开……</div></div>';
  document.body.appendChild(panel);

  function close() { panel.style.display = 'none'; }
  fab.addEventListener('click', function (e) {
    e.stopPropagation();
    var isOpen = panel.style.display === 'flex';
    if (isOpen) { close(); return; }
    panel.style.display = 'flex';
    try {
      var last = localStorage.getItem('canp-last');
      if (last) { open(last); return; }
    } catch (e2) {}
    open('index');
  });
  panel.querySelector('#cp-close').addEventListener('click', close);
  panel.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
  document.addEventListener('pointerdown', function (e) {
    if (panel.style.display !== 'flex') return;
    var t = e.target;
    if (t.closest && (t.closest('#canp-panel') || t.closest('#canp-fab'))) return;
    close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel.style.display === 'flex') close();
  });

  /* ── meta 与取文 ── */
  function ensureMeta(done) {
    if (META) { done(META); return; }
    var s = document.createElement('script');
    s.src = '../data/rufajie_can/meta.js';
    s.onload = function () { META = window.RUFAJIE_CAN_META || []; done(META); };
    s.onerror = function () { META = []; done(META); };
    document.head.appendChild(s);
  }
  function idxOf(key) {
    for (var i = 0; i < META.length; i++) if (META[i].k === key) return i;
    return -1;
  }
  function render(md) {
    var body = panel.querySelector('#cp-body');
    var emb = window._mdDocEmbed(md);
    body.innerHTML = emb.html;
    body.scrollTop = 0;
  }
  function open(key) {
    if (!key) return;
    CUR = key;
    panel.style.display = 'flex';
    try { localStorage.setItem('canp-last', key); } catch (e) {}
    ensureMeta(function (meta) {
      var i = idxOf(key);
      var m = meta[i] || { t: key };
      panel.querySelector('#cp-title').textContent = '🧭 ' + m.t;
      panel.querySelector('#cp-page').href = ('huayan-rufajie-can-' + (key === 'index' ? 'index' : key) + '.html');
      var bp = panel.querySelector('#cp-prev'), bn = panel.querySelector('#cp-next');
      bp.disabled = !(i > 0);
      bn.disabled = !(i >= 0 && i < meta.length - 1);
      bp.onclick = function () { if (i > 0) open(meta[i - 1].k); };
      bn.onclick = function () { if (i < meta.length - 1) open(meta[i + 1].k); };
      var body = panel.querySelector('#cp-body');
      if (Cache[key]) { render(Cache[key]); return; }
      body.innerHTML = '<div class="cp-loading">载入「' + m.t + '」……</div>';
      fetch('../data/rufajie_can/' + key + '.md')
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then(function (txt) { Cache[key] = txt; if (CUR === key) render(txt); })
        .catch(function (err) {
          body.innerHTML = '<div class="cp-loading">载入失败（' + err.message + '）。' +
            '若以 file:// 打开，浏览器会阻止按需读取——请在仓库根目录运行 <code>python -m http.server</code> 后访问，' +
            '或 <a class="canp-open-page" href="huayan-rufajie-can-' + (key === 'index' ? 'index' : key) + '.html">改用独立页 ↗</a>。</div>';
        });
    });
  }

  /* ── 接入点①：主页内一切指向子页的链接 → 开窗（独立页链接除外·修饰键例外）── */
  function keyFromHref(href) {
    var m = /huayan-rufajie-can-(index|\d{2})\.html/.exec(href || '');
    return m ? m[1] : null;
  }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0) return;
    var a = e.target.closest('a');
    if (!a || a.classList.contains('canp-open-page')) return;
    var href = a.getAttribute('href') || '';
    // 窗内「主页 §参N」链接：关窗并滚回本页该参节（不离开本页）
    if (panel.style.display === 'flex' && /huayan-rufajie-pin\.html/.test(href)) {
      e.preventDefault();
      var m = /^(\d{2})$/.exec(CUR || '');
      close();
      if (m) {
        var h = [].slice.call(document.querySelectorAll('#article-full h3')).filter(function (x) {
          return x.textContent.trim().indexOf('参' + parseInt(m[1], 10) + '·') === 0;
        })[0];
        if (h) { h.scrollIntoView({ block: 'start' }); window.scrollBy(0, -70); }
      }
      return;
    }
    var key = keyFromHref(href);
    if (!key) return;
    e.preventDefault();
    open(key);
  });

  /* ── 接入点②：内嵌行历图（embed 模式）postMessage ── */
  window.addEventListener('message', function (e) {
    var d = e.data;
    if (d && d.rufajieCan) open(String(d.rufajieCan));
  });
})();
