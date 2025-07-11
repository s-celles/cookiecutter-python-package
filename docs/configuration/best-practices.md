# Best Practices

This guide outlines best practices for using the Cookiecutter Python Package template and maintaining high-quality Python projects.

## Project Setup Best Practices

### Planning Your Project

#### 1. Define Project Scope
- **Purpose**: Clearly define what your package does
- **Audience**: Identify who will use your package
- **Dependencies**: Minimize external dependencies
- **Compatibility**: Choose appropriate Python version range

#### 2. Choose the Right Tools
- **Start simple**: Don't enable all tools immediately
- **Add gradually**: Include tools as your project grows
- **Team consensus**: Ensure team agrees on tool choices
- **Learn tools**: Understand each tool before adding it

#### 3. Naming Conventions
- **Package name**: Use lowercase with underscores (PEP 8)
- **Project name**: Use descriptive, searchable names
- **Avoid conflicts**: Check PyPI for existing names
- **Be consistent**: Use same naming across all files

### Configuration Best Practices

#### pyproject.toml Structure
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "your-package"
description = "Clear, concise description"
readme = "README.md"
license = {file = "LICENSE"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
keywords = ["keyword1", "keyword2", "keyword3"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
requires-python = ">=3.9"
dependencies = [
    "requests>=2.25.0",
    # Pin major versions, allow minor/patch updates
]
dynamic = ["version"]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "ruff",
    "mypy",
    "pre-commit",
]
docs = [
    "mkdocs",
    "mkdocs-material",
]
test = [
    "pytest>=7.0",
    "pytest-cov",
    "pytest-mock",
]

[project.urls]
Homepage = "https://github.com/username/your-package"
Documentation = "https://your-package.readthedocs.io"
Repository = "https://github.com/username/your-package"
"Bug Tracker" = "https://github.com/username/your-package/issues"
Changelog = "https://github.com/username/your-package/blob/main/CHANGELOG.md"

[project.scripts]
your-package = "your_package.cli:main"

[tool.hatch.version]
path = "src/your_package/__init__.py"
```

#### Dependency Management
```toml
# Good: Specify minimum versions with flexibility
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0",
    "pydantic>=2.0.0,<3.0.0",
]

# Avoid: Exact pinning in libraries (use in applications)
dependencies = [
    "requests==2.31.0",  # Too restrictive for libraries
]

# Good: Group related optional dependencies
[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]
docs = ["mkdocs", "mkdocs-material"]
security = ["bandit", "safety"]
all = ["your-package[dev,docs,security]"]
```

## Code Quality Best Practices

### Code Organization

#### Directory Structure
```
your_package/
├── src/
│   └── your_package/
│       ├── __init__.py          # Package initialization
│       ├── core.py              # Core functionality
│       ├── cli.py               # Command-line interface
│       ├── exceptions.py        # Custom exceptions
│       ├── utils.py             # Utility functions
│       └── py.typed             # Type checking marker
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared test fixtures
│   ├── test_core.py             # Core functionality tests
│   ├── test_cli.py              # CLI tests
│   └── integration/             # Integration tests
│       └── test_integration.py
├── docs/                        # Documentation
├── scripts/                     # Development scripts
└── examples/                    # Usage examples
```

#### Module Design
```python
# Good: Clear module structure
# src/your_package/__init__.py
"""Your Package - A description of what it does."""

from .core import MainClass, main_function
from .exceptions import YourPackageError

__version__ = "0.1.0"
__all__ = ["MainClass", "main_function", "YourPackageError"]

# src/your_package/core.py
"""Core functionality for your package."""

from typing import Optional, List, Dict, Any
from .exceptions import YourPackageError

