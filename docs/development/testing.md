# Testing the Template

Comprehensive guide for testing the Cookiecutter Python Package template to ensure it works correctly across different configurations and environments.

## Test Categories

### 1. Template Generation Tests
Verify that the template generates valid projects with different configurations.

### 2. Generated Project Tests
Ensure that generated projects work correctly and all tools function as expected.

### 3. Hook Tests
Test pre- and post-generation hooks execute correctly.

### 4. Integration Tests
End-to-end testing of the complete workflow.

### 5. Performance Tests
Verify template generation performance and resource usage.

## Setting Up Test Environment

### Test Dependencies
```bash
# Install test dependencies
pip install -e .[dev,test]

# Additional testing tools
pip install pytest-xdist pytest-mock pytest-cov
```

### Test Data Setup
```bash
# Create test configuration directory
mkdir -p tests/configs

# Create sample configurations for different scenarios
tests/
├── configs/
│   ├── minimal.json
│   ├── full-features.json
│   ├── cli-app.json
│   └── library.json
├── fixtures/
│   ├── sample_projects/
│   └── expected_outputs/
└── test_*.py
```

## Template Generation Tests

### Basic Generation Test
```python
# tests/test_template_generation.py
import pytest
import tempfile
from pathlib import Path
from cookiecutter.main import cookiecutter


@pytest.fixture
def temp_output_dir():
    """Provide temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


def test_default_generation(temp_output_dir):
    """Test template generation with default values."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir)
    )

    project_dir = temp_output_dir / "my_python_package"

    # Verify basic structure
    assert project_dir.exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "src" / "my_python_package").exists()
    assert (project_dir / "tests").exists()
    assert (project_dir / "README.md").exists()


def test_minimal_configuration(temp_output_dir):
    """Test minimal tool configuration."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir),
        extra_context={
            "project_name": "Minimal Package",
            "use_mypy": "n",
            "use_bandit": "n",
            "use_safety": "n",
            "use_pre_commit": "n",
            "use_mkdocs": "n",
        }
    )

    project_dir = temp_output_dir / "minimal_package"
    pyproject_content = (project_dir / "pyproject.toml").read_text()

    # Verify minimal configuration
    assert "[tool.mypy]" not in pyproject_content
    assert "[tool.bandit]" not in pyproject_content
    assert not (project_dir / ".pre-commit-config.yaml").exists()
    assert not (project_dir / "mkdocs.yml").exists()


def test_full_configuration(temp_output_dir):
    """Test full feature configuration."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir),
        extra_context={
            "project_name": "Full Feature Package",
            "use_mypy": "y",
            "use_bandit": "y",
            "use_safety": "y",
            "use_pre_commit": "y",
            "use_mkdocs": "y",
            "use_tox": "y",
            "use_docker": "y",
            "command_line_interface": "typer",
        }
    )

    project_dir = temp_output_dir / "full_feature_package"
    pyproject_content = (project_dir / "pyproject.toml").read_text()

    # Verify full configuration
    assert "[tool.mypy]" in pyproject_content
    assert "[tool.bandit]" in pyproject_content
    assert (project_dir / ".pre-commit-config.yaml").exists()
    assert (project_dir / "mkdocs.yml").exists()
    assert (project_dir / "tox.ini").exists()
    assert (project_dir / "Dockerfile").exists()
    assert (project_dir / "src" / "full_feature_package" / "cli.py").exists()


@pytest.mark.parametrize("cli_framework", ["typer", "click", "argparse", "none"])
def test_cli_frameworks(temp_output_dir, cli_framework):
    """Test different CLI framework configurations."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir),
        extra_context={
            "project_name": f"CLI {cli_framework.title()} Package",
            "command_line_interface": cli_framework,
        }
    )

    project_slug = f"cli_{cli_framework}_package"
    project_dir = temp_output_dir / project_slug
    cli_file = project_dir / "src" / project_slug / "cli.py"
    pyproject_content = (project_dir / "pyproject.toml").read_text()

    if cli_framework == "none":
        assert not cli_file.exists()
        assert "[project.scripts]" not in pyproject_content
    else:
        assert cli_file.exists()
        cli_content = cli_file.read_text()

        if cli_framework == "typer":
            assert "import typer" in cli_content
        elif cli_framework == "click":
            assert "import click" in cli_content
        elif cli_framework == "argparse":
            assert "import argparse" in cli_content

        assert "[project.scripts]" in pyproject_content
```

### Configuration Validation Tests
```python
# tests/test_validation.py
def test_invalid_project_names():
    """Test validation of invalid project names."""
    invalid_names = [
        "project with spaces",
        "project-with-dashes",
        "project.with.dots",
        "123numeric_start",
        "project!@#$%",
    ]

    for invalid_name in invalid_names:
        with pytest.raises(Exception):
            cookiecutter(
                ".",
                no_input=True,
                extra_context={"project_name": invalid_name}
            )


def test_python_version_validation():
    """Test Python version requirement validation."""
    valid_versions = [">=3.8", ">=3.9", ">=3.10", ">=3.11", ">=3.12"]
    invalid_versions = [">=3.7", "3.8", ">3.9", ">=3.13"]

    for version in valid_versions:
        # Should not raise exception
        cookiecutter(
            ".",
            no_input=True,
            output_dir="/tmp/test_python_versions",
            extra_context={"python_requires": version}
        )

    for version in invalid_versions:
        with pytest.raises(Exception):
            cookiecutter(
                ".",
                no_input=True,
                extra_context={"python_requires": version}
            )
```

