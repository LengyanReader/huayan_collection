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

  // ── 会众全景流程图（MiaoyanFlow；简明结构流程图；置于目录之后、全文之前）──
  if((typeof renderMiaoyanFlow==='function')&&(typeof ARTICLE_ASSEMBLY!=='undefined')&&ARTICLE_ASSEMBLY&&(ARTICLE_ASSEMBLY.classes||[]).length){
    h+='<div class="section" data-chrome="1" id="article-flow" style="border-left:4px solid var(--gold)"></div>';
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
  // 会众名号数据剖面：仅当 build.py 内嵌了 ARTICLE_EDA（SQLite 中有本文 EDA 表）时出现
  if((typeof ARTICLE_EDA!=='undefined')&&ARTICLE_EDA&&ARTICLE_EDA.payload){
    var _m=ARTICLE_EDA.metrics||{};
    h+='<button class="f-nav-btn" onclick="edaGo()" title="查看会众名号的词素切分、语义域、群组剖面与共现网络">🔬 会众名号剖面（'+(_m.tokens_total||0)+' 词素位／'+(_m.distinct_tokens||0)+' 词素）</button>';
  }
  // 数据科学层：仅当 build.py 内嵌 ARTICLE_BI（本文有 miaoyan_bi.yaml 分析）时出现
  if((typeof ARTICLE_BI!=='undefined')&&ARTICLE_BI&&(typeof renderArticleBI==='function')){
    var _b=(ARTICLE_BI.scorecard&&ARTICLE_BI.scorecard.items)||[];
    h+='<button class="f-nav-btn" onclick="biGo()" title="跳至数据科学分析层：漏斗、语义域、交叉表、相似度、聚类、PCA、网络与稳健性">📊 数据科学（'+_b.length+' 项）</button>';
  }
  // 叙事动画：仅当 build.py 内嵌了 MIAOYAN_NARR 时出现
  if((typeof MIAOYAN_NARR!=='undefined')&&MIAOYAN_NARR&&(MIAOYAN_NARR.beats||[]).length){
    var _nb=(MIAOYAN_NARR.beats||[]).length;
    h+='<button class="f-nav-btn" onclick="narrGo()" title="跳至叙事动画：'+_nb+' 拍会众曼荼罗次第涌现">📽 叙事动画（'+_nb+' 拍）</button>';
  }
  // 会众全景流程：仅当 build.py 内嵌了 ARTICLE_ASSEMBLY 且已加载 renderMiaoyanFlow 时出现
  if((typeof renderMiaoyanFlow==='function')&&(typeof ARTICLE_ASSEMBLY!=='undefined')&&ARTICLE_ASSEMBLY&&(ARTICLE_ASSEMBLY.classes||[]).length){
    var _afc=(ARTICLE_ASSEMBLY.classes||[]),_afn=0;_afc.forEach(function(c){_afn+=(c.members||[]).length;});
    h+='<button class="f-nav-btn" onclick="flowGo()" title="跳至会众全景流程图：依经文列次四十类五环之结构流程图">🗺️ 全景流程（'+_afc.length+' 类／'+_afn+' 名）</button>';
  }
  h+='<button id="article-en-toggle" class="f-nav-btn" onclick="toggleArticleEN()" title="在「含英文批注」与「仅中文正文」之间切换显示">🌐 英文批注：显示</button>';
  h+='</span></h2>';
  h+=embed.html;
  h+='</div>';

  // ── 会众名号数据剖面（EDA；仅当 build.py 内嵌 ARTICLE_EDA 时出现，由 common.js renderArticleEDA 填充）──
  // 交互面板一律纳入默认折叠壳（panel-fold），点开方显；内容渲染入壳内 #article-eda-inner。
  if((typeof ARTICLE_EDA!=='undefined')&&ARTICLE_EDA&&ARTICLE_EDA.payload){
    h+='<div class="section" data-chrome="1" id="article-eda" style="border-left:4px solid var(--gold);padding:0">';
    h+=(typeof _foldShellHtml==='function')?_foldShellHtml('article-eda-inner','🔬 会众名号 · 数据剖面（交互）'):'';
    h+='</div>';
  }

  // ── 相关艺术品 · 文物 · 壁画 · 考古（renderArticleArtifacts 自带 <details> 折叠，无需再包）──
  if((typeof ARTICLE_ARTIFACTS!=='undefined')&&ARTICLE_ARTIFACTS&&(ARTICLE_ARTIFACTS.items||[]).length){
    h+='<div class="section" data-chrome="1" id="article-artifacts" style="border-left:4px solid var(--gold)"></div>';
  }

  // ── 数据科学层（miaoyan_bi.yaml 解释层；置于页脚之前）──
  // 面板自带 h2，恒展开会成附录十一后之独立一节；今包进折叠壳，内容渲染入 #bi-report-inner。
  if(typeof renderArticleBI==='function'){
    try{
      var _biHtml=renderArticleBI();
      if(_biHtml){
        h+='<div class="section" data-chrome="1" style="border-left:4px solid var(--gold);padding:0">';
        h+=(typeof _foldShellHtml==='function')?_foldShellHtml('bi-report-inner','📊 数据科学（解释·交互）'):_biHtml;
        h+='</div>';
      }
    }catch(e){}
  }

  // ── 叙事动画（miaoyan_narrative.yaml 叙事节拍；仅当内嵌 MIAOYAN_NARR 时出现）──
  // 内容渲染入壳内 #article-narrative-inner。
  if((typeof MIAOYAN_NARR!=='undefined')&&MIAOYAN_NARR&&(MIAOYAN_NARR.beats||[]).length){
    h+='<div class="section" data-chrome="1" id="article-narrative" style="border-left:4px solid var(--gold);padding:0">';
    h+=(typeof _foldShellHtml==='function')?_foldShellHtml('article-narrative-inner','📽 叙事动画（会众次第涌现·交互）'):'';
    h+='</div>';
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
  // ── 正文配图收为缩略图，点击看原图 ──
  if(typeof initDocImages==='function' && document.getElementById('article-full')){
    initDocImages('#article-full');
  }
  // ── 相关艺术品/文物/壁画/考古（默认折叠）──
  if(typeof renderArticleArtifacts==='function' && document.getElementById('article-artifacts')){
    renderArticleArtifacts('#article-artifacts');
  }
  // ── 会众名号数据剖面（EDA）：渲染入折叠壳内 ──
  if(typeof renderArticleEDA==='function' && document.getElementById('article-eda-inner')){
    renderArticleEDA('#article-eda-inner');
  }

  // ── 会众全景流程图（MiaoyanFlow；简明结构流程图）──
  if(typeof renderMiaoyanFlow==='function' && document.getElementById('article-flow')){
    try{ renderMiaoyanFlow('#article-flow'); }catch(e){ console.warn('flow', e); }
  }

  // ── 叙事动画播放器（MiaoyanNarrative）：渲染入折叠壳内 ──
  if(typeof renderMiaoyanNarrative==='function' && document.getElementById('article-narrative-inner')){
    try{ renderMiaoyanNarrative('#article-narrative-inner'); }catch(e){ console.warn('narrative', e); }
  }

  // ── 阅读模式：识别「英文/术语批注」块，支持仅中文正文切换 ──
  _initArticleENMode();

  // ── 章节级折叠：h2/h3/h4/h5 分级折叠（默认全部折叠；标题 ▾ 号点击可单独收展）──
  // 依站点设置：正文（含附录）所有标题层次默认折叠。
  // 惟 EDA/数据科学/叙事动画 三面板已各自纳入 <details class="panel-fold"> 折叠壳，
  // 若再施 _foldDoc 便会「壳折叠＋内层节折叠」双重套叠，点开壳仍见其内复折——故此处不再对
  // 该三者施折叠；仅正文 #article-full 与页首会众流程 #article-flow 仍按 h2–h5 分级折叠。
  // 各节工具栏一概不生成（noBar），改由页首「一套」页面级控件统管全页折叠/展开。
  if(typeof _foldDoc==='function'){
    try{ _foldDoc('#article-full', {noBar:true}); }catch(e){}
    try{ _foldDoc('#article-flow .miaoyan-flow', {label:'会众全景流程', noBar:true}); }catch(e){}
  }
  // ── 页面级统一控件：整页仅此一对「全部折叠／全部展开」，兼管章节折叠与 <details>（表·图）──
  if(typeof _installPageBar==='function'){
    try{ _installPageBar({mountSel:'#article-full', rootSel:'#article-root'}); }catch(e){}
  }

  // ── 支持 #锚点 直达（目录跳转用真实 id 锚点；先展开折叠祖先节）──
  if(location.hash){
    setTimeout(function(){
      var el=document.getElementById(location.hash.slice(1));
      if(el){
        if(typeof _reveal==='function')window._reveal(el);
        el.scrollIntoView({behavior:'smooth',block:'start'});
      }
    },80);
  }
}

if(document.readyState!=='loading'){renderArticle();}
else{document.addEventListener('DOMContentLoaded',renderArticle);}

// 会众名号数据剖面：自页头按钮跳至该节。三面板（EDA/数据科学/叙事）现默认折叠，
// 故须经 _scrollReveal 先展开其折叠壳再滚动，否则滚至一处空白折叠条。
function edaGo(){
  if(typeof _scrollReveal==='function' && _scrollReveal('article-eda')) return;
  var el=document.getElementById('article-eda'); if(el) el.scrollIntoView({behavior:'smooth',block:'start'});
}
function biGo(){ // scroll to data-science layer
  if(typeof _scrollReveal==='function' && _scrollReveal('bi-report')){ if(history.replaceState) history.replaceState(null,'','#bi-report'); return; }
  var el=document.getElementById('bi-report');
  if(!el)return;
  el.scrollIntoView({behavior:'smooth',block:'start'});
  if(history.replaceState) history.replaceState(null,'','#bi-report');
}

function narrGo(){ // scroll to narrative animation
  if(typeof _scrollReveal==='function' && _scrollReveal('article-narrative')){ if(history.replaceState) history.replaceState(null,'','#article-narrative'); return; }
  var el=document.getElementById('article-narrative');
  if(!el)return;
  el.scrollIntoView({behavior:'smooth',block:'start'});
  if(history.replaceState) history.replaceState(null,'','#article-narrative');
}

function flowGo(){ // scroll to assembly panorama flow diagram
  var el=document.getElementById('article-flow');
  if(!el)return;
  el.scrollIntoView({behavior:'smooth',block:'start'});
  if(history.replaceState) history.replaceState(null,'','#article-flow');
}

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
}/* ============================================================================
 * renderArticleBI —— 世主妙严品数据科学层渲染
 *
 * 守「严禁假信息」四条：
 *  1. 一切数字与文字皆来自注入的 ARTICLE_BI（源自 data/translation/miaoyan_bi.yaml），
 *     前端零硬编码数值；无数据即不渲染该节，绝不补空猜测。
 *  2. 方法（method）、口径（note）、限制（caveat）与网络截断（truncation）原样呈现，
 *     不得省略改写——省了限制，结论就会被误读为「经文事实」。
 *  3. 三层不得混同：经文事实(assembly) → 编辑析构(EDA) → 解释判断(数据科学层)。
 *     故本层各节标题皆标 [数据科学]，且 scorecard 刻意不给综合总分。
 *  4. 图表仅绘制既有矩阵，不外推、不插值、不跨轴比较（归一后尤忌）。
 * ==========================================================================*/
