// ═══ 华藏世界海 COSMOLOGY TAB ═══
var cosmoScale=1,cosmoSel=null,cosmoShowNet=true;
var COSMO_WINDS=[
  {n:'平等住风轮'},{n:'出生宝庄严风轮'},{n:'清净光风轮'},{n:'光明轮风轮'},{n:'普持风轮'},
  {n:'不动风轮'},{n:'普照风轮'},{n:'法界云风轮'},{n:'大光明风轮'},{n:'法界光明云风轮'}
];
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
  var h="<style>.cosmo-btn{padding:3px 10px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.73em;transition:all 0.2s}.cosmo-btn.active{background:var(--gold);color:#fff;border-color:var(--gold)}#cosmo-info{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin-top:10px;font-size:0.82em;line-height:1.7;min-height:60px;display:none}</style>";
  h+="<div class=section style=border-left:4px solid var(--gold)><h2>🪷 华藏世界海 · 华严经华藏世界品</h2><p style=font-size:0.82em;color:var(--text2);line-height:1.7>据《大方广佛华严经·华藏世界品》,十方风轮持香水海,海中出大莲华,华藏世界安住其中。共<b>二十重世界</b>,娑婆世界为第13层。毗卢遮那佛法身遍满一切。一一世界互摄互入,如因陀罗网重重无尽。<br>源: 《华严经》卷八~卷十 (T10n0279)</p></div>";
  h+="<div style='display:flex;gap:8px;align-items:center;margin-bottom:10px'>";
  h+="<button class='cosmo-btn active' onclick='toggleCosmoNet()'>🕸 因陀罗网</button>";
  h+="<span style=font-size:0.7em;color:var(--text2)>滚轮缩放 | 点击世界层查看详情 | 金色=娑婆世界</span></div>";
  h+="<div style='display:flex;gap:16px;flex-wrap:wrap'><div style='flex:1;min-width:350px;text-align:center'><canvas id=cosmo-canvas style='max-width:100%;cursor:pointer'></canvas></div><div style='flex:1;min-width:200px'><div id=cosmo-info></div><div class=section style=margin-top:8px><h3 style=color:var(--gold);font-size:0.9em>📐 华藏世界结构</h3><p style=font-size:0.78em;line-height:1.8>① 十种风轮(最底)<br>② 无边妙华光香水海<br>③ 一切香摩尼宝庄严大莲华<br>④ 二十重世界层(竖叠)<br>⑤ 第13层=娑婆世界(我们所在)<br>⑥ 一一世界有微尘数佛刹围绕<br>⑦ 因陀罗网:一一珠现一切珠影</p></div></div>";
  cv.innerHTML=h;
  drawCosmo();
  // Event handlers
  var canvas=document.getElementById("cosmo-canvas");
  canvas.addEventListener('wheel',function(e){e.preventDefault();cosmoScale*=e.deltaY<0?1.12:0.89;cosmoScale=Math.max(0.5,Math.min(3,cosmoScale));drawCosmo();});
  canvas.addEventListener('mousemove',function(e){handleCosmoHover(e);});
  canvas.addEventListener('click',function(e){handleCosmoClick(e);});
}

