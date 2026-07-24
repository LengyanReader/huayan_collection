"""华严宗部文献梳理 CLI 主入口.

子命令模块将在后续阶段逐步实现:
  catalog   — 文献目录管理
  graph     — 知识图谱构建
  translate — 藏汉华严对译
"""

import click


@click.group()
@click.version_option(version="0.1.0", prog_name="huayan")
def cli():
    """华严宗部文献与修行资料数字化梳理平台."""


# 子命令将在对应模块实现后注册
# cli.add_command(catalog)
# cli.add_command(graph)
# cli.add_command(translate)


if __name__ == "__main__":
    cli()
