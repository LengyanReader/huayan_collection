# -*- coding: utf-8 -*-
"""为《瑜伽师地论导读与重点阐释》生成 8 幅信息图，并原位替换 md 中的 <figure> 块。

用法（项目根目录）：
    python workspace/yogacara_guide/figures.py       # 重建全部 8 幅
    python web/demo/scripts/build.py                # 重新渲染站点

约定：
  · 每幅图对应一个 md 中已存在的 figcaption（以「图 N｜」定位），脚本只替换其 <figure>；
  · 所有数字（卷界、品数、法数）来自 data/references/cbeta/T30n1579.xml 的实测解析；
  · 文字位置按 900×H 的 viewBox 排布，正文渲染时按容器宽度等比缩放；
  · 图内不画未经底本支持的对应线（如「五法→三自性」逐项配属）。
"""
import pathlib
import sys

GOLD = '#b8863c'; BLUE = '#5e8b9e'; GREEN = '#6f8f6a'; RED = '#a4553f'
FG = 'rgba(184,134,60,0.20)'; FB = 'rgba(94,139,158,0.20)'; FGN = 'rgba(111,143,106,0.20)'; FR = 'rgba(164,85,63,0.18)'
INK = 'currentColor'


def T(x, y, s, size=11, anchor='start', fill=INK, weight='400', op=None):
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    o = f' opacity="{op}"' if op else ''
    return f'<text x="{x}" y="{y}" font-size="{size}"{a} fill="{fill}" font-weight="{weight}"{o}>{s}</text>'


def R(x, y, w, h, fill, stroke=None, rx=3, dash=None, sw=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0.8):.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{st}{d}/>'


def LN(x1, y1, x2, y2, stroke=GOLD, dash=None, op=None, sw=1):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    o = f' opacity="{op}"' if op else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>'


DEFS = ('<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b8863c"/></marker></defs>')


def wrap(svg, cap):
    return ('<figure style="margin:16px 0 20px">\n' + svg +
            f'\n<figcaption style="font-size:0.74em;color:var(--text2,#777);margin-top:7px;line-height:1.65">{cap}</figcaption>\n</figure>')


def open_(w, h, aria):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'style="width:100%;height:auto;max-width:920px;display:block" role="img" aria-label="{aria}">{DEFS}')


# ══ 图1 五分卷界 ═══════════════════════════════════════════
def fig1():
    x0, x1, W = 74, 862, 900
    u = (x1 - x0) / 100.0
    X = lambda j: x0 + (j - 1) * u
    y, h = 82, 40
    g = [open_(W, 176, '五分卷界条带图')]
    g.append(T(x0, 26, '五分百卷 · 卷界与篇幅', 13.5, weight='600'))
    g.append(T(x0, 44, '按卷数等比；条内数字为该分卷数', 9.8, op='0.55'))
    for a, b, nm, fill, st in [(1, 50, '本地分', FG, GOLD), (51, 80, '摄抉择分', FB, BLUE), (85, 100, '摄事分', FR, RED)]:
        w = (b - a + 1) * u
        g.append(R(X(a), y, w, h, fill, st))
        g.append(T(X(a) + w / 2, y + 19, nm, 12, 'middle', weight='600'))
        g.append(T(X(a) + w / 2, y + 33, f'{b - a + 1} 卷', 9, 'middle', op='0.6'))
    for a, b in ((81, 82), (83, 84)):
        g.append(R(X(a), y, (b - a + 1) * u, h, FGN, GREEN))
    c1, c2 = X(81) + u, X(83) + u
    g.append(LN(c1, y - 4, c1, y - 30, GOLD, '3 3', '0.55'))
    g.append(LN(c2, y - 4, c2 + 14, y - 30, GOLD, '3 3', '0.55'))
    g.append(T(c1 - 4, y - 34, '摄释分 2 卷', 9.2, 'end', GOLD, weight='600'))
    g.append(T(c2 + 16, y - 34, '摄异门分 2 卷', 9.2, 'start', GOLD, weight='600'))
    for j in (1, 20, 40, 60, 80, 100):
        g.append(LN(X(j), y + h, X(j), y + h + 6, INK, None, '0.3'))
        g.append(T(X(j), y + h + 20, str(j), 9, 'middle', op='0.5'))
    g.append(T(x1 + 4, y + h + 20, '卷', 9, 'start', op='0.45'))
    g.append('</svg>')
    return wrap('\n'.join(g), '图 1｜五分卷界：本地分 1–50（体）、摄抉择分 51–80（抉择）、摄释 81–82、摄异门 83–84、摄事 85–100（解经与圣教归位）。卷界由 T30n1579 逐卷解析。')


