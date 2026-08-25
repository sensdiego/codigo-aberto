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
    "Makefile", "README.md", "RELEASING.md", "ROADMAP.md", "SECURITY.md", "data", "dist", "references",
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
        if not isinstance(scenario.get("prompt"), str) or not scenario.get("prompt", "").strip():
            errors.append(f"workflow {scenario_id or index}: prompt deve ser texto não vazio")
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


def check_new_file_placeholders():
    errors = []
    roots = [ROOT / "tests", PLUGIN / "references"]
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
        for name in ("README.md", "QUICKSTART.md", "CONTRIBUTING.md", "RELEASING.md", "SECURITY.md")
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
