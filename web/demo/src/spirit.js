// ═══ 灵性仁本·澄明永续 SPIRIT TAB ═══
var SPIRIT_ACTIVE='overview';

function renderSpirit() {
  var cv = document.getElementById("spirit-view");
  if (!cv) return;
  var data = (typeof SPIRIT_DATA !== 'undefined' && SPIRIT_DATA.sections) ? SPIRIT_DATA.sections : [];
  if (!data.length) { cv.innerHTML = '<p style="color:var(--text2);text-align:center;padding:40px">数据载入中…</p>'; return; }

  // Find section by id
  function sec(id) { for (var i=0;i<data.length;i++) { if (data[i].id===id) return data[i]; } return null; }

  var h = '<style>' +
    '.sp-sec{border-left:4px solid var(--gold);margin-bottom:20px;padding-left:14px}' +
    '.sp-topic{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:10px 0}' +
    '.sp-topic h4{color:var(--gold);font-size:0.92em;margin:0 0 6px}' +
    '.sp-topic p{font-size:0.82em;line-height:1.85;color:var(--text);margin:4px 0}' +
    '.sp-nav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}' +
    '.sp-nav button{padding:6px 14px;border:1px solid var(--line);border-radius:16px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.8em;transition:all 0.2s}' +
    '.sp-nav button:hover{border-color:var(--gold);color:var(--gold)}' +
    '.sp-nav button.on{background:var(--gold);color:#fff;border-color:var(--gold)}' +
    '.sp-intro{font-size:0.85em;line-height:1.9;color:var(--text);background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:10px 0}' +
    '.sp-ref{font-size:0.72em;color:var(--text2);margin-top:20px;padding:10px;background:var(--card);border:1px solid var(--line);border-radius:8px}' +
    '.sp-ref h4{color:var(--gold);margin:0 0 4px}' +
    '.sp-ref li{line-height:1.8}' +
    '</style>';

  // Navigation pills
  h += '<div class="sp-nav">';
  data.forEach(function(s) {
    var on = (SPIRIT_ACTIVE === s.id) ? ' on' : '';
    h += '<button class="sp-nav-btn' + on + '" onclick="SPIRIT_ACTIVE=\'' + s.id + '\';renderSpirit();">' + (s.icon||'📌') + ' ' + s.title.split('·')[0] + '</button>';
  });
  h += '</div>';

  // Active section
  var active = sec(SPIRIT_ACTIVE) || data[0];
  if (!active) { cv.innerHTML = h + '<p>请选择章节</p>'; return; }

  h += '<div class="sp-sec">';
  h += '<h2 style="color:var(--gold);margin:0 0 4px">' + active.icon + ' ' + active.title + '</h2>';
  if (active.summary) {
    h += '<p style="font-size:0.85em;color:var(--text2);line-height:1.8">' + active.summary + '</p>';
  }
  h += '</div>';

  if (active.intro) {
    h += '<div class="sp-intro"><p>' + active.intro.replace(/\n/g, '<br>') + '</p></div>';
  }

  // Topics
  if (active.topics && active.topics.length) {
    active.topics.forEach(function(t) {
      h += '<div class="sp-topic">';
      h += '<h4>' + t.title + '</h4>';
      h += '<p>' + t.body.replace(/\n/g, '<br>') + '</p>';
      h += '</div>';
    });
  }

  // ── Bibliography-powered references ──
  h += renderBibForPage('spirit');

  cv.innerHTML = h;
}

// ═══ Shared: render BIBLIOGRAPHY cards filtered by page tag ═══
function renderBibForPage(tag) {
  if (typeof BIBLIOGRAPHY === 'undefined' || !BIBLIOGRAPHY) return '';
  var all = [];
  var cats = ['sutras','books','reports','haiyun','online'];
  cats.forEach(function(c) {
    if (BIBLIOGRAPHY[c]) {
      BIBLIOGRAPHY[c].forEach(function(e) {
        if ((e.tags||[]).indexOf(tag) >= 0) { e._cat = c; all.push(e); }
      });
    }
  });
  if (!all.length) return '';
  var h = '<div class="sp-ref" style="margin-top:20px"><h4>📚 参考文献与延伸阅读 (' + all.length + '条·四方验证)</h4>';
  all.forEach(function(ref) {
    var gr = ref.goodreads_rating || {};
    var db = ref.douban_rating || {};
    h += '<div style="background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;margin:6px 0;font-size:0.78em;line-height:1.7">';
    // Title + links
    h += '<b style="color:var(--gold)">' + (ref.title_zh || ref.title_en || '') + '</b>';
    if (ref.title_en && ref.title_zh) h += ' <span style="color:var(--text2);font-size:0.9em">' + ref.title_en + '</span>';
    h += '<br><span style="color:var(--text2)">' + (ref.author_zh || ref.author_en || '') + ' · ' + (ref.publisher||'') + ' · ' + (ref.year||'') + '</span>';
    // Ratings row
    if (gr.score || db.score) {
      h += ' <span style="font-size:0.85em;margin-left:4px">';
      if (gr.score) h += '⭐GR ' + gr.score + '(' + (gr.ratings||'?') + ') ';
      if (db.score) h += '📖豆瓣 ' + db.score + ' ';
      if (ref.scholar_citations) h += '📊引用 ' + ref.scholar_citations;
      h += '</span>';
    }
    // Quick quote
    if (ref.quote_zh) {
      var q = ref.quote_zh.substring(0, 120);
      h += '<div style="color:var(--text2);font-size:0.9em;margin:4px 0;padding-left:8px;border-left:2px solid var(--gold)">' + q + (ref.quote_zh.length>120?'…':'') + '</div>';
    }
    // Links row
    var links = ref.links || {};
    h += '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:4px">';
    if (links.official || links.deal || links.mitpress || links.cambridge || links.cbeta_online)
      h += '<a href="' + (links.official||links.deal||links.mitpress||links.cambridge||links.cbeta_online) + '" target=_blank style="font-size:0.85em;color:var(--blue)">🏛 官方</a>';
    if (links.goodreads)
      h += '<a href="' + links.goodreads + '" target=_blank style="font-size:0.85em;color:var(--blue)">📗 GR</a>';
    if (links.douban_2010 || links.douban_2007 || links.douban_2022)
      h += '<a href="' + (links.douban_2010||links.douban_2007||links.douban_2022) + '" target=_blank style="font-size:0.85em;color:var(--blue)">📖 豆瓣</a>';
    h += '</div></div>';
  });
  h += '<p style="font-size:0.68em;color:var(--text2);margin-top:4px">📐 文献来源: <a href="https://goodreads.com" target=_blank>Goodreads</a> · <a href="https://book.douban.com" target=_blank>豆瓣读书</a> · <a href="https://scholar.google.com" target=_blank>Google Scholar</a> · 出版社官网 — 原语优先, 四方交叉验证</p>';
  h += '</div>';
  return h;
}
