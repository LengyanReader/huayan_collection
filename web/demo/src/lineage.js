// ═══ DATA LAYERS ═══
var layerVis={theory:true,geo:true,practice:true,edges:true,events:true};
// Multi-layer civilization colors for animation routes & popups
var REL_COLORS={
  buddhist:'#c46b5d',      // 佛教·华严
  indic:'#e08040',          // 南亚·印度
  confucian:'#b8863c',      // 儒家
  daoist:'#7d9a6e',         // 道家
  western:'#5e8b9e',        // 西方
  islamic:'#4a9e8e',        // 伊斯兰
  african:'#c8893e',        // 非洲
  american:'#d48476',       // 美洲
  oceanic:'#8b7a9e'         // 大洋洲
};
var REL_LABELS={
  buddhist:'佛教·华严',
  indic:'南亚·印度',
  confucian:'儒家',
  daoist:'道家',
  western:'西方',
  islamic:'伊斯兰',
  african:'非洲',
  american:'美洲',
  oceanic:'大洋洲'
};
// EN name display — SQLite persons name_en(拼音)/name_sa(梵文) 经 db_reader GRAPH 注入
function _enName(p){if(!p)return '';p=p._primary||p;return (p.name_en||p.name_sa||'');}
function _enNameHtml(p,inline){
  var en=_enName(p);if(!en)return '';
  return inline
    ? '<span class="en-line" style="color:var(--text2);font-size:0.85em;font-weight:400"> '+en+'</span>'
    : '<div class="en-line" style="color:var(--text2);font-size:0.82em;font-weight:400;margin:1px 0 4px">'+en+'</div>';
}
// Data-driven stage arrays: injected globals (from data/events/*.yaml via build.py)
// carry the content wrapped under a key; unwrap here so any hardcoded literal is avoided.
THEORY_STAGES=(typeof THEORY_STAGES!=='undefined'&&THEORY_STAGES&&THEORY_STAGES.stages)?THEORY_STAGES.stages:[];
PRACTICE_STAGES=(typeof PRACTICE_STAGES!=='undefined'&&PRACTICE_STAGES&&PRACTICE_STAGES.stages)?PRACTICE_STAGES.stages:[];
GEO_FLOW=(typeof GEO_FLOW!=='undefined'&&GEO_FLOW&&GEO_FLOW.flow)?GEO_FLOW.flow:[];
KEY_EVENTS=(typeof KEY_EVENTS!=='undefined'&&KEY_EVENTS&&KEY_EVENTS.events)?KEY_EVENTS.events:[];
ERA_BRACKETS=(typeof ERA_BRACKETS!=='undefined'&&ERA_BRACKETS&&ERA_BRACKETS.brackets)?ERA_BRACKETS.brackets:[];
var TYPE_ICONS={patriarch:'祖',translator:'译',scholar:'学',practitioner:'修'};

// ═══ HELPERS ═══
function getPersonLocs(pid){return DATA.locations.filter(function(l){return (l.ps||[]).indexOf(pid)>=0;});}
function getPersonById(id){return nodeMap[id]||null;}
function getRelatedIds(id){
  var related={};related[id]=true;
  DATA.edges.forEach(function(e){
    if(e.s===id){related[e.t]=true;related[e.s]=true;}
    if(e.t===id){related[e.s]=true;related[e.t]=true;}
  });
  var locs=getPersonLocs(id);
  locs.forEach(function(loc){(loc.ps||[]).forEach(function(pid){related[pid]=true;});});
  return related;
}
function calcStats(){
  var persons=DATA.nodes.filter(function(n){return n.b&&n.d;});
  if(!persons.length)return '';
  var span=Math.max.apply(null,persons.map(function(n){return n.d;}))-Math.min.apply(null,persons.map(function(n){return n.b;}));
  var maxGap=0;
  DATA.edges.filter(function(e){return e.r==='MASTER';}).forEach(function(e){
    var s=nodeMap[e.s],t=nodeMap[e.t];if(!s||!t||!s.d||!t.b)return;
    var gap=t.b-s.d;if(gap>maxGap)maxGap=gap;
  });
  return '👤'+DATA.nodes.length+'人 · 🔗'+DATA.edges.length+'边 · 📅跨度'+span+'年 · ⏳最长间隙'+maxGap+'年';
}
// Text truncation helper
function truncText(ctx,text,maxW){
  if(ctx.measureText(text).width<=maxW)return text;
  for(var i=text.length-1;i>0;i--){if(ctx.measureText(text.substring(0,i)+'…').width<=maxW)return text.substring(0,i)+'…';}
  return '';
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

// ═══ CANVAS (HiDPI-aware) ═══
var MIN_ROW_H=64, dps=1; // devicePixelRatio scale
function resizeTL(){
  var p=document.getElementById("tl-panel");
  tl.W=p.clientWidth; var rows=tl.rows.length||1;
  // Mobile: ensure enough height for all rows
  var minH=window.innerWidth<768?rows*50+20:rows*MIN_ROW_H+20;
  tl.H=Math.max(p.clientHeight,minH);
  dps=window.devicePixelRatio||1;
  // Cap DPR on mobile for performance
  if(window.innerWidth<768&&dps>2)dps=2;
  tl.canvas=document.getElementById("tl-canvas");
  tl.canvas.width=tl.W*dps; tl.canvas.height=tl.H*dps;
  tl.canvas.style.width=tl.W+"px"; tl.canvas.style.height=tl.H+"px";
  tl.ctx=tl.canvas.getContext("2d");
  tl.ctx.scale(dps,dps);
}
function tX(y){return (y-tl.minX)*tl.scale+tl.ox;}

// ═══ FONT HELPERS (minimum 10px for legibility) ═══
function f10b(){return 'bold 10px Microsoft YaHei';}
function f11b(){return 'bold 11px Microsoft YaHei';}
function f12b(){return 'bold 12px Microsoft YaHei';}
function f13b(){return 'bold 13px Microsoft YaHei';}
function f9(){return '9px Microsoft YaHei';}
function f10(){return '10px Microsoft YaHei';}
function f11(){return '11px Microsoft YaHei';}
function f12(){return '12px Microsoft YaHei';}

function drawTL(hlId){
  var ctx=tl.ctx,W=tl.W,H=tl.H;if(!ctx)return;ctx.clearRect(0,0,W,H);
  var rh=Math.max(MIN_ROW_H,H/Math.max(tl.rows.length,1));
  var isOverview=tl.scale<0.3;
  var hoverSet=hoveredId?getRelatedIds(hoveredId):null;

  // 0. THEORY EVOLUTION BAND
  if(layerVis.theory&&!isOverview){
    var thY=0,thH=28;
    THEORY_STAGES.forEach(function(ts){
      var x1=tX(ts.s),x2=tX(ts.e);
      if(x2>0&&x1<W&&x2-x1>4){
        ctx.fillStyle=ts.c;ctx.fillRect(Math.max(0,x1),thY,Math.min(W,x2-x1),thH);
        ctx.fillStyle=ts.tc;ctx.font=f11();
        var txt=truncText(ctx,ts.label,x2-x1-6);
        if(txt)ctx.fillText(txt,(x1+x2)/2-ctx.measureText(txt).width/2,thY+19);
      }
    });
    ctx.strokeStyle='#e0d8c8';ctx.lineWidth=0.5;
    ctx.beginPath();ctx.moveTo(0,thH);ctx.lineTo(W,thH);ctx.stroke();
    ctx.fillStyle='#a09080';ctx.font=f10();ctx.fillText('理论演化',4,thH-6);
  }
  var topOff=layerVis.theory&&!isOverview?thH:0;

  // 1. DYNASTY BANDS + LABELS (collision-aware)
  var dynasties=[{n:"唐",s:618,e:907,c:"rgba(200,160,80,0.06)"},{n:"宋",s:960,e:1279,c:"rgba(150,170,190,0.06)"},{n:"明",s:1368,e:1644,c:"rgba(160,150,140,0.04)"},{n:"清",s:1644,e:1912,c:"rgba(150,140,130,0.04)"},{n:"近现代",s:1912,e:1949,c:"rgba(200,150,140,0.08)"},{n:"当代",s:1949,e:2026,c:"rgba(150,190,190,0.08)"}];
  dynasties.forEach(function(d){var x=tX(d.s),x2=tX(d.e);if(x2>0&&x<W){ctx.fillStyle=d.c;ctx.fillRect(Math.max(0,x),topOff,Math.min(W,x2-x),H-topOff);}});
  if(!isOverview){
    var lastLabelX=-999;
    dynasties.forEach(function(d){
      var x=tX(d.s),x2=tX(d.e),cx=(x+x2)/2;
      if(x2-x>50&&cx>0&&cx<W&&cx-lastLabelX>40){
        ctx.fillStyle='rgba(160,144,128,0.35)';ctx.font=f13b();
        ctx.fillText(d.n,cx-13,topOff+16);
        lastLabelX=cx;
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
    pracOff=24;
    var py=topOff+4;
    PRACTICE_STAGES.forEach(function(ps){
      var x1=tX(ps.s),x2=tX(ps.e);
      if(x2>0&&x1<W&&x2-x1>4){
        ctx.fillStyle=ps.c;ctx.fillRect(Math.max(0,x1),py,Math.min(W,x2-x1),pracOff-6);
        ctx.fillStyle=ps.tc;ctx.font=f10();
        var txt2=truncText(ctx,ps.label,x2-x1-6);
        if(txt2)ctx.fillText(txt2,(x1+x2)/2-ctx.measureText(txt2).width/2,py+14);
      }
    });
    ctx.strokeStyle='#e0d8c8';ctx.lineWidth=0.5;
    ctx.beginPath();ctx.moveTo(0,py+pracOff-4);ctx.lineTo(W,py+pracOff-4);ctx.stroke();
    ctx.fillStyle='#a09080';ctx.font=f10();ctx.fillText('修行谱系',4,py-2);
  }

  // 4. ROW BACKGROUNDS (era brackets only on relevant rows)
  var personTop=topOff+pracOff;
  tl.rowLabels=[];
  // Pre-compute which rows are relevant for each era bracket
  var eraRowMap={};
  ERA_BRACKETS.forEach(function(eb,ei){
    var bestRow=-1,bestCount=0;
    tl.rows.forEach(function(r,ri){
      var cnt=0;r.ps.forEach(function(p){if(p.b&&p.b>=eb.s&&p.b<=eb.e)cnt++;});
      if(cnt>bestCount){bestCount=cnt;bestRow=ri;}
    });
    eraRowMap[ei]=bestRow>=0?bestRow:0;
  });

  tl.rows.forEach(function(r,i){
    r.y=i*rh+rh/2+personTop;
    var y0=i*rh+personTop, y2=r.y;
    if(i%2===0){ctx.fillStyle="rgba(255,255,255,0.25)";ctx.fillRect(0,y0,W,rh);}
    // Row label
    ctx.fillStyle=r.color;ctx.font="600 12px Microsoft YaHei";ctx.fillText(r.lineage,10,y0+18);
    ctx.strokeStyle="#e8e0d0";ctx.lineWidth=0.5;ctx.beginPath();ctx.moveTo(0,y0+rh);ctx.lineTo(W,y0+rh);ctx.stroke();
    tl.rowLabels.push({x:0,y:y0,w:Math.max(ctx.measureText(r.lineage).width+20,100),h:rh,lineage:r.lineage,persons:r.ps});
    // Era brackets ONLY on the most relevant row
    if(!isOverview){
      ERA_BRACKETS.forEach(function(eb,ei){
        if(eraRowMap[ei]!==i)return;
        var bx=tX(eb.s),bx2=tX(eb.e);
        if(bx2>0&&bx<W&&bx2-bx>30){
          var byc=y0+rh/2;
          ctx.strokeStyle=r.color+'50';ctx.lineWidth=1.5;
          ctx.beginPath();ctx.moveTo(bx,byc-5);ctx.lineTo(bx,byc+5);ctx.stroke();
          ctx.beginPath();ctx.moveTo(bx2,byc-5);ctx.lineTo(bx2,byc+5);ctx.stroke();
          if(bx2-bx>90){
            ctx.fillStyle=r.color+'55';ctx.font=f10();
            var tw=ctx.measureText(eb.label).width;
            ctx.fillText(eb.label,(bx+bx2)/2-tw/2,byc-3);
          }
        }
      });
    }
  });

  // 5. PERSON LIFESPAN BARS (improved collision: ±28px range, left-side labels)
  tl.hitRects=[];var ds=25,isSearch=searchQuery.length>0;
  tl.rows.forEach(function(r,ri){
    var sorted=r.ps.slice().sort(function(a,b){return (a.b||a.d||0)-(b.b||b.d||0);});
    var slots=[],noDateCount=0;
    sorted.forEach(function(p){
      var b=p.b||(p.d?p.d-ds:null),d=p.d||(p.b?p.b+ds:null);
      if(!b&&!d){p._yOff=noDateCount*14;noDateCount++;return;} // staggered diamond markers
      var bx=tX(b||d-10),dx=tX(d||b+10),bw=Math.max(6,dx-bx);
      var level=0,placed=false;
      while(!placed&&level<4){
        var overlap=false;
        if(!slots[level])slots[level]=[];
        for(var s=0;s<slots[level].length;s++){
          if(!(bx+bw+24<slots[level][s].x || bx>slots[level][s].x+slots[level][s].w+24)){overlap=true;break;}
        }
        if(!overlap){slots[level].push({x:bx,w:bw});placed=true;}
        else level++;
      }
      p._yOff=(level-1.5)*18; // wider range for collision avoidance
    });
  });
  // Track used label areas to avoid cross-row overlap
  var labelRects=[];
  function labelOverlaps(x,y,w,h){
    for(var i=0;i<labelRects.length;i++){
      var lr=labelRects[i];
      if(!(x+w+2<lr.x||x>lr.x+lr.w+2||y+h<lr.y||y>lr.y+lr.h))return true;
    }
    return false;
  }

  tl.rows.forEach(function(r,ri){var y2=r.y;
    r.ps.forEach(function(p){
      var b=p.b||(p.d?p.d-ds:null),d=p.d||(p.b?p.b+ds:null);
      var noDates=!b&&!d;
      var isHL=p.id===hlId,matches=!isSearch||p.n.indexOf(searchQuery)>=0||(p.ti||'').indexOf(searchQuery)>=0||(p.bio||'').indexOf(searchQuery)>=0;
      var hoverDim=hoverSet&&!hoverSet[p.id];

      // Special: persons without dates → diamond marker at left edge
      if(noDates){
        var mx=10+Math.abs(p._yOff||0)*0.5;
        var my=y2+(p._yOff||0);
        ctx.globalAlpha=hoverDim?0.2:(isHL?1:0.7);
        ctx.fillStyle=r.color+'AA';ctx.strokeStyle=r.color;ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(mx,my-5);ctx.lineTo(mx+6,my);ctx.lineTo(mx,my+5);ctx.lineTo(mx-6,my);ctx.closePath();
        ctx.fill();ctx.stroke();
        ctx.globalAlpha=1;
        var ti=TYPE_ICONS[p.tp]||'';
        var prefix=ti?'['+ti+'] ':'';
        ctx.font=(isHL?'bold ':'')+'11px Microsoft YaHei';
        var fullText='◇ '+prefix+p.n+((p.v||0)<1?' °':'');
        ctx.fillStyle=isHL?'#c46b5d':'#5c5040';
        ctx.fillText(fullText,mx+10,my+4);
        var myen=_enName(p);if(myen&&isHL){ctx.font='8px Microsoft YaHei';ctx.fillStyle='#a09080';ctx.fillText(myen,mx+10,my+16);}
        labelRects.push({x:mx+10,y:my-6,w:ctx.measureText(fullText).width,h:12});
        return;
      }
      // Normal dated persons
      var bx=tX(b||d-10),dx=tX(d||b+10),bh=Math.min(22,rh*0.35),by=y2-bh/2+(p._yOff||0);
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

      // Type icon + name label with collision avoidance
      if(!isSearch||matches){
        var ti=TYPE_ICONS[p.tp]||'';
        var prefix=p._isGhost?'↳ ':ti?'['+ti+'] ':'';
        ctx.font=(isHL?"bold ":"")+(p._isGhost?'10':(isHL?'12':'11'))+"px Microsoft YaHei";
        var fullText=prefix+p.n+((p.v||0)<1?' °':'')
        var tw=ctx.measureText(fullText).width;
        // Try right side first, then left side if overlap
        var rightX=rx+rw+5, rightY=(p._yOff||0)<=0?by-3:by+bh+13;
        var leftX=rx-tw-5, leftY=by+bh/2+4;
        var useRight=rightX>0&&!labelOverlaps(rightX,rightY-10,tw,12);
        var useLeft=leftX>0&&!labelOverlaps(leftX,leftY-10,tw,12);
        var lx,ly;
        if(useRight||(!useLeft&&rightX<W-tw)){lx=rightX;ly=rightY;}
        else{lx=leftX;ly=leftY;}
        ctx.fillStyle=isHL?"#c46b5d":(p._isGhost?r.color:"#5c5040");
        ctx.fillText(fullText,lx,ly);
        var lyen=_enName(p);if(lyen&&isHL){ctx.font='8px Microsoft YaHei';ctx.fillStyle='#a09080';ctx.fillText(lyen,lx,ly+12);}
        // 🎬 indicator for persons with trajectory data
        var hasTraj=PERSON_TRAJECTORIES&&PERSON_TRAJECTORIES[p.id];
        if(hasTraj&&!p._isGhost){
          ctx.font='10px Microsoft YaHei';
          ctx.fillText('🎬',lx+tw+2,ly);
          tw+=14;
        }
        // Track this label
        labelRects.push({x:lx,y:ly-10,w:tw,h:12});
      }
      if(!p._isGhost)tl.hitRects.push({x:rx,y:by,w:rw,h:bh,person:p});
    });
  });

  // 6. EDGES
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
      if(sp.d){ctx.beginPath();ctx.arc(sx,sy,isHL?3:2,0,Math.PI*2);ctx.fillStyle=isHL?'#c46b5d':rc;ctx.fill();}
      ctx.beginPath();ctx.moveTo(sx,sy);
      ctx.bezierCurveTo(sx+(ex-sx)*0.4,sy,ex-(ex-sx)*0.4,ey,ex,ey);
      ctx.stroke();
      if(tp.b&&ex>sx+10){
        ctx.beginPath();ctx.moveTo(ex,ey);ctx.lineTo(ex-6,ey-4);ctx.lineTo(ex-6,ey+4);ctx.closePath();ctx.fillStyle=isHL?'#c46b5d':rc;ctx.fill();
      }
      ctx.setLineDash([]);ctx.globalAlpha=1;
    });
  }

  // 7. GEOGRAPHIC MARKERS (staggered + collision-aware)
  if(layerVis.geo&&!isOverview){
    var geoY0=tl.rows.length*rh+personTop+4;
    // Flow waypoints
    var lastGX=-999;
    GEO_FLOW.forEach(function(gf,i){
      var x=tX(gf.y);if(x<0||x>W)return;
      if(x-lastGX<30)return; // skip if too close
      lastGX=x;
      ctx.fillStyle='#c46b5d';ctx.font=f11b();
      ctx.fillText('📍',x-6,geoY0+9);
      if(i<GEO_FLOW.length-1){
        var nx=tX(GEO_FLOW[i+1].y);
        if(nx<W&&nx-x>10){
          ctx.strokeStyle='rgba(196,107,93,0.15)';ctx.lineWidth=1;ctx.setLineDash([3,5]);
          ctx.beginPath();ctx.moveTo(x+4,geoY0+6);ctx.lineTo(nx-4,geoY0+6);ctx.stroke();
          ctx.setLineDash([]);
        }
      }
    });
    // Location markers with staggered y
    var locY=geoY0+20,locLevel=0;var seen={};
    DATA.locations.forEach(function(loc){
      if(!loc.ps||!loc.ps.length)return;
      var p=nodeMap[loc.ps[0]];if(!p||!p.b)return;
      var lx=tX(p.b);if(lx<0||lx>W||seen[loc.id])return;seen[loc.id]=true;
      ctx.fillStyle='#8b6b4a';ctx.font=f10();
      var txt='▾ '+loc.n;
      if(locLevel%2===0){ctx.fillText(txt,lx-10,locY);}else{ctx.fillText(txt,lx-10,locY+26);}
      locLevel++;
    });
  }

  // 8. EVENT MARKERS (4-level staggered + type icons + legend)
  if(layerVis.events&&!isOverview){
    var evY0=H-30;
    var evPositions=[];
    var tpColors={远源:'#b0a898',义学:'#b8863c',翻译:'#a09080',禅观:'#7d9a6e',宗派:'#8b7a9e',文化:'#c8893e',法难:'#c46b5d',教育:'#5e8b9e',传承:'#6d9a6e',宗教:'#9e8b6e',当代:'#5e8b9e'};
    var tpIcons={义学:'📜',翻译:'📖',禅观:'🧘',宗派:'⚡',文化:'🏛',法难:'🔥',教育:'🎓',传承:'🔗',宗教:'☸',当代:'🆕'};
    KEY_EVENTS.forEach(function(ev){
      var x=tX(ev.y);if(x<0||x>W)return;
      evPositions.push({x:x,ev:ev});
    });
    evPositions.forEach(function(ep,i){
      ep.level=0;
      for(var j=0;j<i;j++){
        if(Math.abs(ep.x-evPositions[j].x)<60)ep.level++;
      }
      ep.level=Math.min(ep.level,3);
    });
    evPositions.forEach(function(ep){
      var x=ep.x,ev=ep.ev,ey=evY0-ep.level*13;
      // Connector line
      if(ev.p&&layerVis.edges){
        var pHR=tl.hitRects.find(function(h){return h.person.n===ev.p||h.person.id===ev.p;});
        if(pHR){
          ctx.strokeStyle='rgba(180,134,60,0.15)';ctx.lineWidth=0.6;ctx.setLineDash([1,4]);
          ctx.beginPath();ctx.moveTo(x,ey);ctx.lineTo(pHR.x+pHR.w/2,pHR.y+pHR.h);ctx.stroke();
          ctx.setLineDash([]);
        }
      }
      // Type dot
      var tc=tpColors[ev.tp]||'#b0a898';
      ctx.fillStyle=tc;ctx.beginPath();ctx.arc(x,ey-2,3.5,0,Math.PI*2);ctx.fill();
      ctx.strokeStyle='#fff';ctx.lineWidth=0.8;ctx.beginPath();ctx.arc(x,ey-2,3.5,0,Math.PI*2);ctx.stroke();
      // Event text
      ctx.fillStyle='#5c5040';ctx.font='bold 9px Microsoft YaHei';
      var evTxt=truncText(ctx,ev.l,W-x-8);
      ctx.fillText(evTxt,x+6,ey+3);
    });
    // Legend row (compact)
    var lgX=4,lgY=H-8;
    ctx.fillStyle='#a09080';ctx.font='8px Microsoft YaHei';
    var types=['远源','宗教','义学','翻译','禅观','宗派','文化','教育','传承'];
    types.forEach(function(t){
      var tc2=tpColors[t]||'#b0a898';
      ctx.fillStyle=tc2;ctx.beginPath();ctx.arc(lgX+4,lgY-2,3,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#8a7a6a';ctx.fillText(t,lgX+9,lgY+1);
      lgX+=ctx.measureText(t).width+18;
    });
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
      ctx.fillStyle='#8a7060';ctx.font='10px Microsoft YaHei';
      ctx.fillText(ct.count+'人',cx-8,heatY+heatH-bh-4);
    });
  }
}

