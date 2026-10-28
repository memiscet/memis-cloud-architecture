"""Check local documentation links, schema definitions, and skill metadata."""

import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
import yaml

ROOT = Path(__file__).resolve().parents[1]


def check_repository(root: Path = ROOT) -> list[str]:
    errors = []
    files = [path for path in root.rglob("*.md") if not {".venv", ".git", ".terraform"}.intersection(path.parts)]
    for source in files:
        content = source.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            destination = target.split("#", 1)[0]
            if destination and not (source.parent / destination).exists():
                errors.append(f"Broken local link in {source.relative_to(root)}: {target}")
    for path in (root / "schemas").glob("*.schema.json"):
        try:
            Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
        except (ValueError, SchemaError) as exc:
            errors.append(f"Invalid schema {path.name}: {exc}")
    required = {
        "create-scope", "create-architecture", "create-ux", "decompose-to-deliverables",
        "plan-deliverable", "create-deliverable", "review-deliverable",
    }
    for name in required:
        path = root / "skills" / name / "SKILL.md"
        if not path.is_file():
            errors.append(f"Missing skill {name}")
            continue
        content = path.read_text(encoding="utf-8")
        try:
            if not content.startswith("---\n"):
                raise ValueError("Missing frontmatter")
            metadata = yaml.safe_load(content.split("---", 2)[1])
            if metadata.get("name") != name or not metadata.get("description", "").strip():
                raise ValueError("Name must match folder and description must be present")
        except (ValueError, AttributeError, yaml.YAMLError) as exc:
            errors.append(f"Invalid skill {name}: {exc}")
    return errors


def main() -> int:
    errors = check_repository()
    if errors:
        print("\n".join(errors))
        return 1
    print("Repository checks passed: local Markdown links, schema definitions, and seven skill headers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
