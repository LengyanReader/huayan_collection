// ═══ 华严其观 COSMOLOGY TAB ═══
var COSMO={scale:1,sel:null,net:true,all:false};
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
  var h='<style>.cm-btn{padding:3px 10px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text2);cursor:pointer;font-size:0.73em}.cm-btn.on{background:var(--gold);color:#fff}#cosmo-info{display:none;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin-top:8px;font-size:0.82em;line-height:1.7}</style>';
  h+='<div class=section style=border-left:4px solid var(--gold)><h2>🪷 华严其观 · 华藏世界海</h2><p style=font-size:0.82em;color:var(--text2)>据《华严经·华藏世界品》(T10n0279卷八~十)。十重风轮持香水海,海中出大莲华,二十重世界层层叠绕。毗卢遮那佛法身遍满。源: CBETA T10n0279</p></div>';
  h+='<button class="cm-btn on" onclick="COSMO.net=!COSMO.net;this.classList.toggle(\'on\',COSMO.net);drawCosmo()">🕸 因陀罗网</button> ';
  h+='<button class="cm-btn" onclick="COSMO.all=!COSMO.all;this.classList.toggle(\'on\',COSMO.all);drawCosmo()">📋 全部层名</button> ';
  h+='<span style=font-size:0.7em;color:var(--text2)>滚轮缩放 | 点击世界层查看详情 | 金色=娑婆世界</span>';
  h+='<div style=display:flex;gap:16px;flex-wrap:wrap><div style=flex:1.5;min-width:380px;text-align:center;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px><canvas id=cosmo-canvas style=max-width:100%></canvas></div><div style=flex:1;min-width:200px><div id=cosmo-info></div><div class=section style=margin-top:8px><h3 style=color:var(--gold)>📐 结构(从下至上)</h3><p style=font-size:0.78em;line-height:1.9>⑩~① 十重风轮<br>无边妙华光香水海<br>一切香摩尼宝庄严大莲华<br>第1~20重世界<br>★第13重: 娑婆世界(我们所在)<br>一一世界有微尘数佛刹围绕</p></div></div></div>';
  cv.innerHTML=h;
  var c=document.getElementById("cosmo-canvas");if(!c)return;
  c.addEventListener('wheel',function(e){e.preventDefault();COSMO.scale*=e.deltaY<0?1.12:0.89;COSMO.scale=Math.max(0.4,Math.min(3,COSMO.scale));drawCosmo();});
  c.addEventListener('click',clickCosmo);
  drawCosmo();
}

