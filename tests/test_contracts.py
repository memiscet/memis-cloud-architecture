"""Behavioral checks for damaged handoffs and unsupported completion claims."""

import copy
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from init_project import initialize
from validate import ContractError, plan_digest, read_yaml, validate_project
from check_example import check_guide

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.project = Path(self.scratch.name) / "example"
        shutil.copytree(ROOT / "examples/community-event", self.project)
        self.plan = self.project / "deliveries/GUIDE-001/plan.yaml"
        self.review = self.project / "deliveries/GUIDE-001/review.yaml"
        self.deliverables = self.project / "deliverables.yaml"

    def edit(self, path, change):
        data = read_yaml(path)
        change(data)
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def assert_invalid(self, message):
        with self.assertRaisesRegex(ContractError, message):
            validate_project(self.project)

    def test_completed_example(self):
        self.assertIn("recorded review passed", validate_project(self.project, complete=True)[0])

    def test_software_example_is_valid_but_incomplete(self):
        example = ROOT / "examples/software-request"
        self.assertIn("not reviewed yet", validate_project(example)[0])
        with self.assertRaisesRegex(ContractError, "missing review"):
            validate_project(example, complete=True)

    def test_missing_work_list_is_actionable(self):
        self.deliverables.unlink()
        self.assert_invalid("Run decompose-to-deliverables first")

    def test_unknown_ac_reference(self):
        self.edit(self.plan, lambda data: data["tasks"][0]["acceptance_criteria_refs"].append("GUIDE-001-AC99"))
        self.assert_invalid("Unknown acceptance criterion")

    def test_uncovered_criterion(self):
        self.edit(self.plan, lambda data: data["tasks"][0]["acceptance_criteria_refs"].pop())
        self.assert_invalid("uncovered")

    def test_forward_dependency(self):
        self.edit(self.plan, lambda data: data["tasks"][0]["dependencies"].append("GUIDE-001-T2"))
        self.assert_invalid("forward dependency")

    def test_self_dependency(self):
        self.edit(self.plan, lambda data: data["tasks"][0]["dependencies"].append("GUIDE-001-T1"))
        self.assert_invalid("self, or forward")

    def test_duplicate_task_ids(self):
        self.edit(self.plan, lambda data: data["tasks"].append(copy.deepcopy(data["tasks"][0])))
        self.assert_invalid("Duplicate task IDs")

    def test_changed_promise_invalidates_plan(self):
        self.edit(self.deliverables, lambda data: data["deliverables"][0]["acceptance_criteria"][0].update(then="A newly agreed outcome"))
        self.assert_invalid("Stale plan")

    def test_changed_plan_invalidates_review(self):
        self.edit(self.plan, lambda data: data["assumptions"].append("A newly recorded assumption"))
        self.assert_invalid("Stale review")

    def test_unsupported_pass_is_rejected(self):
        self.edit(self.review, lambda data: data["ac_assessment"][0].update(status="not_verified"))
        self.assert_invalid("unsatisfied ACs")

    def test_not_run_evidence_cannot_satisfy_a_criterion(self):
        self.edit(self.review, lambda data: data["ac_assessment"][0]["evidence"][0].update(result="not_run"))
        self.assert_invalid("Satisfied AC requires passed evidence")

    def test_empty_evidence_is_rejected(self):
        self.edit(self.review, lambda data: data["ac_assessment"][0].update(evidence=[]))
        self.assert_invalid("review at")

    def test_duplicate_assessment(self):
        self.edit(self.review, lambda data: data["ac_assessment"].append(copy.deepcopy(data["ac_assessment"][0])))
        self.assert_invalid("Duplicate review")

    def test_missing_assessment(self):
        self.edit(self.review, lambda data: data["ac_assessment"].pop())
        self.assert_invalid("every AC exactly once")

    def test_status_must_match_review(self):
        self.edit(self.deliverables, lambda data: data["deliverables"][0].update(review_status="pending"))
        self.assert_invalid("status is out of sync")

    def test_notes_must_match_review(self):
        self.edit(self.deliverables, lambda data: data["deliverables"][0].update(review_notes="Something different"))
        self.assert_invalid("notes are out of sync")

    def test_parent_path_escape(self):
        self.edit(self.plan, lambda data: data["tasks"][0]["artifacts_affected"][0].update(path="../outside.txt"))
        self.assert_invalid("Unsafe project-relative path")

    def test_symlink_path_escape(self):
        (self.project / "outside").symlink_to(self.project.parent, target_is_directory=True)
        self.edit(self.plan, lambda data: data["tasks"][0]["artifacts_affected"][0].update(path="outside/result.md"))
        self.assert_invalid("Path escapes project")

    def test_missing_result_file(self):
        (self.project / "artifacts/welcome-guide.md").unlink()
        self.assert_invalid("missing reviewed artifact")

    def test_major_issue_prevents_pass(self):
        self.edit(self.review, lambda data: data["issues"].append(dict(severity="major", category="correctness", description="A required outcome is broken", recommendation="Correct the outcome", ac_ref="GUIDE-001-AC1")))
        self.assert_invalid("major issues")

    def test_unresolved_questions_prevent_pass(self):
        self.edit(self.plan, lambda data: data["open_questions"].append("Who confirms the venue?"))
        self.edit(self.review, lambda data: data.update(plan_digest=plan_digest(self.plan)))
        self.assert_invalid("unresolved plan questions")

    def test_review_without_plan(self):
        self.plan.unlink()
        self.assert_invalid("review requires a plan")

    def test_orphan_delivery(self):
        (self.project / "deliveries/GUIDE-999").mkdir()
        self.assert_invalid("Orphan delivery folder")

    def test_repeated_yaml_keys(self):
        with self.deliverables.open("a", encoding="utf-8") as stream:
            stream.write('\nschema_version: "1.0"\n')
        self.assert_invalid("Duplicate YAML key")

    def test_invalid_review_date(self):
        self.edit(self.review, lambda data: data.update(reviewed_at="2026-02-31"))
        self.assert_invalid("review at reviewed_at")

    def test_nonpassing_review_can_be_valid(self):
        summary = "The content check still needs to run."
        def change(data):
            data.update(verdict="changes_requested", summary=summary)
            data["ac_assessment"][0]["status"] = "not_verified"
            data["ac_assessment"][0]["evidence"][0]["result"] = "not_run"
        self.edit(self.review, change)
        self.edit(self.deliverables, lambda data: data["deliverables"][0].update(review_status="changes_requested", review_notes=summary))
        self.assertIn("changes_requested", validate_project(self.project)[0])
        with self.assertRaisesRegex(ContractError, "complete mode requires a passed review"):
            validate_project(self.project, complete=True)

    def test_example_check_detects_lost_fallback(self):
        path = self.project / "artifacts/welcome-guide.md"
        path.write_text(path.read_text().replace("Do not guess", "Guess"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "AC2"):
            check_guide(path)


class InitializerTests(unittest.TestCase):
    def test_initialization_preserves_existing_work(self):
        with tempfile.TemporaryDirectory() as folder:
            project = initialize("test-project", "Test project", Path(folder))
            marker = project / "docs/scope.md"
            marker.write_text("Existing user work", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                initialize("test-project", "Replacement", Path(folder))
            self.assertEqual(marker.read_text(), "Existing user work")

    def test_slug_cannot_escape_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                initialize("../outside", "Invalid", Path(folder))
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_no_work_is_invented_at_initialization(self):
        with tempfile.TemporaryDirectory() as folder:
            project = initialize("new-project", "New project", Path(folder))
            self.assertTrue((project / "project.yaml").is_file())
            self.assertTrue((project / "docs/experience.md").is_file())
            with self.assertRaisesRegex(ContractError, "Run decompose-to-deliverables first"):
                validate_project(project)


if __name__ == "__main__":
    unittest.main()
