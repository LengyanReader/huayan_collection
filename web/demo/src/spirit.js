// ═══ 灵性仁本·澄明永续 SPIRIT TAB ═══
var SPIRIT_ACTIVE=localStorage.getItem('spirit_active')||'overview';

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

  // ── Navigation moved to left sidebar ──

  // Active section
  var active = sec(SPIRIT_ACTIVE) || data[0];
  if (!active) { cv.innerHTML = h + '<p>请选择章节</p>'; return; }

  h += '<div class="sp-sec">';
  h += '<h2 style="color:var(--gold);margin:0 0 4px">' + active.icon + ' ' + active.title + '</h2>';
  if (active.summary) {
    h += '<p style="font-size:0.85em;color:var(--text2);line-height:1.8">' + (typeof mdToHTML==='function'?mdToHTML(active.summary):active.summary) + '</p>';
  }
  h += '</div>';

  if (active.intro) {
    h += '<div class="sp-intro"><p>' + (typeof mdToHTML==='function'?mdToHTML(active.intro):active.intro).replace(/\n/g, '<br>') + '</p></div>';
  }

  // Topics — collapsible
  if (active.topics && active.topics.length) {
    active.topics.forEach(function(t, idx) {
      h += '<div class="wu-door open" id=sp-topic-' + idx + ' onclick="this.classList.toggle(\'open\')">';
      h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
      h += '<div class=body>';
      h += '<p>' + (typeof mdToHTML==='function'?mdToHTML(t.body):t.body).replace(/\n/g, '<br>') + '</p>';
      h += '</div></div>';
    });
  }

  // ── 海云法师原文辑录 (spiritual_economics 节专属) ──
  if (SPIRIT_ACTIVE === 'spiritual_economics' && SPIRIT_DATA && SPIRIT_DATA.haiyun_primary) {
    h += renderHaiyunPrimary(SPIRIT_DATA.haiyun_primary);
  }

  // ── 环境人文 (env_history / critical_humanities / heritage_practice) ──
  if (['env_history','critical_humanities','heritage_practice'].indexOf(SPIRIT_ACTIVE) >= 0) {
    h += renderEnvHumanities(SPIRIT_ACTIVE);
  }

  // ── Bibliography-powered references ──
  h += renderBibForPage('spirit');

  cv.innerHTML = h;
  try{localStorage.setItem('spirit_active',SPIRIT_ACTIVE);}catch(e){}
}

// ═══ 海云法师灵性经济学原文辑录 ═══
function renderHaiyunPrimary(data) {
  if (!data || !data.quotes) return '';
  var h = '<div class=section style="margin-top:16px;border-left:4px solid var(--gold);padding-left:14px">';
  h += '<h2>📜 ' + (data.meta ? data.meta.title : '原文辑录') + '</h2>';
  h += '<p style="font-size:0.75em;color:var(--text2);margin-bottom:8px">' + (data.meta ? data.meta.principle : '') + '</p>';
  (data.quotes||[]).forEach(function(q) {
    h += '<div class=topic-card style="background:var(--panel)">';
    h += '<blockquote style="font-size:0.85em;line-height:1.9;color:var(--text);margin:0 0 6px;padding-left:10px;border-left:3px solid var(--gold)">' + q.text_zh.replace(/\n/g,'<br>') + '</blockquote>';
    h += '<p style="font-size:0.72em;color:var(--text2)">📎 ' + q.source + '</p>';
    if (q.context) h += '<p style="font-size:0.68em;color:var(--text2)">语境: ' + q.context + '</p>';
    if (q.note) h += '<p style="font-size:0.68em;color:var(--red)">⚠ 注: ' + q.note + '</p>';
    h += '</div>';
  });
  if (data.about_renben) {
    h += '<details style="font-size:0.75em;margin-top:6px"><summary><b>📝 关于「仁本经济学」</b></summary>';
    h += '<p style=color:var(--text2)>' + data.about_renben.note.replace(/\n/g,'<br>') + '</p>';
    if (data.about_renben.action_items) {
      h += '<p style=color:var(--text2)><b>待查:</b><br>' + data.about_renben.action_items.join('<br>') + '</p>';
    }
    h += '</details>';
  }
  h += '</div>';
  return h;
}

// ═══ 环境人文 + 批判遗产 渲染 ═══
function renderEnvHumanities(sectionId) {
  var eh = (SPIRIT_DATA && SPIRIT_DATA.environmental_humanities) ? SPIRIT_DATA.environmental_humanities.environmental_humanities : null;
  if (!eh) return '';
  var sec = null;
  (eh.sections||[]).forEach(function(s) { if (s.id === sectionId) sec = s; });
  if (!sec) return '';
  var h = '<div class=section style="border-left:4px solid var(--gold);padding-left:14px">';
  h += '<h2>' + (sec.icon||'📌') + ' ' + sec.title + '</h2>';
  var md = (typeof mdToHTML==='function') ? mdToHTML : function(s){return s;};
  if (sec.intro) h += '<p style="font-size:0.82em;color:var(--text2);line-height:1.8">' + md(sec.intro).replace(/\n/g,'<br>') + '</p>';
  if (sec.topics) {
    sec.topics.forEach(function(t, idx) {
      h += '<div class="wu-door open" id=eh-topic-' + idx + ' onclick="this.classList.toggle(\'open\')">';
      h += '<span class=arrow>▶</span><span class=ttl>' + t.title + '</span>';
      h += '<div class=body>';
      h += '<p>' + md(t.body).replace(/\n/g,'<br>') + '</p>';
      if (t.sources) {
        h += '<p style="font-size:0.7em;color:var(--text2);margin-top:4px">📚 ';
        t.sources.forEach(function(s,i) { h += (i>0?'<br>':'') + s; });
        h += '</p>';
      }
      h += '</div></div>';
    });
  }
  h += '</div>';
  return h;
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
