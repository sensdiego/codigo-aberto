from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "software-release.yml"


class ReleaseWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW.read_text(encoding="utf-8")
        cls.policy = tomllib.loads(
            (ROOT / ".release-policy.toml").read_text(encoding="utf-8")
        )

    def test_ignored_paths_are_strict_subset_of_non_release_policy(self) -> None:
        block = re.search(r"paths-ignore:\n((?:\s{6}- .+\n)+)", self.text)
        self.assertIsNotNone(block)
        ignored = {
            line.split("- ", 1)[1].strip().strip("\"'")
            for line in block.group(1).splitlines()
        }
        self.assertTrue(ignored < set(self.policy["paths"]["non_release"]))

    def test_release_uses_exact_anchor_and_never_moves_a_tag(self) -> None:
        self.assertIn('git tag -a "$tag" "$ANCHOR"', self.text)
        self.assertIn("Refusing conflicting immutable tag", self.text)
        self.assertNotIn("git tag -f", self.text)

    def test_generated_commit_is_proven_before_push(self) -> None:
        push = self.text.index("git push origin HEAD:main")
        for proof in (
            "scripts/validate_skills.py",
            "tests.test_release tests.test_release_workflow",
            "scripts/build_chatgpt_smoke_bundle.py",
        ):
            self.assertIn(proof, self.text)
            self.assertLess(self.text.index(proof), push)

    def test_release_does_not_install_or_run_the_product(self) -> None:
        executable = "\n".join(
            line for line in self.text.splitlines() if not line.lstrip().startswith("#")
        ).lower()
        for forbidden in ("deploy", "reindex", "railway", "alembic upgrade"):
            self.assertNotIn(forbidden, executable)

    def test_retries_are_bounded(self) -> None:
        self.assertIn("for delay in 0 2 8", self.text)
        self.assertIn("for delay in 1 4 16", self.text)

    def test_generated_release_commit_repairs_a_missing_tag(self) -> None:
        self.assertIn(
            'elif [[ "$subject" == "chore(release): v${version}" ]]', self.text
        )
        self.assertIn('anchor="$(git rev-parse HEAD)"', self.text)

    def test_generated_artifacts_stay_outside_public_tree(self) -> None:
        self.assertIn('plan_file="$RUNNER_TEMP/release-plan.json"', self.text)
        self.assertIn('notes_file="$RUNNER_TEMP/release-notes.md"', self.text)
        self.assertNotIn("> release-plan.json", self.text)
        self.assertNotIn("> release-notes.md", self.text)

    def test_release_publishes_chatgpt_bundles(self) -> None:
        self.assertIn("python3 scripts/build_chatgpt_smoke_bundle.py", self.text)
        self.assertIn('gh release upload "$tag"', self.text)
        self.assertIn("dist/chatgpt-work-smoke/*.zip", self.text)
        self.assertIn("dist/chatgpt-work-smoke/manifest.json", self.text)


if __name__ == "__main__":
    unittest.main()
