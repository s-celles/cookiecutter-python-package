# Quick Start

Get up and running with your new Python package in minutes!

## Prerequisites

- **Python 3.9+** installed on your system
- **Git** for version control
- **pip** or **uv** for package management

## Installation

Install cookiecutter:

=== "pip"
    ```bash
    pip install cookiecutter
    ```

=== "uv"
    ```bash
    uv tool install cookiecutter
    ```

=== "pipx"
    ```bash
    pipx install cookiecutter
    ```

## Create Your Package

1. **Generate the project**:
   ```bash
   cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
   ```

2. **Answer the prompts** (or press Enter for defaults):
   ```
   full_name [Your Name]: John Doe
   email [your.email@example.com]: john@example.com
   github_username [yourusername]: johndoe
   project_name [My Python Package]: Awesome Calculator
   project_slug [awesome_calculator]:
   project_short_description [A modern Python package with best practices built-in.]: A calculator library with advanced features
   version [0.1.0]:
   python_requires [>=3.9]:
   license [MIT]:
   use_uv [y]:
   use_ruff [y]:
   use_mypy [y]:
   use_pytest [y]:
   use_coverage [y]:
   use_pre_commit [y]:
   command_line_interface [typer]:
   # ... more options
   ```

3. **Navigate to your project**:
   ```bash
   cd awesome_calculator
   ```

## Set Up Development Environment

Choose your preferred package manager:

=== "uv (Recommended)"
    ```bash
    # Install dependencies
    uv sync

    # Install pre-commit hooks
    uv run pre-commit install

    # Run tests
    uv run pytest
    ```

=== "pip + venv"
    ```bash
    # Create virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install in development mode
    pip install -e ".[dev]"

    # Install pre-commit hooks
    pre-commit install

    # Run tests
    pytest
    ```

## Verify Everything Works

1. **Run the CLI** (if you chose a CLI interface):
   ```bash
   # With uv
   uv run awesome_calculator --help
   uv run awesome_calculator greet "World"

   # With activated venv
   awesome_calculator --help
   awesome_calculator greet "World"
   ```

2. **Run tests**:
   ```bash
   # With uv
   uv run pytest

   # With activated venv
   pytest
   ```

3. **Check code quality**:
   ```bash
   # With uv
   uv run ruff check src/ tests/
   uv run mypy src/

   # With activated venv
   ruff check src/ tests/
   mypy src/
   ```

## What's Next?

Your package is now ready for development! Here are some common next steps:

### 📝 **Customize Your Package**
- Edit `src/awesome_calculator/core.py` to add your functionality
- Update the CLI commands in `src/awesome_calculator/cli.py`
- Write tests in the `tests/` directory

### 🔄 **Development Workflow**
- Use `pre-commit` hooks to ensure quality (runs automatically on commit)
- Run `pytest` to test your changes
- Use `ruff` for linting and formatting

### 📚 **Documentation**
- Update `README.md` with your project details
- Add documentation in the `docs/` directory (if enabled)
- Keep `CHANGELOG.md` updated with your changes

### 🚀 **Publishing**
- Push to GitHub to trigger CI/CD workflows
- Use GitHub releases for versioning
- Publish to PyPI when ready

## Common Commands

| Task | uv | pip + venv |
|------|-----|-----------|
| Install deps | `uv sync` | `pip install -e ".[dev]"` |
| Run tests | `uv run pytest` | `pytest` |
| Run CLI | `uv run <package-name>` | `<package-name>` |
| Lint code | `uv run ruff check` | `ruff check` |
| Format code | `uv run ruff format` | `ruff format` |
| Type check | `uv run mypy src/` | `mypy src/` |

## Need Help?

- Check the [Configuration Guide](../configuration/template-options.md) for all available options
- See [Usage Examples](examples.md) for different package types
- Review the [Tools Guide](../tools/overview.md) to understand included tools
- Visit our [FAQ](../reference/faq.md) for common questions
