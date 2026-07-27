# Editable Academic Diagram Redraw Skills

Two Codex skills for rebuilding non-editable academic architecture diagrams, workflows, and system diagrams as editable Microsoft PowerPoint graphics.

## Included skills

### `redraw-academic-diagrams`

Quality-baseline workflow for formal candidates. It prioritizes semantic completeness, practical editability, coherent SVG assets, native connectors, PowerPoint validation, and traceable QA.

Current version: **1.0.1**

### `redraw-academic-diagrams-fast`

Iteration-first workflow for short first-delivery time. It preserves the core editability and technical contract but stops low-value search, repeated checks, alternative versions, and optional polish. It may deliver `FAST PASS WITH FIXLIST` for obvious local edits.

Current version: **0.1.0**

## Choose a skill

| Need | Skill |
|---|---|
| Strict reproduction or formal-quality candidate | `redraw-academic-diagrams` |
| Fast editable first pass and normal feedback iteration | `redraw-academic-diagrams-fast` |
| User does not want to make any edits | `redraw-academic-diagrams` |
| User accepts a short explicit fixlist | `redraw-academic-diagrams-fast` |

Both target Microsoft PowerPoint. Neither claims WPS compatibility by default.

## Installation

Clone with SSH:

```bash
git clone git@github.com:Pigeon258/redraw-academic-diagrams-skills.git
```

Copy one or both skill folders into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\redraw-academic-diagrams "$HOME\.codex\skills\"
Copy-Item -Recurse .\skills\redraw-academic-diagrams-fast "$HOME\.codex\skills\"
```

Restart or refresh Codex so the skills are rediscovered.

## Usage

Quality baseline:

```text
Use $redraw-academic-diagrams to redraw this academic system diagram as an editable Microsoft PowerPoint.
```

Fast iteration:

```text
Use $redraw-academic-diagrams-fast to create the fastest useful editable PowerPoint version and list any simple remaining fixes.
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

本仓库包含两个科研图 PowerPoint 重绘 Skill：

- `redraw-academic-diagrams`：质量基线，适合严格复刻和正式候选；
- `redraw-academic-diagrams-fast`：效率优先，适合尽快交付可编辑版本，并通过简短 fixlist 和后续反馈迭代。

仓库不包含任何用户图片、聊天截图、私人 PPTX 或未确认许可的素材。

## License

MIT. See [LICENSE](LICENSE).
