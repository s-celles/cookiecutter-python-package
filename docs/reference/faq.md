# FAQ

Frequently asked questions about the Cookiecutter Python Package template.

## General Questions

### What is this template for?

This template helps you create modern Python packages with best practices built-in. It's designed for:
- Python libraries and packages
- Command-line applications
- Web APIs and services
- Data science projects
- Any Python project that needs professional structure

### How is this different from other Python templates?

This template focuses on:
- **Modern tooling**: Uses latest tools like Ruff, uv, and modern GitHub Actions
- **Flexibility**: Choose only the tools you need
- **Performance**: Emphasizes fast tools (Ruff vs flake8+black+isort)
- **Best practices**: Incorporates years of Python packaging experience
- **Documentation**: Comprehensive guides and examples

### Do I need to use all the tools?

No! The template is designed to be modular. You can:
- Start with minimal setup (just Ruff + pytest)
- Add tools gradually as your project grows
- Skip tools you don't need or want to learn yet

## Tool-Specific Questions

### Why Ruff instead of flake8 + black + isort?

**Ruff advantages**:
- 10-100x faster than traditional tools
- Single tool replaces multiple tools
- Less configuration needed
- Same results with better performance
- Active development and rapid improvements

**When to stick with traditional tools**:
- Existing projects with extensive custom configurations
- Team strongly prefers separate tools
- Need specific plugins not available in Ruff

### Should I use uv or pip?

**Use uv when**:
- You want the fastest dependency resolution
- You're starting a new project
- You want modern Python tooling

**Use pip when**:
- Working with existing projects
- Team is not ready to adopt new tools
- You need specific pip features not in uv

**You can always switch later** - both use the same `requirements.txt` and `pyproject.toml` formats.

### MkDocs vs Sphinx - which should I choose?

**Choose MkDocs when**:
- You prefer writing in Markdown
- You want a modern, clean theme out of the box
- Your documentation is primarily user-focused
- You want quick setup and deployment

**Choose Sphinx when**:
- You need advanced cross-referencing
- You want to generate PDF documentation
- You're working on a large, complex project
- You need the Python ecosystem standard

### Tox vs Nox - what's the difference?

**Tox**:
- INI-based configuration
- Mature and widely adopted
- Great for standard testing scenarios

**Nox**:
- Python-based configuration
- More flexible and programmable
- Easier to customize for complex scenarios

**Recommendation**: Start with Tox for simplicity, move to Nox if you need more flexibility.

## Project Setup Questions

### What Python versions should I support?

**Current recommendations** (as of 2024):
- **Minimum**: Python 3.9 (still has security support)
- **Recommended**: Python 3.10+ (better error messages, match statements)
- **Latest**: Python 3.12 (performance improvements)

**Consider your audience**:
- **Libraries**: Support 3.9+ for wider compatibility
- **Applications**: Can use newer versions (3.11+)
- **Enterprise**: Check company standards

### How do I handle dependencies?

**For libraries** (distributed on PyPI):
```toml
# Use minimum versions with flexibility
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0,<9.0.0",
]
```

**For applications** (deployed directly):
```toml
# More specific pinning is acceptable
dependencies = [
    "requests>=2.31.0,<3.0.0",
    "click==8.1.7",
]
```

### Should I include a CLI interface?

**Include CLI when**:
- Your package solves a problem users might want to run from command line
- You're building a tool or utility
- You want to provide easy access to main functionality

**Skip CLI when**:
- Building a pure library
- Functionality doesn't make sense as command-line tool
- API-only package

## Development Workflow Questions

### How do I set up my development environment?

```bash
# 1. Clone your generated project
cd your-project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install in development mode
pip install -e .[dev]

# 4. Set up pre-commit (if enabled)
pre-commit install

# 5. Run tests to verify setup
pytest
```

### What's the recommended development workflow?

```bash
# Daily workflow
git pull origin main
make test              # or pytest
make lint              # or ruff check src tests
make format            # or ruff format src tests

# Before committing (pre-commit handles this automatically)
make type-check        # or mypy src
make security-check    # or bandit -r src && safety check

# Commit (pre-commit runs automatically)
git add .
git commit -m "feat: add new feature"
git push
```

### How do I add new dependencies?

