from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts import validate_skills

ROOT = Path(__file__).resolve().parents[1]
OS_JUNK = (".DS_Store", "Thumbs.db", "desktop.ini", "ehthumbs.db")
COPY_IGNORE = shutil.ignore_patterns(
    ".git", ".ruff_cache", "dist", "__pycache__", ".venv", *OS_JUNK, "._*"
)


def run_script(tree: Path, script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(tree / "scripts" / script)],
        capture_output=True,
        text=True,
        check=False,
    )


class OsJunkToleranceTest(unittest.TestCase):
    """Arquivos de sistema operacional não podem quebrar validação nem vazar em bundles."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.tree = Path(cls._tmp.name) / "repo"
        shutil.copytree(ROOT, cls.tree, ignore=COPY_IGNORE)
        for junk in (
            cls.tree / ".DS_Store",
            cls.tree / "skills" / "novo-caso" / ".DS_Store",
            cls.tree / "skills" / "redacao-contencioso" / "._SKILL.md",
            cls.tree / "references" / "legislacao" / "cpc" / "Thumbs.db",
            cls.tree / "references" / "desktop.ini",
        ):
            junk.write_bytes(b"junk")

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_validate_ignores_os_junk_anywhere(self) -> None:
        result = run_script(self.tree, "validate_skills.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)

    def test_validate_still_rejects_unknown_root_entries(self) -> None:
        unknown = self.tree / "arquivo-estranho.txt"
        unknown.write_text("nao pertence à distribuição", encoding="utf-8")
        try:
            result = run_script(self.tree, "validate_skills.py")
        finally:
            unknown.unlink()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("arquivo-estranho.txt", result.stdout)

    def test_bundles_exclude_os_junk(self) -> None:
        result = run_script(self.tree, "build_chatgpt_smoke_bundle.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = self.tree / "dist" / "chatgpt-work-smoke"
        archives = sorted(output.glob("*.zip"))
        self.assertEqual(len(archives), 7)
        for archive in archives:
            with zipfile.ZipFile(archive) as bundle:
                for member in bundle.namelist():
                    name = member.rsplit("/", 1)[-1]
                    self.assertNotIn(name, OS_JUNK, f"{archive.name}: {member}")
                    self.assertFalse(
                        name.startswith("._"), f"{archive.name}: {member}"
                    )

    def test_redaction_bundle_includes_tutela_module_and_cpc(self) -> None:
        result = run_script(self.tree, "build_chatgpt_smoke_bundle.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        archive = self.tree / "dist" / "chatgpt-work-smoke" / "redacao-contencioso.zip"
        with zipfile.ZipFile(archive) as bundle:
            members = set(bundle.namelist())
        self.assertIn(
            "redacao-contencioso/references/modulos/tutela-urgencia-evidencia.md",
            members,
        )
        self.assertIn(
            "redacao-contencioso/references/legislacao/cpc/procedimento-comum.md",
            members,
        )


class WorkflowFixtureValidationTest(unittest.TestCase):
    def workflow_errors(self, changes: dict[str, object]) -> list[str]:
        data = json.loads(
            (ROOT / "tests" / "fixtures" / "workflows.json").read_text(encoding="utf-8")
        )
        scenario = data["scenarios"][0]
        scenario.update(changes)
        with tempfile.TemporaryDirectory() as temporary:
            tree = Path(temporary)
            path = tree / "tests" / "fixtures" / "workflows.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(data), encoding="utf-8")
            with patch.object(validate_skills, "ROOT", tree):
                return validate_skills.check_workflow_fixtures()

    def test_accepts_multi_turn_prompt_and_valid_authorizing_turn(self) -> None:
        for authorizing_turn in (None, 2):
            with self.subTest(authorizing_turn=authorizing_turn):
                self.assertEqual(
                    self.workflow_errors(
                        {
                            "prompt": ["primeiro turno", "segundo turno"],
                            "authorizing_turn": authorizing_turn,
                        }
                    ),
                    [],
                )

    def test_rejects_single_item_and_empty_multi_turn_prompts(self) -> None:
        one_item = self.workflow_errors({"prompt": ["apenas um turno"]})
        empty_item = self.workflow_errors({"prompt": ["primeiro", " "]})

        self.assertTrue(any("texto simples" in error for error in one_item), one_item)
        self.assertTrue(
            any("lista de textos não vazios" in error for error in empty_item),
            empty_item,
        )

    def test_rejects_out_of_range_and_boolean_authorizing_turn(self) -> None:
        prompt = ["primeiro turno", "segundo turno"]
        for authorizing_turn in (0, 3, True):
            with self.subTest(authorizing_turn=authorizing_turn):
                errors = self.workflow_errors(
                    {"prompt": prompt, "authorizing_turn": authorizing_turn}
                )
                self.assertTrue(
                    any(
                        "pre-contencioso-incompleto" in error
                        and "authorizing_turn" in error
                        for error in errors
                    ),
                    errors,
                )


if __name__ == "__main__":
    unittest.main()