// ═══ MAP SYSTEM (main view + minimap like StarCraft) ═══
var mapMain=null,_miniMaps={},_trajGroup=null;
var mainMarkers=[];
// Free tile URL constants (no API key required)
var OSM_URL='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var ESRI_IMAGERY='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
var ESRI_TERRAIN='https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}';
var AMAP_URL='https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}';
var OPENTOPO_URL='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';

function tileLayer(){return L.tileLayer(AMAP_URL,{subdomains:['1','2','3','4'],maxZoom:18});}
function terrainTileLayer(){return L.tileLayer(OPENTOPO_URL,{subdomains:['a','b','c'],maxZoom:17,opacity:0.7});}

// ═══ BASEMAP SWITCHER (all free, no API key) ═══
var _basemapLayers=[],currentBasemapIdx=0;
function _osmOverlay(){return L.tileLayer(OSM_URL,{subdomains:['a','b','c'],maxZoom:19,opacity:0.4});}

var BASEMAPS=[
  {name:'现代',icon:'🗺',desc:'高德+OSM',
   create:function(){return [tileLayer(),_osmOverlay()];}},
  {name:'卫星',icon:'🛰',desc:'Esri卫星影像',
   create:function(){return [L.tileLayer(ESRI_IMAGERY,{maxZoom:18,attribution:'Esri,Maxar,Earthstar'})];}},
  {name:'地形',icon:'⛰',desc:'Esri地形渲染',
   create:function(){return [L.tileLayer(ESRI_TERRAIN,{maxZoom:18,attribution:'Esri,USGS'})];}}
];

function _applyBasemap(idx){
  currentBasemapIdx=idx;
  var bm=BASEMAPS[idx];
  _basemapLayers.forEach(function(l){if(mapMain)mapMain.removeLayer(l);});
  _basemapLayers=[];
  if(mapMain){
    var layers=bm.create();
    layers.forEach(function(l){l.addTo(mapMain);_basemapLayers.push(l);});
  }
  var bb=document.getElementById('basemap-btn');
  if(bb){bb.textContent=bm.icon+' '+bm.name;}
}

function cycleBasemap(){
  var next=(currentBasemapIdx+1)%BASEMAPS.length;
  _applyBasemap(next);
}

function initMap(){
  if(typeof L==="undefined"){
    var d1=document.getElementById("map-main");if(d1)d1.innerHTML="<div style=display:flex;align-items:center;justify-content:center;height:100%;color:var(--text2);font-size:0.7em>🗺 地图未加载</div>";
    return;
  }
  // ── Main map: China/East Asia detail ──
  if(!mapMain){
    mapMain=L.map("map-main",{zoomControl:true,zoomControlPosition:'bottomleft'}).setView([34,108],5);
    _applyBasemap(0); // Default: 现代 (高德+OSM)
    // Huayan locations
    var mc={temple:"#b8863c",mountain:"#7d9a6e",region:"#c46b5d"};
    DATA.locations.forEach(function(loc){
      var namesArr=(loc.ps||[]).map(function(pid){var n=nodeMap[pid];return n;}).filter(Boolean);
      var names=namesArr.map(function(n){return n.n;}).join("、");
      var namesEn=namesArr.map(function(n){return _enName(n);}).filter(Boolean);
      var m=L.circleMarker([loc.lat,loc.lng],{radius:8,fillColor:mc[loc.tp]||"#b0a898",color:"#fff",weight:2,fillOpacity:0.9});
      m.addTo(mapMain).bindPopup("<b>"+loc.n+"</b><br>"+(loc.dy||"")+"<br>"+(loc.ds||"")+(names?"<br>👤 "+names:"")+(namesEn.length?'<div class="en-line" style="font-size:0.8em;color:var(--text2)">'+namesEn.join(' · ')+'</div>':""));
      m._ld=loc;m.on("click",function(){if(loc.ps&&loc.ps.length>0)selectPerson(loc.ps[0]);});
      mainMarkers.push(m);
    });
  } else {
    mapMain.invalidateSize();
  }
  initMiniMaps();
  // Ancient map mode enabled by default via init.js (single toggle call)
}
function getMainMap(){return mapMain;}

