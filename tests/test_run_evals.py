from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.run_evals import (
    PUBLIC_SKILLS,
    build_report,
    calculate_verdict,
    check_plugin_installed,
    parse_judge_response,
    parse_judge_verdict,
    parse_transcript,
    write_reports,
)

TRANSCRIPT = "\n".join(
    [
        json.dumps(
            {
                "type": "system",
                "subtype": "init",
                "slash_commands": [f"silo-legal:{skill}" for skill in PUBLIC_SKILLS],
            }
        ),
        json.dumps(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {"skill": "silo-legal:novo-caso"},
                        }
                    ]
                },
            }
        ),
        json.dumps(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Read",
                            "input": {"file_path": "/algum/caminho.md"},
                        }
                    ]
                },
            }
        ),
        json.dumps(
            {
                "type": "result",
                "result": "texto final da execução...",
                "total_cost_usd": 0.1234,
                "num_turns": 5,
            }
        ),
    ]
)


class RunEvalsTest(unittest.TestCase):
    def test_parse_transcript_extracts_eval_signals(self) -> None:
        parsed = parse_transcript(TRANSCRIPT)

        self.assertEqual(parsed["invoked_skills"], ["silo-legal:novo-caso"])
        self.assertEqual(parsed["read_files"], ["/algum/caminho.md"])
        self.assertEqual(parsed["final_text"], "texto final da execução...")
        self.assertEqual(parsed["cost_usd"], 0.1234)
        self.assertEqual(parsed["num_turns"], 5)
        self.assertEqual(
            parsed["available_skills"],
            [f"silo-legal:{skill}" for skill in PUBLIC_SKILLS],
        )

    def test_parse_judge_verdict_handles_json_and_surrounding_text(self) -> None:
        verdict = '{"invariantes": [{"n": 1, "atendido": true, "evidencia": "trecho"}]}'

        self.assertEqual(
            parse_judge_verdict(verdict),
            [{"n": 1, "atendido": True, "evidencia": "trecho"}],
        )
        self.assertEqual(
            parse_judge_verdict(f"Explicação.\n```json\n{verdict}\n```\nFim."),
            [{"n": 1, "atendido": True, "evidencia": "trecho"}],
        )
        self.assertIsNone(parse_judge_verdict("sem JSON válido"))

    def test_parse_judge_response_accepts_envelope_and_event_array(self) -> None:
        verdict = '{"invariantes": [{"n": 1, "atendido": true, "evidencia": "trecho"}]}'
        expected = [{"n": 1, "atendido": True, "evidencia": "trecho"}]
        envelope = json.dumps({"type": "result", "result": verdict})
        array = "⚠ aviso do CLI antes do JSON\n" + json.dumps(
            [
                {"type": "system", "subtype": "init"},
                {"type": "result", "result": verdict, "total_cost_usd": 0.01},
            ]
        )

        self.assertEqual(parse_judge_response(envelope), expected)
        self.assertEqual(parse_judge_response(array), expected)
        self.assertIsNone(parse_judge_response("sem JSON"))

    def test_routing_error_always_fails(self) -> None:
        invariants = [
            {"n": 1, "atendido": True, "evidencia": "primeiro"},
            {"n": 2, "atendido": True, "evidencia": "segundo"},
        ]

        self.assertEqual(calculate_verdict(False, invariants, 2), "FAIL")

    def test_write_reports_creates_valid_json_and_markdown(self) -> None:
        scenarios = [
            {
                "id": "passou",
                "expected_skill": "novo-caso",
                "first_skill": "silo-legal:novo-caso",
                "invoked_skills": ["silo-legal:novo-caso"],
                "routing_ok": True,
                "invariants": [
                    {"n": 1, "invariant": "Atende.", "atendido": True, "evidencia": "sim"}
                ],
                "verdict": "PASS",
                "cost_usd": 0.1,
                "num_turns": 1,
                "read_files": [],
            },
            {
                "id": "falhou",
                "expected_skill": "analise-documental",
                "first_skill": None,
                "invoked_skills": [],
                "routing_ok": False,
                "invariants": [
                    {"n": 1, "invariant": "Não atende.", "atendido": False, "evidencia": "não"}
                ],
                "verdict": "FAIL",
                "cost_usd": 0.2,
                "num_turns": 2,
                "read_files": [],
            },
        ]
        fixture_scenarios = [
            {"expected_skill": "novo-caso"},
            {"expected_skill": "analise-documental"},
        ]
        report = build_report(
            "2026-08-24", "sonnet", "0.2.3", scenarios, fixture_scenarios
        )

        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary) / "evals"
            write_reports(output_dir, report)
            data = json.loads((output_dir / "report.json").read_text(encoding="utf-8"))
            markdown = (output_dir / "report.md").read_text(encoding="utf-8")

        self.assertIn("scenarios", data)
        self.assertEqual(data["counts"], {"total": 2, "PASS": 1, "FAIL": 1, "JUDGE_ERROR": 0})
        self.assertIn("passou", markdown)
        self.assertIn("falhou", markdown)
        self.assertIn("PASS", markdown)
        self.assertIn("FAIL", markdown)

    def test_plugin_check_accepts_injected_executor(self) -> None:
        def executor(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
            self.assertEqual(command, ["claude", "plugin", "list"])
            return subprocess.CompletedProcess(command, 0, stdout="silo-legal\n", stderr="")

        self.assertTrue(check_plugin_installed(executor))


if __name__ == "__main__":
    unittest.main()
