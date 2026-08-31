#!/usr/bin/env python3
"""Extract aggregate, non-identifying structural patterns from fs.brain."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
DEFAULT_OUTPUT = ROOT / "pattern-report.json"

DOCUMENT_TYPES = frozenset(
    {
        "analise_interna",
        "ata",
        "audio_transcript",
        "comprovante",
        "contrato",
        "conversa",
        "decisao",
        "dossie",
        "email",
        "mapa",
        "matricula",
        "matriz",
        "nota",
        "outro",
        "peticao",
        "playbook",
        "procuracao",
        "roteiro",
    }
)
SECTION_TYPES = frozenset(
    {"certidao", "contrato", "decisao", "oficio", "outro", "peticao"}
)
MATERIAL_SCOPES = frozenset(
    {
        "delta_only",
        "document_bundle_partial",
        "full_autos",
        "legal_one_ged_partial",
        "meeting_only",
        "unset",
    }
)
SOURCE_SYSTEMS = frozenset(
    {
        "fs_archive",
        "google_drive",
        "legal_one",
        "local_import",
        "manual_upload",
        "meeting",
        "projudi",
        "reconstructed",
        "unset",
        "upload_inbox",
    }
)
HUMAN_VALIDATION_STATUSES = frozenset(
    {
        "bloqueado_por_fonte",
        "rascunho_agente",
        "revisao_parcial",
        "validado_responsavel",
    }
)
MOVEMENT_CATEGORIES = (
    ("recurso", ("agravo", "apelacao", "embargo", "recurso")),
    ("decisao", ("acordao", "decisao", "julgado", "julgamento", "sentenca")),
    ("despacho", ("despacho",)),
    ("citacao_intimacao", ("citacao", "intimacao", "notificacao")),
    ("publicacao", ("diario", "djen", "disponibilizacao", "publicacao")),
    ("expedicao_oficio", ("expedicao", "mandado", "oficio")),
    ("conclusao", ("conclusao", "conclusos")),
    ("prazo", ("decurso", "prazo")),
    ("remessa_retorno", ("recebidos", "remessa", "retorno")),
    ("audiencia", ("audiencia", "sessao")),
    ("prova_pericia", ("laudo", "pericia", "prova")),
    (
        "financeiro_constricao",
        ("alvara", "bloqueio", "deposito", "levantamento", "pagamento", "penhora"),
    ),
    ("arquivamento_baixa", ("arquiv", "baixa", "extincao")),
    ("distribuicao_autuacao", ("autuacao", "distribuicao")),
    ("certidao_secretaria", ("cartorio", "certidao", "certificado", "secretaria")),
    ("peticao_manifestacao", ("juntada", "manifestacao", "peticao", "protocolo")),
    ("habilitacao", ("habilitacao",)),
    ("suspensao", ("suspensao", "suspenso")),
)
SENSITIVE_PATTERNS = (
    re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b"),
    re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"),
    re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"),
    re.compile(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b"),
    re.compile(r"(?:/Users/|/private/|R\$)"),
)


def normalized(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    return text.encode("ascii", "ignore").decode("ascii").strip().lower()


def fixed_category(value: object, allowed: frozenset[str], fallback: str) -> str:
    candidate = normalized(value).replace("-", "_").replace(" ", "_")
    return candidate if candidate in allowed else fallback


def movement_category(value: object) -> str:
    text = normalized(value)
    for category, needles in MOVEMENT_CATEGORIES:
        if any(needle in text for needle in needles):
            return category
    return "outro"


def quantiles(values: Iterable[int]) -> dict[str, int]:
    ordered = sorted(values)
    if not ordered:
        return {"min": 0, "p25": 0, "median": 0, "p75": 0, "p95": 0, "max": 0}

    def pick(percentile: float) -> int:
        return ordered[round((len(ordered) - 1) * percentile)]

    return {
        "min": ordered[0],
        "p25": pick(0.25),
        "median": pick(0.5),
        "p75": pick(0.75),
        "p95": pick(0.95),
        "max": ordered[-1],
    }


def count_rows(counter: Counter[str]) -> list[dict[str, object]]:
    return [
        {"category": category, "count": count}
        for category, count in sorted(
            counter.items(), key=lambda item: (-item[1], item[0])
        )
    ]


def pair_rows(
    counts: Counter[tuple[str, str]],
    cases: dict[tuple[str, str], set[str]],
    min_support: int,
) -> list[dict[str, object]]:
    rows = [
        {
            "from": source,
            "to": target,
            "count": count,
            "case_support": len(cases[(source, target)]),
        }
        for (source, target), count in counts.items()
        if len(cases[(source, target)]) >= min_support
    ]
    return sorted(
        rows,
        key=lambda row: (
            -int(row["case_support"]),
            -int(row["count"]),
            str(row["from"]),
            str(row["to"]),
        ),
    )


def cooccurrence_rows(
    counts: Counter[tuple[str, str]], min_support: int
) -> list[dict[str, object]]:
    return [
        {"left": left, "right": right, "case_support": count}
        for (left, right), count in sorted(
            counts.items(), key=lambda item: (-item[1], item[0])
        )
        if count >= min_support
    ]


def movement_sort_value(value: object) -> tuple[int, str]:
    match = re.search(r"\d+", str(value or ""))
    return (int(match.group()) if match else 10**12, normalized(value))


def source_commit(fsbrain_root: Path) -> str:
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=fsbrain_root,
        check=True,
        capture_output=True,
        text=True,
    )
    if status.stdout.strip():
        raise ValueError(
            "fs.brain source worktree must be clean for a reproducible report"
        )
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=fsbrain_root,
        check=True,
        capture_output=True,
        text=True,
    )
    commit = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("fs.brain HEAD is not a full Git commit SHA")
    return commit


def validate_output_path(output: Path) -> Path:
    resolved = output.resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError(
            "output must stay inside the current codigo-aberto workspace"
        ) from exc
    return resolved


def validate_report(report: dict[str, Any]) -> str:
    encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(encoded):
            raise ValueError(
                f"aggregate report failed privacy check: {pattern.pattern}"
            )
    if not re.fullmatch(r"[0-9a-f]{40}", str(report.get("source_commit", ""))):
        raise ValueError("aggregate report has an invalid source commit")
    return encoded


def extract(fsbrain_root: Path, min_support: int) -> dict[str, Any]:
    fsbrain_root = fsbrain_root.resolve()
    if not (fsbrain_root / "tooling/brain/cases.py").is_file():
        raise ValueError("--fsbrain-root is not an fs.brain repository")
    if min_support < 2:
        raise ValueError("--min-support must be at least 2")
    snapshot_commit = source_commit(fsbrain_root)

    sys.path.insert(0, str(fsbrain_root))
    previous_cwd = Path.cwd()
    os.chdir(fsbrain_root)
    try:
        from tooling.brain.cases import CASE_REGISTRY
        from tooling.brain.frontmatter import read_frontmatter_only
        from tooling.brain.operational_status import parse_operational_status_source
        from tooling.brain.parser import MarkdownParseError

        eligible: set[str] = set()
        human_validation = Counter[str]()
        for case_slug in CASE_REGISTRY:
            parsed = parse_operational_status_source(
                fsbrain_root / "fs.brain/ops/case-status" / f"{case_slug}.yaml",
                expected_case_slug=case_slug,
            )
            if str(parsed.status.ingestao.status) != "liberada":
                continue
            eligible.add(case_slug)
            status = fixed_category(
                parsed.status.validacao_humana.status,
                HUMAN_VALIDATION_STATUSES,
                "other",
            )
            human_validation[status] += 1

        document_types = Counter[str]()
        material_scopes = Counter[str]()
        source_systems = Counter[str]()
        material_scope_cases: defaultdict[str, set[str]] = defaultdict(set)
        source_system_cases: defaultdict[str, set[str]] = defaultdict(set)
        section_types = Counter[str]()
        section_transition_counts = Counter[tuple[str, str]]()
        section_transition_cases: defaultdict[tuple[str, str], set[str]] = defaultdict(
            set
        )
        section_case_types: defaultdict[str, set[str]] = defaultdict(set)
        document_case_types: defaultdict[str, set[str]] = defaultdict(set)
        case_section_counts = Counter[str]()
        case_movement_records: defaultdict[
            tuple[str, str], list[tuple[tuple[object, ...], str, str]]
        ] = defaultdict(list)
        parsed_notes = Counter[str]()
        output_markdown_parse_errors = 0
        source_note_parse_errors = 0
        eligible_output_markdown = 0
        movement_notes = 0
        movements_without_order = 0
        movements_without_proceeding_id = 0

        output_paths = sorted((fsbrain_root / "fs.brain/outputs").rglob("*.md"))
        for path in output_paths:
            is_source_note = "source-documents" in path.parts
            try:
                frontmatter = read_frontmatter_only(path)
            except (MarkdownParseError, OSError, UnicodeError):
                output_markdown_parse_errors += 1
                source_note_parse_errors += is_source_note
                continue
            case_slug = frontmatter.get("case_slug")
            if not isinstance(case_slug, str) or case_slug not in eligible:
                continue
            eligible_output_markdown += 1
            if not is_source_note:
                continue
            parsed_notes[case_slug] += 1

            document_type = fixed_category(
                frontmatter.get("document_type") or frontmatter.get("kind"),
                DOCUMENT_TYPES,
                "outro",
            )
            material_scope = fixed_category(
                frontmatter.get("material_scope"), MATERIAL_SCOPES, "unset"
            )
            source_system = fixed_category(
                frontmatter.get("source_system"), SOURCE_SYSTEMS, "unset"
            )
            document_types[document_type] += 1
            material_scopes[material_scope] += 1
            source_systems[source_system] += 1
            document_case_types[case_slug].add(document_type)
            material_scope_cases[material_scope].add(case_slug)
            source_system_cases[source_system].add(case_slug)

            fields = frontmatter.get("document_fields")
            fields = fields if isinstance(fields, dict) else {}
            sections = fields.get("internal_sections")
            sections = sections if isinstance(sections, list) else []
            ordered_sections: list[tuple[tuple[int, int], str]] = []
            for position, section in enumerate(sections):
                if not isinstance(section, dict):
                    continue
                section_type = fixed_category(
                    section.get("section_type"), SECTION_TYPES, "outro"
                )
                page = section.get("page_start")
                page_number = page if isinstance(page, int) else 10**12
                ordered_sections.append(((page_number, position), section_type))
                section_types[section_type] += 1
                section_case_types[case_slug].add(section_type)
                case_section_counts[case_slug] += 1
            section_sequence = [item[1] for item in sorted(ordered_sections)]
            for pair in zip(section_sequence, section_sequence[1:]):
                section_transition_counts[pair] += 1
                section_transition_cases[pair].add(case_slug)

            movements = fields.get("movimentacoes")
            movements = movements if isinstance(movements, list) else []
            if movements:
                movement_notes += 1
            for position, movement in enumerate(movements):
                if not isinstance(movement, dict):
                    continue
                major = movement.get("mov_major")
                minor = movement.get("mov_minor")
                if major is None:
                    movements_without_order += 1
                order = (
                    movement_sort_value(major),
                    movement_sort_value(minor),
                    normalized(movement.get("data")),
                    position,
                )
                proceeding = normalized(movement.get("cnj"))
                if not proceeding:
                    movements_without_proceeding_id += 1
                    proceeding = path.as_posix()
                proceeding_key = hashlib.sha256(proceeding.encode()).hexdigest()
                identity_fields = (
                    movement.get("cnj"),
                    movement.get("mov_id") or major,
                    minor,
                )
                identity = hashlib.sha256(
                    json.dumps(
                        identity_fields if identity_fields[1] is not None else movement,
                        default=str,
                        ensure_ascii=False,
                        sort_keys=True,
                    ).encode()
                ).hexdigest()
                case_movement_records[(case_slug, proceeding_key)].append(
                    (order, identity, movement_category(movement.get("tipo")))
                )

        movement_types = Counter[str]()
        movement_transition_counts = Counter[tuple[str, str]]()
        movement_transition_cases: defaultdict[tuple[str, str], set[str]] = defaultdict(
            set
        )
        case_movement_counts = Counter[str]()
        movement_identity_category_conflicts = 0
        for (case_slug, _proceeding_key), records in case_movement_records.items():
            deduplicated: dict[str, tuple[tuple[object, ...], str]] = {}
            for order, identity, category in records:
                existing = deduplicated.get(identity)
                if existing is None:
                    deduplicated[identity] = (order, category)
                elif existing[1] != category:
                    movement_identity_category_conflicts += 1
                    deduplicated[identity] = (min(existing[0], order), "outro")
            sequence = [category for order, category in sorted(deduplicated.values())]
            case_movement_counts[case_slug] += len(sequence)
            movement_types.update(sequence)
            for pair in zip(sequence, sequence[1:]):
                movement_transition_counts[pair] += 1
                movement_transition_cases[pair].add(case_slug)

        section_cooccurrences = Counter[tuple[str, str]]()
        document_cooccurrences = Counter[tuple[str, str]]()
        for values in section_case_types.values():
            section_cooccurrences.update(itertools.combinations(sorted(values), 2))
        for values in document_case_types.values():
            document_cooccurrences.update(itertools.combinations(sorted(values), 2))

        all_case_note_counts = [parsed_notes[case_slug] for case_slug in eligible]
        all_case_section_counts = [
            case_section_counts[case_slug] for case_slug in eligible
        ]
        all_case_movement_counts = [
            case_movement_counts[case_slug] for case_slug in eligible
        ]
        if source_commit(fsbrain_root) != snapshot_commit:
            raise RuntimeError("fs.brain changed during extraction")
        return {
            "schema_version": "fsbrain-aggregate-patterns-v1",
            "source_commit": snapshot_commit,
            "selection": {
                "case_rule": "ingestion_status_liberada",
                "source_note_rule": "registered_case_output_under_source_documents",
                "min_case_support": min_support,
            },
            "privacy_contract": {
                "output": "aggregate_counts_and_fixed_categories_only",
                "excluded": [
                    "case_identifiers",
                    "client_or_party_names",
                    "process_numbers",
                    "document_text",
                    "dates",
                    "monetary_values",
                    "raw_titles",
                    "raw_movement_descriptions",
                ],
            },
            "coverage": {
                "registered_cases": len(CASE_REGISTRY),
                "eligible_cases": len(eligible),
                "eligible_case_output_markdown": eligible_output_markdown,
                "output_markdown_parse_errors_global": output_markdown_parse_errors,
                "eligible_cases_with_source_notes": sum(
                    bool(parsed_notes[case_slug]) for case_slug in eligible
                ),
                "source_notes_parsed": sum(parsed_notes.values()),
                "source_notes_parse_errors": source_note_parse_errors,
                "cases_with_typed_sections": len(section_case_types),
                "typed_sections": sum(section_types.values()),
                "source_notes_with_movements": movement_notes,
                "cases_with_movements": len(case_movement_counts),
                "structured_proceeding_sequences": len(case_movement_records),
                "deduplicated_movements": sum(case_movement_counts.values()),
                "movements_without_numeric_major_order": movements_without_order,
                "movements_without_proceeding_id": movements_without_proceeding_id,
                "movement_identity_category_conflicts": movement_identity_category_conflicts,
                "cases_with_any_full_autos_note": len(
                    material_scope_cases["full_autos"]
                ),
                "full_autos_source_notes": material_scopes["full_autos"],
            },
            "human_validation": count_rows(human_validation),
            "distributions": {
                "document_types_by_source_note": count_rows(document_types),
                "material_scopes_by_source_note": count_rows(material_scopes),
                "material_scopes_by_case": count_rows(
                    Counter(
                        {key: len(value) for key, value in material_scope_cases.items()}
                    )
                ),
                "source_systems_by_source_note": count_rows(source_systems),
                "source_systems_by_case": count_rows(
                    Counter(
                        {key: len(value) for key, value in source_system_cases.items()}
                    )
                ),
                "section_types": count_rows(section_types),
                "movement_categories": count_rows(movement_types),
            },
            "per_case_quantiles": {
                "source_notes_all_eligible_cases": quantiles(all_case_note_counts),
                "typed_sections_all_eligible_cases": quantiles(all_case_section_counts),
                "movements_all_eligible_cases": quantiles(all_case_movement_counts),
                "movements_contributing_cases": quantiles(
                    case_movement_counts.values()
                ),
            },
            "patterns": {
                "section_transitions": pair_rows(
                    section_transition_counts, section_transition_cases, min_support
                ),
                "movement_transitions": pair_rows(
                    movement_transition_counts, movement_transition_cases, min_support
                ),
                "section_type_cooccurrences": cooccurrence_rows(
                    section_cooccurrences, min_support
                ),
                "document_type_cooccurrences": cooccurrence_rows(
                    document_cooccurrences, min_support
                ),
            },
            "coverage_limits": [
                "document_and_section_patterns_apply_to_the_eligible_corpus_only",
                "movement_patterns_apply_only_to_cases_with_structured_movements",
                "full_procedural_history_must_not_be_inferred_from_partial_material",
                "human_validation_status_is_not_a_ground_truth_label_for_each_extracted_pattern",
            ],
        }
    finally:
        os.chdir(previous_cwd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("build", "check"))
    parser.add_argument("--fsbrain-root", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--min-support", type=int, default=5)
    args = parser.parse_args()

    output = validate_output_path(args.output)
    encoded = validate_report(extract(args.fsbrain_root, args.min_support))
    if args.mode == "build":
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
        print(f"PASS: aggregate report written ({len(encoded)} bytes)")
        return 0
    if not output.is_file():
        raise FileNotFoundError(f"report does not exist: {output}")
    if output.read_text(encoding="utf-8") != encoded:
        raise ValueError("report is stale; run build")
    print("PASS: aggregate report is deterministic, current, and privacy-safe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
