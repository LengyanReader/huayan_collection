// ═══ 华藏世界海 COSMOLOGY TAB ═══
// 参考: 敦煌华严海会图 + 华严经华藏世界品 + 日本华严曼荼罗
var cosmoScale=1,cosmoSel=null,cosmoShowNet=true,cosmoShowAll=false;
var COSMO_WINDS=['平等住','出生宝庄严','清净光','光明轮','普持','不动','普照','法界云','大光明','法界光明云'];
var COSMO_LAYERS=[
  {n:'最胜光遍照',b:'净眼离垢灯佛'},{n:'种种香莲华妙庄严',b:'师子光胜照佛'},
  {n:'一切宝庄严普照光',b:'净光智胜幢佛'},{n:'种种光明华庄严',b:'金刚光明无量精进力善出现佛'},
  {n:'普放妙华光',b:'香光喜力海佛'},{n:'净妙光明',b:'普光自在幢佛'},
  {n:'众华焰庄严',b:'欢喜海功德名称自在光佛'},{n:'出生威力地',b:'广大名称智海幢佛'},
  {n:'出妙音声',b:'清净月光明相无能摧伏佛'},{n:'金刚幢',b:'一切法海最胜王佛'},
  {n:'恒出现帝青宝光明',b:'无量功德海光明佛'},{n:'光明照耀',b:'超释梵光佛'},
  {n:'娑婆世界',b:'毗卢遮那如来',saha:true},{n:'寂静离尘光',b:'遍法界胜音佛'},
  {n:'众妙光明灯',b:'不可摧伏力普照幢佛'},{n:'清净光遍照',b:'清净日功德眼佛'},
  {n:'宝庄严藏',b:'无碍智光明遍照十方佛'},{n:'离尘',b:'无量方便最胜幢佛'},
  {n:'清净光普照',b:'普照法界虚空光佛'},{n:'妙宝焰',b:'福德相光明佛'}
];

function renderCosmology(){
  var cv=document.getElementById("cosmology-view");if(!cv)return;
  var h="<style>.cosmo-btn{padding:3px 10px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.73em;transition:all 0.2s}.cosmo-btn.active{background:var(--gold);color:#fff;border-color:var(--gold)}#cosmo-info{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin-top:8px;font-size:0.82em;line-height:1.7;min-height:50px;display:none}</style>";
  h+="<div class=section style=border-left:4px solid var(--gold)><h2>🪷 华藏世界海 · 华严经华藏世界品</h2><p style=font-size:0.82em;color:var(--text2);line-height:1.7>据《大方广佛华严经·华藏世界品》(T10n0279卷八~十),十重风轮持香水海,海中出大莲华,华藏世界安住其中。共<b>二十重世界</b>层层叠绕。毗卢遮那佛法身遍满,一一世界互摄互入如因陀罗网。源: CBETA T10n0279 + 敦煌莫高窟华严海会图</p></div>";
  h+="<div style='display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap'>";
  h+="<button class='cosmo-btn active' id=cosmo-net-btn onclick='toggleCosmoNet()'>🕸 因陀罗网</button>";
  h+="<button class='cosmo-btn' id=cosmo-all-btn onclick='toggleCosmoAll()'>📋 全部层名</button>";
  h+="<span style=font-size:0.7em;color:var(--text2)'>滚轮缩放 | 点击世界层查看</span></div>";
  h+="<div style='display:flex;gap:16px;flex-wrap:wrap'><div style='flex:1.5;min-width:400px;text-align:center;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px'><canvas id=cosmo-canvas style='max-width:100%;cursor:pointer'></canvas></div><div style='flex:1;min-width:220px'><div id=cosmo-info></div><div class=section style=margin-top:8px><h3 style=color:var(--gold);font-size:0.9em>📐 结构 (从下至上)</h3><p style=font-size:0.78em;line-height:1.9>⑩ 法界光明云风轮(顶)<br>⑨...② 中间八重风轮<br>① 平等住风轮(底)<br>━━━━━━━━━━<br>无边妙华光香水海<br>━━━━━━━━━━<br>一切香摩尼宝庄严大莲华<br>━━━━━━━━━━<br>第1~20重世界(自下而上)<br>  ★第13重: 娑婆世界<br>━━━━━━━━━━<br>一一世界有微尘数佛刹围绕</p></div></div></div>";
  cv.innerHTML=h;
  drawCosmo();
  var canvas=document.getElementById("cosmo-canvas");
  canvas.addEventListener('wheel',function(e){e.preventDefault();cosmoScale*=e.deltaY<0?1.12:0.89;cosmoScale=Math.max(0.4,Math.min(3,cosmoScale));drawCosmo();});
  canvas.addEventListener('click',function(e){handleCosmoClick(e);});
}

