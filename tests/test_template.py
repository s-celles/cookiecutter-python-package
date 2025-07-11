"""Comprehensive tests for the cookiecutter template generation."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture
def template_dir() -> Path:
    """Return the path to the template directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def minimal_context() -> dict[str, Any]:
    """Minimal context for quick testing."""
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
        "use_ruff": "n",
        "use_mypy": "n",
        "use_pytest": "y",
        "use_coverage": "n",
        "use_pre_commit": "n",
        "use_bandit": "n",
        "use_safety": "n",
        "use_sphinx": "n",
        "use_mkdocs": "n",
        "use_github_actions": "n",
        "use_dependabot": "n",
        "use_codecov": "n",
        "command_line_interface": "none",
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


@pytest.fixture
def full_context() -> dict[str, Any]:
    """Full context with all features enabled."""
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
        "use_docker": "y",
        "use_devcontainer": "y",
    }


class TestTemplateStructure:
    """Test the template directory structure."""

    def test_template_exists(self, template_dir: Path) -> None:
        """Test that template directory exists."""
        assert template_dir.exists()
        assert template_dir.is_dir()

    def test_cookiecutter_json_exists(self, template_dir: Path) -> None:
        """Test that cookiecutter.json exists and is valid."""
        cookiecutter_json = template_dir / "cookiecutter.json"
        assert cookiecutter_json.exists()

        # Test that it's valid JSON
        with open(cookiecutter_json) as f:
            config = json.load(f)

        # Check required fields
        required_fields = [
            "full_name",
            "email",
            "github_username",
            "project_name",
            "project_slug",
        ]
        for field in required_fields:
            assert field in config

    def test_project_template_exists(self, template_dir: Path) -> None:
        """Test that project template directory exists."""
        project_template = template_dir / "{{cookiecutter.project_slug}}"
        assert project_template.exists()
        assert project_template.is_dir()

    def test_hooks_directory_exists(self, template_dir: Path) -> None:
        """Test that hooks directory exists."""
        hooks_dir = template_dir / "hooks"
        assert hooks_dir.exists()
        assert (hooks_dir / "post_gen_project.py").exists()

    def test_required_template_files(self, template_dir: Path) -> None:
        """Test that all required template files exist."""
        project_template = template_dir / "{{cookiecutter.project_slug}}"

        required_files = [
            "pyproject.toml",
            "README.md",
            "LICENSE",
            ".gitignore",
            "src/{{cookiecutter.project_slug}}/__init__.py",
            "src/{{cookiecutter.project_slug}}/core.py",
            "src/{{cookiecutter.project_slug}}/cli.py",
            "src/{{cookiecutter.project_slug}}/py.typed",
            "tests/__init__.py",
            "tests/test_core.py",
            "tests/test_cli.py",
        ]

        for file_path in required_files:
            full_path = project_template / file_path
            assert full_path.exists(), f"Required file {file_path} not found"


class TestProjectGeneration:
    """Test actual project generation."""

    def test_minimal_generation(
        self, template_dir: Path, minimal_context: dict[str, Any]
    ) -> None:
        """Test generating a project with minimal options."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=minimal_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            assert project_path.exists()
            assert (project_path / "pyproject.toml").exists()
            assert (project_path / "src" / "test_package" / "__init__.py").exists()

    def test_full_generation(
        self, template_dir: Path, full_context: dict[str, Any]
    ) -> None:
        """Test generating a project with all options enabled."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=full_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            assert project_path.exists()

            # Check that optional files are created
            assert (project_path / ".pre-commit-config.yaml").exists()
            assert (project_path / ".github" / "workflows" / "ci.yml").exists()
            assert (project_path / "tox.ini").exists()
            assert (project_path / "noxfile.py").exists()
            assert (project_path / "CHANGELOG.md").exists()
            assert (project_path / "CONTRIBUTING.md").exists()

    @pytest.mark.parametrize("cli_option", ["typer", "click", "argparse", "none"])
    def test_cli_options(
        self, template_dir: Path, minimal_context: dict[str, Any], cli_option: str
    ) -> None:
        """Test different CLI framework options."""
        context = minimal_context.copy()
        context["command_line_interface"] = cli_option

        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            cli_file = project_path / "src" / "test_package" / "cli.py"

            assert cli_file.exists()
            cli_content = cli_file.read_text(encoding="utf-8")

            if cli_option == "typer":
                assert "import typer" in cli_content
            elif cli_option == "click":
                assert "import click" in cli_content
            elif cli_option == "argparse":
                assert "import argparse" in cli_content
            elif cli_option == "none":
                assert "No command line interface" in cli_content

    @pytest.mark.parametrize("license_type", ["MIT", "Apache-2.0", "BSD-3-Clause"])
    def test_license_options(
        self, template_dir: Path, minimal_context: dict[str, Any], license_type: str
    ) -> None:
        """Test different license options."""
        context = minimal_context.copy()
        context["license"] = license_type

        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            license_file = project_path / "LICENSE"

            assert license_file.exists()
            license_content = license_file.read_text(encoding="utf-8")

            if license_type == "MIT":
                assert "MIT License" in license_content
            elif license_type == "Apache-2.0":
                assert "Apache-2.0" in license_content  # SPDX format
            elif license_type == "BSD-3-Clause":
                assert "BSD 3-Clause License" in license_content


