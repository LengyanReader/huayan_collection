// ═══ ERROR CATCH ═══
window.onerror=function(m,s,l,c,e){var d=document.createElement("div");d.style.cssText="position:fixed;top:0;left:0;right:0;z-index:99999;background:#c46b5d;color:#fff;padding:10px;font:12px monospace;white-space:pre-wrap";d.textContent="JS ERROR: "+m+" at line "+l;document.body.appendChild(d);};

// ═══ INIT ═══
resizeTL();
drawTL(null);
initMap();
// Default: ancient map + routes + other schools
setTimeout(function(){toggleAncient();initTransStory();initOtherSchools();},500);
// Stats bar
var sb=document.getElementById("stats-bar");if(sb)sb.textContent=calcStats();
renderGap();
renderPractice();
renderFrontier();
try{renderCosmology();}catch(e){}

// Events
document.getElementById("search-input").addEventListener("input",function(){searchQuery=this.value.trim();drawTL(selectedId);});
var panel=document.getElementById("tl-panel");
panel.addEventListener("wheel",onWheel,{passive:false});
panel.addEventListener("mousedown",onMD); panel.addEventListener("mousemove",onMM);
panel.addEventListener("mouseup",onMU); panel.addEventListener("mouseleave",onMU);
panel.addEventListener("click",onClick);
var touchStartX=0,touchStartY=0,touchMoved=false;
panel.addEventListener("touchstart",function(e){if(e.touches.length===1){tl.drag=true;tl.lastX=e.touches[0].clientX;touchStartX=e.touches[0].clientX;touchStartY=e.touches[0].clientY;touchMoved=false;}},{passive:true});
panel.addEventListener("touchmove",function(e){if(!tl.drag)return;var dx=e.touches[0].clientX-touchStartX;var dy=e.touches[0].clientY-touchStartY;touchMoved=true;if(Math.abs(dx)>Math.abs(dy)){e.preventDefault();tl.ox+=e.touches[0].clientX-tl.lastX;tl.lastX=e.touches[0].clientX;drawTL(selectedId);}},{passive:false});
panel.addEventListener("touchend",function(){tl.drag=false;});

// Bookmarks
document.querySelectorAll("#controls button[data-bookmark]").forEach(function(btn){btn.addEventListener("click",function(){
  var range=btn.dataset.bookmark.split(",");
  var from=parseInt(range[0]),to=parseInt(range[1]);
  tl.ox=40;tl.scale=(tl.W-80)/(to-from);tl.minX=from-50;tl.maxX=to+50;
  tl.ox=40-(from-50-tl.minX)*tl.scale;drawTL(selectedId);
});});

// Controls
document.getElementById("reset-btn").addEventListener("click",function(){clearSelection();searchQuery="";document.getElementById("search-input").value="";tl.minX=100;tl.maxX=2060;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);if(map)map.setView([33,110],4);});
document.querySelectorAll("#controls button[data-filter]").forEach(function(btn){btn.addEventListener("click",function(){
  document.querySelectorAll("#controls button[data-filter]").forEach(function(b){b.classList.remove("active");});
  btn.classList.add("active");
  var lin=btn.dataset.filter;
  if(lin==="all"){clearSelection();return;}
  var ids=DATA.nodes.filter(function(n){return n.li===lin;}).map(function(n){return n.id;});
  if(ids.length>0)selectPerson(ids[0]);
});});

