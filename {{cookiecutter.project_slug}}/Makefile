.PHONY: help install install-dev test test-cov lint format type-check security clean build docs serve-docs
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

{%- if cookiecutter.use_uv == "y" %}
install: ## Install the package
	uv pip install -e .

install-dev: ## Install package with development dependencies
	uv sync

{%- else %}
install: ## Install the package
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e ".[dev]"

{%- endif %}

{%- if cookiecutter.use_pytest == "y" %}
{%- if cookiecutter.use_uv == "y" %}
test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov={{ cookiecutter.project_slug }} --cov-report=html --cov-report=term-missing
{%- else %}
test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov={{ cookiecutter.project_slug }} --cov-report=html --cov-report=term-missing
{%- endif %}
{%- endif %}

{%- if cookiecutter.use_ruff == "y" %}
{%- if cookiecutter.use_uv == "y" %}
lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .
	uv run ruff check --fix .
{%- else %}
lint: ## Run linting
	ruff check .

format: ## Format code
	ruff format .
	ruff check --fix .
{%- endif %}
{%- endif %}

{%- if cookiecutter.use_mypy == "y" %}
{%- if cookiecutter.use_uv == "y" %}
type-check: ## Run type checking
	uv run mypy src/{{ cookiecutter.project_slug }}
{%- else %}
type-check: ## Run type checking
	mypy src/{{ cookiecutter.project_slug }}
{%- endif %}
{%- endif %}

{%- if cookiecutter.use_bandit == "y" %}
{%- if cookiecutter.use_uv == "y" %}
security: ## Run security checks
	uv run bandit -r src/{{ cookiecutter.project_slug }}/
{%- else %}
security: ## Run security checks
	bandit -r src/{{ cookiecutter.project_slug }}/
{%- endif %}
{%- endif %}

{%- if cookiecutter.use_pre_commit == "y" %}
{%- if cookiecutter.use_uv == "y" %}
pre-commit: ## Run pre-commit hooks
	uv run pre-commit run --all-files

install-hooks: ## Install pre-commit hooks
	uv run pre-commit install
{%- else %}
pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

install-hooks: ## Install pre-commit hooks
	pre-commit install
{%- endif %}
{%- endif %}

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
{%- if cookiecutter.use_uv == "y" %}
	rm -rf .venv/
{%- endif %}
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

{%- if cookiecutter.use_uv == "y" %}
build: ## Build package
	uv build
{%- else %}
build: ## Build package
	python -m build
{%- endif %}

{%- if cookiecutter.use_mkdocs == "y" %}
docs: ## Build documentation
	mkdocs build

serve-docs: ## Serve documentation locally
	mkdocs serve
{%- elif cookiecutter.use_sphinx == "y" %}
docs: ## Build documentation
	cd docs && make html

serve-docs: ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000
{%- endif %}

{%- if cookiecutter.use_tox == "y" %}
test-all: ## Run tests on all supported Python versions
	tox
{%- endif %}

{%- if cookiecutter.use_nox == "y" %}
nox: ## Run all nox sessions
	nox

nox-tests: ## Run only test sessions with nox
	nox -s tests
{%- endif %}
