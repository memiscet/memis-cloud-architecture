# Copilot compatibility and verification

The target experience is GitHub Copilot agent mode in VS Code. The repository contains the files it can discover, but no interactive Copilot session was executed while producing this package.

| Feature | Files | Verification |
|---|---|---|
| Repository guidance | .github/copilot-instructions.md | File presence and documentation inspection |
| Skills | .github/skills/<name>/SKILL.md | Seven valid headers and byte-for-byte source synchronization |
| Explicit prompts | .github/prompts/*.prompt.md | Seven headers, command names, hints, and canonical links |
| Scoped instructions | .github/instructions/*.instructions.md | Metadata and nonempty applyTo patterns |
| Automatic discovery in VS Code | Interactive client behavior | not_run: no interactive client session available |
| Full representative workflow in Copilot | Read/write/terminal behavior | not_run: follow the tutorial to verify in your installation |
| Other Copilot clients | Client-specific discovery and features | not_run; no universal compatibility claim |

Skills are generated from canonical skills/ files. Use `python scripts/sync_copilot.py` after edits, then `python scripts/sync_copilot.py --check`. The verifier rejects stale or missing copies. Prompts are maintained separately as small entry points; they link to shared instructions instead of duplicating the workflow.

Supported customization surfaces can vary by client, version, and organization policy. The portable fallback is to ask the assistant to read a named canonical SKILL.md and follow it with explicit project and deliverable arguments.

Official references: [GitHub skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills), [VS Code prompt files](https://code.visualstudio.com/docs/agent-customization/prompt-files), and [scoped instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions).
