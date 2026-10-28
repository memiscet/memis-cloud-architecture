---
name: create-architecture
description: Describe components, responsibilities, dependencies, and important decisions for a scoped project, including non-software work.
---

# Create architecture

Read the selected project's `project.yaml` and `docs/scope.md`. If the scope is missing, report the prerequisite and do not invent it. Inspect an existing project's actual files and conventions before suggesting a replacement approach.

Write `docs/architecture.md`, using `templates/architecture.md`. Explain the parts, what each owns, how information moves, and why consequential choices fit the scope. For a document or process, parts may be people, documents, and handoffs. For software, include relevant interfaces, data ownership, failure boundaries, and the selected stack.

Preserve technologies and constraints the user has chosen. Name real dependencies and access or environment prerequisites. Record tradeoffs and assumptions. An unresolved choice that changes correctness belongs in open questions, not in an invented decision. Do not add infrastructure merely to fill the template.

Check consistency with the scope and the architecture criteria in `evaluations/criteria.md`. Report the output path and decisions that still need input.