// ═══ COMMENT SYSTEM ═══
window.submitComment=function(tab){
  var t=document.getElementById('cmt-input-'+tab);if(!t||!t.value.trim())return;
  var text=t.value.trim();
  var now=new Date();
  var ts=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0')
    +' '+String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0')+':'+String(now.getSeconds()).padStart(2,'0');
  // Get username from token if available
  var token=localStorage.getItem('gh_pat_v4');
  var user='访客';

  function saveComment(ip){
    var cs=[];try{cs=JSON.parse(localStorage.getItem('huayan_cmt_'+tab)||'[]');}catch(e){}
    var entry={d:ts,t:text,u:user,ip:ip||''};
    cs.push(entry);
    localStorage.setItem('huayan_cmt_'+tab,JSON.stringify(cs));t.value='';renderComments(tab);
    // Try to create GitHub Issue
    if(token){
      var labels=tab==='practice'?['行法']:tab==='lineage'?['法脉']:tab==='gap'?['文献']:tab==='cosmology'?['世主妙严']:['前沿'];
      var body='**'+user+'** · '+ts+(ip?' · IP:'+ip:'')+'\n\n---\n\n标签: '+tab+'\n\n'+text;
      fetch('https://api.github.com/repos/LengyanReader/huayan_collection/issues',{
        method:'POST',headers:{'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json'},
        body:JSON.stringify({title:'💬 ['+labels[0]+'] '+text.substring(0,60),body:body,labels:labels})
      }).then(function(r){return r.json();}).then(function(d){
        if(d.html_url){var st=document.getElementById('cmt-'+tab);if(st){var note=st.querySelector('h4');if(note)note.innerHTML+=' ✅<a href='+d.html_url+' target=_blank style=font-size:0.8em>#'+d.number+'</a>';}}
      }).catch(function(){});
    }else{
      // Fallback: open GitHub Issue form for anyone with GitHub account
      var title='💬 ['+tab+'] '+text.substring(0,60);
      var body='**'+user+'** · '+ts+'\n\n---\n\n'+text;
      var url='https://github.com/LengyanReader/huayan_collection/issues/new?title='+encodeURIComponent(title)+'&body='+encodeURIComponent(body);
      window.open(url,'_blank');
    }
  }

  // Get username and IP
  if(token){
    // Try to get GitHub username from cached data or fetch
    var cachedUser=localStorage.getItem('gh_username');
    if(cachedUser){user=cachedUser;tryGetIP(saveComment);}
    else{fetch('https://api.github.com/user',{headers:{'Authorization':'Bearer '+token}}).then(function(r){return r.json();}).then(function(u){
      if(u.login){user=u.login;localStorage.setItem('gh_username',u.login);}
      tryGetIP(saveComment);
    }).catch(function(){tryGetIP(saveComment);});}
  }else{tryGetIP(saveComment);}

  function tryGetIP(cb){
    fetch('https://api.ipify.org?format=json').then(function(r){return r.json();}).then(function(d){cb(d.ip||'');}).catch(function(){cb('');});
  }
};
window.renderComments=function(tab){
  var box=document.getElementById('cmt-'+tab);if(!box)return;
  var cs=[];try{cs=JSON.parse(localStorage.getItem('huayan_cmt_'+tab)||'[]');}catch(e){}
  var token=!!localStorage.getItem('gh_pat_v4');
  var h='<h4>💬 评论与建议 ('+cs.length+')</h4>';
  h+='<div class=c-list>';cs.slice(-8).forEach(function(c,i){var idx=cs.length-8+i;if(idx<0)idx=0;
    var who=c.u&&c.u!=='访客'?('<b style=color:#5e8b9e>@'+c.u+'</b> '):'';var ts=c.d||'';var ip=c.ip?' · '+c.ip:'';
    var ct=c.t;
    // Render embedded images: split approach, DOM-safe
    var imgs=c.t.split(/(!\[[^\]]*\]\(data:image\/[^)]+\))/g);
    ct='';
    for(var ji=0;ji<imgs.length;ji++){
      var pp=imgs[ji];
      var mm=pp.match(/!\[([^\]]*)\]\((data:image\/[^)]+)\)/);
      if(mm){
        ct+='<div style="text-align:center;margin:6px 0"><img src="'+mm[2]+'" alt="'+mm[1]+'" style="max-width:200px;max-height:200px;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,0.1);display:inline-block" onerror="this.outerHTML=this.alt"></div>';
      }else{ct+=pp;}
    }
    h+='<div class=c-item>'+who+'<span style=font-size:0.7em;color:var(--text2)>'+ts+ip+'</span><br>'+ct
      +(token?'<button onclick=deleteComment(\"'+tab+'\",'+idx+') style=background:none;border:none;color:#c46b5d;cursor:pointer;font-size:0.9em title=删除>×</button>':'')
      +'</div>';
  });
  h+='</div><textarea id=cmt-input-'+tab+' placeholder=\"输入文本或直接Ctrl+V贴图…\" rows=2></textarea>';
  h+='<button onclick=submitComment(\"'+tab+'\")>提交</button> ';
  h+='<label style=font-size:0.7em;color:var(--text2);cursor:pointer;border:1px solid var(--line);border-radius:4px;padding:2px 6px>🖼 选图<input type=file accept=image/* style=display:none onchange=\"pickImage(this,\\\''+tab+'\\\')\"></label>';
  h+=(token?'':'<p style=font-size:0.65em;color:var(--text2);margin-top:2px>💡 配置Token后可同步评论至GitHub Issue并可删除</p>');
  box.innerHTML=h;
};
window.pickImage=function(input,tab){
  var file=input.files[0];if(!file)return;
  var reader=new FileReader();
  reader.onload=function(ev){
    var img=new Image();
    img.onload=function(){
      var dataUri=ev.target.result;
      if(img.width>600){var r=600/img.width;var c=document.createElement('canvas');c.width=600;c.height=Math.round(img.height*r);c.getContext('2d').drawImage(img,0,0,600,Math.round(img.height*r));dataUri=c.toDataURL('image/jpeg',0.65);}
      var ta=document.getElementById('cmt-input-'+tab);if(!ta)return;
      ta.value+='\n![图片]('+dataUri+')\n';
    };
    img.src=ev.target.result;
  };
  reader.readAsDataURL(file);
};
window.deleteComment=function(tab,idx){
  var cs=[];try{cs=JSON.parse(localStorage.getItem('huayan_cmt_'+tab)||'[]');}catch(e){}
  if(idx>=0&&idx<cs.length){cs.splice(idx,1);localStorage.setItem('huayan_cmt_'+tab,JSON.stringify(cs));renderComments(tab);}
};
['lineage','gap','practice','frontier','cosmology'].forEach(function(tab){renderComments(tab);});

