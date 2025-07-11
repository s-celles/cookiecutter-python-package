{%- if cookiecutter.create_contributing == "y" %}
# Contributing to {{ cookiecutter.project_name }}

Thank you for your interest in contributing to {{ cookiecutter.project_name }}! This document provides guidelines and instructions for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python {{ cookiecutter.python_requires }}
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
   cd {{ cookiecutter.project_slug }}
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

{%- if cookiecutter.use_pre_commit == "y" %}

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```
{%- endif %}

## 🛠️ Development Workflow

### Code Style

{%- if cookiecutter.use_ruff == "y" %}
We use [Ruff](https://github.com/astral-sh/ruff) for code formatting and linting:

```bash
# Format code
ruff format

# Check for linting issues
ruff check

# Fix auto-fixable issues
ruff check --fix
```
{%- endif %}

{%- if cookiecutter.use_mypy == "y" %}

### Type Checking

We use [MyPy](https://mypy.readthedocs.io/) for static type checking:

```bash
mypy src/{{ cookiecutter.project_slug }}
```
{%- endif %}

{%- if cookiecutter.use_pytest == "y" %}

### Testing

We use [pytest](https://pytest.org/) for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov={{ cookiecutter.project_slug }}

# Run specific test file
pytest tests/test_core.py

# Run tests in parallel
pytest -n auto
```

Make sure to write tests for any new functionality you add.
{%- endif %}

{%- if cookiecutter.use_bandit == "y" %}

### Security

We use [Bandit](https://bandit.readthedocs.io/) for security checks:

```bash
bandit -r src/{{ cookiecutter.project_slug }}/
```
{%- endif %}

## 📝 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise commit messages
   - Add tests for new functionality
   - Update documentation as needed

3. **Run the test suite**
   ```bash
{%- if cookiecutter.use_pytest == "y" %}
   pytest
{%- else %}
   python -m unittest discover tests
{%- endif %}
   ```

{%- if cookiecutter.use_pre_commit == "y" %}

4. **Run pre-commit hooks**
   ```bash
   pre-commit run --all-files
   ```
{%- endif %}

5. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Provide a clear title and description
   - Reference any related issues
   - Ensure all CI checks pass

## 📋 Guidelines

### Code Quality

- Write clear, readable code
- Follow Python naming conventions (PEP 8)
- Add docstrings to all public functions and classes
- Keep functions and classes focused and small

### Documentation

- Update the README.md if you change functionality
{%- if cookiecutter.create_changelog == "y" %}
- Add entries to CHANGELOG.md for notable changes
{%- endif %}
- Write clear commit messages
- Add inline comments for complex logic

### Testing

- Write tests for all new functionality
- Ensure tests are isolated and repeatable
- Use descriptive test names
- Aim for high test coverage

## 🐛 Bug Reports

When filing a bug report, please include:

- Python version
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior
- Any relevant error messages

## 💡 Feature Requests

When requesting a feature:

- Clearly describe the use case
- Explain why it would be beneficial
- Consider if it fits the project's scope
- Be open to discussion about implementation

## 📜 Code of Conduct

{%- if cookiecutter.create_code_of_conduct == "y" %}
Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
{%- else %}
Please be respectful and professional in all interactions related to this project.
{%- endif %}

## 🙋 Questions?

If you have questions about contributing, please:

1. Check the existing issues and documentation
2. Open a new issue with the "question" label
3. Reach out to the maintainers

Thank you for contributing to {{ cookiecutter.project_name }}! 🎉
{%- endif %}
