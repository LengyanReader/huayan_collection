// ═══ HELPERS ═══
function getPersonLocs(pid){return DATA.locations.filter(function(l){return (l.ps||[]).indexOf(pid)>=0;});}
function buildTimelineRows(){
  var order=["华严五祖","李通玄系","日本华严","高丽华严","贤首宗高原法系","月霞系","华严莲社","慈舟系","临济宗","译师","印度源流","当代学者"];
  var rows={}; order.forEach(function(l,i){rows[l]=i;});
  var rd=order.map(function(l){return {lineage:l,ps:[],y:0,color:DATA.lineage_colors[l]||"#b0a898"};});
  DATA.nodes.forEach(function(n){
    var ri=rows[n.li]!==undefined?rows[n.li]:order.length;
    if(!rd[ri])rd[ri]={lineage:n.li||"other",ps:[],y:0,color:DATA.lineage_colors[n.li]||"#b0a898"};
    rd[ri].ps.push(n);
  });
  tl.rows=rd.filter(function(r){return r.ps.length>0;});
}
buildTimelineRows();

// ═══ CANVAS ═══
var MIN_ROW_H=64;
function resizeTL(){var p=document.getElementById("tl-panel");tl.W=p.clientWidth;tl.canvas=document.getElementById("tl-canvas");var rows=tl.rows.length||1;tl.H=Math.max(p.clientHeight,rows*MIN_ROW_H+20);tl.canvas.width=tl.W;tl.canvas.height=tl.H;tl.canvas.style.width=tl.W+"px";tl.canvas.style.height=tl.H+"px";tl.ctx=tl.canvas.getContext("2d");}
function tX(y){return (y-tl.minX)*tl.scale+tl.ox;}

