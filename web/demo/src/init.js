// ═══ INIT ═══
resizeTL();
drawTL(null);
initMap();
renderGap();
renderPractice();

// Events
document.getElementById("search-input").addEventListener("input",function(){searchQuery=this.value.trim();drawTL(selectedId);});
var panel=document.getElementById("tl-panel");
panel.addEventListener("wheel",onWheel,{passive:false});
panel.addEventListener("mousedown",onMD); panel.addEventListener("mousemove",onMM);
panel.addEventListener("mouseup",onMU); panel.addEventListener("mouseleave",onMU);
panel.addEventListener("click",onClick);
panel.addEventListener("touchstart",function(e){if(e.touches.length===1){tl.drag=true;tl.lastX=e.touches[0].clientX;}e.preventDefault();},{passive:false});
panel.addEventListener("touchmove",function(e){if(tl.drag){var dx=e.touches[0].clientX-tl.lastX;tl.ox+=dx;tl.lastX=e.touches[0].clientX;drawTL(selectedId);}e.preventDefault();},{passive:false});
panel.addEventListener("touchend",function(){tl.drag=false;});

// Controls
document.getElementById("reset-btn").addEventListener("click",function(){clearSelection();searchQuery="";document.getElementById("search-input").value="";tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);if(map)map.setView([33,110],4);});
document.querySelectorAll("#controls button[data-filter]").forEach(function(btn){btn.addEventListener("click",function(){
  document.querySelectorAll("#controls button[data-filter]").forEach(function(b){b.classList.remove("active");});
  btn.classList.add("active");
  var lin=btn.dataset.filter;
  if(lin==="all"){clearSelection();return;}
  var ids=DATA.nodes.filter(function(n){return n.li===lin;}).map(function(n){return n.id;});
  if(ids.length>0)selectPerson(ids[0]);
});});

// Final: set viewport & draw
tl.ox=20; tl.scale=(tl.W-40)/(tl.maxX-tl.minX); drawTL(null);
