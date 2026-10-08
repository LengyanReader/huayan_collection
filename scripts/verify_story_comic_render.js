// 连环画·分镜信息图渲染门禁（静态·零 Canvas）：
// 在 Node 中以最小 DOM 桩**实跑** build 产物内联之 story_comic.js（renderStoryComic），
// 校验静态版面与各维度信息图的硬不变量：
//   A. 分镜连环画 —— 分幕数对账 meta.expected.acts、格号连续 1..shots、逐格「出处」在场、
//      reconstruction 格必附「〔编辑判断〕」与判断文、景别/运镜标签不落空；
//   B. 拍点字幕序列 —— 拍数对账 beats 长度、逐拍 narration_ref 出处在场；
//   C. 维度信息图 —— SVG 在场且图节 id 齐、词频条形值与 ARTICLE_DS 数据对账；
//   通用 —— 无 undefined / NaN / [object Object] 泄漏、中英对照 (.en-line) 在场、
//      页首入口按钮与 comicGo() 链路齐。
// （真机浏览器 CDP 本机不可用，故以桩求「逻辑真跑」；像素级渲染待真机复验。）
const fs = require('fs');
const vm = require('vm');
const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');
const errs = [];

/* ── 数据 JSON 抽取 ─────────────────────────────────────────── */
function jsonVar(name) {
  const re = new RegExp('var ' + name + ' = (\\{[\\s\\S]*?\\});<\\/script>');
  const m = html.match(re);
  if (!m) return null;
  try { return JSON.parse(m[1]); }
  catch (e) { errs.push(name + ' JSON parse failed: ' + e.message); return null; }
}
const MIAOYAN_SB = jsonVar('MIAOYAN_SB');
const MIAOYAN_NARR = jsonVar('MIAOYAN_NARR');
const ARTICLE_DS = jsonVar('ARTICLE_DS');
const ARTICLE_ASSEMBLY = jsonVar('ARTICLE_ASSEMBLY');
if (!MIAOYAN_SB && !MIAOYAN_NARR) { console.error('FAIL: neither MIAOYAN_NARR nor MIAOYAN_SB in ' + file); process.exit(1); }

/* ── 渲染器源码抽取（内联 script 中定义 story_comic 者）────── */
const blocks = [];
const reS = /<script>([\s\S]*?)<\/script>/g;
let mm;
while ((mm = reS.exec(html)) !== null) blocks.push(mm[1]);
const src = blocks.find(b => b.indexOf('global.renderStoryComic') >= 0 && b.indexOf('function esc') >= 0);
if (!src) { console.error('FAIL: story_comic.js renderer not inlined'); process.exit(1); }

/* ── 页首入口与折叠壳钩子（由 article.js 生成）──────────────── */
if (html.indexOf('function comicGo') < 0) errs.push('function comicGo missing');
if (html.indexOf('onclick="comicGo()"') < 0) errs.push('comicGo() button missing');
if (html.indexOf('renderStoryComic(\'#story-comic-inner\')') < 0) errs.push('renderStoryComic hook missing');

