from __future__ import annotations

import json
import re
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

    def test_redaction_bundle_includes_every_module_and_cpc_file(self) -> None:
        result = run_script(self.tree, "build_chatgpt_smoke_bundle.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        archive = self.tree / "dist" / "chatgpt-work-smoke" / "redacao-contencioso.zip"
        with zipfile.ZipFile(archive) as bundle:
            members = set(bundle.namelist())
        modules = {
            f"redacao-contencioso/references/modulos/{path.name}"
            for path in (
                self.tree / "skills" / "redacao-contencioso" / "references" / "modulos"
            ).glob("*.md")
        }
        cpc_files = {
            f"redacao-contencioso/references/legislacao/cpc/{path.name}"
            for path in (self.tree / "references" / "legislacao" / "cpc").iterdir()
            if path.is_file() and not validate_skills.is_os_junk(path.name)
        }
        self.assertLessEqual(modules | cpc_files, members)

    def test_redaction_index_covers_every_module(self) -> None:
        modules_root = (
            self.tree / "skills" / "redacao-contencioso" / "references" / "modulos"
        )
        expected = {path.name for path in modules_root.glob("*.md")}
        index = (
            self.tree
            / "skills"
            / "redacao-contencioso"
            / "references"
            / "indice-modulos.md"
        ).read_text(encoding="utf-8")
        linked = set(re.findall(r"\(modulos/([a-z0-9-]+\.md)\)", index))
        self.assertEqual(expected, linked)

    def test_redaction_index_exposes_prebriefing_controls(self) -> None:
        index = (
            self.tree
            / "skills"
            / "redacao-contencioso"
            / "references"
            / "indice-modulos.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(index.split())

        for marker in (
            "Controles de briefing antes da confirmação",
            "Agravo interno:",
            "risco de multa",
            "Jurisdição voluntária — interdição:",
            "intervenções institucionais obrigatórias",
            "Ministério Público",
        ):
            self.assertIn(marker, normalized)


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


class AdaptationFixtureValidationTest(unittest.TestCase):
    def adaptation_errors(self, mutator) -> list[str]:
        data = json.loads(
            (ROOT / "tests" / "fixtures" / "adaptacao-casos-reais.json").read_text(
                encoding="utf-8"
            )
        )
        mutator(data)
        with tempfile.TemporaryDirectory() as temporary:
            tree = Path(temporary)
            fixture = tree / "tests" / "fixtures" / "adaptacao-casos-reais.json"
            fixture.parent.mkdir(parents=True)
            fixture.write_text(json.dumps(data), encoding="utf-8")
            modules = tree / "skills" / "redacao-contencioso" / "references" / "modulos"
            modules.mkdir(parents=True)
            referenced = {
                front["act"]["module"]
                for scenario in data["scenarios"]
                for front in scenario.get("fronts", [])
                if isinstance(front.get("act", {}).get("module"), str)
            }
            referenced.add("tutela-urgencia-evidencia")
            for module in referenced:
                (modules / f"{module}.md").write_text(f"# {module}\n", encoding="utf-8")
            with patch.object(validate_skills, "ROOT", tree):
                return validate_skills.check_adaptation_fixtures()

    def consumer_errors(self, relative: str, marker: str) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary:
            tree = Path(temporary)
            for source_relative in validate_skills.ADAPTATION_CONSUMER_REQUIREMENTS:
                source = ROOT / source_relative
                target = tree / source_relative
                target.parent.mkdir(parents=True, exist_ok=True)
                text = source.read_text(encoding="utf-8")
                if source_relative == relative:
                    pattern = r"\s+".join(re.escape(part) for part in marker.split())
                    text = re.sub(pattern, "", text, count=1)
                target.write_text(text, encoding="utf-8")
            with patch.object(validate_skills, "ROOT", tree):
                return validate_skills.check_adaptation_consumers()

    def adaptation_workflow_errors(self, mutator) -> list[str]:
        workflows = json.loads(
            (ROOT / "tests" / "fixtures" / "adaptacao-workflows.json").read_text(
                encoding="utf-8"
            )
        )
        mutator(workflows)
        with tempfile.TemporaryDirectory() as temporary:
            tree = Path(temporary)
            fixture_root = tree / "tests" / "fixtures"
            fixture_root.mkdir(parents=True)
            (fixture_root / "adaptacao-workflows.json").write_text(
                json.dumps(workflows), encoding="utf-8"
            )
            shutil.copy(
                ROOT / "tests" / "fixtures" / "adaptacao-casos-reais.json",
                fixture_root / "adaptacao-casos-reais.json",
            )
            with patch.object(validate_skills, "ROOT", tree):
                return validate_skills.check_adaptation_workflow_fixtures()

    def test_contract_fixtures_are_valid(self) -> None:
        self.assertEqual(validate_skills.check_adaptation_fixtures(), [])

    def test_consumer_contracts_are_valid(self) -> None:
        self.assertEqual(validate_skills.check_adaptation_consumers(), [])

    def test_adaptation_workflows_are_valid(self) -> None:
        self.assertEqual(validate_skills.check_adaptation_workflow_fixtures(), [])

    def test_adaptation_workflows_enforce_coverage_and_canary(self) -> None:
        def missing_case(data) -> None:
            data["scenarios"].pop()

        def wrong_canary(data) -> None:
            data["scenarios"][4]["canary"] = True

        def missing_redaction_gate(data) -> None:
            data["scenarios"][0].pop("authorizing_turn")

        cases = (
            (missing_case, "cobrir A01–A14 exatamente uma vez"),
            (wrong_canary, "canário comportamental deve conter exatamente A01–A04"),
            (missing_redaction_gate, "authorizing_turn null"),
        )
        for mutator, expected in cases:
            with self.subTest(expected=expected):
                errors = self.adaptation_workflow_errors(mutator)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_adaptation_workflows_reject_malformed_values_without_crashing(self) -> None:
        def malformed(data) -> None:
            scenario = data["scenarios"][0]
            scenario["adaptation_case_id"] = {}
            scenario["expected_skill"] = {}
            scenario["package_facts"] = []

        errors = self.adaptation_workflow_errors(malformed)
        for expected in (
            "adaptation_case_id inválido",
            "consumidor inválido",
            "package_facts insuficientes",
        ):
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_adaptation_workflows_enforce_explicit_fact_bindings(self) -> None:
        def missing_binding(data) -> None:
            facts = data["scenarios"][0]["package_facts"]
            facts[0].pop("finding_id")

        def duplicate_binding(data) -> None:
            facts = data["scenarios"][0]["package_facts"]
            facts[1]["finding_id"] = facts[0]["finding_id"]

        def unknown_binding(data) -> None:
            data["scenarios"][0]["package_facts"][0]["finding_id"] = "F99"

        def unknown_front(data) -> None:
            data["scenarios"][0]["package_facts"][0]["front_id"] = "front-99"

        cases = (
            (missing_binding, "bindings de achados incompletos"),
            (duplicate_binding, "finding_id repetido"),
            (unknown_binding, "finding_id inválido"),
            (unknown_front, "front_id inválido"),
        )
        for mutator, expected in cases:
            with self.subTest(expected=expected):
                errors = self.adaptation_workflow_errors(mutator)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_consumer_contract_markers_are_enforced(self) -> None:
        for relative, markers in validate_skills.ADAPTATION_CONSUMER_REQUIREMENTS.items():
            for marker in markers:
                with self.subTest(relative=relative, marker=marker):
                    errors = self.consumer_errors(relative, marker)
                    self.assertTrue(any(relative in error for error in errors), errors)

    def test_accepts_blocked_and_integral_modes(self) -> None:
        def blocked(data) -> None:
            scenario = data["scenarios"][0]
            scenario.update(
                {
                    "eligibility": "bloqueado",
                    "handoffs": [],
                    "analysis_eligible": False,
                    "fronts": [],
                    "findings": [],
                    "conflicts": [],
                }
            )

        def integral(data) -> None:
            scenario = data["scenarios"][0]
            scenario["eligibility"] = "integral"
            for front in scenario["fronts"]:
                front["coverage"] = "integral"

        for name, mutator in (("bloqueado", blocked), ("integral", integral)):
            with self.subTest(name=name):
                self.assertEqual(self.adaptation_errors(mutator), [])

    def test_rejects_missing_intake_and_scope_fallback(self) -> None:
        def missing_intake(data) -> None:
            data["scenarios"][0]["handoffs"] = ["analise_documental"]

        def unsupported_module(data) -> None:
            data["scenarios"][0]["fronts"][0]["scope_status"] = "nao_suportado"

        cases = (
            (missing_intake, "pacote utilizável exige intake"),
            (unsupported_module, "não pode selecionar módulo"),
        )
        for mutator, expected in cases:
            with self.subTest(expected=expected):
                errors = self.adaptation_errors(mutator)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_rejects_front_level_routing_bypasses(self) -> None:
        def indeterminate_front(data) -> None:
            data["scenarios"][0]["fronts"][0]["status"] = "indeterminada"

        def blocked_coverage(data) -> None:
            data["scenarios"][0]["fronts"][0]["coverage"] = "bloqueada"

        def unnamed_condition(data) -> None:
            data["scenarios"][0]["fronts"][0]["dependencies"] = []

        def missing_scope_state(data) -> None:
            data["scenarios"][3]["fronts"][2]["scope_status"] = "suportado"

        cases = (
            (indeterminate_front, "frente indeterminada não pode selecionar módulo"),
            (blocked_coverage, "cobertura bloqueada não pode selecionar módulo"),
            (unnamed_condition, "escopo condicionado exige dependência nomeada"),
            (missing_scope_state, "devem cobrir os quatro estados de escopo"),
        )
        for mutator, expected in cases:
            with self.subTest(expected=expected):
                errors = self.adaptation_errors(mutator)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_rejects_non_text_lists_without_crashing(self) -> None:
        def malformed_handoffs(data) -> None:
            data["scenarios"][0]["handoffs"] = [{}]

        def malformed_complements(data) -> None:
            data["scenarios"][0]["fronts"][0]["act"]["complements"] = [{}]

        cases = (
            (malformed_handoffs, "handoffs inválidos ou duplicados"),
            (malformed_complements, "complements aceita somente tutela sem duplicata"),
        )
        for mutator, expected in cases:
            with self.subTest(expected=expected):
                errors = self.adaptation_errors(mutator)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_rejects_non_text_choices_without_crashing(self) -> None:
        def malformed_choices(data) -> None:
            scenario = data["scenarios"][0]
            scenario["eligibility"] = {}
            front = scenario["fronts"][0]
            front["scope_status"] = {}
            for field in ("nature", "relation", "status", "coverage"):
                front[field] = {}
            front["act"].update({"status": {}, "module": {}})
            front["deadline"]["status"] = {}
            scenario["findings"][0]["state"] = {}
            scenario["conflicts"][0].update({"delta": {}, "status": {}})

        errors = self.adaptation_errors(malformed_choices)
        for expected in (
            "eligibility inválida",
            "scope_status inválido",
            "nature inválida",
            "módulo inexistente",
            "deadline inválido",
            "state inválido",
            "delta inválido",
        ):
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_rejects_state_promotion_and_undecided_act(self) -> None:
        def confirmed_without_scope(data) -> None:
            data["scenarios"][0]["findings"][0].pop("confirmation_scope")

        def decided_without_receipt(data) -> None:
            data["scenarios"][0]["fronts"][0]["act"]["status"] = "decidido"

        cases = (
            (confirmed_without_scope, "confirmado exige confirmation_scope"),
            (decided_without_receipt, "ato decidido exige recibo de decisão"),
        )
        for mutator, expected in cases:
            with self.subTest(expected=expected):
                errors = self.adaptation_errors(mutator)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_rejects_false_conflict_resolution_and_missing_scenario(self) -> None:
        def false_resolution(data) -> None:
            conflict = data["scenarios"][0]["conflicts"][0]
            conflict["status"] = "resolvido"
            conflict["blocked_claims"] = []

        conflict_errors = self.adaptation_errors(false_resolution)
        self.assertTrue(
            any("conflito resolvido exige fonte controladora" in error for error in conflict_errors),
            conflict_errors,
        )

        def missing_scenario(data) -> None:
            data["scenarios"].pop()

        scenario_errors = self.adaptation_errors(missing_scenario)
        self.assertTrue(
            any("exatamente A01–A14" in error for error in scenario_errors),
            scenario_errors,
        )


if __name__ == "__main__":
    unittest.main()