**For runtime dependencies**:
```toml
# Edit pyproject.toml
[project]
dependencies = [
    "existing-package>=1.0.0",
    "new-package>=2.0.0",  # Add here
]
```

**For development dependencies**:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "new-dev-tool>=1.0.0",  # Add here
]
```

**Then reinstall**:
```bash
pip install -e .[dev]
```

## Testing Questions

### How do I run tests?

```bash
# Basic test run
pytest

# With coverage
pytest --cov=src

# Specific test file
pytest tests/test_core.py

# Specific test function
pytest tests/test_core.py::test_function_name

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### How do I test CLI applications?

```python
# tests/test_cli.py
from typer.testing import CliRunner
from your_package.cli import app

runner = CliRunner()

def test_cli_basic():
    """Test basic CLI functionality."""
    result = runner.invoke(app, ["command", "--option", "value"])
    assert result.exit_code == 0
    assert "expected output" in result.stdout
```

### How do I mock external dependencies?

```python
# Using pytest-mock
def test_with_mock(mocker):
    """Test with mocked external call."""
    mock_requests = mocker.patch('your_package.core.requests.get')
    mock_requests.return_value.json.return_value = {"key": "value"}

    result = your_function()
    assert result == expected_result
    mock_requests.assert_called_once()

# Using unittest.mock
from unittest.mock import patch, Mock

@patch('your_package.core.external_service')
def test_with_patch(mock_service):
    """Test with patched service."""
    mock_service.return_value = Mock()
    mock_service.return_value.process.return_value = "result"

    result = your_function()
    assert result == "processed: result"
```

## Deployment Questions

### How do I publish to PyPI?

**Manual approach**:
```bash
# 1. Build package
python -m build

# 2. Upload to PyPI
twine upload dist/*
```

**Automated approach** (with GitHub Actions):
1. Tag your release: `git tag v1.0.0`
2. Push the tag: `git push origin v1.0.0`
3. GitHub Actions automatically builds and publishes

### How do I handle versioning?

**Manual versioning**:
```python
# src/your_package/__init__.py
__version__ = "0.1.0"
```

**Automatic versioning** (with semantic-release):
- Use conventional commits (`feat:`, `fix:`, `breaking:`)
- Semantic-release automatically increments version
- Generates changelog automatically

### How do I deploy documentation?

**GitHub Pages** (automatic with MkDocs):
```bash
mkdocs gh-deploy
```

**Read the Docs**:
1. Connect your GitHub repository
2. Enable the webhook
3. Documentation builds automatically on push

## Troubleshooting

### Pre-commit hooks are too slow

```yaml
# .pre-commit-config.yaml
# Add to slow hooks:
- id: mypy
  pass_filenames: false
  args: [--cache-dir=.mypy_cache]
```

### Import errors in tests

```python
# Make sure you installed in development mode
pip install -e .

# Check your PYTHONPATH includes src/
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

### CI fails but local tests pass

**Common causes**:
- Different Python versions
- Missing dependencies in CI
- Platform-specific issues
- Environment variables not set

**Solutions**:
- Test locally with same Python version as CI
- Check CI logs for specific errors
- Ensure all dependencies are declared
- Add debugging output to CI

### Tool configuration conflicts

**Ruff vs other formatters**:
```toml
# Don't use black if using ruff format
# Don't use isort if using ruff
[tool.ruff]
select = ["E", "W", "F", "I"]  # I = isort
```

**MyPy finding issues not caught locally**:
```toml
# Ensure consistent mypy config
[tool.mypy]
strict = true
warn_unused_ignores = true
```

## Getting Help

### Where can I get support?

1. **GitHub Issues**: [Template repository issues](https://github.com/s-celles/cookiecutter-python-package/issues)
2. **Discussions**: GitHub Discussions for questions and ideas
3. **Community**: Python Discord, Reddit r/Python
4. **Documentation**: Tool-specific documentation

### How do I contribute to the template?

1. Fork the repository
2. Create a feature branch
3. Test your changes with multiple configurations
4. Update documentation if needed
5. Submit a pull request

### How do I report bugs?

1. Check existing issues first
2. Provide minimal reproduction case
3. Include cookiecutter configuration used
4. Include error messages and logs
5. Specify your operating system and Python version

This FAQ should cover most common questions. If you have additional questions, please check the documentation or open an issue!
