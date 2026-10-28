---
name: create-scope
description: Turn a project idea into a bounded scope with observable success measures before design or delivery planning.
---

# Create scope

Agree on the problem before choosing a solution. Use the caller's explicit project path; read `project.yaml`, the request, and any supplied requirements. If no project exists, propose a path and use `scripts/init_project.py` within the authorized workspace.

Write `docs/scope.md` inside that project, using `templates/scope.md` as a starting point. Describe users, their problem, the intended result, how success will be measured, what is included, and what is excluded. Distinguish facts, assumptions, and open decisions. Do not invent stakeholder agreement, numerical targets, or user research.

Use the user's terminology and constraints. A useful scope can be short. Existing requirements may be summarized and linked rather than rewritten. If an unanswered question changes the core outcome, ask it before treating the scope as settled; continue independent work where possible.

Finish by stating the written path and unresolved decisions. Check it against the scope criteria in `evaluations/criteria.md`. This stage does not authorize implementation or external actions.
