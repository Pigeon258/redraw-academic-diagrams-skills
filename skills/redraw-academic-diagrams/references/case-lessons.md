# Transferable Case Lessons

## Editable objects are not enough

A deck can contain many selectable native objects and still be difficult to edit. Test semantic module movement, internal edits, copy/delete, and connector behavior rather than counting shapes.

## `noGrp` can invalidate an otherwise good redraw

Some imported or generated graphical objects carry `noGrp` or related DrawingML restrictions. The icon may move normally but prevent a containing semantic module from grouping. Inspect the OOXML and test the actual group operation.

## Artifact Tool re-export can flatten groups and add `noGrp`

In one validated Windows/PowerPoint case with `@oai/artifact-tool` 2.8.31, importing and re-exporting a grouped PPTX flattened six semantic groups into 84 top-level objects and added 137 `noGrp="1"` attributes across 14 XML parts. Deterministic inspection reported 71 lock risks.

Deleting only the unintended `noGrp` attributes from a temporary copy reduced the lock findings to zero and allowed three loose objects to be grouped, moved, saved, and reopened in PowerPoint. It did not reconstruct the six lost semantic group boundaries. Therefore:

- compare group counts, important names, locks, and edit tasks before and after every Artifact Tool re-export of an imported/grouped deck;
- do not select the re-exported file when its semantic grouping regresses;
- prefer the pre-export PowerPoint-native candidate when it retains the verified groups and connectors;
- if stripping `noGrp`, operate on a copy, reconstruct lost groups explicitly, and rerun structural inspection plus real PowerPoint edit tests.

A PowerPoint-native candidate is the PPTX last saved directly by Microsoft PowerPoint or PowerPoint COM after construction and grouping, before another import/export tool rewrites its OOXML. It remains an editable PPTX; “native” identifies the final writer and preserved PowerPoint object model, not a screenshot or a claim that every object was created manually.

## Binding is conditional

Binding is valuable when a relationship should follow a moving module and PowerPoint keeps the intended route. Binding is harmful when two straight parallel arrows become slanted or awkward. In that case, preserve one straight unbound arrow object.

## One relationship means one connector

A feedback route that visually resembles an elbow but is built from an arrow and two ordinary lines is hard to edit and violates the relationship model. Use one native elbow connector.

## A line plus a triangle is not an arrow

Some generators add a separate triangle because the line-end arrow renders inconsistently in another renderer. The slide may look correct but the head does not follow when the line is edited. Use a native arrow line or connector and treat generated `__head` objects as a regression signal.

## Validate one structural slice before page-wide repair

When an existing page contains hundreds of loose objects, first unlock and group two representative adjacent modules, replace their relationship with one connector, and move both groups in PowerPoint. Expand the method only after group-internal editing and connector following work.

## Keep connector ownership semantic

Cross-module connectors stay outside endpoint module groups and may bind to stable boundary shapes inside them. A connector can stay inside a module only when both endpoints and the relationship are internal. Count-based grouping checks cannot replace movement tests.

## Icon consistency is page-level

Mixing polished SVG icons with hand-built semantic clocks, gauges, cameras, or routers makes the diagram visibly inconsistent. Once SVG is adopted, select one compatible family for all semantic icons.

## Similar appearance can carry the wrong concept

An icon may be visually neat but semantically wrong. Examples include a GPU substituted for a camera, a horizontal bar chart substituted for a column chart, or a routing icon missing its central node or directional arrows. Verify the intended concept before judging style.

## Data-like icons need a representation decision

A small bar-chart symbol may be an atomic concept icon and therefore SVG, while a chart whose individual bars will be adjusted must use native editable objects. Decide from expected user edits, not appearance alone.

## Composite SVG overlays need opaque masks

A valid clock or check SVG can still expose base-icon strokes through its circular overlay. Put an opaque plate matching the card background behind the overlay, group the composition, and inspect at enlarged scale after save/reopen.

## Fast delivery cannot silently remove the asset gate

A fast reconstruction can be visually convincing while every atomic icon is rebuilt from many native lines and shapes. This makes icon replacement slow and violates the SVG boundary. When the SVG path or preferred build tool fails, switch methods quickly or label the output `WORKING DRAFT`; do not assert `PASS` from a clean OOXML report alone.

## Nearby module arrows do not replace an explicit region arrow

A source can show several bidirectional module links and also a separate one-way transition between their containing regions. The region arrow may look redundant but still expresses workflow level and direction. Inventory relationships before drawing and compare both region-level and module-level connectors before claiming semantic or connector gates passed.

## Human adjustment is not automatic ground truth

A later editor may correctly simplify, merge, or recombine content from multiple source diagrams while leaving locks, loose objects, stale names, or partial connector conversions. Separate the desired semantic/layout changes from remaining technical defects instead of copying the adjusted file wholesale.

## Names must follow semantic restructuring

When modules from different diagrams are recombined, old prefixes can survive even though the visible content has changed. Rename important groups and connectors after structure changes so the Selection Pane supports the next edit.

## Human corrections are evidence

Treat a user-adjusted PPTX as a high-value regression example. Compare object structure and actual edit behavior, extract a transferable rule, and update the governance baseline before changing the Skill.

## Feedback is normal

Academic diagram reconstruction is unlikely to be perfect in one pass because the source can contain incorrect or outdated logic. Aim for a strong editable candidate, then classify feedback and return only to the affected workflow stage.
