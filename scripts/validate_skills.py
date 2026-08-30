#!/usr/bin/env python3
"""Valida a estrutura e os contratos locais do codigo-aberto.

Além da estrutura do plugin, valida links Markdown locais, fixtures de
workflow e a integridade referencial do corpus legislativo do CPC.

Uso:
    python3 scripts/validate_skills.py
"""

import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT
WORKFLOW_SKILLS = {
    "novo-caso",
    "analise-documental",
    "analise-juridica-civel",
    "analise-jurisprudencial",
    "aprofundamento-juridico",
    "redacao-contencioso",
    "redacao-consultivo",
}
PUBLIC_SKILLS = WORKFLOW_SKILLS | {"assinatura-silo", "pesquisa-silo"}
PUBLIC_ROOT_ENTRIES = {
    ".changes", ".claude-plugin", ".git", ".github", ".gitignore", ".ruff_cache",
    ".release-policy.toml", "CHANGELOG.md",
    "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "HANDOFF.md", "LICENSE", "QUICKSTART.md",
    "Makefile", "README.md", "RELEASING.md", "RFC-CA-001-adaptacao-casos-reais.md",
    "ROADMAP.md", "SECURITY.md", "data", "dist", "references",
    "scripts", "skills", "tests",
}
OS_JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", "ehthumbs.db"}
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CPC_REFERENCE_RE = re.compile(r"CPC:[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*(?::[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)*")
SILO_WAITLIST_URL = "https://silo.legal/#waitlist"
PROHIBITED_PUBLIC_CLAIMS = (
    "é comercial por assinatura",
    "o cadastro foi registrado",
    "requer assinatura ativa",
)
ADAPTATION_CONSUMER_REQUIREMENTS = {
    "references/handoff.md": (
        "A única versão reconhecida neste contrato é `case-adaptation-v1`",
        "`scope_status`",
        "Um handoff comum criado diretamente pelo usuário ou por outra skill permanece",
    ),
    "skills/novo-caso/SKILL.md": (
        "## Pacote adaptado",
        "Em `bloqueado`, não crie nem consuma intake",
        "Se não houver recibo de adaptação",
    ),
    "skills/analise-documental/SKILL.md": (
        "## Pacote adaptado",
        "Consuma o handoff opcional de análise documental somente quando cada achado",
        "fonte posterior não controla apenas por ser mais recente",
    ),
    "skills/analise-juridica-civel/SKILL.md": (
        "Várias frentes candidatas exigem delimitação",
        "Em `indeterminado`, delimite o regime",
        "`decidido` exige recibo de escolha humana",
    ),
    "skills/redacao-contencioso/SKILL.md": (
        "Não selecione módulo quando a frente ou o ato estiver `indeterminado`",
        "Módulo indicado pelo pacote é candidato, não ordem",
        "preserve a hierarquia declarada no pacote entre módulo-base e complementos",
        "Sem recibo de adaptação, aplique os pré-requisitos comuns",
    ),
}

def is_os_junk(name: str) -> bool:
    return name in OS_JUNK_NAMES or name.startswith("._")


def parse_frontmatter(text: str):
    """Retorna (frontmatter_dict, erro)."""
    if not text.startswith("---"):
        return None, "falta frontmatter (deve começar com ---)"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "frontmatter sem fechamento (---)"
    block = text[3:end]
    fm = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("<!--"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm, None


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)


def markdown_targets(path: Path):
    text = path.read_text(encoding="utf-8")
    for raw in MARKDOWN_LINK_RE.findall(text):
        target = raw.strip()
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")]
        else:
            target = target.split(maxsplit=1)[0]
        parsed = urlparse(target)
        if parsed.scheme or parsed.netloc or target.startswith(("#", "/")):
            continue
        local = unquote(parsed.path)
        if local:
            yield local


def check_markdown_links(path: Path):
    errors = []
    for target in markdown_targets(path):
        if not (path.parent / target).exists():
            errors.append(f"{path.relative_to(ROOT)}: link local inexistente: {target}")
    return errors


def heading_slug(heading: str):
    text = unicodedata.normalize("NFKD", heading).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"<[^>]+>", "", text.lower())
    text = re.sub(r"[^a-z0-9 _-]", "", text)
    return re.sub(r"[ _]+", "-", text).strip("-")


def has_markdown_anchor(path: Path, anchor: str):
    text = path.read_text(encoding="utf-8")
    explicit = re.compile(rf'<a\s+[^>]*(?:id|name)=["\']{re.escape(anchor)}["\'][^>]*>', re.I)
    if explicit.search(text):
        return True
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.M):
        if heading_slug(heading) == anchor:
            return True
    return False


