# Changelog

## 2026-07-27

### `redraw-academic-diagrams` 1.0.1

- Records a validated Artifact Tool 2.8.31 re-export regression that flattened semantic groups and introduced `noGrp` locks.
- Requires pre/post group, name, lock, and edit-task comparison for imported or grouped deck re-exports.
- Defines PowerPoint-native candidate and clarifies that removing `noGrp` restores groupability but does not reconstruct lost semantic groups.

## 2026-07-25

### `redraw-academic-diagrams` 1.0.0

- First public quality-baseline release.
- Includes editable-object, grouping, connector, SVG, QA, cost, and feedback guidance.
- Includes deterministic PPTX/SVG inspection and PowerPoint roundtrip helpers.

### `redraw-academic-diagrams-fast` 0.1.0

- First public field-trial release.
- Prioritizes first useful editable PowerPoint delivery.
- Supports `FAST PASS WITH FIXLIST` and targeted feedback iteration.
- Shares the validated deterministic scripts with the quality baseline.
