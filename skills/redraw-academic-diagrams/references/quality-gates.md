# Quality Gates

## Artifact lifecycle

- Label every prototype, partial build, review copy, W4 integration, and W5 candidate `WORKING DRAFT`.
- Record incomplete or unrun checks as unverified items under `WORKING DRAFT`; do not use another draft state.
- Treat W5 scores and gate results as provisional while the artifact remains `WORKING DRAFT`.
- Present a version as the final adoptable candidate only after W6 freezes the matching PPTX, preview, and minimum evidence and the applicable formal or practical adoption criteria pass.
- Return every post-freeze edit to `WORKING DRAFT` until the affected checks pass and W6 freezes the new candidate.

## Defect levels

- `BLOCKER`: work cannot continue or be evaluated without user input, an external resource, or a recoverable base file.
- `MAJOR`: repairable but formal delivery is prohibited until fixed.
- `MINOR`: localized deviation that does not harm target semantics, core edits, technical usability, or normal reading.
- `POLISH`: optional improvement, not a contract defect.

Escalate repeated or systemic `MINOR` findings to `MAJOR`.

`USER-FIXABLE` is an additional practical-delivery tag, not a severity. Apply it only when the issue is easy for a normal editor to notice, local, fixable in PowerPoint in about three minutes, requires no high-impact semantic reinterpretation, causes no cascading rework, and leaves core editability and technical usability intact. Never apply it to systemic, hidden, data-truth, module-rebuild, or technically unsafe defects.

## Hard gates

- HG-01: candidate, preview, evidence, and delivery version match.
- HG-02: confirmed target semantics, text, relationships, concepts, and data truth are correct.
- HG-03: required real editing tasks work at the contracted granularity.
- HG-04: every confirmed region-level and module-level relationship is present, and each uses the correct native single connector object, endpoints, level, and direction.
- HG-05: Microsoft PowerPoint opens, saves, reopens, and edits the file without repair.
- HG-06: applicable SVG icons form a compatible, technically stable, traceable asset system.
- HG-07: the diagram is readable at page and detail level without semantic visual ambiguity, including no unintended text/icon intersection with solid borders, dividers, or relationship lines.
- HG-08: the delivery is complete, clean, and free of temporary or mismatched artifacts.

Use “not applicable” only with a concrete reason.

## Quality dimensions

| Dimension | 2 — minimum pass | 3 — good | 4 — extra value |
|---|---|---|---|
| Q1 semantics | confirmed content correct and high-impact ambiguity handled | content consistent and changes fully propagated | organization materially improves understanding without invented meaning |
| Q2 editability | all required edit tasks pass | common edits are efficient and low-friction | structure is highly reusable and extensible |
| Q3 PPT structure | file and objects meet minimum technical rules | names, layers, groups, and repeated styles are stable | structure adds clear maintenance value |
| Q4 SVG/assets | icons and provenance meet minimum rules | family is coherent and technically robust | normalized assets add reuse value |
| Q5 visual | information is understandable and academically suitable | hierarchy, type, color, spacing, and routing are professional | design materially improves comprehension |
| Q6 evidence | candidate, gates, defects, and preview are traceable | evidence is concise and complete | structured evidence reduces future validation cost |

Score 0 when incomplete or unevaluable, and 1 when clearly below contract. Q1 and Q2 cannot be compensated by other dimensions.

## Representative editing tests

- ET-01: edit text without breaking its container or layout.
- ET-02: move a semantic module as one unit.
- ET-03: edit a meaningful internal element without dismantling the page.
- ET-04: replace an atomic SVG icon as one unit.
- ET-05: reroute, reconnect, or reverse a relationship object.
- ET-06: edit a chart or repeated data element at the contracted granularity.
- ET-07: copy, delete, or rearrange a module without dragging unrelated content or leaving fragments.

Select tests by applicable object type. Test at least one representative of each high-risk repeated structure and every user-requested edit.

## Check boundaries

Automate deterministic facts such as archive integrity, slide size, bounds, object types, locks, external relationships, connector properties, SVG raster embedding, and file hashes.

Use real PowerPoint for open/save/reopen, SVG rendering, group operations, connector behavior, font substitution, and edit tasks.

Use human judgment for target semantics, icon meaning, grouping convenience, visual family, page hierarchy, readability, and justified unbound connectors.

Before declaring HG-02 or HG-04 passed, compare a relationship inventory against the reference at two levels: transitions between major regions and connections between modules. A clean OOXML connector report cannot detect a missing source relationship.

At enlarged view, inspect composite SVG icons for transparent overlap leakage. A base line or bar showing through an overlay badge is a visible construction defect even when both source assets are valid SVG.

At 200–300% equivalent zoom, inspect text and icons against solid module borders, region borders, dividers, and connectors. Include the edited scope and adjacent “unchanged” boundary strips. Full-page renders and generic overflow checks can hide one- to three-point intersections.

When a collision exists, first verify semantic ownership and adjacency. Expand or move boundaries at any hierarchy level when useful; do not fix geometry by moving a label or icon into the wrong region or by weakening its relationship to the concept it describes.

## Minimum evidence

Record:

- candidate path, hash, time, slide count, and dimensions;
- HG-01 through HG-08;
- Q1 through Q6 with short reasons;
- selected ET results;
- automated and PowerPoint check summaries;
- matching page preview;
- asset record when external assets are used;
- defects, fixes, and unverified items.

Do not record full video, repetitive screenshots, or complete XML dumps by default.

## Overall state

- any unresolved external dependency or required user decision → `BLOCKED`;
- any failed applicable hard gate or `MAJOR` → `NEEDS REVISION`;
- every hard gate passes but an approved non-hard deviation remains → `CONDITIONAL`;
- every hard gate passes, Q1–Q6 ≥ 2, and no `BLOCKER`/`MAJOR` remains → `PASS`;
- every hard gate passes, all applicable Q ≥ 3, at least one Q = 4, and no unresolved defect or exception remains → `PASS—POLISHED`.

Skipping a required check never becomes “passed.” A user may end work while accepting unverified risk, but the result remains a draft or non-pass state.

These QA results do not override artifact lifecycle: before W6, the version is still `WORKING DRAFT` even if provisional checks indicate `PASS`.

For `FAST`, record a separate practical-delivery result:

- formal `PASS` → `FAST PASS`;
- formal non-pass caused only by a small number of non-systemic `USER-FIXABLE` known issues, with core edits and PowerPoint usability passing → `FAST PASS WITH FIXLIST`;
- blocker, unresolved high-impact semantics, core edit failure, technical failure, systemic defect, or other major → `FAST-NOT-ACCEPTABLE`.

For `FAST PASS WITH FIXLIST`, record the object, issue, suggested edit, and estimated user repair time. Do not present it as formal `PASS`.

A frozen `FAST PASS WITH FIXLIST` candidate may be presented as practically adoptable only when every applicable hard gate, core edit, PowerPoint usability check, candidate-preview identity check, and non-user-fixable requirement passes. Otherwise keep it `WORKING DRAFT`.

## Recheck scope

- local edit: recheck the affected item, direct neighbors, preview, and candidate identity;
- structural edit: recheck related ET, gates, visual area, and PowerPoint reopen;
- global edit or regenerated deck: rerun every applicable hard gate and related checks.