// ── Image paste support for comment textareas ──
document.addEventListener('paste',function(e){
  var ta=e.target.closest('textarea[id^="cmt-input-"]');
  if(!ta)return;
  var items=e.clipboardData&&e.clipboardData.items;
  if(!items)return;
  for(var i=0;i<items.length;i++){
    if(items[i].type.indexOf('image')===0){
      e.preventDefault();
      var blob=items[i].getAsFile();
      var reader=new FileReader();
      reader.onload=function(ev){
        // Compress large images via canvas before storing
        var img=new Image();
        img.onload=function(){
          var dataUri=ev.target.result;
          if(img.width>600){
            var r=600/img.width,w=600,h=Math.round(img.height*r);
            var c=document.createElement('canvas');c.width=w;c.height=h;
            c.getContext('2d').drawImage(img,0,0,w,h);
            dataUri=c.toDataURL('image/jpeg',0.65);
          }
          var tag='![图片]('+dataUri+')';
          var s=ta.selectionStart,e=ta.selectionEnd;
          ta.value=ta.value.substring(0,s)+'\n'+tag+'\n'+ta.value.substring(e);
          ta.focus();
        };
        img.src=ev.target.result;
      };
      reader.readAsDataURL(blob);
      break;
    }
  }
});

// ═══ RESIZE HANDLE ═══
var resizeHandle=document.getElementById('resize-handle');
var sidePanel=document.getElementById('side');
if(resizeHandle&&sidePanel){
  var resizing=false,startX=0,startW=0;
  resizeHandle.addEventListener('mousedown',function(e){
    resizing=true;startX=e.clientX;startW=sidePanel.offsetWidth;
    resizeHandle.classList.add('active');e.preventDefault();
  });
  document.addEventListener('mousemove',function(e){
    if(!resizing)return;
    var newW=startW+(startX-e.clientX);
    newW=Math.max(180,Math.min(600,newW));
    sidePanel.style.width=newW+'px';
    resizeTL();drawTL(selectedId);if(mapMain)mapMain.invalidateSize();if(mapMini)mapMini.invalidateSize();
  });
  document.addEventListener('mouseup',function(){if(resizing){resizing=false;resizeHandle.classList.remove('active');}});
}

// Progress bar seek
var progBar=document.getElementById('anim-progress');
if(progBar){
  progBar.addEventListener('input',function(){
    var v=parseInt(this.value);if(!isNaN(v)&&v>=-1500&&v<=2030)animSeek(v);
  });
}

// Click-outside-to-close popups
document.addEventListener('click',function(e){
  var ip=document.getElementById('info-popup');
  var ri=document.getElementById('route-info');
  if(ip&&ip.style.display==='block'&&!ip.contains(e.target))ip.style.display='none';
  if(ri&&ri.style.display==='block'&&!ri.contains(e.target)&&e.target.id!=='route-info-btn')ri.style.display='none';
});

// Final: set viewport & draw
tl.ox=20; tl.scale=(tl.W-40)/(tl.maxX-tl.minX); drawTL(null);
