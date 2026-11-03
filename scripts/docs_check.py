#!/usr/bin/env python3
"""Minimal documentation checks with no external dependencies."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "node_modules"}
problems = []
warnings = []


def check(path):
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    if not text.endswith(chr(10)):
        problems.append(str(rel) + ": 文件末尾缺少换行")
    level = 0
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith(("<" * 7, "=" * 7, ">" * 7)):
            problems.append(str(rel) + ":" + str(number) + ": 存在合并冲突标记")
        if line.rstrip() != line:
            problems.append(str(rel) + ":" + str(number) + ": 行尾有多余空格")
        if chr(9) in line:
            problems.append(str(rel) + ":" + str(number) + ": 含制表符")
        match = re.match("^(#{1,6})[ ]", line)
        if match:
            current = len(match.group(1))
            if level == 0 and current != 1:
                warnings.append(str(rel) + ":" + str(number) + ": 第一个标题不是一级标题")
            if level and current > level + 1:
                warnings.append(str(rel) + ":" + str(number) + ": 标题层级跳跃")
            level = current


for md in sorted(ROOT.rglob("*.md")):
    if SKIP & set(md.relative_to(ROOT).parts):
        continue
    check(md)

if warnings:
    print("warnings:")
    print(chr(10).join(warnings))
if problems:
    print(chr(10).join(problems))
    sys.exit(1)
print("docs check passed")
