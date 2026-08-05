#!/usr/bin/env python3
"""Append new person trajectory and temple entries to existing YAML files."""

import yaml
import os

# ── Person Trajectories ──────────────────────────────────────────────

PERSON_TRAJECTORIES = """
person_milarepa:
  name: 米拉日巴·西藏瑜伽士
  color: '#8b7a9e'
  source: 桑杰坚赞《米拉日巴传》/ 张澄基译
  verified: 1
  route:
  - y: 1052
    lat: 29
    lng: 85
    label: 诞于后藏贡塘
  - y: 1070
    lat: 29
    lng: 85
    label: 学黑法复仇
  - y: 1078
    lat: 28
    lng: 86
    label: 从玛尔巴学大手印
  - y: 1085
    lat: 28
    lng: 85
    label: 喜马拉雅山洞苦修
  - y: 1090
    lat: 28
    lng: 85
    label: 著《十万歌集》
  - y: 1123
    lat: 28
    lng: 85
    label: 圆寂

person_padmasambhava:
  name: 莲花生·藏传佛教奠基人
  color: '#8b7a9e'
  source: 《莲花生大士本生传》/ 多罗那他《印度佛教史》
  verified: 1
  route:
  - y: 750
    lat: 35
    lng: 72
    label: 诞于乌仗那
  - y: 770
    lat: 29.7
    lng: 91.1
    label: 应赤松德赞之邀入藏
  - y: 775
    lat: 29.3
    lng: 91.5
    label: 建桑耶寺
  - y: 780
    lat: 29
    lng: 91
    label: 传密法·伏藏
  - y: 800
    lat: 29
    lng: 91
    label: 离藏

person_badang:
  name: 八思巴·元朝帝师
  color: '#8b7a9e'
  source: 《元史·释老传》/ 《萨迦世系史》
  verified: 1
  route:
  - y: 1235
    lat: 29
    lng: 88
    label: 诞于后藏
  - y: 1244
    lat: 37.9
    lng: 102.6
    label: 赴凉州见阔端
  - y: 1253
    lat: 40
    lng: 116
    label: 见忽必烈
  - y: 1260
    lat: 39.9
    lng: 116.4
    label: 封为帝师·创蒙古新字
  - y: 1280
    lat: 28.9
    lng: 88
    label: 圆寂于萨迦

person_mazu:
  name: 马祖道一·洪州宗创始人
  color: '#d48476'
  source: 《景德传灯录》卷六·道一
  verified: 1
  route:
  - y: 709
    lat: 31
    lng: 104
    label: 诞于汉州什邡
  - y: 730
    lat: 28.6
    lng: 115.9
    label: 从南岳怀让学
  - y: 740
    lat: 28.6
    lng: 115.9
    label: 洪州开元寺
  - y: 760
    lat: 28.6
    lng: 115.9
    label: 创洪州宗·平常心是道
  - y: 780
    lat: 28.6
    lng: 115.9
    label: 百丈怀海等弟子云集
  - y: 788
    lat: 28.6
    lng: 115.9
    label: 圆寂

person_baizhang:
  name: 百丈怀海·禅门清规创立者
  color: '#d48476'
  source: 《景德传灯录》卷六·怀海 / 《百丈清规》
  verified: 1
  route:
  - y: 720
    lat: 26
    lng: 119
    label: 诞于福州长乐
  - y: 740
    lat: 28.6
    lng: 115.9
    label: 从马祖道一学
  - y: 770
    lat: 28.5
    lng: 115
    label: 洪州百丈山
  - y: 780
    lat: 28.5
    lng: 115
    label: 创百丈清规·一日不作一日不食
  - y: 814
    lat: 28.5
    lng: 115
    label: 圆寂

person_huangbo:
  name: 黄檗希运·临济宗先驱
  color: '#d48476'
  source: 《景德传灯录》卷九·希运 / 《传心法要》
  verified: 1
  route:
  - y: 770
    lat: 26
    lng: 119
    label: 诞于闽
  - y: 790
    lat: 26
    lng: 119
    label: 出家
  - y: 820
    lat: 28.5
    lng: 115
    label: 洪州黄檗山
  - y: 840
    lat: 28.5
    lng: 115
    label: 宰相裴休参学·无心是道
  - y: 850
    lat: 28.5
    lng: 115
    label: 示寂

person_guishan:
  name: 沩山灵祐·沩仰宗创始人
  color: '#d48476'
  source: 《景德传灯录》卷九·灵祐
  verified: 1
  route:
  - y: 771
    lat: 27
    lng: 120
    label: 诞于福州长溪
  - y: 790
    lat: 28.5
    lng: 115
    label: 从百丈怀海学
  - y: 820
    lat: 28
    lng: 112
    label: 潭州沩山
  - y: 840
    lat: 28
    lng: 112
    label: 创沩仰宗·想生相生流注生
  - y: 853
    lat: 28
    lng: 112
    label: 圆寂

person_xitang:
  name: 石头希迁·青原系禅
  color: '#d48476'
  source: 《景德传灯录》卷十四·希迁 / 《参同契》
  verified: 1
  route:
  - y: 700
    lat: 23
    lng: 112
    label: 诞于端州高要
  - y: 720
    lat: 27.2
    lng: 112.7
    label: 从青原行思学
  - y: 742
    lat: 27.2
    lng: 112.7
    label: 衡山南台寺
  - y: 760
    lat: 27.2
    lng: 112.7
    label: 著《参同契》·石头路滑
  - y: 790
    lat: 27.2
    lng: 112.7
    label: 圆寂

person_xuefeng:
  name: 雪峰义存·云门法眼之源
  color: '#d48476'
  source: 《景德传灯录》卷十六·义存
  verified: 1
  route:
  - y: 822
    lat: 25
    lng: 118
    label: 诞于泉州南安
  - y: 840
    lat: 25
    lng: 118
    label: 出家
  - y: 860
    lat: 26.2
    lng: 119
    label: 参德山宣鉴
  - y: 870
    lat: 26.2
    lng: 119
    label: 福州雪峰山
  - y: 890
    lat: 26.2
    lng: 119
    label: 门下出云门文偃·法眼文益
  - y: 908
    lat: 26.2
    lng: 119
    label: 圆寂

person_taohongjing:
  name: 陶弘景·山中宰相·上清派
  color: '#7d9a6e'
  source: 《梁书·陶弘景传》/ 《真诰》
  verified: 1
  route:
  - y: 456
    lat: 32
    lng: 118.8
    label: 诞于丹阳秣陵
  - y: 470
    lat: 32
    lng: 118.8
    label: 从孙游岳学
  - y: 488
    lat: 31.8
    lng: 119.3
    label: 茅山
  - y: 500
    lat: 31.8
    lng: 119.3
    label: 著《真诰》·创上清派茅山宗
  - y: 520
    lat: 31.8
    lng: 119.3
    label: 梁武帝咨询·山中宰相
  - y: 536
    lat: 31.8
    lng: 119.3
    label: 逝于茅山

person_simachengzhen:
  name: 司马承祯·上清派宗师
  color: '#7d9a6e'
  source: 《旧唐书·司马承祯传》/ 《坐忘论》
  verified: 1
  route:
  - y: 647
    lat: 35
    lng: 113
    label: 诞于河内温县
  - y: 660
    lat: 29.2
    lng: 121
    label: 从潘师正学
  - y: 680
    lat: 29.2
    lng: 121
    label: 天台山
  - y: 710
    lat: 29.2
    lng: 121
    label: 著《坐忘论》
  - y: 720
    lat: 35
    lng: 112
    label: 玄宗召见·授篆
  - y: 735
    lat: 35
    lng: 112
    label: 逝于王屋山

person_zhangboduan:
  name: 张伯端·紫阳真人·内丹南宗
  color: '#7d9a6e'
  source: 《历世真仙体道通鉴》/ 《悟真篇》
  verified: 1
  route:
  - y: 984
    lat: 29.2
    lng: 121
    label: 诞于天台
  - y: 1020
    lat: 30.6
    lng: 104
    label: 成都遇刘海蟾授丹诀
  - y: 1030
    lat: 29.2
    lng: 121
    label: 著《悟真篇》·内丹南宗开创
  - y: 1082
    lat: 29.2
    lng: 121
    label: 逝于天台

person_baiyuchan:
  name: 白玉蟾·金丹派南宗五祖
  color: '#7d9a6e'
  source: 《历世真仙体道通鉴》/ 《海琼白真人语录》
  verified: 0
  route:
  - y: 1194
    lat: 20
    lng: 110
    label: 诞于琼州
  - y: 1210
    lat: 27.7
    lng: 118
    label: 从陈楠学
  - y: 1220
    lat: 27.7
    lng: 118
    label: 武夷山
  - y: 1230
    lat: 27.7
    lng: 118
    label: 著《道德宝章》
  - y: 1250
    lat: 27.7
    lng: 118
    label: 逝

person_liangqichao:
  name: 梁启超·近代思想家·佛学研究者
  color: '#5e8b9e'
  source: 梁启超《佛学研究十八篇》/ 丁文江《梁启超年谱长编》
  verified: 1
  route:
  - y: 1873
    lat: 22.5
    lng: 113
    label: 诞于广东新会
  - y: 1890
    lat: 23
    lng: 113
    label: 从康有为学
  - y: 1898
    lat: 35
    lng: 139
    label: 戊戌变法·流亡日本
  - y: 1920
    lat: 39.9
    lng: 116.4
    label: 著《佛学研究十八篇》·清华国学院
  - y: 1929
    lat: 39.9
    lng: 116.4
    label: 逝于北京

person_hushi:
  name: 胡适·近代学者·禅宗史研究
  color: '#5e8b9e'
  source: 胡适《胡适禅学案》/ 唐德刚《胡适口述自传》
  verified: 1
  route:
  - y: 1891
    lat: 31.2
    lng: 121.5
    label: 诞于上海
  - y: 1910
    lat: 40.8
    lng: -73.9
    label: 留美哥伦比亚大学
  - y: 1917
    lat: 39.9
    lng: 116.4
    label: 北大教授
  - y: 1926
    lat: 39.9
    lng: 116.4
    label: 著《中国禅宗史》引发争论
  - y: 1962
    lat: 25
    lng: 121.5
    label: 逝于台北

person_tangyongtong:
  name: 汤用彤·佛教史大家
  color: '#5e8b9e'
  source: 汤用彤《汉魏两晋南北朝佛教史》
  verified: 1
  route:
  - y: 1893
    lat: 30
    lng: 115
    label: 诞于湖北黄梅
  - y: 1917
    lat: 39.9
    lng: 116.4
    label: 清华学堂
  - y: 1922
    lat: 42.4
    lng: -71.1
    label: 哈佛大学哲学系
  - y: 1930
    lat: 39.9
    lng: 116.4
    label: 北大教授·著佛教史
  - y: 1964
    lat: 39.9
    lng: 116.4
    label: 逝于北京

person_lvcheng:
  name: 吕澂·佛学大师
  color: '#5e8b9e'
  source: 吕澂《印度佛学源流略讲》《中国佛学源流略讲》
  verified: 1
  route:
  - y: 1896
    lat: 32
    lng: 119.5
    label: 诞于江苏丹阳
  - y: 1918
    lat: 32
    lng: 118.8
    label: 从欧阳渐学于支那内学院
  - y: 1920
    lat: 35
    lng: 139
    label: 留学日本
  - y: 1943
    lat: 39.9
    lng: 116.4
    label: 著《印度佛学源流略讲》
  - y: 1989
    lat: 39.9
    lng: 116.4
    label: 逝于北京

person_ouyangjingwu:
  name: 欧阳竟无·支那内学院创办人
  color: '#5e8b9e'
  source: 欧阳渐《竟无内外学》/ 吕澂《亲教师欧阳先生事略》
  verified: 1
  route:
  - y: 1871
    lat: 27.5
    lng: 116
    label: 诞于江西宜黄
  - y: 1907
    lat: 32
    lng: 118.8
    label: 从杨文会学
  - y: 1918
    lat: 32
    lng: 118.8
    label: 南京创支那内学院
  - y: 1922
    lat: 32
    lng: 118.8
    label: 著《唯识抉择谈》
  - y: 1937
    lat: 29.5
    lng: 106.5
    label: 内学院迁四川
  - y: 1943
    lat: 29.5
    lng: 106.5
    label: 逝于江津
"""

