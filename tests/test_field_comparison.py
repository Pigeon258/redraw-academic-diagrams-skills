#!/usr/bin/env python3
"""对正式使用记录工具执行无第三方依赖的烟雾测试。"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evaluation" / "record_field_run.py"
SUMMARY = ROOT / "evaluation" / "summarize_field_runs.py"


def run(command: list[str]) -> None:
    """运行命令并在失败时保留完整输出。"""
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise AssertionError(
            f"命令失败：{command}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


def main() -> int:
    """记录两个合成条目并验证汇总结构。"""
    with tempfile.TemporaryDirectory(prefix="diagram-skill-public-test-") as temp:
        root = Path(temp)
        store = root / "runs.jsonl"
        output = root / "summary.json"
        common = [
            "--store",
            str(store),
            "--diagram-class",
            "synthetic-architecture",
            "--builder",
            "artifact-tool+powerpoint",
            "--feedback-rounds",
            "1",
            "--final-accepted",
        ]
        run(
            [
                sys.executable,
                str(RECORD),
                *common,
                "--task-id",
                "synthetic-quality",
                "--skill",
                "redraw-academic-diagrams",
                "--version",
                "1.0.0",
                "--first-minutes",
                "30",
                "--total-minutes",
                "35",
                "--practical-state",
                "FAST PASS",
                "--formal-state",
                "PASS",
            ]
        )
        run(
            [
                sys.executable,
                str(RECORD),
                *common,
                "--task-id",
                "synthetic-fast",
                "--skill",
                "redraw-academic-diagrams-fast",
                "--version",
                "0.1.0",
                "--first-minutes",
                "18",
                "--total-minutes",
                "24",
                "--user-edit-minutes",
                "2",
                "--fixlist-count",
                "1",
                "--practical-state",
                "FAST PASS WITH FIXLIST",
                "--formal-state",
                "NEEDS REVISION",
            ]
        )
        run(
            [
                sys.executable,
                str(SUMMARY),
                "--store",
                str(store),
                "--output",
                str(output),
            ]
        )
        report = json.loads(output.read_text(encoding="utf-8"))
        assert report["record_count"] == 2
        assert set(report["groups"]) == {
            "redraw-academic-diagrams",
            "redraw-academic-diagrams-fast",
        }
    print("正式使用记录工具烟雾测试通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
