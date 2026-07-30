---
name: auto-push-after-changes
description: 每轮修改完成后自动 git commit + push
metadata:
  type: feedback
---

每完成一轮工作修改，在验证通过后自动执行 `git add -A` + `git commit` + `git push`，无需等待用户提醒。

推送范围: **所有未被 .gitignore 忽略的改动**，包括但不限于代码文件、文档、plan 文件、memory 文件、数据文件、配置文件等。

**Why:** 用户明确要求"自动push包含所有的改动，比如文档，代码，等等未被ignore的内容"。

**How to apply:** 每轮工作收尾时：构建 → 验证通过 → `git add -A` → `git commit`（中文描述）→ `git push`。
