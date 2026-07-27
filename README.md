# Editable Academic Diagram Redraw Skills

One actively maintained Codex skill for rebuilding non-editable academic architecture diagrams, workflows, and system diagrams as editable Microsoft PowerPoint graphics. The earlier fast field-trial skill is retained only as a frozen archive.

## Included skills

### `redraw-academic-diagrams`

**Actively maintained and recommended.** It combines strict construction and QA with rapid editable iteration. It provides two presets:

- `DEFAULT`: the complete strict workflow and stable formal-quality target;
- `FAST`: one time-boxed candidate path, compact planning, verified-method reuse, one combined minimum-complete QA pass, and targeted feedback iteration.

An explicit user selection always wins. Without one, a hard time budget of 30 minutes or less selects `FAST`; otherwise the skill selects `DEFAULT`.

Every prototype, partial build, review copy, and pre-freeze candidate remains `WORKING DRAFT`. Only the frozen candidate with matching PPTX, preview, evidence, and applicable checks may be presented as the final adoptable version.

Current version: **1.1.0**

### `redraw-academic-diagrams-fast`

**Retired and paused on 2026-07-27.** Version **0.1.0** is the final frozen field-trial release. It receives no feature updates and must not be used for new work. Use the `FAST` preset in `redraw-academic-diagrams` instead.

The archived files remain available only for history and comparison. Maintenance is limited to critical security, privacy, licensing, or archival-integrity corrections.

## Choose a skill

| Need | Skill |
|---|---|
| Strict reproduction or formal-quality candidate | `redraw-academic-diagrams` with `DEFAULT` |
| Hard time budget of 30 minutes or less | `redraw-academic-diagrams` with automatic `FAST` |
| Fast editable first pass and normal feedback iteration | `redraw-academic-diagrams` with `FAST` |
| No explicit preset or time budget | `redraw-academic-diagrams` with automatic `DEFAULT` |
| User accepts a short explicit fixlist | `redraw-academic-diagrams` with `FAST` |

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

Default strict preset:

```text
Use $redraw-academic-diagrams with the DEFAULT preset to redraw this academic system diagram as an editable Microsoft PowerPoint.
```

Fast iteration:

```text
Use $redraw-academic-diagrams with the FAST preset and a hard 30-minute budget to create one useful editable PowerPoint candidate, matching preview, and concise fixlist.
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

- `redraw-academic-diagrams`：当前主版本，持续迭代；包含严格的 `DEFAULT` 与 30 分钟以内自动采用的 `FAST` 两种预设；
- `redraw-academic-diagrams-fast`：已于 2026-07-27 停止功能更新并暂停使用，仅保留 0.1.0 归档。

用户明确指定的预设优先；未指定时，硬时间预算不超过 30 分钟自动采用 `FAST`，否则采用 `DEFAULT`。最终可采用候选冻结前的所有版本统一标记为 `WORKING DRAFT`。

仓库不包含任何用户图片、聊天截图、私人 PPTX 或未确认许可的素材。

## License

MIT. See [LICENSE](LICENSE).
