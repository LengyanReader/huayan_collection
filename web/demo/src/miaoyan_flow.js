/* ═══════════════════════════════════════════════════════════════════════
 * renderMiaoyanFlow —— 世主妙严品·会众全景流程图（简明静态版 overview）
 *
 * 目的：为整品提供一张一屏可览的结构流程图——依经文列次（idx 0→39）为脉，
 *       按五环（group，恰与经文列次连续对齐）分段，段标配「三世间」教相归属；
 *       每一「类」为一格，格内标 类名·上首，环间以箭头相连。不设展开、检索、
 *       目录等交互；名号之全量在本页正文（全文）逐列具备，本图仅作结构鸟瞰。
 *
 * 数据源（唯一真源，前端零硬编码内容、零臆造）：
 *   data/translation/miaoyan_assembly.yaml → import_all_to_sqlite → SQLite
 *   → db_reader.load_article_assembly() → build.py → var ARTICLE_ASSEMBLY
 *   （其生成器逐字锚定 CBETA T10n0279，本文件「不新增任何经文」。）
 *
 * 不损原则：
 *   ① 四十类之类名、上首逐字入图，皆取 ARTICLE_ASSEMBLY 之既有字段；
 *   ② 全成员名号与本愿原文不因本图简化而丢失——它们恒在页内 ARTICLE_ASSEMBLY
 *      数据层与下方正文之中；本图只承担「结构鸟瞰」一职，非名号清单。
 *   ③ 字段有则显、无则不造：realm/group_zh 缺者留空，绝不臆测。
 * ═══════════════════════════════════════════════════════════════════════ */
