---
name: memis-decompose
description: Follow the decompose-to-deliverables stage using the selected project
  and saved artifacts.
argument-hint: project=projects/memis-cloud [requirements or focus]
agent: agent
---

Follow the [decompose-to-deliverables skill](../../skills/decompose-to-deliverables/SKILL.md). Interpret the text after this command as the project path and requirements or focus supplied by the user.

Require an explicit `project=...` value before writing files. Use the current project card and documents; preserve existing user decisions.

Example invocation: `/memis-decompose project=projects/memis-cloud [requirements or focus]`. Treat the example as syntax guidance, not an automatic selection.

Follow the skill's inputs, outputs, and validation contract. Report missing prerequisites and record actual results, including checks not run.
