# Working in this repository

Read README.md, docs/file-contracts.md, and the selected project's project.yaml before writing artifacts. Treat paths in skill instructions as repository-relative unless described as project-relative.

Use the seven stages: scope, architecture, experience, decomposition, planning, creation, review. Skills are canonical in skills/ and generated for discovery in .github/skills/. Explicit stage prompts are in .github/prompts/. Edit canonical skills and run python scripts/sync_copilot.py; never maintain two different versions.

Require an explicit project path. Delivery stages also need an exact deliverable ID. The root project concerns Copilot integration; projects/memis-cloud concerns AWS. Keep each plan and review in its own deliveries/<ID>/ folder. Use the selected project's documents as the authority for requirements and technology choices.

Preserve V1 schemas. Missing prerequisites must be reported. Record nonblocking assumptions; resolve decisions affecting correctness before dependent work. Replan changed promises, and perform fresh review after plan changes. Never preserve a pass by merely refreshing its digest.

Use .venv/bin/python scripts/verify_workspace.py for local checks. The README gives Terraform fmt, validate, and mocked-test commands. Windows uses .venv/Scripts/python.exe. Record actual evidence, including failed or not_run checks. Static metadata validation does not prove Copilot behavior or AWS readiness.

Deployment and DNS changes require task-specific authorization. The current deliverable is a published architecture/configuration workspace. Follow the user's existing authorization without asking for repeated confirmation.
