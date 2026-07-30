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
  // 古印度文明背景
  {y:-1500,l:'吠陀文明兴起·梨俱吠陀结集',c:'#b0a898',tp:'远源'},
  {y:-800,l:'奥义书时代·梵我哲学形成',c:'#b0a898',tp:'远源'},
  {y:-500,l:'沙门思潮·六师外道·思想百花齐放',c:'#b0a898',tp:'远源'},
  // 印度源流·法身本源
  {y:-483,l:'释迦入灭·佛教创立',c:'#9e8b6e',p:'释迦牟尼',tp:'宗教'},
  {y:80,l:'马鸣造大乘起信论',c:'#9e8b6e',p:'马鸣',tp:'义学'},
  // 汉译·文本传来
  {y:167,l:'支谶译兜沙经(最早华严)',c:'#a09080',p:'支娄迦谶',tp:'翻译'},
  {y:401,l:'鸠摩罗什至长安·译十住经',c:'#a09080',p:'鸠摩罗什',tp:'翻译'},
  {y:420,l:'六十华严译出(建康)',c:'#b8863c',p:'佛驮跋陀罗',tp:'翻译'},
  {y:508,l:'十地经论译出·地论学派兴起',c:'#5e8b9e',p:'菩提流支',tp:'义学'},
  {y:550,l:'地论师南北分派·相州南道/北道',c:'#5e8b9e',tp:'义学'},
  {y:557,l:'杜顺创华严宗·法界观门',c:'#b8863c',p:'杜顺',tp:'禅观'},
  {y:699,l:'八十华严译出·法藏证义',c:'#b8863c',p:'法藏',tp:'翻译'},
  {y:712,l:'法藏圆寂·贤首教学确立',c:'#b8863c',p:'法藏',tp:'义学'},
  {y:798,l:'四十华严译出(入法界品全)',c:'#b8863c',p:'般若',tp:'翻译'},
  {y:800,l:'胜友/智军藏译华严(于阗本)',c:'#c46b5d',tp:'翻译'},
  // 宗派互动·思想交锋
  {y:645,l:'玄奘归国·唯识宗兴起',c:'#8b7a9e',tp:'宗派'},
  {y:713,l:'慧能入灭·南宗禅兴起',c:'#8b7a9e',tp:'宗派'},
  {y:738,l:'澄观出生·历学八宗',c:'#b8863c',p:'澄观',tp:'义学'},
  {y:780,l:'宗密融合禅教·禅源诸诠',c:'#7d9a6e',p:'宗密',tp:'禅观'},
  {y:841,l:'宗密圆寂·华严宗盛极而衰',c:'#b8863c',p:'宗密',tp:'义学'},
  {y:845,l:'唐武宗灭佛·华严典籍大量焚毁',c:'#c46b5d',tp:'法难'},
  // 宋·海外传播
  {y:960,l:'宋统一·佛教义学复兴',c:'#c8893e',tp:'文化'},
  {y:973,l:'均如统一高丽华严南北宗',c:'#6d9a6e',p:'均如',tp:'义学'},
  {y:1011,l:'净源中兴·慧因寺华严道场',c:'#b8863c',p:'净源',tp:'义学'},
  {y:1038,l:'子璿兼弘贤首天台·起信论疏',c:'#c8893e',p:'子璿',tp:'宗派'},
  {y:1085,l:'义天入宋求法·华严东传高丽',c:'#6d9a6e',p:'义天',tp:'文化'},
  // 元明清
  {y:1271,l:'元朝建立·藏传佛教入汉·八思巴帝师',c:'#8b7a9e',tp:'文化'},
  {y:1600,l:'明末四大师·佛教复兴运动',c:'#c8893e',tp:'文化'},
  {y:1641,l:'续法著贤首五教仪·清代华严中兴',c:'#b8863c',p:'续法',tp:'义学'},
  // 近现代
  {y:1914,l:'华严大学创立(常熟)',c:'#5e8b9e',p:'月霞',tp:'教育'},
  {y:1952,l:'华严莲社创社(台北)',c:'#5e8b9e',p:'南亭',tp:'文化'},
  {y:1975,l:'华严专宗学院成立(台北)',c:'#5e8b9e',p:'成一',tp:'教育'},
  {y:2008,l:'钦因传衣钵·三脉汇流',c:'#c46b5d',p:'海云继梦',tp:'传承'},
  {y:2021,l:'84000英译入法界品出版',c:'#5e8b9e',tp:'翻译'},
  {y:2026,l:'九九华严·支提山动土·AI时代',c:'#6d9a6e',tp:'当代'}
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
      var isHL=p.id===hlId,matches=!isSearch||p.n.indexOf(searchQuery)>=0;
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
    // Re-init transmission story and schools
    initTransStory();initOtherSchools();
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
    // Remove transmission story + other schools
    transMarkers.forEach(function(m){map.removeLayer(m);});transMarkers=[];
    transLines.forEach(function(l){map.removeLayer(l);});transLines=[];
    otherSchoolsMarkers.forEach(function(m){map.removeLayer(m);});otherSchoolsMarkers=[];
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
  // Auto-hide timer: close after 5s unless mouse is over it
  if(popup._autoTimer)clearTimeout(popup._autoTimer);
  popup.onmouseenter=function(){if(popup._autoTimer)clearTimeout(popup._autoTimer);};
  popup.onmouseleave=function(){popup._autoTimer=setTimeout(function(){popup.style.display='none';},3000);};
  popup._autoTimer=setTimeout(function(){popup.style.display='none';},5000);
  // Position: mobile=centered, desktop=near click
  var isMobile=window.innerWidth<768;
  if(isMobile){
    popup.style.left='4vw';popup.style.top='10vh';popup.style.width='92vw';
  }else if(e){
    var px=e.pageX+20,py=e.pageY-20;
    if(px+380>window.innerWidth)px=e.pageX-400;
    if(py+300>window.innerHeight)py=window.innerHeight-320;
    popup.style.left=px+'px';popup.style.top=py+'px';popup.style.width='';
  }else{
    popup.style.left=(window.innerWidth-400)+'px';popup.style.top='80px';popup.style.width='';
  }
}

