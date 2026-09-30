// ═══ 独立文章页渲染器 (articles/<id>.html) ═══
// ARTICLE 已由 build.py 内嵌；依赖 common.js 中的 _mdFullToHTML/_mdInline/_mdDocEmbed。
function renderArticle(){
  var a=(typeof ARTICLE!=='undefined')?ARTICLE:null;
  var root=document.getElementById('article-root');
  if(!root){return;}
  if(!a){root.innerHTML='<p style=font-size:0.85em;color:var(--red)>文章数据缺失（ARTICLE 未定义）。</p>';return;}

  var embed=(typeof _mdDocEmbed==='function')?_mdDocEmbed(a.doc_md||''):{html:'',toc:[]};
  var h='';

  // ── 面包屑 ──
  h+='<div style="font-size:0.74em;color:var(--text2);margin-bottom:12px;">';
  h+='<a href="../index.html" style="color:var(--blue);text-decoration:none">主页</a> › ';
  h+='<a href="index.html" style="color:var(--blue);text-decoration:none">独立文章目录</a>';
  if(a.back && a.back.tab){
    h+=' › <a href="../tabs/'+a.back.tab+'.html" style="color:var(--blue);text-decoration:none">'+a.back.label+'</a>';
  }
  h+='</div>';

  // ── 页头横幅 ──
  h+='<div style="background:linear-gradient(120deg,rgba(184,134,60,0.12),rgba(94,139,158,0.08));border:1px solid var(--line);border-radius:12px;padding:20px 22px;margin-bottom:16px;">';
  h+='  <div style="font-size:0.76em;color:var(--text2);letter-spacing:0.5px">📄 独立文章页</div>';
  h+='  <h2 data-skip-toc="1" style="color:var(--gold);margin:6px 0 4px">'+(a.icon?a.icon+' ':'')+a.title+'</h2>';
  if(a.title_sub)h+='  <div style="font-size:0.85em;color:var(--text2)">'+a.title_sub+'</div>';
  if(a.version)h+='  <div style="font-size:0.78em;color:var(--text2);margin-top:6px">'+a.version+'</div>';
  if(a.back && a.back.tab){
    h+='  <a href="../tabs/'+a.back.tab+'.html" style="font-size:0.75em;color:var(--blue);margin-top:10px;display:inline-block">← 返回 '+a.back.label+'</a>';
  }
  h+='</div>';

  // ── 导览 ──
  if(a.meta){
    h+='<div class="section" style="border-left:4px solid var(--gold)" data-chrome="1"><h2>📌 导览</h2>';
    h+='<p style="font-size:0.8em;line-height:1.9;white-space:pre-line">'+_mdInline(a.meta)+'</p></div>';
  }

  // ── 自动目录 ──
  if(embed.toc.length){
    h+='<div class="section" data-chrome="1"><h2>🧭 本文目录</h2>';
    h+='<div style="column-width:250px;column-gap:26px;font-size:0.8em;line-height:1.75">';
    embed.toc.forEach(function(t){
      var pad=(t.lv>2?'padding-left:'+((t.lv-2)*16)+'px;':'');
      h+='<div style="'+pad+'"><a href="#'+t.id+'" style="color:'+(t.lv===2?'var(--gold)':'var(--text2)')+';text-decoration:none">'+t.text+'</a></div>';
    });
    h+='</div></div>';
  }

  // ── 全文 ──
  h+='<div class="section" style="border-left:4px solid var(--gold)" id="article-full">';
  h+='<h2 data-skip-toc="1" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px"><span>📄 '+a.title+' · 全文</span>';
  h+='<span style="display:flex;gap:6px;flex-wrap:wrap">';
  // 名相会处知识图谱：仅当 build.py 内嵌了 ARTICLE_GRAPH（即 SQLite 中有本文名相表）时出现
  if((typeof ARTICLE_GRAPH!=='undefined')&&ARTICLE_GRAPH&&(ARTICLE_GRAPH.terms||[]).length){
    var _n=(ARTICLE_GRAPH.terms||[]).length,_e=(ARTICLE_GRAPH.links||[]).length;
    h+='<button class="f-nav-btn" onclick="openGraphPanel()" title="查看本文名相节点、边与信度分级">🕸 名相会处（'+_n+' 节点／'+_e+' 边）</button>';
  }
  h+='<button id="article-en-toggle" class="f-nav-btn" onclick="toggleArticleEN()" title="在「含英文批注」与「仅中文正文」之间切换显示">🌐 英文批注：显示</button>';
  h+='</span></h2>';
  h+=embed.html;
  h+='</div>';

  // ── 相关艺术品 · 文物 · 壁画 · 考古（默认折叠块，由 common.js renderArticleArtifacts 填充）──
  if((typeof ARTICLE_ARTIFACTS!=='undefined')&&ARTICLE_ARTIFACTS&&(ARTICLE_ARTIFACTS.items||[]).length){
    h+='<div class="section" data-chrome="1" id="article-artifacts" style="border-left:4px solid var(--gold)"></div>';
  }

  // ── 页脚 ──
  h+='<div style="margin-top:18px;padding-top:10px;border-top:1px solid var(--line);font-size:0.74em;color:var(--text2)">';
  h+='<a href="index.html" style="color:var(--blue);text-decoration:none">📚 返回独立文章目录</a>';
  if(a.back && a.back.tab){
    h+=' · <a href="../tabs/'+a.back.tab+'.html" style="color:var(--blue);text-decoration:none">'+a.back.label+'</a>';
  }
  h+='</div>';

  root.innerHTML=h;

  // ── 命中文档名相（自动扫描＋显式标记）──
  if(typeof _markTermRefs==='function' && document.getElementById('article-full')){
    _markTermRefs('#article-full');
  }
  // ── 相关艺术品/文物/壁画/考古（默认折叠）──
  if(typeof renderArticleArtifacts==='function' && document.getElementById('article-artifacts')){
    renderArticleArtifacts('#article-artifacts');
  }

  // ── 阅读模式：识别「英文/术语批注」块，支持仅中文正文切换 ──
  _initArticleENMode();

  // ── 支持 #锚点 直达（目录跳转用真实 id 锚点）──
  if(location.hash){
    setTimeout(function(){
      var el=document.getElementById(location.hash.slice(1));
      if(el)el.scrollIntoView({behavior:'smooth',block:'start'});
    },80);
  }
}

