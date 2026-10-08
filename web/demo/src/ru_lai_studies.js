/* ru_lai_studies.js — 《如来现相品》数据科学层渲染器（三视角：语言统计·代数组合·拓扑）
 * 数据由 build.py 内嵌为全局 RU_LAI_STUDIES（源自 data/translation/ru_lai_studies.yaml）。
 * 零依赖；节点桩可测。渲染入 renderRuLaiStudies(sel) 指定容器。
 */
(function (global) {
  'use strict';

  var DIR = ['E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE', 'U', 'D'];
  var DIR_ZH = { E: '東', SE: '東南', S: '南', SW: '西南', W: '西', NW: '西北', N: '北', NE: '東北', U: '上', D: '下' };

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function x2(v) { return (Math.round(v * 100) / 100).toFixed(2); }

  function bar(v, max, color) {
    var w = max ? Math.round(100 * v / max) : 0;
    return '<span style="display:inline-block;height:9px;width:' + w + 'px;background:' +
      (color || '#b8863c') + ';border-radius:2px;vertical-align:middle"></span>';
  }

  function table(head, rows) {
    var h = '<table style="width:100%;border-collapse:collapse;font-size:0.82em;margin:6px 0">';
    h += '<tr>' + head.map(function (c) {
      return '<th style="text-align:left;border-bottom:2px solid var(--gold);padding:3px 6px">' + esc(c) + '</th>';
    }).join('') + '</tr>';
    rows.forEach(function (r) {
      h += '<tr>' + r.map(function (c) {
        return '<td style="border-bottom:1px solid var(--line);padding:3px 6px">' + c + '</td>';
      }).join('') + '</tr>';
    });
    return h + '</table>';
  }

  function section(id, icon, title, body) {
    return '<div class="section" id="' + id + '" style="border-left:4px solid var(--gold)">' +
      '<h3>' + icon + ' ' + esc(title) + '</h3>' + body + '</div>';
  }

  function renderL1(L) {
    var c = L.corpus, z = L.zipf;
    var h = '<div style="font-size:0.82em;color:var(--text2)">' + esc(c.note_zh) + '</div>';
    h += table(['指标', '值'], [
      ['卷六 CJK 字数', c.cjk_total],
      ['不重复字（types）', c.unique_chars],
      ['型例比 TTR', c.type_token_ratio],
      ['字熵 Shannon（bit）', c.shannon_entropy_bits],
      ['最大熵 log₂(types)', c.max_entropy_bits],
      ['Zipf log–log 斜率', z.slope]
    ]);
    var maxc = (z.top_chars[0] || {}).count || 1;
    h += '<div style="font-size:0.82em;margin-top:8px"><b>字频前 15</b></div>';
    h += table(['字', '频', ''], z.top_chars.map(function (t) {
      return [esc(t.char), t.count, bar(t.count, maxc)];
    }));
    var tc = L.term_counts || {};
    var keys = Object.keys(tc).sort(function (a, b) { return tc[b] - tc[a]; });
    var maxt = tc[keys[0]] || 1;
    h += '<div style="font-size:0.82em;margin-top:8px"><b>关键词频</b></div>';
    h += table(['词', '频', ''], keys.map(function (k) {
      return [esc(k), tc[k], bar(tc[k], maxt, '#5e8b9e')];
    }));
    var sf = L.sea_family || {};
    h += '<div style="font-size:0.82em;margin-top:8px"><b>「海」族词</b>：总计 ' + sf.total_sea +
      ' 见／不同构词 ' + sf.distinct_forms + ' 式</div>';
    h += table(['构词', '频'], (sf.top || []).slice(0, 12).map(function (x) {
      return [esc(x.form), x.count];
    }));
    var tf = L.tfidf || {};
    var gids = Object.keys(tf);
    h += '<div style="font-size:0.82em;margin-top:8px"><b>TF-IDF · 各组特征二字</b>（前 5）</div>';
    h += table(['偈组', '特征词（tf-idf）'], gids.map(function (g) {
      return [esc(g), (tf[g] || []).map(function (t) {
        return esc(t.form) + '<span style="color:var(--text2)">(' + t.tfidf + ')</span>';
      }).join(' ')];
    }));
    return h;
  }

  function renderL2(A) {
    var g = A.octagon_symmetry, ap = A.antipodal, qp = A.questions_partition;
    var h = '<div style="font-size:0.82em;color:var(--text2)">' + esc(g.note_zh) + '</div>';
    h += table(['群', '阶', '生成元', 'Burnside 不动点之和', '轨道数'], [
      [esc(g.group), g.order, esc(g.generators.join('、')), g.burnside_fixed_sum, g.num_orbits]
    ]);
    h += '<div style="font-size:0.82em;margin-top:6px"><b>轨道</b>（下标→方位）：</div>';
    (g.orbits || []).forEach(function (orb, i) {
      h += '<div style="font-size:0.8em">轨道 ' + (i + 1) + '：' +
        orb.map(function (k) { return DIR_ZH[DIR[k]] || k; }).join('、') + '（' + orb.length + ' 员）</div>';
    });
    h += '<div style="font-size:0.82em;color:var(--text2);margin-top:4px">' + esc(g.readout_zh) + '</div>';
    h += '<div style="font-size:0.82em;margin-top:8px"><b>对跖五对</b></div>';
    h += table(['组', '两方'], (ap.pairing || []).map(function (p, i) {
      return [i + 1, esc(DIR_ZH[p[0]] + ' ↔ ' + DIR_ZH[p[1]])];
    }));
    h += '<div style="font-size:0.82em;margin-top:8px"><b>四十问之「海」特征二分</b>：' +
      esc(qp.readout_zh) + '</div>';
    return h;
  }

  function renderL3(T) {
    var g = T.graph, f = T.flag_complex, fil = T.filtration;
    var h = '<div style="font-size:0.82em;color:var(--text2)">' + esc(g.rule_zh) + '</div>';
    h += table(['指标', '值'], [
      ['方位节点 V', g.nodes],
      ['最大共字数', g.max_weight],
      ['t=1 边密度', g.density_t1],
      ['t=1 分量 β₀', f.at_t1.beta0],
      ['t=1 三角形', f.at_t1.triangles],
      ['t=1 旗复形 β₁', f.at_t1.beta1]
    ]);
    h += '<div style="font-size:0.82em;color:var(--text2)">' + esc(g.readout_zh) + '</div>';
    h += table(['共字最多之对', '', ''], (g.top_edges || []).slice(0, 8).map(function (p) {
      return [esc(DIR_ZH[p.a] + ' ↔ ' + DIR_ZH[p.b]), '共字', p.shared];
    }));
    h += '<div style="font-size:0.82em;margin-top:8px"><b>过滤复形</b>：' + esc(fil.note_zh) + '</div>';
    h += table(['t', '边', 'β₀', 'cyclomatic', '三角形', 'β₁'], fil.steps.map(function (s) {
      return [s.threshold, s.edges, s.beta0, s.cyclomatic, s.triangles, s.beta1];
    }));
    h += '<div style="font-size:0.8em;color:var(--text2)">' + esc(f.note_zh) + '</div>';
    return h;
  }

  function renderRuLaiStudies(sel) {
    var d = (typeof global.RU_LAI_STUDIES !== 'undefined') ? global.RU_LAI_STUDIES : null;
    if (!d || !d.linguistic) return '';
    var m = d.meta || {};
    var h = '<div class="section" style="border-left:4px solid var(--gold)"><h3>🧭 ' +
      esc(m.title_zh || '数据科学层') + '</h3>' +
      '<div style="font-size:0.8em;color:var(--text2)">' + esc(m.note_zh || '') + '</div></div>';
    h += section('rls-linguistic', '📊', '视角一 · 语言统计', renderL1(d.linguistic));
    h += section('rls-algebra', '🔷', '视角二 · 代数·组合', renderL2(d.algebra));
    h += section('rls-topology', '🕸', '视角三 · 拓扑', renderL3(d.topology));
    var root = (typeof document !== 'undefined') ? document.querySelector(sel) : null;
    if (root) root.innerHTML = h;
    return h;
  }

  global.renderRuLaiStudies = renderRuLaiStudies;
  if (typeof module !== 'undefined' && module.exports) module.exports = { renderRuLaiStudies: renderRuLaiStudies };
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));