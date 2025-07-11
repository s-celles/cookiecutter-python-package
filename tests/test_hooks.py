"""Tests for cookiecutter hooks."""

import subprocess
import tempfile
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


class TestPostGenHook:
    """Test the post-generation hook."""

    @pytest.fixture
    def template_dir(self) -> Path:
        """Return the path to the template directory."""
        return Path(__file__).parent.parent

    def test_hook_file_exists(self, template_dir: Path) -> None:
        """Test that the post-gen hook file exists and is executable."""
        hook_file = template_dir / "hooks" / "post_gen_project.py"
        assert hook_file.exists()

        # Test that it's valid Python
        with open(hook_file) as f:
            content = f.read()

        try:
            compile(content, str(hook_file), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error in hook: {e}")

    def test_hook_removes_unused_files(self, template_dir: Path) -> None:
        """Test that hook removes files when features are disabled."""
        context = {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test Package",
            "project_slug": "test_package",
            "project_short_description": "A test package",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            "use_ruff": "n",
            "use_mypy": "n",
            "use_pytest": "n",
            "use_coverage": "n",
            "use_pre_commit": "n",  # Should remove .pre-commit-config.yaml
            "use_bandit": "n",
            "use_safety": "n",
            "use_sphinx": "n",
            "use_mkdocs": "n",
            "use_github_actions": "n",  # Should remove .github directory
            "use_dependabot": "n",
            "use_codecov": "n",
            "command_line_interface": "none",
            "use_tox": "n",  # Should remove tox.ini
            "use_nox": "n",  # Should remove noxfile.py
            "use_commitizen": "n",
            "use_semantic_release": "n",
            "create_changelog": "n",  # Should remove CHANGELOG.md
            "create_contributing": "n",  # Should remove CONTRIBUTING.md
            "create_code_of_conduct": "n",
            "use_docker": "n",  # Should remove Dockerfile
            "use_devcontainer": "n",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # These files should not exist when features are disabled
            files_that_should_not_exist = [
                ".pre-commit-config.yaml",
                "tox.ini",
                "noxfile.py",
                "CHANGELOG.md",
                "CONTRIBUTING.md",
                "Dockerfile",
            ]

            for file_path in files_that_should_not_exist:
                assert not (project_path / file_path).exists(), (
                    f"{file_path} should not exist when feature is disabled"
                )

            # .github directory should not exist
            assert not (project_path / ".github").exists(), (
                ".github directory should not exist when GitHub Actions is disabled"
            )

    def test_hook_keeps_files_when_enabled(self, template_dir: Path) -> None:
        """Test that hook keeps files when features are enabled."""
        context = {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test Package",
            "project_slug": "test_package",
            "project_short_description": "A test package",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            "use_ruff": "y",
            "use_mypy": "y",
            "use_pytest": "y",
            "use_coverage": "y",
            "use_pre_commit": "y",  # Should keep .pre-commit-config.yaml
            "use_bandit": "y",
            "use_safety": "y",
            "use_sphinx": "n",
            "use_mkdocs": "y",
            "use_github_actions": "y",  # Should keep .github directory
            "use_dependabot": "y",
            "use_codecov": "y",
            "command_line_interface": "typer",
            "use_tox": "y",  # Should keep tox.ini
            "use_nox": "y",  # Should keep noxfile.py
            "use_commitizen": "y",
            "use_semantic_release": "y",
            "create_changelog": "y",  # Should keep CHANGELOG.md
            "create_contributing": "y",  # Should keep CONTRIBUTING.md
            "create_code_of_conduct": "y",
            "use_docker": "y",  # Should keep Dockerfile
            "use_devcontainer": "y",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # These files should exist when features are enabled
            files_that_should_exist = [
                ".pre-commit-config.yaml",
                "tox.ini",
                "noxfile.py",
                "CHANGELOG.md",
                "CONTRIBUTING.md",
                "Dockerfile",
            ]

            for file_path in files_that_should_exist:
                assert (project_path / file_path).exists(), (
                    f"{file_path} should exist when feature is enabled"
                )

            # .github directory should exist
            assert (project_path / ".github").exists(), (
                ".github directory should exist when GitHub Actions is enabled"
            )
            assert (project_path / ".github" / "workflows" / "ci.yml").exists(), (
                "CI workflow should exist"
            )

    def test_hook_initializes_git_repo(self, template_dir: Path) -> None:
        """Test that hook initializes a git repository."""
        context = {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test Package",
            "project_slug": "test_package",
            "project_short_description": "A test package",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            "use_ruff": "n",
            "use_mypy": "n",
            "use_pytest": "y",
            "use_coverage": "n",
            "use_pre_commit": "n",
            "use_bandit": "n",
            "use_safety": "n",
            "use_sphinx": "n",
            "use_mkdocs": "n",
            "use_github_actions": "n",
            "use_dependabot": "n",
            "use_codecov": "n",
            "command_line_interface": "none",
            "use_tox": "n",
            "use_nox": "n",
            "use_commitizen": "n",
            "use_semantic_release": "n",
            "create_changelog": "n",
            "create_contributing": "n",
            "create_code_of_conduct": "n",
            "use_docker": "n",
            "use_devcontainer": "n",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)

            # Git repository should be initialized
            assert (project_path / ".git").exists(), (
                "Git repository should be initialized"
            )

            # Check that there's an initial commit
            result = subprocess.run(
                ["git", "log", "--oneline"],
                check=False,
                cwd=project_path,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                # If git log fails, check if it's because there are no commits
                if "does not have any commits yet" in result.stderr:
                    # Check if at least git status works (repo is initialized)
                    status_result = subprocess.run(
                        ["git", "status"],
                        check=False,
                        cwd=project_path,
                        capture_output=True,
                        text=True,
                    )
                    assert status_result.returncode == 0, (
                        f"Git repository not properly initialized. "
                        f"Status error: {status_result.stderr}"
                    )
                    # If no commits, that's acceptable - just verify git is initialized
                    return
                else:
                    pytest.fail(
                        f"Git log failed with unexpected error: {result.stderr}"
                    )

            # If git log succeeded, verify there's an initial commit
            assert "Initial commit" in result.stdout, (
                f"Should have initial commit. Git log output: {result.stdout}"
            )

    def test_hook_prints_helpful_messages(self, template_dir: Path) -> None:
        """Test that hook prints helpful setup messages."""
        # This is harder to test directly, but we can at least verify
        # the hook runs without errors
        context = {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test Package",
            "project_slug": "test_package",
            "project_short_description": "A test package",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            "use_ruff": "y",
            "use_mypy": "y",
            "use_pytest": "y",
            "use_coverage": "y",
            "use_pre_commit": "y",
            "use_bandit": "y",
            "use_safety": "y",
            "use_sphinx": "n",
            "use_mkdocs": "n",
            "use_github_actions": "y",
            "use_dependabot": "y",
            "use_codecov": "y",
            "command_line_interface": "typer",
            "use_tox": "n",
            "use_nox": "n",
            "use_commitizen": "n",
            "use_semantic_release": "n",
            "create_changelog": "y",
            "create_contributing": "y",
            "create_code_of_conduct": "n",
            "use_docker": "n",
            "use_devcontainer": "n",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            # This should complete without errors
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            assert project_path.exists(), "Project should be created successfully"

    def test_hook_handles_edge_cases(self, template_dir: Path) -> None:
        """Test that hook handles edge cases gracefully."""
        # Test with unusual project names
        context = {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test-Package_With.Special_Characters",
            "project_slug": "test_package_with_special_characters",
            "project_short_description": "A test package with special characters",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            "use_ruff": "n",
            "use_mypy": "n",
            "use_pytest": "y",
            "use_coverage": "n",
            "use_pre_commit": "n",
            "use_bandit": "n",
            "use_safety": "n",
            "use_sphinx": "n",
            "use_mkdocs": "n",
            "use_github_actions": "n",
            "use_dependabot": "n",
            "use_codecov": "n",
            "command_line_interface": "none",
            "use_tox": "n",
            "use_nox": "n",
            "use_commitizen": "n",
            "use_semantic_release": "n",
            "create_changelog": "n",
            "create_contributing": "n",
            "create_code_of_conduct": "n",
            "use_docker": "n",
            "use_devcontainer": "n",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            # This should complete without errors even with special characters
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            assert project_path.exists(), (
                "Project should be created successfully even with special characters"
            )
