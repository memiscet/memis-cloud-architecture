# Approach: workspace integration

Canonical skills remain in skills/. scripts/sync_copilot.py generates byte-identical .github/skills/ copies and verifies synchronization. Copilot prompt files link to canonical skills, ask for explicit project paths and deliverable IDs, and retain the existing stage contracts. Scoped instructions apply project-specific guidance only to relevant files.

The original schemas, templates, examples, and validator are reused. A separate workspace verifier composes existing checks with network, Copilot, and root/nested project checks. It never runs AWS deployment commands. The GitHub workflow runs both Python and mocked Terraform checks.

The integration project lives at the repository root; the AWS project lives in projects/memis-cloud. This is a deliberate use of the existing root-relative contract, not a schema extension. Stale plans and reviews remain invalid. Editing a canonical skill requires regeneration before checks pass. Interactive discovery remains an explicit manual verification step.
