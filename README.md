# Editable Academic Diagram Redraw Skills

One actively maintained Codex skill for rebuilding non-editable academic architecture diagrams, workflows, and system diagrams as editable Microsoft PowerPoint graphics. The earlier fast field-trial skill is retained only as a frozen archive.

## Included skills

### `redraw-academic-diagrams`

**Actively maintained and recommended.** It supports fast, standard, and polished delivery while prioritizing semantic completeness, practical editability, coherent SVG assets, native connectors, PowerPoint validation, and traceable QA.

Current version: **1.0.2**

### `redraw-academic-diagrams-fast`

**Retired and paused on 2026-07-27.** Version **0.1.0** is the final frozen field-trial release. It receives no feature updates and must not be used for new work. Use the fast delivery mode in `redraw-academic-diagrams` instead.

The archived files remain available only for history and comparison. Maintenance is limited to critical security, privacy, licensing, or archival-integrity corrections.

## Choose a skill

| Need | Skill |
|---|---|
| Strict reproduction or formal-quality candidate | `redraw-academic-diagrams` |
| Fast editable first pass and normal feedback iteration | `redraw-academic-diagrams` in fast delivery mode |
| User does not want to make any edits | `redraw-academic-diagrams` |
| User accepts a short explicit fixlist | `redraw-academic-diagrams` in fast delivery mode |

The maintained skill targets Microsoft PowerPoint and does not claim WPS compatibility by default.

## Installation

Clone with SSH:

```bash
git clone git@github.com:Pigeon258/redraw-academic-diagrams-skills.git
```

Copy the maintained skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\redraw-academic-diagrams "$HOME\.codex\skills\"
```

Do not install `redraw-academic-diagrams-fast` for new work. If it is already installed, stop invoking it and refresh the maintained main skill.

Restart or refresh Codex so the skills are rediscovered.

## Usage

Standard or formal delivery:

```text
Use $redraw-academic-diagrams to redraw this academic system diagram as an editable Microsoft PowerPoint.
```

Fast iteration through the maintained main skill:

```text
Use $redraw-academic-diagrams in fast delivery mode to create the fastest useful editable PowerPoint version and list any simple remaining fixes.
```

## Field comparison

The `evaluation/` folder records anonymized real-use timing, user editing, feedback rounds, fixlists, and final acceptance. It intentionally does not create extra diagrams solely to improve benchmark scores.

Synthetic smoke data must never be presented as performance evidence.

## Privacy and assets

This repository contains:

- no user diagrams, screenshots, chats, PPTX files, or local absolute paths;
- no downloaded third-party icon assets;
- only task-agnostic instructions, deterministic inspection scripts, evaluation utilities, and a synthetic example.

External assets used during a real task remain subject to their own licenses and provenance requirements.

## Validation

```bash
python scripts/validate_public_repo.py
python tests/test_field_comparison.py
```

## 中文说明

本仓库当前只维护一个科研图 PowerPoint 重绘主 Skill，并保留一个冻结归档：

- `redraw-academic-diagrams`：当前主版本，持续迭代；支持快速、标准和精修交付；
- `redraw-academic-diagrams-fast`：已于 2026-07-27 停止功能更新并暂停使用，仅保留 0.1.0 归档。

仓库不包含任何用户图片、聊天截图、私人 PPTX 或未确认许可的素材。

## License

MIT. See [LICENSE](LICENSE).
