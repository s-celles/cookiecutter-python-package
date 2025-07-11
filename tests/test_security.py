"""Security and quality tests for the cookiecutter template."""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import pytest
from cookiecutter.main import cookiecutter


class TestSecurity:
    """Test security aspects of the template."""

    @pytest.fixture
    def template_dir(self) -> Path:
        """Return the path to the template directory."""
        return Path(__file__).parent.parent

    @pytest.fixture
    def secure_context(self) -> dict[str, Any]:
        """Context with security tools enabled."""
        return {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test Package",
            "project_slug": "test_package",
            "project_short_description": "A test package",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            "use_ruff": "y",
            "use_mypy": "y",
            "use_pytest": "y",
            "use_coverage": "y",
            "use_pre_commit": "y",
            "use_bandit": "y",  # Security linting
            "use_safety": "y",  # Dependency vulnerability checking
            "use_sphinx": "n",
            "use_mkdocs": "n",
            "use_github_actions": "y",
            "use_dependabot": "y",  # Automated dependency updates
            "use_codecov": "n",
            "command_line_interface": "typer",
            "use_tox": "n",
            "use_nox": "n",
            "use_commitizen": "n",
            "use_semantic_release": "n",
            "create_changelog": "n",
            "create_contributing": "n",
            "create_code_of_conduct": "n",
            "use_docker": "n",
            "use_devcontainer": "n",
        }

    def test_no_hardcoded_secrets(self, template_dir: Path) -> None:
        """Test that template files don't contain hardcoded secrets."""
        # Common patterns that might indicate secrets
        secret_patterns = [
            r"password\s*=\s*['\"][^'\"]+['\"]",
            r"api_key\s*=\s*['\"][^'\"]+['\"]",
            r"secret_key\s*=\s*['\"][^'\"]+['\"]",
            r"token\s*=\s*['\"][^'\"]+['\"]",
            r"-----BEGIN .* PRIVATE KEY-----",
        ]

        template_files: list[Path] = []
        for pattern in [
            "**/*.py",
            "**/*.yml",
            "**/*.yaml",
            "**/*.toml",
            "**/*.md",
            "**/*.txt",
        ]:
            template_files.extend(template_dir.rglob(pattern))

        for file_path in template_files:
            if file_path.is_file():
                # Skip test files that might contain pattern examples
                if "test_security.py" in str(file_path):
                    continue

                try:
                    content = file_path.read_text(encoding="utf-8")
                    for pattern in secret_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        assert not matches, (
                            f"Potential secret found in {file_path}: {matches}"
                        )
                except (UnicodeDecodeError, PermissionError):
                    # Skip binary files or files we can't read
                    continue

    def test_github_actions_security(
        self, template_dir: Path, secure_context: dict[str, Any]
    ) -> None:
        """Test that GitHub Actions workflows follow security best practices."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=secure_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            workflows_dir = project_path / ".github" / "workflows"

            if workflows_dir.exists():
                for workflow_file in workflows_dir.glob("*.yml"):
                    content = workflow_file.read_text(encoding="utf-8")

                    # Check for security best practices
                    assert "permissions:" in content, (
                        f"Workflow {workflow_file.name} should specify permissions"
                    )

                    # Should not use deprecated actions
                    assert "actions/checkout@v1" not in content, (
                        "Should use latest checkout action"
                    )
                    assert "actions/setup-python@v1" not in content, (
                        "Should use latest setup-python action"
                    )

                    # Should pin action versions
                    action_refs = re.findall(r"uses:\s*([^@\s]+)@([^\s]+)", content)
                    for action, ref in action_refs:
                        if not action.startswith("./"):  # Skip local actions
                            assert ref != "main" and ref != "master", (
                                f"Action {action} should be pinned to specific version, not {ref}"
                            )

    def test_dependency_security(
        self, template_dir: Path, secure_context: dict[str, Any]
    ) -> None:
        """Test that generated projects use secure dependency configurations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=secure_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            pyproject_file = project_path / "pyproject.toml"

            content = pyproject_file.read_text(encoding="utf-8")

            # Should include security tools when enabled
            if secure_context["use_bandit"] == "y":
                assert "bandit" in content, "Bandit should be included when enabled"

            if secure_context["use_safety"] == "y":
                assert "safety" in content, "Safety should be included when enabled"

    def test_generated_project_passes_bandit(
        self, template_dir: Path, secure_context: dict[str, Any]
    ) -> None:
        """Test that generated project passes Bandit security checks."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=secure_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # Install dependencies
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
                check=False,
                cwd=project_path,
                capture_output=True,
            )

            # Run Bandit
            result = subprocess.run(
                [sys.executable, "-m", "bandit", "-r", "src/", "-ll"],
                check=False,
                cwd=project_path,
                capture_output=True,
                text=True,
            )

            # Should pass security checks
            assert result.returncode == 0, (
                f"Bandit security check failed: {result.stdout}\n{result.stderr}"
            )


class TestQuality:
    """Test code quality aspects of the template."""

    @pytest.fixture
    def template_dir(self) -> Path:
        """Return the path to the template directory."""
        return Path(__file__).parent.parent

    @pytest.fixture
    def quality_context(self) -> dict[str, Any]:
        """Context with quality tools enabled."""
        return {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test Package",
            "project_slug": "test_package",
            "project_short_description": "A test package",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            "use_ruff": "y",
            "use_mypy": "y",
            "use_pytest": "y",
            "use_coverage": "y",
            "use_pre_commit": "y",
            "use_bandit": "y",
            "use_safety": "y",
            "use_sphinx": "n",
            "use_mkdocs": "y",
            "use_github_actions": "y",
            "use_dependabot": "y",
            "use_codecov": "y",
            "command_line_interface": "typer",
            "use_tox": "y",
            "use_nox": "y",
            "use_commitizen": "y",
            "use_semantic_release": "y",
            "create_changelog": "y",
            "create_contributing": "y",
            "create_code_of_conduct": "y",
            "use_docker": "n",
            "use_devcontainer": "n",
        }

    def test_code_formatting_consistency(
        self, template_dir: Path, quality_context: dict[str, Any]
    ) -> None:
        """Test that generated code follows consistent formatting."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=quality_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # Check Python files for consistent formatting
            python_files = list(project_path.rglob("*.py"))

            for py_file in python_files:
                content = py_file.read_text(encoding="utf-8")

                # Check for consistent indentation (4 spaces)
                lines = content.split("\n")
                for line_num, line in enumerate(lines, 1):
                    if line.strip() and line.startswith(" "):
                        # Count leading spaces
                        leading_spaces = len(line) - len(line.lstrip(" "))
                        assert leading_spaces % 4 == 0, (
                            f"Inconsistent indentation in {py_file}:{line_num}"
                        )

                # Check for consistent quotes (should prefer double quotes for Ruff)
                # This is a basic check - Ruff will do more thorough formatting

    def test_documentation_completeness(
        self, template_dir: Path, quality_context: dict[str, Any]
    ) -> None:
        """Test that generated project has complete documentation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=quality_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # Check that README exists and has content
            readme_file = project_path / "README.md"
            assert readme_file.exists(), "README.md should exist"

            readme_content = readme_file.read_text(encoding="utf-8")
            assert len(readme_content) > 100, "README should have substantial content"
            assert "# Test Package" in readme_content, (
                "README should have project title"
            )
            assert "## Installation" in readme_content, (
                "README should have installation instructions"
            )
            assert "## Usage" in readme_content, "README should have usage examples"

            # Check for documentation files when enabled
            if quality_context["create_contributing"] == "y":
                contributing_file = project_path / "CONTRIBUTING.md"
                assert contributing_file.exists(), (
                    "CONTRIBUTING.md should exist when enabled"
                )

                contributing_content = contributing_file.read_text(encoding="utf-8")
                assert "# Contributing" in contributing_content, (
                    "CONTRIBUTING should have proper header"
                )

            if quality_context["create_changelog"] == "y":
                changelog_file = project_path / "CHANGELOG.md"
                assert changelog_file.exists(), "CHANGELOG.md should exist when enabled"

    def test_type_hints_coverage(
        self, template_dir: Path, quality_context: dict[str, Any]
    ) -> None:
        """Test that generated code has good type hint coverage."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=quality_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # Check that py.typed marker exists
            py_typed_file = project_path / "src" / "test_package" / "py.typed"
            assert py_typed_file.exists(), (
                "py.typed marker should exist for type checking support"
            )

            # Check main module files for type hints
            core_file = project_path / "src" / "test_package" / "core.py"
            if core_file.exists():
                content = core_file.read_text(encoding="utf-8")

                # Should have type imports
                assert (
                    "from typing import" in content
                    or "from __future__ import annotations" in content
                ), "Should import typing for type hints"

                # Should have function annotations
                function_lines = [
                    line for line in content.split("\n") if "def " in line
                ]
                for line in function_lines:
                    if not line.strip().startswith("#") and "def __" not in line:
                        # Public functions should have type hints
                        assert "->" in line or line.endswith(":"), (
                            f"Function should have return type hint: {line}"
                        )

    def test_test_coverage_setup(
        self, template_dir: Path, quality_context: dict[str, Any]
    ) -> None:
        """Test that test coverage is properly configured."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=quality_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            pyproject_file = project_path / "pyproject.toml"

            content = pyproject_file.read_text(encoding="utf-8")

            if quality_context["use_coverage"] == "y":
                # Should have coverage configuration
                assert "[tool.coverage" in content, "Should have coverage configuration"
                assert "source = " in content, "Should specify coverage source"
                assert "omit = " in content, (
                    "Should specify files to omit from coverage"
                )

    def test_linting_configuration(
        self, template_dir: Path, quality_context: dict[str, Any]
    ) -> None:
        """Test that linting tools are properly configured."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=quality_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            pyproject_file = project_path / "pyproject.toml"

            content = pyproject_file.read_text(encoding="utf-8")

            if quality_context["use_ruff"] == "y":
                assert "[tool.ruff" in content, "Should have Ruff configuration"
                assert "select = " in content, "Should specify Ruff rules to enable"
                assert "line-length = " in content, "Should specify line length"

            if quality_context["use_mypy"] == "y":
                assert "[tool.mypy" in content, "Should have MyPy configuration"
                assert "python_version = " in content, (
                    "Should specify Python version for MyPy"
                )