var _size=550,_minR=0,_layerH=0;
function drawCosmo(){
  var c=document.getElementById("cosmo-canvas");if(!c)return;
  _size=Math.min(550,c.parentElement.clientWidth-30);
  c.width=_size;c.height=_size;c.style.width=_size+'px';c.style.height=_size+'px';
  var ctx=c.getContext("2d"),cx=_size/2,cy=_size/2;
  ctx.clearRect(0,0,_size,_size);
  var bg=ctx.createRadialGradient(cx,cy,0,cx,cy,_size/2);
  bg.addColorStop(0,'#fefdf9');bg.addColorStop(1,'#e0d8c8');
  ctx.fillStyle=bg;ctx.fillRect(0,0,_size,_size);
  var maxR=_size*0.44*COSMO.scale; _minR=_size*0.04*COSMO.scale; _layerH=(maxR-_minR)/20;
  // Wind-wheels
  for(var i=0;i<10;i++){ctx.beginPath();ctx.arc(cx,cy,maxR+5+i*4*COSMO.scale,-0.8*Math.PI,0.8*Math.PI);ctx.strokeStyle='rgba(94,139,158,'+(0.06+i*0.01)+')';ctx.lineWidth=0.8;ctx.setLineDash([2,8]);ctx.stroke();ctx.setLineDash([]);}
  if(COSMO.scale>0.6){ctx.fillStyle='#8a7a6a';ctx.font='9px Microsoft YaHei';ctx.fillText('十重风轮',cx+maxR+10,cy);}
  // Ocean
  ctx.beginPath();ctx.arc(cx,cy,maxR,-0.9*Math.PI,-0.1*Math.PI);ctx.lineTo(cx+maxR*0.6,cy+maxR*0.3);ctx.closePath();
  var og=ctx.createLinearGradient(cx,cy-maxR,cx,cy+maxR);og.addColorStop(0,'rgba(94,139,158,0.02)');og.addColorStop(1,'rgba(70,120,150,0.12)');
  ctx.fillStyle=og;ctx.fill();
  if(COSMO.scale>0.6){ctx.fillStyle='#5e8b9e';ctx.font='bold 9px Microsoft YaHei';ctx.fillText('无边妙华光香水海',cx-45,cy+maxR-8);}
  // Light rays
  for(var r2=0;r2<24;r2++){var ra=(r2/24)*Math.PI*2;ctx.beginPath();ctx.moveTo(cx+Math.cos(ra)*_minR*2,cy+Math.sin(ra)*_minR*2);ctx.lineTo(cx+Math.cos(ra)*maxR*0.85,cy+Math.sin(ra)*maxR*0.85);ctx.strokeStyle='rgba(184,134,60,0.05)';ctx.lineWidth=0.5;ctx.stroke();}
  // 20 layers
  for(var i2=0;i2<COSMO_LAYERS.length;i2++){
    var ly=COSMO_LAYERS[i2],r1=_minR+i2*_layerH,r2=r1+_layerH;
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);ctx.beginPath();ctx.arc(cx,cy,r1,0,Math.PI*2);
    ctx.fillStyle='rgba(184,134,60,'+(ly.saha?0.2:(i2%2?0.04:0.07))+')';ctx.fill('evenodd');
    ctx.beginPath();ctx.arc(cx,cy,r2,0,Math.PI*2);
    ctx.strokeStyle=ly.saha?'#c46b5d':'rgba(184,134,60,'+(i2===0||i2===19?'0.5':'0.25')+')';ctx.lineWidth=ly.saha?2.5:0.6;ctx.stroke();
    var showL=COSMO.scale>0.7||ly.saha||COSMO.all;
    if(showL){var lr=(r1+r2)/2,a2=-Math.PI/2+i2*0.22,lx=cx+Math.cos(a2)*lr,ly2=cy+Math.sin(a2)*lr;ctx.fillStyle=ly.saha?'#c46b5d':'#5c5040';ctx.font=(ly.saha?'bold 10':'9')+'px Microsoft YaHei';ctx.fillText((ly.saha?'★':'')+(COSMO.all?(i2+1)+'.':'')+ly.n,lx+4,ly2+3);if(COSMO.scale>0.9||ly.saha){ctx.fillStyle='#8a7a6a';ctx.font='8px Microsoft YaHei';ctx.fillText(ly.b,lx+4,ly2+14);}}
  }
  // Indra's Net
  if(COSMO.net){var sel=COSMO.sel||COSMO_LAYERS[12],si=COSMO_LAYERS.indexOf(sel),sr=_minR+si*_layerH+_layerH/2;
    for(var i3=0;i3<COSMO_LAYERS.length;i3++){if(i3===si)continue;var tr=_minR+i3*_layerH+_layerH/2,a3=i3*Math.PI*2/20;
    ctx.beginPath();ctx.moveTo(cx+Math.cos(a3)*sr,cy+Math.sin(a3)*sr);ctx.lineTo(cx+Math.cos(a3+0.15)*tr,cy+Math.sin(a3+0.15)*tr);
    ctx.strokeStyle='rgba(125,154,110,0.12)';ctx.lineWidth=0.5;ctx.stroke();}}
  // Center Vairocana
  var hg=ctx.createRadialGradient(cx,cy,_minR*0.3,cx,cy,_minR*2.5);hg.addColorStop(0,'rgba(255,220,150,0.7)');hg.addColorStop(0.3,'rgba(184,134,60,0.3)');hg.addColorStop(1,'rgba(184,134,60,0)');
  ctx.fillStyle=hg;ctx.beginPath();ctx.arc(cx,cy,_minR*2.5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#b8863c';ctx.font='bold '+(16*COSMO.scale)+'px Microsoft YaHei';ctx.fillText('卍',cx-8,cy+4);
  ctx.fillStyle='#8a6040';ctx.font='bold 11px Microsoft YaHei';ctx.fillText('毗卢遮那佛',cx-30,cy-_minR*1.8);
  ctx.fillText('(Vairocana)',cx-28,cy-_minR*1.8+14);
  if(_layerH>0){var sR=_minR+12*_layerH+_layerH/2;ctx.fillStyle='#c46b5d';ctx.font='bold 9px Microsoft YaHei';ctx.fillText('▼ 娑婆(第13层)',cx-48,cy-sR-3);}
}

function clickCosmo(e){
  var c=document.getElementById("cosmo-canvas");if(!c||!_layerH)return;
  var r=c.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  var d=Math.sqrt((mx-c.width/2)*(mx-c.width/2)+(my-c.height/2)*(my-c.height/2));
  for(var i=0;i<COSMO_LAYERS.length;i++){
    var r1=_minR+i*_layerH,r2=r1+_layerH;
    if(d>=r1&&d<=r2){COSMO.sel=COSMO_LAYERS[i];showCosmoInfo(COSMO_LAYERS[i],i);drawCosmo();return;}
  }
  if(d<_minR*2){COSMO.sel=null;var inf=document.getElementById('cosmo-info');if(inf){inf.style.display='block';inf.innerHTML='<h3 style=color:var(--gold)>卍 毗卢遮那佛</h3><p>华严经根本教主。梵名Vairocana,意译<b>光明遍照</b>。法身遍一切处,为华藏世界海之本体。</p><p style=font-size:0.72em;color:var(--text2)>「佛身充满于法界,普现一切众生前;随缘赴感靡不周,而恒处此菩提座。」</p>';}drawCosmo();}
}
function showCosmoInfo(ly,i){
  var inf=document.getElementById('cosmo-info');if(!inf)return;
  inf.style.display='block';
  inf.innerHTML='<h3 style=color:var(--gold)>🪷 '+ly.n+' <span style=font-size:0.65em>第'+(i+1)+'重</span></h3>'
    +'<p>🙏 <b>住佛</b>: '+ly.b+'</p>'
    +(ly.saha?'<p style=color:#c46b5d>★ <b>娑婆世界</b>——我们所居之三千大千世界。释迦牟尼佛于此示现成道,毗卢遮那佛为此世界之法身本源。</p>':'')
    +'<p style=font-size:0.72em;color:var(--text2)>「一一世界海中,各有不可说佛刹微尘数世界围绕;一一微尘中,悉见一切世界;重重无尽,如因陀罗网。」—— 《华严经·华藏世界品》</p>';
}
