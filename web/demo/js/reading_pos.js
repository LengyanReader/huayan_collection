/* reading_pos.js — 阅读位置记忆（localStorage·非 cookie·纯本地）
 * 记录：最近可见标题锚点 id + 相对偏移（折叠感知）
 * 恢复：展开祖先 secfold 后滚回；深链（#hash）优先；90 天过期；可清除
 */
(function () {
  'use strict';
  if (typeof ARTICLE === 'undefined' || !ARTICLE || !ARTICLE.id) return;
  var KEY = 'rp:' + ARTICLE.id;
  var MAXAGE = 90 * 24 * 3600 * 1000;
  var OFFSET = 140;

  function read() { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; } }
  function write(o) { try { o.ts = Date.now(); localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }
  function clear() { try { localStorage.removeItem(KEY); } catch (e) {} }

  function root() { return document.getElementById('article-full') || document.getElementById('article-root'); }

  function absTop(el) { return el.getBoundingClientRect().top + window.scrollY; }

  function headingAt(y) {
    var R = root();
    if (!R) return null;
    var hs = R.querySelectorAll('h2[id],h3[id],h4[id],h5[id]');
    var best = null;
    for (var i = 0; i < hs.length; i++) {
      var h = hs[i];
      if (!h.offsetParent) continue;           // 折叠体中的标题不可见·跳过
      var top = absTop(h);
      if (top - OFFSET <= y) best = { el: h, top: top };
      else break;
    }
    return best;
  }

  var timer = null;
  function saveNow() {
    var y = window.scrollY || window.pageYOffset || 0;
    var b = headingAt(y);
    var rec = { y: Math.round(y) };
    if (b) { rec.id = b.el.id; rec.delta = Math.round(y - b.top); }
    var open = [], hs = document.querySelectorAll('#article-full .secfold');
    for (var i = 0; i < hs.length && i < 500; i++) {
      if (!hs[i].classList.contains('is-folded') && hs[i].id) open.push(hs[i].id);
    }
    rec.open = open;
    write(rec);
  }
  function onScroll() {
    if (timer) return;
    timer = setTimeout(function () { timer = null; saveNow(); }, 600);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('pagehide', saveNow);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') saveNow();
  });

  function toast(msg) {
    var d = document.createElement('div');
    d.style.cssText = 'position:fixed;left:50%;bottom:26px;transform:translateX(-50%);background:rgba(31,36,42,.95);' +
      'color:#e8c877;padding:9px 14px;border-radius:8px;font-size:.8em;z-index:1300;' +
      'box-shadow:0 4px 16px rgba(0,0,0,.32);display:flex;gap:12px;align-items:center';
    var s = document.createElement('span'); s.textContent = msg; d.appendChild(s);
    var a = document.createElement('a'); a.href = '#'; a.textContent = '清除记录';
    a.style.cssText = 'color:#8fb8de;text-decoration:underline';
    a.addEventListener('click', function (ev) { ev.preventDefault(); clear(); d.remove(); });
    d.appendChild(a);
    var x = document.createElement('a'); x.href = '#'; x.textContent = '✕';
    x.style.cssText = 'color:#9aa;text-decoration:none';
    x.addEventListener('click', function (ev) { ev.preventDefault(); d.remove(); });
    d.appendChild(x);
    document.body.appendChild(d);
    setTimeout(function () { if (d.parentNode) d.remove(); }, 9000);
  }

  function revealAll(el) {
    if (typeof window._reveal === 'function') {
      try { window._reveal(el); return; } catch (e) {}
    }
    var p = el;
    while (p) {
      var body = p.closest ? p.closest('.secfold-body') : null;
      if (!body) break;
      var owner = body.previousElementSibling;
      if (owner && owner.classList && owner.classList.contains('secfold')) owner.classList.remove('is-folded');
      p = body.parentElement;
    }
    var q = el;
    while (q && q !== document.body) { if (q.tagName === 'DETAILS') q.setAttribute('open', 'open'); q = q.parentElement; }
  }

  function restore() {
    if (location.hash) return;                  // 深链优先·不抢锚点
    var rec = read();
    if (!rec) return;
    if (Date.now() - (rec.ts || 0) > MAXAGE) { clear(); return; }
    if (rec.open && rec.open.length) {
      for (var i = 0; i < rec.open.length; i++) {
        var h = document.getElementById(rec.open[i]);
        if (h && h.classList.contains('secfold')) h.classList.remove('is-folded');
      }
    }
    var targetY = rec.y || 0;
    var anchored = false;
    if (rec.id) {
      var el = document.getElementById(rec.id);
      if (el) { revealAll(el); targetY = absTop(el) + (rec.delta || 0); anchored = true; }
    }
    setTimeout(function () {
      window.scrollTo(0, Math.max(0, targetY));
      if (anchored) toast('已回到上次阅读位置');
    }, 120);
  }

  var tries = 0;
  (function poll() {
    var R = root();
    if (R && (R.querySelector('h2') || R.querySelector('h3'))) { restore(); return; }
    if (++tries > 80) return;                   // ≈8s 上限
    setTimeout(poll, 100);
  })();
})();
