#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C 面深化：七典实质对读（每典一组双侧引文＋分析）——补 §17.26 之后
仍停在「登记」层的八典之七（参同契的形式层对照已在 §17.40）。

七组（全部起止锚切片，mandoku 源先剥 ¶；判读一律类型判＋「不在场的那半」）：
  1 老子「道法自然」× 華嚴「法如是」         ——终极的自身性
  2 论语「下學而上達」× 華嚴「從初發心成最正覺」——阶梯的两端
  3 中庸「誠者天之道」× 華嚴「如來寂然恒不動」 ——本体与工夫的接口
  4 荀子「虛壹而靜」× 華嚴「心得清淨」         ——心的认知修养
  5 淮南「萬物有以相連」× 華嚴「一微塵中入三昧」 ——连属/摄入
  6 奧義書「於一切中見自我」× 華嚴「佛身充滿於法界」——遍在的两种主词
  7 瑜伽經「心作用之止息」× 華嚴「佛寂然恒不動」  ——止息/不动
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_translation_workshop import Doc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "research" / "c_deepen.json"
TMP = ROOT / ".tmp" / "cdeepen"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_mandoku(key: str, rel: str) -> Doc:
    """mandoku 源剥 ¶ 后装载（换行符会切断锚点）。"""
    raw = (ROOT / rel).read_text(encoding="utf-8")
    TMP.mkdir(parents=True, exist_ok=True)
    tmpf = TMP / Path(rel).name
    tmpf.write_text(raw.replace("¶", ""), encoding="utf-8")
    return Doc(key, tmpf)


