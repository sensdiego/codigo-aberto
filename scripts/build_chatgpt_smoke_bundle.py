#!/usr/bin/env python3
"""Gera sete skills autossuficientes para upload no ChatGPT."""

import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT
OUTPUT = ROOT / "dist" / "chatgpt-work-smoke"
SKILLS = (
    "novo-caso",
    "analise-documental",
    "analise-juridica-civel",
    "analise-jurisprudencial",
    "aprofundamento-juridico",
    "redacao-contencioso",
    "redacao-consultivo",
)
CPC_SKILLS = {
    "analise-documental",
    "analise-juridica-civel",
    "aprofundamento-juridico",
    "redacao-contencioso",
}
REWRITES = {
    "../../references/disciplina.md": "references/disciplina-compartilhada.md",
    "../../references/handoff.md": "references/handoff.md",
    "../../references/deliberacao.md": "references/deliberacao.md",
    "../../references/legislacao/cpc/README.md":
        "references/legislacao/cpc/README.md",
    "../../../references/legislacao/cpc/": "legislacao/cpc/",
}
OS_JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", "ehthumbs.db"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def is_os_junk(name: str) -> bool:
    return name in OS_JUNK_NAMES or name.startswith("._")


def rendered(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() != ".md":
        return data
    text = data.decode("utf-8")
    for source, target in REWRITES.items():
        text = text.replace(source, target)
    return text.encode("utf-8")


def skill_files(name: str) -> dict[str, bytes]:
    source = PLUGIN / "skills" / name
    files = {
        f"{name}/{path.relative_to(source).as_posix()}": rendered(path)
        for path in source.rglob("*")
        if path.is_file() and not is_os_junk(path.name)
    }
    discipline = (PLUGIN / "references" / "disciplina.md").read_bytes()
    files[f"{name}/references/disciplina-compartilhada.md"] = discipline
    files[f"{name}/references/handoff.md"] = (
        PLUGIN / "references" / "handoff.md"
    ).read_bytes()
    files[f"{name}/references/deliberacao.md"] = (
        PLUGIN / "references" / "deliberacao.md"
    ).read_bytes()
    if name in CPC_SKILLS:
        cpc = PLUGIN / "references" / "legislacao" / "cpc"
        for path in cpc.iterdir():
            if path.is_file() and not is_os_junk(path.name):
                files[f"{name}/references/legislacao/cpc/{path.name}"] = path.read_bytes()
    return files


def normalized_member(base: PurePosixPath, target: str) -> str:
    parts = []
    for part in (base / target).parts:
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                raise ValueError(f"link escapa da skill: {target}")
            parts.pop()
        else:
            parts.append(part)
    return PurePosixPath(*parts).as_posix()


def validate(name: str, files: dict[str, bytes]) -> None:
    expected_root = f"{name}/"
    if f"{name}/SKILL.md" not in files:
        raise ValueError(f"{name}: SKILL.md ausente")
    for member, data in files.items():
        if not member.startswith(expected_root):
            raise ValueError(f"{name}: arquivo fora da raiz: {member}")
        if not member.endswith(".md"):
            continue
        text = data.decode("utf-8")
        if "../../" in text:
            raise ValueError(f"{name}: referência externa remanescente em {member}")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlparse(target)
            if parsed.scheme or parsed.netloc or target.startswith(("#", "/")):
                continue
            resolved = normalized_member(PurePosixPath(member).parent, parsed.path)
            if resolved not in files:
                raise ValueError(f"{name}: link inexistente em {member}: {target}")
    has_cpc = any("CPC:" in data.decode("utf-8") for member, data in files.items()
                  if member.endswith(".md"))
    manifest = f"{name}/references/legislacao/cpc/manifest.json"
    if has_cpc and manifest not in files:
        raise ValueError(f"{name}: usa IDs CPC sem manifesto no bundle")


def write_zip(name: str, files: dict[str, bytes]) -> Path:
    target = OUTPUT / f"{name}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for member, data in sorted(files.items()):
            info = zipfile.ZipInfo(member, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return target


def build() -> dict:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    records = []
    for name in SKILLS:
        files = skill_files(name)
        validate(name, files)
        target = write_zip(name, files)
        records.append({
            "name": name,
            "file": target.name,
            "files": len(files),
            "bytes": target.stat().st_size,
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "includes_cpc": name in CPC_SKILLS,
        })
    manifest = {
        "schema_version": "1.0",
        "target": "ChatGPT Skills upload",
        "source": "silo-legal",
        "skills": records,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":
    try:
        result = build()
    except (OSError, UnicodeError, ValueError, zipfile.BadZipFile) as exc:
        print(f"FALHOU — {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(f"OK — {len(result['skills'])} bundles em {OUTPUT}")
