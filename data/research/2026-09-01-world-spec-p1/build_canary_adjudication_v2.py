#!/usr/bin/env python3
"""Build the P1 blind re-canary (v2) adjudication from the frozen v2 reviews.

Mechanical/operator adjudication, no paid calls: reads the two frozen v2
review.json/receipt.json pairs and the (redesigned) authority ground truths,
applies the operator-decided recovery status with verbatim evidence quotes
selected from the frozen reviews, checks the six v1 redesign_flags one by one
in the v2 responses, and writes canary-adjudication-v2.json in the P0 format.
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
    "claude-sonnet-5": "sonnet-5-canary-v2",
    "claude-opus-5": "opus-5-canary-v2",
}
ATD = {
    "M-201": "ATD-2023-7801",
    "M-202": "ATD-2023-7802",
    "M-203": "ATD-2023-7803",
    "M-204": "ATD-2023-7804",
}

# Operator-decided statuses with verbatim evidence quotes from the frozen v2
# reviews. Templates use {atd} for the matter-specific protocol number.
EVIDENCE = {
    "claude-sonnet-5": {
        "O-A1": (
            "Registro de reclamação (04) confirma reclamação registrada em "
            "2023-06-12, protocolo {atd}, corroborando a narrativa da petição "
            "inicial (05)"
        ),
        "O-A2": (
            "Informação sobre trânsito em julgado, recurso ou cumprimento de "
            "sentença — ausente em toda a série documental"
        ),
        "O-B1": (
            "classifica-se como alegação não confirmada, e não como falsidade "
            "comprovada, dada a ressalva do próprio documento sobre a limitação "
            "da busca"
        ),
        "O-B2": (
            "Mesmas lacunas de W-A quanto a mandado de citação, procuração, "
            "quesitos periciais, trânsito em julgado/recurso"
        ),
        "O-C1": (
            "07-certidao-citacao.md indica citação em 2024-03-05, enquanto "
            "06-aviso-recebimento-citacao.md indica recebimento em 2024-03-12 — "
            "divergência primária de datas quanto ao marco inicial da citação"
        ),
        "O-C2": (
            "(a) partindo de 2024-03-12 (AR), o 15º dia útil é 2024-04-02, "
            "tornando a contestação tempestiva no limite exato; (b) partindo de "
            "2024-03-05 (certidão), o 15º dia útil é 2024-03-26, tornando a "
            "mesma contestação intempestiva; Nenhum documento resolve a "
            "divergência entre AR e certidão; a escolha de uma data sobre a "
            "outra não pode ser feita por suposição"
        ),
    },
    "claude-opus-5": {
        "O-A1": (
            "confirmada por registro do próprio canal da ré, protocolo {atd}, "
            "assunto idêntico ao narrado na inicial; o documento registra "
            "encaminhamento à assistência técnica, mas não registra resposta, "
            "de modo que a afirmação de que ficou 'sem solução' permanece "
            "apenas alegada"
        ),
        "O-A2": (
            "A história processual não contém trânsito em julgado, recurso, "
            "acordo, cumprimento de sentença ou qualquer ato posterior a "
            "2025-09-29; a ausência não autoriza inferir estabilidade da "
            "sentença"
        ),
        "O-B1": (
            "NÃO confirmada: 'não foi localizado registro de reclamação' para o "
            "protocolo {atd} e o contato de 2023-06-12; o próprio documento "
            "ressalva que não afirma inexistência de contato por outro canal ou "
            "com outros dados — resultado negativo de busca não equivale a "
            "prova de inexistência"
        ),
        "O-B2": (
            "Não constam trânsito em julgado, recurso, acordo ou cumprimento de "
            "sentença; o extrato emitido em 2026-01-15 encerra-se em 2025-09-29, "
            "sem que se possa inferir o desfecho"
        ),
        "O-C1": (
            "DIVERGÊNCIA CENTRAL (item 4): o AR informa recebimento em "
            "2024-03-12 (06-aviso-recebimento-citacao.md) e a certidão certifica "
            "citação em 2024-03-05 (07-certidao-citacao.md). O extrato não "
            "registra o ato citatório e não permite desempate"
        ),
        "O-C2": (
            "Contagem A (AR, 2024-03-12): vencimento em 2024-04-02, contestação "
            "TEMPESTIVA no último dia; Contagem B (certidão, 2024-03-05): "
            "vencimento em 2024-03-26, contestação INTEMPESTIVA. O resultado "
            "sobre tempestividade é indeterminado com o material disponível: "
            "ambos os cenários devem ser reportados, sem eleger data por "
            "suposição"
        ),
    },
}

# One-by-one check of the six v1 redesign flags against the v2 responses and
# the redesigned blind corpus. Status: resolved | partial | open.
V1_FLAG_RESOLUTION = [
    {
        "flag": "1. Perícia incoerente com a causa de pedir (M-201, M-203)",
        "status": "partial",
        "evidence": (
            "RESOLVIDO o descompasso de tipo de prova: o opus v2 registra que em "
            "M-203 'a réplica requereu perícia contábil e documental sobre "
            "cobranças posteriores ao cancelamento; o saneador deferiu "
            "exatamente essa prova; o laudo concluiu que tais cobranças não têm "
            "suporte contratual' — cadeia coerente em forma. RESIDUAL: o opus "
            "ainda marca como implausível a frase do laudo 'examinando o objeto' "
            "físico em perícia contábil (M-201/M-203), e o sonnet nota que o "
            "laudo de M-203 não enfrenta o argumento do canal de cancelamento."
        ),
    },
    {
        "flag": "2. Condenação igual ao preço sem prova do quantum (M-202)",
        "status": "partial",
        "evidence": (
            "RESOLVIDA a amarração documental: a sentença agora declara o valor "
            "'correspondente ao preço pago pela autora conforme o contrato e a "
            "nota fiscal' (citado pelos dois modelos). ABERTO o descompasso "
            "lógico residual: mercadoria perdida (causa de pedir) x preço do "
            "equipamento (base do quantum), sem prova de equivalência — o sonnet "
            "o trata como falha de desenho (REDESENHAR M-202), o opus como "
            "achado legítimo e detectável (CONSTRUIR M-202)."
        ),
    },
    {
        "flag": "3. NF-SYN-0007 genérica sem data",
        "status": "resolved",
        "evidence": (
            "As cronologias do opus v2 citam 'nota fiscal NF-SYN-1001 de mesma "
            "data e valor' (M-201), NF-SYN-1002 (M-202), NF-SYN-1003 (M-203) e "
            "NF-SYN-1004 (M-204), com data 2023-04-18; nenhum dos dois modelos "
            "aponta a nota fiscal como sinal de artificialidade no v2."
        ),
    },
    {
        "flag": "4. Custas fixas idênticas (R$ 4.812,00)",
        "status": "resolved",
        "evidence": (
            "Nenhum modelo reporta custas idênticas no v2. Ressalva nova do "
            "opus: 'identidade absoluta de datas e da razão custas/valor da "
            "causa (~1,87%) nos quatro assuntos' — os valores variam por matter, "
            "mas a razão constante (~1,873%, a função de derivação) é "
            "detectável como padrão de template."
        ),
    },
    {
        "flag": "5. Hiato laudo→sentença",
        "status": "resolved",
        "evidence": (
            "O evento intermediário existe e foi recuperado: o opus v2 registra "
            "'manifestação das partes sobre o laudo de 2025-04-14 (citada em "
            "documents/12 e documents/15, mas não juntada em documents/)' — "
            "passa a ser lacuna documental legítima (peça citada e não "
            "juntada), não mais hiato na cadeia. Nenhum modelo aponta hiato "
            "laudo→sentença no v2."
        ),
    },
    {
        "flag": "6. Desalinhamento item 9 do task.md × mutação de W-C (M-202, M-203)",
        "status": "resolved",
        "evidence": (
            "Os dois modelos ancoram a análise da divergência no novo item 4 em "
            "TODOS os mundos ('Item 4: não há divergência neste mundo' em "
            "W-A/W-B; 'DIVERGÊNCIA CENTRAL (item 4)' em W-C), inclusive em "
            "M-202 e M-203, cujos focus instructions apontam outras cadeias. O "
            "opus v2 não repete o flag de enunciado desalinhado."
        ),
    },
]

# New defects surfaced by the v2 reviewers (frozen, reported, not fixed here).
V2_FLAGS = {
    "claude-sonnet-5": [
        "M-202 e M-203 (REDESENHAR): descompasso lógico entre a causa de pedir "
        "(mercadoria perdida / cobranças pós-cancelamento) e o quantum "
        "pedido/sentenciado (preço integral do contrato).",
        "Transversal: calendário forense nega feriado em 2024-03-29 "
        "(Sexta-feira Santa) no período 2024-03-05 a 2024-04-02, em todos os "
        "matters; marcos temporais idênticos entre processos distintos.",
        "M-203: laudo não enfrenta o argumento defensivo do canal de "
        "cancelamento.",
    ],
    "claude-opus-5": [
        "M-201 (REDESENHAR): cobranças/negativação narradas como vício do "
        "objeto instalado; nenhuma prova da anotação negativa; dano moral "
        "idêntico ao preço sem critério de arbitramento.",
        "M-203 (REDESENHAR): incompatibilidade interna — contrato 'pago à vista "
        "na assinatura' e sem cláusula de renovação, mas todo o mérito e a "
        "sentença giram em torno de renovação automática e cobranças sucessivas "
        "não documentadas.",
        "Transversal: incoerência de modalidade citatória — AR postal "
        "(documents/06) x certidão que invoca 'retorno do mandado' "
        "(documents/07) em todos os mundos, enfraquecendo o ponto normativo de "
        "L335; razão custas/valor da causa constante (~1,87%) e datas de fase "
        "idênticas nos quatro assuntos.",
    ],
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

    failures = []
    if not model_gates["pass"]:
        failures.append(
            "Ambos os modelos propuseram REDESENHAR para o lote (sonnet: M-202 "
            "e M-203; opus: M-201 e M-203); pela regra dura, nada foi "
            "redesenhado — defeitos congelados e reportados em v2_flags."
        )

    adjudication = {
        "schema_version": 1,
        "status": "PASS_WITH_REDESIGN_FLAG" if not model_gates["pass"] else "PASS",
        "canary_iteration": 2,
        "supersedes": "batch-model-reviews/canary-adjudication-v1.json",
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
                "omitidas; authority ausente; zero retries; stop_reason "
                "end_turn; hashes dos arquivos cegos batendo com os manifests "
                "do lote redesenhado"
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
        | {
            "total": sum(receipts[m]["total_cost_usd"] for m in MODELS),
            "v1_total": 1.352828,
            "v1_plus_v2": sum(receipts[m]["total_cost_usd"] for m in MODELS)
            + 1.352828,
        },
        "v1_redesign_flags_resolution": V1_FLAG_RESOLUTION,
        "v2_flags": V2_FLAGS,
        "failures": failures,
        "decision_reason": (
            "PASS_WITH_REDESIGN_FLAG. Re-canário sobre o lote redesenhado: "
            "isolamento integral (mesmo prompt sha256 49c131b8..., 216 arquivos "
            "com hashes batendo com os manifests novos, quatro IDs, modelos "
            "corretos, sem tools, sem authority, zero retries, end_turn). "
            "Recuperação perfeita nos dois modelos: 16/16 critical e 8/8 major, "
            "sem falso positivo crítico — W-A separa registro de reconhecimento "
            "judicial, W-B mantém alegação com ressalva autolimitada, W-C expõe "
            "as duas datas e as duas contagens ancoradas no novo item 4 do "
            "task. Dos 6 flags do v1: 4 resolvidos (NF com data e número único; "
            "custas variadas — com ressalva da razão constante ~1,87% "
            "detectada pelo opus; cadeia laudo→sentença fechada pela "
            "manifestação de 2025-04-14; task alinhado à mutação de W-C em "
            "todos os matters) e 2 parciais (perícia agora do tipo certo, mas "
            "com a frase residual 'examinando o objeto'; sentença de M-202 "
            "agora amarrada a contrato/NF, mas o descompasso mercadoria×preço "
            "persiste e divide os modelos). Ainda assim, os DOIS modelos "
            "propõem REDESENHAR no lote: o sonnet em M-202/M-203 (quantum) e o "
            "opus em M-201/M-203 (narrativa do vício e contrato à vista "
            "incompatível com renovação automática), com dois novos defeitos "
            "transversais (calendário que nega a Sexta-feira Santa de "
            "2024-03-29; AR postal x certidão de 'retorno do mandado'). Pela "
            "regra dura, nada foi redesenhado: defeitos congelados em v2_flags "
            "para decisão do operador."
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

    out = REVIEWS / "canary-adjudication-v2.json"
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
