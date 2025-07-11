"""Performance and stress tests for the cookiecutter template."""

import concurrent.futures
import tempfile
import time
from pathlib import Path
from typing import Any

import pytest
from cookiecutter.main import cookiecutter


class TestPerformance:
    """Test template generation performance."""

    @pytest.fixture
    def template_dir(self) -> Path:
        """Return the path to the template directory."""
        return Path(__file__).parent.parent

    @pytest.fixture
    def minimal_context(self) -> dict[str, Any]:
        """Minimal context for performance testing."""
        return {
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

    @pytest.mark.slow
    def test_generation_speed(
        self, template_dir: Path, minimal_context: dict[str, Any]
    ) -> None:
        """Test that template generation completes in reasonable time."""
        with tempfile.TemporaryDirectory() as temp_dir:
            start_time = time.time()

            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=minimal_context,
                output_dir=temp_dir,
            )

            end_time = time.time()
            generation_time = end_time - start_time

            # Template generation should complete in under 5 seconds
            assert (
                generation_time < 5.0
            ), f"Template generation took {generation_time:.2f}s, expected < 5s"

            # Verify the project was created
            project_path = Path(result)
            assert project_path.exists()

    @pytest.mark.slow
    def test_concurrent_generation(
        self, template_dir: Path, minimal_context: dict[str, Any]
    ) -> None:
        """Test that multiple templates can be generated concurrently."""
        import platform

        # Skip test on Windows due to filesystem concurrency issues
        if platform.system() == "Windows":
            pytest.skip(
                "Concurrent generation test skipped on Windows due to filesystem limitations"
            )

        def generate_project(project_id: int) -> str:
            context = minimal_context.copy()
            # Use timestamp and process ID to ensure uniqueness
            import os
            import threading

            unique_id = f"{project_id}_{int(time.time() * 1000000)}_{os.getpid()}_{threading.get_ident()}"
            context["project_slug"] = f"test_package_{unique_id}"

            # Each thread gets its own temp directory
            with tempfile.TemporaryDirectory(
                prefix=f"cookiecutter_test_{unique_id}_"
            ) as temp_dir:
                result = cookiecutter(
                    str(template_dir),
                    no_input=True,
                    extra_context=context,
                    output_dir=temp_dir,
                )
                return str(result)

        # Generate 3 projects concurrently
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(generate_project, i) for i in range(3)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        end_time = time.time()
        total_time = end_time - start_time

        # Should complete all 3 in under 10 seconds
        assert (
            total_time < 10.0
        ), f"Concurrent generation took {total_time:.2f}s, expected < 10s"

        # All projects should be generated
        assert len(results) == 3
        for result in results:
            assert Path(result).exists()

    @pytest.mark.slow
    def test_large_project_generation(self, template_dir: Path) -> None:
        """Test generation with all features enabled (largest possible project)."""
        full_context = {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test Package Large",
            "project_slug": "test_package_large",
            "project_short_description": "A large test package with all features",
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
            "use_mkdocs": "y",
            "use_github_actions": "y",
            "use_dependabot": "y",
            "use_codecov": "y",
            "command_line_interface": "typer",
            "use_tox": "y",
            "use_nox": "y",
            "use_commitizen": "y",
            "use_semantic_release": "y",
            "create_changelog": "y",
            "create_contributing": "y",
            "create_code_of_conduct": "y",
            "use_docker": "y",
            "use_devcontainer": "y",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            start_time = time.time()

            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=full_context,
                output_dir=temp_dir,
            )

            end_time = time.time()
            generation_time = end_time - start_time

            # Even large projects should generate quickly
            assert (
                generation_time < 10.0
            ), f"Large project generation took {generation_time:.2f}s, expected < 10s"

            project_path = Path(result)
            assert project_path.exists()

            # Count generated files
            all_files = list(project_path.rglob("*"))
            file_count = len([f for f in all_files if f.is_file()])

            # Should generate a substantial number of files
            assert file_count > 20, f"Expected > 20 files, got {file_count}"


class TestStress:
    """Stress tests for edge cases and unusual inputs."""

    @pytest.fixture
    def template_dir(self) -> Path:
        """Return the path to the template directory."""
        return Path(__file__).parent.parent

    @pytest.mark.parametrize(
        "special_chars",
        [
            "test-package-with-hyphens",
            "test_package_with_underscores",
            "test.package.with.dots",
            "testpackagewithverylongname" * 2,  # Very long name
        ],
    )
    def test_special_project_names(
        self, template_dir: Path, special_chars: str
    ) -> None:
        """Test template generation with special characters in project names."""
        context = {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": f"Test Package {special_chars}",
            "project_slug": special_chars.replace("-", "_").replace(".", "_"),
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
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            assert project_path.exists()

            # Check that Python package directory was created correctly
            package_dir = project_path / "src" / context["project_slug"]
            assert package_dir.exists()

    @pytest.mark.parametrize(
        "unicode_chars",
        [
            "José García",
            "Åse Østerberg",
            "李小明",
            "محمد أحمد",
        ],
    )
    def test_unicode_author_names(self, template_dir: Path, unicode_chars: str) -> None:
        """Test template generation with Unicode characters in author names."""
        context = {
            "full_name": unicode_chars,
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test Package Unicode",
            "project_slug": "test_package_unicode",
            "project_short_description": "A test package with Unicode author",
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
            assert project_path.exists()

            # Check that author name appears correctly in generated files
            pyproject_file = project_path / "pyproject.toml"
            content = pyproject_file.read_text(encoding="utf-8")
            assert unicode_chars in content

    def test_boundary_values(self, template_dir: Path) -> None:
        """Test template with boundary values."""
        context = {
            "full_name": "",  # Empty name
            "email": "a@b.co",  # Minimal valid email
            "github_username": "a",  # Minimal username
            "project_name": "A",  # Minimal project name
            "project_slug": "a",  # Minimal slug
            "project_short_description": "",  # Empty description
            "version": "0.0.1",  # Minimal version
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
            assert project_path.exists()

            # Even with minimal values, basic structure should exist
            assert (project_path / "pyproject.toml").exists()
            assert (project_path / "src" / "a" / "__init__.py").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
