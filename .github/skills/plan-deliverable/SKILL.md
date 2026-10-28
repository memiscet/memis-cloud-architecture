---
name: plan-deliverable
description: Plan one explicitly selected deliverable by connecting tasks, artifacts, risks, and completion checks to every acceptance criterion.
---

# Plan one deliverable

Require a project path and deliverable ID from the caller or unambiguous current context. Do not silently choose the first pending item. Read `project.yaml`, the project documents, `deliverables.yaml`, and the actual files this work will affect. Report missing input or an unknown ID.

Write `deliveries/<ID>/plan.yaml` inside the project using `templates/plan.yaml` and `schemas/plan.schema.json`. Copy the selected deliverable's title, description, and complete criteria into `source_deliverable`; this snapshot lets validation detect changes to promises.

Give each task an ID beginning `<ID>-T`, its concrete approach, relative file paths with `create` or `modify`, relevant risks, dependencies, and an observable `done_when`. Order dependencies before the tasks that use them. Every task must serve a known AC, and every AC must be covered. Check that `modify` files exist and that `create` targets do not unintentionally replace existing work.

Select verification suited to the result. Code changes may need behavior tests and build checks; a guide may need content inspection and a walkthrough. Name the check and its expected result. Use the project's tools and dependency policy; do not introduce a framework-specific stack or testing ceremony without a reason.

Record assumptions and open questions. Questions affecting correct implementation must be resolved before creation. Update `plan_version` when replanning, and explain changes in the implementation summary if creation already began. A changed plan requires fresh review; do not edit a review digest to preserve an old verdict.

Run `python scripts/validate.py --project <project-path>` and check planning criteria in `evaluations/criteria.md`. Report the output path and blockers.
