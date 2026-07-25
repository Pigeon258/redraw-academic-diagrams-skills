#!/usr/bin/env python3
"""验证公开仓库结构、Skill 元数据、Python 语法和隐私边界。"""

from __future__ import annotations

import py_compile
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
PRIVATE_PATTERNS = {
    "windows_absolute_path": re.compile(
        r"[A-Za-z]:\\(?:Users|Files|AppData|Documents|Downloads)\\",
        re.IGNORECASE,
    ),
    "private_chat_id": re.compile(r"wxid_", re.IGNORECASE),
    "wechat_cache": re.compile(r"xwechat|AppFiles", re.IGNORECASE),
    "local_username": re.compile(r"C:/Users/|C:\\\\Users\\\\", re.IGNORECASE),
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    """读取仅包含简单键值的 YAML frontmatter。"""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"缺少 frontmatter：{path}")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"frontmatter 未闭合：{path}") from exc
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"frontmatter 行无冒号：{path}: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def validate_skill(path: Path) -> list[str]:
    """验证一个公开 Skill 的最低结构。"""
    errors: list[str] = []
    skill_md = path / "SKILL.md"
    version = path / "VERSION"
    agents = path / "agents" / "openai.yaml"
    for required in (skill_md, version, agents):
        if not required.is_file():
            errors.append(f"缺少文件：{required.relative_to(ROOT)}")
    if not skill_md.is_file():
        return errors
    try:
        meta = parse_frontmatter(skill_md)
    except ValueError as exc:
        errors.append(str(exc))
        return errors
    name = meta.get("name", "")
    if name != path.name:
        errors.append(f"Skill 名称与目录不一致：{path.name} != {name}")
    if not NAME_RE.fullmatch(name):
        errors.append(f"Skill 名称不合法：{name}")
    if not meta.get("description"):
        errors.append(f"缺少 description：{path.name}")
    if len(skill_md.read_text(encoding="utf-8-sig").splitlines()) > 500:
        errors.append(f"SKILL.md 超过 500 行：{path.name}")
    return errors


def privacy_scan() -> list[str]:
    """扫描公开文本中的明显私人路径和聊天缓存标记。"""
    errors: list[str] = []
    extensions = {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".svg"}
    detector_sources = {
        Path("scripts/validate_public_repo.py"),
        Path("evaluation/record_field_run.py"),
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        if path.relative_to(ROOT) in detector_sources:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label}：{path.relative_to(ROOT)}")
    return errors


def main() -> int:
    """执行全部公开仓库检查。"""
    errors: list[str] = []
    expected = {
        "redraw-academic-diagrams",
        "redraw-academic-diagrams-fast",
    }
    actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    if actual != expected:
        errors.append(f"Skill 集合不匹配：{sorted(actual)}")
    for path in sorted(SKILLS.iterdir()):
        if path.is_dir():
            errors.extend(validate_skill(path))
    errors.extend(privacy_scan())
    for path in ROOT.rglob("*.py"):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"Python 语法错误：{path.relative_to(ROOT)}: {exc}")
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1
    print("公开仓库验证通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
