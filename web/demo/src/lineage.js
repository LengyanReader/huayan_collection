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
  return '👤47人 · 📅跨度'+span+'年 · ⏳最长传承间隙'+maxGap+'年';
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
  tl.H=Math.max(p.clientHeight,rows*MIN_ROW_H+20);
  dps=window.devicePixelRatio||1;
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
    var slots=[];
    sorted.forEach(function(p){
      var b=p.b||(p.d?p.d-ds:null),d=p.d||(p.b?p.b+ds:null);if(!b&&!d)return;
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
      var b=p.b||(p.d?p.d-ds:null),d=p.d||(p.b?p.b+ds:null);if(!b&&!d)return;
      var bx=tX(b||d-10),dx=tX(d||b+10),bh=Math.min(22,rh*0.35),by=y2-bh/2+(p._yOff||0);
      var isHL=p.id===hlId,matches=!isSearch||p.n.indexOf(searchQuery)>=0;
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

  // 8. EVENT MARKERS (staggered y for nearby events)
  if(layerVis.events&&!isOverview){
    var evY0=H-26;
    // Sort events, stagger y for close ones
    var evPositions=[];
    KEY_EVENTS.forEach(function(ev){
      var x=tX(ev.y);if(x<0||x>W)return;
      evPositions.push({x:x,ev:ev});
    });
    // Assign y levels
    evPositions.forEach(function(ep,i){
      ep.level=0;
      for(var j=0;j<i;j++){
        if(Math.abs(ep.x-evPositions[j].x)<80)ep.level++;
      }
      ep.level=Math.min(ep.level,2);
    });
    evPositions.forEach(function(ep){
      var x=ep.x,ev=ep.ev,ey=evY0-ep.level*14;
      if(ev.p&&layerVis.edges){
        var pHR=tl.hitRects.find(function(h){return h.person.n===ev.p||h.person.id===ev.p;});
        if(pHR){
          ctx.strokeStyle='rgba(180,134,60,0.2)';ctx.lineWidth=0.8;ctx.setLineDash([2,4]);
          ctx.beginPath();ctx.moveTo(x,ey);ctx.lineTo(pHR.x+pHR.w/2,pHR.y+pHR.h);ctx.stroke();
          ctx.setLineDash([]);
        }
      }
      ctx.fillStyle=ev.c;ctx.font='bold 10px Microsoft YaHei';
      var evTxt=truncText(ctx,ev.l,W-x-4);
      ctx.fillText('▸ '+evTxt,x,ey);
    });
    // Year labels
    ctx.fillStyle='#a09080';ctx.font=f10();
    var lastYL=-999;
    for(var yy=200;yy<=2000;yy+=100){var x2=tX(yy);if(x2>=0&&x2<=W&&x2-lastYL>30){ctx.fillText(yy,x2-12,H-8);lastYL=x2;}}
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
function selectPerson(id,isShift,ev){
  if(isShift&&selectedId&&id!==selectedId){selectedId2=id;}else{selectedId=id;selectedId2=null;}
  var p=nodeMap[id];if(p&&p.b){
    var rng=(p.d||p.b+50)-p.b;tl.minX=p.b-rng*0.3;tl.maxX=(p.d||p.b+50)+rng*0.7;
    tl.scale=(tl.W-40)/(tl.maxX-tl.minX);tl.ox=20;
  }
  drawTL(selectedId);if(selectedId2)drawTL2(selectedId2);
  showInfo(nodeMap[selectedId],selectedId2?nodeMap[selectedId2]:null,ev);
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
  var sb=document.getElementById("stats-bar");if(sb)sb.textContent=calcStats();
}
function clearSelection(){selectedId=null;selectedId2=null;drawTL(null);document.getElementById('info-popup').style.display='none';var sb=document.getElementById("stats-bar");if(sb)sb.textContent=calcStats();}
function drawTL2(id){}

// ═══ ANCIENT/MODERN MAP TOGGLE (with terrain) ═══
var ancientMode=false,dynastyLayers=[],ancientLabels=[],terrainLayer=null;
var LOC_ANCIENT={
  '大慈恩寺':'唐长安·大慈恩寺', '终南山':'唐终南山·至相寺', '清凉山（五台山）':'唐清凉山·大华严寺',
  '圭峰':'唐终南山·圭峰草堂', '方山':'唐方山·李通玄著论处', '杭州慧因寺':'宋杭州·慧因高丽寺',
  '洛阳佛授记寺':'唐东都·佛授记寺', '台北华严莲社':'今台北·华严莲社', '北京广济寺':'今北京·广济寺',
  '常熟兴福寺':'清常熟·兴福寺(华严大学)', '于阗':'唐于阗·瞿萨旦那国', '敦煌':'唐沙州·敦煌',
  '尼泊尔加德满都谷地':'尼波罗国·加德满都谷地', '匡山（庐山）':'唐匡山·庐山',
  '奈良东大寺':'日本平城京·东大寺', '南投大华严寺':'今南投·云鹤山大华严寺', '台北福慧寺':'今台北·树林福慧寺',
  '印度那烂陀寺':'古印度·那烂陀寺'
};
var DYNASTY_BOUNDARIES=[
  {n:'唐',s:618,e:907,c:'#b8863c',bounds:[[18,73],[42,130]]},
  {n:'宋',s:960,e:1279,c:'#5e8b9e',bounds:[[20,98],[40,125]]},
  {n:'明',s:1368,e:1644,c:'#c8893e',bounds:[[18,98],[43,125]]},
  {n:'清',s:1644,e:1912,c:'#8b7a9e',bounds:[[18,97],[44,132]]}
];
function toggleAncient(){
  ancientMode=!ancientMode;
  var cm=document.getElementById('tab-lineage');
  var btn=document.getElementById('ancient-btn');
  if(ancientMode){
    if(cm)cm.classList.add('map-ancient');
    if(btn){btn.style.background='#b8863c';btn.style.color='#fff';btn.style.borderColor='#b8863c';btn.textContent='🏯 今';}
    // Add terrain overlay (shows mountains/rivers/valleys clearly)
    if(!terrainLayer){terrainLayer=L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',{subdomains:['a','b','c'],maxZoom:17,opacity:0.55}).addTo(map);}
    else{terrainLayer.addTo(map);}
    // Major geographic feature labels
    var geoFeatures=[
      {n:'秦岭山脉',lat:34.0,lng:108.5},{n:'黄河',lat:34.8,lng:110.5},{n:'长江',lat:30.5,lng:114.0},
      {n:'五台山',lat:39.0,lng:113.6},{n:'东海',lat:28.0,lng:123.0},{n:'台湾海峡',lat:23.5,lng:119.5},
      {n:'长安盆地',lat:34.2,lng:108.9},{n:'太湖',lat:31.2,lng:120.2}
    ];
    geoFeatures.forEach(function(gf){
      var gl=L.marker([gf.lat,gf.lng],{icon:L.divIcon({html:'<div style=font-size:10px;color:#6b4e2a;font-weight:600;text-shadow:0 0 4px rgba(255,255,255,0.8)>'+gf.n+'</div>',className:'geo-feature-label',iconSize:[0,0]}),interactive:false,zIndexOffset:-5}).addTo(map);
      ancientLabels.push(gl);
    });
    // Show dynasty boundaries
    DYNASTY_BOUNDARIES.forEach(function(db){
      var r=L.rectangle(db.bounds,{color:db.c,weight:1.5,fillColor:db.c,fillOpacity:0.05,className:'dynasty-boundary'}).addTo(map);
      var cx=(db.bounds[0][1]+db.bounds[1][1])/2,cy=(db.bounds[0][0]+db.bounds[1][0])/2;
      var lbl=L.marker([cy,cx],{icon:L.divIcon({html:'<div style=font-size:11px;color:'+db.c+';font-weight:700;text-shadow:0 0 6px #fff>'+db.n+'</div>',className:'dynasty-label',iconSize:[0,0]}),interactive:false}).addTo(map);
      dynastyLayers.push(r);dynastyLayers.push(lbl);
    });
    // Update all location popups to show ancient names
    map.eachLayer(function(layer){
      if(!layer._ld)return;
      var ld=layer._ld,an=LOC_ANCIENT[ld.n]||ld.n;
      var names=(ld.ps||[]).map(function(pid){var n=nodeMap[pid];return n?n.n:'';}).filter(Boolean).join('、');
      layer.setPopupContent('<b>'+an+'</b><br><span style=font-size:0.75em;color:var(--text2)>今: '+ld.n+'</span><br>'+(ld.dy||'')+'<br>'+(ld.ds||'')+(names?'<br>👤 '+names:''));
      var off=ancientLabels.length%3;
      var loff=[0.003,0.008,0.014][off];
      var al=L.marker([ld.lat+loff,ld.lng],{icon:L.divIcon({html:'<div style=font-size:7px;color:#8b6b2a;font-weight:500;white-space:nowrap;text-shadow:0 0 3px rgba(255,248,235,0.8)>'+an+'</div>',className:'ancient-name-label',iconSize:[0,0]}),interactive:false,zIndexOffset:-10}).addTo(map);
      ancientLabels.push(al);
    });
  }else{
    if(cm)cm.classList.remove('map-ancient');
    if(btn){btn.style.background='';btn.style.color='';btn.style.borderColor='';btn.textContent='🏯 古今';}
    // Remove terrain
    if(terrainLayer){map.removeLayer(terrainLayer);}
    // Remove dynasty boundaries
    dynastyLayers.forEach(function(l){map.removeLayer(l);});
    dynastyLayers=[];
    // Remove ancient labels
    ancientLabels.forEach(function(l){map.removeLayer(l);});
    ancientLabels=[];
    // Restore popups with modern names
    map.eachLayer(function(layer){
      if(!layer._ld)return;
      var ld=layer._ld;
      var names=(ld.ps||[]).map(function(pid){var n=nodeMap[pid];return n?n.n:'';}).filter(Boolean).join('、');
      layer.setPopupContent('<b>'+ld.n+'</b><br>'+(ld.dy||'')+'<br>'+(ld.ds||'')+(names?'<br>👤 '+names:''));
    });
  }
}

// ═══ ENHANCED INFO PANEL ═══
function showInfo(p,p2,e){
  if(!p)return;
  var popup=document.getElementById('info-popup');
  var content=document.getElementById('info-popup-content');
  if(!popup||!content)return;
  var lc=DATA.lineage_colors[p.li]||"#b0a898";
  var locs=getPersonLocs(p.id),locHTML="";
  locs.forEach(function(l){var an=ancientMode?(LOC_ANCIENT[l.n]||l.n):l.n;locHTML+='📍 '+an+'<br>';});
  var teachers=DATA.edges.filter(function(e){return e.t===p.id&&e.r==="MASTER";}).map(function(e){return nodeMap[e.s];}).filter(Boolean);
  var students=DATA.edges.filter(function(e){return e.s===p.id&&e.r==="MASTER";}).map(function(e){return nodeMap[e.t];}).filter(Boolean);
  var allConns={};DATA.edges.forEach(function(e){if(e.s===p.id)allConns[e.t]=e.r;if(e.t===p.id)allConns[e.s]=e.r;});
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
    +((p.v||0)>0?'<span class=tag style=background:rgba(125,154,110,0.1);color:#7d9a6e>✓</span>':'<span class=tag style=background:rgba(200,160,80,0.1);color:#a08020>°</span>')
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
  content.innerHTML=h;
  popup.style.display='block';
  // Position near click or center-right
  if(e){
    var px=e.pageX+20,py=e.pageY-20;
    if(px+380>window.innerWidth)px=e.pageX-400;
    if(py+300>window.innerHeight)py=window.innerHeight-320;
    popup.style.left=px+'px';popup.style.top=py+'px';
  }else{
    popup.style.left=(window.innerWidth-400)+'px';popup.style.top='80px';
  }
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
      if(hoveredId!==pp.id){hoveredId=pp.id;drawTL(selectedId);}
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
  for(var i=0;i<tl.rowLabels.length;i++){
    var rl=tl.rowLabels[i];
    if(mx>=rl.x&&mx<=rl.x+rl.w&&my>=rl.y&&my<=rl.y+rl.h){zoomToLineage(rl.lineage);return;}
  }
  var hit=tl.hitRects.find(function(h){return mx>=h.x&&mx<=h.x+h.w&&my>=h.y&&my<=h.y+h.h;});
  if(hit){selectPerson(hit.person.id,e.shiftKey,e);}else{clearSelection();}
}

// ═══ ANIMATION (with map sync + speed control + route line) ═══
var animTimer=null,animYear=500,animPlaying=false;
var animRouteLine=null,animRouteMarker=null;
var ANIM_WAYPOINTS=[
  {y:420,lat:32.06,lng:118.79,z:6,label:'六十华严译出·建康'},
  {y:590,lat:33.93,lng:108.97,z:7,label:'杜顺·终南山·华严宗创立'},
  {y:699,lat:34.68,lng:112.44,z:7,label:'八十华严译出·洛阳'},
  {y:712,lat:34.26,lng:108.94,z:7,label:'法藏圆寂·长安'},
  {y:798,lat:34.26,lng:108.94,z:7,label:'四十华严译出·长安'},
  {y:839,lat:39.03,lng:113.56,z:7,label:'澄观圆寂·五台山'},
  {y:845,lat:34.26,lng:108.94,z:5,label:'唐武宗灭佛·法难'},
  {y:1085,lat:30.23,lng:120.13,z:7,label:'义天入宋求法·杭州慧因寺'},
  {y:1101,lat:37.57,lng:126.98,z:6,label:'义天圆寂·高丽开京'},
  {y:1641,lat:30.23,lng:120.13,z:6,label:'续法出生·杭州·清代华严复兴'},
  {y:1914,lat:31.65,lng:120.74,z:7,label:'华严大学创立·常熟兴福寺'},
  {y:1952,lat:25.03,lng:121.56,z:8,label:'华严莲社创社·台北'},
  {y:2008,lat:23.92,lng:120.88,z:9,label:'三脉汇流·南投大华严寺'},
  {y:2026,lat:24.53,lng:120.68,z:9,label:'支提山动土·九九华严·苗栗'}
];
var lastAnimLoc=-1;
function getAnimSpeed(){
  var s=document.getElementById('anim-speed');
  return s?parseInt(s.value):15;
}
function toggleAnim(){
  if(animPlaying){
    clearInterval(animTimer);animPlaying=false;
    document.getElementById("anim-btn").textContent="▶ 播放";lastAnimLoc=-1;
    // Clean up map route
    if(animRouteLine){if(map)map.removeLayer(animRouteLine);animRouteLine=null;}
    if(animRouteMarker){if(map)map.removeLayer(animRouteMarker);animRouteMarker=null;}
    return;
  }
  animPlaying=true;document.getElementById("anim-btn").textContent="⏸ 暂停";
  animYear=500;lastAnimLoc=-1;tl.minX=animYear-100;tl.maxX=animYear+300;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);
  if(map){
    map.setView([33,110],4);
    // Init route line
    var routeCoords=ANIM_WAYPOINTS.map(function(w){return [w.lat,w.lng];});
    if(animRouteLine)map.removeLayer(animRouteLine);
    animRouteLine=L.polyline(routeCoords,{color:'#c46b5d',weight:3,opacity:0.5,dashArray:'8,6'}).addTo(map);
    // Route marker (pulsing circle)
    if(animRouteMarker)map.removeLayer(animRouteMarker);
    animRouteMarker=L.circleMarker([33,110],{radius:0,fillColor:'#c46b5d',color:'#fff',weight:2,fillOpacity:0.9}).addTo(map);
  }
  var speedLabel=document.getElementById('speed-label');
  function animStep(){
    var sp=getAnimSpeed();
    if(speedLabel){var x=(15/sp).toFixed(1);speedLabel.textContent=(x===1.0?'1':x)+'×';}
    animYear+=sp;if(animYear>2030){animYear=500;clearInterval(animTimer);animPlaying=false;document.getElementById("anim-btn").textContent="▶ 播放";lastAnimLoc=-1;
      if(animRouteLine){map.removeLayer(animRouteLine);animRouteLine=null;}
      if(animRouteMarker){map.removeLayer(animRouteMarker);animRouteMarker=null;}
      if(speedLabel)speedLabel.textContent='1×';
    }
    tl.minX=animYear-100;tl.maxX=animYear+300;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);
    // Map sync + route progress
    if(map){
      // Update route marker position
      for(var i=0;i<ANIM_WAYPOINTS.length;i++){
        var wp=ANIM_WAYPOINTS[i];
        if(animYear>=wp.y&&lastAnimLoc<i){
          map.flyTo([wp.lat,wp.lng],wp.z,{duration:1.5});
          var popup=L.popup({closeButton:false,autoClose:false,className:'anim-popup'})
            .setLatLng([wp.lat,wp.lng])
            .setContent('<b>'+wp.y+'年</b><br>'+wp.label)
            .openOn(map);
          setTimeout(function(){if(popup&&map)map.closePopup(popup);},2500);
          lastAnimLoc=i;break;
        }
      }
      // Move route marker to interpolated position
      var prev=ANIM_WAYPOINTS[0];
      for(var j=1;j<ANIM_WAYPOINTS.length;j++){
        if(animYear<ANIM_WAYPOINTS[j].y){prev=ANIM_WAYPOINTS[j-1];break;}
        prev=ANIM_WAYPOINTS[j];
      }
      if(animRouteMarker){
        animRouteMarker.setLatLng([prev.lat,prev.lng]);
        animRouteMarker.setRadius(Math.max(6,(animYear%20)*0.3));
      }
    }
  }
  animTimer=setInterval(animStep,200);
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