function drawTL(hlId){
  var ctx=tl.ctx,W=tl.W,H=tl.H;if(!ctx)return;ctx.clearRect(0,0,W,H);
  var rh=Math.max(MIN_ROW_H,H/Math.max(tl.rows.length,1));

  // 1. Dynasty bands
  [{n:"唐",s:618,e:907,c:"rgba(200,160,80,0.06)"},{n:"宋",s:960,e:1279,c:"rgba(150,170,190,0.06)"},{n:"明",s:1368,e:1644,c:"rgba(160,150,140,0.04)"},{n:"清",s:1644,e:1912,c:"rgba(150,140,130,0.04)"},{n:"近现代",s:1912,e:1949,c:"rgba(200,150,140,0.08)"},{n:"当代",s:1949,e:2026,c:"rgba(150,190,190,0.08)"}].forEach(function(d){var x=tX(d.s),x2=tX(d.e);if(x2>0&&x<W){ctx.fillStyle=d.c;ctx.fillRect(Math.max(0,x),0,Math.min(W,x2-x),H);}});

  // 2. Vertical century grid
  ctx.strokeStyle="#e8e0d0";ctx.lineWidth=0.5;ctx.setLineDash([3,6]);
  for(var y=200;y<=2050;y+=100){var x=tX(y);if(x>=0&&x<=W){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}}
  ctx.setLineDash([]);

  // 3. Row backgrounds and labels
  tl.rows.forEach(function(r,i){
    r.y=i*rh+rh/2;
    var y0=i*rh, y2=r.y;
    if(i%2===0){ctx.fillStyle="rgba(255,255,255,0.25)";ctx.fillRect(0,y0,W,rh);}
    // Row label
    ctx.fillStyle=r.color;ctx.font="600 12px Microsoft YaHei";ctx.fillText(r.lineage,10,y0+18);
    // Subtle row separator
    ctx.strokeStyle="#e8e0d0";ctx.lineWidth=0.5;ctx.beginPath();ctx.moveTo(0,y0+rh);ctx.lineTo(W,y0+rh);ctx.stroke();
  });

  // 4. Person lifespan bars
  tl.hitRects=[];var ds=25,isSearch=searchQuery.length>0;

  // First pass: assign y-offsets within each row to avoid overlap
  var rowOffsets={};
  tl.rows.forEach(function(r,ri){
    var sorted=r.ps.slice().sort(function(a,b){return (a.b||a.d||0)-(b.b||b.d||0);});
    var slots=[]; // occupied x-ranges per y-level
    sorted.forEach(function(p){
      var b=p.b||(p.d?p.d-ds:null),d=p.d||(p.b?p.b+ds:null);if(!b&&!d)return;
      var bx=tX(b||d-10),dx=tX(d||b+10),bw=Math.max(6,dx-bx);
      // Find a y-level where this bar doesn't overlap
      var level=0; var placed=false;
      while(!placed&&level<3){
        var overlap=false;
        if(!slots[level])slots[level]=[];
        for(var s=0;s<slots[level].length;s++){
          if(!(bx+bw+20<slots[level][s].x || bx>slots[level][s].x+slots[level][s].w+20)){
            overlap=true;break;
          }
        }
        if(!overlap){slots[level].push({x:bx,w:bw});placed=true;}
        else level++;
      }
      p._yOff=(level-1)*14; // -14, 0, or +14 offset from center
    });
  });

  // Second pass: draw
  tl.rows.forEach(function(r,ri){var y2=r.y;
    r.ps.forEach(function(p){
      var b=p.b||(p.d?p.d-ds:null),d=p.d||(p.b?p.b+ds:null);if(!b&&!d)return;
      var bx=tX(b||d-10),dx=tX(d||b+10),bh=Math.min(22,rh*0.35),by=y2-bh/2+(p._yOff||0);
      var isHL=p.id===hlId,matches=!isSearch||p.n.indexOf(searchQuery)>=0;
      if(isSearch&&!matches)ctx.globalAlpha=0.12;else if(hlId&&!isHL)ctx.globalAlpha=0.18;else ctx.globalAlpha=1;

      // Shadow for highlighted
      if(isHL){ctx.shadowColor="#b8863c";ctx.shadowBlur=16;}

      // Rounded bar
      ctx.fillStyle=isHL?"#c46b5d":(r.color+"DD");var rx=Math.max(0,bx),rw=Math.max(6,dx-rx);
      ctx.beginPath();ctx.moveTo(rx+4,by);ctx.lineTo(rx+rw-4,by);ctx.quadraticCurveTo(rx+rw,by,rx+rw,by+4);ctx.lineTo(rx+rw,by+bh-4);ctx.quadraticCurveTo(rx+rw,by+bh,rx+rw-4,by+bh);ctx.lineTo(rx+4,by+bh);ctx.quadraticCurveTo(rx,by+bh,rx,by+bh-4);ctx.lineTo(rx,by+4);ctx.quadraticCurveTo(rx,by,rx+4,by);ctx.closePath();ctx.fill();

      ctx.shadowColor="transparent";ctx.shadowBlur=0;ctx.globalAlpha=1;

      // Name label (staggered: alternate above/below)
      if(!isSearch||matches){
        var labelAbove=(p._yOff||0)<=0;
        var labelY=labelAbove?by-5:by+bh+13;
        ctx.fillStyle=isHL?"#c46b5d":"#5c5040";ctx.font=(isHL?"bold ":"")+(isHL?12:10)+"px Microsoft YaHei";
        ctx.fillText(p.n,rx+rw+6,labelY);
      }
      tl.hitRects.push({x:rx,y:by,w:rw,h:bh,person:p});
    });
  });

  // 5. Edges (master→disciple connections)
  tl.hitRects.forEach(function(hr){var p=hr.person;
    DATA.edges.filter(function(e){return e.s===p.id&&(e.r==="MASTER"||e.r==="LINEAGE");}).forEach(function(e){var tHR=tl.hitRects.find(function(h){return h.person.id===e.t;});if(!tHR)return;var isHL=p.id===hlId||e.t===hlId;ctx.strokeStyle=isHL?"#b8863c":"#d5cdc0";ctx.lineWidth=isHL?2.2:1;ctx.globalAlpha=isHL?1:0.4;ctx.setLineDash(e.r==="LINEAGE"?[5,4]:[]);ctx.beginPath();var sx=hr.x+hr.w,sy=hr.y+hr.h/2,ex=tHR.x,ey=tHR.y+tHR.h/2;ctx.moveTo(sx,sy);ctx.bezierCurveTo(sx+(ex-sx)*0.4,sy,ex-(ex-sx)*0.4,ey,ex,ey);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;});
  });

  // 6. Event markers
  ctx.fillStyle="#a09080";ctx.font="10px Microsoft YaHei";
  for(var y=200;y<=2000;y+=100){var x=tX(y);if(x>=0&&x<=W)ctx.fillText(y,x-12,H-8);}
  [{y:420,l:"六十华严译出",c:"#b8863c"},{y:699,l:"八十华严译出",c:"#b8863c"},{y:845,l:"唐武宗灭佛·法难",c:"#c46b5d"},{y:1085,l:"义天入宋求法",c:"#6d9a6e"},{y:1914,l:"华严大学创立",c:"#5e8b9e"},{y:1952,l:"华严莲社创社",c:"#5e8b9e"},{y:2008,l:"钦因传衣钵",c:"#c46b5d"}].forEach(function(ev){var x=tX(ev.y);if(x<0||x>W)return;ctx.fillStyle=ev.c;ctx.font="bold 9px Microsoft YaHei";ctx.fillText("▸ "+ev.l,x,H-22);});
}