def main() -> int:
    PUNCT_RE = re.compile(
        r"[，。：；、「」『』（）！？〈〉《》·\s¶#\-.!?;:,]")

    def universal_slice(doc, start, end):
        """标点无关切片：锚点无标点；引文保留原标点与书证格式。"""
        flat = doc.flat
        npos, buf = [], []
        for i, ch in enumerate(flat):
            if not PUNCT_RE.match(ch):
                npos.append(i)
                buf.append(ch)
        s = "".join(buf)
        i = s.find(start)
        if i < 0:
            raise SystemExit(f"{doc.key}: 起锚未命中 {start[:14]!r}")
        j = s.find(end, i + 1)
        if j < 0:
            raise SystemExit(f"{doc.key}: 止锚未命中 {end[:14]!r}")
        f0, f1 = npos[i], npos[j + len(end) - 1]
        raw = doc.raw_of_clean[doc.clean_of_flat[f0]]
        return {"lb": doc.lb_at_raw(raw),
                "text": flat[f0:f1 + 1].strip()}

    docs = {
        "t279": Doc("T279", ROOT / "data/references/cbeta/T10n0279.xml"),
        "laozi": load_mandoku("KR5c0045", "data/references/daojia_laozi/KR5c0045_001.txt"),
        "lunyu": load_mandoku("KR1h0004", "data/references/rujia_lunyu/KR1h0004_014.txt"),
        "lunyu2": load_mandoku("KR1h0004_2", "data/references/rujia_lunyu/KR1h0004_002.txt"),
        "zhongyong": load_mandoku("KR1h0041", "data/references/rujia_zhongyong/KR1h0041_002.txt"),
        "xunzi": load_mandoku("KR3a0002", "data/references/zhuzi_xunzi/KR3a0002_015.txt"),
        "huainanzi": load_mandoku("KR3j0010", "data/references/zhuzi_huainanzi/KR3j0010_020.txt"),
        "huainanzi2": load_mandoku("KR3j0010_11", "data/references/zhuzi_huainanzi/KR3j0010_011.txt"),
        "isha": Doc("īśā", ROOT / "data/references/yindu_ishaupanisad/ishaupanisad.txt"),
        "yoga": Doc("YS", ROOT / "data/references/sanskrit/yoga_sutra.txt"),
    }

    def slice_(key, start, end):
        q = universal_slice(docs[key], start, end)
        return {"source": key, "lb": q.get("lb", ""),
                "text": q["text"].replace("¶", "").strip()}

    groups = [
        {
            "id": "laozi_ziran",
            "title": "老子「道法自然」× 華嚴「法如是」",
            "tradition": "道家",
            "non_buddhist": [
                slice_("laozi", "人法地地法天天法道道法自然", "道法自然"),
                slice_("laozi", "有物混成先天地生", "可以爲天下母"),
            ],
            "buddhist": [
                slice_("t279", "一切諸佛法如是悉坐菩提樹王下", "住於道"),
            ],
            "level": "概念同构",
            "direction": "平行发展（《老子》~4th c. BC，华严 ~2nd c. CE+——无接触证据）。",
            "analysis": ("老子把终极安放在「自然」（自己如此，不由他使）；華嚴以「法如是」"
                        "描述诸佛境界（如其所是，不由造作）。两者在「终极不另需根据」"
                        "这一点上同构。不在场的那半：老子的自然是**道**的属性"
                        "（道先天地、有物混成——仍有生成论骨架），華嚴的法如是是**缘起**"
                        "的如实（无一法自生——恰恰否定任何自性）；「自然」在老子是"
                        "肯定词，在華嚴语境里「自然智」之「自然」已转指离造作的觉智。"),
        },
        {
            "id": "lunyu_ladder",
            "title": "论语「下學而上達」× 華嚴「從初發心成最正覺」",
            "tradition": "儒家",
            "non_buddhist": [
                slice_("lunyu", "不怨天不尤人下學而上達", "知我者其天乎"),
                slice_("lunyu2", "七十而從心所欲不踰矩", "不踰矩"),
            ],
            "buddhist": [
                slice_("t279", "三世諸佛從初發心修菩薩行成最正覺", "乃至示現入般涅槃"),
            ],
            "level": "结构同构",
            "direction": "平行发展（无接触证据）。",
            "analysis": ("论语自述生命阶梯（志学→而立→不惑→知天命→耳順→從心不踰矩）"
                        "并以「下學而上達」总括其方向——由人事而上通。華嚴的菩薩行"
                        "同为由初发心至成正觉的长阶。两者都把终极安放在**可行的阶梯**"
                        "末端而非顿现。不在场的那半：儒家的阶梯是**一生之内**的"
                        "修养次第（七十从心是终点），華嚴的阶梯是**三祇劫**的行位体系"
                        "（成正觉之后仍示现不涅槃）——阶梯的长度与终点性质完全异质。"),
        },
        {
            "id": "zhongyong_cheng",
            "title": "中庸「誠者天之道」× 華嚴「寂然恒不動」",
            "tradition": "儒家",
            "non_buddhist": [
                slice_("zhongyong", "誠者天之道也誠之者人之道也", "從容中道聖人也"),
            ],
            "buddhist": [
                slice_("t279", "而佛寂然恒不動此", "寂靜解脫天人主"),
            ],
            "level": "功能同构",
            "direction": "平行发展（无接触证据）；宋明理学以华严框架重释中庸时"
                        "此接口被激活（§17.26 孟子组同）。",
            "analysis": ("中庸以「誠」贯通天道与人道（天之道自诚、人之道思诚）；"
                        "華嚴以佛的「寂然恒不動」表现本体在应化中的不动。两者都在"
                        "找一个**不动之动**的表述：诚者不勉而中，佛寂然而十方无处不现前。"
                        "不在场的那半：诚是**伦理-形上**的贯通概念（诚者物之终始——"
                        "有生成论承诺），寂然是**禅定-解脱**的境界描述（无生成论承诺）；"
                        "中庸由此开出修身为本的实践论，華嚴由此开出无碍自在的观行论。"),
        },
        {
            "id": "xunzi_mind",
            "title": "荀子「虛壹而靜」× 華嚴「心得清淨」",
            "tradition": "诸子",
            "non_buddhist": [
                slice_("xunzi", "未得道而求道者謂之", "虚壹而靜"),
            ],
            "buddhist": [
                slice_("t279", "何能令他心得清淨", "重自勸勵"),
            ],
            "level": "功能同构",
            "direction": "平行发展（无接触证据）。",
            "analysis": ("荀子答「心何以知道」：虚（不蔽于已有）、壹（不分于两）、"
                        "静（不扰于动）——心的认知条件。華嚴菩薩行中「令他心得清淨」"
                        "是利他的目标态。两者都以**心的澄澈**为通达的前提。"
                        "不在场的那半：荀子的虚壹静服务于**知道**（认知论的），"
                        "华严的心清净服务于**行愿**（伦理-宗教的）；荀子据此建立"
                        "解蔽的论证术，华严据此建立回向的利他行。"),
        },
        {
            "id": "huainanzi_net",
            "title": "淮南「萬物有以相連」× 華嚴「一微塵中入三昧」",
            "tradition": "诸子",
            "non_buddhist": [
                slice_("huainanzi", "萬物有以相連精祲", "有以相蕩也"),
                slice_("huainanzi2", "徃古來今謂之宙四方上下謂之宇", "莫知其所"),
            ],
            "buddhist": [
                slice_("t279", "一微塵中入三昧成就一切微塵定", "於一普現難思剎"),
            ],
            "level": "功能同构",
            "direction": "平行发展（无接触证据）。",
            "analysis": ("淮南记「萬物有以相連，精祲有以相蕩」——万物经气之浸荡"
                        "而相互连属（气化的感应宇宙论）；華嚴以一微尘摄一切剎"
                        "（缘起的重重摄入）。两者都打破物与物的边界。不在场的那半："
                        "淮南的相连靠**气**作介质（气感论——仍是物态的延伸），"
                        "華嚴的摄入不设介质（缘起性空——介质的缺席正是重重无尽的"
                        "条件）；相连是横向的感应网，摄入是纵向的层层含摄。"),
        },
        {
            "id": "isha_atman",
            "title": "奧義書「於一切中見自我」× 華嚴「佛身充滿於法界」",
            "tradition": "印度·奥义书",
            "non_buddhist": [
                slice_("isha", "yastusarvāṇibhūtānyātmanyevānupaśyati",
                       "tatonavijugupsate"),
                slice_("isha", "īśāvāsyamidaṃsarvaṃ", "jagatyāṃjagat"),
            ],
            "buddhist": [
                slice_("t279", "佛身充滿於法界普現一切眾生前", "而恒處此菩提座"),
            ],
            "level": "功能同构",
            "direction": "平行发展（共同印度底色；华严成立时奥义书传统已千年，"
                        "无直接接触证据）。",
            "analysis": ("《Īśā》6：于一切众生中见自我、于自我中见一切众生——"
                        "遍在的**自我**；華嚴：佛身充满法界、普现一切众生前——"
                        "遍在的**佛身**。几何结构相同（一在一切、一切在一）。"
                        "不在场的那半：奥义书的遍在者是 **ātman**（有我——"
                        "且正是华严所否定的执取对象），華嚴的遍在者是无我的"
                        "法身功德；「见」在奥义书是**证知同一**，在華嚴是**现前"
                        "应化**——一个走向梵我合一，一个走向无碍行。"),
        },
        {
            "id": "yoga_nirodha",
            "title": "瑜伽經「心作用之止息」× 華嚴「寂然恒不動」",
            "tradition": "印度·瑜伽",
            "non_buddhist": [
                slice_("yoga", "yogaścittavṛttinirodhaḥ", "svarūpe'vasthānam"),
            ],
            "buddhist": [
                slice_("t279", "正身端坐當願眾生坐菩提座心無所著", "得不動地"),
            ],
            "level": "功能同构",
            "direction": "平行发展（佛教与数论-瑜伽传统同源于沙门外道生态，"
                        "有对话但《華嚴》无直接引用证据）。",
            "analysis": ("YS 1.2–1.3：瑜伽是心作用的止息，于是观者住于自身——"
                        "止息之后**观者（draṣṭuḥ）**独立显现；華嚴〈淨行品〉：「正身"
                        "端坐當願眾生坐菩提座，心無所著」——坐定而心无所住。两者都以"
                        "「心的活动止息／无所著」为真容显现的条件。"
                        "止息」为真容显现的条件。不在场的那半：瑜伽经的观者是"
                        "**puruṣa**（神我——与prakṛti 对立的独立实在），華嚴的"
                        "寂然者无我可得；止息在瑜伽经通往**独存（kaivalya）**，"
                        "在華嚴通往**起用**（不动而遍现）——终点方向相反。"),
        },
    ]

    docs["jain"] = Doc("Utt", ROOT / "data/references/prakrt_uttaradhyayana/uttaradhyayana.txt")
    groups.append({
        "id": "jain_karma",
        "title": "耆那教「業繫」× 華嚴「業力生剎」",
        "tradition": "印度·耆那教",
        "non_buddhist": [
            slice_("jain", "yantidussīlaṃ", "kammāṇibalavantihi"),
        ],
        "buddhist": [
            slice_("t279", "一切諸國土皆隨業力生", "彼心令剎海一切成染污"),
        ],
        "level": "功能同构",
        "direction": "平行发展（同沙门生态、针锋相对的教义对手；佛教文献记耆那"
                    "为六大师之一，但《華嚴》无直接引用证据）。",
        "analysis": ("Uttarādhyayana 以业（kammāṇi）为系缚力量（邪戒者业势强）；"
                    "華嚴〈華藏世界品〉言「一切諸國土皆隨業力生……彼心令剎海"
                    "一切成染污」——两者都把**业**立为世界图景的动力。"
                    "不在场的那半：耆那的业是**物质微粒**（粘着 jīva、须苦行"
                    "剥除——业是实体），華嚴的业由**心**造（彼心令剎海染污——"
                    "业是缘起心行，无实体可得）；于是耆那的解脱=业剥离的"
                    "苦行技术，華嚴的解脱=心转则剎转的观行——同题异构的"
                    "两个业力宇宙论。〔本文判断〕"),
    })

    data = {
        "meta": {
            "date": date.today().isoformat(),
            "title": "C 面深化：七典实质对读",
            "method": ("每典一组双侧引文，起止锚切片（mandoku 源剥 ¶ 后装载），lb/位置可回源；"
                       "判读一律类型判＋「不在场的那半」。与 §17.26 四组合计 11 典、"
                       "11 组实质对读。"),
            "sources": {
                "t279": {"path": "data/references/cbeta/T10n0279.xml",
                         "sha256": sha256((ROOT / "data/references/cbeta/T10n0279.xml").read_bytes())},
                "daojia_laozi": {"dir": "data/references/daojia_laozi"},
                "rujia_lunyu": {"dir": "data/references/rujia_lunyu"},
                "rujia_zhongyong": {"dir": "data/references/rujia_zhongyong"},
                "zhuzi_xunzi": {"dir": "data/references/zhuzi_xunzi"},
                "zhuzi_huainanzi": {"dir": "data/references/zhuzi_huainanzi"},
                "ishaupanisad": {"path": "data/references/yindu_ishaupanisad/ishaupanisad.txt",
                                 "sha256": sha256((ROOT / "data/references/yindu_ishaupanisad/ishaupanisad.txt").read_bytes())},
                "yogasutra": {"path": "data/references/sanskrit/yoga_sutra.txt",
                              "sha256": sha256((ROOT / "data/references/sanskrit/yoga_sutra.txt").read_bytes())},
                "jain": {"path": "data/references/prakrt_uttaradhyayana/uttaradhyayana.txt",
                         "sha256": sha256((ROOT / "data/references/prakrt_uttaradhyayana/uttaradhyayana.txt").read_bytes())},
            },
            "discipline": "非佛藏文本一律类型判；负向（不在场的那半）如实记录。",
        },
        "groups": groups,
        "summary": {"groups": len(groups),
                    "quotes_total": sum(len(g["non_buddhist"]) + len(g["buddhist"])
                                        for g in groups)},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print(f"groups {len(groups)} quotes {data['summary']['quotes_total']}")
    for g in groups:
        print(f"  {g['id']} [{g['level']}]")
        for side in ("non_buddhist", "buddhist"):
            for q in g[side]:
                print(f"    {side[:4]} {q.get('lb', '@')} {q['text'][:44]}…")
    print("written", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
