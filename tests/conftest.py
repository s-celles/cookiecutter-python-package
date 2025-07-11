"""Shared pytest fixtures for the cookiecutter template tests."""

import subprocess
import sys
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from cookiecutter.main import cookiecutter

# Explicitly tell pytest to ignore the template directory
collect_ignore = ["../{{cookiecutter.project_slug}}"]


@pytest.fixture(scope="session")
def template_dir() -> Path:
    """Return the path to the template directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_project_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test projects."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


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
        "project_name": "Test Package Full",
        "project_slug": "test_package_full",
        "project_short_description": "A test package with all features",
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


@pytest.fixture
def generated_minimal_project(
    template_dir: Path, minimal_context: dict[str, Any], temp_project_dir: Path
) -> Generator[Path, None, None]:
    """Generate a minimal test project."""
    result = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=minimal_context,
        output_dir=str(temp_project_dir),
    )

    project_path = Path(result)
    yield project_path


@pytest.fixture
def generated_full_project(
    template_dir: Path, full_context: dict[str, Any], temp_project_dir: Path
) -> Generator[Path, None, None]:
    """Generate a full-featured test project."""
    result = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=full_context,
        output_dir=str(temp_project_dir),
    )

    project_path = Path(result)
    yield project_path


@pytest.fixture
def installed_project(generated_minimal_project: Path) -> Generator[Path, None, None]:
    """Generate and install a test project."""
    project_path = generated_minimal_project

    # Install the project in development mode
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
        check=False,
        cwd=project_path,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        pytest.fail(f"Failed to install project: {result.stderr}")

    yield project_path

    # Cleanup - uninstall the package
    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", "test_package"],
        check=False,
        capture_output=True,
    )


@pytest.fixture(scope="session")
def cookiecutter_config() -> dict[str, Any]:
    """Load and validate cookiecutter.json configuration."""
    import json

    template_dir = Path(__file__).parent.parent
    config_file = template_dir / "cookiecutter.json"

    with open(config_file) as f:
        config: dict[str, Any] = json.load(f)

    return config


@pytest.fixture
def git_repo(temp_project_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary git repository."""
    repo_path = temp_project_dir / "test_repo"
    repo_path.mkdir()

    # Initialize git repo
    subprocess.run(["git", "init"], check=False, cwd=repo_path, capture_output=True)
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        check=False,
        cwd=repo_path,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        check=False,
        cwd=repo_path,
        capture_output=True,
    )

    yield repo_path


def pytest_configure(config: Any) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "bake: mark test as baking/generating projects")
    config.addinivalue_line("markers", "security: mark test as security-related")
    config.addinivalue_line("markers", "performance: mark test as performance-related")
    config.addinivalue_line("markers", "quality: mark test as code quality-related")


def pytest_collection_modifyitems(config: Any, items: list[Any]) -> None:
    """Modify test collection to add markers automatically."""
    for item in items:
        # Mark slow tests
        if "slow" in item.name or "performance" in item.name:
            item.add_marker(pytest.mark.slow)

        # Mark integration tests
        if "integration" in item.name or "workflow" in item.name:
            item.add_marker(pytest.mark.integration)

        # Mark baking tests
        if "bake" in item.name or "generation" in item.name or "generated" in item.name:
            item.add_marker(pytest.mark.bake)

        # Mark security tests
        if "security" in item.name or "bandit" in item.name or "safety" in item.name:
            item.add_marker(pytest.mark.security)

        # Mark quality tests
        if "quality" in item.name or "lint" in item.name or "format" in item.name:
            item.add_marker(pytest.mark.quality)
