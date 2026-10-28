"""Validate artifact structure and handoffs. Never execute project commands."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

from jsonschema import Draft202012Validator, FormatChecker
import yaml

ROOT = Path(__file__).resolve().parents[1]


class ContractError(ValueError):
    """An input violates a documented file contract."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject repeated YAML labels instead of silently keeping the last one."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, str):
            raise ContractError("YAML mapping keys must be text.")
        if key in result:
            raise ContractError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_yaml(path: Path):
    try:
        # Dates and versions must be quoted in artifacts so YAML keeps them as text.
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        return data
    except (OSError, yaml.YAMLError, RecursionError) as exc:
        raise ContractError(f"Cannot read {path}: {exc}") from exc


def check_schema(data, name: str):
    schema = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data),
        key=lambda error: str(list(error.absolute_path)),
    )
    if errors:
        error = errors[0]
        location = ".".join(map(str, error.absolute_path)) or "root"
        raise ContractError(f"{name} at {location}: {error.message}")


def require(condition: bool, message: str):
    if not condition:
        raise ContractError(message)


def unique(values, label: str):
    require(len(values) == len(set(values)), f"Duplicate {label}.")


def project_path(project: Path, value: str) -> Path:
    """Artifact paths are portable, relative, and contained in the project."""
    raw = PurePosixPath(value)
    require(
        bool(value.strip()) and not raw.is_absolute() and ".." not in raw.parts
        and "\\" not in value and ":" not in value and str(raw) != ".",
        f"Unsafe project-relative path: {value}",
    )
    path = (project / value).resolve()
    require(path.is_relative_to(project.resolve()), f"Path escapes project: {value}")
    return path


def source_snapshot(deliverable: dict) -> dict:
    return {key: deliverable[key] for key in ("title", "deliverable_description", "acceptance_criteria")}


def plan_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_plan(plan: dict, deliverable: dict, project: Path):
    check_schema(plan, "plan")
    identifier = deliverable["id"]
    require(plan["deliverable_id"] == identifier, "Plan deliverable_id does not match its folder.")
    require(plan["source_deliverable"] == source_snapshot(deliverable),
            "Stale plan: source_deliverable differs from the current deliverable. Replan first.")
    tasks = plan["tasks"]
    unique([task["id"] for task in tasks], "task IDs")
    criteria = {item["id"] for item in deliverable["acceptance_criteria"]}
    covered, earlier = set(), set()
    for task in tasks:
        require(task["id"].startswith(identifier + "-T"), "Task IDs must start with the deliverable ID and -T.")
        dependencies = task["dependencies"]
        unique(dependencies, "task dependencies")
        require(set(dependencies) <= earlier, f"Unknown, self, or forward dependency in {task['id']}.")
        refs = task["acceptance_criteria_refs"]
        unique(refs, "task acceptance criterion references")
        require(set(refs) <= criteria, f"Unknown acceptance criterion in {task['id']}.")
        covered.update(refs)
        for artifact in task["artifacts_affected"]:
            project_path(project, artifact["path"])
        earlier.add(task["id"])
    require(covered == criteria, f"Plan leaves acceptance criteria uncovered: {sorted(criteria - covered)}")


def validate_review(review: dict, deliverable: dict, plan: dict, plan_path: Path):
    check_schema(review, "review")
    require(review["deliverable_id"] == deliverable["id"], "Review deliverable_id does not match its folder.")
    require(review["plan_digest"] == plan_digest(plan_path), "Stale review: plan_digest does not match plan.yaml.")
    criteria = {item["id"] for item in deliverable["acceptance_criteria"]}
    assessments = review["ac_assessment"]
    unique([item["ac_id"] for item in assessments], "review acceptance criterion assessments")
    require({item["ac_id"] for item in assessments} == criteria, "Review must assess every AC exactly once.")
    for issue in review["issues"]:
        require(issue["ac_ref"] in criteria | {"general"}, "Issue references an unknown acceptance criterion.")
    for assessment in assessments:
        if assessment["status"] == "satisfied":
            require(all(item["result"] == "passed" for item in assessment["evidence"]),
                    "Satisfied AC requires passed evidence; failed/not-run checks cannot count as satisfied.")
    if review["verdict"] == "passed":
        require(all(item["status"] == "satisfied" for item in assessments), "Passed review has unsatisfied ACs.")
        require(not plan["open_questions"], "Passed review cannot have unresolved plan questions.")
        require(not any(item["severity"] in {"blocker", "major"} for item in review["issues"]),
                "Passed review cannot contain blocker or major issues.")
    require(deliverable["review_status"] == review["verdict"], "Review status is out of sync with deliverables.yaml.")
    require(deliverable["review_notes"] == review["summary"], "Review notes are out of sync with the review summary.")


