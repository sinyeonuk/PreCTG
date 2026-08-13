#!/usr/bin/env python3
"""Validate the repository's agent instruction system without third-party packages."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTRUCTION_DIRS = (ROOT / "agents" / "common", ROOT / "agents" / "project")
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".json", ".txt"}
MANAGED_FILES = (
    ROOT / ".editorconfig",
    ROOT / ".gitattributes",
    ROOT / ".github" / "workflows" / "validate.yml",
    ROOT / "AGENTS.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "project-instruction-example.md",
    ROOT / "docs" / "template-lifecycle.md",
    ROOT / "tools" / "terminology.json",
    ROOT / "tools" / "test_validate_instructions.py",
    ROOT / "tools" / "validate_instructions.py",
)
REFERENCE_RE = re.compile(r"`([^`\n]+\.md)`")
BULLET_RE = re.compile(r"^\s*-\s+(.+?)\s*$")
H1_RE = re.compile(r"^# (\S.*)$", re.MULTILINE)
CATALOG_FILE_RE = re.compile(r"^\|\s*`([^`]+\.md)`\s*\|", re.MULTILINE)
CATALOG_DIR_RE = re.compile(r"^\|\s*`([^`]+/)`\s*\|", re.MULTILINE)
CATALOG_ENTRY_RE = re.compile(r"^\|\s*`([^`]+(?:\.md|/))`\s*\|", re.MULTILINE)
CODE_SPAN_RE = re.compile(r"`[^`]*`")


def managed_files() -> list[Path]:
    files = {path for path in MANAGED_FILES if path.is_file()}
    for directory in INSTRUCTION_DIRS:
        files.update(path for path in directory.rglob("*.md") if path.is_file())
    return sorted(files)


def instruction_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.rglob("*.md") if path.name != "README.md")


def direct_instruction_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.glob("*.md") if path.name != "README.md")


def instruction_directories() -> list[Path]:
    directories: set[Path] = set(INSTRUCTION_DIRS)
    for root in INSTRUCTION_DIRS:
        for path in root.rglob("*"):
            if path.is_dir() and instruction_files(path):
                directories.add(path)
    return sorted(directories)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def decode_text_files(files: list[Path], errors: list[str]) -> dict[Path, str]:
    texts: dict[Path, str] = {}
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"AGENTS.md", ".editorconfig", ".gitattributes"}:
            continue
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{relative(path)}: UTF-8 BOM is not allowed")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative(path)}: not valid UTF-8 ({exc})")
            continue
        if "\r" in text:
            errors.append(f"{relative(path)}: use LF line endings")
        if text and not text.endswith("\n"):
            errors.append(f"{relative(path)}: missing final newline")
        if any(line.endswith((" ", "\t")) for line in text.splitlines()):
            errors.append(f"{relative(path)}: trailing whitespace")
        texts[path] = text
    return texts


def check_instruction_shape(texts: dict[Path, str], errors: list[str]) -> None:
    for directory in instruction_directories():
        if directory in INSTRUCTION_DIRS:
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", directory.name):
            errors.append(f"{relative(directory)}: policy directory name must use lowercase English kebab-case")
    for directory in INSTRUCTION_DIRS:
        for path in instruction_files(directory):
            if path.name != path.name.lower() or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*\.md", path.name):
                errors.append(f"{relative(path)}: instruction file name must use lowercase English kebab-case")
            text = texts.get(path, "")
            headings = H1_RE.findall(text)
            if len(headings) != 1 or not text.startswith("# "):
                errors.append(f"{relative(path)}: expected exactly one leading H1 heading")
            first_body = next((line for line in text.splitlines()[1:] if line.strip()), "")
            if not first_body:
                errors.append(f"{relative(path)}: missing purpose statement after H1")


def check_catalogs(errors: list[str]) -> None:
    for directory in instruction_directories():
        readme = directory / "README.md"
        if not readme.exists():
            errors.append(f"{relative(readme)}: missing human-readable index")
            continue
        text = readme.read_text(encoding="utf-8")
        listed_files = set(CATALOG_FILE_RE.findall(text))
        actual_files = {path.name for path in direct_instruction_files(directory)}
        child_directories = {
            path.name + "/"
            for path in directory.iterdir()
            if path.is_dir() and instruction_files(path)
        }
        listed_directories = set(CATALOG_DIR_RE.findall(text))
        listed_entries = CATALOG_ENTRY_RE.findall(text)
        if listed_entries != sorted(listed_entries, key=str.casefold):
            errors.append(f"{relative(readme)}: catalog entries must be sorted alphabetically")
        for name in sorted(actual_files - listed_files):
            errors.append(f"{relative(readme)}: missing catalog entry for {name}")
        for name in sorted(listed_files - actual_files):
            errors.append(f"{relative(readme)}: catalog entry points to missing file {name}")
        for name in sorted(child_directories - listed_directories):
            errors.append(f"{relative(readme)}: missing catalog entry for {name}")
        for name in sorted(listed_directories - child_directories):
            errors.append(f"{relative(readme)}: catalog entry points to missing directory {name}")


def resolve_reference(source: Path, reference: str) -> Path:
    candidate = Path(reference.replace("\\", "/"))
    if "/" in reference or "\\" in reference:
        return (ROOT / candidate).resolve()
    if reference == "AGENTS.md":
        return (ROOT / reference).resolve()
    return (source.parent / candidate).resolve()


def check_references_and_cycles(texts: dict[Path, str], errors: list[str]) -> None:
    graph: dict[Path, set[Path]] = defaultdict(set)
    instruction_set = {path.resolve() for directory in INSTRUCTION_DIRS for path in instruction_files(directory)}
    sources = [ROOT / "AGENTS.md", *sorted(instruction_set)]
    known_names = {path.name for path in instruction_set} | {"AGENTS.md"}
    for source in sources:
        for reference in REFERENCE_RE.findall(texts.get(source, "")):
            if "/" not in reference and "\\" not in reference and reference not in known_names:
                continue
            target = resolve_reference(source, reference)
            if not target.exists():
                errors.append(f"{relative(source)}: broken Markdown reference `{reference}`")
            elif source.resolve() in instruction_set and target in instruction_set:
                graph[source.resolve()].add(target)

    visiting: set[Path] = set()
    visited: set[Path] = set()

    def visit(node: Path, chain: list[Path]) -> None:
        if node in visiting:
            start = chain.index(node)
            cycle = chain[start:] + [node]
            errors.append("instruction reference cycle: " + " -> ".join(relative(path) for path in cycle))
            return
        if node in visited:
            return
        visiting.add(node)
        for target in graph[node]:
            visit(target, chain + [target])
        visiting.remove(node)
        visited.add(node)

    for node in sorted(instruction_set):
        visit(node, [node])


def check_loading_coverage(texts: dict[Path, str], errors: list[str]) -> None:
    root_path = ROOT / "AGENTS.md"
    root_text = texts.get(root_path, "")
    start_marker = "Always read these core instructions:"
    end_marker = "These instructions define the default behavior shared by every project."
    if start_marker not in root_text or end_marker not in root_text:
        errors.append("AGENTS.md: cannot locate the common-instruction loading section")
        return
    loading_text = root_text.split(start_marker, 1)[1].split(end_marker, 1)[0]
    loaded: set[Path] = set()
    for reference in REFERENCE_RE.findall(loading_text):
        target = resolve_reference(root_path, reference)
        if target.name != "README.md" and target.exists():
            loaded.add(target.resolve())
    common_files = {path.resolve() for path in instruction_files(ROOT / "agents" / "common")}
    for path in sorted(common_files - loaded):
        errors.append(f"{relative(path)}: common instruction is not reachable from the AGENTS.md loading rules")


def normalize_bullet(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def check_duplicate_rules(texts: dict[Path, str], errors: list[str]) -> None:
    owners: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    for directory in INSTRUCTION_DIRS:
        for path in instruction_files(directory):
            for number, line in enumerate(texts.get(path, "").splitlines(), 1):
                match = BULLET_RE.match(line)
                if match:
                    owners[normalize_bullet(match.group(1))].append((path, number))
    for locations in owners.values():
        distinct_files = {path for path, _ in locations}
        if len(distinct_files) > 1:
            rendered = ", ".join(f"{relative(path)}:{line}" for path, line in locations)
            errors.append(f"duplicate instruction bullet: {rendered}")


def check_terminology(texts: dict[Path, str], errors: list[str]) -> None:
    terminology_data = json.loads((ROOT / "tools" / "terminology.json").read_text(encoding="utf-8"))
    mappings = terminology_data["non_preferred_terms"]
    glossary_path = ROOT / "agents" / "common" / "terminology.md"
    glossary = texts.get(glossary_path, "")
    for term, preferred in mappings.items():
        if term not in glossary or preferred not in glossary:
            errors.append(
                f"tools/terminology.json: `{term}` -> `{preferred}` must also be documented in "
                f"{relative(glossary_path)}"
            )
    targets = [ROOT / "docs"]
    targets.extend(directory / "README.md" for directory in instruction_directories())
    files: list[Path] = []
    for target in targets:
        files.extend(target.rglob("*.md") if target.is_dir() else [target])
    for path in files:
        text = CODE_SPAN_RE.sub("", texts.get(path, ""))
        for term, preferred in sorted(mappings.items(), key=lambda item: len(item[0]), reverse=True):
            if term in text:
                errors.append(f"{relative(path)}: use `{preferred}` instead of `{term}`")


def main() -> int:
    errors: list[str] = []
    files = managed_files()
    texts = decode_text_files(files, errors)
    check_instruction_shape(texts, errors)
    check_catalogs(errors)
    check_references_and_cycles(texts, errors)
    check_loading_coverage(texts, errors)
    check_duplicate_rules(texts, errors)
    check_terminology(texts, errors)
    if errors:
        print(f"Validation failed with {len(errors)} issue(s):")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1
    print("Instruction system validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
