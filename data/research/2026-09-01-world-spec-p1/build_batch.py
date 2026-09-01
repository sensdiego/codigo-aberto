#!/usr/bin/env python3
"""Build and check 12 synthetic matters derived from the reviewed P1 seed."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import tempfile
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Callable

import build_worlds as seed


ROOT = Path(__file__).resolve().parent
BATCH_SPEC_PATH = ROOT / "batch-spec.json"
SEED_SPEC_PATH = ROOT / "world_spec.json"
EMPIRICAL_BASIS_PATH = ROOT / "empirical-basis.json"
OUTPUT_ROOT = ROOT / "batch-generated"
MATTER_KEYS = {
    "id",
    "motif",
    "process",
    "court",
    "plaintiff",
    "defendant",
    "action_label",
    "object",
    "principal_brl",
    "symptom",
    "claim_summary",
    "judgment_command",
    "defense_thesis",
    "report_conclusion",
    "proof_request",
    "timeline_shift_years",
}
DATE_FACT_IDS = (
    "F010",
    "F013",
    "F020",
    "F030",
    "F040",
    "F041",
    "F042",
    "F050",
    "F060",
    "F070",
    "F072",
    "F080",
    "F092",
    "F093",
)
OPTIONAL_MATTER_KEYS = {"contract_variant"}
CONTRACT_VARIANTS = {
    "a_vista",
    "assinatura_periodica",
    "credito_parcelado",
    "intermediacao",
    "parcelado",
    "permuta_torna",
    "transporte",
}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def json_bytes(payload: Any) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode()


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def initial_petition_batch(spec: dict[str, Any], facts: dict[str, str]) -> str:
    variant = spec["dataset"].get("contract_variant", "a_vista")
    if variant == "intermediacao":
        narrative = (
            f"{facts['F003']} propôs ação de {facts['F101']} contra\n"
            f"{facts['F004']}. Narra que, em {facts['F010']}, foi contratada "
            "pela ré para a intermediação comercial dos contratos, com "
            f"comissão ajustada de R$ {facts['F012']}, e que, após a "
            f"conclusão dos contratos intermediados em {facts['F013']}, "
            f"restou caracterizado “{facts['F014']}”."
        )
    elif variant == "permuta_torna":
        narrative = (
            f"{facts['F003']} propôs ação de {facts['F101']} contra\n"
            f"{facts['F004']}. Narra que, em {facts['F010']}, contratou o "
            f"objeto com torna ajustada de R$ {facts['F012']} paga à ré e "
            f"que, recebido parcialmente em {facts['F013']}, o objeto passou "
            f"a apresentar “{facts['F014']}”."
        )
    elif variant == "transporte":
        narrative = (
            f"{facts['F003']} propôs ação de {facts['F101']} contra\n"
            f"{facts['F004']}. Narra que, em {facts['F010']}, contratou o "
            f"objeto com valor de carga declarado de R$ {facts['F012']} e "
            f"que, durante a execução em {facts['F013']}, verificou-se "
            f"“{facts['F014']}”."
        )
    elif variant == "credito_parcelado":
        narrative = (
            f"{facts['F003']} propôs ação de {facts['F101']} contra\n"
            f"{facts['F004']}. Narra que, em {facts['F010']}, contratou o "
            f"objeto pelo preço de R$ {facts['F012']}, financiado em "
            "parcelas mensais, e que o objeto, instalado "
            f"em {facts['F013']}, passou a apresentar “{facts['F014']}”."
        )
    else:
        narrative = (
            f"{facts['F003']} propôs ação de {facts['F101']} contra\n"
            f"{facts['F004']}. Narra que, em {facts['F010']}, contratou o\n"
            f"objeto pelo preço de R$ {facts['F012']} e que o objeto, "
            f"instalado\nem {facts['F013']}, passou a apresentar "
            f"“{facts['F014']}”."
        )
    return f"""# Petição inicial sintética — {facts["F101"]}

**Processo:** {facts["F001"]}{'  '}
**Juízo:** {facts["F002"]}{'  '}
**Data do protocolo:** {facts["F030"]}

{narrative}

Alega ter reclamado extrajudicialmente junto à ré em {facts["F020"]},
sem solução.

## Pedido resumido

{facts["F031"]}, com base nos documentos comerciais anexados.
"""


def answer_batch(spec: dict[str, Any], facts: dict[str, str]) -> str:
    variant = spec["dataset"].get("contract_variant", "a_vista")
    if variant == "transporte":
        # The defendant cannot deny the occurrence its own occurrence report
        # registers; the defense contests extension/quantum and causation.
        return f"""# Contestação sintética

**Processo:** {facts["F001"]}{'  '}
**Protocolo:** {facts["F042"]}