# ══ 图2 十七地 ═════════════════════════════════════════════
def fig2():
    x0, x1, W = 108, 856, 900
    u = (x1 - x0) / 49.0
    X = lambda j: x0 + (j - 1) * u
    rows = [('五识身相应地', 1, 1, 'j'), ('意地', 1, 3, 'j'),
            ('有寻有伺等三地', 4, 10, 'j'), ('三摩呬多地', 11, 13, 'j'),
            ('非三摩呬多地', 13, 13, 'j'), ('有心地', 13, 13, 'j'),
            ('无心地', 13, 13, 'j'), ('闻所成地', 13, 15, 'x'),
            ('思所成地', 16, 19, 'x'), ('修所成地', 20, 20, 'x'),
            ('声闻地', 21, 34, 'x'), ('独觉地', 34, 34, 'x'),
            ('菩萨地', 35, 50, 'x'), ('有余依地', 50, 50, 'g'),
            ('无余依地', 50, 50, 'g')]
    col = {'j': (FB, BLUE), 'x': (FG, GOLD), 'g': (FR, RED)}
    H = 66 + len(rows) * 19 + 40
    g = [open_(W, H, '本地分十七地卷次阶梯图')]
    g.append(T(12, 26, '本地分十七地 · 卷次阶梯', 13.5, weight='600'))
    for k, (nm, fillc, st) in enumerate([('境', FB, BLUE), ('行', FG, GOLD), ('果', FR, RED)]):
        g.append(R(700 + k * 54, 15, 12, 10, fillc, st, 2))
        g.append(T(717 + k * 54, 24, nm, 9.6, op='0.75'))
    for i, (nm, a, b, kind) in enumerate(rows):
        y = 48 + i * 19
        fillc, st = col[kind]
        g.append(T(x0 - 10, y + 9.5, nm, 10.4, 'end'))
        w = (b - a) * u + 3
        g.append(R(X(a), y, w, 12, fillc, st))
        lab = f'{a}' if a == b else f'{a}–{b}'
        if w > 50:
            g.append(T(X(a) + 6, y + 9, lab, 8.6, op='0.85'))
        else:
            g.append(T(X(a) + w + 5, y + 9, lab, 8.4, op='0.6'))
    for j, nm in ((11, '卷 11'), (21, '卷 21'), (35, '卷 35')):
        g.append(LN(X(j) - 0.5, 42, X(j) - 0.5, 48 + len(rows) * 19 - 7, INK, '3 4', '0.25'))
        g.append(T(X(j) - 3, 44 + len(rows) * 19 + 14, nm, 8.6, 'end', op='0.55'))
    g.append(T(x0, 44 + len(rows) * 19 + 14, '卷 1', 8.6, 'middle', op='0.55'))
    g.append(T(x1 + 3, 44 + len(rows) * 19 + 14, '卷 50', 8.6, 'start', op='0.55'))
    g.append('</svg>')
    return wrap('\n'.join(g), '图 2｜十七地起讫：前九地为「境」，闻思修为「行」，三乘与二涅槃为「果」。重叠处（卷 13、34、50）为两地同卷分界，非笔误。')