var MiaoyanFlow = (function () {
  'use strict';

  function esc(t) {
    return String(t == null ? '' : t)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // 五环配色（依叙事动画既有调色，保持一致性；仅为视觉辨识，非经义高下）
  var GC = {
    bodhisattva: '#b8863c', deities: '#3f5e8c', eight: '#4a7c6f',
    desire: '#a05e3c', form: '#7fa3b3'
  };
  function gcolor(g) { return GC[g] || '#7a6a58'; }
  var CIRC = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩'];

  function render(containerId) {
    var d = (typeof ARTICLE_ASSEMBLY !== 'undefined') ? ARTICLE_ASSEMBLY : null;
    if (!d || !d.classes || !d.classes.length) return false;
    var el = document.querySelector(containerId);
    if (!el) return false;

    /* ── 数据整理（严格按 idx 升序＝经文列次；不重排）── */
    var cls = d.classes.slice().sort(function (a, b) { return (a.idx || 0) - (b.idx || 0); });
    var N = cls.length;
    var nMembers = cls.reduce(function (a, c) { return a + (c.members ? c.members.length : 0); }, 0);
    function uniq(arr) { var s = []; for (var k = 0; k < arr.length; k++) if (s.indexOf(arr[k]) < 0) s.push(arr[k]); return s; }

    // 按 group 之连续段落切带（group 于经文列次本即连续，故此即五环分段）
    var bands = [];
    for (var i = 0; i < N; i++) {
      var g = cls[i].group;
      if (!bands.length || bands[bands.length - 1].group !== g) bands.push({ group: g, cls: [cls[i]] });
      else bands[bands.length - 1].cls.push(cls[i]);
    }
    function bandMeta(b) {
      var names = 0; b.cls.forEach(function (c) { names += (c.members ? c.members.length : 0); });
      return {
        group_zh: uniq(b.cls.map(function (c) { return c.group_zh; })).filter(Boolean).join('／'),
        realm: uniq(b.cls.map(function (c) { return c.realm; })).filter(Boolean).join('／'),
        nCls: b.cls.length, nNames: names
      };
    }

    function stat(v, label) {
      return '<div class="mfd-stat"><b>' + esc(v) + '</b><span>' + esc(label) + '</span></div>';
    }

    /* ── 组装（纯静态流程图，无交互）── */
    var h = '';
    h += '<section class="miaoyan-flow mfd" data-chrome="1">';
    h += '<h2>🗺️ ' + esc(d.title || '世主妙严品 · 会众全景流程')
      + '<span class="en-line" style="font-size:0.6em;color:var(--text2);margin-left:8px">Assembly Panorama — Sutra-order Flow (idx 0–' + (N - 1) + ')</span></h2>';
    h += '<div class="mfd-note">依经文列次（idx 0→' + (N - 1) + '）为脉，按五环分段，段标配「三世间」教相归属；每一「类」为一格，格内标 类名·上首。'
      + '<b>数据全出〈世主妙严品〉卷一列名段（CBETA T10n0279，生成器逐字锚定），本页不增一经文；名号全量见下方正文。</b></div>';

    // 指标总览（一行）
    h += '<div class="mfd-stats">'
      + stat(N, '类') + stat(nMembers, '明列名号') + stat(bands.length, '环')
      + stat(uniq(cls.map(function (c) { return c.realm; })).filter(Boolean).length, '世间')
      + '</div>';

    // 流程图主体：根 → 五段，段间以箭头相连
    h += '<div class="mfd-flow">';
    h += '<div class="mfd-root">本品会众 · ' + N + ' 类 · ' + nMembers + ' 名</div>';
    bands.forEach(function (b, bi) {
      var bm = bandMeta(b);
      if (bi > 0) h += '<div class="mfd-arrow">↓</div>';
      h += '<div class="mfd-band mfd-g-' + esc(b.group) + '" style="border-left-color:' + gcolor(b.group) + '">';
      h += '<div class="mfd-band-h"><span class="mfd-no">' + (CIRC[bi] || (bi + 1)) + '</span>'
        + '<b>' + esc(bm.group_zh || b.group) + '</b>'
        + (bm.realm ? '<span class="mfd-realm">' + esc(bm.realm) + '主</span>' : '')
        + '<span class="mfd-cnt">' + bm.nCls + '类·' + bm.nNames + '名</span>'
        + '<span class="mfd-range">idx ' + esc(b.cls[0].idx) + '–' + esc(b.cls[b.cls.length - 1].idx) + '</span></div>';
      h += '<div class="mfd-cells">';
      b.cls.forEach(function (c) {
        h += '<div class="mfd-cell"'
          + (c.count_expr ? ' title="类众：' + esc(c.count_expr) + '（经文但作约数）"' : '')
          + '><span class="mfd-idx">' + esc(c.idx) + '</span>'
          + '<span class="mfd-cat">' + esc(c.cat) + '</span>'
          + '<span class="mfd-up">' + esc(c.leader) + '</span></div>';
      });
      h += '</div></div>';
    });
    h += '</div>';

    // 图例（五环配色）
    h += '<div class="mfd-legend">';
    bands.forEach(function (b) {
      h += '<span class="mfd-lg"><i style="background:' + gcolor(b.group) + '"></i>' + esc(bandMeta(b).group_zh || b.group) + '</span>';
    });
    h += '<span class="mfd-lg-hint">格内：上首之名</span>';
    h += '</div>';

    h += '<div class="mfd-src">📎 底本出处：<a href="https://cbetaonline.dila.edu.tw/zh/T10n0279" target="_blank" rel="noopener" style="color:var(--blue)">CBETA T10n0279《华严经·世主妙严品》↗</a>'
      + '　<span style="color:var(--text2)">（本图属「经文事实(assembly)」层，不作词素析构与解释判断）</span></div>';

    // 交叉入口（仅跳既有区块，不臆造映射）
    h += '<div class="mfd-xref">另可参：';
    if (typeof narrGo === 'function') h += '<button class="f-nav-btn" type="button" onclick="narrGo()">📽 叙事动画（会众次第涌现）</button>';
    if (typeof edaGo === 'function') h += '<button class="f-nav-btn" type="button" onclick="edaGo()">🔬 名号剖面（词素析构）</button>';
    h += '</div>';

    h += '</section>';
    el.innerHTML = h;
    return true;
  }

  return { render: render };
})();

/* 兼容 article.js 之调用签名：renderMiaoyanFlow('#article-flow') */
function renderMiaoyanFlow(containerId) {
  return MiaoyanFlow.render(containerId);
}
