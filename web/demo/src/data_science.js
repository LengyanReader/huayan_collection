/* data_science.js — 数据科学层渲染器（四视角：语言统计·代数组合·拓扑·几何持久同调）
 * 通用：数据由 build.py 内嵌为全局 ARTICLE_DS（源自 data/translation/<article>_studies.yaml）。
 * 零依赖；节点桩可测。渲染入 renderDataScience(sel) 指定容器。
 * L2 代数视角按数据形状分派：octagon_symmetry（D8 群作用）／census（组合普查）。
 */
(function (global) {
  'use strict';

  var DIR_ZH = { E: '東', SE: '東南', S: '南', SW: '西南', W: '西', NW: '西北', N: '北', NE: '東北', U: '上', D: '下' };

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

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
      ['底本 CJK 字数', c.cjk_total],
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
    var sf = L.sea_family;
    if (sf) {
      h += '<div style="font-size:0.82em;margin-top:8px"><b>「' + esc(sf.char || '海') + '」族词</b>：总计 ' + sf.total_sea +
        ' 见／不同构词 ' + sf.distinct_forms + ' 式</div>';
      h += table(['构词', '频'], (sf.top || []).slice(0, 12).map(function (x) {
        return [esc(x.form), x.count];
      }));
    }
    var tf = L.tfidf || {};
    var gids = Object.keys(tf);
    if (gids.length) {
      h += '<div style="font-size:0.82em;margin-top:8px"><b>TF-IDF · 各组特征二字</b></div>';
      h += table(['文档组', '特征词（tf-idf）'], gids.map(function (g) {
        return [esc(g), (tf[g] || []).map(function (t) {
          return esc(t.form || t.term) + '<span style="color:var(--text2)">(' + (t.tfidf != null ? t.tfidf : t.score) + ')</span>';
        }).join(' ')];
      }));
    }
    return h;
  }

  // ── L2 代数·组合（分派）──
  function renderL2(A) {
    if (A.octagon_symmetry) return renderL2Symmetry(A);
    if (A.census) return renderL2Census(A);
    return '<div style="font-size:0.82em;color:var(--text2)">（无代数视角数据）</div>';
  }

  function renderL2Census(A) {
    var h = '<div style="font-size:0.82em;color:var(--text2)">' + esc(A.note_zh || '') + '</div>';
    (A.census || []).forEach(function (tbl) {
      h += '<div style="font-size:0.82em;margin-top:8px"><b>' + esc(tbl.title_zh) + '</b>' +
        (tbl.title_en ? ' <span style="color:var(--text2)">' + esc(tbl.title_en) + '</span>' : '') + '</div>';
      var maxv = 0;
      (tbl.rows || []).forEach(function (r) { if (r[1] > maxv) maxv = r[1]; });
      h += table(['类别', '类数', ''], (tbl.rows || []).map(function (r) {
        return [esc(r[0]), r[1], bar(r[1], maxv, '#5e8b9e')];
      }));
    });
    h += '<div style="font-size:0.82em;color:var(--text2);margin-top:4px">' + esc(A.readout_zh || '') + '</div>';
    return h;
  }

  function renderL2Symmetry(A) {
    var g = A.octagon_symmetry, ap = A.antipodal, qp = A.questions_partition;
    var h = '<div style="font-size:0.82em;color:var(--text2)">' + esc(g.note_zh) + '</div>';
    h += table(['群', '阶', '生成元', 'Burnside 不动点之和', '轨道数'], [
      [esc(g.group), g.order, esc(g.generators.join('、')), g.burnside_fixed_sum, g.num_orbits]
    ]);
    h += '<div style="font-size:0.82em;margin-top:6px"><b>轨道</b>（下标→方位）：</div>';
    (g.orbits || []).forEach(function (orb, i) {
      h += '<div style="font-size:0.8em">轨道 ' + (i + 1) + '：' +
        orb.map(function (k) { return DIR_ZH[({ E: 0, SE: 1, S: 2, SW: 3, W: 4, NW: 5, N: 6, NE: 7, U: 8, D: 9 })[k]] || k; }).join('、') +
        '（' + orb.length + ' 员）</div>';
    });
    h += '<div style="font-size:0.82em;color:var(--text2);margin-top:4px">' + esc(g.readout_zh) + '</div>';
    h += '<div style="font-size:0.82em;margin-top:8px"><b>对跖五对</b></div>';
    h += table(['组', '两方'], (ap.pairing || []).map(function (p, i) {
      return [i + 1, esc((DIR_ZH[p[0]] || p[0]) + ' ↔ ' + (DIR_ZH[p[1]] || p[1]))];
    }));
    h += '<div style="font-size:0.82em;margin-top:8px"><b>四十问之「海」特征二分</b>：' +
      esc(qp.readout_zh) + '</div>';
    return h;
  }

  function renderL3(T) {
    var g = T.graph, f = T.flag_complex, fil = T.filtration;
    var lab = function (k) { return (g.labels && g.labels[k]) || DIR_ZH[k] || k; };
    var h = '<div style="font-size:0.82em;color:var(--text2)">' + esc(g.rule_zh) + '</div>';
    h += table(['指标', '值'], [
      ['节点 V', g.nodes],
      ['最大共字数', g.max_weight],
      ['t=1 边密度', g.density_t1],
      ['t=1 分量 β₀', f.at_t1.beta0],
      ['t=1 三角形', f.at_t1.triangles],
      ['t=1 旗复形 β₁', f.at_t1.beta1]
    ]);
    h += '<div style="font-size:0.82em;color:var(--text2)">' + esc(g.readout_zh) + '</div>';
    h += table(['共字最多之对', '', ''], (g.top_edges || []).map(function (p) {
      return [esc(lab(p.a) + ' ↔ ' + lab(p.b)), '共字', p.shared];
    }));
    h += '<div style="font-size:0.82em;margin-top:8px"><b>过滤复形</b>：' + esc(fil.note_zh) + '</div>';
    h += table(['t', '边', 'β₀', 'cyclomatic', '三角形', 'β₁'], fil.steps.map(function (s) {
      return [s.threshold, s.edges, s.beta0, s.cyclomatic, s.triangles, s.beta1];
    }));
    h += '<div style="font-size:0.8em;color:var(--text2)">' + esc(f.note_zh) + '</div>';
    return h;
  }

  function renderL4(G) {
    var h = '<div style="font-size:0.82em;color:var(--text2)">' + esc(G.method_zh) + '</div>';
    h += table(['指标', '值'], [
      ['单纯形总数', G.n_simplices],
      ['最大维数', G.max_dim],
      ['本质类', 'H₀ ×' + ((G.essential || {}).H0 || []).length],
      ['Euler 特征 χ（Σ(−1)ⁱfᵢ）', G.euler_char],
      ['Euler–Poincaré 校验', (G.euler_ok ? 'χ = Σ(−1)ⁱβᵢ ✓' : 'χ ≠ Σ(−1)ⁱβᵢ ✗')]
    ]);
    var bf = G.betti_final || {};
    var bfk = Object.keys(bf).sort(function (a, b) { return (+a.slice(1)) - (+b.slice(1)); });
    if (bfk.length) {
      h += '<div style="font-size:0.82em;margin-top:8px"><b>最终复形之 Betti 数</b>（直接 GF(2) 约化，与持久条形互校）</div>';
      h += table(['同调'].concat(bfk), [['βᵢ'].concat(bfk.map(function (k) { return bf[k]; }))]);
    }
    var barcode = G.barcode || {}, ess = G.essential || {};
    var dims = Object.keys(barcode).sort(function (a, b) { return (+a.slice(1)) - (+b.slice(1)); });
    var zh = { H0: 'H₀（连通）', H1: 'H₁（环）', H2: 'H₂（空腔）', H3: 'H₃' };
    var summ = dims.map(function (k) {
      var b = (barcode[k] || []).slice(), mx = 0, top = null;
      b.forEach(function (p) {
        var len = p.birth - (p.death == null ? 0 : p.death);
        if (len > mx) { mx = len; top = p; }
      });
      return [zh[k] || k, b.length, ((ess[k] || []).length),
        top ? (top.birth + ' → ' + top.death + '（幅度 ' + mx + '）') : '—'];
    });
    h += '<div style="font-size:0.82em;margin-top:8px"><b>持久条形摘要</b>（幅度＝birth−death；本质类＝终不灭）</div>';
    h += table(['同调', '有限条数', '本质类', '最长条（birth → death）'], summ);

    var rows = [];
    dims.forEach(function (k) {
      (barcode[k] || []).slice().sort(function (a, b) {
        return (b.birth - (b.death == null ? 0 : b.death)) - (a.birth - (a.death == null ? 0 : a.death));
      }).slice(0, 5).forEach(function (p) {
        rows.push([zh[k] || k, p.birth, (p.death == null ? '∞' : p.death), p.birth - (p.death == null ? 0 : p.death)]);
      });
    });
    h += '<div style="font-size:0.82em;margin-top:8px"><b>各维最长条（前 5）</b></div>';
    h += table(['同调', 'birth(t)', 'death(t)', '幅度'], rows);

    var curve = G.betti_curve || [];
    var ckeys = Object.keys(curve[0] || {}).filter(function (k) { return /^beta/.test(k); })
      .sort(function (a, b) { return (+a.slice(4)) - (+b.slice(4)); });
    h += '<div style="font-size:0.82em;margin-top:8px"><b>Betti 曲线</b>（t 自大至小，复形渐满）</div>';
    h += table(['t', '边 n₁', '三角 n₂', '四面 n₃'].concat(ckeys.map(function (k) { return 'β' + k.slice(4); })),
      curve.map(function (s) {
        return [s.t, s.n1, s.n2, s.n3].concat(ckeys.map(function (k) { return s[k]; }));
      }));
    h += '<div style="font-size:0.82em;color:var(--text2);margin-top:4px">' + esc(G.readout_zh || '') + '</div>';
    if (G.spectral) h += renderSpectral(G.spectral);
    return h;
  }

  function renderSpectral(S) {
    var spec = S.spectrum || [];
    var mx = spec.length ? Math.max.apply(null, spec) : 1;
    var h = '<div style="font-size:0.82em;margin-top:10px"><b>谱几何 · 加权图 Laplacian</b>' +
      ' <span style="color:var(--text2)">L = D − W（W＝共字边权，t=' + S.t + '）</span></div>';
    h += '<div style="font-size:0.8em;color:var(--text2)">' + esc(S.note_zh || '') + '</div>';
    h += table(['不变量', '值'], [
      ['节点 V', S.n_nodes],
      ['加权边和 m', S.n_edges_weighted],
      ['代数连通度 λ₂（Fiedler）', S.algebraic_connectivity],
      ['谱半径 λₙ', S.spectral_radius],
      ['零特征值数（＝连通分量）', S.n_zero_eigen],
      ['谱和 Σλ（＝2m）', S.sum_eigen_equals_2m],
      ['归一化 λ₂（Cheeger 配对）', S.normalized_algebraic_connectivity]
    ]);
    var ch = S.cheeger || {};
    if (ch.value != null) {
      h += '<div style="font-size:0.82em;margin-top:6px"><b>Cheeger 扫掠切（isoperimetric／conductance）</b></div>';
      h += table(['量', '值'], [
        ['最小割比 h（Fiedler 扫掠切）', ch.value + '（|S|=' + ch.cut_size + '）'],
        ['Cheeger 界 [λ₂/2, √(2λ₂)]', '[' + ch.bound_lo + ', ' + ch.bound_hi + ']'],
        ['不等式校验 λ₂/2 ≤ h ≤ √(2λ₂)', (ch.inequality_ok ? '✓' : '✗')]
      ]);
    }
    h += '<div style="font-size:0.82em;margin-top:6px"><b>谱（升序）</b></div>';
    h += table(['#', '特征值', ''], spec.map(function (e, i) {
      return [i, e, bar(Math.max(0, e), mx, '#8a6db0')];
    }));
    var f = S.fiedler || {};
    var lab = function (k) { return (f.labels && f.labels[k]) || DIR_ZH[k] || k; };
    h += '<div style="font-size:0.82em;margin-top:6px"><b>重心分域（Fiedler 向量正负二分）</b>：' +
      '正号域 ' + (f.id_pos || []).length + ' ／ 负号域 ' + (f.id_neg || []).length + '</div>';
    h += '<div style="font-size:0.8em">⊕ ' + (f.id_pos || []).map(function (k) { return esc(lab(k)); }).join('、') + '</div>';
    h += '<div style="font-size:0.8em">⊖ ' + (f.id_neg || []).map(function (k) { return esc(lab(k)); }).join('、') + '</div>';
    return h;
  }

  function renderDataScience(sel) {
    var d = (typeof global.ARTICLE_DS !== 'undefined') ? global.ARTICLE_DS : null;
    if (!d || !d.linguistic) return '';
    var m = d.meta || {};
    var h = '<div class="section" style="border-left:4px solid var(--gold)"><h3>🧭 ' +
      esc(m.title_zh || '数据科学层') + '</h3>' +
      '<div style="font-size:0.8em;color:var(--text2)">' + esc(m.note_zh || '') + '</div></div>';
    h += section('ds-linguistic', '📊', '视角一 · 语言统计', renderL1(d.linguistic));
    h += section('ds-algebra', '🔷', '视角二 · 代数·组合', renderL2(d.algebra));
    h += section('ds-topology', '🕸', '视角三 · 拓扑', renderL3(d.topology));
    if (d.geometry) h += section('ds-geometry', '📐', '视角四 · 几何（持久同调 · 谱几何）', renderL4(d.geometry));
    var root = (typeof document !== 'undefined') ? document.querySelector(sel) : null;
    if (root) root.innerHTML = h;
    return h;
  }

  global.renderDataScience = renderDataScience;
  if (typeof module !== 'undefined' && module.exports) module.exports = { renderDataScience: renderDataScience };
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));