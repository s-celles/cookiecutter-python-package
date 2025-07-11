# Cookiecutter Python Package

A modern [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for Python packages with best practices built-in.

[![CI](https://github.com/s-celles/cookiecutter-python-package/actions/workflows/test.yml/badge.svg)](https://github.com/s-celles/cookiecutter-python-package/actions/workflows/test.yml)
[![Documentation](https://github.com/s-celles/cookiecutter-python-package/actions/workflows/docs.yml/badge.svg)](https://s-celles.github.io/cookiecutter-python-package/)
[![Python versions](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

!!! tip "Get Started in 30 Seconds"
    ```bash
    pip install cookiecutter
    cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
    ```

!!! warning "Development Status"
    This project is currently in active development.

!!! info "AI-Generated Content Notice"
    A significant portion of this project's content (including code, documentation, and examples) has been generated using AI assistance. Please review all code and documentation carefully before use in production environments. We recommend thorough testing and validation of any AI-generated components.

## What You Get

This template creates a Python package with modern best practices and industry-standard tools:

### 📦 **Modern Package Structure**
- **Source layout** (`src/` directory) for cleaner organization
- **PEP 621** compliant `pyproject.toml` configuration
- **Type hints** and `py.typed` marker for better IDE support
- **Entry points** for CLI applications

### 🧪 **Quality Assurance**
- **pytest** for modern testing with fixtures and parametrization
- **Coverage** reporting with HTML/XML output
- **Ruff** for ultra-fast linting and formatting
- **MyPy** for static type checking
- **Bandit** for security vulnerability scanning

### 🔧 **Development Tools**
- **uv** for ultra-fast package management (optional)
- **pre-commit** hooks for automated quality checks
- **GitHub Actions** for CI/CD automation
- **Dependabot** for dependency updates

### 🛠️ **CLI Support**
Choose your preferred CLI framework:
- **Typer** (modern, type-based)
- **Click** (decorator-based)
- **Argparse** (standard library)

### 📚 **Documentation Ready**
- **MkDocs** or **Sphinx** support
- **README** templates with badges
- **CHANGELOG** following Keep a Changelog format
- **Contributing** guidelines

## Quick Examples

=== "Minimal Package"
    Perfect for simple libraries:
    ```bash
    cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
    # Choose 'n' for most optional tools
    ```

=== "Full-Featured Package"
    Complete setup with all quality tools:
    ```bash
    cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
    # Choose 'y' for recommended tools
    ```

=== "CLI Application"
    Command-line application with Typer:
    ```bash
    cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
    # Select 'typer' for command_line_interface
    ```

## Why This Template?

!!! success "Modern Best Practices"
    - **PEP 621** compliant packaging
    - **Source layout** for cleaner imports
    - **Type hints** throughout
    - **Security scanning** built-in

!!! info "Developer Experience"
    - **Fast setup** with sensible defaults
    - **Comprehensive tooling** options
    - **Automated quality** checks
    - **CI/CD ready** workflows

!!! note "Flexibility"
    - **All tools optional** - choose what you need
    - **Multiple CLI frameworks** supported
    - **Documentation options** (MkDocs/Sphinx)
    - **Container support** with Docker

## Next Steps

1. **[Quick Start](getting-started/quick-start.md)** - Create your first package in minutes
2. **[Configuration](configuration/template-options.md)** - Understand all available options
3. **[Tools Guide](tools/overview.md)** - Learn about included tools
4. **[Examples](getting-started/examples.md)** - See real-world usage patterns

## Community

- **[GitHub Repository](https://github.com/s-celles/cookiecutter-python-package)** - Source code and issues
- **[Contributing](development/contributing.md)** - Help improve the template
- **[Discussions](https://github.com/s-celles/cookiecutter-python-package/discussions)** - Ask questions and share ideas

---

*Built with ❤️ for the Python community*