// ═══ SELECTION ═══
function selectPerson(id,isShift,ev){
  if(isShift&&selectedId&&id!==selectedId){selectedId2=id;}else{selectedId=id;selectedId2=null;}
  var p=nodeMap[id];if(p&&p.b){
    var rng=(p.d||p.b+50)-p.b;tl.minX=p.b-rng*0.3;tl.maxX=(p.d||p.b+50)+rng*0.7;
    tl.scale=(tl.W-40)/(tl.maxX-tl.minX);tl.ox=20;
  }
  drawTL(selectedId);if(selectedId2)drawTL2(selectedId2);
  showInfo(nodeMap[selectedId],selectedId2?nodeMap[selectedId2]:null,ev);
  var locs=getPersonLocs(id);
  // Clear previous: footprints + ALL trajectory layers + popups
  if(window._personFootprints){for(var fi=0;fi<window._personFootprints.length;fi++){try{mapMain.removeLayer(window._personFootprints[fi]);}catch(e){}}}
  window._personFootprints=[];
  _clearTrajMarkers();
  if(mapMain&&locs.length>0){
    var loc=locs[0];mapMain.flyTo([loc.lat,loc.lng],locs.length===1?12:10,{duration:0.8});
    // Draw footprint line + numbered markers
    if(locs.length>1){
      var fpCoords=locs.map(function(l){return [l.lat,l.lng];});
      var fpLine=L.polyline(fpCoords,{color:'#c46b5d',weight:3,opacity:0.6,dashArray:'6,4'}).addTo(mapMain);
      fpLine.bindTooltip(p.n+'的足迹',{permanent:false});
      window._personFootprints.push(fpLine);
      locs.forEach(function(l,i){
        var icon=L.divIcon({html:'<div style=background:#c46b5d;color:#fff;border-radius:50%;width:20px;height:20px;text-align:center;line-height:20px;font-size:10px;font-weight:700;border:2px solid #fff>'+(i+1)+'</div>',iconSize:[20,20],iconAnchor:[10,10]});
        var m=L.marker([l.lat,l.lng],{icon:icon}).addTo(mapMain);
        m.bindPopup('<b>'+(i+1)+'. '+l.n+'</b><br>'+(l.dy||'')+'<br>'+(l.ds||''));
        window._personFootprints.push(m);
      });
    }
  // ── Auto-show person trajectory on map ──
  if(PERSON_TRAJECTORIES&&PERSON_TRAJECTORIES[id]&&mapMain){
    showTrajectoryOnMap(id);
  }
  setTimeout(function(){
    mapMain.eachLayer(function(layer){
      if(!layer._ld)return;
      var isRelated=locs.some(function(l){return l.id===layer._ld.id;});
      if(isRelated){layer.setRadius(13);layer.setStyle({fillColor:"#c46b5d",color:"#fff",weight:3,fillOpacity:1});if(!layer._popupOpen){layer.openPopup();layer._popupOpen=true;setTimeout(function(){layer.closePopup();layer._popupOpen=false;},3000);}}
      else{layer.setRadius(7);layer.setStyle({fillOpacity:0.5});}
    });
  },900);
  setTimeout(function(){
    mapMain.eachLayer(function(layer){if(!layer._ld)return;var mc={temple:"#b8863c",mountain:"#7d9a6e",region:"#c46b5d"};layer.setRadius(8);layer.setStyle({fillColor:mc[layer._ld.tp]||"#b0a898",color:"#fff",weight:2,fillOpacity:0.9});});
  },5000);
  }
  var sb=document.getElementById("stats-bar");if(sb)sb.textContent=calcStats();
}
function clearSelection(){selectedId=null;selectedId2=null;drawTL(null);document.getElementById('info-popup').style.display='none';if(_trajTimer){clearTimeout(_trajTimer);_trajTimer=null;}if(_trajPopup&&mapMain){mapMain.closePopup(_trajPopup);_trajPopup=null;}if(mapMain)mapMain.closePopup();var sb=document.getElementById("stats-bar");if(sb)sb.textContent=calcStats();}
function drawTL2(id){}

// ═══ ANCIENT/MODERN MAP TOGGLE (with terrain) ═══
var ancientMode=false,dynastyLayers=[],ancientLabels=[],terrainLayer=null,_miniTerrainLayers=[];

// ═══ FILTER PRESET SYSTEM ═══
var FILTER_PRESETS=[
  {name:'无', cls:'', desc:'原始色彩'},
  {name:'羊皮纸', cls:'filter-parchment', desc:'Parchment·暖黄怀旧'},
  {name:'银盐', cls:'filter-silver', desc:'Monochrome·黑白摄影'},
  {name:'靛蓝', cls:'filter-indigo', desc:'Indigo·古地图'},
  {name:'琥珀', cls:'filter-amber', desc:'Amber·旧胶片'},
  {name:'暮色', cls:'filter-twilight', desc:'Twilight·沉静暗调'}
];
var currentFilterIdx=0;

function applyFilter(idx){
  currentFilterIdx=idx;
  var preset=FILTER_PRESETS[idx];
  var side=document.getElementById('side');
  var mm=document.getElementById('mini-maps-grid');
  // Remove all filter classes
  FILTER_PRESETS.forEach(function(p){if(p.cls){if(side)side.classList.remove(p.cls);if(mm)mm.classList.remove(p.cls);}});
  // Add new filter class
  if(preset.cls){if(side)side.classList.add(preset.cls);if(mm)mm.classList.add(preset.cls);}
  // Update button
  var fb=document.getElementById('filter-btn');
  if(fb){fb.textContent='🎨 '+preset.name;if(idx>0){fb.classList.add('filter-btn-active');}else{fb.classList.remove('filter-btn-active');}}
}

function cycleFilter(){
  var next=(currentFilterIdx+1)%FILTER_PRESETS.length;
  applyFilter(next);
}

// ── Ancient/Modern Map Toggle ──
LOC_ANCIENT=(typeof LOC_ANCIENT!=='undefined'&&LOC_ANCIENT&&LOC_ANCIENT.mapping)?LOC_ANCIENT.mapping:{};

// ═══ PERSON TRAJECTORIES (global injected from YAML, fallback if missing) ═══
if (typeof PERSON_TRAJECTORIES === 'undefined') { console.warn("PERSON_TRAJECTORIES not loaded from YAML"); var PERSON_TRAJECTORIES = {}; }
DYNASTY_BOUNDARIES=(typeof DYNASTY_BOUNDARIES!=='undefined'&&DYNASTY_BOUNDARIES&&DYNASTY_BOUNDARIES.dynasties)?DYNASTY_BOUNDARIES.dynasties:[];
function toggleAncient(){
  ancientMode=!ancientMode;
  var cm=document.getElementById('tab-lineage');
  var btn=document.getElementById('ancient-btn');
  if(ancientMode){
    if(cm)cm.classList.add('map-ancient');
    if(btn){btn.style.background='#b8863c';btn.style.color='#fff';btn.style.borderColor='#b8863c';btn.textContent='🏯 今';}
    applyFilter(1); // Default ancient filter: 古卷
    // Add terrain overlay to main map
    if(!terrainLayer){terrainLayer=terrainTileLayer();terrainLayer.addTo(mapMain);}else{terrainLayer.addTo(mapMain);}
    // Major geographic feature labels (source of truth: data/events/geo_features.yaml -> GEO_FEATURES)
    var geoFeatures=(typeof GEO_FEATURES!=='undefined'&&GEO_FEATURES&&GEO_FEATURES.features)?GEO_FEATURES.features:[];
    geoFeatures.forEach(function(gf){
      var gl=L.marker([gf.lat,gf.lng],{icon:L.divIcon({html:'<div style=font-size:10px;color:#6b4e2a;font-weight:600;text-shadow:0 0 4px rgba(255,255,255,0.8)>'+gf.n+'</div>',className:'geo-feature-label',iconSize:[0,0]}),interactive:false,zIndexOffset:-5}).addTo(mapMain);
      ancientLabels.push(gl);
    });
    // Re-init transmission story and schools
    initTransStory();initOtherSchools();
    // Show dynasty boundaries (Chinese + world civilizations)
    var allCivs = (typeof WORLD_CIVILIZATIONS !== 'undefined' && WORLD_CIVILIZATIONS.civilizations)
      ? DYNASTY_BOUNDARIES.concat(WORLD_CIVILIZATIONS.civilizations) : DYNASTY_BOUNDARIES;
    allCivs.forEach(function(db){
      var r=L.rectangle(db.bounds,{color:db.c,weight:1.5,fillColor:db.c,fillOpacity:0.04,className:'dynasty-boundary'}).addTo(mapMain);
      var cx=(db.bounds[0][1]+db.bounds[1][1])/2,cy=(db.bounds[0][0]+db.bounds[1][0])/2;
      var lblName=db.n||db.name||'?'; // support both DYNASTY_BOUNDARIES(n) and world_civilizations(name)
      var lbl=L.marker([cy,cx],{icon:L.divIcon({html:'<div style=font-size:8px;color:'+db.c+';font-weight:600;text-shadow:0 0 4px #fff;white-space:nowrap>'+lblName+'</div>',className:'dynasty-label',iconSize:[0,0]}),interactive:false}).addTo(mapMain);
      dynastyLayers.push({rect:r,label:lbl,db:db});
    });
    updateDynastyVisibility(-600);
    // Add terrain to mini maps
    var mmGrid=document.getElementById('mini-maps-grid');
    if(mmGrid)mmGrid.classList.add('map-ancient');
    Object.keys(_miniMaps).forEach(function(k){
      var mm=_miniMaps[k];if(!mm||!mm.map)return;
      var t=terrainTileLayer();t.addTo(mm.map);
      _miniTerrainLayers.push({map:mm.map,layer:t});
    });
  }else{
    if(cm)cm.classList.remove('map-ancient');
    if(btn){btn.style.background='';btn.style.color='';btn.style.borderColor='';btn.textContent='🏯 古今';}
    applyFilter(0); // Back to no filter
    // Remove terrain from main map
    if(terrainLayer){mapMain.removeLayer(terrainLayer);}
    // Remove dynasty boundaries
    dynastyLayers.forEach(function(d){mapMain.removeLayer(d.rect);mapMain.removeLayer(d.label);});
    dynastyLayers=[];
    // Remove ancient labels
    ancientLabels.forEach(function(l){mapMain.removeLayer(l);});
    ancientLabels=[];
    // Remove transmission story + other schools
    transMarkers.forEach(function(m){mapMain.removeLayer(m);});transMarkers=[];
    transLines.forEach(function(l){mapMain.removeLayer(l);});transLines=[];
    otherSchoolsMarkers.forEach(function(m){mapMain.removeLayer(m);});otherSchoolsMarkers=[];
    // Remove terrain from mini maps
    var mmGrid2=document.getElementById('mini-maps-grid');
    if(mmGrid2)mmGrid2.classList.remove('map-ancient');
    _miniTerrainLayers.forEach(function(tl){tl.map.removeLayer(tl.layer);});
    _miniTerrainLayers=[];
  }
}

