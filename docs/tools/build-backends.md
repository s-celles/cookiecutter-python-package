# Build Backend Selection Guide

This guide helps you choose the right build backend for your Python package based on your project's needs and requirements.

## 🔧 Available Build Backends

### setuptools (Traditional)
📖 **Documentation**: [https://setuptools.pypa.io/](https://setuptools.pypa.io/)

**Best for**:
- Legacy projects requiring maximum compatibility
- Complex build requirements with C extensions
- Projects with existing setup.py configurations

**Pros**:
- ✅ Maximum compatibility across Python ecosystem
- ✅ Mature, battle-tested with extensive documentation
- ✅ Supports complex build scenarios and C extensions
- ✅ Wide tool support and community knowledge

**Cons**:
- ❌ Slower build times compared to modern alternatives
- ❌ More verbose configuration required
- ❌ Legacy baggage from older Python packaging era

**Configuration Example**:
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

---

### hatchling (Modern Default)
📖 **Documentation**: [https://hatch.pypa.io/](https://hatch.pypa.io/)

**Best for**:
- New projects starting fresh
- Teams wanting modern best practices
- Projects prioritizing build speed and simplicity

**Pros**:
- ✅ Fast build times with parallel processing
- ✅ Minimal configuration with sensible defaults
- ✅ Modern design following current best practices
- ✅ Excellent plugin ecosystem for extensibility
- ✅ Built-in support for src layout

**Cons**:
- ❌ Newer tool with smaller community (but growing rapidly)
- ❌ Less documentation for complex edge cases
- ❌ May require learning new configuration patterns

**Configuration Example**:
```toml
[build-system]
requires = ["hatchling>=1.26"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

---

### flit (Minimalist)
📖 **Documentation**: [https://flit.pypa.io/](https://flit.pypa.io/)

**Best for**:
- Pure Python packages with minimal complexity
- Developers who prefer extremely simple configuration
- Libraries without special build requirements

**Pros**:
- ✅ Ultra-simple configuration and setup
- ✅ Very fast builds for pure Python packages
- ✅ Designed specifically for pyproject.toml workflow
- ✅ Automatic inclusion of common files

**Cons**:
- ❌ Limited to pure Python packages only
- ❌ Fewer configuration options for complex needs
- ❌ Not suitable for packages with C extensions
- ❌ Smaller ecosystem compared to setuptools

**Configuration Example**:
```toml
[build-system]
requires = ["flit_core>=3.2,<4"]
build-backend = "flit_core.buildapi"

[tool.flit.module]
name = "my_package"
path = "src/my_package/__init__.py"
```

---

### pdm (Enterprise)
📖 **Documentation**: [https://pdm-project.org/](https://pdm-project.org/)

**Best for**:
- Team projects with complex dependency management
- Projects requiring dependency locking
- Organizations standardizing on PDM workflow

**Pros**:
- ✅ Advanced dependency resolution and locking
- ✅ Integrated project management features
- ✅ Modern PEP 582 support (local packages)
- ✅ Excellent for reproducible builds

**Cons**:
- ❌ Requires adopting PDM workflow ecosystem
- ❌ More complex than other build backends
- ❌ Newer tool with evolving best practices
- ❌ Additional learning curve for teams

**Configuration Example**:
```toml
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[tool.pdm.build]
includes = ["src/"]
package-dir = "src"
```

## 🎯 Decision Matrix

| Criteria | setuptools | hatchling | flit | pdm |
|----------|------------|-----------|------|-----|
| **Build Speed** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Compatibility** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Simplicity** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Features** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **C Extensions** | ✅ | ✅ | ❌ | ✅ |
| **Plugin System** | ✅ | ✅ | ❌ | ✅ |

## 🚀 Migration Guide

### From setuptools to hatchling
```bash
# 1. Update pyproject.toml
[build-system]
requires = ["hatchling>=1.26"]
build-backend = "hatchling.build"

# 2. Remove setup.py and setup.cfg if present
# 3. Add hatchling-specific configuration if needed
[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

### From any backend to setuptools
```bash
# Generally involves updating build-system section
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

# May need to add setup.py for complex builds
```

## 🛠️ Development Workflow Impact

### setuptools Workflow
```bash
# Traditional workflow
pip install -e .
python setup.py test
python setup.py bdist_wheel
```

### Modern Backend Workflow (hatchling/flit/pdm)
```bash
# Modern workflow
pip install -e .
python -m pytest
python -m build
```

## 🎯 Recommendations

### For New Projects
1. **Start with hatchling** - Modern, fast, well-designed
2. **Consider flit** if pure Python and simple requirements
3. **Use setuptools** only if compatibility is critical

### For Existing Projects
1. **Keep setuptools** if already working well
2. **Migrate to hatchling** for performance benefits
3. **Evaluate carefully** before changing working systems

### For Teams
1. **Standardize on one backend** across projects
2. **Document the choice** and rationale
3. **Provide migration guides** for existing projects

## 🔍 Backend-Specific Features

### hatchling Unique Features
- **Version management**: Dynamic versioning from VCS
- **Environment variables**: Build-time variable substitution
- **Custom hooks**: Extensible build process

### flit Unique Features
- **Automatic discovery**: Smart detection of package structure
- **Minimal metadata**: Extracts info from module docstrings
- **Upload integration**: Direct publishing to PyPI

### pdm Unique Features
- **Lock files**: Reproducible dependency resolution
- **Local packages**: PEP 582 __pypackages__ support
- **Script management**: Integrated task runner

## 📚 Further Reading

- [PEP 517 - Build System Interface](https://peps.python.org/pep-0517/)
- [PEP 518 - Build System Requirements](https://peps.python.org/pep-0518/)
- [Python Packaging Guide - Build Systems](https://packaging.python.org/en/latest/tutorials/packaging-projects/#choosing-a-build-backend)
- [Build Backend Comparison](https://pradyunsg.me/blog/2023/01/21/thoughts-on-python-packaging/)

Choose the backend that best fits your project's needs, team experience, and long-term maintenance goals. When in doubt, hatchling provides an excellent balance of modern features and practical usability.