function drawCosmo(){
  var canvas=document.getElementById("cosmo-canvas");if(!canvas)return;
  var size=Math.min(600,canvas.parentElement.clientWidth-30);
  canvas.width=size;canvas.height=size;canvas.style.width=size+'px';canvas.style.height=size+'px';
  var ctx=canvas.getContext("2d");var cx=size/2,cy=size/2;
  ctx.clearRect(0,0,size,size);

  // ── Background ──
  var bgGrad=ctx.createRadialGradient(cx,cy,0,cx,cy,size/2);
  bgGrad.addColorStop(0,'#fefdf9');bgGrad.addColorStop(0.6,'#f6f2e8');bgGrad.addColorStop(1,'#e0d8c8');
  ctx.fillStyle=bgGrad;ctx.fillRect(0,0,size,size);

  var maxR=size*0.44*cosmoScale,minR=size*0.04*cosmoScale;
  var layerH=(maxR-minR)/20;

  // ── Wind-wheels (bottom arc, clockwise swirls) ──
  var windBase=maxR+5;
  for(var i=0;i<10;i++){
    var wR=windBase+i*4*cosmoScale;
    ctx.beginPath();ctx.arc(cx,cy,wR,-0.8*Math.PI,0.8*Math.PI);
    ctx.strokeStyle='rgba(94,139,158,'+(0.08+i*0.015)+')';ctx.lineWidth=0.8;ctx.setLineDash([2,8]);ctx.stroke();ctx.setLineDash([]);
    // Swirl mark at sides
    if(i%3===0){
      var sx=cx+wR*0.95,sy=cy;
      ctx.beginPath();ctx.arc(sx,sy,3*cosmoScale,0,Math.PI*2);ctx.fillStyle='rgba(94,139,158,0.3)';ctx.fill();
    }
  }
  if(cosmoScale>0.6){
    ctx.fillStyle='#8a7a6a';ctx.font='9px Microsoft YaHei';ctx.fillText('十重风轮',cx+maxR+15,cy);
  }

  // ── Fragrant ocean (blue semi-circle at bottom) ──
  ctx.beginPath();ctx.arc(cx,cy,maxR,-0.9*Math.PI,-0.1*Math.PI);
  ctx.lineTo(cx+maxR*0.6,cy+maxR*0.3);ctx.closePath();
  var oceanGrad=ctx.createLinearGradient(cx,cy-maxR,cx,cy+maxR);
  oceanGrad.addColorStop(0,'rgba(94,139,158,0.02)');oceanGrad.addColorStop(0.5,'rgba(94,150,170,0.08)');oceanGrad.addColorStop(1,'rgba(70,120,150,0.15)');
  ctx.fillStyle=oceanGrad;ctx.fill();
  if(cosmoScale>0.6){
    ctx.fillStyle='#5e8b9e';ctx.font='bold 10px Microsoft YaHei';
    ctx.fillText('无边妙华光香水海',cx-50,cy+maxR-10);
  }

  // ── Great Lotus petals (surrounding the cosmos) ──
  for(var p=0;p<20;p++){
    var ang=(p/20)*Math.PI*2-Math.PI/2;
    var petalR=maxR*1.02,petalW=maxR*0.08;
    ctx.beginPath();
    ctx.moveTo(cx+Math.cos(ang-0.04)*maxR*0.9,cy+Math.sin(ang-0.04)*maxR*0.9);
    ctx.quadraticCurveTo(cx+Math.cos(ang)*petalR*1.15,cy+Math.sin(ang)*petalR*1.15,
                         cx+Math.cos(ang+0.04)*maxR*0.9,cy+Math.sin(ang+0.04)*maxR*0.9);
    ctx.strokeStyle='rgba(184,134,60,0.2)';ctx.lineWidth=0.8;ctx.stroke();
  }

  // ── Light rays from center (dharmakaya radiance) ──
  for(var r=0;r<24;r++){
    var ra=(r/24)*Math.PI*2;
    ctx.beginPath();ctx.moveTo(cx+Math.cos(ra)*minR*2,cy+Math.sin(ra)*minR*2);
    ctx.lineTo(cx+Math.cos(ra)*maxR*0.85,cy+Math.sin(ra)*maxR*0.85);
    ctx.strokeStyle='rgba(184,134,60,0.06)';ctx.lineWidth=0.5;ctx.stroke();
  }

  // ── 20 world layers ──
  cosmoLayerRects=[];
  for(var i2=0;i2<COSMO_LAYERS.length;i2++){
    var ly=COSMO_LAYERS[i2];
    var r1=minR+i2*layerH,r2=r1+layerH;
    // Ring fill
    var alpha=ly.saha?0.2:(i2%2===0?0.04:0.07);
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);
    ctx.beginPath();ctx.arc(cx,cy,r1,0,Math.PI*2);
    ctx.fillStyle='rgba(184,134,60,'+alpha+')';ctx.fill('evenodd');
    // Ring border
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);
    ctx.strokeStyle=ly.saha?'#c46b5d':(i2===0||i2===19?'rgba(184,134,60,0.5)':'rgba(184,134,60,0.25)');
    ctx.lineWidth=ly.saha?2.5:(i2===0||i2===19?1:0.6);
    ctx.stroke();
    // Label (show when zoomed in or showAll mode)
    var showLabel=cosmoScale>0.7||ly.saha||cosmoShowAll;
    if(showLabel){
      var lr=(r1+r2)/2;
      var angle2=-Math.PI/2+(i2*0.22);
      var lx=cx+Math.cos(angle2)*lr,lyy=cy+Math.sin(angle2)*lr;
      ctx.fillStyle=ly.saha?'#c46b5d':'#5c5040';
      ctx.font=(ly.saha?'bold 11':'9')+'px Microsoft YaHei';
      var lbl=(ly.saha?'★ ':'')+(cosmoShowAll?(i2+1)+'·':'')+ly.n;
      ctx.fillText(lbl,lx+6,lyy+3);
      if(cosmoScale>0.9||ly.saha){
        ctx.fillStyle='#8a7a6a';ctx.font='8px Microsoft YaHei';
        ctx.fillText(ly.b,lx+6,lyy+14);
      }
    }
    cosmoLayerRects.push({r1:r1,r2:r2,layer:ly});
  }

  // ── Indra's Net ──
  if(cosmoShowNet){
    var sel=cosmoSel||COSMO_LAYERS[12];
    var selIdx=COSMO_LAYERS.indexOf(sel);
    var selR=minR+selIdx*layerH+layerH/2;
    for(var i3=0;i3<COSMO_LAYERS.length;i3++){
      if(i3===selIdx)continue;
      var tr=minR+i3*layerH+layerH/2;
      var a2=(i3*Math.PI*2/20);
      ctx.beginPath();ctx.moveTo(cx+Math.cos(a2)*selR,cy+Math.sin(a2)*selR);
      ctx.lineTo(cx+Math.cos(a2+0.15)*tr,cy+Math.sin(a2+0.15)*tr);
      ctx.strokeStyle='rgba(125,154,110,0.15)';ctx.lineWidth=0.5;ctx.stroke();
    }
  }

  // ── Center: Vairocana ──
  // Mandala (body halo)
  var haloGrad=ctx.createRadialGradient(cx,cy,minR*0.3,cx,cy,minR*2.5);
  haloGrad.addColorStop(0,'rgba(255,220,150,0.7)');haloGrad.addColorStop(0.3,'rgba(184,134,60,0.3)');haloGrad.addColorStop(0.7,'rgba(184,134,60,0.05)');haloGrad.addColorStop(1,'rgba(184,134,60,0)');
  ctx.fillStyle=haloGrad;ctx.beginPath();ctx.arc(cx,cy,minR*2.5,0,Math.PI*2);ctx.fill();
  // Head halo
  var headGrad=ctx.createRadialGradient(cx,cy-minR*0.4,0,cx,cy-minR*0.3,minR*1.2);
  headGrad.addColorStop(0,'rgba(255,240,200,0.9)');headGrad.addColorStop(0.5,'rgba(200,160,80,0.3)');headGrad.addColorStop(1,'rgba(184,134,60,0)');
  ctx.fillStyle=headGrad;ctx.beginPath();ctx.arc(cx,cy-minR*0.3,minR*1.2,0,Math.PI*2);ctx.fill();
  // Central 卍
  ctx.fillStyle='#b8863c';ctx.font='bold '+(16*cosmoScale)+'px Microsoft YaHei';
  ctx.fillText('卍',cx-9*cosmoScale,cy+5*cosmoScale);
  // Buddha label
  ctx.fillStyle='#8a6040';ctx.font='bold 12px Microsoft YaHei';
  ctx.fillText('毗卢遮那佛',cx-32,cy-minR*1.8);
  ctx.fillStyle='#a09080';ctx.font='9px Microsoft YaHei';
  ctx.fillText('(Vairocana · 法身)',cx-36,cy-minR*1.8+14);
  // Saha indicator
  ctx.fillStyle='#c46b5d';ctx.font='bold 10px Microsoft YaHei';
  var sahaR=minR+12*layerH+layerH/2;
  ctx.fillText('▼ 娑婆世界(第13层)',cx-48,cy-sahaR-4);
}

