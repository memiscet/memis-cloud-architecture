---
name: create-ux
description: Describe the user's journey, visible outcomes, error recovery, and accessibility for a scoped product, document, event, or process.
---

# Create experience guidance

Read `project.yaml`, `docs/scope.md`, and `docs/architecture.md` in the selected project. Report missing prerequisites. Write `docs/experience.md` from `templates/experience.md`. The skill keeps the familiar UX name; its output also covers experiences that have no screen.

Describe each relevant person's starting point, action, feedback, decision, and end state. Include likely mistakes and a practical recovery route. Use exact labels or thresholds when established by the requirements. If they are undecided, mark them as proposals instead of inventing precision.

For a UI, explain empty, loading, failure, and success states where applicable; include keyboard access, focus behavior, and alternatives to color-only information. For documents or events, consider reading, print, language, and access needs. Do not prescribe UI components unless the project already selects them.

Keep behavior consistent with the scope and architecture. Check `evaluations/criteria.md`. Report the path and assumptions that affect later acceptance criteria.
