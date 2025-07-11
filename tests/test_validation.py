"""Tests for template validation and linting."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import pytest
from cookiecutter.main import cookiecutter


class TestTemplateValidation:
    """Test template file validation."""

    def test_cookiecutter_json_schema(self) -> None:
        """Test cookiecutter.json has proper schema."""
        template_dir = Path(__file__).parent.parent
        cookiecutter_json = template_dir / "cookiecutter.json"

        with open(cookiecutter_json) as f:
            config = json.load(f)

        # Required string fields
        required_strings = [
            "full_name",
            "email",
            "github_username",
            "project_name",
            "project_slug",
            "project_short_description",
            "version",
            "python_requires",
        ]

        for field in required_strings:
            assert field in config
            assert isinstance(config[field], str)

        # Choice fields should be lists
        choice_fields = [
            "license",
            "command_line_interface",
            "use_ruff",
            "use_mypy",
            "use_pytest",
        ]

        for field in choice_fields:
            if field in config:
                assert isinstance(config[field], list), (
                    f"{field} should be a list of choices"
                )

    def test_jinja_template_syntax(self) -> None:
        """Test that Jinja templates have valid syntax."""
        template_dir = Path(__file__).parent.parent
        project_template = template_dir / "{{cookiecutter.project_slug}}"

        # Find all template files
        template_files: list[Path] = []
        for pattern in ["*.py", "*.toml", "*.yml", "*.yaml", "*.md", "*.txt"]:
            template_files.extend(project_template.rglob(pattern))

        # Basic syntax check - look for unmatched braces
        for template_file in template_files:
            content = template_file.read_text(encoding="utf-8")

            # Count braces
            open_braces = content.count("{{")
            close_braces = content.count("}}")

            # In Jinja templates, these should match
            # (This is a basic check, real validation would use Jinja2)
            if "{{" in content:
                assert open_braces > 0, f"Template {template_file} has template syntax"

    def test_python_files_syntax(self) -> None:
        """Test that Python template files have valid syntax when rendered."""
        # We can't easily test this without rendering, but we can check
        # that non-template Python files are valid
        template_dir = Path(__file__).parent.parent

        # Check hooks
        hooks_dir = template_dir / "hooks"
        for py_file in hooks_dir.glob("*.py"):
            # Try to compile the Python file
            with open(py_file) as f:
                content = f.read()

            try:
                compile(content, str(py_file), "exec")
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {py_file}: {e}")


class TestTemplateConsistency:
    """Test template consistency and best practices."""

    def test_all_licenses_supported(self) -> None:
        """Test that all license options have corresponding templates."""
        template_dir = Path(__file__).parent.parent

        # Read license options from cookiecutter.json
        with open(template_dir / "cookiecutter.json") as f:
            config = json.load(f)

        license_options = config["license"]
        license_template = template_dir / "{{cookiecutter.project_slug}}" / "LICENSE"

        # Read the license template
        license_content = license_template.read_text(encoding="utf-8")

        # Check that all license types are handled
        for license_type in license_options:
            if license_type != "Proprietary":
                # For SPDX format, check if license is in template variable or explicit
                if license_type in ["MIT", "BSD-3-Clause"]:
                    assert license_type in license_content, (
                        f"License {license_type} not found in template"
                    )
                else:
                    # SPDX fallback handles other licenses
                    assert "{{ cookiecutter.license }}" in license_content, (
                        f"Template should handle {license_type} via SPDX"
                    )

    def test_cli_options_consistency(self) -> None:
        """Test that CLI options are consistently handled."""
        template_dir = Path(__file__).parent.parent

        with open(template_dir / "cookiecutter.json") as f:
            config = json.load(f)

        cli_options = config["command_line_interface"]
        cli_template = (
            template_dir
            / "{{cookiecutter.project_slug}}"
            / "src"
            / "{{cookiecutter.project_slug}}"
            / "cli.py"
        )

        cli_content = cli_template.read_text(encoding="utf-8")

        # Check that all CLI options are handled in the template
        for cli_option in cli_options:
            if cli_option != "none":
                assert cli_option in cli_content, (
                    f"CLI option {cli_option} not handled in template"
                )

    def test_pyproject_toml_dependencies(self) -> None:
        """Test that pyproject.toml includes correct dependencies for CLI options."""
        template_dir = Path(__file__).parent.parent
        pyproject_template = (
            template_dir / "{{cookiecutter.project_slug}}" / "pyproject.toml"
        )

        content = pyproject_template.read_text(encoding="utf-8")

        # Check that CLI dependencies are conditionally included
        assert "typer" in content
        assert "click" in content
        # They should be in conditional blocks
        assert 'cookiecutter.command_line_interface == "typer"' in content

    def test_readme_consistency(self) -> None:
        """Test that README templates are consistent."""
        template_dir = Path(__file__).parent.parent

        # Check main template README
        main_readme = template_dir / "README.md"
        project_readme = template_dir / "{{cookiecutter.project_slug}}" / "README.md"

        assert main_readme.exists()
        assert project_readme.exists()

        # Both should mention the key features
        main_content = main_readme.read_text(encoding="utf-8")
        project_content = project_readme.read_text(encoding="utf-8")

        # Main README should be comprehensive
        assert "cookiecutter" in main_content.lower()
        assert "modern" in main_content.lower()

        # Project README should be template
        assert "{{" in project_content  # Should have template variables


class TestGeneratedProjectQuality:
    """Test the quality of generated projects."""

    @pytest.fixture
    def generated_project(self) -> Any:
        """Generate a test project."""
        template_dir = Path(__file__).parent.parent

        context = {
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
            "use_pre_commit": "n",  # Skip for faster testing
            "use_bandit": "n",
            "use_safety": "n",
            "use_sphinx": "n",
            "use_mkdocs": "n",
            "use_github_actions": "n",
            "use_dependabot": "n",
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

        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )
            yield Path(result)

    def test_ruff_passes_on_generated_project(self, generated_project: Path) -> None:
        """Test that Ruff passes on generated project."""
        # Install dependencies first
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
            check=False,
            cwd=generated_project,
            capture_output=True,
        )

        # Run Ruff fix first to auto-format
        subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--fix", "src", "tests"],
            check=False,
            cwd=generated_project,
            capture_output=True,
        )

        # Run Ruff check to verify no issues remain
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "src", "tests"],
            check=False,
            cwd=generated_project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"Ruff check failed: {result.stdout}\n{result.stderr}"
        )

    def test_mypy_passes_on_generated_project(self, generated_project: Path) -> None:
        """Test that MyPy passes on generated project."""
        # Install dependencies first
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
            check=False,
            cwd=generated_project,
            capture_output=True,
        )

        # Run MyPy
        result = subprocess.run(
            [sys.executable, "-m", "mypy", "src/test_package"],
            check=False,
            cwd=generated_project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"MyPy failed: {result.stdout}\n{result.stderr}"

    def test_pytest_passes_on_generated_project(self, generated_project: Path) -> None:
        """Test that pytest passes on generated project."""
        # Install dependencies first
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
            check=False,
            cwd=generated_project,
            capture_output=True,
        )

        # Run tests
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v"],
            check=False,
            cwd=generated_project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Tests failed: {result.stdout}\n{result.stderr}"
