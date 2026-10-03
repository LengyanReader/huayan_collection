/* ═══════════════════════════════════════════════════════════════════════
 * renderMiaoyanKeypoints —— 世主妙严品·要点导览播放器（overview）
 *
 * 目的：在读者进入逐组分述之前，先以「位之四层」为骨架，把本品八处要点
 *       循序播放一遍，求其「整体观」与「要点之感知」，每点附经文原句、
 *       信度分级与「详见」指针，便于读后回查分述。
 *
 * 数据源（唯一真源，前端零硬编码内容）：
 *   data/narrative/miaoyan_keypoints.yaml → build.py → var MIAOYAN_KP
 *
 * 不损原则（重要信息与内容绝不丢失）：
 *   ① 播放器逐点呈现，但另附「八要点全文」静态清单，逐条透出每一要点之
 *      全部字段（标题中英·所属层·要旨中英·经文原句·出处·信度徽标·本文
 *      判断·抽象小图·方位），故纵不按播放，信息亦无遗漏。
 *   ② 环与四层为示意骨架，半径之比取「由内而外、摄化愈广」之意，非经文
 *      所定距离，亦非比例尺——disclaimer 与 closer 中英皆原样透出。
 *   ③ 八要点皆置于所属层之环上；为求清晰无叠，画布上角度按序号均分，
 *      而作者所留 `point_at` 方位值仍逐条列于文（不隐没其数据）。
 *   ④ 凡经文明文标 T0，据注疏或实测互证标 T1，属本文判断标 T2 并附
 *      judgment_zh——三层绝不混同，图例亦中英并陈。
 *   ⑤ 图形为抽象线画，只作辨识之用（meta.icon_note_zh），非图像史形象。
 * ═══════════════════════════════════════════════════════════════════════ */
