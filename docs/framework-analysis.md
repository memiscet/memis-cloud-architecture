# What was extracted from the original framework

The source workspace combines a teaching framework with a Pantry inventory application built using that framework. Its reusable value is the sequence of decisions and the files exchanged between steps. The particular app, teaching schedule, and technology stack are separate concerns.

This analysis describes the local working snapshot inspected on 2026-10-28, including uncommitted files. It is not limited to the last source commit.

## The reusable skeleton

| Layer | Source evidence | Reusable idea | New home |
|---|---|---|---|
| Instruction cards | Seven pipeline skills in `.devin/skills/` | Give each stage a purpose, inputs, outputs, and useful constraints | `skills/` |
| Product understanding | Scope, architecture, UX skills and `sample-docs/` | Establish the problem, approach, and experience before implementation | Project `docs/` |
| Work breakdown | Decomposition skill and `deliverables.yaml` | Small outcomes described by observable acceptance criteria | Project `deliverables.yaml` |
| Planning | Planning skill, root plan, and `plans/` | Connect tasks, files, risks, and completion checks to promises | `deliveries/<ID>/plan.yaml` |
| Creation | Creation skill and implementation summary | Produce the work and record what was actually checked | Planned artifacts and `implementation-summary.md` |
| Review loop | Review skill and schema documentation | Judge each promise, record issues, update the work list | `review.yaml` beside its plan |
| Evaluation | Evaluation criteria documents and contrasting sample inputs | Improve instructions in response to observed failures | `evaluations/` and tutorial 3 |

The source also contains a Terraform review skill. That is a domain-specific extension, so it is not one of the seven general stages.

## What the source already does well

File handoffs make work inspectable and recoverable. Given/When/Then criteria describe behavior before implementation. Plans connect tasks to criteria, identify risks, and name affected files. Review writes back to the work list, closing the loop. Evaluation criteria distinguish the quality of an AI output from the behavior of a particular product.

The stronger source skills explain why rules exist, then give concrete constraints. This is the useful part of the Role / Task / Context / Constraints pattern: describe the job, its purpose, and the rules that materially affect the result. The new cards preserve those functions without requiring four headings in every file.

## Gaps and how this starter addresses them

| Observed in the source | Consequence | New behavior |
|---|---|---|
| README refers to `skills/`; actual files are in `.devin/skills/` | People look in the wrong place | One canonical `skills/` folder with explicit editor integration guidance |
| Several skills are unfinished Role/Task teaching stubs | Critical assumptions remain unstated | All seven cards have actionable inputs, outputs, and completion rules |
| A root `plan.yaml` coexists with per-deliverable copies | The next plan can overwrite the previous one | Exactly one plan and review location per deliverable |
| Schema prose requires one failure case; decomposition requires two | Different checks can disagree | V1 requires one or more criteria; quality guidance asks for relevant normal, failure, and boundary cases without arbitrary counts |
| Fixed limits of 3–8 deliverables and criteria | A small project can grow artificial work | No universal workstream size or criterion count beyond nonempty lists |
| Some text says every skill reads one file and writes one file | Actual creation and review use multiple inputs and outputs | Contracts state the real files and updates |
| YAML formats are explained but no executable schemas exist | Invalid handoffs may reach later stages | JSON Schema plus cross-file validation |
| Review schema has no evidence field or unverified state | A review can sound conclusive without running checks | Per-criterion evidence, `not_verified`, and explicit `not_run` results |
| Evaluation folders mostly contain prose; adversarial and harness folders are placeholders | Readers may mistake future training work for operating tools | Checklists, concrete challenge cases, runnable validation, and clear limits |
| Source conventions mandate a particular test-first practice and dependency age | Local teaching decisions can appear universal | Project-specific verification and dependency decisions belong in the project card and plan |
| Pantry-specific stack and paths appear in creation guidance | Unrelated projects inherit irrelevant choices | Technology comes from each project's documents |

## Deliberate contract changes

This starter is a new V1 format, not a drop-in reader for old YAML. It adds explicit schema versions and a project card. Plans capture the entire source promise so changed criteria invalidate old plans. Reviews record a SHA-256 digest of the plan so editing a plan requires a new review. File operations have separate `action` and `path` fields rather than strings such as “create path”.

Review status is updated in the deliverables list, but reviews remain alongside their own plans. The validator detects mismatches. It does not write changes, execute plan commands, inspect real-world outcomes, or guarantee that recorded evidence is truthful. A reviewer must still judge the result.

## Kept out of the generic starter

The Pantry application code, database schema, migration, API routes, UI components, live project plans, class schedule, and original sample prose were not copied. Neither were local configuration, credentials, dependency folders, or source Git history. We did not extract a generic full-stack application because its choices belong to that example, rather than to the delivery method.

Automated AI execution, multi-agent coordination, publishing, deployments, and live integrations are not implemented. Those can be added for a specific project with its own permissions and operational requirements.
