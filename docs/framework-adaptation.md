# How the original framework was applied

The source is Reusable Delivery Framework at commit 6cbbcb5205c28ada8e8e956bd593fe73eb12d0c6. Its skills, templates, V1 schemas, examples, validator, and evaluation criteria were inspected before adapting it. The original starter workspace also contains Pantry-specific application code and training artifacts; those are not infrastructure conventions and were not carried into this project.

| Source element | Kept | Applied here |
|---|---|---|
| Seven canonical skills | Same instructions and stage sequence | AWS scope, architecture, operator experience, decomposition, plans, outputs, review |
| V1 schemas | Unchanged | Root integration and nested AWS project use the same contracts |
| Per-deliverable folders | Unchanged | ARCH-001, INFRA-001, OPS-001, and COPILOT-001 each have a plan, summary, review |
| Source snapshots and plan digests | Unchanged | Changed promises invalidate plans; changed plans invalidate reviews |
| Evidence and not_verified | Unchanged | Local artifact evidence stays distinct from live checks |
| Generic examples/tests | Reused | Provide small examples and regression protection for handoffs |
| Evaluation criteria | Reused | Add domain-specific configuration tests without turning AWS choices into universal rules |
| Canonical skills/ directory | Retained | Generate synchronized .github/skills/ copies for Copilot |

## Why there are two projects

The root project owns Copilot integration files, which live under .github/. The nested projects/memis-cloud project owns AWS configuration and operational documents. A nested plan cannot name ../../.github paths because the original contract forbids escaping a project root. Using two ordinary projects preserves that rule without extending the schema.

The first three stages produce the project documents. Decomposition creates work lists. Plans were written before their implementation artifacts, with explicit files and checks. Creation produced configuration and guides. Reviews cite checks and inspections rather than treating format validation as runtime success.

## Additions

Copilot prompt files wrap the existing skills rather than reimplementing their logic. Scoped instructions keep memis.cloud facts local. A synchronization tool prevents generated-skill drift. Terraform is a new project-specific tool choice because the source has no established IaC implementation. Its mock tests and network checks supplement the original validator.

The verifier composes existing validation with new integration checks. CI checks Python compatibility and Terraform configuration. It does not deploy infrastructure or execute an AI agent service.

## Deliberate limits

The six-subnet baseline is a documented compromise, not a claim of fully isolated tiers in each AZ. The Nginx page is a bootstrap service. Actual application logic, database-user provisioning, live AWS tests, and interactive Copilot verification remain explicit. See the validation record and live checklist for their status.
