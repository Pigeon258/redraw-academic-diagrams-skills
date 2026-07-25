#!/usr/bin/env python3
"""汇总双 Skill 的匿名化正式使用记录。"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_records(path: Path) -> list[dict[str, Any]]:
    """加载 JSONL，并给出明确的坏行错误。"""
    records: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"第 {number} 行不是有效 JSON：{exc}") from exc
    return records


def summarize_group(records: list[dict[str, Any]]) -> dict[str, Any]:
    """生成单个 Skill 的描述性统计，不自动宣称优胜。"""
    numeric = (
        "first_minutes",
        "total_minutes",
        "user_edit_minutes",
        "ai_revision_minutes",
        "feedback_rounds",
        "fixlist_count",
    )
    result: dict[str, Any] = {
        "runs": len(records),
        "accepted_runs": sum(bool(item.get("final_accepted")) for item in records),
        "practical_states": dict(
            Counter(item.get("practical_state") for item in records)
        ),
        "formal_states": dict(Counter(item.get("formal_state") for item in records)),
        "builders": dict(Counter(item.get("builder") for item in records)),
    }
    for field in numeric:
        values = [float(item[field]) for item in records if field in item]
        result[field] = {
            "median": statistics.median(values) if values else None,
            "mean": statistics.fmean(values) if values else None,
        }
    return result


def main() -> int:
    """生成按 Skill 分组的 JSON 汇总。"""
    parser = argparse.ArgumentParser(description="汇总双 Skill 正式使用记录。")
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not args.store.is_file():
        parser.error(f"记录文件不存在：{args.store}")
    try:
        records = load_records(args.store)
    except ValueError as exc:
        parser.error(str(exc))

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[str(record.get("skill", "unknown"))].append(record)

    report = {
        "record_count": len(records),
        "groups": {
            name: summarize_group(items) for name, items in sorted(grouped.items())
        },
        "decision": (
            "FIELD DATA REQUIRED"
            if len(grouped) < 2
            else "DESCRIPTIVE ONLY — review task complexity and toolchain confounders"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"汇总已生成：{args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
