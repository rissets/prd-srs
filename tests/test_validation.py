import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_skill.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class StructuralValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "prd-srs"
        self.skill.mkdir()
        for name in ["SKILL.md", "agents", "references"]:
            source = ROOT / name
            target = self.skill / name
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)

    def test_valid_skill(self):
        self.assertEqual(validator.check(self.skill)["status"], "pass")

    def test_missing_reference_rejected(self):
        (self.skill / "references/database-design.md").unlink()
        self.assertEqual(validator.check(self.skill)["status"], "fail")

    def test_missing_invocation_rejected(self):
        path = self.skill / "agents/openai.yaml"
        path.write_text(path.read_text(encoding="utf-8").replace("$prd-srs", "the skill"), encoding="utf-8")
        self.assertEqual(validator.check(self.skill)["status"], "fail")

    def test_unclosed_fence_rejected(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n```mermaid\nflowchart LR\n A --> B\n", encoding="utf-8")
        self.assertEqual(validator.check(self.skill)["status"], "fail")

    def test_release_version_consistent(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
        self.assertEqual(yaml.safe_load(content)["metadata"]["version"], (ROOT / "VERSION").read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    unittest.main()
