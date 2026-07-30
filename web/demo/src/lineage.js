// ═══ DATA LAYERS ═══
var layerVis={theory:true,geo:true,practice:true,edges:true,events:true};
var THEORY_STAGES=[
  {label:'法界观门/五教止观',s:557,e:700,c:'rgba(184,134,60,0.10)',tc:'#b8863c'},
  {label:'五教十宗/法界缘起',s:643,e:820,c:'rgba(94,139,158,0.10)',tc:'#5e8b9e'},
  {label:'禅教融合',s:780,e:850,c:'rgba(125,154,110,0.10)',tc:'#7d9a6e'},
  {label:'义学沉寂·法脉隐传',s:850,e:1850,c:'rgba(160,144,128,0.06)',tc:'#a09080'},
  {label:'华严大学/现代复兴',s:1850,e:1981,c:'rgba(196,107,93,0.10)',tc:'#c46b5d'},
  {label:'普贤乘华严/东山法门',s:1981,e:2026,c:'rgba(109,154,110,0.10)',tc:'#6d9a6e'}
];
var PRACTICE_STAGES=[
  {label:'法界三昧观',s:557,e:640,c:'rgba(184,134,60,0.06)',tc:'#b8863c'},
  {label:'华严三昧观',s:643,e:820,c:'rgba(125,154,110,0.06)',tc:'#7d9a6e'},
  {label:'禅教融合观',s:780,e:850,c:'rgba(94,139,158,0.06)',tc:'#5e8b9e'},
  {label:'修行法脉隐传',s:850,e:1914,c:'rgba(160,144,128,0.03)',tc:'#a09080'},
  {label:'华严大学禅观',s:1914,e:1981,c:'rgba(196,107,93,0.06)',tc:'#c46b5d'},
  {label:'东山法门等持工程',s:1981,e:2026,c:'rgba(109,154,110,0.06)',tc:'#6d9a6e'}
];
var GEO_FLOW=[
  {l:'终南山',y:590},{l:'洛阳',y:695},{l:'长安',y:700},
  {l:'五台山',y:790},{l:'杭州',y:1060},{l:'常熟/上海',y:1914},{l:'台北',y:1952}
];
var KEY_EVENTS=[
  {y:420,l:'六十华严译出(建康)',c:'#b8863c',p:'佛驮跋陀罗'},
  {y:699,l:'八十华严译出(洛阳)',c:'#b8863c',p:'实叉难陀'},
  {y:798,l:'四十华严译出(长安)',c:'#b8863c',p:'般若'},
  {y:845,l:'唐武宗灭佛·法难',c:'#c46b5d'},
  {y:1085,l:'义天入宋求法',c:'#6d9a6e',p:'义天'},
  {y:1914,l:'华严大学创立(上海)',c:'#5e8b9e',p:'月霞'},
  {y:1952,l:'华严莲社创社(台北)',c:'#5e8b9e',p:'成一'},
  {y:2008,l:'钦因传衣钵·三脉汇流',c:'#c46b5d',p:'海云继梦'}
];
var ERA_BRACKETS=[
  {label:'华严五祖时代',s:557,e:841},
  {label:'高丽华严传入',s:1085,e:1101},
  {label:'高原法系·明清中兴',s:1570,e:1700},
  {label:'华严大学·现代复兴',s:1858,e:1952},
  {label:'普贤乘·AI新时代',s:2008,e:2026}
];
var TYPE_ICONS={patriarch:'祖',translator:'译',scholar:'学',practitioner:'修'};

