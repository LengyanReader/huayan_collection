# -*- coding: utf-8 -*-
"""§1.5 三版用字交叉校勘·次数实测复核（审计脚本）。

用途：§1.5 表列三版（T279／袖珍繁／袖珍简）关键词出现次数，其「次数之差」前稿标
〔存疑待查〕。本脚本实测之，以判其差之成因（范围／凡例目次／CBETA 校勘异文／
真实增删），不得以「非本文所能尽考」一句了之。

口径：
  T279   ：剥控制符／<note>／<app>（校勘异文），剥一切空白，按
           <cb:juan n fun="open"> 切卷 → 卷一–五＝本品；全经＝卷一–八十。
           另计「含 app」之数以见校勘异文之贡献（剥与不剥之差）。
  袖珍繁／简：纯文本，以正文卷标「大方廣佛華嚴經卷第X」切卷（**目次之「卷X」不
           计入**）；卷一–五＝本品；全文件含目次与凡例，另列以见其贡献。
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(ROOT / "scripts"))
import miaoyan_metrics as MM  # noqa: E402

XZ_F = ROOT / "docs/huayanhai/义学专题/经论原典/八十华严-繁-大华严寺袖珍版_1.txt"
XZ_S = ROOT / "docs/huayanhai/义学专题/经论原典/八十华严-简-大华严寺袖珍版_1.txt"

# (T279 形, 袖珍繁形, 袖珍简形)
PAIRS = [("瑠璃", "琉璃", "琉璃"), ("覩", "睹", "睹"), ("踈", "疏", "疏"),
         ("輝", "輝", "晖"), ("徧", "遍", "遍"), ("遍", "遍", "遍"),
         ("毘盧", "毘盧", "毘卢"), ("毗盧", "毗盧", "毗卢"),
         ("尸棄", "尸棄", "尸弃"),
         ("優曇", "優曇", "优昙"), ("閻浮", "閻浮", "阎浮")]

CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8,
      "九": 9}


def cn2int(s):
    """「十一」→「11」；「二十」→「20」。"""
    if s.startswith("第"):
        s = s[1:]
    if s == "十":
        return 10
    if "十" in s:
        a, _, b = s.partition("十")
        return (CN.get(a, 1) * 10) + (CN.get(b, 0) if b else 0)
    return CN.get(s)


def flat(s):
    return re.sub(r"[\s　]", "", s)


def xz_juan(txt):
    """以正文卷标切卷；并返回目次区（首个体标之前）。"""
    ms = [(m.start(), cn2int(m.group(1))) for m in
          re.finditer(r"大[方廣广][廣广]佛[華华][嚴严][經经]卷(第[一二三四五六七八九十]+)", txt)]
    out, toc = {}, txt[:ms[0][0]] if ms else txt
    for i, (p, n) in enumerate(ms):
        seg = txt[p:ms[i + 1][0]] if i + 1 < len(ms) else txt[p:]
        if n is not None and n not in out:
            out[n] = seg
    return out, toc


def main():
    xml = MM.T279.read_bytes().decode("utf-8")
    J = MM._juan_of(xml)                       # 剥 app（权威口径）
    J_app = MM._juan_of(xml, drop_app=False)   # 含 app（校勘异文在内）
    pin = "".join(J[n] for n in range(1, 6))
    pin_app = "".join(J_app[n] for n in range(1, 6))
    quan = "".join(J[n] for n in sorted(J))
    quan_app = "".join(J_app[n] for n in sorted(J_app))

    cols = {}
    for tag, path in (("F", XZ_F), ("S", XZ_S)):
        raw = path.read_bytes().decode("utf-8", errors="replace")
        JJ, toc = xz_juan(raw)
        cols[tag] = {
            "juan": sorted(JJ),
            "jj": {k: flat(v) for k, v in JJ.items()},
            "pin": "".join(flat(JJ[n]) for n in sorted(JJ) if n <= 5),
            "all": flat(raw),
            "toc": flat(toc),
        }

    print(f"T279 本品(卷一–五) {MM.cjk_len(pin)} 字／全经 {MM.cjk_len(quan)} 字")
    print(f"袖珍繁 正文检出卷数 {len(cols['F']['juan'])}（首五：{cols['F']['juan'][:5]}）"
          f" 目次区 {len(cols['F']['toc'])} 字")
    print(f"袖珍简 正文检出卷数 {len(cols['S']['juan'])}"
          f"（首五：{cols['S']['juan'][:5]}） 目次区 {len(cols['S']['toc'])} 字")
    print()

    hdr = (f"{'词形':<12}{'T279 本品':>10}{'T279 本品+校勘':>14}"
           f"{'T279 全经':>10}{'T279 全经+校勘':>14}"
           f"{'袖珍繁 本品':>12}{'袖珍繁 全文件':>13}{'袖珍简 本品':>12}"
           f"{'袖珍简 全文件':>13}")
    print(hdr)
    print("-" * len(hdr))
    for t279f, ff, sf in PAIRS:
        print(f"{t279f+'/'+ (ff if ff==sf else ff+'/'+sf):<12}"
              f"{pin.count(t279f):>10}{pin_app.count(t279f):>14}"
              f"{quan.count(t279f):>10}{quan_app.count(t279f):>14}"
              f"{cols['F']['pin'].count(ff):>12}{cols['F']['all'].count(ff):>13}"
              f"{cols['S']['pin'].count(sf):>12}{cols['S']['all'].count(sf):>13}")
    print()
    # 三版之「承佛威力/威神/神力」——卷二十二组导语用字
    for tag, src in (("T279 本品", pin), ("袖珍繁 本品", cols["F"]["pin"]),
                     ("袖珍简 本品", cols["S"]["pin"])):
        print(f"{tag:<12} 承佛威力={src.count('承佛威力'):<4}"
              f"承佛威神={src.count('承佛威神'):<4}"
              f"承佛神力={src.count('承佛神力'):<4}"
              f"復承如來威神之力={src.count('復承如來威神之力')}")
    print()
    # 瑠/琉：T279 两种写法皆计之
    print("瑠/琉 T279 本品：瑠璃", pin.count("瑠璃"), "／琉璃", pin.count("琉璃"),
          "；全经：瑠璃", quan.count("瑠璃"), "／琉璃", quan.count("琉璃"))
    print("覩/睹 T279 全经：覩", quan.count("覩"), "／睹", quan.count("睹"))
    print("輝/晖 T279 全经：輝", quan.count("輝"), "／晖", quan.count("晖"))
    print("毘盧 T279 全经：毘盧", quan.count("毘盧"), "／毗盧", quan.count("毗盧"),
          "；+校勘：毘盧", quan_app.count("毘盧"))
    for tag, s in (("剥app", quan), ("含app", quan_app)):
        print(f"  毘盧[{tag}] 毘盧遮那 {s.count('毘盧遮那')}"
              f"＋毘盧舍那 {s.count('毘盧舍那')}"
              f"＋裸盧舍那 {s.count('盧舍那')}")
    print()
    # 逐卷「承佛威力／威神／神力」——用以核 §1.5「卷二十二组皆作威力」之说
    print("逐卷 承佛威力/承佛威神/承佛神力/復承如來威神之力")
    print(f"{'卷':<5}{'T279':>22}{'袖珍繁':>22}{'袖珍简':>22}")
    for n in range(1, 6):
        def trip(s):
            return (f"{s.count('承佛威力')}/{s.count('承佛威神')}/"
                    f"{s.count('承佛神力')}/{s.count('復承如來威神之力')}")
        print(f"卷{['一','二','三','四','五'][n-1]:<4}"
              f"{trip(J[n]):>22}{trip(cols['F']['jj'][n]):>22}"
              f"{trip(cols['S']['jj'].get(n, '')):>22}")
    print("（格式：承佛威力/承佛威神/承佛神力/復承如來威神之力）")
    print()
    # 「疏」「毘卢」在两袖珍本之实际用字（判「统一改字」须逐本各验其形）
    print("袖珍繁 疏 =", cols["F"]["all"].count("疏"), "；踈 =",
          cols["F"]["all"].count("踈"))
    print("袖珍简 疏 =", cols["S"]["all"].count("疏"), "；踈 =",
          cols["S"]["all"].count("踈"))
    print("袖珍繁 毘盧 =", cols["F"]["all"].count("毘盧"), "；毗盧 =",
          cols["F"]["all"].count("毗盧"))
    print("袖珍简 毘盧 =", cols["S"]["all"].count("毘盧"), "；毘卢 =",
          cols["S"]["all"].count("毘卢"), "；毗卢 =", cols["S"]["all"].count("毗卢"))
    # 简本卷五「復承如來…」何以不见
    s5 = cols["S"]["jj"].get(5, "")
    print("袖珍简 卷五 復承如來 =", s5.count("復承如來"), "；复承如来 =",
          s5.count("复承如来"), "；承佛威力 =", s5.count("承佛威力"))
    for m in re.finditer(r".{0,12}[復复]承如來?.{0,16}", s5):
        print("   ", repr(m.group(0)))
    # 裸「盧舍那」逐卷（§2.7 之注称 7 见，须核）
    print("裸盧舍那 逐卷：",
          {n: J[n].count("盧舍那") for n in sorted(J) if J[n].count("盧舍那")})
    print("毘盧舍那 逐卷：",
          {n: J[n].count("毘盧舍那") for n in sorted(J) if J[n].count("毘盧舍那")})


if __name__ == "__main__":
    main()