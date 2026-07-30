// ═══ 华藏世界海 COSMOLOGY TAB ═══
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
  var h='<style>.cosmo-btn{padding:3px 10px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.73em}.cosmo-btn.active{background:var(--gold);color:#fff;border-color:var(--gold)}#cosmo-info{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin-top:8px;font-size:0.82em;line-height:1.7;display:none}</style>';
  h+='<div class=section style=border-left:4px solid var(--gold)><h2>🪷 华藏世界海</h2><p style=font-size:0.82em;color:var(--text2)>据《华严经·华藏世界品》(T10n0279),十重风轮持香水海,海中出大莲华,共<b>二十重世界</b>。毗卢遮那佛法身遍满。源: CBETA T10n0279</p></div>';
  h+='<button class="cosmo-btn active" onclick="cosmoShowNet=!cosmoShowNet;this.classList.toggle(\'active\',cosmoShowNet);drawCosmo()">🕸 因陀罗网</button> ';
  h+='<button class="cosmo-btn" onclick="cosmoShowAll=!cosmoShowAll;this.classList.toggle(\'active\',cosmoShowAll);drawCosmo()">📋 全部层名</button> ';
  h+='<span style=font-size:0.7em;color:var(--text2)>滚轮缩放 | 点击世界层</span>';
  h+='<div style=display:flex;gap:16px;flex-wrap:wrap><div style=flex:1.5;min-width:380px;text-align:center;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px><canvas id=cosmo-canvas style=max-width:100%></canvas></div><div style=flex:1;min-width:200px><div id=cosmo-info></div><div class=section style=margin-top:8px><h3 style=color:var(--gold);font-size:0.9em>📐 结构(从下至上)</h3><p style=font-size:0.78em;line-height:1.9>⑩~① 十重风轮<br>无边妙华光香水海<br>大莲华<br>第1~20重世界<br>★第13重: 娑婆世界</p></div></div></div>';
  cv.innerHTML=h;
  var c=document.getElementById("cosmo-canvas");if(!c)return;
  c.addEventListener('wheel',function(e){e.preventDefault();cosmoScale*=e.deltaY<0?1.12:0.89;cosmoScale=Math.max(0.4,Math.min(3,cosmoScale));drawCosmo();});
  c.addEventListener('click',function(e){var r=c.getBoundingClientRect();var mx=e.clientX-r.left,my=e.clientY-r.top;var cx=c.width/2,cy=c.height/2;var d=Math.sqrt((mx-cx)*(mx-cx)+(my-cy)*(my-cy));var s=size*0.04*cosmoScale,lh=(size*0.44*cosmoScale-s)/20;for(var i=0;i<COSMO_LAYERS.length;i++){var r1=s+i*lh,r2=r1+lh;if(d>=r1&&d<=r2){cosmoSel=COSMO_LAYERS[i];var inf=document.getElementById('cosmo-info');if(inf){inf.style.display='block';inf.innerHTML='<h3 style=color:var(--gold)>'+COSMO_LAYERS[i].n+' 第'+(i+1)+'重</h3><p>佛: '+COSMO_LAYERS[i].b+(COSMO_LAYERS[i].saha?'</p><p style=color:#c46b5d>★娑婆世界——我们所居</p>':'</p>');}drawCosmo();return;}}drawCosmo();});
  drawCosmo();
}

