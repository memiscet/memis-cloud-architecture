# Using the instruction cards with an AI assistant

The canonical cards are in `skills/<name>/SKILL.md`. Each has a short machine-readable name and description followed by its instructions. They use relative paths rooted at this repository and project-relative artifact paths.

## The portable method

Use this prompt with an assistant that can read your workspace:

> Read `skills/create-scope/SKILL.md` and follow it for `projects/my-project`. My project idea is: [explain your idea].

For a delivery stage, include the ID:

> Read `skills/plan-deliverable/SKILL.md` and follow it for `projects/my-project`, deliverable `WORK-001`. Use the current project documents and files.

This method works without automatic discovery or slash commands. An assistant that cannot write files can draft the contents for you to save. An assistant that cannot run checks must say which checks were not run.

## Automatic discovery

Some tools look for skills in their own special folders, and their supported metadata differs. This repository does not promise that an arbitrary editor will discover `skills/` automatically. Use the portable method first. If your tool supports local skills, register or copy these folders using that tool's documented mechanism; keep `skills/` as the source of truth and refresh copies after changes.

Do not put proprietary project requirements into a shared skill just to make discovery work. Keep project facts in project documents. Do not assume a skill's name guarantees a slash command exists in your tool.

## Which card comes next?

Read the table in [file contracts](file-contracts.md). The first four stages describe and divide the whole project. The last three repeat for each deliverable. Review can send work back for fixes. You do not need to rewrite an unchanged scope for every iteration.
