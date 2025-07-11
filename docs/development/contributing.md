# Contributing

Thank you for your interest in contributing to this modern Python package template! This guide will help you get started.

## 🎯 Overview

This cookiecutter template helps developers create modern Python packages with best practices built-in. We welcome contributions that:

- Improve the template quality and usability
- Add support for new tools and practices
- Fix bugs and issues
- Enhance documentation
- Add comprehensive tests

## 🚀 Quick Start

1. **Fork and Clone**
   ```bash
   git clone https://github.com/s-celles/cookiecutter-python-package.git
   cd cookiecutter-python-package
   ```

2. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

4. **Run Tests**
   ```bash
   make test
   # Or manually:
   pytest
   ```

## 🛠️ Development Workflow

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Template files are in `{{cookiecutter.project_slug}}/`
   - Template configuration is in `cookiecutter.json`
   - Hooks are in `hooks/`
   - Tests are in `tests/`

3. **Test Your Changes**
   ```bash
   # Run all tests
   make test

   # Test template generation
   make bake-test

   # Run quality checks
   make check
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

### Testing Template Changes

When modifying the template, always test:

1. **Template Generation**
   ```bash
   cookiecutter . --no-input
   ```

2. **Different Configurations**
   ```bash
   # Test minimal config
   cookiecutter . --no-input use_ruff=n use_mypy=n

   # Test full config
   cookiecutter . --no-input use_ruff=y use_mypy=y use_github_actions=y
   ```

3. **Generated Project Quality**
   ```bash
   cd generated-project/
   pip install -e ".[dev]"
   pytest
   ruff check .
   mypy src/
   ```

## 📋 Types of Contributions

### 🔧 Template Improvements

- **Adding New Tools**: Update `cookiecutter.json`, template files, and documentation
- **Improving Configurations**: Enhance tool configurations for better defaults
- **File Structure**: Improve the generated project structure

### 🧪 Testing

- **Template Tests**: Add tests for template generation and validation
- **Generated Project Tests**: Ensure generated projects work correctly
- **Edge Cases**: Test unusual configurations and inputs

### 📚 Documentation

- **Usage Examples**: Add more usage examples and configurations
- **Tool Explanations**: Improve documentation with better explanations
- **README Updates**: Keep documentation current and comprehensive

### 🐛 Bug Fixes

- **Template Issues**: Fix problems with template generation
- **Configuration Bugs**: Fix issues with tool configurations
- **Cross-platform Issues**: Ensure template works on Windows, macOS, Linux

## 🎨 Code Style

### Template Files

- Use **4 spaces** for indentation in Python files
- Use **double quotes** for strings (Ruff default)
- Follow **PEP 8** guidelines
- Include **type hints** where appropriate

### Jinja2 Templates

- Use clear, readable Jinja2 syntax
- Add comments for complex conditionals
- Keep template logic simple and maintainable

Example:
```jinja2
{%- if cookiecutter.use_ruff == 'y' %}
# Ruff configuration
[tool.ruff]
line-length = 88
{%- endif %}
```

### Test Code

- Write **clear, descriptive** test names
- Include **docstrings** explaining test purpose
- Use **fixtures** for common setup
- Add **parametrized tests** for multiple scenarios

## 📝 Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `ci:` - CI/CD changes

Examples:
```bash
feat: add support for Poetry as build backend
fix: resolve Windows path issues in hooks
docs: update tools guide with MyPy explanation
test: add integration tests for CLI generation
```

## 🔍 Review Process

### Before Submitting

1. **Run Full Test Suite**
   ```bash
   make test-all
   make check
   make bake-test
   ```

2. **Update Documentation**
   - Update documentation for new tools
   - Update README for new features
   - Add docstrings and comments

3. **Test Multiple Configurations**
   - Test with different Python versions
   - Test on different operating systems
   - Test various tool combinations

### Pull Request Guidelines

1. **Clear Description**
   - Explain what changes were made
   - Include motivation and context
   - Link to related issues

2. **Test Coverage**
   - Include tests for new features
   - Ensure existing tests pass
   - Add integration tests where needed

3. **Documentation**
   - Update relevant documentation
   - Include examples for new features
   - Update changelog if applicable

## 🚦 CI/CD Pipeline

Our CI pipeline runs:

1. **Linting and Formatting**
   - Ruff for code quality
   - MyPy for type checking
   - Bandit for security

2. **Testing**
   - Unit tests for template logic
   - Integration tests for generation
   - Cross-platform testing

3. **Template Validation**
   - Generate projects with different configs
   - Test generated project quality
   - Verify all features work

## 🏗️ Template Architecture

### Directory Structure

```
cookiecutter-python-package/
├── cookiecutter.json          # Template configuration
├── hooks/                     # Post-generation hooks
│   └── post_gen_project.py   # Cleanup and setup script
├── tests/                     # Template tests
│   ├── test_template.py      # Template generation tests
│   ├── test_validation.py    # Validation tests
│   └── test_hooks.py         # Hook tests
├── {{cookiecutter.project_slug}}/  # Main template
│   ├── src/                   # Source code structure
│   ├── tests/                 # Test structure
│   ├── pyproject.toml        # Python project configuration
│   └── ...                   # Other project files
└── docs/                      # Template documentation
```

### Key Files

- **`cookiecutter.json`**: Defines all template variables and options
- **`hooks/post_gen_project.py`**: Cleans up unused files based on configuration
- **`{{cookiecutter.project_slug}}/pyproject.toml`**: Modern Python project configuration
- **Template tests**: Ensure template works correctly

## 🤝 Getting Help

### Questions and Discussions

- **GitHub Discussions**: For questions and ideas
- **Issues**: For bug reports and feature requests
- **Email**: Contact maintainers directly

### Resources

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Modern Python Tools](../tools/overview.md)

## 🎉 Recognition

Contributors are recognized:

- In the project README
- In release notes
- In the contributor's guide

Thank you for contributing to making Python development better for everyone! 🐍✨