var MiaoyanKeypoints = (function () {
  'use strict';

  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function easeOut(p) { return 1 - Math.pow(1 - p, 3); }

  var TONE = { gold: '#b8863c', jade: '#4a7c6f', lapis: '#3f5e8c', ash: '#7a6a58' };
  function toneColor(t) { return TONE[t] || TONE.ash; }

  function esc(t) {
    return String(t == null ? '' : t)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function render(containerId) {
    var d = (typeof MIAOYAN_KP !== 'undefined') ? MIAOYAN_KP : null;
    if (!d || !d.keypoints || !d.keypoints.length) return false;
    var el = document.querySelector(containerId);
    if (!el) return false;

    /* ── 数据整理 ── */
    var kps = d.keypoints.slice().sort(function (a, b) { return (a.idx || 0) - (b.idx || 0); });
    var frame = d.frame || {};
    var meta = d.meta || {};
    var layers = (frame.layers || []).slice().sort(function (a, b) { return (a.order || 0) - (b.order || 0); });
    var layerById = {}, maxR = 0;
    for (var li = 0; li < layers.length; li++) {
      layerById[layers[li].id] = layers[li];
      maxR = Math.max(maxR, layers[li].radius || 0);
    }
    var evLevels = d.evidence_levels || {};
    var n = kps.length;
    var total = kps.reduce(function (a, k) { return a + (k.duration_s || 0); }, 0) || 1;

    var W = 960, H = 600, CX = W / 2, CY = H / 2;
    var SCALE = (Math.min(W, H) / 2 - 78) / (maxR || 1);
    function slotAngle(i) { return -Math.PI / 2 + (i * 2 * Math.PI) / n; }
    function slotPos(i) {
      var lay = layerById[kps[i].layer] || { radius: maxR };
      var r = (lay.radius || 0) * SCALE, a = slotAngle(i);
      return { x: CX + Math.cos(a) * r, y: CY + Math.sin(a) * r, ang: a };
    }

    /* ── 单点全字段渲染（播放面板与静态清单共用，确保无遗漏）── */
    function iconSvg(dstr) {
      if (!dstr) return '';
      return '<svg class="mk-icon" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">'
        + '<path d="' + esc(dstr) + '" fill="none" stroke="currentColor" stroke-width="1.6" '
        + 'stroke-linecap="round" stroke-linejoin="round"/></svg>';
    }
    function kpDetailHTML(kp, i) {
      var lay = layerById[kp.layer] || {};
      var lv = evLevels[kp.evidence] || {};
      var s = '<div class="mk-dHead">' + iconSvg(kp.icon)
        + '<span class="mk-dNo">要点 ' + esc(kp.idx || (i + 1)) + '</span>'
        + '<span class="mk-badge mk-ev-' + esc(kp.evidence || 'na') + '">' + esc(lv.label_zh || kp.evidence || '') + '</span>'
        + '<span class="mk-dTitle">' + esc(kp.title_zh || '') + '</span></div>';
      if (kp.title_en) s += '<div class="en-line mk-dTitleEn">' + esc(kp.title_en) + '</div>';
      s += '<div class="mk-dReg">🅢 所属层：' + esc(lay.label_zh || kp.layer || '')
        + (lay.label_en ? ' <span class="en-line">· ' + esc(lay.label_en) + '</span>' : '')
        + '　🎯 方位 point_at：[' + (kp.point_at ? esc(kp.point_at.join(', ')) : '—') + ']'
        + '　⏱ ' + esc(kp.duration_s || '') + 's</div>';
      if (kp.gist_zh) s += '<div class="mk-gist">' + esc(kp.gist_zh) + '</div>';
      if (kp.gist_en) s += '<div class="en-line mk-gist-en">' + esc(kp.gist_en) + '</div>';
      if (kp.quote_zh) s += '<blockquote class="mk-quote"><div class="mk-qt">「' + esc(kp.quote_zh) + '」</div>'
        + '<div class="mk-ref">📎 ' + esc(kp.ref || '') + '　〔详见分述〕</div></blockquote>';
      if (kp.judgment && kp.judgment_zh) s += '<div class="mk-judge"><b>〔本文判断〕</b> ' + esc(kp.judgment_zh) + '</div>';
      return s;
    }

    /* ── DOM ── */
    var h = '';
    h += '<section class="miaoyan-kp" data-chrome="1">';
    h += '<h2>🧭 ' + esc(meta.title_zh || '世主妙严品 · 要点导览')
      + '<span class="en-line" style="font-size:0.62em;color:var(--text2);margin-left:8px">🧭 '
      + esc(meta.title_en || 'Guided Tour of the Key Points') + '</span></h2>';
    h += '<div class="mk-meta">版本 ' + esc(meta.version || '—') + ' · 状态 ' + esc(meta.status || '—')
      + (meta.source_text_verified ? ' · 经文已回源核验（source_text_verified）' : '') + '</div>';
    if (meta.note_zh) h += '<div class="bi-note">' + esc(meta.note_zh) + '</div>';
    if (meta.note_en) h += '<div class="en-line" style="font-size:0.8em;color:var(--text2);margin:4px 0 8px">' + esc(meta.note_en) + '</div>';

    /* 骨架说明（含周匝之环概念）*/
    h += '<div class="mk-frame">' + esc(frame.title_zh || '')
      + (frame.title_en ? ' <span class="en-line">· ' + esc(frame.title_en) + '</span>' : '')
      + (frame.sweep_zh ? '　◯ ' + esc(frame.sweep_zh) + (frame.sweep_en ? '（' + esc(frame.sweep_en) + '）' : '') : '')
      + '</div>';

    /* 控制条 */
    h += '<div class="mk-ctrl">';
    h += '<button class="f-nav-btn mk-play" type="button">▶ 播放要点</button>';
    h += '<button class="f-nav-btn mk-prev" type="button" title="上一要点">⏮ 上一</button>';
    h += '<button class="f-nav-btn mk-next" type="button" title="下一要点">⏭ 下一</button>';
    h += '<label class="mk-rate">速度 <select class="mk-speed">'
      + '<option value="0.75">0.75×</option><option value="1" selected>1×</option>'
      + '<option value="1.5">1.5×</option><option value="2">2×</option></select></label>';
    h += '<span class="mk-time"><span class="mk-cur">0.0</span> / ' + total.toFixed(0) + ' s</span>';
    h += '</div>';
    h += '<input class="mk-seek" type="range" min="0" max="1000" value="0" step="1" aria-label="播放进度">';

    /* 图层开关 */
    h += '<div class="mk-layers">';
    h += '<label><input type="checkbox" class="mk-lg" data-k="labels" checked> 层名</label>';
    h += '<label><input type="checkbox" class="mk-lg" data-k="en" checked> 英文标签</label>';
    h += '<label><input type="checkbox" class="mk-lg" data-k="links" checked> 佛座引线</label>';
    h += '<label><input type="checkbox" class="mk-lg" data-k="all" checked> 预显全部要点</label>';
    h += '</div>';

    h += '<canvas class="mk-cv" width="' + W + '" height="' + H + '" role="img" '
      + 'aria-label="世主妙严品要点导览：位之四层环上周匝八要点"></canvas>';

    /* 要点条 chips */
    h += '<div class="mk-chips">';
    for (var ci = 0; ci < n; ci++) {
      h += '<button class="mk-chip' + (ci === 0 ? ' on' : '') + '" data-i="' + ci + '" type="button" '
        + 'title="' + esc(kps[ci].title_zh) + '"><b>' + esc(kps[ci].idx || (ci + 1)) + '</b> '
        + esc(shortTitle(kps[ci].title_zh)) + '</button>';
    }
    h += '</div>';

    /* 播放面板（当前要点全字段）*/
    h += '<div class="mk-panel" aria-live="polite"></div>';

    /* 信度图例（中英·规则并陈）*/
    h += '<div class="mk-legend">';
    ['T0', 'T1', 'T2'].forEach(function (k) {
      var lv = evLevels[k]; if (!lv) return;
      h += '<div class="mk-leg"><b>' + esc(lv.label_zh || k) + '</b>'
        + (lv.label_en ? '<span class="en-line">' + esc(lv.label_en) + '</span>' : '')
        + '<span>' + esc(lv.rule_zh || '') + '</span>'
        + (lv.rule_en ? '<span class="en-line">' + esc(lv.rule_en) + '</span>' : '') + '</div>';
    });
    h += '</div>';

    /* 示意声明与页脚判断（中英）*/
    if (frame.disclaimer_zh) h += '<div class="mk-disc">⚠︎ ' + esc(frame.disclaimer_zh)
      + (frame.disclaimer_en ? ' <span class="en-line">' + esc(frame.disclaimer_en) + '</span>' : '') + '</div>';
    if (meta.icon_note_zh) h += '<div class="mk-disc">✎ ' + esc(meta.icon_note_zh) + '</div>';
    if (d.closer && d.closer.zh) h += '<div class="mk-closer">' + esc(d.closer.zh)
      + (d.closer.en ? '<div class="en-line">' + esc(d.closer.en) + '</div>' : '') + '</div>';

    /* 底本出处 */
    if (meta.source_url) {
      h += '<div class="mk-src">📎 底本：<a href="' + esc(meta.source_url)
        + '" target="_blank" rel="noopener" style="color:var(--blue)">'
        + esc(meta.source_primary || meta.source_url) + '</a></div>';
    }

    /* ── 八要点全文静态清单（不损之保证：纵不播放，逐条俱在）── */
    h += '<details class="mk-all" open><summary>📜 八要点全文（逐条可查，不依赖播放）'
      + '<span class="en-line" style="font-size:.86em"> · Full text of all eight points</span></summary>';
    for (var qi = 0; qi < n; qi++) {
      h += '<div class="mk-card">' + kpDetailHTML(kps[qi], qi) + '</div>';
    }
    h += '</details>';
    h += '</section>';
    el.innerHTML = h;

    function shortTitle(t) { t = t || ''; return t.length > 8 ? t.slice(0, 8) + '…' : t; }

    /* ── 状态 ── */
    var cv = el.querySelector('.mk-cv');
    var cx = cv.getContext('2d');
    var ui = {
      play: el.querySelector('.mk-play'), seek: el.querySelector('.mk-seek'),
      spd: el.querySelector('.mk-speed'), cur: el.querySelector('.mk-cur'),
      panel: el.querySelector('.mk-panel')
    };
    var S = { playing: false, ki: 0, p: 0, speed: 1, last: 0,
      layer: { labels: true, en: true, links: true, all: true } };

    function elapsedTo(i, frac) {
      var acc = 0; for (var k = 0; k < i; k++) acc += (kps[k].duration_s || 0);
      return acc + frac * (kps[i].duration_s || 0);
    }
    function clock() { return elapsedTo(S.ki, S.p); }

    function setPoint(i, keepP) {
      S.ki = clamp(i, 0, n - 1);
      if (!keepP) S.p = 0;
      ui.panel.innerHTML = kpDetailHTML(kps[S.ki], S.ki);
      var chips = el.querySelectorAll('.mk-chip');
      for (var c = 0; c < chips.length; c++) chips[c].className = 'mk-chip' + (c === S.ki ? ' on' : '');
    }

    /* ── 绘制 ── */
    function draw() {
      cx.clearRect(0, 0, W, H);
      cx.fillStyle = '#f7f2e7'; cx.fillRect(0, 0, W, H);

      if (S.layer.links) {
        for (var q = 0; q < n; q++) {
          if (!isShown(q)) continue;
          var pp = slotPos(q);
          cx.strokeStyle = 'rgba(184,134,60,' + (q === S.ki ? 0.55 : 0.14) + ')';
          cx.lineWidth = q === S.ki ? 1.6 : 1;
          cx.beginPath(); cx.moveTo(CX, CY); cx.lineTo(pp.x, pp.y); cx.stroke();
        }
      }

      for (var ri = 0; ri < layers.length; ri++) {
        var lay = layers[ri], R = (lay.radius || 0) * SCALE;
        cx.strokeStyle = toneColor(lay.tone); cx.globalAlpha = 0.5; cx.lineWidth = 1.2;
        cx.beginPath(); cx.arc(CX, CY, R, 0, Math.PI * 2); cx.stroke(); cx.globalAlpha = 1;
        if (S.layer.labels) {
          var la = -Math.PI * 0.78, lx = CX + Math.cos(la) * R, ly = CY + Math.sin(la) * R;
          cx.fillStyle = toneColor(lay.tone);
          cx.font = '12px "Noto Serif SC", serif'; cx.textAlign = 'left'; cx.textBaseline = 'middle';
          cx.fillText(lay.label_zh || '', lx + 4, ly - (S.layer.en ? 6 : 0));
          if (S.layer.en && lay.label_en) {
            cx.globalAlpha = 0.7; cx.font = '10px sans-serif';
            cx.fillText(lay.label_en, lx + 4, ly + 7); cx.globalAlpha = 1;
          }
        }
      }

      var r0 = 30 * (1 + (S.playing ? 0.05 * Math.sin(clock() * 3) : 0));
      var gr = cx.createRadialGradient(CX, CY, 0, CX, CY, r0 * 2.4);
      gr.addColorStop(0, 'rgba(184,134,60,0.55)'); gr.addColorStop(1, 'rgba(184,134,60,0)');
      cx.fillStyle = gr; cx.beginPath(); cx.arc(CX, CY, r0 * 2.4, 0, Math.PI * 2); cx.fill();
      cx.fillStyle = '#b8863c'; cx.beginPath(); cx.arc(CX, CY, r0, 0, Math.PI * 2); cx.fill();
      cx.fillStyle = '#fff'; cx.font = 'bold 13px "Noto Serif SC", serif';
      cx.textAlign = 'center'; cx.textBaseline = 'middle';
      cx.fillText(frame.center_label_zh || '佛座', CX, CY - (S.layer.en && frame.center_label_en ? 6 : 0));
      if (S.layer.en && frame.center_label_en) {
        cx.font = '9px sans-serif'; cx.fillStyle = '#f6ead6';
        cx.fillText(frame.center_label_en, CX, CY + 8);
      }

      for (var i = 0; i < n; i++) {
        var pos = slotPos(i), col = toneColor((layerById[kps[i].layer] || {}).tone);
        var shown = isShown(i), active = (i === S.ki);
        if (!shown && !S.layer.all) continue;
        var rr = active ? 13 * (0.7 + 0.3 * easeOut(clamp(S.p * 3, 0, 1))) : (shown ? 8 : 6);
        if (active) { cx.fillStyle = hexA(col, 0.22); cx.beginPath(); cx.arc(pos.x, pos.y, rr + 9, 0, Math.PI * 2); cx.fill(); }
        cx.globalAlpha = shown ? 1 : 0.28;
        cx.fillStyle = shown ? col : '#f7f2e7'; cx.strokeStyle = col; cx.lineWidth = active ? 2.4 : 1.4;
        cx.beginPath(); cx.arc(pos.x, pos.y, rr, 0, Math.PI * 2); cx.fill(); cx.stroke();
        cx.fillStyle = shown ? '#fff' : col; cx.font = (active ? 'bold ' : '') + '12px sans-serif';
        cx.textAlign = 'center'; cx.textBaseline = 'middle';
        cx.fillText(String(kps[i].idx || (i + 1)), pos.x, pos.y);
        cx.globalAlpha = 1;
        if (active && S.p > 0) {
          cx.strokeStyle = hexA(col, 0.9); cx.lineWidth = 3; cx.beginPath();
          cx.arc(pos.x, pos.y, rr + 6, -Math.PI / 2, -Math.PI / 2 + S.p * Math.PI * 2); cx.stroke();
        }
      }

      ui.cur.textContent = clock().toFixed(1);
      if (!S.playing) ui.seek.value = Math.round((clock() / total) * 1000);
    }
    function isShown(i) { return S.layer.all ? true : (i < S.ki || (i === S.ki && S.p > 0.15)); }
    function hexA(hex, a) {
      var m = /^#?([0-9a-f]{6})$/i.exec(hex); if (!m) return 'rgba(0,0,0,' + a + ')';
      var v = parseInt(m[1], 16);
      return 'rgba(' + ((v >> 16) & 255) + ',' + ((v >> 8) & 255) + ',' + (v & 255) + ',' + a + ')';
    }

    /* ── 时钟 ── */
    function frameLoop(ts) {
      if (S.playing) {
        if (!S.last) S.last = ts;
        var dt = Math.min(0.1, (ts - S.last) / 1000); S.last = ts;
        var dur = kps[S.ki].duration_s || 1;
        S.p += (dt * S.speed) / dur;
        if (S.p >= 1) { if (S.ki < n - 1) { setPoint(S.ki + 1); } else { S.p = 1; pause(); } }
        ui.seek.value = Math.round((clock() / total) * 1000);
      } else { S.last = 0; }
      draw();
      requestAnimationFrame(frameLoop);
    }

    function play() { if (S.ki === n - 1 && S.p >= 1) { setPoint(0); } S.playing = true; ui.play.innerHTML = '⏸ 暂停'; S.last = 0; }
    function pause() { S.playing = false; ui.play.innerHTML = '▶ 播放要点'; S.last = 0; }
    function toggle() { S.playing ? pause() : play(); }
    function seekTo(frac) {
      var tt = clamp(frac, 0, 1) * total, acc = 0;
      for (var i = 0; i < n; i++) {
        var di = kps[i].duration_s || 0;
        if (tt <= acc + di || i === n - 1) { S.ki = i; S.p = di ? clamp((tt - acc) / di, 0, 1) : 1; break; }
        acc += di;
      }
      setPoint(S.ki, true);
    }

    /* ── 事件 ── */
    ui.play.addEventListener('click', toggle);
    el.querySelector('.mk-prev').addEventListener('click', function () {
      if (S.p > 0.02) { setPoint(S.ki, true); } else { setPoint(S.ki - 1); } pause();
    });
    el.querySelector('.mk-next').addEventListener('click', function () {
      if (S.ki < n - 1) { setPoint(S.ki + 1); } pause();
    });
    ui.spd.addEventListener('change', function () { S.speed = parseFloat(ui.spd.value) || 1; });
    ui.seek.addEventListener('input', function () { pause(); seekTo(ui.seek.value / 1000); });
    var lgs = el.querySelectorAll('.mk-lg');
    for (var gi = 0; gi < lgs.length; gi++) {
      lgs[gi].addEventListener('change', function () { S.layer[this.getAttribute('data-k')] = this.checked; draw(); });
    }
    var chips = el.querySelectorAll('.mk-chip');
    for (var c2 = 0; c2 < chips.length; c2++) {
      chips[c2].addEventListener('click', function () { setPoint(parseInt(this.getAttribute('data-i'), 10)); pause(); });
    }

    setPoint(0);
    draw();
    requestAnimationFrame(frameLoop);
    return true;
  }

  return { render: render };
})();

/* 兼容 article.js 之调用签名：renderMiaoyanKeypoints('#article-kp') */
function renderMiaoyanKeypoints(containerId) {
  return MiaoyanKeypoints.render(containerId);
}