// ═══ LAYER TOGGLE ═══
function toggleLayer(layer){
  layerVis[layer]=!layerVis[layer];
  var btn=document.querySelector('#controls button[data-layer="'+layer+'"]');
  if(btn){if(layerVis[layer]){btn.classList.add('active');}else{btn.classList.remove('active');}}
  drawTL(selectedId);
}

// ═══ TRANSMISSION STORY (人物+事件串讲·取代粗糙线段) ═══
var TRANS_STORY=[
  {y:-483,p:'释迦牟尼',lat:24.7,lng:84.99,ev:'释迦入灭于菩提伽耶。据华严宗传统,《华严经》为成道后最初三七日于菩提树下为法身大士所说。',src:'佛教通说'},
  {y:-260,p:'阿育王',lat:25.3,lng:83.0,ev:'阿育王皈依佛教,派传教师向四方传播佛法。第三次结集后佛教开始向中亚、东南亚扩散。',src:'阿育王石刻诏书'},
  {y:65,p:'迦腻色迦王',lat:33.7,lng:72.8,ev:'贵霜帝国迦腻色迦王于犍陀罗举行第四次结集。佛法由印度深入中亚,犍陀罗成为佛教东传的枢纽站。',src:'佛教史·贵霜时期'},
  {y:80,p:'马鸣',lat:27.5,lng:77.7,ev:'马鸣菩萨造《大乘起信论》。该论「一心二门」之说后成为华严宗心性论与判教体系的重要理论基础。',src:'传统著录'},
  {y:167,p:'支娄迦谶',lat:34.7,lng:112.4,ev:'月氏僧支谶来华至洛阳,译《佛说兜沙经》。此为华严经文最早汉译,仅1卷,对应《如来名号品》。',src:'《高僧传》卷一'},
  {y:320,p:'无著·世亲',lat:25.1,lng:85.4,ev:'无著、世亲兄弟于那烂陀弘传瑜伽行派。世亲造《十地经论》,后经菩提流支汉译催生地论学派。',src:'《大唐西域记》卷九'},
  {y:344,p:'鸠摩罗什',lat:41.7,lng:82.9,ev:'罗什生于龟兹。401年至长安,主持史上最大译场。译《十住经》(十地品别译)、《十住毗婆沙论》等,为华严学提供关键文本基础。',src:'《高僧传》卷二'},
  {y:359,p:'佛驮跋陀罗',lat:34.0,lng:72.0,ev:'觉贤生于北天竺迦毗罗卫。后至建康译出《六十华严》34品。此为《华严经》首次汉译全本。',src:'《高僧传》卷二'},
  {y:401,p:'鸠摩罗什',lat:34.3,lng:108.9,ev:'罗什至长安逍遥园。主持中国史上最大译场,八百沙门参与。译出《十住经》《中论》《法华经》等,深刻影响华严义学。',src:'《出三藏记集》卷十四'},
  {y:420,p:'佛驮跋陀罗',lat:32.1,lng:118.8,ev:'六十华严译出于建康道场寺。七处八会三十四品。法业等百余人参与笔受。华严经首次以全貌呈现于汉地。',src:'《出三藏记集》卷九'},
  {y:468,p:'慧光',lat:34.7,lng:112.4,ev:'慧光生于北魏。从勒那摩提学《十地经论》,开地论南道派。后被尊为四分律宗初祖。其学经数代传至智俨、法藏,是为华严宗义学之前身。',src:'《续高僧传》卷二十一'},
  {y:508,p:'菩提流支',lat:34.7,lng:112.4,ev:'北印度僧菩提流支至洛阳,与勒那摩提译世亲《十地经论》十二卷。此论催生了南北朝最重要的义学流派——地论学派。',src:'《续高僧传》卷一'},
  {y:557,p:'杜顺',lat:33.9,lng:109.0,ev:'杜顺于终南山开创华严宗。著《华严法界观门》《五教止观》。以「法界三观」和「五教止观」为华严宗奠定修行理论基础。',src:'《续高僧传》卷二十五'},
  {y:643,p:'法藏',lat:34.3,lng:108.9,ev:'法藏生于长安。从智俨学华严。后系统化「五教十宗」判教,著《华严五教章》等。武则天赐号「贤首」。参与八十华严译场证义。华严宗至此正式确立。',src:'《宋高僧传》卷五'},
  {y:652,p:'实叉难陀',lat:37.1,lng:79.9,ev:'实叉难陀生于于阗。后奉武则天诏来华译经。于阗在中亚佛教网络中地位关键——既是实叉难陀故乡,又是藏译华严底本来源。',src:'《宋高僧传》卷二'},
  {y:699,p:'实叉难陀·法藏',lat:34.7,lng:112.4,ev:'八十华严译出于洛阳佛授记寺。法藏参与证义。七处九会三十九品,为后世流传最广的汉译本。',src:'《宋高僧传》卷二'},
  {y:780,p:'宗密',lat:34.0,lng:108.7,ev:'宗密住终南山圭峰。融合禅宗(荷泽系)与华严,著《禅源诸诠集都序》。华严与禅宗的深度融合,奠定了「教禅一致」的思想基础。',src:'《宋高僧传》卷六'},
  {y:800,p:'胜友·智军',lat:29.7,lng:91.1,ev:'胜友、智军等于吐蕃将《华严经》由于阗本译为藏文(Toh44)。华严传入西藏,形成独立于汉译的藏传华严传承。',src:'德格版甘珠尔目录'},
  {y:1085,p:'义天',lat:30.2,lng:120.1,ev:'高丽王子义天入宋,于杭州慧因寺从净源受华严。华严经由杭州传入朝鲜半岛。义天归国后编《义天录》,为华严文献学奠基。',src:'《高丽史》卷九十'},
  {y:1173,p:'明惠',lat:35.0,lng:135.8,ev:'日本华严中兴之祖明惠于京都高山寺复兴华严。兼弘戒律与真言。日本华严经历镰仓时代再兴,形成东亚华严网络最终一环。',src:'日本佛教史'}
];

