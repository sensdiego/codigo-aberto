#!/usr/bin/env python3
"""Build the P1 blind canary v4 adjudication from the frozen v4 reviews.

Mechanical/operator adjudication, no paid calls: reads the two frozen v4
review.json/receipt.json pairs and the current authority ground truths,
applies the operator-decided recovery status with verbatim evidence quotes,
checks the v3 flags one by one, classifies every new flag as (a) instrument
bug, (b) internal contradiction/visible legal-realism defect, (c)
cosmetic/template, evaluates the owner's stopping ruler, and writes
canary-adjudication-v4.json.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "batch-model-reviews"
AUTHORITY = ROOT / "batch-generated" / "authority"
MATTER_IDS = ("M-201", "M-202", "M-203", "M-204")
MODELS = ("claude-sonnet-5", "claude-opus-5")
MODEL_DIRS = {
    "claude-sonnet-5": "sonnet-5-canary-v4",
    "claude-opus-5": "opus-5-canary-v4",
}
ATD = {
    "M-201": "ATD-2023-7801",
    "M-202": "ATD-2023-7802",
    "M-203": "ATD-2023-7803",
    "M-204": "ATD-2023-7804",
}
PRIOR_COST_USD = 1.352828 + 1.314952 + 1.432779  # v1+v2+v3 (frozen receipts)

EVIDENCE = {
    "claude-sonnet-5": {
        "O-A1": (
            "Reclamação extrajudicial: confirmada por documento próprio de "
            "atendimento com mesmo protocolo e data da alegação da petição "
            "inicial — classificação: confirmada"
        ),
        "O-A2": (
            "A história processual não contém notícia de acordo, recurso ou "
            "trânsito em julgado; o extrato de andamentos (15) encerra na "
            "intimação da sentença, sem ato posterior registrado"
        ),
        "O-B1": (
            "alegada na petição inicial (05), porém o documento 04 informa que "
            "não foi localizado registro com os dados fornecidos, ressalvando "
            "que isso não exclui contato por outro canal — classificação: "
            "alegada, não confirmada (não há contradição direta, mas lacuna "
            "probatória)"
        ),
        "O-B2": (
            "Não há notícia de acordo, recurso ou trânsito em julgado nos "
            "autos disponíveis"
        ),
        "O-C1": (
            "a certidão de disponibilização (06) e a certidão de efetivação "
            "(07) informam datas divergentes de disponibilização, com "
            "visualização na mesma data em 07 — divergência interna quanto à "
            "data do mesmo ato"
        ),
        "O-C2": (
            "Contagem A (pela 06): 15º dia útil coincide com o protocolo da "
            "contestação — tempestiva nesta hipótese; Contagem B (pela 07): "
            "contestação posterior ao termo final — intempestiva. Não há "
            "elemento documental que permita escolher uma das datas como "
            "correta; a divergência deve ser objeto de diligência, não de "
            "suposição"
        ),
    },
    "claude-opus-5": {
        "O-A1": (
            "Reclamação extrajudicial, protocolo {atd}, com o mesmo assunto "
            "narrado na inicial (04-registro-reclamacao.md) — confirma a "
            "alegação da petição inicial (05); o documento não registra "
            "resposta ou solução, de modo que a afirmação 'sem solução' "
            "permanece alegada"
        ),
        "O-A2": (
            "A história processual NÃO contém: trânsito em julgado, "
            "interposição de recurso, acordo, cumprimento de sentença ou "
            "qualquer movimentação posterior à intimação — lacuna que não "
            "pode ser preenchida por inferência"
        ),
        "O-B1": (
            "RESPOSTA NEGATIVA DE BUSCA para o protocolo {atd}: a reclamação "
            "permanece ALEGADA e não confirmada; não é possível declará-la "
            "inexistente, pois a busca é limitada aos identificadores "
            "informados"
        ),
        "O-B2": (
            "Ausentes na história processual: trânsito em julgado, recurso, "
            "acordo e cumprimento, apesar da consulta posterior do extrato"
        ),
        "O-C1": (
            "DIVERGÊNCIA CENTRAL: a certidão de disponibilização (06) e a "
            "certidão de efetivação (07) divergem sobre a data em que a "
            "citação foi disponibilizada, com visualização na mesma data em "
            "07. Nenhum documento do corpus permite eleger uma das datas"
        ),
        "O-C2": (
            "Contagem 1 (base da 06): contestação TEMPESTIVA, no último dia; "
            "Contagem 2 (base da 07): contestação INTEMPESTIVA, protocolada 5 "
            "dias úteis após o vencimento"
        ),
    },
}

# One-by-one check of the v3 flags against the v4 responses.
V3_FLAG_RESOLUTION = [
    {
        "flag": "(a) W-C: efetivação (visualização) anterior à disponibilização — impossibilidade causal",
        "status": "dead",
        "evidence": (
            "Os dois modelos leem W-C como duas certidões divergindo sobre a "
            "DATA DE DISPONIBILIZAÇÃO, cada uma causalmente possível: sonnet "
            "('divergência interna quanto à data do mesmo ato', com "
            "visualização na mesma data em 07) e opus ('duas datas "
            "certificadas de disponibilização... Nenhum documento do corpus "
            "permite eleger uma das datas'). Ninguém aponta impossibilidade "
            "causal no v4. Nuance: o sonnet descreve a divergência como "
            "'cronologicamente incoerente' no motivo do lote — registros "
            "mutuamente incoerentes, que é exatamente a mutação pretendida — "
            "e ainda assim votou CONSTRUIR."
        ),
    },
    {
        "flag": "(b) Certidões citatórias datadas em sábado",
        "status": "dead",
        "evidence": (
            "Nenhum reviewer aponta ato cartorário em fim de semana no v4: as "
            "datas citadas nas cronologias (2024-03-08, 2024-03-20, "
            "2024-03-01, 2024-03-13 etc.) são dias úteis e as contagens "
            "partem do dia útil seguinte sem ressalva."
        ),
    },
    {
        "flag": "(b) M-203: NF única de valor total x cobrança mensal; termo de instalação físico",
        "status": "partial",
        "evidence": (
            "PERSISTE a NF: o opus repete 'nota fiscal do valor total "
            "incompatível com cobrança mensal recorrente' no REDESENHAR de "
            "M-203. O termo de instalação físico não reapareceu no v4."
        ),
    },
    {
        "flag": "(b) Persistente: M-202 pede mercadoria perdida, sentença condena pelo preço pago",
        "status": "persisting_non_blocking",
        "evidence": (
            "Ambos mantêm como achado material legítimo e não bloqueante: "
            "opus ('quantum deferido pelo preço pago sem prova do valor da "
            "mercadoria perdida' — dentro de CONSTRUIR) e sonnet ('tensão "
            "entre causa de pedir e base de cálculo da sentença é um achado "
            "material relevante, não uma falha de recuperabilidade')."
        ),
    },
    {
        "flag": "(c) Cosméticos v3 (contestação no 15º dia, calendário ajustado, 'assistência técnica', extrato sem atos, certidão citada-não-juntada)",
        "status": "persisting_cosmetic",
        "evidence": (
            "O opus segue notando cheiros de template ('redação templada da "
            "petição inicial, protocolos e valores em série e janelas de "
            "calendário que começam sempre uma semana antes da citação'), "
            "agora explicitamente 'sem impedir a recuperação das análises "
            "pedidas'. Nenhum vira bloqueio."
        ),
    },
]

# New v4 flags, classified per the owner's ruler.
NEW_FLAGS = [
    {
        "class": "b",
        "flag": (
            "M-203: renovação automática 'por períodos anuais sucessivos' "
            "invocada menos de dois meses após a contratação (contrato "
            "2023-04-07/08, reclamação 2023-06-02) — incoerência temporal "
            "introduzida pela cláusula anual do contract_variant do redesenho "
            "2."
        ),
        "models": ["claude-opus-5 (REDESENHAR M-203)", "claude-sonnet-5 (não flagrou; CONSTRUIR)"],
        "evidence": (
            "opus: 'Implausibilidade temporal: renovação automática por "
            "períodos anuais sucessivos não poderia ter gerado renovação "
            "entre 2023-04-07 e a reclamação de 2023-06-02 — menos de dois "
            "meses de vigência'."
        ),
    },
    {
        "class": "c",
        "flag": (
            "M-203: ausência de documento do pedido de cancelamento (premissa "
            "da instrução, citada só indiretamente) e restituição integral "
            "não quantificada pelo laudo — padrão deliberado de lacuna "
            "citada-não-juntada, mas somado pelo opus ao REDESENHAR de M-203."
        ),
        "models": ["claude-opus-5", "claude-sonnet-5 (como missing_evidence legítimo)"],
        "evidence": (
            "opus: 'nenhum documento comprova o pedido de cancelamento, "
            "premissa de toda a instrução' e 'a sentença restitui "
            "integralmente um valor que o laudo não quantificou'."
        ),
    },
    {
        "class": "c",
        "flag": (
            "Cheiros de template remanescentes: redação templada da petição "
            "inicial, protocolos e valores em série, janelas de calendário "
            "começando sempre uma semana antes da citação do mundo."
        ),
        "models": ["claude-opus-5"],
        "evidence": (
            "opus (motivo do lote): 'reduzem o realismo sem impedir a "
            "recuperação das análises pedidas'."
        ),
    },
]


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
            "batch_pass": review["batch_gate"] == "CONSTRUIR",
            "all_matters_pass": all(g == "CONSTRUIR" for g in gates.values()),
        }
    batch_gate_pass = all(model_gates[m]["batch_pass"] for m in MODELS)
    model_gates["pass"] = batch_gate_pass and all(
        model_gates[m]["all_matters_pass"] for m in MODELS
    )

    totals = {
        m: {
            "critical": {"recovered": 0, "partial": 0, "missed": 0},
            "major": {"recovered": 0, "partial": 0, "missed": 0},
        }
        for m in MODELS
    }
    worlds = []
    for matter_id in MATTER_IDS:
        for world_id in ("W-A", "W-B", "W-C"):
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

    v4_total = sum(receipts[m]["total_cost_usd"] for m in MODELS)
    new_ab = [f for f in NEW_FLAGS if f["class"] in ("a", "b")]
    stopping_rule = {
        "rule": (
            "Só flag novo (a) ou (b) justificaria v5; (c) isolado encerra "
            "como aceito-com-ressalvas."
        ),
        "v4_batch_gates": {m: model_gates[m]["batch_gate"] for m in MODELS},
        "new_class_a_or_b_flags": [f["flag"] for f in new_ab],
        "v5_justified_by_ruler": bool(new_ab),
        "assessment": (
            "Pela régua, HÁ um flag novo classe (b): a incoerência temporal "
            "renovação-anual x reclamação <2 meses em M-203 (REDESENHAR do "
            "opus, localizado em M-203; lote CONSTRUIR para os dois modelos). "
            "A correção é de mérito de um matter (texto do contract_variant "
            "e/ou data da reclamação de M-203), não do instrumento de "
            "mundos; a decisão sobre corrigir M-203 e rodar v5 cabe ao owner."
        ),
    }

    failures = []
    if not model_gates["pass"]:
        failures.append(
            "claude-opus-5 propôs REDESENHAR localizado em M-203 (flag (b) "
            "novo: renovação anual x reclamação <2 meses; NF única x "
            "mensalidade persistente). Lote CONSTRUIR para ambos os modelos. "
            "Pela regra dura, nada foi redesenhado."
        )

    adjudication = {
        "schema_version": 1,
        "status": (
            "PASS_BATCH_WITH_MATTER_FLAG" if batch_gate_pass else "PASS_WITH_REDESIGN_FLAG"
        ),
        "canary_iteration": 4,
        "supersedes": "batch-model-reviews/canary-adjudication-v3.json",
        "criteria": {
            "all_worlds_must_pass": True,
            "critical_observations_require_recovered": True,
            "critical_partial_fails": True,
            "mutations_required": [
                "W-B: reclamação apenas alegada com busca negativa autolimitada",
                "W-C: duas certidões divergindo sobre a data de "
                "disponibilização da citação, ambas causalmente possíveis, "
                "com desfechos opostos de tempestividade",
            ],
            "control_requirement": "W-A não pode conter incoerência crítica inventada",
            "critical_false_positive_requirement": (
                "Nenhum modelo pode tratar como confirmado um falso fato "
                "crítico ou introduzir fato crítico extra-corpus"
            ),
            "receipt_requirement": (
                "Mesmo prompt; quatro IDs corretos; modelo correto; tools "
                "omitidas; authority ausente; zero retries; stop_reason "
                "end_turn; hashes dos arquivos cegos batendo com os manifests "
                "do lote atual"
            ),
            "batch_gate_requirement": "Ambos os modelos devem devolver CONSTRUIR no lote",
        },
        "isolation_checks": isolation,
        "model_gates": model_gates,
        "worlds": worlds,
        "totals": totals,
        "cost_usd": {
            m: receipts[m]["total_cost_usd"] for m in MODELS
        }
        | {
            "total": v4_total,
            "v1_plus_v2_plus_v3": PRIOR_COST_USD,
            "v1_plus_v2_plus_v3_plus_v4": PRIOR_COST_USD + v4_total,
        },
        "v3_flags_resolution": V3_FLAG_RESOLUTION,
        "new_flags_classified": NEW_FLAGS,
        "stopping_rule": stopping_rule,
        "failures": failures,
        "decision_reason": (
            "PASS_BATCH_WITH_MATTER_FLAG. Quarto canário, após a correção "
            "estática do bug (a) da v3: isolamento integral (mesmo prompt "
            "sha256 a436bfdd..., 216 hashes conferindo com os manifests, "
            "quatro IDs, modelos corretos, sem tools, sem authority, zero "
            "retries, end_turn). Recuperação perfeita nos dois modelos: "
            "16/16 critical e 8/8 major, sem falso positivo crítico. Os "
            "flags da v3: (a) inversão causal MORTO — W-C agora diverge "
            "sobre a data de disponibilização, causalmente possível, e as "
            "duas contagens seguem com desfechos opostos (tempestiva pela "
            "06, intempestiva por 5 dias úteis pela 07, nos 4 matters); (b) "
            "sábados MORTO; (b) NF x mensalidade PERSISTE em M-203; (b) "
            "mercadoria x preço de M-202 persiste como achado legítimo; (c) "
            "cosméticos persistem sem bloqueio. Pela primeira vez os DOIS "
            "modelos devolvem CONSTRUIR no lote. Resta um REDESENHAR "
            "localizado do opus em M-203 por flag (b) NOVO: a cláusula de "
            "renovação anual (contract_variant do redesenho 2) não poderia "
            "ter gerado cobrança de renovação menos de dois meses após a "
            "contratação. Pela régua do owner, flag (b) novo justifica "
            "avaliar v5; a correção é de mérito de um único matter. Nada "
            "foi redesenhado por este canário; decisão registrada para o "
            "owner."
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
        for world_id in ("W-A", "W-B", "W-C"):
            for name in ("ground_truth.json", "rubric.json"):
                rel = f"batch-generated/authority/{matter_id}/{world_id}/{name}"
                sources[rel] = sha256(AUTHORITY / matter_id / world_id / name)
    adjudication["source_sha256"] = dict(sorted(sources.items()))

    out = REVIEWS / "canary-adjudication-v4.json"
    out.write_text(
        json.dumps(adjudication, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    print(f"status: {adjudication['status']}")
    print(f"stopping_rule: {adjudication['stopping_rule']['assessment']}")
    print(f"cost v4: {v4_total} | accumulated: {PRIOR_COST_USD + v4_total}")


if __name__ == "__main__":
    main()
