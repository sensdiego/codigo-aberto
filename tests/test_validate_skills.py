from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
