// ═══ PRACTICE TAB ═══
function renderPractice(){
  var pv=document.getElementById("practice-view");if(!pv)return;
  var h="";
  h+="<style>.wu-door{cursor:pointer;padding:10px 14px;margin:4px 0;background:var(--card);border:1px solid var(--line);border-radius:8px;transition:all 0.2s}.wu-door:hover{border-color:var(--gold-l)}.wu-door .arrow{display:inline-block;transition:transform 0.2s;margin-right:6px}.wu-door.open .arrow{transform:rotate(90deg)}.wu-door .body{display:none;margin-top:8px;padding-top:8px;border-top:1px solid var(--line);font-size:0.9em;line-height:1.8;color:var(--text2)}.wu-door.open .body{display:block}.wu-door .ttl{font-weight:600;color:var(--gold);font-size:1em}</style>";

  h+="<div class=section><h2>🧘 华严行法 — 修行蓝图</h2><p style=line-height:1.8>参考大华严寺海云继梦和上所立 <b>普贤乘华严宗</b> 修行体系。以华严禅法为核心，透过<b>心法工程</b>止住安心、令真心起作用。</p>";

  h+="<div style='display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin:12px 0'>";
  h+="<div style='flex:1;min-width:180px;background:rgba(184,134,60,0.08);border:1px solid #b8863c;border-radius:10px;padding:16px;text-align:center'>";
  h+="<div style='font-size:1.05em;font-weight:700;color:#b8863c;margin-bottom:4px'>资粮道</div>";
  h+="<div style='font-size:0.8em;color:#8a7060'>发心工程</div><div style='font-size:0.7em;color:#a09080;margin-top:4px'>三摩呬多 samāhita</div></div>";
  h+="<div style='display:flex;align-items:center;color:#c0b098;font-size:1.2em'>→</div>";
  h+="<div style='flex:1;min-width:180px;background:rgba(94,139,158,0.08);border:1px solid #5e8b9e;border-radius:10px;padding:16px;text-align:center'>";
  h+="<div style='font-size:1.05em;font-weight:700;color:#5e8b9e;margin-bottom:4px'>前行·正行</div>";
  h+="<div style='font-size:0.8em;color:#6a7060'>内摄·等持</div><div style='font-size:0.7em;color:#a09080;margin-top:4px'>三摩钵底 samāpatti</div></div>";
  h+="<div style='display:flex;align-items:center;color:#c0b098;font-size:1.2em'>→</div>";
  h+="<div style='flex:1;min-width:180px;background:rgba(196,107,93,0.08);border:1px solid #c46b5d;border-radius:10px;padding:16px;text-align:center'>";
  h+="<div style='font-size:1.05em;font-weight:700;color:#c46b5d;margin-bottom:4px'>三摩地</div>";
  h+="<div style='font-size:0.8em;color:#8a6060'>海印三昧</div><div style='font-size:0.7em;color:#a09080;margin-top:4px'>三摩地 samādhi</div></div>";
  h+="</div></div>";

  h+="<div class=section><h2>📐 修行三阶段</h2>";
  h+="<div class=stage-box><b>一、资粮道 — 发心工程</b><br>三门必修: 人格健康+出离心+菩提心。技术面: 纯化禅(动→静)→象限转移→瞬间定。工程面: 心性培养+戒律基础。</div>";
  h+="<div class=stage-box><b>二、前行 — 内摄工程（界内定）</b><br>核心: 安那般那数息观(数·随·止·观·还·净)。四种观法: 唯心识观→真如实现→毗婆舍那→奢摩他。</div>";
  h+="<div class=stage-box><b>三、正行 — 等持工程（界外定）</b><br>前半程三摩呬多→后半程三摩钵底→究竟三摩地。依杜顺法界三观，透过海印三昧呈现华严境界。</div>";
  h+="</div>";

  h+="<div class=section><h2>📜 五教止观（杜顺和尚·点击展开）</h2>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>一、法有我无门（小乘教）</span><div class=body>破除「我执」，体悟我空，但法执犹存。一切法因缘和合，因果历然。对应四禅八定中的初、二、三、四禅。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>二、生即无生门（大乘始教）</span><div class=body>体悟「法空」——外境皆由阿赖耶识变现，生而无生。达我法二空之境。此门始破「法执」，识心无体，境不自境。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>三、事理圆融门（大乘终教）</span><div class=body>空有不二，悲智双运。实现「空有双亡」之境——理（真如）不碍事（万象），事不碍理，理事圆融无碍。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>四、语观双绝门（大乘顿教）</span><div class=body>离心行言说之境。言语道断，心行处灭。唯有真如及真如智。言语不能及，观想不能到，唯证相应。</div></div>";
  h+="<div class=wu-door onclick='this.classList.toggle(\"open\")'><span class=arrow>▶</span><span class=ttl>五、华严三昧门（一乘圆教·究竟）</span><div class=body>见法界缘起之相——万象影现，一即一切、圆融无碍。若能当下认证万法从缘，便可顿入法界缘起。此即海印三昧——如大海映现万象，佛心如海，一时普现十方法界无尽缘起。</div></div>";
  h+="</div>";

  h+="<div class=section><h2>📊 十信法门</h2><table class=v-table><tr><th>信位</th><th>禅定</th><th>法位</th><th>观法</th><th>关键检验</th></tr>";
  h+="<tr><td>初信</td><td>四天王定</td><td>煖法</td><td>唯心识观</td><td>自省三业·觉醒生命意义</td></tr>";
  h+="<tr><td>二信</td><td>忉利定</td><td>顶法</td><td>观妄念所由生</td><td>确认菩提心·收心工程完成</td></tr>";
  h+="<tr><td>三信</td><td>欲界定</td><td>忍法</td><td>轻安三相</td><td>菩提心稳定·摄众共修</td></tr>";
  h+="<tr><td>四信</td><td>未到定</td><td>世第一法</td><td>安般守意</td><td>置心风门·心不散乱</td></tr>";
  h+="<tr><td>五~十信</td><td>色界·无色界定</td><td>—</td><td>奢摩他·毗婆舍那</td><td>舍妄念→入界外定</td></tr>";
  h+="</table></div>";

  h+="<div class=section><h2>🎯 三摩呬多·三摩钵底·三摩地</h2><table class=v-table><tr><th>名相</th><th>梵语</th><th>定位</th><th>操作要点</th></tr>";
  h+="<tr><td>三摩呬多</td><td>Samāhita</td><td>入定前·专注调心</td><td>粗住→细住→欲界定。排除妄想执著</td></tr>";
  h+="<tr><td>三摩钵底</td><td>Samāpatti</td><td>以观导定·定慧双运</td><td>勘定三界定。须善知识勘定</td></tr>";
  h+="<tr><td>三摩地</td><td>Samādhi</td><td>究竟·心一境性</td><td>出入自在。破法执我执</td></tr>";
  h+="</table></div>";

  h+="<div class=section><h2>📚 华严六科</h2><table class=v-table><tr><th>科目</th><th>内容</th></tr>";
  h+="<tr><td>华严学概论</td><td>华严经结构·五教十宗·法界缘起</td></tr>";
  h+="<tr><td>华严经教行法</td><td>经文解读·修行法门·善财五十三参</td></tr>";
  h+="<tr><td>华严禅行法</td><td>安般守意·置心一处·三摩地次第</td></tr>";
  h+="<tr><td>华严戒律观</td><td>菩萨戒·梵网经·现代持戒</td></tr>";
  h+="<tr><td>华严净土法门</td><td>华藏世界·毗卢遮那净土</td></tr>";
  h+="<tr><td>华严密法</td><td>华严字母·曼荼罗·真言持诵</td></tr>";
  h+="</table></div>";

  h+="<div class=section><h2>🎬 讲法资源</h2><p style=line-height:1.8>";
  h+="▶ <a href='https://search.bilibili.com/all?keyword=%E6%B5%B7%E4%BA%91%E7%BB%A7%E6%A2%A6' target=_blank>Bilibili: 海云继梦讲经全集</a> —《华严六科》(42h完整版)<br>";
  h+="▶ YouTube: 搜索「大華嚴寺」— 大华严寺官方频道<br>";
  h+="🎙 <a href='https://podcasts.apple.com/au/podcast/普贤乘华严宗/id1523368889' target=_blank>Apple Podcast</a> · <a href='https://open.spotify.com/show/2ZDlq4cOOiynQvlzPARkmc' target=_blank>Spotify</a><br>";
  h+="🌐 <a href='https://www.huayenworld.org/' target=_blank>大华严寺官网</a></p></div>";

  h+="<div class=section><h2>🏛 相关道场</h2><p style=line-height:1.8>";
  h+="📍 <b>南投大华严寺</b> — 海云继梦导师·普贤乘根本道场<br>";
  h+="📍 <b>台北福慧寺</b> — 钦因长老·高原法系<br>";
  h+="📍 <b>台北华严莲社</b> — 贤度法师·华严专宗学院</p></div>";

  pv.innerHTML=h;
}
