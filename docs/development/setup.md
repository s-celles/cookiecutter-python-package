# Development Setup

Guide for setting up a development environment to contribute to the Cookiecutter Python Package template itself.

## Prerequisites

### Required Software
- **Python 3.9+** (3.11+ recommended)
- **Git** for version control
- **Cookiecutter** for testing template generation

### Optional but Recommended
- **GitHub CLI** for easier repository management
- **VS Code** with recommended extensions
- **Docker** for testing in isolated environments

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/cookiecutter-python-package.git
cd cookiecutter-python-package

# Add upstream remote
git remote add upstream https://github.com/s-celles/cookiecutter-python-package.git
```

### 2. Development Environment Setup

#### Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (Command Prompt)
venv\Scripts\activate.bat
```

#### Install Development Dependencies
```bash
# Install the template in development mode
pip install -e .[dev]

# Verify installation
cookiecutter --version
```

### 3. Development Tools Setup

#### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks on all files (optional)
pre-commit run --all-files
```

#### VS Code Configuration
If using VS Code, install recommended extensions:
- Python
- Ruff
- YAML
- Jinja2
- GitLens

## Development Workflow

### Testing Template Changes

#### Basic Template Testing
```bash
# Test template generation with default values
cookiecutter . --no-input

# Test with specific configuration
cookiecutter . --no-input --config-file tests/configs/minimal.json

# Test interactively
cookiecutter .
```

#### Comprehensive Testing
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_template.py
pytest tests/test_hooks.py
pytest tests/test_validation.py

# Run with coverage
pytest --cov=. --cov-report=html
```

#### Testing Generated Projects
```bash
# Generate test project
cookiecutter . --no-input --output-dir /tmp/test-output

# Test the generated project
cd /tmp/test-output/my_python_package
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
pytest
```

### Code Quality Checks

#### Linting and Formatting
```bash
# Format code
ruff format .

# Check for linting issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

#### Type Checking
```bash
# Run MyPy (if enabled)
mypy hooks/ tests/
```

#### Security Scanning
```bash
# Check for security issues
bandit -r hooks/ tests/

