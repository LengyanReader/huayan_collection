// 分镜总览门禁（Node）：以最小 DOM + Canvas 桩**真跑** build 产物内联的
// MiaoyanStoryboard / renderMiaoyanStoryboard，校验
//   ① 挂载壳（article.js 生成 #article-sb 折叠壳并挂载渲染器——L.116 起分镜不在 doc 正文内）
//   ② 数据层不变量（meta.expected 锚点对账；镜号连续／drift 三轴／景别运镜皆注册／判断齐备）
//   ③ 播放·暂停·步进·跳镜·跳幕·进度·倍速·四图层皆可驱动，且无 undefined/NaN 泄漏
// 浏览器 CDP 本机不可用，故以桩执行求「逻辑真跑」；像素级渲染仍待真机复验。
const fs = require('fs');
const ART = process.argv[2] || 'web/demo/articles/shizhu-miaoyan.html';
const JS = process.argv[3] || 'web/demo/js/common.js';
const html = fs.readFileSync(ART, 'utf8');
const errs = [];
const ok = (c, m) => { if (!c) errs.push(m); };

/* ══ 一、数据层 ══════════════════════════════════════════ */
const md = html.match(/var MIAOYAN_SB = (\{[\s\S]*?\});<\/script>/);
if (!md) { console.error('FAIL: MIAOYAN_SB not found in ' + ART); process.exit(1); }
const SB = JSON.parse(md[1]);
const NARRm = html.match(/var MIAOYAN_NARR = (\{[\s\S]*?\});<\/script>/);
const NARR = NARRm ? JSON.parse(NARRm[1]) : null;

const acts = SB.acts || [];
const flat = [].concat.apply([], acts.map(a => a.shots || []));
/* 契约锚点取自数据自身 meta.expected（L.116 立）——防「改了数据而门禁不察」。
   expected 缺则门禁无效：宁失败，勿以硬编码旧数充当校验。 */
const exp = (SB.meta || {}).expected || {};
ok(exp.acts != null, 'meta.expected.acts missing — anchors required');
ok(exp.shots != null, 'meta.expected.shots missing — anchors required');
ok(exp.seconds != null, 'meta.expected.seconds missing — anchors required');
ok(acts.length === exp.acts, 'acts = ' + acts.length + ', expected ' + exp.acts + ' (meta.expected)');
ok(flat.length === exp.shots, 'shots = ' + flat.length + ', expected ' + exp.shots + ' (meta.expected)');

/* 时长对账：逐镜合计须等于锚点声明（幕级 duration 已并入逐镜计算，不再单列）*/
const sumShot = flat.reduce((a, s) => a + s.duration_s, 0);
ok(Math.abs(sumShot - exp.seconds) < 1e-6,
  `duration mismatch: shots ${sumShot} vs meta.expected ${exp.seconds}`);
for (const a of acts) {
  const ad = (a.shots || []).reduce((x, s) => x + s.duration_s, 0);
  ok(ad > 0, 'act ' + a.no + ' has zero total duration');
}

/* 镜号连续 1..N 且全局唯一 */
const nos = flat.map(s => s.no);
ok(nos.join(',') === Array.from({ length: exp.shots }, (_, i) => i + 1).join(','),
  'shot numbers not contiguous 1..' + exp.shots + ': ' + nos.join(','));
ok(new Set(nos).size === exp.shots, 'duplicate shot numbers');

/* 景别与运镜皆注册；drift 必须三轴（推拉/横移/升降不可串轴）*/
const SIZES = SB.shot_sizes || {}, MOVES = SB.camera_moves || {};
for (const s of flat) {
  ok(SIZES[s.size], 'shot ' + s.no + ' unregistered size: ' + s.size);
  ok(MOVES[s.move], 'shot ' + s.no + ' unregistered move: ' + s.move);
  ok(/^[T卷]/.test(s.ref || ''), 'shot ' + s.no + ' untraceable ref: ' + s.ref);
  ok(s.quote_zh && s.quote_en && s.subtitle_zh && s.subtitle_en,
    'shot ' + s.no + ' missing zh/en');
  /* 凡标〔本文判断〕者必自陈其判断内容——否则等于以重构冒经文 */
  if (s.reconstruction) ok(s.judgment_zh && s.judgment_zh.length > 8,
    'shot ' + s.no + ' marked reconstruction without judgment');
  ok(Array.isArray(s.focus) && s.focus.length > 0, 'shot ' + s.no + ' has no focus prop');
}
for (const k of Object.keys(MOVES)) {
  ok(Array.isArray(MOVES[k].drift) && MOVES[k].drift.length === 3,
    'move ' + k + ' drift must be 3-axis [dz,dx,dy], got ' + JSON.stringify(MOVES[k].drift));
}

