# Contributing

## Scope

Contributions should improve editable Microsoft PowerPoint redraws of academic architecture diagrams, workflows, and system diagrams.

## Rule admission

Do not add a rule for every isolated correction. A new rule should be:

- repeated or high impact;
- transferable across tasks;
- shorter and cheaper than the failure it prevents;
- supported by a real artifact, anonymized report, or deterministic regression;
- compatible with both editability and first-delivery cost.

Project-specific coordinates, private files, paper terminology, and one-off visual preferences do not belong in the skills.

## Pull requests

1. Explain the user impact and affected skill.
2. Add or update the smallest relevant test.
3. Run:

   ```bash
   python scripts/validate_public_repo.py
   python tests/test_field_comparison.py
   ```

4. State what was validated in Microsoft PowerPoint, if applicable.
5. Confirm that no user data, absolute local paths, private screenshots, or unlicensed assets are included.

## Style

- Keep `SKILL.md` concise.
- Put detailed conditional guidance in one-level `references/`.
- Put deterministic repeated work in `scripts/`.
- Add assets only when licensing, reuse value, and PowerPoint behavior are clear.
