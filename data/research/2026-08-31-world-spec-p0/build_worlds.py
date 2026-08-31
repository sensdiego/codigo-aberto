#!/usr/bin/env python3
"""Render and validate the three blind worlds from one authoritative spec."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
SPEC_PATH = ROOT / "world_spec.json"
EMPIRICAL_BASIS_PATH = ROOT / "empirical-basis.json"
OUTPUT_ROOT = ROOT / "generated"


def value(facts: dict[str, str], fact_id: str) -> str:
    return facts[fact_id]


def contract(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Contrato de fornecimento — extrato sintético

## Partes

- Contratante: {value(facts, "F004")}
- Fornecedora: {value(facts, "F003")}

## Condições principais

Em {value(facts, "F010")}, as partes contrataram o {value(facts, "F011")}.
O preço ajustado foi de R$ {value(facts, "F012")}, com vencimento em
{value(facts, "F014")} após a entrega e o aceite.
"""


def invoice(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Nota fiscal sintética NF-SYN-0001

- Emitente: {value(facts, "F003")}
- Destinatária: {value(facts, "F004")}
- Valor: R$ {value(facts, "F012")}
- Vencimento informado: {value(facts, "F014")}
- Situação: emitida.
"""


def delivery(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Termo sintético de entrega e aceite

Em {value(facts, "F013")}, {value(facts, "F004")} declarou ter recebido de
{value(facts, "F003")} o objeto descrito como “{value(facts, "F011")}”.

O termo registra entrega sem ressalvas técnicas.
"""


def initial_petition(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Petição inicial sintética — cobrança

**Processo:** {value(facts, "F001")}{'  '}
**Juízo:** {value(facts, "F002")}{'  '}
**Data do protocolo:** {value(facts, "F020")}

{value(facts, "F003")} propôs ação de cobrança contra
{value(facts, "F004")}. Alegou inadimplemento do principal de
R$ {value(facts, "F012")} após o vencimento de {value(facts, "F014")}.

## Pedido resumido

Condenação ao pagamento do principal, atualização e juros, com base nos
documentos comerciais anexados.
"""


def service_receipt(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Aviso sintético de recebimento da citação

- Processo: {value(facts, "F001")}
- Destinatária: {value(facts, "F004")}
- Data de recebimento: {value(facts, "F024")}
- Resultado: entregue no endereço indicado nos autos.
"""


def judgment(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Sentença sintética — extrato

**Processo:** {value(facts, "F001")}{'  '}
**Juízo:** {value(facts, "F002")}{'  '}
**Data:** {value(facts, "F021")}

Julgo procedente o pedido de {value(facts, "F003")} contra
{value(facts, "F004")} para determinar: {value(facts, "F022")}.
"""


def finality_certificate(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Certidão sintética de trânsito em julgado

Certifico que a sentença do processo {value(facts, "F001")} transitou em
julgado em {value(facts, "F023")}.
"""


def enforcement_petition(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Requerimento sintético de cumprimento de sentença

**Processo:** {value(facts, "F001")}{'  '}
**Juízo:** {value(facts, "F002")}{'  '}
**Protocolo:** {value(facts, "F030")}

{value(facts, "F003")} requer o início do cumprimento contra
{value(facts, "F004")} pelo total declarado de R$ {value(facts, "F031")}.

Pede intimação para pagamento e junta demonstrativo discriminado em arquivo
separado.
"""


def calculation(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Demonstrativo sintético do crédito

- Processo: {value(facts, "F001")}
- Principal histórico: R$ {value(facts, "F012")}
- Critério declarado: {value(facts, "F032")}
- Total declarado: R$ {value(facts, "F031")}
"""


def notice_order(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Despacho sintético de intimação

**Processo:** {value(facts, "F001")}{'  '}
**Juízo:** {value(facts, "F002")}{'  '}
**Data:** {value(facts, "F040")}

Determino {value(facts, "F041")}.
"""


def court_gazette(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Diário da Justiça sintético — extrato

- Processo: {value(facts, "F001")}
- Ato: intimação do despacho para pagamento
- Data indicada para a publicação: {value(facts, "F042")}
"""


def publication_certificate(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Certidão sintética de publicação

Certifico que o despacho de intimação para pagamento no processo
{value(facts, "F001")} foi publicado em {value(facts, "F043")}.
"""


def debtor_email(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# E-mail sintético da executada ao escritório

**Remetente:** jurídico de {value(facts, "F004")}{'  '}
**Data:** {value(facts, "F050")}{'  '}
**Assunto:** pagamento — {value(facts, "F001")}

Informamos que hoje transferimos R$ {value(facts, "F051")} para a
{value(facts, "F052")}. Solicitamos que seja verificada a baixa e que o juízo
seja informado.
"""


def payment_receipt(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Comprovante bancário sintético

- Ordenante: {value(facts, "F004")}
- Data da transferência: {value(facts, "F050")}
- Valor: R$ {value(facts, "F051")}
- Destino informado: {value(facts, "F052")}
- Status bancário exibido: transferência efetivada
"""


def payment_receipt_missing(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Resposta bancária sintética à busca de comprovante

- Solicitante: {value(facts, "F004")}
- Processo informado: {value(facts, "F001")}
- Transferência pesquisada: {value(facts, "F050")}, R$ {value(facts, "F051")}
- Destino informado na solicitação: {value(facts, "F052")}
- Resultado: não foi localizado comprovante com os dados fornecidos

A pesquisa foi realizada pelos identificadores informados. O resultado não
afirma se houve operação com dados diferentes.
"""


def docket(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Extrato sintético de andamentos

**Processo:** {value(facts, "F001")}

**Consulta emitida em:** {value(facts, "F061")}

1. {value(facts, "F021")} — sentença.
2. {value(facts, "F023")} — trânsito em julgado.
3. {value(facts, "F030")} — requerimento de cumprimento.
4. {value(facts, "F040")} — despacho de intimação para pagamento.
5. {value(facts, "F060")}.
"""


def legal_note(spec: dict[str, Any], facts: dict[str, str]) -> str:
    lines = ["# Nota normativa para a tarefa", ""]
    for source in spec["legal_sources"]:
        lines.append(
            f"- **{source['id']} — {source['anchor']}:** {source['proposition']}"
        )
    lines.extend(
        [
            "",
            "Esta nota reúne somente as proposições normativas autorizadas para a",
            "análise. A aplicação depende dos fatos registrados nas demais peças.",
            "",
        ]
    )
    return "\n".join(lines)


def court_calendar(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Calendário sintético de expediente forense — março de 2026

{value(facts, "F070")}.
"""


RENDERERS: dict[str, Callable[[dict[str, Any], dict[str, str]], str]] = {
    "contract": contract,
    "invoice": invoice,
    "delivery": delivery,
    "initial_petition": initial_petition,
    "service_receipt": service_receipt,
    "judgment": judgment,
    "finality_certificate": finality_certificate,
    "enforcement_petition": enforcement_petition,
    "calculation": calculation,
    "notice_order": notice_order,
    "court_gazette": court_gazette,
    "publication_certificate": publication_certificate,
    "debtor_email": debtor_email,
    "payment_receipt": payment_receipt,
    "payment_receipt_missing": payment_receipt_missing,
    "docket": docket,
    "legal_note": legal_note,
    "court_calendar": court_calendar,
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_empirical_basis(spec: dict[str, Any]) -> None:
    basis = load_json(EMPIRICAL_BASIS_PATH)
    if basis.get("schema_version") != 1:
        raise ValueError("unsupported empirical basis schema")
    if basis.get("applies_to_dataset_revision") != spec["dataset"]["revision"]:
        raise ValueError("empirical basis targets another dataset revision")

    report_path = (ROOT / basis["pattern_report_path"]).resolve()
    try:
        report_path.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError(
            "empirical pattern report must stay inside the workspace"
        ) from exc
    report = load_json(report_path)
    if report.get("schema_version") != "fsbrain-aggregate-patterns-v1":
        raise ValueError("unsupported empirical pattern report schema")
    if report.get("source_commit") != basis["pattern_report_source_commit"]:
        raise ValueError("empirical pattern report source commit changed")
    for key, expected in basis["coverage_snapshot"].items():
        if report["coverage"].get(key) != expected:
            raise ValueError(f"empirical coverage changed: {key}")
    for expected in basis["supported_topology"]:
        rows = report["patterns"].get(expected["pattern"], [])
        candidate = {key: value for key, value in expected.items() if key != "pattern"}
        if candidate not in rows:
            raise ValueError(f"empirical topology changed: {expected['pattern']}")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_locators(text: str, needle: str, filename: str) -> list[str]:
    return [
        f"{filename}:{line_number}"
        for line_number, line in enumerate(text.splitlines(), start=1)
        if needle in line
    ]


def spec_hash() -> str:
    return sha256(SPEC_PATH)


def weekday_deadline(publication: str, days: int = 15) -> date:
    current = date.fromisoformat(publication)
    counted = 0
    while counted < days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            counted += 1
    return current


def resolved_facts(spec: dict[str, Any], world: dict[str, Any]) -> dict[str, str]:
    facts = {fact_id: fact["value"] for fact_id, fact in spec["facts"].items()}
    for fact_id, replacement in world["fact_overrides"].items():
        if fact_id not in facts:
            raise ValueError(f"override references unknown fact: {fact_id}")
        facts[fact_id] = replacement
    return facts


def render_task(spec: dict[str, Any]) -> str:
    instructions = "\n".join(
        f"{index}. {item}"
        for index, item in enumerate(spec["task"]["instructions"], start=1)
    )
    return f"""# {spec["task"]["title"]}

{spec["dataset"]["notice"]}

Examine somente os arquivos do diretório `documents/`.

{instructions}

## Formato de entrega

{spec["task"]["output"]}
"""


def reviewer_instructions(spec: dict[str, Any]) -> str:
    world_ids = ", ".join(f"`{world_id}`" for world_id in spec["worlds"])
    return f"""# Protocolo de revisão jurídica cega

## Objetivo

Verificar se um advogado consegue recuperar dos documentos os fatos, lacunas e
conflitos relevantes sem consultar a verdade oculta usada para gerá-los.

## Regra de cegamento

1. Revise {world_ids}, em ordem aleatória ou na ordem apresentada.
2. Em cada pasta, leia apenas `task.md` e `documents/`.
3. Não abra `../authority/`, `world_spec.json` ou `build_worlds.py` antes de
   congelar suas três respostas.
4. Registre a resposta e a avaliação de realismo no template fornecido.
5. Só depois da entrega congelada, um segundo operador compara as respostas com
   as rubricas em `../authority/<mundo>/rubric.json`.

## Critério do gate

O check estático não autoriza construção. A decisão humana deve registrar:

- **CONSTRUIR P0:** os três mundos são distinguíveis pelas provas e a tarefa é
  juridicamente plausível sem depender de fatos inventados;
- **REDESENHAR:** o mecanismo funciona, mas documento, mutação ou rubrica
  precisa de correção identificada;
- **REMOVER:** a especificação curta não controla com segurança o conjunto.

Copie `resultado-revisao.template.json` para `../../human-review-result.json`
e preencha a cópia. O gerador nunca altera esse recibo humano.
"""


def review_template(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "reviewer": "",
        "reviewed_at": "",
        "blind_before_submission": None,
        "decision_options": ["CONSTRUIR P0", "REDESENHAR", "REMOVER"],
        "worlds": {
            world_id: {
                "response_path": "",
                "recovered_material_facts": [],
                "identified_missing_evidence": [],
                "identified_contradictions": [],
                "implausible_or_leaking_documents": [],
                "realism_1_to_5": None,
            }
            for world_id in spec["worlds"]
        },
        "decision": "PENDING",
        "decision_reason": "",
    }


def build() -> None:
    spec = load_json(SPEC_PATH)
    if OUTPUT_ROOT != ROOT / "generated":
        raise RuntimeError("refusing to replace unexpected output path")
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)

    blind_root = OUTPUT_ROOT / "blind"
    authority_root = OUTPUT_ROOT / "authority"
    blind_root.mkdir(parents=True)
    authority_root.mkdir(parents=True)

    (blind_root / "INSTRUCOES-REVISOR.md").write_text(
        reviewer_instructions(spec), encoding="utf-8"
    )
    write_json(blind_root / "resultado-revisao.template.json", review_template(spec))

    world_map: dict[str, Any] = {}
    for world_id, world in spec["worlds"].items():
        facts = resolved_facts(spec, world)
        world_blind = blind_root / world_id
        documents_dir = world_blind / "documents"
        documents_dir.mkdir(parents=True)
        (world_blind / "task.md").write_text(render_task(spec), encoding="utf-8")

        provenance: list[dict[str, Any]] = []
        for document in spec["documents"]:
            renderer_name = world["document_renderer_overrides"].get(
                document["id"], document["renderer"]
            )
            renderer = RENDERERS[renderer_name]
            output_path = documents_dir / document["filename"]
            content = renderer(spec, facts)
            output_path.write_text(content, encoding="utf-8")
            provenance.append(
                {
                    "document_id": document["id"],
                    "filename": document["filename"],
                    "renderer": renderer_name,
                    "fact_ids": document.get("fact_ids", []),
                    "fact_locators": {
                        fact_id: exact_locators(
                            content, facts[fact_id], document["filename"]
                        )
                        for fact_id in document.get("fact_ids", [])
                    },
                    "legal_source_ids": document.get("legal_source_ids", []),
                    "legal_source_locators": [
                        f"{source['path']}#{source['anchor']}"
                        for source in spec["legal_sources"]
                        if source["id"] in document.get("legal_source_ids", [])
                    ],
                    "sha256": sha256(output_path),
                }
            )

        manifest = {
            "schema_version": 1,
            "world_id": world_id,
            "spec_sha256": spec_hash(),
            "task_sha256": sha256(world_blind / "task.md"),
            "document_count": len(provenance),
            "documents": {item["filename"]: item["sha256"] for item in provenance},
        }
        write_json(world_blind / "manifest.json", manifest)

        world_authority = authority_root / world_id
        write_json(
            world_authority / "ground_truth.json",
            {
                "schema_version": 1,
                "world_id": world_id,
                "authority_label": world["authority_label"],
                "description": world["description"],
                "resolved_facts": facts,
                "document_renderer_overrides": world["document_renderer_overrides"],
                "fact_overrides": world["fact_overrides"],
                "expected_observations": world["expected_observations"],
                "spec_sha256": spec_hash(),
            },
        )
        write_json(world_authority / "provenance.json", provenance)
        write_json(
            world_authority / "rubric.json",
            {
                "schema_version": 1,
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
        world_map[world_id] = {
            "authority_label": world["authority_label"],
            "description": world["description"],
            "expected_changed_documents": world["expected_changed_documents"],
        }

    write_json(authority_root / "world-map.json", world_map)
    report = validate(spec, require_qa=False)
    write_json(authority_root / "qa-report.json", report)
    validate(spec, require_qa=True)


def validate(spec: dict[str, Any], require_qa: bool = True) -> dict[str, Any]:
    if spec.get("schema_version") != 1:
        raise ValueError("unsupported spec schema")
    validate_empirical_basis(spec)
    if len(spec["worlds"]) != 3:
        raise ValueError("P0 must contain exactly three worlds")

    fact_ids = set(spec["facts"])
    source_id_list = [source["id"] for source in spec["legal_sources"]]
    source_ids = set(source_id_list)
    observation_id_list = [
        observation["id"]
        for world in spec["worlds"].values()
        for observation in world["expected_observations"]
    ]
    observation_ids = set(observation_id_list)
    rubric_id_list = [criterion["id"] for criterion in spec["common_rubric"]]
    if len(source_id_list) != len(source_ids):
        raise ValueError("duplicate legal source id")
    if len(observation_id_list) != len(observation_ids):
        raise ValueError("duplicate observation id")
    if len(rubric_id_list) != len(set(rubric_id_list)):
        raise ValueError("duplicate rubric id")
    rubric_authorities = fact_ids | source_ids | observation_ids | {"TASK"}
    allowed_classes = {
        "fact",
        "relation",
        "absence",
        "contradiction",
        "law",
        "process",
        "prohibition",
    }
    allowed_severities = {"minor", "major", "critical"}
    for criterion in spec["common_rubric"]:
        if criterion["class"] not in allowed_classes:
            raise ValueError(f"unknown rubric class: {criterion['class']}")
        if criterion["severity"] not in allowed_severities:
            raise ValueError(f"unknown rubric severity: {criterion['severity']}")
        if not set(criterion["authority_ids"]) <= rubric_authorities:
            raise ValueError(f"unknown rubric authority in {criterion['id']}")
    for world in spec["worlds"].values():
        for observation in world["expected_observations"]:
            if observation["class"] not in allowed_classes:
                raise ValueError(f"unknown observation class: {observation['class']}")
            if observation["severity"] not in allowed_severities:
                raise ValueError(
                    f"unknown observation severity: {observation['severity']}"
                )
    document_ids: set[str] = set()
    filenames: set[str] = set()
    covered_fact_ids: set[str] = set()
    covered_source_ids: set[str] = set()
    for document in spec["documents"]:
        if document["id"] in document_ids or document["filename"] in filenames:
            raise ValueError("duplicate document id or filename")
        document_ids.add(document["id"])
        filenames.add(document["filename"])
        if document["renderer"] not in RENDERERS:
            raise ValueError(f"unknown renderer: {document['renderer']}")
        if not set(document.get("fact_ids", [])) <= fact_ids:
            raise ValueError(f"unknown fact in {document['id']}")
        if not set(document.get("legal_source_ids", [])) <= source_ids:
            raise ValueError(f"unknown legal source in {document['id']}")
        covered_fact_ids.update(document.get("fact_ids", []))
        covered_source_ids.update(document.get("legal_source_ids", []))
    for world in spec["worlds"].values():
        overrides = world["document_renderer_overrides"]
        if not set(overrides) <= document_ids:
            raise ValueError("renderer override references unknown document")
        if not set(overrides.values()) <= set(RENDERERS):
            raise ValueError("renderer override references unknown renderer")
    if covered_fact_ids != fact_ids:
        raise ValueError(
            f"facts without document plan: {sorted(fact_ids - covered_fact_ids)}"
        )
    if covered_source_ids != source_ids:
        raise ValueError(
            f"legal sources without document plan: {sorted(source_ids - covered_source_ids)}"
        )

    for source in spec["legal_sources"]:
        source_path = REPO_ROOT / source["path"]
        if not source_path.is_file():
            raise ValueError(f"missing legal source: {source['path']}")
        if f'id="{source["anchor"]}"' not in source_path.read_text(encoding="utf-8"):
            raise ValueError(f"missing legal anchor: {source['anchor']}")

    control = resolved_facts(spec, spec["worlds"]["W-A"])
    conflict = resolved_facts(spec, spec["worlds"]["W-C"])
    payment_date = date.fromisoformat(control["F050"])
    if not (
        weekday_deadline(conflict["F043"])
        < payment_date
        <= weekday_deadline(control["F042"])
    ):
        raise ValueError("chronology mutation no longer changes weekday timeliness")

    baseline_files: dict[str, str] | None = None
    world_counts: dict[str, int] = {}
    blind_forbidden = {
        world["authority_label"] for world in spec["worlds"].values()
    } | {
        observation["id"]
        for world in spec["worlds"].values()
        for observation in world["expected_observations"]
    }
    blind_forbidden |= set(fact_ids) | {"world_spec", "expected_observations"}

    for world_id, world in spec["worlds"].items():
        world_blind = OUTPUT_ROOT / "blind" / world_id
        documents_dir = world_blind / "documents"
        actual_files = {
            path.name: sha256(path) for path in sorted(documents_dir.glob("*.md"))
        }
        expected_files = {document["filename"] for document in spec["documents"]}
        if set(actual_files) != expected_files:
            raise ValueError(f"unexpected document set in {world_id}")
        if not 10 <= len(actual_files) <= 20:
            raise ValueError(f"document count outside 10..20 in {world_id}")
        world_counts[world_id] = len(actual_files)

        manifest = load_json(world_blind / "manifest.json")
        if manifest["documents"] != actual_files:
            raise ValueError(f"manifest hash mismatch in {world_id}")
        if manifest["spec_sha256"] != spec_hash():
            raise ValueError(f"stale spec hash in {world_id}")
        if manifest["task_sha256"] != sha256(world_blind / "task.md"):
            raise ValueError(f"task hash mismatch in {world_id}")

        blind_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [world_blind / "task.md", *sorted(documents_dir.glob("*.md"))]
        )
        leaked = sorted(token for token in blind_forbidden if token in blind_text)
        if leaked:
            raise ValueError(f"authority token leaked in {world_id}: {leaked}")

        ground_truth = load_json(
            OUTPUT_ROOT / "authority" / world_id / "ground_truth.json"
        )
        if ground_truth["resolved_facts"] != resolved_facts(spec, world):
            raise ValueError(f"ground truth mismatch in {world_id}")
        provenance = load_json(OUTPUT_ROOT / "authority" / world_id / "provenance.json")
        if {item["filename"]: item["sha256"] for item in provenance} != actual_files:
            raise ValueError(f"provenance hash mismatch in {world_id}")
        facts = resolved_facts(spec, world)
        for item in provenance:
            document_text = (documents_dir / item["filename"]).read_text(
                encoding="utf-8"
            )
            for fact_id in item["fact_ids"]:
                expected_locators = exact_locators(
                    document_text, facts[fact_id], item["filename"]
                )
                if not expected_locators:
                    raise ValueError(
                        f"fact {fact_id} lacks visible locator in {world_id}"
                    )
                if item["fact_locators"].get(fact_id) != expected_locators:
                    raise ValueError(f"stale fact locator in {world_id}: {fact_id}")

        for observation in world["expected_observations"]:
            for evidence in observation["evidence"]:
                if evidence not in actual_files:
                    raise ValueError(
                        f"missing expected evidence {evidence} in {world_id}"
                    )

        if baseline_files is None:
            baseline_files = actual_files
        else:
            if set(actual_files) != set(baseline_files):
                raise ValueError(f"blind file inventory differs in {world_id}")
            changed = {
                filename
                for filename in set(baseline_files) | set(actual_files)
                if baseline_files.get(filename) != actual_files.get(filename)
            }
            if changed != set(world["expected_changed_documents"]):
                raise ValueError(
                    f"undeclared mutation in {world_id}: {sorted(changed)}"
                )

    if require_qa:
        qa = load_json(OUTPUT_ROOT / "authority" / "qa-report.json")
        if (
            qa.get("status") != "PASS"
            or qa.get("world_document_counts") != world_counts
        ):
            raise ValueError("stale QA report")

    return {
        "schema_version": 1,
        "status": "PASS",
        "spec_sha256": spec_hash(),
        "world_document_counts": world_counts,
        "checks": [
            "three opaque blind worlds",
            "10..20 documents per world",
            "legal source files and anchors resolve",
            "all fact and source references resolve",
            "every expressed fact has an exact filename:line locator",
            "every rubric criterion names class severity and authority",
            "blind files contain no authority labels or ids",
            "manifests and provenance match document hashes",
            "all expected evidence exists",
            "blind file inventory is identical across worlds",
            "only declared documents differ from control",
            "chronology mutation changes weekday-only timeliness",
        ],
        "human_review": "PENDING",
    }


def main() -> int:
    command = sys.argv[1] if len(sys.argv) == 2 else ""
    if command == "build":
        build()
    elif command == "check":
        validate(load_json(SPEC_PATH))
    else:
        print("usage: build_worlds.py {build|check}", file=sys.stderr)
        return 2
    print(f"{command}: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