def check_cpc_manifest():
    errors = []
    path = PLUGIN / "references" / "legislacao" / "cpc" / "manifest.json"
    if not path.exists():
        return ["falta references/legislacao/cpc/manifest.json"]

    data, err = load_json(path)
    if err:
        return [f"manifesto CPC inválido: {err}"]
    if not isinstance(data, dict):
        return ["manifesto CPC deve ser um objeto JSON"]

    source_url = data.get("source_url", "")
    host = (urlparse(source_url).hostname or "").lower()
    if urlparse(source_url).scheme != "https" or not (host == "planalto.gov.br" or host.endswith(".planalto.gov.br")):
        errors.append("manifesto CPC: source_url deve apontar por HTTPS para o Planalto")

    try:
        date.fromisoformat(data.get("updated_at", ""))
    except (TypeError, ValueError):
        errors.append("manifesto CPC: updated_at ausente ou inválido (use AAAA-MM-DD)")

    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("manifesto CPC: entries deve ser uma lista não vazia")
        entries = []

    ids = set()
    corpus_root = path.parent.resolve()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            errors.append(f"manifesto CPC: entry {index} não é objeto")
            continue
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not CPC_REFERENCE_RE.fullmatch(entry_id):
            errors.append(f"manifesto CPC: entry {index} tem id inválido")
        elif entry_id in ids:
            errors.append(f"manifesto CPC: id duplicado {entry_id}")
        else:
            ids.add(entry_id)

        file_name = entry.get("file")
        anchor = str(entry.get("anchor", "")).removeprefix("#")
        if not isinstance(file_name, str) or not file_name or not anchor:
            errors.append(f"manifesto CPC: {entry_id or index} precisa de file e anchor")
            continue
        target = (path.parent / file_name).resolve()
        try:
            target.relative_to(corpus_root)
        except ValueError:
            errors.append(f"manifesto CPC: {entry_id or index} aponta para fora do corpus")
            continue
        if not target.is_file():
            errors.append(f"manifesto CPC: arquivo inexistente para {entry_id or index}: {file_name}")
        elif not has_markdown_anchor(target, anchor):
            errors.append(f"manifesto CPC: âncora inexistente para {entry_id or index}: {anchor}")

    for md in (PLUGIN / "skills").rglob("*.md"):
        for ref in CPC_REFERENCE_RE.findall(md.read_text(encoding="utf-8")):
            if ref not in ids:
                errors.append(f"{md.relative_to(ROOT)}: referência CPC ausente do manifesto: {ref}")
    return errors


def check_workflow_fixtures():
    errors = []
    path = ROOT / "tests" / "fixtures" / "workflows.json"
    if not path.exists():
        return ["falta tests/fixtures/workflows.json"]
    data, err = load_json(path)
    if err:
        return [f"fixtures de workflow inválidas: {err}"]
    scenarios = data.get("scenarios") if isinstance(data, dict) else None
    if not isinstance(scenarios, list) or len(scenarios) < 12:
        return ["fixtures de workflow devem conter ao menos 12 scenarios"]

    existing = {p.name for p in (PLUGIN / "skills").iterdir() if p.is_dir()}
    ids = set()
    referenced = set()
    for index, scenario in enumerate(scenarios, start=1):
        if not isinstance(scenario, dict):
            errors.append(f"workflow {index}: cenário deve ser objeto")
            continue
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            errors.append(f"workflow {index}: id ausente")
        elif scenario_id in ids:
            errors.append(f"workflow {index}: id duplicado {scenario_id}")
        else:
            ids.add(scenario_id)
        for field in ("prompt", "expected_skill", "invariants"):
            if field not in scenario:
                errors.append(f"workflow {scenario_id or index}: falta {field}")
        prompt = scenario.get("prompt")
        if isinstance(prompt, str):
            if not prompt.strip():
                errors.append(
                    f"workflow {scenario_id or index}: prompt deve ser texto não vazio"
                )
            turn_count = 1
        elif isinstance(prompt, list):
            turn_count = len(prompt)
            if len(prompt) == 1:
                errors.append(
                    f"workflow {scenario_id or index}: prompt com um turno deve ser texto simples"
                )
            elif len(prompt) < 2 or not all(
                isinstance(item, str) and item.strip() for item in prompt
            ):
                errors.append(
                    f"workflow {scenario_id or index}: prompt deve ser lista de textos não vazios"
                )
        else:
            turn_count = 1
            errors.append(
                f"workflow {scenario_id or index}: prompt deve ser texto não vazio ou lista de turnos"
            )
        if "authorizing_turn" in scenario:
            authorizing_turn = scenario["authorizing_turn"]
            if authorizing_turn is not None and (
                not isinstance(authorizing_turn, int)
                or isinstance(authorizing_turn, bool)
                or not 1 <= authorizing_turn <= turn_count
            ):
                errors.append(
                    f"workflow {scenario_id or index}: authorizing_turn deve ser null ou inteiro entre 1 e {turn_count}"
                )
        expected = scenario.get("expected_skill")
        if isinstance(expected, str):
            referenced.add(expected)
        else:
            errors.append(f"workflow {scenario_id or index}: expected_skill deve ser texto")
        invariants = scenario.get("invariants")
        if not isinstance(invariants, list) or not invariants or not all(isinstance(item, str) and item.strip() for item in invariants):
            errors.append(f"workflow {scenario_id or index}: invariants deve ser lista não vazia de textos")
        setup_files = scenario.get("setup_files")
        if setup_files is not None:
            if not isinstance(setup_files, dict) or not setup_files:
                errors.append(f"workflow {scenario_id or index}: setup_files deve ser objeto não vazio")
            else:
                for name, content in setup_files.items():
                    relative = isinstance(name, str) and name.strip() and not name.startswith("/") and ".." not in name.split("/")
                    if not relative or not isinstance(content, str):
                        errors.append(f"workflow {scenario_id or index}: setup_files exige caminhos relativos seguros e conteúdo textual")
                        break

    for skill in sorted(WORKFLOW_SKILLS | referenced):
        if skill not in existing:
            errors.append(f"skill de workflow ausente: {skill}")
    return errors