var cosmoLayerRects=[];
function handleCosmoClick(e){
  var canvas=document.getElementById("cosmo-canvas");if(!canvas)return;
  var rect=canvas.getBoundingClientRect();
  var mx=e.clientX-rect.left,my=e.clientY-rect.top;
  var cx=canvas.width/2,cy=canvas.height/2;
  var dist=Math.sqrt((mx-cx)*(mx-cx)+(my-cy)*(my-cy));
  for(var i=0;i<cosmoLayerRects.length;i++){
    var lr=cosmoLayerRects[i];
    if(dist>=lr.r1&&dist<=lr.r2){
      cosmoSel=lr.layer;
      var info=document.getElementById("cosmo-info");
      if(info){
        info.style.display='block';
        info.innerHTML='<h3 style=color:var(--gold)>🪷 '+lr.layer.n+' <span style=font-size:0.65em;color:var(--text2)>第'+(i+1)+'重</span></h3>'
          +'<p>🙏 <b>住佛</b>: '+lr.layer.b+'</p>'
          +(lr.layer.saha?'<p style=color:#c46b5d;line-height:1.7>★ <b>娑婆世界</b>——我们所居之三千大千世界。释迦牟尼佛于此示现成道度众生,而毗卢遮那佛为此世界之<b>法身本源</b>。《华严经》云:「此世界名娑婆,以金刚庄严为际,依种种色风轮所持莲华网住。」</p>':'')
          +'<p style=font-size:0.72em;color:var(--text2)>「一一世界海中,各有不可说佛刹微尘数世界围绕;一一微尘中,悉见一切世界;重重无尽,如因陀罗网。」<br>—— 《华严经·华藏世界品》</p>';
      }
      drawCosmo();return;
    }
  }
  // Click center = select Vairocana
  if(dist<minR*2){
    cosmoSel=COSMO_LAYERS[12];
    var info2=document.getElementById("cosmo-info");
    if(info2){info2.style.display='block';info2.innerHTML='<h3 style=color:var(--gold)>卍 毗卢遮那佛</h3><p>华严经根本教主。梵名Vairocana,意译<b>光明遍照</b>、大日如来。法身遍一切处,为华藏世界海之本体。二十重世界海中,一一佛刹皆毗卢遮那佛法身之显现。</p><p style=font-size:0.72em;color:var(--text2)>「佛身充满于法界,普现一切众生前;随缘赴感靡不周,而恒处此菩提座。」</p>';}
    drawCosmo();return;
  }
}
function toggleCosmoNet(){cosmoShowNet=!cosmoShowNet;document.getElementById('cosmo-net-btn').classList.toggle('active',cosmoShowNet);drawCosmo();}
function toggleCosmoAll(){cosmoShowAll=!cosmoShowAll;document.getElementById('cosmo-all-btn').classList.toggle('active',cosmoShowAll);drawCosmo();}