## Generated Project Tests

### Functional Tests
```python
# tests/test_generated_projects.py
import subprocess
import os


def test_generated_project_installation(temp_output_dir):
    """Test that generated project can be installed."""
    # Generate project
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir)
    )

    project_dir = temp_output_dir / "my_python_package"

    # Create virtual environment and install
    venv_dir = project_dir / "test_venv"
    subprocess.run([
        "python", "-m", "venv", str(venv_dir)
    ], check=True)

    # Determine activation script
    if os.name == "nt":  # Windows
        pip_path = venv_dir / "Scripts" / "pip"
        python_path = venv_dir / "Scripts" / "python"
    else:  # Unix-like
        pip_path = venv_dir / "bin" / "pip"
        python_path = venv_dir / "bin" / "python"

    # Install package
    subprocess.run([
        str(pip_path), "install", "-e", ".[dev]"
    ], cwd=project_dir, check=True)

    # Test import
    result = subprocess.run([
        str(python_path), "-c", "import my_python_package; print('Import successful')"
    ], cwd=project_dir, capture_output=True, text=True)

    assert result.returncode == 0
    assert "Import successful" in result.stdout


def test_generated_project_tests(temp_output_dir):
    """Test that generated project tests pass."""
    # Generate project with pytest
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir),
        extra_context={"use_pytest": "y"}
    )

    project_dir = temp_output_dir / "my_python_package"

    # Setup environment
    venv_dir = project_dir / "test_venv"
    subprocess.run([
        "python", "-m", "venv", str(venv_dir)
    ], check=True)

    pip_path = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "pip"
    pytest_path = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "pytest"

    # Install and run tests
    subprocess.run([
        str(pip_path), "install", "-e", ".[dev]"
    ], cwd=project_dir, check=True)

    result = subprocess.run([
        str(pytest_path), "-v"
    ], cwd=project_dir, capture_output=True, text=True)

    assert result.returncode == 0
    assert "PASSED" in result.stdout


def test_cli_functionality(temp_output_dir):
    """Test CLI functionality in generated project."""
    # Generate project with CLI
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir),
        extra_context={
            "command_line_interface": "typer",
            "project_name": "CLI Test Package"
        }
    )

    project_dir = temp_output_dir / "cli_test_package"

    # Setup environment
    venv_dir = project_dir / "test_venv"
    subprocess.run([
        "python", "-m", "venv", str(venv_dir)
    ], check=True)

    pip_path = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "pip"
    python_path = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "python"

    # Install package
    subprocess.run([
        str(pip_path), "install", "-e", "."
    ], cwd=project_dir, check=True)

    # Test CLI command
    result = subprocess.run([
        str(python_path), "-m", "cli_test_package", "--help"
    ], cwd=project_dir, capture_output=True, text=True)

    assert result.returncode == 0
    assert "Usage:" in result.stdout or "help" in result.stdout.lower()
```

### Tool Configuration Tests
```python
# tests/test_tool_configs.py
def test_ruff_configuration(temp_output_dir):
    """Test Ruff configuration in generated project."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir),
        extra_context={"use_ruff": "y"}
    )

    project_dir = temp_output_dir / "my_python_package"

    # Check Ruff runs without errors
    result = subprocess.run([
        "ruff", "check", "src", "tests"
    ], cwd=project_dir, capture_output=True, text=True)

    # Should pass or only have fixable issues
    assert result.returncode in [0, 1]  # 0 = no issues, 1 = fixable issues


def test_mypy_configuration(temp_output_dir):
    """Test MyPy configuration in generated project."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir),
        extra_context={"use_mypy": "y"}
    )

    project_dir = temp_output_dir / "my_python_package"

    # Install MyPy and run type checking
    subprocess.run([
        "pip", "install", "mypy"
    ], check=True)

    result = subprocess.run([
        "mypy", "src"
    ], cwd=project_dir, capture_output=True, text=True)

    # Should pass type checking
    assert result.returncode == 0


def test_pre_commit_hooks(temp_output_dir):
    """Test pre-commit hooks in generated project."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir),
        extra_context={"use_pre_commit": "y"}
    )

    project_dir = temp_output_dir / "my_python_package"

    # Initialize git repository
    subprocess.run(["git", "init"], cwd=project_dir, check=True)
    subprocess.run(["git", "add", "."], cwd=project_dir, check=True)

    # Install pre-commit
    subprocess.run([
        "pip", "install", "pre-commit"
    ], check=True)

    # Install hooks
    subprocess.run([
        "pre-commit", "install"
    ], cwd=project_dir, check=True)

    # Run hooks
    result = subprocess.run([
        "pre-commit", "run", "--all-files"
    ], cwd=project_dir, capture_output=True, text=True)

    # Hooks should pass (or only have auto-fixable issues)
    assert result.returncode in [0, 1]
```