def check_adaptation_fixtures():
    errors = []

    def allowed(value, choices):
        return isinstance(value, str) and value in choices

    path = ROOT / "tests" / "fixtures" / "adaptacao-casos-reais.json"
    if not path.exists():
        return ["falta tests/fixtures/adaptacao-casos-reais.json"]
    data, err = load_json(path)
    if err or not isinstance(data, dict):
        return [f"fixtures de adaptação inválidas: {err or 'objeto esperado'}"]
    if data.get("schema_version") != "case-adaptation-fixtures-v1":
        errors.append("fixtures de adaptação: schema_version deve ser case-adaptation-fixtures-v1")
    if data.get("contract_version") != "case-adaptation-v1":
        errors.append("fixtures de adaptação: contract_version deve ser case-adaptation-v1")

    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list):
        return [*errors, "fixtures de adaptação: scenarios deve ser lista"]
    expected_ids = {f"A{index:02d}" for index in range(1, 15)}
    actual_ids = {
        scenario.get("id")
        for scenario in scenarios
        if isinstance(scenario, dict) and isinstance(scenario.get("id"), str)
    }
    if actual_ids != expected_ids or len(scenarios) != len(expected_ids):
        errors.append("fixtures de adaptação devem conter exatamente A01–A14, sem duplicatas")

    allowed_eligibility = {"bloqueado", "parcial_utilizavel", "integral"}
    allowed_handoffs = {"intake", "analise_documental"}
    allowed_scope = {
        "suportado",
        "suportado_condicionado",
        "nao_suportado",
        "indeterminado",
    }
    allowed_front_natures = {
        "processo",
        "recurso",
        "incidente",
        "reconvencao",
        "execucao",
        "credito",
        "administrativo",
        "dependencia",
    }
    allowed_relations = {"principal", "dependente", "paralelo", "sucessor", "apenso"}
    allowed_front_statuses = {"ativa", "dependente", "latente", "encerrada", "indeterminada"}
    allowed_act_statuses = {"demonstrado", "candidato", "decidido", "indeterminado", "sem_ato"}
    allowed_coverage = {"integral", "parcial", "bloqueada"}
    allowed_deadlines = {"verificado", "pendente", "nao_aplicavel"}
    allowed_finding_states = {
        "confirmado",
        "informado pelo usuario",
        "inferido",
        "hipotese",
        "contraditado",
        "pendente",
    }
    allowed_deltas = {"confirma", "complementa", "contradiz", "substitui", "nao_afeta"}
    allowed_conflict_statuses = {"aberto", "resolvido"}
    modules_root = ROOT / "skills" / "redacao-contencioso" / "references" / "modulos"
    existing_modules = {module.stem for module in modules_root.glob("*.md")}
    observed_scope = set()

    for index, scenario in enumerate(scenarios, start=1):
        if not isinstance(scenario, dict):
            errors.append(f"adaptação {index}: cenário deve ser objeto")
            continue
        scenario_id = scenario.get("id") or index
        for field in (
            "id",
            "title",
            "eligibility",
            "handoffs",
            "analysis_eligible",
            "fronts",
            "findings",
            "conflicts",
            "blockers",
            "invariants",
        ):
            if field not in scenario:
                errors.append(f"adaptação {scenario_id}: falta {field}")

        if not isinstance(scenario.get("title"), str) or not scenario["title"].strip():
            errors.append(f"adaptação {scenario_id}: title deve ser texto não vazio")
        eligibility = scenario.get("eligibility")
        if not allowed(eligibility, allowed_eligibility):
            errors.append(f"adaptação {scenario_id}: eligibility inválida")

        handoffs = scenario.get("handoffs")
        if (
            not isinstance(handoffs, list)
            or any(not isinstance(item, str) for item in handoffs)
            or len(handoffs) != len(set(handoffs))
            or any(item not in allowed_handoffs for item in handoffs)
        ):
            errors.append(f"adaptação {scenario_id}: handoffs inválidos ou duplicados")
            handoffs = []
        if eligibility == "bloqueado" and handoffs:
            errors.append(f"adaptação {scenario_id}: bloqueado não pode emitir handoff")
        if eligibility in ("parcial_utilizavel", "integral") and "intake" not in handoffs:
            errors.append(f"adaptação {scenario_id}: pacote utilizável exige intake")

        analysis_eligible = scenario.get("analysis_eligible")
        if not isinstance(analysis_eligible, bool):
            errors.append(f"adaptação {scenario_id}: analysis_eligible deve ser booleano")
        elif analysis_eligible != ("analise_documental" in handoffs):
            errors.append(
                f"adaptação {scenario_id}: analise_documental deve acompanhar analysis_eligible"
            )

        fronts = scenario.get("fronts")
        if not isinstance(fronts, list):
            errors.append(f"adaptação {scenario_id}: fronts deve ser lista")
            fronts = []
        if eligibility != "bloqueado" and not fronts:
            errors.append(f"adaptação {scenario_id}: pacote utilizável exige ao menos uma frente")
        if eligibility == "bloqueado" and fronts:
            errors.append(f"adaptação {scenario_id}: bloqueado não pode expor frentes")
        front_ids = set()
        for front_index, front in enumerate(fronts, start=1):
            label = f"adaptação {scenario_id} frente {front_index}"
            if not isinstance(front, dict):
                errors.append(f"{label}: deve ser objeto")
                continue
            front_id = front.get("front_id")
            if not isinstance(front_id, str) or not front_id.strip():
                errors.append(f"{label}: front_id ausente")
            elif front_id in front_ids:
                errors.append(f"{label}: front_id duplicado {front_id}")
            else:
                front_ids.add(front_id)
            scope = front.get("scope_status")
            if not allowed(scope, allowed_scope):
                errors.append(f"{label}: scope_status inválido")
            else:
                observed_scope.add(scope)
            if not allowed(front.get("nature"), allowed_front_natures):
                errors.append(f"{label}: nature inválida")
            if not allowed(front.get("relation"), allowed_relations):
                errors.append(f"{label}: relation inválida")
            front_status = front.get("status")
            if not allowed(front_status, allowed_front_statuses):
                errors.append(f"{label}: status inválido")
            coverage = front.get("coverage")
            if not allowed(coverage, allowed_coverage):
                errors.append(f"{label}: coverage inválida")
            for field in ("represented_role", "phase", "current_objective"):
                if not isinstance(front.get(field), str) or not front[field].strip():
                    errors.append(f"{label}: {field} deve ser texto não vazio")

            event = front.get("controlling_event")
            if not isinstance(event, dict) or any(
                not isinstance(event.get(field), str) or not event[field].strip()
                for field in ("source_ref", "locator")
            ):
                errors.append(f"{label}: controlling_event exige source_ref e locator")

            act = front.get("act")
            if not isinstance(act, dict):
                errors.append(f"{label}: act deve ser objeto")
                continue
            act_status = act.get("status")
            module = act.get("module")
            complements = act.get("complements")
            if not allowed(act_status, allowed_act_statuses):
                errors.append(f"{label}: act.status inválido")
            if module is not None and not allowed(module, existing_modules):
                errors.append(f"{label}: módulo inexistente {module}")
            if module == "tutela-urgencia-evidencia":
                errors.append(f"{label}: tutela não pode ser módulo-base")
            if (
                not isinstance(complements, list)
                or any(not isinstance(item, str) for item in complements)
                or len(complements) != len(set(complements))
                or any(item != "tutela-urgencia-evidencia" for item in complements)
            ):
                errors.append(f"{label}: complements aceita somente tutela sem duplicata")
                complements = []
            if complements and module is None:
                errors.append(f"{label}: complemento exige módulo-base")
            if scope in ("nao_suportado", "indeterminado") and module is not None:
                errors.append(f"{label}: escopo {scope} não pode selecionar módulo")
            if front_status == "indeterminada" and module is not None:
                errors.append(f"{label}: frente indeterminada não pode selecionar módulo")
            if coverage == "bloqueada" and module is not None:
                errors.append(f"{label}: cobertura bloqueada não pode selecionar módulo")
            if act_status in ("indeterminado", "sem_ato") and (module is not None or complements):
                errors.append(f"{label}: ato {act_status} não pode selecionar módulo")
            decision_receipt = act.get("decision_receipt")
            if not isinstance(decision_receipt, bool):
                errors.append(f"{label}: decision_receipt deve ser booleano")
            elif act_status == "decidido" and not decision_receipt:
                errors.append(f"{label}: ato decidido exige recibo de decisão")

            deadline = front.get("deadline")
            if not isinstance(deadline, dict) or not allowed(
                deadline.get("status"), allowed_deadlines
            ):
                errors.append(f"{label}: deadline inválido")
            elif deadline["status"] == "verificado" and any(
                not isinstance(deadline.get(field), str) or not deadline[field].strip()
                for field in ("event_source", "rule_source")
            ):
                errors.append(f"{label}: prazo verificado exige evento e regra")
            dependencies = front.get("dependencies")
            if not isinstance(dependencies, list) or any(
                not isinstance(item, str) or not item.strip() for item in dependencies
            ):
                errors.append(f"{label}: dependencies deve ser lista de textos")
            elif scope == "suportado_condicionado" and not dependencies:
                errors.append(f"{label}: escopo condicionado exige dependência nomeada")

        if eligibility == "integral" and any(
            isinstance(front, dict) and front.get("coverage") != "integral" for front in fronts
        ):
            errors.append(f"adaptação {scenario_id}: pacote integral exige frentes integrais")

        findings = scenario.get("findings")
        if not isinstance(findings, list):
            errors.append(f"adaptação {scenario_id}: findings deve ser lista")
            findings = []
        if analysis_eligible is True and not findings:
            errors.append(f"adaptação {scenario_id}: análise elegível exige achados")
        if analysis_eligible is False and findings:
            errors.append(f"adaptação {scenario_id}: achados analíticos exigem análise elegível")
        finding_ids = set()
        for finding_index, finding in enumerate(findings, start=1):
            label = f"adaptação {scenario_id} achado {finding_index}"
            if not isinstance(finding, dict):
                errors.append(f"{label}: deve ser objeto")
                continue
            finding_id = finding.get("id")
            if not isinstance(finding_id, str) or not finding_id.strip():
                errors.append(f"{label}: id ausente")
            elif finding_id in finding_ids:
                errors.append(f"{label}: id duplicado {finding_id}")
            else:
                finding_ids.add(finding_id)
            if not allowed(finding.get("state"), allowed_finding_states):
                errors.append(f"{label}: state inválido")
            for field in ("source_ref", "locator"):
                if not isinstance(finding.get(field), str) or not finding[field].strip():
                    errors.append(f"{label}: {field} deve ser texto não vazio")
            if finding.get("state") == "confirmado" and (
                not isinstance(finding.get("confirmation_scope"), str)
                or not finding["confirmation_scope"].strip()
            ):
                errors.append(f"{label}: confirmado exige confirmation_scope")

        conflicts = scenario.get("conflicts")
        if not isinstance(conflicts, list):
            errors.append(f"adaptação {scenario_id}: conflicts deve ser lista")
            conflicts = []
        for conflict_index, conflict in enumerate(conflicts, start=1):
            label = f"adaptação {scenario_id} conflito {conflict_index}"
            if not isinstance(conflict, dict):
                errors.append(f"{label}: deve ser objeto")
                continue
            if not allowed(conflict.get("delta"), allowed_deltas):
                errors.append(f"{label}: delta inválido")
            conflict_status = conflict.get("status")
            if not allowed(conflict_status, allowed_conflict_statuses):
                errors.append(f"{label}: status inválido")
            sources = conflict.get("sources")
            if not isinstance(sources, list) or len(sources) < 2 or any(
                not isinstance(item, str) or not item.strip() for item in sources
            ):
                errors.append(f"{label}: sources exige ao menos duas fontes")
                sources = []
            controlling_source = conflict.get("controlling_source")
            blocked_claims = conflict.get("blocked_claims")
            if not isinstance(blocked_claims, list) or any(
                not isinstance(item, str) or not item.strip() for item in blocked_claims
            ):
                errors.append(f"{label}: blocked_claims deve ser lista de textos")
                blocked_claims = []
            if conflict_status == "aberto":
                if controlling_source is not None:
                    errors.append(f"{label}: conflito aberto não pode escolher fonte controladora")
                if not blocked_claims:
                    errors.append(f"{label}: conflito aberto deve bloquear conclusão dependente")
            if conflict_status == "resolvido":
                if controlling_source not in sources:
                    errors.append(f"{label}: conflito resolvido exige fonte controladora listada")
                if blocked_claims:
                    errors.append(f"{label}: conflito resolvido não mantém conclusão bloqueada")

        for field in ("blockers", "invariants"):
            values = scenario.get(field)
            if not isinstance(values, list) or any(
                not isinstance(item, str) or not item.strip() for item in values
            ):
                errors.append(f"adaptação {scenario_id}: {field} deve ser lista de textos")
        invariants = scenario.get("invariants")
        if isinstance(invariants, list) and len(invariants) < 2:
            errors.append(f"adaptação {scenario_id}: invariants exige ao menos dois itens")
    if observed_scope != allowed_scope:
        errors.append("fixtures de adaptação devem cobrir os quatro estados de escopo")
    return errors