class TestGeneratedProject:
    """Test that generated projects work correctly."""

    def test_pyproject_toml_is_valid(
        self, template_dir: Path, minimal_context: dict[str, Any]
    ) -> None:
        """Test that generated pyproject.toml is valid."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=minimal_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            pyproject_file = project_path / "pyproject.toml"

            # Try to parse the TOML file
            try:
                import tomllib  # Python 3.11+
            except ImportError:
                import tomli as tomllib

            with open(pyproject_file, "rb") as f:
                config = tomllib.load(f)

            # Check required sections
            assert "build-system" in config
            assert "project" in config
            assert config["project"]["name"] == "test_package"

    def test_package_can_be_installed(
        self, template_dir: Path, minimal_context: dict[str, Any]
    ) -> None:
        """Test that generated package can be installed."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=minimal_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # Try to install the package in development mode
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", "."],
                check=False,
                cwd=project_path,
                capture_output=True,
                text=True,
            )

            # Installation should succeed
            assert result.returncode == 0, f"Installation failed: {result.stderr}"

    def test_generated_tests_pass(
        self, template_dir: Path, minimal_context: dict[str, Any]
    ) -> None:
        """Test that generated tests pass."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=minimal_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # Install the package first
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
                check=False,
                cwd=project_path,
                capture_output=True,
            )

            # Run the tests
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-v"],
                check=False,
                cwd=project_path,
                capture_output=True,
                text=True,
            )

            # Tests should pass
            assert result.returncode == 0, (
                f"Tests failed: {result.stdout}\n{result.stderr}"
            )


class TestHooks:
    """Test the post-generation hooks."""

    def test_post_gen_hook_runs(
        self, template_dir: Path, minimal_context: dict[str, Any]
    ) -> None:
        """Test that post-generation hook runs successfully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # The hook should run automatically during generation
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=minimal_context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # Check that git repo was initialized
            assert (project_path / ".git").exists()

    def test_hook_removes_unused_files(
        self, template_dir: Path, minimal_context: dict[str, Any]
    ) -> None:
        """Test that hooks remove files based on configuration."""
        context = minimal_context.copy()
        context["use_pre_commit"] = "n"
        context["use_tox"] = "n"
        context["use_docker"] = "n"

        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # These files should not exist when features are disabled
            assert not (project_path / ".pre-commit-config.yaml").exists()
            assert not (project_path / "tox.ini").exists()
            assert not (project_path / "Dockerfile").exists()


@pytest.mark.slow
class TestIntegration:
    """Integration tests (slower tests)."""

    def test_full_workflow(
        self, template_dir: Path, full_context: dict[str, Any]
    ) -> None:
        """Test the complete workflow with all tools enabled."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=full_context,
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

            # Auto-fix Ruff issues first
            subprocess.run(
                [sys.executable, "-m", "ruff", "check", "--fix", "."],
                check=False,
                cwd=project_path,
                capture_output=True,
            )

            # Auto-format with Ruff
            subprocess.run(
                [sys.executable, "-m", "ruff", "format", "."],
                check=False,
                cwd=project_path,
                capture_output=True,
            )

            # Run various tools
            tools_to_test = [
                ([sys.executable, "-m", "pytest"], "Tests should pass"),
                (
                    [sys.executable, "-m", "ruff", "check", "."],
                    "Ruff check should pass",
                ),
                (
                    [sys.executable, "-m", "ruff", "format", "--check", "."],
                    "Ruff format should pass",
                ),
                (
                    [sys.executable, "-m", "mypy", "src/test_package"],
                    "MyPy should pass",
                ),
            ]

            for cmd, description in tools_to_test:
                result = subprocess.run(
                    cmd, check=False, cwd=project_path, capture_output=True, text=True
                )
                assert result.returncode == 0, f"{description}: {result.stderr}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
