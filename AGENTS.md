# Working in this repository

Read README.md and docs/file-contracts.md before changing framework behavior.

The seven canonical skills live in skills/. Generated Copilot copies live in .github/skills/. Edit canonical files and run scripts/sync_copilot.py; check synchronization before committing. Explicit prompts live in .github/prompts/. See docs/copilot-compatibility.md for tested surfaces and limits.

For project work, use the explicit project path and deliverable ID. Read project.yaml and the project's documents. Keep plans, summaries, and reviews in deliveries/<ID>/ inside that project. Never select work silently or overwrite another project's files.

Preserve the user's project scope and technology choices. A missing prerequisite or an unresolved decision that affects correctness should be reported, rather than filled in as a fact. Record nonblocking assumptions. The framework does not grant permission to publish, deploy, send messages, or change live services.

The repository root is the workspace-integration project; projects/memis-cloud is the AWS project. Select one explicitly. This preserves project-relative path containment for repository-level integration files.

Run python scripts/verify_workspace.py for local workspace checks. Infrastructure changes also require Terraform fmt, validate, and mocked tests in projects/memis-cloud/infra. These commands do not establish live AWS readiness. Keep schemas, templates, examples, instructions, and documentation consistent when changing contracts. Do not claim a deliverable passed based only on schema validation.
