/* reading_pos.js — 阅读位置记忆（localStorage·非 cookie·纯本地）
 * 记录：最近可见标题锚点 id + 相对偏移 + 已展开章节 id 集合
 * 恢复：展开祖先 secfold 后滚回；深链（#hash）优先；90 天过期；可清除
 * L.467：底部提示与左下角「上次阅读」均可点击，随时跳回记录位置
 */
(function () {
  'use strict';
  if (typeof ARTICLE === 'undefined' || !ARTICLE || !ARTICLE.id) return;
  var KEY = 'rp:' + ARTICLE.id;
  var MAXAGE = 90 * 24 * 3600 * 1000;
  var OFFSET = 140;
  var toastEl = null, chipEl = null, styleEl = null;
  var entryRec = null;                          // 本次打开时的历史位置（芯片据此回跳）

  function read() { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; } }
  function write(o) { try { o.ts = Date.now(); localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }
  function clear() {
    try { localStorage.removeItem(KEY); } catch (e) {}
    entryRec = null;
    if (toastEl && toastEl.parentNode) toastEl.parentNode.removeChild(toastEl);
    toastEl = null;
    hideChip();
  }

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

  function collectOpen() {
    var open = [], hs = document.querySelectorAll('#article-full .secfold');
    for (var i = 0; i < hs.length && i < 500; i++) {
      if (!hs[i].classList.contains('is-folded') && hs[i].id) open.push(hs[i].id);
    }
    return open;
  }

  function applyOpen(rec) {
    if (!rec || !rec.open || !rec.open.length) return;
    for (var i = 0; i < rec.open.length; i++) {
      var h = document.getElementById(rec.open[i]);
      if (h && h.classList && h.classList.contains('secfold')) h.classList.remove('is-folded');
    }
  }

  var timer = null;
  function saveNow() {
    var y = window.scrollY || window.pageYOffset || 0;
    var b = headingAt(y);
    var rec = { y: Math.round(y) };
    if (b) { rec.id = b.el.id; rec.delta = Math.round(y - b.top); }
    rec.open = collectOpen();
    write(rec);
    updateChip();
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

  /* ── 展开祖先折叠（优先用站点自带的 window._reveal）── */
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

  /* ── 计算目标绝对位置（折叠展开后重新量）── */
  function targetFor(rec) {
    var targetY = rec.y || 0, anchored = false, el = null;
    if (rec.id) {
      el = document.getElementById(rec.id);
      if (el) {
        revealAll(el);
        targetY = absTop(el) + (rec.delta || 0);
        anchored = true;
      }
    }
    return { y: Math.max(0, Math.round(targetY)), el: el, anchored: anchored };
  }

  function flash(el) {
    if (!el) return;
    var old = el.style.transition, oldBg = el.style.backgroundColor, oldShadow = el.style.boxShadow;
    el.style.transition = 'background-color .25s';
    el.style.backgroundColor = 'rgba(232,200,119,.42)';
    el.style.boxShadow = '0 0 0 6px rgba(232,200,119,.18)';
    setTimeout(function () {
      el.style.backgroundColor = oldBg;
      el.style.boxShadow = oldShadow;
      setTimeout(function () { el.style.transition = old; }, 400);
    }, 1300);
  }

  /* ── 跳回记录位置（toast 与左下角芯片共用）── */
  function jumpTo(rec, announce) {
    if (!rec) return false;
    applyOpen(rec);
    var t = targetFor(rec);
    window.scrollTo(0, t.y);                    // 先精确落位·不依赖平滑动画
    if (announce) flash(t.el);
    [350, 900].forEach(function (ms) {
      setTimeout(function () {
        var cur = window.scrollY || window.pageYOffset || 0;
        if (Math.abs(cur - t.y) > 500) return;   // 用户已自行滚走·不再拉回
        var t2 = targetFor(rec);
        if (Math.abs(t2.y - cur) > 16) window.scrollTo(0, t2.y);
      }, ms);
    });
    return t.anchored;
  }

  /* ── 样式 ── */
  function ensureStyle() {
    if (styleEl) return;
    styleEl = document.createElement('style');
    styleEl.id = 'rp-style';
    styleEl.textContent =
      '#rp-toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);z-index:1500;' +
      'display:flex;align-items:center;gap:10px;max-width:calc(100vw - 36px);padding:9px 14px;border-radius:10px;' +
      'background:rgba(31,36,42,.96);color:#e8c877;font-size:.82em;line-height:1.35;cursor:pointer;' +
      'box-shadow:0 6px 20px rgba(0,0,0,.35);border:1px solid rgba(184,134,60,.45)}' +
      '#rp-toast:hover{background:rgba(52,58,66,.97)}' +
      '#rp-toast .rp-ico{font-size:1.05em}' +
      '#rp-toast .rp-sub{color:#9fb4c8;font-size:.88em}' +
      '#rp-toast a{color:#8fb8de;text-decoration:underline;white-space:nowrap}' +
      '#rp-toast .rp-x{color:#9aa;text-decoration:none}' +
      '#rp-chip{position:fixed;left:18px;bottom:18px;z-index:1240;display:none;align-items:center;gap:5px;' +
      'padding:7px 12px;border-radius:18px;border:1px solid rgba(184,134,60,.6);background:rgba(31,36,42,.93);' +
      'color:#e8c877;font-size:.78em;cursor:pointer;box-shadow:0 3px 12px rgba(0,0,0,.3);font-family:inherit}' +
      '#rp-chip:hover{background:rgba(52,58,66,.97)}' +
      '@media(max-width:640px){#rp-toast{bottom:18px;gap:7px}#rp-toast .rp-sub{display:none}}';
    document.head.appendChild(styleEl);
  }

  function showToast() {
    if (toastEl || !document.body) return;
    ensureStyle();
    var d = document.createElement('div');
    d.id = 'rp-toast';
    d.setAttribute('role', 'button');
    d.tabIndex = 0;
    d.title = '点击回到上次阅读位置';
    d.innerHTML = '<span class="rp-ico">↩</span><span class="rp-txt">已回到上次阅读位置</span>' +
      '<span class="rp-sub">点击可重新定位</span>' +
      '<a class="rp-clear" href="#">清除记录</a><a class="rp-x" href="#">✕</a>';
    var doJump = function (ev) {
      if (ev && ev.target && ev.target.closest && ev.target.closest('a')) return;
      if (ev) ev.preventDefault();
      var rec = entryRec || read();
      if (!rec) { d.querySelector('.rp-txt').textContent = '暂无阅读记录'; return; }
      jumpTo(rec, true);
      d.querySelector('.rp-txt').textContent = '已回到上次阅读位置';
    };
    d.addEventListener('click', doJump);
    d.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); doJump(ev); }
    });
    d.querySelector('.rp-clear').addEventListener('click', function (ev) {
      ev.preventDefault(); ev.stopPropagation(); clear();
    });
    d.querySelector('.rp-x').addEventListener('click', function (ev) {
      ev.preventDefault(); ev.stopPropagation();
      if (d.parentNode) d.parentNode.removeChild(d);
      toastEl = null;
    });
    document.body.appendChild(d);
    toastEl = d;
    setTimeout(function () {
      if (d.parentNode) d.parentNode.removeChild(d);
      if (toastEl === d) toastEl = null;
    }, 12000);
  }

  function showChip() {
    if (chipEl || !document.body) return;
    ensureStyle();
    var b = document.createElement('button');
    b.id = 'rp-chip';
    b.type = 'button';
    b.style.display = 'inline-flex';
    b.title = '回到上次阅读位置';
    b.textContent = '↩ 上次阅读';
    b.addEventListener('click', function () {
      var rec = entryRec || read();
      if (rec) jumpTo(rec, true);
    });
    document.body.appendChild(b);
    chipEl = b;
  }
  function hideChip() {
    if (chipEl && chipEl.parentNode) chipEl.parentNode.removeChild(chipEl);
    chipEl = null;
  }
  function updateChip() {
    var y = window.scrollY || window.pageYOffset || 0;
    if (entryRec && Math.abs(y - (entryRec.y || 0)) > 800) showChip();
    else hideChip();
  }

  function restore() {
    if (location.hash) return;                  // 深链优先·不抢锚点
    var rec = read();
    if (!rec) return;
    if (Date.now() - (rec.ts || 0) > MAXAGE) { clear(); return; }
    entryRec = rec;                             // 冻结本次打开时的历史位置
    applyOpen(rec);
    setTimeout(function () {
      var t = targetFor(rec);
      window.scrollTo(0, t.y);
      // 图片/字体陆续载入引发布局位移时的二次校正
      setTimeout(function () {
        var cur = window.scrollY || window.pageYOffset || 0;
        if (Math.abs(cur - t.y) > 500) return;
        var t2 = targetFor(rec);
        if (Math.abs(t2.y - cur) > 24) window.scrollTo(0, t2.y);
      }, 700);
      if (t.anchored) showToast();
      updateChip();
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
