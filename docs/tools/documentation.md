# Documentation Tools

Documentation tools help create, maintain, and publish comprehensive documentation for your Python projects.

## 📚 MkDocs vs Sphinx

This template supports both MkDocs and Sphinx for documentation generation. Here's a comparison to help you choose:

### MkDocs (Recommended for most projects)

**What it is**: Static site generator focused on project documentation

**Pros**:
- **Markdown-based**: Easy to write and maintain
- **Fast setup**: Quick to get started
- **Modern themes**: Beautiful Material Design theme
- **Live reload**: Real-time preview during development
- **Simple configuration**: YAML-based configuration
- **GitHub Pages**: Easy deployment

**Best for**:
- API documentation
- User guides
- Getting started guides
- Small to medium projects
- Teams new to documentation

### Sphinx (Traditional choice)

**What it is**: Powerful documentation generator used by Python core

**Pros**:
- **reStructuredText**: More powerful markup than Markdown
- **Extensible**: Rich plugin ecosystem
- **Cross-references**: Advanced linking capabilities
- **API autodoc**: Automatic API documentation from docstrings
- **Multiple formats**: PDF, EPUB, HTML output
- **Python ecosystem standard**: Used by most major Python projects

**Best for**:
- Large, complex projects
- Academic or scientific documentation
- Projects requiring PDF output
- Extensive API documentation
- When you need advanced features

## 📖 MkDocs Setup

### Installation
```bash
pip install mkdocs mkdocs-material
```

### Configuration (mkdocs.yml)
```yaml
site_name: My Python Package
site_description: A modern Python package with best practices
site_url: https://username.github.io/my-package/
repo_url: https://github.com/username/my-package
repo_name: username/my-package

theme:
  name: material
  palette:
    # Light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode

    # Dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.path
    - navigation.top
    - search.highlight
    - search.share
    - content.code.copy
    - content.code.annotate

plugins:
  - search
  - git-revision-date-localized:
      enable_creation_date: true

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  - admonition
  - pymdownx.details
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - attr_list
  - md_in_html
  - tables

nav:
  - Home: index.md
  - Getting Started:
      - Quick Start: getting-started/quick-start.md
      - Installation: getting-started/installation.md
  - User Guide:
      - Configuration: user-guide/configuration.md
      - Usage Examples: user-guide/examples.md
  - API Reference:
      - Core Module: api/core.md
      - CLI Module: api/cli.md
  - Development:
      - Contributing: development/contributing.md
      - Testing: development/testing.md
```

### Directory Structure
```
docs/
├── index.md                    # Homepage
├── getting-started/
│   ├── quick-start.md         # Quick start guide
│   └── installation.md       # Installation instructions
├── user-guide/
│   ├── configuration.md      # Configuration options
│   └── examples.md           # Usage examples
├── api/
│   ├── core.md               # Core API documentation
│   └── cli.md                # CLI documentation
└── development/
    ├── contributing.md       # Contributing guidelines
    └── testing.md            # Testing documentation
```

### Building Documentation
```bash
# Serve locally with live reload
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## 📝 Sphinx Setup

### Installation
```bash
pip install sphinx sphinx-rtd-theme sphinx-autoapi
```

### Configuration (conf.py)
```python
# docs/source/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

project = 'My Python Package'
copyright = '2023, Your Name'
author = 'Your Name'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'autoapi.extension',
]

# Auto API configuration
autoapi_dirs = ['../../src']
autoapi_type = 'python'
autoapi_template_dir = '_templates'

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# HTML theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://docs.python-requests.org/en/stable/', None),
}
```

### reStructuredText Examples
```rst
API Reference
=============

Core Module
-----------

.. automodule:: my_package.core
   :members:
   :undoc-members:
   :show-inheritance:

CLI Module
----------

.. automodule:: my_package.cli
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

Basic usage::

    from my_package import MyClass

    instance = MyClass()
    result = instance.process_data(data)

Advanced usage:

.. code-block:: python

    from my_package import AdvancedClass

    # Create instance with configuration
    instance = AdvancedClass(
        option1=True,
        option2="custom_value"
    )

    # Process with callback
    result = instance.process_with_callback(
        data,
        callback=lambda x: print(f"Processing {x}")
    )

.. note::
   This is an important note about the API.

.. warning::
   Be careful when using this feature.
```

## 📋 Documentation Best Practices

### Content Organization

#### Homepage (index.md)
```markdown
# Project Name

Brief description of what the project does and why it's useful.

## Features

- ✨ Key feature 1
- 🚀 Key feature 2
- 🔧 Key feature 3