class MainClass:
    """Main class documentation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def main_method(self, input_data: str) -> str:
        """Process input data and return result."""
        if not input_data:
            raise YourPackageError("Input data cannot be empty")

        return f"Processed: {input_data}"
```

### Error Handling

#### Custom Exceptions
```python
# src/your_package/exceptions.py
"""Custom exceptions for your package."""

class YourPackageError(Exception):
    """Base exception for your package."""
    pass

class ValidationError(YourPackageError):
    """Raised when input validation fails."""
    pass

class ConfigurationError(YourPackageError):
    """Raised when configuration is invalid."""
    pass

# Usage in core module
def validate_input(data: str) -> None:
    """Validate input data."""
    if not isinstance(data, str):
        raise ValidationError(f"Expected string, got {type(data).__name__}")

    if len(data) < 3:
        raise ValidationError("Input must be at least 3 characters long")
```

#### Robust Error Handling
```python
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def safe_file_operation(file_path: Path) -> Optional[str]:
    """Safely read file with proper error handling."""
    try:
        return file_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except PermissionError:
        logger.error(f"Permission denied: {file_path}")
        return None
    except UnicodeDecodeError:
        logger.error(f"Could not decode file as UTF-8: {file_path}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error reading {file_path}: {e}")
        return None
```

### Type Hints Best Practices

#### Comprehensive Type Annotations
```python
from typing import (
    Dict, List, Optional, Union, Any, Callable, TypeVar, Generic,
    Protocol, runtime_checkable
)
from pathlib import Path

# Use specific types
def process_data(
    data: List[Dict[str, Any]],
    output_path: Path,
    processor: Callable[[Dict[str, Any]], Dict[str, Any]]
) -> bool:
    """Process data with type safety."""
    try:
        processed = [processor(item) for item in data]
        output_path.write_text(str(processed))
        return True
    except Exception:
        return False

# Use Protocols for duck typing
@runtime_checkable
class Processable(Protocol):
    """Protocol for objects that can be processed."""

    def process(self) -> Dict[str, Any]:
        """Process the object."""
        ...

def handle_processable(obj: Processable) -> Dict[str, Any]:
    """Handle any object that implements Processable protocol."""
    return obj.process()
```

## Testing Best Practices

### Test Organization

#### Test Structure
```python
# tests/test_core.py
"""Tests for core functionality."""

import pytest
from unittest.mock import Mock, patch
from your_package.core import MainClass
from your_package.exceptions import ValidationError

class TestMainClass:
    """Test MainClass functionality."""

    @pytest.fixture
    def main_instance(self):
        """Create MainClass instance for testing."""
        return MainClass({"setting": "value"})

    def test_initialization_default(self):
        """Test default initialization."""
        instance = MainClass()
        assert instance.config == {}

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"key": "value"}
        instance = MainClass(config)
        assert instance.config == config

    def test_main_method_success(self, main_instance):
        """Test successful processing."""
        result = main_instance.main_method("test input")
        assert result == "Processed: test input"

    def test_main_method_empty_input(self, main_instance):
        """Test error handling for empty input."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            main_instance.main_method("")

    @pytest.mark.parametrize("input_data,expected", [
        ("hello", "Processed: hello"),
        ("world", "Processed: world"),
        ("test123", "Processed: test123"),
    ])
    def test_main_method_various_inputs(self, main_instance, input_data, expected):
        """Test method with various inputs."""
        assert main_instance.main_method(input_data) == expected

# Integration tests
class TestIntegration:
    """Integration tests."""

    def test_end_to_end_workflow(self, tmp_path):
        """Test complete workflow."""
        # Setup
        input_file = tmp_path / "input.txt"
        input_file.write_text("test data")

        # Execute
        result = process_file(input_file)

        # Verify
        assert result is not None
        assert "Processed" in result
```

### Test Configuration
```python
# tests/conftest.py
"""Shared test configuration and fixtures."""

import pytest
import tempfile
from pathlib import Path
from your_package.core import MainClass

@pytest.fixture
def temp_dir():
    """Provide temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
    }

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration."""
    return {
        "debug": True,
        "timeout": 30,
        "retries": 3,
    }
```

## Documentation Best Practices

### README Structure
```markdown
# Project Name

Brief description of what the project does.

