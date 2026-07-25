# PowerPoint Structure

## Semantic groups

- A module group should move, copy, and delete as one semantic unit.
- Important internal text, icons, bars, and sub-elements remain accessible.
- Avoid a giant whole-page group and unowned top-level fragments.
- Keep cross-module connectors outside module groups.
- A connector whose two endpoints and meaning are entirely internal may remain inside that module group.
- Test group and ungroup behavior in real Microsoft PowerPoint.
- Keep nesting shallow and intentional; region → module → internal object is the normal maximum useful hierarchy.

An individually selectable object does not prove practical editability.

## Object locks

Inspect DrawingML for `noGrp`, `noUngrp`, `noSelect`, `noMove`, and `noResize`. Remove restrictions from objects the later editor must manipulate unless a specific approved protection purpose exists.

`noGrp` may be embedded in graphic-frame or SVG-related non-visual properties even when the object appears movable. Inspect nested group members as well as top-level objects.

## Connectors

- Use a connector or arrow line for every visible relationship.
- Use one object per continuous relationship.
- Use one elbow connector for folded, feedback, or routed paths.
- Bind endpoints when attachment is stable and visually correct.
- Leave the connector unbound when binding makes an intended horizontal or vertical path slant.
- Keep an unbound relationship as one movable/reconnectable object.
- Do not create an elbow path from one arrow plus ordinary lines.
- Do not create an arrow from a line plus an independent triangle, chevron, or `__head` shape.
- Do not group a cross-module connector into one endpoint module.
- For a bound cross-module relationship, attach to stable boundary shapes within the module groups while keeping the connector at page level; move each representative module in PowerPoint and confirm both the route and attachment.

When building programmatically, place connectors behind nodes. If nodes are created first during exploration, correct the final layer order before delivery.

## Charts and repeated elements

Use a native chart when users edit data, axes, or legends. Use native shapes with semantic grouping when users directly drag individual bars, nodes, time segments, or repeated objects.

Avoid a single SVG or screenshot when the contract requires per-element editing.

## Naming

Use unique stable names for important objects:

- `REG_` region;
- `MOD_` module;
- `ICON_` SVG icon;
- `CONN_` relationship;
- `CHART_` chart;
- `TXT_` important independent text.

Do not spend time naming every tiny decorative object.

After the user reorganizes, merges, or repurposes modules, rename important groups and connectors. Old source prefixes or names from a previous diagram can make a structurally editable file misleading in the Selection Pane.

## Layers and selection

Use a stable order such as background → region plates → connectors → modules → icons → text.

Make intentional masks fully opaque. Do not leave large transparent shapes that intercept clicks. Prefer correct layering over many white patches.

Remove unused hidden objects, off-slide leftovers, duplicated assets, source overlays, debug frames, placeholder text, broken links, and unnecessary embedded files.

## File behavior

The formal PPTX must:

- open, save, and reopen without repair;
- avoid macros, ActiveX, broken external relationships, and special dependencies;
- preserve expected fonts or report substitution;
- keep formal objects within the canvas;
- remain editable in Microsoft PowerPoint.

Do not use WPS behavior as evidence of Microsoft PowerPoint correctness.

## COM safety

- Operate on a copy for destructive or roundtrip tests.
- Do not overwrite the candidate during a test.
- Release COM objects in `finally`.
- Close only the PowerPoint application instance created by the script.
- Never kill all PowerPoint processes.
- Treat automation failure as an inconclusive test, not proof that the candidate passed or failed.
