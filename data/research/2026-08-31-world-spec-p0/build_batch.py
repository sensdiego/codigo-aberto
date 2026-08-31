#!/usr/bin/env python3
"""Build and check 12 synthetic matters derived from the reviewed P0 seed."""

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
from decimal import Decimal
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
    "creditor",
    "debtor",
    "object",
    "principal_brl",
    "updated_brl",
    "timeline_shift_weeks",
}
DATE_FACT_IDS = (
    "F010",
    "F013",
    "F014",
    "F020",
    "F021",
    "F023",
    "F024",
    "F030",
    "F040",
    "F042",
    "F043",
    "F050",
)
KNOWN_COURT_CLOSURES_2026 = {
    date(2026, 4, 3),
    date(2026, 4, 21),
    date(2026, 5, 1),
    date(2026, 6, 4),
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


def notice_writ(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Ofício sintético de informação do Diário da Justiça

**Processo:** {facts["F001"]}{'  '}
**Juízo:** {facts["F002"]}{'  '}
**Despacho:** {facts["F040"]}

Em resposta à consulta da secretaria sobre a veiculação do despacho que determinou
{facts["F041"]}, informa-se ao juízo que a publicação ocorreu em {facts["F042"]}.
"""


def batch_calendar(spec: dict[str, Any], facts: dict[str, str]) -> str:
    return f"""# Calendário sintético de expediente forense — {facts["F071"]}

{facts["F070"]}.
"""


RENDERERS: dict[str, Callable[[dict[str, Any], dict[str, str]], str]] = {
    **seed.RENDERERS,
    "batch_calendar": batch_calendar,
    "notice_writ": notice_writ,
}


def brl_decimal(value: str) -> Decimal:
    if not re.fullmatch(r"\d{1,3}(?:\.\d{3})*,\d{2}", value):
        raise ValueError(f"invalid BRL amount: {value}")
    return Decimal(value.replace(".", "").replace(",", "."))


def validate_batch_spec(batch: dict[str, Any], seed_spec: dict[str, Any]) -> None:
    if batch.get("schema_version") != 1:
        raise ValueError("unsupported batch schema")
    if seed.sha256(SEED_SPEC_PATH) != batch.get("seed_spec_sha256"):
        raise ValueError("seed spec hash changed")
    if seed.sha256(EMPIRICAL_BASIS_PATH) != batch.get("empirical_basis_sha256"):
        raise ValueError("empirical basis hash changed")
    if batch.get("worlds_per_matter") != 3 or len(seed_spec["worlds"]) != 3:
        raise ValueError("batch must preserve exactly three seed worlds")
    if (
        batch.get("timeline_policy")
        != "weekly_offsets_preserving_reviewed_weekday_relation"
    ):
        raise ValueError("P0 batch must preserve the reviewed weekday relation")
    seed.validate_empirical_basis(seed_spec)

    motifs = batch.get("motifs")
    matters = batch.get("matters")
    if not isinstance(motifs, dict) or not isinstance(matters, list):
        raise ValueError("batch motifs and matters are required")
    if len(matters) != 12:
        raise ValueError("P0 batch must contain exactly 12 matters")

    document_ids = {document["id"] for document in seed_spec["documents"]}
    for motif_id, motif in motifs.items():
        if not isinstance(motif, dict) or motif.get("target_count", 0) < 1:
            raise ValueError(f"invalid motif: {motif_id}")
        if not set(motif.get("evidence_document_ids", ())) <= document_ids:
            raise ValueError(f"motif references unknown document: {motif_id}")
        if not str(motif.get("focus_instruction", "")).strip():
            raise ValueError(f"motif lacks focus instruction: {motif_id}")

    identifiers: list[str] = []
    timeline_shifts: list[int] = []
    motif_counts = Counter[str]()
    for matter in matters:
        if not isinstance(matter, dict) or set(matter) != MATTER_KEYS:
            raise ValueError("matter fields do not match the batch contract")
        if matter["motif"] not in motifs:
            raise ValueError(f"unknown matter motif: {matter['motif']}")
        if not re.fullmatch(r"M-\d{3}", matter["id"]):
            raise ValueError(f"invalid matter id: {matter['id']}")
        if not re.fullmatch(r"BR-CIV-EXEC-\d{3}", matter["process"]):
            raise ValueError(f"invalid synthetic process id: {matter['process']}")
        if brl_decimal(matter["updated_brl"]) <= brl_decimal(matter["principal_brl"]):
            raise ValueError(f"updated amount must exceed principal: {matter['id']}")
        if (
            not isinstance(matter["timeline_shift_weeks"], int)
            or not 0 <= matter["timeline_shift_weeks"] <= 21
        ):
            raise ValueError(f"invalid timeline shift: {matter['id']}")
        if any(not str(matter[key]).strip() for key in MATTER_KEYS):
            raise ValueError(f"matter contains an empty value: {matter['id']}")
        identifiers.extend((matter["id"], matter["process"]))
        timeline_shifts.append(matter["timeline_shift_weeks"])
        motif_counts[matter["motif"]] += 1

    if len(identifiers) != len(set(identifiers)):
        raise ValueError("matter or process identifiers are duplicated")
    if len(timeline_shifts) != len(set(timeline_shifts)):
        raise ValueError("timeline shifts must be unique across the P0 batch")
    expected_counts = Counter(
        {motif_id: motif["target_count"] for motif_id, motif in motifs.items()}
    )
    if motif_counts != expected_counts:
        raise ValueError(f"motif distribution changed: {dict(motif_counts)}")


def shifted(value: str, weeks: int) -> str:
    return (date.fromisoformat(value) + timedelta(weeks=weeks)).isoformat()


def update_observation_claims(
    spec: dict[str, Any], updated_brl: str, office_motif: bool
) -> None:
    facts = {fact_id: fact["value"] for fact_id, fact in spec["facts"].items()}
    for observation in spec["worlds"]["W-A"]["expected_observations"]:
        if observation["id"] == "O-A1":
            observation["claim"] = (
                "A executada alegou e documentou transferência de "
                f"R$ {updated_brl} em {facts['F050']}."
            )
    for observation in spec["worlds"]["W-C"]["expected_observations"]:
        if observation["id"] == "O-C1":
            source = "O ofício" if office_motif else "O Diário"
            observation["claim"] = (
                f"{source} registra publicação em {facts['F042']} e a certidão "
                f"registra {spec['worlds']['W-C']['fact_overrides']['F043']}."
            )
        elif observation["id"] == "O-C2":
            observation["claim"] = (
                "Sem resolver o marco inicial, não é seguro concluir se o pagamento "
                f"de {facts['F050']} ocorreu dentro do prazo."
            )


def use_office_motif(spec: dict[str, Any]) -> None:
    document = next(item for item in spec["documents"] if item["id"] == "D041")
    document.update(
        {
            "filename": "11-oficio-informacao-diario.md",
            "renderer": "notice_writ",
            "fact_ids": ["F001", "F002", "F040", "F041", "F042"],
        }
    )
    conflict = spec["worlds"]["W-C"]
    conflict["description"] = (
        "O comprovante existe, mas ofício e certidão divergem sobre a data da "
        "publicação, tornando ambígua a tempestividade."
    )
    for observation in conflict["expected_observations"]:
        observation["evidence"] = [
            "11-oficio-informacao-diario.md" if item == "11-diario-justica.md" else item
            for item in observation["evidence"]
        ]


def use_batch_calendar(spec: dict[str, Any]) -> None:
    document = next(item for item in spec["documents"] if item["id"] == "D071")
    document.update(
        {
            "renderer": "batch_calendar",
            "fact_ids": ["F070", "F071"],
        }
    )


def materialize_spec(
    seed_spec: dict[str, Any], batch: dict[str, Any], matter: dict[str, str]
) -> dict[str, Any]:
    spec = copy.deepcopy(seed_spec)
    spec["dataset"].update(
        {
            "id": matter["id"],
            "batch_id": batch["batch_id"],
            "matter_id": matter["id"],
            "motif": matter["motif"],
        }
    )
    weeks = matter["timeline_shift_weeks"]
    # ponytail: weekly offsets preserve the reviewed weekdays; introduce other
    # chronology shapes only after this first batch earns expansion.
    for fact_id in DATE_FACT_IDS:
        spec["facts"][fact_id]["value"] = shifted(
            spec["facts"][fact_id]["value"], weeks
        )
    conflict_date = shifted(spec["worlds"]["W-C"]["fact_overrides"]["F043"], weeks)
    spec["worlds"]["W-C"]["fact_overrides"]["F043"] = conflict_date
    facts = {fact_id: fact["value"] for fact_id, fact in spec["facts"].items()}
    publication = date.fromisoformat(facts["F042"])
    payment = date.fromisoformat(facts["F050"])
    deadline = seed.weekday_deadline(facts["F042"])
    period = f"{conflict_date} a {deadline.isoformat()}"
    spec["facts"]["F071"] = {"name": "periodo_calendario", "value": period}
    spec["facts"]["F070"]["value"] = (
        f"no período de {period}, houve expediente regular de segunda a sexta-feira; "
        "não incidiu feriado nacional, feriado local ou suspensão"
    )
    values = {
        "F001": matter["process"],
        "F002": matter["court"],
        "F003": matter["creditor"],
        "F004": matter["debtor"],
        "F011": matter["object"],
        "F012": matter["principal_brl"],
        "F022": (
            f"pagar R$ {matter['principal_brl']}, com atualização pelo IPCA-E "
            f"desde {facts['F014']} e juros simples de 1% ao mês desde a citação"
        ),
        "F031": matter["updated_brl"],
        "F032": (
            f"demonstrativo declara IPCA-E até {facts['F030']} e juros simples "
            f"de 1% ao mês desde {facts['F024']}"
        ),
        "F051": matter["updated_brl"],
        "F052": f"conta judicial vinculada ao processo {matter['process']}",
        "F060": (
            f"{(publication + timedelta(days=1)).isoformat()} — juntada da certidão "
            "de publicação da intimação para pagamento"
        ),
        "F061": f"{(payment + timedelta(days=2)).isoformat()} 09:10",
    }
    for fact_id, value in values.items():
        spec["facts"][fact_id]["value"] = value
    spec["task"]["title"] = f"Análise do cumprimento de sentença — {matter['id']}"
    spec["task"]["instructions"].append(
        batch["motifs"][matter["motif"]]["focus_instruction"]
    )
    office_motif = matter["motif"] == "decisao_oficio_certidao"
    if office_motif:
        use_office_motif(spec)
    use_batch_calendar(spec)
    update_observation_claims(spec, matter["updated_brl"], office_motif)
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
    payment = seed.date.fromisoformat(control["F050"])
    start = seed.date.fromisoformat(conflict["F043"])
    deadline = seed.weekday_deadline(control["F042"])
    current = start
    relevant_dates: set[date] = set()
    while current <= deadline:
        if current.weekday() < 5:
            relevant_dates.add(current)
        current += timedelta(days=1)
    closures = sorted(relevant_dates & KNOWN_COURT_CLOSURES_2026)
    if closures or payment in KNOWN_COURT_CLOSURES_2026:
        raise ValueError(f"effective spec crosses a known court closure: {closures}")
    if not (
        seed.weekday_deadline(conflict["F043"])
        < payment
        <= seed.weekday_deadline(control["F042"])
    ):
        raise ValueError("effective spec lost the reviewed chronology mutation")


def render_world(
    output_root: Path,
    batch_sha256: str,
    matter: dict[str, str],
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
            "weekly timeline offsets preserve the reviewed weekday relation",
            "known 2026 court closures are absent from deadline windows",
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