function drawCosmo(){
  var canvas=document.getElementById("cosmo-canvas");if(!canvas)return;
  var size=Math.min(600,canvas.parentElement.clientWidth-20);
  canvas.width=size;canvas.height=size;canvas.style.width=size+'px';canvas.style.height=size+'px';
  var ctx=canvas.getContext("2d");var cx=size/2,cy=size/2;
  ctx.clearRect(0,0,size,size);
  // Background
  var grad=ctx.createRadialGradient(cx,cy,0,cx,cy,size/2);
  grad.addColorStop(0,'#fdfaf3');grad.addColorStop(1,'#e8e0d2');
  ctx.fillStyle=grad;ctx.fillRect(0,0,size,size);

  var maxR=size*0.46*cosmoScale,minR=size*0.06*cosmoScale;
  var layerH=(maxR-minR)/COSMO_LAYERS.length;

  // Wind-wheels (outermost, 10 dashed rings)
  for(var i=0;i<COSMO_WINDS.length;i++){
    var r=maxR+8+(i*5)*cosmoScale;
    ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);
    ctx.strokeStyle='rgba(94,139,158,0.2)';ctx.lineWidth=0.8;ctx.setLineDash([3,6]);ctx.stroke();ctx.setLineDash([]);
  }
  // Wind label
  if(cosmoScale>0.8){
    ctx.fillStyle='#a09080';ctx.font='9px Microsoft YaHei';
    ctx.fillText('十重风轮',cx+maxR+20,cy-10);
  }

  // Fragrant ocean (blue ring)
  ctx.beginPath();ctx.arc(cx,cy,maxR,0,Math.PI*2);
  ctx.beginPath();ctx.arc(cx,cy,minR-layerH*1.5,0,Math.PI*2);
  ctx.fillStyle='rgba(94,139,158,0.06)';ctx.fill('evenodd');

  // 20 world layers
  cosmoLayerRects=[];
  for(var i2=0;i2<COSMO_LAYERS.length;i2++){
    var ly=COSMO_LAYERS[i2];
    var r1=minR+i2*layerH,r2=r1+layerH;
    var alpha=ly.saha?0.18:(i2%2===0?0.04:0.07);
    // Fill ring
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);
    ctx.beginPath();ctx.arc(cx,cy,r1,0,Math.PI*2);
    ctx.fillStyle='rgba(184,134,60,'+alpha+')';ctx.fill('evenodd');
    // Border
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);
    ctx.strokeStyle=ly.saha?'#c46b5d':'rgba(184,134,60,0.4)';ctx.lineWidth=ly.saha?2.5:0.8;
    ctx.stroke();
    // Label
    if(cosmoScale>0.65||ly.saha){
      var lr=(r1+r2)/2;
      var angle=-Math.PI/2+(i2*0.15); // stagger labels around ring
      var lx=cx+Math.cos(angle)*lr,lyy=cy+Math.sin(angle)*lr;
      ctx.fillStyle=ly.saha?'#c46b5d':'#5c5040';
      ctx.font=(ly.saha?'bold 11':'9')+'px Microsoft YaHei';
      ctx.fillText((ly.saha?'★':'')+ly.n,lx+4,lyy+4);
      // Buddha name (smaller, offset)
      if(cosmoScale>0.9||ly.saha){
        ctx.fillStyle='#8a7a6a';ctx.font='8px Microsoft YaHei';
        ctx.fillText(ly.b,lx+4,lyy+14);
      }
    }
    // Store hit rect for this layer
    cosmoLayerRects.push({r1:r1,r2:r2,layer:ly});
  }

  // Indra's Net overlay
  if(cosmoShowNet&&cosmoScale>0.7){
    var sel=cosmoSel||COSMO_LAYERS[12];
    var selIdx=COSMO_LAYERS.indexOf(sel);
    var selR=minR+selIdx*layerH+layerH/2;
    for(var i3=0;i3<COSMO_LAYERS.length;i3++){
      if(i3===selIdx)continue;
      var tr=minR+i3*layerH+layerH/2;
      var a=(i3*Math.PI*2/20);
      ctx.beginPath();ctx.moveTo(cx+Math.cos(a)*selR,cy+Math.sin(a)*selR);
      ctx.lineTo(cx+Math.cos(a+0.2)*tr,cy+Math.sin(a+0.2)*tr);
      ctx.strokeStyle='rgba(125,154,110,0.12)';ctx.lineWidth=0.5;ctx.stroke();
    }
  }

  // Center: Vairocana
  var glow=ctx.createRadialGradient(cx,cy,0,cx,cy,minR);
  glow.addColorStop(0,'rgba(184,134,60,0.7)');glow.addColorStop(0.5,'rgba(184,134,60,0.2)');glow.addColorStop(1,'rgba(184,134,60,0)');
  ctx.fillStyle=glow;ctx.beginPath();ctx.arc(cx,cy,minR,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#b8863c';ctx.font='bold 12px Microsoft YaHei';
  ctx.fillText('毗卢遮那',cx-24,cy+4);
  // 卍 symbol
  ctx.fillStyle='#b8863c';ctx.font='bold 20px Microsoft YaHei';
  ctx.fillText('卍',cx-10,cy-14);
}

var cosmoLayerRects=[];
function handleCosmoHover(e){
  var canvas=document.getElementById("cosmo-canvas");if(!canvas)return;
  var rect=canvas.getBoundingClientRect();
  var mx=e.clientX-rect.left,my=e.clientY-rect.top;
  var cx=canvas.width/2,cy=canvas.height/2;
  var dist=Math.sqrt((mx-cx)*(mx-cx)+(my-cy)*(my-cy));
  var hit=null;
  for(var i=0;i<cosmoLayerRects.length;i++){
    var lr=cosmoLayerRects[i];
    if(dist>=lr.r1&&dist<=lr.r2){hit=lr;break;}
  }
  canvas.style.cursor=hit?'pointer':'default';
}
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
        info.innerHTML='<h3 style=color:var(--gold)>'+lr.layer.n+' <span style=font-size:0.7em;color:var(--text2)>第'+(i+1)+'重</span></h3>'
          +'<p>🙏 <b>佛</b>: '+lr.layer.b+'</p>'
          +(lr.layer.saha?'<p style=color:#c46b5d>★ 此即娑婆世界——我们所居之三千大千世界。释迦牟尼佛于此示现成道,而毗卢遮那佛为法身本源。</p>':'')
          +'<p style=font-size:0.75em;color:var(--text2)>据《华严经·华藏世界品》。一一世界海中,各有不可说佛刹微尘数世界围绕;一尘中见一切世界,重重无尽如因陀罗网。</p>';
      }
      drawCosmo();return;
    }
  }
}
function toggleCosmoNet(){cosmoShowNet=!cosmoShowNet;var btn=document.querySelector('.cosmo-btn');if(btn)btn.classList.toggle('active',cosmoShowNet);drawCosmo();}