function renderArticleBI(){
  var bi = (typeof ARTICLE_BI !== 'undefined') ? ARTICLE_BI : null;
  if(!bi) return '';

  /* ---------- 小工具 ---------- */
  function esc(t){return String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
  function md(t){return esc(t).replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>');}
  function zhEn(zh,en){var s='';if(zh)s+='<div>'+md(zh)+'</div>';if(en)s+='<div class="en-line" style="color:var(--text2)">📖 '+md(en)+'</div>';return s;}
  function num(v,d){
    if(v===null||v===undefined||v==='')return '—';
    var x=Number(v); if(!isFinite(x))return '—';
    if(Math.abs(x)>=10000)return x.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g,',');
    if(Number.isInteger(x))return String(x);
    return x.toFixed(d===undefined?4:d).replace(/0+$/,'').replace(/\.$/,'');
  }
  function pct(v,d){return (v===null||v===undefined)?'—':(num(v*100,d===undefined?2:d)+'%');}
  function tbl(head,rows){
    var s='<table class="bi-tbl">';
    if(head)s+='<tr>'+head.map(function(x){return '<th>'+esc(x)+'</th>';}).join('')+'</tr>';
    rows.forEach(function(r){s+='<tr>'+r.map(function(c){return '<td>'+(c==null?'':c)+'</td>';}).join('')+'</tr>';});
    return s+'</table>';
  }
  function kv(k,v){return tbl(null,[[esc(k),'<span style="text-align:right;font-family:var(--mono,monospace)">'+v+'</span>']]);}
  function note(zh,en){return '<div class="bi-note">'+zhEn(zh,en)+'</div>';}
  function caveat(zh,en){
    if(!zh&&!en)return '';
    return '<div class="bi-caveat">⚠️ '+zhEn(zh,en)+'</div>';
  }
  /* 分节：折叠门，首节默认展开 */
  var secState={};
  function sec(id,icon,title,titleEn,body,openByDefault){
    var open = secState[id]!==undefined ? secState[id] : !!openByDefault;
    return '<div class="wu-door'+(open?' open':'')+'" id="'+id+'" onclick="this.classList.toggle(\'open\')">'
      +'<span class="arrow">▶</span><span class="ttl">'+icon+' '+esc(title)+'</span>'
      +(titleEn?'<div class="en-line" style="font-size:0.62em;color:var(--text2);margin-left:18px;margin-bottom:4px">📖 '+esc(titleEn)+'</div>':'')
      +'<div class="body">'+body+'</div></div>';
  }

  var h='';
  h+='<section id="bi-report">';
  h+='<h2>📊 数据科学</h2>';
  h+='<div class="en-line" style="font-size:0.66em;color:var(--text2);margin:-6px 0 10px">📖 Data Science</div>';

  /* ---------- 0. 分层声明与总则 ---------- */
  var head='';
  if(bi.disclaimer&&(bi.disclaimer.zh||bi.disclaimer.en)) head+=note(bi.disclaimer.zh,bi.disclaimer.en);
  var m=bi.method||{};
  if(m.pipeline_zh)    head+='<div class="bi-li"><b>三层分源</b>：'+zhEn(m.pipeline_zh,m.pipeline_en)+'</div>';
  if(m.determinism_zh) head+='<div class="bi-li"><b>可复现</b>：'+zhEn(m.determinism_zh,m.determinism_en)+'</div>';
  if(m.deps_zh)        head+='<div class="bi-li"><b>零新增依赖</b>：'+zhEn(m.deps_zh,m.deps_en)+'</div>';
  if(m.integrity_zh)   head+='<div class="bi-li"><b>不改动 EDA</b>：'+zhEn(m.integrity_zh,m.integrity_en)+'</div>';
  h+=sec('bi-method','🔬','读法总则（分层 · 可复现 · 不改动上游）','How to Read This Report (Layers · Reproducibility)',head,true);

  /* ---------- 1. 网络截断声明（置于一切中心性结论之前）---------- */
  var nw=bi.network||{};
  var tr=nw.truncation;
  if(tr){
    var tb='';
    tb+='<div class="bi-caveat bi-caveat-warn">🔻 '+zhEn(tr.zh,tr.en)+'</div>';
    tb+=tbl(['共现对之计量','数值'],[
      ['全部相邻共现对',num(tr.n_all_pairs)],
      ['实际入网之边（权重最高前 N）',num(tr.n_used_edges)],
      ['被截断之对',num(tr.n_dropped_pairs)],
      ['截断比例',pct(tr.dropped_pct,2)]
    ]);
    if(tr.pair_counting_zh) tb+=note(tr.pair_counting_zh,tr.pair_counting_en);
    h+=sec('bi-truncation','🔻','网络截断声明（中心性之适用范围）','Network Truncation: Scope of Centrality Claims',tb,true);
  }

  /* ---------- 2. 记分卡 ---------- */
  var sc=bi.scorecard;
  if(sc&&sc.items&&sc.items.length){
    var b='';
    b+=note(sc.note,sc.note_en);
    b+='<div class="bi-kpis">';
    sc.items.forEach(function(it){
      b+='<div class="bi-kpi"><div class="bi-kpi-v">'+esc(it.display!==undefined?it.display:num(it.value))+'</div>'
        +'<div class="bi-kpi-k">'+esc(it.zh)+'</div>'
        +(it.definition?'<div class="bi-kpi-d">'+esc(it.definition)+'</div>':'')
        +(it.en?'<div class="en-line bi-kpi-d">📖 '+esc(it.en)+'</div>':'')+'</div>';
    });
    b+='</div>';
    h+=sec('bi-scorecard','🪧','记分卡（分项列示 · 刻意不给综合总分）','Scorecard (Components Only — No Composite Score)',b,true);
  }

  /* ---------- 3. 漏斗（两轨不可连读）---------- */
  var fn=bi.funnel;
  if(fn){
    var b=note(fn.note,fn.note_en);
    function track(title,zh,en){
      var s='<h4>'+esc(zh)+(en?'<span class="en-line" style="font-size:0.7em;color:var(--text2)"> 📖 '+esc(en)+'</span>':'')+'</h4>';
      var st=zh&&zh.stages||[];
      var mx=0; st.forEach(function(x){if(Number(x.n)>mx)mx=Number(x.n);});
      st.forEach(function(x){
        var w=mx?Number(x.n)/mx*100:0;
        s+='<div class="bi-stage"><div class="bi-stage-h">'
          +'<span class="bi-stage-zh">'+esc(x.zh)+'</span>'
          +'<span class="bi-stage-n">'+num(x.n)+'　<span style="color:var(--text2)">'+pct(x.pct_of_track,1)+'</span></span></div>'
          +'<div class="bi-bar"><span style="width:'+w.toFixed(1)+'%"></span></div>'
          +(x.definition?'<div class="bi-stage-d">'+esc(x.definition)+(x.en?'<div class="en-line">📖 '+esc(x.en)+'</div>':'')+'</div>':'')
          +'</div>';
      });
      return s;
    }
    if(fn.track_names)  b+=track('names',fn.track_names.zh,fn.track_names.en);
    if(fn.track_tokens) b+=track('tokens',fn.track_tokens.zh,fn.track_tokens.en);
    if(fn.conversion){
      b+='<table class="bi-tbl" style="margin-top:8px"><tr><th>换算</th><th>值</th></tr>'
        +'<tr><td>每名平均析为几位词素</td><td style="text-align:right">'+num(fn.conversion.tokens_per_name,4)+'</td></tr>'
        +'<tr><td>无核名（记 ∅）</td><td style="text-align:right">'+num(fn.conversion.no_core)+'</td></tr></table>';
    }
    var g=fn.grades||{};
    if(Object.keys(g).length){
      var grows=[];
      ['high','medium','low'].forEach(function(k){
        var x=g[k]; if(!x)return;
        grows.push([esc(k),num(x.n),pct(x.pct,2),esc(x.zh)+(x.duty?'<div style="font-size:0.85em;color:var(--text2)">'+esc(x.duty)+'</div>':'')
          +(x.en?'<div class="en-line" style="font-size:0.9em;color:var(--text2)">📖 '+esc(x.en)+(x.duty_en?' · '+esc(x.duty_en):'')+'</div>':'')]);
      });
      b+=tbl(['判读等级','词素位','占比','说明 · 义务'],grows);
    }
    if(fn.reconciliation){
      b+=note(fn.reconciliation.zh,fn.reconciliation.en);
      b+=caveat(fn.reconciliation.caveat_zh,fn.reconciliation.caveat_en);
    }
    h+=sec('bi-funnel','📉','转换漏斗（一名析为多位 · 属扩张非流失）','Conversion Funnel (Expansion, Not Attrition)',b,false);
  }

  /* ---------- 4. 语义域景观 ---------- */
  var dl=bi.domain_landscape;
  if(dl&&dl.rows&&dl.rows.length){
    var b=note(dl.note,dl.note_en);
    var mx=0; dl.rows.forEach(function(r){if(Number(r.n)>mx)mx=Number(r.n);});
    var rows=dl.rows.map(function(r){
      var w=mx?Number(r.n)/mx*100:0;
      return [ '<span style="display:inline-block;width:9px;height:9px;border-radius:2px;background:'+esc(r.color||'var(--gold)')+';margin-right:5px"></span>'+esc(r.zh||r.key),
        String(r.rank),num(r.n),pct(r.pct,2),pct(r.cum_pct,2),
        '<div class="bi-bar" style="min-width:70px"><span style="width:'+w.toFixed(1)+'%;background:'+esc(r.color||'var(--gold)')+'"></span></div>' ];
    });
    b+=tbl(['语义域','#','词素位','占比','累计','分布'],rows);
    var c=dl.concentration||{};
    if(c.hhi!==undefined){
      b+=tbl(['集中度量','值','读法'],[
        ['HHI（Σp²）',num(c.hhi,6),c.hhi_note+(c.hhi_note_en?'<div class="en-line" style="font-size:0.9em;color:var(--text2)">📖 '+esc(c.hhi_note_en)+'</div>':'')],
        ['归一化熵',num(c.normalized_entropy,4),'0＝全聚于一项，1＝完全均布'],
        ['有效域数 e^H',num(c.effective_domains,3),c.effective_note+(c.effective_note_en?'<div class="en-line" style="font-size:0.9em;color:var(--text2)">📖 '+esc(c.effective_note_en)+'</div>':'')]
      ]);
    }
    h+=sec('bi-domain','🧭','语义域景观（构词层面貌 · 非教义权重）','Semantic-Domain Landscape (Morphemic Surface, Not Doctrinal Weight)',b,false);
  }

  /* ---------- 5. 群组 × 域 交叉表 ---------- */
  var ct=bi.crosstab;
  if(ct&&ct.matrix&&ct.groups&&ct.domains){
    var b=note(ct.note,ct.note_en);
    /* 行为语义域(17)，列为群组(5) */
    var G=ct.groups,D=ct.domains;
    var CW=Math.max(52,Math.min(74,Math.floor(820/Math.max(1,G.length))));
    var LW=Math.max(92,Math.min(150,Math.floor(260/Math.max(1,D.length))*3));
    var W=LW+G.length*CW+16, H=D.length*19+40;
    var mx=0; ct.matrix.forEach(function(r){r.forEach(function(v){if(Number(v)>mx)mx=Number(v);});});
    var svg='<svg viewBox="0 0 '+W+' '+H+'" style="width:100%;min-width:'+Math.min(W,900)+'px;height:auto" role="img" aria-label="group by domain heatmap">';
    svg+='<text x="4" y="12" font-size="10" fill="currentColor">域 ＼ 群</text>';
    G.forEach(function(g,j){
      var cx=LW+j*CW+CW/2;
      svg+='<text x="'+cx+'" y="12" font-size="9.5" fill="currentColor" text-anchor="end" transform="rotate(-42 '+cx+' 12)">'+esc(g.zh)+'</text>';
    });
    D.forEach(function(dm,i){
      var y=22+i*19;
      svg+='<text x="'+(LW-6)+'" y="'+(y+12)+'" font-size="9.5" text-anchor="end" fill="currentColor">'+esc(dm.zh||dm.key)+'</text>';
      for(var j=0;j<G.length;j++){
        var v=Number(ct.matrix[i][j]||0), t=mx?v/mx:0;
        svg+='<rect x="'+(LW+j*CW)+'" y="'+y+'" width="'+(CW-2)+'" height="17" fill="var(--gold)" opacity="'+(0.05+0.62*t).toFixed(3)+'"><title>'+esc(dm.zh)+' / '+esc(G[j].zh)+': '+v+'</title></rect>';
        if(v>0) svg+='<text x="'+(LW+j*CW+CW/2-1)+'" y="'+(y+12)+'" font-size="9" text-anchor="middle" fill="'+(t>0.55?'#1a1410':'currentColor')+'">'+v+'</text>';
      }
    });
    svg+='</svg>';
    b+='<div style="overflow-x:auto">'+svg+'</div>';
    if(ct.chi2!==undefined){
      b+=tbl(['统计量','值'],[
        ['χ²',num(ct.chi2,4)],
        ['自由度 df',num(ct.df)],
        ['Cramér’s V',num(ct.cramers_v,4)],
        ['p 值',esc(ct.p_approx_txt||num(ct.p_approx))+(ct.p_approx_txt_en?'<div class="en-line" style="font-size:0.9em;color:var(--text2)">📖 '+esc(ct.p_approx_txt_en)+'</div>':'')],
        ['Wilson–Hilferty z',num(ct.p_wh_z,4)]
      ]);
    }
    if(ct.df_note_zh)    b+=note(ct.df_note_zh,ct.df_note_en);
    if(ct.v_strength_zh) b+=note(ct.v_strength_zh,ct.v_strength_en);
    if(ct.p_note)        b+=note(ct.p_note,ct.p_note_en);
    function liftTable(title,arr,color){
      if(!arr||!arr.length)return '';
      var s='<h4>'+esc(title)+'</h4>';
      s+=tbl(['语义域','群组','观测','期望','lift'],arr.slice(0,12).map(function(r){
        var hi=Number(r.lift)>1;
        return [esc(r.domain_zh),esc(r.group_zh),num(r.obs),num(r.exp,2),
          '<b style="color:'+(hi?'var(--gold)':'var(--text2)')+'">'+num(r.lift,3)+'</b>'];
      }));
      return s;
    }
    b+=liftTable('偏好此域之组合（lift > 1）· 前 12',ct.top_over);
    b+=liftTable('回避此域之组合（lift < 1）· 前 12',ct.top_under);
    h+=sec('bi-crosstab','🧮','群组 × 语义域 交叉表与独立性检验','Group × Domain Crosstab & Test of Independence',b,false);
  }

  /* ---------- 6. 相似度 ---------- */
  var sm=bi.similarity;
  if(sm){
    var b=note((sm.space_zh||'')+'<br>'+(sm.caveat_zh||''),'');
    if(sm.space_en) b+='<div class="en-line" style="color:var(--text2);font-size:0.9em">📖 '+esc(sm.space_en)+(sm.caveat_en?'<br>'+esc(sm.caveat_en):'')+'</div>';
    if(sm.matrix&&sm.names&&sm.names.length){
      var N=Math.min(sm.names.length,30);
      var SZ=Math.max(360,Math.min(600,N*17));
      var cell=SZ/N, LW2=Math.max(70,Math.min(130,SZ*0.22));
      var W2=LW2+SZ+8, H2=22+SZ+8;
      var mx3=0; for(var i=0;i<N;i++)for(var j=0;j<N;j++){var vv=Number(sm.matrix[i][j]||0);if(vv>mx3)mx3=vv;}
      var svg2='<svg viewBox="0 0 '+W2+' '+H2+'" style="width:100%;max-width:780px;height:auto" role="img" aria-label="similarity heatmap">';
      for(var i=0;i<N;i++)for(var j=0;j<N;j++){
        var v=Number(sm.matrix[i][j]||0), t=mx3?v/mx3:0;
        svg2+='<rect x="'+(LW2+j*cell)+'" y="'+(22+i*cell)+'" width="'+Math.max(1,cell-1)+'" height="'+Math.max(1,cell-1)+'" fill="var(--gold)" opacity="'+(0.05+0.6*t).toFixed(3)+'"><title>'+esc(sm.names[i])+' ↔ '+esc(sm.names[j])+': '+num(v,4)+'</title></rect>';
      }
      for(var i=0;i<N;i++){
        svg2+='<text x="'+(LW2-4)+'" y="'+(28+i*cell)+'" font-size="8.5" text-anchor="end" fill="currentColor">'+esc(sm.names[i])+'</text>';
        svg2+='<text x="'+(LW2+i*cell+2)+'" y="17" font-size="8.5" fill="currentColor" transform="rotate(-60 '+(LW2+i*cell+2)+' 17)">'+esc(sm.names[i])+'</text>';
      }
      svg2+='</svg>';
      b+='<div style="overflow-x:auto">'+svg2+'</div>';
      b+='<div style="font-size:0.74em;color:var(--text2);margin-top:4px">'+N+' / '+sm.names.length+' 类（按相似度矩阵前 '+N+' 类绘制；完整 40×40 见 YAML）</div>';
    }
    if(sm.within_mean!==undefined){
      b+=tbl(['平均相似度','值','n'],[
        ['同群组内',num(sm.within_mean,4),num(sm.within_n)],
        ['跨群组',num(sm.across_mean,4),num(sm.across_n)]
      ]);
    }
    if(sm.verdict_zh) b+=note(sm.verdict_zh,sm.verdict_en);
    var cf=sm.confound;
    if(cf){
      if(cf.adj_same_template_mean!==undefined){
        b+=tbl(['去混淆（同为类尾同字者 vs 不同）','值'],[
          ['相邻且同类尾',num(cf.adj_same_template_mean,4)],
          ['相邻但类尾不同',num(cf.adj_diff_template_mean,4)],
          ['差（同−异）',num(cf.same_minus_diff,4)]
        ]);
      }
      if(cf.tail_of_class) b+=note('类尾（模板代理）为：'+(cf.tail_of_class||[]).slice(0,12).map(function(t){return esc(t.cat)+'→'+esc(t.tail);}).join('、')+' …（共 '+(cf.tail_of_class||[]).length+' 类）','');
    }
    h+=sec('bi-sim','🔗','类间相似度（构词层语汇 · 非词义向量）','Inter-Class Similarity (Lexical Composition, Not Semantic Embedding)',b,false);
  }

  /* ---------- 7. 聚类 ---------- */
  var cl=bi.clustering;
  if(cl){
    var b='';
    b+=caveat(cl.caveat_zh,cl.caveat_en);
    if(cl.method_zh) b+=note(cl.method_zh,cl.method_en);
    if(cl.stability_method_zh) b+=note(cl.stability_method_zh,cl.stability_method_en);
    b+=tbl(['选定项','值'],[
      ['最佳簇数 k',num(cl.best_k)],
      ['平均轮廓系数',num(cl.best_silhouette,4)],
      ['扫描区间','k = '+(cl.k_range||[]).join(' … ')],
      ['共形相关系数',num(cl.cophenetic_corr,4)]
    ]);
    if(cl.k_boundary_note_zh) b+=note(cl.k_boundary_note_zh,cl.k_boundary_note_en);
    if(cl.weak_structure_zh)   b+=note(cl.weak_structure_zh,cl.weak_structure_en);
    if(cl.cophenetic_note_zh)  b+=note(cl.cophenetic_note_zh,cl.cophenetic_note_en);
    /* k–轮廓曲线 */
    if(cl.curve&&cl.curve.length){
      var W4=560,H4=200,P4=38;
      var xs=cl.curve.map(function(c){return Number(c.k);});
      var ys=cl.curve.map(function(c){return Number(c.silhouette);});
      var x0=Math.min.apply(null,xs),x1=Math.max.apply(null,xs);
      var y0=Math.min.apply(null,ys),y1=Math.max.apply(null,ys);
      var sx=function(v){return P4+(x1===x0?0:(v-x0)/(x1-x0)*(W4-2*P4));};
      var sy=function(v){return H4-P4-(y1===y0?0:(v-y0)/(y1-y0)*(H4-2*P4));};
      var pts=cl.curve.map(function(c){return sx(Number(c.k)).toFixed(1)+','+sy(Number(c.silhouette)).toFixed(1);}).join(' ');
      var svg4='<svg viewBox="0 0 '+W4+' '+H4+'" style="width:100%;max-width:600px;height:auto" role="img" aria-label="silhouette curve">';
      svg4+='<line x1="'+P4+'" y1="'+(H4-P4)+'" x2="'+(W4-P4)+'" y2="'+(H4-P4)+'" stroke="currentColor" opacity="0.35"/>';
      svg4+='<polyline points="'+pts+'" fill="none" stroke="var(--gold)" stroke-width="1.6"/>';
      cl.curve.forEach(function(c){
        var bk=Number(c.k)===Number(cl.best_k);
        svg4+='<circle cx="'+sx(Number(c.k)).toFixed(1)+'" cy="'+sy(Number(c.silhouette)).toFixed(1)+'" r="'+(bk?4.5:2.4)+'" fill="'+(bk?'var(--gold)':'currentColor')+'" opacity="'+(bk?1:0.6)+'"><title>k='+c.k+': '+num(c.silhouette,4)+'</title></circle>';
        svg4+='<text x="'+sx(Number(c.k)).toFixed(1)+'" y="'+(H4-P4+12)+'" font-size="8.5" text-anchor="middle" fill="currentColor">'+c.k+'</text>';
      });
      svg4+='<text x="4" y="12" font-size="9.5" fill="currentColor">轮廓系数</text><text x="'+(W4-4)+'" y="'+(H4-6)+'" font-size="9.5" text-anchor="end" fill="currentColor">k</text>';
      svg4+='</svg>';
      b+='<div style="overflow-x:auto">'+svg4+'</div>';
    }
    /* 簇成员 */
    if(cl.clusters&&cl.clusters.length){
      var rows=cl.clusters.map(function(c,ci){
        var mem=c.members||[];
        var gmap={}; mem.forEach(function(m){gmap[m.group_zh||m.group]=(gmap[m.group_zh||m.group]||0)+1;});
        var memTxt=mem.map(function(m){return esc(m.cat);}).join('、');
        return ['C'+(ci+1),String(mem.length),
          mem.length?esc(Object.keys(gmap).map(function(k){return k+'×'+gmap[k];}).join('　')):'—',
          '<span style="font-size:0.86em">'+memTxt+'</span>'];
      });
      b+=tbl(['簇','规模','群组构成','成员类'],rows);
    }
    h+=sec('bi-cluster','🌿','聚类结构（探索性切分 · 非经文自有类别）','Cluster Structure (Exploratory Partition, Not Sutra-given)',b,false);
  }

  /* ---------- 8. PCA ---------- */
  var pc=bi.pca;
  if(pc){
    var b=caveat(pc.caveat_zh,pc.caveat_en);
    if(pc.method_zh) b+=note(pc.method_zh,pc.method_en);
    if(pc.explained&&pc.explained.length){
      var W5=560,H5=170,P5=36;
      var mx5=0; pc.explained.forEach(function(e){if(Number(e.pct)>mx5)mx5=Number(e.pct);});
      var svg5='<svg viewBox="0 0 '+W5+' '+H5+'" style="width:100%;max-width:600px;height:auto" role="img" aria-label="explained variance">';
      var bw=W5/(pc.explained.length*1.7);
      pc.explained.forEach(function(e,i){
        var v=Number(e.pct), hgt=mx5?v/mx5*(H5-2*P5):0;
        var x=P5+i*bw*1.7,y=H5-P5-hgt;
        svg5+='<rect x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+bw.toFixed(1)+'" height="'+hgt.toFixed(1)+'" fill="var(--gold)" opacity="0.75"><title>PC'+e.pc+': '+pct(v,2)+'</title></rect>';
        svg5+='<text x="'+(x+bw/2).toFixed(1)+'" y="'+(y-4).toFixed(1)+'" font-size="9" text-anchor="middle" fill="currentColor">'+pct(v,1)+'</text>';
        svg5+='<text x="'+(x+bw/2).toFixed(1)+'" y="'+(H5-P5+12)+'" font-size="9" text-anchor="middle" fill="currentColor">PC'+e.pc+'</text>';
      });
      svg5+='<line x1="'+P5+'" y1="'+(H5-P5)+'" x2="'+(W5-P5)+'" y2="'+(H5-P5)+'" stroke="currentColor" opacity="0.35"/>';
      svg5+='</svg>';
      b+='<div style="overflow-x:auto">'+svg5+'</div>';
    }
    if(pc.points&&pc.points.length){
      var xs=pc.points.map(function(p){return Number(p.x);});
      var ys=pc.points.map(function(p){return Number(p.y);});
      var xa=Math.min.apply(null,xs),xb=Math.max.apply(null,xs);
      var ya=Math.min.apply(null,ys),yb=Math.max.apply(null,ys);
      var W6=640,H6=440,P6=46;
      var sx=function(v){return P6+(xb===xa?0:(v-xa)/(xb-xa)*(W6-2*P6));};
      var sy=function(v){return H6-P6-(yb===ya?0:(v-ya)/(yb-ya)*(H6-2*P6));};
      var gc=pc.group_centroids||{};
      var gcol={}; var pal=['#b8863c','#5e8b9e','#8b5e8b','#6b8b3c','#a05e3c'];
      Object.keys(gc||{}).forEach(function(g,i){gcol[g]=pal[i%pal.length];});
      var svg6='<svg viewBox="0 0 '+W6+' '+H6+'" style="width:100%;max-width:660px;height:auto" role="img" aria-label="PCA scatter">';
      svg6+='<line x1="'+P6+'" y1="'+(H6-P6)+'" x2="'+(W6-P6)+'" y2="'+(H6-P6)+'" stroke="currentColor" opacity="0.35"/>';
      svg6+='<line x1="'+P6+'" y1="'+P6+'" x2="'+P6+'" y2="'+(H6-P6)+'" stroke="currentColor" opacity="0.35"/>';
      svg6+='<line x1="'+P6+'" y1="'+(sy(0).toFixed(1))+'" x2="'+(W6-P6)+'" y2="'+(sy(0).toFixed(1))+'" stroke="currentColor" opacity="0.16" stroke-dasharray="3 3"/>';
      svg6+='<line x1="'+sx(0).toFixed(1)+'" y1="'+P6+'" x2="'+sx(0).toFixed(1)+'" y2="'+(H6-P6)+'" stroke="currentColor" opacity="0.16" stroke-dasharray="3 3"/>';
      pc.points.forEach(function(p){
        var cx=sx(Number(p.x)),cy=sy(Number(p.y));
        var r=Math.max(3,Math.min(9,Math.sqrt(Number(p.n_named||1))*1.5));
        svg6+='<circle cx="'+cx.toFixed(1)+'" cy="'+cy.toFixed(1)+'" r="'+r.toFixed(1)+'" fill="'+(gcol[p.group]||'var(--gold)')+'" opacity="0.8"><title>'+esc(p.cat)+' ('+esc(p.group_zh)+'): n_named='+num(p.n_named)+'</title></circle>';
      });
      Object.keys(gc||{}).forEach(function(g){
        var c0=gc[g]; if(!c0)return;
        var cx=sx(Number(c0.x!==undefined?c0.x:c0.cx)),cy=sy(Number(c0.y!==undefined?c0.y:c0.cy));
        svg6+='<path d="M'+(cx-6)+','+cy+'L'+(cx+6)+','+cy+'M'+cx+','+(cy-6)+'L'+cx+','+(cy+6)+'" stroke="'+(gcol[g]||'currentColor')+'" stroke-width="1.8"/>';
      });
      svg6+='<text x="'+(W6/2)+'" y="'+(H6-8)+'" font-size="10" text-anchor="middle" fill="currentColor">PC1</text>';
      svg6+='<text x="12" y="'+(H6/2)+'" font-size="10" text-anchor="middle" fill="currentColor" transform="rotate(-90 12 '+(H6/2)+')">PC2</text>';
      svg6+='</svg>';
      b+='<div style="overflow-x:auto">'+svg6+'</div>';
      var leg='<div class="bi-legend">';
      Object.keys(gc||{}).forEach(function(g){
        leg+='<span class="bi-lg"><i style="background:'+(gcol[g]||'var(--gold)')+'"></i>'+esc((gc[g]&&(gc[g].zh||gc[g].group_zh))||g)+'</span>';
      });
      b+=leg+'</div>';
      b+='<div style="font-size:0.74em;color:var(--text2)">气泡大小＝该类名号数；十字＝群组重心（40 类逐类实点，未作任何外推）</div>';
    }
    h+=sec('bi-pca','📐','主成分分析（降维观察 · 投影有损）','PCA (Dimension Reduction; Projection Is Lossy)',b,false);
  }

  /* ---------- 9. 帕累托 ---------- */
  var pa=bi.pareto;
  if(pa&&pa.series&&pa.series.length){
    var b=note(pa.note_zh,pa.note_en);
    var rows=pa.series.map(function(s){
      return [esc(s.label)+(s.label_en?'<div class="en-line" style="font-size:0.9em;color:var(--text2)">📖 '+esc(s.label_en)+'</div>':''),
        num(s.total),num(s.n_items),num(s.k80),pct(s.k80_pct_items,2)];
    });
    b+=tbl(['量度','总频次','项数','k80','k80 占项数比'],rows);
    /* 首项累计曲线（取第一组之 points） */
    var s0=pa.series[0];
    if(s0&&s0.points&&s0.points.length){
      var pts=s0.points.slice(0,40);
      var W7=600,H7=220,P7=40;
      var xs7=pts.map(function(p){return Number(p.rank);});
      var ys7=pts.map(function(p){return Number(p.cum_pct);});
      var x7a=Math.min.apply(null,xs7),x7b=Math.max.apply(null,xs7);
      var y7a=Math.min.apply(null,ys7),y7b=Math.max.apply(null,ys7);
      var sx7=function(v){return P7+(x7b===x7a?0:(v-x7a)/(x7b-x7a)*(W7-2*P7));};
      var sy7=function(v){return H7-P7-(y7b===y7a?0:(v-y7a)/(y7b-y7a)*(H7-2*P7));};
      var svg7='<svg viewBox="0 0 '+W7+' '+H7+'" style="width:100%;max-width:640px;height:auto" role="img" aria-label="cumulative curve">';
      /* 80% 参考线 */
      var y80=sy7(0.8);
      svg7+='<line x1="'+P7+'" y1="'+y80.toFixed(1)+'" x2="'+(W7-P7)+'" y2="'+y80.toFixed(1)+'" stroke="var(--red)" stroke-width="1" stroke-dasharray="4 3" opacity="0.8"/>';
      svg7+='<text x="'+(W7-P7)+'" y="'+(y80-4).toFixed(1)+'" font-size="9" text-anchor="end" fill="var(--red)">80% 线</text>';
      svg7+='<line x1="'+P7+'" y1="'+(H7-P7)+'" x2="'+(W7-P7)+'" y2="'+(H7-P7)+'" stroke="currentColor" opacity="0.35"/>';
      svg7+='<polyline points="'+pts.map(function(p){return sx7(Number(p.rank)).toFixed(1)+','+sy7(Number(p.cum_pct)).toFixed(1);}).join(' ')+'" fill="none" stroke="var(--gold)" stroke-width="1.8"/>';
      pts.forEach(function(p){
        svg7+='<circle cx="'+sx7(Number(p.rank)).toFixed(1)+'" cy="'+sy7(Number(p.cum_pct)).toFixed(1)+'" r="2.2" fill="var(--gold)"><title>#'+p.rank+' '+esc(p.key)+' n='+num(p.n)+' 累计 '+pct(p.cum_pct,2)+'</title></circle>';
      });
      svg7+='<text x="4" y="12" font-size="9.5" fill="currentColor">'+esc(s0.label)+' · 累计占比（前 '+pts.length+' 项）</text>';
      svg7+='<text x="'+(W7/2)+'" y="'+(H7-6)+'" font-size="9.5" text-anchor="middle" fill="currentColor">位次 rank</text>';
      svg7+='</svg>';
      b+='<div style="overflow-x:auto">'+svg7+'</div>';
    }
    h+=sec('bi-pareto','📊','帕累托与集中度（语汇集中于少数词素）','Pareto & Concentration',b,false);
  }

  /* ---------- 10. 网络中心性（必置于截断声明之后）---------- */
  if(nw&&(nw.n_nodes!==undefined)){
    var b=note(nw.note_zh,nw.note_en);
    b+=caveat('本页以下中心性数值仅为**强共现子图**上之中心性，'+num(tr?tr.n_used_edges:0)+' 边（自全部 '+num(tr?tr.n_all_pairs:0)+' 对截断而来），**非全网之中心性**。','All centrality figures below are computed on the strong-co-occurrence subgraph, not on the full network.');
    b+=tbl(['网络规模','值'],[
      ['节点数（不同词素）',num(nw.n_nodes)],
      ['入网边数',num(nw.n_edges)],
      ['活跃节点（入网者）',num(nw.n_active)],
      ['孤立节点（零共现）',num(nw.isolated)]
    ]);
    if(nw.isolated_note_zh) b+=note(nw.isolated_note_zh,nw.isolated_note_en);
    if(nw.top_pagerank&&nw.top_pagerank.length){
      b+='<h4>PageRank（前 12）</h4>';
      b+=tbl(['词素','语义域','出现次数','PageRank','度'],[
        nw.top_pagerank.slice(0,12).map(function(r){
          return [esc(r.zh||r.id),esc(r.domain||''),num(r.n),num(r.pagerank,6),num(r.degree)];
        })
      ]);
    }
    if(nw.top_betweenness&&nw.top_betweenness.length){
      b+='<h4>介数中心性（前 10）</h4>';
      b+=tbl(['词素','语义域','介数'],[
        nw.top_betweenness.slice(0,10).map(function(r){
          return [esc(r.zh||r.id),esc(r.domain||''),num(r.betweenness!==undefined?r.betweenness:r.value,6)];
        })
      ]);
    }
    if(nw.communities&&nw.communities.length){
      b+='<h4>社群（'+(nw.communities||[]).length+' 个 · 覆盖 '+pct(nw.community_coverage,1)+'）</h4>';
      b+=tbl(['社群','规模','代表词素（前 8）'],[
        nw.communities.slice(0,12).map(function(c,i){
          var mem=c.members||[];
          return ['G'+(i+1),num(c.size!==undefined?c.size:mem.length),
            '<span style="font-size:0.86em">'+mem.slice(0,8).map(function(m){return esc(m.zh||m.id);}).join('、')+'</span>'];
        })
      ]);
    }
    if(nw.method_zh) b+=note(nw.method_zh,nw.method_en);
    h+=sec('bi-network','🕸️','词素共现网络中心性（限强共现子图）','Morpheme Co-occurrence Centrality (Strong Subgraph Only)',b,false);
  }

  /* ---------- 11. 序位置换检验 ---------- */
  var od=bi.ordinal;
  if(od){
    var b=note(od.note_zh,od.note_en);
    if(od.method_zh) b+=note(od.method_zh,od.method_en);
    b+=tbl(['观测量','值'],[
      ['相邻类平均相似度（观测）',num(od.adjacent_mean,4)],
      ['零分布均值（随机置换）',num(od.null_mean,4)],
      ['零分布标准差',num(od.null_sd,4)],
      ['z 值',num(od.z,4)],
      ['p 值（正态近似）',od.p===0?'< 1e-9':num(od.p,6)],
      ['全部两两平均相似度',num(od.all_pairs_mean,4)],
      ['同群组相邻对',num(od.same_group_adjacent,4)],
      ['跨群组相邻对',num(od.cross_group_adjacent,4)]
    ]);
    var cf2=od.confound;
    if(cf2&&cf2.adj_same_template_mean!==undefined){
      b+=tbl(['去混淆（模板代理＝类尾）','值'],[
        ['相邻且同类尾',num(cf2.adj_same_template_mean,4)],
        ['相邻但类尾不同',num(cf2.adj_diff_template_mean,4)],
        ['差（同−异）',num(cf2.same_minus_diff,4)]
      ]);
      b+=caveat('模板标签为**类首名末字之代理**（如「主城神」「主地神」皆以「神」为类尾），系分析层之代理变量，非经文所定之语义类。','Template labels are a proxy derived from the last character of each class name, not a sutra-given semantic class.');
    }
    if(od.segments&&od.segments.length){
      b+=tbl(['分段','类次范围','类数','段内相邻平均相似度'],[
        od.segments.map(function(s){
          return [esc(s.zh||s.group),(s.from_idx!==undefined?(s.from_idx+'–'+s.to_idx):'—'),num(s.n_classes),num(s.mean_sim_internal,4)];
        })
      ]);
    }
    if(od.conclusion_zh) b+='<div class="bi-find">'+zhEn(od.conclusion_zh,od.conclusion_en)+'</div>';
    h+=sec('bi-ordinal','🔢','序位结构检验（类次编排含语义梯度？）','Ordinal Structure Test: Is Sutra Order Semantic?',b,false);
  }

  /* ---------- 12. 质量与稳健性 ---------- */
  var q=bi.quality;
  if(q){
    var b=note(q.note_zh,q.note_en);
    if(q.grade_policy_zh) b+='<div class="bi-caveat">'+zhEn(q.grade_policy_zh,q.grade_policy_en)+'</div>';
    if(q.robustness&&q.robustness.length){
      var rows=q.robustness.map(function(r){
        return [esc(r.id||''),'<b>'+md(r.claim_zh||r.zh||'')+'</b>'+(r.claim_en?'<div class="en-line" style="font-size:0.9em;color:var(--text2)">📖 '+esc(r.claim_en||r.en)+'</div>':'')
          ,md(r.finding_zh||r.result_zh||r.result||'')+(r.finding_en||r.result_en?'<div class="en-line" style="font-size:0.9em;color:var(--text2)">📖 '+esc(r.finding_en||r.result_en)+'</div>':'')];
      });
      b+=tbl(['#','稳健性检验','结果'],rows);
    }
    if(q.worst_classes&&q.worst_classes.length){
      b+='<h4>判读存疑率最高之群</h4>';
      b+=tbl(['群组','判读存疑率'],[
        q.worst_classes.slice(0,8).map(function(r){
          return [esc(r.zh||r.key||r.group_zh),pct(r.rate!==undefined?r.rate:r.pct,2)];
        })
      ]);
    }
    if(q.outliers&&q.outliers.length){
      b+='<h4>离群类（语汇面貌与他类皆不相近）</h4>';
      b+=tbl(['类','群组','与他类平均相似度'],[
        q.outliers.map(function(r){return [esc(r.cat),esc(r.group_zh),num(r.mean_sim,4)];})
      ]);
      if(q.outlier_note_zh) b+=note(q.outlier_note_zh,q.outlier_note_en);
    }
    h+=sec('bi-quality','✅','数据质量与稳健性（度量分析自身之可信度）','Data Quality & Robustness (Reliability of This Analysis)',b,false);
  }

  /* ---------- 13. 结论摘要 ---------- */
  var ex=bi.executive;
  if(ex&&ex.findings&&ex.findings.length){
    var b=note(ex.note_zh,ex.note_en);
    b+='<ol class="bi-findings">';
    ex.findings.forEach(function(f){
      b+='<li>'+(f.id?'<b>'+esc(f.id)+'</b>　':'')+md(f.zh||f.text_zh||'')
        +(f.en||f.text_en?'<div class="en-line" style="color:var(--text2);font-size:0.94em">📖 '+md(f.en||f.text_en)+'</div>':'')
        +(f.evidence?'<div style="font-size:0.78em;color:var(--text2);margin-top:2px">🔎 证据：'+esc(f.evidence)+'</div>':'')+'</li>';
    });
    b+='</ol>';
    h+=sec('bi-exec','📌','分析结论（解释层 · 非经文）','Findings (Interpretive Layer, Not Sutra Text)',b,false);
  }

  h+='</section>';
  return h;
}
