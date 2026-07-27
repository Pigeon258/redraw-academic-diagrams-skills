# Product Rules

## Semantic target

Resolve content in this order:

1. user-confirmed changes;
2. user-supplied text, data, annotations, or sketches;
3. clearly readable source content;
4. supported inference.

Do not silently place important inference, guessed text, or OCR output into a formal candidate. Preserve terminology, case, abbreviations, numbers, units, symbols, formulas, and meaningful color semantics.

## Editable object model

Use native PowerPoint objects for:

- text;
- containers and layout boundaries;
- arrows and relationships;
- data-bearing charts;
- bars, timeline nodes, and repeated elements that the user wants to adjust;
- geometry whose internal relationship will change.

Use SVG for an atomic visual icon that a later editor will move, scale, copy, or replace as a whole without editing its internal structure.

Never flatten intended editable text, relationships, data, or structures into a screenshot.

## Semantic grouping

- Group each semantic module so it moves as one unit.
- Preserve useful access to group-internal elements.
- Avoid one giant page group and top-level fragments with no semantic ownership.
- Keep cross-module connectors outside individual module groups.
- Group a composite icon into one semantic icon unit.
- Keep a relationship fully inside a module group only when both endpoints and the relationship are internal to that module.

## Relationships

- Every visible arrow is a native connector or arrow line.
- Direction, endpoints, branches, merges, feedback, and cross-region links follow the confirmed semantic target.
- Use one elbow connector for one folded or feedback relationship.
- Bind endpoints when PowerPoint behavior remains stable.
- Leave a connector unbound when binding damages the intended straight route; keep it a single object.
- Do not confuse decorative lines with semantic relationships.
- Do not leave a separate triangle, chevron, or generated `__head` shape as the visible head of an arrow.
- Preserve explicit region-to-region relationships separately from module-to-module relationships, even when they look redundant. Remove or merge one only after semantic confirmation.

## Charts and data

- Use original data when available.
- Prefer a native chart when users need to edit its data table, axes, or legend.
- Use grouped native shapes when users need to drag individual bars, nodes, or periods directly.
- Do not invent unrecoverable exact values from a raster reference.
- Mark a visual-trend reconstruction as schematic when exact data is unavailable.

## Visual expression

- Use restrained academic styling and clear hierarchy.
- Keep one primary font family and stable title/body roles.
- Use limited, explainable colors and sufficient contrast.
- Standardize repeated borders, radii, padding, line styles, and spacing.
- Keep primary reading direction obvious and connector paths distinguishable.
- Preserve macro regions, relative module relationships, confirmed semantic colors, and the source's core visual language.
- Improve non-semantic typography, spacing, icon consistency, line widths, and routing when useful.

## Technical structure

- The PPTX opens, saves, and edits in Microsoft PowerPoint without repair.
- Do not depend on macros, ActiveX, broken external links, or unusual software.
- Remove unintended `noGrp`, `noUngrp`, `noSelect`, `noMove`, and `noResize`.
- Use stable object names for important regions, modules, icons, connectors, charts, and text.
- Refresh important names after user-driven rearrangement or cross-diagram recomposition; a syntactically valid stale name is still misleading.
- Keep background, connectors, modules, icons, and text in a stable layer order.
- Do not leave large transparent selection blockers, temporary white patches, hidden duplicates, off-slide leftovers, debug shapes, source overlays, or placeholder text.

## Delivery

Do not overwrite sources or accepted versions. Keep every prototype, partial build, review copy, and pre-freeze candidate as `WORKING DRAFT`; list any unverified item under that state. Only W6 may freeze a final adoptable candidate after applicable checks and candidate-preview identity are complete.

Deliver one PPTX and one matching full-page preview by default. For `FAST`, add a concise fixlist only when every item qualifies as `USER-FIXABLE`. Add a short note only for approved exceptions, unresolved semantics, asset restrictions, or unverified work.

Any post-freeze edit creates a new `WORKING DRAFT` until affected checks pass and the candidate is frozen again.
