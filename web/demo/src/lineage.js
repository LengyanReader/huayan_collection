// ═══ DATA LAYERS ═══
var layerVis={theory:true,geo:true,practice:true,edges:true,events:true};
// Multi-layer religion colors for animation routes & popups
var REL_COLORS={buddhist:'#c46b5d',confucian:'#b8863c',daoist:'#7d9a6e',western:'#5e8b9e',islamic:'#8b7a9e'};
var REL_LABELS={buddhist:'佛教/华严主线',confucian:'儒家',daoist:'道家',western:'西方哲学',islamic:'其他传统'};
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
var mapMain=null,_miniMaps={};
var mainMarkers=[];
function tileLayer(){return L.tileLayer("https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",{subdomains:["1","2","3","4"],maxZoom:18});}
function terrainTileLayer(){return L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",{subdomains:["a","b","c"],maxZoom:17,opacity:0.7});}

function initMap(){
  if(typeof L==="undefined"){
    var d1=document.getElementById("map-main");if(d1)d1.innerHTML="<div style=display:flex;align-items:center;justify-content:center;height:100%;color:var(--text2);font-size:0.7em>🗺 地图未加载</div>";
    return;
  }
  // ── Main map: China/East Asia detail ──
  if(!mapMain){
    mapMain=L.map("map-main",{zoomControl:true,zoomControlPosition:'bottomleft'}).setView([34,108],5);
    tileLayer().addTo(mapMain);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{subdomains:["a","b","c"],maxZoom:19,opacity:0.4}).addTo(mapMain);
    // Huayan locations
    var mc={temple:"#b8863c",mountain:"#7d9a6e",region:"#c46b5d"};
    DATA.locations.forEach(function(loc){
      var names=(loc.ps||[]).map(function(pid){var n=nodeMap[pid];return n?n.n:"";}).filter(Boolean).join("、");
      var m=L.circleMarker([loc.lat,loc.lng],{radius:8,fillColor:mc[loc.tp]||"#b0a898",color:"#fff",weight:2,fillOpacity:0.9});
      m.addTo(mapMain).bindPopup("<b>"+loc.n+"</b><br>"+(loc.dy||"")+"<br>"+(loc.ds||"")+(names?"<br>👤 "+names:""));
      m._ld=loc;m.on("click",function(){if(loc.ps&&loc.ps.length>0)selectPerson(loc.ps[0]);});
      mainMarkers.push(m);
    });
  } else {
    mapMain.invalidateSize();
  }
  initMiniMaps();
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
  // Clear previous footprints + trajectory markers
  if(window._personFootprints){window._personFootprints.forEach(function(l){if(mapMain)mapMain.removeLayer(l);});}
  if(window._trajMarkers){window._trajMarkers.forEach(function(l){if(mapMain)mapMain.removeLayer(l);});}
  window._personFootprints=[];window._trajMarkers=[];
  if(_trajLine&&mapMain){mapMain.removeLayer(_trajLine);_trajLine=null;}
  if(_trajMarker&&mapMain){mapMain.removeLayer(_trajMarker);_trajMarker=null;}
  if(_trajHighlight&&mapMain){mapMain.removeLayer(_trajHighlight);_trajHighlight=null;}
  if(_trajPopup&&mapMain){mapMain.closePopup(_trajPopup);_trajPopup=null;}
  if(_trajTimer){clearTimeout(_trajTimer);_trajTimer=null;}
  // Close all Leaflet popups on map
  if(mapMain)mapMain.closePopup();
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
var ancientMode=false,dynastyLayers=[],ancientLabels=[],terrainLayer=null;

// ── Ancient/Modern Map Toggle ──
var LOC_ANCIENT={
  '大慈恩寺':'唐长安·大慈恩寺', '终南山':'唐终南山·至相寺', '清凉山（五台山）':'唐清凉山·大华严寺',
  '圭峰':'唐终南山·圭峰草堂', '方山':'唐方山·李通玄著论处', '杭州慧因寺':'宋杭州·慧因高丽寺',
  '洛阳佛授记寺':'唐东都·佛授记寺', '台北华严莲社':'今台北·华严莲社', '北京广济寺':'今北京·广济寺',
  '常熟兴福寺':'清常熟·兴福寺(华严大学)', '于阗':'唐于阗·瞿萨旦那国', '敦煌':'唐沙州·敦煌',
  '尼泊尔加德满都谷地':'尼波罗国·加德满都谷地', '匡山（庐山）':'唐匡山·庐山',
  '奈良东大寺':'日本平城京·东大寺', '南投大华严寺':'今南投·云鹤山大华严寺', '台北福慧寺':'今台北·树林福慧寺',
  '印度那烂陀寺':'古印度·那烂陀寺'
};

// ═══ PERSON TRAJECTORIES (global injected from YAML, fallback if missing) ═══
if (typeof PERSON_TRAJECTORIES === 'undefined') { console.warn("PERSON_TRAJECTORIES not loaded from YAML"); var PERSON_TRAJECTORIES = {}; }
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
    // Add terrain overlay to main map
    if(!terrainLayer){terrainLayer=terrainTileLayer();terrainLayer.addTo(mapMain);}else{terrainLayer.addTo(mapMain);}
    // Major geographic feature labels
    var geoFeatures=[
      {n:'秦岭山脉',lat:34.0,lng:108.5},{n:'黄河',lat:34.8,lng:110.5},{n:'长江',lat:30.5,lng:114.0},
      {n:'五台山',lat:39.0,lng:113.6},{n:'东海',lat:28.0,lng:123.0},{n:'台湾海峡',lat:23.5,lng:119.5},
      {n:'长安盆地',lat:34.2,lng:108.9},{n:'太湖',lat:31.2,lng:120.2}
    ];
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
  }else{
    if(cm)cm.classList.remove('map-ancient');
    if(btn){btn.style.background='';btn.style.color='';btn.style.borderColor='';btn.textContent='🏯 古今';}
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
  var gen=0,tmp=p;
  var teachers=DATA.edges.filter(function(e){return e.t===p.id&&(e.r==='MASTER'||e.r==='MASTER_OF');}).map(function(e){return nodeMap[e.s];}).filter(Boolean);
  while(tmp){var next=teachers.find(function(t){return t.id!==tmp.id;});if(!next)break;tmp=next;gen++;}
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
    +"<span class=tag style=background:"+lc+"20;color:"+lc+">"+(p.li||"—")+"</span>"
    +"<span class=tag style=background:rgba(0,0,0,0.04)>"+(p.tp==="patriarch"?"祖师":p.tp==="translator"?"译师":p.tp==="scholar"?"学者":"行者")+"</span>"
    +((p.v||0)>0?'<span class=tag style=background:rgba(125,154,110,0.1);color:#7d9a6e>✓</span>':'<span class=tag style=background:rgba(200,160,80,0.1);color:#a08020>°</span>')
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
  if(srcNote)h+='<div style="margin-top:3px;font-size:0.65em;color:var(--text2);opacity:0.7">📚 '+srcNote+'</div>';
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
  popup.onclick=function(e){if(e.target.tagName==='BUTTON'||e.target.tagName==='A')return;popup.style.display='none';};
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
  // Stop any existing playback
  if(_trajTimer){clearTimeout(_trajTimer);_trajTimer=null;}
  if(_trajMarker&&mapMain){mapMain.removeLayer(_trajMarker);_trajMarker=null;}
  if(_trajLine&&mapMain){mapMain.removeLayer(_trajLine);_trajLine=null;}
  if(_trajHighlight&&mapMain){mapMain.removeLayer(_trajHighlight);_trajHighlight=null;}
  if(_trajPopup&&mapMain){mapMain.closePopup(_trajPopup);_trajPopup=null;}
  _trajIndex=0;
  var route=traj.route,color=traj.color||'#c46b5d',name=traj.name||'';
  // Draw base route line
  var coords=route.map(function(p){return [p.lat,p.lng];});
  if(mapMain){
    _trajLine=L.polyline(coords,{color:color,weight:2,opacity:0.35,dashArray:'6,4'}).addTo(mapMain);
    mapMain.fitBounds(_trajLine.getBounds().pad(0.15));
    // Start marker
    L.circleMarker([route[0].lat,route[0].lng],{radius:7,fillColor:'#7d9a6e',color:'#fff',weight:2,fillOpacity:0.9})
      .bindTooltip('▶ '+route[0].label+' ('+route[0].y+')',{permanent:true,direction:'right'}).addTo(mapMain);
    // End marker
    var last=route[route.length-1];
    L.circleMarker([last.lat,last.lng],{radius:7,fillColor:'#c46b5d',color:'#fff',weight:2,fillOpacity:0.9})
      .bindTooltip('⏹ '+last.label+' ('+last.y+')',{permanent:true,direction:'right'}).addTo(mapMain);
    // Moving marker
    _trajMarker=L.circleMarker([route[0].lat,route[0].lng],{radius:10,fillColor:color,color:'#ffe066',weight:3,fillOpacity:0.95}).addTo(mapMain);
  }
  document.getElementById('info-popup').style.display='none';
  var sb=document.getElementById('anim-status');if(sb)sb.style.opacity='1';
  // Show nav popup on map
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
    +'<br><span style=font-size:0.65em;color:var(--text2)>点击地图暂停/继续</span>'
    +'</div>';
  if(_trajPopup&&mapMain)mapMain.closePopup(_trajPopup);
  _trajPopup=L.popup({closeButton:false,autoClose:false,className:'anim-popup',maxWidth:280,autoPan:false,offset:[0,-15]})
    .setLatLng([pt.lat,pt.lng]).setContent(html).openOn(mapMain);
  // Click map to pause/resume
  mapMain.off('click');mapMain.on('click',function(){
    if(_trajTimer){clearTimeout(_trajTimer);_trajTimer=null;if(sb)document.getElementById('anim-status').style.opacity='0';}
    else{_trajTimer=setTimeout(function(){_stepTrajectory(route,color,document.getElementById('anim-status'),name);},1200);}
  });
}
function _stepTrajectory(route,color,sb,name){
  if(_trajIndex>=route.length){
    if(sb)sb.style.opacity='0';
    if(_trajPopup&&mapMain)mapMain.closePopup(_trajPopup);
    // Flash end marker
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
  if(_trajHighlight&&mapMain)mapMain.removeLayer(_trajHighlight);
  if(prev&&mapMain){
    _trajHighlight=L.polyline([[prev.lat,prev.lng],[pt.lat,pt.lng]],{color:color,weight:5,opacity:0.8}).addTo(mapMain);
  }
  // Update nav popup
  _showTrajNav(route,color,name,_trajIndex);
  _trajIndex++;
  _trajTimer=setTimeout(function(){_stepTrajectory(route,color,sb,name);},1200);
}
function showTrajectoryOnMap(pid){
  var traj=PERSON_TRAJECTORIES[pid];if(!traj||!traj.route)return;
  // Clear previous
  if(_trajLine&&mapMain)mapMain.removeLayer(_trajLine);
  if(_trajMarker&&mapMain)mapMain.removeLayer(_trajMarker);
  // Also clear any numbered markers from previous show
  if(window._trajMarkers){window._trajMarkers.forEach(function(m){if(mapMain)mapMain.removeLayer(m);});}
  window._trajMarkers=[];
  var coords=traj.route.map(function(p){return [p.lat,p.lng];});
  var color=traj.color||'#c46b5d';
  if(mapMain){
    // Thick semi-transparent glow + thin solid core
    _trajLine=L.polyline(coords,{color:color,weight:5,opacity:0.25}).addTo(mapMain);
    window._trajMarkers.push(_trajLine);
    var core=L.polyline(coords,{color:color,weight:2.5,opacity:0.85,dashArray:'8,3'}).addTo(mapMain);
    window._trajMarkers.push(core);
    // Start marker (green dot)
    var start=traj.route[0];
    var startM=L.circleMarker([start.lat,start.lng],{radius:8,fillColor:'#7d9a6e',color:'#fff',weight:2.5,fillOpacity:1})
      .bindTooltip('▶ '+start.label+' ('+start.y+')',{permanent:true,direction:'right'}).addTo(mapMain);
    window._trajMarkers.push(startM);
    // End marker (red dot)
    var end=traj.route[traj.route.length-1];
    var endM=L.circleMarker([end.lat,end.lng],{radius:8,fillColor:'#c46b5d',color:'#fff',weight:2.5,fillOpacity:1})
      .bindTooltip('⏹ '+end.label+' ('+end.y+')',{permanent:true,direction:'right'}).addTo(mapMain);
    window._trajMarkers.push(endM);
    // Numbered intermediate markers
    for(var i=1;i<traj.route.length-1;i++){
      var pt=traj.route[i];
      var m=L.circleMarker([pt.lat,pt.lng],{radius:5,fillColor:color,color:'#fff',weight:1.5,fillOpacity:0.85})
        .bindTooltip((i+1)+'. '+pt.label+' ('+pt.y+')').addTo(mapMain);
      window._trajMarkers.push(m);
    }
    // Zoom to fit with generous padding
    var bounds=L.latLngBounds(coords);
    mapMain.fitBounds(bounds,{padding:[50,50],maxZoom:8});
  }
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
  // 汉传高僧·古代
  if(/安世高|道安|僧肇|道生|僧祐|永明|大慧|憨山|蕅益|雪窦|佛驮跋陀罗|实叉难陀|支娄迦谶|般若/.test(full))return '☸ 汉传高僧';
  // 近现代高僧大德
  if(/虚云|太虚|印光|弘一|印顺|梦参|圆瑛|谛闲|倓虚/.test(full))return '🏛 近现代高僧大德';
  // 译师(从名相推断)
  if(/译|胜友|智军/.test(full))return '📖 译师';
  // 求法僧
  if(/法显|义净|玄奘|西行|求法/.test(full))return '🚶 求法僧';
  // 天台宗
  if(/天台|智顗|湛然|知礼/.test(full))return '☸ 天台宗';
  // 禅宗各派
  if(/禅|慧能|弘忍|神秀|达摩|马祖|临济|曹洞|云门|法眼|沩仰|黄檗|石头|赵州|百丈|雪峰|洞山/.test(full))return '☸ 禅宗';
  // 净土宗
  if(/净土|善导|慧远|莲池|昙鸾|道绰|省庵/.test(full))return '☸ 净土宗';
  // 法相唯识
  if(/法相|唯识|窥基|圆测|世亲/.test(full))return '☸ 法相宗·唯识';
  // 三论宗
  if(/三论|吉藏|僧肇/.test(full))return '☸ 三论宗';
  // 律宗
  if(/律宗|道宣|鉴真|弘一|元照|僧祐/.test(full))return '☸ 律宗';
  // 密宗
  if(/密宗|善无畏|金刚智|不空|一行|慧果/.test(full))return '☸ 密宗·唐密';
  // 藏传
  if(/宗喀巴|达赖|班禅|阿底峡|莲花生|米拉日巴|八思巴|寂天/.test(full))return '🔴 藏传佛教';
  // 印度佛教/瑜伽
  if(/印度|瑜伽|拉克鲁希|巴布基|普拉梵|克利普|胜师子|马鸣|龙树|无著/.test(full))return '🕉 印度佛教';
  // 日本佛教
  if(/空海|最澄|道元|荣西|日莲|亲鸾|法然|良弁|明惠|凝然/.test(full))return '☸ 日本佛教';
  // 印度教
  if(/罗摩克里希纳|辨喜|奥罗宾多|拉玛那/.test(full))return '🕉 印度教·近代';
  // 儒家
  if(/孔子|孟子|荀子|董仲舒|朱熹|王阳明|王守仁|陆九渊|程颢|程颐|周敦颐|张载|邵雍|韩愈|柳宗元|欧阳修|苏轼|王安石|苏洵|苏辙|曾巩|颜回|子思|司马迁|班昭|郑玄|顾炎武|黄宗羲|王夫之/.test(full))return '📜 儒家';
  // 道家
  if(/老子|庄子|列子|张道陵|王重阳|关尹子|葛洪|寇谦之|吕洞宾|陈抟|丘处机|张三丰|陶弘景|司马承祯|白玉蟾|张伯端/.test(full))return '☯ 道家·道教';
  // 西方
  if(/耶稣|穆罕默德|柏拉图|亚里士多德|奥古斯丁|阿奎那|康德|黑格尔/.test(full))return '🔮 西方哲学·宗教';
  // 伊斯兰
  if(/鲁米|伊本|安萨里|花拉子密/.test(full))return '☪ 伊斯兰教';

  // ── 近现代学人(名相) ──
  if(/胡适|梁启超|欧阳竟无|吕澂|汤用彤|魏道儒|王颂|邱高兴|张文良/.test(full))return '🎓 近现代学者';

  // ── 最后防线: 类型推断(仅对li和名相都无法匹配的人员) ──
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
    all.push({id:p.id,n:p.n,ti:p.ti||'',tp:p.tp||'',li:p.li||'',b:p.b,d:p.d,color:DATA.lineage_colors[p.li]||'#b0a898',groups:groups});
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
    all.push({id:tid,n:t.name.split('·')[0],ti:t.name,li:'',b:yr,d:yr2,color:t.color||'#b0a898',groups:groups2});
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
        +(_tr&&_tr.verified?' <span style=color:#7d9a6e title='+(_tr.source||'')+'>✓</span>':'')
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
    if(nodeMap&&nodeMap[pid])selectPerson(pid);
    else if(typeof selectSuggestion==='function')selectSuggestion(pid);
    else console.error('Cannot select:',pid);
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
var TRANS_STORY=[
  {y:-1500,p:'吠陀仙人',lat:29.0,lng:76.0,ev:'雅利安人进入印度,吠陀宗教体系形成。梨俱吠陀为印度最古老宗教文献。轮回(karma)、禅定(dhyāna)等概念开始萌芽,为后来佛教思想提供了深厚的文化土壤。',src:'印度上古史'},
  {y:-800,p:'奥义书哲人',lat:26.5,lng:82.0,ev:'奥义书时代思想家提出梵(Brahman)与阿特曼(ātman)的哲学概念。佛教「无我」(anātman)说正是在与这一传统的对话和批判中形成。',src:'奥义书文献'},
  {y:-563,p:'释迦牟尼',lat:27.5,lng:83.3,ev:'悉达多太子诞生于迦毗罗卫城蓝毗尼园(今尼泊尔)。幼年受婆罗门传统教育,后出家求道,经历六年苦行。',src:'巴利文献·佛传'},
  {y:-528,p:'释迦牟尼',lat:24.7,lng:84.99,ev:'35岁时于菩提伽耶菩提树下觉悟成佛。华严宗传统认为《华严经》即于此后三七日中,于定中为法身大士所说,揭示法界缘起之宇宙实相。此为华严经教之源头。',src:'华严宗传统'},
  {y:-528,p:'释迦牟尼',lat:25.4,lng:83.0,ev:'成道后至鹿野苑为五比丘初转法轮,讲四圣谛八正道。佛教僧团成立。此后45年游化恒河流域,讲经三百余会。',src:'《杂阿含经》'},
  {y:-483,p:'释迦牟尼',lat:26.7,lng:83.9,ev:'80岁时于拘尸那罗入灭。佛教由此向四方传播。华严宗法身思想将释迦入灭理解为「化身隐而法身常」,毗卢遮那佛永恒说法于华藏世界。',src:'《大般涅槃经》'},
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
      tip.innerHTML="<div style=font-size:0.85em><b style=color:"+lc+">"+(ti||"?")+"</b> <b>"+pp.n+"</b> <span style=color:var(--text2)>"+pp.dy+"</span></div>"
	        +"<div style=font-size:0.7em;color:var(--text2);line-height:1.3>"+(pp.ti||"")+"</div>"
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
var ANIM_WAYPOINTS=[
  // 古印度文明·中国先秦
  {y:-1500,lat:29,lng:76,z:3,label:'吠陀文明·梨俱吠陀',info:'雅利安人入印,吠陀宗教体系形成。轮回、业力、禅定概念萌芽。'},
  {y:-800,lat:26.5,lng:82,z:3,label:'奥义书哲人·梵我哲学',info:'梵(Brahman)与阿特曼(ātman)概念提出。佛教「无我」说在此对话中形成。'},
  {y:-600,lat:34.0,lng:114.0,z:5,rel:'daoist',label:'☯老子·《道德经》',info:'老子(约前6世纪),道家学派创始人。据《史记》为周守藏室之史,居洛邑。后见周衰,西出函谷关,应关令尹喜之请著《道德经》五千言而去。',src:'《史记·老子韩非列传》'},
  {y:-570,lat:34.6,lng:112.4,z:5,rel:'daoist',label:'☯老子·周守藏室之史',info:'老子居洛邑任周王室守藏室之史(国家图书馆馆长)。在此期间博览典籍,形成其道法自然的哲学体系。',src:'《史记·老子韩非列传》'},
  {y:-551,lat:35.6,lng:116.9,z:5,rel:'confucian',label:'📖孔子诞生·鲁国陬邑',info:'孔子(前551-前479)生于鲁国陬邑(今山东曲阜)。父叔梁纥,母颜徵在。三岁丧父,家贫而好学。',src:'《史记·孔子世家》'},
  {y:-522,lat:35.6,lng:116.9,z:5,rel:'confucian',label:'📖孔子·三十而立·始教',info:'孔子约三十岁时开始授徒讲学,创办私学。主张有教无类,打破贵族对教育的垄断。',src:'《史记·孔子世家》'},
  {y:-497,lat:36.0,lng:117.0,z:5,rel:'confucian',label:'📖孔子·周游列国',info:'孔子55岁离开鲁国,开始14年周游列国之旅。先后至卫宋陈蔡等十余国,宣扬仁政德治,然终不见用。途中困于陈蔡之间,仍弦歌不辍。',src:'《史记·孔子世家》'},
  {y:-484,lat:35.6,lng:116.9,z:5,rel:'confucian',label:'📖孔子·归鲁删述六经',info:'68岁归鲁。整理《诗》《书》《礼》《乐》《易》《春秋》六经,为中国文化传承做出奠基性贡献。',src:'《史记·孔子世家》'},
  {y:-479,lat:35.6,lng:116.9,z:5,rel:'confucian',label:'📖孔子逝世·儒学历程开始',info:'73岁卒于鲁国。弟子编《论语》,儒学逐渐成为中华文明主流思想,后与佛教形成长达两千年的融突关系。'},
  {y:-372,lat:35.5,lng:117.0,z:5,rel:'confucian',label:'📖孟子·性善论',info:'孟子(约前372-前289),战国儒家代表。提出性善论仁政说。其心性之学后与佛教如来藏思想有深层对话空间。',src:'《史记·孟子荀卿列传》'},
  {y:-335,lat:36.0,lng:117.0,z:5,rel:'confucian',label:'📖孟子·游说齐梁',info:'孟子效法孔子周游列国,先后至齐梁等国宣扬仁政王道。齐宣王时曾为客卿,但主张终不见用。晚年退而与弟子万章等作《孟子》七篇。',src:'《史记·孟子荀卿列传》'},
  {y:-469,lat:37.9,lng:23.7,z:4,rel:'western',label:'🏛苏格拉底·雅典',info:'苏格拉底(前469-前399),古希腊哲学奠基人。与孔子大致同时代,东西方哲学两大源头并行发展。',bg:1,src:'西洋哲学史'},
  {y:-334,lat:33.0,lng:44.0,z:3,rel:'western',label:'🏛亚历山大大帝东征',info:'亚历山大东征至印度河流域,希腊文化与印度文明首次大规模接触。为后来犍陀罗佛教艺术的出现埋下伏笔。',bg:1,src:'世界史'},
  {y:-479,lat:35.6,lng:116.9,z:5,rel:'confucian',label:'📖孔子逝世·儒学历程开始',info:'孔子逝世后,弟子编《论语》。儒学逐渐成为中华文明主流思想,后与佛教形成长达两千年的融突关系。'},
  {y:-372,lat:35.5,lng:117.0,z:5,rel:'confucian',label:'📖孟子·性善论',info:'孟子(约前372-前289),战国儒家代表。提出性善论仁政说。其心性之学后与佛教如来藏思想有深层对话空间。',src:'《史记·孟子荀卿列传》'},
  {y:-369,lat:33.5,lng:115.0,z:5,rel:'daoist',label:'☯庄子·蒙地漆园吏',info:'庄子(约前369-前286)生于宋国蒙地(今豫皖交界)。曾任漆园吏,后弃官隐居。楚威王曾聘其为相,庄子笑拒:宁游戏污渎之中自快,无为有国者所羁。',src:'《史记·老子韩非列传》'},
  {y:-300,lat:33.5,lng:115.0,z:5,rel:'daoist',label:'☯庄子·著《南华真经》',info:'庄子晚年著书十万余言。《逍遥游》论精神自由,《齐物论》破主客二元,《养生主》说庖丁解牛。其坐忘心斋之说后与佛教禅观相通。',src:'《庄子》/《史记》'},
  {y:-313,lat:35.0,lng:116.0,z:5,rel:'confucian',label:'📖荀子·性恶论',info:'荀子(约前313-前238),战国儒家。性恶隆礼重法。其天人之分与佛教缘起论有可比较处。',src:'《史记·孟子荀卿列传》'},
  // 释迦生平
  {y:-563,lat:27.5,lng:83.3,z:5,label:'释迦诞生·蓝毗尼园',info:'悉达多太子生于迦毗罗卫。幼受婆罗门教育,后出家求道。'},
  {y:-528,lat:24.7,lng:85,z:5,label:'释迦成道·菩提伽耶',info:'35岁菩提树下觉悟。华严宗传统:此后三七日于定中说《华严经》,揭示法界缘起。'},
  {y:-500,lat:25.5,lng:83.0,z:4,label:'六师外道·印度思想百花齐放',info:'佛陀时代六大非佛教思想家活跃。耆那教(尼乾陀若提子)、唯物论(阿耆多)、宿命论(末伽梨)等与佛教同时竞争。佛教正是在这一多元思想生态中确立其独特教义。',bg:1,src:'《沙门果经》(DN 2)'},
  {y:-528,lat:25.4,lng:83,z:5,label:'初转法轮·鹿野苑',info:'为五比丘说四圣谛八正道。僧团成立,佛教诞生。此后45年游化讲经。'},
  {y:-483,lat:26.74,lng:83.89,z:5,label:'释迦入灭·拘尸那罗',info:'80岁于拘尸那罗入灭。弟子结集经律,佛教由此向四方传播。'},
  // 佛教东传
  {y:-260,lat:25.3,lng:83,z:4,label:'阿育王·佛教走出印度',info:'阿育王皈依,派传教师向中亚东南亚传播。第三次结集。佛教从区域宗教变为世界宗教。',src:'阿育王石刻诏书'},
  {y:-200,lat:34.0,lng:72.0,z:4,label:'希腊·犍陀罗佛教艺术(有争议)',info:'希腊-巴克特里亚时期佛教与希腊艺术在犍陀罗相遇。最早佛像出现时间学界有争议:一说公元前1世纪,一说公元1世纪。犍陀罗在佛教东传中的枢纽地位则无争议。',src:'佛教艺术史(有学术争议)'},
  {y:-100,lat:33.7,lng:72.8,z:4,label:'犍陀罗·大乘经论结集',info:'犍陀罗地区成为大乘佛教发展重镇。般若经、华严经等大乘经典在此地区逐步形成。',src:'佛教文献学'},
  {y:65,lat:33.7,lng:72.8,z:4,label:'迦腻色迦王·犍陀罗结集',info:'贵霜帝国第四次结集。佛法深入中亚,犍陀罗成东传枢纽。大乘经论在此大量结集。'},
  {y:80,lat:27.5,lng:77.7,z:4,label:'马鸣·大乘起信论',info:'造《大乘起信论》。一心二门之说后为华严心性论与判教体系的重要理论基础。'},
  {y:-136,lat:34.3,lng:108.9,z:5,rel:'confucian',label:'📖汉武帝·独尊儒术',info:'董仲舒建议罢黜百家独尊儒术。儒学成为汉朝官方意识形态,后来佛教入华时与儒家伦理产生深刻碰撞与融合。',src:'《汉书·董仲舒传》'},
  {y:0,lat:31.7,lng:35.2,z:4,rel:'western',label:'✝耶稣诞生·伯利恒',info:'耶稣基督诞生于犹太伯利恒。基督教此后逐渐发展为世界性宗教,与佛教在欧亚大陆两端并行发展。',bg:1,src:'《新约圣经》'},
  {y:34,lat:32.0,lng:108.0,z:5,rel:'daoist',label:'☯张道陵诞生·沛国丰县',info:'张道陵(34-156),原名张陵,沛国丰县人(今江苏丰县)。早年通晓五经,后弃儒学道。',src:'《后汉书》《神仙传》'},
  {y:100,lat:30.0,lng:105.0,z:5,rel:'daoist',label:'☯张道陵·入蜀鹤鸣山',info:'张道陵入蜀至鹤鸣山(今四川大邑)。在此得太上老君亲授天师之位,创正一盟威之道(五斗米道)。',src:'《神仙传》'},
  {y:142,lat:30.5,lng:104.0,z:5,rel:'daoist',label:'☯张道陵·青城山·道教正式创立',info:'张道陵在青城山设二十四治(教区),正式建立天师道。奉老子为教祖,以《道德经》为根本经典,《老子想尔注》阐发教义。道教从此成为有组织的宗教。',src:'《后汉书·刘焉传》《神仙传》'},
  {y:156,lat:30.5,lng:104.0,z:5,rel:'daoist',label:'☯张道陵·飞升·系师张衡继任',info:'张道陵于青城山飞升(逝世),享年123岁。其子张衡继任为第二代天师(系师),孙张鲁为第三代天师,天师世家由此传承至今。',src:'《神仙传》《三国志·张鲁传》'},
  {y:167,lat:34.7,lng:112.4,z:5,label:'支谶译兜沙经·华严首入汉地',info:'月氏僧支娄迦谶至洛阳,译《佛说兜沙经》。虽仅1卷,却是华严经文首次汉译。'},
  {y:320,lat:25.1,lng:85.4,z:4,label:'无著·世亲·那烂陀寺',info:'瑜伽行派于那烂陀弘传。世亲造《十地经论》,后经汉译催生地论学派。'},
  // 西域走廊
  {y:344,lat:41.7,lng:82.9,z:4,label:'鸠摩罗什出生·龟兹',info:'罗什生于西域龟兹。后至长安成四大译师之首,译十住经等为华严学奠基。'},
  {y:359,lat:34,lng:72,z:4,label:'佛驮跋陀罗·北天竺',info:'觉贤生于北天竺。后至建康首译六十华严全本。'},
  {y:401,lat:34.3,lng:108.9,z:5,label:'罗什至长安·译经运动',info:'弘始三年至长安,八百沙门参与译场。译中论/十住经/法华经等。'},
  // 汉地·华严宗形成
  {y:320,lat:30.0,lng:115.0,z:5,rel:'daoist',label:'☯葛洪·《抱朴子》',info:'葛洪(283-363),晋代道教思想家。著《抱朴子》内篇系统阐述道教神仙理论。道教从此有了完整的理论体系。',bg:1,src:'《晋书·葛洪传》'},
  {y:399,lat:34.3,lng:108.9,z:5,label:'法显西行·长安出发',info:'法显(337-422)以65岁高龄从长安出发,经河西走廊、敦煌、鄯善、于阗,越葱岭至印度。同行11人,途中或返或亡。',src:'《佛国记》'},
  {y:405,lat:37.1,lng:79.9,z:5,label:'法显·于阗·观行像盛会',info:'法显至于阗国,恰逢盛大的行像法会。记录于阗佛教繁荣景象。于阗后为藏译华严底本来源。',src:'《佛国记》'},
  {y:410,lat:25.1,lng:85.4,z:5,label:'法显·抵达中天竺',info:'法显越过葱岭雪山进入印度。游历那烂陀、菩提伽耶、鹿野苑等圣迹,学梵书梵语,抄写戒律。',src:'《佛国记》'},
  {y:420,lat:32.1,lng:118.8,z:5,label:'六十华严·建康道场寺',info:'佛驮跋陀罗译六十华严34品。华严经首次以全貌呈现汉地。'},
  {y:468,lat:34.7,lng:112.4,z:5,label:'慧光·地论南道派',info:'从勒那摩提学十地经论,开地论南道。其学数代传至智俨法藏,为华严义学前身。'},
  {y:313,lat:41.0,lng:28.9,z:4,rel:'western',label:'✝米兰敕令·基督教合法化',info:'罗马皇帝君士坦丁颁布米兰敕令,基督教在罗马帝国合法化。从此基督教与佛教在欧亚大陆两端各自传播发展。',bg:1,src:'罗马帝国史'},
  {y:508,lat:34.7,lng:112.4,z:5,label:'十地经论·洛阳译出',info:'菩提流支译世亲十地经论。催生南北朝最重要的义学流派:地论学派。'},
  {y:557,lat:33.9,lng:109,z:6,label:'杜顺·终南山·华严创宗',info:'著法界观门/五教止观。以法界三观和五教止观为华严宗奠定修行理论基础。'},
  {y:597,lat:29.2,lng:121,z:5,label:'智𫖮·天台宗成立',info:'天台宗于天台山成立(中国最早宗派)。华严判教中「同教一乘」即针对天台而设。'},
  {y:602,lat:33.9,lng:109,z:6,label:'智俨·华严二祖',info:'从杜顺出家,著搜玄记/一乘十玄门。开创华严宗经疏传统,为法藏之师。'},
  {y:643,lat:34.3,lng:108.9,z:6,label:'法藏·华严三祖·宗派确立',info:'系统化五教十宗判教。武则天赐号贤首。参与八十华严译场证义。华严宗至此正式确立。'},
  {y:629,lat:34.3,lng:108.9,z:5,label:'玄奘西行·长安出发',info:'玄奘(602-664)29岁从长安出发,经秦州、凉州、瓜州,偷渡玉门关,穿越莫贺延碛沙漠,九死一生抵高昌。',src:'《大唐大慈恩寺三藏法师传》'},
  {y:631,lat:25.1,lng:85.4,z:5,label:'玄奘·抵达那烂陀寺',info:'玄奘越兴都库什山进入印度,在那烂陀寺师从戒贤法师,学习瑜伽师地论等。戒贤为无著世亲瑜伽行派传人。',src:'《大慈恩寺三藏法师传》'},
  {y:643,lat:24.7,lng:84.9,z:5,label:'玄奘·曲女城无遮大会',info:'戒日王为玄奘在曲女城举行无遮大会,18国王齐聚。玄奘立真唯识量,18日无人能破,获大乘天和解脱天尊号。',src:'《大慈恩寺三藏法师传》'},
  {y:645,lat:34.3,lng:108.9,z:5,label:'玄奘归国·唯识宗兴起',info:'玄奘携657部梵本归国,创唯识宗。华严性宗与唯识相宗形成教内深度对话。'},
  {y:671,lat:23.1,lng:113.3,z:5,label:'义净·广州乘船赴印',info:'义净(635-713)37岁从广州搭乘波斯商船出发,经南海诸国至印度。选择海路避开了西域战乱,开辟求法新路线。',src:'《南海寄归内法传》'},
  {y:675,lat:25.1,lng:85.4,z:5,label:'义净·那烂陀寺留学',info:'义净抵达那烂陀寺,留学十载。学习瑜伽、中观、因明,并抄写戒律典籍。期间还到访王舍城灵鹫山等圣迹。',src:'《南海寄归内法传》'},
  {y:695,lat:34.3,lng:108.9,z:5,label:'义净归国·洛阳',info:'义净携梵本400余部归国,武则天亲迎于洛阳。后主持译场译经56部230卷,偏重律藏。与法显、玄奘并称中国三大求法僧。',src:'《宋高僧传》卷一'},
  {y:652,lat:37.1,lng:79.9,z:4,label:'实叉难陀·于阗',info:'生于于阗。于阗为中亚佛教枢纽:既是实叉难陀故乡,又是藏译华严底本来源。'},
  {y:699,lat:34.7,lng:112.4,z:6,label:'八十华严·洛阳佛授记寺',info:'实叉难陀译八十华严39品。法藏证义。后世流传最广汉译本。'},
  {y:712,lat:34.3,lng:108.9,z:6,label:'法藏圆寂·长安',info:'华严三祖圆寂。讲华严经三十余遍,著五教章/探玄记。实际创立者功业圆满。'},
  {y:713,lat:24.8,lng:113.6,z:5,label:'慧能入灭·南宗禅兴起',info:'六祖慧能入灭。南宗禅此后大盛。华严五祖宗密兼为禅宗荷泽传人,开启禅教融合。'},
  {y:780,lat:34,lng:108.7,z:6,label:'宗密·圭峰·禅教融合',info:'华严五祖宗密住圭峰。著禅源诸诠集都序,融合华严与禅宗。教禅一致思想基础确立。'},
  {y:798,lat:34.3,lng:108.9,z:6,label:'四十华严·长安',info:'般若三藏译四十华严(入法界品全本)。善财五十三参完整故事得以汉译。'},
  {y:716,lat:34.3,lng:108.9,z:6,label:'善无畏·金刚智·开元三大士',info:'善无畏(637-735)716年至长安译大日经传胎藏界。金刚智(671-741)719年至长安译金刚顶经传金刚界。与不空并称开元三大士,中国密宗奠基。',src:'《宋高僧传》'},
  {y:725,lat:34.3,lng:108.9,z:6,label:'一行·大日经疏·大衍历',info:'一行(683-727)师事善无畏,协助译大日经并著疏二十卷。制大衍历为唐代最精确历法。兼通天文学与密宗义学。',src:'《宋高僧传》卷五'},
  {y:800,lat:29.7,lng:91.1,z:4,label:'藏译华严·吐蕃',info:'胜友/智军将于阗本华严译为藏文Toh44(45品)。华严经中亚于阗传入西藏。'},
  {y:805,lat:34.3,lng:108.9,z:6,label:'慧果·青龙寺·密宗集大成',info:'慧果(746-805)兼承善无畏胎藏界与金刚智金刚界两部密法。住长安青龙寺,为密宗第七祖。日本空海从此受法。',src:'空海《御请来目录》'},
  {y:806,lat:34.2,lng:135.6,z:6,label:'空海归国·日本真言宗创立',info:'空海(774-835)804年入唐从慧果受法,806年归国于高野山开创日本真言宗。著十住心论以华严判教框架判摄显密诸宗。',src:'日本佛教史'},
  {y:839,lat:39,lng:113.6,z:6,label:'澄观圆寂·五台山',info:'华严四祖圆寂。著华严经疏60卷/演义钞90卷。集大成者,历七帝之师。'},
  {y:610,lat:21.4,lng:39.8,z:4,rel:'islamic',label:'☪穆罕默德·伊斯兰教创立',info:'穆罕默德在麦加开始传播伊斯兰教。世界三大宗教格局(佛教/基督教/伊斯兰教)至此确立。',bg:1,src:'《古兰经》/伊斯兰教史'},
  {y:841,lat:34,lng:108.7,z:5,label:'宗密圆寂·华严盛极而衰',info:'五祖宗密圆寂。次年武宗灭佛,华严典籍大量焚毁,此后转入隐传阶段。'},
  {y:845,lat:34.3,lng:108.9,z:5,label:'会昌法难·华严典籍焚毁',info:'唐武宗灭佛。华严传承几近断绝。此后义学隐传,直至宋代复兴。'},
  {y:800,lat:30.0,lng:112.0,z:5,rel:'daoist',label:'☯吕洞宾·道教内丹',info:'吕洞宾(约798-?),唐末五代道教宗师。后被尊为八仙之一。其内丹学说吸收佛教禅宗心性论,体现佛道深度融合。',bg:1,src:'道教神仙传'},
  {y:868,lat:40.0,lng:94.8,z:5,label:'金刚经雕版·敦煌',info:'敦煌出土咸通九年(868年)雕版印刷金刚经,世界现存最早有纪年的印刷品。佛教经典的传播方式从此革命性变化。',src:'大英图书馆藏敦煌文献'},
  {y:907,lat:34.3,lng:108.9,z:5,label:'唐亡·五代十国',info:'唐朝灭亡,进入五代十国分裂时期。北方战乱频繁,佛教学术重心南移。吴越钱氏、南唐李氏保护佛教。',src:'中国通史'},
  // 东亚传播·宗派互动
  {y:973,lat:37.6,lng:127,z:5,label:'均如·统一高丽华严',info:'高丽学僧均如统一华严南北二宗。著三宝章圆通钞。早于义天,为高丽华严前驱。'},
  {y:1011,lat:30.2,lng:120.1,z:6,label:'净源中兴·杭州慧因寺',info:'宋代华严复兴。慧因寺世称华严第一道场。后义天入宋求法于此。'},
  {y:1038,lat:30.2,lng:120.1,z:6,label:'子璿·兼弘贤首天台',info:'长水子璿著起信论疏笔削记。兼弘贤首与天台,体现宋代宗派融合趋势。'},
  {y:1050,lat:34.0,lng:113.0,z:5,rel:'confucian',label:'📖宋明理学兴起',info:'周敦颐(1017-1073)创太极图说,张载(1020-1077)立气论,二程(1032-1085)发明天理。理学吸收佛教心性论与华严理事无碍思维,开儒学新纪元。',src:'《宋史·道学传》'},
  {y:1085,lat:30.2,lng:120.1,z:6,label:'义天入宋·杭州慧因寺',info:'高丽王子义天从净源受华严。归国编义天录。华严经杭州传入朝鲜半岛。'},
  {y:1101,lat:37.6,lng:127,z:5,label:'义天圆寂·高丽开京',info:'义天圆寂。此后高丽学僧继续弘扬,朝鲜半岛成东亚华严重镇。'},
  {y:1173,lat:35,lng:135.8,z:5,label:'明惠中兴·日本高山寺',info:'明惠复兴日本华严。高山寺开山,兼弘戒律真言。东亚华严网络最终一环形成。'},
  {y:1271,lat:39.9,lng:116.4,z:5,label:'元朝·八思巴帝师',info:'元朝建立,藏传佛教入汉。八思巴为国师。海云继梦认为此后禅宗正法心法失传七~八百年。'},
  {y:1200,lat:28.0,lng:118.0,z:5,rel:'confucian',label:'📖朱熹·理学集大成',info:'朱熹(1130-1200)集北宋理学大成,确立程朱理学体系。其格物穷理与华严事事无碍有可比较的认识论结构。朱子学后传入朝鲜日本,影响东亚思想史。',src:'《宋元学案》'},
  {y:1368,lat:32.0,lng:118.8,z:5,label:'明朝建立·洪武',info:'朱元璋建都南京,早年曾出家为僧。明初设立僧官制度,整顿佛教,天下寺院分禅讲教三类管理。',src:'《明史》'},
  {y:1409,lat:29.6,lng:91.1,z:5,label:'宗喀巴·格鲁派创立',info:'宗喀巴大师在拉萨创大昭寺传召法会,格鲁派(黄教)正式确立。藏传佛教进入新的发展阶段。',src:'藏传佛教史'},
  {y:1508,lat:26.5,lng:106.7,z:5,rel:'confucian',label:'📖王阳明·龙场悟道',info:'王守仁(1472-1529)在贵州龙场悟道,提出知行合一。阳明心学与禅宗明心见性有深度亲缘性,其「致良知」近于佛教本觉思想。后传入日本,影响明治维新。',src:'《明儒学案》'},
  {y:1517,lat:51.0,lng:11.0,z:4,rel:'western',label:'✝马丁·路德·宗教改革',info:'马丁·路德在维滕堡贴出九十五条论纲,欧洲宗教改革开始。此后基督教世界分裂,西方进入宗教多元化时代。',bg:1,src:'世界史'},
  {y:1687,lat:52.0,lng:-0.1,z:4,rel:'western',label:'🔬牛顿·自然哲学原理',info:'牛顿发表《自然哲学的数学原理》,科学革命达到高峰。此后科学与宗教的关系成为西方思想核心议题,与佛教对宇宙的解释形成遥远对照。',bg:1,src:'科学史'},
  {y:1578,lat:38.0,lng:110.0,z:5,label:'俺答汗·达赖喇嘛封号',info:'蒙古俺答汗迎请三世达赖索南嘉措,赠予达赖喇嘛称号。藏传佛教与蒙古政治力量结合。',src:'蒙藏佛教史'},
  // 近现代
  {y:1600,lat:30.2,lng:120.1,z:5,label:'明末四大师·佛教复兴',info:'紫柏/憨山/莲池/澫益四大师推动晚明佛教全面复兴。华严学亦受此波影响。'},
  {y:1644,lat:39.9,lng:116.4,z:5,label:'清军入关·明亡',info:'清朝建立。顺治帝笃信佛教,礼敬禅僧。清初佛教在战乱后逐步恢复。',src:'《清史稿》'},
  {y:1641,lat:30.2,lng:120.1,z:6,label:'续法·清代华严集大成',info:'著贤首五教仪整理判教,编华严宗佛祖传梳理谱系。讲经二十余遍。'},
  {y:1720,lat:30.0,lng:91.0,z:5,label:'康熙平定西藏',info:'清军入藏,确立对西藏的管辖。藏传佛教格鲁派与清廷关系制度化。',src:'《清圣祖实录》'},
  {y:1793,lat:29.6,lng:91.1,z:5,label:'乾隆·钦定藏内善后章程',info:'确立金瓶掣签制度。藏传佛教活佛转世纳入国家管理。',src:'《卫藏通志》'},
  {y:1860,lat:32.0,lng:118.8,z:5,label:'太平天国·佛教重创',info:'太平军占据江南,大量寺院被毁,经书遭焚。江南佛教遭受空前打击。',src:'中国近代佛教史'},
  {y:1898,lat:39.9,lng:116.4,z:5,label:'戊戌变法·庙产兴学',info:'张之洞提出庙产兴学主张,将寺院财产充作教育经费。此政策持续影响近代佛教至民国。',src:'《劝学篇》'},
  {y:1880,lat:34.0,lng:109.0,z:5,rel:'daoist',label:'☯陈撄宁·现代道教复兴',info:'陈撄宁(1880-1969),近代道教重要学者。创办《仙学》月刊,提倡仙学独立于儒释,推动道教的现代化转型。',bg:1,src:'中国道教史'},
  {y:1912,lat:34.5,lng:110.0,z:5,rel:'daoist',label:'☯张志顺·全真高道',info:'张志顺(1912-2015),全真龙门派第二十一代传人。以百岁高龄仍坚持修行传道,被认为是近代道家实修的典范人物。',bg:1,src:'道教人物志'},
  {y:1914,lat:31.7,lng:120.7,z:7,label:'华严大学·常熟兴福寺',info:'月霞创立近代第一所华严专宗教育机构。培养常惺/持松等现代学僧。'},
  {y:1936,lat:34.3,lng:108.9,z:5,rel:'daoist',label:'☯任法融·中国道协会长',info:'任法融(1936-2021),原中国道教协会会长。著《道德经释义》等,以现代语言诠释道家经典。推动道教与当代社会对话。',bg:1,src:'中国道教协会'},
  {y:1952,lat:25,lng:121.6,z:7,label:'华严莲社·台北',info:'智光/南亭创社,开启台湾华严弘传。成一/贤度相继,发展为现代学术教育中心。'},
  {y:1975,lat:25,lng:121.5,z:7,label:'华严专宗学院·台北',info:'成一法师创办,以专修/专研/专弘华严为宗旨。当代最重要华严教育机构。'},
  {y:1991,lat:25,lng:121.5,z:7,label:'梦参剃度·临济47代',info:'海云继梦(陈鹤山)于梦参老和尚座下剃度,法名昌一号继梦。此前十年以在家身弘法,奠定现代语言诠释华严的教学风格。'},
  {y:2004,lat:34.2,lng:108.9,z:6,label:'西安弘法·社科院演讲',info:'受聘陕师大华严研究所荣誉所长。社科院演讲(首位登台出家人)。2006-2010北京广化寺系统弘讲四十华严全本。'},
  {y:2008,lat:23.9,lng:120.9,z:9,label:'三脉汇流·普贤乘确立',info:'★核心★钦因传华严衣钵(贤首42世)+胜师子王菩萨传瑜伽行。三脉归一开创普贤乘华严宗。技术面(数随止)+工程面(ABC心法)双轨。四阶段:出离→菩提→菩萨→普贤乘。'},
  {y:2011,lat:25,lng:121.5,z:7,label:'华严六科·五大行法定型',info:'六科(概论/经教/禅法/戒律/净土/密法)+五大行法(禅净律密经教)完整出版。三部曲(非常坛经/金刚经/心经)确立修行框架。'},
  {y:2013,lat:25,lng:121.5,z:7,label:'海云华严研究所成立',info:'熊琬教授任所长。华严学报创刊(已出14期)。忍可灌顶制度+禅观一览表公开发布。修学体系从个人教学转向制度化僧团教育。'},
  {y:2021,lat:27.7,lng:85.3,z:5,label:'84000英译·华严回归国际',info:'Peter Alan Roberts英译入法界品出版。藏文华严首次系统英译。'},
  {y:2026,lat:24.5,lng:120.7,z:9,label:'九九华严·支提山动土',info:'台北TICC五年讲座。苗栗通霄支提山大华严寺动土,隔海与福建宁德支提华严祖庭相望。五十三位嘉宾执铲呼应善财五十三参。义理传播与道场建设双线并行。'}
];
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
          var popupOffset={buddhist:[0,-12],confucian:[30,-20],daoist:[-30,-8],western:[20,-30],islamic:[-20,-25]};
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
