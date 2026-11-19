# -*- coding: utf-8 -*-
"""信息图几何自检：文字越界、文字互压、SVG 是否渲染出尺寸。"""
import sys
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:8765/web/demo/articles/yogacarabhumi-guide.html'
with sync_playwright() as pw:
    b = pw.chromium.launch(channel='chrome')
    pg = b.new_page(viewport={'width': 1180, 'height': 900})
    pg.goto(URL, wait_until='load')
    pg.wait_for_timeout(600)
    pg.eval_on_selector_all('.secfold-body', "els => els.forEach(e => e.style.display='block')")
    res = pg.evaluate("""() => {
      return [...document.querySelectorAll('#article-root figure svg')].map((svg, k) => {
        const vb = svg.viewBox.baseVal;
        const ts = [...svg.querySelectorAll('text')].map(t => { const b = t.getBBox();
          return { s: t.textContent.slice(0, 18), x: b.x, y: b.y, w: b.width, h: b.height }; });
        const over = ts.filter(t => t.x < -2 || t.y < -2 || t.x + t.w > vb.width + 2 || t.y + t.h > vb.height + 2);
        const ov = [];
        for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) {
          const a = ts[i], c = ts[j];
          const ox = Math.min(a.x + a.w, c.x + c.w) - Math.max(a.x, c.x);
          const oy = Math.min(a.y + a.h, c.y + c.h) - Math.max(a.y, c.y);
          if (ox > 1.5 && oy > 1.5) ov.push(a.s + ' × ' + c.s);
        }
        const r = svg.getBoundingClientRect();
        return { k: k + 1, vb: [vb.width, vb.height], size: [Math.round(r.width), Math.round(r.height)],
                 texts: ts.length, over: over.map(t => t.s), overlaps: ov.slice(0, 6) };
      });
    }""")
    bad = 0
    for r in res:
        flag = 'OK ' if (r['size'][0] > 0 and not r['over'] and not r['overlaps']) else 'BAD'
        if flag == 'BAD':
            bad += 1
        print(flag, r['k'], r['vb'], r['size'], 'texts', r['texts'],
              'over', r['over'], 'overlaps', r['overlaps'])
    print('figures', len(res), 'bad', bad)
    b.close()
    sys.exit(0 if bad == 0 and len(res) == 8 else 1)
