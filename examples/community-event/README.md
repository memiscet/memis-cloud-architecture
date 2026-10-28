# Example: a community welcome guide

This fictional project demonstrates the complete flow without an application, database, or live event. Its result is a short [welcome guide](artifacts/welcome-guide.md).

Read the files in this order:

1. [Project card](project.yaml): who owns the example and how it will be checked.
2. [Scope](docs/scope.md): the problem and boundaries.
3. [Approach](docs/architecture.md): responsibility for information and updates.
4. [Experience](docs/experience.md): arrival, missing information, and room changes.
5. [Work list](deliverables.yaml): one useful result with three promises.
6. [Plan](deliveries/GUIDE-001/plan.yaml): the task, risks, output, and check.
7. [Result](artifacts/welcome-guide.md) and [summary](deliveries/GUIDE-001/implementation-summary.md).
8. [Review](deliveries/GUIDE-001/review.yaml): the evidence and recorded verdict.

From the repository root:

```sh
.venv/bin/python scripts/check_example.py
.venv/bin/python scripts/validate.py --project examples/community-event --complete
```

The first command checks the sample guide's content against its three narrow criteria. The second checks handoffs and recorded completion. Neither evaluates a real event, a guest's actual experience, or physical print quality. Those claims are outside this sample's scope.
