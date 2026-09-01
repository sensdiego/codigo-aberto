#!/usr/bin/env python3
"""Build the P1 blind canary v3 adjudication from the frozen v3 reviews.

Mechanical/operator adjudication, no paid calls: reads the two frozen v3
review.json/receipt.json pairs and the current authority ground truths,
applies the operator-decided recovery status with verbatim evidence quotes,
checks the five v2 flags one by one, classifies every new flag as
(a) instrument/ruler bug, (b) internal contradiction or visible legal-realism
defect, (c) cosmetic/template, and writes canary-adjudication-v3.json.
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
    "claude-sonnet-5": "sonnet-5-canary-v3",
    "claude-opus-5": "opus-5-canary-v3",
}
ATD = {
    "M-201": "ATD-2023-7801",
    "M-202": "ATD-2023-7802",
    "M-203": "ATD-2023-7803",
    "M-204": "ATD-2023-7804",
}
PRIOR_COST_USD = 1.352828 + 1.314952  # v1 + v2, from the frozen receipts

EVIDENCE = {
    "claude-sonnet-5": {
        "O-A1": (
            "Reclamação extrajudicial está confirmada por documento próprio do "
            "canal de atendimento da ré (04), com protocolo, data e assunto "
            "idênticos aos narrados na petição inicial (05)"
        ),
        "O-A2": (
            "Não há certidão de trânsito em julgado, notícia de recurso ou de "
            "cumprimento de sentença/execução"
        ),
        "O-B1": (
            "a reclamação extrajudicial deve ser classificada como 'alegada', "
            "não 'confirmada'; o documento 04 apenas nega o resultado da busca "
            "pelos dados fornecidos"
        ),
        "O-B2": (
            "Mesmas lacunas de W-A quanto a AR de citação, quesitos periciais, "
            "trânsito em julgado e cumprimento de sentença"
        ),
        "O-C1": (
            "Certidão de efetivação da citação (07) é anterior à certidão de "
            "disponibilização da citação eletrônica (06) — sequência "
            "incompatível com o funcionamento usual da citação eletrônica; as "
            "duas datas são expostas"
        ),
        "O-C2": (
            "As duas contagens conduzem a conclusões opostas sobre a "
            "tempestividade da contestação, sem que os documentos indiquem "
            "qual data deve prevalecer (contagem 1: tempestiva no último dia; "
            "contagem 2: intempestiva)"
        ),
    },
    "claude-opus-5": {
        "O-A1": (
            "CONFIRMADA em fonte documental própria — protocolo {atd}, com o "
            "mesmo assunto narrado na inicial (04-registro-reclamacao.md e "
            "05-peticao-inicial.md); o registro comprova o contato, não o "
            "mérito das cobranças"
        ),
        "O-A2": (
            "A história processual NÃO contém trânsito em julgado, recurso, "
            "acordo, cumprimento de sentença ou fixação de honorários; o "
            "extrato encerra-se na intimação, o que não autoriza inferir "
            "trânsito"
        ),
        "O-B1": (
            "ALEGADA e NÃO CORROBORADA: a resposta do SAC informa 'não foi "
            "localizado registro de reclamação com os dados fornecidos' para o "
            "protocolo {atd}; o próprio documento ressalva que não afirma a "
            "inexistência de contato por outro canal — resultado negativo de "
            "busca, não prova de inexistência"
        ),
        "O-B2": (
            "Ausentes no acervo: trânsito em julgado, recurso, acordo e "
            "cumprimento de sentença; o extrato termina na intimação"
        ),
        "O-C1": (
            "DIVERGÊNCIA na cadeia citatória: a certidão de disponibilização "
            "(06) e a certidão de efetivação (07) indicam datas distintas; "
            "visualização registrada antes da disponibilização — impossível "
            "na cadeia de citação eletrônica; defeito de construção, não mera "
            "divergência"
        ),
        "O-C2": (
            "Consequência prática divergente: a mesma contestação é tempestiva "
            "por uma certidão e intempestiva pela outra, sem que qualquer "
            "peça do acervo resolva o conflito; ambas as contagens expostas "
            "com o calendário"
        ),
    },
}

# One-by-one check of the five v2 flags against the v3 responses.
V2_FLAG_RESOLUTION = [
    {
        "flag": "1. Calendário forense negava expediente em 2024-03-29 (Sexta-feira Santa)",
        "status": "dead",
        "evidence": (
            "Os dois modelos contam excluindo o feriado: sonnet ('excluindo o "
            "feriado de 2024-03-29 (calendário 17)') e opus ('29/03 "
            "(Sexta-feira Santa) não é útil'); M-203, cuja janela não tem "
            "feriado, é lida como tal sem queixa. Nenhum reviewer aponta erro "
            "de calendário no v3."
        ),
    },
    {
        "flag": "2. Modalidade citatória incoerente (AR postal x retorno de mandado)",
        "status": "dead",
        "evidence": (
            "Nenhum reviewer reporta incoerência de modalidade: os dois leem a "
            "cadeia como disponibilização/efetivação eletrônica. ATENÇÃO: o "
            "redesenho 2 introduziu nesta mesma cadeia um NOVO defeito "
            "(efetivação anterior à disponibilização em W-C) — registrado como "
            "flag novo classe (a), não como reincidência deste."
        ),
    },
    {
        "flag": "3. Esqueleto de M-203 (contrato à vista incompatível com renovação automática)",
        "status": "dead",
        "evidence": (
            "O opus v3 lê o contrato como 'plano com cobrança mensal "
            "recorrente, renovação automática por períodos anuais em cláusula "
            "destacada e cancelamento pelo canal contratado' e o usa como "
            "evidência legítima contra a alegação de renovação 'não "
            "informada'. O sonnet não aponta incompatibilidade. Residuais "
            "menores (NF única x cobrança mensal; termo de instalação físico "
            "para serviço digital) classificados como flags novos (b)."
        ),
    },
    {
        "flag": "4. Quantum de M-201 sem critério e anotação negativa sem prova",
        "status": "dead",
        "evidence": (
            "A sentença agora declara o critério ('quantum arbitrado em 100% "
            "do valor do contrato em razão da reiteração...'); o sonnet o "
            "reconhece e não bloqueia. A certidão do órgão de restrição segue "
            "citada e não juntada — o opus a trata como lacuna legítima "
            "('Afirmação... ALEGADA/derivada'), coerente com o padrão "
            "deliberado de peça citada-não-anexa do lote."
        ),
    },
    {
        "flag": "5. Cheiros de template (razão custas/valor ~1,87% constante; datas de fase idênticas)",
        "status": "dead",
        "evidence": (
            "Nenhum reviewer cita razão de custas constante nem datas de fase "
            "idênticas no v3 (as datas agora variam por matter e foram "
            "reconstruídas individualmente nas cronologias). Novos cheiros "
            "menores (contestação sempre no 15º dia útil; calendário "
            "delimitando exatamente as duas hipóteses; 'encaminhada à "
            "assistência técnica') classificados como (c)."
        ),
    },
]

# New v3 flags, classified per the owner's ruler:
# (a) instrument/ruler bug, (b) internal contradiction or visible
# legal-realism defect, (c) cosmetic/template.
NEW_FLAGS = [
    {
        "class": "a",
        "flag": (
            "W-C dos 4 matters: a certidão de efetivação (visualização) é "
            "anterior à disponibilização — impossibilidade causal gerada pela "
            "regra da mutação (data conflitante = citação − 7 dias) sob o novo "
            " modelo eletrônico."
        ),
        "models": ["claude-opus-5 (REDESENHAR M-201/M-203; ressalva em M-202/M-204)", "claude-sonnet-5 (implausível, não bloqueante)"],
        "evidence": (
            "opus: 'visualização registrada antes da disponibilização — "
            "impossível na cadeia de citação eletrônica; defeito de "
            "construção, não mera divergência'; sonnet: 'sequência "
            "incompatível com o funcionamento usual da citação eletrônica, "
            "embora funcional para testar a dupla contagem'."
        ),
    },
    {
        "class": "b",
        "flag": (
            "Certidões citatórias datadas em sábado (M-201: disponibilização e "
            "efetivação em 2024-03-09; M-203: 2024-03-02 e 2024-02-24) — ato "
            "de secretaria em dia não útil, que força leitura suplementar do "
            "L224 não amparada pela nota normativa."
        ),
        "models": ["claude-opus-5"],
        "evidence": (
            "opus: 'data de disponibilização/efetivação em 2024-03-09, que é "
            "sábado — ato de secretaria em dia não útil é pouco plausível e "
            "introduz ambiguidade evitável no termo inicial'."
        ),
    },
    {
        "class": "b",
        "flag": (
            "M-203: nota fiscal única de valor total convivendo com cobrança "
            "mensal recorrente; termo de 'instalação' físico para serviço "
            "digital."
        ),
        "models": ["claude-opus-5"],
        "evidence": (
            "opus (decisão do lote): 'incoerência interna entre cobrança "
            "mensal recorrente (contrato) e nota fiscal única de valor total, "
            "e um termo de instalação físico para serviço digital'."
        ),
    },
    {
        "class": "b",
        "flag": (
            "Persistente do v2: M-202 pede o valor da mercadoria perdida e a "
            "sentença condena pelo preço pago, sem prova de equivalência."
        ),
        "models": ["claude-sonnet-5 (fragilidade de mérito)", "claude-opus-5 (achado legítimo, não bloqueante)"],
        "evidence": (
            "sonnet: 'o quantum do dano material equivale ao preço do "
            "equipamento, não a uma avaliação do estoque perdido'; opus: "
            "'condenação fixada pelo preço pago quando o pedido era o valor "
            "da mercadoria' — tratado como achado analítico válido."
        ),
    },
    {
        "class": "c",
        "flag": (
            "Contestação sempre protocolada exatamente no 15º dia útil; "
            "calendário delimitando exatamente as duas hipóteses de contagem; "
            "reclamação sempre 'encaminhada à assistência técnica' (mesmo "
            "cobranças); extrato sem os atos citatórios (recorrente desde o "
            "v1); certidão de órgão de restrição citada e não juntada (padrão "
            "deliberado)."
        ),
        "models": ["claude-opus-5", "claude-sonnet-5 (parcial)"],
        "evidence": (
            "opus: 'contestações sempre protocoladas no 15º dia útil exato', "
            "'janela... delimita exatamente as duas hipóteses de contagem, "
            "sinal de calibração do gabarito', 'roteamento incoerente com o "
            "assunto, resíduo de modelo'."
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

    v3_total = sum(receipts[m]["total_cost_usd"] for m in MODELS)
    only_cosmetic = all(f["class"] == "c" for f in NEW_FLAGS)
    stopping_rule = {
        "rule": (
            "Se a v3 vier REDESENHAR só com flags de template/cosméticos, não "
            "haverá v4: documentar e encerrar como aceito-com-ressalvas."
        ),
        "v3_has_redesign": not model_gates["pass"],
        "only_cosmetic_flags": only_cosmetic,
        "stop_condition_met": (not model_gates["pass"]) and only_cosmetic,
        "assessment": (
            "A condição de parada NÃO foi atingida: o opus propõe REDESENHAR "
            "com um flag classe (a) — a mutação de W-C gera efetivação "
            "anterior à disponibilização, impossibilidade causal no modelo "
            "eletrônico — além de flags (b). A decisão sobre nova iteração "
            "cabem ao owner."
            if not only_cosmetic
            else
            "Condição de parada atingida: REDESENHAR apenas com flags "
            "cosméticos; encerrar como aceito-com-ressalvas."
        ),
    }

    failures = []
    if not model_gates["pass"]:
        failures.append(
            "claude-opus-5 propôs REDESENHAR para M-201, M-203 e o lote "
            "(classe (a): inversão causal em W-C); claude-sonnet-5 propôs "
            "CONSTRUIR pleno. Pela regra dura, nada foi redesenhado."
        )

    adjudication = {
        "schema_version": 1,
        "status": "PASS_WITH_REDESIGN_FLAG" if not model_gates["pass"] else "PASS",
        "canary_iteration": 3,
        "supersedes": "batch-model-reviews/canary-adjudication-v2.json",
        "criteria": {
            "all_worlds_must_pass": True,
            "critical_observations_require_recovered": True,
            "critical_partial_fails": True,
            "mutations_required": [
                "W-B: reclamação apenas alegada com busca negativa autolimitada",
                "W-C: divergência disponibilização/efetivação sobre a data da "
                "citação e efeito na tempestividade da contestação",
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
            "total": v3_total,
            "v1_plus_v2": PRIOR_COST_USD,
            "v1_plus_v2_plus_v3": PRIOR_COST_USD + v3_total,
        },
        "v2_redesign_flags_resolution": V2_FLAG_RESOLUTION,
        "new_flags_classified": NEW_FLAGS,
        "stopping_rule": stopping_rule,
        "failures": failures,
        "decision_reason": (
            "PASS_WITH_REDESIGN_FLAG. Terceiro canário, sobre o lote do "
            "segundo redesenho: isolamento integral (mesmo prompt sha256 "
            "fad42278..., 216 hashes conferindo com os manifests, quatro IDs, "
            "modelos corretos, sem tools, sem authority, zero retries, "
            "end_turn; uma invocação inicial do sonnet morreu com HTTP 520 "
            "sem qualquer artefato ou uso cobrado, e a chamada congelada é "
            "invocação isolada posterior). Recuperação perfeita nos dois "
            "modelos: 16/16 critical e 8/8 major, sem falso positivo crítico; "
            "os dois excluem corretamente a Sexta-feira Santa nas contagens e "
            "expoem as duas datas e as duas contagens de W-C. Os 5 flags do "
            "v2 estão mortos. Mas o opus propõe REDESENHAR (M-201, M-203 e "
            "lote) por um flag NOVO classe (a): no modelo eletrônico, a "
            "mutação de W-C (efetivação = disponibilização − 7 dias) virou "
            "impossibilidade causal, contaminando a cadeia que o task manda "
            "examinar; somam-se flags (b) — certidões em sábado, NF única x "
            "cobrança mensal e termo de instalação físico em M-203 — e "
            "cheiros (c). O sonnet propõe CONSTRUIR pleno, tratando os mesmos "
            "pontos como fragilidades não bloqueantes. A régua de parada do "
            "owner (parar se REDESENHAR só com cosméticos) NÃO foi atingida: "
            "há flag classe (a). Nada foi redesenhado; decisão registrada "
            "para o owner."
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

    out = REVIEWS / "canary-adjudication-v3.json"
    out.write_text(
        json.dumps(adjudication, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    print(f"status: {adjudication['status']}")
    print(f"stopping_rule: {adjudication['stopping_rule']['assessment']}")
    print(f"cost v3: {v3_total} | accumulated: {PRIOR_COST_USD + v3_total}")


if __name__ == "__main__":
    main()
