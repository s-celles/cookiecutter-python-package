#!/usr/bin/env python3
"""Post-generation hook for cookiecutter-python-package."""

import os
import shutil
from pathlib import Path

# Get the project directory
PROJECT_DIRECTORY = Path.cwd()


def remove_file(filepath: Path) -> None:
    """Remove a file if it exists."""
    if filepath.exists():
        filepath.unlink()


def remove_dir(dirpath: Path) -> None:
    """Remove a directory if it exists."""
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)


def main():
    """Main post-generation cleanup."""
    try:
        # Remove files based on configuration
        if "{{ cookiecutter.use_pre_commit }}" != "y":
            remove_file(PROJECT_DIRECTORY / ".pre-commit-config.yaml")

        if "{{ cookiecutter.use_github_actions }}" != "y":
            remove_dir(PROJECT_DIRECTORY / ".github")

        if "{{ cookiecutter.use_tox }}" != "y":
            remove_file(PROJECT_DIRECTORY / "tox.ini")

        if "{{ cookiecutter.use_nox }}" != "y":
            remove_file(PROJECT_DIRECTORY / "noxfile.py")

        if "{{ cookiecutter.use_docker }}" != "y":
            remove_file(PROJECT_DIRECTORY / "Dockerfile")
            remove_file(PROJECT_DIRECTORY / "docker-compose.yml")

        if "{{ cookiecutter.create_changelog }}" != "y":
            remove_file(PROJECT_DIRECTORY / "CHANGELOG.md")

        if "{{ cookiecutter.create_contributing }}" != "y":
            remove_file(PROJECT_DIRECTORY / "CONTRIBUTING.md")

        if "{{ cookiecutter.create_code_of_conduct }}" != "y":
            remove_file(PROJECT_DIRECTORY / "CODE_OF_CONDUCT.md")

        if "{{ cookiecutter.command_line_interface }}" == "none":
            # Remove CLI-related test file if no CLI is wanted
            cli_test_file = PROJECT_DIRECTORY / "tests" / "test_cli.py"
            if cli_test_file.exists():
                remove_file(cli_test_file)

        # Create initial git repository
        os.system("git init")
        os.system("git add .")
        os.system('git commit -m "Initial commit from cookiecutter-python-package"')

        print(
            "\n*** Project '{ cookiecutter.project_name }' has been created successfully! ***"
        )
        print(f"Location: {PROJECT_DIRECTORY}")
        print("\nNext steps:")
        print("1. cd {{ cookiecutter.project_slug }}")
        print("2. Create and activate a virtual environment")
        print('3. pip install -e ".[dev]"')

        if "{{ cookiecutter.use_pre_commit }}" == "y":
            print("4. pre-commit install")

        print("\nHappy coding!")

        # Print tool explanations
        print("\nIncluded Tools and Their Importance:")

        if "{{ cookiecutter.use_ruff }}" == "y":
            print(
                "* Ruff: Ultra-fast Python linter and formatter that replaces multiple tools (flake8, black, isort)"
            )

        if "{{ cookiecutter.use_mypy }}" == "y":
            print(
                "* MyPy: Static type checker that helps catch bugs early and improves code documentation"
            )

        if "{{ cookiecutter.use_pytest }}" == "y":
            print(
                "* pytest: Modern testing framework with powerful features and fixtures"
            )

        if "{{ cookiecutter.use_coverage }}" == "y":
            print(
                "* Coverage: Measures test coverage to ensure your tests are comprehensive"
            )

        if "{{ cookiecutter.use_pre_commit }}" == "y":
            print(
                "* pre-commit: Runs checks before commits to maintain code quality automatically"
            )

        if "{{ cookiecutter.use_bandit }}" == "y":
            print(
                "* Bandit: Security linter that finds common security issues in Python code"
            )

        if "{{ cookiecutter.use_safety }}" == "y":
            print("* Safety: Checks dependencies for known security vulnerabilities")

        if "{{ cookiecutter.use_github_actions }}" == "y":
            print(
                "* GitHub Actions: Automated CI/CD pipelines for testing and deployment"
            )

        if "{{ cookiecutter.use_dependabot }}" == "y":
            print(
                "* Dependabot: Automated dependency updates to keep your project secure"
            )

    except Exception as e:
        print(f"Error during project setup: {e}")
        print("The project was created, but some cleanup steps may have failed.")


if __name__ == "__main__":
    main()
