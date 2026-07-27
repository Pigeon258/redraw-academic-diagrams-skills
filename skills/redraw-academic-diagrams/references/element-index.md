# Element Index and Change Map

Use an element index as the recommended modification vocabulary for diagrams that will receive iterative feedback, contain several hierarchy levels, or need handoff to another editor. Skip it for a trivial one-off edit unless the user requests one.

## Required structure

### Candidate identity

Record:

- current candidate filename;
- matching preview filename;
- compatible earlier versions when useful;
- candidate date and SHA-256.

Update these fields whenever the indexed candidate changes.

### Stable prefixes

Assign short human-facing IDs by semantic ownership:

| Prefix | Meaning | Example |
|---|---|---|
| `G` | page-global object | `G1` page title |
| `A`, `B`, ... | major region and its descendants | `A4.3` gate inside module A4 |
| `X` | cross-region boundary or handoff object | `X2` frozen handoff |
| `R` | semantic relationship or connector | `R9` evaluator feedback |

Use `0` for a region root, integer IDs for first-level modules, and dot notation for descendants:

```text
A0       Offline region
A4       Evaluator
A4.3     Parent gate
A4.3.1   Gate icon
```

The prefix letters are examples, not fixed meanings. Choose letters that remain stable and easy to say during review.

### Hierarchy tree

Show the complete semantic hierarchy in one compact tree. Include regions, modules, important submodules, and cross-region handoffs. Omit purely decorative micro-elements unless they are likely modification targets.

### Mapping tables

For every indexed item record:

| Field | Purpose |
|---|---|
| ID | stable review handle |
| Display name | visible or human-readable name |
| Semantic role | what the item means or does |
| PowerPoint object name | exact `REG_`, `MOD_`, `ICON_`, `CONN_`, `CHART_`, or `TXT_` name |

Keep relationships in a separate table with source, target, direction, level, meaning, and connector object name.

## Maintenance rules

- Preserve IDs when only geometry, typography, or styling changes.
- Change an ID when semantic ownership changes across regions or modules.
- Rename important PowerPoint objects when their semantic role changes.
- Keep parent IDs usable as whole-module edit targets and leaf IDs usable for local edits.
- Distinguish cross-region handoffs from objects owned by either adjacent region.
- Refresh the candidate identity, hierarchy, mappings, and preview after structural changes.
- Prefer one index document per evolving figure rather than separate incompatible notes for every revision.