// ═══ ENHANCED INFO PANEL ═══
function showInfo(p,p2,e){
  var popup=document.getElementById('info-popup');
  if(!popup)return;
  // Always clear previous state first
  if(popup._autoTimer)clearTimeout(popup._autoTimer);
  popup._autoTimer=null;
  popup.onmouseenter=popup.onmouseleave=popup.onclick=null;
  if(!p){popup.style.display='none';return;}
  // Use popup directly (compatible with showTempleInfo which sets innerHTML)
  var lc=(p.li&&DATA.lineage_colors[p.li])?DATA.lineage_colors[p.li]:"#b0a898";
  var locs=getPersonLocs(p.id),locHTML="";
  locs.forEach(function(l){var an=ancientMode?(LOC_ANCIENT[l.n]||l.n):l.n;locHTML+='📍 '+an+'<br>';});
  // Gather ALL relationships by type (simplified)
  var rels={};
  DATA.edges.forEach(function(e){
    var t=null,dir='';
    if(e.s===p.id){t=nodeMap[e.t];dir='out';}
    if(e.t===p.id){t=nodeMap[e.s];dir='in';}
    if(!t)return;
    var label='';
    if(e.r==='MASTER'||e.r==='MASTER_OF')label=(dir==='out'?'⬇ 传法':'⬆ 师承');
    else if(e.r==='LINEAGE')label='🔗 法脉';
    else if(e.r==='INFLUENCED')label=(dir==='out'?'⬇ 影响':'⬆ 受影响');
    else if(e.r==='INFLUENCE')label=(dir==='out'?'⬇ 影响':'⬆ 受影响');
    else if(e.r==='CONTEMPORARY')label='👥 同代';
    else label=e.r;
    if(!rels[label])rels[label]=[];
    if(rels[label].indexOf(t.n)<0)rels[label].push(t.n);
  });
  var gen=0,tmp=p, visitedGen={};
  visitedGen[p.id]=true;
  var teachers=DATA.edges.filter(function(e){return e.t===p.id&&(e.r==='MASTER'||e.r==='MASTER_OF');}).map(function(e){return nodeMap[e.s];}).filter(Boolean);
  while(tmp){
    var next=null;
    for(var ti=0;ti<teachers.length;ti++){
      if(!visitedGen[teachers[ti].id]){next=teachers[ti];break;}
    }
    if(!next)break;
    visitedGen[next.id]=true;tmp=next;gen++;
  }
  var lifeSpan=(p.b&&p.d)?('享年'+(p.d-p.b)+'岁 · '):'';
  // Build relationship HTML
  var relHTML='';
  Object.keys(rels).forEach(function(k){
    var arr=rels[k];if(!arr||!arr.length)return;
    relHTML+='<div style=margin:2px 0><b style=color:#b8863c>'+k+'</b>: '+arr.join(' · ')+'</div>';
  });
  var ti=TYPE_ICONS[p.tp]||'';
  var connCount=Object.keys(rels).reduce(function(s,k){return s+(rels[k]?rels[k].length:0);},0);
  var h="<span class=close-btn onclick=\"document.getElementById('info-popup').style.display='none'\">&times;</span>"
    +"<h3>"+(ti?'['+ti+'] ':'')+p.n+" <span style=font-size:0.7em;color:var(--text2)>"+(p.ti||"")+"</span></h3>"
    +_enNameHtml(p)
    +"<span class=tag style=background:"+lc+"20;color:"+lc+">"+(p.li||"—")+"</span>"
    +"<span class=tag style=background:rgba(0,0,0,0.04)>"+(p.tp==="patriarch"?"祖师":p.tp==="translator"?"译师":p.tp==="scholar"?"学者":"行者")+"</span>"
    +((p.v||0)>0?'<span class=tag style="background:rgba(125,154,110,0.1);color:#7d9a6e" title="来源已核实">✓</span>':'<span class=tag style="background:rgba(196,107,93,0.1);color:#c46b5d" title="来源缺失或尚未核实，需补第一手出处并标注存疑">⚠️ 存疑</span>')
    +(gen?'<span class=tag style=background:rgba(184,134,60,0.06)>第'+gen+'代传人</span>':'')
    +(connCount?'<span class=tag style=background:rgba(184,134,60,0.08)>'+connCount+'个关联</span>':'')+"<br>"
    +"📅 <b>"+(p.dy||"?")+"</b> · "+(p.b||"?")+"–"+(p.d||"?")+" "+lifeSpan+"<br>"
    +locHTML+relHTML
    +(p.bio?"<div style=color:var(--text2);line-height:1.5;margin-top:4px;padding-top:4px;border-top:1px solid var(--line)>"+p.bio+"</div>":"")
    +(p.wk&&p.wk.length?"<div style=margin-top:4px>📖 <b>"+p.wk.map(function(w){var lk=p.wl&&p.wl[w];return lk?'<a href='+lk+' target=_blank style=color:var(--blue)>'+w+'</a>':w;}).join("</b> · <b>")+"</b></div>":"");
  // ── Source/literature citation ──
  var srcNote='';
  if(PERSON_TRAJECTORIES&&PERSON_TRAJECTORIES[p.id]&&PERSON_TRAJECTORIES[p.id].source)srcNote=PERSON_TRAJECTORIES[p.id].source;
  if(!srcNote&&p.src)srcNote=p.src;
  if(srcNote)h+='<div style="margin-top:3px;font-size:0.65em;color:var(--text2);opacity:0.7">📚 '+srcNote+'</div>'
    +'<div style="margin-top:2px;font-size:0.62em;color:var(--text2)">('+((p.v||0)>0?'来源信息为已核实状态':'来源已登记，待人工核实')+')</div>';
  else h+='<div style="margin-top:3px;font-size:0.65em;color:#c46b5d;background:rgba(196,107,93,0.06);padding:3px 8px;border-radius:6px;display:inline-block">⚠️ 暂无来源标注 — 存疑，待补第一手出处</div>';
  // ── Huayan connection annotation ──
  var ha=null;
  try{ha=(EVENTS&&EVENTS.huayan_annotations&&EVENTS.huayan_annotations.persons)?EVENTS.huayan_annotations.persons[p.id]:null;}catch(e){}
  if(ha&&ha.note){
    var lvlColors={direct:'#b8863c',indirect:'#5e8b9e',dialogue:'#7d9a6e',parallel:'#c8893e',influence:'#8b7a9e'};
    var lvlLabels={direct:'直接关联',indirect:'间接渊源',dialogue:'跨传统对话',parallel:'修行印证',influence:'思想影响'};
    var lc2=lvlColors[ha.level]||'#b8863c';
    h+='<div style="margin-top:4px;padding:6px 8px;background:'+lc2+'0a;border-left:3px solid '+lc2+';border-radius:0 6px 6px 0;font-size:0.78em;line-height:1.6;color:var(--text2)">'
      +'<b style=color:'+lc2+'>🪷 华严关联</b> <span style=font-size:0.85em;color:'+lc2+'>['+(lvlLabels[ha.level]||ha.level)+']</span><br>'
      +ha.note+'</div>';
  }
  if(p2){
    var lc2=DATA.lineage_colors[p2.li]||"#b0a898";var ti2=TYPE_ICONS[p2.tp]||'';
    h+="<div style='margin-top:10px;padding-top:8px;border-top:2px solid var(--gold)'><h3 style=color:#5e8b9e>"+(ti2?'['+ti2+'] ':'')+p2.n+" <span style=font-size:0.7em;color:var(--text2)>"+(p2.ti||"")+"</span></h3>"
      +_enNameHtml(p2)
      +"<span class=tag style=background:"+lc2+"20;color:"+lc2+">"+(p2.li||"—")+"</span>"
      +"📅 <b>"+(p2.dy||"?")+"</b> · "+(p2.b||"?")+"–"+(p2.d||"?")+"<br>"
      +(p2.bio?"<div style=color:var(--text2)>"+p2.bio+"</div>":"")+"</div>";
  }
  // ── Person trajectory (micro: person journey) ──
  var traj=PERSON_TRAJECTORIES[p.id];
  if(traj&&traj.route&&traj.route.length){
    h+='<div style="margin-top:6px;padding-top:6px;border-top:1px solid var(--line)">';
    h+='<b style=color:'+(traj.color||'#b8863c')+'>🗺 '+traj.name+'</b> ';
    h+='<span style=font-size:0.7em;color:var(--text2)>('+traj.route.length+'个节点)</span><br>';
    h+='<button onclick="playTrajectory(\''+p.id+'\')" style="padding:3px 10px;border:1px solid '+(traj.color||'#b8863c')+';border-radius:12px;background:var(--card);color:'+(traj.color||'#b8863c')+';cursor:pointer;font-size:0.72em;margin-top:4px">🎬 播放足迹</button> ';
    h+='<button onclick="showTrajectoryOnMap(\''+p.id+'\')" style="padding:3px 10px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.72em;margin-top:4px">📍 查看路线</button>';
    h+='</div>';
  }
  // ── Civilization exchange context (macro) ──
  var eraEvents=KEY_EVENTS.filter(function(ev){return p.b&&ev.y>=p.b-50&&ev.y<=p.d+50;}).slice(0,3);
  if(eraEvents.length){
    h+='<div style="margin-top:4px;padding-top:4px;border-top:1px dotted var(--line)">';
    h+='<span style=font-size:0.7em;color:var(--blue)>🌏 同时代事件:</span> ';
    eraEvents.forEach(function(ev,ei){
      h+='<span style=font-size:0.68em;color:var(--text2)'+(ei===0?'':'')+'>'+ev.y+' '+ev.l.substring(0,30)+'</span> ';
    });
    h+='</div>';
  }
  // ── Relationship graph canvas ──
  h+='<canvas id=rel-graph width=240 height=150 style="display:block;margin:6px auto 0;border-radius:6px;background:rgba(246,242,232,0.5)"></canvas>';
  popup.innerHTML=h;
  // Draw relationship graph after DOM update
  setTimeout(function(){drawRelationGraph(p.id);},50);
  popup.style.display='block';popup.style.visibility='visible';popup.style.opacity='1';
  // Ensure popup has sensible default position
  if(!popup.style.left||popup.style.left==='0px'){popup.style.left='60vw';popup.style.top='10vh';}
  // Auto-hide: 12s initial, stays while hovering, 5s after mouse leaves
  // Click to pin: click the popup to toggle fixed mode
  if(popup._autoTimer)clearTimeout(popup._autoTimer);
  popup.onmouseenter=function(){if(popup._autoTimer)clearTimeout(popup._autoTimer);};
  popup.onmouseleave=function(){popup._autoTimer=setTimeout(function(){popup.style.display='none';},5000);};
  popup.onclick=function(e){if(e.target.closest('button')||e.target.closest('a'))return;popup.style.display='none';};
  popup._autoTimer=setTimeout(function(){popup.style.display='none';},12000);
  // Position: mobile=centered, desktop=near click
  var isMobile=window.innerWidth<768;
  if(isMobile){
    popup.style.left='4vw';popup.style.top='10vh';popup.style.width='92vw';
  }else if(e){
    var px=e.pageX+14,py=e.pageY-14;
    if(px+290>window.innerWidth)px=e.pageX-300;
    if(py+280>window.innerHeight)py=window.innerHeight-290;
    popup.style.left=px+'px';popup.style.top=py+'px';popup.style.width='';
  }else{
    popup.style.left=(window.innerWidth-310)+'px';popup.style.top='60px';popup.style.width='';
  }
}

// ═══ PERSON TRAJECTORY PLAYBACK ═══
var _trajTimer=null,_trajMarker=null,_trajLine=null,_trajIndex=0,_trajHighlight=null,_trajPopup=null;
function playTrajectory(pid){
  var traj=PERSON_TRAJECTORIES[pid];if(!traj||!traj.route)return;
  _clearTrajMarkers();
  if(!mapMain)return;
  _trajGroup=L.layerGroup().addTo(mapMain);
  _trajIndex=0;
  var route=traj.route,color=traj.color||'#c46b5d',name=traj.name||'';
  var coords=route.map(function(p){return [p.lat,p.lng];});
  _trajLine=L.polyline(coords,{color:color,weight:2,opacity:0.35,dashArray:'6,4'}).addTo(_trajGroup);
  mapMain.fitBounds(_trajLine.getBounds().pad(0.15));
  L.circleMarker([route[0].lat,route[0].lng],{radius:7,fillColor:'#7d9a6e',color:'#fff',weight:2,fillOpacity:0.9})
    .bindTooltip('▶ '+route[0].label+' ('+route[0].y+')',{direction:'right'}).addTo(_trajGroup);
  var last=route[route.length-1];
  L.circleMarker([last.lat,last.lng],{radius:7,fillColor:'#c46b5d',color:'#fff',weight:2,fillOpacity:0.9})
    .bindTooltip('⏹ '+last.label+' ('+last.y+')',{direction:'right'}).addTo(_trajGroup);
  _trajMarker=L.circleMarker([route[0].lat,route[0].lng],{radius:10,fillColor:color,color:'#ffe066',weight:3,fillOpacity:0.95}).addTo(mapMain);
  document.getElementById('info-popup').style.display='none';
  var sb=document.getElementById('anim-status');if(sb)sb.style.opacity='1';
  _showTrajNav(route,color,name,0);
  _stepTrajectory(route,color,sb,name);
}
function _showTrajNav(route,color,name,idx){
  if(!mapMain)return;
  var pt=route[idx],next=idx+1<route.length?route[idx+1]:null;
  var progress=Math.round((idx/route.length)*100);
  var html='<div style=max-width:260px;font-size:0.75em;line-height:1.5>'
    +'<b style=color:'+color+'>🎬 '+name+'</b>'
    +'<br>📍 <b>'+pt.y+'年</b> '+pt.label
    +(next?'<br>➡ <span style=color:var(--text2)>下一站: '+next.y+'年 '+next.label+'</span>':'')
    +'<br><span style=font-size:0.7em;color:var(--text2)>进度: '+idx+'/'+route.length+' ('+progress+'%)</span>'
    +'<br><span style=font-size:0.65em;color:var(--text2)>点击地图暂停/继续 · 播放完毕自动关闭</span>'
    +'</div>';
  if(_trajPopup&&mapMain)mapMain.closePopup(_trajPopup);
  _trajPopup=L.popup({closeButton:false,autoClose:false,className:'anim-popup',maxWidth:280,autoPan:false,offset:[0,-15]})
    .setLatLng([pt.lat,pt.lng]).setContent(html).openOn(mapMain);
  // Click map to pause/resume (only if trajectory still active)
  mapMain.off('click');mapMain.on('click',function(){
    if(_trajIndex>=route.length)return; // trajectory already done
    if(_trajTimer){clearTimeout(_trajTimer);_trajTimer=null;document.getElementById('anim-status').style.opacity='0';}
    else{_trajTimer=setTimeout(function(){_stepTrajectory(route,color,document.getElementById('anim-status'),name);},1200);}
  });
}
function _stepTrajectory(route,color,sb,name){
  if(_trajIndex>=route.length){
    if(sb)sb.style.opacity='0';
    if(_trajTimer){clearTimeout(_trajTimer);_trajTimer=null;}
    if(mapMain){mapMain.off('click');}
    if(_trajPopup&&mapMain){mapMain.closePopup(_trajPopup);_trajPopup=null;}
    if(_trajMarker){_trajMarker.setStyle({fillColor:'#7d9a6e',radius:12});setTimeout(function(){if(_trajMarker)_trajMarker.setStyle({fillColor:color,radius:10});},500);}
    return;
  }
  var pt=route[_trajIndex],prev=_trajIndex>0?route[_trajIndex-1]:null;
  if(sb)sb.innerHTML='<b style=color:'+color+'>'+pt.y+'年</b> '+pt.label+' <span style=font-size:0.8em;color:var(--text2)>('+(_trajIndex+1)+'/'+route.length+')</span>';
  if(_trajMarker&&mapMain){
    _trajMarker.setLatLng([pt.lat,pt.lng]);
    mapMain.panTo([pt.lat,pt.lng],{animate:true,duration:0.6});
  }
  // Highlight current segment
  if(_trajHighlight&&_trajGroup)_trajGroup.removeLayer(_trajHighlight);
  if(prev&&_trajGroup){
    _trajHighlight=L.polyline([[prev.lat,prev.lng],[pt.lat,pt.lng]],{color:color,weight:5,opacity:0.8}).addTo(_trajGroup);
  }
  // Update nav popup
  _showTrajNav(route,color,name,_trajIndex);
  _trajIndex++;
  _trajTimer=setTimeout(function(){_stepTrajectory(route,color,sb,name);},1200);
}
function _clearTrajMarkers(){
  try{
    if(_trajGroup&&mapMain){mapMain.removeLayer(_trajGroup);}
    if(_trajMarker&&mapMain)try{mapMain.removeLayer(_trajMarker);}catch(e){}
    if(mapMain){mapMain.closePopup();mapMain.closeTooltip();}
  }catch(e){console.error('_clearTrajMarkers:',e);}
  _trajGroup=null;_trajLine=null;_trajMarker=null;_trajHighlight=null;_trajPopup=null;
  if(_trajTimer){clearTimeout(_trajTimer);_trajTimer=null;}
}
function showTrajectoryOnMap(pid){
  
  var traj=PERSON_TRAJECTORIES[pid];if(!traj||!traj.route)return;
  _clearTrajMarkers();
  if(!mapMain)return;
  _trajGroup=L.layerGroup().addTo(mapMain);
  var coords=traj.route.map(function(p){return [p.lat,p.lng];});
  var color=traj.color||'#c46b5d';
  // Glow + core lines
  _trajLine=L.polyline(coords,{color:color,weight:5,opacity:0.25}).addTo(_trajGroup);
  L.polyline(coords,{color:color,weight:2.5,opacity:0.85,dashArray:'8,3'}).addTo(_trajGroup);
  // Start marker (green)
  var start=traj.route[0];
  L.circleMarker([start.lat,start.lng],{radius:8,fillColor:'#7d9a6e',color:'#fff',weight:2.5,fillOpacity:1})
    .bindTooltip('▶ '+start.label+' ('+start.y+')',{direction:'right'}).addTo(_trajGroup);
  // End marker (red)
  var end=traj.route[traj.route.length-1];
  L.circleMarker([end.lat,end.lng],{radius:8,fillColor:'#c46b5d',color:'#fff',weight:2.5,fillOpacity:1})
    .bindTooltip('⏹ '+end.label+' ('+end.y+')',{direction:'right'}).addTo(_trajGroup);
  // Numbered intermediate markers
  for(var i=1;i<traj.route.length-1;i++){
    var pt=traj.route[i];
    L.circleMarker([pt.lat,pt.lng],{radius:5,fillColor:color,color:'#fff',weight:1.5,fillOpacity:0.85})
      .bindTooltip((i+1)+'. '+pt.label+' ('+pt.y+')').addTo(_trajGroup);
  }
  // Zoom to fit
  var bounds=L.latLngBounds(coords);
  mapMain.fitBounds(bounds,{padding:[50,50],maxZoom:8});
}