// ═══ MAP ═══
function initMap(){
  if(map){map.invalidateSize();return;}
  if(typeof L==="undefined"){document.getElementById("map").innerHTML="<div style=display:flex;align-items:center;justify-content:center;height:100%;color:var(--text2)>🗺 地图组件未加载</div>";return;}
  map=L.map("map",{zoomControl:true}).setView([33,110],4);
  L.tileLayer("https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",{subdomains:["1","2","3","4"],maxZoom:18}).addTo(map);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{subdomains:["a","b","c"],maxZoom:19,opacity:0.5}).addTo(map);
  var mc={temple:"#b8863c",mountain:"#7d9a6e",region:"#c46b5d"};
  DATA.locations.forEach(function(loc){
    var names=(loc.ps||[]).map(function(pid){var n=nodeMap[pid];return n?n.n:"";}).filter(Boolean).join("、");
    var m=L.circleMarker([loc.lat,loc.lng],{radius:9,fillColor:mc[loc.tp]||"#b0a898",color:"#fff",weight:2,fillOpacity:0.9});
    m.addTo(map).bindPopup("<b>"+loc.n+"</b><br>"+(loc.dy||"")+"<br>"+(loc.ds||"")+(names?"<br>👤 "+names:""));
    m._ld=loc;m.on("click",function(){if(loc.ps&&loc.ps.length>0)selectPerson(loc.ps[0]);});
  });
}

// ═══ SELECTION ═══
function selectPerson(id,isShift){
  if(isShift&&selectedId&&id!==selectedId){selectedId2=id;}else{selectedId=id;selectedId2=null;}
  drawTL(selectedId);if(selectedId2)drawTL2(selectedId2);
  showInfo(nodeMap[selectedId],selectedId2?nodeMap[selectedId2]:null);
  var lc=DATA.lineage_colors[p.li]||"#b0a898";
  var locs=getPersonLocs(id),locHTML="";
  locs.forEach(function(l){locHTML+="📍 "+l.n+"<br>";});
  var teachers=DATA.edges.filter(function(e){return e.t===id&&e.r==="MASTER";}).map(function(e){return nodeMap[e.s];}).filter(Boolean);
  var students=DATA.edges.filter(function(e){return e.s===id&&e.r==="MASTER";}).map(function(e){return nodeMap[e.t];}).filter(Boolean);
  var tch=teachers.length?"⬆ 师承: "+teachers.map(function(t){return t.n;}).join("、")+"<br>":"";
  var std=students.length?"⬇ 传法: "+students.map(function(t){return t.n;}).join("、")+"<br>":"";
  // Contemporary figures
  var contemp=DATA.nodes.filter(function(n){return n.dy===p.dy&&n.id!==p.id&&n.li===p.li;}).slice(0,3);
  var cont=contemp.length?"👥 同代: "+contemp.map(function(n){return n.n;}).join("、")+"<br>":"";
  document.getElementById("info-box").innerHTML="<h3>"+p.n+" <span style=font-size:0.7em;color:var(--text2)>"+(p.ti||"")+"</span></h3>"
    +"<span class=tag style=background:"+lc+"20;color:"+lc+">"+(p.li||"—")+"</span>"
    +"<span class=tag style=background:rgba(0,0,0,0.04)>"+(p.tp==="patriarch"?"祖师":p.tp==="translator"?"译师":p.tp==="scholar"?"学者":"行者")+"</span><br>"
    +"📅 <b>"+(p.dy||"?")+"</b> · "+(p.b||"?")+"–"+(p.d||"?")+"<br>"
    +locHTML+tch+std+cont
    +(p.bio?"<div style=color:var(--text2);line-height:1.5;margin-top:4px;padding-top:4px;border-top:1px solid var(--line)>"+p.bio+"</div>":"")
    +(p.wk&&p.wk.length?"<div style=margin-top:4px>📖 <b>"+p.wk.join("</b> · <b>")+"</b></div>":"");
  if(map&&locs.length>0){
    var loc=locs[0];map.flyTo([loc.lat,loc.lng],locs.length===1?10:8,{duration:0.8});
    // Highlight all related markers
    setTimeout(function(){
      map.eachLayer(function(layer){
        if(!layer._ld)return;
        var isRelated=locs.some(function(l){return l.id===layer._ld.id;});
        if(isRelated){
          layer.setRadius(13);layer.setStyle({fillColor:"#c46b5d",color:"#fff",weight:3,fillOpacity:1});
          if(!layer._popupOpen){layer.openPopup();layer._popupOpen=true;setTimeout(function(){layer.closePopup();layer._popupOpen=false;},3000);}
        }else{
          layer.setRadius(7);layer.setStyle({fillOpacity:0.5});
        }
      });
    },900);
    // Reset after 4 seconds
    setTimeout(function(){
      map.eachLayer(function(layer){
        if(!layer._ld)return;
        var mc={temple:"#b8863c",mountain:"#7d9a6e",region:"#c46b5d"};
        layer.setRadius(9);layer.setStyle({fillColor:mc[layer._ld.tp]||"#b0a898",color:"#fff",weight:2,fillOpacity:0.9});
      });
    },4000);
  }
}
function clearSelection(){selectedId=null;selectedId2=null;drawTL(null);document.getElementById("info-box").innerHTML="<div class=empty>👆 点击人物寿命条查看详情<br><span style=font-size:0.8em>Shift+点击第二人可并排对比</span></div>";}
function drawTL2(id){/* placeholder for second highlight */}