def check_adaptation_consumers():
    errors = []
    for relative, markers in ADAPTATION_CONSUMER_REQUIREMENTS.items():
        path = ROOT / relative
        if not path.exists():
            errors.append(f"consumidor de adaptação ausente: {relative}")
            continue
        text = " ".join(path.read_text(encoding="utf-8").split())
        for marker in markers:
            if " ".join(marker.split()) not in text:
                errors.append(f"{relative}: falta contrato de adaptação: {marker}")
    return errors


def check_adaptation_workflow_fixtures():
    errors = []
    path = ROOT / "tests" / "fixtures" / "adaptacao-workflows.json"
    case_path = ROOT / "tests" / "fixtures" / "adaptacao-casos-reais.json"
    data, err = load_json(path)
    case_data, case_err = load_json(case_path)
    if err or not isinstance(data, dict):
        return [f"fixture comportamental de adaptação inválida: {err or 'objeto esperado'}"]
    if case_err or not isinstance(case_data, dict):
        return [f"fixture estrutural de adaptação inválida: {case_err or 'objeto esperado'}"]
    if data.get("schema_version") != "adaptation-behavior-workflows-v1":
        errors.append("fixture comportamental: schema_version inválida")
    if data.get("case_fixture") != "adaptacao-casos-reais.json":
        errors.append("fixture comportamental deve reutilizar adaptacao-casos-reais.json")

    scenarios = data.get("scenarios")
    cases = case_data.get("scenarios")
    if not isinstance(scenarios, list):
        return [*errors, "fixture comportamental: scenarios deve ser lista"]
    if not isinstance(cases, list):
        return [*errors, "fixture estrutural: scenarios deve ser lista"]
    case_findings = {
        case.get("id"): len(case.get("findings", []))
        for case in cases
        if isinstance(case, dict)
        and isinstance(case.get("id"), str)
        and isinstance(case.get("findings"), list)
    }
    expected_case_ids = {f"A{index:02d}" for index in range(1, 15)}
    expected_consumers = {
        "novo-caso",
        "analise-documental",
        "analise-juridica-civel",
        "redacao-contencioso",
    }
    scenario_ids = set()
    referenced_cases = set()
    covered_consumers = set()
    canary_cases = set()
    for index, scenario in enumerate(scenarios, start=1):
        if not isinstance(scenario, dict):
            errors.append(f"fixture comportamental {index}: cenário deve ser objeto")
            continue
        scenario_id = scenario.get("id")
        case_id = scenario.get("adaptation_case_id")
        label = scenario_id if isinstance(scenario_id, str) else index
        if not isinstance(scenario_id, str) or not scenario_id:
            errors.append(f"fixture comportamental {index}: id ausente")
        elif scenario_id in scenario_ids:
            errors.append(f"fixture comportamental {scenario_id}: id duplicado")
        else:
            scenario_ids.add(scenario_id)
        if not isinstance(case_id, str) or case_id not in expected_case_ids:
            errors.append(f"fixture comportamental {label}: adaptation_case_id inválido")
        elif case_id in referenced_cases:
            errors.append(f"fixture comportamental {label}: caso repetido {case_id}")
        else:
            referenced_cases.add(case_id)

        prompt = scenario.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"fixture comportamental {label}: prompt deve ser texto")
        consumer = scenario.get("expected_skill")
        if not isinstance(consumer, str) or consumer not in expected_consumers:
            errors.append(f"fixture comportamental {label}: consumidor inválido")
        else:
            covered_consumers.add(consumer)
        facts = scenario.get("package_facts")
        finding_count = case_findings.get(case_id, 0) if isinstance(case_id, str) else 0
        minimum_facts = max(1, finding_count)
        if (
            not isinstance(facts, list)
            or len(facts) < minimum_facts
            or not all(isinstance(fact, str) and fact.strip() for fact in facts)
        ):
            errors.append(
                f"fixture comportamental {label}: package_facts insuficientes"
            )
        invariants = scenario.get("invariants")
        if (
            not isinstance(invariants, list)
            or len(invariants) < 3
            or not all(
                isinstance(invariant, str) and invariant.strip()
                for invariant in invariants
            )
        ):
            errors.append(f"fixture comportamental {label}: invariants exige três textos")
        canary = scenario.get("canary")
        if not isinstance(canary, bool):
            errors.append(f"fixture comportamental {label}: canary deve ser booleano")
        elif canary and isinstance(case_id, str):
            canary_cases.add(case_id)
        if consumer == "redacao-contencioso" and scenario.get("authorizing_turn", "absent") is not None:
            errors.append(
                f"fixture comportamental {label}: redação deve manter authorizing_turn null"
            )
        if "setup_files" in scenario:
            errors.append(
                f"fixture comportamental {label}: setup_files é materializado pelo runner"
            )

    if referenced_cases != expected_case_ids or len(scenarios) != len(expected_case_ids):
        errors.append("fixture comportamental deve cobrir A01–A14 exatamente uma vez")
    if covered_consumers != expected_consumers:
        errors.append("fixture comportamental deve cobrir os quatro consumidores")
    if canary_cases != {"A01", "A02", "A03", "A04"}:
        errors.append("canário comportamental deve conter exatamente A01–A04")
    return errors