/* 幕内镜头之 focus/subject 必为本幕 props 所实有——不得指向不存在的图元。
   subject 允许 null：全镜总览（如第 1 镜）本无单一主体，如实留空而非硬指某元。 */
for (const a of acts) {
  const ids = new Set((a.props || []).map(p => p.id));
  for (const s of a.shots || []) {
    ok(s.subject === null || ids.has(s.subject),
      'shot ' + s.no + ' subject not in act props: ' + s.subject);
    for (const f of s.focus || [])
      ok(ids.has(f), 'shot ' + s.no + ' focus not in act props: ' + f);
  }
}
ok(flat.some(s => s.subject === null), 'no establishing shot with null subject — '
  + '全镜总览应如实留空 subject，而非硬指某一要素');
ok((SB.corrections || []).length === exp.corrections,
  'corrections = ' + (SB.corrections || []).length + ', expected ' + exp.corrections + ' (meta.expected)');

/* 机位须真作用于要素坐标：若 pan/zoom 只动背景而不动图元，
   则「平移摇摄」在画面上等于不动——运镜沦为装饰。故须有两镜之
   要素坐标确实随镜头而异（drift 不同 → 变换后坐标必不同）。*/
{
  const sA = flat.find(s => s.drift_zoom || (MOVES[s.move] || {}).drift || [0, 0, 0]);
  ok(!!sA, 'no shot carries camera drift');
}

/* 合幕曼荼罗须为全片唯一，且环位数据在场（一点＝一类之口径由 MIAOYAN_NARR.space.rings 供）*/
const mand = [];
for (const a of acts) for (const p of a.props || []) if (p.kind === 'mandala') mand.push(a.no);
ok(mand.length === 1 && mand[0] === '合',
  'mandala prop must appear exactly once, in the coda act; got ' + JSON.stringify(mand));
if (NARR && NARR.space) {
  const sumCls = (NARR.space.rings || []).reduce((a, r) => a + (r.member_classes || 0), 0);
  ok(sumCls === 40, 'mandala ring classes sum = ' + sumCls + ', expected 40');
}

/* ══ 二、挂载壳：分镜面板由 article.js 以折叠壳 #article-sb 生成于正文之外 ══
   （L.116 起分镜不再置于 doc 正文内，故不校 doc 占位与章节重编号；
    改校构建产物确含①壳之生成 ②renderMiaoyanStoryboard 之挂载——缺一则分镜无从现身。）*/
ok(html.indexOf("_foldShellHtml('article-sb'") >= 0
  || html.indexOf('_foldShellHtml("article-sb"') >= 0,
  'article chrome does not create the #article-sb fold shell');
ok(html.indexOf('renderMiaoyanStoryboard') >= 0,
  'renderMiaoyanStoryboard mount call absent from built page');
ok(html.indexOf("document.getElementById('article-sb')") >= 0
  || html.indexOf('document.getElementById("article-sb")') >= 0,
  'built page does not guard the storyboard mount on #article-sb existence');

