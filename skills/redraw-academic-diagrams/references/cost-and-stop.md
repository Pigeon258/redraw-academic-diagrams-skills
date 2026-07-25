# Cost and Stop Rules

## Time

- `T_elapsed`: user-perceived elapsed delivery time; optimize first.
- `T_active`: active analysis, asset, construction, integration, QA, and repair time.
- `T_wait`: user, network, service, or external-file waiting time.

Track only coarse stage time and meaningful delays.

## Delivery modes

- Fast: produce a worthwhile editable version quickly; prefer formal `PASS`, but allow `FAST PASS WITH FIXLIST` when only qualifying `USER-FIXABLE` issues remain.
- Standard: default; reach stable `PASS`, fix cheap/high-visibility minors, allow one normal feedback round.
- Polished: pursue `PASS—POLISHED` only when requested or clearly valuable.

Use `WORKING DRAFT` for an editable agreed subset. Use `UNVERIFIED DRAFT` when required checks remain.

## Priority

- P0: remove blockers.
- P1: target semantics, editability, connectors, technical integrity, applicable asset gates, readability, and minimum evidence.
- P2: high-frequency edits, high-visibility issues, systemic fixes, and cheap high-impact improvements.
- P3: ordinary local consistency and low-impact minors.
- P4: theoretical best assets, extra variants, pixel matching, and repeated polishing.

Never silently delete P1. Reduce scope or delivery state instead.

## Budget control

After decomposition, state the mode, estimate, hard cap, P1 scope, and cancellable P3/P4 work. Reserve about 20% for integration, minimum QA, and repairs.

At about 50%, verify the core structure and method can finish within budget. At about 80%, stop new alternatives, P3/P4, and open-ended asset search; finish P1 and high-value P2.

If overrun is forecast:

1. change method;
2. reuse modules or assets;
3. stop P4;
4. stop low-value P3;
5. reduce variants and exports;
6. narrow scope;
7. deliver a working draft;
8. ask for more time.

Do not silently exceed the approved cap.

## Failure attempts

After one failure, diagnose and correct. After a second similar failure, change method. After a third failure or no alternative, report the blocker instead of retrying blindly.

## Stop

Stop formal work at `PASS` unless polished delivery was requested. Do not extend work only for minor or polish findings.

In fast mode, stop at `FAST PASS WITH FIXLIST` when there is no blocker or unresolved high-impact semantic issue, PowerPoint and core edits pass, every remaining issue qualifies as `USER-FIXABLE`, the fixlist is explicit, and waiting for AI repair costs more than user editing or the next feedback round. Continue to formal `PASS` when the user requests strict reproduction or does not want to make the edits.

Stop asset search when concept, family, PowerPoint stability, license, and edit cost are acceptable. Then prefer same-family composition, normalized/simple custom SVG, confirmed near-meaning substitute, or user decision.

Stop module polishing when semantics, editability, grouping, icons, relationships, page readability, and repeated style are adequate. Complete the whole page before another uniform adjustment pass.

Perform one integrated review and targeted rechecks. Run the full suite again only after global layout, style, SVG-family, hierarchy, or regeneration changes.

End a feedback round when agreed changes are complete, the user accepts the version, `PASS` is reached, only polish remains, the time cap is reached, or a new decision is required.

Record a post-task lesson only for a reusable defect, rule, asset, method, or invalidated cost assumption.
