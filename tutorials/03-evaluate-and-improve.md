# Improve instructions using evidence

An assistant can produce neat-looking work that misses the point. Improving it starts with a specific failure and a check that catches it.

Suppose a plan covers the happy path but forgets what should happen when information is missing. “Be more careful” is unlikely to fix that consistently. Asking each task to reference the promises it serves makes the gap visible.

## 1. Save a realistic case

Keep the project inputs, the skill version, and the output that failed. Describe the actual failure in one sentence, such as “AC2 has no task.” Keep sensitive project information out of public examples.

## 2. Choose the right kind of check

Use a deterministic check for structure: unique IDs, references, dependencies, or required fields. Use artifact inspection or behavior tests for actual outcomes. Use a reviewer for meaning: whether the scope solves the user's problem, whether the slices are useful, or whether a proposed design is feasible.

The validator can prove that AC2 appears in a task. It cannot prove that the task is a sensible way to satisfy AC2.

## 3. Observe a useful failure

Copy `examples/community-event` to a temporary folder outside the repository. In the copied plan, remove the AC3 reference from its only task. Run:

```sh
.venv/bin/python scripts/validate.py --project /path/to/your-copy
```

It should reject the uncovered criterion. Restore the reference. Now change one acceptance criterion in the work list without replanning. The validator should reject the stale plan. These failures protect handoffs; neither demonstrates that an AI skill improved.

## 4. Change the smallest useful instruction

If a skill repeatedly drops criteria, explain the source of truth and require complete AC coverage. If it invents an implementation stack, tell it to use the project architecture and record unresolved choices. Do not add a rule about one event's welcome desk to a skill used for every project.

## 5. Try a different project

Rerun the failing scenario and a case from another domain. Use [challenge cases](../evaluations/challenge-cases.md) for ideas. Compare observable output, not whether the wording resembles your preferred answer. Record checks not run.

## 6. Keep an improvement record

Use a short note with: input case, failure observed, change made, checks run, result, and limitations. Commit the note with the instruction change if version control is being used. When a schema changes, update every consumer together.

The included unit tests cover validator behavior. They do not run an AI service or establish an AI quality score. Add a model evaluation harness only when a project needs repeatable model calls and has the necessary access, cost limits, and review process.
