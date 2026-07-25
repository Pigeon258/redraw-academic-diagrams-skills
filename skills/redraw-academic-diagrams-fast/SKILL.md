---
name: redraw-academic-diagrams-fast
description: Rapidly redraw PNG, JPG, screenshots, or other non-editable academic architecture diagrams, workflow diagrams, and system diagrams into iteration-ready Microsoft PowerPoint files. Use when the user prioritizes first-pass speed, accepts a short explicit fixlist, and wants editable text, semantic groups, native arrows, consistent SVG icons, and fast feedback cycles rather than exhaustive first-pass polish.
---

# Fast Redraw Academic Diagrams

## Mission

Create a useful editable PowerPoint version faster than manual redrawing. Expect iteration: deliver a coherent first pass, let the user make obvious local edits when convenient, and return only affected regions to AI when further work is needed.

Use the installed Presentations skill for PPTX creation, rendering, and delivery. Target Microsoft PowerPoint.

## Start Fast

1. Inspect the source and requested semantic changes.
2. Set a short time cap and reserve the final 15% for integration and minimum QA.
3. Inventory major regions, module boundaries, readable text, and visible relationships.
4. Decide the native-object, SVG, chart, and connector representation once.
5. Batch only high-impact questions; do not pause for low-risk styling choices.
6. Build one version. Do not create alternatives unless the user requests them.

Read [references/fast-workflow.md](references/fast-workflow.md) before building. Read [references/core-contract.md](references/core-contract.md) when choosing object types, grouping, SVGs, or connectors. Read [references/field-comparison.md](references/field-comparison.md) when recording a real-use comparison with the quality-baseline skill.

## Fast Workflow

| Stage | Action |
|---|---|
| F0 | Confirm source, scope, time cap, and high-impact semantics |
| F1 | Create a compact region/module/relationship inventory |
| F2 | Reuse a verified method and one coherent SVG family |
| F3 | Build editable modules and integrate the page |
| F4 | Run one visual pass, deterministic inspection, and minimum PowerPoint smoke test |
| F5 | Deliver PPTX, preview, and a short fixlist |
| F6 | Apply targeted feedback without regenerating unaffected regions |

Skip method prototypes when a verified builder, SVG family, grouping pattern, or connector pattern already exists. Stop open-ended search and polishing early.

## Core Requirements

Fast does not mean flat or fake:

- keep readable text editable;
- keep semantic modules movable as groups;
- keep useful internal elements accessible;
- use SVG for atomic icons whose internals will not be edited;
- once SVG icons are used, keep one compatible SVG family across the page;
- use native PowerPoint connectors or arrow lines for every visible relationship;
- represent one routed relationship with one connector, not several lines plus a triangle;
- keep editable charts and repeated data elements native at the requested granularity;
- preserve every high-impact region and relationship;
- never overwrite source files or accepted versions;
- ensure Microsoft PowerPoint opens, saves, and reopens the candidate.

When connector binding visibly bends a route that should remain straight, keep the single connector unbound and easy to reconnect.

## Time-Saving Defaults

- Prefer `build.mjs` / `@oai/artifact-tool`; use PowerPoint COM only for required grouping, connector binding, repair, and smoke checks.
- Reuse known primitives, verified SVG families, and previous technical patterns.
- Stop external icon search after the task-local cap; use a simple same-family custom SVG instead of continuing to browse.
- Perform one integrated visual review, not repeated full-deck reviews.
- Test one representative text edit, module move, connector edit, and SVG replacement when applicable.
- Do not pursue pixel matching, extra variants, exhaustive naming, repeated exports, or optional polish.
- After a local feedback edit, recheck only the affected area, candidate identity, preview, and PowerPoint reopen.

## Delivery Decision

Use two independent results:

- formal QA state, when evaluated;
- practical delivery state.

Practical states:

- `FAST PASS`: formal requirements are already met;
- `FAST PASS WITH FIXLIST`: only a small number of obvious, local, non-cascading issues remain that a normal editor can fix in about three minutes each;
- `FAST-NOT-ACCEPTABLE`: a blocker, hidden high-impact semantic risk, broken core edit, technical failure, systemic defect, or other non-user-fixable major remains.

For `FAST PASS WITH FIXLIST`, state the object, issue, suggested edit, and estimated user time. Never hide incomplete work or call it formal `PASS`.

## Minimum QA

Before delivery:

1. compare the full-page preview with the source and user changes;
2. confirm major regions, readable text, and relationship directions;
3. run `scripts/inspect_pptx.py`;
4. run `scripts/inspect_svg.py` when SVG assets are present;
5. open, save, and reopen in Microsoft PowerPoint;
6. perform the applicable minimum representative edits;
7. freeze one candidate and its matching preview.

Use `scripts/build_qa_manifest.py` when a machine-readable record is useful. Do not add full evidence packages when the user only needs the PPTX, preview, and fixlist.

## Feedback

Treat feedback as normal:

- obvious local issue → repair only that object or area;
- module issue → rebuild only the module;
- page routing or layout issue → reintegrate affected regions;
- semantic target change → update the inventory before editing;
- repeated general failure → propose a Skill update after the task.

Do not add a new Skill rule for every one-off correction.