TEMPLE_ENTRIES = """
  # ═══════════════════════════════════════
  # 藏传佛教 补充
  # ═══════════════════════════════════════
  - id: t_tibetan_003
    name: 桑耶寺
    school: 藏传佛教
    type: temple
    location: 西藏山南扎囊
    lat: 29.3
    lng: 91.5
    dynasty: 唐
    founded: 775
    founder: 莲花生
    description: 西藏第一座佛法僧三宝俱全的寺院。莲花生大师主持修建，赤松德赞倡导。仿印度飞行寺形制，三层分别以藏汉印风格建造。
    significance: 西藏第一座佛教寺院·印藏汉三地风格融合
    persons: [person_padmasambhava]
    source: 王森《西藏佛教发展史略》
    verified: 1

  - id: t_tibetan_004
    name: 布达拉宫
    school: 藏传佛教·格鲁派
    type: temple
    location: 西藏拉萨
    lat: 29.65
    lng: 91.12
    dynasty: 唐/清
    founded: 641
    founder: 松赞干布
    description: 松赞干布为文成公主始建，五世达赖重建为政教合一中心。世界文化遗产。红宫白宫面积13万平方米。
    significance: 西藏政教合一象征·世界文化遗产
    source: 王森《西藏佛教发展史略》
    verified: 1

  - id: t_tibetan_005
    name: 萨迦寺
    school: 藏传佛教·萨迦派
    type: temple
    location: 西藏日喀则萨迦
    lat: 28.9
    lng: 88.0
    dynasty: 宋/元
    founded: 1073
    founder: 昆·贡却杰布
    description: 萨迦派祖庭。八思巴驻锡于此，创蒙古新字、为元朝帝师。萨迦派的政教合一由此始。以灰色墙壁得名。
    significance: 萨迦派祖庭·八思巴驻锡处
    persons: [person_badang]
    source: 王森《西藏佛教发展史略》/ 《萨迦世系史》
    verified: 1

  # ═══════════════════════════════════════
  # 禅宗 补充
  # ═══════════════════════════════════════
  - id: t_chan_006
    name: 洪州开元寺(佑民寺)
    school: 禅宗·洪州宗
    type: temple
    location: 江西南昌
    lat: 28.6
    lng: 115.9
    dynasty: 唐
    founded: 740
    founder: 马祖道一
    description: 马祖道一于此创洪州宗。「平常心是道」「即心即佛」出此。马祖建丛林、百丈立清规——中国禅宗寺院制度由此成型。
    significance: 洪州宗发源地·马祖道场
    persons: [person_mazu, person_baizhang]
    source: 《景德传灯录》
    verified: 1

  - id: t_chan_007
    name: 百丈山百丈寺
    school: 禅宗·洪州宗
    type: temple
    location: 江西奉新
    lat: 28.5
    lng: 115.0
    dynasty: 唐
    founded: 780
    founder: 百丈怀海
    description: 百丈怀海于此创《百丈清规》，为天下禅林共守。「一日不作一日不食」出此。禅宗从此有了独立的寺院经济与管理制度。
    significance: 百丈清规诞生地·禅宗独立制度发源地
    persons: [person_baizhang]
    source: 《景德传灯录》《百丈清规》
    verified: 1

  - id: t_chan_008
    name: 福州雪峰崇圣寺
    school: 禅宗
    type: temple
    location: 福建闽侯
    lat: 26.2
    lng: 119.0
    dynasty: 唐
    founded: 870
    founder: 雪峰义存
    description: 雪峰义存于此开法。门下出云门文偃、法眼文益——云门宗法眼宗皆源于此。有「南方第一丛林」之称。
    significance: 云门宗法眼宗根源·南方第一丛林
    persons: [person_xuefeng]
    source: 《景德传灯录》
    verified: 1

  - id: t_chan_009
    name: 雪窦山资圣寺
    school: 禅宗
    type: temple
    location: 浙江奉化
    lat: 29.7
    lng: 121.2
    dynasty: 唐/宋
    founded: 840
    founder: 常通禅师
    description: 宋代雪窦重显于此著《雪窦颂古》开文字禅先河。弥勒道场·佛教五大名山之一。
    significance: 文字禅发源地·弥勒道场
    source: 《五灯会元》
    verified: 1

  # ═══════════════════════════════════════
  # 道家 补充
  # ═══════════════════════════════════════
  - id: t_daoist_005
    name: 茅山道院
    school: 道家·上清派
    type: mountain
    location: 江苏句容茅山
    lat: 31.8
    lng: 119.3
    dynasty: 汉/历代
    founded: -100
    founder: 茅盈(传说)
    description: 道教上清派祖庭。陶弘景于此创茅山宗。「茅山道士」闻名天下。与终南山(楼观台·全真)并称道教两大祖山。
    significance: 上清派祖庭·茅山宗发源地
    persons: [person_taohongjing]
    source: 《梁书·陶弘景传》/ 《茅山志》
    verified: 1

  - id: t_daoist_006
    name: 王屋山阳台宫
    school: 道家·上清派
    type: mountain
    location: 河南济源王屋山
    lat: 35.1
    lng: 112.3
    dynasty: 唐
    founded: 725
    founder: 司马承祯
    description: 司马承祯于此著《坐忘论》。唐玄宗召见于此授篆。王屋山为道教十大洞天之第一「小有清虚之天」。
    significance: 道教第一洞天·司马承祯道场
    persons: [person_simachengzhen]
    source: 《旧唐书·司马承祯传》
    verified: 1
"""


