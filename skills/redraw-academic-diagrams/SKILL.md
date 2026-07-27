---
name: redraw-academic-diagrams
description: "Actively maintained main skill for redrawing PNG, JPG, screenshots, or other non-editable academic architecture diagrams, workflow diagrams, and system diagrams into editable Microsoft PowerPoint files. Use for strict, iteration-ready reconstruction, revision, or evaluation with two presets: user-selected DEFAULT or FAST; when the user does not choose, use FAST for a time budget of 30 minutes or less and DEFAULT otherwise. Keep every pre-final version as WORKING DRAFT."
---

# Redraw Academic Diagrams

## Mission

Convert a non-editable research diagram into a clear Microsoft PowerPoint graphic model that a later editor can revise at semantic-module and element level. Treat the source image as a reference, not an unquestionable semantic truth. Optimize real editing experience within the approved time budget.

This is the actively maintained and recommended skill. Keep a strict construction and QA contract while treating rapid editable iteration as a central operating principle: build one useful candidate early, preserve accepted regions, apply feedback locally, and avoid repeated whole-page work.

Use the installed Presentations skill for PPTX creation, editing, rendering, and artifact delivery. Apply this skill for diagram-specific semantics, object representation, grouping, connectors, SVG assets, quality gates, and iteration.

Target Microsoft PowerPoint. Do not claim WPS compatibility unless the user explicitly expands the scope.

## Start a Task

1. Inspect every source image, PPTX, screenshot, note, and requested modification.
2. Confirm the intended diagram and output scope.
3. Select `DEFAULT` or `FAST`. Honor an explicit user choice first. Without one, select `FAST` when the approved hard time budget is 30 minutes or less; otherwise select `DEFAULT`, including when no budget is given.
4. Record the preset, estimate, hard cap, P1 scope, and cancellable P3/P4 work.
5. Mark every prototype, partial build, review copy, and pre-freeze candidate as `WORKING DRAFT`. Do not use another draft state.
6. Preserve source files and previously accepted versions.
7. Batch high-impact semantic questions; continue independent regions while waiting.
8. Use compact working notes. Inventory every visible semantic relationship by source, target, direction, level, and connector shape, but do not separately inventory decorative micro-elements unless they affect layout.
9. Build one candidate path. Do not create alternatives unless the user requests them or the current method fails.
10. For iterative review or handoff, create or update the recommended element index described in [references/element-index.md](references/element-index.md).

Read [references/workflow.md](references/workflow.md) and [references/product-rules.md](references/product-rules.md) before decomposing a new diagram.

## Presets

`DEFAULT` is the strict default preset. Use the complete applicable construction, semantic, asset, editability, PowerPoint, visual, and evidence gates. Target stable formal `PASS`; treat `PASS—POLISHED` as an optional finish target, not a third preset.

`FAST` is the time-boxed preset. Reuse verified methods and one coherent SVG family, prototype only the smallest unfamiliar high-risk slice, stop open-ended search and optional polish early, integrate once, run one combined minimum-complete QA pass, and return a concise fixlist when appropriate. Keep P0/P1, every applicable hard gate, core edit tests, PowerPoint open/save/reopen, candidate-preview identity, and honest delivery labels.

The explicit user choice always overrides the automatic time-budget rule. A later budget change does not override a previously explicit choice unless the user changes the preset.

## Core Workflow

| Stage | Action |
|---|---|
| W0 | Define source, scope, platform, preset, time cap, and `WORKING DRAFT` state |
| W1 | Decompose regions, modules, elements, semantics, and object representations |
| W2 | Prototype only unproven high-risk SVG, grouping, connector, or chart methods |
| W3 | Search assets and build independently editable semantic modules |
| W4 | Integrate one candidate page, cross-module connectors, layers, spacing, and names |
| W5 | Run deterministic checks, real PowerPoint edit tasks, and one integrated review |
| W6 | Freeze the final adoptable candidate, generate matching preview and evidence, then deliver |
| W7 | Return a changed candidate to `WORKING DRAFT`, repair only affected scope, recheck, and refreeze |

Skip W2 only when the same method has reliable historical evidence. In `FAST`, prototype the smallest representative slice and change method quickly after repeated failure. Treat W7 as a normal iteration loop, not automatic evidence that the first pass failed.

## Non-negotiable Rules

- User-confirmed target semantics override the source image.
- Practical editability is the first quality value.
- Keep text, containers, data structures, relationships, and changeable geometry as native objects.
- Use SVG for atomic icons whose internal structure a later editor will not modify.
- Once a page adopts SVG icons, use SVG for every semantic icon and keep one compatible visual family.
- When selecting an SVG, treat the local asset library and license-clear online sources as one candidate space. A validated exact local match may be used immediately; otherwise perform a bounded online comparison and record the selection or promotion decision.
- `FAST` does not waive the applicable SVG/asset gate. If compliant atomic SVG icons cannot be completed within the cap, keep the result `WORKING DRAFT` instead of silently hand-drawing them or claiming `PASS`.
- Do not replace editable charts or per-bar/per-node structures with screenshots or monolithic SVG.
- Group each semantic module for whole-module movement while preserving useful group-internal editing.
- Keep cross-module connectors outside individual module groups.
- Make every visible arrow a native connector or arrow line.
- Preserve every confirmed region-level and module-level relationship; never remove an explicit arrow merely because another nearby connector looks redundant.
- Do not let text or icons intersect solid borders, dividers, or relationship lines. Repair the collision without changing semantic ownership, adjacency, or handoff meaning; boundaries at every hierarchy level are adjustable layout variables, not fixed conditions.
- Never create a visible arrow from a line plus an independent triangle or `__head` shape.
- Represent one continuous folded, feedback, or routed relationship with one native elbow connector.
- Leave a connector unbound when binding harms the intended straight route, but never simulate one relationship with several lines.
- Never overwrite source files, user-adjusted files, or delivered versions.
- Keep every version `WORKING DRAFT` until W6 freezes a final adoptable candidate whose applicable checks and matching artifacts are complete.
- Return any post-freeze edit to `WORKING DRAFT` until the affected checks pass and the new candidate is frozen.
- Stop when the approved state and quality threshold are met; do not continue low-value polishing.

