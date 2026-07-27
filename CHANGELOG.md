# Changelog

## 2026-07-27

### Repository lifecycle

- Retires and pauses `redraw-academic-diagrams-fast` at its final frozen version, 0.1.0.
- Disables implicit invocation of the archived fast skill and redirects new fast-delivery requests to `redraw-academic-diagrams`.
- Makes `redraw-academic-diagrams` the only actively maintained and recommended skill.

### `redraw-academic-diagrams` 1.0.2

- Marks the skill as the actively maintained main version.
- Clarifies that fast delivery remains available as a mode within the main workflow.

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
