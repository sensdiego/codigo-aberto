from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.release import (
    ReleaseError,
    apply_plan,
    build_plan,
    classify_paths,
    create_fragment,
    load_fragments,
    load_policy,
    release_notes,
)


class ReleaseProtocolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".claude-plugin").mkdir()
        (self.root / ".changes").mkdir()
        (self.root / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": "silo-legal", "version": "0.2.0"}) + "\n",
            encoding="utf-8",
        )
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\nMudanças publicadas do plugin `silo-legal`.\n",
            encoding="utf-8",
        )
        (self.root / ".release-policy.toml").write_text(
            """schema = 1
adapter = "codigo-aberto-release-python-v1"
manifest = ".claude-plugin/plugin.json"
manifest_kind = "json"
package_name = "silo-legal"
changelog = "CHANGELOG.md"
fragments_dir = ".changes"
tag_prefix = "v"
current_version_source = "version"
[paths]
non_release = ["README.md"]
release = [".changes/*.json", ".claude-plugin/**", "skills/**"]
""",
            encoding="utf-8",
        )
        self._git("init", "-b", "main")
        self._git("config", "user.name", "Test")
        self._git("config", "user.email", "test@example.com")
        self._git(
            "add", ".release-policy.toml", ".claude-plugin/plugin.json", "CHANGELOG.md"
        )
        self._git("commit", "-m", "initial")
        self.policy = load_policy(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _git(self, *args: str) -> None:
        subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)

    def test_bootstrap_keeps_manifest_version_and_generates_changelog(self) -> None:
        create_fragment(
            self.policy,
            name="public-skills",
            kind="minor",
            category="Added",
            summary="Publica as skills.",
        )

        plan = build_plan(self.policy)
        self.assertTrue(plan.bootstrap)
        self.assertEqual(plan.next_version, "0.2.0")
        result = apply_plan(self.policy, plan, date(2026, 8, 21))

        self.assertTrue(result["publish"])
        self.assertEqual(load_fragments(self.policy), ())
        changelog = (self.root / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [0.2.0] - 2026-08-21", changelog)
        self.assertIn("### Added", changelog)
        self.assertIn("- Publica as skills.", changelog)
        self.assertIn("Publica as skills.", release_notes(self.policy, "0.2.0"))

    def test_patch_after_first_tag_bumps_manifest(self) -> None:
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [0.2.0] - 2026-08-21\n\n### Added\n\n- Base.\n",
            encoding="utf-8",
        )
        self._git("tag", "v0.2.0")
        create_fragment(
            self.policy,
            name="fix-link",
            kind="patch",
            category="Fixed",
            summary="Corrige um link.",
        )

        plan = build_plan(self.policy)
        self.assertFalse(plan.bootstrap)
        self.assertEqual(plan.next_version, "0.2.1")
        apply_plan(self.policy, plan, date(2026, 8, 22))

        manifest = json.loads(
            (self.root / ".claude-plugin" / "plugin.json").read_text()
        )
        self.assertEqual(manifest["version"], "0.2.1")

    def test_release_paths_win_and_ambiguous_paths_fail_closed(self) -> None:
        impact = classify_paths(
            self.policy,
            ["README.md", "skills/novo-caso/SKILL.md", "LICENSE"],
        )
        self.assertEqual(impact.non_release, ("README.md",))
        self.assertEqual(impact.release, ("skills/novo-caso/SKILL.md",))
        self.assertEqual(impact.ambiguous, ("LICENSE",))
        self.assertTrue(impact.requires_fragment)

    def test_major_fragment_requires_breaking_description(self) -> None:
        with self.assertRaises(ReleaseError):
            create_fragment(
                self.policy,
                name="breaking",
                kind="major",
                category="Changed",
                summary="Muda o contrato.",
            )

    def test_fragment_add_contract_can_infer_changelog_category(self) -> None:
        target = create_fragment(
            self.policy,
            name="automatic-category",
            kind="patch",
            category=None,
            summary="Corrige o contrato do adaptador.",
        )
        fragment = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(fragment["category"], "Fixed")


if __name__ == "__main__":
    unittest.main()
