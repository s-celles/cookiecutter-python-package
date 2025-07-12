# Cookiecutter Python Package

A modern [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for Python packages with best practices built-in.

[![CI](https://github.com/s-celles/cookiecutter-python-package/actions/workflows/test.yml/badge.svg)](https://github.com/s-celles/cookiecutter-python-package/actions/workflows/test.yml)
[![Documentation](https://github.com/s-celles/cookiecutter-python-package/actions/workflows/docs.yml/badge.svg)](https://s-celles.github.io/cookiecutter-python-package/)
[![Python versions](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

```bash
# Install cookiecutter
pip install cookiecutter

# Create your package
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
```

## 📋 Usage

After generating your project:

1. **Navigate to your project**: `cd your-project-name`
2. **Set up development environment**: `pip install -e .[dev]`
3. **Configure tools**: Choose from Ruff, MyPy, pytest, pre-commit, and more
4. **Start developing**: Write your code in `src/` with tests in `tests/`
5. **Run quality checks**: `make lint`, `make test`, `make type-check`
6. **Commit and push**: Pre-commit hooks ensure code quality

For detailed setup instructions, see our [Quick Start Tutorial](docs/getting-started/quick-start.md).

## ⚙️ Template Options

Customize your generated project by choosing from these options:

- **Build Backend**: setuptools, hatchling, flit, or pdm
- **Code Quality**: Ruff, MyPy, Bandit, Safety
- **Testing**: pytest, coverage reporting
- **Documentation**: MkDocs or Sphinx
- **CLI Framework**: Typer, Click, Argparse, or none
- **Package Management**: uv or pip
- **Automation**: pre-commit, GitHub Actions, Dependabot

See [Template Configuration](docs/configuration/template-options.md) for all available options.

## ✨ Features

- 📦 Modern `pyproject.toml` configuration (PEP 621)
- 🧪 Testing with pytest and coverage
- 🔍 Code quality with Ruff, MyPy, Bandit, Safety
- 🔧 Optional tools: uv, pre-commit, Tox, Nox
- 🚀 CI/CD with GitHub Actions
- 📚 Documentation with Sphinx or MkDocs
- 🐳 Docker and dev container support
- 🛠️ CLI support with Typer/Click/Argparse

## 📖 Documentation

For complete documentation, visit: **[Documentation Site](https://s-celles.github.io/cookiecutter-python-package)**

### Quick Links

- [Installation Guide](docs/getting-started/installation.md)
- [Quick Start Tutorial](docs/getting-started/quick-start.md)
- [Template Configuration](docs/configuration/template-options.md)
- [Available Tools](docs/tools/overview.md)
- [Contributing Guide](docs/development/contributing.md)

## 📚 What's Included

The generated package includes:

- Source layout with `src/` directory
- Comprehensive testing setup
- Code quality tools and linting
- CI/CD workflows
- Documentation framework
- Development tools and automation
- Security scanning
- Type checking support

## 🤝 Contributing

See our [Contributing Guide](docs/development/contributing.md) for details on how to contribute to this project.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.
