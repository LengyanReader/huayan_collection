// 要点导览渲染冒烟测试：在 Node 中以最小 DOM + Canvas 桩执行 build 产物内联的
// MiaoyanKeypoints / renderMiaoyanKeypoints，先证数据不变量（要点号连续／所属层
// 皆在四层注册之内／判断者必附 judgment_zh 且双向／duration 为正／point_at 为
// 有限二维数组／引文逐字见于 T279——须先去 CBETA 标签再去空白，因 <lb/> 换行
// 会在句中断开），再证静态产物无遗漏（八要点全文俱在、图例、closer、出处），
// 末驱控件（播放/暂停/步进/跳点/进度/倍速/图层）。
// 用法：node verify_keypoints_render.js <html> <common.js> <T10n0279.xml>
// （浏览器 CDP 本机不可用，故以桩执行求「逻辑真跑」；像素级渲染仍待真机复验。）
const fs = require('fs');
const file = process.argv[2];
const t279file = process.argv[4];
const html = fs.readFileSync(file, 'utf8');
const errs = [];

/* ── 抽取数据与源码 ─────────────────────────────────────── */
const dm = html.match(/var MIAOYAN_KP = (\{[\s\S]*?\});<\/script>/);
if (!dm) { console.error('FAIL: MIAOYAN_KP not found in ' + file); process.exit(1); }
const MIAOYAN_KP = JSON.parse(dm[1]);

const si = html.indexOf('var MiaoyanKeypoints = (function');
const wi = html.indexOf('function renderMiaoyanKeypoints(containerId)');
if (si < 0 || wi < 0) { console.error('FAIL: keypoints renderer not found'); process.exit(1); }
const we = html.indexOf('\n}', wi);
if (we < 0) { console.error('FAIL: renderer source bounds not found'); process.exit(1); }
const src = html.slice(si, we + 2);

/* ── 数据层不变量（先于渲染校验）───────────────────────── */
const frame = MIAOYAN_KP.frame || {};
const layers = frame.layers || [];
const layerIds = new Set(layers.map(l => l.id));
const evLevels = MIAOYAN_KP.evidence_levels || {};
const kps = (MIAOYAN_KP.keypoints || []).slice().sort((a, b) => (a.idx || 0) - (b.idx || 0));
const n = kps.length;
if (n === 0) { console.error('FAIL: no keypoints'); process.exit(1); }
if (MIAOYAN_KP.keypoint_count != null && MIAOYAN_KP.keypoint_count !== n)
  errs.push('keypoint_count=' + MIAOYAN_KP.keypoint_count + ' != actual ' + n);

// 要点号连续 1..n
for (let i = 0; i < n; i++) {
  if ((kps[i].idx || 0) !== i + 1) errs.push('idx not continuous at position ' + i + ': ' + kps[i].idx);
}

// T279 归一：先去标签，再去所有空白（CBETA 之 <lb/> 会在句中断行）
let t279norm = '';
if (t279file && fs.existsSync(t279file)) {
  t279norm = fs.readFileSync(t279file, 'utf8').replace(/<[^>]+>/g, '').replace(/\s+/g, '');
} else {
  errs.push('T279 xml not found: ' + t279file);
}

for (const k of kps) {
  const tag = 'kp' + (k.idx || '?');
  if (!layerIds.has(k.layer)) errs.push(tag + ' layer not registered: ' + k.layer);
  if (!(k.duration_s > 0)) errs.push(tag + ' duration_s must be > 0: ' + k.duration_s);
  if (!['T0', 'T1', 'T2'].includes(k.evidence)) errs.push(tag + ' bad evidence: ' + k.evidence);
  else if (!evLevels[k.evidence]) errs.push(tag + ' evidence level undefined in legend: ' + k.evidence);
  // 判断双向不变量：judgment:true ⟺ judgment_zh 存在
  if (k.judgment && !k.judgment_zh) errs.push(tag + ' judgment=true but no judgment_zh');
  if (!k.judgment && k.judgment_zh) errs.push(tag + ' judgment_zh present but judgment!=true');
  // point_at 为有限二维数组
  const pa = k.point_at;
  if (!Array.isArray(pa) || pa.length !== 2 || !pa.every(x => Number.isFinite(x)))
    errs.push(tag + ' point_at not a finite 2-tuple: ' + JSON.stringify(pa));
  // 必备文案字段
  if (!k.title_zh || !k.gist_zh || !k.quote_zh || !k.ref) errs.push(tag + ' missing title/gist/quote/ref');
  // 引文逐字见于 T279（去空白后）
  if (t279norm) {
    const qnorm = String(k.quote_zh).replace(/\s+/g, '');
    if (!t279norm.includes(qnorm)) errs.push(tag + ' quote NOT verbatim in T279: ' + k.quote_zh.slice(0, 18) + '…');
  }
}

