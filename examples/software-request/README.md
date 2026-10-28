# Example: plan a software change

This fictional project plans a small Python function for ranking support requests. It demonstrates technical project choices without forcing them into shared skills.

Read the [scope](docs/scope.md), [architecture](docs/architecture.md), [experience](docs/experience.md), [work list](deliverables.yaml), and [plan](deliveries/QUEUE-001/plan.yaml).

The project is deliberately pending. No implementation, tests, summary, or review is supplied, so no behavior has been claimed as verified.

```sh
.venv/bin/python scripts/validate.py --project examples/software-request
```

Run that from the framework repository root. Normal validation should pass the planning handoffs. `--complete` should fail because delivery has not happened. To practice, make a copy in `projects/`, then follow creation and review for `QUEUE-001`.