var transMarkers=[],transLines=[],otherSchoolsMarkers=[];

function initTransStory(){
  if(!map)return;
  transMarkers.forEach(function(m){map.removeLayer(m);});
  transLines.forEach(function(l){map.removeLayer(l);});
  transMarkers=[];transLines=[];
  // Draw connecting lines between consecutive story points
  for(var i=1;i<TRANS_STORY.length;i++){
    var prev=TRANS_STORY[i-1],cur=TRANS_STORY[i];
    var l=L.polyline([[prev.lat,prev.lng],[cur.lat,cur.lng]],{color:'#b8863c',weight:1.5,opacity:0.35,dashArray:'5,8'}).addTo(map);
    transLines.push(l);
  }
  // Draw story markers (small numbered circles)
  TRANS_STORY.forEach(function(ts,i){
    var sz=ts.p==='杜顺'||ts.p==='法藏'||ts.p.indexOf('华严')>=0?20:14;
    var icon=L.divIcon({html:'<div style=background:#b8863c;color:#fff;border-radius:50%;width:'+sz+'px;height:'+sz+'px;text-align:center;line-height:'+sz+'px;font-size:'+(sz>14?'9':'7')+'px;font-weight:700;border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,0.2)>'+(i+1)+'</div>',iconSize:[sz,sz],iconAnchor:[sz/2,sz/2]});
    var m=L.marker([ts.lat,ts.lng],{icon:icon}).addTo(map);
    m.bindPopup('<b>['+(i+1)+'] '+ts.y+'年</b> · '+ts.p+'<br>'+ts.ev+'<br><span style=font-size:0.68em;color:var(--text2)>源: '+ts.src+'</span>');
    transMarkers.push(m);
  });
}

