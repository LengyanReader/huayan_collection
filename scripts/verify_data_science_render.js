/* verify_data_science_render.js — 数据科学层（四视角）渲染门禁（最小 DOM 桩·实跑·数据驱动）
 *
 * A. 自构建产物（任意含 var ARTICLE_DS 之文章页）抽出内嵌 ARTICLE_DS（验集成）；
 * B. 以最小 DOM 桩加载 web/demo/src/data_science.js，实跑 renderDataScience，
 *    校验输出无 undefined/NaN、四节俱在，并核数据不变量（数据形状驱动）：
 *    - L2 视形状分派：octagon_symmetry → Burnside 定轨；census → 类数/员数对账。
 *    - L3：过滤每步 β1 = cyclomatic − rank∂2；β0 随阈值降不增；t=1 旗复形 β1 恒等。
 *    - L4：H0 有限条 = nv−1；H0 本质类 = 1；Betti 曲线末 t=1 连通；未限维时 n_simplices = 2^nv−1。
 * 退出码非 0 即失败。用法：node scripts/verify_data_science_render.js <article.html>
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGE = process.argv[2] || path.join(ROOT, 'web', 'demo', 'articles', 'ru-lai-xian-xiang.html');
const SRC = process.env.DS_SRC || path.join(ROOT, 'web', 'demo', 'src', 'data_science.js');

let fails = [];
function check(name, cond, extra) {
  if (!cond) fails.push(name + (extra ? '  [' + extra + ']' : ''));
}

// ── A. 抽内嵌数据 ──
const html = fs.readFileSync(PAGE, 'utf8');
const m = /var ARTICLE_DS = ([\s\S]*?);<\/script>/.exec(html);
if (!m) { console.log('FAIL: ARTICLE_DS not found in built page'); process.exit(1); }
const data = JSON.parse(m[1]);
const expectId = path.basename(PAGE).replace(/\.html$/, '');

// ── 最小 DOM 桩 ──
global.document = {
  querySelector: function () {
    return { set innerHTML(v) { global.__cap = v; }, get innerHTML() { return global.__cap || ''; } };
  },
};
global.ARTICLE_DS = data;

// 加载渲染器（IIFE 会挂到 global）
eval(fs.readFileSync(SRC, 'utf8'));
check('meta.article 与页名相符', data.meta && data.meta.article === expectId, data.meta && data.meta.article);
check('含四视角 data', !!(data.linguistic && data.algebra && data.topology && data.geometry));
check('renderDataScience 已定义', typeof global.renderDataScience === 'function');
const out = global.renderDataScience('#ds-inner') || '';
check('渲染输出非空', out.length > 0);
check('四节俱在', ['ds-linguistic', 'ds-algebra', 'ds-topology', 'ds-geometry']
  .every(function (id) { return out.indexOf(id) >= 0; }));
check('无 undefined 泄漏', out.indexOf('undefined') < 0);
check('无 NaN 泄漏', out.indexOf('NaN') < 0);

// ── 分析说明卡（lens_guides：目的 · 方法 · 效果，中英必配，零硬编码）──
// 断言取自数据（YAML→内嵌）并要求逐字实印于渲染输出；
// 数字之外更验「说明」本身上版面——数据在而说明缺席即为失职。
const GG = data.lens_guides || {};
const GUIDE_KEYS = ['linguistic', 'algebra', 'topology', 'geometry'];
const GUIDE_FIELDS = ['purpose_zh', 'purpose_en', 'method_zh', 'method_en', 'effect_zh', 'effect_en'];
function printed(s) {
  if (!s) return false;
  if (out.indexOf(s) >= 0) return true;
  // 渲染器经 esc() 者（&<>"）以转义形态比对（story-comic corrections 教训）
  const escd = String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  return escd !== s && out.indexOf(escd) >= 0;
}
check('lens_guides 四视角俱在', GUIDE_KEYS.every(function (k) { return !!GG[k]; }));
check('说明卡三标签齐（目的/方法/效果）',
  ['<b>目的</b>', '<b>方法</b>', '<b>效果</b>'].every(function (t) { return out.indexOf(t) >= 0; }));
check('说明卡标题在版面', out.indexOf('分析说明：目的 · 方法 · 效果') >= 0);
check('说明卡英文标题在版面', out.indexOf('Analytical note: what this lens asks') >= 0);
GUIDE_KEYS.forEach(function (k) {
  const g = GG[k] || {};
  check('说明卡 data-guide=' + k + ' 在版面', out.indexOf('data-guide="' + k + '"') >= 0);
  GUIDE_FIELDS.forEach(function (f) {
    check(k + '.' + f + ' 非空', typeof g[f] === 'string' && g[f].length > 0, String(g[f]));
    check(k + '.' + f + ' 实印', printed(g[f]), String(g[f]).slice(0, 40));
  });
  check(k + '.en-line 中英对照随行', (function () {
    const m = out.match(new RegExp('<div class="ds-guide" data-guide="' + k + '"[\\s\\S]*?(?=<div class="ds-guide"|<div class="section"|$)'));
    return !!m && /class="en-line"/.test(m[0]);
  })());
});

// ── L1 语言统计 ──
const c = data.linguistic.corpus;
check('CJK 字数 > 0', c.cjk_total > 0, String(c.cjk_total));
check('不重复字 > 0', c.unique_chars > 0, String(c.unique_chars));
check('字熵 > 0 且 ≤ log2(types)+ε', c.shannon_entropy_bits > 0 &&
  c.shannon_entropy_bits <= Math.log2(c.unique_chars) + 1e-6,
  c.shannon_entropy_bits + '/' + Math.log2(c.unique_chars));
check('Zipf 斜率为负', data.linguistic.zipf.slope < 0, String(data.linguistic.zipf.slope));

// ── L2 代数（视形状分派） ──
const A = data.algebra;
if (A.octagon_symmetry) {
  const g = A.octagon_symmetry;
  check('Burnside 定轨数为整数', g.burnside_fixed_sum % g.order === 0, g.burnside_fixed_sum + '/' + g.order);
  check('轨道数 = 不动点之和 / 阶', g.num_orbits === g.burnside_fixed_sum / g.order);
  check('对跖五对', (A.antipodal.pairing || []).length === 5);
  const qp = A.questions_partition;
  check('四十问总数 40', qp.total === 40);
  check('甲组无「海」', qp.group_a_endswith_sea === 0);
  check('乙组全「海」', qp.group_b_endswith_sea === 20);
} else if (A.census) {
  const rowsSum = A.census.reduce(function (s, tbl) {
    return s + (tbl.rows || []).reduce(function (a, r) { return a + (r[1] || 0); }, 0);
  }, 0);
  check('普查表非空', A.census.length > 0);
  check('类数 = total_classes', A.total_classes === 40, String(A.total_classes));
  check('员数 = named_total = 414', A.total_named === 414, String(A.total_named));
  check('普查各表之和一致（按组/世间/员数三切）', rowsSum === 40 * 3, String(rowsSum));
} else {
  check('L2 视角存在（octagon 或 census）', false);
}

// ── L3 拓扑 ──
const T = data.topology, fil = T.filtration.steps;
check('过滤步数 = 最大阈值', fil.length === T.filtration.max_threshold, fil.length + '/' + T.filtration.max_threshold);
fil.forEach(function (s) {
  check('t' + s.threshold + ' β1 = cyclomatic − rank∂2', s.beta1 === s.cyclomatic - s.rank_d2);
});
for (let i = 1; i < fil.length; i++) {
  check('t' + fil[i].threshold + ' β0 不降（阈值升高→碎裂）', fil[i].beta0 >= fil[i - 1].beta0);
}
check('t=1 旗复形 β1 恒等（=cyclomatic−rank∂2）',
  T.flag_complex.at_t1.beta1 === T.flag_complex.at_t1.cyclomatic - T.flag_complex.at_t1.rank_d2);
const t1 = T.flag_complex.at_t1;
check('t=1 边数 ≥ 0 且与密度一致',
  T.graph.nodes > 1 ? Math.abs(T.graph.density_t1 - 2 * t1.edges / (T.graph.nodes * (T.graph.nodes - 1))) < 1e-3 : true);

// ── L4 几何·持久同调 ──
const G = data.geometry;
const GROM = G.barcode || {}, GEss = G.essential || {};
check('最大维 ≤ nv−1', G.max_dim <= T.graph.nodes - 1, G.max_dim + '/' + T.graph.nodes);
check('H0 有限条 = nv−1', (GROM.H0 || []).length === T.graph.nodes - 1, String((GROM.H0 || []).length));
check('H0 本质类 = 1（连通）', (GEss.H0 || []).length === 1);
check('H0 类总数 = nv', (GROM.H0 || []).length + (GEss.H0 || []).length === T.graph.nodes);
const nvN = T.graph.nodes;
if (!G.truncated && G.max_dim === nvN - 1 && nvN <= 20) {
  check('全枚举时 n_simplices = 2^nv − 1', G.n_simplices === Math.pow(2, nvN) - 1,
    G.n_simplices + '/' + (Math.pow(2, nvN) - 1));
} else {
  check('限维时 n_simplices ≤ 2^nv − 1', G.n_simplices <= Math.pow(2, nvN) - 1,
    String(G.n_simplices));
}
const cv = G.betti_curve || [];
check('Betti 曲线非空', cv.length > 0);
check('Betti 曲线末行 t=1 连通（β0=1）', cv.length > 0 && cv[cv.length - 1].beta0 === 1,
  String(cv[cv.length - 1] && cv[cv.length - 1].beta0));
for (let i = 1; i < cv.length; i++) {
  check('β0 随 t 降不增', cv[i].beta0 <= cv[i - 1].beta0, 't' + cv[i].t);
}
check('渲染输出含几何节 id', out.indexOf('ds-geometry') >= 0);

// ── L4b Euler 特征 · Euler–Poincaré 恒等式 ──
const BF = G.betti_final || {};
check('betti_final 非空（直接同调）', Object.keys(BF).length > 0, String(Object.keys(BF).length));
let eulFromBetti = 0;
Object.keys(BF).forEach(function (k) { eulFromBetti += Math.pow(-1, +k.slice(1)) * BF[k]; });
check('Euler–Poincaré：χ = Σ(−1)ⁱβᵢ', typeof G.euler_char === 'number' &&
  Math.abs(G.euler_char - eulFromBetti) < 1e-9, G.euler_char + '/' + eulFromBetti);
check('euler_ok 标记为真', G.euler_ok === true, String(G.euler_ok));
check('最终复形 β0 = 1（连通）', BF.H0 === 1, String(BF.H0));
check('渲染输出含 Euler 校验', out.indexOf('Euler') >= 0);

// ── L4b 谱几何（加权图 Laplacian） ──
const SP = G.spectral;
check('谱几何存在', !!SP);
if (SP) {
  const ev = SP.spectrum || [];
  for (let i = 1; i < ev.length; i++) {
    check('谱升序 #' + i, ev[i] >= ev[i - 1] - 1e-6, ev[i] + '<' + ev[i - 1]);
  }
  check('谱和 Σλ = 2m（Laplacian 迹）', Math.abs(SP.sum_eigen_equals_2m - SP.two_edges) < 1e-3,
    SP.sum_eigen_equals_2m + '/' + SP.two_edges);
  check('零特征值数 = t=1 连通分量数', SP.n_zero_eigen === t1.beta0, SP.n_zero_eigen + '/' + t1.beta0);
  check('代数连通度 λ₂ ≥ 0', SP.algebraic_connectivity >= -1e-9, String(SP.algebraic_connectivity));
  check('Fiedler 二分覆盖全节点',
    ((SP.fiedler.id_pos || []).length + (SP.fiedler.id_neg || []).length) === T.graph.nodes);
  check('渲染输出含谱几何文本', out.indexOf('谱几何') >= 0);

  // 归一化谱 · Cheeger 不等式
  const nrm = SP.normalized_algebraic_connectivity;
  check('归一化 λ₂ ∈ [0, 2]', typeof nrm === 'number' && nrm >= -1e-9 && nrm <= 2 + 1e-6, String(nrm));
  const CH = SP.cheeger || {};
  check('Cheeger 扫掠切存在', typeof CH.value === 'number', String(CH.value));
  check('Cheeger 值 ≥ 0', CH.value >= -1e-12, String(CH.value));
  check('Cheeger 不等式 λ₂/2 ≤ h ≤ √(2λ₂)', CH.inequality_ok === true,
    CH.bound_lo + ' <= ' + CH.value + ' <= ' + CH.bound_hi);
  check('Cheeger 下界 = 归一化λ₂/2', Math.abs(CH.bound_lo - Math.max(0, nrm) / 2) < 1e-4,
    CH.bound_lo + '/' + (Math.max(0, nrm) / 2));
  check('渲染输出含 Cheeger 扫掠切', out.indexOf('Cheeger') >= 0);
}

if (fails.length) {
  console.log('FAIL: ' + fails.length + ' check(s) failed');
  fails.forEach(function (f) { console.log('  - ' + f); });
  process.exit(1);
}
console.log('verify_data_science_render[' + expectId + ']: ALL CHECKS PASSED');