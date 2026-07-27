# Cost and Stop Rules

## Time

- `T_elapsed`: user-perceived elapsed delivery time; optimize first.
- `T_active`: active analysis, asset, construction, integration, QA, and repair time.
- `T_wait`: user, network, service, or external-file waiting time.

Track only coarse stage time and meaningful delays.

## Preset selection

Use two presets:

- `DEFAULT`: run the complete applicable strict workflow and QA, target stable formal `PASS`, fix cheap high-visibility minors, and allow one normal feedback round.
- `FAST`: produce one worthwhile editable candidate quickly, stop optional work early, and allow `FAST PASS WITH FIXLIST` only when every remaining issue qualifies as `USER-FIXABLE`.

Apply them in this order:

1. Honor an explicit user selection of `DEFAULT` or `FAST`.
2. Without an explicit selection, use `FAST` when the approved hard time budget is 30 minutes or less.
3. Otherwise use `DEFAULT`, including when no budget is given.

Treat `PASS—POLISHED` as an optional finish target under `DEFAULT`, not a third preset.

Keep every version `WORKING DRAFT` until W6 freezes the final adoptable candidate. Record missing checks as unverified items under `WORKING DRAFT`; do not create a separate draft state.

## Fast iteration defaults

- Build one candidate path and do not create alternatives unless requested or the method fails.
- Use compact notes while preserving a complete semantic-relationship inventory.
- Reuse verified primitives, grouping patterns, connectors, and one SVG family.
- Prototype only the smallest unfamiliar high-risk slice and switch methods quickly after repeated failure.
- Stop asset search when a conceptually correct, family-compatible, PowerPoint-stable, license-clear option exists.
- Integrate once, run one combined minimum-complete QA pass, and recheck only affected scope after feedback.
- Deliver one PPTX, one matching preview, and a concise fixlist when applicable.
- Never defer P0/P1, applicable hard gates, core edit tests, or honest state labeling.

## Priority

- P0: remove blockers.
- P1: target semantics, editability, connectors, technical integrity, applicable asset gates, readability, and minimum evidence.
- P2: high-frequency edits, high-visibility issues, systemic fixes, and cheap high-impact improvements.
- P3: ordinary local consistency and low-impact minors.
- P4: theoretical best assets, extra variants, pixel matching, and repeated polishing.

Never silently delete P1. Reduce scope or delivery state instead.

## Budget control

After decomposition, state the preset, selection reason, estimate, hard cap, P1 scope, and cancellable P3/P4 work. Reserve about 20% in `DEFAULT` and at least 15% in `FAST` for integration, minimum QA, and repairs.

At about 50%, verify the core structure and method can finish within budget. At about 80%, stop new alternatives, P3/P4, and open-ended asset search; finish P1 and high-value P2.

If overrun is forecast:

1. change method;
2. reuse modules or assets;
3. stop P4;
4. stop low-value P3;
5. reduce variants and exports;
6. narrow scope;
7. deliver a `WORKING DRAFT`;
8. ask for more time.

Do not silently exceed the approved cap.

## Failure attempts

After one failure, diagnose and correct. After a second similar failure, change method. After a third failure or no alternative, report the blocker instead of retrying blindly.

## Stop

Stop formal work at `PASS` unless polished finishing was requested. Do not extend work only for minor or polish findings.

In `FAST`, stop at `FAST PASS WITH FIXLIST` when there is no blocker or unresolved high-impact semantic issue, PowerPoint and core edits pass, every remaining issue qualifies as `USER-FIXABLE`, the fixlist is explicit, and waiting for AI repair costs more than user editing or the next feedback round. Continue to formal `PASS` when the user requests strict reproduction or does not want to make the edits.

Stop asset search when concept, family, PowerPoint stability, license, and edit cost are acceptable. Then prefer same-family composition, normalized/simple custom SVG, confirmed near-meaning substitute, or user decision.

Stop module polishing when semantics, editability, grouping, icons, relationships, page readability, and repeated style are adequate. Complete the whole page before another uniform adjustment pass.

Perform one integrated review and targeted rechecks. Run the full suite again only after global layout, style, SVG-family, hierarchy, or regeneration changes.

After any feedback edit, return the new version to `WORKING DRAFT`. End the round only after affected checks pass and W6 refreezes the final adoptable candidate, or when the time cap requires an explicitly labeled draft handoff.

Record a post-task lesson only for a reusable defect, rule, asset, method, or invalidated cost assumption.