[![CI](https://github.com/user/repo/workflows/CI/badge.svg)](https://github.com/user/repo/actions)
[![PyPI version](https://badge.fury.io/py/package-name.svg)](https://badge.fury.io/py/package-name)
[![Python versions](https://img.shields.io/pypi/pyversions/package-name.svg)](https://pypi.org/project/package-name/)

## Features

- ✨ Feature 1
- 🚀 Feature 2
- 🔧 Feature 3

## Quick Start

```python
from package_name import MainClass

# Basic usage
instance = MainClass()
result = instance.process("your data")
print(result)
```

## Installation

```bash
pip install package-name
```

## Documentation

Full documentation is available at [docs.example.com](https://docs.example.com).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
```

### Docstring Standards
```python
def complex_function(
    data: List[Dict[str, Any]],
    threshold: float = 0.5,
    output_format: str = "json"
) -> Dict[str, Any]:
    """Process complex data with multiple options.

    This function processes a list of data dictionaries and applies
    various transformations based on the provided parameters.

    Args:
        data: List of dictionaries containing the data to process.
            Each dictionary should have 'value' and 'weight' keys.
        threshold: Minimum threshold for processing (default: 0.5).
            Values below this threshold will be filtered out.
        output_format: Format for output data. Supported formats:
            'json', 'csv', 'xml'. Default is 'json'.

    Returns:
        Dictionary containing processed results with keys:
        - 'processed_count': Number of items processed
        - 'filtered_count': Number of items filtered out
        - 'results': List of processed items
        - 'metadata': Processing metadata

    Raises:
        ValueError: If data is empty or contains invalid items.
        TypeError: If data items don't have required keys.
        UnsupportedFormatError: If output_format is not supported.

    Example:
        >>> data = [{'value': 0.8, 'weight': 1.0}, {'value': 0.3, 'weight': 0.5}]
        >>> result = complex_function(data, threshold=0.5)
        >>> result['processed_count']
        1

        >>> # With custom threshold
        >>> result = complex_function(data, threshold=0.2, output_format='csv')
        >>> result['processed_count']
        2

    Note:
        This function modifies the input data in-place for performance.
        If you need to preserve the original data, pass a copy.
    """
```

## Release and Deployment Best Practices

### Version Management
```python
# src/your_package/__init__.py
"""Package version management."""

__version__ = "0.1.0"

# Use semantic versioning
# MAJOR.MINOR.PATCH
# - MAJOR: Breaking changes
# - MINOR: New features (backward compatible)
# - PATCH: Bug fixes (backward compatible)
```

### Changelog Maintenance
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Changed feature description

### Deprecated
- Deprecated feature description

### Removed
- Removed feature description

### Fixed
- Bug fix description

### Security
- Security fix description

## [0.2.0] - 2023-10-01

### Added
- New CLI command for data processing
- Support for additional file formats

### Changed
- Improved error messages
- Updated dependencies

### Fixed
- Fixed memory leak in data processing
- Corrected edge case in validation

## [0.1.0] - 2023-09-01

### Added
- Initial release
- Core functionality
- Basic CLI interface
- Documentation
```

### Release Checklist
- [ ] Update version number
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Build and test package locally
- [ ] Create GitHub release
- [ ] Deploy to PyPI
- [ ] Announce release

## Security Best Practices

### Dependency Security
```bash
# Regular dependency updates
pip install --upgrade pip
pip list --outdated

# Security scanning
safety check
bandit -r src/
```

### Code Security
```python
# Good: Use environment variables for secrets
import os

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")

# Good: Validate inputs
def safe_filename(filename: str) -> str:
    """Create safe filename by removing dangerous characters."""
    import re
    return re.sub(r'[^a-zA-Z0-9._-]', '', filename)

# Good: Use secure random for tokens
import secrets

def generate_token(length: int = 32) -> str:
    """Generate cryptographically secure random token."""
    return secrets.token_urlsafe(length)
```

Following these best practices will help you create maintainable, secure, and professional Python packages that scale with your project's needs.
