#!/usr/bin/env python3
"""记录一条匿名化的真实科研图重绘使用结果。"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


SKILLS = {"redraw-academic-diagrams", "redraw-academic-diagrams-fast"}
PRACTICAL_STATES = {
    "FAST PASS",
    "FAST PASS WITH FIXLIST",
    "FAST-NOT-ACCEPTABLE",
}
FORMAL_STATES = {
    "BLOCKED",
    "NEEDS REVISION",
    "CONDITIONAL",
    "PASS",
    "PASS—POLISHED",
    "NOT EVALUATED",
}
PRIVATE_PATTERNS = (
    re.compile(r"[A-Za-z]:\\"),
    re.compile(r"/(?:home|Users)/"),
    re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    re.compile(r"wxid_", re.IGNORECASE),
)


def ensure_public_text(label: str, value: str) -> str:
    """拒绝明显包含绝对路径、邮箱或聊天账号的字段。"""
    if any(pattern.search(value) for pattern in PRIVATE_PATTERNS):
        raise ValueError(f"{label} 可能包含隐私或绝对路径，请先匿名化。")
    return value.strip()


def nonnegative(value: str) -> float:
    """解析非负时间或计数。"""
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("数值不得为负。")
    return number


def main() -> int:
    """解析参数并追加 JSONL 记录。"""
    parser = argparse.ArgumentParser(description="记录匿名化双 Skill 正式使用结果。")
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--skill", choices=sorted(SKILLS), required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--diagram-class", required=True)
    parser.add_argument("--builder", required=True)
    parser.add_argument("--first-minutes", type=nonnegative, required=True)
    parser.add_argument("--total-minutes", type=nonnegative, required=True)
    parser.add_argument("--user-edit-minutes", type=nonnegative, default=0)
    parser.add_argument("--ai-revision-minutes", type=nonnegative, default=0)
    parser.add_argument("--feedback-rounds", type=int, default=0)
    parser.add_argument(
        "--practical-state", choices=sorted(PRACTICAL_STATES), required=True
    )
    parser.add_argument("--formal-state", choices=sorted(FORMAL_STATES), required=True)
    parser.add_argument("--fixlist-count", type=int, default=0)
    parser.add_argument("--defect", action="append", default=[])
    parser.add_argument("--note", action="append", default=[])
    parser.add_argument("--final-accepted", action="store_true")
    args = parser.parse_args()

    if args.feedback_rounds < 0 or args.fixlist_count < 0:
        parser.error("轮次和 fixlist 数量不得为负。")
    if args.total_minutes < args.first_minutes:
        parser.error("总时间不得小于首轮时间。")
    if (
        args.practical_state == "FAST PASS WITH FIXLIST"
        and args.fixlist_count == 0
    ):
        parser.error("FAST PASS WITH FIXLIST 必须记录至少一个 fixlist 项。")

    try:
        record = {
            "recorded_utc": datetime.now(timezone.utc).isoformat(),
            "task_id": ensure_public_text("task-id", args.task_id),
            "skill": args.skill,
            "version": ensure_public_text("version", args.version),
            "diagram_class": ensure_public_text(
                "diagram-class", args.diagram_class
            ),
            "builder": ensure_public_text("builder", args.builder),
            "first_minutes": args.first_minutes,
            "total_minutes": args.total_minutes,
            "user_edit_minutes": args.user_edit_minutes,
            "ai_revision_minutes": args.ai_revision_minutes,
            "feedback_rounds": args.feedback_rounds,
            "practical_state": args.practical_state,
            "formal_state": args.formal_state,
            "fixlist_count": args.fixlist_count,
            "final_accepted": args.final_accepted,
            "defects": [
                ensure_public_text("defect", item) for item in args.defect
            ],
            "notes": [ensure_public_text("note", item) for item in args.note],
        }
    except ValueError as exc:
        parser.error(str(exc))

    args.store.parent.mkdir(parents=True, exist_ok=True)
    with args.store.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"已记录：{args.store.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
