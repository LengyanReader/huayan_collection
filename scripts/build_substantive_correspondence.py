#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""实质对应：四组双侧引文＋分析——佛藏外对应的实质层。

四组对应，每组双侧引文逐条回源（起止锚切片），加实质性分析（不是计数）：
  ① 道 × 华严·法身——道教義樞三身四德 vs T279 法身遍在/心画师
  ② 儒 × 华严·心——孟子万物皆备于我 vs T279 三界唯心/心如工画师
  ③ 庄 × 华严·帝网——天地与我并生 vs 一微尘中入三昧
  ④ 印 × 华严·遍在——薄伽梵歌我住众生中 vs T279 佛身遍法界

判读纪律：
  · 每组标「同构层级」（概念同构/结构同构/功能同构）
  · 标「方向」（谁影响谁/独立发展/共同来源）
  · 负向如实（如薄伽梵歌的「我」是有神论的，华严的「心」是无神论的——不在场的那半更重要）
"""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_translation_workshop import Doc, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "substantive_correspondence.json"


def main() -> int:
    # mandoku 源先剥 ¶ 换行符再装载（换行符会切断锚点）
    def load_mandoku(key, rel):
        raw = (ROOT / rel).read_text(encoding="utf-8")
        stripped = raw.replace("¶", "")
        tmp = ROOT / ".tmp" / "subst"
        tmp.mkdir(parents=True, exist_ok=True)
        tmpf = tmp / Path(rel).name
        tmpf.write_text(stripped, encoding="utf-8")
        return Doc(key, tmpf)

    docs = {
        "t279": Doc("T279", ROOT / "data/references/cbeta/T10n0279.xml"),
        "daojiao": load_mandoku("KR5e0031", "data/references/daozang/KR5e0031_001.txt"),
        "daojiao7": load_mandoku("KR5e0031_7", "data/references/daozang/KR5e0031_007.txt"),
        "zhongyong": load_mandoku("KR1h0041", "data/references/rujia_zhongyong/KR1h0041_001.txt"),
        "mengzi": load_mandoku("KR1h0002", "data/references/rujia_mengzi/KR1h0002_013.txt"),
        "zhuangzi": load_mandoku("KR5c0138", "data/references/daojia_zhuangzi/KR5c0138_001.txt"),
        "bhagavadgita": Doc("BhG", ROOT / "data/references/yindu_bhagavadgita/bhagavadgita.txt"),
    }
    sources = {}
    for key, d in docs.items():
        sources[key] = {"path": str(d.path.relative_to(ROOT)).replace("\\", "/"),
                        "bytes": d.path.stat().st_size,
                        "sha256": sha256(d.path.read_bytes())}

    # ---- 四组双侧引文 ----
    def slice_(key, start, end):
        q = docs[key].slice_quote(start, end)
        return {"source": key, "lb": q["lb"],
                "text": q["text"].replace("¶", "").strip()}

    groups = [
        {
            "id": "dao_fashen",
            "title": "道藏·道教義樞·法身義 × 华严·法身遍在",
            "tradition": "道藏",
            "non_buddhist": [
                slice_("daojiao", "三稱者一者道身二者真身三者報",
                       "度人經云唯道爲身"),
                slice_("daojiao", "三者自在四者清淨", "不爲無常無常所動"),
                slice_("daojiao7", "道性者理存真極義實圓通", "道性衆生皆與自然同也"),
            ],
            "buddhist": [
                slice_("t279", "心如工畫師，能畫諸世間", "無法而不造。"),
                slice_("t279", "三界唯心、三世唯心", "而了知其心無量無邊"),
                slice_("t279", "無一眾生而不具有如來智慧", "無礙智則得現前"),
            ],
            "level": "结构同构",
            "direction": "道教義樞（唐初孟安排）移植佛教法身/三身/四德框架，以道教经典"
                        "（《太平經》《本際經》《度人經》）填充——是佛教→道教的影响，"
                        "不是平行发展（年代差＋框架来源明确）。",
            "analysis": ("道教義樞的「三稱」（道身/真身/報身）与佛教三身（法/報/應）结构完全同构；"
                        "「四德」（常存/快樂/自在/清淨）即佛教涅槃四德（常樂我淨）的道教重述。"
                        "但填充内容全出道经——道身引《太平經》「道無不導道無不生」，"
                        "报身引《本際經》「元始正身…報得此身」。框架是移植的，肉是道教的。"
                        "华严侧的对应文本「心如工畫師」强调心的创造性，「三界唯心」强调心的遍在——"
                        "与道教義樞的「法身」（本体论位格）不同层：华严讲的是心的变现力，"
                        "道教讲的是道的实体化。同在「终极实在」这一概念层，但教义功能不同。"
                        "第三对（卷七〈道性義〉）是全书最强的一组：道性義云「煩惑所覆，"
                        "暫滯凡因；障累若消，還登聖果」——与〈如來出現品〉「無一眾生而"
                        "不具有如來智慧，但以妄想顛倒執著而不證得」四段完全对榫"
                        "（本具→覆障→消障→证得）；「太玄經云：道性眾生皆與自然同」"
                        "即佛性论的道教重述。注意：道性義自注引《太玄經》，"
                        "其『非空不空亦非不空』的三句式带明显中观印记——"
                        "移植痕迹比三身章更深。"),
        },
        {
            "id": "ru_mind",
            "title": "儒家·孟子「萬物皆備於我」× 华严「三界唯心」",
            "tradition": "儒家",
            "non_buddhist": [
                slice_("mengzi", "萬物皆備於我矣反身而誠樂莫", "強恕而行"),
                slice_("mengzi", "盡其心者知其性也知其性", "則知天也"),
            ],
            "buddhist": [
                slice_("t279", "心如工畫師，能畫諸世間", "無法而不造。"),
                slice_("t279", "三界唯心、三世唯心", "而了知其心無量無邊"),
            ],
            "level": "功能同构",
            "direction": "平行发展（孟子 ~300 BC，华严 ~2nd c. CE+——无接触证据），"
                        "不是影响关系。但两者在「内转即可得全体」这一结构上同构。",
            "analysis": ("孟子说「萬物皆備於我矣，反身而誠，樂莫大焉」——转向内即可得万物之全。"
                        "华严说「心如工畫師，能畫諸世間」——世间由心所画。"
                        "结构同构：都把「终极实在」放在主体内。但方向相反——"
                        "孟子是道德主体（倫理学的），华严是存在主体（本体论的）。"
                        "孟子的「備」是德性之備（我本有仁義禮智），华严的「畫」是存在之畫（心造万法）。"
                        "同构在「内转即得」，异质在「得什么」。这就是为什么宋明理学"
                        "能用华严框架重新诠释孟子——不是因为孟子本来就说了华严的话，"
                        "而是因为两者在「内转」这个结构位上兼容。"),
        },
        {
            "id": "zhuang_net",
            "title": "莊子「天地與我並生」× 华严「一微塵中入三昧」",
            "tradition": "道家·诸子",
            "non_buddhist": [
                slice_("zhuangzi", "萬物與我為一", "萬物與我為一"),
                slice_("zhuangzi", "樞始得其環中以應無窮", "以應無窮"),
            ],
            "buddhist": [
                slice_("t279", "一一微塵中，能證一切法", "周行十方國。"),
                slice_("t279", "於一毛孔現不思議佛剎", "無障礙解脫門"),
            ],
            "level": "功能同构",
            "direction": "平行发展（莊子 ~300 BC，华严帝网喻 ~2nd c. CE+——无接触证据）。"
                        "但两者在「个体即全体」这一直觉上同构。",
            "analysis": ("莊子说「天地與我並生，而萬物與我為一」——物我齐一，"
                        "消解主体与客体的边界。华严说「一一微塵中入三昧」、"
                        "「於一毛孔現不思議佛剎」——一即一切，一切即一。"
                        "结构同构：都打破「一」与「多」的二元。但庄子的「一」是"
                        "消解性的（万物与我无别，所以无分别），华严的「一入一切」是"
                        "建设性的（一微尘中摄一切法，所以每个微尘都是完整的法界）。"
                        "庄子的「齐物」是减法（减去分别心），华严的「相即」是加法"
                        "（加上重重无尽的缘起关系）。同构在「消解一二对立」，"
                        "异质在「消解之后剩什么」——庄子剩虚无，华严剩无量。"),
        },
        {
            "id": "india_immanence",
            "title": "薄伽梵歌「我住众生中」× 华严「佛身遍法界」",
            "tradition": "印度·薄伽梵歌",
            "non_buddhist": [
                slice_("bhagavadgita", "sarvabhūtasthamātmānaṃ",
                       "sarvatrasamadarśanaḥ"),
                slice_("bhagavadgita", "matsthānisarvabhūtāninacāhaṃteṣvavasthitaḥ",
                       "matsthānisarvabhūtāninacāhaṃteṣvavasthitaḥ"),
                slice_("bhagavadgita", "samaṃsarveṣubhūteṣutiṣṭhantaṃparameśvaram",
                       "parameśvaram"),
            ],
            "buddhist": [
                slice_("t279", "心如工畫師，能畫諸世間", "無法而不造。"),
            ],
            "level": "功能同构",
            "direction": "平行发展（BhG 是有神论的印度教经典，华严是大乘佛教——"
                        "两者有共同的吠陀-奥义书背景但属不同传统）。"
                        "但「遍在」这个直觉——终极实在不在远方而在一切中——是印度思想的共同底色。",
            "analysis": ("薄伽梵歌 6.29「sarvabhūtastham ātmānaṃ sarvabhūtāni cātmani "
                        "īkṣate」（在一切众生中见自我，在自我中见一切众生）与 9.4"
                        "「matsthāni sarvabhūtāni na cāhaṃ teṣv avasthitaḥ」"
                        "（一切众生在我中，但我不在他们中）——这两个方向合起来"
                        "就是「遍在而不被包含」的结构。华严的「佛身遍法界」有同样的"
                        "「遍在而不被限」结构，但华严否认「我」（无我），薄伽梵歌"
                        "肯定「我」（ātman = brahman）。同构在「遍在」的几何结构，"
                        "异质在「遍在者是什么」——有神的 ātman vs 无神的心。"
                        "不在场的那半（无我）比在场的那半（遍在）更重要。"),
        },
    ]

    data = {
        "meta": {
            "operator": "C1/C3/D5（跨传统实质对应）",
            "title": "四组实质对应：不是计数，是双侧引文＋分析",
            "date": date.today().isoformat(),
            "method": ("每组双侧引文逐条以起止锚在源文切片（不手抄），lb/位置可回源；"
                       "源文件记 sha256；每组标同构层级、方向、分析三栏。"),
            "sources": sources,
            "discipline": "非佛藏文本一律类型判；同构判必须标层级（概念/结构/功能）"
                          "和方向（影响/平行/共同来源）；负向（不在场的那半）如实记录。",
        },
        "groups": groups,
        "summary": {"groups": len(groups),
                    "quotes_total": sum(len(g["non_buddhist"]) + len(g["buddhist"])
                                        for g in groups)},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"groups {len(groups)}  total quotes {data['summary']['quotes_total']}")
    for g in groups:
        print(f"  {g['id']}: {g['title']} [{g['level']}]")
        for side in ("non_buddhist", "buddhist"):
            for q in g[side]:
                print(f"    {side[:4]} {q.get('lb','@')} {q['text'][:40]}…")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