/* ── 最小 DOM + Canvas 桩 ───────────────────────────────── */
let CTX = null;
function makeCtx() {
  const calls = Object.create(null);
  const target = {
    calls,
    createRadialGradient: () => ({ addColorStop: () => { } }),
    canvas: { width: 960, height: 600 },
  };
  return new Proxy(target, {
    get(t, p) { if (p in t) return t[p]; return (...a) => { calls[p] = (calls[p] || 0) + 1; }; },
    set(t, p, v) { t[p] = v; return true; },
    has() { return true; },
  });
}
const LG_KEYS = ['labels', 'en', 'links', 'all'];
function mkEl(sel, idx) {
  const h = {};
  const el = {
    _html: '', _sel: sel, _idx: idx,
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    textContent: '', className: '', style: {}, dataset: {}, value: '0', checked: true,
    addEventListener(t, f) { (h[t] = h[t] || []).push(f); },
    fire(t, ev) { (h[t] || []).forEach(f => f.call(el, ev || {})); return (h[t] || []).length; },
    nHandlers(t) { return (h[t] || []).length; },
    getAttribute(k) {
      if (k === 'data-i') return String(this._idx);
      if (k === 'data-k') return LG_KEYS[this._idx] || '';
      return null;
    },
    querySelector(s) { return root.querySelector(s); },
    querySelectorAll(s) { return root.querySelectorAll(s); },
    getContext() { CTX = makeCtx(); return CTX; },
  };
  return el;
}
const cache = new Map();
const root = {
  _html: '',
  get innerHTML() { return this._html; },
  set innerHTML(v) { this._html = String(v); },
  querySelector(s) { if (!cache.has(s)) cache.set(s, mkEl(s, 0)); return cache.get(s); },
  querySelectorAll(s) {
    if (!cache.has('ALL' + s)) {
      cache.set('ALL' + s, s === '.mk-chip'
        ? Array.from({ length: n }, (_, i) => mkEl(s, i))
        : LG_KEYS.map((k, i) => mkEl(s, i)));
    }
    return cache.get('ALL' + s);
  },
};
let rafQ = [];
global.document = { querySelector: () => root, getElementById: () => null, createElement: () => mkEl('tmp', 0) };
global.requestAnimationFrame = (fn) => { rafQ.push(fn); return rafQ.length; };
function pump(k, t0) { for (let i = 0; i < k; i++) { const q = rafQ.splice(0); q.forEach(f => f((t0 || 0) + i * 16.7)); } }
function ops() { return CTX ? Object.values(CTX.calls).reduce((a, b) => a + b, 0) : 0; }

/* ── 执行 ──────────────────────────────────────────────── */
let renderFn;
try {
  renderFn = new Function('MIAOYAN_KP', src + '\nreturn renderMiaoyanKeypoints;')(MIAOYAN_KP);
} catch (e) {
  console.error('FAIL: renderer threw on load — ' + e.message + '\n' + e.stack); process.exit(1);
}
if (typeof renderFn !== 'function') { console.error('FAIL: not a function'); process.exit(1); }
try { renderFn('#article-kp'); }
catch (e) { console.error('FAIL: render() threw — ' + e.message + '\n' + e.stack); process.exit(1); }

