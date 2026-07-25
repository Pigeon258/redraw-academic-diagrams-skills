# SVG and Asset Rules

## Representation boundary

Use SVG for an atomic semantic or decorative icon whose internal structure a later editor will not change.

Keep text, containers, relationships, data charts, draggable bars/nodes, repeated editable structures, and changing geometry as native PowerPoint objects.

Once a page uses SVG icons, use SVG for every semantic icon. Do not mix formal SVG with temporary hand-drawn gauges, clocks, cameras, GPUs, routers, targets, or similar symbols.

## Family compatibility

Evaluate:

- line, fill, or mixed style;
- line weight and corner radius;
- visual weight and complexity;
- perspective;
- fill rules;
- internal and external whitespace.

Matching color alone does not make icons compatible.

## Search order

1. reuse a validated same-family asset;
2. find a complete icon in the chosen family;
3. combine same-family SVG components;
4. normalize or create a simple SVG under one visual specification;
5. use a confirmed near-meaning substitute.

Stop when the concept is correct, family is compatible, PowerPoint display is stable, provenance is acceptable, and further search adds little value.

Search one page-level family rather than allowing each module to choose independently. Start a separate search only for a genuinely difficult concept.

## Technical admission

Reject SVG that:

- embeds raster image data;
- depends on external images, fonts, styles, scripts, or network resources;
- contains a watermark;
- relies on unstable filters or animation;
- clips unexpectedly or has excessive blank canvas;
- renders, recolors, or scales unreliably in PowerPoint;
- costs more to repair than to replace.

Validate insertion, scaling, recoloring, save, close, and reopen in Microsoft PowerPoint for high-risk assets.

## Composite icons

Prefer a complete same-family SVG, then same-family composition, then normalized custom SVG, then confirmed near-meaning substitute.

Group semantic components into one icon unit. A native base plate or fully opaque mask may support the icon, but do not hand-draw a missing semantic component.

When an overlay such as a clock, check mark, status badge, or target covers a base icon, give the overlay an opaque plate that matches the local card background. At enlarged view, no database line, bar, checklist stroke, or other base detail may show through the overlay. Recheck the mask after recoloring and after PowerPoint save/reopen.

## Color

Map SVG colors to page-level semantic color roles. Preserve multiple colors only when each color carries meaning. Recheck holes, masks, transparency, and fills after recoloring.

## Provenance

For every external asset record:

- search or asset name;
- source site and exact page;
- author, project, or collection when available;
- license or acceptable-use basis;
- acquisition date;
- final local filename;
- file hash;
- PowerPoint validation state.

Mark user-provided assets as user-provided and still run technical checks. Record both original and modified versions when normalizing an external SVG. Mark fully self-created assets honestly.

License uncertainty requiring a user decision is a `BLOCKER`. A clearly unusable asset with an available replacement is a `MAJOR`.

Do not bundle temporary, private, or non-redistributable assets into the Skill.