A ré {facts["F004"]} sustenta que {facts["F043"]}. Reconhece a
ocorrência registrada em seu próprio termo, mas impugna a extensão e o
valor do dano descrito como “{facts["F014"]}”, bem como o pedido de
{facts["F101"]}.
"""
    return f"""# Contestação sintética

**Processo:** {facts["F001"]}{'  '}
**Protocolo:** {facts["F042"]}

A ré {facts["F004"]} sustenta que {facts["F043"]}. Nega a
existência de “{facts["F014"]}” nos termos alegados pela autora e
impugna o pedido de {facts["F101"]}.
"""


def court_calendar_batch(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Calendário sintético de expediente forense — {facts["F102"]}

{facts["F100"]}.
"""


def contract_batch(spec: dict[str, Any], facts: dict[str, str]) -> str:
    # Matters whose dispute presupposes a non-standard economic structure
    # cannot rest on the flat "paid upfront" contract. The variant comes from
    # the matter itself (batch-spec contract_variant); everything else keeps
    # the upfront template.
    variant = spec["dataset"].get("contract_variant", "a_vista")
    parties = (
        f"- Contratante: {facts['F003']}\n- Contratada: {facts['F004']}"
    )
    if variant == "assinatura_periodica":
        conditions = (
            f"Em {facts['F010']}, as partes contrataram o {facts['F011']}, em "
            "plano de assinatura com cobrança mensal recorrente e renovação "
            "automática mensal, mediante cláusula de renovação automática em "
            "destaque no instrumento. O valor total "
            f"contratado foi de R$ {facts['F012']}, com cancelamento possível "
            "pelo canal contratado a qualquer tempo."
        )
    elif variant == "parcelado":
        parcela = format_brl(parse_brl_centavos(facts["F012"]) // 8)
        conditions = (
            f"Em {facts['F010']}, as partes contrataram o {facts['F011']}.\n"
            f"O preço ajustado foi de R$ {facts['F012']}, pago em 8 parcelas "
            f"mensais de R$ {parcela}, conforme plano de pagamento anexo ao "
            "instrumento, com instalação inclusa no objeto."
        )
    elif variant == "intermediacao":
        # Single economic direction: the defendant hired the plaintiff
        # (broker) and owes the commission — the money never flows both ways.
        parties = (
            f"- Contratante: {facts['F004']}\n- Contratada: {facts['F003']}"
        )
        conditions = (
            f"Em {facts['F010']}, as partes contrataram a {facts['F011']}. "
            f"A comissão ajustada foi de R$ {facts['F012']}, devida pela "
            "contratante à contratada após o fechamento dos contratos "
            "intermediados."
        )
    elif variant == "permuta_torna":
        conditions = (
            f"Em {facts['F010']}, as partes contrataram o {facts['F011']}, "
            "com cláusula de torna em dinheiro. O valor da torna ajustado foi "
            f"de R$ {facts['F012']}, pago à vista na assinatura pela "
            "contratante à contratada."
        )
    elif variant == "transporte":
        conditions = (
            f"Em {facts['F010']}, as partes contrataram o {facts['F011']}. "
            f"O valor declarado da carga foi de R$ {facts['F012']}, com "
            "frete ajustado entre as partes conforme o instrumento."
        )
    elif variant == "credito_parcelado":
        conditions = (
            f"Em {facts['F010']}, as partes contrataram o {facts['F011']}.\n"
            f"O preço ajustado foi de R$ {facts['F012']}, financiado pela "
            "própria contratada em parcelas mensais, com encargos contratados "
            "em quadro resumo anexo ao instrumento."
        )
    else:
        conditions = (
            f"Em {facts['F010']}, as partes contrataram o {facts['F011']}.\n"
            f"O preço ajustado foi de R$ {facts['F012']}, pago à vista na "
            "assinatura, com instalação inclusa no objeto."
        )
    return f"""# Contrato de prestação de serviços — extrato sintético

## Partes

{parties}

## Condições principais

{conditions}
"""


def invoice_batch(spec: dict[str, Any], facts: dict[str, str]) -> str:
    # The batch invoice carries a matter-unique number (derived
    # deterministically like the ATD protocol) and an emission date coherent
    # with the spine. Variants adapt the document to the matter's economic
    # structure (commission flow, permuta torna, cargo CT-e).
    matter_index = int(spec["dataset"]["matter_id"].split("-")[1]) - 200
    number = f"NF-SYN-{1000 + matter_index}"
    variant = spec["dataset"].get("contract_variant", "a_vista")
    if variant == "intermediacao":
        return f"""# Nota fiscal sintética {number}

- Emitente: {facts["F003"]}
- Destinatária: {facts["F004"]}
- Data de emissão: {facts["F013"]}
- Valor: R$ {facts["F012"]}
- Referente: comissão de corretagem pelos contratos intermediados, faturada
  após o fechamento.
- Situação: emitida.
"""
    if variant == "permuta_torna":
        return f"""# Nota fiscal sintética {number}

- Emitente: {facts["F004"]}
- Destinatária: {facts["F003"]}
- Data de emissão: {facts["F010"]}
- Valor: R$ {facts["F012"]}
- Referente: torna do contrato de permuta.
- Situação: emitida.
"""
    if variant == "transporte":
        return f"""# Conhecimento de transporte eletrônico sintético CT-e-{1000 + matter_index}

- Emitente (transportadora): {facts["F004"]}
- Remetente: {facts["F003"]}
- Data de emissão: {facts["F010"]}
- Valor da carga declarado: R$ {facts["F012"]}
- Situação: emitido.
"""
    return f"""# Nota fiscal sintética {number}

- Emitente: {facts["F004"]}
- Destinatária: {facts["F003"]}
- Data de emissão: {facts["F010"]}
- Valor: R$ {facts["F012"]}
- Situação: emitida.
"""


def delivery_intermediacao(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Relatório sintético de intermediação concluída

Em {facts["F013"]}, {facts["F003"]} apresentou a {facts["F004"]} o relatório
da {facts["F011"]}, com a planilha de negócios concluídos anexa.

O relatório registra o fechamento dos contratos intermediados, sem pendências
registradas.
"""


def delivery_transporte(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Termo sintético de ocorrência no transporte

Em {facts["F013"]}, {facts["F004"]} registrou, no curso do {facts["F011"]},
ocorrência de colisão rodoviária com avaria na carga transportada, comunicada
a {facts["F003"]}.

O termo registra a avaria parcial da carga, sem conclusão sobre o valor dos
danos.
"""


def delivery_ressalva(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Termo sintético de aceite parcial com ressalva

Em {facts["F013"]}, {facts["F003"]} declarou ter recebido de
{facts["F004"]} o objeto descrito como “{facts["F011"]}”.

O termo registra aceite parcial, com ressalva expressa de pendências de
entrega das unidades modulares permutadas.
"""


def reply_batch(spec: dict[str, Any], facts: dict[str, str]) -> str:
    # Canary P1 fix: the proof requested in the reply is the same proof the
    # case management order later determines (F061, derived from the matter),
    # so a contractual dispute is not sent to an equipment expertise.
    return f"""# Réplica sintética

**Processo:** {facts["F001"]}{'  '}
**Protocolo:** {facts["F050"]}

A autora {facts["F003"]} manifesta-se sobre a contestação, insistindo
na procedência do pedido e requerendo a produção de {facts["F061"]}.
"""


def expert_report_batch(spec: dict[str, Any], facts: dict[str, str]) -> str:
    # Canary P1 fix: the report names the proof determined in the case
    # management order (F061, derived from the matter) and keeps the examined
    # object, so object, scope and conclusion stay aligned with the claim.
    return f"""# Laudo pericial sintético — extrato

**Processo:** {facts["F001"]}{'  '}
**Data de entrega:** {facts["F070"]}

O perito realizou a prova determinada no despacho saneador — {facts["F061"]} —,
examinando o objeto descrito como “{facts["F011"]}” e a documentação comercial
dos autos, e concluiu: {facts["F071"]}.
"""


RENDERERS: dict[str, Callable[[dict[str, Any], dict[str, str]], str]] = {
    **seed.RENDERERS,
    "answer_batch": answer_batch,
    "contract_batch": contract_batch,
    "court_calendar_batch": court_calendar_batch,
    "delivery_intermediacao": delivery_intermediacao,
    "delivery_ressalva": delivery_ressalva,
    "delivery_transporte": delivery_transporte,
    "expert_report_batch": expert_report_batch,
    "initial_petition_batch": initial_petition_batch,
    "invoice_batch": invoice_batch,
    "reply_batch": reply_batch,
}


def brl(value: str) -> None:
    if not re.fullmatch(r"\d{1,3}(?:\.\d{3})*,\d{2}", value):
        raise ValueError(f"invalid BRL amount: {value}")


def validate_batch_spec(batch: dict[str, Any], seed_spec: dict[str, Any]) -> None:
    if batch.get("schema_version") != 1:
        raise ValueError("unsupported batch schema")
    if seed.sha256(SEED_SPEC_PATH) != batch.get("seed_spec_sha256"):
        raise ValueError("seed spec hash changed")
    if seed.sha256(EMPIRICAL_BASIS_PATH) != batch.get("empirical_basis_sha256"):
        raise ValueError("empirical basis hash changed")
    if batch.get("worlds_per_matter") != 3 or len(seed_spec["worlds"]) != 3:
        raise ValueError("batch must preserve exactly three seed worlds")
    if batch.get("timeline_policy") != "yearly_offsets_preserving_chronology_relations":
        raise ValueError("P1 batch must preserve the reviewed chronology relations")
    seed.validate_empirical_basis(seed_spec)

    motifs = batch.get("motifs")
    matters = batch.get("matters")
    if not isinstance(motifs, dict) or not isinstance(matters, list):
        raise ValueError("batch motifs and matters are required")
    if len(matters) != 12:
        raise ValueError("P1 batch must contain exactly 12 matters")

    document_ids = {document["id"] for document in seed_spec["documents"]}
    for motif_id, motif in motifs.items():
        if not isinstance(motif, dict) or motif.get("target_count", 0) < 1:
            raise ValueError(f"invalid motif: {motif_id}")
        if not set(motif.get("evidence_document_ids", ())) <= document_ids:
            raise ValueError(f"motif references unknown document: {motif_id}")
        if not str(motif.get("focus_instruction", "")).strip():
            raise ValueError(f"motif lacks focus instruction: {motif_id}")

    identifiers: list[str] = []
    names: list[str] = []
    motif_counts = Counter[str]()
    motif_shift_combos = Counter[tuple[str, int]]()
    for matter in matters:
        if not isinstance(matter, dict) or not (
            MATTER_KEYS <= set(matter) <= MATTER_KEYS | OPTIONAL_MATTER_KEYS
        ):
            raise ValueError("matter fields do not match the batch contract")
        if matter.get("contract_variant", "a_vista") not in CONTRACT_VARIANTS:
            raise ValueError(f"unknown contract variant: {matter['id']}")
        if matter["motif"] not in motifs:
            raise ValueError(f"unknown matter motif: {matter['motif']}")
        if not re.fullmatch(r"M-2\d{2}", matter["id"]):
            raise ValueError(f"invalid matter id: {matter['id']}")
        if not re.fullmatch(r"BR-CIV-CON-2\d{2}", matter["process"]):
            raise ValueError(f"invalid synthetic process id: {matter['process']}")
        brl(matter["principal_brl"])
        if matter["timeline_shift_years"] not in (-2, -1, 0):
            raise ValueError(f"invalid timeline shift: {matter['id']}")
        if any(not str(matter[key]).strip() for key in MATTER_KEYS):
            raise ValueError(f"matter contains an empty value: {matter['id']}")
        identifiers.extend((matter["id"], matter["process"]))
        names.extend((matter["court"], matter["plaintiff"], matter["defendant"]))
        motif_counts[matter["motif"]] += 1
        motif_shift_combos[(matter["motif"], matter["timeline_shift_years"])] += 1

    if len(identifiers) != len(set(identifiers)):
        raise ValueError("matter or process identifiers are duplicated")
    if len(names) != len(set(names)):
        raise ValueError("court or party names are duplicated across the batch")
    if max(motif_shift_combos.values()) > 2:
        raise ValueError("motif x shift combination repeated more than twice")
    expected_counts = Counter(
        {motif_id: motif["target_count"] for motif_id, motif in motifs.items()}
    )
    if motif_counts != expected_counts:
        raise ValueError(f"motif distribution changed: {dict(motif_counts)}")


def shifted(value: str, years: int) -> str:
    day = date.fromisoformat(value)
    try:
        return day.replace(year=day.year + years).isoformat()
    except ValueError:
        return day.replace(year=day.year + years, day=28).isoformat()


def update_observation_claims(spec: dict[str, Any]) -> None:
    facts = {fact_id: fact["value"] for fact_id, fact in spec["facts"].items()}
    conflict_citation = spec["worlds"]["W-C"]["fact_overrides"]["F041"]
    for observation in spec["worlds"]["W-A"]["expected_observations"]:
        if observation["id"] == "O-A1":
            observation["claim"] = (
                f"A autora alegou reclamação extrajudicial de {facts['F020']} e "
                f"o registro de atendimento {facts['F021']} corrobora a data."
            )
    for observation in spec["worlds"]["W-B"]["expected_observations"]:
        if observation["id"] == "O-B1":
            observation["claim"] = (
                f"A reclamação de {facts['F020']} consta apenas da petição "
                "inicial; a busca no serviço de atendimento não localizou "
                "registro correspondente."
            )
    for observation in spec["worlds"]["W-C"]["expected_observations"]:
        if observation["id"] == "O-C1":
            observation["claim"] = (
                f"A certidão de disponibilização registra a disponibilização "
                f"da citação em {facts['F040']} e a certidão de efetivação "
                f"registra disponibilização e visualização em "
                f"{conflict_citation}."
            )
        elif observation["id"] == "O-C2":
            observation["claim"] = (
                "Sem resolver a data da citação, não é seguro concluir se a "
                f"contestação de {facts['F042']} foi tempestiva na contagem em "
                "dias úteis."
            )


def use_batch_renderers(spec: dict[str, Any]) -> None:
    updates = {
        "D010": ("contract_batch", []),
        "D011": ("invoice_batch", ["F010"]),
        "D020": ("initial_petition_batch", ["F101"]),
        "D030": ("answer_batch", ["F101"]),
        "D031": ("reply_batch", []),
        "D040": ("expert_report_batch", []),
        "D071": ("court_calendar_batch", ["F102"]),
    }
    for document in spec["documents"]:
        if document["id"] in updates:
            renderer, extra_facts = updates[document["id"]]
            document["renderer"] = renderer
            document["fact_ids"] = [*document["fact_ids"], *extra_facts]
    # Variant-specific delivery document (03): physical installation does not
    # exist for intermediation, transport or partial-delivery matters; and the
    # transport matter anchors its cargo value in a CT-e instead of an invoice.
    variant = spec["dataset"].get("contract_variant", "a_vista")
    delivery_overrides = {
        "intermediacao": ("03-relatorio-intermediacao.md", "delivery_intermediacao"),
        "permuta_torna": ("03-termo-aceite-parcial.md", "delivery_ressalva"),
        "transporte": ("03-termo-ocorrencia-transporte.md", "delivery_transporte"),
    }
    for document in spec["documents"]:
        if document["id"] == "D012" and variant in delivery_overrides:
            filename, renderer = delivery_overrides[variant]
            document["filename"] = filename
            document["renderer"] = renderer
        if document["id"] == "D011" and variant == "transporte":
            document["filename"] = "02-cte-conhecimento-carga.md"
        if document["id"] == "D011" and variant == "intermediacao":
            # The commission invoice is issued at the taxable event (the
            # closing of the intermediated contracts), not at contracting.
            document["fact_ids"] = [
                "F013" if fact_id == "F010" else fact_id
                for fact_id in document["fact_ids"]
            ]


def parse_brl_centavos(value: str) -> int:
    return int(value.replace(".", "").replace(",", ""))


def format_brl(centavos: int) -> str:
    return f"{centavos // 100:,}".replace(",", ".") + f",{centavos % 100:02d}"


def batch_fee_brl(matter: dict[str, Any], matter_index: int) -> str:
    # Canary fixes: court fees vary per matter (no flat R$ 4.812,00) and the
    # effective rate also varies per matter, deterministically, in
    # [1.40%, 2.30%], so the fees/principal ratio is not a template constant.
    # A small index jitter keeps the cents non-round.
    rate_basis_points = 140 + (matter_index * 37) % 91
    fee_centavos = (
        parse_brl_centavos(matter["principal_brl"]) * rate_basis_points // 10000
        + matter_index * 13
    )
    return format_brl(fee_centavos)


def materialize_spec(
    seed_spec: dict[str, Any], batch: dict[str, Any], matter: dict[str, Any]
) -> dict[str, Any]:
    spec = copy.deepcopy(seed_spec)
    spec["dataset"].update(
        {
            "id": matter["id"],
            "batch_id": batch["batch_id"],
            "matter_id": matter["id"],
            "motif": matter["motif"],
            "contract_variant": matter.get("contract_variant", "a_vista"),
        }
    )
    years = matter["timeline_shift_years"]
    # ponytail: yearly offsets keep the spine relations; introduce other
    # chronology shapes only after this first batch earns expansion.
    for fact_id in DATE_FACT_IDS:
        spec["facts"][fact_id]["value"] = shifted(
            spec["facts"][fact_id]["value"], years
        )
    spec["worlds"]["W-C"]["fact_overrides"]["F041"] = shifted(
        spec["worlds"]["W-C"]["fact_overrides"]["F041"], years
    )
    # Deterministic per-matter day jitter (±14 days) so phase dates are not
    # identical across matters. A uniform translation of every spine date
    # preserves the ordering and every prazo relation.
    matter_index = int(matter["id"].split("-")[1]) - 200
    jitter = timedelta(days=((matter_index * 11) % 29) - 14)
    for fact_id in DATE_FACT_IDS:
        shifted_day = date.fromisoformat(spec["facts"][fact_id]["value"]) + jitter
        spec["facts"][fact_id]["value"] = shifted_day.isoformat()
    conflict_citation = (
        date.fromisoformat(spec["worlds"]["W-C"]["fact_overrides"]["F041"])
        + jitter
    )
    spec["worlds"]["W-C"]["fact_overrides"]["F041"] = (
        conflict_citation.isoformat()
    )
    # The jitter can land registry acts on a weekend (v3 flag); snap every
    # spine date to the nearest weekday. Snapping moves each date by at most
    # one day, far less than any spine gap, so ordering and prazo relations
    # are preserved.
    for fact_id in DATE_FACT_IDS:
        snapped = seed.snap_to_weekday(
            date.fromisoformat(spec["facts"][fact_id]["value"])
        )
        spec["facts"][fact_id]["value"] = snapped.isoformat()
    spec["worlds"]["W-C"]["fact_overrides"]["F041"] = seed.snap_to_weekday(
        date.fromisoformat(spec["worlds"]["W-C"]["fact_overrides"]["F041"])
    ).isoformat()
    # Whole-year offsets and the day jitter change weekdays, so a plainly
    # shifted answer date can fall outside the 15-weekday window. The reviewed
    # relation is "answer filed on the last weekday of the deadline", so
    # recompute it from the citation with the shared court calendar (the same
    # holiday-aware rule used by the calendar text and the validators).
    spec["facts"]["F042"]["value"] = seed.court_deadline(
        spec["facts"]["F040"]["value"]
    ).isoformat()
    facts = {fact_id: fact["value"] for fact_id, fact in spec["facts"].items()}
    start = min(
        date.fromisoformat(facts["F040"]),
        date.fromisoformat(spec["worlds"]["W-C"]["fact_overrides"]["F041"]),
    )
    deadline = seed.court_deadline(facts["F040"])
    period = f"{start.isoformat()} a {deadline.isoformat()}"
    consultation = seed.snap_to_weekday(
        date.fromisoformat(shifted(facts["F091"].split(" ")[0], years)) + jitter
    )
    values = {
        "F001": matter["process"],
        "F002": matter["court"],
        "F003": matter["plaintiff"],
        "F004": matter["defendant"],
        "F011": matter["object"],
        "F012": matter["principal_brl"],
        "F014": matter["symptom"],
        "F021": f"ATD-{facts['F020'][:4]}-{7800 + matter_index}",
        "F031": matter["claim_summary"],
        "F043": matter["defense_thesis"],
        "F061": matter["proof_request"],
        "F071": matter["report_conclusion"],
        "F081": matter["judgment_command"],
        "F094": batch_fee_brl(matter, matter_index),
        "F090": (
            f"{facts['F092']} — juntada da certidão de intimação da sentença"
        ),
        "F091": f"{consultation.isoformat()} {facts['F091'].split(' ')[1]}",
        "F100": seed.calendar_text(start, deadline),
    }
    for fact_id, value in values.items():
        spec["facts"][fact_id]["value"] = value
    spec["facts"]["F101"] = {"name": "rotulo_acao", "value": matter["action_label"]}
    spec["facts"]["F102"] = {"name": "periodo_calendario", "value": period}
    use_batch_renderers(spec)
    spec["task"]["title"] = f"Análise da ação de conhecimento — {matter['id']}"
    spec["task"]["instructions"].append(
        batch["motifs"][matter["motif"]]["focus_instruction"]
    )
    update_observation_claims(spec)
    return spec


def validate_effective_spec(spec: dict[str, Any]) -> None:
    fact_ids = set(spec["facts"])
    document_ids: set[str] = set()
    filenames: set[str] = set()
    covered_facts: set[str] = set()
    for document in spec["documents"]:
        if document["id"] in document_ids or document["filename"] in filenames:
            raise ValueError("effective spec has duplicate document identity")
        if document["renderer"] not in RENDERERS:
            raise ValueError(f"unknown renderer: {document['renderer']}")
        if not set(document.get("fact_ids", ())) <= fact_ids:
            raise ValueError(f"unknown fact in document: {document['id']}")
        document_ids.add(document["id"])
        filenames.add(document["filename"])
        covered_facts.update(document.get("fact_ids", ()))
    if covered_facts != fact_ids:
        raise ValueError(f"uncovered facts: {sorted(fact_ids - covered_facts)}")
    for world in spec["worlds"].values():
        if not set(world["document_renderer_overrides"]) <= document_ids:
            raise ValueError("world override references an unknown document")
        if not set(world["document_renderer_overrides"].values()) <= set(RENDERERS):
            raise ValueError("world override references an unknown renderer")

    control = seed.resolved_facts(spec, spec["worlds"]["W-A"])
    conflict = seed.resolved_facts(spec, spec["worlds"]["W-C"])

    spine = ["F010", "F013", "F020", "F030", "F040", "F042", "F050", "F060", "F070", "F072", "F080", "F092"]
    ordered = [date.fromisoformat(control[fact_id]) for fact_id in spine]
    if any(later <= earlier for earlier, later in zip(ordered, ordered[1:])):
        raise ValueError("effective spec lost the spine ordering")

    answer_date = date.fromisoformat(control["F042"])
    citation_control = date.fromisoformat(control["F040"])
    citation_conflict = date.fromisoformat(conflict["F041"])
    if not (
        seed.court_deadline(conflict["F041"])
        < answer_date
        <= seed.court_deadline(control["F040"])
    ):
        raise ValueError("effective spec lost the reviewed chronology mutation")

    deadline = seed.court_deadline(control["F040"])
    start = min(citation_control, citation_conflict)
    # The calendar text and this validator share the same holiday-aware
    # counting rule; refuse any build whose calendar hides a window holiday or
    # whose answer date is not exactly the shared court deadline.
    window_holidays = seed.court_holidays_between(start, deadline)
    calendar = control["F100"]
    hidden = [
        day.isoformat()
        for day in window_holidays
        if day.isoformat() not in calendar
    ]
    if hidden:
        raise ValueError(f"calendar hides a window holiday: {hidden}")
    if (
        answer_date != deadline
        or answer_date.weekday() >= 5
        or answer_date in window_holidays
    ):
        raise ValueError("answer is not on the shared court deadline")
    # Both citation certificates (control and the W-C conflict) must be dated
    # on a court day of their own calendar — never weekend or holiday.
    for label, day in (
        ("F040", citation_control),
        ("F041-conflict", citation_conflict),
    ):
        if day.weekday() >= 5 or seed.court_holidays_between(day, day):
            raise ValueError(f"citation date is not a court day: {label} {day}")


def render_world(
    output_root: Path,
    batch_sha256: str,
    matter: dict[str, Any],
    spec: dict[str, Any],
    spec_sha256: str,
    world_id: str,
    world: dict[str, Any],
) -> dict[str, str]:
    facts = seed.resolved_facts(spec, world)
    blind_root = output_root / "blind" / matter["id"] / world_id
    documents_root = blind_root / "documents"
    documents_root.mkdir(parents=True)
    (blind_root / "task.md").write_text(seed.render_task(spec), encoding="utf-8")

    provenance: list[dict[str, Any]] = []
    for document in spec["documents"]:
        renderer_name = world["document_renderer_overrides"].get(
            document["id"], document["renderer"]
        )
        content = RENDERERS[renderer_name](spec, facts)
        output_path = documents_root / document["filename"]
        output_path.write_text(content, encoding="utf-8")
        locators = {
            fact_id: seed.exact_locators(content, facts[fact_id], document["filename"])
            for fact_id in document.get("fact_ids", ())
        }
        if any(not value for value in locators.values()):
            raise ValueError(
                f"fact lacks visible locator: {matter['id']} {document['id']}"
            )
        provenance.append(
            {
                "document_id": document["id"],
                "filename": document["filename"],
                "renderer": renderer_name,
                "fact_ids": document.get("fact_ids", []),
                "fact_locators": locators,
                "legal_source_ids": document.get("legal_source_ids", []),
                "legal_source_locators": [
                    f"{source['path']}#{source['anchor']}"
                    for source in spec["legal_sources"]
                    if source["id"] in document.get("legal_source_ids", [])
                ],
                "sha256": seed.sha256(output_path),
            }
        )

    document_hashes = {item["filename"]: item["sha256"] for item in provenance}
    seed.write_json(
        blind_root / "manifest.json",
        {
            "schema_version": 1,
            "batch_id": spec["dataset"]["batch_id"],
            "matter_id": matter["id"],
            "world_id": world_id,
            "batch_spec_sha256": batch_sha256,
            "effective_spec_sha256": spec_sha256,
            "task_sha256": seed.sha256(blind_root / "task.md"),
            "document_count": len(document_hashes),
            "documents": document_hashes,
        },
    )

    authority_root = output_root / "authority" / matter["id"] / world_id
    seed.write_json(
        authority_root / "ground_truth.json",
        {
            "schema_version": 1,
            "matter_id": matter["id"],
            "motif": matter["motif"],
            "world_id": world_id,
            "authority_label": world["authority_label"],
            "description": world["description"],
            "resolved_facts": facts,
            "expected_observations": world["expected_observations"],
            "effective_spec_sha256": spec_sha256,
        },
    )
    seed.write_json(authority_root / "provenance.json", provenance)
    seed.write_json(
        authority_root / "rubric.json",
        {
            "schema_version": 1,
            "matter_id": matter["id"],
            "world_id": world_id,
            "common": spec["common_rubric"],
            "world_specific": [
                {
                    "observation_id": observation["id"],
                    "class": observation["class"],
                    "severity": observation["severity"],
                    "authority_ids": [observation["id"]],
                    "criterion": observation["rubric"],
                    "expected_state": observation["state"],
                    "weight": 3,
                }
                for observation in world["expected_observations"]
            ],
        },
    )

    forbidden = {
        *spec["facts"],
        "world_spec",
        "expected_observations",
        world["authority_label"],
        *(item["id"] for item in world["expected_observations"]),
    }
    blind_text = (blind_root / "task.md").read_text(encoding="utf-8") + "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(documents_root.glob("*.md"))
    )
    leaked = sorted(token for token in forbidden if token in blind_text)
    if leaked:
        raise ValueError(f"authority token leaked: {matter['id']} {world_id} {leaked}")
    return document_hashes


def build_tree(output_root: Path) -> dict[str, Any]:
    batch = seed.load_json(BATCH_SPEC_PATH)
    seed_spec = seed.load_json(SEED_SPEC_PATH)
    validate_batch_spec(batch, seed_spec)
    batch_sha256 = seed.sha256(BATCH_SPEC_PATH)

    if output_root.exists() and output_root.resolve() != OUTPUT_ROOT.resolve():
        raise RuntimeError("refusing to replace an unexpected existing directory")
    if output_root.exists():
        shutil.rmtree(output_root)
    (output_root / "blind").mkdir(parents=True)
    (output_root / "authority").mkdir(parents=True)

    total_documents = 0
    motif_counts = Counter[str]()
    for matter in batch["matters"]:
        spec = materialize_spec(seed_spec, batch, matter)
        validate_effective_spec(spec)
        spec_sha256 = sha256_bytes(json_bytes(spec))
        seed.write_json(
            output_root / "authority" / matter["id"] / "effective-spec.json", spec
        )
        motif_counts[matter["motif"]] += 1

        control_hashes: dict[str, str] | None = None
        for world_id, world in spec["worlds"].items():
            hashes = render_world(
                output_root,
                batch_sha256,
                matter,
                spec,
                spec_sha256,
                world_id,
                world,
            )
            total_documents += len(hashes)
            if control_hashes is None:
                control_hashes = hashes
                continue
            changed = {
                filename
                for filename in set(control_hashes) | set(hashes)
                if control_hashes.get(filename) != hashes.get(filename)
            }
            if changed != set(world["expected_changed_documents"]):
                raise ValueError(
                    f"undeclared world mutation: {matter['id']} {world_id} {sorted(changed)}"
                )

    matter_count = len(batch["matters"])
    world_count = matter_count * len(seed_spec["worlds"])
    if total_documents != matter_count * len(seed_spec["worlds"]) * len(
        seed_spec["documents"]
    ):
        raise ValueError("batch document count is inconsistent")

    report = {
        "schema_version": 1,
        "status": "STATIC_PASS",
        "blind_review_receipt": "SEPARATE_FROM_STATIC_BUILD",
        "batch_id": batch["batch_id"],
        "batch_spec_sha256": batch_sha256,
        "seed_spec_sha256": batch["seed_spec_sha256"],
        "empirical_basis_sha256": batch["empirical_basis_sha256"],
        "matter_count": matter_count,
        "world_count": world_count,
        "document_count": total_documents,
        "motif_counts": dict(sorted(motif_counts.items())),
        "blind_tree_sha256": tree_sha256(output_root / "blind"),
        "authority_tree_sha256": tree_sha256(output_root / "authority"),
        "checks": [
            "12 unique synthetic matters",
            "four motifs match the empirical allocation",
            "three controlled worlds per matter",
            "17 documents per world",
            "all declared facts have visible locators",
            "only the declared document changes in each mutation",
            "no authority identifiers leak into blind files",
            "yearly timeline offsets preserve the spine ordering",
            "chronology mutation keeps the weekday timeliness split per matter",
            "calendar marks every national holiday in each contestation window",
            "the answer lands exactly on the shared holiday-aware court deadline",
        ],
    }
    seed.write_json(output_root / "batch-manifest.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("build", "check"))
    args = parser.parse_args()

    if args.mode == "build":
        if OUTPUT_ROOT != ROOT / "batch-generated":
            raise RuntimeError("refusing to replace an unexpected batch output path")
        report = build_tree(OUTPUT_ROOT)
        print(
            "PASS: "
            f"{report['matter_count']} matters, {report['world_count']} worlds, "
            f"{report['document_count']} documents"
        )
        return 0

    if not OUTPUT_ROOT.is_dir():
        raise FileNotFoundError("batch output is absent; run build")
    with tempfile.TemporaryDirectory(prefix="codigo-aberto-batch-check-") as temp:
        expected_root = Path(temp) / "batch-generated"
        build_tree(expected_root)
        if tree_sha256(expected_root) != tree_sha256(OUTPUT_ROOT):
            raise ValueError("batch output is stale; run build")
    print("PASS: batch is deterministic, current, and statically valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
