# -*- coding: utf-8 -*-
"""scripts/ingest_sixty_juan.py — 六十华严（T09n0278）逐卷 clean txt 生成器 + 保真校验。

用法：
    python -X utf8 scripts/ingest_sixty_juan.py            # 只校验（默认卷 001-007 群）
    python -X utf8 scripts/ingest_sixty_juan.py --emit --juans 005,006,007

保真口径（承 L.176 勘误批的修正提取器·STEP0 增正）：
 1) SKIP 元素（note/rdg/mulu/pb/lb/milestone/fig/caesura/anchor）不取内容、**取回 tail**；
 2) app 取 lem 分支（底本字入文），跳 rdg/note；
 3) mulu 整体跳过——旧入库器曾泄漏 mulu 文本成杂线（juan3.txt L9「之二」），本器不重演；
 4) 断行：jhead（title 后断）/head/byline/p/l 各一行；卷尾题（close jhead+tail）合一行；
 5) 校验甲/丙：cjk(生成正文·去卷尾题行) == 平文校验器 slice_juan 段（双独立实现全等）；
    校验乙：与既有旧档对源（去注释行 cjk difflib），残差须等于预期（卷三 1 处 mulu 泄漏）。

依赖同目录 `cbeta_juan_slice.py`（即 _p1_lib.slice_juan 的跟踪版）。
"""
import io, re, sys, difflib
import xml.etree.ElementTree as ET

TEI = '{http://www.tei-c.org/ns/1.0}'
CB = '{http://www.cbeta.org/ns/1.0}'
SKIP = {'note', 'rdg', 'mulu', 'pb', 'lb', 'milestone', 'fig', 'caesura', 'anchor'}
NL = {'p', 'l', 'head', 'byline'}
CN = {'001': '一', '002': '二', '003': '三', '004': '四', '005': '五', '006': '六', '007': '七',
      '008': '八', '009': '九', '010': '十'}
HDR = ('# 大正新脩大藏經 {sig}《大方廣佛華嚴經》(六十華嚴) 卷第{jx}\n'
       '# 經號: {sig} | 卷次: 第{n}卷 | 譯者: 東晉天竺三藏佛馱跋陀羅\n'
       '# 來源: https://cdn.jsdelivr.net/gh/cbeta-org/xml-p5@master/T/T09/T09n0278.xml\n'
       '# 抓取日期: 2026-10-24（本地 xml·INGEST_log sha256:a2bfcee6213f）\n'
       '# 生成: scripts/ingest_sixty_juan.py（承 L.176 修正提取器·lem 保字·mulu 不泄漏·p/l/head/byline 斷行）\n'
       '# 字形: CBETA 繁體原字形 (Traditional Chinese, original CBETA glyphs)\n\n')


def local(tag):
    return tag.split('}')[-1]


def cjk(s):
    return ''.join(ch for ch in s if '\u4e00' <= ch <= '\u9fff')


def _clean(s):
    return ''.join(s.split()) if s else ''


class JuanRender:
    """RAW 平文生成器（保标点·按结构断行）。"""

    def __init__(self):
        self.vols = {}
        self.buf = None

    def _add(self, s):
        if self.buf is not None and s:
            self.buf.append(s)

    def _nl(self):
        if self.buf is not None:
            self.buf.append('\n')

    def run(self, xmlp):
        root = ET.parse(xmlp).getroot()
        for body in root.iter(TEI + 'text'):
            self._walk_children(body)
            break
        return {k: ''.join(v) for k, v in self.vols.items()}

    def _walk_children(self, el):
        for ch in el:
            self._walk(ch)

    def _gather(self, el):
        """子树平文合行（卷尾题用），含 el 自身 tail。"""
        tag = local(el.tag)
        if tag in SKIP:
            return _clean(el.tail)
        if tag == 'app':
            s = ''.join(self._gather(ch) for ch in el if local(ch.tag) == 'lem')
            return s + _clean(el.tail)
        s = _clean(el.text)
        for ch in el:
            s += self._gather(ch)
        return s + _clean(el.tail)

    def _walk(self, el):
        tag = local(el.tag)
        ns = el.tag.split('}')[0] + '}' if '}' in el.tag else ''
        if tag == 'juan':
            n = el.get(TEI + 'n') or el.get('n') or el.get(CB + 'n')
            fun = el.get('fun')
            if fun == 'open':
                self.buf = self.vols.setdefault(n, [])
            elif fun == 'close':
                self._add(self._gather(el))
                self._nl()
                self.buf = None
                return
            self._walk_children(el)
            return
        if ns == CB and tag == 'mulu':
            self._add(_clean(el.tail))
            return
        if tag in SKIP:
            self._add(_clean(el.tail))
            return
        if tag == 'app':
            for ch in el:
                if local(ch.tag) == 'lem':
                    self._walk(ch)
            self._add(_clean(el.tail))
            return
        if tag == 'title':
            self._add(_clean(el.text))
            self._walk_children(el)
            self._add(_clean(el.tail))
            if self.buf is not None:
                self._nl()
            return
        if tag == 'jhead':
            self._walk_children(el)
            self._add(_clean(el.tail))
            self._nl()
            return
        self._add(_clean(el.text))
        self._walk_children(el)
        self._add(_clean(el.tail))
        if tag in NL:
            self._nl()


