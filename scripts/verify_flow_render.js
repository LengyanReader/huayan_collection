// 会众全景流程图（简明静态版）渲染门禁：在 Node 中以最小 DOM 桩执行 build 产物内联之 MiaoyanFlow。
// 三重校验：
//   ① 数据不变量——四十类、idx 连续 0–39、五环 group 于列次连续成段、成员之和＝414、
//      每类皆具 cat/leader/vow/source 与成员；
//   ② 不损（渲染产物）——每一类之 类名/上首 皆逐字见于渲染 HTML（.mfd-cell 四十格、五段齐备）；
//   ③ 回源覆核——类名/上首/成员/本愿原文逐字见于 CBETA T10n0279（先去标签再去空白，
//      因 <lb/> 换行会在句中断开）。成员/本愿虽不入本图，仍在校验之列以护源数据不漂移。
// 本图为静态流程图，无检索/展开/跳转，故不再驱交互控件。
// 用法：node verify_flow_render.js <html> <common.js> <T10n0279.xml>
const fs = require('fs');
const file = process.argv[2];
const t279file = process.argv[4];
const html = fs.readFileSync(file, 'utf8');
const errs = [];

/* ── 抽取数据与源码 ─────────────────────────────────────── */
const dm = html.match(/var ARTICLE_ASSEMBLY = (\{[\s\S]*?\});<\/script>/);
if (!dm) { console.error('FAIL: ARTICLE_ASSEMBLY not found in ' + file); process.exit(1); }
const ASM = JSON.parse(dm[1]);

const si = html.indexOf('var MiaoyanFlow = (function');
const wi = html.indexOf('function renderMiaoyanFlow(containerId)');
if (si < 0 || wi < 0) { console.error('FAIL: flow renderer not found'); process.exit(1); }
const we = html.indexOf('\n}', wi);
if (we < 0) { console.error('FAIL: renderer source bounds not found'); process.exit(1); }
const src = html.slice(si, we + 2);

/* ── 数据层不变量（先于渲染校验）───────────────────────── */
const cls = (ASM.classes || []).slice().sort((a, b) => (a.idx || 0) - (b.idx || 0));
const N = cls.length;
if (N === 0) { console.error('FAIL: no classes'); process.exit(1); }
const sumMembers = cls.reduce((a, c) => a + ((c.members || []).length), 0);
for (let i = 0; i < N; i++) {
  if ((cls[i].idx || 0) !== i) errs.push('idx not continuous at ' + i + ': ' + cls[i].idx);
  if (!cls[i].cat || !cls[i].leader || !cls[i].vow) errs.push('cls' + i + ' missing cat/leader/vow');
  if (!(cls[i].members || []).length) errs.push('cls' + i + ' has no members');
  if (!cls[i].source) errs.push('cls' + i + ' missing source');
}
// 五环 group 于列次连续成段
const seen = new Set(); let prev = null;
for (const c of cls) { if (c.group !== prev) { if (seen.has(c.group)) errs.push('group not contiguous: ' + c.group); seen.add(c.group); prev = c.group; } }
if (N !== 40) errs.push('classes=' + N + ', expected 40');
if (sumMembers !== 414) errs.push('sum members=' + sumMembers + ', expected 414');
if (seen.size !== 5) errs.push('bands=' + seen.size + ', expected 5');

// members 为对象 {i,name,is_leader}；兼容纯字符串
const mname = (m) => (typeof m === 'string') ? m : ((m && m.name) || '');

// T279 归一：先去标签，再去所有空白
let t279norm = '';
if (t279file && fs.existsSync(t279file)) {
  t279norm = fs.readFileSync(t279file, 'utf8').replace(/<[^>]+>/g, '').replace(/\s+/g, '');
} else { errs.push('T279 xml not found: ' + t279file); }

/* ── 最小 DOM 桩（本图为静态，仅需承接 innerHTML）───────── */
const root = {
  _html: '',
  get innerHTML() { return this._html; },
  set innerHTML(v) { this._html = String(v); },
  querySelector() { return null; },
  querySelectorAll() { return []; },
};
global.document = { querySelector: () => root, getElementById: () => null, createElement: () => ({ style: {} }) };