# Check dependencies
safety check
```

## Template Structure

### Key Files and Directories

```
cookiecutter-python-package/
├── cookiecutter.json              # Template configuration
├── hooks/                         # Pre/post generation hooks
│   └── post_gen_project.py       # Post-generation processing
├── tests/                         # Template tests
│   ├── configs/                   # Test configurations
│   ├── test_template.py          # Template generation tests
│   ├── test_hooks.py             # Hook functionality tests
│   └── test_validation.py        # Input validation tests
├── docs/                          # Template documentation
├── {{cookiecutter.project_slug}}/ # Template directory
│   ├── src/                      # Package source code template
│   ├── tests/                    # Test template
│   ├── docs/                     # Documentation template
│   ├── .github/                  # GitHub workflows template
│   ├── pyproject.toml.jinja     # Project configuration template
│   └── README.md.jinja          # README template
├── pyproject.toml                # Template project configuration
├── .pre-commit-config.yaml       # Pre-commit configuration
└── README.md                     # Template documentation
```

### Template Files

Template files use Jinja2 syntax:

#### Variable Substitution
```jinja2
{# In {{cookiecutter.project_slug}}/pyproject.toml.jinja #}
[project]
name = "{{cookiecutter.project_slug}}"
description = "{{cookiecutter.project_short_description}}"
authors = [
    {name = "{{cookiecutter.full_name}}", email = "{{cookiecutter.email}}"},
]
```

#### Conditional Content
```jinja2
{# Include section only if tool is enabled #}
{% if cookiecutter.use_mypy == 'y' -%}
[tool.mypy]
python_version = "{{cookiecutter.python_requires.split('>=')[1]}}"
strict = true
{%- endif %}
```

#### File Inclusion/Exclusion
Files are conditionally included based on template variables:
- Files with `.jinja` extension are processed as templates
- Files without conditions are always included
- Post-generation hooks can remove unwanted files

### Hooks

#### post_gen_project.py
This script runs after template generation and:
- Removes unused files based on tool selection
- Sets up Git repository
- Installs dependencies (if requested)
- Initializes pre-commit hooks

```python
#!/usr/bin/env python3
"""Post-generation hook for cookiecutter template."""

import os
import shutil
from pathlib import Path

# Get template variables
use_mypy = "{{cookiecutter.use_mypy}}" == "y"
use_mkdocs = "{{cookiecutter.use_mkdocs}}" == "y"

# Remove files based on configuration
if not use_mypy:
    # Remove MyPy configuration
    pass

if not use_mkdocs:
    # Remove MkDocs files
    if Path("mkdocs.yml").exists():
        os.remove("mkdocs.yml")
    if Path("docs").exists():
        shutil.rmtree("docs")
```

## Writing Tests

### Test Categories

#### Template Generation Tests
```python
# tests/test_template.py
import pytest
from cookiecutter.main import cookiecutter

def test_default_generation(tmp_path):
    """Test template generation with default values."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(tmp_path)
    )

    project_dir = tmp_path / "my_python_package"
    assert project_dir.exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "src").exists()

def test_minimal_configuration(tmp_path):
    """Test minimal tool configuration."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(tmp_path),
        extra_context={
            "use_mypy": "n",
            "use_bandit": "n",
            "use_safety": "n",
        }
    )

    project_dir = tmp_path / "my_python_package"
    pyproject = (project_dir / "pyproject.toml").read_text()

    # Verify minimal configuration
    assert "[tool.mypy]" not in pyproject
    assert "[tool.bandit]" not in pyproject
```

#### Hook Tests
```python
# tests/test_hooks.py
def test_post_gen_hook_removes_unused_files(tmp_path):
    """Test that post-generation hook removes unused files."""
    result = cookiecutter(
        ".",
        no_input=True,
        output_dir=str(tmp_path),
        extra_context={"use_mkdocs": "n"}
    )

    project_dir = tmp_path / "my_python_package"

    # Verify MkDocs files were removed
    assert not (project_dir / "mkdocs.yml").exists()
    assert not (project_dir / "docs").exists()
```

#### Validation Tests
```python
# tests/test_validation.py
def test_invalid_project_name():
    """Test validation of project name."""
    with pytest.raises(Exception):
        cookiecutter(
            ".",
            no_input=True,
            extra_context={"project_name": "invalid-name!"}
        )
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_template.py

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run tests matching pattern
pytest -k "test_default"
```

## Documentation Updates

### Updating Documentation

When making changes that affect users:

1. **Update relevant documentation pages** in `docs/`
2. **Update README.md** if the change affects basic usage
3. **Update CHANGELOG.md** following Keep a Changelog format
4. **Test documentation builds** locally

```bash
# Install documentation dependencies
pip install mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

### Documentation Guidelines

- Use clear, concise language
- Include code examples for new features
- Update navigation in `mkdocs.yml` if adding new pages
- Test all code examples
- Use consistent formatting and style

## Contributing Guidelines

### Pull Request Process

1. **Create feature branch** from main
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** following code style guidelines

3. **Add tests** for new functionality

4. **Update documentation** as needed

5. **Run quality checks**
   ```bash
   pytest
   pre-commit run --all-files
   ```

6. **Commit with clear messages**
   ```bash
   git commit -m "feat: add support for new tool"
   git commit -m "fix: resolve issue with hook execution"
   git commit -m "docs: update installation guide"
   ```

7. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `ci:` - CI/CD changes
- `chore:` - Maintenance tasks

### Code Style Guidelines

- Follow PEP 8 (enforced by Ruff)
- Use type hints where appropriate
- Write clear docstrings
- Keep functions focused and small
- Use meaningful variable names
- Add comments for complex logic

## Release Process

### Preparing a Release

1. **Update version** in relevant files
2. **Update CHANGELOG.md** with release notes
3. **Create release PR** and get approval
4. **Tag release** after merging
5. **Create GitHub release** with release notes

### Testing Before Release

```bash
# Test template with multiple configurations
for config in tests/configs/*.json; do
    echo "Testing $config"
    cookiecutter . --no-input --config-file "$config" --output-dir /tmp/test-releases
done

# Test generated projects
cd /tmp/test-releases
for dir in */; do
    echo "Testing generated project: $dir"
    cd "$dir"
    python -m venv venv
    source venv/bin/activate
    pip install -e .[dev]
    pytest
    cd ..
done
```

This development setup ensures that contributions to the template maintain high quality and don't break existing functionality.