// ═══ HELPERS ═══
function getPersonLocs(pid){return DATA.locations.filter(function(l){return (l.ps||[]).indexOf(pid)>=0;});}
function getPersonById(id){return nodeMap[id]||null;}
function getRelatedIds(id){
  // Find all persons connected to id via any edge type
  var related={};related[id]=true;
  DATA.edges.forEach(function(e){
    if(e.s===id){related[e.t]=true;related[e.s]=true;}
    if(e.t===id){related[e.s]=true;related[e.t]=true;}
  });
  // Also add persons at same location
  var locs=getPersonLocs(id);
  locs.forEach(function(loc){
    (loc.ps||[]).forEach(function(pid){related[pid]=true;});
  });
  return related;
}
function calcStats(){
  var persons=DATA.nodes.filter(function(n){return n.b&&n.d;});
  if(!persons.length)return '';
  var ages=persons.map(function(n){return n.d-n.b;}).filter(function(a){return a>0&&a<120;});
  var avgAge=Math.round(ages.reduce(function(s,a){return s+a;},0)/ages.length);
  var span=Math.max.apply(null,persons.map(function(n){return n.d;}))-Math.min.apply(null,persons.map(function(n){return n.b;}));
  // Find longest gap between master death and student birth
  var maxGap=0;
  DATA.edges.filter(function(e){return e.r==='MASTER';}).forEach(function(e){
    var s=nodeMap[e.s],t=nodeMap[e.t];if(!s||!t||!s.d||!t.b)return;
    var gap=t.b-s.d;if(gap>maxGap)maxGap=gap;
  });
  return '👤47人 · 📅跨度'+span+'年 · ⏳最长传承间隙'+maxGap+'年';
}
function buildTimelineRows(){
  var order=["华严五祖","李通玄系","日本华严","高丽华严","贤首宗高原法系","月霞系","华严莲社","慈舟系","临济宗","译师","印度源流","当代学者"];
  var rows={}; order.forEach(function(l,i){rows[l]=i;});
  var rd=order.map(function(l){return {lineage:l,ps:[],y:0,color:DATA.lineage_colors[l]||"#b0a898"};});
  DATA.nodes.forEach(function(n){
    var ri=rows[n.li]!==undefined?rows[n.li]:order.length;
    if(!rd[ri])rd[ri]={lineage:n.li||"other",ps:[],y:0,color:DATA.lineage_colors[n.li]||"#b0a898"};
    n._isGhost=false; rd[ri].ps.push(n);
    if(n.multi&&n.multi.length){
      n.multi.forEach(function(ml){
        var mri=rows[ml]!==undefined?rows[ml]:order.length;
        if(!rd[mri])rd[mri]={lineage:ml,ps:[],y:0,color:DATA.lineage_colors[ml]||"#b0a898"};
        rd[mri].ps.push({id:n.id,n:n.n,dy:n.dy,ti:n.ti,li:ml,b:n.b,d:n.d,bio:n.bio,wk:n.wk,tp:n.tp,_isGhost:true,_primary:n});
      });
    }
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
  var isOverview=tl.scale<0.3;
  var hoverSet=hoveredId?getRelatedIds(hoveredId):null;

  // 0. THEORY EVOLUTION BAND
  if(layerVis.theory&&!isOverview){
    var thY=0,thH=26;
    THEORY_STAGES.forEach(function(ts){
      var x1=tX(ts.s),x2=tX(ts.e);
      if(x2>0&&x1<W){
        ctx.fillStyle=ts.c;ctx.fillRect(Math.max(0,x1),thY,Math.min(W,x2-x1),thH);
        ctx.fillStyle=ts.tc;ctx.font='11px Microsoft YaHei';
        var tw=ctx.measureText(ts.label).width;
        if(x2-x1>tw+10)ctx.fillText(ts.label,(x1+x2)/2-tw/2,thY+17);
      }
    });
    ctx.strokeStyle='#e0d8c8';ctx.lineWidth=0.5;
    ctx.beginPath();ctx.moveTo(0,thH);ctx.lineTo(W,thH);ctx.stroke();
    ctx.fillStyle='#a09080';ctx.font='9px Microsoft YaHei';ctx.fillText('理论演化',4,thH-4);
  }
  var topOff=layerVis.theory&&!isOverview?thH:0;

  // 1. DYNASTY BANDS + LABELS
  var dynasties=[{n:"唐",s:618,e:907,c:"rgba(200,160,80,0.06)"},{n:"宋",s:960,e:1279,c:"rgba(150,170,190,0.06)"},{n:"明",s:1368,e:1644,c:"rgba(160,150,140,0.04)"},{n:"清",s:1644,e:1912,c:"rgba(150,140,130,0.04)"},{n:"近现代",s:1912,e:1949,c:"rgba(200,150,140,0.08)"},{n:"当代",s:1949,e:2026,c:"rgba(150,190,190,0.08)"}];
  dynasties.forEach(function(d){var x=tX(d.s),x2=tX(d.e);if(x2>0&&x<W){ctx.fillStyle=d.c;ctx.fillRect(Math.max(0,x),topOff,Math.min(W,x2-x),H-topOff);}});
  if(!isOverview){
    dynasties.forEach(function(d){
      var x=tX(d.s),x2=tX(d.e),cx=(x+x2)/2;
      if(x2-x>60&&cx>0&&cx<W){
        ctx.fillStyle='rgba(160,144,128,0.35)';ctx.font='bold 13px Microsoft YaHei';
        ctx.fillText(d.n,cx-13,topOff+16);
      }
    });
  }

  // 2. CENTURY GRID
  ctx.strokeStyle="#e8e0d0";ctx.lineWidth=0.5;ctx.setLineDash([3,6]);
  for(var y=200;y<=2050;y+=100){var x=tX(y);if(x>=0&&x<=W){ctx.beginPath();ctx.moveTo(x,topOff);ctx.lineTo(x,H);ctx.stroke();}}
  ctx.setLineDash([]);

  // 3. PRACTICE LINEAGE BAND
  var pracOff=0;
  if(layerVis.practice&&!isOverview){
    pracOff=22;
    var py=topOff+4;
    PRACTICE_STAGES.forEach(function(ps){
      var x1=tX(ps.s),x2=tX(ps.e);
      if(x2>0&&x1<W){
        ctx.fillStyle=ps.c;ctx.fillRect(Math.max(0,x1),py,Math.min(W,x2-x1),pracOff-6);
        ctx.fillStyle=ps.tc;ctx.font='10px Microsoft YaHei';
        var tw2=ctx.measureText(ps.label).width;
        if(x2-x1>tw2+10)ctx.fillText(ps.label,(x1+x2)/2-tw2/2,py+13);
      }
    });
    ctx.strokeStyle='#e0d8c8';ctx.lineWidth=0.5;
    ctx.beginPath();ctx.moveTo(0,py+pracOff-4);ctx.lineTo(W,py+pracOff-4);ctx.stroke();
    ctx.fillStyle='#a09080';ctx.font='9px Microsoft YaHei';ctx.fillText('修行谱系',4,py-2);
  }

  // 4. ROW BACKGROUNDS AND LABELS (with clickable era brackets)
  var personTop=topOff+pracOff;
  tl.rowLabels=[];
  tl.rows.forEach(function(r,i){
    r.y=i*rh+rh/2+personTop;
    var y0=i*rh+personTop, y2=r.y;
    if(i%2===0){ctx.fillStyle="rgba(255,255,255,0.25)";ctx.fillRect(0,y0,W,rh);}
    // Row label - track for click detection
    var lw=ctx.measureText(r.lineage).width;
    ctx.fillStyle=r.color;ctx.font="600 12px Microsoft YaHei";ctx.fillText(r.lineage,10,y0+18);
    ctx.strokeStyle="#e8e0d0";ctx.lineWidth=0.5;ctx.beginPath();ctx.moveTo(0,y0+rh);ctx.lineTo(W,y0+rh);ctx.stroke();
    // Clickable row label area
    tl.rowLabels.push({x:0,y:y0,w:Math.max(lw+20,100),h:rh,lineage:r.lineage,persons:r.ps});
    // Era bracket on selected lineage row
    if(!isOverview){
      ERA_BRACKETS.forEach(function(eb){
        var bx=tX(eb.s),bx2=tX(eb.e);
        if(bx2>0&&bx<W){
          var byc=y0+rh/2;
          ctx.strokeStyle=r.color+'60';ctx.lineWidth=2;
          ctx.beginPath();ctx.moveTo(bx,byc-6);ctx.lineTo(bx,byc+6);ctx.stroke();
          ctx.beginPath();ctx.moveTo(bx2,byc-6);ctx.lineTo(bx2,byc+6);ctx.stroke();
          if(bx2-bx>80){
            ctx.fillStyle=r.color+'50';ctx.font='9px Microsoft YaHei';
            ctx.fillText(eb.label,(bx+bx2)/2-ctx.measureText(eb.label).width/2,byc-3);
          }
        }
      });
    }
  });

  // 5. PERSON LIFESPAN BARS
  tl.hitRects=[];var ds=25,isSearch=searchQuery.length>0;
  tl.rows.forEach(function(r,ri){
    var sorted=r.ps.slice().sort(function(a,b){return (a.b||a.d||0)-(b.b||b.d||0);});
    var slots=[];
    sorted.forEach(function(p){
      var b=p.b||(p.d?p.d-ds:null),d=p.d||(p.b?p.b+ds:null);if(!b&&!d)return;
      var bx=tX(b||d-10),dx=tX(d||b+10),bw=Math.max(6,dx-bx);
      var level=0,placed=false;
      while(!placed&&level<3){
        var overlap=false;
        if(!slots[level])slots[level]=[];
        for(var s=0;s<slots[level].length;s++){
          if(!(bx+bw+20<slots[level][s].x || bx>slots[level][s].x+slots[level][s].w+20)){overlap=true;break;}
        }
        if(!overlap){slots[level].push({x:bx,w:bw});placed=true;}
        else level++;
      }
      p._yOff=(level-1)*14;
    });
  });
  tl.rows.forEach(function(r,ri){var y2=r.y;
    r.ps.forEach(function(p){
      var b=p.b||(p.d?p.d-ds:null),d=p.d||(p.b?p.b+ds:null);if(!b&&!d)return;
      var bx=tX(b||d-10),dx=tX(d||b+10),bh=Math.min(22,rh*0.35),by=y2-bh/2+(p._yOff||0);
      var isHL=p.id===hlId,matches=!isSearch||p.n.indexOf(searchQuery)>=0;
      // Hover dimming
      var hoverDim=hoverSet&&!hoverSet[p.id];
      if(isSearch&&!matches)ctx.globalAlpha=0.12;
      else if(hlId&&!isHL)ctx.globalAlpha=hoverDim?0.12:0.18;
      else ctx.globalAlpha=hoverDim?0.2:1;
      if(isHL){ctx.shadowColor="#b8863c";ctx.shadowBlur=16;}

      if(p._isGhost){bh=Math.max(4,bh*0.4);by=y2-bh/2;ctx.globalAlpha=hoverDim?0.1:0.5;ctx.setLineDash([3,3]);ctx.fillStyle=r.color+"40";ctx.strokeStyle=r.color;ctx.lineWidth=1;}
      else{ctx.fillStyle=isHL?"#c46b5d":(r.color+"DD");}
      var rx=Math.max(0,bx),rw=Math.max(6,dx-rx);
      ctx.beginPath();ctx.moveTo(rx+4,by);ctx.lineTo(rx+rw-4,by);ctx.quadraticCurveTo(rx+rw,by,rx+rw,by+4);ctx.lineTo(rx+rw,by+bh-4);ctx.quadraticCurveTo(rx+rw,by+bh,rx+rw-4,by+bh);ctx.lineTo(rx+4,by+bh);ctx.quadraticCurveTo(rx,by+bh,rx,by+bh-4);ctx.lineTo(rx,by+4);ctx.quadraticCurveTo(rx,by,rx+4,by);ctx.closePath();
      if(p._isGhost){ctx.stroke();}else{ctx.fill();}
      ctx.setLineDash([]);ctx.shadowColor="transparent";ctx.shadowBlur=0;ctx.globalAlpha=1;

      // Type icon + name label
      if(!isSearch||matches){
        var labelAbove=(p._yOff||0)<=0;
        var labelY=labelAbove?by-5:by+bh+13;
        var ti=TYPE_ICONS[p.tp]||'';
        ctx.fillStyle=isHL?"#c46b5d":(p._isGhost?r.color:"#5c5040");
        ctx.font=(isHL?"bold ":"")+(p._isGhost?8:(isHL?12:10))+"px Microsoft YaHei";
        var prefix=p._isGhost?'↳ ':ti?'['+ti+'] ':'';
        ctx.fillText(prefix+p.n,rx+rw+6,labelY);
      }
      if(!p._isGhost)tl.hitRects.push({x:rx,y:by,w:rw,h:bh,person:p});
    });
  });

  // 6. EDGES (death→birth bezier, color-coded)
  if(layerVis.edges){
    var relColors={MASTER:'#b8863c',LINEAGE:'#7d9a6e',INFLUENCED:'#5e8b9e',CONTEMPORARY:'#c0b098'};
    var relDash={MASTER:[],LINEAGE:[5,4],INFLUENCED:[3,5],CONTEMPORARY:[2,4]};
    DATA.edges.forEach(function(e){
      var sHR=tl.hitRects.find(function(h){return h.person.id===e.s;});
      var tHR=tl.hitRects.find(function(h){return h.person.id===e.t;});
      if(!sHR||!tHR)return;
      var isHL=e.s===hlId||e.t===hlId||(hoverSet&&(hoverSet[e.s]||hoverSet[e.t]));
      var rc=relColors[e.r]||'#d5cdc0';
      ctx.strokeStyle=isHL?((e.r==='MASTER')?'#c46b5d':'#5e8b9e'):rc;
      ctx.lineWidth=isHL?2.4:(e.r==='MASTER'?1.8:1.0);
      ctx.globalAlpha=isHL?1:(hoverSet?0.15:(e.r==='MASTER'?0.55:0.3));
      ctx.setLineDash(relDash[e.r]||[]);
      var sp=sHR.person,tp=tHR.person;
      var sx=sp.d?tX(sp.d):(sHR.x+sHR.w);
      var sy=sHR.y+sHR.h/2;
      var ex=tp.b?tX(tp.b):tHR.x;
      var ey=tHR.y+tHR.h/2;
      if(sp.d){ctx.beginPath();ctx.arc(sx,sy,isHL?3.5:2.5,0,Math.PI*2);ctx.fillStyle=isHL?'#c46b5d':rc;ctx.fill();}
      ctx.beginPath();ctx.moveTo(sx,sy);
      ctx.bezierCurveTo(sx+(ex-sx)*0.4,sy,ex-(ex-sx)*0.4,ey,ex,ey);
      ctx.stroke();
      if(tp.b&&ex>sx+10){
        ctx.beginPath();ctx.moveTo(ex,ey);ctx.lineTo(ex-6,ey-4);ctx.lineTo(ex-6,ey+4);ctx.closePath();ctx.fillStyle=isHL?'#c46b5d':rc;ctx.fill();
      }
      ctx.setLineDash([]);ctx.globalAlpha=1;
    });
  }

  // 7. GEOGRAPHIC MARKERS
  if(layerVis.geo&&!isOverview){
    GEO_FLOW.forEach(function(gf,i){
      var x=tX(gf.y);if(x<0||x>W)return;
      ctx.fillStyle='#c46b5d';ctx.font='bold 10px Microsoft YaHei';
      var ly=tl.rows.length*rh+personTop+4;
      ctx.fillText('📍',x-7,ly+10);
      if(i<GEO_FLOW.length-1){
        var nx=tX(GEO_FLOW[i+1].y);
        if(nx<W){
          ctx.strokeStyle='rgba(196,107,93,0.2)';ctx.lineWidth=1;ctx.setLineDash([4,6]);
          ctx.beginPath();ctx.moveTo(x,ly+8);ctx.lineTo(nx,ly+8);ctx.stroke();
          ctx.setLineDash([]);
        }
      }
    });
    var locY=tl.rows.length*rh+personTop+24;var seen={};
    DATA.locations.forEach(function(loc){
      if(!loc.ps||!loc.ps.length)return;
      var p=nodeMap[loc.ps[0]];if(!p||!p.b)return;
      var lx=tX(p.b);if(lx<0||lx>W||seen[loc.id])return;seen[loc.id]=true;
      ctx.fillStyle='#8b6b4a';ctx.font='8px Microsoft YaHei';
      ctx.fillText('▾ '+loc.n,lx-10,locY);locY+=13;
    });
  }

  // 8. EVENT MARKERS
  if(layerVis.events&&!isOverview){
    var evY=H-24;
    KEY_EVENTS.forEach(function(ev){
      var x=tX(ev.y);if(x<0||x>W)return;
      if(ev.p&&layerVis.edges){
        var pHR=tl.hitRects.find(function(h){return h.person.n===ev.p||h.person.id===ev.p;});
        if(pHR){
          ctx.strokeStyle='rgba(180,134,60,0.25)';ctx.lineWidth=1;ctx.setLineDash([2,5]);
          ctx.beginPath();ctx.moveTo(x,evY);ctx.lineTo(pHR.x+pHR.w/2,pHR.y+pHR.h);ctx.stroke();
          ctx.setLineDash([]);
        }
      }
      ctx.fillStyle=ev.c;ctx.font='bold 9px Microsoft YaHei';
      ctx.fillText('▸ '+ev.l,x,evY);
    });
    ctx.fillStyle='#a09080';ctx.font='10px Microsoft YaHei';
    for(var yy=200;yy<=2000;yy+=100){var x2=tX(yy);if(x2>=0&&x2<=W)ctx.fillText(yy,x2-12,H-8);}
  }

  // 9. SEMANTIC ZOOM
  if(isOverview){
    ctx.fillStyle='rgba(45,35,25,0.7)';ctx.font='bold 16px Microsoft YaHei';
    ctx.fillText('🔍 千年全景 — 滚轮放大查看人物细节',W/2-160,personTop+40);
    var centuries=[];for(var c=500;c<=2000;c+=100){var count=0;DATA.nodes.forEach(function(n){if(n.b&&n.b>=c&&n.b<c+100)count++;});if(count>0)centuries.push({c:c,count:count});}
    var maxC=Math.max.apply(null,centuries.map(function(c){return c.count;}));
    var heatY=personTop+80,heatH=60;
    centuries.forEach(function(ct){
      var cx=tX(ct.c+50),bw=Math.max(8,(ct.c+100-ct.c)*tl.scale*0.6);
      var bh=(ct.count/maxC)*heatH;
      var alpha=0.15+(ct.count/maxC)*0.5;
      ctx.fillStyle='rgba(184,134,60,'+alpha+')';ctx.fillRect(cx-bw/2,heatY+heatH-bh,bw,bh);
      ctx.fillStyle='#8a7060';ctx.font='9px Microsoft YaHei';ctx.fillText(ct.count+'人',cx-8,heatY+heatH-bh-4);
    });
  }
}

// ═══ MAP ═══
function initMap(){
  if(map){map.invalidateSize();return;}
  if(typeof L==="undefined"){document.getElementById("map").innerHTML="<div style=display:flex;align-items:center;justify-content:center;height:100%;color:var(--text2);flex-direction:column;gap:8px'><div>🗺 地图组件未加载</div><div style=font-size:0.7em>Leaflet CDN 不可用，请检查网络</div></div>";return;}
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
  // Zoom to person's era
  var p=nodeMap[id];if(p&&p.b){
    var rng=(p.d||p.b+50)-p.b;tl.minX=p.b-rng*0.3;tl.maxX=(p.d||p.b+50)+rng*0.7;
    tl.scale=(tl.W-40)/(tl.maxX-tl.minX);tl.ox=20;
  }
  drawTL(selectedId);if(selectedId2)drawTL2(selectedId2);
  showInfo(nodeMap[selectedId],selectedId2?nodeMap[selectedId2]:null);
  // Map sync
  var locs=getPersonLocs(id);
  if(map&&locs.length>0){
    var loc=locs[0];map.flyTo([loc.lat,loc.lng],locs.length===1?10:8,{duration:0.8});
    setTimeout(function(){
      map.eachLayer(function(layer){
        if(!layer._ld)return;
        var isRelated=locs.some(function(l){return l.id===layer._ld.id;});
        if(isRelated){layer.setRadius(13);layer.setStyle({fillColor:"#c46b5d",color:"#fff",weight:3,fillOpacity:1});if(!layer._popupOpen){layer.openPopup();layer._popupOpen=true;setTimeout(function(){layer.closePopup();layer._popupOpen=false;},3000);}}
        else{layer.setRadius(7);layer.setStyle({fillOpacity:0.5});}
      });
    },900);
    setTimeout(function(){
      map.eachLayer(function(layer){if(!layer._ld)return;var mc={temple:"#b8863c",mountain:"#7d9a6e",region:"#c46b5d"};layer.setRadius(9);layer.setStyle({fillColor:mc[layer._ld.tp]||"#b0a898",color:"#fff",weight:2,fillOpacity:0.9});});
    },4000);
  }
  // Update stats bar
  var sb=document.getElementById("stats-bar");if(sb)sb.textContent=calcStats();
}
function clearSelection(){selectedId=null;selectedId2=null;drawTL(null);document.getElementById("info-box").innerHTML="<div class=empty>👆 点击人物寿命条查看详情<br><span style=font-size:0.8em>Shift+点击第二人可并排对比</span></div>";var sb=document.getElementById("stats-bar");if(sb)sb.textContent=calcStats();}
function drawTL2(id){}

// ═══ ENHANCED INFO PANEL ═══
function showInfo(p,p2){
  if(!p)return;var box=document.getElementById("info-box");if(!box)return;
  var lc=DATA.lineage_colors[p.li]||"#b0a898";
  var locs=getPersonLocs(p.id),locHTML="";
  locs.forEach(function(l){locHTML+="📍 "+l.n+"<br>";});
  var teachers=DATA.edges.filter(function(e){return e.t===p.id&&e.r==="MASTER";}).map(function(e){return nodeMap[e.s];}).filter(Boolean);
  var students=DATA.edges.filter(function(e){return e.s===p.id&&e.r==="MASTER";}).map(function(e){return nodeMap[e.t];}).filter(Boolean);
  // Also find all connected persons (any edge type)
  var allConns={};DATA.edges.forEach(function(e){if(e.s===p.id)allConns[e.t]=e.r;if(e.t===p.id)allConns[e.s]=e.r;});
  // Generation number approximation
  var gen=0,tmp=p;while(tmp){var next=teachers.find(function(t){return t.id!==tmp.id;});if(!next){var prev=DATA.edges.filter(function(e){return e.t===tmp.id&&e.r==="MASTER";});next=prev.length?nodeMap[prev[0].s]:null;}if(!next)break;tmp=next;gen++;}
  var lifeSpan=(p.b&&p.d)?('享年'+(p.d-p.b)+'岁 · '):'';
  var tch=teachers.length?"⬆ 师承("+teachers.length+"): "+teachers.map(function(t){return t.n;}).join("、")+"<br>":"";
  var std=students.length?"⬇ 传法("+students.length+"): "+students.map(function(t){return t.n;}).join("、")+"<br>":"";
  var allC=Object.keys(allConns).length?'🔗 关联('+Object.keys(allConns).length+'): 师徒/影响/同代<br>':'';
  var contemp=DATA.nodes.filter(function(n){return n.dy===p.dy&&n.id!==p.id&&n.li===p.li;}).slice(0,3);
  var cont=contemp.length?"👥 同代: "+contemp.map(function(n){return n.n;}).join("、")+"<br>":"";
  var ti=TYPE_ICONS[p.tp]||'';
  var h="<h3>"+(ti?'['+ti+'] ':'')+p.n+" <span style=font-size:0.7em;color:var(--text2)>"+(p.ti||"")+"</span></h3>"
    +"<span class=tag style=background:"+lc+"20;color:"+lc+">"+(p.li||"—")+"</span>"
    +"<span class=tag style=background:rgba(0,0,0,0.04)>"+(p.tp==="patriarch"?"祖师":p.tp==="translator"?"译师":p.tp==="scholar"?"学者":"行者")+"</span>"
    +(gen?'<span class=tag style=background:rgba(184,134,60,0.06)>第'+gen+'代传人</span>':'')+"<br>"
    +"📅 <b>"+(p.dy||"?")+"</b> · "+(p.b||"?")+"–"+(p.d||"?")+" "+lifeSpan+"<br>"
    +locHTML+tch+std+allC+cont
    +(p.bio?"<div style=color:var(--text2);line-height:1.5;margin-top:4px;padding-top:4px;border-top:1px solid var(--line)>"+p.bio+"</div>":"")
    +(p.wk&&p.wk.length?"<div style=margin-top:4px>📖 <b>"+p.wk.join("</b> · <b>")+"</b></div>":"");
  if(p2){
    var lc2=DATA.lineage_colors[p2.li]||"#b0a898";var ti2=TYPE_ICONS[p2.tp]||'';
    h+="<div style='margin-top:10px;padding-top:8px;border-top:2px solid var(--gold)'><h3 style=color:#5e8b9e>"+(ti2?'['+ti2+'] ':'')+p2.n+" <span style=font-size:0.7em;color:var(--text2)>"+(p2.ti||"")+"</span></h3>"
      +"<span class=tag style=background:"+lc2+"20;color:"+lc2+">"+(p2.li||"—")+"</span>"
      +"📅 <b>"+(p2.dy||"?")+"</b> · "+(p2.b||"?")+"–"+(p2.d||"?")+"<br>"
      +(p2.bio?"<div style=color:var(--text2)>"+p2.bio+"</div>":"")+"</div>";
  }
  box.innerHTML=h;
}

// ═══ LAYER TOGGLE ═══
function toggleLayer(layer){
  layerVis[layer]=!layerVis[layer];
  var btn=document.querySelector('#controls button[data-layer="'+layer+'"]');
  if(btn){if(layerVis[layer]){btn.classList.add('active');}else{btn.classList.remove('active');}}
  drawTL(selectedId);
}

// ═══ LINEAGE ZOOM ═══
function zoomToLineage(lineage){
  var row=tl.rows.find(function(r){return r.lineage===lineage;});
  if(!row||!row.ps.length)return;
  var births=row.ps.map(function(p){return p.b;}).filter(Boolean);
  var deaths=row.ps.map(function(p){return p.d;}).filter(Boolean);
  if(!births.length)return;
  var minB=Math.min.apply(null,births),maxD=Math.max.apply(null,deaths.length?deaths:births);
  tl.minX=minB-30;tl.maxX=maxD+30;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);
  drawTL(selectedId);
}

// ═══ INTERACTION ═══
function onWheel(e){e.preventDefault();var p=document.getElementById("tl-panel");var r=p.getBoundingClientRect();var mx=e.clientX-r.left;var before=(mx-tl.ox)/tl.scale;tl.scale*=e.deltaY<0?1.12:0.89;tl.scale=Math.max(0.12,Math.min(6,tl.scale));tl.ox=mx-before*tl.scale;drawTL(selectedId);}
function onMD(e){if(e.target.tagName==="CANVAS"){tl.drag=true;tl.lastX=e.clientX;}}
function onMM(e){
  var p=document.getElementById("tl-panel"),r=p.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  if(!tl.drag){
    var hit=tl.hitRects.find(function(h){return mx>=h.x&&mx<=h.x+h.w&&my>=h.y&&my<=h.y+h.h;});
    var tip=document.getElementById("tl-tooltip");
    if(hit){var pp=hit.person;
      // Set hover state
      if(hoveredId!==pp.id){hoveredId=pp.id;drawTL(selectedId);}
      // Enhanced tooltip
      var ti=TYPE_ICONS[pp.tp]||'';var lc=DATA.lineage_colors[pp.li]||"#b0a898";
      var locs=getPersonLocs(pp.id);var locTxt=locs.length?'📍 '+locs[0].n:'';
      var ageTxt=(pp.b&&pp.d)?' ('+(pp.d-pp.b)+'岁)':'';
      var stuCount=DATA.edges.filter(function(e){return e.s===pp.id&&e.r==="MASTER";}).length;
      var tchCount=DATA.edges.filter(function(e){return e.t===pp.id&&e.r==="MASTER";}).length;
      var relTxt='';if(tchCount||stuCount)relTxt='⬆'+tchCount+' ⬇'+stuCount+' · ';
      tip.style.opacity="1";
      tip.innerHTML="<h3>"+(ti?'['+ti+'] ':'')+pp.n+"</h3><span style=color:"+lc+">"+pp.li+"</span> · "+pp.dy+" · "+(pp.b||"?")+"–"+(pp.d||"?")+ageTxt+"<br>"+locTxt+" · "+relTxt+(pp.ti||"")+(pp.wk&&pp.wk.length?"<br>📖 "+pp.wk.slice(0,2).join(" · "):"");
      tip.style.left=(e.pageX+14)+"px";tip.style.top=(e.pageY-20)+"px";
    }else{
      if(hoveredId){hoveredId=null;drawTL(selectedId);}
      tip.style.opacity="0";
    }
    return;
  }
  var dx=e.clientX-tl.lastX;tl.ox+=dx;tl.lastX=e.clientX;drawTL(selectedId);
}
function onMU(){tl.drag=false;}
function onClick(e){
  if(tl.drag||Math.abs(e.clientX-tl.lastX)>3)return;
  var p=document.getElementById("tl-panel"),r=p.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  // Check row label clicks first
  for(var i=0;i<tl.rowLabels.length;i++){
    var rl=tl.rowLabels[i];
    if(mx>=rl.x&&mx<=rl.x+rl.w&&my>=rl.y&&my<=rl.y+rl.h){
      zoomToLineage(rl.lineage);return;
    }
  }
  // Check person hit rects
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
if(location.hash){var h=location.hash.slice(1);if(document.getElementById("tab-"+h))switchTab(h);}