/* ── 最小 DOM 桩 ───────────────────────────────────────────── */
function mkEl(sel) {
  let h = '';
  return {
    _sel: sel,
    get innerHTML() { return h; },
    set innerHTML(v) { h = String(v); },
    scrollIntoView() {},
    addEventListener() {},
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    style: {}, dataset: {},
    appendChild() {}, setAttribute() {}, getAttribute() { return null; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    getContext() { return null; },
    textContent: '',
  };
}
const els = {};
function sel(s) { if (!els[s]) els[s] = mkEl(s); return els[s]; }

const sandbox = {
  console, Math, JSON, Date, Array, Object, String, Number, Boolean, RegExp, Error, isFinite, isNaN,
  MIAOYAN_SB, MIAOYAN_NARR, ARTICLE_DS, ARTICLE_ASSEMBLY,
  document: { querySelector: sel, getElementById: id => sel('#' + id) },
  setTimeout, clearTimeout, requestAnimationFrame: f => f(),
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
try { vm.runInContext(src, sandbox, { filename: 'story_comic.js' }); }
catch (e) { console.error('FAIL: renderer eval — ' + e.message); process.exit(1); }
if (typeof sandbox.renderStoryComic !== 'function') { console.error('FAIL: renderStoryComic not exported'); process.exit(1); }

let out = '';
try { out = sandbox.renderStoryComic('#story-comic-inner') || ''; }
catch (e) { console.error('FAIL: renderStoryComic threw — ' + e.message); process.exit(1); }
const inDom = sel('#story-comic-inner').innerHTML;
if (!out) { console.error('FAIL: renderer returned empty'); process.exit(1); }
if (inDom !== out) errs.push('innerHTML not written (or differs from returned markup)');
if (process.env.SC_DEBUG) fs.writeFileSync(process.env.SC_DEBUG, out, 'utf8');

/* ── 通用：泄漏与中英对照 ───────────────────────────────────── */
for (const bad of ['undefined', 'NaN', '[object Object]', 'null 词']) {
  const i = out.indexOf(bad);
  if (i >= 0) errs.push('leak "' + bad + '" at ' + i + ': …' + out.slice(Math.max(0, i - 60), i + 60).replace(/\s+/g, ' '));
}
const enLines = (out.match(/class="en-line"/g) || []).length;
if (enLines < 1) errs.push('no .en-line (中英对照缺失)');

/* ── A. 分镜连环画 ─────────────────────────────────────────── */
function count(re) { return (out.match(re) || []).length; }
if (MIAOYAN_SB) {
  const exp = (MIAOYAN_SB.meta && MIAOYAN_SB.meta.expected) || {};
  const acts = MIAOYAN_SB.acts || [];
  if (!acts.length) errs.push('MIAOYAN_SB has no acts');
  const nPanels = acts.reduce((a, x) => a + (x.shots || []).length, 0);
  if (out.indexOf('id="story-panels"') < 0) errs.push('#story-panels section missing');
  // 头注与逐幕标题：非空 + 实际印上版面（否则「|| ''」会静默吞掉空标题）
  const meta = MIAOYAN_SB.meta || {};
  ['title_zh', 'title_en', 'subtitle_zh', 'subtitle_en', 'source_primary', 'method_zh'].forEach(k => {
    if (!meta[k]) errs.push('meta.' + k + ' empty');
    else if (out.indexOf(String(meta[k])) < 0) errs.push('meta.' + k + ' not printed');
  });
  // 凡例英译与分镜规格出处（数据有则必印，中英必配）
  if (meta.method_en) { if (out.indexOf(String(meta.method_en)) < 0) errs.push('meta.method_en not printed'); }
  else errs.push('meta.method_en empty (中英必配)');
  if (meta.spec_ref) { if (out.indexOf(String(meta.spec_ref)) < 0) errs.push('meta.spec_ref not printed'); }
  if (meta.spec_ref_en && out.indexOf(String(meta.spec_ref_en)) < 0) errs.push('meta.spec_ref_en not printed');
  if (meta.reconstruction_flag_en && out.indexOf(String(meta.reconstruction_flag_en)) < 0)
    errs.push('meta.reconstruction_flag_en not printed');
  // 全幅画面要素索引：按幕分账（同名 id 在不同幕各有名相，不可跨幕串用）
  const ACTPMAP = acts.map(a => {
    const m = {};
    (a.props || []).forEach(p => { m[p.id] = p; });
    return m;
  });
  acts.forEach((a, ai) => {
    const tag = 'act' + (a.no || (ai + 1));
    if (!a.title_zh) errs.push(tag + ' missing title_zh');
    else if (out.indexOf(a.title_zh) < 0) errs.push(tag + ' title_zh not printed');
    if (!a.title_en) errs.push(tag + ' missing title_en (中英必配)');
    if (!a.fascicle_zh) errs.push(tag + ' missing fascicle_zh');
    if (a.fascicle_en) { if (out.indexOf(a.fascicle_en) < 0) errs.push(tag + ' fascicle_en not printed'); }
    else errs.push(tag + ' missing fascicle_en (中英必配)');
    if (a.lead_zh) {
      if (out.indexOf(a.lead_zh) < 0) errs.push(tag + ' lead_zh not printed');
      if (!a.lead_en) errs.push(tag + ' missing lead_en (中英必配)');
      else if (out.indexOf(a.lead_en) < 0) errs.push(tag + ' lead_en not printed');
    }
    const props = a.props || [];
    props.forEach(p => {
      if (!p.label_zh) errs.push(tag + ' prop ' + p.id + ' missing label_zh');
      else if (out.indexOf(p.label_zh) < 0) errs.push(tag + ' prop ' + p.id + ' label_zh not printed');
      // 画面要素：名相＋经文原句＋英译皆须上版面（原 title tooltip → 正文）
      if (p.label_en && out.indexOf(p.label_en) < 0) errs.push(tag + ' prop ' + p.id + ' label_en not printed');
      if (p.quote_zh && out.indexOf(p.quote_zh) < 0) errs.push(tag + ' prop ' + p.id + ' quote_zh not printed');
      if (p.quote_en && out.indexOf(p.quote_en) < 0) errs.push(tag + ' prop ' + p.id + ' quote_en not printed');
      if (p.quote_zh && !p.quote_en) errs.push(tag + ' prop ' + p.id + ' missing quote_en (中英必配)');
    });
    if (a.layout && out.indexOf('版面类型 ' + a.layout) < 0) errs.push(tag + ' layout chip not printed');
  });
  if (exp.acts != null && acts.length !== exp.acts) errs.push('acts=' + acts.length + ' ≠ expected ' + exp.acts);
  if (exp.shots != null && nPanels !== exp.shots) errs.push('shots=' + nPanels + ' ≠ expected ' + exp.shots);
  const printed = count(/第 \d+ 格/g);
  if (printed !== nPanels) errs.push('printed panels=' + printed + ', data shots=' + nPanels);
  const dividers = count(/▼ 转入下幕/g);
  if (dividers !== Math.max(0, acts.length - 1)) errs.push('act dividers=' + dividers + ', want ' + (acts.length - 1));
  // 格号连续 1..N；窗口以下一格锚点为界（新增内容后固定长度窗口易漏项）
  const PANEL_AT = {};
  let scanFrom = 0;
  for (let k = 1; k <= nPanels; k++) {
    const i = out.indexOf('第 ' + k + ' 格', scanFrom);
    if (i >= 0) { PANEL_AT[k] = i; scanFrom = i + 1; }
  }
  const SHOT_ACT = {};
  acts.forEach((a, ai) => (a.shots || []).forEach(s => { SHOT_ACT[s.no] = ai; }));
  let no = 0, noncontig = [];
  for (const a of acts) for (const s of (a.shots || [])) {
    no += 1;
    if (s.no !== no) noncontig.push('data ' + s.no + '≠' + no);
    if (!s.ref) errs.push('shot ' + s.no + ' missing ref');
    if (!s.subtitle_zh) errs.push('shot ' + s.no + ' missing subtitle_zh');
    if (!s.subtitle_en) errs.push('shot ' + s.no + ' missing subtitle_en (中英必配)');
    if (!s.quote_zh) errs.push('shot ' + s.no + ' missing quote_zh');
    const px = PANEL_AT[s.no] != null ? PANEL_AT[s.no] : out.indexOf('第 ' + s.no + ' 格');
    if (px < 0) errs.push('shot ' + s.no + ' not printed');
    else {
      const end = PANEL_AT[s.no + 1] != null ? PANEL_AT[s.no + 1] : px + 8000;
      const win = out.slice(px, Math.max(end, px + 500));
      if (s.ref && win.indexOf(s.ref) < 0) errs.push('shot ' + s.no + ' ref not printed');
      if (s.reconstruction && win.indexOf('〔编辑判断〕') < 0) errs.push('shot ' + s.no + ' missing 〔编辑判断〕');
      if (s.reconstruction && s.judgment_zh && win.indexOf(s.judgment_zh) < 0) errs.push('shot ' + s.no + ' judgment not printed');
      if (s.subtitle_zh && win.indexOf(s.subtitle_zh) < 0) errs.push('shot ' + s.no + ' subtitle_zh not printed');
      if (s.quote_zh && win.indexOf(s.quote_zh) < 0) errs.push('shot ' + s.no + ' quote_zh not printed');
      if (s.reconstruction && s.judgment_en && win.indexOf(s.judgment_en) < 0)
        errs.push('shot ' + s.no + ' judgment_en not printed (中英必配)');
      // 取景：主体与焦点须以本幕名相呈现（同名 id 跨幕不串用），且取景行在场
      const AM = ACTPMAP[SHOT_ACT[s.no]] || {};
      const framing = (s.focus || []).concat(s.subject ? [s.subject] : []);
      if (framing.length && win.indexOf('取景：') < 0) errs.push('shot ' + s.no + ' framing line missing');
      for (const id of framing) {
        const p = AM[id];
        if (!p) { errs.push('shot ' + s.no + ' framing id unresolved in own act: ' + id); continue; }
        if (p.label_zh && win.indexOf(p.label_zh) < 0)
          errs.push('shot ' + s.no + ' framing label not printed: ' + id);
      }
      // 景别/运镜标签须为 zh 文（而非空/未解析 id）
      const sz = MIAOYAN_SB.shot_sizes && MIAOYAN_SB.shot_sizes[s.size];
      if (sz && sz.zh && win.indexOf(sz.zh) < 0) errs.push('shot ' + s.no + ' size label not printed');
      const mv = MIAOYAN_SB.camera_moves && MIAOYAN_SB.camera_moves[s.move];
      if (mv && mv.zh && win.indexOf(mv.zh) < 0) errs.push('shot ' + s.no + ' move label not printed');
    }
  }
  if (noncontig.length) errs.push('shot numbering not contiguous: ' + noncontig.slice(0, 3).join('; '));
  const recon = [];
  for (const a of acts) for (const s of (a.shots || [])) if (s.reconstruction) recon.push(s.no);
  const flag = count(/〔编辑判断〕/g);
  if (recon.length && flag < recon.length) errs.push('〔编辑判断〕 printed ' + flag + ', reconstruction shots ' + recon.length);
  // 回源更正：数据有 corrections 者须在版面上留下痕迹（逐条中英；渲染器会做 HTML 转义）
  if ((MIAOYAN_SB.corrections || []).length && out.indexOf('回源更正') < 0) errs.push('corrections not surfaced');
  const htmlEsc = t => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  (MIAOYAN_SB.corrections || []).forEach((c, i) => {
    const zh = typeof c === 'string' ? c : (c.text_zh || c.zh || '');
    const en = typeof c === 'string' ? '' : (c.text_en || c.en || '');
    const has = t => out.indexOf(t) >= 0 || out.indexOf(htmlEsc(t)) >= 0;
    if (zh && !has(zh)) errs.push('correction ' + (i + 1) + ' zh not printed');
    if (en && !has(en)) errs.push('correction ' + (i + 1) + ' en not printed');
  });
}

/* ── B. 拍点字幕序列 ───────────────────────────────────────── */
if (MIAOYAN_NARR) {
  const beats = (MIAOYAN_NARR.beats || []).slice().sort((a, b) => (a.order || 0) - (b.order || 0));
  if (!beats.length) errs.push('MIAOYAN_NARR has no beats');
  if (out.indexOf('id="story-beats"') < 0) errs.push('#story-beats section missing');
  const nmeta = MIAOYAN_NARR.meta || {};
  ['title_zh', 'title_en'].forEach(k => {
    if (!nmeta[k]) errs.push('NARR.meta.' + k + ' empty');
    else if (out.indexOf(String(nmeta[k])) < 0) errs.push('NARR.meta.' + k + ' not printed');
  });
  const printed = count(/第 \d+ 拍/g);
  if (printed !== beats.length) errs.push('printed beats=' + printed + ', data=' + beats.length);
  // meta.sources：可点回源链接须上版面
  (nmeta.sources || []).forEach((s, i) => {
    if (!s.url) errs.push('NARR.meta.sources[' + i + '] missing url');
    else if (out.indexOf(s.url) < 0) errs.push('NARR.meta.sources[' + i + '] url not printed');
    if (s.label && out.indexOf(s.label) < 0) errs.push('NARR.meta.sources[' + i + '] label not printed');
  });
  // 拍点窗口：以下一拍锚点为界（画面/环位/构成入版后固定长度窗口易漏项）
  const BEAT_AT = {};
  let bscan = 0;
  for (let k = 1; k <= beats.length; k++) {
    const i = out.indexOf('第 ' + k + ' 拍', bscan);
    if (i >= 0) { BEAT_AT[k] = i; bscan = i + 1; }
  }
  beats.forEach((b, i) => {
    if (!b.narration_ref) errs.push('beat ' + (b.id || i) + ' missing narration_ref');
    if (!b.narration_zh) errs.push('beat ' + (b.id || i) + ' missing narration_zh');
    const px = BEAT_AT[i + 1] != null ? BEAT_AT[i + 1] : out.indexOf('第 ' + (i + 1) + ' 拍');
    if (px < 0) { errs.push('beat ' + (i + 1) + ' not printed'); return; }
    const bend = BEAT_AT[i + 2] != null ? BEAT_AT[i + 2] : px + 10000;
    const win = out.slice(px, Math.max(bend, px + 600));
    if (b.narration_ref && win.indexOf(b.narration_ref) < 0) errs.push('beat ' + (i + 1) + ' narration_ref not printed');
    if (b.narration_zh && win.indexOf(b.narration_zh) < 0) errs.push('beat ' + (i + 1) + ' narration_zh not printed');
    if (b.title_zh && win.indexOf(b.title_zh) < 0) errs.push('beat ' + (i + 1) + ' title_zh not printed');
    if (b.narration_en && win.indexOf(b.narration_en) < 0) errs.push('beat ' + (i + 1) + ' narration_en not printed');
    if ((b.uncertainty || []).length && win.indexOf('存疑标注') < 0) errs.push('beat ' + (i + 1) + ' uncertainty not printed');
    // 画面动作 / 环位 / 画面构成（原动画层信息降级，皆须上版面且不裸露 id）
    const bacts = b.actions || [];
    if (bacts.length && win.indexOf('画面：') < 0) errs.push('beat ' + (i + 1) + ' actions line missing');
    bacts.forEach((a, j) => {
      if (a.zh && win.indexOf(a.zh) < 0) errs.push('beat ' + (i + 1) + ' action[' + j + '] zh not printed');
      if (a.en && win.indexOf(a.en) < 0) errs.push('beat ' + (i + 1) + ' action[' + j + '] en not printed');
    });
    const sf = b.space_focus || [];
    sf.forEach(id => {
      const lab = spaceLab(id, 'zh');
      if (!lab) errs.push('beat ' + (i + 1) + ' space_focus unresolved: ' + id);
      else if (win.indexOf(lab) < 0) errs.push('beat ' + (i + 1) + ' space_focus label not printed: ' + id);
    });
    (b.cast_groups || []).forEach(t => {
      const lab = spaceLab(t, 'zh');
      if (!lab) errs.push('beat ' + (i + 1) + ' cast token unresolved (id leak): ' + t);
      else if (win.indexOf(lab) < 0) errs.push('beat ' + (i + 1) + ' cast label not printed: ' + t);
    });
  });
}

/* ── B″. 环位与口径节（space 层：中心＋同心环表＋校准说明）────── */
function spaceLab(id, lang) {
  const key = 'label_' + lang;
  const cl = MIAOYAN_NARR && MIAOYAN_NARR.visual_style && MIAOYAN_NARR.visual_style.cast_labels;
  if (cl && cl[id] && cl[id][key]) return cl[id][key];
  const sp = MIAOYAN_NARR && MIAOYAN_NARR.space;
  if (!sp) return null;
  if (sp.center && (id === sp.center.id || id === 'center')) return sp.center[key] || null;
  const r = (sp.rings || []).find(x => x.id === id);
  if (r) return r[key] || null;
  if (id === 'bg') return (sp.background && sp.background[key]) || null;
  return null;
}
if (MIAOYAN_NARR && MIAOYAN_NARR.space && (MIAOYAN_NARR.space.rings || []).length) {
  const sp = MIAOYAN_NARR.space, bg = sp.background || {};
  if (out.indexOf('id="story-space"') < 0) errs.push('#story-space section missing');
  if (sp.center && sp.center.label_zh && out.indexOf(sp.center.label_zh) < 0)
    errs.push('space.center label not printed');
  (sp.rings || []).forEach(r => {
    if (!r.label_zh) errs.push('ring ' + r.id + ' missing label_zh');
    else if (out.indexOf(r.label_zh) < 0) errs.push('ring ' + r.id + ' label_zh not printed');
    if (r.label_en && out.indexOf(r.label_en) < 0) errs.push('ring ' + r.id + ' label_en not printed');
    if (!r.source_ref) errs.push('ring ' + r.id + ' missing source_ref');
    else if (out.indexOf(r.source_ref) < 0) errs.push('ring ' + r.id + ' source_ref not printed');
  });
  if (bg.calibration) {
    if (out.indexOf(bg.calibration) < 0) errs.push('space.background.calibration not printed');
    if (!bg.calibration_en) errs.push('space.background.calibration_en missing (中英必配)');
    else if (out.indexOf(bg.calibration_en) < 0) errs.push('space.background.calibration_en not printed');
  }
  if (bg.token_note) {
    if (out.indexOf(bg.token_note) < 0) errs.push('space.background.token_note not printed');
    if (bg.token_note_en && out.indexOf(bg.token_note_en) < 0) errs.push('space.background.token_note_en not printed');
  }
  // 口径行（共 N 类 · 具名 M 名）须以合并字面出现——仅分别查数字会被「类→组」之类的
  // 渲染器改字蒙过（M11 曾假绿，故断言整行字面）
  if (sp.expected && sp.expected.classes != null && sp.expected.named != null) {
    const line = '口径：共 ' + sp.expected.classes + ' 类 · 具名 ' + sp.expected.named + ' 名';
    if (out.indexOf(line) < 0) errs.push('口径行未整行打印: ' + line);
  }
}

/* ── B'. space 数值契约（一点＝一类）──────────────────────────
 * 旧叙事播放器门禁已随播放器一并撤除；此「40 类／414 名」口径不因播放器退场而失守，
 * 故移入本门禁作为数据层硬不变量（有 expected 方校验，无则略）。 */
if (MIAOYAN_NARR && MIAOYAN_NARR.space && MIAOYAN_NARR.space.expected) {
  const sp = MIAOYAN_NARR.space, rings = sp.rings || [];
  if (!rings.length) errs.push('space.expected present but no rings');
  const sCls = rings.reduce((a, r) => a + (r.member_classes || 0), 0);
  const sMem = rings.reduce((a, r) => a + (r.member_count || 0), 0);
  if (sp.expected.classes != null && sCls !== sp.expected.classes)
    errs.push('member_classes sum=' + sCls + ' ≠ expected ' + sp.expected.classes);
  if (sp.expected.named != null && sMem !== sp.expected.named)
    errs.push('member_count sum=' + sMem + ' ≠ expected ' + sp.expected.named);
}

/* ── C. 维度信息图 ─────────────────────────────────────────── */
if (out.indexOf('id="story-figs"') < 0) errs.push('#story-figs section missing');
if (count(/<svg /g) < 1) errs.push('no <svg> infographic');
// 图幅收敛：SVG 须限宽（viewBox 560 单位若通栏 100% 会被放大约 2.7 倍，字号失度）
for (const tag of (out.match(/<svg [^>]*>/g) || [])) {
  if (tag.indexOf('max-width:') < 0) errs.push('svg without max-width cap: ' + tag.slice(0, 70));
}
const figIds = ['sc-fig-topchars', 'sc-fig-betti', 'sc-fig-spectrum', 'sc-fig-assembly'];
const wantFigs = [];
if (ARTICLE_DS && ARTICLE_DS.linguistic && ARTICLE_DS.linguistic.zipf &&
    (ARTICLE_DS.linguistic.zipf.top_chars || []).length) wantFigs.push('sc-fig-topchars');
if (ARTICLE_DS && ARTICLE_DS.geometry && (ARTICLE_DS.geometry.betti_curve || []).length > 1) wantFigs.push('sc-fig-betti');
if (ARTICLE_DS && ARTICLE_DS.geometry && ARTICLE_DS.geometry.spectral && ARTICLE_DS.geometry.spectral.spectrum) wantFigs.push('sc-fig-spectrum');
if (ARTICLE_ASSEMBLY && (ARTICLE_ASSEMBLY.classes || []).length) wantFigs.push('sc-fig-assembly');
for (const f of wantFigs) if (out.indexOf('id="' + f + '"') < 0) errs.push('figure ' + f + ' missing (wanted)');
for (const f of figIds) if (wantFigs.indexOf(f) < 0 && out.indexOf('id="' + f + '"') >= 0) errs.push('figure ' + f + ' printed but data absent');
if (!wantFigs.length) errs.push('no figure data present at all');
// 词频条形值须与数据对账（取前 3）
const tc = (ARTICLE_DS && ARTICLE_DS.linguistic && ARTICLE_DS.linguistic.zipf &&
            ARTICLE_DS.linguistic.zipf.top_chars || []).slice(0, 3);
if (tc.length && out.indexOf('sc-fig-topchars') >= 0) {
  for (const t of tc) {
    const px = out.indexOf('sc-fig-topchars');
    const win = out.slice(px, px + 4000);
    if (win.indexOf('>' + t.char + '<') < 0) errs.push('top char "' + t.char + '" not labelled in figure');
    if (win.indexOf('>' + t.count + '<') < 0) errs.push('top char count ' + t.count + ' not printed');
  }
}
// 会众结构：类数须与 ARTICLE_ASSEMBLY 对账
if (wantFigs.indexOf('sc-fig-assembly') >= 0) {
  const cls = ARTICLE_ASSEMBLY.classes.length;
  if (out.indexOf('共 ' + cls + ' 类') < 0) errs.push('assembly class count ' + cls + ' not printed');
}

/* ── 结论 ───────────────────────────────────────────────────── */
if (errs.length) {
  console.error('FAIL (' + errs.length + '):');
  errs.slice(0, 40).forEach(e => console.error('  - ' + e));
  if (errs.length > 40) console.error('  … and ' + (errs.length - 40) + ' more');
  process.exit(1);
}
const parts = [];
if (MIAOYAN_SB) {
  const acts = MIAOYAN_SB.acts || [];
  parts.push(acts.length + '幕/' + acts.reduce((a, x) => a + (x.shots || []).length, 0) + '格');
}
if (MIAOYAN_NARR) parts.push(((MIAOYAN_NARR.beats || []).length) + '拍');
parts.push(wantFigs.length + '图');
parts.push(enLines + ' en-line');
console.log('OK: ' + parts.join(' · '));
