# -*- coding: utf-8 -*-
"""生成 data/narrative/miaoyan_storyboard.yaml —— 世主妙严品「动画电影式分镜」26 镜
依 L.94⑩-3 之序/承/转/合四幕规格，并据回源实况作三处更正：
  ①普賢入三昧在卷五开篇 → 移入合幕，序幕仅作列名上首（伏笔—兑现）
  ②卷五内「迴向」0 次，「卷末回向」不成立 → 合幕改「卷末頌別」
  ③「四十類雲集」真锚点在卷二开篇「眾海悉已雲集」→ 置于承幕
一切引文生成时断言逐字见于 T10n0279。
"""
import io, sys, re, yaml
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(r'C:\DA_Practice\huayan_collection')
raw = (ROOT / "data/references/cbeta" / "T10n0279.xml").read_text(encoding='utf-8')
TXT = re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', raw))

META = {
 'id': 'shizhu-miaoyan-storyboard',
 'title_zh': '世主妙严品 · 电影式分镜', 'title_en': 'Adorning the World-Ruler: A Cinematic Storyboard',
 'subtitle_zh': '四幕二十六镜——序幕·承·转·合',
  'subtitle_en': 'Four acts, twenty-six shots: Prelude, Assumption, Transition, Coda',
 'source_primary': 'CBETA T10n0279（八十华严·实叉难陀译）——本经唯一现行底本',
 'source_ref': 'https://cbetaonline.dila.edu.tw/zh/T10n0279',
 'spec_ref': '本设计依用户 2026-10-01 指示之「动画电影式分镜」规格（台账 L.94 ⑩-3）编排',
 'tradition_zh': '佛教「變相圖／經變」传统以圖繪釋教義、構畫佛會之莊嚴；本分鏡與之可相比擬，'
                '然其形制與布局出于现代视觉重构，**非經變圖之复现**，不可混同。',
 'tradition_en': 'Comparable to the bianxiang tu (經變) tradition of Buddhist pictorial exegesis, '
                 'this storyboard is nonetheless a modern visual reconstruction, not a reproduction of such images.',
 'method_zh': '每镜之**要素**（地・樹・珠・殿・座・網・幢等）悉出底本，逐字可覆核；'
              '其**空间关系、取景、运镜、光色氛围**则属现代重构，凡此一律标〔本文判断〕，不冒充经文所陈。',
 'method_en': 'Every element in every shot derives from the base text and can be verified word for word; '
              'spatial relations, framing, camera moves and atmosphere are modern reconstruction, '
              'always marked as editorial judgement.',
 'uncertainty_zh': '经文所述为同时圆融之境，非时间先后。分镜之先后为阅读之便而设，'
                   '不代表义理上的次第〔待考〕。四幕之界亦然。',
 'uncertainty_en': 'The states described are simultaneous, not successive; the shot order is editorial (pending verification).',
 'reconstruction_flag_zh': '〔本文判断〕', 'reconstruction_flag_en': '[Editorial judgement]',
}

SHOT_SIZES = {  # 景别（data-driven，渲染层不得硬编码）
 'ews':  {'zh': '大远景', 'en': 'Extreme wide shot', 'zoom': 1.00},
 'ws':   {'zh': '远景',   'en': 'Wide shot',        'zoom': 0.68},
 'ms':   {'zh': '中景',   'en': 'Medium shot',      'zoom': 0.44},
 'cu':   {'zh': '近景',   'en': 'Close shot',       'zoom': 0.26},
 'ecu':  {'zh': '大特写', 'en': 'Extreme close-up', 'zoom': 0.15},
}
CAMERA_MOVES = {  # 运镜　drift = [推拉 dz, 横移 dx, 升降 dy]
 'static':    {'zh': '固定',   'en': 'Static',        'drift': [0, 0, 0]},
 'push':      {'zh': '推近',   'en': 'Push in',       'drift': [0.62, 0, -0.14]},
 'pull':      {'zh': '拉远',   'en': 'Pull back',     'drift': [-0.62, 0, 0.14]},
 'pan_left':  {'zh': '左横移', 'en': 'Pan left',      'drift': [0, -0.52, 0]},
 'pan_right': {'zh': '右横移', 'en': 'Pan right',     'drift': [0, 0.52, 0]},
 'tilt_up':   {'zh': '上摇',   'en': 'Tilt up',       'drift': [0, 0, -0.46]},
 'tilt_down': {'zh': '下摇',   'en': 'Tilt down',     'drift': [0, 0, 0.46]},
 'orbit':     {'zh': '环绕',   'en': 'Orbit',         'drift': [0.40, 0.40, -0.10]},
}

def P(i, kind, lz, le, qz, qe, **kw):
    d = {'id': i, 'kind': kind, 'label_zh': lz, 'label_en': le,
         'quote_zh': qz, 'quote_en': qe}
    d.update(kw)
    return d

