# Release Process

This document outlines the complete process for releasing new versions of the Cookiecutter Python Package template.

## Release Types

### Patch Release (0.1.1)
- Bug fixes
- Documentation updates
- Minor configuration improvements
- Security patches

### Minor Release (0.2.0)
- New features
- New tool support
- Template structure improvements
- Backward-compatible changes

### Major Release (1.0.0)
- Breaking changes
- Major template restructuring
- Removal of deprecated features
- Significant workflow changes

## Pre-Release Checklist

### Code Quality
- [ ] All tests pass locally and in CI
- [ ] Code coverage meets minimum threshold (90%+)
- [ ] No security vulnerabilities detected
- [ ] Documentation is up to date
- [ ] All example configurations work

### Template Testing
- [ ] Generate projects with multiple configurations
- [ ] Test generated projects install and run correctly
- [ ] Verify all tool combinations work
- [ ] Test on multiple platforms (Windows, macOS, Linux)
- [ ] Test with multiple Python versions (3.9-3.12)

### Documentation
- [ ] README is accurate and complete
- [ ] CHANGELOG is updated with all changes
- [ ] Documentation builds without errors
- [ ] All links are working
- [ ] API examples are tested and current

## Version Management

### Semantic Versioning
This project follows [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes that require user action
- **MINOR**: New features that are backward compatible
- **PATCH**: Bug fixes and improvements

### Version Update Process

#### 1. Update Version Numbers
```bash
# Update version in pyproject.toml
[project]
version = "0.2.0"

# Update version in __init__.py (if applicable)
__version__ = "0.2.0"

# Update version in documentation (if hardcoded anywhere)
```

#### 2. Update CHANGELOG.md
```markdown
# Changelog

## [0.2.0] - 2024-01-15

### Added
- Support for uv package manager
- New security scanning tools
- Enhanced CLI templates

### Changed
- Improved documentation structure
- Updated default Python version to 3.9+

### Fixed
- Fixed issue with Windows path handling
- Resolved MyPy configuration conflicts

### Deprecated
- Old configuration format (will be removed in 1.0.0)

## [0.1.1] - 2023-12-01
...
```

## Release Workflow

### Step 1: Prepare Release Branch
```bash
# Create release branch from main
git checkout main
git pull origin main
git checkout -b release/v0.2.0

# Make version updates
# Update pyproject.toml, CHANGELOG.md, etc.

# Commit changes
git add .
git commit -m "chore: prepare release v0.2.0"
```

### Step 2: Final Testing
```bash
# Run comprehensive test suite
pytest tests/

# Test template generation with various configs
for config in tests/configs/*.json; do
    echo "Testing with $config"
    cookiecutter . --no-input --config-file "$config" --output-dir /tmp/release-test/
done

# Test generated projects
cd /tmp/release-test
for dir in */; do
    echo "Testing generated project: $dir"
    cd "$dir"
    python -m venv test-venv
    source test-venv/bin/activate
    pip install -e .[dev]
    pytest
    cd ..
done
```

### Step 3: Create Release PR
```bash
# Push release branch
git push origin release/v0.2.0

# Create PR via GitHub CLI or web interface
gh pr create \
    --title "Release v0.2.0" \
    --body "$(cat CHANGELOG.md | sed -n '/## \[0.2.0\]/,/## \[/p' | head -n -1)" \
    --base main \
    --head release/v0.2.0
```

### Step 4: Review and Merge
- [ ] Code review by maintainers
- [ ] All CI checks pass
- [ ] Documentation review
- [ ] Final testing approval
- [ ] Merge to main branch

### Step 5: Tag and Release
```bash
# Checkout main and pull latest
git checkout main
git pull origin main

# Create annotated tag
git tag -a v0.2.0 -m "Release version 0.2.0

- Added support for uv package manager
- New security scanning tools
- Enhanced CLI templates
- Improved documentation structure"

# Push tag
git push origin v0.2.0
```

### Step 6: Create GitHub Release
```bash
# Using GitHub CLI
gh release create v0.2.0 \
    --title "Release v0.2.0" \
    --notes "$(cat CHANGELOG.md | sed -n '/## \[0.2.0\]/,/## \[/p' | head -n -1)" \
    --prerelease  # Remove for stable releases

# Or create via GitHub web interface
```

## Automated Release (Optional)

### Using GitHub Actions
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

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Run tests
        run: |
          pip install -e .[dev]
          pytest

      - name: Test template generation
        run: |
          for config in tests/configs/*.json; do
            cookiecutter . --no-input --config-file "$config" --output-dir /tmp/test/
          done

      - name: Extract release notes
        id: extract_notes
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          NOTES=$(awk '/^## \['$VERSION'\]/{flag=1; next} /^## \[/{flag=0} flag' CHANGELOG.md)
          echo "RELEASE_NOTES<<EOF" >> $GITHUB_OUTPUT
          echo "$NOTES" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: ${{ steps.extract_notes.outputs.RELEASE_NOTES }}
          draft: false
          prerelease: false
```

### Using Semantic Release
```bash
# Install semantic-release
npm install -g semantic-release @semantic-release/changelog @semantic-release/git

# Configure .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/git",
    "@semantic-release/github"
  ]
}

# Use conventional commits
git commit -m "feat: add support for new tool"
git commit -m "fix: resolve configuration issue"
git commit -m "feat!: breaking change description"
```

## Post-Release Tasks

### Immediate Tasks
- [ ] Verify release is published on GitHub
- [ ] Test template generation from GitHub URL
- [ ] Update project documentation links
- [ ] Announce release in README badges

### Communication
- [ ] Update main branch protection rules (if needed)
- [ ] Notify community via discussions/issues
- [ ] Update any external documentation
- [ ] Share on social media/forums (if appropriate)

### Monitoring
- [ ] Monitor for bug reports related to new release
- [ ] Watch for user feedback and questions
- [ ] Track adoption of new features
- [ ] Plan next release cycle

## Hotfix Process

For critical issues requiring immediate release:

### Step 1: Create Hotfix Branch
```bash
# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/v0.1.2

# Make minimal fix
# Update version to patch level
# Update CHANGELOG
```

### Step 2: Fast-Track Testing
```bash
# Run focused tests on the fix
pytest tests/test_specific_issue.py

# Test affected configurations only
cookiecutter . --no-input --config-file tests/configs/affected.json
```

### Step 3: Emergency Release
```bash
# Create PR and get expedited review
# Merge to main
# Tag and release immediately
git tag -a v0.1.2 -m "Hotfix v0.1.2: Critical bug fix"
git push origin v0.1.2
```

## Release Notes Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### 🎉 New Features
- Feature description with link to PR #123

### 🔧 Improvements
- Improvement description with link to PR #124

### 🐛 Bug Fixes
- Bug fix description with link to PR #125

### 📚 Documentation
- Documentation update description

### 🔒 Security
- Security fix description (if any)

### ⚠️ Breaking Changes
- Breaking change description with migration guide

### 📦 Dependencies
- Updated dependency information

### 🙏 Contributors
- @username1
- @username2

**Full Changelog**: https://github.com/s-celles/cookiecutter-python-package/compare/v0.1.0...v0.2.0
```

## Rollback Procedure

If a release has critical issues:

### Step 1: Assess Impact
- Determine severity of issue
- Check if hotfix is possible
- Evaluate rollback necessity

### Step 2: Emergency Hotfix (Preferred)
```bash
# Create hotfix as described above
git checkout -b hotfix/v0.2.1
# Fix issue, test, release
```

### Step 3: Rollback Release (Last Resort)
```bash
# Hide problematic release on GitHub
gh release edit v0.2.0 --draft

# Communicate issue to users
# Prepare fixed version ASAP
```

## Release Metrics

Track these metrics for each release:
- Time from tag to release publication
- Number of test failures during release process
- User adoption rate of new features
- Bug reports in first 48 hours post-release
- Community feedback and satisfaction

This systematic release process ensures high quality, reliable releases while maintaining clear communication with users and contributors.
