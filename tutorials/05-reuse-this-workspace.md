# Reuse this workspace for another project

Keep the workflow and replace the facts. You do not need Route 53, Nginx, or PostgreSQL for an unrelated project.

1. Read docs/file-contracts.md and create a new project with `python scripts/init_project.py another-project --name "Another project"` using your virtual environment.
2. Fill the project card, scope, approach, and experience. Existing trusted documents may be summarized and linked.
3. Run the first four stages to produce a bounded work list. A document, process, or software project can use the same contracts.
4. Select one explicit deliverable, plan it, create its outputs, and review evidence. Repeat for other deliverables.
5. Keep project-specific technologies and constraints in that project's documents. The memis.cloud infrastructure instruction is scoped to its own folder.
6. Change a canonical skill only for a recurring workflow problem; add an evaluation case and regenerate the Copilot copies.

For a separate repository, retain skills/, schemas/, templates/, scripts/, the desired examples/tests, and Copilot files. Update links and root instructions to match the new layout. Archive or remove the memis.cloud project deliberately; its verifier currently expects that project, so adapt verification and CI together. Do not advertise it as a configurable universal infrastructure module.

The root integration project exists because repository-level Copilot files live outside the nested AWS project. Both use the original schema without unsafe parent-relative paths. Use the same pattern if a future project needs repository-wide work; a single root project is also valid for a small codebase.

If you migrate older deliverables, preserve their history and perform fresh review where source promises or plans changed. A copied passing verdict is not proof that new project behavior has been checked.