/* ══ 三、最小 DOM + Canvas 桩 ═════════════════════════════ */
let CTX = null;
function makeCtx() {
  const calls = Object.create(null);
  const target = {
    calls,
    createRadialGradient: () => ({ addColorStop: () => {} }),
    canvas: { width: 960, height: 480 },
  };
  return new Proxy(target, {
    get(t, p) {
      if (p in t) return t[p];
      return (...a) => {
        calls[p] = (calls[p] || 0) + 1;
        /* 只记要素落点之 translate（背景光网之 arc/lineTo 不在其列）*/
        if (p === 'translate' && typeof a[0] === 'number' && typeof a[1] === 'number') {
          /* 记当前 strokeStyle：焦点图元用 gold、其余用 lapis/ash，
             由此可据颜色认出「焦点图元」，无须依赖图元次序 */
          tr.push(['translate', a[0], a[1], String(this.strokeStyle || '')]);
        }
        return undefined;
      };
    },
    set(t, p, v) { t[p] = v; return true; },
    has() { return true; },
  });
}
function mkEl(sel, idx, ds) {
  const h = {};
  const el = {
    _html: '', _sel: sel, _idx: idx, _ds: ds || {},
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    get dataset() { return this._ds; },
    textContent: '', className: '', value: '0', hidden: false,
    style: {}, checked: true, parentNode: null,
    get classList() {
      const self = this;
      return { toggle() {}, add() {}, remove() {}, contains() { return false; } };
    },
    addEventListener(t, f) { (h[t] = h[t] || []).push(f); },
    fire(t, ev) { (h[t] || []).forEach(f => f.call(el, ev || {})); return (h[t] || []).length; },
    nHandlers(t) { return (h[t] || []).length; },
    appendChild(c) { (this._kids = this._kids || []).push(c); return c; },
    querySelector(s) { return root.querySelector(s); },
    querySelectorAll(s) { return root.querySelectorAll(s); },
    getContext() { CTX = makeCtx(); return CTX; },
    closest(c) { return this._closest === c ? this : null; },
  };
  el.parentNode = { clientWidth: 960 };
  return el;
}
const cache = new Map();
/* translate 实参表：供「运镜是否真作用于要素坐标」之核验取样 */
const tr = [];
/* 分镜格由 renderer 以 document.createElement 造出后 appendChild 入 sheet，
   不经 innerHTML，故须另记一线，querySelectorAll('…__cell') 方能返其真身 */
const realCells = [];
const root = {
  _html: '',
  get innerHTML() { return this._html; },
  set innerHTML(v) { this._html = String(v); },
  querySelector(s) {
    if (!cache.has(s)) cache.set(s, mkEl(s, 0));
    return cache.get(s);
  },
  querySelectorAll(s) {
    const key = 'ALL' + s;
    if (cache.has(key)) return cache.get(key);
    let arr;
    if (s.indexOf('__cell') >= 0) {
      if (realCells.length) arr = realCells;
      else arr = Array.from({ length: flat.length }, (_, i) => mkEl(s, i, { i: String(i) }));
    } else if (s.indexOf('__act') >= 0) {
      arr = acts.map((a, i) => mkEl(s, i, { act: String(i) }));
    } else {
      arr = [];
    }
    cache.set(key, arr);
    return arr;
  },
};
let rafQ = [];
global.document = {
  querySelector: () => root,
  querySelectorAll: (s) => root.querySelectorAll(s),
  getElementById: () => null,
  createElement: () => {
    const e = mkEl('cell', realCells.length, { i: String(realCells.length) });
    realCells.push(e);
    return e;
  },
  activeElement: null,
};
global.window = global;
global.addEventListener = () => {};
global.removeEventListener = () => {};
global.requestAnimationFrame = (fn) => { rafQ.push(fn); return rafQ.length; };
/* 假时钟：渲染器以 performance.now() 推算播放位置，若任其取真实时间，
   则同步 pump 内 now()-t0 ≈ 0，播放「看似推进而实则不动」，
   倍速与时基之病皆测不出来。故须随 pump 逐帧推进。*/
let VT = 0;
global.performance = { now: () => VT };
function pump(n) {
  for (let i = 0; i < n; i++) { VT += 16.7; rafQ.splice(0).forEach(f => f(VT)); }
}
function ops() { return CTX ? Object.values(CTX.calls).reduce((a, b) => a + b, 0) : 0; }
/* 归位至首镜（供各段测试后复位，免相互污染）*/
function go0() { const sk = $('#sb-seek'); sk.value = '0'; sk.oninput(); }
const $ = s => root.querySelector(s);

/* ══ 四、执行渲染器 ══════════════════════════════════════ */
/* 抽取边界须与产物形态一致：渲染器为 `(function (global) { … })(typeof window…)` 之 IIFE，
   故自 IIFE 头部取至其收尾，而非 `var X = (function…` 之类 */
const si = html.indexOf('(function (global) {');
const ei = html.indexOf('})(typeof window', si);
if (si < 0 || ei < 0) { console.error('FAIL: storyboard renderer not found'); process.exit(1); }
const src = html.slice(si, ei + '})(typeof window !== \'undefined\' ? window : this);'.length);
ok(src.indexOf('renderMiaoyanStoryboard') > 0, 'extracted source lacks renderMiaoyanStoryboard');
ok(src.indexOf('MiaoyanStoryboard') > 0, 'extracted source lacks MiaoyanStoryboard');