var OTHER_SCHOOLS=[
  {n:'天台宗',y:597,lat:29.2,lng:121.0,c:'#7d9a6e',founder:'智𫖮',loc:'天台山',
   desc:'中国最早成立的佛教宗派。以《法华经》为根本经典。华严宗判教体系中「同教一乘」即针对天台而设。澄观曾参学天台。',src:'《续高僧传》卷十七·智𫖮传 /《宋高僧传》卷五·澄观传'},
  {n:'三论宗',y:597,lat:34.3,lng:108.9,c:'#a09080',founder:'吉藏',loc:'长安',
   desc:'以《中论》《百论》《十二门论》立宗。华严宗继承三论空性论证方法，法藏判教将三论归入大乘始教。',src:'《续高僧传》卷十一·吉藏传'},
  {n:'唯识宗',y:645,lat:34.3,lng:108.9,c:'#8b7a9e',founder:'玄奘',loc:'长安',
   desc:'以《成唯识论》立宗。与华严宗同源瑜伽行派但取径不同。玄奘译《显无边佛土功德经》(T0289)即华严寿量品别译。',src:'《大唐大慈恩寺三藏法师传》'},
  {n:'净土宗',y:402,lat:29.6,lng:116.0,c:'#b8863c',founder:'慧远',loc:'庐山',
   desc:'以念佛往生为宗旨。华严经普贤行愿品为净土行者重视，华严「华藏世界」与净土「极乐世界」之间有深层义学互动。',src:'《高僧传》卷六·慧远传'},
  {n:'禅宗',y:520,lat:34.5,lng:112.5,c:'#d48476',founder:'达摩→慧能',loc:'少林寺→曹溪',
   desc:'以教外别传为宗。华严五祖宗密同时是禅宗荷泽系传人，著《禅源诸诠集都序》系统融合禅教。澄观亦参谒禅门牛头宗。',src:'《宋高僧传》卷六·宗密传 / 宗密《禅源诸诠集都序》'},
  {n:'律宗',y:626,lat:33.9,lng:109.0,c:'#9e8b6e',founder:'道宣',loc:'终南山',
   desc:'以四分律为根本。与华严宗同以终南山为根本道场。慧光(地论师·华严义学前身)同时被尊为四分律宗初祖。',src:'《宋高僧传》卷十四·道宣传 / 《续高僧传》卷二十一·慧光传'},
  {n:'密宗',y:716,lat:34.3,lng:108.9,c:'#c8893e',founder:'善无畏·金刚智·不空',loc:'长安',
   desc:'唐代开元三大士传入。华严宗内贤首密法(秽迹金刚)自成体系。海云继梦所得印度瑜伽行传承亦与此有历史关联。',src:'《宋高僧传》卷二·善无畏传 / 大华严寺官方资料'}
];
function initOtherSchools(){
  if(!map)return;
  otherSchoolsMarkers.forEach(function(m){map.removeLayer(m);});
  otherSchoolsMarkers=[];
  OTHER_SCHOOLS.forEach(function(s){
    var icon=L.divIcon({html:'<div style=background:'+s.c+';color:#fff;border-radius:50%;width:22px;height:22px;text-align:center;line-height:22px;font-size:10px;font-weight:700;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.2)>'+s.n[0]+'</div>',iconSize:[22,22],iconAnchor:[11,11]});
    var m=L.marker([s.lat,s.lng],{icon:icon}).addTo(map);
    m.bindPopup('<b>'+s.n+'</b> ('+s.y+'年·'+s.loc+')<br>创始人: '+s.founder+'<br><span style=font-size:0.8em>'+s.desc+'</span>');
    m._school=s;
    otherSchoolsMarkers.push(m);
  });
}

