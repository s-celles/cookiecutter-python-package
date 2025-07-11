# Troubleshooting

Common issues and solutions when using the Cookiecutter Python Package template.

## Installation Issues

### Cookiecutter Command Not Found

**Problem**: `cookiecutter: command not found` after installation

**Solutions**:

#### Check PATH (Most Common)
```bash
# Check if cookiecutter is installed
pip show cookiecutter

# Find where it's installed
python -m pip show cookiecutter

# Add Scripts directory to PATH
# Windows (PowerShell)
$env:PATH += ";C:\Users\YourUser\AppData\Local\Programs\Python\Python311\Scripts"

# Linux/macOS (bash/zsh)
export PATH="$HOME/.local/bin:$PATH"
```

#### Use Python Module Syntax
```bash
# If command not found, use module syntax
python -m cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
```

#### Reinstall with User Flag
```bash
# Install for current user only
pip install --user cookiecutter

# Or use pipx for isolated installation
pipx install cookiecutter
```

### SSL Certificate Errors

**Problem**: SSL certificate verification failed

**Solutions**:

#### Update Certificates
```bash
# Update pip and certificates
pip install --upgrade pip certifi

# Upgrade cookiecutter
pip install --upgrade cookiecutter
```

#### Corporate Network/Firewall
```bash
# Use trusted hosts (temporary fix)
pip install --trusted-host pypi.org --trusted-host pypi.python.org cookiecutter

# Set proxy if needed
pip install --proxy http://proxy.company.com:8080 cookiecutter
```

### Permission Errors

**Problem**: Permission denied during installation

**Solutions**:

#### Windows
```powershell
# Run as Administrator or use --user flag
pip install --user cookiecutter
```

#### Linux/macOS
```bash
# Use user installation
pip install --user cookiecutter

# Or use sudo (not recommended)
sudo pip install cookiecutter
```

## Template Generation Issues

### Git Clone Failures

**Problem**: Cannot clone template repository

**Solutions**:

#### Use HTTPS Instead of SSH
```bash
# Use HTTPS (works everywhere)
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git

# Instead of SSH (requires key setup)
cookiecutter git@github.com:s-celles/cookiecutter-python-package.git
```

#### Download ZIP Alternative
```bash
# Download and extract manually
# Then use local path
cookiecutter /path/to/extracted/template
```

### Template Validation Errors

**Problem**: Invalid characters in project name

**Solutions**:

#### Valid Project Names
```bash
# Good examples
project_name: "My Python Package"
project_slug: "my_python_package"  # Auto-generated

# Avoid
project_name: "My-Package!" # Special characters
project_slug: "My Package"  # Spaces not allowed
```

#### Python Package Naming Rules
- Use lowercase letters
- Use underscores for separation
- No spaces or special characters
- Start with letter, not number
- Avoid Python keywords

### Directory Already Exists

**Problem**: Directory with same name already exists

**Solutions**:

#### Remove Existing Directory
```bash
# Remove existing directory
rm -rf existing_project_name

# Or use different name
# project_slug: "my_package_v2"
```

#### Use Different Location
```bash
# Generate in different directory
mkdir ~/projects
cd ~/projects
cookiecutter template_url
```

## Development Environment Issues

### Virtual Environment Problems

**Problem**: Virtual environment not activating or packages not found

**Solutions**:

#### Recreate Virtual Environment
```bash
# Remove old environment
rm -rf venv

# Create new environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify activation
which python  # Should show venv path
```

#### Python Version Issues
```bash
# Use specific Python version
python3.11 -m venv venv

# Or use pyenv
pyenv local 3.11.0
python -m venv venv
```

### Package Installation Failures

**Problem**: `pip install -e .[dev]` fails

**Solutions**:

#### Update pip and Build Tools
```bash
# Update pip
python -m pip install --upgrade pip

# Install build dependencies
pip install build setuptools wheel
```

#### Syntax Issues
```bash
# Use quotes on some shells
pip install -e ".[dev]"

# Or install separately
pip install -e .
pip install pytest ruff mypy
```

#### Check pyproject.toml Syntax
```bash
# Validate TOML syntax
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"

# Or use online TOML validator
```

### Import Errors

**Problem**: Cannot import your package modules

**Solutions**:

#### Verify Installation
```bash
# Check if package is installed
pip list | grep your_package

# Reinstall in development mode
pip install -e .
```

#### Check PYTHONPATH
```python
# In Python shell
import sys
print(sys.path)

# Should include your project src/ directory
```

#### Verify Package Structure
```bash
# Check __init__.py exists
ls src/your_package/__init__.py

# Check for syntax errors
python -m py_compile src/your_package/__init__.py
```

## Tool Configuration Issues

### Ruff Configuration Problems

**Problem**: Ruff not finding configuration or giving unexpected results

**Solutions**:

#### Check Configuration Location
```bash
# Ruff looks for config in these locations (in order):
# 1. pyproject.toml
# 2. ruff.toml
# 3. .ruff.toml

# Verify configuration is loaded
ruff check --show-settings
```

#### Common Configuration Issues
```toml
# pyproject.toml
[tool.ruff]
line-length = 88  # Not "line_length"
target-version = "py39"  # String, not py39

# Exclude patterns
exclude = [
    ".git",
    "__pycache__",
    ".venv",
]
```

### MyPy Type Checking Issues

**Problem**: MyPy errors that seem incorrect

**Solutions**:

#### Install Type Stubs
```bash
# Install type stubs for common packages
pip install types-requests types-setuptools

# Or use mypy to suggest stubs
mypy --install-types src/
```

#### Gradual Adoption
```python
# Use type: ignore for gradual migration
result = legacy_function()  # type: ignore[misc]

# Or ignore entire file temporarily
# mypy: ignore-errors
```

