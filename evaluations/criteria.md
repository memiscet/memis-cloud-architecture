# How to judge the assistant's output

These criteria assess the quality of a stage's output. Acceptance criteria describe the promised behavior of a particular deliverable. Keep the two distinct.

Use the applicable rows after each stage. Record the input, output, observed failure, and improvement. Some checks are automatic; judgments such as usefulness still require a person or a carefully reviewed AI assessment.

| Stage | Checkable questions | Who checks? |
|---|---|---|
| Scope | Are intended users, problem, result, boundaries, and success measures stated? Are proposed targets labeled? | Reviewer |
| Architecture | Does every part have a responsibility? Does the approach respect the scope and existing tools? Are important dependencies and tradeoffs explained? | Reviewer |
| Experience | Does each journey have a starting point and an end state? Are likely errors and recovery covered? Are relevant access needs addressed? | Reviewer |
| Decomposition | Is the structure valid? Are IDs unique? Are criteria observable and traceable to the scope? Do the slices have useful outcomes? Are plausible failure and boundary cases covered? | Validator for structure; reviewer for meaning |
| Planning | Does every AC have a task? Do references and dependency order work? Is the source snapshot current? Are affected files and completion checks concrete? | Validator for handoffs; reviewer for feasibility |
| Creation | Does each task produce the intended result? Were named checks actually run? Are deviations and environment blockers recorded? Does the work stay within scope? | Tests and artifact inspection |
| Review | Is every AC assessed once? Does each judgment cite actual evidence? Are unverified results explicit? Does the work-list status match? Is a pass supported? | Validator for records; reviewer for truth |

## Improving a skill

Start with a real failure. For example, if a plan overlooks a required criterion, save the input and failing output. Add a check that catches the omission. Then make the smallest instruction change that prevents it. Rerun the original case and a different project so the fix does not teach the assistant to memorize one example.

Do not add a universal rule for a one-off preference. A project's database, document format, or review style belongs in its project documents unless there is evidence it should be shared.

The runnable test suite deliberately corrupts otherwise valid projects to check unknown references, stale records, false passes, missing evidence, path escapes, and missing prerequisites. It tests file integrity; it does not evaluate an AI model's output quality or claim a benchmark score.
