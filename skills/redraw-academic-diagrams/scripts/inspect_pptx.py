#!/usr/bin/env python3
"""检查 PPTX ZIP/OOXML 中可确定的结构事实。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}
SLIDE_RE = re.compile(r"ppt/slides/slide(\d+)\.xml$")
LOCK_ATTRIBUTES = {"noGrp", "noUngrp", "noSelect", "noMove", "noResize"}
RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".emf", ".wmf"}
NON_VISUAL_CONTAINERS = {
    "nvSpPr",
    "nvPicPr",
    "nvCxnSpPr",
    "nvGraphicFramePr",
    "nvGrpSpPr",
}


def sha256_file(path: Path) -> str:
    """计算文件 SHA-256。"""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def local_name(tag: str) -> str:
    """移除 XML 命名空间。"""
    return tag.rsplit("}", 1)[-1]


def add_finding(
    findings: list[dict[str, Any]],
    severity: str,
    code: str,
    message: str,
    slide: int | None = None,
    object_name: str | None = None,
) -> None:
    """追加结构化发现。"""
    item: dict[str, Any] = {
        "severity": severity,
        "code": code,
        "message": message,
    }
    if slide is not None:
        item["slide"] = slide
    if object_name:
        item["object_name"] = object_name
    findings.append(item)


def parse_xml(data: bytes, member: str, findings: list[dict[str, Any]]) -> ET.Element | None:
    """解析 ZIP 成员 XML。"""
    try:
        return ET.fromstring(data)
    except ET.ParseError as exc:
        add_finding(findings, "error", "malformed_xml", f"{member} XML 损坏：{exc}")
        return None


def first_descendant(element: ET.Element, local: str) -> ET.Element | None:
    """按本地名称查找首个后代。"""
    for child in element.iter():
        if local_name(child.tag) == local:
            return child
    return None


def non_visual_container(element: ET.Element) -> ET.Element | None:
    """读取当前对象自身的非视觉属性容器，不进入子对象。"""
    return next(
        (
            child
            for child in element
            if local_name(child.tag) in NON_VISUAL_CONTAINERS
        ),
        None,
    )


def shape_name_and_id(element: ET.Element) -> tuple[str | None, str | None]:
    """读取当前对象 cNvPr 名称与 ID。"""
    container = non_visual_container(element)
    c_nv_pr = first_descendant(container, "cNvPr") if container is not None else None
    if c_nv_pr is None:
        return None, None
    return c_nv_pr.attrib.get("name"), c_nv_pr.attrib.get("id")


def shape_bounds(element: ET.Element) -> tuple[int, int, int, int] | None:
    """读取顶层对象的 off/ext；组内坐标不转换。"""
    xfrm = first_descendant(element, "xfrm")
    if xfrm is None:
        return None
    off = next((child for child in xfrm if local_name(child.tag) == "off"), None)
    ext = next((child for child in xfrm if local_name(child.tag) == "ext"), None)
    if off is None or ext is None:
        return None
    try:
        return (
            int(off.attrib.get("x", "0")),
            int(off.attrib.get("y", "0")),
            int(ext.attrib.get("cx", "0")),
            int(ext.attrib.get("cy", "0")),
        )
    except ValueError:
        return None


def lock_attributes(element: ET.Element) -> dict[str, str]:
    """提取当前对象自身的锁定属性。"""
    locks: dict[str, str] = {}
    container = non_visual_container(element)
    if container is None:
        return locks
    for child in container.iter():
        if local_name(child.tag).endswith("Locks"):
            for key, value in child.attrib.items():
                local_key = local_name(key)
                if local_key in LOCK_ATTRIBUTES and value not in {"0", "false", "False"}:
                    locks[local_key] = value
    return locks


def iter_shape_nodes(
    parent: ET.Element,
    depth: int = 0,
    parent_group: str | None = None,
):
    """递归遍历顶层及组内对象，并保留分组上下文。"""
    for element in list(parent):
        object_type = local_name(element.tag)
        if object_type in {"nvGrpSpPr", "grpSpPr"}:
            continue
        object_name, _object_id = shape_name_and_id(element)
        yield element, object_type, depth, parent_group
        if object_type == "grpSp":
            next_parent = object_name or parent_group
            yield from iter_shape_nodes(element, depth + 1, next_parent)


def is_independent_arrowhead_name(object_name: str | None) -> bool:
    """识别生成器常见的独立箭头头部命名。"""
    if not object_name:
        return False
    lowered = object_name.lower()
    return lowered.endswith(".__head") or lowered.endswith("__head")


def connector_info(element: ET.Element) -> dict[str, Any]:
    """读取连接符几何、箭头和端点连接。"""
    info: dict[str, Any] = {
        "geometry": None,
        "head_arrow": None,
        "tail_arrow": None,
        "start_connected": False,
        "end_connected": False,
    }
    for child in element.iter():
        name = local_name(child.tag)
        if name == "prstGeom":
            info["geometry"] = child.attrib.get("prst")
        elif name == "headEnd":
            info["head_arrow"] = child.attrib.get("type")
        elif name == "tailEnd":
            info["tail_arrow"] = child.attrib.get("type")
        elif name == "stCxn":
            info["start_connected"] = True
        elif name == "endCxn":
            info["end_connected"] = True
    return info


def is_line_like(element: ET.Element, object_type: str) -> bool:
    """判断对象是否允许宽度或高度为零。"""
    if object_type == "cxnSp":
        return True
    geometry = first_descendant(element, "prstGeom")
    if geometry is None:
        return False
    preset = geometry.attrib.get("prst", "")
    return preset == "line" or "Connector" in preset


def inspect_pptx(path: Path) -> dict[str, Any]:
    """检查 PPTX 文件。"""
    report: dict[str, Any] = {
        "path": str(path.resolve()),
        "sha256": None,
        "size_bytes": None,
        "slide_count": 0,
        "slide_size_emu": None,
        "slides": [],
        "media": {"svg": 0, "raster": 0, "other": 0, "files": []},
        "external_relationships": [],
        "findings": [],
    }
    findings: list[dict[str, Any]] = report["findings"]

    try:
        report["sha256"] = sha256_file(path)
        report["size_bytes"] = path.stat().st_size
    except OSError as exc:
        add_finding(findings, "error", "read_failed", f"文件读取失败：{exc}")
        return report

    if not zipfile.is_zipfile(path):
        add_finding(findings, "error", "not_zip", "文件不是有效 ZIP/PPTX。")
        return report

    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            for required in {"[Content_Types].xml", "ppt/presentation.xml"}:
                if required not in names:
                    add_finding(
                        findings, "error", "missing_required_part", f"缺少 {required}。"
                    )

            if "ppt/presentation.xml" in names:
                root = parse_xml(
                    archive.read("ppt/presentation.xml"),
                    "ppt/presentation.xml",
                    findings,
                )
                if root is not None:
                    slide_size = root.find(".//p:sldSz", NS)
                    if slide_size is not None:
                        try:
                            report["slide_size_emu"] = {
                                "cx": int(slide_size.attrib["cx"]),
                                "cy": int(slide_size.attrib["cy"]),
                            }
                        except (KeyError, ValueError):
                            add_finding(
                                findings,
                                "risk",
                                "invalid_slide_size",
                                "页面尺寸属性无效。",
                            )

            slide_members = sorted(
                (
                    (int(match.group(1)), member)
                    for member in names
                    if (match := SLIDE_RE.match(member))
                ),
                key=lambda item: item[0],
            )
            report["slide_count"] = len(slide_members)
            slide_size = report["slide_size_emu"]

            for slide_number, member in slide_members:
                slide_result: dict[str, Any] = {
                    "slide": slide_number,
                    "objects": 0,
                    "recursive_objects": 0,
                    "groups": 0,
                    "top_level_groups": 0,
                    "max_group_depth": 0,
                    "group_details": [],
                    "semantic_group_candidates": [],
                    "connectors": [],
                    "line_shapes_with_arrow": [],
                    "independent_arrowhead_candidates": [],
                    "native_icon_candidates": [],
                    "object_types": {},
                    "recursive_object_types": {},
                    "duplicate_names": [],
                }
                root = parse_xml(archive.read(member), member, findings)
                if root is None:
                    report["slides"].append(slide_result)
                    continue

                sp_tree = root.find(".//p:spTree", NS)
                if sp_tree is None:
                    add_finding(
                        findings,
                        "risk",
                        "missing_shape_tree",
                        "缺少 spTree。",
                        slide_number,
                    )
                    report["slides"].append(slide_result)
                    continue

                seen_names: dict[str, int] = {}
                for element, object_type, depth, parent_group in iter_shape_nodes(sp_tree):
                    if depth == 0:
                        slide_result["objects"] += 1
                        slide_result["object_types"][object_type] = (
                            slide_result["object_types"].get(object_type, 0) + 1
                        )
                    slide_result["recursive_objects"] += 1
                    slide_result["recursive_object_types"][object_type] = (
                        slide_result["recursive_object_types"].get(object_type, 0) + 1
                    )
                    slide_result["max_group_depth"] = max(
                        slide_result["max_group_depth"], depth
                    )
                    if object_type == "grpSp":
                        slide_result["groups"] += 1
                        if depth == 0:
                            slide_result["top_level_groups"] += 1

                    object_name, _object_id = shape_name_and_id(element)
                    if object_name:
                        seen_names[object_name] = seen_names.get(object_name, 0) + 1
                    if object_type == "grpSp":
                        direct_children = sum(
                            1
                            for child in element
                            if local_name(child.tag) not in {"nvGrpSpPr", "grpSpPr"}
                        )
                        slide_result["group_details"].append(
                            {
                                "name": object_name,
                                "depth": depth,
                                "parent_group": parent_group,
                                "direct_children": direct_children,
                            }
                        )
                        if object_name and object_name.upper().startswith("MOD_"):
                            slide_result["semantic_group_candidates"].append(object_name)

                    container = non_visual_container(element)
                    hidden = (
                        first_descendant(container, "cNvPr")
                        if container is not None
                        else None
                    )
                    if hidden is not None and hidden.attrib.get("hidden") in {"1", "true"}:
                        add_finding(
                            findings,
                            "warning",
                            "hidden_object",
                            "检测到隐藏对象。",
                            slide_number,
                            object_name,
                        )

                    locks = lock_attributes(element)
                    if locks:
                        add_finding(
                            findings,
                            "risk",
                            "object_lock",
                            f"检测到对象锁：{locks}",
                            slide_number,
                            object_name,
                        )

                    bounds = shape_bounds(element) if depth == 0 else None
                    if bounds:
                        x, y, cx, cy = bounds
                        line_like = is_line_like(element, object_type)
                        if (cx <= 0 and cy <= 0) or (
                            not line_like and (cx <= 0 or cy <= 0)
                        ):
                            add_finding(
                                findings,
                                "warning",
                                "non_positive_size",
                                f"对象尺寸异常：x={x} y={y} cx={cx} cy={cy}",
                                slide_number,
                                object_name,
                            )
                        if slide_size and (
                            x < 0
                            or y < 0
                            or x + cx > slide_size["cx"]
                            or y + cy > slide_size["cy"]
                        ):
                            add_finding(
                                findings,
                                "warning",
                                "off_slide",
                                f"顶层对象越界：x={x} y={y} cx={cx} cy={cy}",
                                slide_number,
                                object_name,
                            )

                    if object_type == "cxnSp":
                        info = connector_info(element)
                        info["name"] = object_name
                        info["depth"] = depth
                        info["parent_group"] = parent_group
                        slide_result["connectors"].append(info)
                    elif object_type == "sp":
                        info = connector_info(element)
                        if info["head_arrow"] or info["tail_arrow"]:
                            info["name"] = object_name
                            info["depth"] = depth
                            info["parent_group"] = parent_group
                            slide_result["line_shapes_with_arrow"].append(info)

                    if is_independent_arrowhead_name(object_name):
                        candidate = {
                            "name": object_name,
                            "type": object_type,
                            "depth": depth,
                            "parent_group": parent_group,
                        }
                        slide_result["independent_arrowhead_candidates"].append(candidate)
                        add_finding(
                            findings,
                            "risk",
                            "independent_arrowhead_candidate",
                            "对象名表明它可能是与线条分离的箭头头部；应确认并改为单一原生箭头或连接符。",
                            slide_number,
                            object_name,
                        )

                    if (
                        object_name
                        and object_name.upper().startswith("ICON_")
                        and object_type in {"sp", "cxnSp", "graphicFrame"}
                    ):
                        slide_result["native_icon_candidates"].append(
                            {
                                "name": object_name,
                                "type": object_type,
                                "depth": depth,
                                "parent_group": parent_group,
                            }
                        )

                if slide_result["native_icon_candidates"]:
                    candidate_names = [
                        item["name"]
                        for item in slide_result["native_icon_candidates"][:8]
                    ]
                    add_finding(
                        findings,
                        "risk",
                        "native_icon_candidates",
                        "检测到以 ICON_ 命名但由原生形状/连接符构成的对象；若它们是无需内部编辑的原子图标，应改为可整体替换的 SVG。"
                        f" 候选：{', '.join(candidate_names)}",
                        slide_number,
                    )

                duplicates = sorted(name for name, count in seen_names.items() if count > 1)
                slide_result["duplicate_names"] = duplicates
                for duplicate in duplicates:
                    add_finding(
                        findings,
                        "warning",
                        "duplicate_object_name",
                        f"对象名称重复：{duplicate}",
                        slide_number,
                        duplicate,
                    )

                report["slides"].append(slide_result)

            for member in sorted(names):
                if member.startswith("ppt/media/") and not member.endswith("/"):
                    suffix = Path(member).suffix.lower()
                    if suffix == ".svg":
                        report["media"]["svg"] += 1
                    elif suffix in RASTER_SUFFIXES:
                        report["media"]["raster"] += 1
                    else:
                        report["media"]["other"] += 1
                    report["media"]["files"].append(member)

                if member.endswith(".rels"):
                    root = parse_xml(archive.read(member), member, findings)
                    if root is not None:
                        for relation in root:
                            if relation.attrib.get("TargetMode") == "External":
                                item = {
                                    "part": member,
                                    "type": relation.attrib.get("Type"),
                                    "target": relation.attrib.get("Target"),
                                }
                                report["external_relationships"].append(item)

            if report["external_relationships"]:
                add_finding(
                    findings,
                    "risk",
                    "external_relationships",
                    f"检测到 {len(report['external_relationships'])} 个外部关系。",
                )

            suspicious_members = [
                member
                for member in names
                if "activex" in member.lower()
                or member.lower().endswith("vbaproject.bin")
                or member.lower().endswith(".bin")
            ]
            if suspicious_members:
                add_finding(
                    findings,
                    "risk",
                    "active_content",
                    f"检测到宏、ActiveX 或二进制内容：{', '.join(sorted(suspicious_members)[:8])}",
                )

    except (OSError, zipfile.BadZipFile) as exc:
        add_finding(findings, "error", "archive_failed", f"读取 PPTX 失败：{exc}")

    return report


def summary_for(report: dict[str, Any]) -> dict[str, int]:
    """汇总发现严重度。"""
    summary = {"error": 0, "risk": 0, "warning": 0}
    for finding in report["findings"]:
        severity = finding["severity"]
        summary[severity] = summary.get(severity, 0) + 1
    return summary


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="检查 PPTX 的确定性结构事实。")
    parser.add_argument("pptx", type=Path, help="PPTX 文件")
    parser.add_argument("--json-out", type=Path, help="写入 JSON 报告")
    parser.add_argument(
        "--max-findings",
        type=int,
        default=50,
        help="控制台最多显示多少条发现；JSON 仍保留全部",
    )
    args = parser.parse_args()

    if not args.pptx.is_file():
        print("脚本错误：PPTX 文件不存在。", file=sys.stderr)
        return 2

    report = inspect_pptx(args.pptx)
    summary = summary_for(report)
    report["summary"] = summary
    print(
        f"PPTX 检查：slides={report['slide_count']} "
        f"error={summary['error']} risk={summary['risk']} warning={summary['warning']}"
    )
    max_findings = max(0, args.max_findings)
    for finding in report["findings"][:max_findings]:
        location = ""
        if "slide" in finding:
            location += f" slide={finding['slide']}"
        if finding.get("object_name"):
            location += f" object={finding['object_name']}"
        print(
            f"[{finding['severity'].upper()}]{location} "
            f"{finding['code']} :: {finding['message']}"
        )
    omitted = len(report["findings"]) - max_findings
    if omitted > 0:
        print(f"... 另有 {omitted} 条发现仅保存在 JSON 报告中。")

    if args.json_out:
        try:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except OSError as exc:
            print(f"脚本错误：无法写入 JSON：{exc}", file=sys.stderr)
            return 2

    if summary["error"] or summary["risk"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