// ═══ RELATIONSHIP GRAPH ═══
var _huayanCore=['person_001','person_002','person_003','person_004','person_005','person_042'];
function drawRelationGraph(pid){
  var c=document.getElementById('rel-graph');if(!c)return;
  var W=240,H=150,cx=W/2,cy=H/2;
  c.width=W;c.height=H;
  var ctx=c.getContext('2d');
  ctx.clearRect(0,0,W,H);
  // Background
  ctx.fillStyle='rgba(246,242,232,0.3)';ctx.fillRect(0,0,W,H);
  var p=nodeMap[pid];if(!p)return;
  // Collect connected Huayan persons and events
  var connections=[];
  DATA.edges.forEach(function(e){
    if(e.s===pid||e.t===pid){
      var otherId=e.s===pid?e.t:e.s;
      var other=nodeMap[otherId];if(!other)return;
      var ann=null;
      try{ann=(EVENTS&&EVENTS.huayan_annotations&&EVENTS.huayan_annotations.persons)?EVENTS.huayan_annotations.persons[otherId]:null;}catch(e){}
      if(ann||_huayanCore.indexOf(otherId)>=0||(other.li||'').indexOf('华严')>=0){
        connections.push({id:otherId,n:other.n,li:other.li,r:e.r,level:ann?ann.level:'unknown',color:DATA.lineage_colors[other.li]||'#b0a898'});
      }
    }
  });
  // Add this person's own annotation level
  var selfAnn=null;
  try{selfAnn=(EVENTS&&EVENTS.huayan_annotations&&EVENTS.huayan_annotations.persons)?EVENTS.huayan_annotations.persons[pid]:null;}catch(e){}
  var selfLevel=selfAnn?selfAnn.level:'unknown';
  var lvlColors={direct:'#b8863c',indirect:'#5e8b9e',dialogue:'#7d9a6e',parallel:'#c8893e',influence:'#8b7a9e',unknown:'#b0a898'};
  // Center node
  var centerR=14;
  ctx.beginPath();ctx.arc(cx,cy,centerR,0,Math.PI*2);
  ctx.fillStyle=lvlColors[selfLevel]||'#b0a898';ctx.fill();
  ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
  ctx.fillStyle='#fff';ctx.font='bold 9px Microsoft YaHei';ctx.textAlign='center';
  var ct=p.n.length>3?p.n.substring(0,3):p.n;ctx.fillText(ct,cx,cy+3);
  // Title
  ctx.fillStyle='#5c5040';ctx.font='9px Microsoft YaHei';
  ctx.fillText('🪷 华严关系',cx,H-4);
  // Limit to 8 connections
  var conns=connections.slice(0,8);if(conns.length===0)return;
  var ringR=Math.min(90,Math.max(50,cy-20));
  conns.forEach(function(conn,i){
    var angle=(i/conns.length)*Math.PI*2-Math.PI/2;
    var nx=cx+Math.cos(angle)*ringR,ny=cy+Math.sin(angle)*ringR;
    // Line
    ctx.beginPath();ctx.moveTo(cx+Math.cos(angle)*centerR,cy+Math.sin(angle)*centerR);
    ctx.lineTo(nx-Math.cos(angle)*8,ny-Math.sin(angle)*8);
    var rc=conn.r==='MASTER'||conn.r==='MASTER_OF'?'#b8863c':conn.r==='INFLUENCED'?'#c8893e':conn.r==='LINEAGE'?'#7d9a6e':'#c0b098';
    ctx.strokeStyle=rc;ctx.lineWidth=conn.r==='MASTER'?2:0.8;ctx.setLineDash(conn.r==='MASTER'?[]:[2,3]);ctx.stroke();ctx.setLineDash([]);
    // Node
    ctx.beginPath();ctx.arc(nx,ny,7,0,Math.PI*2);
    ctx.fillStyle=conn.color;ctx.fill();
    ctx.strokeStyle='#fff';ctx.lineWidth=1;ctx.stroke();
    // Label
    var lbl=conn.n.length>2?conn.n.substring(0,2):conn.n;
    ctx.fillStyle='#fff';ctx.font='7px Microsoft YaHei';ctx.textAlign='center';
    ctx.fillText(lbl,nx,ny+3);
  });
  ctx.textAlign='start';
}

// ═══ PERSON ROSTER (名录·全人物) ═══
function _classifyPerson(p,traj){
  var li=p.li||'',tp=p.tp||'',n=p.n||'';
  var tname=traj?traj.name||'':'';
  // Explicit group field in trajectory data overrides everything
  if(traj&&traj.group)return traj.group;

  // ── 华严宗·内部支系 ──
  if(li==='华严宗'||li==='华严五祖'||li==='华严宗远祖')return '🪷 华严宗·五祖时代';
  if(li==='李通玄系')return '🪷 华严宗·李通玄系';
  if(li==='贤首宗高原法系'||li==='智光系')return '🪷 华严宗·高原法系';
  if(li==='华严莲社')return '🪷 华严宗·华严莲社';
  if(li==='月霞系')return '🪷 华严宗·月霞系';
  if(li==='慈舟系')return '🪷 华严宗·慈舟系';
  if(li==='日本华严')return '🪷 华严宗·日本';
  if(li==='高丽华严')return '🪷 华严宗·朝鲜半岛';
  if(/华严/.test(li))return '🪷 华严宗';

  // ── 禅宗·内部支系 ──
  if(li==='临济宗')return '☸ 禅宗·临济宗';
  if(li==='曹洞宗')return '☸ 禅宗·曹洞宗';
  if(li==='云门宗')return '☸ 禅宗·云门宗';
  if(li==='法眼宗')return '☸ 禅宗·法眼宗';
  if(li==='沩仰宗')return '☸ 禅宗·沩仰宗';
  if(li==='黄龙派')return '☸ 禅宗·黄龙派';
  if(li==='杨岐派')return '☸ 禅宗·杨岐派';
  if(tp==='practitioner'&&/禅|慧能|弘忍|神秀|达摩|马祖/.test(n+tname))return '☸ 禅宗';

  // ── 天台宗 ──
  if(li==='天台宗')return '☸ 天台宗';
  if(/天台|智顗|湛然|知礼/.test(n+tname))return '☸ 天台宗';

  // ── 净土宗 ──
  if(li==='净土宗')return '☸ 净土宗';
  if(/净土|善导|印光|慧远|莲池|昙鸾|道绰|省庵/.test(n+tname))return '☸ 净土宗';

  // ── 法相宗/唯识宗 ──
  if(li==='法相宗'||li==='唯识宗')return '☸ 法相宗·唯识';
  if(/法相|唯识|窥基|圆测/.test(n+tname))return '☸ 法相宗·唯识';

  // ── 三论宗 ──
  if(li==='三论宗')return '☸ 三论宗';
  if(/三论|吉藏|僧肇/.test(n+tname))return '☸ 三论宗';

  // ── 律宗 ──
  if(li==='律宗'||li==='南山律宗')return '☸ 律宗';
  if(/律宗|道宣|鉴真|弘一|元照/.test(n+tname))return '☸ 律宗';

  // ── 密宗/唐密 ──
  if(li==='密宗'||li==='唐密')return '☸ 密宗·唐密';
  if(/密宗|善无畏|金刚智|不空|一行|慧果/.test(n+tname))return '☸ 密宗·唐密';

  // ── 译师·求法僧 (from li field) ──
  if(li==='译师')return '📖 译师';
  if(li==='求法僧')return '🚶 求法僧';

  // ── 藏传佛教·内部支系 ──
  if(li==='藏传佛教·格鲁派'||li==='格鲁派')return '🔴 藏传·格鲁派';
  if(li==='藏传佛教·萨迦派'||li==='萨迦派')return '🔴 藏传·萨迦派';
  if(li==='藏传佛教·宁玛派'||li==='宁玛派')return '🔴 藏传·宁玛派';
  if(li==='藏传佛教·噶举派'||li==='噶举派')return '🔴 藏传·噶举派';
  if(/宗喀巴|达赖|班禅|阿底峡|莲花生/.test(n+tname))return '🔴 藏传佛教';
  if(li==='藏传佛教'||/藏传/.test(li))return '🔴 藏传佛教';

  // ── 印度源流 ──
  if(li==='印度源流'||li==='大乘瑜伽行法')return '🕉 印度佛教·瑜伽行';
  if(/印度|瑜伽|拉克鲁希|巴布基|普拉梵|克利普|胜师子|马鸣|龙树/.test(n+tname))return '🕉 印度佛教';

  // ── 南传佛教 ──
  if(li==='上座部'||li==='南传佛教')return '🟡 南传佛教';

  // ── 近现代学者 ──
  if(li==='当代学者')return '🎓 近现代学者';

  // ── 参考线 ──
  if(li==='参考线')return '🏛 近现代高僧大德';

  // ── 儒家 ──
  if(li==='儒家'||/儒家/.test(li))return '📜 儒家';
  if(/孔子|孟子|荀子|董仲舒|朱熹|王阳明|陆九渊|程颢|程颐|周敦颐|张载|邵雍|韩愈|柳宗元|欧阳修|苏轼|王安石|苏洵|苏辙|曾巩|颜回|子思|司马迁|班昭|郑玄|顾炎武|黄宗羲|王夫之/.test(n+tname))return '📜 儒家';

  // ── 道家·道教 ──
  if(li==='道家'||li==='道教'||/道家/.test(li))return '☯ 道家·道教';
  if(/老子|庄子|列子|张道陵|王重阳|关尹子|葛洪|寇谦之|吕洞宾|陈抟|丘处机|张三丰|陶弘景/.test(n+tname))return '☯ 道家·道教';

  // ── 西方哲学·宗教 ──
  if(li==='西方哲学'||li==='西方')return '🔮 西方哲学·宗教';
  if(/耶稣|穆罕默德|柏拉图|亚里士多德|奥古斯丁|阿奎那|康德|黑格尔/.test(n+tname))return '🔮 西方哲学·宗教';

  // ── 伊斯兰教 ──
  if(li==='伊斯兰教'||/伊斯兰/.test(li))return '☪ 伊斯兰教';
  if(/鲁米|伊本|安萨里|花拉子密/.test(n+tname))return '☪ 伊斯兰教';

  // ── 印度教·耆那教 ──
  if(li==='印度教'||li==='耆那教')return '🕉 印度教·耆那教';
  if(/罗摩克里希纳|辨喜|奥罗宾多|拉玛那/.test(n+tname))return '🕉 印度教·近代';

  // ── 日本佛教(非华严) ──
  if(li==='日本天台宗')return '☸ 日本·天台宗';
  if(li==='日本真言宗')return '☸ 日本·真言宗';
  if(li==='日本禅宗'||li==='日本临济宗'||li==='日本曹洞宗')return '☸ 日本·禅宗';
  if(li==='日本净土宗'||li==='日本净土真宗')return '☸ 日本·净土宗';
  if(li==='日本日莲宗')return '☸ 日本·日莲宗';
  if(/空海|最澄|道元|荣西|日莲|亲鸾|法然/.test(n+tname))return '☸ 日本佛教';

  // ── 朝鲜佛教(非华严) ──
  if(li==='朝鲜佛教'||li==='韩国佛教')return '☸ 朝鲜佛教';
  if(/义天|均如|义湘/.test(n+tname))return '☸ 朝鲜佛教';

  // ── 名相模式匹配(仅对li为空或None的trajectory-only人员生效) ──
  var full=n+tname;
  // ⚠ 顺序关键: 先精确后模糊, 学者/研究者必须在宗派名相之前
  // 近现代学人(胡适等非宗派人物)
  if(/胡适|梁启超|欧阳竟无|吕澂|汤用彤|魏道儒|王颂|邱高兴|张文良/.test(full))return '🎓 近现代学者';
  // 近现代高僧大德
  if(/虚云|太虚|印光|弘一|印顺|梦参|圆瑛|谛闲|倓虚/.test(full))return '🏛 近现代高僧大德';
  // 汉传高僧·古代(具体人名)
  if(/安世高|道安|僧肇|道生|僧祐|永明延寿|大慧宗杲|憨山德清|蕅益智旭|雪窦重显/.test(full))return '☸ 汉传高僧';
  // 译师(具体人名,非泛/译/)
  if(/佛驮跋陀罗|实叉难陀|支娄迦谶|般若|鸠摩罗什|真谛|求那跋陀罗|竺法护|胜友|智军/.test(full))return '📖 译师';
  // 求法僧
  if(/法显|义净|玄奘|慧超/.test(full))return '🚶 求法僧';
  // 天台宗(具体人名)
  if(/智顗|湛然|知礼/.test(full))return '☸ 天台宗';
  // 净土宗(具体人名)
  if(/善导|慧远|莲池|昙鸾|道绰|省庵/.test(full))return '☸ 净土宗';
  // 禅宗各派(具体人名,不用/禅/避免误伤学者)
  if(/慧能|弘忍|神秀|达摩|马祖道一|百丈怀海|黄檗希运|沩山灵祐|石头希迁|赵州从谂|雪峰义存|洞山良价|临济义玄|云门文偃|法眼文益|曹山本寂/.test(full))return '☸ 禅宗';
  // 法相唯识(具体人名)
  if(/窥基|圆测|世亲/.test(full))return '☸ 法相宗·唯识';
  // 三论宗(具体人名)
  if(/吉藏/.test(full))return '☸ 三论宗';
  // 律宗(具体人名)
  if(/道宣|鉴真|元照/.test(full))return '☸ 律宗';
  // 密宗(具体人名)
  if(/善无畏|金刚智|不空|一行|慧果/.test(full))return '☸ 密宗·唐密';
  // 藏传(具体人名)
  if(/宗喀巴|阿底峡|莲花生|米拉日巴|八思巴|寂天/.test(full))return '🔴 藏传佛教';
  // 印度佛教(具体人名)
  if(/马鸣|龙树|无著|拉克鲁希|巴布基|普拉梵|克利普|胜师子/.test(full))return '🕉 印度佛教';
  // 日本佛教(具体人名)
  if(/空海|最澄|道元|荣西|日莲|亲鸾|法然|良弁|明惠|凝然/.test(full))return '☸ 日本佛教';
  // 印度教
  if(/罗摩克里希纳|辨喜|奥罗宾多|拉玛那/.test(full))return '🕉 印度教·近代';
  // 儒家(具体人名)
  if(/孔子|孟子|荀子|董仲舒|朱熹|王守仁|陆九渊|程颢|程颐|周敦颐|张载|邵雍|韩愈|柳宗元|欧阳修|苏轼|王安石|苏洵|苏辙|曾巩|颜回|子思|司马迁|班昭|郑玄|顾炎武|黄宗羲|王夫之/.test(full))return '📜 儒家';
  // 道家(具体人名)
  if(/老子|庄子|列子|张道陵|王重阳|关尹子|葛洪|寇谦之|吕洞宾|陈抟|丘处机|张三丰|陶弘景|司马承祯|白玉蟾|张伯端/.test(full))return '☯ 道家·道教';
  // 西方(具体人名)
  if(/耶稣|柏拉图|亚里士多德|奥古斯丁|阿奎那|康德|黑格尔|穆罕默德/.test(full))return '🔮 西方哲学·宗教';
  // 伊斯兰(具体人名)
  if(/鲁米|伊本|安萨里|花拉子密/.test(full))return '☪ 伊斯兰教';

  // ── 最后防线: 类型推断 ──
  if(tp==='translator')return '📖 译师';
  if(tp==='scholar')return '🎓 近现代学者';

  return '📌 其他';
}
function toggleRoster(){
  var modal=document.getElementById('roster-modal');
  if(!modal)return;
  if(modal.style.display==='flex'){modal.style.display='none';return;}
  renderRoster();modal.style.display='flex';
  modal.onclick=function(e){if(e.target===modal)modal.style.display='none';};
}
function renderRoster(){
  var ct=document.getElementById('roster-content');
  var cnt=document.getElementById('roster-count');
  if(!ct||!cnt)return;
  // Collect ALL persons: graph nodes + trajectory-only figures
  var all=[];
  var seen={};
  DATA.nodes.forEach(function(p){
    if(!p.b&&!p.d)return;
    var traj=PERSON_TRAJECTORIES&&PERSON_TRAJECTORIES[p.id];
    var primary=_classifyPerson(p,traj);
    // Multi-group support: trajectory group field can use ; separator
    var groups=[primary];
    if(traj&&traj.group&&traj.group.indexOf(';')>=0){
      groups=traj.group.split(';').map(function(s){return s.trim();});
    }else if(traj&&traj.group){
      groups=[traj.group];  // explicit single group overrides auto-classification
    }
    all.push({id:p.id,n:p.n,ti:p.ti||'',tp:p.tp||'',li:p.li||'',b:p.b,d:p.d,color:DATA.lineage_colors[p.li]||'#b0a898',groups:groups,ne:_enName(p)});
    seen[p.id]=true;
  });
  // Add trajectory-only persons
  if(PERSON_TRAJECTORIES)for(var tid in PERSON_TRAJECTORIES){
    if(seen[tid])continue;
    var t=PERSON_TRAJECTORIES[tid];if(!t||!t.name||!t.route)continue;
    var yr=t.route[0]?t.route[0].y:null;
    var yr2=t.route[t.route.length-1]?t.route[t.route.length-1].y:null;
    var primary2=_classifyPerson({n:t.name.split('·')[0],li:''},t);
    var groups2=[primary2];
    if(t.group&&t.group.indexOf(';')>=0){
      groups2=t.group.split(';').map(function(s){return s.trim();});
    }else if(t.group){
      groups2=[t.group];
    }
    all.push({id:tid,n:t.name.split('·')[0],ti:t.name,li:'',b:yr,d:yr2,color:t.color||'#b0a898',groups:groups2,ne:''});
    seen[tid]=true;
  }
  cnt.textContent=all.length;
  // Build group index — one person can appear in multiple groups
  var groups={};
  all.forEach(function(p){
    p.groups.forEach(function(g){
      if(!groups[g])groups[g]=[];
      groups[g].push(p);
    });
  });
  // Group order — must match _classifyPerson return values exactly
  var grpOrder=[
    '🪷 华严宗·五祖时代','🪷 华严宗·李通玄系','🪷 华严宗·高原法系','🪷 华严宗·华严莲社',
    '🪷 华严宗·月霞系','🪷 华严宗·慈舟系','🪷 华严宗·日本','🪷 华严宗·朝鲜半岛','🪷 华严宗',
    '☸ 禅宗·临济宗','☸ 禅宗·曹洞宗','☸ 禅宗·云门宗','☸ 禅宗·法眼宗','☸ 禅宗·沩仰宗',
    '☸ 禅宗·黄龙派','☸ 禅宗·杨岐派','☸ 禅宗',
    '☸ 天台宗','☸ 净土宗','☸ 法相宗·唯识','☸ 三论宗','☸ 律宗','☸ 密宗·唐密',
    '📖 译师','🚶 求法僧',
    '🔴 藏传·格鲁派','🔴 藏传·萨迦派','🔴 藏传·宁玛派','🔴 藏传·噶举派','🔴 藏传佛教',
    '🕉 印度佛教·瑜伽行','🕉 印度佛教',
    '🟡 南传佛教',
    '☸ 汉传高僧','🏛 近现代高僧大德','🎓 近现代学者',
    '☸ 日本·天台宗','☸ 日本·真言宗','☸ 日本·禅宗','☸ 日本·净土宗','☸ 日本·日莲宗','☸ 日本佛教',
    '☸ 朝鲜佛教',
    '📜 儒家','☯ 道家·道教',
    '🔮 西方哲学·宗教','☪ 伊斯兰教','🕉 印度教·近代','🕉 印度教·耆那教',
    '📌 其他'
  ];
  var usedGroups={};
  var h='';
  // Render groups in defined order
  grpOrder.forEach(function(g){
    if(!groups[g]||groups[g].length===0)return;
    usedGroups[g]=true;
    h+=_rosterGroupHTML(g,groups[g]);
  });
  // Render any remaining groups not in grpOrder (safety net)
  Object.keys(groups).sort().forEach(function(g){
    if(usedGroups[g]||!groups[g]||!groups[g].length)return;
    h+=_rosterGroupHTML(g,groups[g]);
  });
  ct.innerHTML=h;
}
function _rosterGroupHTML(g,persons){
  var html='<div style="margin-bottom:6px"><b style=color:#b8863c;font-size:0.82em">'+g+'</b> <span style=font-size:0.7em;color:var(--text2)>'+persons.length+'人</span></div>';
  html+='<div style="display:flex;flex-wrap:wrap;gap:3px;margin-bottom:10px">';
  persons.forEach(function(p){
      var yrs=(p.b||'?')+'-'+(p.d||'?');
      var c=p.color||'#b0a898';
      var _tr=PERSON_TRAJECTORIES&&PERSON_TRAJECTORIES[p.id];
      html+='<span onclick="_rosterClick(\''+p.id+'\')" style="cursor:pointer;padding:2px 7px;border-radius:10px;font-size:0.68em;background:'+c+'0d;border:1px solid '+c+'28;white-space:nowrap"'
        +' onmouseover="this.style.background=\''+c+'25\'" onmouseout="this.style.background=\''+c+'0d\'">'
        +(p.tp==='patriarch'?'[祖]':p.tp==='translator'?'[译]':p.tp==='scholar'?'[学]':'')
        +'<b>'+p.n+'</b>'
        +(p.ne?' <span class="en-line" style=color:var(--text2);font-size:0.85em>'+p.ne+'</span>':'')
        +(_tr&&_tr.verified?' <span style=color:#7d9a6e title='+(_tr.source||'')+'>✓</span>':(_tr&&_tr.source?'':' <span style=color:#c46b5d title="来源缺失，存疑待核">⚠️存疑</span>'))
        +' '
        +'<span style=color:var(--text2);font-size:0.9em>'+yrs+'</span></span>';
  });
  html+='</div>';
  return html;
}

