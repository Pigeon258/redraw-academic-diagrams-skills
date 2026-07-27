# Workflow

## Preset and artifact lifecycle

Use exactly one workflow preset:

- honor an explicit user selection of `DEFAULT` or `FAST`;
- without an explicit selection, use `FAST` when the approved hard time budget is 30 minutes or less;
- otherwise use `DEFAULT`, including when no time budget is given.

Keep every prototype, partial build, integrated review copy, and pre-freeze candidate as `WORKING DRAFT`. W5 may calculate provisional QA findings, but only W6 can freeze and label a final adoptable candidate. Any post-freeze edit returns the new version to `WORKING DRAFT` until affected checks pass and W6 freezes it again.

## Stages and gates

### W0 — Intake

Record source files, target diagram, requested changes, Microsoft PowerPoint target, selected preset, selection reason, estimate, hard time cap, P1 scope, and cancellable P3/P4 work. Apply the preset rule before planning.

G0 passes when the source is readable, the intended diagram is identifiable, the output form is clear enough to analyze, and the preset and `WORKING DRAFT` state are recorded.

### W1 — Semantic decomposition

Split the page into regions, semantic modules, internal elements, text, icons, charts, relationships, and decoration. Mark each item as retain, modify, confirm, or normalize. Choose native shape, SVG, chart, or connector representation.

Create a relationship inventory before construction. For every visible arrow record source, target, direction, region-level or module-level ownership, and straight/elbow/bidirectional form. Do not collapse an explicit region transition into nearby module connectors without user confirmation.

G1 passes for a region when its core semantics, main text, relationships, and object representations are known. Confirm or explicitly record every high-impact ambiguity.

### W2 — High-risk prototype

Prototype only unproven risks such as SVG display, `noGrp`, nested grouping, connector binding, elbow routing, or chart granularity. When converting a loose existing deck, first repair one representative pair of modules and their relationship before applying the method page-wide.

In `FAST`, reuse a verified method whenever possible. For an unfamiliar risk, prototype only the smallest representative slice. After one failure, diagnose and correct; after a second similar failure, change method instead of extending the prototype.

G2 passes when one method works in real PowerPoint, supports the required editing level, and fits the budget. Skip W2 only with reusable historical evidence.

### W3 — Assets and modules

Apply one page-level style contract. Search and normalize SVG assets, record sources, create native chart/data elements, group module internals, and name important objects.

In `FAST`, use this asset order: verified same-family SVG, short license-clear search, simple same-family custom SVG, confirmed near-meaning substitute, then user decision for high-impact ambiguity. Stop when a contract-satisfying option exists.

G3 passes when a module is semantically correct enough to integrate, moves as one unit, permits intended internal edits, has no known lock or placeholder, and uses compliant assets.

### W4 — Page integration

Place modules, create cross-module relationships, decide connector binding, set layers, align spacing, name page-level objects, and check canvas bounds.

Integrate one candidate path. Normalize region boundaries, spacing, typography, color, line weight, and icon scale in one page-level pass. Do not regenerate acceptable regions or create alternatives unless the user requests them or the method fails.

G4 passes when required modules and relationships are complete, semantic modules move correctly, cross-module connectors remain outside module groups, and the page is complete enough for integrated evaluation.

### W5 — QA and targeted repair

Run deterministic checks, representative PowerPoint edit tasks, semantic checks, visual review, asset checks, and one integrated review. Compare the final connector inventory against the confirmed source/target/direction list at both region and module level. Repair by impact and recheck only affected scope.

`DEFAULT` runs every applicable strict check and targets stable formal `PASS`. `FAST` combines the applicable minimum checks into one pass, stops optional polish and repeated full-deck review, and still runs every applicable hard gate, P1 check, representative core edit, PowerPoint open/save/reopen, and candidate-preview identity check.

Formal G5 passes when every applicable hard gate passes, Q1–Q6 are at least 2, and no `BLOCKER` or `MAJOR` remains. Draft G5 passes when agreed scope and known risks are explicit.

For `FAST`, G5 may also record `FAST PASS WITH FIXLIST` when formal status is not `PASS` solely because of a small number of qualifying `USER-FIXABLE` issues. Preserve the formal QA status separately. The artifact remains `WORKING DRAFT` until W6.

### W6 — Freeze and deliver

Clean temporary objects, save and reopen in PowerPoint, render the matching preview, identify one candidate, build minimum evidence, and freeze the final adoptable version. Deliver one PPTX and one matching preview by default; add a concise fixlist when applicable.

G6 passes when PPTX, preview, and evidence match one candidate; source and accepted versions are preserved; every required check has an explicit result; and formal and practical delivery states support adoption. Before G6 passes, keep the artifact `WORKING DRAFT`.

## Build toolchain

Use the Presentations skill's `build.mjs` / `@oai/artifact-tool` route as the default primary builder. Use PowerPoint COM for necessary grouping, native connector binding, targeted repair, save/reopen, and edit checks.

Direct PowerPoint COM construction is an allowed fallback when Artifact Tool is unavailable, an existing deck must be edited, or it materially reduces native-connector work. Record the builder, postprocessing, fallback reason, and tool delay. Do not compare elapsed time across different toolchains without identifying that confounder.

### W7 — Feedback

List requested changes, classify local/structural/global impact, re-estimate time, return the new version to `WORKING DRAFT`, preserve unaffected modules, modify only affected scope, recheck, refresh important object names after semantic restructuring, and refreeze through W6.

G7 passes when the agreed feedback round is complete, affected scope is rechecked, version relationships are clear, and remaining work is explicit.

## Return paths

- wrong input or scope → W0
- semantic or relationship change → W1
- method failure → W2
- module rebuild → W3
- page layout or cross-module relationship → W4
- local defect → W5
- any post-freeze edit → at least W5

## Asset search

- W1 defines concept, family, license, and time requirements.
- W2 validates high-risk assets.
- W3 performs main search, filtering, normalization, and source recording.
- W5 only replaces failed assets.
- W7 returns new asset requests to W3.

## Human confirmation

Confirm high-impact semantics, relationship direction, near-meaning icon substitutions, structure-changing layout, license risk, budget overrun, scope reduction, hard-gate skipping, or a change from formal to draft delivery.

Autonomously normalize alignment, spacing, typography, same-family equivalent SVG, line styling, object names, non-semantic connector routing, justified unbound connectors, and obvious technical defects.

Batch questions. Continue independent regions while waiting.

## Parallel boundaries

One owner controls semantics, style, the formal PPTX, integration, and final judgment. Parallelize only disjoint modules, shared asset search, independent prototypes, and read-only checks.

The main PPTX has one writer. Asset tasks write candidates and manifests. QA tasks are read-only. Stop parallel work when outputs overlap, merge cost grows, or a page-level decision is required.

## Recovery checkpoints

Keep source files, valuable W3 modules, the W4 integrated draft, W5 candidates, and W6 releases. Preserve the latest known-good PowerPoint file. On corruption, stop editing the failed file and recover from a copied checkpoint.
