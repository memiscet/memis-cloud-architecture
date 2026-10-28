"""Check integration failures that matter when reusing this workspace."""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_copilot import check_copilot
from sync_copilot import synchronize
from verify_workspace import check_network


class NetworkAllocationTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.path = Path(self.scratch.name) / "network.yaml"
        shutil.copyfile(ROOT / "projects/memis-cloud/network.yaml", self.path)

    def change(self, action):
        data = yaml.safe_load(self.path.read_text())
        action(data)
        self.path.write_text(yaml.safe_dump(data))

    def test_baseline_allocation(self):
        check_network(self.path)

    def test_overlapping_subnets_are_rejected(self):
        self.change(lambda data: data["subnets"]["b"].update(private_cidr=data["subnets"]["a"]["private_cidr"]))
        with self.assertRaisesRegex(ValueError, "overlap"):
            check_network(self.path)

    def test_subnet_outside_vpc_is_rejected(self):
        self.change(lambda data: data["subnets"]["c"].update(private_cidr="10.65.0.0/24"))
        with self.assertRaisesRegex(ValueError, "inside the VPC"):
            check_network(self.path)

    def test_missing_zone_is_rejected(self):
        self.change(lambda data: data["subnets"].pop("c"))
        with self.assertRaisesRegex(ValueError, "keys a, b, c"):
            check_network(self.path)


class CopilotIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        for folder in ("skills", ".github"):
            shutil.copytree(ROOT / folder, self.root / folder)

    def test_complete_integration(self):
        self.assertEqual(check_copilot(self.root), [])

    def test_generated_copy_drift_is_rejected_without_repair(self):
        path = self.root / ".github/skills/create-scope/SKILL.md"
        path.write_text(path.read_text() + "\nAn unintended divergent instruction.\n")
        before = path.read_bytes()
        self.assertTrue(synchronize(self.root, check=True))
        self.assertEqual(path.read_bytes(), before)

    def test_canonical_edit_can_be_regenerated(self):
        path = self.root / "skills/create-scope/SKILL.md"
        path.write_text(path.read_text() + "\nA deliberate source revision.\n")
        self.assertTrue(synchronize(self.root, check=True))
        self.assertEqual(synchronize(self.root), [])
        self.assertEqual(synchronize(self.root, check=True), [])

    def test_missing_prompt_is_rejected(self):
        (self.root / ".github/prompts/plan.prompt.md").unlink()
        self.assertTrue(check_copilot(self.root))

    def test_wrong_skill_reference_is_rejected(self):
        path = self.root / ".github/prompts/review.prompt.md"
        path.write_text(path.read_text().replace("../../skills/review-deliverable/SKILL.md", "../../skills/create-scope/SKILL.md"))
        self.assertTrue(any("canonical skill" in item for item in check_copilot(self.root)))

    def test_unscoped_instructions_are_rejected(self):
        path = self.root / ".github/instructions/infrastructure.instructions.md"
        path.write_text('---\ndescription: "Scope removed"\n---\nExample\n')
        self.assertTrue(any("applyTo" in item for item in check_copilot(self.root)))


if __name__ == "__main__":
    unittest.main()