def S(no, size, move, dur, subject, focus, sz, se, qz, qe, ref, rec=False, jz=''):
    d = {'no': no, 'size': size, 'move': move, 'duration_s': dur,
         'subject': subject, 'focus': focus,
         'subtitle_zh': sz, 'subtitle_en': se,
         'quote_zh': qz, 'quote_en': qe, 'ref': ref,
         'reconstruction': rec}
    if rec:
        d['judgment_zh'] = jz
    return d

ACTS = [
# ═══════════════════════════ 序幕 · 卷一 ═══════════════════════════
{'no': '序', 'id': 'prelude', 'layout': 'buddhafield',
 'title_zh': '序幕 · 正觉所现之境庄严', 'title_en': 'Prelude: The Adornment Manifested at Awakening',
 'fascicle_zh': '卷一（品首）', 'fascicle_en': 'Fascicle 1',
 'lead_zh': '一時，佛在摩竭提國阿蘭若法菩提場中，始成正覺。',
 'lead_en': 'At one time, the Buddha, in the Place of Enlightenment at Araññavipṛśa in Magadha, attained perfect awakening.',
 'props': [
  P('ground','ground','地·堅固','Ground, solid','其地堅固，金剛所成','The ground is solid, made of vajra.',level=0),
  P('wheel','wheel','上妙寶輪','Wondrous jeweled wheel','上妙寶輪，及眾寶華、清淨摩尼，以為嚴飾','Above it a wondrous jeweled wheel, with jeweled blossoms and pure jewels as adornment.',level=0),
  P('blossom','lotus','眾寶華','Jeweled blossoms','眾寶華、清淨摩尼，以為嚴飾','Jeweled blossoms and pure jewels serve as adornment.',level=0),
  P('mani','jewel','清淨摩尼','Pure maṇi jewel','眾寶華、清淨摩尼，以為嚴飾','Jeweled blossoms and pure jewels serve as adornment.',level=0),
  P('formsea','lightsea','諸色相海','Sea of forms and colors','諸色相海，無邊顯現','Seas of forms and colors appear without bound.',level=0),
  P('banner','banner','摩尼為幢','Maṇi as banner','摩尼為幢，常放光明，恒出妙音','A maṇi banner, constantly radiating light, forever emitting wondrous sound.',level=1),
  P('net','net','眾寶羅網','Jeweled net','眾寶羅網，妙香華纓，周匝垂布','A jeweled net and scented blossom-garlands hang all around.',level=1),
  P('garland','cloud','妙香華纓','Scented blossom-garlands','眾寶羅網，妙香華纓，周匝垂布','A jeweled net and scented blossom-garlands hang all around.',level=1),
  P('maniking','jewelrain','摩尼寶王','Maṇi jewel-king','摩尼寶王，變現自在，雨無盡寶及眾妙華分散於地','The maṇi jewel-king manifests freely, raining endless jewels and wondrous blossoms upon the ground.',level=0),
  P('trees','tree','寶樹行列','Rows of jeweled trees','寶樹行列，枝葉光茂','Jeweled trees stand in rows, their branches and leaves luminous and flourishing.',level=0),
  P('bodhi','tree','菩提樹','The Bodhi Tree','其菩提樹高顯殊特：金剛為身，瑠璃為幹','Its bodhi tree, tall and singular: vajra for its body, lapis lazuli for its trunk.',level=0,role='focus'),
  P('bodhi_trunk','trunk','瑠璃為幹','Lapis lazuli trunk','其菩提樹高顯殊特：金剛為身，瑠璃為幹','Vajra for its body, lapis lazuli for its trunk.',level=1),
  P('bodhi_branch','branch','寶為枝條・寶葉扶踈','Jewel branches, jewel leaves','眾雜妙寶以為枝條；寶葉扶踈，垂蔭如雲','Assorted wondrous jewels for its branches; jewel-leaves support and spread, hanging shade like clouds.',level=2),
  P('bodhi_fruit','jewel','寶華雜色・摩尼為果','Jewel blossoms, maṇi fruit','寶華雜色，分枝布影，復以摩尼而為其果，含輝發焰','Jewel-blossoms of varied colors, branching and casting shadows; and maṇi jewels for its fruit, holding radiance, emitting flames.',level=3),
  P('bodhi_inner','assembly','寶內諸菩薩如雲','Bodhisattvas within, a cloud','摩尼寶內，有諸菩薩，其眾如雲，俱時出現','Within the maṇi jewels there are bodhisattvas, a host like clouds, appearing all at once.',level=3),
  P('bodhi_sound','sound','恒出妙音','Ever-sounding wondrous tone','其菩提樹恒出妙音，說種種法，無有盡極','The bodhi tree forever emits wondrous sound, speaking all manner of Dharma without end.',level=1),
  P('palace','palace','宮殿樓閣','Palace and mansions','如來所處宮殿樓閣，廣博嚴麗充遍十方','The palace and mansions where the Tathāgata abides are spacious and stately, filling the ten directions.',level=0),
  P('adorn','lightstream','莊嚴具流光成幢','Adornments streaming light into banners','諸莊嚴具流光如雲，從宮殿間萃影成幢','All adornments stream light like clouds; their shadows gather from between the mansions into banners.',level=1),
  P('manicloud','cloudpair','摩尼光雲','Clouds of maṇi light','摩尼光雲，互相照耀；十方諸佛，化現珠玉','Clouds of maṇi light illuminate one another; the Buddhas of the ten directions manifest as pearls and gems.',level=1),
  P('seat','seat','師子座','The Lion Throne','其師子座，高廣妙好：摩尼為臺，蓮華為網','His lion throne, tall and broad: maṇi for its platform, lotus for its net.',level=0),
  P('seat_detail','hall','堂榭階砌戶牖','Halls, steps, doors and windows','堂榭、樓閣、階砌、戶牖，凡諸物像，備體莊嚴','Halls, pavilions, towers, steps, terraces, doors and windows — every form is fully adorned.',level=1),
  P('awake','sun','成最正覺','Perfect awakening','於一切法成最正覺','He attained the unsurpassed right awakening to all phenomena.',level=0),
  P('void','void','虛空譬','Simile of space','譬如虛空具含眾像，於諸境界無所分別','Like space, which contains all images and distinguishes no realms.',level=0),
  P('hairtip','hairtip','毛端容世界','All worlds in a hair-tip','一一毛端，悉能容受一切世界而無障礙','In each single hair-tip he contains all worlds without obstruction.',level=0),
 ],
 'shots': [
  S(1,'ews','static',5.0,None,['ground','wheel','blossom','mani','trees'],
    '菩提場全境：地・寶輪・寶華摩尼・寶樹行列',
    'The whole Place of Enlightenment: ground, jeweled wheel, blossoms and jewels, rows of trees',
    '一時，佛在摩竭提國阿蘭若法菩提場中，始成正覺。',
    'At one time, the Buddha, in the Place of Enlightenment at Araññavipṛśa in Magadha, attained perfect awakening.',
    'T10n0279 卷一·品首',
    True,'摩竭提国之地理氛围、方位与光色皆为意象性补足；经文唯言「佛在……菩提場中，始成正覺」，未描摹环境。'),
  S(2,'ews','push',4.5,'ground',['ground','wheel'],
    '其地堅固，金剛所成；上妙寶輪',
    'The ground is solid, made of vajra; above it, a wondrous jeweled wheel',
    '其地堅固，金剛所成','The ground is solid, made of vajra.','T10n0279 卷一·品首'),
  S(3,'ws','pan_right',4.0,'blossom',['blossom','mani','wheel'],
    '眾寶華、清淨摩尼，以為嚴飾',
    'Jeweled blossoms and pure jewels serve as its adornment',
    '眾寶華、清淨摩尼，以為嚴飾','Jeweled blossoms and pure jewels serve as adornment.',
    'T10n0279 卷一·品首'),
  S(4,'ws','pull',4.0,'formsea',['formsea'],
    '諸色相海，無邊顯現','Seas of forms and colors appear without bound',
    '諸色相海，無邊顯現','Seas of forms and colors appear without bound.','T10n0279 卷一·品首'),
  S(5,'ms','tilt_up',4.5,'banner',['banner','net'],
    '摩尼為幢，常放光明，恒出妙音','A maṇi banner, constantly radiating light, forever emitting wondrous sound',
    '摩尼為幢，常放光明，恒出妙音','A maṇi banner, constantly radiating light, forever emitting wondrous sound.',
    'T10n0279 卷一·品首'),
  S(6,'ms','orbit',4.5,'net',['net','garland'],
    '眾寶羅網，妙香華纓，周匝垂布','A jeweled net and scented blossom-garlands hang all around',
    '眾寶羅網，妙香華纓，周匝垂布','A jeweled net and scented blossom-garlands hang all around.',
    'T10n0279 卷一·品首'),
  S(7,'ws','push',4.0,'maniking',['maniking','ground'],
    '摩尼寶王，變現自在，雨無盡寶及眾妙華分散於地',
    'The maṇi jewel-king manifests freely, raining endless jewels and wondrous blossoms on the ground',
    '摩尼寶王，變現自在，雨無盡寶及眾妙華分散於地',
    'The maṇi jewel-king manifests freely, raining endless jewels and wondrous blossoms upon the ground.',
    'T10n0279 卷一·品首'),
  S(8,'ws','push',5.0,'bodhi',['bodhi','trees'],
    '菩提樹高顯殊特：金剛為身，瑠璃為幹',
    'The bodhi tree, tall and singular: vajra for its body, lapis lazuli for its trunk',
    '其菩提樹高顯殊特：金剛為身，瑠璃為幹','Its bodhi tree, tall and singular: vajra for its body, lapis lazuli for its trunk.',
    'T10n0279 卷一·品首'),
  S(9,'cu','tilt_up',4.5,'bodhi_branch',['bodhi_trunk','bodhi_branch'],
    '眾雜妙寶以為枝條；寶葉扶踈，垂蔭如雲',
    'Assorted jewels for its branches; jewel-leaves spread, hanging shade like clouds',
    '眾雜妙寶以為枝條；寶葉扶踈，垂蔭如雲',
    'Assorted wondrous jewels for its branches; jewel-leaves support and spread, hanging shade like clouds.',
    'T10n0279 卷一·品首'),
  S(10,'ecu','static',4.0,'bodhi_fruit',['bodhi_fruit'],
    '寶華雜色，分枝布影；復以摩尼而為其果，含輝發焰',
    'Jewel-blossoms of varied hues; and maṇi jewels for its fruit, holding radiance, emitting flames',
    '寶華雜色，分枝布影，復以摩尼而為其果，含輝發焰，與華間列',
    'Jewel-blossoms of varied colors, branching and casting shadows; and maṇi jewels for its fruit, holding radiance and emitting flames, set among the blossoms.',
    'T10n0279 卷一·品首'),
  S(11,'ms','orbit',5.0,'bodhi_inner',['bodhi_inner','bodhi_sound'],
    '光明中雨摩尼寶，寶內諸菩薩如雲俱時出現；樹恒出妙音',
    'Within the light it rains maṇi jewels; within them bodhisattvas appear like clouds; the tree forever sounds',
    '其樹周圍咸放光明，於光明中雨摩尼寶，摩尼寶內，有諸菩薩，其眾如雲，俱時出現',
    'All around it radiates light, and within that light it rains maṇi jewels; within the maṇi jewels there are bodhisattvas, a host like clouds, appearing all at once.',
    'T10n0279 卷一·品首'),
  S(12,'ws','pull',5.0,'palace',['palace','adorn','manicloud'],
    '宮殿樓閣充遍十方；莊嚴具流光如雲，萃影成幢',
    'Palace and mansions fill the ten directions; adornments stream light, shadows gathering into banners',
    '如來所處宮殿樓閣，廣博嚴麗充遍十方','The palace and mansions where the Tathāgata abides are spacious and stately, filling the ten directions.',
    'T10n0279 卷一·品首'),
  S(13,'ms','push',5.0,'seat',['seat','seat_detail','manicloud'],
    '師子座高廣妙好：摩尼為臺，蓮華為網，妙寶為輪，雜華作瓔珞',
    'The lion throne, tall and broad: maṇi platform, lotus net, jeweled wheels, blossom necklaces',
    '其師子座，高廣妙好：摩尼為臺，蓮華為網','His lion throne, tall and broad: maṇi for its platform, lotus for its net.',
    'T10n0279 卷一·品首'),
 ]},
# ═══════════════════════════ 承幕 · 卷一末–卷二 ═══════════════════════════
{'no': '承', 'id': 'assumption', 'layout': 'assembly',
 'title_zh': '承 · 正觉广大 · 众海云集', 'title_en': 'Assumption: The Vastness of Awakening, the Assembly Gathered',
 'fascicle_zh': '卷一末–卷二', 'fascicle_en': 'End of fascicle 1 – fascicle 2',
 'lead_zh': '其身充滿一切世間，其音普順十方國土。',
 'lead_en': 'His body fills all the worlds; his voice accords with all lands of the ten directions.',
 'props': [
  P('awake','sun','成最正覺','Perfect awakening','於一切法成最正覺','He attained the unsurpassed right awakening to all phenomena.',level=0),
  P('void','void','虛空具含眾像','Space containing all images','譬如虛空具含眾像，於諸境界無所分別','Like space, which contains all images and distinguishes no realms.',level=0),
  P('hairtip','hairtip','毛端悉容世界','All worlds within a hair-tip','一一毛端，悉能容受一切世界而無障礙','In each single hair-tip he contains all worlds without obstruction.',level=0),
  P('onemind','void','一念悉包法界','In one thought, all of dharmadhātu','又以諸佛神力所加，一念之間，悉包法界','And by the power of the Buddhas, in a single moment he embraces all of dharmadhātu.',level=0),
  P('dwellings','assembly','眾生屋宅皆現影像','Dwellings of beings appear within','一切眾生居處屋宅，皆於此中現其影像','The dwellings of all sentient beings all appear within it.',level=1),
  P('samantabhadra','seat','普賢菩薩（十首之首）','Samantabhadra, first of the ten','其名曰：普賢菩薩摩訶薩','Their names are: Samantabhadra Bodhisattva, and the rest.',level=0,role='focus'),
  P('vajraspirit','ring','執金剛神','Vajra-holding spirits','復有佛世界微塵數執金剛神','There are further a dust-mote number of vajra-holding spirits.',level=0),
  P('cloudsea','assembly','道場眾海悉已雲集','The ocean of the field has gathered','爾時，如來道場眾海，悉已雲集','Then the ocean of the assembly at the Tathāgata\'s field had fully gathered.',level=0,role='focus'),
  P('variety','assembly','形色部從各各差別','Forms and colors, each distinct','無邊品類，周匝遍滿；形色部從，各各差別','Boundless in kind, filling all around; in form and color and array, each distinctly its own.',level=0),
  P('gaze','assembly','隨所來方一心瞻仰','Each facing the World-Honored One','隨所來方，親近世尊，一心瞻仰','Coming from whatever direction, they draw near the World-Honored One and gaze on him with one mind.',level=0),
  P('purity','light','摧重障山見佛無礙','The mountain of great obstacles shattered','此諸眾會，已離一切煩惱心垢及其餘習，摧重障山，見佛無礙','These assemblies had already left all mental defilement of passions and their residue, had shattered the mountain of great obstacles, and see the Buddha without hindrance.',level=0),
  P('heavens','ring','天王得解脫門','Celestial kings enter the liberations','妙焰海大自在天王，得法界、虛空界寂靜方便力解脫門','Maitreya-of-the-wondrous-sea, the Great Free One, obtained the liberation-door of the still and easy power of the dharmadhātu and the empty realm.',level=0),
 ],
 'shots': [
  S(14,'ecu','static',4.5,'awake',['awake'],
    '爾時，世尊處于此座，於一切法成最正覺',
    'Then, seated on this throne, the World-Honored One attained the unsurpassed right awakening to all phenomena',
    '於一切法成最正覺','He attained the unsurpassed right awakening to all phenomena.','T10n0279 卷一·世尊處座'),
  S(15,'ews','pull',5.0,'void',['void','hairtip','onemind'],
    '譬如虛空具含眾像；一一毛端，悉能容受一切世界',
    'Like space containing all images; in each hair-tip, all worlds',
    '譬如虛空具含眾像，於諸境界無所分別','Like space, which contains all images and distinguishes no realms.',
    'T10n0279 卷一·正覺段'),
  S(16,'ws','push',4.5,'samantabhadra',['samantabhadra','vajraspirit'],
    '普賢菩薩摩訶薩為十首之首；復有執金剛神',
    'Samantabhadra heads the ten foremost; and there are the vajra-holding spirits',
    '有十佛世界微塵數菩薩摩訶薩所共圍遶，其名曰：普賢菩薩摩訶薩',
    'Surrounded by a dust-mote number of bodhisattvas from ten Buddha-worlds, whose names are: Samantabhadra Bodhisattva...',
    'T10n0279 卷一·菩薩列名'),
  S(17,'ews','pull',5.5,'cloudsea',['cloudsea','variety','gaze','purity','heavens'],
    '如來道場眾海，悉已雲集；形色部從，各各差別，隨所來方，一心瞻仰',
    'The ocean of the assembly at the field has gathered; each from its own direction, gazing with one mind',
    '爾時，如來道場眾海，悉已雲集；無邊品類，周匝遍滿；形色部從，各各差別；隨所來方，親近世尊，一心瞻仰',
    'Then the ocean of the assembly at the Tathāgata\'s field had fully gathered; boundless in kind, filling all around; in form and color and array, each distinctly its own; coming from whatever direction, they drew near the World-Honored One and gazed on him with one mind.',
    'T10n0279 卷二·品首'),
 ]},
# ═══════════════════════════ 转幕 · 卷一–卷四 ═══════════════════════════
{'no': '转', 'id': 'transition', 'layout': 'classes',
 'title_zh': '转 · 逐类陈愿', 'title_en': 'Transition: Vows Uttered Class by Class',
 'fascicle_zh': '卷一–卷四', 'fascicle_en': 'Fascicles 1–4',
 'lead_zh': '皆於往昔無量劫中恒發大願，願常親近供養諸佛',
 'lead_en': 'In past eons without number they constantly formed great vows, wishing always to draw near and make offerings to the Buddhas.',
 'props': [
  P('bodyspirit','ring','身眾神','Body-spirits','有佛世界微塵數身眾神','There are a dust-mote number of body-spirits.',level=0),
  P('footspirit','ring','足行神','Foot-walking spirits','有佛世界微塵數足行神','There are a dust-mote number of foot-walking spirits.',level=0),
  P('fieldspirit','ring','道場神','Field spirits','復有佛世界微塵數道場神','There are further a dust-mote number of field-spirits.',level=0),
  P('cityspirit','ring','主城神','City-spirits','復有佛世界微塵數主城神','There are a dust-mote number of city-spirits.',level=0),
  P('earthspirit','ring','主地神','Earth-spirits','復有佛世界微塵數主地神','There are a dust-mote number of earth-spirits.',level=0),
  P('mountainspirit','ring','主山神','Mountain-spirits','復有無量主山神','There are further countless mountain-spirits.',level=0),
  P('forestspirit','ring','主林神','Forest-spirits','復有不可思議數主林神','There are further inconceivable numbers of forest-spirits.',level=0),
  P('herbspirit','ring','主藥神','Herb-spirits','復有無量主藥神','There are further countless herb-spirits.',level=0),
  P('gandharva','ring','持國乾闥婆王','The gandharva king Dhrtarastra','復次，持國乾闥婆王，得自在方便攝一切眾生解脫門','Then King Dhrtarastra the gandharva obtained the liberation-door of the self-wielding expedient that gathers all beings.',level=0,role='focus'),
  P('firegod','ring','普光焰藏主火神','The fire-spirit Praphu-rakshita','復次，普光焰藏主火神，得悉除一切世間闇解脫門','Then the fire-spirit Great Light Flame-Treasure obtained the liberation-door of totally removing the darkness of the world.',level=0,role='focus'),
  P('vow1','light','同修福業','Practicing virtue together','皆於往昔發深重願，願常親近諸佛如來，同修福業','In past lives they formed profound vows, wishing always to draw near the Buddhas and practice virtue together.',level=0),
  P('vow2','light','嚴淨如來所居宮殿','Purifying the Buddha\'s abiding palace','皆於無量不思議劫，嚴淨如來所居宮殿','Throughout countless inconceivable eons they purify the palace wherein the Tathāgata abides.',level=0),
  P('vow3','light','性皆離垢，仁慈祐物','Free of defilement, benign toward beings','其數無量，性皆離垢，仁慈祐物','Their number is countless; all are free of defilement, benign and assisting beings.',level=0),
 ],
 'shots': [
  S(18,'ms','pan_right',4.0,'bodyspirit',['bodyspirit','footspirit'],
    '身眾神、足行神：親近如來，隨逐不捨','Body-spirits and foot-walking spirits: following the Buddha unfailingly',
    '有佛世界微塵數身眾神','There are a dust-mote number of body-spirits.','T10n0279 卷一·列名'),
  S(19,'ms','pan_left',4.0,'fieldspirit',['fieldspirit','cityspirit','earthspirit'],
    '道場神、主城神、主地神：嚴淨宮殿，同修福業','Field-, city- and earth-spirits: purifying the palace, practicing virtue together',
    '皆於無量不思議劫，嚴淨如來所居宮殿','Throughout countless inconceivable eons they purify the palace wherein the Tathāgata abides.',
    'T10n0279 卷一·主城神'),
  S(20,'ws','pan_right',4.5,'mountainspirit',['mountainspirit','forestspirit','herbspirit'],
    '主山神、主林神、主藥神：性皆離垢，仁慈祐物','Mountain-, forest- and herb-spirits: all free of defilement, benign to beings',
    '其數無量，性皆離垢，仁慈祐物','Their number is countless; all are free of defilement, benign and assisting beings.',
    'T10n0279 卷一·主藥神'),
  S(21,'ws','push',4.5,'gandharva',['gandharva'],
    '持國乾闥婆王得自在方便攝一切眾生解脫門',
    'King Dhrtarastra the gandharva obtained the liberation-door of gathering all beings',
    '復次，持國乾闥婆王，得自在方便攝一切眾生解脫門',
    'Then King Dhrtarastra the gandharva obtained the liberation-door of the self-wielding expedient that gathers all beings.',
    'T10n0279 卷三·品首'),
  S(22,'ws','push',4.5,'firegod',['firegod'],
    '普光焰藏主火神得悉除一切世間闇解脫門',
    'The fire-spirit Great Light Flame-Treasure obtained the liberation-door of removing all worldly darkness',
    '復次，普光焰藏主火神，得悉除一切世間闇解脫門',
    'Then the fire-spirit Great Light Flame-Treasure obtained the liberation-door of totally removing the darkness of the world.',
    'T10n0279 卷四·品首'),
 ]},
# ═══════════════════════════ 合幕 · 卷五 ═══════════════════════════
{'no': '合', 'id': 'coda', 'layout': 'mandala',
 'title_zh': '合 · 普贤入三昧 · 四十类总现 · 卷末颂别', 'title_en': 'Coda: Samantabhadra Enters the Ocean of Merit, the Forty Classes Appear, the Final Verse',
 'fascicle_zh': '卷五', 'fascicle_en': 'Fascicle 5',
 'lead_zh': '復次，普賢菩薩摩訶薩，入不思議解脫門方便海，入如來功德海。',
 'lead_en': 'Then Samantabhadra Bodhisattva entered the ocean of the inconceivable liberation-doors and expedients, and the ocean of the Buddhas\'s merits.',
 'note_zh': '【据回源更正】台账 L.94⑩-3 原拟「合（四十类云集·卷末回向）」。实测卷五内「迴向」二字为 0 次，'
            '卷五以妙色那羅延執金剛神之頌收束（「…示佛所行處。」），故不作回向；'
            '「四十类云集」之真锚点为卷二开篇「眾海悉已雲集」（已置于承幕第 17 镜）。',
 'note_en': 'Correction: the originally planned "closing dedication" does not exist — the word 迴向 occurs zero times in fascicle 5, '
            'which closes instead with the verse of the vajra-holding spirit Vimalaprabha.',
 'props': [
  P('samantabhadra','seat','普賢菩薩入三昧','Samantabhadra enters the samadhi','復次，普賢菩薩摩訶薩，入不思議解脫門方便海，入如來功德海','Then Samantabhadra Bodhisattva entered the ocean of the inconceivable liberation-doors and expedients, and the ocean of the Buddhas\'s merits.',level=0,role='focus'),
  P('gate1','gate','嚴淨一切佛國土','Purifying all Buddhaland','有解脫門，名：嚴淨一切佛國土調伏眾生令究竟出離','There is a liberation-door named: purifying all Buddhaland and taming sentient beings, bringing them to final release.',level=1),
  P('gate2','gate','普現微塵數無量身','Manifesting countless bodies','有解脫門，名：普現法界微塵數無量身','There is a liberation-door named: universally manifesting countless bodiless bodies.',level=1),
  P('gate3','gate','一念現三世劫成壞','A moment containing aeons','有解脫門，名：一念中現三世劫成壞事','There is a liberation-door named: within a single moment, manifesting the arising and perishing of aeons across the three times.',level=1),
  P('gaze_all','assembly','普觀一切眾會海','Surveying the whole ocean of assemblies','普觀一切眾會海已，即說頌言','Having surveyed the whole ocean of assemblies, he spoke this verse.',level=0),
  P('mandala','mandala','四十類雲集（曼荼羅全景）','The forty classes gathered (mandala view)','爾時，如來道場眾海，悉已雲集','Then the ocean of the assembly at the Tathāgata\'s field had fully gathered.',level=0,rings_ref='miaoyan_narrative.yaml:space.rings'),
  P('final','sound','卷末頌：示佛所行處','Final verse: showing where the Buddha walks','焰雲普照明，種種光圓滿，法界無不及，示佛所行處','Flame-clouds shine everywhere, all lights made full, nothing of dharmadhātu unreached — showing where the Buddha walks.',level=0,role='focus'),
 ],
 'shots': [
  S(23,'ms','push',5.0,'samantabhadra',['samantabhadra'],
    '普賢菩薩摩訶薩，入不思議解脫門方便海，入如來功德海',
    'Samantabhadra entered the ocean of inconceivable liberation-doors and the ocean of merit',
    '復次，普賢菩薩摩訶薩，入不思議解脫門方便海，入如來功德海',
    'Then Samantabhadra Bodhisattva entered the ocean of the inconceivable liberation-doors and expedients, and the ocean of the Buddhas\'s merits.',
    'T10n0279 卷五·品首'),
  S(24,'ws','orbit',5.0,'gate1',['gate1','gate2','gate3','gaze_all'],
    '十解脫門；普觀一切眾會海已，即說頌言','The ten liberation-doors; having surveyed all assemblies, he spoke verse',
    '普觀一切眾會海已，即說頌言','Having surveyed the whole ocean of assemblies, he spoke this verse.',
    'T10n0279 卷五·普賢頌'),
  S(25,'ews','static',6.0,'mandala',['mandala'],
    '四十類雲集——六環曼荼羅全景（40 類／414 名）',
    'The forty classes gathered — the six-ring mandala in full (40 classes / 414 named)',
    '爾時，如來道場眾海，悉已雲集','Then the ocean of the assembly at the Tathāgata\'s field had fully gathered.',
    'T10n0279 卷二·品首（钟位数据依 miaoyan_assembly.yaml）',
    True,'曼荼罗六环之环数、环距、环位及各类之代表点分布，属现代重构；'
        '经文唯言「眾海悉已雲集」「無邊品類」，未陈方位与排列。四十类／414名之数则出 assembly 实测。'),
  S(26,'ecu','static',5.0,'final',['final'],
    '焰雲普照明，種種光圓滿，法界無不及，示佛所行處',
    'Flame-clouds shine everywhere, all lights made full, nothing of dharmadhātu unreached — showing where the Buddha walks',
    '焰雲普照明，種種光圓滿，法界無不及，示佛所行處',
    'Flame-clouds shine everywhere, all lights made full, nothing of dharmadhātu unreached — showing where the Buddha walks.',
    'T10n0279 卷五·妙色那羅延執金剛神頌（卷末）'),
 ]},
]