/* 须挂到 globalThis 而非用 new Function 形参：渲染器内部读 `global.MIAOYAN_SB`，
   而其 `global` 即 `window`（本桩中 window = globalThis）。以形参传入则读到 undefined，
   渲染器会静默 return —— 那正是「假绿」的来源。 */
globalThis.window = globalThis;
globalThis.MIAOYAN_SB = SB;
globalThis.MIAOYAN_NARR = NARR;
let renderFn;
try {
  renderFn = new Function(src + '\nreturn renderMiaoyanStoryboard;')();
} catch (e) {
  console.error('FAIL: renderer threw on load — ' + e.message + '\n' + e.stack); process.exit(1);
}
try { renderFn('#article-sb'); }
catch (e) { console.error('FAIL: render() threw — ' + e.message + '\n' + e.stack); process.exit(1); }

/* ══ 五、控件齐备与驱动 ══════════════════════════════════ */
const H = root.innerHTML;
ok(H.length > 3000, 'innerHTML too short: ' + H.length);
for (const s of ['sb-play', 'sb-prev', 'sb-next', 'sb-speed', 'sb-seek', 'sb-l-props',
  'sb-l-labels', 'sb-l-en', 'sb-l-frame', 'sb-sheet', 'sb-sub', 'sb-q',
  'sb-ref', 'sb-no', 'sb-size', 'sb-move', 'sb-judge', 'miaoyan-sb__corr'])
  ok(H.indexOf(s) >= 0, 'control/panel missing from DOM: ' + s);
ok(H.indexOf('miaoyan-sb__cv') >= 0, 'canvas missing from DOM');
/* 分镜表：26 格，且每格皆出镜号·幕·景别·运镜·字幕（取自 sheet 之实子元素）*/
const cells = $('#sb-sheet')._kids || [];
ok(cells.length === 26, 'storyboard sheet cells = ' + cells.length + ', expected 26');
ok(cells.every((c, i) => c.innerHTML.indexOf('>' + (i + 1) + '<') >= 0),
  'sheet cell missing its shot number');
ok(cells.every(c => c.innerHTML.indexOf('miaoyan-sb__cellSize') >= 0),
  'sheet cell missing shot size');

/* 首镜初始态 */
ok($('#sb-no').textContent.indexOf('1') >= 0, 'slate did not show shot 1');
ok(!!$('#sb-q').textContent, 'quote panel empty at shot 1');
ok($('#sb-ref').textContent.indexOf('出处') === 0, 'ref panel malformed');
ok($('#sb-sub').textContent.length > 0, 'subtitle empty at shot 1');

/* 逐控件驱动：先验 handler 存在，再调用——缺失即记错并跳过，
   免得 TypeError 掩盖后续检查（崩溃虽亦非零码，但覆盖范围会被截断） */
function tap(sel, ev, label) {
  const b = $(sel);
  if (typeof b[ev] !== 'function') { errs.push('control has no ' + ev + ' handler: ' + label); return false; }
  b[ev]();
  return true;
}

/* 播放 → 时间推进、按钮改字、canvas 真画 */
const before = ops();
tap('#sb-play', 'onclick', '播放');
ok($('#sb-play').textContent.indexOf('暂停') >= 0, 'play button did not switch to pause');
pump(12);
ok(parseFloat($('#sb-t').textContent.replace(':', '')) !== 0 || ops() > before,
  'playback did not advance / did not paint');
ok(ops() > 200, 'canvas ops too low: ' + ops() + ' — renderer may not be drawing');

/* 总时长须真显示（片长 02:01）——空着即控件残缺 */
ok(/^\d\d:\d\d$/.test($('#sb-d').textContent), 'total duration blank: "' + $('#sb-d').textContent + '"');
ok($('#sb-d').textContent === '02:01', 'total duration shown as ' + $('#sb-d').textContent);

