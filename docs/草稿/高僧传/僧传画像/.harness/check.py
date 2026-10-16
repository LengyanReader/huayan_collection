#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check.py · 僧传画像 harness self-check (M3 gate, strict)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # 僧传画像/
MANIFEST = ROOT / ".harness" / "manifest.json"

def check_files():
    """Every file in manifest.files must exist on disk."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    missing = [f for f in m["files"] if not (ROOT / f).exists()]
    return missing

def check_placeholders():
    """No unrendered {{placeholder}} or TODO_unresolved markers."""
    pat = re.compile(r"\{\{[^}]+\}\}|TODO_unresolved")
    hits = []
    this = Path(__file__).resolve()
    harness_dir = ROOT / ".harness"
    for f in ROOT.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".json", ".py") and f.resolve() != this and harness_dir not in f.parents:
            try:
                for line in f.read_text(encoding="utf-8").splitlines():
                    if pat.search(line):
                        hits.append(f"{f.relative_to(ROOT)}: {line.strip()[:60]}")
            except (UnicodeDecodeError, PermissionError):
                pass
    return hits

def check_plan_sections():
    """PLAN.md must have ## Goal, ## DoD, ## First move."""
    plan = ROOT / "tasks" / "PLAN.md"
    if not plan.exists():
        return ["tasks/PLAN.md not found"]
    text = plan.read_text(encoding="utf-8")
    required = ["## Goal", "## DoD", "## First move"]
    return [r for r in required if r not in text]

def main():
    print("=" * 50)
    print("  僧传画像 · harness check (strict)")
    print("=" * 50)
    ok = True

    missing = check_files()
    print(f"[{'PASS' if not missing else 'FAIL'}] manifest files exist ({len(missing)} missing)")
    if missing: ok=False; [print(f"  MISS: {m}") for m in missing]

    ph = check_placeholders()
    print(f"[{'PASS' if not ph else 'FAIL'}] no unrendered placeholders ({len(ph)} found)")
    if ph: ok=False; [print(f"  HIT: {p}") for p in ph[:5]]

    sec = check_plan_sections()
    print(f"[{'PASS' if not sec else 'FAIL'}] PLAN sections present ({len(sec)} missing)")
    if sec: ok=False; [print(f"  MISS: {s}") for s in sec]

    print("=" * 50)
    if ok:
        print("ALL CHECKS PASSED")
        sys.exit(0)
    else:
        print("CHECK FAILED — see above")
        sys.exit(1)

if __name__ == "__main__":
    main()