# ══ 图3 摄抉择分 ═══════════════════════════════════════════
def fig3():
    rows = [('五识身地／意地（八证）', 51, 57), ('有寻有伺等三地', 58, 61),
            ('三摩呬多／非三摩呬多／有心地', 62, 63), ('闻所成地', 64, 64),
            ('思所成地', 65, 66), ('修所成地＋声闻地之一', 67, 67),
            ('声闻地之二至之五', 68, 71), ('菩萨地之一至之九', 72, 80),
            ('有余依／无余依地', 80, 80)]
    x0, x1, W = 268, 856, 900
    u = (x1 - x0) / 30.0
    X = lambda j: x0 + (j - 51) * u
    top, rh = 62, 26
    H = top + len(rows) * rh + 42
    g = [open_(W, H, '摄抉择分卷段分布图')]
    g.append(T(12, 26, '摄抉择分 51–80 · 卷段分布', 13.5, weight='600'))
    g.append(T(12, 44, '条长＝卷段长度；细条数字标于条右', 9.6, op='0.55'))
    for j in (51, 60, 70, 80):
        g.append(LN(X(j) + 0.5, top - 8, X(j) + 0.5, top + len(rows) * rh - 4, INK, None, '0.12'))
    for i, (nm, a, b) in enumerate(rows):
        y = top + i * rh
        g.append(T(x0 - 14, y + 12, nm, 10.3, 'end'))
        w = max((b - a) * u, 10)
        g.append(R(X(a), y + 2, w, 15, FB, BLUE))
        lab = f'{a}–{b}' if a != b else f'{a}'
        if w > 58:
            g.append(T(X(a) + 6, y + 12.6, lab, 8.9, op='0.85'))
        else:
            g.append(T(X(a) + w + 5, y + 12.6, lab, 8.5, op='0.65'))
    ay = top + len(rows) * rh
    g.append(LN(x0, ay, x1, ay, INK, None, '0.25'))
    for j in (51, 60, 70, 80):
        g.append(LN(X(j), ay, X(j), ay + 5, INK, None, '0.3'))
        g.append(T(X(j), ay + 19, str(j), 9, 'middle', op='0.5'))
    g.append(T(x1 + 4, ay + 19, '卷', 9, 'start', op='0.45'))
    g.append('</svg>')
    return wrap('\n'.join(g), '图 3｜摄抉择分分段（据底本「攝決擇分中…」科判逐卷核）：58–61 三地、62–63 定学三地、64 闻、65–66 思、67 修＋声闻、68–71 声闻、72–80 菩萨、80 有余／无余依。')


# ══ 图4 菩萨地四持 ═════════════════════════════════════════
def fig4():
    rows = [('初持瑜伽处 · 持品等', '18 品', 35, 46, FG, GOLD),
            ('第二持随法瑜伽处 · 相／分／增上意乐／住', '4 品', 47, 48, FB, BLUE),
            ('第三持究竟瑜伽处 · 生／摄受／地／行／建立', '5 品', 48, 50, FGN, GREEN),
            ('第四持次第瑜伽处 · 发正等菩提心', '1 品', 50, 50, FR, RED)]
    x0, x1, W = 330, 806, 900
    u = (x1 - x0) / 16.0
    X = lambda j: x0 + (j - 35) * u
    top, rh = 62, 34
    H = top + len(rows) * rh + 42
    g = [open_(W, H, '菩萨地四持卷界图')]
    g.append(T(12, 26, '菩萨地 35–50 · 二十八品入四持', 13.5, weight='600'))
    g.append(T(12, 44, '条长＝卷数；条后数字为该持品数（据底本科判）', 9.6, op='0.55'))
    for i, (nm, cnt, a, b, fillc, st) in enumerate(rows):
        y = top + i * rh
        g.append(T(x0 - 14, y + 16, nm, 10.2, 'end'))
        w = max((b - a + 1) * u, 16)
        g.append(R(X(a), y + 2, w, 22, fillc, st))
        g.append(T(X(a) + 7, y + 17, f'卷 {a}–{b}' if a != b else f'卷 {a}', 8.8, op='0.9'))
        g.append(T(X(a) + w + 9, y + 17, cnt, 9.6, 'start', GOLD, weight='600'))
    ay = top + len(rows) * rh
    g.append(LN(x0, ay, x1, ay, INK, None, '0.25'))
    for j in (35, 40, 45, 50):
        g.append(LN(X(j), ay, X(j), ay + 5, INK, None, '0.3'))
        g.append(T(X(j), ay + 19, str(j), 9, 'middle', op='0.5'))
    g.append(T(x1 + 4, ay + 19, '卷', 9, 'start', op='0.45'))
    g.append('</svg>')
    return wrap('\n'.join(g), '图 4｜菩萨地二十八品归四持：初持十八品（35–46）、第二持四品（47–48）、第三持五品（48–50）、第四持一品（50）。48 与 50 两卷跨持，故条带重叠。')