def slice_juan_cjk(xmlp):
    """平文校验器（_p1_lib.slice_juan 同口径·独立第二实现）：整 app 跳、只保 tail、cjk 过滤。"""
    root = ET.parse(xmlp).getroot()
    segs = {}
    for jbody in root.iter(TEI + 'text'):
        cur, buf = None, []
        for el in jbody.iter():
            tag = local(el.tag)
            if tag == 'juan':
                n = el.get(TEI + 'n') or el.get('n')
                if el.get('fun') == 'open':
                    if cur is not None:
                        segs.setdefault(cur, []).extend(buf)
                    cur, buf = n, []
                elif el.get('fun') == 'close':
                    segs.setdefault(cur, []).extend(buf)
                    cur, buf = None, []
                if el.tail and cur is None:
                    buf.append(el.tail)
                continue
            if tag in SKIP | {'app'}:
                if el.tail and cur is not None:
                    buf.append(el.tail)
                continue
            if cur is None:
                continue
            if el.text:
                buf.append(el.text)
            if el.tail:
                buf.append(el.tail)
        if cur is not None:
            segs.setdefault(cur, []).extend(buf)
    return {k: cjk(''.join(v)) for k, v in segs.items()}


def main(argv):
    emit = '--emit' in argv
    juans = None
    for a in argv:
        if a.startswith('--juans'):
            juans = a.split('=', 1)[1].split(',') if '=' in a else None
    xmlp = 'data/references/cbeta/T09n0278.xml'
    r = JuanRender()
    vols = r.run(xmlp)
    segs = slice_juan_cjk(xmlp)

    def body(n):
        return re.sub(r'\n{2,}', '\n', vols[n]).strip('\n')

    def body_no_tailtitle(n):
        ls = body(n).splitlines()
        assert re.match(r'^大方廣佛華嚴經卷第[一二三四五六七八九十百]+。?$', ls[-1]), \
            f'卷{n} 尾题异态: {ls[-1]!r}'
        return '\n'.join(ls[:-1])

    # 校验群：卷一~七全验；emit 默认仅新档五卷（既有的卷三/四**不覆写**·残差仅作旧档对照证据）
    verify_group = ('001', '002', '003', '004', '005', '006', '007')
    target = juans or [k for k in sorted(vols) if k in verify_group]
    ok = True
    for n in target:
        a, b = cjk(body_no_tailtitle(n)), segs[n]
        same = a == b
        ok &= same
        print(f'[双实现] 卷{n}: cjk={len(a)} slice={len(b)} 等值:{same}')
        if not same:
            sm = difflib.SequenceMatcher(None, a, b)
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op != 'equal':
                    print('   ', op, repr(a[i1:i2][:50]), '|', repr(b[j1:j2][:50]))
        old_fp = f'data/references/cbeta_txt/T09n0278_juan{int(n)}.txt'
        try:
            old = cjk('\n'.join(l for l in io.open(old_fp, encoding='utf-8').read().splitlines()
                                if not l.startswith('#')))
        except FileNotFoundError:
            print(f'[旧档对源] 卷{n}: 无旧档（新入库）')
            continue
        new = cjk(body(n))
        ops = [o for o in difflib.SequenceMatcher(None, old, new).get_opcodes() if o[0] != 'equal']
        print(f'[旧档对源] 卷{n}: 旧={len(old)} 新={len(new)} 残差={len(ops)}',
              [(o[0], old[o[1]:o[2]][:12]) for o in ops])
    if not ok:
        print('ABORT：双实现未全等，不写文件')
        sys.exit(1)
    if emit:
        emit_group = set(juans) if juans else {'001', '002', '005', '006', '007'}
        for n in target:
            if n not in emit_group:
                print(f'[skip-emit] 卷{n} 旧档在册·不覆写')
                continue
            jx = CN.get(n) or n
            fp = f'data/references/cbeta_txt/T09n0278_juan{int(n)}.txt'
            txt = HDR.format(sig='T09n0278', jx=jx, n=n) + body(n) + '\n'
            io.open(fp, 'w', encoding='utf-8', newline='\n').write(txt)
            print('WROTE', fp, len(txt), 'chars')


if __name__ == '__main__':
    main(sys.argv[1:])
