#!/usr/bin/env python3
"""检查 SVG 的确定性技术风险，不判断语义、风格或许可。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


XLINK = "{http://www.w3.org/1999/xlink}href"
URL_PATTERN = re.compile(r"(?:url\(|@import\s+)[^#)]*(?:https?:|file:|//)", re.I)


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
    findings: list[dict[str, str]], severity: str, code: str, message: str
) -> None:
    """追加结构化发现。"""
    findings.append({"severity": severity, "code": code, "message": message})


def inspect_svg(path: Path) -> dict[str, Any]:
    """检查单个 SVG 文件。"""
    result: dict[str, Any] = {
        "path": str(path.resolve()),
        "sha256": None,
        "size_bytes": None,
        "root": None,
        "viewBox": None,
        "width": None,
        "height": None,
        "element_counts": {},
        "findings": [],
    }
    findings: list[dict[str, str]] = result["findings"]

    try:
        result["sha256"] = sha256_file(path)
        result["size_bytes"] = path.stat().st_size
        raw = path.read_bytes()
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        add_finding(findings, "error", "malformed_xml", f"XML 解析失败：{exc}")
        return result
    except OSError as exc:
        add_finding(findings, "error", "read_failed", f"文件读取失败：{exc}")
        return result

    root_name = local_name(root.tag)
    result["root"] = root_name
    result["viewBox"] = root.attrib.get("viewBox")
    result["width"] = root.attrib.get("width")
    result["height"] = root.attrib.get("height")

    if root_name.lower() != "svg":
        add_finding(findings, "error", "not_svg_root", "根元素不是 svg。")

    if not result["viewBox"]:
        add_finding(findings, "warning", "missing_viewbox", "缺少 viewBox。")
    if not result["width"] and not result["height"] and not result["viewBox"]:
        add_finding(findings, "risk", "missing_dimensions", "缺少尺寸和 viewBox。")

    counts: dict[str, int] = {}
    external_refs: list[str] = []
    embedded_rasters = 0
    risky_style_refs = 0

    for element in root.iter():
        name = local_name(element.tag)
        counts[name] = counts.get(name, 0) + 1

        if name == "script":
            add_finding(findings, "risk", "script_element", "包含 script 元素。")
        elif name == "foreignObject":
            add_finding(
                findings, "risk", "foreign_object", "包含 foreignObject 元素。"
            )
        elif name == "image":
            href = element.attrib.get("href") or element.attrib.get(XLINK) or ""
            if href.startswith("data:image/"):
                embedded_rasters += 1
            elif href:
                external_refs.append(href)
            else:
                add_finding(findings, "risk", "image_without_href", "image 缺少 href。")

        for attr_name, value in element.attrib.items():
            attr_local = local_name(attr_name)
            if attr_local == "href" and name != "image":
                if value and not value.startswith("#") and not value.startswith("data:"):
                    external_refs.append(value)
            if attr_local in {"style", "class"} and URL_PATTERN.search(value or ""):
                risky_style_refs += 1

        text = element.text or ""
        if name == "style" and URL_PATTERN.search(text):
            risky_style_refs += 1
        if name == "style" and "@font-face" in text:
            add_finding(
                findings,
                "risk",
                "font_face",
                "样式中包含 @font-face，可能依赖外部字体。",
            )

    result["element_counts"] = counts

    if embedded_rasters:
        add_finding(
            findings,
            "risk",
            "embedded_raster",
            f"包含 {embedded_rasters} 个嵌入位图 image。",
        )
    if external_refs:
        unique_refs = sorted(set(external_refs))
        add_finding(
            findings,
            "risk",
            "external_reference",
            f"包含外部引用：{', '.join(unique_refs[:5])}",
        )
        result["external_references"] = unique_refs
    if risky_style_refs:
        add_finding(
            findings,
            "risk",
            "external_style_reference",
            f"检测到 {risky_style_refs} 处外部样式引用。",
        )

    filter_count = counts.get("filter", 0)
    if filter_count:
        add_finding(
            findings,
            "warning",
            "svg_filters",
            f"包含 {filter_count} 个 filter，需在 PowerPoint 中实测。",
        )

    return result


def collect_svg_files(inputs: list[Path], recursive: bool) -> list[Path]:
    """展开文件和目录输入。"""
    files: list[Path] = []
    for input_path in inputs:
        if input_path.is_file():
            files.append(input_path)
        elif input_path.is_dir():
            pattern = "**/*.svg" if recursive else "*.svg"
            files.extend(input_path.glob(pattern))
    return sorted({path.resolve() for path in files}, key=lambda item: str(item).lower())


def summarize(results: list[dict[str, Any]]) -> dict[str, int]:
    """汇总严重度数量。"""
    summary = {"files": len(results), "error": 0, "risk": 0, "warning": 0}
    for result in results:
        for finding in result["findings"]:
            severity = finding["severity"]
            summary[severity] = summary.get(severity, 0) + 1
    return summary


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="检查 SVG 的确定性技术风险。")
    parser.add_argument("paths", nargs="+", type=Path, help="SVG 文件或目录")
    parser.add_argument("--recursive", action="store_true", help="递归扫描目录")
    parser.add_argument("--json-out", type=Path, help="写入 JSON 报告")
    args = parser.parse_args()

    files = collect_svg_files(args.paths, args.recursive)
    if not files:
        print("脚本错误：没有找到 SVG 文件。", file=sys.stderr)
        return 2

    results = [inspect_svg(path) for path in files]
    summary = summarize(results)
    report = {"tool": "inspect_svg", "summary": summary, "files": results}

    print(
        f"SVG 检查：{summary['files']} 个文件，"
        f"error={summary['error']} risk={summary['risk']} warning={summary['warning']}"
    )
    for result in results:
        for finding in result["findings"]:
            print(
                f"[{finding['severity'].upper()}] "
                f"{result['path']} :: {finding['code']} :: {finding['message']}"
            )

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
