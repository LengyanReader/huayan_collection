// 渲染冒烟测试：在 Node 中执行 build 产物内联的 renderArticleBI，校验其无运行时异常、
// 各节皆出、且无 undefined/NaN/[object Object] 泄漏。（该函数纯拼字符串、不触 DOM，故可在 Node 跑。）
const fs = require('fs');
const path = require('path');
const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');

const m = html.match(/var ARTICLE_BI = (\{[\s\S]*?\});<\/script>/);
if (!m) { console.error('FAIL: ARTICLE_BI not found in ' + file); process.exit(1); }
const ARTICLE_BI = JSON.parse(m[1]);

const fi = html.indexOf('function renderArticleBI(){');
if (fi < 0) { console.error('FAIL: renderArticleBI not found'); process.exit(1); }
// 函数体之末为行首「}」。构建产物为 CRLF，故容许 \r。
// 函数内所有闭合花括号皆缩进，故首个行首「}」即函数之末。
const em = html.slice(fi).match(/function renderArticleBI\(\)\{[\s\S]*?\r?\n\}\r?\n/);
if (!em) { console.error('FAIL: renderArticleBI end not found'); process.exit(1); }
const src = em[0];

let out;
try {
  out = new Function('ARTICLE_BI', src + '\nreturn renderArticleBI();')(ARTICLE_BI);
} catch (e) {
  console.error('FAIL: renderArticleBI threw — ' + e.message + '\n' + e.stack);
  process.exit(1);
}

const errs = [];
if (typeof out !== 'string' || out.length < 5000) errs.push('output too short: ' + (out ? out.length : 0));

// 必出之节（与 renderArticleBI 的 sec() id 对应）
const sections = ['bi-method', 'bi-truncation', 'bi-scorecard', 'bi-funnel', 'bi-domain',
  'bi-crosstab', 'bi-sim', 'bi-cluster', 'bi-pca', 'bi-pareto', 'bi-network',
  'bi-ordinal', 'bi-quality', 'bi-exec'];
for (const s of sections) {
  if (!out.includes('id="' + s + '"')) errs.push('missing section: ' + s);
}

// 图表：SVG 须成对且有内容
const nSvg = (out.match(/<svg /g) || []).length;
const nSvgEnd = (out.match(/<\/svg>/g) || []).length;
if (nSvg < 6) errs.push('too few svg: ' + nSvg);
if (nSvg !== nSvgEnd) errs.push('unbalanced svg: ' + nSvg + '/' + nSvgEnd);
if (!/<rect /.test(out)) errs.push('no heatmap rect');
if (!/<polygon|<polyline/.test(out)) errs.push('no curve polyline');

// 分层与限制声明（守「严禁假信息」：省了 caveat，结论即被误读为经文事实）
if (!out.includes('强共现子图')) errs.push('missing truncation caveat 强共现子图');
if (!out.includes('探索性')) errs.push('missing cluster exploratory caveat');
if (!out.includes('分源')) errs.push('missing three-layer disclaimer 分源');

// 泄漏检查
const leaks = [];
for (const bad of ['undefined', 'NaN', '[object Object]', 'null%', 'undefined%']) {
  const c = out.split(bad).length - 1;
  if (c > 0) leaks.push(bad + ' x' + c);
}
if (leaks.length) errs.push('leak: ' + leaks.join(', '));

// 不得出现综合总分（本项目守则：刻意不给 composite score）。
// 注：文中允许、并预期出现「刻意不给综合总分」之说明，故校验「凡提及必在否定语 14 字之内」，
// 而非禁词——否则连「不给」之声明本身亦被误判。
const cre = /综合(评分|得分|总分)/g;
let cm;
while ((cm = cre.exec(out)) !== null) {
  const before = out.slice(Math.max(0, cm.index - 14), cm.index);
  if (!/不给|不宜|无法|无从|勿/.test(before)) {
    errs.push('composite score asserted at ' + cm.index + ': …' + before + '[综合]');
    break;
  }
}

if (errs.length) { console.error('FAIL:\n  - ' + errs.join('\n  - ')); process.exit(1); }
console.log('OK  renderArticleBI: ' + out.length.toLocaleString('en-US') + ' chars, ' +
  sections.length + ' sections, ' + nSvg + ' svg, no leaks');