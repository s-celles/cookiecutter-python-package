# Packaging & Build Tools

Modern Python packaging follows established standards and best practices to ensure your package is distributable, maintainable, and follows community conventions.

## 📦 pyproject.toml (PEP 621)

**What it is**: Modern Python project configuration file

**Why important**:
- Single source of truth for project metadata
- Replaces setup.py, setup.cfg, and requirements.txt
- Supported by all modern Python tools
- Better dependency management

### Key Benefits
- **Standardized**: Follows PEP 621 standard
- **Tool-agnostic**: Works with pip, poetry, hatch, etc.
- **Dependency management**: Clear separation of runtime vs development dependencies
- **Build system**: Configurable build backend (setuptools, hatchling, etc.)

### Example Configuration
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
description = "A great Python package"
readme = "README.md"
license = {file = "LICENSE"}
authors = [
    {name = "Your Name", email = "you@example.com"},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
requires-python = ">=3.8"
dependencies = [
    "requests>=2.25.0",
]
dynamic = ["version"]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "ruff",
    "mypy",
]

[project.urls]
Homepage = "https://github.com/username/my-package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/username/my-package"
```

## 🗂️ src/ Layout

**What it is**: Package code in `src/package_name/` directory

**Why important**:
- Prevents accidentally importing from source during development
- Cleaner separation between source and tests
- Industry best practice for Python packages
- Ensures tests run against installed package

### Directory Structure
```
project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
├── tests/
│   ├── test_core.py
│   └── test_cli.py
├── docs/
├── pyproject.toml
└── README.md
```

### Benefits
- **Import isolation**: Prevents accidental imports from source
- **Testing accuracy**: Tests run against the installed package
- **Distribution ready**: Package structure matches installed layout
- **Tool compatibility**: Works well with all modern Python tools

## 🔧 Build Tools

### Hatchling (Recommended)
- **Modern**: Built for pyproject.toml era
- **Fast**: Efficient build process
- **Standards-compliant**: Follows PEP standards
- **Plugin system**: Extensible for custom needs

### Setuptools (Traditional)
- **Mature**: Well-established and widely used
- **Compatible**: Works with legacy configurations
- **Feature-rich**: Extensive plugin ecosystem
- **Migration path**: Easy upgrade from setup.py

### Poetry (Alternative)
- **Dependency resolution**: Advanced dependency management
- **Virtual environments**: Built-in environment management
- **Publishing**: Integrated PyPI publishing
- **Lock files**: Reproducible builds

## 📋 MANIFEST.in

**Purpose**: Controls which files are included in source distributions

**When needed**:
- Including non-Python files (data, documentation)
- Excluding development files from distribution
- Custom file inclusion patterns

### Example
```
include README.md
include LICENSE
include CHANGELOG.md
recursive-include src/my_package *.py
recursive-include docs *.md *.rst
global-exclude *.pyc
global-exclude __pycache__
```

## Best Practices

1. **Use pyproject.toml**: Modern standard for project configuration
2. **Adopt src/ layout**: Better import isolation and testing
3. **Pin build dependencies**: Ensure reproducible builds
4. **Include necessary files**: Use MANIFEST.in for non-Python files
5. **Version management**: Use dynamic versioning or version files
6. **Metadata completeness**: Include all relevant project metadata
7. **Dependency specification**: Use appropriate version constraints