// ═══ ROUTE INFO ═══
function toggleRouteInfo(){
  var ri=document.getElementById('route-info');
  if(!ri)return;
  if(ri.style.display==='none'){ri.style.display='block';ri._autoTimer=setTimeout(function(){ri.style.display='none';},8000);}
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
var animTimer=null,animYear=-600,animPlaying=false;
var animRouteLine=null,animRouteMarker=null;
var ANIM_WAYPOINTS=[
  // 印度起源
  {y:-483,lat:24.7,lng:84.99,z:5,label:'释迦入灭·菩提伽耶',info:'佛陀成道处。华严宗传统认为《华严经》为释迦成道后最初三七日于菩提树下为法身大士所说。'},
  {y:80,lat:27.5,lng:77.7,z:5,label:'马鸣造起信论·中印度',info:'马鸣菩萨约公元1-2世纪生于中印度。所造《大乘起信论》「一心二门」之说为华严宗心性论提供了重要理论基础。'},
  {y:320,lat:25.14,lng:85.44,z:6,label:'那烂陀寺兴盛·瑜伽行派',info:'古印度佛教最高学府。无著、世亲在此弘传瑜伽行派。世亲《十地经论》后经菩提流支汉译，成为华严宗义学之源。'},
  // 中亚·西域传播走廊
  {y:344,lat:41.7,lng:82.9,z:5,label:'鸠摩罗什出生·龟兹国',info:'龟兹(今新疆库车)。罗什后至长安译《十住经》《十住毗婆沙论》等，为华严学在中国的传播提供了关键文本基础。'},
  {y:359,lat:34.0,lng:72.0,z:5,label:'佛驮跋陀罗出生·北天竺',info:'北天竺迦毗罗卫(今尼泊尔/印度边境)。后至建康译出《六十华严》，为华严经汉译之始。'},
  {y:401,lat:34.26,lng:108.94,z:6,label:'鸠摩罗什至长安·译经运动',info:'后秦弘始三年(401)至长安，主持中国史上最大译场。所译中观论典深刻影响华严宗的空性论证与判教框架。'},
  // 汉地翻译·教义建立
  {y:420,lat:32.06,lng:118.79,z:6,label:'六十华严译出·建康',info:'佛驮跋陀罗于建康(今南京)道场寺译出《六十华严》，共七处八会三十四品。此为《华严经》首次汉译全本。'},
  {y:508,lat:34.68,lng:112.44,z:6,label:'十地经论译出·洛阳',info:'菩提流支与勒那摩提于洛阳译出世亲《十地经论》。此论催生了南北朝地论学派，是为华严宗义学之远源。'},
  {y:590,lat:33.93,lng:108.97,z:7,label:'杜顺·终南山·华严宗创立',info:'杜顺(557-640)于终南山至相寺开创华严宗观法体系。著《法界观门》《五教止观》，奠定华严宗修行理论基础。'},
  {y:652,lat:37.11,lng:79.91,z:5,label:'实叉难陀出生·于阗国',info:'于阗(今新疆和田)为中亚佛教枢纽。实叉难陀后来华译八十华严。藏文Toh44亦译自于阗原本，足见于阗在华严传播中的枢纽地位。'},
  {y:699,lat:34.68,lng:112.44,z:7,label:'八十华严译出·洛阳',info:'实叉难陀于洛阳佛授记寺译八十卷《华严经》。法藏参与译场证义。八十华严为后世流传最广的汉译本。'},
  {y:712,lat:34.26,lng:108.94,z:7,label:'法藏圆寂·长安',info:'华严三祖法藏(643-712)于长安圆寂。系统化「五教十宗」判教体系，为华严宗实际创立者。讲说《华严经》三十余遍。'},
  {y:798,lat:34.26,lng:108.94,z:7,label:'四十华严译出·长安',info:'般若三藏译出《四十华严》，即全本《入法界品》。善财童子五十三参的完整故事得以汉译。文末《普贤行愿赞》为汉藏共同尊奉。'},
  {y:800,lat:29.65,lng:91.1,z:5,label:'藏译华严完成·吐蕃',info:'胜友、智军等于吐蕃将《华严经》从于阗本译为藏文(Toh44·45品)。此为华严传播史上的重要分支——经中亚于阗传入西藏。'},
  {y:839,lat:39.03,lng:113.56,z:7,label:'澄观圆寂·五台山',info:'华严四祖澄观(738-839)于五台山圆寂。著《华严经疏》六十卷、《演义钞》九十卷，为华严教学集大成者。历七帝之师。'},
  {y:845,lat:34.26,lng:108.94,z:5,label:'唐武宗灭佛·法难',info:'会昌法难。华严典籍大量焚毁，义学传承几近断绝。此后华严转入隐传阶段，直至宋代净源、子璿等复兴。'},
  // 东亚传播
  {y:1085,lat:30.23,lng:120.13,z:7,label:'义天入宋求法·杭州慧因寺',info:'高丽王子义天入宋，于杭州慧因寺从净源受华严教法。归国后编《义天录》，为华严东传朝鲜半岛的关键人物。'},
  {y:1101,lat:37.57,lng:126.98,z:6,label:'义天圆寂·高丽开京',info:'义天圆寂于高丽开京(今开城)。其后均如、体元等高丽学僧继续弘扬华严，使朝鲜半岛成为东亚华严学重镇。'},
  {y:1173,lat:35.01,lng:135.77,z:6,label:'明惠中兴·日本高山寺',info:'日本华严宗中兴之祖明惠(1173-1232)于京都高山寺复兴华严教学，兼弘戒律与真言。日本华严宗经历镰仓时代之再兴。'},
  // 近现代复兴
  {y:1641,lat:30.23,lng:120.13,z:6,label:'续法·清代华严集大成',info:'续法(1641-1728)于杭州著《贤首五教仪》，系统整理华严判教。讲《华严经》二十余遍，为清代华严学之集大成。'},
  {y:1914,lat:31.65,lng:120.74,z:7,label:'华严大学创立·常熟兴福寺',info:'月霞长老于常熟兴福寺创立华严大学，为中国近代第一所华严专宗教育机构。培养常惺、持松等一批现代华严学僧。'},
  {y:1952,lat:25.03,lng:121.56,z:8,label:'华严莲社创社·台北',info:'智光、南亭于台北创立华严莲社，开启台湾华严宗弘传事业。成一、贤度等相继住持，发展为现代华严学术与教育中心。'},
  {y:1975,lat:25.04,lng:121.51,z:8,label:'华严专宗学院·台北',info:'成一法师创办华严专宗学院，以「专修、专研、专弘华严」为宗旨，为当代最重要的华严教育机构之一。'},
  {y:2008,lat:23.92,lng:120.88,z:9,label:'三脉汇流·南投大华严寺',info:'海云继梦受钦因传华严衣钵(贤首42世)，同年得印度胜师子王菩萨传瑜伽行法。华严·临济·瑜伽行三脉汇一，开创「普贤乘华严宗」。'},
  {y:2021,lat:27.7,lng:85.32,z:5,label:'84000英译·华严回归国际',info:'84000项目发布Peter Alan Roberts英译《入法界品》(Toh44-45)。藏文华严首次系统英译，华严学研究进入多语对读新时代。'},
  {y:2026,lat:24.53,lng:120.68,z:9,label:'九九华严·支提山动土·苗栗',info:'海云继梦于台北TICC启动五年讲座「九九华严」。支提山大华严寺动土，面向台湾海峡与福建支提华严祖庭隔海相望。'}
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
  animYear=-600;lastAnimLoc=-1;tl.minX=animYear-100;tl.maxX=animYear+300;tl.ox=20;tl.scale=(tl.W-40)/(tl.maxX-tl.minX);drawTL(null);
  if(map){
    map.setView([28,78],3);
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
    animYear+=sp;if(animYear>2030){animYear=-600;clearInterval(animTimer);animPlaying=false;document.getElementById("anim-btn").textContent="▶ 播放";lastAnimLoc=-1;
      if(animRouteLine){map.removeLayer(animRouteLine);animRouteLine=null;}
      if(animRouteMarker){map.removeLayer(animRouteMarker);animRouteMarker=null;}
      if(speedLabel)speedLabel.textContent='1×';
      // Clean up route highlights
      transLines.forEach(function(l){l.setStyle({opacity:0.35,weight:1.5});});
    }
    // Highlight active routes based on current year
    if(animYear>-400&&animYear<900&&transLines.length){
      transLines.forEach(function(l){l.setStyle({opacity:Math.min(0.7,0.2+animYear/1500),weight:Math.min(3,1.5+animYear/800)});});
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
