# Changelog

All notable changes to this cookiecutter template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite for the template itself
- Performance and stress testing
- Security and quality validation tests
- Documentation completeness tests
- Pre-commit hooks for template development
- GitHub Actions workflow for template CI/CD
- Dependabot configuration for automated updates
- Makefile with development commands
- CONTRIBUTING.md with detailed development guidelines
- conftest.py with shared test fixtures

### Changed
- Enhanced pyproject.toml with comprehensive tool configurations
- Improved test organization with proper fixtures and markers
- Better error handling in post-generation hooks

### Fixed
- Template validation and consistency checks
- Cross-platform compatibility issues
- Unicode handling in author names

## [2.0.0] - 2025-01-11

### Added
- Modern pyproject.toml-based configuration
- Support for Ruff (ultra-fast linter and formatter)
- MyPy integration for type checking
- Comprehensive GitHub Actions workflows
- Pre-commit hooks for code quality
- Bandit security scanning
- Safety dependency vulnerability checking
- MkDocs documentation support
- Sphinx documentation support (alternative)
- Multiple CLI frameworks (Typer, Click, Argparse)
- Tox and Nox for testing automation
- Commitizen for conventional commits
- Semantic release automation
- Docker and DevContainer support
- Dependabot integration
- CodeCov integration
- TOOLS_GUIDE.md explaining modern Python tools

### Changed
- Migrated from setup.py to pyproject.toml
- Updated to src/ layout (best practice)
- Modernized all tool configurations
- Improved template structure and organization

### Removed
- Legacy setup.py and setup.cfg support
- Outdated tool configurations
- Deprecated Python version support

## [1.0.0] - Previous Version

### Added
- Basic cookiecutter template structure
- Traditional setup.py configuration
- Basic testing setup
- Simple CI configuration

---

## Template Features Timeline

### Modern Python Packaging (2.0.0+)
- **pyproject.toml**: PEP 621 compliant project metadata
- **src/ layout**: Prevents accidental imports during development
- **Type hints**: Full typing support with py.typed marker

### Quality Assurance Tools
- **Ruff**: Lightning-fast linting and formatting
- **MyPy**: Static type checking
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checking
- **Coverage**: Test coverage measurement

### Automation & CI/CD
- **Pre-commit**: Automated quality checks on commit
- **GitHub Actions**: Comprehensive CI/CD pipelines
- **Dependabot**: Automated dependency updates
- **Semantic Release**: Automated versioning and releases

### Documentation
- **MkDocs**: Modern documentation with Material theme
- **Sphinx**: Traditional Python documentation (alternative)
- **README templates**: Comprehensive project documentation

### Development Experience
- **Multiple CLI options**: Typer, Click, or Argparse
- **Testing frameworks**: pytest with comprehensive configuration
- **Docker support**: Containerized development and deployment
- **DevContainer**: VS Code development containers

## Migration Guide

### From 1.x to 2.x

1. **Update build system**: Migrate from setup.py to pyproject.toml
2. **Adopt src/ layout**: Move package code to src/ directory
3. **Update CI/CD**: Use new GitHub Actions workflows
4. **Add quality tools**: Integrate Ruff, MyPy, and security scanners
5. **Update documentation**: Use modern documentation tools

### Breaking Changes in 2.x

- Requires Python 3.9+
- Uses pyproject.toml instead of setup.py
- src/ layout is now default
- Different tool configurations

## Compatibility Matrix

| Template Version | Python Versions | Build System | Layout |
|------------------|----------------|--------------|--------|
| 2.x              | 3.9-3.13       | pyproject.toml | src/   |
| 1.x              | 3.6-3.11       | setup.py      | flat   |

## Support Policy

- **Current version (2.x)**: Full support with new features and bug fixes
- **Previous version (1.x)**: Security fixes only (until EOL)
- **Python versions**: Support for currently maintained Python versions

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Development setup
- Testing procedures
- Code style guidelines
- Pull request process
