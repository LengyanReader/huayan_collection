// ═══ FRONTIER TAB ═══
// Renders from FRONTIER_DATA (YAML-loaded) with fallback to hardcoded content

function _escFrontier(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function _mdFrontier(s){return _escFrontier(s).replace(/\n/g,'<br>');}

function _renderDomain(d){
  var h='<div class=f-card>';
  h+='<h3>'+(d.icon||'')+' '+_escFrontier(d.domain)+'</h3>';
  // core issues
  if(d.core_issues && d.core_issues.length){
    h+='<p><b>核心议题:</b> '+d.core_issues.map(function(c){return _escFrontier(c);}).join('、')+'</p>';
  }
  // main perspective (huayan_perspective or key_findings)
  var persp = d.huayan_perspective || d.key_findings;
  if(persp){
    var label = d.key_findings ? '⚡ 关键发现' : '⚡ 华严视角';
    h+='<div class=stage-box><b>'+label+'</b><br>'+_mdFrontier(persp)+'</div>';
  }
  // related people
  if(d.related && d.related.length){
    h+='<div class=stage-box><b>📎 相关研究与人物</b><br>';
    d.related.forEach(function(r){
      h+='<b>'+_escFrontier(r.name)+'</b>';
      if(r.affiliation) h+=' ('+_escFrontier(r.affiliation)+')';
      h+=': '+_escFrontier(r.description)+'<br>';
    });
    h+='</div>';
  }
  // sources
  if(d.sources && d.sources.length){
    h+='<div class=stage-box style="font-size:0.78em"><b>📚 文献出处</b><br>';
    d.sources.forEach(function(s){h+=_escFrontier(s)+'<br>';});
    h+='</div>';
  }
  h+='</div>';
  return h;
}

function _renderSection(key, sec){
  var h='<div id=fv-'+key+(key==='huayan'?'':' style=display:none')+'>';
  h+='<div class=section style=border-left:4px solid var(--gold)>';
  h+='<h2>'+_escFrontier(sec.title)+'</h2>';
  if(sec.intro) h+='<p style=line-height:1.8>'+_mdFrontier(sec.intro)+'</p>';
  h+='</div>';
  if(sec.domains){
    sec.domains.forEach(function(d){
      var card=_renderDomain(d);
      if(d.id) card='<div id=fv-'+key+'-'+d.id+'>'+card+'</div>';
      h+=card;
    });
  }
  h+='</div>';
  return h;
}

function _renderLitReview(lr){
  var h='<div id=fv-litreview style=display:none>';
  h+='<div class=section style=border-left:4px solid var(--gold)>';
  h+='<h2>📑 多语言文献综述 (2023-2026)</h2>';
  if(lr.intro) h+='<p style="font-size:0.78em;color:var(--text2);margin-bottom:8px">'+_mdFrontier(lr.intro)+'</p>';
  h+='</div>';
  // trends
  if(lr.trends && lr.trends.length){
    h+='<div class=section><h2>📈 研究趋势</h2>';
    lr.trends.forEach(function(t){
      h+='<div class=stage-box><b>'+_escFrontier(t.title)+'</b><br>'+_escFrontier(t.description)+'</div>';
    });
    h+='</div>';
  }
  // critical assessment
  if(lr.critical_assessment && lr.critical_assessment.length){
    h+='<div class=section><h2>🔍 批判性评估</h2>';
    lr.critical_assessment.forEach(function(c){
      h+='<div class=stage-box><b>'+_escFrontier(c.title)+'</b><br>'+_escFrontier(c.description)+'</div>';
    });
    h+='</div>';
  }
  // papers by year
  var years = lr.papers_by_year ? Object.keys(lr.papers_by_year).sort().reverse() : [];
  years.forEach(function(y){
    var papers = lr.papers_by_year[y];
    if(!papers || !papers.length) return;
    h+='<h3 style=color:var(--gold);font-size:0.9em>'+_escFrontier(y)+'</h3>';
    h+='<div class=stage-box>';
    papers.forEach(function(p){h+=_escFrontier(p)+'<br>';});
    h+='</div>';
  });
  // disclaimer
  if(lr.disclaimer) h+='<p style="font-size:0.78em;color:var(--text2);margin-top:8px">'+_mdFrontier(lr.disclaimer)+'</p>';
  h+='</div>';
  return h;
}

function renderFrontier(){
  var fv=document.getElementById("frontier-view");if(!fv)return;
  fv.innerHTML="<style>.f-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:14px}.f-card h3{color:var(--gold);margin-bottom:6px;font-size:1em}.f-card p{font-size:0.85em;line-height:1.8;color:var(--text)}.f-link{color:var(--blue);font-size:0.8em}.f-nav-btn{padding:4px 12px;border:1px solid var(--line);border-radius:14px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.78em;transition:all 0.2s}.f-nav-btn.active{background:var(--gold);color:#fff;border-color:var(--gold)}.f-target{position:relative;scroll-margin-top:90px}.f-target::after{content:'';position:absolute;inset:-6px;border:2px solid var(--gold);border-radius:12px;animation:fTarget 1.8s ease-out forwards;pointer-events:none}@keyframes fTarget{0%{opacity:1}100%{opacity:0}}";

  var fd = (typeof FRONTIER_DATA !== 'undefined') ? FRONTIER_DATA : null;
  var sec = fd && fd.sections ? fd.sections : null;

  if(sec){
    // Render from YAML data
    ['huayan','chinese','buddhist','others'].forEach(function(key){
      if(sec[key]) fv.innerHTML += _renderSection(key, sec[key]);
    });
    if(sec.litreview) fv.innerHTML += _renderLitReview(sec.litreview);
  } else {
    // Fallback: render placeholder
    fv.innerHTML += '<div class=section style=border-left:4px solid var(--gold)><h2>前沿对话</h2><p>数据加载中...</p></div>';
  }

  // References
  var refs = fd && fd.references ? fd.references : [];
  if(refs.length){
    fv.innerHTML += '<div class=section style="margin-top:16px"><details><summary style="cursor:pointer;font-size:0.85em;color:var(--gold)">📚 参考文献总目 ('+refs.length+'条)</summary><ul style="font-size:0.75em;line-height:1.8">';
    refs.forEach(function(r){ fv.innerHTML += '<li>'+_escFrontier(r)+'</li>'; });
    fv.innerHTML += '</ul></details></div>';
  }

  fv.innerHTML += '<div id=fv-bibliography></div>';
  // 逐域插入「独立文章页」入口（域登记了 id 时）
  setTimeout(function(){
    if(!sec) return;
    Object.keys(sec).forEach(function(key){
      var s=sec[key];
      if(!s||!s.domains) return;
      s.domains.forEach(function(d){
        if(d.id && typeof articleChip==='function') articleChip(d.id, '#fv-'+key+'-'+d.id);
      });
    });
  }, 80);
  // Render BIBLIOGRAPHY at bottom
  setTimeout(function(){
    var bibDiv = document.getElementById('fv-bibliography');
    if (bibDiv && typeof renderBibForPage === 'function') {
      bibDiv.innerHTML = renderBibForPage('frontier');
    }
  }, 100);
}

function switchFrontier(view){
  document.querySelectorAll('.f-nav-btn').forEach(function(b){b.classList.remove('active');});
  var btn=document.querySelector('.f-nav-btn[onclick*=\"'+view+'\"]');if(btn)btn.classList.add('active');
  ['huayan','chinese','buddhist','others','litreview'].forEach(function(v){
    var el=document.getElementById('fv-'+v);if(el)el.style.display=(v===view?'block':'none');
  });
  try{localStorage.setItem('frontier_view',view);}catch(e){}
}
setTimeout(function(){
  var v=localStorage.getItem('frontier_view')||'huayan';
  switchFrontier(v);
},100);
function switchFrontierNav(view,link){
  switchFrontier(view);
  document.querySelectorAll('#sidebar .nav-link').forEach(function(l){l.classList.remove('active');});
  if(link)link.classList.add('active');
}
// 子目录跳转：切到对应对话节并滚动/高亮该域卡片（f-target 动画一次）
function switchFrontierDomain(key,id){
  switchFrontierNav(key,null);
  document.querySelectorAll('#sidebar .nav-link').forEach(function(l){
    var oc=l.getAttribute('onclick')||'';
    if(oc.indexOf('switchFrontierNav')>=0&&oc.indexOf("'"+key+"'")>=0) l.classList.add('active');
  });
  setTimeout(function(){
    var dc=document.getElementById('fv-'+key+'-'+id);
    if(dc){
      dc.classList.remove('f-target');
      void dc.offsetWidth;
      dc.classList.add('f-target');
      dc.scrollIntoView({behavior:'smooth',block:'start'});
    }
  },120);
}