if(document.readyState!=='loading'){renderArticle();}
else{document.addEventListener('DOMContentLoaded',renderArticle);}

// ═══ 多语对读阅读模式：折叠/展开英文批注块 ═══
// 批注块特征：以「英译对读 / 节级英译要义 / 术语格义 / 主题对读注 / 卷末批注」开头的 blockquote 视作「外文批注」，
// 可一键切换「仅中文正文」阅读；页头「源文本/对读体例」等研究说明块不受影响。
function _initArticleENMode(){
  var s=document.getElementById('article-en-style');
  if(!s){
    s=document.createElement('style');
    s.id='article-en-style';
    s.textContent='#article-full.en-hidden blockquote.en-block{display:none}';
    document.head.appendChild(s);
  }
  var full=document.getElementById('article-full');
  if(full&&!full.dataset.enMarked){
    full.dataset.enMarked='1';
    full.querySelectorAll('blockquote').forEach(function(bq){
      var txt=(bq.textContent||'').replace(/\s+/g,' ').trim();
      if(/^(英译对读|EN对应|EN\s*corresponding|EN\s*note|EN\s*register|EN\s*block|🔑|术语格义|主题对读注|卷末批注)/i.test(txt)) bq.classList.add('en-block');
    });
  }
  _applyArticleENMode();
}
function toggleArticleEN(){
  var cur=(sessionStorage.getItem('article_en_hide')||'')==='1';
  sessionStorage.setItem('article_en_hide', cur?'0':'1');
  localStorage.removeItem('article_en_hide');
  _applyArticleENMode();
  var block=document.getElementById('article-full');
  if(block){
    block.scrollIntoView({behavior:'smooth',block:'start'});
    setTimeout(function(){window.scrollBy(0,-140);},200);
  }
}
function _applyArticleENMode(){
  var full=document.getElementById('article-full');
  var btn=document.getElementById('article-en-toggle');
  var hide=(sessionStorage.getItem('article_en_hide')||'')==='1';
  if(full) full.classList.toggle('en-hidden', hide);
  if(btn) btn.textContent=hide?'🌐 英文批注：展开':'🌐 英文批注：显示';
}