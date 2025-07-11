# {{ cookiecutter.project_name }}

[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml)
{%- if cookiecutter.use_codecov == "y" %}
[![codecov](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
{%- endif %}
[![PyPI version](https://badge.fury.io/py/{{ cookiecutter.project_slug }}.svg)](https://badge.fury.io/py/{{ cookiecutter.project_slug }})
[![Python versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_slug }}.svg)](https://pypi.org/project/{{ cookiecutter.project_slug }}/)
[![License: {{ cookiecutter.license }}](https://img.shields.io/badge/License-{{ cookiecutter.license }}-blue.svg)](https://opensource.org/licenses/{{ cookiecutter.license }})

{{ cookiecutter.project_short_description }}

## Installation

Install {{ cookiecutter.project_name }} from PyPI:

```bash
pip install {{ cookiecutter.project_slug }}
```

Or install the latest development version from GitHub:

```bash
pip install git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
```

## Quick Start

```bash
# Install from PyPI
pip install {{ cookiecutter.project_slug }}

# Install from source
pip install git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
```

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