// ═══ ROSTER CLICK WRAPPERS (ensure popup shows after modal close) ═══
window._rosterClick=function(pid){
  var m=document.getElementById('roster-modal');if(m)m.style.display='none';
  setTimeout(function(){
    if(nodeMap&&nodeMap[pid]){
      selectPerson(pid);
    }else{
      // Trajectory-only person: clear old markers, show trajectory + brief info
      _clearTrajMarkers();
      var traj=PERSON_TRAJECTORIES&&PERSON_TRAJECTORIES[pid];
      if(traj&&traj.route&&traj.route.length&&mapMain){
        showTrajectoryOnMap(pid);
        var popup=document.getElementById('info-popup');
        if(popup){
          var h='<span class=close-btn onclick="var p=document.getElementById(&quot;info-popup&quot;);if(p)p.style.display=&quot;none&quot;">&times;</span>'
            +'<h3>'+traj.name+'</h3>'
            +'<p style=font-size:0.78em;color:var(--text2)>共'+traj.route.length+'个足迹节点</p>'
            +'<button onclick="playTrajectory(&quot;'+pid+'&quot;)" style="padding:3px 10px;border:1px solid '+(traj.color||'#b8863c')+';border-radius:12px;background:var(--card);color:'+(traj.color||'#b8863c')+';cursor:pointer;font-size:0.72em">播放足迹</button>';
          if(traj.source)h+='<div style=margin-top:4px;font-size:0.65em;color:var(--text2)>'+traj.source+'</div>';
          popup.innerHTML=h;popup.style.display='block';
          popup.style.left='60vw';popup.style.top='10vh';
          if(popup._autoTimer)clearTimeout(popup._autoTimer);
          popup._autoTimer=setTimeout(function(){popup.style.display='none';},15000);
        }
      }
    }
  },80);
};
window._templeClick=function(tid){
  var m=document.getElementById('roster-modal');if(m)m.style.display='none';
  setTimeout(function(){showTempleInfo(tid);},80);
};

// ═══ TEMPLE DIRECTORY (道场名录) ═══
var TEMPLE_DATA=null;
function toggleTempleDir(){
  var modal=document.getElementById('roster-modal'); // reuse same modal
  if(!modal)return;
  if(modal.style.display==='flex'&&modal._mode==='temple'){modal.style.display='none';return;}
  renderTempleDir();modal.style.display='flex';modal._mode='temple';
  modal.onclick=function(e){if(e.target===modal)modal.style.display='none';};
}
function renderTempleDir(){
  var ct=document.getElementById('roster-content');
  var cnt=document.getElementById('roster-count');
  if(!ct||!cnt)return;
  // Load temple data from EVENTS (auto-loaded by build)
  var temples=[];
  try{if(typeof TEMPLE_DIRECTORY!=='undefined'&&TEMPLE_DIRECTORY&&TEMPLE_DIRECTORY.temples)temples=TEMPLE_DIRECTORY.temples;}catch(e){}
  if(temples.length===0){ct.innerHTML='<p style=color:var(--text2)>道场数据未加载</p>';return;}
  cnt.textContent=temples.length;
  // Group by school
  var groups={},order=['华严宗','华严宗·普贤乘','贤首宗高原法系','禅宗','禅宗·临济宗','天台宗','净土宗','律宗·南山律','法相宗','三论宗','密宗','藏传·格鲁派','藏传佛教','日本华严宗','日本真言宗','高丽华严宗','印度佛教','道家','道家·天师道','道家·全真','道家·丹鼎派','儒家','儒家·理学'];
  temples.forEach(function(t){
    var s=t.school||'其他';
    if(!groups[s])groups[s]=[];
    groups[s].push(t);
  });
  var h='<div id=roster-title style="font-size:0.8em;color:var(--gold);margin-bottom:8px">🏛 道场名录 — 按宗派分组 · 点击查看详情</div>';
  order.concat(Object.keys(groups).filter(function(k){return order.indexOf(k)<0;})).forEach(function(s){
    if(!groups[s]||groups[s].length===0)return;
    h+='<div style="margin-bottom:6px"><b style=color:#b8863c;font-size:0.8em>'+s+'</b> <span style=font-size:0.68em;color:var(--text2)>'+groups[s].length+'座</span></div>';
    h+='<div style="display:flex;flex-wrap:wrap;gap:3px;margin-bottom:8px">';
    groups[s].forEach(function(t){
      var v=t.verified?' ✓':'';
      h+='<span onclick="_templeClick(\''+t.id+'\')" style="cursor:pointer;padding:3px 8px;border-radius:10px;font-size:0.68em;background:rgba(184,134,60,0.06);border:1px solid rgba(184,134,60,0.2);white-space:nowrap"'
        +' onmouseover="this.style.background=\'rgba(184,134,60,0.2)\'" onmouseout="this.style.background=\'rgba(184,134,60,0.06)\'">'
        +'<b>'+t.name+'</b>'
        +(v?'<span style=color:#7d9a6e title=已核实>'+v+'</span>':'')
        +' <span style=font-size:0.85em;color:var(--text2)>'+t.location+'</span></span>';
    });
    h+='</div>';
  });
  ct.innerHTML=h;
}
function showTempleInfo(tid){
  var modal=document.getElementById('roster-modal');if(modal)modal.style.display='none';
  var temples=[];try{if(typeof TEMPLE_DIRECTORY!=='undefined'&&TEMPLE_DIRECTORY)temples=TEMPLE_DIRECTORY.temples||[];}catch(e){console.error('TEMPLE_DIRECTORY error:',e);}
  if(temples.length===0){console.error('TEMPLE_DIRECTORY empty');return;}
  var t=temples.find(function(x){return x.id===tid;});
  if(!t){console.error('Temple not found:',tid);return;}
  var popup=document.getElementById('info-popup');if(!popup){console.error('popup not found');return;}
  var h='<span class=close-btn onclick="document.getElementById(\'info-popup\').style.display=\'none\'">&times;</span>'
    +'<h3 style=color:#b8863c>🏛 '+t.name+'</h3>'
    +'<span class=tag style=background:rgba(184,134,60,0.1)><b>'+t.school+'</b></span> '
    +'<span class=tag>'+t.type+'</span> '
    +'<span class=tag>'+t.dynasty+'</span>'
    +(t.verified?'<span class=tag style=background:rgba(125,154,110,0.1);color:#7d9a6e>✓ 已核实</span>':'')
    +'<br>📍 <b>'+t.location+'</b>'+(t.ancient_name?' <span style=font-size:0.65em;color:var(--text2)>('+t.ancient_name+')</span>':'')
    +' · 📅 '+t.founded
    +(t.founder?' · 👤 '+t.founder:'')
    +'<br>📝 <span style=font-size:0.78em;line-height:1.6>'+t.description+'</span>'
    +(t.significance?'<br>⭐ <b style=color:#b8863c>'+t.significance+'</b>':'')
    +(t.events&&t.events.length?'<br>📜 重大事件: '+t.events.join(' · '):'')
    +(t.source?'<div style="margin-top:3px;font-size:0.65em;color:var(--text2);opacity:0.7">📚 '+t.source+'</div>':'')
    +(t.links&&t.links.length?'<div style=margin-top:4px>🔗 '+t.links.map(function(l){return '<a href='+l.url+' target=_blank style=color:var(--blue);font-size:0.7em>'+l.name+'</a>';}).join(' · ')+'</div>':'');
  popup.style.zIndex='2001'; // Above roster-modal (2000)
  popup.innerHTML=h;popup.style.display='block';popup.style.visibility='visible';popup.style.opacity='1';
  popup.style.left='55vw';popup.style.top='8vh';popup.style.width='320px';
  popup.onclick=function(e){if(e.target.tagName!=='BUTTON'&&e.target.tagName!=='A')popup.style.display='none';};
  if(popup._autoTimer)clearTimeout(popup._autoTimer);
  popup.onmouseenter=function(){if(popup._autoTimer)clearTimeout(popup._autoTimer);};
  popup.onmouseleave=function(){popup._autoTimer=setTimeout(function(){popup.style.display='none';},5000);};
  popup._autoTimer=setTimeout(function(){popup.style.display='none';},15000);
  // Fly map to temple location
  if(mapMain&&t.lat&&t.lng){setTimeout(function(){mapMain.flyTo([t.lat,t.lng],12,{duration:1});},100);}
}