def check_new_file_placeholders():
    errors = []
    roots = [
        ROOT / "RFC-CA-001-adaptacao-casos-reais.md",
        ROOT / "tests",
        PLUGIN / "references",
    ]
    roots.extend(PLUGIN / "skills" / name for name in WORKFLOW_SKILLS)
    for root in roots:
        if not root.exists():
            continue
        paths = [root] if root.is_file() else root.rglob("*")
        for path in paths:
            if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml"}:
                if "[PLACEHOLDER]" in path.read_text(encoding="utf-8"):
                    errors.append(f"{path.relative_to(ROOT)}: contém [PLACEHOLDER]")
    return errors


def check_silo_access_copy():
    errors = []
    paths = [
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / "references" / "disciplina.md",
        ROOT / "skills" / "assinatura-silo" / "SKILL.md",
        ROOT / "skills" / "pesquisa-silo" / "SKILL.md",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for claim in PROHIBITED_PUBLIC_CLAIMS:
            if claim in text:
                errors.append(
                    f"{path.relative_to(ROOT)}: claim comercial incompatível com a validação privada: {claim}"
                )
    access_skill = paths[2].read_text(encoding="utf-8")
    if SILO_WAITLIST_URL not in access_skill:
        errors.append("skill assinatura-silo não aponta para a lista de espera oficial")
    return errors

def check_skill(path: Path):
    errors = []
    text = path.read_text(encoding="utf-8")
    fm, err = parse_frontmatter(text)
    if err:
        return [err]
    if "name" not in fm:
        errors.append("frontmatter sem campo 'name'")
    else:
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", fm["name"]):
            errors.append(f"name '{fm['name']}' não é kebab-case (só minúsculas, hífens)")
    if "description" not in fm:
        errors.append("frontmatter sem campo 'description'")
    elif len(fm["description"]) < 20:
        errors.append("description muito curta (<20 chars) — descreva o que faz e QUANDO usar")
    if "O que esta skill não faz" not in text:
        errors.append("falta seção 'O que esta skill não faz'")
    if "rascunho para revisão do advogado" not in text.lower() and "revisão e validação obrigatória" not in text.lower():
        errors.append("falta menção a rascunho/revisão obrigatória do advogado (disclaimer)")
    if "[review]" not in text and "[model knowledge — verify]" not in text and "[verificar]" not in text:
        errors.append("nenhuma tag de verificação ([verificar]/[review]) — toda skill deve sinalizar incerteza")
    return errors

def check_plugin(plugin_dir: Path, expected_name: str):
    errors = []
    pj = plugin_dir / ".claude-plugin" / "plugin.json"
    if not pj.exists():
        return [f"falta {plugin_dir.name}/.claude-plugin/plugin.json"]
    data = json.loads(pj.read_text(encoding="utf-8"))
    for field in ("name", "version", "description", "author"):
        if field not in data:
            errors.append(f"plugin.json de {plugin_dir.name} falta campo '{field}'")
    if "name" in data and data["name"] != expected_name:
        errors.append(f"plugin.json name '{data['name']}' != marketplace '{expected_name}'")
    skills = plugin_dir / "skills"
    if skills.exists():
        for skill_dir in skills.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    errors.append(f"skill {skill_dir.name} sem SKILL.md")
                else:
                    for e in check_skill(skill_md):
                        errors.append(f"skill/{skill_dir.name}: {e}")
    return errors

def main():
    errors = []

    root_entries = {path.name for path in ROOT.iterdir() if not is_os_junk(path.name)}
    for name in sorted(root_entries - PUBLIC_ROOT_ENTRIES):
        errors.append(f"entrada não prevista na distribuição pública: {name}")

    # Marketplace
    mkt = ROOT / ".claude-plugin" / "marketplace.json"
    marketplace = None
    if not mkt.exists():
        errors.append("falta .claude-plugin/marketplace.json")
    else:
        marketplace, err = load_json(mkt)
        if err or not isinstance(marketplace, dict):
            errors.append(f"marketplace.json inválido: {err or 'objeto esperado'}")
            marketplace = None
        plugins = (marketplace or {}).get("plugins", [])
        actual_plugins = [
            (plugin.get("name"), plugin.get("source"))
            for plugin in plugins
            if isinstance(plugin, dict)
        ]
        if actual_plugins != [("silo-legal", "./")]:
            errors.append("marketplace deve listar somente o plugin silo-legal")
        for plugin in plugins:
            src = ROOT / plugin["source"]
            if not src.exists():
                errors.append(f"marketplace aponta para fonte inexistente: {plugin['source']}")
            else:
                for e in check_plugin(src, plugin["name"]):
                    errors.append(f"plugin {plugin['name']}: {e}")

    if (ROOT / "silo-litigio").exists():
        errors.append("árvore legada silo-litigio ainda existe")
    if (ROOT / "silo-legal").exists():
        errors.append("subárvore silo-legal não deve existir; as skills ficam na raiz")

    # Arquivos raiz essenciais
    for req in ("README.md", "QUICKSTART.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md"):
        if not (ROOT / req).exists():
            errors.append(f"falta arquivo raiz {req}")

    skills_root = ROOT / "skills"
    existing_skills = {
        path.name for path in skills_root.iterdir() if path.is_dir()
    } if skills_root.exists() else set()
    for name in sorted(PUBLIC_SKILLS - existing_skills):
        errors.append(f"skill pública ausente: {name}")
    for name in sorted(existing_skills - PUBLIC_SKILLS):
        errors.append(f"skill não prevista na distribuição pública: {name}")

    link_sources = {
        ROOT / name
        for name in (
            "README.md",
            "QUICKSTART.md",
            "CONTRIBUTING.md",
            "RELEASING.md",
            "RFC-CA-001-adaptacao-casos-reais.md",
            "SECURITY.md",
        )
    }
    link_sources.update(ROOT.rglob("SKILL.md"))
    for references in ROOT.rglob("references"):
        if references.is_dir():
            link_sources.update(references.rglob("*.md"))
    for path in sorted(link_sources):
        errors.extend(check_markdown_links(path))

    errors.extend(check_new_file_placeholders())
    errors.extend(check_silo_access_copy())
    errors.extend(check_workflow_fixtures())
    errors.extend(check_adaptation_fixtures())
    errors.extend(check_adaptation_consumers())
    errors.extend(check_adaptation_workflow_fixtures())
    errors.extend(check_cpc_manifest())

    if errors:
        print(f"FALHOU — {len(errors)} problema(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK — estrutura pública válida: marketplace, skills, referências e fixtures.")
    print(f"  Skills: {len(PUBLIC_SKILLS)} publicadas em skills/")

if __name__ == "__main__":
    main()
