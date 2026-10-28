# Scope: workspace integration

Make the source framework discoverable by GitHub Copilot without changing its V1 contracts. Contributors need seven synchronized skills, seven explicit prompts, scoped instructions, and an understandable tutorial. Success means local discovery metadata, references, and handoffs validate and generated copies cannot drift unnoticed.

The repository root is the integration project; projects/memis-cloud is the AWS project. This keeps repository-level integration artifacts within their project root while preserving the framework's prohibition on paths escaping a project. The root deliverable concerns Copilot integration; the nested project's deliverables concern architecture, infrastructure configuration, and operations.

Interactive Copilot sessions and live AWS deployment are outside the available local verification. They must be labeled not_run. Requirements and assumptions for AWS are in the nested project's scope. No unresolved decision blocks generating integration files.
