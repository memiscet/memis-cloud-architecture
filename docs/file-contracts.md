# What each file means

A file contract is an agreement about where information lives and what it contains. The assistant can use several input files and write several outputs. The goal is a clear handoff, not an artificial one-file limit.

## Project layout

```text
projects/my-project/
├── project.yaml
├── docs/
│   ├── scope.md
│   ├── architecture.md
│   └── experience.md
├── deliverables.yaml
├── artifacts/                         One possible output location
└── deliveries/
    └── WORK-001/
        ├── plan.yaml
        ├── implementation-summary.md
        └── review.yaml
```

`artifacts/` is a convention for documents, not a required application layout. Software may live in `src/`, `api/`, or another planned location within the project. Artifact paths in a plan are relative to its project root, use `/`, and cannot escape to a parent directory. For an existing codebase, make its root the project root and pass that path explicitly.

## Stage handoffs

| Skill | Reads inside the selected project | Writes or updates |
|---|---|---|
| create-scope | Request, project card, supplied requirements | `docs/scope.md` |
| create-architecture | Project card, scope, existing files where relevant | `docs/architecture.md` |
| create-ux | Project card, scope, architecture | `docs/experience.md` |
| decompose-to-deliverables | Project card and all three documents | `deliverables.yaml` |
| plan-deliverable | Project card, documents, work list, affected files | `deliveries/<ID>/plan.yaml` |
| create-deliverable | Project card, documents, work list, selected plan | Planned artifacts and `deliveries/<ID>/implementation-summary.md` |
| review-deliverable | All selected inputs, artifacts, and summary | `deliveries/<ID>/review.yaml`; selected item's status and notes in `deliverables.yaml` |

Review the existing documents before replacing them. A missing prerequisite is a clear request for the previous step, not permission to invent its content.

## Structured files

All four structured formats have `schema_version: "1.0"`. Their exact fields are defined in [schemas](../schemas/). Extra fields are rejected so misspellings do not disappear silently. Use quotes for dates and version numbers. YAML keys must be text and cannot repeat.

| File | Main information |
|---|---|
| `project.yaml` | Project ID, name, kind, owner, and verification approach |
| `deliverables.yaml` | One workstream and a nonempty list of deliverables, criteria, and review statuses |
| `plan.yaml` | Deliverable ID, plan version, source promise snapshot, tasks, dependencies, files, risks, AC references, assumptions, and questions |
| `review.yaml` | Review ID and date, deliverable ID, plan digest, verdict, issues, per-AC evidence, and summary |

Project IDs look like `community-event`. Deliverable IDs look like `GUIDE-001`. AC IDs append `-AC1`; task IDs append `-T1`. Numbering is local to each project. A plan's `source_deliverable` contains the current title, description, and full acceptance criteria in their original order. Review status and notes are excluded from that snapshot so recording a review does not invalidate the plan.

An `artifacts_affected` entry has an `action` (`create` or `modify`) and a `path`. The creation skill checks those actions against actual files before doing work. After review, the validator checks that all declared files exist. It cannot retrospectively prove whether a file was newly created or modified.

## What the validator checks

```sh
.venv/bin/python scripts/validate.py --project projects/my-project
```

Normal mode supports work in progress. It requires the project card, three documents, and a work list. Deliverables may be unplanned, and plans may be unreviewed; those items must still say `pending` with empty notes. Reviews require a plan, summary, and declared artifacts. A recorded non-passing review is valid if its handoffs are consistent.

It checks required fields, allowed values, unique IDs, dependency order, known and complete AC references, current source snapshots, safe paths, complete review assessments, evidence records, and synchronized verdicts. It rejects orphan delivery folders and reviews without plans.

```sh
.venv/bin/python scripts/validate.py --project projects/my-project --complete
```

Complete mode additionally requires a plan, summary, declared artifacts, and passed review for every deliverable. A passed review requires every AC satisfied with passed evidence, no major/blocker issues, and no unresolved plan questions. This verifies recorded completion; it does not rerun evidence or prove semantic correctness. Document templates can be structurally present while still containing poor content, so read them.

## Review evidence and status

Each AC receives one assessment: `satisfied`, `not_satisfied`, `partially_satisfied`, or `not_verified`. Each assessment includes one or more evidence entries. An entry names the method (`automated_test`, `manual_check`, or `document_inspection`), result (`passed`, `failed`, or `not_run`), and enough detail to understand or reproduce it.

The deliverable begins as `pending`. A review changes it to `passed`, `failed`, or `changes_requested`. Copy the review's verdict into `review_status` and its exact summary into `review_notes`. The original review file is the detailed record.

A review also records the exact plan it assessed. Compute its digest from the repository root:

```sh
.venv/bin/python -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('projects/my-project/deliveries/WORK-001/plan.yaml').read_bytes()).hexdigest())"
```

Copy that value into `plan_digest` during a fresh review. Any later byte change to the plan, including formatting, invalidates the review digest. Reassess the changed plan and artifacts before writing a new review. Do not merely refresh the digest to keep an old pass.

The digest protects the plan handoff only. It does not hash implementation artifacts. Rerun relevant tests and review when those artifacts change, even if file validation passes. Version control preserves the history; the validator is not an audit or provenance service.
