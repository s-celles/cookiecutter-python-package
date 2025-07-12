# Template Options

This template provides extensive customization options through `cookiecutter.json`. You can configure every aspect of your Python package to match your specific needs.

## Project Information

### Basic Details
- **`full_name`**: Your full name (used in LICENSE and package metadata)
- **`email`**: Your email address (package author contact)
- **`github_username`**: Your GitHub username (for repository URLs)
- **`project_name`**: The display name of your project
- **`project_slug`**: Package/directory name (auto-generated from project_name)
- **`project_short_description`**: Brief project description for README and package metadata
- **`version`**: Initial version number (default: 0.1.0)
- **`python_requires`**: Minimum Python version (default: >=3.9)
- **`license`**: License type (MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, LGPL-3.0, MPL-2.0, Unlicense, Proprietary)

### Example Configuration
```json
{
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "github_username": "johndoe",
    "project_name": "Awesome Calculator",
    "project_slug": "awesome_calculator",
    "project_short_description": "A calculator library with advanced mathematical operations",
    "version": "0.1.0",
    "python_requires": ">=3.9",
    "license": "MIT"
}
```

## Development Tools

### Core Quality Tools
- **`use_ruff`** (default: y): Ultra-fast linter and formatter
  - Replaces flake8, black, isort, and pyupgrade
  - 10-100x faster than traditional tools
  - Recommended for all projects

- **`use_mypy`** (default: y): Static type checking
  - Catches type-related bugs early
  - Improves code documentation and IDE support
  - Enables better refactoring

- **`use_pytest`** (default: y): Modern testing framework
  - More readable than unittest
  - Powerful fixtures and parametrization
  - Rich plugin ecosystem

- **`use_coverage`** (default: y): Test coverage reporting
  - Identifies untested code paths
  - HTML and XML reports
  - CI/CD integration

### Package Management
- **`use_uv`** (default: y): Modern Python package manager
  - Ultra-fast dependency resolution
  - Built-in virtual environment management
  - Rust-based for speed
  - Alternative to pip/poetry

### Pre-commit Hooks
- **`use_pre_commit`** (default: y): Automated quality checks
  - Runs linting and formatting before commits
  - Prevents bad code from entering repository
  - Configurable hook selection

### Security Tools
- **`use_bandit`** (default: y): Security linting
  - Finds common security vulnerabilities
  - Scans for hardcoded secrets
  - Industry compliance support

- **`use_safety`** (default: y): Dependency vulnerability scanning
  - Checks for known security vulnerabilities
  - Automated alerts for security updates
  - Supply chain security

## Documentation Options

### Documentation Framework
- **`use_sphinx`** (default: n): Traditional Python documentation
  - reStructuredText-based
  - Powerful for complex documentation
  - Python ecosystem standard
  - PDF/EPUB output support

- **`use_mkdocs`** (default: y): Modern Markdown documentation
  - Easier to write and maintain
  - Beautiful Material Design theme
  - Fast setup and deployment
  - Live reload during development

!!! tip "Documentation Choice"
    For most projects, MkDocs is recommended due to its simplicity and modern appearance. Use Sphinx for large, complex projects that need advanced features.

## CI/CD & Automation

### Continuous Integration
- **`use_github_actions`** (default: y): GitHub Actions workflows
  - Automated testing on multiple Python versions
  - Cross-platform testing (Linux, Windows, macOS)
  - Free for open source projects

- **`use_dependabot`** (default: y): Automated dependency updates
  - Security vulnerability alerts
  - Automatic pull requests for updates
  - Configurable update frequency

### Code Quality Services
- **`use_codecov`** (default: y): Coverage reporting service
  - Visual coverage reports
  - Pull request integration
  - Coverage trend tracking

- **`use_semantic_release`** (default: n): Automated versioning
  - Conventional commit-based releases
  - Automated changelog generation
  - PyPI publishing automation

### Commit Standards
- **`use_commitizen`** (default: n): Conventional commits
  - Standardized commit message format
  - Automated versioning support
  - Better changelog generation

