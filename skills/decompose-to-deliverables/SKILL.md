---
name: decompose-to-deliverables
description: Break an agreed project scope into useful deliverables with observable acceptance criteria and write the project work list.
---

# Decompose work

Read `project.yaml` and all three files in `docs/` for the explicitly selected project. Report missing prerequisites. Use `docs/file-contracts.md`, `schemas/deliverables.schema.json`, and `templates/deliverables.yaml` for the output contract.

Write `deliverables.yaml` inside the project. Use one workstream containing as many useful slices as the scope actually needs. Each deliverable should be independently checkable in its stated context. Do not claim independence when another unfinished capability is required; choose a narrower slice or state a real, already available prerequisite in the documents.

Use unique IDs such as `GUIDE-001` and `GUIDE-001-AC1`. Describe the beneficiary, capability, and benefit. Write Given/When/Then criteria about observable results. Technical results are appropriate when technical consumers are the users; keep incidental implementation choices in the architecture and plan.

Cover the normal outcome, plausible failure, and meaningful boundaries when they exist. There is no universal number of deliverables or criteria. Do not invent unlikely cases to meet a quota. New items start with `review_status: pending` and empty `review_notes`.

If updating an existing list, preserve unrelated IDs and review records. Changes to promises make existing plans stale; flag affected deliveries for replanning and fresh review. Do not reset a failed result merely to make it pending.

Run `python scripts/validate.py --project <project-path>`. Address structural failures; judge usefulness using the decomposition criteria in `evaluations/criteria.md`. Report unresolved content questions separately from validation results.
