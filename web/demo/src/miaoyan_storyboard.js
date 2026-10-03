/* 世主妙严品 · 电影式分镜播放器
   数据源：data/narrative/miaoyan_storyboard.yaml（MIAOYAN_SB）
           合幕曼荼罗环位复用 data/narrative/miaoyan_narrative.yaml（MIAOYAN_NARR.space.rings）
   本文件不含任何经文、名相或布局内容——一切要素、层次、引文、景别、运镜、镜序皆自数据读出。
   几何、配色、图元笔法属渲染层。 */
(function (global) {
  'use strict';

  var PAL = {
    gold: '#d4a03c', goldSoft: 'rgba(212,160,60,', ink: '#2a2118',
    jade: '#4a9d8e', lapis: '#3f6fb5', rose: '#c4707e',
    violet: '#8b6bb8', ash: '#8d8577', paper: '#f7f2e7'
  };

  /* ── 小工具 ─────────────────────────────────────────── */
  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function easeInOut(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function now() { return (global.performance && performance.now) ? performance.now() : Date.now(); }
  function fmt(sec) {
    var m = Math.floor(sec / 60), s = Math.floor(sec % 60);
    return (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s);
  }
  /* 稳定散点：同一 id 恒得同一位置，避免每帧抖动 */
  function hsh(str, salt) {
    var h = 2166136261 ^ salt, i;
    str = String(str);
    for (i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = (h * 16777619) >>> 0; }
    return (h % 100000) / 100000;
  }

  /* ── 图元笔法：按 props[].kind 分派 ──────────────────── */
  var GLYPH = {};

  GLYPH.ground = function (g, x, y, r, col) {
    g.beginPath(); g.moveTo(x - r * 2.4, y + r * 0.5); g.lineTo(x + r * 2.4, y + r * 0.5);
    g.strokeStyle = col; g.lineWidth = Math.max(1.2, r * 0.16); g.stroke();
    var i, w = r * 1.9;
    g.globalAlpha = 0.5;
    for (i = -2; i <= 2; i++) {
      g.beginPath(); g.moveTo(x + i * w * 0.42, y + r * 0.5); g.lineTo(x + i * w * 0.42 + r * 0.5, y + r * 1.15);
      g.stroke();
    }
    g.globalAlpha = 1;
  };

  GLYPH.wheel = function (g, x, y, r, col) {
    g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2);
    g.strokeStyle = col; g.lineWidth = Math.max(1, r * 0.14); g.stroke();
    var i, n = 12;
    g.globalAlpha = 0.75;
    for (i = 0; i < n; i++) {
      var a = i / n * Math.PI * 2;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r); g.stroke();
    }
    g.globalAlpha = 1;
  };

  GLYPH.lotus = function (g, x, y, r, col) {
    var i, n = 8;
    for (i = 0; i < n; i++) {
      var a = i / n * Math.PI * 2;
      g.beginPath();
      g.moveTo(x, y);
      g.quadraticCurveTo(x + Math.cos(a - 0.34) * r, y + Math.sin(a - 0.34) * r,
                         x + Math.cos(a) * r * 1.25, y + Math.sin(a) * r * 1.25);
      g.quadraticCurveTo(x + Math.cos(a + 0.34) * r, y + Math.sin(a + 0.34) * r, x, y);
      g.strokeStyle = col; g.lineWidth = Math.max(0.8, r * 0.1); g.stroke();
    }
  };

  GLYPH.jewel = function (g, x, y, r, col) {
    g.beginPath();
    for (var i = 0; i < 6; i++) {
      var a = i / 6 * Math.PI * 2 - Math.PI / 2;
      var px = x + Math.cos(a) * r, py = y + Math.sin(a) * r;
      i ? g.lineTo(px, py) : g.moveTo(px, py);
    }
    g.closePath();
    g.strokeStyle = col; g.lineWidth = Math.max(1, r * 0.16); g.stroke();
    g.globalAlpha = 0.4; g.fillStyle = col; g.fill(); g.globalAlpha = 1;
  };

  GLYPH.lightsea = function (g, x, y, r, col) {
    var i;
    for (i = 1; i <= 3; i++) {
      g.beginPath(); g.arc(x, y, r * (0.45 + i * 0.28), Math.PI * 0.12, Math.PI * 0.88);
      g.strokeStyle = col; g.globalAlpha = 0.34 + i * 0.12;
      g.lineWidth = Math.max(0.8, r * 0.09); g.stroke();
    }
    g.globalAlpha = 1;
  };

  GLYPH.banner = function (g, x, y, r, col) {
    g.beginPath(); g.moveTo(x, y - r * 1.5); g.lineTo(x, y + r * 1.4);
    g.strokeStyle = col; g.lineWidth = Math.max(1, r * 0.13); g.stroke();
    g.beginPath();
    g.moveTo(x, y - r * 1.45); g.lineTo(x + r * 0.95, y - r * 1.05);
    g.lineTo(x + r * 0.72, y - r * 0.35); g.lineTo(x, y - r * 0.6);
    g.closePath(); g.stroke();
    g.beginPath(); g.arc(x, y - r * 1.6, r * 0.2, 0, Math.PI * 2); g.stroke();
  };

  GLYPH.net = function (g, x, y, r, col) {
    var i, j, n = 5, s = r * 1.5;
    g.globalAlpha = 0.62; g.strokeStyle = col; g.lineWidth = Math.max(0.6, r * 0.07);
    for (i = 0; i <= n; i++) {
      g.beginPath(); g.moveTo(x - s + i * s * 2 / n, y - s); g.lineTo(x - s + i * s * 2 / n, y + s); g.stroke();
      g.beginPath(); g.moveTo(x - s, y - s + i * s * 2 / n); g.lineTo(x + s, y - s + i * s * 2 / n); g.stroke();
    }
    g.globalAlpha = 1;
  };

  function cloudPuff(g, x, y, r) {
    g.beginPath();
    g.arc(x - r * 0.7, y, r * 0.6, 0, Math.PI * 2);
    g.arc(x, y - r * 0.25, r * 0.78, 0, Math.PI * 2);
    g.arc(x + r * 0.75, y, r * 0.55, 0, Math.PI * 2);
    g.arc(x, y + r * 0.5, r * 0.72, 0, Math.PI * 2);
  }
  GLYPH.cloud = function (g, x, y, r, col) {
    cloudPuff(g, x, y, r); g.strokeStyle = col; g.lineWidth = Math.max(0.9, r * 0.1);
    g.globalAlpha = 0.8; g.stroke(); g.globalAlpha = 1;
  };
  GLYPH.cloudpair = function (g, x, y, r, col) {
    cloudPuff(g, x - r * 0.8, y, r * 0.78); g.strokeStyle = col; g.lineWidth = Math.max(0.9, r * 0.09); g.stroke();
    cloudPuff(g, x + r * 0.85, y + r * 0.15, r * 0.7); g.stroke();
  };

  GLYPH.jewelrain = function (g, x, y, r, col, seed) {
    var i, s = hsh(seed, 7);
    g.fillStyle = col;
    for (i = 0; i < 16; i++) {
      var k = hsh(seed, i * 31 + 3), k2 = hsh(seed, i * 17 + 11);
      var px = x + (k - 0.5) * r * 3.4, py = y - r * 1.5 + ((k2 + s) % 1) * r * 2.6;
      g.globalAlpha = 0.35 + 0.5 * k2;
      g.beginPath(); g.arc(px, py, r * 0.11, 0, Math.PI * 2); g.fill();
    }
    g.globalAlpha = 1;
  };

  GLYPH.tree = function (g, x, y, r, col) {
    g.beginPath(); g.moveTo(x, y + r * 1.6); g.lineTo(x, y - r * 0.1);
    g.lineWidth = Math.max(1.2, r * 0.2); g.strokeStyle = col; g.stroke();
    cloudPuff(g, x, y - r * 0.45, r * 0.95);
    g.globalAlpha = 0.72; g.lineWidth = Math.max(0.8, r * 0.09); g.stroke(); g.globalAlpha = 1;
  };

  GLYPH.trunk = function (g, x, y, r, col) {
    g.beginPath();
    g.moveTo(x - r * 0.42, y + r * 1.7); g.lineTo(x - r * 0.2, y - r * 0.6);
    g.lineTo(x + r * 0.2, y - r * 0.6); g.lineTo(x + r * 0.42, y + r * 1.7);
    g.closePath(); g.strokeStyle = col; g.lineWidth = Math.max(1, r * 0.12); g.stroke();
    g.globalAlpha = 0.25; g.fillStyle = col; g.fill(); g.globalAlpha = 1;
  };

  GLYPH.branch = function (g, x, y, r, col) {
    g.beginPath();
    g.moveTo(x, y + r * 1.3);
    g.quadraticCurveTo(x - r * 0.5, y, x - r * 1.3, y - r * 0.75);
    g.moveTo(x, y + r * 1.3);
    g.quadraticCurveTo(x + r * 0.5, y, x + r * 1.3, y - r * 0.75);
    g.strokeStyle = col; g.lineWidth = Math.max(1, r * 0.13); g.stroke();
  };

  GLYPH.assembly = function (g, x, y, r, col, seed) {
    var i, n = 26;
    g.fillStyle = col;
    for (i = 0; i < n; i++) {
      var a = i / n * Math.PI * 2, k = hsh(seed || 'a', i);
      var rr = r * (1 + 0.16 * (k - 0.5) * 2);
      g.globalAlpha = 0.4 + 0.45 * k;
      g.beginPath(); g.arc(x + Math.cos(a) * rr, y + Math.sin(a) * rr * 0.42, r * 0.1, 0, Math.PI * 2); g.fill();
    }
    g.globalAlpha = 1;
  };

  GLYPH.sound = function (g, x, y, r, col) {
    var i;
    for (i = 1; i <= 3; i++) {
      g.beginPath(); g.arc(x, y, r * (0.3 + i * 0.34), -0.9, 0.9);
      g.strokeStyle = col; g.globalAlpha = 0.75 - i * 0.16;
      g.lineWidth = Math.max(0.9, r * 0.1); g.stroke();
    }
    g.globalAlpha = 1;
  };

  GLYPH.palace = function (g, x, y, r, col) {
    var w = r * 2.1, h = r * 1.15;
    g.beginPath();
    g.moveTo(x - w, y); g.lineTo(x - w * 0.62, y - h * 0.5);
    g.lineTo(x - w * 0.3, y - h * 0.5); g.quadraticCurveTo(x, y - h * 1.15, x + w * 0.3, y - h * 0.5);
    g.lineTo(x + w * 0.62, y - h * 0.5); g.lineTo(x + w, y);
    g.closePath();
    g.strokeStyle = col; g.lineWidth = Math.max(1, r * 0.12); g.stroke();
    g.globalAlpha = 0.2; g.fillStyle = col; g.fill(); g.globalAlpha = 1;
    g.beginPath(); g.moveTo(x - w * 0.62, y); g.lineTo(x + w * 0.62, y); g.stroke();
    var i;
    for (i = -2; i <= 2; i++) {
      g.globalAlpha = 0.6; g.beginPath();
      g.moveTo(x + i * w * 0.22, y); g.lineTo(x + i * w * 0.22, y - h * 0.34); g.stroke();
    }
    g.globalAlpha = 1;
  };

  GLYPH.lightstream = function (g, x, y, r, col, seed) {
    var i;
    g.strokeStyle = col;
    for (i = -4; i <= 4; i++) {
      var k = hsh(seed || 's', i + 40);
      g.globalAlpha = 0.22 + 0.4 * k;
      g.lineWidth = Math.max(0.6, r * 0.08);
      g.beginPath(); g.moveTo(x + i * r * 0.3, y - r * 1.5); g.lineTo(x + i * r * 0.34, y + r * 1.5); g.stroke();
    }
    g.globalAlpha = 1;
  };

  GLYPH.seat = function (g, x, y, r, col) {
    g.beginPath();
    g.moveTo(x - r * 1.15, y + r * 1.1); g.lineTo(x - r * 0.8, y - r * 0.4);
    g.lineTo(x, y - r * 1.15); g.lineTo(x + r * 0.8, y - r * 0.4);
    g.lineTo(x + r * 1.15, y + r * 1.1); g.closePath();
    g.strokeStyle = col; g.lineWidth = Math.max(1.1, r * 0.13); g.stroke();
    g.globalAlpha = 0.22; g.fillStyle = col; g.fill(); g.globalAlpha = 1;
    g.beginPath(); g.moveTo(x - r * 1.5, y + r * 1.1); g.lineTo(x + r * 1.5, y + r * 1.1); g.stroke();
  };

  GLYPH.hall = function (g, x, y, r, col) {
    var i, w = r * 2.3;
    g.strokeStyle = col; g.lineWidth = Math.max(0.9, r * 0.1);
    for (i = -1; i <= 1; i++) {
      var bw = w * 0.3, bh = r * (0.7 + 0.3 * (1 - Math.abs(i)));
      g.beginPath();
      g.moveTo(x + i * w * 0.34 - bw, y + r * 0.7); g.lineTo(x + i * w * 0.34 - bw, y + r * 0.7 - bh);
      g.lineTo(x + i * w * 0.34 + bw, y + r * 0.7 - bh); g.lineTo(x + i * w * 0.34 + bw, y + r * 0.7);
      g.stroke();
    }
  };

  GLYPH.sun = function (g, x, y, r, col) {
    var i;
    g.beginPath(); g.arc(x, y, r * 0.52, 0, Math.PI * 2);
    g.strokeStyle = col; g.lineWidth = Math.max(1.2, r * 0.14); g.stroke();
    for (i = 0; i < 16; i++) {
      var a = i / 16 * Math.PI * 2, L = i % 2 ? r * 0.85 : r * 1.25;
      g.globalAlpha = i % 2 ? 0.4 : 0.85;
      g.beginPath(); g.moveTo(x + Math.cos(a) * r * 0.62, y + Math.sin(a) * r * 0.62);
      g.lineTo(x + Math.cos(a) * L, y + Math.sin(a) * L); g.stroke();
    }
    g.globalAlpha = 1;
  };

  GLYPH.void = function (g, x, y, r, col) {
    var grd = g.createRadialGradient(x, y, r * 0.1, x, y, r);
    grd.addColorStop(0, PAL.goldSoft + '0.5)'); grd.addColorStop(1, PAL.goldSoft + '0)');
    g.fillStyle = grd; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
    g.globalAlpha = 0.55; g.strokeStyle = col; g.lineWidth = Math.max(0.8, r * 0.05);
    g.setLineDash([r * 0.22, r * 0.18]); g.beginPath(); g.arc(x, y, r * 0.92, 0, Math.PI * 2); g.stroke();
    g.setLineDash([]); g.globalAlpha = 1;
  };

  GLYPH.hairtip = function (g, x, y, r, col) {
    g.beginPath(); g.moveTo(x - r * 1.9, y); g.quadraticCurveTo(x, y - r * 0.55, x + r * 1.9, y);
    g.strokeStyle = col; g.lineWidth = Math.max(1, r * 0.12); g.stroke();
    GLYPH.void(g, x, y, r * 0.5, col);
    for (var i = 0; i < 6; i++) {
      var a = i / 6 * Math.PI * 2;
      g.globalAlpha = 0.7; g.beginPath();
      g.arc(x + Math.cos(a) * r * 0.32, y + Math.sin(a) * r * 0.32, r * 0.07, 0, Math.PI * 2);
      g.fillStyle = col; g.fill();
    }
    g.globalAlpha = 1;
  };

  GLYPH.ring = function (g, x, y, r, col, seed) {
    g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2);
    g.strokeStyle = col; g.globalAlpha = 0.5; g.lineWidth = Math.max(0.8, r * 0.06); g.stroke();
    g.globalAlpha = 1;
    g.fillStyle = col;
    for (var i = 0; i < 10; i++) {
      var a = i / 10 * Math.PI * 2, k = hsh(seed || 'r', i);
      g.globalAlpha = 0.45 + 0.4 * k;
      g.beginPath(); g.arc(x + Math.cos(a) * r, y + Math.sin(a) * r * 0.44, r * 0.1, 0, Math.PI * 2); g.fill();
    }
    g.globalAlpha = 1;
  };

  GLYPH.gate = function (g, x, y, r, col) {
    g.beginPath();
    g.moveTo(x - r * 0.72, y + r); g.lineTo(x - r * 0.72, y - r * 0.2);
    g.quadraticCurveTo(x, y - r * 1.2, x + r * 0.72, y - r * 0.2);
    g.lineTo(x + r * 0.72, y + r); g.stroke();
    g.strokeStyle = col; g.lineWidth = Math.max(1.1, r * 0.14); g.stroke();
    g.globalAlpha = 0.18; g.fillStyle = col; g.fill(); g.globalAlpha = 1;
  };

  /* ── 舞台排布：每种 layout 给出 props 的画面坐标 ────────── */
  function stagePos(act, prop, W, H) {
    var cx = W / 2, cy = H * 0.54;
    var id = prop.id, h1 = hsh(id, 1), h2 = hsh(id, 2), h3 = hsh(id, 3);
    var lx, ly, lr;
    switch (act.layout) {
      case 'buddhafield':
        if (prop.kind === 'ground') { lx = cx; ly = H * 0.86; lr = W * 0.3; }
        else if (prop.kind === 'tree' && id === 'bodhi') { lx = cx; ly = H * 0.42; lr = W * 0.15; }
        else if (prop.kind === 'seat') { lx = cx; ly = H * 0.66; lr = W * 0.1; }
        else if (prop.kind === 'palace') { lx = W * 0.79; ly = H * 0.24; lr = W * 0.11; }
        else if (prop.kind === 'sun' || prop.kind === 'void' || prop.kind === 'hairtip') { lx = cx; ly = H * 0.4; lr = W * 0.12; }
        else {
          var ring = [0.22, 0.31, 0.2, 0.27][prop.level || 0] || 0.25;
          var a = (h1 * 0.62 + 0.06) * Math.PI * 2;
          lx = cx + Math.cos(a) * W * ring * 1.15;
          ly = cy + Math.sin(a) * H * ring * 0.78;
          lr = W * 0.055 * (1.25 - (prop.level || 0) * 0.22);
        }
        break;
      case 'assembly':
        var r2 = [0.34, 0.24, 0.15][prop.level || 0] || 0.2;
        var a2 = (h1 * 0.75 + 0.03) * Math.PI * 2;
        lx = cx + Math.cos(a2) * W * r2 * 1.2;
        ly = cy + Math.sin(a2) * H * r2 * 0.85;
        lr = W * 0.06 * (1.2 - (prop.level || 0) * 0.2);
        break;
      case 'classes':
        var col = Math.floor(h1 * 4), row = prop.level || 0;
        lx = W * (0.2 + col * 0.2) + (h2 - 0.5) * W * 0.05;
        ly = H * (0.26 + row * 0.2) + (h3 - 0.5) * H * 0.05;
        lr = W * 0.058;
        break;
      default: /* mandala */
        var rm = [0.4, 0.3, 0.2][prop.level || 0] || 0.24;
        var a3 = (h1 * 0.8 + 0.02) * Math.PI * 2;
        lx = cx + Math.cos(a3) * W * rm; ly = cy + Math.sin(a3) * H * rm * 0.72;
        lr = W * 0.05;
    }
    return { x: lx, y: ly, r: lr };
  }

  /* 合幕曼荼罗：由 MIAOYAN_NARR.space.rings 实算（一点＝一类） */
  function drawMandala(g, cx, cy, maxR, rings, alpha) {
    if (!rings || !rings.length) return;
    var i, j;
    g.save(); g.globalAlpha = alpha;
    for (i = 0; i < rings.length; i++) {
      var rg = rings[i], rr = maxR * (0.34 + 0.62 * (i + 1) / rings.length);
      g.beginPath(); g.arc(cx, cy, rr, 0, Math.PI * 2);
      g.strokeStyle = PAL.ash; g.globalAlpha = alpha * 0.3;
      g.lineWidth = 1; g.stroke();
      var cls = rg.classes || [];
      for (j = 0; j < cls.length; j++) {
        var a = j / cls.length * Math.PI * 2 - Math.PI / 2;
        var k = hsh(cls[j].id || (rg.id + j), j + i * 13);
        g.globalAlpha = alpha * (0.5 + 0.45 * k);
        g.fillStyle = PAL.gold;
        g.beginPath();
        g.arc(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr, Math.max(1.6, maxR * 0.011), 0, Math.PI * 2);
        g.fill();
      }
    }
    var grd = g.createRadialGradient(cx, cy, 0, cx, cy, maxR * 0.3);
    grd.addColorStop(0, PAL.goldSoft + (alpha * 0.55) + ')');
    grd.addColorStop(1, PAL.goldSoft + '0)');
    g.fillStyle = grd; g.beginPath(); g.arc(cx, cy, maxR * 0.3, 0, Math.PI * 2); g.fill();
    g.restore();
  }

  /* ── 主体构造 ─────────────────────────────────────────── */
  function MiaoyanStoryboard(DATA, NARR) {
    var M = DATA.meta || {}, SIZES = DATA['shot_sizes'] || {}, MOVES = DATA['camera_moves'] || {};
    var ACTS = DATA.acts || [];
    var FLAT = [], ai;
    for (ai = 0; ai < ACTS.length; ai++) {
      ACTS[ai].idx = ai;
      (ACTS[ai].shots || []).forEach(function (s) { FLAT.push({ act: ACTS[ai], shot: s }); });
    }
    var TOTAL = FLAT.reduce(function (a, f) { return a + f.shot.duration_s; 0; }, 0);
    var STARTS = [], acc = 0;
    FLAT.forEach(function (f) { STARTS.push(acc); acc += f.shot.duration_s; });

    return {
      meta: M, acts: ACTS, flat: FLAT, sizes: SIZES, moves: MOVES, narr: NARR || null,
      starts: STARTS, totalDuration: TOTAL, corrections: DATA.corrections || [],
      shotCount: FLAT.length,
      render: function (sel) { new Player(this, sel).mount(); }
    };
  }

  function Player(M, sel) {
    var self = this; this.M = M;
    /* SIZES / MOVES / STARTS / TOTAL 皆属 MiaoyanStoryboard 之局部量，
       于 Player 作用域不可见，故一律自模型取别名——否则浏览器中亦抛 ReferenceError。 */
    var SIZES = M.sizes || {}, MOVES = M.moves || {}, STARTS = M.starts || [], TOTAL = M.totalDuration || 0;
    var idx = 0, playing = false, speed = 1, clock = 0, t0 = 0, raf = 0;
    var canvas, g, layers = { props: true, labels: true, en: true, frame: true };
    var shotStartAbs = 0;

    function esc(s) {
      return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      });
    }

    this.mount = function () {
      var root = document.querySelector(sel);
      if (!root) return;
      /* 面板取值一律走 root（容器内各 id 唯一），与事件绑定同源；
         幕条与分镜格之状态切换用带前缀选择器，因二者是集合而非单元素 */
      var el = function (k) { return root.querySelector('#' + k); };
      var H = [];
      H.push('<div class="miaoyan-sb">');

      /* 体例声明（常驻） */
      H.push('<div class="miaoyan-sb__note">');
      H.push('<div class="miaoyan-sb__noteRow"><span class="miaoyan-sb__tag">底本</span><span>' + esc(M.meta.source_primary) +
             ' · <a href="' + esc(M.meta.source_ref) + '" target="_blank" rel="noopener">CBETA 在线</a></span></div>');
      H.push('<div class="miaoyan-sb__noteRow"><span class="miaoyan-sb__tag">体例</span><span>' + esc(M.meta.method_zh) + '</span></div>');
      H.push('<div class="miaoyan-sb__noteRow miaoyan-sb__noteRow--warn"><span class="miaoyan-sb__tag">' +
             esc(M.meta.reconstruction_flag_zh || '〔本文判断〕') + '</span><span>' +
             '本片之<b>要素</b>悉出底本，可逐字覆核；其<b>空间关系、取景、运镜、光色氛围</b>属现代视觉重构，' +
             '与佛教「經變／變相圖」传统可相比拟，<b>然非經變圖之复现</b>。</span></div>');
      H.push('<div class="miaoyan-sb__noteRow"><span class="miaoyan-sb__tag">存疑</span><span>' + esc(M.meta.uncertainty_zh) + '</span></div>');
      H.push('</div>');

      /* 回源更正 */
      if (M.corrections.length) {
        H.push('<details class="miaoyan-sb__corr"><summary>回源更正 ' + M.corrections.length +
               ' 处（与原台账规格不符者，已改）</summary><ol>');
        M.corrections.forEach(function (c) {
          H.push('<li>' + esc(c.zh) + '<div class="en-line">' + esc(c.en) + '</div></li>');
        });
        H.push('</ol></details>');
      }

      /* 幕条 */
      H.push('<div class="miaoyan-sb__acts">');
      M.acts.forEach(function (a, i) {
        H.push('<button type="button" class="miaoyan-sb__act" data-act="' + i + '">' +
               '<b>' + esc(a.no) + '</b> ' + esc(a.title_zh) +
               '<i>' + esc(a.fascicle_zh) + ' · ' + a.shots.length + ' 镜</i></button>');
      });
      H.push('</div>');

      /* 画面 */
      H.push('<div class="miaoyan-sb__stage"><canvas class="miaoyan-sb__cv"></canvas>' +
             '<div class="miaoyan-sb__slate"><b id="sb-no"></b><span id="sb-size"></span>' +
             '<span id="sb-move"></span><span id="sb-fasc"></span></div></div>');

      /* 字幕 */
      H.push('<div class="miaoyan-sb__subs"><div class="miaoyan-sb__sub" id="sb-sub"></div>' +
             '<div class="miaoyan-sb__sub en-line" id="sb-sub-en"></div></div>');

      /* 经文 */
      H.push('<div class="miaoyan-sb__quote"><div class="miaoyan-sb__quoteRef" id="sb-ref"></div>' +
             '<blockquote id="sb-q"></blockquote><div class="en-line" id="sb-qen"></div>' +
             '<div class="miaoyan-sb__judge" id="sb-judge" hidden></div></div>');

      /* 控制 */
      H.push('<div class="miaoyan-sb__ctl">' +
             '<button type="button" id="sb-play" class="miaoyan-sb__btn">▶ 播放</button>' +
             '<button type="button" id="sb-prev" class="miaoyan-sb__btn">◀ 上一镜</button>' +
             '<button type="button" id="sb-next" class="miaoyan-sb__btn">下一镜 ▶</button>' +
             '<span class="miaoyan-sb__time"><b id="sb-t">00:00</b> / <span id="sb-d"></span></span>' +
             '<select id="sb-speed" class="miaoyan-sb__sel">' +
             '<option value="0.5">0.5×</option><option value="1" selected>1×</option>' +
             '<option value="1.5">1.5×</option><option value="2">2×</option></select>' +
             '<span class="miaoyan-sb__toggles">' +
             '<label><input type="checkbox" id="sb-l-props" checked>要素</label>' +
             '<label><input type="checkbox" id="sb-l-labels" checked>标名</label>' +
             '<label><input type="checkbox" id="sb-l-en" checked>EN</label>' +
             '<label><input type="checkbox" id="sb-l-frame" checked>取景框</label>' +
             '</span></div>');
      H.push('<input type="range" id="sb-seek" class="miaoyan-sb__seek" min="0" max="' +
             Math.round(TOTALABS() * 100) / 100 + '" step="0.01" value="0">');

      /* 分镜表 */
      H.push('<div class="miaoyan-sb__sheetHead">分镜表 · ' + M.shotCount + ' 镜（点格跳镜）' +
             '<i>景别：' + sizeLegend() + '</i><i>运镜：' + moveLegend() + '</i></div>');
      H.push('<div class="miaoyan-sb__sheet" id="sb-sheet"></div>');

      H.push('</div>');
      root.innerHTML = H.join('');

      canvas = root.querySelector('.miaoyan-sb__cv');
      g = canvas.getContext('2d');

      /* 分镜表格子 */
      var sheet = root.querySelector('#sb-sheet');
      M.flat.forEach(function (f, i) {
        var s = f.shot;
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'miaoyan-sb__cell'; b.dataset.i = i;
        b.innerHTML = '<span class="miaoyan-sb__cellNo">' + s.no + '</span>' +
          '<span class="miaoyan-sb__cellAct">' + esc(f.act.no) + '</span>' +
          '<span class="miaoyan-sb__cellSize">' + esc(SIZES[s.size] ? SIZES[s.size].zh : s.size) + '</span>' +
          '<span class="miaoyan-sb__cellMove">' + esc(MOVES[s.move] ? MOVES[s.move].zh : s.move) + '</span>' +
          '<span class="miaoyan-sb__cellSub">' + esc(s.subtitle_zh.slice(0, 22)) + '…</span>' +
          '<span class="miaoyan-sb__cellBar"><i style="width:' +
          Math.round(s.duration_s / 7 * 100) + '%"></i></span>';
        sheet.appendChild(b);
      });

      /* 事件 */
      root.querySelector('#sb-play').onclick = function () { toggle(); };
      root.querySelector('#sb-prev').onclick = function () { go(idx - 1); };
      root.querySelector('#sb-next').onclick = function () { go(idx + 1); };
      root.querySelector('#sb-speed').onchange = function () {
        speed = parseFloat(this.value) || 1;
        /* 倍速变更须重锚时基：以「未加速之真实秒」记 t0，
           否则 clock = (now()-t0)*speed 会把既得进度再乘一次 speed（累积漂移）*/
        anchor();
      };
      root.querySelector('#sb-seek').oninput = function () { clock = parseFloat(this.value) || 0; sync(); draw(); };
      ['props', 'labels', 'en', 'frame'].forEach(function (k) {
        root.querySelector('#sb-l-' + k).onchange = function () { layers[k] = this.checked; draw(); };
      });
      sheet.onclick = function (e) {
        var c = e.target.closest('.miaoyan-sb__cell');
        if (c) go(parseInt(c.dataset.i, 10));
      };
      /* 幕条与分镜格之绑定、状态切换，一律用同一带前缀选择器，避免二者指向不同集合 */
      document.querySelectorAll(sel + ' .miaoyan-sb__act').forEach(function (b) {
        b.onclick = function () {
          var a = parseInt(b.dataset.act, 10);
          for (var i = 0; i < M.flat.length; i++) if (M.flat[i].act === M.acts[a]) { go(i); break; }
        };
      });

      resize();
      global.addEventListener('resize', resize);
      go(0);
      draw();

      function TOTALABS() { return M.totalDuration; }
      function sizeLegend() {
        return Object.keys(SIZES).map(function (k) { return SIZES[k].zh; }).join('／');
      }
      function moveLegend() {
        return Object.keys(MOVES).map(function (k) { return MOVES[k].zh; }).join('／');
      }
      function resize() {
        var w = canvas.parentNode.clientWidth || 900;
        var dpr = global.devicePixelRatio || 1;
        canvas.width = Math.round(w * dpr);
        canvas.height = Math.round(Math.round(w * 0.5) * dpr);
        canvas.style.width = w + 'px';
        canvas.style.height = Math.round(w * 0.5) + 'px';
        g.setTransform(dpr, 0, 0, dpr, 0, 0);
        canvas.__w = w; canvas.__h = Math.round(w * 0.5);
        draw();
      }
      this.toggle = toggle; this.go = go; this.draw = draw; this.sync = sync;

/* 时基锚定：t0 记的是「未加速之真实秒」，clock 再乘 speed 得播放位置。
   故暂停续播、跳镜、跳幕、变速诸处皆须以 clock/speed 回锚，
   否则每次续播都把既得进度再乘一次 speed——累积成不可追之漂移。 */
function anchor() { t0 = now() - (clock / speed) * 1000; }
function toggle() {
        /* 播毕后再按播放：自首镜重放，而非零时立刻又触发「已到片尾」而纹丝不动 */
        if (!playing && clock >= M.totalDuration - 1e-6) { idx = 0; clock = 0; }
        playing = !playing; anchor(); paint(); step();
      }
function go(i) {
        idx = clamp(i, 0, M.flat.length - 1);
        clock = STARTS[idx];
        anchor();
        sync(); draw();
      }
      function step() {
        if (!playing) return;
        clock = (now() - t0) / 1000 * speed;
        if (clock >= M.totalDuration) { clock = M.totalDuration; playing = false; paint(); }
        sync(); draw();
        if (playing) raf = global.requestAnimationFrame(step);
      }
      function shotIndexAt(t) {
        for (var i = M.flat.length - 1; i >= 0; i--) if (t >= STARTS[i] - 1e-6) return i;
        return 0;
      }
      function sync() {
        var i = shotIndexAt(clock);
        if (i !== idx) { idx = i; shotStartAbs = STARTS[i]; }
        else if (clock < shotStartAbs) shotStartAbs = STARTS[i];
        var f = M.flat[idx], s = f.shot;
        el('sb-no').textContent = '第 ' + s.no + ' 镜 / ' + M.shotCount;
        el('sb-size').textContent = '景别 ' + (SIZES[s.size] ? SIZES[s.size].zh : s.size);
        el('sb-move').textContent = '运镜 ' + (MOVES[s.move] ? MOVES[s.move].zh : s.move);
        el('sb-fasc').textContent = f.act.no + '幕 · ' + f.act.fascicle_zh;
        el('sb-sub').textContent = s.subtitle_zh;
        el('sb-sub-en').textContent = s.subtitle_en;
        el('sb-ref').textContent = '出处：' + s.ref;
        el('sb-q').textContent = s.quote_zh;
        el('sb-qen').textContent = s.quote_en;
        var jd = el('sb-judge');
        if (s.reconstruction) {
          jd.hidden = false;
          jd.textContent = (M.meta.reconstruction_flag_zh || '〔本文判断〕') + ' ' + (s.judgment_zh || '');
        } else jd.hidden = true;
        el('sb-t').textContent = fmt(clock);
        var dd = el('sb-d');
        if (dd && !dd.textContent) dd.textContent = fmt(M.totalDuration);
        var sk = el('sb-seek');
        if (document.activeElement !== sk) sk.value = clock;
        var cells = document.querySelectorAll(sel + ' .miaoyan-sb__cell');
        for (var c = 0; c < cells.length; c++) cells[c].classList.toggle('is-on', c === idx);
        var abs = document.querySelectorAll(sel + ' .miaoyan-sb__act');
        for (var a = 0; a < abs.length; a++) abs[a].classList.toggle('is-on', abs[a].dataset.act == f.act.idx);
        paint();
      }
      function paint() {
        var b = el('sb-play');
        if (b) b.textContent = playing ? '⏸ 暂停' : '▶ 播放';
      }

      function draw() {
        var W = canvas.__w || 900, H = canvas.__h || 450;
        var f = M.flat[idx], s = f.shot, act = f.act;
        var sz = SIZES[s.size] || { zoom: 1 }, mv = MOVES[s.move] || { drift: [0, 0, 0] };
        var lt = clamp((clock - STARTS[idx]) / s.duration_s, 0, 1);
        var e = easeInOut(lt);
        var dz = mv.drift[0] || 0, dx = mv.drift[1] || 0, dy = mv.drift[2] || 0;
        var zoom = sz.zoom * (1 + dz * e);
        var cx = W / 2 + dx * e * W * 0.34, cy = H * 0.54 + dy * e * H * 0.34;

        g.clearRect(0, 0, W, H);
        g.fillStyle = PAL.paper; g.fillRect(0, 0, W, H);

        /* 背景光网 */
        g.save();
        for (var i = 1; i <= 7; i++) {
          g.beginPath(); g.arc(cx, cy, Math.min(W, H) * 0.11 * i, 0, Math.PI * 2);
          g.strokeStyle = 'rgba(140,130,110,0.16)'; g.lineWidth = 1; g.stroke();
        }
        for (var a2 = 0; a2 < 12; a2++) {
          var aa = a2 / 12 * Math.PI * 2;
          g.beginPath(); g.moveTo(cx, cy);
          g.lineTo(cx + Math.cos(aa) * W, cy + Math.sin(aa) * W);
          g.strokeStyle = 'rgba(140,130,110,0.09)'; g.stroke();
        }
        g.restore();

        var maxR = Math.min(W, H) * 0.46 * zoom;

        /* 镜头之空间变换：以机位 (cx,cy) 为中心、zoom 为比，作仿射。
           要素、标名、主体高亮环三者共用此式，故「看到的位移」与「被框住的」
           恒为同一坐标——否则平移摇摄时高亮框会与图元脱节，形同虚设。 */
        function cam(pp) {
          return {
            x: cx + (pp.x - W / 2) * zoom,
            y: cy + (pp.y - H * 0.54) * zoom,
            r: pp.r * zoom
          };
        }

        /* 合幕曼荼罗 */
        var mand = (act.props || []).filter(function (p) { return p.kind === 'mandala'; })[0];
        if (mand && layers.props) {
          drawMandala(g, cx, cy, maxR,
            (M.narr && M.narr.space) ? M.narr.space.rings : null, 0.95);
        }

        /* 要素 */
        var focus = s.focus || [], i2, pr;
        for (i2 = 0; i2 < (act.props || []).length; i2++) {
          pr = act.props[i2];
          if (pr.kind === 'mandala') continue;
          var on = focus.indexOf(pr.id) >= 0;
          if (!layers.props && !on) continue;
          var pp = stagePos(act, pr, W, H);
          pp = cam(pp);
          var sz2 = pr.r ? pr.r * zoom : pp.r * (on ? 1.16 : 1);
          var col = on ? PAL.gold : (pr.level ? PAL.ash : PAL.lapis);
          g.save();
          g.globalAlpha = on ? 1 : 0.62;
          g.translate(pp.x, pp.y);
          var fn = GLYPH[pr.kind] || GLYPH.jewel;
          fn(g, 0, 0, sz2, col, pr.id);
          g.restore();
          /* 标名 */
          if (layers.labels && (on || zoom > 0.5 || pr.level === 0)) {
            g.save();
            g.font = (on ? '600 ' : '') + '12px "Noto Serif SC", serif';
            g.textAlign = 'center'; g.textBaseline = 'top';
            g.fillStyle = on ? PAL.ink : 'rgba(90,84,72,0.85)';
            g.fillText(pr.label_zh, pp.x, pp.y + sz2 + 7);
            if (layers.en) {
              g.font = '10px/1.4 Georgia, serif'; g.fillStyle = 'rgba(90,84,72,0.7)';
              g.fillText(pr.label_en, pp.x, pp.y + sz2 + 21);
            }
            g.restore();
          }
        }

        /* 主体高亮环 */
        var subj = (act.props || []).filter(function (p) { return p.id === s.subject; })[0];
        if (subj) {
          var sp = stagePos(act, subj, W, H);
          sp = cam(sp);
          g.save();
          g.strokeStyle = PAL.rose; g.lineWidth = 2;
          g.globalAlpha = 0.5 + 0.35 * Math.sin(clock * 3);
          g.setLineDash([7, 6]);
          g.strokeRect(sp.x - sp.r * 1.7, sp.y - sp.r * 1.7, sp.r * 3.4, sp.r * 3.4);
          g.restore();
        }

        /* 取景框（景别可视化） */
        if (layers.frame) {
          g.save();
          g.strokeStyle = 'rgba(63,111,181,0.65)'; g.lineWidth = 1.5;
          g.setLineDash([9, 7]);
          var fw = W * 0.86 / Math.max(0.12, zoom), fh = H * 0.8 / Math.max(0.12, zoom);
          g.strokeRect(cx - fw / 2, cy - fh / 2, fw, fh);
          g.setLineDash([]);
          g.font = '10px Georgia, serif'; g.fillStyle = 'rgba(63,111,181,0.85)';
          g.textAlign = 'left'; g.textBaseline = 'bottom';
          g.fillText(SIZES[s.size] ? SIZES[s.size].zh : s.size, cx - fw / 2, cy - fh / 2 - 4);
          g.restore();
        }
      }
    };
  }

  function renderMiaoyanStoryboard(sel, data, narr) {
    var D = data || global.MIAOYAN_SB;
    if (!D || !D.acts) return;
    MiaoyanStoryboard(D, narr || global.MIAOYAN_NARR).render(sel);
  }

  global.MiaoyanStoryboard = MiaoyanStoryboard;
  global.renderMiaoyanStoryboard = renderMiaoyanStoryboard;
})(typeof window !== 'undefined' ? window : this);