DATA = {'meta': META, 'shot_sizes': SHOT_SIZES, 'camera_moves': CAMERA_MOVES,
        'corrections': [
  {'no': 1, 'zh': '普賢入三昧在卷五开篇（已移入合幕第 23 镜）；卷一仅作列名上首（第 16 镜）',
   'en': 'Samantabhadra\'s entry into the samadhi is at the opening of fascicle 5 (shot 23); in fascicle 1 he appears only as first among the named (shot 16).'},
  {'no': 2, 'zh': '卷五内「迴向」0 次，「卷末回向」不成立，合幕改为「卷末頌別」',
   'en': 'The word 迴向 occurs zero times in fascicle 5; the planned "closing dedication" does not exist, so the coda closes with a verse.'},
  {'no': 3, 'zh': '「四十類雲集」真锚点在卷二开篇「眾海悉已雲集」（置于承幕第 17 镜），非卷末',
   'en': 'The true anchor for "the forty classes gathered" is at the opening of fascicle 2 (shot 17), not the end.'},
 ], 'acts': ACTS}

# ── 断言：一切引文逐字见于底本 ─────────────────────────────
allq, miss = [], []
for a in ACTS:
    allq.append(a['lead_zh'])
    for p in a['props']:
        allq.append(p['quote_zh'])
    for s in a['shots']:
        allq.append(s['quote_zh'])