/* ── 静态产物校验（不损之保证）────────────────────────── */
const H = root.innerHTML;
if (H.length < 2000) errs.push('innerHTML too short: ' + H.length);
for (const s of ['mk-play', 'mk-prev', 'mk-next', 'mk-speed', 'mk-seek',
  'mk-layers', 'mk-cv', 'mk-chips', 'mk-panel', 'mk-legend', 'mk-all']) {
  if (!H.includes(s)) errs.push('missing element/class: ' + s);
}
const chips = (H.match(/class="mk-chip[" ]/g) || []).length;  // [" ] 以免误计容器 mk-chips
if (chips !== n) errs.push('chips=' + chips + ', expected ' + n);
const cards = (H.match(/class="mk-card"/g) || []).length;
if (cards !== n) errs.push('full-text cards=' + cards + ', expected ' + n);
if (!/width="960" height="600"/.test(H)) errs.push('canvas size not set');
for (const leak of ['undefined', 'NaN', '[object Object]']) {
  if (H.includes(leak)) errs.push('leak in innerHTML: ' + leak);
}
// ── 不损保证（逐字段核验）：每一要点之全部作者内容字段，皆须在静态清单中原样可查 ──
// 渲染器以 esc() 转义后再写入，故核验时同法转义（& < > "），避免因字符差异误报。
const escH = (t) => String(t == null ? '' : t)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;')
  .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const layerById = {}; (frame.layers || []).forEach(l => { layerById[l.id] = l; });
for (const k of kps) {
  const tag = 'kp' + (k.idx || '?');
  // 正文内容：中英标题、中英要旨、经文原句、出处——皆不得丢
  const contentFields = ['title_zh', 'title_en', 'gist_zh', 'gist_en', 'quote_zh', 'ref'];
  for (const f of contentFields) {
    if (k[f] && !H.includes(escH(k[f]))) errs.push('static list missing ' + f + ': ' + tag);
  }
  // 判断（T2）必与其文字同现
  if (k.judgment && k.judgment_zh && !H.includes(escH(k.judgment_zh))) errs.push('judgment missing: ' + tag);
  // 结构元数据：所属层名、方位 point_at、时长 duration_s、抽象小图 icon——逐条透出
  const lay = layerById[k.layer] || {};
  if (lay.label_zh && !H.includes(escH(lay.label_zh))) errs.push('static list missing register label: ' + tag);
  if (Array.isArray(k.point_at) && !H.includes(escH(k.point_at.join(', ')))) errs.push('static list missing point_at: ' + tag);
  if (k.duration_s != null && !H.includes(escH(k.duration_s))) errs.push('static list missing duration: ' + tag);
  if (k.icon && !H.includes(escH(k.icon))) errs.push('static list missing icon path: ' + tag);
}
// 全局元信息不得丢：版本/状态/回源核验、框架标题与周匝概念、图标声明、图例中英、closer 中英、出处
const M = MIAOYAN_KP.meta || {};
for (const [f, v] of Object.entries({ version: M.version, status: M.status, title_zh: M.title_zh, note_zh: M.note_zh, icon_note_zh: M.icon_note_zh }))
  if (v && !H.includes(escH(v))) errs.push('meta.' + f + ' missing');
if (frame.title_zh && !H.includes(escH(frame.title_zh))) errs.push('frame.title_zh missing');
if (frame.sweep_zh && !H.includes(escH(frame.sweep_zh))) errs.push('frame.sweep_zh missing');
for (const ev of ['T0', 'T1', 'T2']) {
  const lv = evLevels[ev]; if (!lv) continue;
  for (const f of ['label_zh', 'label_en', 'rule_zh', 'rule_en'])
    if (lv[f] && !H.includes(escH(lv[f]))) errs.push('legend ' + ev + ' missing ' + f);
}
if (MIAOYAN_KP.closer && MIAOYAN_KP.closer.zh && !H.includes(escH(MIAOYAN_KP.closer.zh)))
  errs.push('closer.zh missing');
