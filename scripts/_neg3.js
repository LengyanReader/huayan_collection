// 叙事动画渲染冒烟测试：在 Node 中以最小 DOM + Canvas 桩执行 build 产物内联的
// MiaoyanNarrative / renderMiaoyanNarrative，校验其无运行时异常、各控件皆出、
// 播放/暂停/步进/跳拍/图层/进度皆可驱动，且无 undefined/NaN/[object Object] 泄漏。
// （浏览器 CDP 本机不可用，故以桩执行求「逻辑真跑」；像素级渲染仍待真机复验。）
const fs = require('fs');
const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');
const errs = [];

/* ── 抽取数据与源码 ─────────────────────────────────────── */
const md = html.match(/var MIAOYAN_NARR = (\{[\s\S]*?\});<\/script>/);
if (!md) { console.error('FAIL: MIAOYAN_NARR not found in ' + file); process.exit(1); }
const MIAOYAN_NARR = JSON.parse(md[1]);

const si = html.indexOf('var MiaoyanNarrative = (function(){');
const ei = html.indexOf('function renderMiaoyanNarrative(containerId){');
if (si < 0 || ei < 0) { console.error('FAIL: narrative renderer not found'); process.exit(1); }
const ri = html.lastIndexOf('return { render: render };', ei);
const se = html.indexOf('\n}', ri);
const we = html.indexOf('\n}', ei);
if (ri < 0 || se < 0 || we < 0) { console.error('FAIL: source bounds not found'); process.exit(1); }
const src = html.slice(si, we + 2);

/* ── 数据层不变量（先于渲染校验）───────────────────────── */
const rings = (MIAOYAN_NARR.space && MIAOYAN_NARR.space.rings) || [];
const sumCls = rings.reduce((a, r) => a + (r.member_classes || 0), 0);
const sumMem = rings.reduce((a, r) => a + (r.member_count || 0), 0);
if (sumCls !== 40) errs.push('member_classes sum = ' + sumCls + ', expected 40');
if (sumMem !== 414) errs.push('member_count sum = ' + sumMem + ', expected 414');
const beats = MIAOYAN_NARR.beats || [];
if (beats.length !== 11) errs.push('beats = ' + beats.length + ', expected 11');
for (const b of beats) {
  if (!(b.time_end_s > b.time_start_s)) errs.push('beat ' + b.id + ' bad time range');
  if (!b.narration_zh || !b.narration_en) errs.push('beat ' + b.id + ' missing zh/en narration');
  if (!/T10n0279|T279|miaoyan_assembly/.test(b.narration_ref || ''))
    errs.push('beat ' + b.id + ' ref not traceable: ' + b.narration_ref);
}

/* ── 最小 DOM + Canvas 桩（元素按选择器记忆化，方可事后取控件）── */
let CTX = null;
function makeCtx() {
  const calls = Object.create(null);
  const target = {
    calls,                       // 须置于 target：否则 Proxy 会当成 ctx 方法返回录制函数
    createRadialGradient: () => ({ addColorStop: () => {} }),
    canvas: { width: 960, height: 620 },
  };
  return new Proxy(target, {
    get(t, p) { if (p in t) return t[p]; return (...a) => { calls[p] = (calls[p] || 0) + 1; }; },
    set(t, p, v) { t[p] = v; return true; },
    has() { return true; },
  });
}
function mkEl(sel, idx) {
  const h = {};
  const el = {
    _html: '', _sel: sel, _idx: idx,
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    textContent: '', className: '', style: {}, dataset: {},
    addEventListener(t, f) { (h[t] = h[t] || []).push(f); },
    fire(t, ev) { (h[t] || []).forEach(f => f.call(el, ev || {})); return (h[t] || []).length; },
    nHandlers(t) { return (h[t] || []).length; },
    getAttribute(k) {
      if (k === 'data-i') return String(this._idx);
      if (k === 'data-k') return ['grid', 'dots', 'labels', 'en'][this._idx] || '';
      return null;
    },
    querySelector(s) { return root.querySelector(s); },
    querySelectorAll(s) { return root.querySelectorAll(s); },
    getContext() { CTX = makeCtx(); return CTX; },
  };
  return el;
}
const cache = new Map();
const LG_KEYS = ['grid', 'dots', 'labels', 'en'];
const root = {
  _html: '',
  get innerHTML() { return this._html; },
  set innerHTML(v) { this._html = String(v); },
  querySelector(s) {
    if (!cache.has(s)) cache.set(s, mkEl(s, 0));
    return cache.get(s);
  },
  querySelectorAll(s) {
    // 须记忆化：否则渲染时绑定之 handler 与事后取得之对象非同一实例
    if (!cache.has('ALL' + s)) {
      cache.set('ALL' + s, s === '.mn-chip'
        ? Array.from({ length: beats.length }, (_, i) => mkEl(s, i))
        : LG_KEYS.map((k, i) => mkEl(s, i)));
    }
    return cache.get('ALL' + s);
  },
};
let rafQ = [];
global.document = { querySelector: () => root, getElementById: () => null, createElement: () => mkEl('tmp', 0) };
global.requestAnimationFrame = (fn) => { rafQ.push(fn); return rafQ.length; };
function pump(n, t0) {
  for (let i = 0; i < n; i++) {
    const q = rafQ.splice(0);
    q.forEach(f => f((t0 || 0) + i * 16.7));
  }
}
function ops() { return CTX ? Object.values(CTX.calls).reduce((a, b) => a + b, 0) : 0; }

