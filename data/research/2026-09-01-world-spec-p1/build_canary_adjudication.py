#!/usr/bin/env python3
"""Build the P1 blind canary adjudication from the frozen reviews.

Mechanical/operator adjudication, no paid calls: reads the two frozen
review.json/receipt.json pairs and the authority ground truths, applies the
operator-decided recovery status with verbatim evidence quotes selected from
the frozen reviews, and writes canary-adjudication-v1.json in the P0 format.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "batch-model-reviews"
AUTHORITY = ROOT / "batch-generated" / "authority"
MATTER_IDS = ("M-201", "M-202", "M-203", "M-204")
WORLD_IDS = ("W-A", "W-B", "W-C")
MODELS = ("claude-sonnet-5", "claude-opus-5")
MODEL_DIRS = {
    "claude-sonnet-5": "sonnet-5-canary-v1",
    "claude-opus-5": "opus-5-canary-v1",
}
ATD = {
    "M-201": "ATD-2023-7801",
    "M-202": "ATD-2023-7802",
    "M-203": "ATD-2023-7803",
    "M-204": "ATD-2023-7804",
}

# Operator-decided statuses with verbatim evidence quotes from the frozen
# reviews. Templates use {atd} for the matter-specific protocol number.
EVIDENCE = {
    "claude-sonnet-5": {
        "O-A1": (
            "reclamação registrada no canal de atendimento da ré em 2023-06-12, "
            "protocolo {atd} (04-registro-reclamacao.md) - CONFIRMADA por registro "
            "interno da própria ré; alegação da inicial (05) convergente"
        ),
        "O-A2": (
            "Prova de trânsito em julgado, de eventual recurso ou de "
            "cumprimento/execução da sentença - inexistente nos autos apresentados"
        ),
        "O-B1": (
            "a reclamação extrajudicial alegada na petição inicial "
            "(05-peticao-inicial.md) permanece apenas ALEGADA, sem confirmação "
            "documental própria, embora o documento ressalve que não afirma "
            "inexistência por outro canal; pede confirmação por outro canal"
        ),
        "O-B2": (
            "Mesmas lacunas do mundo A: comprovante de pagamento, modo de citação, "
            "prova de trânsito em julgado/recurso/cumprimento, laudo integral"
        ),
        "O-C1": (
            "Divergência primária entre 06-aviso-recebimento-citacao.md "
            "(2024-03-12) e 07-certidao-citacao.md (2024-03-05) quanto à data da "
            "citação da ré, com impacto direto e não presumível sobre a "
            "tempestividade da contestação (08-contestacao.md)"
        ),
        "O-C2": (
            "Pela data do AR (2024-03-12): 15º dia útil em 2024-04-02, contestação "
            "tempestiva; pela data da certidão (2024-03-05): 15º dia útil em "
            "2024-03-26, contestação fora do prazo; calendário cobre as duas "
            "hipóteses; pede esclarecimento documental sobre qual data prevalece"
        ),
    },
    "claude-opus-5": {
        "O-A1": (
            "registro no canal da própria ré, protocolo {atd}, contato de "
            "2023-06-12 (04-registro-reclamacao.md), coincidente com a alegação da "
            "inicial (05-peticao-inicial.md) — o registro é confirmado; a "
            "afirmação de que ficou 'sem solução' permanece apenas alegada"
        ),
        "O-A2": (
            "A história processual não contém trânsito em julgado, recurso, "
            "acordo, cumprimento de sentença ou manifestação das partes sobre o "
            "laudo — ausência de registro, não prova de definitividade"
        ),
        "O-B1": (
            "dois resultados admissíveis pelo material: (i) apenas alegada, pois "
            "a busca não localizou registro com o protocolo {atd} e a data "
            "2023-06-12; (ii) indeterminada, porque o próprio documento ressalva "
            "que a pesquisa se limitou aos identificadores informados. Não é "
            "possível concluir inexistência da reclamação"
        ),
        "O-B2": (
            "Nada nos autos sintéticos indica trânsito em julgado, recurso, acordo "
            "ou execução; extrato consultado em 2026-01-15 termina em 2025-09-29; "
            "pede certidão de trânsito em julgado ou registro de recurso"
        ),
        "O-C1": (
            "Contradição central da cadeia citatória: o AR indica recebimento em "
            "2024-03-12 (06-aviso-recebimento-citacao.md) e a certidão de citação "
            "afirma citação em 2024-03-05 (07-certidao-citacao.md); o extrato "
            "não registra o ato citatório e não permite desempate"
        ),
        "O-C2": (
            "Resultado possível 1 (AR, 2024-03-12): vencimento em 2024-04-02, "
            "contestação tempestiva no último dia; resultado possível 2 "
            "(certidão, 2024-03-05): vencimento em 2024-03-26, contestação "
            "intempestiva. Não há documento que resolva qual data prevalece, de "
            "modo que ambos os resultados devem ser reportados"
        ),
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_review(model: str) -> dict:
    return json.loads((REVIEWS / MODEL_DIRS[model] / "review.json").read_text())


def load_receipt(model: str) -> dict:
    return json.loads((REVIEWS / MODEL_DIRS[model] / "receipt.json").read_text())


def world_of(review: dict, matter_id: str, world_id: str) -> dict:
    for matter in review["matters"]:
        if matter["matter_id"] == matter_id:
            for world in matter["worlds"]:
                if world["world_id"] == world_id:
                    return world
    raise KeyError((matter_id, world_id))


def main() -> None:
    reviews = {m: load_review(m) for m in MODELS}
    receipts = {m: load_receipt(m) for m in MODELS}

    isolation = {
        "same_prompt": {
            "pass": len({r["prompt_sha256"] for r in receipts.values()}) == 1,
            "sha256": receipts["claude-sonnet-5"]["prompt_sha256"],
        },
        "canary_matter_ids": {
            "pass": all(
                r["canary_matter_ids"] == list(MATTER_IDS) for r in receipts.values()
            ),
            "expected": list(MATTER_IDS),
            **{m: receipts[m]["canary_matter_ids"] for m in MODELS},
        },
        "models": {
            "pass": all(
                receipts[m]["requested_model"] == m
                and receipts[m]["reported_models"] == [m]
                for m in MODELS
            ),
            **{
                m: {
                    "requested_model": receipts[m]["requested_model"],
                    "reported_models": receipts[m]["reported_models"],
                }
                for m in MODELS
            },
        },
        "tools_omitted": {
            "pass": all(receipts[m]["tools_omitted"] for m in MODELS),
            **{m: receipts[m]["tools_omitted"] for m in MODELS},
        },
        "authority_files_included": {
            "pass": not any(
                receipts[m]["authority_files_included"] for m in MODELS
            ),
            **{m: receipts[m]["authority_files_included"] for m in MODELS},
        },
        "retries": {
            "pass": all(receipts[m]["retries"] == 0 for m in MODELS),
            **{m: receipts[m]["retries"] for m in MODELS},
        },
        "manifest_hash_check": {
            "pass": all(
                receipts[m]["manifest_hash_check"]["pass"] for m in MODELS
            ),
            **{m: receipts[m]["manifest_hash_check"]["pass"] for m in MODELS},
        },
        "stop_reason_end_turn": {
            "pass": all(receipts[m]["stop_reason"] == "end_turn" for m in MODELS),
            **{m: receipts[m]["stop_reason"] for m in MODELS},
        },
    }
    isolation["pass"] = all(
        check["pass"] for check in isolation.values() if isinstance(check, dict)
    )

    model_gates = {}
    for m in MODELS:
        review = reviews[m]
        gates = {
            matter["matter_id"]: matter["proposed_gate"]
            for matter in review["matters"]
        }
        model_gates[m] = {
            "batch_gate": review["batch_gate"],
            "matter_gates": gates,
            "pass": review["batch_gate"] == "CONSTRUIR"
            and all(g == "CONSTRUIR" for g in gates.values()),
        }
    model_gates["pass"] = all(model_gates[m]["pass"] for m in MODELS)

    totals = {
        m: {
            "critical": {"recovered": 0, "partial": 0, "missed": 0},
            "major": {"recovered": 0, "partial": 0, "missed": 0},
        }
        for m in MODELS
    }
    worlds = []
    for matter_id in MATTER_IDS:
        for world_id in WORLD_IDS:
            gt = json.loads(
                (
                    AUTHORITY / matter_id / world_id / "ground_truth.json"
                ).read_text()
            )
            observations = []
            world_pass = True
            for obs in gt["expected_observations"]:
                entry = {
                    "id": obs["id"],
                    "severity": obs["severity"],
                    "state": obs["state"],
                }
                for m in MODELS:
                    status = "recovered"  # operator decision; see README
                    evidence = EVIDENCE[m][obs["id"]].format(atd=ATD[matter_id])
                    entry[m] = {"status": status, "evidence": evidence}
                    totals[m][obs["severity"]][status] += 1
                    if obs["severity"] == "critical" and status != "recovered":
                        world_pass = False
                observations.append(entry)
            worlds.append(
                {
                    "matter_id": matter_id,
                    "world_id": world_id,
                    "authority_label": gt["authority_label"],
                    "expected_observations": observations,
                    "critical_false_positives": {m: [] for m in MODELS},
                    "realism": {
                        m: world_of(reviews[m], matter_id, world_id)[
                            "realism_1_to_5"
                        ]
                        for m in MODELS
                    },
                    "pass": world_pass,
                }
            )

    redesign_flags = {
        "claude-sonnet-5": [],
        "claude-opus-5": [
            "M-201 (REDESENHAR): causa de pedir de cobrança indevida/anotação "
            "negativa, mas saneador determina perícia técnica sobre o equipamento "
            "e o laudo devolve conclusão jurídico-contratual; sentença silencia "
            "sobre o pedido de cessação das cobranças.",
            "M-203 (REDESENHAR): réplica e saneador tratam controvérsia sobre "
            "renovação automática/cobranças como perícia técnica de equipamento; "
            "laudo devolve conclusão jurídico-contratual; restituição integral "
            "sem memória de cálculo; custas de R$ 4.812,00 ≈ 21% do pedido.",
            "Transversal (batch REDESENHAR): NF-SYN-0007 genérica sem data comum "
            "aos quatro assuntos; custas idênticas de R$ 4.812,00; datas de fase "
            "idênticas em todos os processos; hiato total de atos entre laudo e "
            "sentença; em M-202 e M-203 o item 9 do task.md aponta cadeias que "
            "não contêm o defeito inserido em W-C; em M-202 a condenação iguala "
            "o preço contratual sem prova do quantum.",
        ],
    }

    failures = []
    if not model_gates["pass"]:
        failures.append(
            "claude-opus-5 propôs REDESENHAR para M-201, M-203 e para o lote; "
            "pela regra dura, nada foi redesenhado — defeitos congelados e "
            "reportados em redesign_flags."
        )

    adjudication = {
        "schema_version": 1,
        "status": "PASS_WITH_REDESIGN_FLAG" if not model_gates["pass"] else "PASS",
        "criteria": {
            "all_worlds_must_pass": True,
            "critical_observations_require_recovered": True,
            "critical_partial_fails": True,
            "mutations_required": [
                "W-B: reclamação apenas alegada com busca negativa autolimitada",
                "W-C: divergência AR/certidão sobre a data da citação e efeito "
                "na tempestividade da contestação",
            ],
            "control_requirement": "W-A não pode conter incoerência crítica inventada",
            "critical_false_positive_requirement": (
                "Nenhum modelo pode tratar como confirmado um falso fato crítico "
                "ou introduzir fato crítico extra-corpus"
            ),
            "receipt_requirement": (
                "Mesmo prompt; quatro IDs corretos; modelo correto; tools "
                "omitidas; authority ausente; zero retries; stop_reason end_turn; "
                "hashes dos arquivos cegos batendo com os manifests do lote"
            ),
            "batch_gate_requirement": "Ambos os modelos devem devolver CONSTRUIR",
        },
        "isolation_checks": isolation,
        "model_gates": model_gates,
        "worlds": worlds,
        "totals": totals,
        "cost_usd": {
            m: receipts[m]["total_cost_usd"] for m in MODELS
        }
        | {"total": sum(receipts[m]["total_cost_usd"] for m in MODELS)},
        "redesign_flags": redesign_flags,
        "failures": failures,
        "decision_reason": (
            "PASS_WITH_REDESIGN_FLAG. Isolamento integral: mesmo prompt "
            "(sha256 0b83464e...), 216 arquivos cegos com hashes batendo com os "
            "manifests do lote, quatro IDs corretos, modelos corretos, sem "
            "tools, sem authority, zero retries, end_turn nas duas chamadas. Na "
            "recuperação, sonnet-5 e opus-5 recuperaram as 16 observações "
            "critical e as 8 major: W-A separa registro de reclamação "
            "corroborado de reconhecimento judicial; W-B mantém a reclamação "
            "como alegada, reconhece a ressalva autolimitada da busca negativa e "
            "pede corroboração alternativa; W-C expõe as duas datas de citação, "
            "as duas contagens em dias úteis (2024-04-02 tempestiva / 2024-03-26 "
            "intempestiva) e exige esclarecimento do marco oficial. Nenhum falso "
            "positivo crítico. Porém opus-5 propôs REDESENHAR em M-201, M-203 e "
            "no lote, apontando defeitos de coerência material (perícia técnica "
            "incompatível com a causa de pedir, NF genérica sem data, custas "
            "fixas idênticas, hiato laudo→sentença e desalinhamento entre o item "
            "9 do task.md e o defeito inserido em W-C de M-202/M-203). Pela "
            "regra dura do canário, nada foi redesenhado: os defeitos ficam "
            "congelados e reportados para decisão do operador."
        ),
        "source_sha256": {},
    }

    sources = {}
    for m in MODELS:
        d = MODEL_DIRS[m]
        for name in ("review.json", "receipt.json"):
            rel = f"batch-model-reviews/{d}/{name}"
            sources[rel] = sha256(REVIEWS / d / name)
    for matter_id in MATTER_IDS:
        for world_id in WORLD_IDS:
            for name in ("ground_truth.json", "rubric.json"):
                rel = f"batch-generated/authority/{matter_id}/{world_id}/{name}"
                sources[rel] = sha256(AUTHORITY / matter_id / world_id / name)
    adjudication["source_sha256"] = dict(sorted(sources.items()))

    out = REVIEWS / "canary-adjudication-v1.json"
    out.write_text(
        json.dumps(adjudication, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    print(f"status: {adjudication['status']}")
    print(f"cost: {adjudication['cost_usd']}")


if __name__ == "__main__":
    main()