if (MIAOYAN_KP.closer && MIAOYAN_KP.closer.en && !H.includes(escH(MIAOYAN_KP.closer.en)))
  errs.push('closer.en missing');
if (frame.disclaimer_zh && !H.includes(escH(frame.disclaimer_zh))) errs.push('disclaimer missing');
if (M.source_url && !H.includes(M.source_url)) errs.push('source link missing');

/* ── 交互驱动 ──────────────────────────────────────────── */
const c = (s) => root.querySelector(s);
for (const s of ['.mk-play', '.mk-prev', '.mk-next']) {
  if (c(s).nHandlers('click') < 1) errs.push('no click handler: ' + s);
}
if (c('.mk-seek').nHandlers('input') < 1) errs.push('no input handler: .mk-seek');
if (c('.mk-speed').nHandlers('change') < 1) errs.push('no change handler: .mk-speed');
const chipEls = root.querySelectorAll('.mk-chip');
if (chipEls.some(e => e.nHandlers('click') < 1)) errs.push('chip missing click handler');
const lgs = root.querySelectorAll('.mk-lg');
if (lgs.some(e => e.nHandlers('change') < 1)) errs.push('layer toggle missing handler');

// 面板首点内容
pump(3, 0);
const panel = c('.mk-panel'), cur = c('.mk-cur');
if (!H || panel.innerHTML.indexOf(kps[0].title_zh) < 0) errs.push('panel did not render point 1');
const ops0 = ops();
if (!(ops0 > 0)) errs.push('no canvas ops on first paint');

// 播放 → 时钟推进
c('.mk-play').fire('click');
pump(40, 100);
if (!(ops() > ops0)) errs.push('no further canvas ops while playing');
if (!(parseFloat(cur.textContent) > 0)) errs.push('clock did not advance: ' + cur.textContent);
if (!/⏸/.test(c('.mk-play').innerHTML)) errs.push('play label did not switch to pause');
c('.mk-play').fire('click');
const paused = cur.textContent;
pump(20, 200);
if (cur.textContent !== paused) errs.push('clock advanced while paused');

// 下一点 / 上一点
c('.mk-next').fire('click');
if (panel.innerHTML.indexOf(kps[1].title_zh) < 0) errs.push('next point failed');
c('.mk-prev').fire('click');
if (panel.innerHTML.indexOf(kps[0].title_zh) < 0) errs.push('prev point failed');

// 跳点（第 5 点）
chipEls[4].fire('click');
if (panel.innerHTML.indexOf(kps[4].title_zh) < 0) errs.push('chip jump failed');

// 进度条 seek 到 90%（应落在靠后之点）
const sk = c('.mk-seek'); sk.value = '900'; sk.fire('input'); pump(2, 300);
if (!(parseFloat(cur.textContent) > 0)) errs.push('seek did not move clock');

// 倍速
const sp = c('.mk-speed'); sp.value = '2'; sp.fire('change');
c('.mk-play').fire('click'); pump(20, 400); c('.mk-play').fire('click');

// 图层开关（四项皆切换且不出错）
for (let i = 0; i < lgs.length; i++) {
  lgs[i].checked = false; lgs[i].fire('change', { target: lgs[i] });
  lgs[i].checked = true; lgs[i].fire('change', { target: lgs[i] });
}

// 逐点走完全程
chipEls.forEach(e => e.fire('click'));
pump(5, 1000);

/* ── 汇总 ──────────────────────────────────────────────── */
if (errs.length) {
  console.error('FAIL (' + errs.length + '):');
  errs.forEach(e => console.error('  - ' + e));
  process.exit(1);
}
// 此行须保持纯 ASCII —— verify_demo 以 locale 编码读取 node 输出。
console.log('OK: keypoints render - ' + n + ' points, ' + layers.length +
  ' registers, all quotes verbatim in T279 (tag+ws normalized), judgment pairs balanced, ' +
  'static list has ' + cards + ' cards, canvas ' + ops() +
  ' ops; play/pause/next/prev/chip/seek/speed/layers driven; no leaks');
