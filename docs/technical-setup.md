# Technical setup

The framework documents and skills work without installing anything. Python tools are optional helpers for creating project folders and checking structured files.

## Install the tools

Use Python 3.11 or newer. From the repository root on macOS or Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The following examples use `.venv/bin/python`; on Windows substitute `.venv\Scripts\python.exe`. A virtual environment keeps these libraries separate from the rest of your machine. Do not commit `.venv/`.

The requirements file pins the two direct dependencies: PyYAML reads YAML, and jsonschema checks the structured formats. Transitive dependencies are resolved by pip; this is not a fully locked dependency environment. No packages are needed by a target project merely because this framework uses Python for validation.

## Create and validate a project

```sh
.venv/bin/python scripts/init_project.py community-guide --name "Community guide"
```

The command refuses to reuse an existing folder. `--destination /path/to/work` changes the parent directory for the new project. It does not initialize Git, install project dependencies, call AI, or create deliverables automatically.

After filling the three documents and creating a work list:

```sh
.venv/bin/python scripts/validate.py --project projects/community-guide
```

Normal mode validates existing work at its current stage. `--complete` requires all deliverables to have recorded passing reviews. Both modes exit with 0 for valid records and 1 for a contract error. They never execute commands stored in plans or evidence fields.

## Verify this starter

```sh
.venv/bin/python scripts/check_example.py
.venv/bin/python scripts/validate.py --project examples/community-event --complete
.venv/bin/python scripts/validate.py --project examples/software-request
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/check_repository.py
```

The first command checks the included sample welcome guide. The next two validate a finished example and a work-in-progress example. Unit tests verify meaningful failure cases. The last command checks local Markdown links, schema definitions, and skill metadata. CI runs these checks on supported Python versions.

## Publish your own copy

The repository must contain only files you intend to publish. For a new local copy, initialize Git, review its status, and commit your files. Then authenticate GitHub CLI and create a new public repository:

```sh
git init -b main
git add .
git commit -m "Add reusable delivery workspace"
gh auth login -h github.com
gh repo create your-repository-name --public --source . --remote origin --push
```

Run these in the new copy's root, not an unrelated existing repository. The command creates a public repository immediately. Use a private repository instead if the project contains information you have not chosen to publish. The framework itself never publishes automatically.

Sources: [Python virtual environments](https://docs.python.org/3/library/venv.html), [GitHub CLI repository creation](https://cli.github.com/manual/gh_repo_create).
