# Adapt the skeleton to your project

Keep the handoffs and replace the project-specific facts. You do not need the original Pantry app, the example event, or a particular AI editor.

## Starting a new project

Create a project with the initializer or copy the templates manually. Fill in the project card, then scope, approach, and experience. Keep the technology choice open until the requirements justify one. For a process project, components may be roles, records, and handoffs; for software they may be services, screens, and data stores.

Use the seven cards in order. The last three repeat per deliverable. Check one useful piece before planning everything in detail.

## Adopting it in an existing codebase

Treat that codebase's root as the project root. Add `project.yaml`, the three project documents under `docs/`, and `deliverables.yaml` only after checking for naming conflicts. Keep the framework's scripts, schemas, and skills in this separate toolkit repository; `--project` accepts an absolute path to another project. The cards can be referenced by their absolute toolkit paths.

If existing files use those names for another purpose, use a separate project wrapper or deliberately change the contract in your own copy. Do not overwrite them. The supplied validator expects the documented paths and cannot infer a custom layout.

Summarize and link existing trusted requirements instead of pretending the project starts from zero. Inspect current code before planning modifications. Existing tests and build tools should inform verification. A plan's artifact paths are relative to the codebase root when that is the selected project.

## Change the right layer

| If you need to change… | Change this |
|---|---|
| Users, promises, features, or project boundaries | Scope and relevant deliverables; revisit affected plans |
| Language, libraries, data flow, or responsibilities | Architecture and affected plans |
| Messages, journeys, access needs, or recovery | Experience document and relevant criteria |
| Where a file goes or which task creates it | Selected plan; repeat review after changing it |
| A recurring AI mistake across projects | A narrowly targeted skill instruction and evaluation case |
| The shape of structured files | Schemas, validator, templates, examples, and contract documentation together |

## Software example

The [request-priority example](../examples/software-request/README.md) shows a developer planning a pure function for sorting support requests. It has no front end or database because the scope does not call for them. The example stops at planning and is labeled pending. It demonstrates how software facts belong in project documents, rather than in the shared cards.

## Moving from the original framework

Do not copy old YAML straight into this starter and expect it to validate. Add `schema_version: "1.0"`; create a project card and the three documented inputs; move each plan to `deliveries/<ID>/plan.yaml`; replace action/path strings with structured entries; and copy the complete current promise into `source_deliverable`.

Review records need per-criterion evidence and a digest of their exact plan. Do not convert an old verdict into a new passing review without checking the underlying work. Keep original files in history or an archive until you have verified the migration.

## Make a smaller framework when appropriate

For a short document change, a few sentences per input document can be enough. For a complex project, link substantial references from those documents. Keep only instructions that help the next person or assistant make a real decision.