/* 归零须三方对平：进度条归零，画面时钟亦须归零。*/
{
  const sp = $('#sb-speed');
  const sk = $('#sb-seek');
  sp.value = '1'; sp.onchange();
  /* 先确保处于暂停态（按钮读数即状态：播放中显「暂停」）。
     否则前段遗留之「播放中」会被本段第一次点击反转为暂停，
     后续 pump 自然不动——门禁自身之状态污染，必先排除。*/
  const isPlaying = () => $('#sb-play').textContent.indexOf('暂停') >= 0;
  if (isPlaying()) tap('#sb-play', 'onclick', '暂停');
  ok(!isPlaying(), 'could not reach paused state');
  sk.value = '0'; sk.oninput();
  ok(clock() === 0, 'seek to 0 does not reset the clock (readback ' + clock() + ')');
  /* 先播放一段（令时钟离开 0），再归零：此须仍为 0。
     须播逾 60 帧：时钟读数以 mm:ss 显示，不足一秒则读数恒为 00:00，
     「是否推进」将无从分辨——即门禁自身须避免假阴性。*/
  tap('#sb-play', 'onclick', '播放');
  pump(120);
  tap('#sb-play', 'onclick', '暂停');
  const played = clock();
  ok(played > 0, 'playback did not advance the clock (still ' + played
    + 's after 2s of frames)');
  sk.value = '0'; sk.oninput();
  ok(clock() === 0, 'after playing, seek to 0 leaves clock at ' + clock() + ' — '
    + 'anchor 漏除 speed，归零重播实为旧处续播');
  /* 倍速续播不得使既得进度跳变。此为 anchor() 之枢：t0 记「未加速之真实秒」，
     故 clock = (now-t0)/1000*speed 于续播瞬间必仍落在 clock 原值。
     旧法 t0 = now - clock*1000（漏除 speed）则续播瞬间 clock 变为 clock*speed：
     于 2× 下 30s 骤跳 60s —— 一按快放即须重新寻找进度。
     注意：speed=1 时新旧两式恒等，故此测非于 1× 而必于倍速下验之。*/
  sk.value = '30'; sk.oninput();
  ok(clock() === 30, 'seek to 30 failed (readback ' + clock() + ')');
  sp.value = '2'; sp.onchange();
  const atPause = clock();
  tap('#sb-play', 'onclick', '2× 续播');
  const afterResume = clock();
  ok(Math.abs(afterResume - atPause) <= 1, 'resuming at 2x jumped the clock: '
    + atPause + 's -> ' + afterResume + 's（t0 漏除 speed，续播即把进度乘一次倍速）');
  tap('#sb-play', 'onclick', '暂停');
  sp.value = '1'; sp.onchange();
  sk.value = '0'; sk.oninput();
}

/* 运镜须真作用于要素坐标：取两镜 drift 不同者，其要素落点必异。
   若渲染器只平移背景而不变换图元，此二坐标将完全相同（运镜沦为装饰）。*/
/* 时刻表：读 #sb-t 之 mm:ss（播放器未外露 clock，故取自其显示）。
   播放器亦未外露倍率，故由选项自身反读——须与画面同时钟对账。*/
function clock() {
  const m = /^(\d\d):(\d\d)$/.exec($('#sb-t').textContent);
  return m ? (+m[1]) * 60 + (+m[2]) : NaN;
}


/* 跳至某镜之内某时刻（经进度条 oninput → sync+draw），取该帧「焦点图元」之落点。
   同镜取两刻，方能证运镜真在镜内推移图元；跨镜相比则为幕间布局差异，与镜头变换无涉。
   取焦点图元而非「首个 translate」：首个 translate 可能属别幕之固定前导元素，
   恒居画心不动——以其为据则真运镜亦测不出（反向验证⑨ 即因此假绿）。*/