/* ── 执行 ──────────────────────────────────────────────── */
let renderFn;
try {
  renderFn = new Function('ARTICLE_ASSEMBLY', src + '\nreturn renderMiaoyanFlow;')(ASM);
} catch (e) {
  console.error('FAIL: renderer threw on load — ' + e.message + '\n' + e.stack); process.exit(1);
}
if (typeof renderFn !== 'function') { console.error('FAIL: not a function'); process.exit(1); }
try { renderFn('#article-flow'); }
catch (e) { console.error('FAIL: render() threw — ' + e.message + '\n' + e.stack); process.exit(1); }

/* ── 静态产物校验（不损之保证）────────────────────────── */
const H = root.innerHTML;
if (H.length < 3000) errs.push('innerHTML too short: ' + H.length);
const escH = (t) => String(t == null ? '' : t)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

for (const s of ['mfd-flow', 'mfd-stats', 'mfd-root', 'mfd-band', 'mfd-cell', 'mfd-legend', 'mfd-arrow', 'mfd-src']) {
  if (!H.includes(s)) errs.push('missing element/class: ' + s);
}
const cellCnt = (H.match(/class="mfd-cell"/g) || []).length;
if (cellCnt !== N) errs.push('rendered .mfd-cell=' + cellCnt + ', expected ' + N);
const bandCnt = (H.match(/class="mfd-band /g) || []).length;
if (bandCnt !== seen.size) errs.push('rendered .mfd-band=' + bandCnt + ', expected ' + seen.size);
const arrowCnt = (H.match(/class="mfd-arrow"/g) || []).length;
if (arrowCnt !== seen.size - 1) errs.push('rendered .mfd-arrow=' + arrowCnt + ', expected ' + (seen.size - 1));
for (const leak of ['undefined', 'NaN', '[object Object]']) {
  if (H.includes(leak)) errs.push('leak in innerHTML: ' + leak);
}
// 不损（渲染产物）：每一类之 cat/leader 皆须见于渲染 HTML
for (const c of cls) {
  const tag = 'cls' + c.idx;
  if (!H.includes(escH(c.cat))) errs.push('render missing cat: ' + tag);
  if (!H.includes(escH(c.leader))) errs.push('render missing leader: ' + tag);
}

// 回源覆核：类名/上首/成员/本愿原文逐字见于 T279（去标签去空白后）
if (t279norm) {
  const norm = (t) => String(t).replace(/\s+/g, '');
  for (const c of cls) {
    if (!t279norm.includes(norm(c.cat))) errs.push('cat NOT in T279: cls' + c.idx);
    if (!t279norm.includes(norm(c.leader))) errs.push('leader NOT in T279: cls' + c.idx);
    if (!t279norm.includes(norm(c.vow))) errs.push('vow NOT in T279: cls' + c.idx);
    for (const m of (c.members || [])) { const nm = mname(m); if (!nm || !t279norm.includes(norm(nm))) errs.push('member NOT in T279「' + nm + '」@cls' + c.idx); }
  }
}

/* ── 汇总 ──────────────────────────────────────────────── */
if (errs.length) {
  console.error('FAIL (' + errs.length + '):');
  errs.slice(0, 40).forEach(e => console.error('  - ' + e));
  if (errs.length > 40) console.error('  ... +' + (errs.length - 40) + ' more');
  process.exit(1);
}
// 此行须保持纯 ASCII —— verify_demo 以 locale 编码读取 node 输出，非 ASCII 会致 decode 失败、假绿。
console.log('OK: flow render - ' + N + ' classes, ' + sumMembers + ' members, ' + seen.size +
  ' contiguous group bands; diagram has ' + cellCnt + ' cells + ' + bandCnt + ' bands + ' + arrowCnt +
  ' arrows; cats/leaders present in DOM AND verbatim in T279 (no-loss); cats/leaders/vows/members all verbatim in T279; static (no interaction); no leaks');