def validate_project(project: Path, complete: bool = False) -> list[str]:
    project = project.resolve()
    config = read_yaml(project / "project.yaml")
    check_schema(config, "project")
    for name in ("scope.md", "architecture.md", "experience.md"):
        require((project / "docs" / name).is_file(), f"Missing prerequisite docs/{name}.")
    deliverables_path = project / "deliverables.yaml"
    require(deliverables_path.is_file(), "Missing deliverables.yaml. Run decompose-to-deliverables first.")
    data = read_yaml(deliverables_path)
    check_schema(data, "deliverables")
    project_path(project, data["workstream"]["source_scope"])
    require(project_path(project, data["workstream"]["source_scope"]).is_file(), "source_scope file does not exist.")
    deliverables = data["deliverables"]
    unique([item["id"] for item in deliverables], "deliverable IDs")
    unique([ac["id"] for item in deliverables for ac in item["acceptance_criteria"]], "acceptance criterion IDs")
    ids = {item["id"] for item in deliverables}
    deliveries = project / "deliveries"
    if deliveries.exists():
        for folder in deliveries.iterdir():
            if folder.is_dir():
                require(folder.name in ids, f"Orphan delivery folder: {folder.name}")
    messages = []
    for item in deliverables:
        identifier = item["id"]
        require(all(ac["id"].startswith(identifier + "-AC") for ac in item["acceptance_criteria"]),
                f"AC IDs must start with {identifier}-AC.")
        folder = project_path(project, f"deliveries/{identifier}")
        plan_path = folder / "plan.yaml"
        review_path = folder / "review.yaml"
        require(not review_path.exists() or plan_path.exists(), f"{identifier}: review requires a plan.")
        if not plan_path.exists():
            require(not complete, f"{identifier}: missing plan.yaml in complete mode.")
            require(item["review_status"] == "pending" and item["review_notes"] == "",
                    f"{identifier}: unreviewed work must be pending with empty notes.")
            messages.append(f"{identifier}: deliverable valid; not planned yet")
            continue
        plan = read_yaml(plan_path)
        validate_plan(plan, item, project)
        if review_path.exists():
            review = read_yaml(review_path)
            validate_review(review, item, plan, plan_path)
            require((folder / "implementation-summary.md").is_file(), f"{identifier}: reviewed work requires an implementation summary.")
            # A reviewed task's declared outputs must exist even if the verdict requests changes.
            for task in plan["tasks"]:
                for artifact in task["artifacts_affected"]:
                    require(project_path(project, artifact["path"]).is_file(),
                            f"{identifier}: missing reviewed artifact {artifact['path']}.")
            if complete:
                require(review["verdict"] == "passed", f"{identifier}: complete mode requires a passed review.")
            messages.append(f"{identifier}: structure and handoffs valid; recorded review {review['verdict']}")
        else:
            require(not complete, f"{identifier}: missing review.yaml in complete mode.")
            require(item["review_status"] == "pending" and item["review_notes"] == "",
                    f"{identifier}: unreviewed work must be pending with empty notes.")
            messages.append(f"{identifier}: plan valid; not reviewed yet")
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--complete", action="store_true", help="Require a plan, summary, artifacts, and passed review for every deliverable")
    args = parser.parse_args()
    try:
        for message in validate_project(args.project, args.complete):
            print(message)
    except (ContractError, OSError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print("VALID: file contracts checked. Recorded evidence was not rerun by this validator.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