## Quick Example

```python
from my_package import example_function

result = example_function("hello world")
print(result)  # Output: processed hello world
```

## Installation

```bash
pip install my-package
```

## Next Steps

- [Quick Start Guide](getting-started/quick-start.md)
- [API Reference](api/core.md)
- [Examples](user-guide/examples.md)
```

#### API Documentation
```markdown
# Core API

## MyClass

::: my_package.core.MyClass
    options:
      show_root_heading: true
      show_source: true
      show_signature_annotations: true

### Example Usage

```python
from my_package import MyClass

# Create instance
instance = MyClass(config="value")

# Use methods
result = instance.process_data(input_data)
```

### Methods

#### process_data

Processes input data and returns result.

**Parameters:**
- `data` (str): Input data to process
- `options` (dict, optional): Processing options

**Returns:**
- `str`: Processed data

**Raises:**
- `ValueError`: If data is invalid
- `TypeError`: If data is not a string

**Example:**
```python
result = instance.process_data("hello")
assert result == "processed: hello"
```
```

### Docstring Standards

#### Google Style (Recommended)
```python
def process_data(data: str, options: Optional[Dict[str, Any]] = None) -> str:
    """Process input data with optional configuration.

    This function takes input data and processes it according to the
    specified options. The processing includes validation, transformation,
    and formatting.

    Args:
        data: The input data to process. Must be a non-empty string.
        options: Optional configuration dictionary. Supported keys:
            - format (str): Output format ('json' or 'text')
            - validate (bool): Whether to validate input

    Returns:
        The processed data as a formatted string.

    Raises:
        ValueError: If data is empty or invalid.
        TypeError: If data is not a string.

    Example:
        >>> process_data("hello", {"format": "json"})
        '{"result": "processed: hello"}'

        >>> process_data("world")
        'processed: world'
    """
```

#### NumPy Style
```python
def process_data(data: str, options: Optional[Dict[str, Any]] = None) -> str:
    """Process input data with optional configuration.

    Parameters
    ----------
    data : str
        The input data to process. Must be a non-empty string.
    options : dict, optional
        Optional configuration dictionary. Supported keys:

        * format : str
            Output format ('json' or 'text')
        * validate : bool
            Whether to validate input

    Returns
    -------
    str
        The processed data as a formatted string.

    Raises
    ------
    ValueError
        If data is empty or invalid.
    TypeError
        If data is not a string.

    Examples
    --------
    >>> process_data("hello", {"format": "json"})
    '{"result": "processed: hello"}'

    >>> process_data("world")
    'processed: world'
    """
```

## 🚀 Automated Documentation

### GitHub Pages Deployment
```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install mkdocs mkdocs-material
        pip install -e .

    - name: Build documentation
      run: mkdocs build

    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      run: mkdocs gh-deploy --force
```

### API Documentation from Docstrings
```bash
# Install mkdocstrings for automatic API docs
pip install mkdocstrings[python]
```

```yaml
# mkdocs.yml
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            show_signature_annotations: true
```

```markdown
# API Reference

::: my_package.core
    options:
      show_root_heading: true
      show_source: true
      members_order: source
```

## 📊 Documentation Analytics

### Google Analytics Integration
```yaml
# mkdocs.yml
google_analytics:
  - 'UA-XXXXXXXX-X'
  - 'auto'
```

### User Feedback
```html
<!-- Add to custom theme -->
<div class="feedback">
  <p>Was this page helpful?</p>
  <button onclick="trackFeedback('yes')">👍 Yes</button>
  <button onclick="trackFeedback('no')">👎 No</button>
</div>
```

## 📋 Documentation Checklist

### Content Quality
- [ ] Clear project description and purpose
- [ ] Installation instructions for all platforms
- [ ] Quick start guide with working examples
- [ ] Comprehensive API documentation
- [ ] Usage examples for common scenarios
- [ ] Troubleshooting section
- [ ] Contributing guidelines
- [ ] Changelog with version history

### Technical Quality
- [ ] All code examples are tested and working
- [ ] Documentation builds without errors
- [ ] Links are valid and up-to-date
- [ ] Search functionality works
- [ ] Mobile-responsive design
- [ ] Fast loading times
- [ ] Accessible design (WCAG compliance)

### Maintenance
- [ ] Automated builds on documentation changes
- [ ] Version synchronization with code
- [ ] Regular content reviews
- [ ] User feedback collection
- [ ] Analytics tracking
- [ ] Dead link checking

This comprehensive documentation setup ensures your project has professional, maintainable, and user-friendly documentation that helps users understand and adopt your software.
