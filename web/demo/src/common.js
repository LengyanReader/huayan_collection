// ═══ 华严宗部 — 共享脚本 ═══

// ── Error Catch ──
window.onerror=function(m,s,l,c,e){
  var d=document.createElement("div");
  d.style.cssText="position:fixed;top:0;left:0;right:0;z-index:99999;background:#c46b5d;color:#fff;padding:10px;font:12px monospace;white-space:pre-wrap";
  d.textContent="JS ERROR: "+m+" at line "+l;
  document.body.appendChild(d);
};

// ── Comment System ──
window.submitComment=function(tab){
  var t=document.getElementById('cmt-input-'+tab);if(!t||!t.value.trim())return;
  var text=t.value.trim();
  var now=new Date();
  var ts=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0')
    +' '+String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0')+':'+String(now.getSeconds()).padStart(2,'0');
  var token=localStorage.getItem('gh_pat_v4');
  var user='访客';

  function saveComment(ip){
    var cs=[];try{cs=JSON.parse(localStorage.getItem('huayan_cmt_'+tab)||'[]');}catch(e){}
    cs.push({d:ts,t:text,u:user,ip:ip||''});
    localStorage.setItem('huayan_cmt_'+tab,JSON.stringify(cs));t.value='';renderComments(tab);
    if(token){
      var labels=tab==='jiaoxing'?['华严教行']:tab==='lineage'?['法脉']:tab==='gap'?['文献']:tab==='cosmology'?['世主妙严']:['前沿'];
      var body='**'+user+'** · '+ts+(ip?' · IP:'+ip:'')+'\n\n---\n\n标签: '+tab+'\n\n'+text;
      fetch('https://api.github.com/repos/LengyanReader/huayan_collection/issues',{
        method:'POST',headers:{'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json'},
        body:JSON.stringify({title:'💬 ['+labels[0]+'] '+text.substring(0,60),body:body,labels:labels})
      }).then(function(r){return r.json();}).then(function(d){
        if(d.html_url){var st=document.getElementById('cmt-'+tab);if(st){var note=st.querySelector('h4');if(note)note.innerHTML+=' ✅<a href='+d.html_url+' target=_blank style=font-size:0.8em>#'+d.number+'</a>';}}
      }).catch(function(){});
    }
  }

  if(token){
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
  h+='<div class=c-list>';
  cs.slice(-8).forEach(function(c,i){
    var idx=cs.length-8+i;if(idx<0)idx=0;
    var who=c.u&&c.u!=='访客'?('<b style=color:#5e8b9e>@'+c.u+'</b> '):'';
    var ts=c.d||'';var ip=c.ip?' · '+c.ip:'';
    var ct=c.t;
    // Process data:image URLs
    var buf='',j=0;
    while(j<ct.length){
      var s=ct.indexOf('](data:image/',j);
      if(s<0){buf+=ct.substring(j);break;}
      var start=ct.lastIndexOf('![',s);
      if(start<0||start<j){buf+=ct.substring(j,s+2);j=s+2;continue;}
      var uriEnd=s+2;var d=1;
      while(uriEnd<ct.length&&d>0){if(ct[uriEnd]==='(')d++;else if(ct[uriEnd]===')')d--;uriEnd++;}
      uriEnd--;
      var uri=ct.substring(s+2,uriEnd);
      buf+=ct.substring(j,start);
      buf+='<div style="text-align:center;margin:6px 0"><img src="'+uri+'" style="max-width:200px;max-height:200px;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,0.1)"></div>';
      j=uriEnd+1;
    }
    ct=buf;
    h+='<div class=c-item>'+who+'<span style=font-size:0.7em;color:var(--text2)>'+ts+ip+'</span><br>'+ct
      +(token?'<button onclick=deleteComment(\"'+tab+'\",'+idx+') style=background:none;border:none;color:#c46b5d;cursor:pointer;font-size:0.9em title=删除>×</button>':'')
      +'</div>';
  });
  h+='</div><textarea id=cmt-input-'+tab+' placeholder=\"输入文本或直接Ctrl+V贴图…\" rows=2></textarea>';
  h+='<button onclick=submitComment(\"'+tab+'\")>提交</button> ';
  h+='<label style=font-size:0.7em;color:var(--text2);cursor:pointer;border:1px solid var(--line);border-radius:4px;padding:2px 6px;margin-left:4px">🖼 选图<input type=file accept=image/* style=display:none onchange=\"pickImage(this,\\\''+tab+'\\\')\"></label>';
  h+=(token?'':'<p style=font-size:0.65em;color:var(--text2);margin-top:2px>(配置Token后可同步评论至GitHub)</p>');
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

// ── Image paste support ──
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

// ── GitHub Auth ──
window.heartLogin=function(){
  var token=prompt('请输入GitHub Personal Access Token (需要有repo权限):','');
  if(!token)return;
  fetch('https://api.github.com/user',{headers:{'Authorization':'Bearer '+token}})
    .then(function(r){return r.json();})
    .then(function(u){
      if(u.login){
        localStorage.setItem('gh_pat_v4',token);
        localStorage.setItem('gh_username',u.login);
        heartToast('已授权: @'+u.login);
      }else{
        heartToast('授权失败,请检查Token');
      }
    }).catch(function(){heartToast('网络错误');});
};

window.heartLogout=function(){
  localStorage.removeItem('gh_pat_v4');
  localStorage.removeItem('gh_username');
  heartToast('已退出');
};

window.heartExport=function(){
  var data={};
  for(var i=0;i<localStorage.length;i++){
    var k=localStorage.key(i);
    if(k.indexOf('huayan_')===0||k.indexOf('gh_')===0)data[k]=localStorage.getItem(k);
  }
  var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  var a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='huayan_backup_'+new Date().toISOString().slice(0,10)+'.json';
  a.click();
};

window.heartImport=function(){
  var input=document.createElement('input');input.type='file';input.accept='.json';
  input.onchange=function(){
    var file=input.files[0];if(!file)return;
    var reader=new FileReader();
    reader.onload=function(e){
      try{var data=JSON.parse(e.target.result);
        Object.keys(data).forEach(function(k){localStorage.setItem(k,data[k]);});
        heartToast('导入成功,刷新页面生效');}
      catch(ex){heartToast('导入失败: 文件格式错误');}
    };
    reader.readAsText(file);
  };
  input.click();
};

window.heartToast=function(msg){
  var t=document.createElement('div');
  t.style.cssText='position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:99999;background:#3d3427;color:#fefdf9;padding:8px 20px;border-radius:20px;font-size:0.82em;transition:opacity 0.3s';
  t.textContent=msg;document.body.appendChild(t);
  setTimeout(function(){t.style.opacity='0';setTimeout(function(){t.remove();},300);},2000);
};

window.heartCopy=function(elId){
  var el=document.getElementById(elId);if(!el)return;
  var text=el.textContent||el.innerText;
  navigator.clipboard.writeText(text).then(function(){heartToast('已复制');}).catch(function(){heartToast('复制失败');});
};

// ── Scroll to Top Button ──
(function(){
  var btn=document.querySelector('.back-to-top');
  if(btn){
    window.addEventListener('scroll',function(){
      btn.classList.toggle('visible',window.scrollY>300);
    });
  }
})();

// ── Sidebar Scroll-Spy ──
(function(){
  var sidebar=document.getElementById('sidebar');
  if(!sidebar)return;
  var links=sidebar.querySelectorAll('.nav-link');
  if(links.length===0)return;
  window.addEventListener('scroll',function(){
    var scrollPos=window.scrollY+80;
    links.forEach(function(link){
      var section=link.getAttribute('data-section');
      if(!section)return;
      // Look for related sections in content
      var target=document.getElementById(section)||document.querySelector('[id*="'+section+'"]');
      if(!target)return;
      var top=target.offsetTop,bottom=top+target.offsetHeight;
      if(scrollPos>=top&&scrollPos<bottom){
        links.forEach(function(l){l.classList.remove('active');});
        link.classList.add('active');
      }
    });
  });

  // Click handler for smooth scroll
  links.forEach(function(link){
    link.addEventListener('click',function(e){
      e.preventDefault();
      var section=link.getAttribute('data-section');
      var target=document.getElementById(section)||document.querySelector('[id*="'+section+'"]');
      if(target){target.scrollIntoView({behavior:'smooth',block:'start'});}
    });
  });
})();