miss = [q for q in allq if re.sub(r'\s+', '', q) not in TXT]
if miss:
    print('❌ 引文未见于底本：')
    for q in miss: print('   ✗', q)
    raise SystemExit(1)

ns = sum(len(a['shots']) for a in ACTS)
dur = sum(s['duration_s'] for a in ACTS for s in a['shots'])
print(f'✅ {len(ACTS)} 幕 / {ns} 镜 / 总时长 {dur}s / 引文 {len(allq)} 句——逐字见于 T279')

# 契约断言
for a in ACTS:
    ids = {p['id'] for p in a['props']}
    for s in a['shots']:
        assert s['size'] in SHOT_SIZES, f"第{s['no']}镜景别未注册"
        assert s['move'] in CAMERA_MOVES, f"第{s['no']}镜运镜未注册"
        assert 3.0 <= s['duration_s'] <= 7.0, f"第{s['no']}镜时长越界"
        if s['reconstruction']: assert s.get('judgment_zh'), f"第{s['no']}镜标了重构却无判断说明"
        # subject 或为 null（全镜总览，无单一主体，如第 1 镜），或必为本幕 props 之实有；
        # focus 恒须为本幕 props 之实有，否则渲染器的高亮框与标名将指向不存在的图元
        assert s['subject'] is None or s['subject'] in ids, \
            f"第{s['no']}镜 subject 非本幕要素：{s['subject']!r}"
        assert s['focus'], f"第{s['no']}镜无 focus"
        for f in s['focus']:
            assert f in ids, f"第{s['no']}镜 focus 非本幕要素：{f}"
