# Linting & Formatting Tools

Code quality tools ensure consistent style, catch common mistakes, and improve code maintainability across your project and team.

## ⚡ Ruff

📖 **Documentation**: [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

**What it is**: Ultra-fast Python linter and formatter

**Why important**:

- 10-100x faster than alternatives (flake8, black, isort)
- Combines multiple tools into one
- Consistent code style across team
- Catches common Python mistakes
- Automatically fixes many issues

### Tool Consolidation
```bash
# One tool replaces many:
# black (formatting) - https://black.readthedocs.io/
# isort (import sorting) - https://pycqa.github.io/isort/
# flake8 (linting) - https://flake8.pycqa.org/
# pyupgrade (syntax modernization) - https://github.com/asottile/pyupgrade
ruff format  # Format code
ruff check   # Lint code
```

### Configuration (pyproject.toml)
```toml
[tool.ruff]
target-version = "py38"
line-length = 88
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "ARG",  # flake8-unused-arguments
    "SIM",  # flake8-simplify
    "ICN",  # flake8-import-conventions
]
ignore = [
    "E501",  # line too long, handled by formatter
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.per-file-ignores]
"tests/**/*" = ["PLR2004", "S101", "TID252"]

[tool.ruff.isort]
known-first-party = ["my_package"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

### Key Features

#### Automatic Fixes
```bash
# Check and auto-fix issues
ruff check --fix

# Format code
ruff format

# Both in one command
ruff check --fix && ruff format
```

#### Rule Categories
- **E/W**: pycodestyle errors and warnings
- **F**: pyflakes (undefined names, unused imports)
- **I**: isort (import sorting)
- **B**: flake8-bugbear (common bugs)
- **C4**: flake8-comprehensions (list/dict comprehensions)
- **UP**: pyupgrade (modern Python syntax)
- **SIM**: flake8-simplify (code simplification)

### Before and After Examples

#### Import Sorting
```python
# Before
import os
import sys
from typing import List
import requests
from my_package import utils

# After (ruff format)
import os
import sys
from typing import List

import requests

from my_package import utils
```

#### Code Formatting
```python
# Before
def long_function_name(parameter_one,parameter_two,parameter_three,parameter_four):
    return parameter_one+parameter_two+parameter_three+parameter_four

# After (ruff format)
def long_function_name(
    parameter_one, parameter_two, parameter_three, parameter_four
):
    return parameter_one + parameter_two + parameter_three + parameter_four
```

## 🎯 MyPy (Type Checking)

📖 **Documentation**: [https://mypy.readthedocs.io/](https://mypy.readthedocs.io/)

**What it is**: Static type checker for Python

**Why important**:

- Catches type-related bugs before runtime
- Improves code documentation
- Better IDE support (autocomplete, refactoring)
- Easier code maintenance
- Gradual adoption possible

### Type Hints Examples
```python
# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Collection types
from typing import List, Dict, Optional

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def find_user(user_id: int) -> Optional[User]:
    # Returns User or None
    return database.get_user(user_id)

# Class with type hints
class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def is_adult(self) -> bool:
        return self.age >= 18
```

### MyPy Configuration (pyproject.toml)
```toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### Benefits of Type Checking
```python
# MyPy catches this error
def greet(name: str) -> str:
    return f"Hello, {name}!"

greet(123)  # Error: Argument 1 to "greet" has incompatible type "int"; expected "str"

# IDE benefits
user: User = get_user()
user.name  # IDE knows this is a string
user.  # IDE shows available methods/attributes
```

### Gradual Adoption
```python
# Start with Any type for gradual migration
from typing import Any

def legacy_function(data: Any) -> Any:
    # Can be migrated to proper types later
    return process_data(data)

# Ignore specific lines during transition
result = legacy_api_call()  # type: ignore[misc]
```

## 🔧 pre-commit

📖 **Documentation**: [https://pre-commit.com/](https://pre-commit.com/)

**What it is**: Git hooks that run before commits

**Why important**:

- Enforces code quality automatically
- Prevents bad code from entering repository
- Fast feedback loop for developers
- Consistent standards across team

### Configuration (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### Installation and Usage
```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run on all files (optional)
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

### What Runs on Each Commit
```bash
# Automatically runs on every commit:
# 1. Remove trailing whitespace
# 2. Fix end of files
# 3. Check YAML syntax
# 4. Check for large files
# 5. Check for merge conflicts
# 6. Lint code with Ruff (and fix issues)
# 7. Format code with Ruff
# 8. Check types with MyPy
```

## 🛠️ Make/Makefile

📖 **Documentation**: [https://www.gnu.org/software/make/manual/](https://www.gnu.org/software/make/manual/)

**What it is**: Simple task automation

**Why important**:

- Common interface for development tasks
- Easy onboarding for new developers
- Works across platforms
- Industry standard

### Example Makefile
```makefile
.PHONY: install install-dev test lint format type-check clean

install:
	pip install -e .

install-dev:
	pip install -e .[dev]

test:
	pytest

test-cov:
	pytest --cov=src --cov-report=html --cov-report=term

lint:
	ruff check src tests

format:
	ruff format src tests

type-check:
	mypy src

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

all: clean install-dev test lint type-check

ci: install-dev test lint type-check
```

### Usage
```bash
# Common development tasks
make install-dev    # Install development dependencies
make test          # Run tests
make lint          # Check code quality
make format        # Format code
make type-check    # Check types
make clean         # Clean build artifacts
make all           # Run full development setup
make ci            # Run CI checks locally
```

## 🔄 Tool Integration Workflow

### Development Workflow
```bash
# 1. Set up development environment
make install-dev
pre-commit install

# 2. Make changes to code
# ... edit files ...

# 3. Check code quality (optional, pre-commit will do this)
make lint
make type-check
make format

# 4. Run tests
make test

# 5. Commit (pre-commit runs automatically)
git add .
git commit -m "feat: add new feature"
```

### IDE Integration

#### VS Code Settings
📖 **VS Code Python Extension**: [https://marketplace.visualstudio.com/items?itemName=ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
📖 **Ruff Extension**: [https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

```json
{
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "none",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": true,
            "source.organizeImports.ruff": true
        }
    }
}
```

#### PyCharm Configuration
📖 **PyCharm Documentation**: [https://www.jetbrains.com/help/pycharm/](https://www.jetbrains.com/help/pycharm/)
📖 **Ruff Plugin**: [https://plugins.jetbrains.com/plugin/20574-ruff](https://plugins.jetbrains.com/plugin/20574-ruff)

- Enable Ruff plugin
- Configure MyPy integration
- Set up automatic formatting on save
- Enable import optimization

## 📋 Best Practices

### Tool Configuration
1. **Centralize configuration**: Use pyproject.toml when possible
2. **Version control configs**: Include all configuration files in git
3. **Document exceptions**: Comment any ignored rules or special cases
4. **Regular updates**: Keep tools updated for latest features and fixes

### Team Adoption
1. **Start gradually**: Introduce tools one at a time
2. **Provide training**: Ensure team understands tool benefits
3. **Automate enforcement**: Use pre-commit hooks and CI
4. **Be consistent**: Apply same standards across all projects

### Performance Tips
1. **Use Ruff**: Significantly faster than traditional tools
2. **Cache results**: Enable caching for MyPy and other tools
3. **Parallel execution**: Run tools in parallel in CI
4. **Incremental checks**: Only check changed files when possible

This comprehensive linting and formatting setup ensures your code maintains high quality, consistent style, and catches issues early in the development process.

## 📚 Related Tools & Documentation

### Core Tools
- **Ruff**: [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/) - Ultra-fast Python linter and formatter
- **MyPy**: [https://mypy.readthedocs.io/](https://mypy.readthedocs.io/) - Static type checker for Python
- **pre-commit**: [https://pre-commit.com/](https://pre-commit.com/) - Git hooks framework
- **Make**: [https://www.gnu.org/software/make/manual/](https://www.gnu.org/software/make/manual/) - Build automation tool

### Tools Replaced by Ruff
- **Black**: [https://black.readthedocs.io/](https://black.readthedocs.io/) - Python code formatter
- **isort**: [https://pycqa.github.io/isort/](https://pycqa.github.io/isort/) - Import sorting utility
- **flake8**: [https://flake8.pycqa.org/](https://flake8.pycqa.org/) - Python linting tool
- **pyupgrade**: [https://github.com/asottile/pyupgrade](https://github.com/asottile/pyupgrade) - Python syntax modernizer

### IDE Extensions
- **VS Code Python**: [https://marketplace.visualstudio.com/items?itemName=ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- **VS Code Ruff**: [https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- **PyCharm Ruff Plugin**: [https://plugins.jetbrains.com/plugin/20574-ruff](https://plugins.jetbrains.com/plugin/20574-ruff)
