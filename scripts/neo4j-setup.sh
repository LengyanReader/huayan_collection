#!/usr/bin/env bash
# ============================================================
# 华严项目 — Neo4j 初始化设置脚本 (Git Bash / WSL)
# 1. 设置初始密码
# 2. 运行 Cypher 初始化脚本创建 Schema
# ============================================================
set -euo pipefail

NEO4J_HOME="${USERPROFILE}/neo4j-community-5.26.4"
export JAVA_HOME="C:/Program Files/Java/jdk-20"
export PATH="${JAVA_HOME}/bin:${PATH}"

echo "=== Neo4j 初始化设置 ==="

# Step 1: Set initial password
echo "[1/3] Setting initial password..."
"${NEO4J_HOME}/bin/neo4j-admin.bat" dbms set-initial-password huayan2024 2>/dev/null || \
  echo "  (password may already be set, continuing...)"

echo "[2/3] Schema and seed data will be loaded via:"
echo "  huayan graph init"
echo "  huayan graph load"

echo "[3/3] Done. Start Neo4j with:"
echo "  cmd.exe /c scripts\\\\neo4j-start.bat console"
