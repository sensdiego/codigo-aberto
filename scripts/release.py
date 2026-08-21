#!/usr/bin/env python3
"""Versionamento, changelog e releases do Código Aberto, sem dependências."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Literal, Sequence

ROOT = Path(__file__).resolve().parent.parent
KINDS = ("none", "patch", "minor", "major")
CATEGORIES = ("Added", "Changed", "Fixed", "Security", "Removed")
KIND_RANK = {kind: rank for rank, kind in enumerate(KINDS)}
DEFAULT_CATEGORY = {
    "none": "Changed",
    "patch": "Fixed",
    "minor": "Added",
    "major": "Changed",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
RELEASE_HEADING_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})$", re.M)


class ReleaseError(RuntimeError):
    pass


@dataclass(frozen=True, order=True)
class SemVer:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> "SemVer":
        match = VERSION_RE.fullmatch(value)
        if not match:
            raise ReleaseError(f"invalid semantic version: {value!r}")
        return cls(*(int(part) for part in match.groups()))

    def bump(self, kind: str) -> "SemVer":
        if kind == "major":
            return SemVer(self.major + 1, 0, 0)
        if kind == "minor":
            return SemVer(self.major, self.minor + 1, 0)
        if kind == "patch":
            return SemVer(self.major, self.minor, self.patch + 1)
        raise ReleaseError(f"cannot bump version with kind: {kind!r}")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class ReleasePolicy:
    root: Path
    adapter: str
    manifest: str
    package_name: str
    changelog: str
    fragments_dir: str
    tag_prefix: str
    release_paths: tuple[str, ...]
    non_release_paths: tuple[str, ...]


@dataclass(frozen=True)
class ChangeFragment:
    path: Path
    kind: Literal["none", "patch", "minor", "major"]
    category: str
    summary: str
    areas: tuple[str, ...]
    issue: str | None
    breaking: str | None

    def public_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "path": self.path.as_posix(),
            "kind": self.kind,
            "category": self.category,
            "summary": self.summary,
            "areas": list(self.areas),
        }
        if self.issue:
            payload["issue"] = self.issue
        if self.breaking:
            payload["breaking"] = self.breaking
        return payload


@dataclass(frozen=True)
class Impact:
    release: tuple[str, ...]
    non_release: tuple[str, ...]
    ambiguous: tuple[str, ...]
    requires_fragment: bool


@dataclass(frozen=True)
class ReleasePlan:
    current_version: str
    next_version: str | None
    bootstrap: bool
    publish: bool
    changed: bool
    increment: str | None
    fragments: tuple[str, ...]
    fragments_digest: str | None


def _run(
    command: Sequence[str], root: Path, *, check: bool = True
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command, cwd=root, capture_output=True, text=True, check=False
    )
    if check and result.returncode != 0:
        raise ReleaseError(
            result.stderr.strip() or result.stdout.strip() or "command failed"
        )
    return result


def load_policy(root: Path = ROOT) -> ReleasePolicy:
    policy_path = root / ".release-policy.toml"
    try:
        raw = tomllib.loads(policy_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ReleaseError(f"invalid release policy: {exc}") from exc
    required = {
        "schema",
        "adapter",
        "manifest",
        "manifest_kind",
        "package_name",
        "changelog",
        "fragments_dir",
        "tag_prefix",
        "current_version_source",
        "paths",
    }
    missing = sorted(required - raw.keys())
    if missing:
        raise ReleaseError(f"release policy missing fields: {', '.join(missing)}")
    if raw["schema"] != 1:
        raise ReleaseError("release policy schema must be 1")
    if raw["adapter"] != "codigo-aberto-release-python-v1":
        raise ReleaseError("unsupported release adapter")
    if raw["manifest_kind"] != "json" or raw["current_version_source"] != "version":
        raise ReleaseError("manifest must be JSON with version as source")
    paths = raw["paths"]
    if not isinstance(paths, dict):
        raise ReleaseError("release policy paths must be a table")
    release_paths = _string_tuple(paths.get("release"), "paths.release")
    non_release_paths = _string_tuple(paths.get("non_release"), "paths.non_release")
    policy = ReleasePolicy(
        root=root.resolve(),
        adapter=raw["adapter"],
        manifest=raw["manifest"],
        package_name=raw["package_name"],
        changelog=raw["changelog"],
        fragments_dir=raw["fragments_dir"],
        tag_prefix=raw["tag_prefix"],
        release_paths=release_paths,
        non_release_paths=non_release_paths,
    )
    if not (policy.root / policy.manifest).is_file():
        raise ReleaseError(f"manifest not found: {policy.manifest}")
    read_manifest_version(policy)
    return policy


def _string_tuple(value: object, label: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(item, str) for item in value)
    ):
        raise ReleaseError(f"{label} must be a non-empty string array")
    return tuple(value)


def read_manifest_version(policy: ReleasePolicy) -> SemVer:
    try:
        data = json.loads((policy.root / policy.manifest).read_text(encoding="utf-8"))
        value = data["version"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ReleaseError(
            f"cannot read version from {policy.manifest}: {exc}"
        ) from exc
    if not isinstance(value, str):
        raise ReleaseError("manifest version must be a string")
    return SemVer.parse(value)


def load_fragment(path: Path, root: Path) -> ChangeFragment:
    if not NAME_RE.fullmatch(path.stem) or path.suffix != ".json":
        raise ReleaseError(f"invalid fragment filename: {path.name!r}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleaseError(f"invalid fragment {path.name}: {exc}") from exc
    if not isinstance(raw, dict) or raw.get("schema") != 1:
        raise ReleaseError(f"fragment {path.name} must use schema 1")
    kind = raw.get("kind")
    category = raw.get("category")
    summary = raw.get("summary")
    areas = raw.get("areas", [])
    issue = raw.get("issue")
    breaking = raw.get("breaking")
    if kind not in KINDS:
        raise ReleaseError(f"fragment {path.name} has invalid kind: {kind!r}")
    if category not in CATEGORIES:
        raise ReleaseError(f"fragment {path.name} has invalid category: {category!r}")
    if not isinstance(summary, str) or not summary.strip() or "\n" in summary:
        raise ReleaseError(f"fragment {path.name} summary must be one non-empty line")
    if not isinstance(areas, list) or not all(
        isinstance(area, str) and area for area in areas
    ):
        raise ReleaseError(f"fragment {path.name} areas must be a string array")
    if issue is not None and not isinstance(issue, str):
        raise ReleaseError(f"fragment {path.name} issue must be a string")
    if breaking is not None and (not isinstance(breaking, str) or not breaking.strip()):
        raise ReleaseError(f"fragment {path.name} breaking must be non-empty text")
    if kind == "major" and not breaking:
        raise ReleaseError(f"fragment {path.name} major change requires breaking")
    return ChangeFragment(
        path=path.relative_to(root),
        kind=kind,
        category=category,
        summary=summary.strip(),
        areas=tuple(areas),
        issue=issue,
        breaking=breaking,
    )


def load_fragments(policy: ReleasePolicy) -> tuple[ChangeFragment, ...]:
    directory = policy.root / policy.fragments_dir
    if not directory.is_dir():
        raise ReleaseError(f"fragments directory not found: {policy.fragments_dir}")
    return tuple(
        load_fragment(path, policy.root) for path in sorted(directory.glob("*.json"))
    )


def create_fragment(
    policy: ReleasePolicy,
    *,
    name: str,
    kind: str,
    category: str | None,
    summary: str,
    issue: str | None = None,
    breaking: str | None = None,
) -> Path:
    if not NAME_RE.fullmatch(name):
        raise ReleaseError(f"invalid fragment name: {name!r}")
    if kind not in KINDS:
        raise ReleaseError(f"invalid fragment kind: {kind!r}")
    resolved_category = category or DEFAULT_CATEGORY[kind]
    if resolved_category not in CATEGORIES:
        raise ReleaseError(f"invalid fragment category: {category!r}")
    if not summary.strip() or "\n" in summary:
        raise ReleaseError("fragment summary must be one non-empty line")
    if kind == "major" and not breaking:
        raise ReleaseError("major fragment requires breaking")
    directory = policy.root / policy.fragments_dir
    target = directory / f"{name}.json"
    if target.exists():
        raise ReleaseError(f"fragment already exists: {target.name}")
    payload: dict[str, object] = {
        "schema": 1,
        "kind": kind,
        "category": resolved_category,
        "summary": summary,
    }
    if issue:
        payload["issue"] = issue
    if breaking:
        payload["breaking"] = breaking
    directory.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    load_fragment(target, policy.root)
    return target


def changed_paths(root: Path, ref_range: str) -> tuple[str, ...]:
    commands = (
        ("git", "diff", "--name-only", "--diff-filter=ACMRD", ref_range),
        ("git", "diff", "--name-only", "--cached"),
        ("git", "diff", "--name-only"),
        ("git", "ls-files", "--others", "--exclude-standard"),
    )
    found: set[str] = set()
    for command in commands:
        result = _run(command, root, check=False)
        if result.returncode == 0:
            found.update(line for line in result.stdout.splitlines() if line)
        elif command[-1] == ref_range:
            raise ReleaseError(result.stderr.strip() or f"cannot inspect {ref_range}")
    return tuple(sorted(found))


def classify_paths(policy: ReleasePolicy, paths: Sequence[str]) -> Impact:
    release: list[str] = []
    non_release: list[str] = []
    ambiguous: list[str] = []
    for path in sorted(set(paths)):
        if any(fnmatch.fnmatchcase(path, pattern) for pattern in policy.release_paths):
            release.append(path)
        elif any(
            fnmatch.fnmatchcase(path, pattern) for pattern in policy.non_release_paths
        ):
            non_release.append(path)
        else:
            ambiguous.append(path)
    return Impact(
        release=tuple(release),
        non_release=tuple(non_release),
        ambiguous=tuple(ambiguous),
        requires_fragment=bool(release or ambiguous),
    )


def fragments_digest(fragments: Sequence[ChangeFragment], root: Path) -> str | None:
    if not fragments:
        return None
    digest = hashlib.sha256()
    for fragment in sorted(fragments, key=lambda item: item.path.as_posix()):
        digest.update(fragment.path.as_posix().encode())
        digest.update((root / fragment.path).read_bytes())
    return digest.hexdigest()


def _semantic_tags(policy: ReleasePolicy) -> tuple[SemVer, ...]:
    result = _run(
        ["git", "tag", "--list", f"{policy.tag_prefix}*"], policy.root, check=False
    )
    versions: list[SemVer] = []
    for tag in result.stdout.splitlines():
        value = tag.removeprefix(policy.tag_prefix)
        if VERSION_RE.fullmatch(value):
            versions.append(SemVer.parse(value))
    return tuple(sorted(set(versions)))


def changelog_versions(policy: ReleasePolicy) -> tuple[SemVer, ...]:
    path = policy.root / policy.changelog
    if not path.exists():
        return ()
    return tuple(
        SemVer.parse(value)
        for value, _released in RELEASE_HEADING_RE.findall(
            path.read_text(encoding="utf-8")
        )
    )


def highest_increment(fragments: Sequence[ChangeFragment]) -> str | None:
    release_kinds = [fragment.kind for fragment in fragments if fragment.kind != "none"]
    return max(release_kinds, key=KIND_RANK.__getitem__) if release_kinds else None


def build_plan(policy: ReleasePolicy) -> ReleasePlan:
    current = read_manifest_version(policy)
    fragments = load_fragments(policy)
    increment = highest_increment(fragments)
    tags = _semantic_tags(policy)
    changelog = changelog_versions(policy)
    if tags and max(tags) > current:
        raise ReleaseError("newest semantic tag is ahead of manifest version")
    bootstrap = not tags and not changelog
    if increment:
        next_version = current if bootstrap else current.bump(increment)
        publish = True
    else:
        next_version = None
        publish = False
    return ReleasePlan(
        current_version=str(current),
        next_version=str(next_version) if next_version else None,
        bootstrap=bootstrap,
        publish=publish,
        changed=bool(fragments),
        increment=increment,
        fragments=tuple(fragment.path.as_posix() for fragment in fragments),
        fragments_digest=fragments_digest(fragments, policy.root),
    )


def render_release_section(
    version: str, fragments: Sequence[ChangeFragment], released: date
) -> str:
    lines = [f"## [{version}] - {released.isoformat()}"]
    for category in CATEGORIES:
        selected = [
            fragment
            for fragment in fragments
            if fragment.kind != "none" and fragment.category == category
        ]
        if not selected:
            continue
        lines.extend(("", f"### {category}", ""))
        for fragment in selected:
            suffix = f" [{fragment.issue}]" if fragment.issue else ""
            lines.append(f"- {fragment.summary}{suffix}")
            if fragment.breaking:
                lines.append(f"  - **Breaking:** {fragment.breaking}")
    return "\n".join(lines) + "\n"


def _update_manifest(policy: ReleasePolicy, version: str) -> None:
    path = policy.root / policy.manifest
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _prepend_changelog(policy: ReleasePolicy, section: str) -> None:
    path = policy.root / policy.changelog
    header = "# Changelog\n\nMudanças publicadas do plugin `silo-legal`.\n"
    existing = path.read_text(encoding="utf-8") if path.exists() else header
    first_release = RELEASE_HEADING_RE.search(existing)
    if first_release:
        updated = (
            existing[: first_release.start()].rstrip()
            + "\n\n"
            + section
            + "\n"
            + existing[first_release.start() :]
        )
    else:
        updated = existing.rstrip() + "\n\n" + section
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def apply_plan(
    policy: ReleasePolicy, plan: ReleasePlan, released: date | None = None
) -> dict[str, object]:
    fragments = load_fragments(policy)
    if tuple(fragment.path.as_posix() for fragment in fragments) != plan.fragments:
        raise ReleaseError(
            "release fragments changed after planning; recompute the plan"
        )
    if fragments_digest(fragments, policy.root) != plan.fragments_digest:
        raise ReleaseError(
            "release fragment content changed after planning; recompute the plan"
        )
    if plan.publish:
        assert plan.next_version is not None
        if plan.next_version != plan.current_version:
            _update_manifest(policy, plan.next_version)
        _prepend_changelog(
            policy,
            render_release_section(
                plan.next_version, fragments, released or date.today()
            ),
        )
    for fragment in fragments:
        (policy.root / fragment.path).unlink()
    payload = asdict(plan)
    payload["version"] = plan.next_version or plan.current_version
    return payload


def release_notes(policy: ReleasePolicy, version: str) -> str:
    SemVer.parse(version)
    text = (policy.root / policy.changelog).read_text(encoding="utf-8")
    heading = re.search(
        rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$", text, re.M
    )
    if not heading:
        raise ReleaseError(f"changelog section not found for {version}")
    next_heading = RELEASE_HEADING_RE.search(text, heading.end())
    return (
        text[
            heading.start() : next_heading.start() if next_heading else len(text)
        ].rstrip()
        + "\n"
    )


def audit_release(policy: ReleasePolicy) -> dict[str, object]:
    manifest = str(read_manifest_version(policy))
    tags = _semantic_tags(policy)
    changelog = changelog_versions(policy)
    fragments = load_fragments(policy)
    latest_tag = str(max(tags)) if tags else None
    latest_changelog = str(max(changelog)) if changelog else None
    if fragments:
        state = "pending fragments"
    elif manifest == latest_tag == latest_changelog:
        state = "aligned"
    elif not tags and not changelog:
        state = "bootstrap pending"
    else:
        state = "manifest/changelog/tag drift"
    return {
        "ok": state in {"aligned", "bootstrap pending", "pending fragments"},
        "state": state,
        "manifest_version": manifest,
        "changelog_version": latest_changelog,
        "local_tag_version": latest_tag,
        "pending_fragments": len(fragments),
    }


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    impact = sub.add_parser("impact")
    impact.add_argument("--ref-range", default="origin/main...HEAD")
    sub.add_parser("validate")
    fragment = sub.add_parser("fragment-add")
    fragment.add_argument("--name", required=True)
    fragment.add_argument("--kind", required=True, choices=KINDS)
    fragment.add_argument("--category", choices=CATEGORIES)
    fragment.add_argument("--summary", required=True)
    fragment.add_argument("--issue")
    fragment.add_argument("--breaking")
    sub.add_parser("plan")
    sub.add_parser("apply")
    sub.add_parser("audit")
    notes = sub.add_parser("notes")
    notes.add_argument("--version", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        policy = load_policy()
        if args.command == "impact":
            impact = classify_paths(policy, changed_paths(policy.root, args.ref_range))
            payload = asdict(impact)
            payload["pending_fragments"] = len(load_fragments(policy))
            payload["ok"] = (
                not impact.requires_fragment or payload["pending_fragments"] > 0
            )
            _emit(payload)
            return 0 if payload["ok"] else 2
        if args.command == "validate":
            _emit(
                {
                    "ok": True,
                    "fragments": [
                        item.public_dict() for item in load_fragments(policy)
                    ],
                }
            )
            return 0
        if args.command == "fragment-add":
            target = create_fragment(
                policy,
                name=args.name,
                kind=args.kind,
                category=args.category,
                summary=args.summary,
                issue=args.issue,
                breaking=args.breaking,
            )
            _emit({"ok": True, "path": target.relative_to(policy.root).as_posix()})
            return 0
        if args.command == "plan":
            _emit(asdict(build_plan(policy)))
            return 0
        if args.command == "apply":
            _emit(apply_plan(policy, build_plan(policy)))
            return 0
        if args.command == "audit":
            _emit(audit_release(policy))
            return 0
        if args.command == "notes":
            sys.stdout.write(release_notes(policy, args.version))
            return 0
        raise ReleaseError(f"unknown command: {args.command}")
    except ReleaseError as exc:
        _emit({"ok": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