/* ── 执行 ──────────────────────────────────────────────── */
let renderFn;
try {
  renderFn = new Function('MIAOYAN_NARR', src + '\nreturn renderMiaoyanNarrative;')(MIAOYAN_NARR);
} catch (e) {
  console.error('FAIL: renderer threw on load — ' + e.message + '\n' + e.stack); process.exit(1);
}
if (typeof renderFn !== 'function') { console.error('FAIL: not a function'); process.exit(1); }

try { renderFn('#article-narrative'); }
catch (e) { console.error('FAIL: render() threw — ' + e.message + '\n' + e.stack); process.exit(1); }

/* ── 静态产物校验 ─────────────────────────────────────── */
const H = root.innerHTML;
if (H.length < 1500) errs.push('innerHTML too short: ' + H.length);
for (const s of ['mn-play', 'mn-prev', 'mn-next', 'mn-speed', 'mn-seek',
  'mn-layers', 'mn-cv', 'mn-beats', 'mn-narr']) {
  if (!H.includes(s)) errs.push('missing control: ' + s);
}
const chips = (H.match(/class="mn-chip/g) || []).length;
if (chips !== beats.length) errs.push('chips = ' + chips + ', expected ' + beats.length);
if (!/width="960" height="620"/.test(H)) errs.push('canvas size not set');
for (const leak of ['undefined', 'NaN', '[object Object]']) {
  if (H.includes(leak)) errs.push('leak in innerHTML: ' + leak);
}
if (!H.includes('cbetaonline.dila.edu.tw/zh/T10n0279')) errs.push('T10n0279 source link missing');
if (!H.includes('不可尽言')) errs.push('calibration note missing');
if (!/= 414/.test(H)) errs.push('414 calibration not shown');
if (/Mahādevī/.test(H)) errs.push('stray title leaked into page');
if (/T09n0279/.test(H.replace(/[^]*?仅作对照[^]*?T09n0279/, ''))) {
  // 允许 meta.sources 中「仅作对照」那一处，旧译不得作底本
  const hits = (H.match(/T09n0279/g) || []).length;
  if (hits > 2) errs.push('T09n0279 appears ' + hits + ' times (expect label+url only)');
}

/* ── 交互驱动 ──────────────────────────────────────────── */
const c = (s) => root.querySelector(s);
for (const s of ['.mn-play', '.mn-prev', '.mn-next']) {
  if (c(s).nHandlers('click') < 1) errs.push('no click handler: ' + s);
}
if (c('.mn-seek').nHandlers('input') < 1) errs.push('no input handler: .mn-seek');
if (c('.mn-speed').nHandlers('change') < 1) errs.push('no change handler: .mn-speed');
for (const k of LG_KEYS) {
  const lg = root.querySelectorAll('.mn-lg')[LG_KEYS.indexOf(k)];
  if (lg.nHandlers('change') < 1) errs.push('no change handler: layer ' + k);
}
const chipEls = root.querySelectorAll('.mn-chip');
if (chipEls.some(e => e.nHandlers('click') < 1)) errs.push('chip missing click handler');

// 首拍：时钟与旁白
pump(3, 0);
const nt = c('.mn-nt'), nz = c('.mn-nz'), ne = c('.mn-ne'), meta = c('.mn-nmeta'), cur = c('.mn-cur');
if (!beats[0].title_zh.includes(nt.textContent.split('  ·')[0]))
  errs.push('beat0 title mismatch: ' + nt.textContent);
if (!beats[0].narration_zh.includes(nz.textContent.replace(/<\/?b>/g, '')))
  errs.push('beat0 narration mismatch');
if (beats[0].narration_en !== ne.textContent) errs.push('beat0 EN narration mismatch');
// 渲染器以 innerHTML 写入旁白/按钮/元信息，故桩校验亦读 innerHTML
if (!/T10n0279|assembly/.test(meta.innerHTML)) errs.push('beat0 ref not shown');
if (!/存疑/.test(meta.innerHTML)) errs.push('beat0 uncertainty not shown');

const ops0 = ops();
if (!(ops0 > 0)) errs.push('no canvas ops on first paint');

// 播放 → 时钟推进
c('.mn-play').fire('click');           // → 播放
pump(40, 100);
if (!(ops() > ops0)) errs.push('no further canvas ops while playing');
if (parseFloat(cur.textContent) <= 0) errs.push('clock did not advance: ' + cur.textContent);
if (!/⏸/.test(c('.mn-play').innerHTML)) errs.push('play button label did not switch to pause');
c('.mn-play').fire('click');           // → 暂停
const paused = cur.textContent;
pump(20, 200);
if (cur.textContent !== paused) errs.push('clock advanced while paused');

// 下一拍 / 上一拍
c('.mn-next').fire('click');
if (!beats[1].title_zh.includes(nt.textContent.split('  ·')[0]))
  errs.push('next beat failed: ' + nt.textContent);
if (!beats[1].narration_en.includes(ne.textContent) && ne.textContent !== beats[1].narration_en)
  errs.push('next beat EN mismatch');
c('.mn-prev').fire('click');
if (!beats[0].title_zh.includes(nt.textContent.split('  ·')[0]))
  errs.push('prev beat failed: ' + nt.textContent);

// 直接跳拍（第 5 拍 = 法界/上层相关）
chipEls[5].fire('click');
if (!beats[5].title_zh.includes(nt.textContent.split('  ·')[0]))
  errs.push('chip jump failed: ' + nt.textContent);

// 进度条 seek 到 70%（总时长 32s，70% = 22.4s → 落 B7 区间 22.0–24.5）
const sk = c('.mn-seek');
sk.value = '700';
sk.fire('input');
pump(2, 300);
if (!beats[7].title_zh.includes(nt.textContent.split('  ·')[0]))
  errs.push('seek 70% should land in B7 (22.4s), got: ' + nt.textContent);

// 倍速
const sp = c('.mn-speed');
sp.value = '2';
sp.fire('change');
c('.mn-play').fire('click');
pump(30, 400);
c('.mn-play').fire('click');

// 图层开关（四项皆应可切换且不出错）
for (const k of ['grid', 'dots', 'labels', 'en']) {
  const lg = root.querySelectorAll('.mn-lg')[LG_KEYS.indexOf(k)];
  lg.checked = false; lg.fire('change', { target: lg });
  lg.checked = true;  lg.fire('change', { target: lg });
}

// 逐拍走完全程，确认每一拍皆出图、无异常
chipEls.forEach(e => e.fire('click'));
pump(5, 1000);

/* ── 汇总 ──────────────────────────────────────────────── */
if (errs.length) {
  console.error('FAIL (' + errs.length + '):');
  errs.forEach(e => console.error('  - ' + e));
  process.exit(1);
}
// 注意：此行须保持纯 ASCII —— verify_demo 以 locale 编码读取 node 输出，
// 非 ASCII 会致 decode 失败、stdout 变 None，而门禁仍显示 OK（空消息）。
console.log('OK: narrative render - ' + beats.length + ' beats, rings ' + sumCls +
  ' classes/' + sumMem + ' named, canvas ' + ops() +
  ' ops; play/pause/next/prev/chip/seek/speed/layers all driven; ' +
  'refs+uncertainty shown; no leaks');