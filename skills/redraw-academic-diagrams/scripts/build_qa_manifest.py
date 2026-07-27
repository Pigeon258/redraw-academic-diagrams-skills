#!/usr/bin/env python3
"""生成候选 PPTX 的最低 QA 事实清单，不自行判断是否通过。"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
ALLOWED_STATES = {
    "BLOCKED",
    "NEEDS REVISION",
    "CONDITIONAL",
    "PASS",
    "PASS—POLISHED",
    "WORKING DRAFT",
}
ALLOWED_PRACTICAL_STATES = {
    "FAST PASS",
    "FAST PASS WITH FIXLIST",
    "FAST-NOT-ACCEPTABLE",
}


def sha256_file(path: Path) -> str:
    """计算文件 SHA-256。"""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_identity(path: Path) -> dict[str, Any]:
    """生成文件身份信息。"""
    stat = path.stat()
    return {
        "path": str(path.resolve()),
        "size_bytes": stat.st_size,
        "modified_utc": datetime.fromtimestamp(
            stat.st_mtime, tz=timezone.utc
        ).isoformat(),
        "sha256": sha256_file(path),
    }


def pptx_metadata(path: Path) -> dict[str, Any]:
    """读取 PPTX 页数和尺寸。"""
    metadata: dict[str, Any] = {"slide_count": None, "slide_size_emu": None}
    with zipfile.ZipFile(path) as archive:
        slide_names = [
            name
            for name in archive.namelist()
            if name.startswith("ppt/slides/slide")
            and name.endswith(".xml")
            and "/_rels/" not in name
        ]
        metadata["slide_count"] = len(slide_names)
        root = ET.fromstring(archive.read("ppt/presentation.xml"))
        size = root.find(".//p:sldSz", NS)
        if size is not None:
            metadata["slide_size_emu"] = {
                "cx": int(size.attrib["cx"]),
                "cy": int(size.attrib["cy"]),
            }
    return metadata


def parse_named_path(value: str) -> tuple[str, Path]:
    """解析 name=path 参数。"""
    if "=" not in value:
        raise ValueError(f"参数必须是 name=path：{value}")
    name, raw_path = value.split("=", 1)
    if not name.strip() or not raw_path.strip():
        raise ValueError(f"参数必须是 name=path：{value}")
    return name.strip(), Path(raw_path.strip())


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="生成候选 PPTX 的最低 QA 清单。")
    parser.add_argument("--pptx", type=Path, required=True, help="候选 PPTX")
    parser.add_argument("--preview", type=Path, help="对应整页预览")
    parser.add_argument(
        "--check", action="append", default=[], help="检查报告，格式 name=path"
    )
    parser.add_argument("--asset-manifest", type=Path, help="资产清单")
    parser.add_argument(
        "--state", required=True, choices=sorted(ALLOWED_STATES), help="调用者判定状态"
    )
    parser.add_argument(
        "--practical-state",
        choices=sorted(ALLOWED_PRACTICAL_STATES),
        help="可选的快速实际交付结论",
    )
    parser.add_argument(
        "--fix-item",
        action="append",
        default=[],
        help="用户可快速修复事项，可重复",
    )
    parser.add_argument(
        "--unverified", action="append", default=[], help="未验证事项，可重复"
    )
    parser.add_argument("--note", action="append", default=[], help="简短说明，可重复")
    parser.add_argument("--output", type=Path, required=True, help="输出 JSON")
    args = parser.parse_args()

    if args.practical_state == "FAST PASS WITH FIXLIST" and not args.fix_item:
        parser.error("FAST PASS WITH FIXLIST 至少需要一个 --fix-item。")

    adoptable_claim = args.state in {"CONDITIONAL", "PASS", "PASS—POLISHED"} or (
        args.practical_state in {"FAST PASS", "FAST PASS WITH FIXLIST"}
    )
    artifact_lifecycle = (
        "FINAL ADOPTABLE CANDIDATE" if adoptable_claim else "WORKING DRAFT"
    )
    if args.state == "WORKING DRAFT" and args.practical_state in {
        "FAST PASS",
        "FAST PASS WITH FIXLIST",
    }:
        parser.error("WORKING DRAFT 不能声明为可采用的快速交付结论。")
    if adoptable_claim and not args.preview:
        parser.error("最终可采用候选必须提供匹配预览。")
    if adoptable_claim and args.unverified:
        parser.error("最终可采用候选不能包含未验证事项；请改为 WORKING DRAFT。")

    if not args.pptx.is_file():
        print("脚本错误：候选 PPTX 不存在。", file=sys.stderr)
        return 2
    if not zipfile.is_zipfile(args.pptx):
        print("脚本错误：候选文件不是有效 PPTX/ZIP。", file=sys.stderr)
        return 2

    try:
        checks: dict[str, Any] = {}
        for raw_check in args.check:
            name, check_path = parse_named_path(raw_check)
            if not check_path.is_file():
                raise FileNotFoundError(f"检查报告不存在：{check_path}")
            checks[name] = file_identity(check_path)

        report: dict[str, Any] = {
            "tool": "build_qa_manifest",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "artifact_lifecycle": artifact_lifecycle,
            "state_asserted_by_caller": args.state,
            "practical_state_asserted_by_caller": args.practical_state,
            "user_fixable_items": args.fix_item,
            "candidate": file_identity(args.pptx),
            "presentation": pptx_metadata(args.pptx),
            "preview": file_identity(args.preview) if args.preview else None,
            "checks": checks,
            "asset_manifest": (
                file_identity(args.asset_manifest) if args.asset_manifest else None
            ),
            "unverified": args.unverified,
            "notes": args.note,
        }

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"脚本错误：{exc}", file=sys.stderr)
        return 2

    print(f"QA 清单已生成：{args.output.resolve()}")
    print(f"产物生命周期：{artifact_lifecycle}")
    print(f"候选状态由调用者声明：{args.state}")
    if args.practical_state:
        print(f"快速实际交付结论由调用者声明：{args.practical_state}")
    if not args.preview:
        print("[WARNING] 未提供预览。")
    if args.state == "WORKING DRAFT" and not args.unverified:
        print("[WARNING] WORKING DRAFT 未记录未验证事项或剩余工作。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