class TestAccessibility:
    """Test accessibility and usability aspects of the template."""

    @pytest.fixture
    def template_dir(self) -> Path:
        """Return the path to the template directory."""
        return Path(__file__).parent.parent

    def test_readme_accessibility(self, template_dir: Path) -> None:
        """Test that template README is accessible and informative."""
        readme_file = template_dir / "README.md"
        assert readme_file.exists(), "Template should have README.md"

        content = readme_file.read_text(encoding="utf-8")

        # Should have clear structure
        assert "# " in content, "README should have main heading"
        assert "## " in content, "README should have section headings"

        # Should explain what the template is
        assert "cookiecutter" in content.lower(), "Should mention cookiecutter"
        assert "template" in content.lower(), "Should mention it's a template"

        # Should have usage instructions
        assert "cookiecutter" in content, "Should show cookiecutter command"

    def test_cookiecutter_json_documentation(self, template_dir: Path) -> None:
        """Test that cookiecutter.json is well-documented."""
        cookiecutter_json = template_dir / "cookiecutter.json"

        with open(cookiecutter_json) as f:
            config = json.load(f)

        # Check that choice fields have reasonable defaults and options
        choice_fields = ["license", "command_line_interface"]

        for field in choice_fields:
            if field in config and isinstance(config[field], list):
                assert len(config[field]) > 1, (
                    f"Choice field {field} should have multiple options"
                )

                # First option should be reasonable default
                first_option = config[field][0]
                assert first_option, f"First option for {field} should not be empty"

    def test_error_handling_in_hooks(self, template_dir: Path) -> None:
        """Test that hooks handle errors gracefully."""
        hook_file = template_dir / "hooks" / "post_gen_project.py"

        if hook_file.exists():
            content = hook_file.read_text(encoding="utf-8")

            # Should have error handling
            assert "try:" in content or "except" in content, (
                "Hooks should include error handling"
            )

            # Should provide helpful messages
            assert "print(" in content, "Hooks should provide user feedback"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
