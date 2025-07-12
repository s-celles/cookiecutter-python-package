{%- if cookiecutter.use_nox == "y" %}
"""Nox configuration for {{ cookiecutter.project_name }}."""

import nox

# Supported Python versions
PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]

# Default sessions to run
nox.options.sessions = [
    "tests",
{%- if cookiecutter.use_ruff == "y" %}
    "lint",
{%- endif %}
{%- if cookiecutter.use_mypy == "y" %}
    "type_check",
{%- endif %}
]


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run tests with pytest."""
    session.install("-e", ".[dev]")
{%- if cookiecutter.use_pytest == "y" %}
    session.run(
        "pytest",
        *session.posargs,
        env={"COVERAGE_FILE": f".coverage.{session.python}"},
    )
{%- else %}
    session.run("python", "-m", "unittest", "discover", "tests")
{%- endif %}


{%- if cookiecutter.use_ruff == "y" %}
@nox.session
def lint(session: nox.Session) -> None:
    """Run ruff linter and formatter."""
    session.install("ruff")
    session.run("ruff", "check", "src", "tests")
    session.run("ruff", "format", "--check", "src", "tests")


@nox.session
def format(session: nox.Session) -> None:
    """Format code with ruff."""
    session.install("ruff")
    session.run("ruff", "format", "src", "tests")
    session.run("ruff", "check", "--fix", "src", "tests")
{%- endif %}


{%- if cookiecutter.use_mypy == "y" %}
@nox.session
def type_check(session: nox.Session) -> None:
    """Run mypy type checker."""
    session.install("-e", ".[dev]")
    session.run("mypy", "src/{{ cookiecutter.project_slug }}")
{%- endif %}


{%- if cookiecutter.use_bandit == "y" or cookiecutter.use_safety == "y" %}
@nox.session
def security(session: nox.Session) -> None:
    """Run security checks."""
{%- if cookiecutter.use_bandit == "y" %}
    session.install("bandit")
    session.run("bandit", "-r", "src/{{ cookiecutter.project_slug }}/")
{%- endif %}
{%- if cookiecutter.use_safety == "y" %}
    session.install("safety")
    session.run("safety", "check")
{%- endif %}
{%- endif %}


@nox.session
def build(session: nox.Session) -> None:
    """Build the package."""
    session.install("build")
    session.run("python", "-m", "build")


{%- if cookiecutter.use_coverage == "y" and cookiecutter.use_pytest == "y" %}
@nox.session
def coverage(session: nox.Session) -> None:
    """Generate coverage report."""
    session.install("coverage")
    session.run("coverage", "combine")
    session.run("coverage", "report", "--show-missing")
    session.run("coverage", "html")
{%- endif %}


{%- if cookiecutter.use_sphinx == "y" or cookiecutter.use_mkdocs == "y" %}
@nox.session
def docs(session: nox.Session) -> None:
    """Build documentation."""
    session.install("-e", ".[docs]")
{%- if cookiecutter.use_sphinx == "y" %}
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")
{%- elif cookiecutter.use_mkdocs == "y" %}
    session.run("mkdocs", "build")
{%- endif %}
{%- endif %}
{%- endif %}
