"""catalog 子命令 — 文献目录库初始化.

`init` 只建 schema（data/catalog/schema.sql → huayan.db）。
数据导入与 backfill 仍在 scripts/（import_all_to_sqlite.py · backfill_*.py），
完整重建链见 Makefile `db-rebuild` 目标。
"""
import sqlite3
from pathlib import Path

import click

ROOT = Path(__file__).resolve().parents[2]  # src/cli/catalog.py → 仓根
DEFAULT_DB = ROOT / "data" / "catalog" / "huayan.db"
SCHEMA_PATH = ROOT / "data" / "catalog" / "schema.sql"


@click.group()
def catalog():
    """文献目录管理（SQLite catalog）。"""


@catalog.command()
@click.option("--db", "db_path", type=click.Path(path_type=Path), default=None,
              help="目标 DB 路径（默认 data/catalog/huayan.db）")
@click.option("--if-missing", is_flag=True,
              help="仅缺库时创建 · 绝不删除已存在的 DB（安全模式）")
def init(db_path, if_missing):
    """从 schema.sql 初始化目录库。"""
    target = db_path or DEFAULT_DB
    if target.exists():
        if if_missing:
            click.echo(f"已存在 · 跳过: {target}")
            return
        target.unlink()
        click.echo(f"Removed old {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target))
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    conn.close()
    click.echo(f"Created {target}")
    click.echo(f"Tables ({len(tables)}): {tables}")