## Hook Tests

### Post-Generation Hook Tests
```python
# tests/test_hooks.py
def test_file_removal_hooks(temp_output_dir):
    """Test that hooks remove files based on configuration."""
    # Test MkDocs file removal
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir),
        extra_context={"use_mkdocs": "n"}
    )

    project_dir = temp_output_dir / "my_python_package"

    # MkDocs files should be removed
    assert not (project_dir / "mkdocs.yml").exists()
    assert not (project_dir / "docs").exists()


def test_dependency_installation_hook(temp_output_dir):
    """Test optional dependency installation."""
    # This would test if the hook offers to install dependencies
    # Implementation depends on hook behavior
    pass


def test_git_initialization_hook(temp_output_dir):
    """Test Git repository initialization."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(temp_output_dir)
    )

    project_dir = temp_output_dir / "my_python_package"

    # Git repository should be initialized
    assert (project_dir / ".git").exists()

    # Initial commit should exist
    result = subprocess.run([
        "git", "log", "--oneline"
    ], cwd=project_dir, capture_output=True, text=True)

    assert result.returncode == 0
    assert "Initial commit" in result.stdout or len(result.stdout.strip()) > 0
```

## Performance Tests

### Generation Speed Tests
```python
# tests/test_performance.py
import time


def test_generation_performance():
    """Test template generation performance."""
    start_time = time.time()

    result = cookiecutter(
        ".",
        no_input=True,
        output_dir="/tmp/perf_test"
    )

    end_time = time.time()
    generation_time = end_time - start_time

    # Should complete within reasonable time (adjust threshold as needed)
    assert generation_time < 30  # 30 seconds max


def test_memory_usage():
    """Test memory usage during generation."""
    import psutil
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    result = cookiecutter(
        ".",
        no_input=True,
        output_dir="/tmp/memory_test"
    )

    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory

    # Should not use excessive memory (adjust threshold as needed)
    assert memory_increase < 100 * 1024 * 1024  # 100MB max increase
```

## Integration Tests

### End-to-End Workflow Tests
```python
# tests/test_integration.py
def test_complete_workflow():
    """Test complete development workflow."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        project_dir = Path(tmp_dir) / "test_project"

        # 1. Generate project
        result = cookiecutter(
            ".",
            no_input=True,
            output_dir=str(Path(tmp_dir)),
            extra_context={
                "project_name": "Test Project",
                "use_pytest": "y",
                "use_ruff": "y",
                "use_mypy": "y",
                "command_line_interface": "typer"
            }
        )

        # 2. Setup development environment
        subprocess.run([
            "python", "-m", "venv", "venv"
        ], cwd=project_dir, check=True)

        pip_path = project_dir / "venv" / ("Scripts" if os.name == "nt" else "bin") / "pip"
        python_path = project_dir / "venv" / ("Scripts" if os.name == "nt" else "bin") / "python"

        # 3. Install package
        subprocess.run([
            str(pip_path), "install", "-e", ".[dev]"
        ], cwd=project_dir, check=True)

        # 4. Run tests
        result = subprocess.run([
            str(python_path), "-m", "pytest"
        ], cwd=project_dir, capture_output=True, text=True)
        assert result.returncode == 0

        # 5. Check code quality
        result = subprocess.run([
            str(python_path), "-m", "ruff", "check", "src", "tests"
        ], cwd=project_dir, capture_output=True, text=True)
        assert result.returncode in [0, 1]  # 0 or fixable issues

        # 6. Test CLI
        result = subprocess.run([
            str(python_path), "-m", "test_project", "--help"
        ], cwd=project_dir, capture_output=True, text=True)
        assert result.returncode == 0
```

## Running Tests

### Local Testing
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_template_generation.py
pytest tests/test_generated_projects.py
pytest tests/test_hooks.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run performance tests
pytest tests/test_performance.py

# Run integration tests
pytest tests/test_integration.py

# Parallel execution
pytest -n auto
```

### Continuous Integration Testing
```yaml
# .github/workflows/test.yml
name: Test Template
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev,test]

    - name: Run tests
      run: pytest --cov=. --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Test Configuration Files
```json
# tests/configs/minimal.json
{
    "project_name": "Minimal Test Package",
    "use_mypy": "n",
    "use_bandit": "n",
    "use_safety": "n",
    "use_pre_commit": "n",
    "use_mkdocs": "n",
    "command_line_interface": "none"
}

# tests/configs/full-features.json
{
    "project_name": "Full Featured Package",
    "use_mypy": "y",
    "use_bandit": "y",
    "use_safety": "y",
    "use_pre_commit": "y",
    "use_mkdocs": "y",
    "use_tox": "y",
    "use_docker": "y",
    "command_line_interface": "typer"
}
```

This comprehensive testing strategy ensures the template works correctly across different configurations, platforms, and use cases.
