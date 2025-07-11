{%- if cookiecutter.create_changelog == "y" %}
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Basic functionality
{%- if cookiecutter.use_pytest == "y" %}
- Test suite with pytest
{%- endif %}
{%- if cookiecutter.use_ruff == "y" %}
- Code formatting and linting with Ruff
{%- endif %}
{%- if cookiecutter.use_mypy == "y" %}
- Type checking with MyPy
{%- endif %}
{%- if cookiecutter.use_pre_commit == "y" %}
- Pre-commit hooks for code quality
{%- endif %}
{%- if cookiecutter.use_github_actions == "y" %}
- CI/CD pipeline with GitHub Actions
{%- endif %}

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [{{ cookiecutter.version }}] - {% now 'local', '%Y-%m-%d' %}

### Added
- Initial release
- Project setup and configuration
{%- endif %}
