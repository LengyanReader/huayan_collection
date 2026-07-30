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
  var cs=[];try{cs=JSON.parse(localStorage.getItem('huayan_cmt_'+tab)||'[]');}catch(e){}
  cs.push({d:new Date().toISOString().slice(0,10),t:t.value.trim()});
  localStorage.setItem('huayan_cmt_'+tab,JSON.stringify(cs));t.value='';renderComments(tab);
};
window.renderComments=function(tab){
  var box=document.getElementById('cmt-'+tab);if(!box)return;
  var cs=[];try{cs=JSON.parse(localStorage.getItem('huayan_cmt_'+tab)||'[]');}catch(e){}
  var h='<h4>💬 评论与建议 ('+cs.length+')</h4>';
  h+='<div class=c-list>';cs.slice(-8).forEach(function(c){h+='<div class=c-item><b>'+c.d+'</b>: '+c.t+'</div>';});
  h+='</div><textarea id=cmt-input-'+tab+' placeholder=输入修改建议或评论… rows=2></textarea>';
  h+='<button onclick=submitComment(\"'+tab+'\")>提交</button>';
  box.innerHTML=h;
};
['lineage','gap','practice','frontier'].forEach(function(tab){renderComments(tab);});

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

// Click-outside-to-close popups
document.addEventListener('click',function(e){
  var ip=document.getElementById('info-popup');
  var ri=document.getElementById('route-info');
  if(ip&&ip.style.display==='block'&&!ip.contains(e.target))ip.style.display='none';
  if(ri&&ri.style.display==='block'&&!ri.contains(e.target)&&e.target.id!=='route-info-btn')ri.style.display='none';
});

// Final: set viewport & draw
tl.ox=20; tl.scale=(tl.W-40)/(tl.maxX-tl.minX); drawTL(null);