// ═══ INTERACTION ═══
function onWheel(e){e.preventDefault();var p=document.getElementById("tl-panel");var r=p.getBoundingClientRect();var mx=e.clientX-r.left;var before=(mx-tl.ox)/tl.scale;tl.scale*=e.deltaY<0?1.12:0.89;tl.scale=Math.max(0.12,Math.min(6,tl.scale));tl.ox=mx-before*tl.scale;drawTL(selectedId);}
function onMD(e){if(e.target.tagName==="CANVAS"){tl.drag=true;tl.lastX=e.clientX;}}
function onMM(e){
  if(!tl.drag){
    var p=document.getElementById("tl-panel"),r=p.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
    var hit=tl.hitRects.find(function(h){return mx>=h.x&&mx<=h.x+h.w&&my>=h.y&&my<=h.y+h.h;});
    var tip=document.getElementById("tl-tooltip");
    if(hit){var pp=hit.person;tip.style.opacity="1";tip.innerHTML="<h3>"+pp.n+"</h3>"+(pp.ti||"")+" · "+pp.dy+" · "+(pp.b||"?")+"–"+(pp.d||"?");tip.style.left=(e.pageX+14)+"px";tip.style.top=(e.pageY-20)+"px";}
    else{tip.style.opacity="0";}
    return;
  }
  var dx=e.clientX-tl.lastX;tl.ox+=dx;tl.lastX=e.clientX;drawTL(selectedId);
}
function onMU(){tl.drag=false;}
function onClick(e){
  if(tl.drag||Math.abs(e.clientX-tl.lastX)>3)return;
  var p=document.getElementById("tl-panel"),r=p.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  var hit=tl.hitRects.find(function(h){return mx>=h.x&&mx<=h.x+h.w&&my>=h.y&&my<=h.y+h.h;});
  if(hit){selectPerson(hit.person.id,e.shiftKey);}else{clearSelection();}
}

// ═══ ANIMATION ═══
var animTimer=null,animYear=500,animPlaying=false;
function toggleAnim(){
  if(animPlaying){clearInterval(animTimer);animPlaying=false;document.getElementById("anim-btn").textContent="▶ 播放";return;}
  animPlaying=true;document.getElementById("anim-btn").textContent="⏸ 暂停";
  animYear=500;tl.minX=animYear-100;tl.maxX=animYear+300;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);
  animTimer=setInterval(function(){
    animYear+=15;if(animYear>2030){animYear=500;clearInterval(animTimer);animPlaying=false;document.getElementById("anim-btn").textContent="▶ 播放";}
    tl.minX=animYear-100;tl.maxX=animYear+300;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);
  },200);
}

// ═══ TABS ═══
document.getElementById("tabs").addEventListener("click",function(e){
  if(e.target.tagName!=="BUTTON")return;
  switchTab(e.target.dataset.tab);
});
function switchTab(tab){
  document.querySelectorAll("#tabs button").forEach(function(b){b.classList.remove("active");});
  document.querySelector("#tabs button[data-tab="+tab+"]").classList.add("active");
  document.querySelectorAll(".tab-content").forEach(function(t){t.classList.remove("active");});
  document.getElementById("tab-"+tab).classList.add("active");
  location.hash=tab;
  if(tab==="lineage"){setTimeout(function(){resizeTL();drawTL(selectedId);if(map)map.invalidateSize();},200);}
}
// Restore tab from URL hash on load
if(location.hash){var h=location.hash.slice(1);if(document.getElementById("tab-"+h))switchTab(h);}