function pt(i, f) {
  tr.length = 0;
  const st = flat.slice(0, i).reduce((a, s) => a + s.duration_s, 0);
  const sk = $('#sb-seek');
  sk.value = String(st + flat[i].duration_s * f);
  sk.oninput();
  /* 取「焦点图元」之落点（焦点以 gold 描色，与余者 lapis/ash 异，可据色认）。
     不可取首个 translate：首个或属恒居画心之固定前导元素，则真运镜亦测不出
     ——反向验证⑨ 即因此假绿过一次。*/
  /* 焦点色为 PAL.gold = #d4a03c */
  const t = tr.find(o => /#d4a03c/i.test(o[3])) || tr[tr.length - 1] || tr[0];
  return t ? t[1] + ',' + t[2] : null;
}

/* 机位须真作用于要素坐标。
   判据取「同一镜之内，镜首与镜中之落点必异」：若渲染器只平移背景而不对
   图元作仿射，则该镜之内图元静止（stuck），运镜沦为装饰。*/
{
  let picked = -1;
  for (let i = 0; i < flat.length; i++) {
    const d = MOVES[flat[i].move].drift;
    if ((d[0] || d[1] || d[2]) && (flat[i].focus || []).length) { picked = i; break; }
  }
  ok(picked >= 0, 'no shot carries camera drift');
  if (picked >= 0) {
    const a = pt(picked, 0.05), b = pt(picked, 0.75);
    ok(a !== null && b !== null, 'prop coordinate not sampled (translate absent)');
    ok(a !== b, 'props do not move within shot ' + flat[picked].no
      + ' — camera drift transforms only the backdrop, so the move is decorative'
      + ' (' + a + ' vs ' + b + ')');
  }
  go0();
}

/* 步进 */
tap('#sb-next', 'onclick', '下一镜');
const n2 = $('#sb-no').textContent;
ok(n2.indexOf('2') >= 0, 'next shot did not advance (slate=' + n2 + ')');
tap('#sb-prev', 'onclick', '上一镜');
ok($('#sb-no').textContent.indexOf('1') >= 0, 'prev shot did not return');

/* 点格跳镜 */
const sheet = $('#sb-sheet');
ok(typeof sheet.onclick === 'function', 'sheet has no click handler');
if (cells[24] && typeof sheet.onclick === 'function') {
  cells[24]._closest = '.miaoyan-sb__cell';
  sheet.onclick({ target: cells[24] });
  ok($('#sb-no').textContent.indexOf('25') >= 0, 'sheet click did not jump to shot 25');
}

/* 跳幕 */
const actBtns = root.querySelectorAll('#article-sb .miaoyan-sb__act');
ok(actBtns.length === 4, 'act buttons = ' + actBtns.length + ', expected 4');
ok(typeof actBtns[0].onclick === 'function', 'act button has no handler');
/* 缺 handler 时只记错、不调用——否则 TypeError 会中断后续全部检查，
   使「后续项从未被检验」而门禁仍以非零码退出，掩盖真实覆盖范围 */
if (typeof actBtns[3].onclick === 'function') {
  actBtns[3].onclick();
  ok($('#sb-fasc').textContent.indexOf('卷五') >= 0, 'act jump did not reach the coda (Book Five)');
}

/* 进度条 */
$('#sb-seek').value = '60';
$('#sb-seek').oninput();
ok(!!$('#sb-q').textContent, 'seek produced empty quote');

/* 倍速 */
$('#sb-speed').value = '2';
$('#sb-speed').onchange();

/* 四图层皆可开关且不抛 */
for (const k of ['props', 'labels', 'en', 'frame']) {
  const cb = $('#sb-l-' + k);
  ok(typeof cb.onchange === 'function', 'layer toggle missing: ' + k);
  cb.checked = false; cb.onchange();
  cb.checked = true; cb.onchange();
}

/* 〔本文判断〕面板：标记者显、未标者隐 */
cells[0]._closest = '.miaoyan-sb__cell'; sheet.onclick({ target: cells[0] });
ok($('#sb-judge').hidden === false, 'shot 1 judgement panel should be visible');
$('#sb-seek').value = '0'; $('#sb-seek').oninput();

/* 无泄漏 */
for (const bad of ['undefined', 'NaN', '[object Object]']) {
  ok(H.indexOf(bad) < 0, 'innerHTML leaks "' + bad + '"');
  ok($('#sb-q').textContent.indexOf(bad) < 0, 'quote panel leaks "' + bad + '"');
}

/* ══ 报告 ════════════════════════════════════════════════ */
if (errs.length) {
  console.error('FAIL: ' + errs.length + ' check(s) failed');
  errs.forEach(e => console.error('  · ' + e));
  process.exit(1);
}
console.log('✅ 分镜门禁通过');
console.log(`   数据　${acts.length} 幕 / ${flat.length} 镜 / ${sumShot} 秒 · 镜号 1–${flat.length} 连续 · drift 三轴（对账 meta.expected）`);
console.log(`   挂载　article.js 生成 #article-sb 折叠壳并挂载渲染器（分镜于正文外现身）`);
console.log(`   控件　播放/暂停·上一镜/下一镜·点格跳镜·跳幕·进度·倍速·四图层 皆可驱动`);
console.log(`   canvas　${ops()} 次绘制调用 · 无 undefined/NaN 泄漏`);