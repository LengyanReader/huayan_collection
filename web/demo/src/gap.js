// ═══ GAP TAB ═══
function renderGap(){
  var gv=document.getElementById("gap-view");if(!gv)return;
  var h="<h2 style=color:var(--gold)>📜 版本对照</h2><div class=section><table class=v-table><tr><th>版本</th><th>品目</th><th>卷/册</th><th>译者</th><th>年代</th></tr>";
  GAP.vs.forEach(function(v){h+="<tr><td>"+v.n+"</td><td style=font-weight:700;color:var(--gold)>"+v.c+"</td><td>"+v.v+"</td><td>"+v.t+"</td><td>"+v.p+"</td></tr>";});
  h+="</table></div>";
  var ds={A:{i:"🔴",l:"藏文独有品目",c:"#c46b5d",d:"汉文三译完全缺失"},B:{i:"🟠",l:"内容实质性参差",c:"#c8893e",d:"同名品内容有显著差异"},C:{i:"🟡",l:"结构/开合不同",c:"#a08020",d:"品目序号名称开合不同"},D:{i:"🔵",l:"品目级微小差异",c:"#5e8b9e",d:"个别段落不同"},E:{i:"🟢",l:"汉藏基本对应",c:"#7d9a6e",d:"32品大致一致"}};
  h+="<h2 style=color:var(--gold)>📊 差异分布 (藏文45品 vs 汉文39品)</h2><div class=section style=display:flex;gap:10px;flex-wrap:wrap>";
  ["A","B","C","D","E"].forEach(function(t){var d=ds[t];h+="<span style=flex:1;min-width:130px;background:var(--card);border-radius:10px;padding:14px;text-align:center;border:1px solid var(--line);border-left:3px solid "+d.c+"><div style=font-size:1.3em>"+d.i+"</div><div style=font-size:2em;font-weight:700;color:"+d.c+">"+(GAP.sm[t]||0)+"</div><div style=font-weight:600>"+d.l+"</div><div style=font-size:0.8em;color:var(--text2)>"+d.d+"</div></span>";});
  h+="</div>";
  h+="<h2 style=color:var(--gold)>📋 逐品差异详情</h2><div class=section><table class=v-table><tr><th>藏文#</th><th>八十华严#</th><th>品名</th><th>类型</th><th>差异说明</th></tr>";
  GAP.cs.forEach(function(ch){var b="badge b"+ch.tp;h+="<tr><td>"+(ch.bo||"—")+"</td><td>"+(ch.z80||"<span class=miss>✗</span>")+"</td><td>"+ch.ti+(ch.sa?" <span style=font-size:0.8em;color:var(--text2)>"+ch.sa+"</span>":"")+"</td><td><span class='"+b+"'>"+ch.tp+"</span></td><td style=font-size:0.8em>"+(ch.sm||"")+"</td></tr>";});
  h+="</table></div>";
  h+="<h2 style=color:var(--gold)>🗺 对译优先级</h2><div class=section><p><b style=color:#c46b5d>P0</b> Ch.11 如来华严品 · Ch.28 普贤宣说品 — 汉文全缺</p><p><b style=color:#c8893e>P1</b> Ch.27 十地品 · Ch.40 离世间品 — 内容参差</p></div>";
  GAP.wn.forEach(function(w){h+="<div style=background:rgba(196,107,93,0.05);border:1px solid rgba(196,107,93,0.2);border-radius:8px;padding:8px 12px;margin:4px 0;font-size:0.8em;color:var(--red)>"+w+"</div>";});
  gv.innerHTML=h;
}