# ══ 图5 九住心 × 六力 × 四作意 ════════════════════════════
def fig5():
    plain = ['内住', '等住', '安住', '近住', '调顺', '寂静', '最极寂静', '专注一趣', '等持']
    zuoyi = ['力励', '力励', '有间缺', '有间缺', '有间缺', '有间缺', '有间缺', '无间缺', '无功用']
    zcolor = {'力励': (FR, RED), '有间缺': (FG, GOLD), '无间缺': (FB, BLUE), '无功用': (FGN, GREEN)}
    liu = [('听闻＋思惟', 0, 1), ('忆念', 2, 3), ('正知', 4, 5), ('精进', 6, 6), ('串习', 7, 8)]
    x0, colw, W = 60, 90, 900
    H = 236
    g = [open_(W, H, '九住心与六力四作意对应矩阵')]
    g.append(T(12, 22, '九住心 × 六力 × 四作意', 13.5, weight='600'))
    g.append(T(12, 38, '底本卷 30：「由六種力，方能成辦九種心住」', 9.6, op='0.55'))
    for i in range(9):
        cx = x0 + i * colw + colw / 2
        nm = plain[i]
        if len(nm) > 4:
            g.append(T(cx, 68, nm[:2], 10.4, 'middle'))
            g.append(T(cx, 81, nm[2:], 10.4, 'middle'))
        else:
            g.append(T(cx, 74, nm, 10.4, 'middle'))
        fillc, st = zcolor[zuoyi[i]]
        g.append(R(cx - colw / 2 + 4, 92, colw - 8, 26, fillc, st, 4))
        g.append(T(cx, 109, zuoyi[i], 9, 'middle', op='0.9'))
        g.append(R(cx - colw / 2 + 4, 132, colw - 8, 20, 'rgba(0,0,0,0.04)', None, 4))
    for nm, a, b in liu:
        cx = x0 + (a + b + 1) / 2 * colw
        w = (b - a + 1) * colw - 8
        g.append(R(x0 + a * colw + 4, 132, w, 20, FB, BLUE, 4))
        g.append(T(cx, 146, nm, 9.2, 'middle', op='0.95'))
        g.append(T(cx, 166, f'{a+1}–{b+1}' if a != b else f'{a+1}', 8.2, 'middle', op='0.45'))
    g.append(T(12, 190, '四作意：力励（1–2）→ 有间缺（3–7）→ 无间缺（8）→ 无功用（9）', 9.6, op='0.7'))
    g.append(T(12, 206, '六力：闻思（1–2）｜忆念（3–4）｜正知（5–6）｜精进（7）｜串习（8–9）', 9.6, op='0.7'))
    g.append(T(12, 221, '注：第 8 住之配属，底本「精進力…最極寂靜專注一趣，由串習力…等持成滿」一句连读，诸家科判微异〔待核〕。', 8.6, op='0.45'))
    g.append('</svg>')
    return wrap('\n'.join(g), '图 5｜禅修进度表：每一住对应的「劲力」（四作意）与「凭什么进步」（六力）。九住非九个阶位，而是同一心一境性的九种成熟度。')


