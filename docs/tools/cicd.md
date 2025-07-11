# CI/CD Tools

Continuous Integration and Continuous Deployment tools automate testing, quality checks, and deployment processes to ensure reliable software delivery.

## 🚀 GitHub Actions

**What it is**: CI/CD automation platform integrated with GitHub

**Why important**:
- Automated testing on multiple Python versions
- Automated deployment to PyPI
- Cross-platform testing (Windows, macOS, Linux)
- Automatic dependency updates
- Free for open source projects

### Basic CI Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

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

    - name: Lint with Ruff
      run: |
        ruff check src tests
        ruff format --check src tests

    - name: Type check with MyPy
      run: mypy src

    - name: Test with pytest
      run: |
        pytest --cov=src --cov-report=xml --cov-report=term

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### Security Scanning Workflow
```yaml
# .github/workflows/security.yml
name: Security

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  security:
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
        pip install bandit[toml] safety
        pip install -e .

    - name: Run Bandit security scan
      run: |
        bandit -r src/ -f json -o bandit-report.json
        bandit -r src/

    - name: Run Safety dependency scan
      run: safety check --json --output safety-report.json

    - name: Upload security reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json
```

### Release Workflow
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Check package
      run: twine check dist/*

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*

    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
```

## 📦 Dependabot

**What it is**: Automated dependency updates

**Why important**:
- Security vulnerabilities in dependencies
- Keeps packages up-to-date automatically
- Reduces maintenance burden
- Configurable update frequency

### Configuration (.github/dependabot.yml)
```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    reviewers:
      - "maintainer-username"
    assignees:
      - "maintainer-username"
    commit-message:
      prefix: "deps"
      include: "scope"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    commit-message:
      prefix: "ci"
      include: "scope"
```

### Dependabot Configuration Options
```yaml
# Advanced Dependabot configuration
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"

    # Ignore specific dependencies
    ignore:
      - dependency-name: "requests"
        versions: ["2.x"]
      - dependency-name: "django"
        update-types: ["version-update:semver-major"]

    # Group updates
    groups:
      dev-dependencies:
        patterns:
          - "pytest*"
          - "ruff"
          - "mypy"

    # Custom branch naming
    target-branch: "develop"

    # Auto-merge (use with caution)
    auto-merge:
      enabled: true
      merge-method: "squash"
```

## 📊 Codecov

**What it is**: Code coverage reporting service

**Why important**:
- Visualizes test coverage
- Track coverage over time
- Integrates with pull requests
- Helps identify untested code

### Configuration (.codecov.yml)
```yaml
coverage:
  status:
    project:
      default:
        target: 90%
        threshold: 1%
    patch:
      default:
        target: 80%
        threshold: 1%

comment:
  layout: "reach,diff,flags,tree"
  behavior: default
  require_changes: false

ignore:
  - "tests/"
  - "docs/"
  - "**/__init__.py"
  - "src/*/cli.py"  # CLI modules often have coverage challenges
```

### GitHub Actions Integration
```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    flags: unittests
    name: codecov-umbrella
    fail_ci_if_error: true
```

## 🏷️ Semantic Release

**What it is**: Automated versioning and publishing

**Why important**:
- Consistent versioning based on commit messages
- Automated changelog generation
- Automated PyPI publishing
- Reduces manual release errors

### Configuration (.releaserc.json)
```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    [
      "@semantic-release/changelog",
      {
        "changelogFile": "CHANGELOG.md"
      }
    ],
    [
      "@semantic-release/exec",
      {
        "prepareCmd": "python -m build"
      }
    ],
    [
      "@semantic-release/github",
      {
        "assets": ["dist/*.tar.gz", "dist/*.whl"]
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": ["CHANGELOG.md", "pyproject.toml"],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ]
  ]
}
```

### Commit Message Convention
```bash
# Feature commits
feat: add new user authentication
feat(api): add user profile endpoint

# Bug fixes
fix: resolve login issue with special characters
fix(auth): handle expired tokens properly

# Breaking changes
feat!: change API response format
feat(api)!: remove deprecated endpoints

# Other types
docs: update installation guide
style: fix code formatting
refactor: simplify user service
test: add integration tests
chore: update dependencies
ci: improve GitHub Actions workflow
```

## 🎯 Advanced CI/CD Patterns

### Matrix Testing
```yaml
strategy:
  matrix:
    python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
    os: [ubuntu-latest, windows-latest, macos-latest]
    extras: ["minimal", "full"]
    include:
      - python-version: "3.11"
        os: ubuntu-latest
        extras: "dev"
        coverage: true
    exclude:
      - python-version: "3.8"
        os: macos-latest  # Skip if not needed
```

### Conditional Jobs
```yaml
jobs:
  test:
    if: github.event_name == 'pull_request'
    # ... test configuration

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: test
    # ... deployment configuration

  security-scan:
    if: github.event_name == 'schedule'
    # ... security scan configuration
```

### Caching
```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Cache pre-commit
  uses: actions/cache@v3
  with:
    path: ~/.cache/pre-commit
    key: ${{ runner.os }}-pre-commit-${{ hashFiles('.pre-commit-config.yaml') }}
```

### Parallel Jobs
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      # ... linting steps

  type-check:
    runs-on: ubuntu-latest
    steps:
      # ... type checking steps

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
    steps:
      # ... testing steps

  security:
    runs-on: ubuntu-latest
    steps:
      # ... security scanning steps

  build:
    needs: [lint, type-check, test, security]
    runs-on: ubuntu-latest
    steps:
      # ... build steps
```

## 🔐 Secrets Management in CI

### GitHub Secrets
```yaml
# Access secrets in workflows
env:
  PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
  CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
  SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
```

### Environment-specific Secrets
```yaml
jobs:
  deploy-staging:
    environment: staging
    env:
      DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

  deploy-production:
    environment: production
    env:
      DATABASE_URL: ${{ secrets.PRODUCTION_DATABASE_URL }}
```

## 📱 Notifications

### Slack Integration
```yaml
- name: Notify Slack on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
    message: "Build failed for ${{ github.ref }}"
```

### Email Notifications
```yaml
- name: Send email on release
  if: startsWith(github.ref, 'refs/tags/')
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: "New release: ${{ github.ref }}"
    body: "A new version has been released!"
    to: team@company.com
```

## 📋 CI/CD Best Practices

### Performance Optimization
1. **Use caching**: Cache dependencies and build artifacts
2. **Parallel execution**: Run independent jobs in parallel
3. **Fail fast**: Stop builds early on critical failures
4. **Optimize test selection**: Run only relevant tests for changes

### Security Best Practices
1. **Minimal permissions**: Use least privilege principle
2. **Secure secrets**: Use GitHub secrets, not environment variables
3. **Audit dependencies**: Regular security scans
4. **Signed commits**: Verify commit authenticity

### Reliability
1. **Retry on failure**: Handle transient failures
2. **Timeout limits**: Prevent hanging jobs
3. **Health checks**: Verify deployment success
4. **Rollback capability**: Quick recovery from failed deployments

### Monitoring
1. **Build metrics**: Track build times and success rates
2. **Deployment tracking**: Monitor deployment frequency
3. **Error alerts**: Immediate notification on failures
4. **Performance monitoring**: Track application metrics

This comprehensive CI/CD setup ensures your project maintains high quality, security, and reliability while automating the tedious aspects of software delivery.
