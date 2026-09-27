# 华严宗部文献梳理项目 — Makefile
# 使用 conda 环境 hy_py312

CONDA_ENV = hy_py312
CONDA_PYTHON = $(HOME)/miniconda3/envs/$(CONDA_ENV)/python.exe
PIP = $(CONDA_PYTHON) -m pip
PYTHON = $(CONDA_PYTHON)

# Neo4j 本地路径
NEO4J_HOME = $(HOME)/neo4j-community-5.26.4
JAVA_HOME = "C:/Program Files/Java/jdk-20"

.PHONY: install install-dev db-init db-reset db-rebuild neo4j-start neo4j-console neo4j-stop neo4j-status graph-init lint test test-pipeline clean env-info verify-sources verify-data verify-all demo demo-build demo-verify demo-serve demo-deploy evolve evolve-apply evolve-links evolve-ledger

## 环境信息
env-info:
	@echo "Conda env:  $(CONDA_ENV)"
	@echo "Python:     $$( $(PYTHON) --version 2>&1 )"
	@echo "Neo4j:      $(NEO4J_HOME)"
	@echo "Java:       $(JAVA_HOME)"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"

install-all:
	$(PIP) install -e ".[dev,web,ner]"

## 数据库 (SQLite)
db-init:
	$(PYTHON) -c "from src.cli.main import cli; cli(['catalog', 'init', '--if-missing'])"

db-reset:
	@echo "⚠️ db-reset 删除 huayan.db · backfill 人工订正若未入快照会丢 · 建议先: python scripts/db_backup.py --snapshot"
	rm -f data/catalog/huayan.db
	$(PYTHON) -c "from src.cli.main import cli; cli(['catalog', 'init'])"

## 完整重建链(源头=git 内 YAML/JSON+脚本 · 尾端=快照入库 · 2026-09-27 事故后可复现)
db-rebuild: db-reset
	$(PYTHON) scripts/import_all_to_sqlite.py
	$(PYTHON) scripts/backfill_core_sources.py
	$(PYTHON) scripts/backfill_secondary_sources.py
	$(PYTHON) scripts/backfill_chapters_title_en.py
	$(PYTHON) scripts/backfill_location_sources.py
	$(PYTHON) scripts/rebuild_fts.py
	$(PYTHON) scripts/db_backup.py --snapshot
	$(PYTHON) scripts/db_backup.py --verify
	@echo "重建完成 · 把 data/catalog/backups/huayan_latest.sql 随代码一起 commit"

## 图谱 (Neo4j)
neo4j-console:
	@echo "Starting Neo4j in console mode..."
	cmd.exe /c "set JAVA_HOME=$(JAVA_HOME)&& $(NEO4J_HOME)\bin\neo4j.bat console"

neo4j-start:
	cmd.exe /c "set JAVA_HOME=$(JAVA_HOME)&& $(NEO4J_HOME)\bin\neo4j.bat start"

neo4j-stop:
	cmd.exe /c "set JAVA_HOME=$(JAVA_HOME)&& $(NEO4J_HOME)\bin\neo4j.bat stop"

neo4j-status:
	cmd.exe /c "set JAVA_HOME=$(JAVA_HOME)&& $(NEO4J_HOME)\bin\neo4j.bat status"

graph-init:
	$(PYTHON) -c "from src.cli.main import cli; cli(['graph', 'init'])"

graph-load:
	$(PYTHON) -c "from src.cli.main import cli; cli(['graph', 'load'])"

## 代码质量
lint:
	$(PYTHON) -m ruff check src/
	$(PYTHON) -m ruff check scripts/ --select F,E9 --extend-ignore F841  ## scripts 存量宽仅错误级·F841(占位变量4处)登记豁免

test:
	$(PYTHON) -m pytest -v

test-pipeline:
	$(PYTHON) scripts/test_pipeline.py

## 信息校验
verify-sources:
	$(PYTHON) scripts/verify_sources.py --fixme

verify-sources-json:
	$(PYTHON) scripts/verify_sources.py --json

verify-data: verify-sources
	-$(PYTHON) scripts/audit_consistency.py
	-$(PYTHON) scripts/check_drift.py || echo "↑ 派生副本漂移已检出 · 处置(同步/移除 docs 副本)待维护者定 · 暂不阻塞"
	@echo "Data validation complete."

## 全量验收（三道闸 · 会话收尾必跑；详 harness/workflows/verification.md）
verify-all: test-pipeline demo-verify verify-sources
	@echo "All verification gates ran. 任一未绿不得声称完成。"

## Demo (web/demo/index.html)
demo-build:
	cd web/demo && $(PYTHON) scripts/build.py

demo-verify:
	$(PYTHON) scripts/verify_demo.py

demo-serve:
	@echo "Starting local server at http://localhost:8080"
	cd web/demo && $(PYTHON) -m http.server 8080

demo: demo-build demo-verify
	@echo "Demo built and verified. Run 'make demo-serve' for local testing."

demo-deploy: demo
	git add web/demo/
	git commit -m "deploy: rebuild demo (tabs/articles/assets)" || true
	@echo "已本地 commit · 按项目规矩不自动 push · 确认无误后手动: git push origin main"
	@echo "Pages 源=main 根 · push 后等 ~2min CDN 刷新。"
	@echo "NOTE: 海云讲法正文 txt 属 docs/huayanhai/，须另行提交（见 harness/workflows/deploy.md）。"

## 自我进化机制 (docs/self-evolution.md)
evolve:
	$(PYTHON) scripts/self_evolve.py

evolve-apply:
	$(PYTHON) scripts/self_evolve.py --apply

evolve-links:
	$(PYTHON) scripts/self_evolve.py --check-links

evolve-ledger:
	$(PYTHON) scripts/self_evolve.py --ledger

## 清理
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
