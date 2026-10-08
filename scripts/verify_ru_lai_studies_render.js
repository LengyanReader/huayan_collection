/* verify_ru_lai_studies_render.js — 《如来现相品》数据科学层 渲染门禁（最小 DOM 桩·实跑）
 *
 * A. 自构建产物 articles/ru-lai-xian-xiang.html 抽出内嵌 RU_LAI_STUDIES（验集成）；
 * B. 以最小 DOM 桩加载 web/demo/src/ru_lai_studies.js，实跑 renderRuLaiStudies，
 *    校验输出无 undefined/NaN、三节俱在，并核数据不变量（Burnside、过滤 β1 恒等）。
 * 退出码非 0 即失败。用法：node scripts/verify_ru_lai_studies_render.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGE = process.argv[2] || path.join(ROOT, 'web', 'demo', 'articles', 'ru-lai-xian-xiang.html');
const SRC = process.env.RLS_SRC || path.join(ROOT, 'web', 'demo', 'src', 'ru_lai_studies.js');

let fails = [];
let nchecks = 0;
function check(name, cond, extra) {
  if (!cond) fails.push(name + (extra ? '  [' + extra + ']' : ''));
}

// ── A. 抽内嵌数据 ──
const html = fs.readFileSync(PAGE, 'utf8');
const m = /var RU_LAI_STUDIES = ([\s\S]*?);<\/script>/.exec(html);
if (!m) { console.log('FAIL: RU_LAI_STUDIES not found in built page'); process.exit(1); }
const data = JSON.parse(m[1]);
check('meta.article = ru-lai-xian-xiang', data.meta && data.meta.article === 'ru-lai-xian-xiang', data.meta && data.meta.article);
check('含三视角 data', !!(data.linguistic && data.algebra && data.topology));

// ── 最小 DOM 桩 ──
let cap = '';
global.document = {
  querySelector: function () {
    return { set innerHTML(v) { global.__cap = v; }, get innerHTML() { return global.__cap || ''; } };
  },
};
global.RU_LAI_STUDIES = data;

// 加载渲染器（IIFE 会挂到 global）
eval(fs.readFileSync(SRC, 'utf8'));
check('renderRuLaiStudies 已定义', typeof global.renderRuLaiStudies === 'function');
const out = global.renderRuLaiStudies('#rls-inner') || '';
check('渲染输出非空', out.length > 0);
check('三节俱在', ['rls-linguistic', 'rls-algebra', 'rls-topology'].every(function (id) { return out.indexOf(id) >= 0; }));
check('几何节（第四视角）俱在', out.indexOf('rls-geometry') >= 0);
check('无 undefined 泄漏', out.indexOf('undefined') < 0);
check('无 NaN 泄漏', out.indexOf('NaN') < 0);

// ── 数据不变量 ──
const A = data.algebra, g = A.octagon_symmetry;
check('Burnside 定轨数为整数', g.burnside_fixed_sum % g.order === 0, g.burnside_fixed_sum + '/' + g.order);
check('轨道数 = 不动点之和 / 阶', g.num_orbits === g.burnside_fixed_sum / g.order);
check('轨道数 = 3（八方+二极）', g.num_orbits === 3);
check('对跖五对', (A.antipodal.pairing || []).length === 5);
const qp = A.questions_partition;
check('四十问总数 40', qp.total === 40);
check('甲组无「海」', qp.group_a_endswith_sea === 0);
check('乙组全「海」', qp.group_b_endswith_sea === 20);

const T = data.topology, fil = T.filtration.steps;
check('过滤步数 = 最大阈值', fil.length === T.filtration.max_threshold);
fil.forEach(function (s) {
  check('t' + s.threshold + ' β1 = cyclomatic − rank∂2', s.beta1 === s.cyclomatic - s.rank_d2);
});
for (let i = 1; i < fil.length; i++) {
  check('t' + fil[i].threshold + ' β0 不降（阈值升高→碎裂）', fil[i].beta0 >= fil[i - 1].beta0);
}
check('t=1 完全图 K10（E=45, cyclomatic=36）', fil[0].edges === 45 && fil[0].cyclomatic === 36);
check('t=1 旗复形 β1=0（K10 可缩）', T.flag_complex.at_t1.beta1 === 0);

// ── 几何视角·持久同调不变量 ──
const G = data.geometry;
check('几何视角存在', !!G);
const GROM = G && G.barcode, GEss = G && G.essential;
check('单纯形数 = 2^nv − 1 = 1023', G.n_simplices === 1023, String(G && G.n_simplices));
check('最大维 = nv − 1 = 9', G.max_dim === 9);
check('H0 有限条 = nv − 1 = 9', (GROM.H0 || []).length === 9, String((GROM.H0 || []).length));
check('H0 本质类 = 1（连通）', (GEss.H0 || []).length === 1);
check('H0 类总数 = nv（9 有限 + 1 本质）', (GROM.H0 || []).length + (GEss.H0 || []).length === 10);
const cv = G.betti_curve || [];
check('Betti 曲线首行 t=max，β0∈[1,10]', cv.length > 0 && cv[0].beta0 >= 1 && cv[0].beta0 <= 10, String(cv[0] && cv[0].beta0));
check('Betti 曲线末行 t=1，β0=1（连通）', cv.length > 0 && cv[cv.length - 1].beta0 === 1, String(cv[cv.length - 1] && cv[cv.length - 1].beta0));
check('Betti 曲线末行 β1=β2=β3=0（终为可缩 K10）', cv.length > 0 && cv[cv.length - 1].beta1 === 0 && cv[cv.length - 1].beta2 === 0 && cv[cv.length - 1].beta3 === 0);
for (let i = 1; i < cv.length; i++) {
  check('β0 随 t 降不增', cv[i].beta0 <= cv[i - 1].beta0, 't' + cv[i].t);
}
check('渲染输出含几何节 id', out.indexOf('rls-geometry') >= 0);

if (fails.length) {
  console.log('FAIL: ' + fails.length + ' check(s) failed');
  fails.forEach(function (f) { console.log('  - ' + f); });
  process.exit(1);
}
console.log('verify_ru_lai_studies_render: ALL CHECKS PASSED');