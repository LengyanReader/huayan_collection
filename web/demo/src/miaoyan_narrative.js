/* ═══════════════════════════════════════════════════════════════════════
 * renderMiaoyanNarrative —— 世主妙严品·叙事动画播放器
 * 数据源（唯一真源，零硬编码内容）：
 *   data/narrative/miaoyan_narrative.yaml → build.py → var MIAOYAN_NARR
 *   member_count / member_classes 之真源为 data/translation/miaoyan_assembly.yaml
 *   （六环 member_count 之和 == assembly.metrics.named_total == 414）
 * 绘制原则：
 *   ① 环上【一点 = 一类】，故全图共 40 点 == 40 类；员数另以文字标注，
 *      不以点数冒充人数（微尘刹海之广不可尽言，仅取列次为空间意象）。
 *   ② 一切几何（半径/层序/配色/时长/错峰/缓动/旁白）皆自 MIAOYAN_NARR 读出。
 *   ③ 旁白 ref 与 uncertainty 原样透出，不隐藏存疑。
 * ═══════════════════════════════════════════════════════════════════════ */
var MiaoyanNarrative = (function(){
  'use strict';

  function clamp(v,a,b){ return v<a?a:(v>b?b:v); }
  function easeInOut(p){ return p<0.5 ? 2*p*p : 1-Math.pow(-2*p+2,2)/2; }
  function easeOut(p){ return 1-Math.pow(1-p,3); }

  /* 由 beats 之 actions 推导「揭示事件」：每件几何事件带起止进度 */
  function deriveEvents(d){
    var beats = d.beats, ev = [], t0 = 0;
    for(var i=0;i<beats.length;i++){
      var b = beats[i];
      var dur = Math.max(0.001,(b.time_end_s - b.time_start_s));
      var acts = b.actions||[];
      for(var j=0;j<acts.length;j++){
        var a = acts[j];
        var delay = (a.delay_ms||0)/1000;
        var adur  = (a.dur_ms||d.visual_style.duration_base_ms||900)/1000;
        var s = clamp(delay/dur, 0, 0.9);
        var e = clamp((delay+adur)/dur, s+0.02, 1);
        ev.push({beat:i, kind:a.type, target:a.target||null, ring:a.ring||null,
                 zh:a.zh||'', en:a.en||'', s:s, e:e});
      }
      t0 += dur;
    }
    return ev;
  }

  /* 环之 splits（上层欲界/色界分列，见 YAML r5.splits）*/
  function ringById(space, id){
    var rs = space.rings||[];
    for(var i=0;i<rs.length;i++) if(rs[i].id===id) return rs[i];
    return null;
  }

  function render(containerId){
    var d = (typeof MIAOYAN_NARR!=='undefined') ? MIAOYAN_NARR : null;
    if(!d || !d.beats || !d.beats.length) return false;
    var el = document.querySelector(containerId);
    if(!el) return false;

    var beats = d.beats.slice().sort(function(a,b){ return (a.order||0)-(b.order||0); });
    var space = d.space||{}, rings = space.rings||[], vs = d.visual_style||{}, pal = vs.palette||{};
    var bg   = space.background||{};
    var ev   = deriveEvents(d);
    var total = beats[beats.length-1].time_end_s || 1;
    var W=960, H=620, CX=W/2, CY=H/2;
    var maxR = 0;
    for(var q=0;q<rings.length;q++) maxR = Math.max(maxR, rings[q].r||0);
    var SCALE = (Math.min(W,H)/2 - 46) / (maxR||1);

    /* ── DOM ─────────────────────────────────────────── */
    var h='';
    /* h2 置于 section 之外，充当 _foldDoc 的折叠标题：其相邻兄弟 <section> 会被裹入
       .secfold-body 并默认收起。若标题嵌在 section 内，wrapLevel 只认直接子级、无从包裹，
       折叠便形同虚设——叙事动画会一直铺在页面底部。 */
    h += '<h2>📽 '+(d.meta&&d.meta.title_zh?d.meta.title_zh:'叙事动画')
       + (d.meta&&d.meta.title_en?'<span class="en-line" style="font-size:0.62em;color:var(--text2);margin-left:8px">📖 '+d.meta.title_en+'</span>':'')
       + '</h2>';
    h += '<section class="miaoyan-narr" data-chrome="1">';

    if(d.meta && d.meta.note_zh){
      h += '<div class="bi-note">'+d.meta.note_zh+'</div>';
    }
    if(d.meta && d.meta.note_en){
      h += '<div class="en-line" style="font-size:0.8em;color:var(--text2);margin:4px 0 10px">'+d.meta.note_en+'</div>';
    }

    /* 控制条 */
    h += '<div class="mn-ctrl">';
    h += '<button class="f-nav-btn mn-play" type="button">▶ 播放</button>';
    h += '<button class="f-nav-btn mn-prev" type="button" title="上一拍">⏮ 上一拍</button>';
    h += '<button class="f-nav-btn mn-next" type="button" title="下一拍">⏭ 下一拍</button>';
    h += '<label class="mn-rate">速度 <select class="mn-speed">'
       + '<option value="0.5">0.5×</option><option value="1" selected>1×</option>'
       + '<option value="1.5">1.5×</option><option value="2">2×</option></select></label>';
    h += '<span class="mn-time"><span class="mn-cur">0.0</span> / '+total.toFixed(1)+' s</span>';
    h += '</div>';
    h += '<input class="mn-seek" type="range" min="0" max="1000" value="0" step="1" aria-label="播放进度">';

    /* 图层开关 */
    h += '<div class="mn-layers">';
    h += '<label><input type="checkbox" class="mn-lg" data-k="grid" checked> 背景光网</label>';
    h += '<label><input type="checkbox" class="mn-lg" data-k="dots" checked> 环上会众点</label>';
    h += '<label><input type="checkbox" class="mn-lg" data-k="labels" checked> 环名</label>';
    h += '<label><input type="checkbox" class="mn-lg" data-k="en" checked> 英文标签</label>';
    h += '</div>';

    h += '<canvas class="mn-cv" width="'+W+'" height="'+H+'" role="img" aria-label="'+((d.meta&&d.meta.title_zh)||'会众')+'叙事动画"></canvas>';

    /* 拍条 */
    h += '<div class="mn-beats">';
    for(var i=0;i<beats.length;i++){
      h += '<button class="mn-chip'+(i===0?' on':'')+'" data-i="'+i+'" type="button" title="'+beats[i].title_zh+'">'
         + beats[i].title_zh.replace(/^B\d+ · /,'') + '</button>';
    }
    h += '</div>';

    /* 旁白 */
    h += '<div class="mn-narr" aria-live="polite">'
       + '<div class="mn-nt"></div><div class="mn-nz"></div>'
       + '<div class="en-line mn-ne" style="font-size:0.86em;color:var(--text2)"></div>'
       + '<div class="mn-nmeta"></div></div>';

    /* 存疑声明 */
    h += '<div style="margin-top:8px;font-size:0.76em;color:var(--text2)">'
       + '⚠︎ 本动画依会众列次重组为叙事节拍，用以表达「次第出现」与「时空圆融」之意向，'
       + '<b>不等同于逐颂逐句的演绎</b>；节拍边界与时序多为〔待核〕，见每拍出处与存疑标记。'
       + '</div>';

    /* 数据来源与口径 */
    if(d.meta && d.meta.sources && d.meta.sources.length){
      h += '<div style="margin-top:6px;font-size:0.74em;color:var(--text2)">📎 底本：';
      for(var s=0;s<d.meta.sources.length;s++){
        var sc=d.meta.sources[s];
        h += (s?' · ':'') + '<a href="'+sc.url+'" target="_blank" rel="noopener" style="color:var(--blue)">'+sc.label+'</a>';
      }
      h += '</div>';
    }
    var cal = bg.calibration, tn = bg.token_note;
    if(cal){
      h += '<div style="margin-top:4px;font-size:0.72em;color:var(--text2)">🧮 '+cal+'</div>';
    }
    if(tn){
      h += '<div style="font-size:0.72em;color:var(--text2)">🔵 '+tn+'</div>';
    }
    h += '</section>';
    el.innerHTML = h;

    /* ── 状态 ────────────────────────────────────────── */
    var cv = el.querySelector('.mn-cv');
    var cx = cv.getContext('2d');
    var ui = {
      play: el.querySelector('.mn-play'),
      seek: el.querySelector('.mn-seek'),
      spd:  el.querySelector('.mn-speed'),
      cur:  el.querySelector('.mn-cur'),
      t:    el.querySelector('.mn-nt'),
      z:    el.querySelector('.mn-nz'),
      e:    el.querySelector('.mn-ne'),
      meta: el.querySelector('.mn-nmeta')
    };
    var S = { playing:false, bi:0, p:0, speed:1, last:0,
              layer:{grid:true, dots:true, labels:true, en:true} };

    function clock(){ return beats[S.bi].time_start_s + S.p*(beats[S.bi].time_end_s-beats[S.bi].time_start_s); }

    function setBeat(i, keepP){
      S.bi = clamp(i, 0, beats.length-1);
      if(!keepP) S.p = 0;
      var b = beats[S.bi];
      ui.t.textContent = b.title_zh + (b.title_en? '  ·  '+b.title_en : '');
      ui.z.innerHTML = '<b>'+(b.narration_zh||'')+'</b>';
      ui.e.textContent = b.narration_en||'';
      var mm = [];
      if(b.narration_ref) mm.push('📎 '+b.narration_ref);
      if(b.uncertainty && b.uncertainty.length) mm.push('⚠︎ 存疑：'+b.uncertainty.join('、'));
      ui.meta.innerHTML = mm.join('<br>');
      var chips = el.querySelectorAll('.mn-chip');
      for(var k=0;k<chips.length;k++) chips[k].className = 'mn-chip'+(k===S.bi?' on':'');
    }

    /* ── 绘制 ────────────────────────────────────────── */
    function ringColor(rg){
      /* 环色优先取数据所给 rg.color；否则退回世主妙严品旧环位映射，末位取 deities 色 */
      if(rg && rg.color) return rg.color;
      var rid = (rg && rg.id) || rg;
      return {r1:pal.bodhisattva, r2:pal.vajra, r3:pal.deities,
              r4:pal.eight, r5:pal.desire}[rid] || pal.deities;
    }
    function progFor(evs){
      /* 返回 kind|ring|target → 0..1 进度（依当前拍）*/
      var m = {};
      for(var i=0;i<evs.length;i++){
        var e = evs[i];
        if(e.beat>S.bi) continue;
        var p = (e.beat<S.bi) ? 1 : clamp((S.p-e.s)/(e.e-e.s), 0, 1);
        m[e.kind+'|'+e.ring+'|'+e.target] = p;
      }
      return m;
    }
    function P(m,key){ return m[key]||0; }

    function draw(){
      var t = clock();
      cx.clearRect(0,0,W,H);
      /* 背景 */
      cx.fillStyle = pal.bg||'#0f1419';
      cx.fillRect(0,0,W,H);

      /* 相机：自上一拍缓入本拍 */
      var prev = beats[Math.max(0,S.bi-1)].camera||{}, cur = beats[S.bi].camera||{};
      var ez = easeInOut(S.p);
      var zoom  = (prev.zoom  ||1) + ((cur.zoom  ||1)-(prev.zoom  ||1))*ez;
      var panx  = (prev.pan_x ||0) + ((cur.pan_x ||0)-(prev.pan_x ||0))*ez;
      var pany  = (prev.pan_y ||0) + ((cur.pan_y ||0)-(prev.pan_y ||0))*ez;

      var M = progFor(ev);

      /* 背景光网 */
      var gridP = Math.max(P(M,'grid_fade_in|null|bg-mandala'), P(M,'adorn|null|bg-mandala'));
      if(bg.mandala_grid && S.layer.grid && gridP>0){
        cx.save();
        cx.globalAlpha = (bg.opacity||0.12) * gridP;
        cx.strokeStyle = pal.light||'#f5e9b8';
        cx.lineWidth = 1;
        var g = 64;
        for(var x=-W;x<W*2;x+=g){ cx.beginPath(); cx.moveTo(x,0); cx.lineTo(x+W,H); cx.stroke(); }
        for(var y=-H;y<H*2;y+=g){ cx.beginPath(); cx.moveTo(0,y); cx.lineTo(W,y+g); cx.stroke(); }
        cx.restore();
      }
      /* 世界海涟漪 */
      var ripP = P(M,'ripple|null|bg-worldsea');
      if(bg.worldsea && ripP>0){
        cx.save();
        cx.strokeStyle = pal.light||'#f5e9b8';
        for(var k2=0;k2<5;k2++){
          var ph = clamp(ripP*1.6 - k2*0.12, 0, 1);
          if(ph<=0) continue;
          cx.globalAlpha = 0.30*(1-easeOut(ph))*gridAlpha(gridP);
          cx.lineWidth = 1.6;
          cx.beginPath();
          cx.arc(CX, CY, (maxR+30+k2*26)*SCALE*zoom + (1-easeOut(ph))*26, 0, Math.PI*2);
          cx.stroke();
        }
        cx.restore();
      }

      cx.save();
      cx.translate(CX+panx, CY+pany);
      cx.scale(zoom, zoom);
      cx.translate(-CX, -CY);

      /* 各环 */
      for(var ri=0;ri<rings.length;ri++){
        var rg = rings[ri];
        var rp = ringProgress(rg.id, M);
        if(rp<=0) continue;
        var R = (rg.r||0)*SCALE;
        cx.save();
        cx.globalAlpha = rp;
        cx.strokeStyle = ringColor(rg);
        cx.lineWidth = 1.2;
        cx.beginPath(); cx.arc(CX,CY,R,0,Math.PI*2); cx.stroke();
        /* 环名 */
        if(S.layer.labels){
          cx.globalAlpha = rp*0.92;
          cx.fillStyle = ringColor(rg);
          cx.font = '12px "Noto Serif SC", serif';
          cx.textAlign = 'left'; cx.textBaseline = 'middle';
          var ang = -Math.PI*0.78;
          var lx = CX + Math.cos(ang)*R, ly = CY + Math.sin(ang)*R;
          var zh = rg.label_zh||'', en = S.layer.en? (rg.label_en||'') : '';
          cx.fillText(zh, lx+6, ly-6);
          if(en){ cx.globalAlpha = rp*0.6; cx.font='10px sans-serif'; cx.fillText(en, lx+6, ly+7); }
          /* 员数标注（一点=一类，人数另标）*/
          cx.globalAlpha = rp*0.75; cx.font='10px sans-serif'; cx.fillStyle=pal.light||'#f5e9b8';
          cx.fillText((rg.member_classes||'?')+' 类／'+(rg.member_count||'?')+' 名', lx+6, ly+19);
        }
        /* 会众点：一点 = 一类 */
        if(S.layer.dots && rg.member_classes){
          var nc = rg.member_classes;
          for(var d2=0; d2<nc; d2++){
            var stag = (nc<=1) ? 0 : (d2/nc)*0.55;
            var dp = clamp((rp-stag)/Math.max(0.2,0.45-stag), 0, 1);
            if(dp<=0) continue;
            var a2 = -Math.PI/2 + (d2/nc)*Math.PI*2;
            var px = CX + Math.cos(a2)*R, py = CY + Math.sin(a2)*R;
            var rr = (nc>12? 3.2 : 4.6) * easeOut(dp);
            /* 上层环分欲界/色界两半着色 */
            var col = ringColor(rg);
            if(rg.splits && rg.splits.length){
              var rel = d2/nc;
              col = (rel < (rg.splits[0].classes||1)/nc) ? pal.desire : pal.form;
            }
            cx.globalAlpha = 0.35 + 0.6*dp;
            cx.fillStyle = col;
            cx.beginPath(); cx.arc(px,py,rr,0,Math.PI*2); cx.fill();
          }
        }
        cx.restore();
      }

      /* 中心法界座 */
      var cP = Math.max(P(M,'awaken|null|center-buddha'), P(M,'breathe|null|center-buddha'), P(M,'gesture|null|r1')>0?P(M,'gesture|null|r1'):0);
      if(cP>0){
        var br = P(M,'breathe|null|center-buddha');
        var pulse = br>0 ? 1 + 0.06*Math.sin(t*(2*Math.PI/((vs.breath_ms||1200)/1000)))*br : 1;
        var R0 = 34*pulse*easeOut(cP);
        var gr = cx.createRadialGradient(CX,CY,0,CX,CY,Math.max(R0,1));
        gr.addColorStop(0, pal.center||'#f2d77c');
        gr.addColorStop(1, 'rgba(242,215,124,0)');
        cx.globalAlpha = 0.55*cP;
        cx.fillStyle = gr;
        cx.beginPath(); cx.arc(CX,CY,R0*2.6,0,Math.PI*2); cx.fill();
        cx.globalAlpha = cP;
        cx.fillStyle = pal.center||'#f2d77c';
        cx.beginPath(); cx.arc(CX,CY,R0,0,Math.PI*2); cx.fill();
        if(S.layer.labels){
          cx.globalAlpha = cP*0.95; cx.fillStyle=pal.light||'#f5e9b8';
          cx.font='12px "Noto Serif SC", serif'; cx.textAlign='center';
          cx.fillText((space.center&&space.center.label_zh)||'法界座（世主）', CX, CY+R0+20);
        }
      }
      /* 放光 */
      var rad = P(M,'radiate|null|center-buddha');
      if(rad>0){
        cx.save();
        cx.globalAlpha = 0.30*rad;
        cx.strokeStyle = pal.light||'#f5e9b8';
        cx.lineWidth = 1.4;
        for(var n2=0;n2<24;n2++){
          var a3 = n2/24*Math.PI*2 + t*0.15;
          cx.beginPath();
          cx.moveTo(CX+Math.cos(a3)*40, CY+Math.sin(a3)*40);
          cx.lineTo(CX+Math.cos(a3)*maxR*SCALE*zoom, CY+Math.sin(a3)*maxR*SCALE*zoom);
          cx.stroke();
        }
        cx.restore();
      }
      cx.restore();

      ui.cur.textContent = t.toFixed(1);
      if(!S.playing) ui.seek.value = Math.round((t/total)*1000);
    }
    function gridAlpha(p){ return 0.4+0.6*p; }

    function ringProgress(rid, M){
      var p = 0;
      var a = P(M,'emerge_spiral|'+rid+'|null'), b = P(M,'emerge_ring|'+rid+'|null'), c = P(M,'emerge_up|'+rid+'|null');
      return Math.max(a,b,c);
    }

    /* ── 时钟 ────────────────────────────────────────── */
    function frame(ts){
      if(S.playing){
        if(!S.last) S.last = ts;
        var dt = Math.min(0.1,(ts-S.last)/1000);
        S.last = ts;
        var dur = beats[S.bi].time_end_s - beats[S.bi].time_start_s;
        S.p += (dt*S.speed)/dur;
        if(S.p>=1){
          if(S.bi < beats.length-1){ S.bi++; S.p = 0; setBeat(S.bi); }
          else { S.p = 1; pause(); }
        }
        ui.seek.value = Math.round((clock()/total)*1000);
      } else { S.last = 0; }
      draw();
      requestAnimationFrame(frame);
    }

    function play(){ if(S.bi===beats.length-1 && S.p>=1){ S.bi=0; S.p=0; setBeat(0);} S.playing=true; ui.play.innerHTML='⏸ 暂停'; S.last=0; }
    function pause(){ S.playing=false; ui.play.innerHTML='▶ 播放'; S.last=0; }
    function toggle(){ S.playing? pause() : play(); }
    function seekTo(frac){
      var tt = clamp(frac,0,1)*total, acc=0;
      for(var i=0;i<beats.length;i++){
        var d2 = beats[i].time_end_s - beats[i].time_start_s;
        if(tt <= acc+d2 || i===beats.length-1){
          S.bi=i; S.p = clamp((tt-acc)/d2,0,1); break;
        }
        acc += d2;
      }
      setBeat(S.bi, true);
    }

    /* ── 事件绑定 ────────────────────────────────────── */
    ui.play.addEventListener('click', toggle);
    el.querySelector('.mn-prev').addEventListener('click', function(){
      if(S.p>0.02){ S.p=0; } else { setBeat(S.bi-1); } setBeat(S.bi,true); pause();
    });
    el.querySelector('.mn-next').addEventListener('click', function(){
      if(S.bi<beats.length-1){ setBeat(S.bi+1); } pause();
    });
    ui.spd.addEventListener('change', function(){ S.speed = parseFloat(ui.spd.value)||1; });
    ui.seek.addEventListener('input', function(){ pause(); seekTo(ui.seek.value/1000); });
    var lgs = el.querySelectorAll('.mn-lg');
    for(var gi=0; gi<lgs.length; gi++){
      lgs[gi].addEventListener('change', function(){
        S.layer[this.getAttribute('data-k')] = this.checked; draw();
      });
    }
    var chips = el.querySelectorAll('.mn-chip');
    for(var ci=0; ci<chips.length; ci++){
      chips[ci].addEventListener('click', function(){
        setBeat(parseInt(this.getAttribute('data-i'),10)); pause();
      });
    }

    setBeat(0);
    draw();
    requestAnimationFrame(frame);
    return true;
  }

  return { render: render };
})();

/* 兼容既有调用签名：renderMiaoyanNarrative('#article-narrative') */
function renderMiaoyanNarrative(containerId){
  return MiaoyanNarrative.render(containerId);
}