#### Configuration Issues
```toml
[tool.mypy]
python_version = "3.9"  # String, not number
ignore_missing_imports = true  # For packages without stubs
```

### Pre-commit Hook Failures

**Problem**: Pre-commit hooks fail or are too slow

**Solutions**:

#### Skip Hooks Temporarily
```bash
# Skip all hooks for one commit
git commit --no-verify -m "emergency fix"

# Skip specific hook
SKIP=mypy git commit -m "skip mypy for now"
```

#### Speed Up Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.0
    hooks:
      - id: mypy
        args: [--cache-dir=.mypy_cache]  # Enable caching
        pass_filenames: false  # Check all files at once
```

#### Debug Hook Issues
```bash
# Run specific hook manually
pre-commit run mypy --all-files

# Enable verbose output
pre-commit run --verbose mypy

# Update hooks
pre-commit autoupdate
```

## Testing Issues

### Pytest Discovery Problems

**Problem**: Pytest not finding tests

**Solutions**:

#### Check Test Discovery Rules
```bash
# Pytest looks for:
# - Files: test_*.py or *_test.py
# - Classes: Test* (and not __init__)
# - Functions: test_*

# Verify test discovery
pytest --collect-only
```

#### Configuration Issues
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

#### Import Issues in Tests
```python
# tests/conftest.py
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
```

### Coverage Issues

**Problem**: Coverage reports missing files or showing wrong percentages

**Solutions**:

#### Configuration Problems
```toml
[tool.coverage.run]
source = ["src"]  # Measure coverage in src/
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
]
```

#### Branch Coverage
```bash
# Enable branch coverage
pytest --cov=src --cov-branch

# Generate HTML report
pytest --cov=src --cov-report=html
```

## CI/CD Issues

### GitHub Actions Failures

**Problem**: CI passes locally but fails on GitHub Actions

**Solutions**:

#### Environment Differences
```yaml
# .github/workflows/ci.yml
- name: Debug environment
  run: |
    python --version
    pip --version
    pip list
    env | sort
```

#### Platform-Specific Issues
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.9", "3.10", "3.11", "3.12"]
  fail-fast: false  # Don't stop on first failure
```

#### Cache Issues
```yaml
# Clear cache if needed
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Secrets and Environment Variables

**Problem**: Tests fail due to missing secrets

**Solutions**:

#### Skip Tests Requiring Secrets
```python
import pytest
import os

@pytest.mark.skipif(
    not os.getenv("API_KEY"),
    reason="API_KEY not available"
)
def test_api_call():
    """Test that requires API key."""
    pass
```

#### Mock External Services
```python
@pytest.fixture
def mock_api_service(mocker):
    """Mock external API service."""
    return mocker.patch('your_package.api.external_service')
```

## Performance Issues

### Slow Tool Execution

**Problem**: Tools take too long to run

**Solutions**:

#### Ruff Optimization
```toml
[tool.ruff]
# Cache results
cache-dir = ".ruff_cache"

# Only check changed files in CI
# Use --diff flag in pre-commit
```

#### MyPy Optimization
```toml
[tool.mypy]
# Enable incremental mode
incremental = true
cache_dir = ".mypy_cache"

# Fast module lookup
namespace_packages = true
```

#### Parallel Test Execution
```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest -n auto
```

### Memory Issues

**Problem**: Tools consuming too much memory

**Solutions**:

#### Reduce Scope
```bash
# Check specific directories only
ruff check src/  # Instead of entire project
mypy src/       # Instead of all files
```

#### Increase System Limits
```bash
# Linux: Increase memory limits
ulimit -v 8000000  # 8GB virtual memory

# Or use containerized environment
```

## Documentation Issues

### MkDocs Build Failures

**Problem**: MkDocs fails to build documentation

**Solutions**:

#### Check YAML Syntax
```yaml
# mkdocs.yml - common issues
site_name: "Your Site"  # Use quotes for special characters
nav:
  - Home: index.md      # Ensure files exist
  - API: api/index.md   # Check all referenced files
```

#### Missing Files
```bash
# Check all referenced files exist
mkdocs serve --strict  # Fail on warnings

# List missing files
find docs/ -name "*.md" | while read file; do
  if ! grep -q "$(basename "$file")" mkdocs.yml; then
    echo "Unreferenced: $file"
  fi
done
```

#### Plugin Issues
```bash
# Install missing plugins
pip install mkdocs-material
pip install mkdocs-git-revision-date-localized-plugin

# Check plugin compatibility
mkdocs serve --verbose
```

## Getting More Help

### Enable Debug Mode

```bash
# Verbose output for most tools
cookiecutter --verbose template_url
pytest --verbose
ruff check --verbose
mypy --verbose src/
```

### Log Files and Debugging

```bash
# Enable Python debugging
export PYTHONVERBOSE=1

# Cookiecutter debug
cookiecutter --debug template_url

# Pre-commit debug
pre-commit run --verbose --all-files
```

### Community Support

1. **Search existing issues**: Check GitHub issues for similar problems
2. **Minimal reproduction**: Create minimal example that reproduces the issue
3. **Environment details**: Include OS, Python version, tool versions
4. **Error messages**: Include complete error messages and stack traces
5. **Configuration files**: Share relevant configuration (remove secrets)

### Creating Bug Reports

```bash
# Gather system information
python --version
pip --version
cookiecutter --version

# Include package versions
pip freeze > requirements-debug.txt

# Include configuration
cp pyproject.toml debug-pyproject.toml
cp .pre-commit-config.yaml debug-precommit.yaml
```

Remember: Most issues are configuration-related and can be solved by carefully checking file paths, syntax, and tool versions.