nos = [s['no'] for a in ACTS for s in a['shots']]
assert nos == list(range(1, ns + 1)), '镜号不连续'
# 全片曼荼罗图元有且仅一，且必在合幕
mand = [(a['no'], p['id']) for a in ACTS for p in a['props'] if p['kind'] == 'mandala']
assert mand == [('合', 'mandala')], f'曼荼罗图元应唯一且在合幕，实为 {mand}'
print('✅ 契约：景别／运镜皆已注册、时长皆在 3–7s、〔本文判断〕皆有说明、镜号 1–%d 连续' % ns)
print('✅ 契约：subject/focus 皆为本幕要素（subject 允许 null 表全镜）、曼荼罗唯一且在合幕')

out = ROOT / "data" / "narrative" / "miaoyan_storyboard.yaml"
out.parent.mkdir(parents=True, exist_ok=True)
hdr = ('# 世主妙严品 · 电影式分镜数据（序/承/转/合 · 26 镜）\n'
       '# 一切引文逐字见于 CBETA T10n0279（八十华严·实叉难陀译）；本文件由脚本生成并附核验断言。\n'
       '# 空间关系/取景/运镜/光色氛围为现代视觉重构，凡此标 reconstruction: true 并附 judgment_zh。\n')
out.write_text(hdr + yaml.safe_dump(DATA, allow_unicode=True, sort_keys=False,
                                    width=100, default_flow_style=False), encoding='utf-8')
print(f'   写入 {out.relative_to(ROOT)} · {out.stat().st_size:,} B')

d2 = yaml.safe_load(out.read_text(encoding='utf-8'))
assert len(d2['acts']) == 4 and sum(len(a['shots']) for a in d2['acts']) == ns
print('✅ 回读复验通过')