# Your first project: a welcome guide

You can complete this tutorial without installing software. Use a text editor and an AI assistant that can read the repository. If the assistant cannot write files, ask for their contents and save them yourself.

The goal is a one-page welcome guide for a fictional community event. It should help a guest arrive, ask for help, and cope with a last-minute room change. The [finished example](../examples/community-event/README.md) is available for comparison.

## 1. Open a project folder

Create `projects/my-event/`. Copy the three Markdown templates into its `docs/` subfolder. For `project.yaml`, use the project card in the finished example and change the ID, name, owner, and verification approach to match your event. If you prefer, the optional initializer does these copies:

```sh
.venv/bin/python scripts/init_project.py my-event --name "My community event"
```

## 2. Explain the problem

Ask your assistant:

> Read `skills/create-scope/SKILL.md` and follow it for `projects/my-event`. Guests need a short printed guide that explains arrival and where to get help. The room can change at short notice. We want a document, and event registration is outside this project. Treat event details as fictional examples until I confirm them.

Read `docs/scope.md`. Can you explain the promised result in one sentence? Does it clearly say what is excluded? Correct anything the assistant assumed incorrectly.

## 3. Decide the approach and experience

Use these prompts in order:

> Follow `skills/create-architecture/SKILL.md` for `projects/my-event`. Use the current scope. Keep the result as a simple document.

> Follow `skills/create-ux/SKILL.md` for `projects/my-event`. Describe how a guest uses a printed guide, including what happens when information is missing.

Read the outputs. For this example, the approach might give the event coordinator responsibility for confirmed details and make the welcome desk the fallback for changes. The experience should work without a phone or internet connection.

## 4. Make the work list

> Follow `skills/decompose-to-deliverables/SKILL.md` for `projects/my-event`. Keep the list as small as the scope allows.

Open `deliverables.yaml`. Read each Given/When/Then as a real situation. Replace “helpful,” “easy,” and similar vague results with something you could observe. Expect a normal case, a missing-information case, and a room-change case if those are part of your scope. Do not copy a technology stack from an unrelated project.

## 5. Plan and create one piece

Find its ID in the work list; use that actual ID in these prompts:

> Follow `skills/plan-deliverable/SKILL.md` for `projects/my-event`, deliverable `GUIDE-001`.

Read the tasks before continuing. They should name the file being produced and how it will be checked.

> Follow `skills/create-deliverable/SKILL.md` for `projects/my-event`, deliverable `GUIDE-001`.

Read the guide itself. Check the summary for what was actually verified. A proposed walkthrough is different from a walkthrough someone performed.

## 6. Review the promises

> Follow `skills/review-deliverable/SKILL.md` for `projects/my-event`, deliverable `GUIDE-001`. Inspect the guide against each acceptance criterion. Record missing checks honestly.

The result may be `changes_requested`. That is useful: it tells you what remains. Fix the stated problems and review again. A passed review needs evidence for every promise. The example's automated content check checks only the fictional sample; it does not prove your event is ready.

You have completed the tutorial when the guide exists, its acceptance criteria have evidence, the review verdict is justified, and the work list matches it. If using the tools, run the validator in complete mode. Otherwise, manually compare the files using [file contracts](../docs/file-contracts.md).
