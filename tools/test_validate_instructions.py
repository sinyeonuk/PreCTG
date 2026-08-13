#!/usr/bin/env python3
"""Regression tests for the repository instruction validator."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name) / "repository"
        shutil.copytree(
            SOURCE_ROOT,
            self.root,
            ignore=shutil.ignore_patterns(".git", ".venv", "venv", "node_modules", "__pycache__"),
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-X", "utf8", "tools/validate_instructions.py"],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_current_repository_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_orphan_common_instruction_fails(self) -> None:
        agents_path = self.root / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")
        agents_path.write_text(text.replace("`agents/common/testing.md`, ", ""), encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("common instruction is not reachable", result.stdout)

    def test_missing_catalog_entry_fails(self) -> None:
        policy_path = self.root / "agents" / "common" / "example-policy.md"
        policy_path.write_text(
            "# Example Policy\n\nThis document exists only to test missing catalog detection.\n",
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing catalog entry for example-policy.md", result.stdout)

    def test_broken_explicit_reference_fails(self) -> None:
        policy_path = self.root / "agents" / "common" / "coding.md"
        text = policy_path.read_text(encoding="utf-8")
        policy_path.write_text(text + "\nFollow `agents/common/missing.md`.\n", encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("broken Markdown reference", result.stdout)

    def test_unmanaged_project_file_is_not_style_checked(self) -> None:
        source_path = self.root / "src" / "legacy.py"
        source_path.parent.mkdir(exist_ok=True)
        source_path.write_bytes(b"\xef\xbb\xbfvalue = 1  \r\n")
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_utf8_bom_in_managed_file_fails(self) -> None:
        policy_path = self.root / "agents" / "common" / "coding.md"
        policy_path.write_bytes(b"\xef\xbb\xbf" + policy_path.read_bytes())
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("UTF-8 BOM is not allowed", result.stdout)

    def test_invalid_utf8_in_managed_file_fails(self) -> None:
        policy_path = self.root / "agents" / "common" / "coding.md"
        policy_path.write_bytes(policy_path.read_bytes() + b"\xff\n")
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("not valid UTF-8", result.stdout)

    def test_crlf_in_managed_file_fails(self) -> None:
        policy_path = self.root / "agents" / "common" / "git.md"
        text = policy_path.read_text(encoding="utf-8")
        policy_path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("use LF line endings", result.stdout)

    def test_missing_final_newline_fails(self) -> None:
        policy_path = self.root / "agents" / "common" / "quality.md"
        text = policy_path.read_text(encoding="utf-8")
        policy_path.write_text(text.rstrip("\n"), encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing final newline", result.stdout)

    def test_trailing_whitespace_fails(self) -> None:
        policy_path = self.root / "agents" / "common" / "communication.md"
        text = policy_path.read_text(encoding="utf-8")
        policy_path.write_text(text + "Trailing whitespace.  \n", encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("trailing whitespace", result.stdout)

    def test_instruction_reference_cycle_fails(self) -> None:
        policy_path = self.root / "agents" / "common" / "testing.md"
        text = policy_path.read_text(encoding="utf-8")
        policy_path.write_text(text + "\nFollow `coding.md`.\n", encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("instruction reference cycle", result.stdout)

    def test_duplicate_instruction_bullet_fails(self) -> None:
        duplicate = "- Inspect the example invariant before continuing.\n"
        for name in ("coding.md", "testing.md"):
            policy_path = self.root / "agents" / "common" / name
            text = policy_path.read_text(encoding="utf-8")
            policy_path.write_text(text + "\n" + duplicate, encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("duplicate instruction bullet", result.stdout)

    def test_non_preferred_terminology_fails(self) -> None:
        docs_path = self.root / "docs" / "README.md"
        text = docs_path.read_text(encoding="utf-8")
        docs_path.write_text(text + "\n이 리포지토리를 확인합니다.\n", encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("use `저장소` instead of `리포지토리`", result.stdout)

    def test_nested_instruction_directory_requires_readme(self) -> None:
        policy_path = self.root / "agents" / "project" / "platform" / "windows.md"
        policy_path.parent.mkdir()
        policy_path.write_text(
            "# Windows\n\nThis document defines confirmed Windows-specific project behavior.\n",
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing human-readable index", result.stdout)

    def test_unsorted_catalog_fails(self) -> None:
        readme_path = self.root / "agents" / "common" / "README.md"
        lines = readme_path.read_text(encoding="utf-8").splitlines()
        coding_index = next(index for index, line in enumerate(lines) if line.startswith("| `coding.md`"))
        communication_index = next(
            index for index, line in enumerate(lines) if line.startswith("| `communication.md`")
        )
        lines[coding_index], lines[communication_index] = lines[communication_index], lines[coding_index]
        readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("catalog entries must be sorted alphabetically", result.stdout)


if __name__ == "__main__":
    unittest.main()