// ═══ DYNASTY VISIBILITY (古地图随年份变化) ═══
function updateDynastyVisibility(year){
  dynastyLayers.forEach(function(d){
    var visible = year >= d.db.s && year <= d.db.e;
    if(d.rect._map !== mapMain && visible) { d.rect.addTo(mapMain); d.label.addTo(mapMain); }
    else if(d.rect._map === mapMain && !visible) { mapMain.removeLayer(d.rect); mapMain.removeLayer(d.label); }
    if(visible && d.rect._map === mapMain) {
      d.rect.setStyle({fillOpacity: 0.08, weight: 2});
      d.label.setOpacity(1);
    }
  });
}
var _MINI_REGIONS=[
  {id:'huayan',label:'☸ 汉传诸宗',key:'han_buddhist_schools',color:'#c46b5d',center:[32,110],zoom:4},
  {id:'chinese',label:'📜 东亚儒道',key:'east_asian_thought',color:'#b8863c',center:[37,120],zoom:4},
  {id:'south_asia',label:'🕉 南亚次大陆',key:'south_asia_timeline',color:'#e08040',center:[22,80],zoom:4},
  {id:'southeast_asia',label:'🛕 东南亚',key:'southeast_asia_timeline',color:'#4a9e8e',center:[12,106],zoom:4},
  {id:'mena',label:'🌙 中东·中亚·北非',key:'mena_timeline',color:'#d4784c',center:[30,40],zoom:3},
  {id:'west',label:'🏛 欧洲',key:'western_timeline',color:'#5e8b9e',center:[48,10],zoom:3},
  {id:'africa',label:'🌴 撒哈拉以南非洲',key:'africa_timeline',color:'#7d9a6e',center:[0,25],zoom:3},
  {id:'north_america',label:'🦅 北美·中美',key:'north_america_timeline',color:'#d48476',center:[35,-100],zoom:3},
  {id:'south_america',label:'🦜 南美洲',key:'south_america_timeline',color:'#c8893e',center:[-12,-65],zoom:3},
  {id:'oceania',label:'🏝 大洋洲',key:'oceania_timeline',color:'#8b7a9e',center:[-20,160],zoom:3}
];
function _getEvents(data){
  if(!data)return null;
  if(data.events)return data.events;
  if(Array.isArray(data))return data.filter(function(w){return w.lat&&w.lng;});
  return null;
}
function initMiniMaps(){
  var grid=document.getElementById('mini-maps-grid');if(!grid)return;
  _MINI_REGIONS.forEach(function(r){
    var wrap=document.createElement('div');
    wrap.style.cssText='flex:0 0 170px;position:relative;border:2px solid '+r.color+';border-radius:6px;overflow:hidden;background:#fdfaf3;height:105px';
    var mapDiv=document.createElement('div');mapDiv.style.cssText='width:100%;height:100%';
    wrap.appendChild(mapDiv);
    var lbl=document.createElement('div');
    lbl.style.cssText='position:absolute;top:2px;left:4px;font-size:7px;color:'+r.color+';z-index:700;pointer-events:none;font-weight:600;line-height:1.2';
    lbl.textContent=r.label;wrap.appendChild(lbl);
    var evLbl=document.createElement('div');
    evLbl.style.cssText='position:absolute;bottom:2px;left:2px;right:2px;font-size:6.5px;color:#fff;background:rgba(0,0,0,0.55);padding:1px 3px;border-radius:2px;pointer-events:none;line-height:1.2;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;z-index:700;display:none';
    evLbl.id='mm-ev-'+r.id;wrap.appendChild(evLbl);grid.appendChild(wrap);
    setTimeout(function(){
      var m=L.map(mapDiv,{zoomControl:false,attributionControl:false,zoomSnap:0.5,zoomDelta:0.5}).setView(r.center,r.zoom);
      tileLayer().addTo(m);
      var data=null;
      try{var vn=r.key.toUpperCase();if(window[vn])data=window[vn];else if(typeof EVENTS!=='undefined'&&EVENTS[r.key])data=EVENTS[r.key];}catch(e){}
      var evts=_getEvents(data);
      if(evts&&evts.length>1){
        var pts=evts.map(function(w){return [w.lat,w.lng];});
        L.polyline(pts,{color:r.color,weight:1.5,opacity:0.5}).addTo(m);
      }
      var mk=L.circleMarker(r.center,{radius:5,fillColor:r.color,color:'#ffe066',weight:2,fillOpacity:0.9}).addTo(m);
      _miniMaps[r.id]={map:m,marker:mk,dataKey:r.key,color:r.color,evLbl:evLbl};
    },r.id==='huayan'?50:200);
  });
}
function updateMiniMaps(year){
  Object.keys(_miniMaps).forEach(function(id){
    var mm=_miniMaps[id];if(!mm||!mm.map)return;
    var data=null;
    try{var vn=mm.dataKey.toUpperCase();if(window[vn])data=window[vn];else if(typeof EVENTS!=='undefined'&&EVENTS[mm.dataKey])data=EVENTS[mm.dataKey];}catch(e){}
    var evts=_getEvents(data);if(!evts||!evts.length)return;
    var best=null;
    evts.forEach(function(w){if(w.y<=year&&(!best||w.y>best.y))best=w;});
    if(!best||!best.lat)return;
    mm.marker.setLatLng([best.lat,best.lng]);mm.map.panTo([best.lat,best.lng],{animate:false});
    // Update event label
    if(mm.evLbl){
      mm.evLbl.style.display='block';
      mm.evLbl.textContent=best.y+'年 '+best.label;
    }
  });
}
// ═══ LAYER TOGGLE ═══
function toggleLayer(layer){
  layerVis[layer]=!layerVis[layer];
  var btn=document.querySelector('#controls button[data-layer="'+layer+'"]');
  if(btn){if(layerVis[layer]){btn.classList.add('active');}else{btn.classList.remove('active');}}
  drawTL(selectedId);
}

// ═══ TRANSMISSION STORY (人物+事件串讲·取代粗糙线段) ═══
// TRANS_STORY source of truth: data/events/transmission_story.yaml (injected as TRANSMISSION_STORY, wrapped .story)
TRANS_STORY=(typeof TRANSMISSION_STORY!=='undefined'&&TRANSMISSION_STORY&&TRANSMISSION_STORY.story)?TRANSMISSION_STORY.story:[];

var transMarkers=[],transLines=[],otherSchoolsMarkers=[];

function initTransStory(){
  if(!map)return;
  transMarkers.forEach(function(m){mapMain.removeLayer(m);});
  transLines.forEach(function(l){mapMain.removeLayer(l);});
  transMarkers=[];transLines=[];
  // Draw connecting lines between consecutive story points
  for(var i=1;i<TRANS_STORY.length;i++){
    var prev=TRANS_STORY[i-1],cur=TRANS_STORY[i];
    var l=L.polyline([[prev.lat,prev.lng],[cur.lat,cur.lng]],{color:'#b8863c',weight:1.5,opacity:0.35,dashArray:'5,8'}).addTo(mapMain);
    transLines.push(l);
  }
  // Draw story markers (small numbered circles)
  TRANS_STORY.forEach(function(ts,i){
    var sz=ts.p==='杜顺'||ts.p==='法藏'||ts.p.indexOf('华严')>=0?20:14;
    var icon=L.divIcon({html:'<div style=background:#b8863c;color:#fff;border-radius:50%;width:'+sz+'px;height:'+sz+'px;text-align:center;line-height:'+sz+'px;font-size:'+(sz>14?'9':'7')+'px;font-weight:700;border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,0.2)>'+(i+1)+'</div>',iconSize:[sz,sz],iconAnchor:[sz/2,sz/2]});
    var m=L.marker([ts.lat,ts.lng],{icon:icon}).addTo(mapMain);
    m.bindPopup('<b>['+(i+1)+'] '+ts.y+'年</b> · '+ts.p+'<br>'+ts.ev+'<br><span style=font-size:0.68em;color:var(--text2)>源: '+ts.src+'</span>');
    transMarkers.push(m);
  });
}

// OTHER_SCHOOLS source of truth: data/events/other_schools.yaml (injected as OTHER_SCHOOLS, wrapped .schools)
OTHER_SCHOOLS=(typeof OTHER_SCHOOLS!=='undefined'&&OTHER_SCHOOLS&&OTHER_SCHOOLS.schools)?OTHER_SCHOOLS.schools:[];
function initOtherSchools(){
  if(!map)return;
  otherSchoolsMarkers.forEach(function(m){mapMain.removeLayer(m);});
  otherSchoolsMarkers=[];
  OTHER_SCHOOLS.forEach(function(s){
    var icon=L.divIcon({html:'<div style=background:'+s.c+';color:#fff;border-radius:50%;width:22px;height:22px;text-align:center;line-height:22px;font-size:10px;font-weight:700;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.2)>'+s.n[0]+'</div>',iconSize:[22,22],iconAnchor:[11,11]});
    var m=L.marker([s.lat,s.lng],{icon:icon}).addTo(mapMain);
    m.bindPopup('<b>'+s.n+'</b> ('+s.y+'年·'+s.loc+')<br>创始人: '+s.founder+'<br><span style=font-size:0.8em>'+s.desc+'</span>');
    m._school=s;
    otherSchoolsMarkers.push(m);
  });
}

// ═══ ROUTE INFO ═══
function toggleRouteInfo(){
  var ri=document.getElementById('route-info');
  // Create route-info div dynamically if missing (GitHub Pages stale deploy workaround)
  if(!ri){
    ri=document.createElement('div');ri.id='route-info';
    ri.style.cssText='display:none;position:absolute;bottom:8px;left:8px;right:8px;background:rgba(254,253,249,0.9);border:1px solid var(--line);border-radius:6px;padding:6px 10px;font-size:0.68em;color:var(--text2);z-index:500;line-height:1.5';
    ri.innerHTML='🪷 <span style=color:#c46b5d>佛教·华严</span> <span style=color:#e08040>南亚</span> <span style=color:#b8863c>儒家</span> <span style=color:#7d9a6e>道家</span> <span style=color:#5e8b9e>西方</span> <span style=color:#4a9e8e>伊斯兰</span> <span style=color:#c8893e>非洲</span> <span style=color:#d48476>美洲</span> <span style=color:#8b7a9e>大洋洲</span> — 彩色路线代表全球文明传统的传播与交融';
    var mw=document.getElementById('map-main-wrap');if(mw)mw.appendChild(ri);
  }
  if(!ri)return;
  if(ri.style.display==='none'||!ri.style.display){ri.style.display='block';ri._autoTimer=setTimeout(function(){ri.style.display='none';},8000);}
  else{ri.style.display='none';if(ri._autoTimer)clearTimeout(ri._autoTimer);}
  ri.onmouseenter=function(){if(ri._autoTimer)clearTimeout(ri._autoTimer);};
  ri.onmouseleave=function(){ri._autoTimer=setTimeout(function(){ri.style.display='none';},3000);};
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
      if(hoveredId!==pp.id){hoveredId=pp.id;drawTL(selectedId);}
      var ti=TYPE_ICONS[pp.tp]||'';var lc=DATA.lineage_colors[pp.li]||"#b0a898";
      var locs=getPersonLocs(pp.id);var locTxt=locs.length?'📍 '+locs[0].n:'';
      var ageTxt=(pp.b&&pp.d)?' ('+(pp.d-pp.b)+'岁)':'';
      var stuCount=DATA.edges.filter(function(e){return e.s===pp.id&&e.r==="MASTER";}).length;
      var tchCount=DATA.edges.filter(function(e){return e.t===pp.id&&e.r==="MASTER";}).length;
      var relTxt='';if(tchCount||stuCount)relTxt='⬆'+tchCount+' ⬇'+stuCount+' · ';
      tip.style.opacity="1";
      tip.innerHTML="<div style=font-size:0.85em><b style=color:"+lc+">"+(ti||"?")+"</b> <b>"+pp.n+"</b> <span style=color:var(--text2)>"+pp.dy+"</span></div>"
	        +"<div style=font-size:0.7em;color:var(--text2);line-height:1.3>"+(pp.ti||"")+"</div>"
	        +_enNameHtml(pp)
	        +(pp.b?"<div style=font-size:0.65em;color:#a09080>"+pp.b+"–"+(pp.d||"—")+ageTxt+" "+locTxt+"</div>":"");
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
  // Click during animation → pause/resume
  if(animPlaying){if(animPaused){resumeAnim();}else{pauseAnim();}return;}
  var p=document.getElementById("tl-panel"),r=p.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  for(var i=0;i<tl.rowLabels.length;i++){
    var rl=tl.rowLabels[i];
    if(mx>=rl.x&&mx<=rl.x+rl.w&&my>=rl.y&&my<=rl.y+rl.h){zoomToLineage(rl.lineage);return;}
  }
  var hit=tl.hitRects.find(function(h){return mx>=h.x&&mx<=h.x+h.w&&my>=h.y&&my<=h.y+h.h;});
  if(hit){selectPerson(hit.person.id,e.shiftKey,e);}else{clearSelection();}
}