# ══ 图6 八证 ═══════════════════════════════════════════════
def fig6():
    items = [('依止執受', '根身谁持'), ('最初生起', '识如何得起'), ('有明了性', '意识何故有时不明'),
             ('有種子性', '善恶如何相续'), ('業用差別', '一识如何多业'), ('身受差別', '何故有苦乐舍'),
             ('處無心定', '灭尽定时识何在'), ('命終時識', '命终识如何离身')]
    W, H = 900, 320
    g = [open_(W, H, '八证反证结构图')]
    g.append(T(14, 26, '八证：同一归谬形式', 13.5, weight='600'))
    g.append(T(14, 44, '「由八種相，證阿賴耶識決定是有」——每条都以「若离此识，则某事不应道理」收束。', 9.6, op='0.55'))
    g.append(R(14, 84, 156, 176, FR, RED, 8))
    g.append(T(92, 128, '若離', 10.6, 'middle', op='0.85'))
    g.append(T(92, 152, '阿賴耶識', 12.6, 'middle', RED, weight='600'))
    g.append(T(92, 178, '則此八事', 10.4, 'middle', op='0.8'))
    g.append(T(92, 198, '不應道理', 10.4, 'middle', op='0.8'))
    g.append(T(92, 226, '（反证，非直证）', 8.8, 'middle', op='0.45'))
    g.append(R(196, 66, 690, 216, 'rgba(184,134,60,0.05)', GOLD, 8, '5 4'))
    g.append(T(206, 82, '八種現象', 9.2, GOLD, weight='600', op='0.85'))
    g.append(T(262, 82, '若无此识，则皆不可解', 8.8, op='0.45'))
    bw, bh, gx, gy = 322, 38, 16, 10
    for k, (nm, why) in enumerate(items):
        col, row = k % 2, k // 2
        x = 208 + col * (bw + gx)
        y = 92 + row * (bh + gy)
        g.append(R(x, y, bw, bh, 'rgba(255,255,255,0.5)', 'rgba(184,134,60,0.55)', 5))
        g.append(T(x + 12, y + 17, nm, 10.5, weight='600'))
        g.append(T(x + 12, y + 31, why, 8.8, op='0.55'))
        g.append(T(x + bw - 12, y + 23, '✕', 12, 'end', RED, weight='700'))
    g.append(f'<path d="M176,172 H193" fill="none" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#arw)"/>')
    g.append('</svg>')
    return wrap('\n'.join(g), '图 6｜八证的结构：嗢拕南八目（執受、初、明了、種子、業、身受、無心定、命終）。八条共用同一形式，故图中以「八事集合」一框承之，不复逐条连线。')


# ══ 图7 五法 / 三自性 / 三无性 ════════════════════════════
def fig7():
    W, H = 900, 300
    g = [open_(W, H, '五法三自性三无性关系图')]
    g.append(T(14, 26, '五法 · 三自性 · 三无性', 13.5, weight='600'))
    g.append(T(14, 44, '上：五法自是一条「妄→真」的认知链；中下：三自性与三无性一一相即。', 9.6, op='0.55'))
    x0 = 92
    names = ['相', '名', '分别', '真如', '正智']
    bw, gap = 132, 40
    for i, nm in enumerate(names):
        x = x0 + i * (bw + gap)
        fill = 'rgba(0,0,0,0.045)'
        st = 'rgba(0,0,0,0.28)'
        g.append(R(x, 66, bw, 28, fill, st, 5))
        g.append(T(x + bw / 2, 85, nm, 11, 'middle', weight='500'))
        if i < 4:
            g.append(LN(x + bw + 4, 80, x + bw + gap - 6, 80, GOLD, None, '0.5'))
    g.append(R(x0, 100, 3 * bw + 2 * gap, 16, 'rgba(164,85,63,0.10)', None, 4))
    g.append(T(x0 + (3 * bw + 2 * gap) / 2, 112, '前三是「妄」的环节', 9, 'middle', RED, op='0.85'))
    xr = x0 + 3 * (bw + gap)
    g.append(R(xr, 100, 2 * bw + gap, 16, 'rgba(111,143,106,0.12)', None, 4))
    g.append(T(xr + (2 * bw + gap) / 2, 112, '后二是「真」的环节', 9, 'middle', GREEN, op='0.9'))
    g.append(T(14, 85, '五法', 10, op='0.5'))
    g.append(T(14, 112, '〔本文判断〕', 8.2, op='0.4'))
    y2 = 152
    g.append(T(14, y2 + 19, '三自性', 10, op='0.5'))
    cols = [('遍計所執自性', FG, GOLD), ('依他起自性', FB, BLUE), ('圓成實自性', FGN, GREEN)]
    cw, cgap = 236, 34
    for i, (nm, fill, st) in enumerate(cols):
        x = x0 + i * (cw + cgap)
        g.append(R(x, y2, cw, 30, fill, st, 5))
        g.append(T(x + cw / 2, y2 + 20, nm, 10.8, 'middle', weight='600'))
    y3 = 236
    g.append(T(14, y3 + 19, '三无性', 10, op='0.5'))
    cols2 = [('相無性性', FG, GOLD), ('生無性性', FB, BLUE), ('勝義無性性', FGN, GREEN)]
    for i, (nm, fill, st) in enumerate(cols2):
        x = x0 + i * (cw + cgap)
        g.append(R(x, y3, cw, 28, fill, st, 5))
        g.append(T(x + cw / 2, y3 + 19, nm, 10.4, 'middle'))
        g.append(LN(x + cw / 2, y2 + 30, x + cw / 2, y3 - 2, INK, '3 3', '0.35'))
    g.append('</svg>')
    return wrap('\n'.join(g), '图 7｜三自性与三无性一一相即（遍计—相无性、依他—生无性、圆成—胜义无性），五法则另是一条「相→名→分别→真如→正智」的链条，不与三者逐项对应。')


