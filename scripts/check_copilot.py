"""Validate Copilot file metadata and canonical skill references."""

from pathlib import Path
import yaml

from sync_copilot import ROOT, SKILLS, synchronize

PROMPTS = dict(zip(("scope", "architecture", "experience", "decompose", "plan", "create", "review"), SKILLS))


def metadata(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or len(text.split("---", 2)) < 3:
        raise ValueError(f"Missing frontmatter: {path.name}")
    result = yaml.safe_load(text.split("---", 2)[1])
    if not isinstance(result, dict):
        raise ValueError(f"Frontmatter must be a mapping: {path.name}")
    return result


def check_copilot(root: Path = ROOT) -> list[str]:
    errors = synchronize(root, check=True)
    if not (root / ".github/copilot-instructions.md").is_file():
        errors.append("Missing repository Copilot instructions")
    for short, skill in PROMPTS.items():
        path = root / ".github/prompts" / f"{short}.prompt.md"
        try:
            header = metadata(path)
            if header.get("agent") != "agent" or not header.get("description") or not header.get("argument-hint"):
                raise ValueError(f"Prompt needs agent, description and argument-hint: {path.name}")
            if header.get("name") != f"memis-{short}":
                raise ValueError(f"Unexpected command name: {path.name}")
            target = f"../../skills/{skill}/SKILL.md"
            if f"]({target})" not in path.read_text(encoding="utf-8"):
                raise ValueError(f"Prompt must link its canonical skill: {path.name}")
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(str(exc))
    for name in ("infrastructure", "documentation", "artifacts"):
        path = root / ".github/instructions" / f"{name}.instructions.md"
        try:
            header = metadata(path)
            if not isinstance(header.get("applyTo"), str) or not header["applyTo"].strip():
                raise ValueError(f"Missing applyTo: {path.name}")
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(str(exc))
    return errors


if __name__ == "__main__":
    errors = check_copilot()
    print("\n".join(errors) if errors else "Copilot static checks passed: seven skills, seven prompts, and three scoped instruction files.")
    raise SystemExit(bool(errors))