// ═══ ANIMATION (dual map sync) ═══
var animTimer=null,animYear=-600,animPlaying=false;
var animRouteLineM=null,animRouteMarkerM=null; // macro
var animRouteLineU=null,animRouteMarkerU=null,animRelLines=[]; // micro + per-religion
// ANIM_WAYPOINTS source of truth: data/events/anim_waypoints.yaml (wrapped .waypoints)
ANIM_WAYPOINTS=(typeof ANIM_WAYPOINTS!=='undefined'&&ANIM_WAYPOINTS&&ANIM_WAYPOINTS.waypoints)?ANIM_WAYPOINTS.waypoints:[];
var lastAnimLoc=-1;
function getAnimSpeed(){
  var s=document.getElementById('anim-speed');
  // slider 5-40: left=slow(600ms), right=fast(75ms)
  return s?Math.max(60,(45-parseInt(s.value))*15):225;
}
var animPaused=false;
var _seekBusy=false;
function animSeek(yr){
  if(_seekBusy)return;_seekBusy=true;
  animPaused=true;clearTimeout(animTimer);
  animYear=parseInt(yr);lastAnimLoc=-1;
  var py=document.getElementById('prog-year');if(py)py.textContent=animYear+'年';
  tl.minX=animYear-100;tl.maxX=animYear+300;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);
  if(ancientMode)updateDynastyVisibility(animYear);
  updateMiniMaps(animYear);
  var sb=document.getElementById('anim-status');if(sb)sb.style.opacity='1';
  // Find the closest waypoint at or before animYear
  var bestWp=null;
  for(var i=0;i<ANIM_WAYPOINTS.length;i++){if(ANIM_WAYPOINTS[i].y<=animYear)bestWp=ANIM_WAYPOINTS[i];}
  if(bestWp){
    var wp=bestWp;
    if(mapMain&&!wp.bg){
      mapMain.flyTo([wp.lat,wp.lng],Math.max(3,wp.z-2),{duration:1});
      if(animRouteMarkerM)animRouteMarkerM.setLatLng([wp.lat,wp.lng]);
    }
    if(animRouteMarkerU)animRouteMarkerU.setLatLng([wp.lat,wp.lng]);
    if(sb)sb.innerHTML='<b>'+wp.y+'年</b> '+wp.label;
  }
  _seekBusy=false;
}
function animJump(dir){
  animPlaying=true;animPaused=true;
  var pg=document.getElementById('anim-progress');
  var cur=(pg?parseInt(pg.value):animYear)+dir*5;
  if(cur<-1500)cur=-1500;if(cur>2030)cur=2030;
  animSeek(cur);
}
function pauseAnim(){
  if(!animPlaying||animPaused)return;
  animPaused=true;clearTimeout(animTimer);
  document.getElementById("anim-btn").textContent="▶ 继续";
  
}
function resumeAnim(){
  if(!animPaused)return;
  animPaused=false;
  document.getElementById("anim-btn").textContent="⏸ 暂停";
  
  animTimer=setTimeout(animTick,getAnimSpeed());
}
function stopAnim(){
  clearTimeout(animTimer);animPlaying=false;animPaused=false;lastAnimLoc=-1;
  animYear=-600;
  document.getElementById("anim-btn").textContent="▶ 播放";
  document.getElementById("anim-stop-btn").style.display="none";
  
  
  var sb=document.getElementById('anim-status');if(sb){sb.style.opacity='0';sb.innerHTML='';}
  var py=document.getElementById('prog-year');if(py)py.textContent='-600年';
  var pg=document.getElementById('anim-progress');if(pg)pg.value=-600;
  var sl=document.getElementById('speed-label');if(sl)sl.textContent='1x';
  [animRouteLineM,animRouteMarkerM,animRouteLineU,animRouteMarkerU].forEach(function(l){if(l&&mapMain)mapMain.removeLayer(l);});
  animRouteLineM=animRouteMarkerM=animRouteLineU=animRouteMarkerU=null;
  if(mapMain)mapMain.off('click');
  tl.minX=100;tl.maxX=2060;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);
}
function animTick(){
  if(!animPlaying||animPaused)return;
  var speedLabel=document.getElementById('speed-label');
  var delay=getAnimSpeed();
  if(speedLabel){var x=(150/delay).toFixed(1);speedLabel.textContent=(x==='1.0'?'1':x)+'x';}
  // Adaptive step: count waypoints in next 50 years → adjust speed
  var density=0;
  for(var d=0;d<ANIM_WAYPOINTS.length;d++){if(ANIM_WAYPOINTS[d].y>animYear&&ANIM_WAYPOINTS[d].y<=animYear+50)density++;}
  var step=Math.max(1,Math.min(20,Math.round(10-density*2)));
  animYear+=step;
  var pg=document.getElementById('anim-progress');if(pg)pg.value=animYear;
  var py=document.getElementById('prog-year');if(py)py.textContent=animYear+'年';
  tl.minX=animYear-100;tl.maxX=animYear+300;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);
  if(ancientMode)updateDynastyVisibility(animYear);
  // Sync Western mini-map
  updateMiniMaps(animYear);
  var sb=document.getElementById('anim-status');if(sb)sb.style.opacity='1';
  // Stop AFTER processing year 2030
  if(animYear>2030){
    animPlaying=false;animPaused=false;lastAnimLoc=-1;
    document.getElementById("anim-btn").textContent="▶ 播放";
    document.getElementById("anim-stop-btn").style.display="none";
    
    
    if(speedLabel)speedLabel.textContent='1x';if(sb)sb.style.opacity='0';
    return;
  }
  // Find matching waypoint + show popup
  for(var i=0;i<ANIM_WAYPOINTS.length;i++){
    var wp=ANIM_WAYPOINTS[i];
    if(animYear>=wp.y&&lastAnimLoc<i){
      if(mapMain){
        if(!wp.bg){
          mapMain.flyTo([wp.lat,wp.lng],Math.max(3,wp.z-2),{duration:1.5});
          mapMain.closePopup();
          var relColor=REL_COLORS[wp.rel||'buddhist']||'#c46b5d';
          // Stagger popup by religion: buddhist=center, confucian=right, daoist=left, western=top-right
          var popupOffset={buddhist:[0,-12],indic:[15,-18],confucian:[30,-20],daoist:[-30,-8],western:[20,-30],islamic:[-20,-25],african:[-15,10],american:[25,10],oceanic:[30,20]};
          var off=popupOffset[wp.rel||'buddhist']||[0,-10];
          var pc='<div style=max-width:240px><b style=color:'+relColor+'>'+wp.y+'年</b><br><b>'+wp.label+'</b><br><span style=font-size:0.75em;line-height:1.4>'+wp.info+'</span></div>';
          L.popup({closeButton:false,autoClose:false,className:'anim-popup',maxWidth:200,autoPan:false,offset:L.point(off[0],off[1])})
            .setLatLng([wp.lat+0.3,wp.lng+0.2]).setContent(pc).openOn(mapMain);
        }
        if(animRouteMarkerM)animRouteMarkerM.setLatLng([wp.lat,wp.lng]);
      }
      if(animRouteMarkerU)animRouteMarkerU.setLatLng([wp.lat,wp.lng]);
      // ── Stage card: 寻找此年代前后活跃的人物, 制造「聚光灯」效果 ──
      var eraPersons=DATA.nodes.filter(function(nd){
        return nd.b&&nd.b>=wp.y-80&&nd.b<=wp.y+20&&nd.dy&&nd.tp&&nd.tp!=="scholar";
      }).slice(0,3);
      var eraHTML='';
      eraPersons.forEach(function(ep,ei){
        var elc=DATA.lineage_colors[ep.li]||"#b0a898";
        var etype=(ep.tp==="patriarch"?"祖":ep.tp==="translator"?"译":"修");
        eraHTML+='<span style=display:inline-block;margin:2px 4px;padding:2px 6px;border-radius:4px;font-size:0.7em;'
          +'background:'+elc+'18;border:1px solid '+elc+'40;'
          +(ei===0?'opacity:1':'opacity:0.55;filter:brightness(0.8)')
          +'>'+etype+' <b>'+ep.n+'</b> '+(ep.b||"")+'–'+(ep.d||"")+'</span>';
      });
      if(sb){sb.style.opacity='1';sb.innerHTML='<b style=color:'+relColor+'>'+wp.y+'年</b> '+wp.label
        +(eraHTML?' <span style=font-size:0.75em>🎭 '+eraHTML+'</span>':'');}
      lastAnimLoc=i;break;
    }
  }
  animTimer=setTimeout(animTick,delay);
}
function toggleAnim(){
  var speedLabel=document.getElementById('speed-label');
  // ── Resume from pause ──
  if(animPaused){resumeAnim();return;}
  // ── STOP ──
  if(animPlaying){
    clearTimeout(animTimer);animPlaying=false;animPaused=false;lastAnimLoc=-1;
    document.getElementById("anim-btn").textContent="▶ 播放";
    
    
    var sb2=document.getElementById('anim-status');if(sb2){sb2.style.opacity='0';sb2.innerHTML='';}
    [animRouteLineM,animRouteMarkerM,animRouteLineU,animRouteMarkerU].forEach(function(l){if(l&&mapMain)mapMain.removeLayer(l);});
    animRouteLineM=animRouteMarkerM=animRouteLineU=animRouteMarkerU=null;
    if(mapMain)mapMain.off('click');
    if(speedLabel)speedLabel.textContent='1x';
    transLines.forEach(function(l){l.setStyle({opacity:0.35,weight:1.5});});
    return;
  }
  // ── START ──
  animPlaying=true;animPaused=false;document.getElementById("anim-btn").textContent="⏸ 暂停";document.getElementById("anim-stop-btn").style.display="inline";
  animYear=-1500;lastAnimLoc=-1;
  tl.minX=animYear-100;tl.maxX=animYear+300;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);

  // Per-religion colors (global REL_COLORS) + weight/dash per layer
  var rcWeight={buddhist:4,confucian:2.5,daoist:2.5,western:2,islamic:2};
  var rcDash={buddhist:null,confucian:'6,4',daoist:'4,6',western:'3,5',islamic:'8,4'};
  // Init both maps with global view
  if(mapMain){
    mapMain.setView([28,78],3);
    // Per-religion colored routes on MAIN map (multi-layer visualization)
    animRelLines.forEach(function(l){if(mapMain)mapMain.removeLayer(l);});animRelLines=[];
    Object.keys(REL_COLORS).forEach(function(k){
      var pts=ANIM_WAYPOINTS.filter(function(w){return (w.rel||'buddhist')===k;}).map(function(w){return [w.lat,w.lng];});
      if(pts.length>1){
        var rl=L.polyline(pts,{color:REL_COLORS[k],weight:rcWeight[k]||2,opacity:k==='buddhist'?0.75:0.45,
          dashArray:rcDash[k]||null}).addTo(mapMain);
        animRelLines.push(rl);
      }
    });
    animRouteMarkerM=L.circleMarker([28,78],{radius:9,fillColor:'#b8863c',color:'#ffe066',weight:3,fillOpacity:0.95}).addTo(mapMain);
    // Click map to pause/resume
    mapMain.off('click');mapMain.on('click',function(){if(animPlaying){if(animPaused)resumeAnim();else pauseAnim();}});
  }
  animTimer=setTimeout(animTick,getAnimSpeed());
}

// ═══ TABS (safe: skip if standalone page has no #tabs) ═══
var _tabs=document.getElementById("tabs");
if(_tabs){
  _tabs.addEventListener("click",function(e){
    if(e.target.tagName!=="BUTTON")return;
    switchTab(e.target.dataset.tab);
  });
}
function switchTab(tab){
  var tb=document.getElementById("tabs");if(!tb)return;
  document.querySelectorAll("#tabs button").forEach(function(b){b.classList.remove("active");});
  var btn=document.querySelector("#tabs button[data-tab="+tab+"]");
  if(btn)btn.classList.add("active");
  document.querySelectorAll(".tab-content").forEach(function(t){t.classList.remove("active");});
  var tc=document.getElementById("tab-"+tab);
  if(tc)tc.classList.add("active");
  location.hash=tab;
  if(tab==="lineage"){setTimeout(function(){resizeTL();drawTL(selectedId);if(mapMain)mapMain.invalidateSize();},200);}
  if(tab==="practice"){setTimeout(function(){if(typeof renderPractice==="function")renderPractice();},100);}
}
// Restore hash (safe)
(function(){
  var hash=window.location.hash.replace('#','');
  if(!hash||['lineage','practice','gap','cosmology','frontier'].indexOf(hash)<0)return;
  var tb=document.getElementById("tabs");if(!tb)return;
  var ab=document.querySelector('#tabs button.active');
  if(ab)ab.classList.remove('active');
  var btn=document.querySelector('#tabs button[data-tab='+hash+']');
  if(btn)btn.classList.add('active');
  document.querySelectorAll('.tab-content').forEach(function(t){t.classList.remove('active');});
  var tc=document.getElementById('tab-'+hash);
  if(tc)tc.classList.add('active');
  if(hash==='lineage'){setTimeout(function(){resizeTL();drawTL(selectedId);if(mapMain)mapMain.invalidateSize();},300);}
})();
if(location.hash){var h=location.hash.slice(1);if(document.getElementById("tab-"+h))switchTab(h);}
