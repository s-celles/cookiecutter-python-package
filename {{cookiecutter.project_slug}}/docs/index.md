{%- if cookiecutter.use_mkdocs == "y" %}
# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Features

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

## Quick Start

### Installation

```bash
pip install {{ cookiecutter.project_slug }}
```

### Basic Usage

```python
import {{ cookiecutter.project_slug }}

# Example usage
```

{%- if cookiecutter.command_line_interface != "none" %}

### Command Line Interface

```bash
{{ cookiecutter.project_slug }} --help
```
{%- endif %}

## Links

- [GitHub Repository](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
- [PyPI Package](https://pypi.org/project/{{ cookiecutter.project_slug }}/)
{%- if cookiecutter.create_changelog == "y" %}
- [Changelog](changelog.md)
{%- endif %}
{%- if cookiecutter.create_contributing == "y" %}
- [Contributing Guidelines](contributing.md)
{%- endif %}
{%- endif %}
