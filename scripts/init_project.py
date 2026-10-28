"""Create an isolated project without overwriting existing work."""

import argparse
from pathlib import Path
import re
import shutil
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]


def initialize(slug: str, name: str, destination: Path) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Use a lowercase project slug such as community-event.")
    if not name.strip():
        raise ValueError("The project name cannot be blank.")
    project = destination / slug
    # mkdir is deliberately exclusive; no existing project may be overwritten.
    project.mkdir(parents=True, exist_ok=False)
    (project / "docs").mkdir()
    (project / "deliveries").mkdir()
    for filename in ("scope.md", "architecture.md", "experience.md"):
        shutil.copyfile(ROOT / "templates" / filename, project / "docs" / filename)
    config = {
        "schema_version": "1.0",
        "id": slug,
        "name": name,
        "kind": "Choose software, document, process, event, or another description",
        "owner": "Name the person or team making project decisions",
        "verification": ["Describe how the result will be checked"],
    }
    (project / "project.yaml").write_text(
        yaml.safe_dump(config, sort_keys=False), encoding="utf-8"
    )
    return project


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="Folder name, for example community-event")
    parser.add_argument("--name", required=True, help="Human-readable project name")
    parser.add_argument("--destination", type=Path, default=ROOT / "projects")
    args = parser.parse_args()
    try:
        project = initialize(args.slug, args.name, args.destination)
    except (OSError, ValueError) as exc:
        print(f"Cannot initialize project: {exc}", file=sys.stderr)
        return 1
    print(f"Created {project}")
    print("Fill project.yaml and docs/, then create deliverables.yaml using the decomposition skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
