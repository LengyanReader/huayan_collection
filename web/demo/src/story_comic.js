/* story_comic.js — 连环画式分镜信息图 · 拍点字幕序列 · 维度信息图（静态·零 Canvas）
 *
 * 取代此前两套 Canvas 播放器（miaoyan_narrative.js / miaoyan_storyboard.js）之方案 B 落地：
 *   A. 分镜连环画 —— MIAOYAN_SB 四幕二十六镜，以「编号 + 分幕 + 箭头」之静态版面承载序列
 *      （连环画式），每格列景别/运镜/时长、字幕、经文引文、出处、〔编辑判断〕；
 *   B. 拍点字幕序列 —— MIAOYAN_NARR 各拍降级为逐拍文字（narration + 出处 + 存疑标记），
 *      时码仅作标签（不再为播放服务）；
 *   C. 维度信息图 —— 各角度 SVG 静态图：词频条形 / Betti 曲线 / 谱柱状 / 会众结构。
 * 序列感由版面表达、信息量由信息图承载——动画信道窄且本机无真机渲染可验，故撤播放器留数据。
 */
(function (global) {
  'use strict';

  var C_TXT = '#1d232b', C_TXT2 = '#5b6470', C_LINE = '#d8dde3', C_GOLD = '#c9a227',
      C_BLUE = '#3a7bbd', C_PURP = '#8a6db0', C_GREEN = '#4f9d69', C_RED = '#b5524a',
      C_BG = '#f4f1ea';

  function esc(s) {
    return String(s === null || s === undefined ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function n(v) { return (typeof v === 'number' && isFinite(v)) ? v : 0; }
  function chip(t, col) {
    return '<span style="display:inline-block;padding:0 6px;margin:0 4px 3px 0;border:1px solid ' +
      (col || C_LINE) + ';border-radius:9px;font-size:0.78em;color:' + (col || C_TXT2) + '">' +
      esc(t) + '</span>';
  }
  function panel(title, body) {
    return '<div style="margin-top:12px;border:1px solid ' + C_LINE + ';border-radius:6px;padding:8px 10px;background:' + C_BG + '">' +
      '<div style="font-size:0.86em;font-weight:600;margin-bottom:5px">' + esc(title) + '</div>' + body + '</div>';
  }

  // ───────────────────────── SVG 静态图 ─────────────────────────
  function svgBars(items, opt) {
    opt = opt || {};
    if (!items || !items.length) return '';
    var color = opt.color || C_GOLD, lblW = opt.lblW || 62, rowH = 19, W = 560;
    var h = items.length * rowH + 4, barMax = W - lblW - 74;
    var mx = 1;
    items.forEach(function (it) { var v = Math.abs(n(it.value)); if (v > mx) mx = v; });
    var s = '<svg viewBox="0 0 ' + W + ' ' + h + '" width="100%" role="img" ' +
      'aria-label="' + esc(opt.label || '条形图') + '" style="display:block;width:100%;max-width:' +
      (opt.maxW || 620) + 'px;height:auto;margin:0 auto">';
    items.forEach(function (it, i) {
      var y = 2 + i * rowH, v = Math.abs(n(it.value));
      var w = Math.max(1, Math.round(barMax * v / mx));
      s += '<text x="0" y="' + (y + 13) + '" font-size="11" fill="' + C_TXT2 + '">' + esc(it.label) + '</text>';
      s += '<rect x="' + lblW + '" y="' + (y + 3) + '" width="' + w + '" height="' + (rowH - 7) +
        '" fill="' + (it.color || color) + '" rx="2"/>';
      s += '<text x="' + (lblW + w + 6) + '" y="' + (y + 13) + '" font-size="11" fill="' + C_TXT + '">' +
        esc(opt.fmt ? opt.fmt(v) : String(v)) + '</text>';
    });
    s += '</svg>';
    return s;
  }

  function svgLines(series, opt) {
    opt = opt || {};
    if (!series || !series.length) return '';
    var W = 560, H = opt.height || 168, pl = 36, pb = 24, pt = 10, pr = 10;
    var len = 0, mx = 1;
    series.forEach(function (s) {
      len = Math.max(len, s.points.length);
      s.points.forEach(function (p) { if (n(p) > mx) mx = n(p); });
    });
    if (len < 2) return '';
    var xs = function (i) { return pl + i * (W - pl - pr) / (len - 1); };
    var ys = function (v) { return H - pb - (H - pb - pt) * (n(v) / mx); };
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" role="img" ' +
      'aria-label="' + esc(opt.label || '折线图') + '" style="display:block;width:100%;max-width:' +
      (opt.maxW || 700) + 'px;height:auto;margin:0 auto">';
    // 网格与轴
    for (var g = 0; g <= 4; g++) {
      var gv = mx * g / 4, gy = ys(gv);
      s += '<line x1="' + pl + '" y1="' + gy + '" x2="' + (W - pr) + '" y2="' + gy +
        '" stroke="' + C_LINE + '" stroke-width="1"/>';
      s += '<text x="0" y="' + (gy + 4) + '" font-size="10" fill="' + C_TXT2 + '">' + gv.toFixed(0) + '</text>';
    }
    series.forEach(function (se) {
      var d = se.points.map(function (p, i) { return (i ? 'L' : 'M') + xs(i).toFixed(1) + ' ' + ys(p).toFixed(1); }).join(' ');
      s += '<path d="' + d + '" fill="none" stroke="' + se.color + '" stroke-width="2" ' +
        (se.dash ? 'stroke-dasharray="5 3" ' : '') + '/>';
    });
    s += '<line x1="' + pl + '" y1="' + (H - pb) + '" x2="' + (W - pr) + '" y2="' + (H - pb) +
      '" stroke="' + C_TXT2 + '" stroke-width="1"/>';
    if (opt.xLabel) {
      s += '<text x="' + pl + '" y="' + (H - 6) + '" font-size="10" fill="' + C_TXT2 + '">' + esc(opt.xLabel[0]) + '</text>';
      s += '<text x="' + (W - pr) + '" y="' + (H - 6) + '" font-size="10" text-anchor="end" fill="' +
        C_TXT2 + '">' + esc(opt.xLabel[1]) + '</text>';
    }
    // 图例
    var lx = pl + 6, ly = 16;
    series.forEach(function (se) {
      s += '<line x1="' + lx + '" y1="' + ly + '" x2="' + (lx + 16) + '" y2="' + ly +
        '" stroke="' + se.color + '" stroke-width="2" ' + (se.dash ? 'stroke-dasharray="5 3" ' : '') + '/>';
      s += '<text x="' + (lx + 20) + '" y="' + (ly + 4) + '" font-size="10" fill="' + C_TXT2 + '">' +
        esc(se.name) + '</text>';
      lx += 24 + se.name.length * 11;
    });
    s += '</svg>';
    return s;
  }

  // ───────────────────────── A. 分镜连环画 ─────────────────────────
  var UNC = {
    scene_boundary: '段落边界', sequence_timing: '节拍次序', timing: '时码',
    spatial_mapping: '空间映射', orientation: '方位取向', arrangement: '排布',
    hierarchy_reading: '层次读法', conceptual_mapping: '概念对应',
    subtlety: '微细义', role: '角色判定', ending: '收束',
    detail: '细节', translation_pending: '英译待定'
  };

  function comicShot(shot, sizes, moves, isLast, meta, propMap) {
    var sz = (sizes && sizes[shot.size] && sizes[shot.size].zh) || shot.size || '';
    var mv = (moves && moves[shot.move] && moves[shot.move].zh) || shot.move || '';
    function lab(id) { var p = propMap && propMap[id]; return p ? (p.label_zh || id) : id; }
    function labEn(id) { var p = propMap && propMap[id]; return p ? (p.label_en || id) : id; }
    var h = '<div style="border:1px solid ' + C_LINE + ';border-radius:6px;background:#fff;padding:8px 10px;margin-bottom:8px">';
    h += '<div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap">' +
      '<b style="color:' + C_GOLD + '">第 ' + n(shot.no) + ' 格</b>' +
      chip(sz, C_BLUE) + chip(mv, C_PURP) + chip(n(shot.duration_s) + ' 秒', C_TXT2) + '</div>';
    // 取景：主体与焦点（自本幕画面要素查标签，故焦点 id 不裸露）
    var zhBits = [], enBits = [];
    if (shot.subject) { zhBits.push('主体「' + lab(shot.subject) + '」'); enBits.push('subject “' + labEn(shot.subject) + '”'); }
    if (shot.focus && shot.focus.length) {
      zhBits.push('焦点 ' + shot.focus.map(function (id) { return '「' + lab(id) + '」'; }).join('、'));
      enBits.push('focus ' + shot.focus.map(function (id) { return '“' + labEn(id) + '”'; }).join(', '));
    }
    if (zhBits.length) {
      h += '<div style="font-size:0.78em;color:' + C_TXT2 + ';margin-top:4px">取景：' + zhBits.join(' · ') + '</div>' +
        '<div class="en-line" style="font-size:0.76em;color:' + C_TXT2 + '">Framing: ' + enBits.join(' · ') + '</div>';
    }
    if (shot.subtitle_zh) {
      h += '<div style="font-size:0.94em;margin-top:5px">' + esc(shot.subtitle_zh) + '</div>' +
        (shot.subtitle_en ? '<div class="en-line" style="font-size:0.85em;color:' + C_TXT2 + '">' + esc(shot.subtitle_en) + '</div>' : '');
    }
    if (shot.quote_zh) {
      h += '<div style="border-left:3px solid ' + C_GOLD + ';padding-left:8px;margin-top:6px;font-size:0.9em">' +
        esc(shot.quote_zh) + '</div>' +
        (shot.quote_en ? '<div class="en-line" style="border-left:3px solid ' + C_GOLD + ';padding-left:8px;margin-top:3px;font-size:0.82em;color:' + C_TXT2 + '">' + esc(shot.quote_en) + '</div>' : '');
    }
    h += '<div style="font-size:0.8em;color:' + C_TXT2 + ';margin-top:6px">出处：' + esc(shot.ref || '〔无出处〕') + '</div>';
    if (shot.reconstruction) {
      h += '<div style="font-size:0.8em;margin-top:5px;background:#fdf4e3;border:1px dashed #d9b45a;border-radius:4px;padding:4px 6px">' +
        chip('〔编辑判断〕', '#a0651a') +
        (meta.reconstruction_flag_en ? chip(meta.reconstruction_flag_en, '#a0651a') : '') +
        esc(shot.judgment_zh || '（未附判断说明）') +
        (shot.judgment_en ? '<div class="en-line" style="color:' + C_TXT2 + ';font-size:0.96em;margin-top:2px">' +
          esc(shot.judgment_en) + '</div>' : '') + '</div>';
    }
    if (!isLast) h += '<div style="text-align:right;color:' + C_GOLD + ';font-size:0.8em">↓ 下一格</div>';
    h += '</div>';
    return h;
  }

  function comicSection(SB) {
    if (!SB || !SB.acts || !SB.acts.length) return '';
    var meta = SB.meta || {}, exp = meta.expected || {};
    var h = '<div style="font-size:0.9em;color:' + C_TXT2 + '">' + esc(meta.subtitle_zh || '') +
      '<div class="en-line">' + esc(meta.subtitle_en || '') + '</div></div>';
    h += '<div style="font-size:0.86em;color:' + C_TXT2 + ';margin-top:4px">底本：' + esc(meta.source_primary || '') +
      ' <a href="' + esc(meta.source_ref || '#') + '" target="_blank" rel="noopener">〔可点回源〕</a></div>';
    h += '<div style="margin-top:8px;border:1px dashed #d9b45a;border-radius:6px;padding:6px 8px;font-size:0.84em;background:#fdf8ee">' +
      chip('凡例', '#a0651a') + esc(meta.method_zh || '') +
      (meta.method_en ? '<div class="en-line" style="color:' + C_TXT2 + ';font-size:0.97em;margin-top:3px">' +
        esc(meta.method_en) + '</div>' : '') + '</div>';
    if (meta.spec_ref) {
      h += '<div style="margin-top:6px;font-size:0.8em;color:' + C_TXT2 + '">分镜规格：' + esc(meta.spec_ref) +
        (meta.spec_ref_en ? '<div class="en-line">' + esc(meta.spec_ref_en) + '</div>' : '') + '</div>';
    }
    if (meta.reconstruction_flag_zh) {
      h += '<div style="margin-top:6px;font-size:0.84em">' + chip(meta.reconstruction_flag_zh, '#a0651a') +
        esc(meta.uncertainty_zh || '') + '<div class="en-line">' + esc(meta.uncertainty_en || '') + '</div></div>';
    }
    if (exp.acts && exp.shots) {
      h += '<div style="margin-top:8px;font-size:0.84em;color:' + C_TXT2 + '">共 ' + n(exp.acts) + ' 幕 · ' +
        n(exp.shots) + ' 格' + (exp.seconds ? ' · 约 ' + n(exp.seconds) + ' 秒（时序参照）' : '') + '</div>';
    }
    if (SB.corrections && SB.corrections.length) {
      h += '<div style="margin-top:6px;font-size:0.82em;color:' + C_TXT2 + '">回源更正 ' +
        SB.corrections.length + ' 处：</div>' +
        SB.corrections.map(function (c) {
          var zh = typeof c === 'string' ? c : (c.text_zh || c.zh || '');
          var en = (typeof c === 'string') ? '' : (c.text_en || c.en || '');
          return '<div style="margin-top:3px;font-size:0.94em">' + esc(zh) +
            (en ? '<div class="en-line" style="color:' + C_TXT2 + '">' + esc(en) + '</div>' : '') + '</div>';
        }).join('');
    }
    var gNo = 0;
    SB.acts.forEach(function (act, ai) {
      h += '<div style="margin-top:14px;border-top:2px solid ' + C_GOLD + ';padding-top:8px">' +
        '<div style="font-size:1.02em;font-weight:700">' + esc(act['no'] || '') + ' · ' + esc(act.title_zh || '') + '</div>' +
        '<div class="en-line" style="font-size:0.84em;color:' + C_TXT2 + '">' + esc(act.title_en || '') + '</div>' +
        '<div style="font-size:0.82em;color:' + C_TXT2 + '">' + esc(act.fascicle_zh || '') +
        (act.fascicle_en ? '<div class="en-line" style="font-size:0.96em">' + esc(act.fascicle_en) + '</div>' : '') + '</div>' +
        (act.layout ? '<div style="margin-top:3px">' + chip('版面类型 ' + act.layout, C_GREEN) + '</div>' : '');
      if (act.lead_zh) {
        h += '<div style="border-left:3px solid ' + C_LINE + ';padding-left:8px;margin-top:5px;font-size:0.88em">' +
          esc(act.lead_zh) + '<div class="en-line" style="color:' + C_TXT2 + ';font-size:0.86em">' + esc(act.lead_en || '') + '</div></div>';
      }
      // 本幕画面要素（props）：逐项列名相＋经文原句＋英译（自 title tooltip 转为可检索正文）
      var props = act.props || [];
      if (props.length) {
        h += '<div style="margin-top:6px;font-size:0.8em;color:' + C_TXT2 + '">画面要素（' + props.length +
          '）· 逐项出经、可回源：</div>';
        h += '<div style="margin-top:3px;border-top:1px dotted ' + C_LINE + '">' + props.map(function (p) {
          return '<div style="padding:2px 0;border-bottom:1px dotted ' + C_LINE + ';font-size:0.78em">' +
            '<b>' + esc(p.label_zh || p.id) + '</b>　' + esc(p.quote_zh || '') +
            '<div class="en-line" style="color:' + C_TXT2 + ';font-size:1.02em">' +
            esc(p.label_en || '') + (p.quote_en ? '　' + esc(p.quote_en) : '') + '</div></div>';
        }).join('') + '</div>';
      }
      var propMap = {};
      props.forEach(function (p) { propMap[p.id] = p; });
      var shots = act.shots || [];
      shots.forEach(function (sh, si) {
        gNo += 1;
        h += comicShot(sh, SB.shot_sizes, SB.camera_moves, si === shots.length - 1, meta, propMap);
      });
      if (ai < SB.acts.length - 1) {
        h += '<div style="text-align:center;color:' + C_GOLD + ';font-weight:700;margin:6px 0">▼ 转入下幕</div>';
      }
      h += '</div>';
    });
    return h;
  }

  // ───────────── 空间（环位）标签解析：id → 中英名 ─────────────
  function spaceLabel(NARR, id) {
    var sp = (NARR && NARR.space) || {};
    if (sp.center && (id === sp.center.id || id === 'center')) return sp.center.label_zh || id;
    var rs = sp.rings || [];
    for (var i = 0; i < rs.length; i++) if (rs[i].id === id) return rs[i].label_zh || id;
    if (id === 'bg') return (sp.background && sp.background.label_zh) || null;
    return null;
  }
  function spaceLabelEn(NARR, id) {
    var sp = (NARR && NARR.space) || {};
    if (sp.center && (id === sp.center.id || id === 'center')) return sp.center.label_en || id;
    var rs = sp.rings || [];
    for (var i = 0; i < rs.length; i++) if (rs[i].id === id) return rs[i].label_en || id;
    if (id === 'bg') return (sp.background && sp.background.label_en) || null;
    return null;
  }
  function ringColor(NARR, id) {
    var rs = ((NARR && NARR.space) || {}).rings || [];
    for (var i = 0; i < rs.length; i++) if (rs[i].id === id && rs[i].color) return rs[i].color;
    return null;
  }
  // 画面构成（cast token）名相：先查 visual_style.cast_labels，次查 space 标签，不裸露内部 id
  function castLabel(NARR, t, lang) {
    var cl = ((NARR && NARR.visual_style) || {}).cast_labels || {};
    if (cl[t] && cl[t][lang === 'en' ? 'label_en' : 'label_zh']) return cl[t][lang === 'en' ? 'label_en' : 'label_zh'];
    return lang === 'en' ? spaceLabelEn(NARR, t) : spaceLabel(NARR, t);
  }

  // ───────────── 环位与口径（space 层：中心＋同心环＋校准说明） ─────────────
  function spaceSection(NARR) {
    var sp = NARR && NARR.space;
    if (!sp || !(sp.rings || []).length) return '';
    var bg = sp.background || {}, h = '';
    if (sp.center && sp.center.label_zh) {
      h += '<div style="font-size:0.85em;margin-bottom:6px">' + chip('中心', C_GOLD) +
        esc(sp.center.label_zh) +
        (sp.center.label_en ? '<div class="en-line" style="color:' + C_TXT2 + '">Center: ' +
          esc(sp.center.label_en) + '</div>' : '') + '</div>';
    }
    var rows = (sp.rings || []).map(function (r) {
      return [esc(r.label_zh || r.id) + '<div class="en-line" style="color:' + C_TXT2 + '">' +
              esc(r.label_en || '') + '</div>',
              String(n(r.member_classes)), String(n(r.member_count)),
              esc(r.source_ref || '〔待核〕')];
    });
    h += '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:0.8em">' +
      '<tr>' + ['环位', '类数', '员数', '出处'].map(function (t) {
        return '<th style="border-bottom:1px solid ' + C_LINE + ';text-align:left;padding:3px 6px">' + t + '</th>';
      }).join('') + '</tr>' +
      rows.map(function (r) {
        return '<tr>' + r.map(function (c, i) {
          return '<td style="border-bottom:1px dotted ' + C_LINE + ';padding:3px 6px;vertical-align:top;' +
            (i === 1 || i === 2 ? 'text-align:right' : '') + '">' + c + '</td>';
        }).join('') + '</tr>';
      }).join('') + '</table></div>';
    if (sp.expected && (sp.expected.classes != null || sp.expected.named != null)) {
      h += '<div style="font-size:0.8em;color:' + C_TXT2 + ';margin-top:4px">口径：共 ' +
        n(sp.expected.classes) + ' 类 · 具名 ' + n(sp.expected.named) + ' 名（各环员数之和对账）</div>';
    }
    if (bg.calibration) {
      h += '<div style="margin-top:6px;font-size:0.8em;background:#fdf8ee;border:1px dashed #d9b45a;' +
        'border-radius:4px;padding:4px 6px">' + chip('口径校准', '#a0651a') + esc(bg.calibration) +
        (bg.calibration_en ? '<div class="en-line" style="color:' + C_TXT2 + '">' + esc(bg.calibration_en) + '</div>' : '') +
        '</div>';
    }
    if (bg.token_note) {
      h += '<div style="margin-top:5px;font-size:0.8em;color:' + C_TXT2 + '">' + chip('示意说明', '#a0651a') +
        esc(bg.token_note) +
        (bg.token_note_en ? '<div class="en-line">' + esc(bg.token_note_en) + '</div>' : '') + '</div>';
    }
    return h;
  }

  // ───────────────────────── B. 拍点字幕序列 ─────────────────────────
  function beatSection(NARR) {
    if (!NARR || !NARR.beats || !NARR.beats.length) return '';
    var beats = NARR.beats.slice().sort(function (a, b) { return n(a.order) - n(b.order); });
    var m = NARR.meta || {};
    var h = '<div style="font-size:0.9em;color:' + C_TXT2 + '">' + esc(m.title_zh || '') +
      (m.title_en ? '<div class="en-line">' + esc(m.title_en) + '</div>' : '') + '</div>';
    h += '<div style="margin-top:6px;font-size:0.84em;color:' + C_TXT2 + '">共 ' + beats.length +
      ' 拍 · 静态逐拍文字序列（时码仅作参照，非播放）</div>';
    var srcs = m.sources || [];
    if (srcs.length) {
      h += '<div style="margin-top:4px;font-size:0.8em;color:' + C_TXT2 + '">回源：' + srcs.map(function (s) {
        return '<a href="' + esc(s.url || '#') + '" target="_blank" rel="noopener">' + esc(s.label || s.url || '') + '</a>';
      }).join('　') + '</div>';
    }
    h += '<div style="margin-top:8px">' + beats.map(function (b, i) {
      var h2 = '<div style="border:1px solid ' + C_LINE + ';border-left:4px solid ' + C_BLUE +
        ';border-radius:6px;padding:7px 9px;margin-bottom:7px;background:#fff">';
      h2 += '<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:baseline">' +
        '<b style="color:' + C_BLUE + '">第 ' + (i + 1) + ' 拍</b>' +
        '<span style="font-size:0.9em">' + esc(b.title_zh || '') + '</span>' +
        chip(n(b.time_start_s).toFixed(1) + '–' + n(b.time_end_s).toFixed(1) + 's', C_TXT2) + '</div>';
      if (b.title_en) h2 += '<div class="en-line" style="font-size:0.82em;color:' + C_TXT2 + '">' + esc(b.title_en) + '</div>';
      // 本拍画面动作（原动画 actions 之降级文字，中英并列）
      var bacts = b.actions || [];
      if (bacts.length) {
        h2 += '<div style="font-size:0.8em;color:' + C_TXT2 + ';margin-top:4px">画面：' +
          bacts.map(function (a) { return esc(a.zh || ''); }).filter(Boolean).join('；') + '</div>' +
          '<div class="en-line" style="font-size:0.8em;color:' + C_TXT2 + '">Frame: ' +
          bacts.map(function (a) { return esc(a.en || ''); }).filter(Boolean).join('; ') + '</div>';
      }
      // 本拍所摄环位与画面构成（自 space 查标签，故 id 不裸露）
      var sf = b.space_focus || [];
      if (sf.length) {
        h2 += '<div style="margin-top:4px;font-size:0.78em">' + chip('环位', C_PURP) +
          sf.map(function (id) { return chip(spaceLabel(NARR, id), C_PURP); }).join('') + '</div>' +
          '<div class="en-line" style="font-size:0.76em;color:' + C_TXT2 + '">Rings: ' +
          sf.map(function (id) { return esc(spaceLabelEn(NARR, id)); }).join(', ') + '</div>';
      }
      var cg = b.cast_groups || [];
      if (cg.length) {
        var pal = (NARR.visual_style && NARR.visual_style.palette) || {};
        h2 += '<div style="margin-top:4px;font-size:0.78em">' + chip('画面构成', C_GREEN) +
          cg.map(function (t) {
            var col = pal[t] || ringColor(NARR, t) || C_LINE;
            return '<span style="display:inline-block;border:1px solid ' + C_LINE + ';border-radius:4px;' +
              'padding:0 5px;margin:0 4px 3px 0;font-size:0.96em"><span style="display:inline-block;width:8px;' +
              'height:8px;border-radius:50%;background:' + esc(col) + ';margin-right:4px"></span>' +
              esc(castLabel(NARR, t, 'zh') || t) + '</span>';
          }).join('') + '</div>' +
          '<div class="en-line" style="font-size:0.76em;color:' + C_TXT2 + '">Composition: ' +
          cg.map(function (t) { return esc(castLabel(NARR, t, 'en') || t); }).join(', ') + '</div>';
      }
      if (b.narration_zh) h2 += '<div style="font-size:0.9em;margin-top:4px">' + esc(b.narration_zh) + '</div>';
      if (b.narration_en) h2 += '<div class="en-line" style="font-size:0.83em;color:' + C_TXT2 + '">' + esc(b.narration_en) + '</div>';
      h2 += '<div style="font-size:0.8em;color:' + C_TXT2 + ';margin-top:5px">出处：' +
        esc(b.narration_ref || '〔无出处〕') + '</div>';
      var unc = b.uncertainty || [];
      if (unc.length) {
        h2 += '<div style="margin-top:5px">' + chip('存疑标注', '#a0651a') +
          unc.map(function (u) { return chip(UNC[u] || u, '#a0651a'); }).join('') + '</div>';
      }
      if (i < beats.length - 1) h2 += '<div style="text-align:right;color:' + C_GOLD + ';font-size:0.78em">↓</div>';
      h2 += '</div>';
      return h2;
    }).join('') + '</div>';
    return h;
  }

  // ───────────────────────── C. 维度信息图 ─────────────────────────
  function figure(id, title, titleEn, note, body) {
    return '<div id="' + id + '" style="border:1px solid ' + C_LINE + ';border-radius:6px;padding:8px 10px;background:#fff;margin-bottom:10px">' +
      '<div style="font-size:0.9em;font-weight:600">' + esc(title) + '</div>' +
      '<div class="en-line" style="font-size:0.8em;color:' + C_TXT2 + '">' + esc(titleEn || '') + '</div>' +
      (note ? '<div style="font-size:0.78em;color:' + C_TXT2 + ';margin:3px 0 6px">' + note + '</div>' : '') +
      body + '</div>';
  }

  function figsSection() {
    var out = [], any = false;
    var DS = (global.ARTICLE_DS && global.ARTICLE_DS.linguistic) ? global.ARTICLE_DS : null;

    // 图一：名号/经文字频条形（L1 语言统计）
    if (DS && DS.linguistic && DS.linguistic.zipf && DS.linguistic.zipf.top_chars &&
        DS.linguistic.zipf.top_chars.length) {
      var tc = DS.linguistic.zipf.top_chars.slice(0, 12);
      var body = svgBars(tc.map(function (t) {
        return { label: t.char, value: t.count };
      }), { label: '字频条形图', color: C_GOLD });
      body += '<div style="font-size:0.78em;color:' + C_TXT2 + ';margin-top:4px">Zipf 斜率 ' +
        n(DS.linguistic.zipf.slope).toFixed(4) + ' · 独字 ' + n(DS.linguistic.corpus.unique_chars) +
        ' · 香农熵 ' + n(DS.linguistic.corpus.shannon_entropy_bits).toFixed(4) + ' bit</div>';
      out.push(figure('sc-fig-topchars', '图一 · 高频字条形（前 12）', 'Top 12 characters by frequency',
        '语料为本品逐字（剥校勘），横轴＝出现次数。', body));
      any = true;
    }
    // 图二：Betti 曲线（L4 持久同调）
    if (DS && DS.geometry && DS.geometry.betti_curve && DS.geometry.betti_curve.length > 1) {
      var cv = DS.geometry.betti_curve;
      var keys = ['beta0', 'beta1', 'beta2', 'beta3'].filter(function (k) { return k in cv[0]; });
      var cols = { beta0: C_BLUE, beta1: C_RED, beta2: C_GREEN, beta3: C_PURP };
      var ser = keys.map(function (k) {
        return { name: 'β' + k.slice(4), color: cols[k], points: cv.map(function (s) { return s[k]; }) };
      });
      var b2 = svgLines(ser, { label: 'Betti 曲线', xLabel: ['t=' + cv[0].t + '（疏）', 't=' + cv[cv.length - 1].t + '（满）'] });
      out.push(figure('sc-fig-betti', '图二 · Betti 曲线（复形随阈值渐满）',
        'Betti curve as the threshold lowers',
        '横轴为共字阈值 t（自大至小），纵轴为各维同调类数。', b2));
      any = true;
    }
    // 图三：谱几何
    if (DS && DS.geometry && DS.geometry.spectral && DS.geometry.spectral.spectrum) {
      var sp = DS.geometry.spectral;
      var ev = (sp.spectrum || []).slice(0, 14);
      var b3 = svgBars(ev.map(function (e, i) { return { label: 'λ' + (i + 1), value: e }; }),
        { label: 'Laplacian 谱柱状图', color: C_PURP, lblW: 34 });
      var ch = sp.cheeger || {};
      b3 += '<div style="font-size:0.78em;color:' + C_TXT2 + ';margin-top:4px">λ₂（代数连通度）' +
        n(sp.algebraic_connectivity).toFixed(4) + ' · 归一化 λ₂ ' + n(sp.normalized_algebraic_connectivity).toFixed(4) +
        ' · 谱半径 ' + n(sp.spectral_radius).toFixed(4) + ' · Cheeger 扫掠切 h＝' + n(ch.value).toFixed(4) +
        ' ∈ [' + n(ch.bound_lo).toFixed(4) + ', ' + n(ch.bound_hi).toFixed(4) + ']</div>';
      out.push(figure('sc-fig-spectrum', '图三 · 图 Laplacian 谱柱状（截前 14）',
        'Spectrum of the weighted graph Laplacian',
        '加权图 L＝D−W；谱和 Σλ＝2m，零特征值数＝连通分量数。', b3));
      any = true;
    }
    // 图四：会众结构（40 类 × 414 名，仅当 ARTICLE_ASSEMBLY 在场）
    var ASM = global.ARTICLE_ASSEMBLY;
    if (ASM && ASM.classes && ASM.classes.length) {
      var byGroup = {}, byRealm = {}, named = 0, classes = ASM.classes.length;
      ASM.classes.forEach(function (c) {
        var g = c.group_zh || c.group_key || '未分组';
        var r = c.realm || '未标';
        var nm = n(c.n_named);
        named += nm;
        if (!byGroup[g]) byGroup[g] = { cls: 0, nm: 0 };
        byGroup[g].cls += 1; byGroup[g].nm += nm;
        if (!byRealm[r]) byRealm[r] = { cls: 0, nm: 0 };
        byRealm[r].cls += 1; byRealm[r].nm += nm;
      });
      var gArr = Object.keys(byGroup).map(function (k) { return { label: k, value: byGroup[k].cls }; });
      var rArr = Object.keys(byRealm).map(function (k) { return { label: k, value: byRealm[k].cls }; });
      var b4 = '<div style="font-size:0.8em;font-weight:600;margin-bottom:2px">按群组之「类数」</div>' +
        svgBars(gArr, { label: '按群组类数条形图', color: C_BLUE, lblW: 78 }) +
        '<div style="font-size:0.8em;font-weight:600;margin:8px 0 2px">按世间之「类数」</div>' +
        svgBars(rArr, { label: '按世间类数条形图', color: C_GREEN, lblW: 78 }) +
        '<div style="font-size:0.78em;color:' + C_TXT2 + ';margin-top:5px">共 ' + classes + ' 类 · 具名 ' +
        named + ' 名（n_named＝经文明出之名数，非类之大小；类之大小经作微塵數／無量）</div>';
      out.push(figure('sc-fig-assembly', '图四 · 会众结构（类数分布）',
        'Assembly structure: classes by group and realm',
        '依经文列次；具名数不作人头数用（类之大小经作微塵數／無量）。', b4));
      any = true;
    }
    if (!any) return '';
    return out.join('');
  }

  // ───────────────────────── 组装 ─────────────────────────
  function renderStoryComic(sel) {
    var SB = (global.MIAOYAN_SB && global.MIAOYAN_SB.acts && global.MIAOYAN_SB.acts.length) ? global.MIAOYAN_SB : null;
    var NR = (global.MIAOYAN_NARR && global.MIAOYAN_NARR.beats && global.MIAOYAN_NARR.beats.length) ? global.MIAOYAN_NARR : null;
    if (!SB && !NR) return '';
    var m = (SB ? SB.meta : NR.meta) || {};
    var h = '<div class="section" style="border-left:4px solid ' + C_GOLD + '">' +
      '<h3>🎞 ' + esc(m.title_zh || '连环画 · 分镜信息图') + '</h3>' +
      (m.title_en ? '<div class="en-line" style="font-size:0.86em;color:' + C_TXT2 + '">' + esc(m.title_en) + '</div>' : '') +
      '<div style="font-size:0.82em;color:' + C_TXT2 + '">' + esc(m.tradition_zh || m.note_zh || '') +
      '<div class="en-line">' + esc(m.tradition_en || m.note_en || '') + '</div></div></div>';

    var CN = ['一', '二', '三', '四'];
    var parts = [];
    if (SB) parts.push(['story-panels', '分镜连环画', 'Storyboard as a static picture-strip', comicSection(SB)]);
    if (NR) parts.push(['story-beats', '拍点字幕序列', 'Beat-by-beat caption sequence', beatSection(NR)]);
    var spHtml = NR ? spaceSection(NR) : '';
    if (spHtml) parts.push(['story-space', '环位与口径', 'Ring layout, counts and calibration', spHtml]);
    parts.forEach(function (p, i) {
      h += '<div id="' + p[0] + '" style="margin-top:14px"><div style="font-size:0.95em;font-weight:700">' +
        (CN[i] || (i + 1)) + ' · ' + esc(p[1]) + '</div>' +
        '<div class="en-line" style="font-size:0.82em;color:' + C_TXT2 + '">' + esc(p[2]) + '</div>' +
        p[3] + '</div>';
    });
    var f = figsSection();
    if (f) {
      h += '<div id="story-figs" style="margin-top:14px"><div style="font-size:0.95em;font-weight:700">' +
        (CN[parts.length] || (parts.length + 1)) + ' · 维度信息图</div>' +
        '<div class="en-line" style="font-size:0.82em;color:' + C_TXT2 + '">Information graphics across dimensions</div>' +
        f + '</div>';
    }
    var root = (global.document && global.document.querySelector) ? global.document.querySelector(sel) : null;
    if (root) root.innerHTML = h;
    return h;
  }

  global.renderStoryComic = renderStoryComic;
})(this);
