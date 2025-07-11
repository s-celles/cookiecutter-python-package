.PHONY: help clean test test-fast test-slow test-all lint format check install install-dev docs docs-serve bake-test

help: ## Show this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

install: ## Install the package
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev,docs]"

test: ## Run all tests
	pytest

test-fast: ## Run fast tests only (exclude slow tests)
	pytest -m "not slow"

test-slow: ## Run slow tests only
	pytest -m "slow"

test-all: ## Run all tests with coverage
	pytest --cov=. --cov-report=html --cov-report=term

lint: ## Run linting tools
	ruff check .
	mypy hooks/ tests/
	bandit -r hooks/ -ll

format: ## Format code
	ruff format .

check: ## Run all quality checks
	@echo "Running Ruff checks..."
	ruff check .
	@echo "Running Ruff format check..."
	ruff format --check .
	@echo "Running MyPy..."
	mypy hooks/ tests/
	@echo "Running Bandit security checks..."
	bandit -r hooks/ -ll
	@echo "Running Safety checks..."
	safety check
	@echo "All checks passed!"

docs: ## Build documentation
	mkdocs build

docs-serve: ## Serve documentation locally
	mkdocs serve

bake-test: ## Test baking a project with different configurations
	@echo "Testing minimal configuration..."
	cookiecutter . --no-input --output-dir=test-bake project_name="Test Minimal" project_slug="test_minimal" use_ruff=n use_mypy=n
	@echo "Testing full configuration..."
	cookiecutter . --no-input --output-dir=test-bake project_name="Test Full" project_slug="test_full" use_ruff=y use_mypy=y use_github_actions=y
	@echo "Cleaning up test projects..."
	rm -rf test-bake/

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

validate: ## Validate template structure and configuration
	python -c "import json; json.load(open('cookiecutter.json'))" && echo "cookiecutter.json is valid"
	python -m py_compile hooks/post_gen_project.py && echo "hooks are syntactically valid"

release-check: ## Check if ready for release
	@echo "Checking release readiness..."
	@echo "1. Running all tests..."
	$(MAKE) test-all
	@echo "2. Running quality checks..."
	$(MAKE) check
	@echo "3. Validating template..."
	$(MAKE) validate
	@echo "4. Testing project generation..."
	$(MAKE) bake-test
	@echo "✅ Ready for release!"

ci: ## Run CI pipeline locally
	$(MAKE) install-dev
	$(MAKE) check
	$(MAKE) test-all
	$(MAKE) bake-test