## Build Toolchain

- Use the installed Presentations skill's `build.mjs` / `@oai/artifact-tool` workflow as the default primary builder.
- Use PowerPoint COM only for necessary grouping, connector binding, targeted repair, save/reopen, and real edit validation.
- Direct PowerPoint COM construction is an allowed fallback when Artifact Tool is unavailable, an existing deck must be edited, or native connector behavior materially lowers time.
- Treat Artifact Tool re-export of an imported or grouped deck as a high-risk transformation. Compare pre/post group counts, names, and lock findings; if re-export flattens semantic groups or adds `noGrp`, keep the pre-export PowerPoint-native candidate or repair and fully revalidate a copy.
- Record the primary builder, PowerPoint postprocessing, fallback reason, and tool delays. Never let a fallback silently waive SVG, grouping, connector, or editability rules.
- Treat timing from different builder toolchains as confounded unless the comparison controls for the toolchain.

## Read References Conditionally

- Read [references/svg-assets.md](references/svg-assets.md) when the diagram contains icons or external assets.
- Read [references/element-index.md](references/element-index.md) when the user needs stable module identifiers, iterative feedback vocabulary, or an editor handoff.
- Read [references/powerpoint-structure.md](references/powerpoint-structure.md) before implementing grouping, connectors, charts, layers, or PowerPoint-specific object behavior.
- Read [references/quality-gates.md](references/quality-gates.md) before W5 and when evaluating an existing redraw.
- Read [references/cost-and-stop.md](references/cost-and-stop.md) when the user emphasizes speed, sets a time cap, or the estimate risks overrun.
- Read [references/case-lessons.md](references/case-lessons.md) when handling `noGrp`, connector binding, elbow routing, mixed icon systems, composite-icon overlap, icon/text line collisions, uncertain icon concepts, or a human-adjusted example.

Do not load every reference unconditionally.

## Use Scripts

Run scripts with the current workspace Python or PowerShell runtime:

- Use `scripts/inspect_svg.py` before or after importing external SVG assets.
- Use `scripts/inspect_pptx.py` on an integrated candidate during W5.
- Use `scripts/build_qa_manifest.py` during W6 to bind the candidate, preview, check summaries, and asset record.
- Use `scripts/test_powerpoint_roundtrip.ps1` only when it exists in the installed version and has been validated in the current Windows/PowerPoint environment.

Scripts verify deterministic facts only. A clean script result does not replace semantic comparison, visual inspection, or real PowerPoint editing.

## Parallel Work

- Keep one owner for target semantics, global style, the formal PPTX, integration, and final judgment.
- Parallelize independent regions, one shared page-level asset search, disjoint high-risk prototypes, and read-only QA.
- Never let multiple workers edit the same PPTX.
- Give every parallel task a fixed input, output, write boundary, style contract, and acceptance condition.
- Return to serial work when coordination or merge cost approaches the expected time saving.

## Quality and Delivery

Before W6, record QA findings provisionally but keep the artifact state `WORKING DRAFT`. Only the frozen W6 output may be presented as a final adoptable candidate.

For a formal `PASS` final candidate:

- all applicable hard gates pass;
- Q1 through Q6 are at least 2;
- no `BLOCKER` or `MAJOR` remains;
- required edit tasks pass in Microsoft PowerPoint;
- the PPTX, preview, and minimum evidence identify the same candidate.
- every applicable asset gate and edit task has an explicit result; never use the caller-asserted manifest state as proof by itself.

Use `CONDITIONAL` only for an explicitly accepted non-hard deviation after every hard gate passes. Keep scope-incomplete, check-incomplete, blocked, or unverified outputs as `WORKING DRAFT` and list the gap. Never label an unverified requirement as passed.

For `FAST`, also report a separate practical result on the frozen final candidate:

- `FAST PASS` when formal `PASS` is already met;
- `FAST PASS WITH FIXLIST` when only a small number of non-systemic, obvious, local issues remain that a normal editor can fix in about three minutes without semantic reinterpretation or cascading rework, while core editability and PowerPoint usability pass;
- `FAST-NOT-ACCEPTABLE` when a blocker, hidden semantic risk, technical failure, systemic defect, or non-user-fixable major remains.

Tag an issue `USER-FIXABLE` only when it is easy to notice, local, quick in PowerPoint, non-cascading, and does not damage the rest of the file. This tag never changes the formal defect severity or retroactively creates formal `PASS`. Always include the object, suggested edit, and estimated user time.

## Feedback and Evolution

Classify feedback:

- semantic target change → W1;
- failed technical method → W2;
- module rebuild → W3;
- page layout or cross-module relationship → W4;
- local defect → W5.

Recheck only the affected scope unless a global change invalidates the complete candidate. Let the user finish simple edits when they prefer. Record a reusable lesson only when it changes a general rule, asset, method, or cost assumption.

## Final Response

Report concisely:

- the absolute output path;
- version and delivery state;
- important editable structures completed;
- necessary verification actually performed;
- unverified items or remaining user decisions.

Do not attach internal working notes, long QA logs, or temporary assets unless requested.