## Command Line Interface

- **`command_line_interface`** (default: typer): CLI framework choice
  - **typer**: Modern, type-based CLI framework (recommended)
  - **click**: Mature, decorator-based framework
  - **argparse**: Standard library option
  - **none**: No CLI interface

### CLI Framework Comparison

| Framework | Pros | Cons | Best For |
|-----------|------|------|----------|
| **Typer** | Type hints, auto-completion, modern | Newer, smaller ecosystem | New projects, type-heavy code |
| **Click** | Mature, extensive features, plugins | More verbose | Complex CLIs, existing Click knowledge |
| **Argparse** | Standard library, no dependencies | Verbose, limited features | Simple CLIs, minimal dependencies |

## Advanced Options

### Testing & Quality
- **`use_tox`** (default: n): Multi-version testing
  - Test across multiple Python versions
  - Isolated environments
  - Standardized commands

- **`use_nox`** (default: n): Flexible task automation
  - Python-based configuration
  - More flexible than Tox
  - Better tool integration

### Containerization
- **`use_docker`** (default: n): Container support
  - Dockerfile with multi-stage builds
  - Production-ready container
  - Development container support

- **`use_devcontainer`** (default: n): VS Code development containers
  - Consistent development environment
  - Pre-configured tools and extensions
  - Easy onboarding for contributors

## Project Types & Presets

### Quick Setup Presets

#### Minimal Package
```bash
# Answers for minimal setup
use_ruff: y
use_mypy: n
use_pytest: y
use_coverage: n
use_pre_commit: n
use_bandit: n
use_safety: n
use_github_actions: y
command_line_interface: none
```

#### Library Package
```bash
# Answers for library development
use_ruff: y
use_mypy: y
use_pytest: y
use_coverage: y
use_pre_commit: y
use_bandit: y
use_safety: y
use_github_actions: y
use_mkdocs: y
command_line_interface: none
```

#### CLI Application
```bash
# Answers for CLI application
use_ruff: y
use_mypy: y
use_pytest: y
use_coverage: y
use_pre_commit: y
use_bandit: y
use_safety: y
use_github_actions: y
use_mkdocs: y
command_line_interface: typer
```

#### Enterprise Package
```bash
# Answers for enterprise/team development
use_ruff: y
use_mypy: y
use_pytest: y
use_coverage: y
use_pre_commit: y
use_bandit: y
use_safety: y
use_github_actions: y
use_dependabot: y
use_codecov: y
use_mkdocs: y
use_tox: y
use_docker: y
command_line_interface: typer
```

## Configuration Tips

### Starting Simple
1. Begin with minimal configuration
2. Add tools gradually as you understand their value
3. Enable more tools as your project grows
4. Consider team expertise when choosing tools

### Tool Dependencies
Some tools work better together:
- **pytest + coverage**: Natural pairing for testing
- **ruff + mypy + pre-commit**: Comprehensive quality suite
- **github_actions + codecov**: CI/CD with coverage reporting
- **semantic_release + commitizen**: Automated release workflow

### Performance Considerations
- **Ruff**: Much faster than flake8/black/isort
- **uv**: Significantly faster than pip
- **MyPy**: Can be slow on large codebases (use incremental mode)
- **pre-commit**: Add `--hook-stage manual` for slow hooks

### License Compatibility
Make sure your license choice is compatible with your dependencies and usage:
- **MIT**: Most permissive, good for libraries
- **Apache-2.0**: Includes patent grant, good for larger projects
- **BSD-3-Clause**: Similar to MIT with additional attribution clause
- **GPL-3.0**: Copyleft, requires derivatives to be GPL
- **LGPL-3.0**: Lesser GPL, allows linking with proprietary code
- **MPL-2.0**: Mozilla Public License, file-level copyleft
- **Unlicense**: Public domain dedication
- **Proprietary**: Custom license for private/commercial use

This flexible configuration system allows you to create exactly the Python package structure you need, from simple scripts to complex enterprise applications.
