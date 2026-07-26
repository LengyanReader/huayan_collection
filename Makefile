# 华严宗部文献梳理项目 — Makefile
# 使用 conda 环境 hy_py312

CONDA_ENV = hy_py312
CONDA_PYTHON = $(HOME)/miniconda3/envs/$(CONDA_ENV)/python.exe
PIP = $(CONDA_PYTHON) -m pip
PYTHON = $(CONDA_PYTHON)

# Neo4j 本地路径
NEO4J_HOME = $(HOME)/neo4j-community-5.26.4
JAVA_HOME = "C:/Program Files/Java/jdk-20"

.PHONY: install install-dev db-init db-reset neo4j-start neo4j-console neo4j-stop neo4j-status graph-init lint test clean env-info verify-sources verify-data demo demo-build demo-verify demo-serve demo-deploy

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
	$(PYTHON) -c "from src.cli.main import cli; cli(['catalog', 'init'])"

db-reset:
	rm -f data/catalog/huayan.db
	$(PYTHON) -c "from src.cli.main import cli; cli(['catalog', 'init'])"

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

test:
	$(PYTHON) -m pytest -v

## 信息校验
verify-sources:
	$(PYTHON) scripts/verify_sources.py --fixme

verify-sources-json:
	$(PYTHON) scripts/verify_sources.py --json

verify-data: verify-sources
	@echo "Data validation complete."

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
	git add web/demo/index.html
	git commit -m "deploy: demo update" || true
	git push origin main
	@echo "Deployed. Wait ~2min for GitHub Pages CDN."

## 清理
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
