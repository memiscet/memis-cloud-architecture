"""Generate Copilot skill copies from canonical skills, or check for drift."""

import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "create-scope", "create-architecture", "create-ux", "decompose-to-deliverables",
    "plan-deliverable", "create-deliverable", "review-deliverable",
)


def synchronize(root: Path = ROOT, check: bool = False) -> list[str]:
    errors = []
    for name in SKILLS:
        source = root / "skills" / name / "SKILL.md"
        target = root / ".github/skills" / name / "SKILL.md"
        if not source.is_file():
            errors.append(f"Missing canonical skill: {name}")
            continue
        if check:
            if not target.is_file() or source.read_bytes() != target.read_bytes():
                errors.append(f"Copilot skill drift: {name}; run python scripts/sync_copilot.py")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = synchronize(check=args.check)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Seven Copilot skill copies match canonical sources." if args.check else "Generated seven Copilot skill copies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
