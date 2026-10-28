---
name: create-deliverable
description: Produce the artifacts in an existing deliverable plan and record actual verification, assumptions, and deviations.
---

# Create a deliverable

Require an explicit project and deliverable ID. Read the project card, project documents, `deliverables.yaml`, and `deliveries/<ID>/plan.yaml`. Report missing prerequisites. Validate handoffs before implementing. If `open_questions` affect correctness, resolve them before dependent work.

Produce the planned artifacts in dependency order. Paths are relative to the project. Use the selected tools and conventions. Check `create`/`modify` actions against the current files; do not overwrite unrelated work. Add supporting files only when needed for the agreed result, recording any material deviation and revising the plan when its contract changes.

Use verification proportional to the work. Where tests are useful, check observable behavior from the acceptance criteria. Run the checks named by `done_when` when the environment permits. Do not weaken a check to make it pass. If access, dependencies, or missing information block completion, record the blocker and finish independent authorized work. Stop repeated attempts when no new evidence suggests a different result.

Write `deliveries/<ID>/implementation-summary.md` using the summary template. Include task status, outputs, commands or manual checks actually performed, results, and deviations. Label unexecuted checks `not_run` with the reason. Do not imply a test ran because its source file exists.

Check creation criteria in `evaluations/criteria.md`. Report the result and remaining blockers. Creating local artifacts does not itself authorize committing, publishing, deploying, or sending them elsewhere; use the user's existing authorization for those actions.