var size=550;
function drawCosmo(){
  var c=document.getElementById("cosmo-canvas");if(!c)return;
  size=Math.min(550,c.parentElement.clientWidth-30);
  c.width=size;c.height=size;c.style.width=size+'px';c.style.height=size+'px';
  var ctx=c.getContext("2d"),cx=size/2,cy=size/2;
  ctx.clearRect(0,0,size,size);
  var bg=ctx.createRadialGradient(cx,cy,0,cx,cy,size/2);
  bg.addColorStop(0,'#fefdf9');bg.addColorStop(1,'#e0d8c8');
  ctx.fillStyle=bg;ctx.fillRect(0,0,size,size);
  var maxR=size*0.44*cosmoScale,minR=size*0.04*cosmoScale,layerH=(maxR-minR)/20;
  // Wind-wheels
  for(var i=0;i<10;i++){ctx.beginPath();ctx.arc(cx,cy,maxR+5+i*4*cosmoScale,-0.8*Math.PI,0.8*Math.PI);ctx.strokeStyle='rgba(94,139,158,'+(0.06+i*0.01)+')';ctx.lineWidth=0.8;ctx.setLineDash([2,8]);ctx.stroke();ctx.setLineDash([]);}
  // Ocean
  ctx.beginPath();ctx.arc(cx,cy,maxR,-0.9*Math.PI,-0.1*Math.PI);ctx.lineTo(cx+maxR*0.6,cy+maxR*0.3);ctx.closePath();
  var og=ctx.createLinearGradient(cx,cy-maxR,cx,cy+maxR);og.addColorStop(0,'rgba(94,139,158,0.02)');og.addColorStop(1,'rgba(70,120,150,0.12)');
  ctx.fillStyle=og;ctx.fill();
  // Light rays
  for(var r=0;r<24;r++){var ra=(r/24)*Math.PI*2;ctx.beginPath();ctx.moveTo(cx+Math.cos(ra)*minR*2,cy+Math.sin(ra)*minR*2);ctx.lineTo(cx+Math.cos(ra)*maxR*0.85,cy+Math.sin(ra)*maxR*0.85);ctx.strokeStyle='rgba(184,134,60,0.05)';ctx.lineWidth=0.5;ctx.stroke();}
  // 20 layers
  for(var i2=0;i2<COSMO_LAYERS.length;i2++){
    var ly=COSMO_LAYERS[i2],r1=minR+i2*layerH,r2=r1+layerH;
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);ctx.beginPath();ctx.arc(cx,cy,r1,0,Math.PI*2);
    ctx.fillStyle='rgba(184,134,60,'+(ly.saha?0.2:(i2%2?0.04:0.07))+')';ctx.fill('evenodd');
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);
    ctx.strokeStyle=ly.saha?'#c46b5d':'rgba(184,134,60,'+(i2===0||i2===19?'0.5':'0.25')+')';ctx.lineWidth=ly.saha?2.5:0.6;ctx.stroke();
    var showL=cosmoScale>0.7||ly.saha||cosmoShowAll;
    if(showL){var lr=(r1+r2)/2,a2=-Math.PI/2+i2*0.22,lx=cx+Math.cos(a2)*lr,lyy=cy+Math.sin(a2)*lr;ctx.fillStyle=ly.saha?'#c46b5d':'#5c5040';ctx.font=(ly.saha?'bold 10':'9')+'px Microsoft YaHei';ctx.fillText((ly.saha?'★':'')+(cosmoShowAll?(i2+1)+'.':'')+ly.n,lx+5,lyy+3);if(cosmoScale>0.9||ly.saha){ctx.fillStyle='#8a7a6a';ctx.font='8px Microsoft YaHei';ctx.fillText(ly.b,lx+5,lyy+14);}}
  }
  // Indra's Net
  if(cosmoShowNet){var sel=cosmoSel||COSMO_LAYERS[12],si=COSMO_LAYERS.indexOf(sel),sr=minR+si*layerH+layerH/2;for(var i3=0;i3<COSMO_LAYERS.length;i3++){if(i3===si)continue;var tr=minR+i3*layerH+layerH/2,a3=i3*Math.PI*2/20;ctx.beginPath();ctx.moveTo(cx+Math.cos(a3)*sr,cy+Math.sin(a3)*sr);ctx.lineTo(cx+Math.cos(a3+0.15)*tr,cy+Math.sin(a3+0.15)*tr);ctx.strokeStyle='rgba(125,154,110,0.12)';ctx.lineWidth=0.5;ctx.stroke();}}
  // Center: Vairocana
  var hg=ctx.createRadialGradient(cx,cy,minR*0.3,cx,cy,minR*2.5);hg.addColorStop(0,'rgba(255,220,150,0.7)');hg.addColorStop(0.3,'rgba(184,134,60,0.3)');hg.addColorStop(1,'rgba(184,134,60,0)');ctx.fillStyle=hg;ctx.beginPath();ctx.arc(cx,cy,minR*2.5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#b8863c';ctx.font='bold '+Math.max(12,16*cosmoScale)+'px Microsoft YaHei';ctx.fillText('卍',cx-8,cy+4);
  ctx.fillStyle='#8a6040';ctx.font='bold 11px Microsoft YaHei';ctx.fillText('毗卢遮那佛',cx-30,cy-minR*1.8);ctx.fillText('(Vairocana)',cx-28,cy-minR*1.8+14);
  var sR=minR+12*layerH+layerH/2;ctx.fillStyle='#c46b5d';ctx.font='bold 9px Microsoft YaHei';ctx.fillText('▼ 娑婆世界(第13层)',cx-46,cy-sR-3);
}
