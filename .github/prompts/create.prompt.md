---
name: memis-create
description: Follow the create-deliverable stage using the selected project and saved
  artifacts.
argument-hint: project=projects/memis-cloud deliverable=INFRA-001
agent: agent
---

Follow the [create-deliverable skill](../../skills/create-deliverable/SKILL.md). Interpret the text after this command as the project path and deliverable ID supplied by the user.

Require an explicit `project=...` value before writing files. Also require `deliverable=...`; do not select a pending item silently.

Example invocation: `/memis-create project=projects/memis-cloud deliverable=INFRA-001`. Treat the example as syntax guidance, not an automatic selection.

Follow the skill's inputs, outputs, and validation contract. Report missing prerequisites and record actual results, including checks not run.
