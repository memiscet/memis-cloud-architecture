"""Check the fictional welcome guide's three narrow content promises."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def check_guide(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    sections = {}
    current = None
    for line in content.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current:
            sections[current].append(line)
    sections = {name: "\n".join(lines).lower() for name, lines in sections.items()}
    arrival = sections.get("Arrival", "")
    missing = sections.get("Missing details", "")
    changes = sections.get("Room changes", "")
    results = []
    checks = [
        ("GUIDE-001-AC1", all(part in arrival for part in ("riverside community hall", "main entrance", "welcome desk"))),
        ("GUIDE-001-AC2", all(part in missing for part in ("confirmation", "ask the welcome desk", "do not guess"))),
        ("GUIDE-001-AC3", all(part in changes for part in ("printed", "ask the welcome desk", "current directions"))
         and not re.search(r"https?://|\]\(", content)),
    ]
    for identifier, passed in checks:
        if not passed:
            raise ValueError(f"{identifier}: sample guide content check failed")
        results.append(f"{identifier}: passed sample document content check")
    return results


def main() -> int:
    try:
        for result in check_guide(ROOT / "examples/community-event/artifacts/welcome-guide.md"):
            print(result)
    except (OSError, ValueError) as exc:
        print(f"FAILED: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
