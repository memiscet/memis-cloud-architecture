# When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Python cannot import yaml or jsonschema | The validation libraries are not in this Python environment | Install requirements and use the virtual environment's Python |
| Initializer says the folder exists | Existing work is being protected | Use that project, choose another slug, or move it yourself after inspecting it |
| Missing deliverables.yaml | The project has not reached decomposition | Finish the documents and follow the decomposition card |
| Missing docs file | A required input is absent | Create or map the existing document before continuing |
| Duplicate YAML key | A label occurs twice in the same mapping | Keep one intended value; do not depend on “last value wins” |
| Schema error for a version or date | YAML interpreted the value as another type | Quote versions such as "1.0" and dates such as "2026-10-28" |
| Unknown or forward dependency | A task depends on itself, an absent task, or a later task | Correct the reference and order tasks before their dependents |
| Uncovered AC | At least one promise has no planned task | Add the needed work or correct the AC references |
| Stale plan | The current promise differs from the plan snapshot | Revisit the tasks, update the snapshot and version, then review again |
| Stale review | The plan changed after the recorded review | Reassess the work and write a fresh review with the new digest |
| Review status or notes out of sync | The detailed review and work list disagree | Copy the real verdict and exact summary into the selected work-list item |
| Missing reviewed artifact | A declared result does not exist | Restore or produce it, or revise the plan and review truthfully |
| Complete mode fails on pending work | Complete mode expects every result to have passed | Use normal mode during work; finish the missing stages before claiming completion |
| Unsafe project-relative path | A file points outside the project or uses an unsupported path format | Use a relative path with `/` inside the selected project root |
| Validator passes but the result is poor | File structure checks do not judge usefulness | Read the artifacts and inspect evidence against the real acceptance criteria |
| Assistant cannot find a skill | The editor may not discover the canonical folder | Ask it to read the exact SKILL.md path; see using-skills.md |
| GitHub returns Requires authentication | CLI login is missing or expired | Run gh auth login -h github.com locally; do not paste tokens into project files |

If you need help, share the error, the command, and a small sanitized example. Distinguish a file-contract error from a failed project test: they need different fixes.
