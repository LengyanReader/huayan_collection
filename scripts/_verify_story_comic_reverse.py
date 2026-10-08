#!/usr/bin/env python3
"""反向验证 scripts/verify_story_comic_render.js —— 破坏性变异须如期 FAIL。

L.106/L.107 之原则：门禁全绿而无反向验证，不足为凭；变异若为「空操作」「字面只覆盖
部分写法」或「变异落在别处而渲染源未变」，则测不到东西（假绿）。故每条变异：
  ① 锚点必须真实存在于构建产物（不存在即报错，绝不 SKIP——§F13）；
  ② **变异作用域受限于对应内联 JSON 块或渲染器源码**，不得误伤页面他处；
  ③ 变异后以 Node 实跑门禁，首行非 OK 方为「如期失败」；
  ④ 每次变异用临时副本，互不干扰；正本须先通过，否则反向无意义。
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODE = shutil.which('node')
GATE = os.path.join(ROOT, 'scripts', 'verify_story_comic_render.js')
P_SZ = os.path.join(ROOT, 'web', 'demo', 'articles', 'shizhu-miaoyan.html')
P_RL = os.path.join(ROOT, 'web', 'demo', 'articles', 'ru-lai-xian-xiang.html')

if not NODE:
    print('SKIP: node not found')
    sys.exit(1)
if not os.path.exists(GATE):
    print('FAIL: gate not found: ' + GATE)
    sys.exit(1)


def run(page):
    r = subprocess.run([NODE, GATE, page], capture_output=True,
                       encoding='utf-8', errors='replace')
    out = ((r.stdout or '') + (r.stderr or '')).strip()
    return r.returncode, out


def json_block(src, varname):
    """(start, end, body) of `var <varname> = {...};</script>`; 锚点缺失即抛。"""
    m = re.search(r'var ' + varname + r' = (\{[\s\S]*?\});</script>', src)
    if not m:
        raise AssertionError('内联 JSON 缺失: ' + varname)
    return m.start(1), m.end(1), m.group(1)


def in_json(src, varname, fn, label):
    st, en, body = json_block(src, varname)
    nb = fn(body)
    if nb == body:
        raise AssertionError(label + ': 变异未改变内容（空操作）')
    return src[:st] + nb + src[en:]


def sub_once(pattern, repl, text, label):
    if not re.search(pattern, text):
        raise AssertionError(label + ': 锚点不存在 ' + pattern)
    return re.sub(pattern, repl, text, count=1)


# (name, page_tag, scope, (old, new, desc, mode))  scope ∈ {'json:<var>', 'page'}
# mode: 'lit' 字面锚点 / 're' 正则（首个命中）/ 'all' 全量替换
MUTS = [
    ('M1 挂载钩子指向失效容器', 'sz', 'page',
     ('renderStoryComic(\'#story-comic-inner\')', 'renderStoryComic(\'#never-mounted\')',
      '断钩 → 渲染内容无处可去', 'lit')),
    ('M2 comicGo 入口被改名', 'sz', 'page',
     ('function comicGo()', 'function comicgo()', '页首按钮所绑函数失联', 'lit')),
    ('M3 分镜格数契约被破坏', 'sz', 'json:MIAOYAN_SB',
     ('"shots": 26', '"shots": 25', 'expected.shots 与实际 26 格不符', 'lit')),
    ('M4 首格出处被抹去', 'sz', 'json:MIAOYAN_SB',
     (r'"ref": "[^"]*"', '"ref": ""', '引文失去可溯出处', 're')),
    ('M5 首拍出处被抹去', 'sz', 'json:MIAOYAN_NARR',
     (r'"narration_ref": "[^"]*"', '"narration_ref": ""', '拍点无据', 're')),
    ('M6 首格字幕被抹去', 'sz', 'json:MIAOYAN_SB',
     (r'("focus": \[[^\]]*\], )"subtitle_zh": "[^"]*"', r'\1"subtitle_zh": ""',
      '连环画正文空缺', 're')),
    ('M15 幕题英文被抹去', 'sz', 'json:MIAOYAN_SB',
     (r'"title_en": "[^"]*", "fascicle_zh"', r'"title_en": "", "fascicle_zh"',
      '幕级中英必配失守', 're')),
    ('M16 头注英文被抹去', 'sz', 'json:MIAOYAN_SB',
     (r'"subtitle_en": "[^"]*"', '"subtitle_en": ""', '头注中英必配失守', 're')),
    ('M7 〔编辑判断〕标记被改', 'sz', 'page',
     ('〔编辑判断〕', '〔编判断〕', '重建格判断标记不可识别', 'all')),
    ('M8 中英对照类被抽掉', 'sz', 'page',
     ('class="en-line"', 'class="en-XX"', '违反中英必配', 'all')),
    ('M9 信息图容器被改名', 'sz', 'page',
     ('id="story-figs"', 'id="story-figX"', '维度信息图整节失踪', 'lit')),
    ('M10 词频数据被破坏', 'sz', 'json:ARTICLE_DS',
     (r'"char": "[^"]*", "count": -?\d+', '"char": "一", "count": -1',
      '条形图与数据对账失败', 're')),
    ('M11 会众类数断言被改', 'sz', 'page',
     ('类 · 具名', '组 · 具名', '图四不再打印「共 40 类」', 'lit')),
    ('M12 40/414 口径被破坏', 'sz', 'json:MIAOYAN_NARR',
     ('"named": 414', '"named": 413', 'space.expected 与 rings 之和不符', 'lit')),
    ('M13 拍点节容器被改名', 'rl', 'page',
     ('story-beats', 'story-beatX', '拍点序列整节失踪', 'lit')),
    ('M14 首拍出处被抹去', 'rl', 'json:MIAOYAN_NARR',
     (r'"narration_ref": "[^"]*"', '"narration_ref": ""', '（如来现相品）拍点无据', 're')),
    # ── L.118 续批（充实·缩图）新增断言的反向覆盖 ──
    ('M17 分镜规格出处未上版面', 'sz', 'page',
     ("分镜规格：' + esc(meta.spec_ref)", "分镜规格：'",
      '数据在而渲染层不印 spec_ref（头注出处失真）', 'lit')),
    ('M18 口径校准英译被抹去', 'sz', 'json:MIAOYAN_NARR',
     (r'"calibration_en": "[^"]*"', '"calibration_en": ""',
      '环位口径中英必配失守', 're')),
    ('M19 画面要素英译被抹去', 'sz', 'json:MIAOYAN_SB',
     (r'"quote_en": "[^"]*"', '"quote_en": ""',
      '画面要素经文英译缺失（中英必配失守）', 're')),
    ('M20 画面构成名相被抹去', 'sz', 'json:MIAOYAN_NARR',
     (r'"light": \{"label_zh": "[^"]*"', '"light": {"label_zh": ""',
      'cast token 名相丢失 → 内部 id 裸露上版面', 're')),
    ('M21 背景环位标签被抹去', 'rl', 'json:MIAOYAN_NARR',
     (r'"label_zh": "背景[^"]*"', '"label_zh": ""',
      'bg 环位名相丢失 → space_focus 无法解析', 're')),
]


def apply(name, scope, spec, src):
    old, new = spec[0], spec[1]
    mode = spec[3]

    def do(text):
        if mode == 'all':
            if old not in text:
                raise AssertionError(name + ': 锚点不存在 ' + old)
            return text.replace(old, new)
        if mode == 're':
            return sub_once(old, new, text, name)
        if old not in text:
            raise AssertionError(name + ': 锚点不存在 ' + old)
        return text.replace(old, new, 1)

    if scope.startswith('json:'):
        return in_json(src, scope[5:], do, name)
    return do(src)


def main():
    if not os.path.exists(P_SZ) or not os.path.exists(P_RL):
        print('FAIL: 构建产物缺失（先跑 build.py）')
        sys.exit(1)
    for tag, page in (('sz', P_SZ), ('rl', P_RL)):
        rc, out = run(page)
        if rc != 0 or not out.startswith('OK:'):
            print('FAIL: 正本未通过，无法反向验证 — ' + out[:400])
            sys.exit(1)
    print('  正本 2/2 通过')

    base = {'sz': io.open(P_SZ, encoding='utf-8').read(),
            'rl': io.open(P_RL, encoding='utf-8').read()}
    tmpdir = tempfile.mkdtemp(prefix='sc_rev_')
    passed, failed = [], []
    for i, (name, tag, scope, spec) in enumerate(MUTS):
        try:
            mutated = apply(name, scope, spec, base[tag])
        except AssertionError as e:
            failed.append(name + ' → ' + str(e))
            continue
        if mutated == base[tag]:
            failed.append(name + ' → 变异未改变内容（空操作）')
            continue
        if scope.startswith('json:'):
            mm = re.search(r'var ' + scope[5:] + r' = (\{[\s\S]*?\});<\/script>', mutated)
            try:
                json.loads(mm.group(1)) if mm else None
            except Exception as e:
                failed.append(name + ' → 变异破坏了 JSON 语法（测不到目标断言）: ' + str(e)[:60])
                continue
        p = os.path.join(tmpdir, 'm%02d.html' % i)
        with io.open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(mutated)
        rc, out = run(p)
        first = (out.splitlines() or [''])[0]
        if rc == 0 or first.startswith('OK:'):
            failed.append(name + ' → 变异后仍通过（假绿）〔' + spec[2] + '〕')
        else:
            passed.append(name + ' → ' + first[:100])
    shutil.rmtree(tmpdir, ignore_errors=True)

    for line in passed:
        print('  OK   ' + line)
    for line in failed:
        print('  FAIL ' + line)
    if failed:
        print('反向验证：%d/%d 如期失败，%d 条未捕获' % (len(passed), len(MUTS), len(failed)))
        sys.exit(1)
    print('反向验证：%d/%d 如期失败 + 两正本通过' % (len(passed), len(MUTS)))


if __name__ == '__main__':
    main()