def main():
    base = r"c:\DA_Practice\huayan_collection"

    # ── Person Trajectories ──────────────────────────────────────
    traj_path = os.path.join(base, "data", "events", "person_trajectories.yaml")
    print(f"Appending {len([l for l in PERSON_TRAJECTORIES.split(chr(10)) if l.startswith('person_')])} person entries to {traj_path}")

    with open(traj_path, "a", encoding="utf-8") as f:
        f.write(PERSON_TRAJECTORIES)

    # Validate
    with open(traj_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    person_count = len(data)
    print(f"  person_trajectories.yaml: {person_count} total entries, YAML valid OK")

    # ── Temple Directory ──────────────────────────────────────────
    temple_path = os.path.join(base, "data", "locations", "temple_directory.yaml")
    print(f"\nAppending {len([l for l in TEMPLE_ENTRIES.split(chr(10)) if l.strip().startswith('- id:')])} temple entries to {temple_path}")

    with open(temple_path, "a", encoding="utf-8") as f:
        f.write(TEMPLE_ENTRIES)

    # Validate
    with open(temple_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    temple_count = len(data.get("temples", []))
    print(f"  temple_directory.yaml: {temple_count} total temples, YAML valid OK")

    print("\nAll entries appended and validated successfully.")


if __name__ == "__main__":
    main()