# ══ 图8 十三住 ═════════════════════════════════════════════
def fig8():
    rows = [('種性住', '地前', 'j'), ('勝解行住', '地前', 'j'),
            ('極歡喜住', '初地', 'x'), ('增上戒住', '二地', 'x'), ('增上心住', '三地', 'x'),
            ('覺分相應增上慧住', '四地', 'x'), ('諸諦相應增上慧住', '五地', 'x'),
            ('緣起流轉止息相應增上慧住', '六地', 'x'),
            ('無相有功用住', '七地', 'x'), ('無相無功用住', '八地', 'x'),
            ('無礙解住', '九地', 'x'), ('最上成滿菩薩住', '十地', 'x'),
            ('如來住', '佛地', 'g')]
    col = {'j': (FB, BLUE), 'x': (FG, GOLD), 'g': (FR, RED)}
    W = 900
    top, rh = 52, 21
    H = top + len(rows) * rh + 46
    g = [open_(W, H, '十三住与十地对应图')]
    g.append(T(12, 26, '十三住 × 十地', 13.5, weight='600'))
    g.append(T(150, 26, '十二菩萨住＋如来住', 9.6, op='0.5'))
    g.append(T(126, 44, '住名', 8.8, op='0.45'))
    g.append(T(628, 44, '地', 8.8, op='0.45'))
    g.append(T(742, 44, '分位', 8.8, op='0.45'))
    for i, (nm, di, kind) in enumerate(rows):
        y = top + i * rh
        fillc, st = col[kind]
        g.append(R(126, y, 472, 16, fillc, st, 3))
        g.append(T(136, y + 12, nm, 10.2, weight='500'))
        g.append(R(620, y + 1, 56, 14, 'rgba(0,0,0,0.05)', None, 3))
        g.append(T(648, y + 11.4, di, 8.8, 'middle', op='0.8'))

    def bracket(y1, y2, label):
        g.append(f'<path d="M712,{y1} h-8 v{y2 - y1} h8" fill="none" stroke="{GOLD}" stroke-width="1" opacity="0.5"/>')
        g.append(T(722, (y1 + y2) / 2 + 4, label, 9.2, 'start', GOLD, weight='600', op='0.9'))

    bracket(top, top + 2 * rh - 5, '地前（2 住）')
    bracket(top + 2 * rh, top + 12 * rh - 5, '十地（10 住）')
    bracket(top + 12 * rh, top + 13 * rh - 5, '佛地（1 住）')
    g.append(T(12, top + len(rows) * rh + 22, '十地对应自极欢喜住起依次排列；「三慧」三住对应四至六地〔本文判断〕。', 8.8, op='0.5'))
    g.append('</svg>')
    return wrap('\n'.join(g), '图 8｜十二菩萨住＋如来住：偈摄其纲，长行开其目；读时以长行为准。初二住为地前，极欢喜住起配初地，末住为佛地。')


FIGS = {1: fig1, 2: fig2, 3: fig3, 4: fig4, 5: fig5, 6: fig6, 7: fig7, 8: fig8}

if __name__ == '__main__':
    root = pathlib.Path(__file__).resolve().parents[2]
    md_path = root / 'docs/宗派研究/瑜伽师地论导读与重点阐释.md'
    s = md_path.read_text(encoding='utf-8')
    for no in sorted(FIGS):
        key = f'图 {no}｜'
        i = s.find(key)
        if i < 0:
            print('FAIL locate', key)
            sys.exit(1)
        a = s.rfind('<figure style="margin:16px 0 20px">', 0, i)
        b = s.find('</figure>', i) + len('</figure>')
        s = s[:a] + FIGS[no]() + s[b:]
        print('rebuilt 图', no)
    md_path.write_text(s, encoding='utf-8')
    print('figures', s.count('<figure'), 'svg', s.count('<svg'))
