# Testing & Quality Tools

Comprehensive testing and quality assurance tools ensure your code is reliable, maintainable, and follows best practices.

## 🧪 pytest

**What it is**: Modern Python testing framework

**Why important**:

- More readable test syntax than unittest
- Powerful fixtures for test setup
- Parametrized testing
- Rich plugin ecosystem
- Better error messages

### Comparison with unittest
```python
# pytest style - clean and readable
def test_addition():
    assert add(2, 3) == 5

# vs unittest style - verbose
class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add(2, 3), 5)
```

### Key Features

#### Fixtures
```python
@pytest.fixture
def user_data():
    return {"name": "John", "email": "john@example.com"}

def test_user_creation(user_data):
    user = User(**user_data)
    assert user.name == "John"
```

#### Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert square(input) == expected
```

### Configuration
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]
```

## 📊 Coverage

**What it is**: Measures how much of your code is tested

**Why important**:

- Identifies untested code paths
- Helps maintain high code quality
- Required by many CI/CD pipelines
- Shows where more tests are needed

### Usage
```bash
# Run tests with coverage
pytest --cov=src

# Generate HTML report
pytest --cov=src --cov-report=html

# Set coverage thresholds
pytest --cov=src --cov-fail-under=90
```

### Configuration
```toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
]
show_missing = true
fail_under = 90
```

### Coverage Reports

- **Terminal**: Quick overview with missing lines
- **HTML**: Detailed interactive reports
- **XML**: For CI/CD integration
- **JSON**: For programmatic processing

## ⚡ Tox

**What it is**: Testing across multiple Python versions

**Why important**:

- Ensures compatibility across Python versions
- Isolated testing environments
- Standardized testing commands
- Integration with CI systems

### Configuration (tox.ini)
```ini
[tox]
envlist = py38,py39,py310,py311,py312,lint,type

[testenv]
deps =
    pytest
    pytest-cov
commands = pytest {posargs}

[testenv:lint]
deps = ruff
commands =
    ruff check src tests
    ruff format --check src tests

[testenv:type]
deps = mypy
commands = mypy src
```

### Usage
```bash
# Run all environments
tox

# Run specific environment
tox -e py311

# Run with arguments
tox -e py311 -- -v tests/test_core.py
```

## 🔧 Nox

**What it is**: Flexible task automation (modern Tox alternative)

**Why important**:
- Python-based configuration (vs INI files)
- More flexible than Tox
- Better integration with modern tools
- Easier to customize

### Configuration (noxfile.py)
```python
import nox

@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def tests(session):
    session.install("pytest", "pytest-cov")
    session.install("-e", ".")
    session.run("pytest", *session.posargs)

@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", "src", "tests")
    session.run("ruff", "format", "--check", "src", "tests")

@nox.session
def type_check(session):
    session.install("mypy")
    session.install("-e", ".")
    session.run("mypy", "src")
```

### Usage
```bash
# List available sessions
nox --list

# Run all sessions
nox

# Run specific session
nox -s tests

# Run with arguments
nox -s tests -- -v tests/test_core.py
```

## 🎯 Testing Best Practices

### Test Organization
```
tests/
├── conftest.py          # Shared fixtures
├── test_core.py         # Core functionality tests
├── test_cli.py          # CLI tests
├── test_integration.py  # Integration tests
└── fixtures/            # Test data
    ├── sample_data.json
    └── mock_responses.py
```

### Writing Good Tests

#### 1. Clear Test Names
```python
def test_user_creation_with_valid_data():
    """Test that a user can be created with valid data."""
    pass

def test_user_creation_raises_error_with_invalid_email():
    """Test that user creation raises ValueError for invalid email."""
    pass
```

#### 2. Arrange-Act-Assert Pattern
```python
def test_user_full_name():
    # Arrange
    user = User(first_name="John", last_name="Doe")

    # Act
    full_name = user.get_full_name()

    # Assert
    assert full_name == "John Doe"
```

#### 3. Use Fixtures for Setup
```python
@pytest.fixture
def sample_user():
    return User(
        first_name="John",
        last_name="Doe",
        email="john@example.com"
    )

def test_user_email_validation(sample_user):
    assert sample_user.is_valid_email()
```

### Testing Different Scenarios

#### Happy Path
```python
def test_successful_user_login():
    user = User("john@example.com", "password123")
    assert user.login() is True
```

#### Error Cases
```python
def test_login_with_wrong_password():
    user = User("john@example.com", "wrong_password")
    with pytest.raises(AuthenticationError):
        user.login()
```

#### Edge Cases
```python
def test_empty_username():
    with pytest.raises(ValueError, match="Username cannot be empty"):
        User("", "password123")
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]

    - name: Run tests
      run: pytest --cov=src --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

This comprehensive testing setup ensures your code is thoroughly tested, compatible across Python versions, and maintains high quality standards.
