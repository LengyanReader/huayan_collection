# 藏文版《华严经》（BDRC T00AG0322）

## 来源
- **BDRC 资源**: [bdr:T00AG0322](https://library.bdrc.io/show/bdr:T00AG0322?uilang=zh)
- **Topic**: Avataṃsaka Sūtra (华严经)
- **Instance**: bdr:MW1PD96685（Choni Kangyur，德格版，108卷）
- **Section**: bdr:MW1PD96685_S0010（phal chen / 华严经）
- **卷范围**: 卷89-94（6卷，共3,428页）

## 下载方式
使用 BDRC IIIF 图像服务直接下载：
```
https://iiif.bdrc.io/bdr:I1PD105XXX::I1PD105XXX0YYY.jpg/full/full/0/default.jpg
```
- XXX = 卷号后3位（152-157）
- YYY = 页码（零填充4位）

## 目录结构
```
T00AG0322/
├── metadata.json          # 元数据
├── README.md              # 本文件
└── images/
    ├── vol_089/           # 卷89 (568页)
    ├── vol_090/           # 卷90 (574页)
    ├── vol_091/           # 卷91 (592页)
    ├── vol_092/           # 卷92 (526页)
    ├── vol_093/           # 卷93 (594页)
    └── vol_094/           # 卷94 (574页)
```

## 许可
- BDRC 访问策略：[https://www.bdrc.io/access-policies/](https://www.bdrc.io/access-policies/)
- 本资源为开放访问（AccessOpen）
- 仅供学术研究使用

## 下载脚本
```bash
python scripts/download_avatamsaka.py --resume
```

## 验证
下载完成后，检查每个卷目录的文件数量是否与 metadata.json 中的 total_pages 一致。