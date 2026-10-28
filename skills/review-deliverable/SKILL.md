---
name: review-deliverable
description: Review a planned deliverable against every acceptance criterion, record evidence and issues, and update its work-list status.
---

# Review a deliverable

Require a project path and deliverable ID. Read `project.yaml`, the documents, `deliverables.yaml`, the matching plan, implementation summary, and actual planned artifacts. Report missing prerequisites. Check for stale inputs before judging results; a review cannot repair a stale plan by ignoring changed promises.

Follow `docs/file-contracts.md` and `schemas/review.schema.json`. Write `deliveries/<ID>/review.yaml`. Compute `plan_digest` as SHA-256 of the exact plan bytes; the contracts guide gives a command. Assess every AC exactly once and reference actual evidence. Inspect artifacts rather than trusting the implementation summary alone. Run relevant checks if authorized and feasible, recording the command or inspection and observed result.

Distinguish `satisfied`, `not_satisfied`, `partially_satisfied`, and `not_verified`. Each assessment has evidence with method, result (`passed`, `failed`, or `not_run`), and a concrete detail. A missing or unrun check cannot satisfy a promise. Automated structure validation is evidence about file contracts, not proof of the project's behavior.

Use `passed` only when every AC has passed evidence, no blocker or major issue remains, and the plan has no unresolved questions. Use `failed` for a result that fundamentally misses the promised outcome; use `changes_requested` for specific fixes or missing verification. Explain each issue and a useful next action.

Update only the selected deliverable's `review_status` and `review_notes` to exactly match the verdict and summary. Preserve other deliverables. Run `python scripts/validate.py --project <project-path>` and check review criteria in `evaluations/criteria.md`.

For another iteration, keep the earlier review in version control or archive it outside the canonical path; revise the plan when needed, correct the work, and perform a fresh review. Do not mark work passed solely to unblock the next stage.
