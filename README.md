# Cookiecutter Python Package

A modern [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for Python packages# Enable: all tools for maximum code quality
```

## ⚙️ Template Options

This template provides extensive customization options through `cookiecutter.json`:

### Project Information
- `full_name`: Your full name
- `email`: Your email address  
- `github_username`: Your GitHub username
- `project_name`: The project display name
- `project_slug`: Package/directory name (auto-generated)
- `project_short_description`: Brief project description
- `version`: Initial version (default: 0.1.0)
- `python_requires`: Minimum Python version (default: >=3.9)
- `license`: License type (MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, etc.)

### Development Tools
- `use_ruff`: Ultra-fast linter and formatter (recommended: y)
- `use_mypy`: Static type checking (recommended: y)
- `use_pytest`: Modern testing framework (recommended: y)
- `use_coverage`: Test coverage reporting (recommended: y)
- `use_pre_commit`: Pre-commit hooks for quality (recommended: y)
- `use_bandit`: Security linting (recommended: y)
- `use_safety`: Dependency vulnerability scanning (recommended: y)

### Documentation
- `use_sphinx`: Sphinx documentation (traditional)
- `use_mkdocs`: MkDocs documentation (modern Markdown)

### CI/CD & Automation  
- `use_github_actions`: GitHub Actions workflows (recommended: y)
- `use_dependabot`: Automated dependency updates
- `use_codecov`: Coverage reporting service
- `use_semantic_release`: Automated versioning and releases
- `use_commitizen`: Conventional commits

### Advanced Options
- `command_line_interface`: CLI framework (typer/click/argparse/none)
- `use_tox`: Multi-version testing
- `use_nox`: Flexible task automation
- `use_docker`: Container support
- `use_devcontainer`: VS Code development containers

## 🛠️ Tool Explanationsh best practices built-in.

[![CI](https://github.com/s-celles/cookiecutter-python-package/actions/workflows/ci.yml/badge.svg)](https://github.com/s-celles/cookiecutter-python-package/actions/workflows/ci.yml)
[![Python versions](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

This template creates a Python package with modern best practices:

### 📦 **Core Package Structure**
- Modern `pyproject.toml` configuration (PEP 621)
- Source layout (`src/` directory)
- Proper package metadata and dependencies
- Type hints and `py.typed` marker

### 🧪 **Testing & Quality Assurance**
- **pytest** - Modern testing framework with fixtures and parametrization
- **Coverage** - Test coverage reporting with HTML/XML output
- **Ruff** - Ultra-fast linting and formatting (replaces flake8, black, isort)
- **MyPy** - Static type checking for better code quality
- **Bandit** - Security linting to catch vulnerabilities
- **Safety** - Dependency vulnerability scanning

### 🔧 **Development Tools**
- **pre-commit** - Automated code quality checks before commits
- **Tox** - Testing across multiple Python versions
- **Nox** - Flexible task automation (alternative to Tox)
- **Commitizen** - Conventional commits and automated versioning

### 🚀 **CI/CD & Automation**
- **GitHub Actions** - Automated testing, linting, and deployment
- **Dependabot** - Automated dependency updates
- **Codecov** - Coverage reporting integration
- **Semantic Release** - Automated versioning and publishing

### 📚 **Documentation**
- **Sphinx** or **MkDocs** - Documentation generation
- **README.md** with badges and usage examples
- **CHANGELOG.md** following Keep a Changelog format
- **CONTRIBUTING.md** with development guidelines

### 🛠️ **Command Line Interface**
- **Typer**, **Click**, or **Argparse** support
- Automatic entry point configuration
- Built-in testing for CLI commands

### 🐳 **Containerization & Deployment**
- **Docker** support with multi-stage builds
- **Dev Container** configuration for VS Code
- **PyPI** publishing workflow

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)

```bash
pip install cookiecutter
```

### Create Your Package

```bash
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
```

You'll be prompted to configure your package:

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
use_ruff [y]: 
use_mypy [y]: 
use_pytest [y]: 
use_coverage [y]: 
use_pre_commit [y]: 
# ... more options
```

### After Creation

```bash
cd your-package-name
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install  # If you chose pre-commit
```

## Usage

This cookiecutter template can be used to create different types of Python packages:

### Basic Package
```bash
# Create a simple package with minimal setup
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
# Choose 'n' for most optional tools
```

### Library Package
```bash
# Create a library with testing and documentation
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
# Enable: pytest, coverage, sphinx/mkdocs, github actions
```

### CLI Application
```bash
# Create a command-line application
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
# Choose typer/click for command_line_interface
# Enable testing and pre-commit hooks
```

### Enterprise Package
```bash
# Create a package with all quality tools
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
# Enable: all tools for maximum code quality
```

## 🛠️ Tool Explanations

### Why These Tools Matter

| Tool | Purpose | Why Important |
|------|---------|---------------|
| **Ruff** | Linting & Formatting | 10-100x faster than flake8/black, combines multiple tools |
| **MyPy** | Type Checking | Catches bugs early, improves code documentation |
| **pytest** | Testing | Modern features, fixtures, parametrization |
| **pre-commit** | Quality Gates | Ensures consistent code quality before commits |
| **Bandit** | Security | Finds security vulnerabilities in your code |
| **Safety** | Dependency Security | Checks for vulnerable dependencies |
| **GitHub Actions** | CI/CD | Automated testing and deployment |
| **Dependabot** | Security | Automated dependency updates |

### Optional vs Required

All tools are **optional** - you can choose which ones to include based on your needs:

- **Minimal setup**: Just pyproject.toml and basic structure
- **Testing focus**: Add pytest, coverage, and pre-commit
- **Full setup**: All tools for maximum code quality and automation

## 📁 Generated Project Structure

```
your-package/
├── .github/                    # GitHub workflows and settings
│   ├── workflows/
│   │   ├── ci.yml             # Continuous Integration
│   │   └── release.yml        # Automated releases
│   └── dependabot.yml         # Dependency updates
├── src/
│   └── your_package/
│       ├── __init__.py
│       ├── core.py            # Main functionality
│       ├── cli.py             # Command line interface
│       └── py.typed           # Type checking marker
├── tests/
│   ├── __init__.py
│   ├── test_core.py           # Core functionality tests
│   └── test_cli.py            # CLI tests
├── docs/                      # Documentation (if enabled)
├── .gitignore                 # Git ignore patterns
├── .pre-commit-config.yaml    # Pre-commit hooks (if enabled)
├── pyproject.toml             # Project configuration
├── README.md                  # Project documentation
├── CHANGELOG.md               # Change log (if enabled)
├── CONTRIBUTING.md            # Contribution guidelines (if enabled)
├── LICENSE                    # License file
├── tox.ini                    # Tox configuration (if enabled)
├── noxfile.py                 # Nox configuration (if enabled)
└── Dockerfile                 # Docker configuration (if enabled)
```

## 🎯 Best Practices Included

### Code Quality
- Type hints throughout the codebase
- Docstrings for all public functions
- Comprehensive test coverage
- Security scanning with Bandit
- Dependency vulnerability checking

### Development Workflow
- Pre-commit hooks for consistent quality
- Automated testing in CI
- Code coverage reporting
- Automated dependency updates
- Semantic versioning

### Modern Python Packaging
- PEP 621 compliant pyproject.toml
- Source layout (src/ directory)
- Proper entry points for CLI tools
- Optional dependencies for development
- Type information (py.typed)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage)
- Built with modern Python packaging best practices
- Incorporates lessons learned from the Python community

## 📚 Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [pre-commit Documentation](https://pre-commit.com/)
