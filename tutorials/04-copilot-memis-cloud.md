# Continue memis.cloud with Copilot

A skill is an instruction card. A prompt is a convenient way to start one stage. Saved files let a later conversation continue the same work without relying on the previous chat.

## 1. Open the right folder
Clone this repository and open its root in VS Code. Sign into GitHub Copilot using your normal account flow. Select Copilot's agent mode; if your VS Code exposes multiple harness choices, use the Copilot/Local experience supporting these customization files. Features and organization policies vary, so use the official references in the [compatibility record](../docs/copilot-compatibility.md) for your installation.

Read the [simple guide](../docs/start-here.md), then the [scope](../projects/memis-cloud/docs/scope.md). This is a reference architecture with local evidence, not a claim of a running memis.cloud deployment.

## 2. Find the instructions
The repository-wide guidance is in .github/copilot-instructions.md. Skills are discoverable under .github/skills/, and the manually invoked prompts are under .github/prompts/. Type `/` in Copilot Chat to look for the memis-prefixed prompts, or use VS Code's prompt-file picker.

If discovery is unavailable, use this explicit prompt:

> Read `skills/create-architecture/SKILL.md` and follow it for `projects/memis-cloud`. First inspect the existing scope and architecture. Explain any proposed revision before changing established decisions.

## 3. Follow the seven stages
The project already contains an initial pass. Review it before asking Copilot to regenerate files. To practice the whole method, create a new project with the initializer and use its path in place of projects/memis-cloud.

| Stage | Example prompt invocation |
|---|---|
| Scope | `/memis-scope project=projects/memis-cloud focus=review-existing-scope` |
| Architecture | `/memis-architecture project=projects/memis-cloud focus=review-existing-design` |
| Experience | `/memis-experience project=projects/memis-cloud focus=operator-recovery` |
| Decomposition | `/memis-decompose project=projects/memis-cloud focus=inspect-current-deliverables` |
| Planning | `/memis-plan project=projects/memis-cloud deliverable=INFRA-001` |
| Creation | `/memis-create project=projects/memis-cloud deliverable=INFRA-001` |
| Review | `/memis-review project=projects/memis-cloud deliverable=INFRA-001` |

The arguments are text the prompt instructs Copilot to interpret; they are not a separate executable CLI. Use the actual project and ID you intend to change. For repository integration, select `project=.` and `deliverable=COPILOT-001` instead.

## 4. Inspect results and run checks
Open the modified documents, plan, and declared files. Ask Copilot to explain changes using the acceptance criteria. Run the local and Terraform checks in the [setup guide](../projects/memis-cloud/docs/setup.md). Read failures rather than asking for a green verdict without evidence.

If you change a requirement, revise the affected plan and repeat review. If you change a canonical skill, regenerate its Copilot copy and run the synchronization check. Never edit a digest merely to keep a previous passing review.

## 5. Handle a failure
For a stale-copy failure, run `python scripts/sync_copilot.py` with your configured Python environment. For a stale-plan failure, reread the updated promise and replan. For an AWS runtime failure, use the operations guide and collect live observations; local mocks cannot diagnose a real account automatically.

## 6. Continue in a new chat
Use a prompt such as:

> Read README.md, AGENTS.md, and docs/file-contracts.md. Continue project `projects/memis-cloud`, deliverable `INFRA-001`. Inspect its current deliverable, plan, implementation summary, and review before proposing changes. Check the validation record and live checklist so you distinguish completed local checks from work not run.

## 7. Verify your Copilot installation
Confirm the repository instructions are available, choose one prompt, and ask for a read-only review of an existing artifact. Inspect whether the correct project files and skill were used. Then try a change in a disposable copy and run validation. Record VS Code/Copilot versions, observed discovery, files changed, commands run, and results. Those interactive checks remain not_run in this package until someone performs them.
