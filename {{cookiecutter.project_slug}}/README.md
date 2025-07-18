# {{ cookiecutter.project_name }}

[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml)
{%- if cookiecutter.use_codecov == "y" %}
[![codecov](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
{%- endif %}
[![PyPI version](https://badge.fury.io/py/{{ cookiecutter.project_slug }}.svg)](https://badge.fury.io/py/{{ cookiecutter.project_slug }})
[![Python versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_slug }}.svg)](https://pypi.org/project/{{ cookiecutter.project_slug }}/)
[![License: {{ cookiecutter.license }}](https://img.shields.io/badge/License-{{ cookiecutter.license }}-blue.svg)](https://opensource.org/licenses/{{ cookiecutter.license }})
{%- if cookiecutter.use_pre_commit == "y" %}
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
{%- endif %}
{%- if cookiecutter.use_commitizen == "y" %}
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
{%- endif %}
{%- if cookiecutter.use_ruff == "y" %}
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
{%- endif %}
{%- if cookiecutter.use_mypy == "y" %}
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
{%- endif %}
{%- if cookiecutter.use_bandit == "y" %}
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
{%- endif %}
{%- if cookiecutter.use_safety == "y" %}
[![Safety check](https://img.shields.io/badge/safety-checked-green.svg)](https://github.com/pyupio/safety)
{%- endif %}
{%- if cookiecutter.use_pytest == "y" %}
[![Tests](https://img.shields.io/badge/tests-pytest-blue.svg)](https://github.com/pytest-dev/pytest)
{%- endif %}
{%- if cookiecutter.use_github_actions == "y" %}
[![Release](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/release.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/release.yml)
{%- endif %}
{%- if cookiecutter.use_semantic_release == "y" %}
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)
{%- endif %}
{%- if cookiecutter.build_backend == "hatchling" %}
[![Built with: Hatch](https://img.shields.io/badge/built%20with-hatch-4051b5.svg)](https://github.com/pypa/hatch)
{%- elif cookiecutter.build_backend == "pdm" %}
[![Built with: PDM](https://img.shields.io/badge/built%20with-pdm-blueviolet.svg)](https://pdm.fming.dev/)
{%- elif cookiecutter.build_backend == "flit" %}
[![Built with: Flit](https://img.shields.io/badge/built%20with-flit-orange.svg)](https://flit.pypa.io/)
{%- endif %}
{%- if cookiecutter.use_uv == "y" %}
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
{%- endif %}
{%- if cookiecutter.use_mkdocs == "y" %}
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }})
{%- elif cookiecutter.use_sphinx == "y" %}
[![Documentation](https://img.shields.io/badge/docs-sphinx-blue.svg)](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }})
{%- endif %}
{%- if cookiecutter.build_backend == "hatchling" %}
[![Built with: Hatch](https://img.shields.io/badge/built%20with-hatch-4051b5.svg)](https://github.com/pypa/hatch)
{%- elif cookiecutter.build_backend == "pdm" %}
[![Built with: PDM](https://img.shields.io/badge/built%20with-pdm-blueviolet.svg)](https://pdm.fming.dev/)
{%- elif cookiecutter.build_backend == "flit" %}
[![Built with: Flit](https://img.shields.io/badge/built%20with-flit-orange.svg)](https://flit.pypa.io/)
{%- endif %}
{%- if cookiecutter.use_uv == "y" %}
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
{%- endif %}

{{ cookiecutter.project_short_description }}

## Installation

{%- if cookiecutter.use_uv == "y" %}

### Using uv (Recommended)

```bash
uv add {{ cookiecutter.project_slug }}
```

### Using pip

{%- endif %}

Install {{ cookiecutter.project_name }} from PyPI:

```bash
pip install {{ cookiecutter.project_slug }}
```

Or install the latest development version from GitHub:

```bash
pip install git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
```

## Quick Start

{%- if cookiecutter.use_uv == "y" %}

```bash
# Install with uv (recommended)
uv add {{ cookiecutter.project_slug }}

# Or install from PyPI
pip install {{ cookiecutter.project_slug }}

# Install from source
pip install git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
```

{%- else %}

```bash
# Install from PyPI
pip install {{ cookiecutter.project_slug }}

# Install from source
pip install git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
```

{%- endif %}

## ✨ Features

- Modern Python packaging with pyproject.toml
{%- if cookiecutter.use_ruff == "y" %}
- Fast linting and formatting with Ruff
{%- endif %}
{%- if cookiecutter.use_mypy == "y" %}
- Type checking with MyPy
{%- endif %}
{%- if cookiecutter.use_pytest == "y" %}
- Testing with pytest
{%- endif %}
{%- if cookiecutter.use_pre_commit == "y" %}
- Pre-commit hooks for code quality
{%- endif %}
{%- if cookiecutter.use_github_actions == "y" %}
- Automated CI/CD with GitHub Actions
{%- endif %}

## 🛠️ Development

### Setup Development Environment

{%- if cookiecutter.use_uv == "y" %}

#### Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager and project manager. It's much faster than pip and handles virtual environments automatically.

```bash
# Clone the repository
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Install dependencies and create virtual environment automatically
uv sync

# Install in development mode
uv pip install -e ".[dev]"

# Activate the virtual environment (optional, uv run handles this automatically)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

For most development tasks, you can use `uv run` which automatically activates the virtual environment:

```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check

# Run type checking
uv run mypy src/{{ cookiecutter.project_slug }}
```

#### Using pip/venv (Alternative)

{%- endif %}

```bash
# Clone the repository
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

{%- if cookiecutter.use_pre_commit == "y" %}

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install
```

Run hooks manually:

```bash
pre-commit run --all-files
```
{%- endif %}

{%- if cookiecutter.use_pytest == "y" %}

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov={{ cookiecutter.project_slug }}

# Run specific test file
pytest tests/test_{{ cookiecutter.project_slug }}.py
```
{%- endif %}

{%- if cookiecutter.use_ruff == "y" %}

### Code Quality

```bash
# Format code
ruff format

# Lint code
ruff check

# Fix auto-fixable issues
ruff check --fix
```
{%- endif %}

{%- if cookiecutter.use_mypy == "y" %}

### Type Checking

```bash
mypy src/{{ cookiecutter.project_slug }}
```
{%- endif %}

## Usage

```python
import {{ cookiecutter.project_slug }}

# Add your usage examples here
```

## 🤝 Contributing

{%- if cookiecutter.create_contributing == "y" %}
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
{%- else %}
Contributions are welcome! Please feel free to submit a Pull Request.
{%- endif %}

## 📝 License

This project is licensed under the {{ cookiecutter.license }} License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors
- Built with modern Python packaging best practices
