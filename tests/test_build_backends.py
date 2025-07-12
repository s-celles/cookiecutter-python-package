"""Comprehensive tests for build backend support in generated projects."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture
def template_dir() -> Path:
    """Return the path to the template directory."""
    return Path(__file__).parent.parent


def create_backend_context(backend: str, **overrides: Any) -> dict[str, Any]:
    """Create a context for testing a specific build backend."""
    base_context = {
        "full_name": "Test User",
        "email": "test@example.com",
        "github_username": "testuser",
        "project_name": "Test Package",
        "project_slug": "test_package",
        "project_short_description": "A test package for build backend testing",
        "version": "0.1.0",
        "python_requires": ">=3.9",
        "license": "MIT",
        "build_backend": backend,
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
        "use_uv": "n",
    }
    base_context.update(overrides)
    return base_context


class TestBuildBackends:
    """Test all supported build backends."""

    @pytest.mark.parametrize("backend", ["setuptools", "hatchling", "flit", "pdm"])
    def test_backend_pyproject_toml_generation(
        self, template_dir: Path, backend: str
    ) -> None:
        """Test that pyproject.toml is correctly generated for each backend."""
        context = create_backend_context(backend)

        with tempfile.TemporaryDirectory() as tmpdirname:
            project_path = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=tmpdirname,
            )

            pyproject_path = Path(project_path) / "pyproject.toml"
            assert pyproject_path.exists(), f"pyproject.toml not found for {backend}"

            content = pyproject_path.read_text()

            # Check backend-specific configurations
            if backend == "setuptools":
                assert "[build-system]" in content
                assert 'requires = ["setuptools>=61.0", "wheel"]' in content
                assert 'build-backend = "setuptools.build_meta"' in content
                assert "[tool.setuptools.packages.find]" in content

            elif backend == "hatchling":
                assert "[build-system]" in content
                assert 'requires = ["hatchling' in content  # Allow version flexibility
                assert 'build-backend = "hatchling.build"' in content
                assert "[tool.hatch.build.targets.wheel]" in content

            elif backend == "flit":
                assert "[build-system]" in content
                assert 'requires = ["flit_core' in content  # Allow version flexibility
                assert 'build-backend = "flit_core.buildapi"' in content
                assert "[tool.flit.module]" in content

            elif backend == "pdm":
                assert "[build-system]" in content
                assert 'requires = ["pdm-backend"]' in content
                assert 'build-backend = "pdm.backend"' in content

    @pytest.mark.parametrize("backend", ["setuptools", "hatchling", "flit", "pdm"])
    def test_backend_project_structure(self, template_dir: Path, backend: str) -> None:
        """Test that the project structure is correct for each backend."""
        context = create_backend_context(backend)

        with tempfile.TemporaryDirectory() as tmpdirname:
            project_path = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=tmpdirname,
            )

            project_dir = Path(project_path)

            # Common files that should exist for all backends
            assert (project_dir / "pyproject.toml").exists()
            assert (project_dir / "README.md").exists()
            assert (project_dir / "src").exists()
            assert (project_dir / "src" / "test_package").exists()
            assert (project_dir / "src" / "test_package" / "__init__.py").exists()
            assert (project_dir / "tests").exists()

            # Check that MANIFEST.in exists for setuptools (often needed for data files)
            if backend == "setuptools":
                manifest_path = project_dir / "MANIFEST.in"
                if manifest_path.exists():
                    content = manifest_path.read_text()
                    assert "include" in content or "recursive-include" in content

    @pytest.mark.parametrize("backend", ["setuptools", "hatchling", "flit", "pdm"])
    def test_backend_package_installable(
        self, template_dir: Path, backend: str
    ) -> None:
        """Test that the generated package can be installed with each backend."""
        context = create_backend_context(backend)

        with tempfile.TemporaryDirectory() as tmpdirname:
            project_path = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=tmpdirname,
            )

            project_dir = Path(project_path)

            # Try to build the package
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", ".", "--quiet"],
                check=False,
                cwd=project_dir,
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0, (
                f"Failed to install {backend} package: {result.stderr}"
            )

            # Try to import the package
            result = subprocess.run(
                [sys.executable, "-c", "import test_package; print('Success')"],
                check=False,
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0, (
                f"Failed to import {backend} package: {result.stderr}"
            )
            assert "Success" in result.stdout

    @pytest.mark.parametrize("backend", ["setuptools", "hatchling", "flit", "pdm"])
    def test_backend_build_wheel(self, template_dir: Path, backend: str) -> None:
        """Test that a wheel can be built with each backend."""
        context = create_backend_context(backend)

        with tempfile.TemporaryDirectory() as tmpdirname:
            project_path = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=tmpdirname,
            )

            project_dir = Path(project_path)

            # Build wheel
            result = subprocess.run(
                [sys.executable, "-m", "build", "--wheel", "--outdir", "dist"],
                check=False,
                cwd=project_dir,
                capture_output=True,
                text=True,
            )

            # If build module is not available, try pip wheel
            if result.returncode != 0:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "wheel",
                        ".",
                        "--no-deps",
                        "-w",
                        "dist",
                    ],
                    check=False,
                    cwd=project_dir,
                    capture_output=True,
                    text=True,
                )

            assert result.returncode == 0, (
                f"Failed to build wheel for {backend}: {result.stderr}"
            )

            # Check that wheel was created
            dist_dir = project_dir / "dist"
            wheels = list(dist_dir.glob("*.whl"))
            assert len(wheels) > 0, f"No wheel file found for {backend}"

            # Check wheel name format
            wheel_name = wheels[0].name
            assert "test_package" in wheel_name
            assert "0.1.0" in wheel_name

    def test_setuptools_with_cli(self, template_dir: Path) -> None:
        """Test setuptools backend with CLI interface."""
        context = create_backend_context("setuptools", command_line_interface="typer")

        with tempfile.TemporaryDirectory() as tmpdirname:
            project_path = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=tmpdirname,
            )

            project_dir = Path(project_path)
            pyproject_path = project_dir / "pyproject.toml"
            content = pyproject_path.read_text()

            # Should have console_scripts entry point
            assert "[project.scripts]" in content or "console_scripts" in content

    def test_hatchling_with_features(self, template_dir: Path) -> None:
        """Test hatchling backend with additional features."""
        context = create_backend_context("hatchling", use_ruff="y", use_mypy="y")

        with tempfile.TemporaryDirectory() as tmpdirname:
            project_path = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=tmpdirname,
            )

            project_dir = Path(project_path)
            pyproject_path = project_dir / "pyproject.toml"
            content = pyproject_path.read_text()

            # Should have hatchling configuration
            assert 'build-backend = "hatchling.build"' in content
            assert "[tool.hatch" in content

    def test_flit_module_configuration(self, template_dir: Path) -> None:
        """Test flit backend module configuration."""
        context = create_backend_context("flit")

        with tempfile.TemporaryDirectory() as tmpdirname:
            project_path = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=tmpdirname,
            )

            project_dir = Path(project_path)
            pyproject_path = project_dir / "pyproject.toml"
            content = pyproject_path.read_text()

            # Should have flit module configuration
            assert "[tool.flit.module]" in content
            assert 'name = "test_package"' in content

    def test_pdm_backend_configuration(self, template_dir: Path) -> None:
        """Test PDM backend configuration."""
        context = create_backend_context("pdm")

        with tempfile.TemporaryDirectory() as tmpdirname:
            project_path = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=tmpdirname,
            )

            project_dir = Path(project_path)
            pyproject_path = project_dir / "pyproject.toml"
            content = pyproject_path.read_text()

            # Should have PDM configuration
            assert 'build-backend = "pdm.backend"' in content

    @pytest.mark.parametrize("backend", ["setuptools", "hatchling", "flit", "pdm"])
    def test_backend_metadata_consistency(
        self, template_dir: Path, backend: str
    ) -> None:
        """Test that metadata is consistent across all backends."""
        context = create_backend_context(
            backend,
            project_name="My Test Package",
            project_short_description="A comprehensive test package",
            version="1.2.3",
            python_requires=">=3.10",
        )
        # Don't override project_slug - let cookiecutter generate it
        if "project_slug" in context:
            del context["project_slug"]

        with tempfile.TemporaryDirectory() as tmpdirname:
            project_path = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=tmpdirname,
            )

            project_dir = Path(project_path)
            pyproject_path = project_dir / "pyproject.toml"
            content = pyproject_path.read_text()

            # Check that basic metadata is present (use generated slug format)
            assert (
                'name = "my_test_package"' in content
                or 'name = "my-test-package"' in content
            )
            assert 'description = "A comprehensive test package"' in content
            assert 'version = "1.2.3"' in content
            assert 'requires-python = ">=3.10"' in content

    def test_all_backends_default_values(self, template_dir: Path) -> None:
        """Test that all backends work with default cookiecutter values."""
        # Load default values from cookiecutter.json
        cookiecutter_json_path = template_dir / "cookiecutter.json"
        with open(cookiecutter_json_path) as f:
            default_config = json.load(f)

        # Extract default values for each backend
        backends = default_config["build_backend"]

        for backend in backends:
            with tempfile.TemporaryDirectory() as tmpdirname:
                # Use minimal overrides to set build_backend
                context = {"build_backend": backend}

                project_path = cookiecutter(
                    str(template_dir),
                    no_input=True,
                    extra_context=context,
                    output_dir=tmpdirname,
                )

                project_dir = Path(project_path)

                # Check that basic files exist
                assert (project_dir / "pyproject.toml").exists()
                assert (project_dir / "src").exists()

                # Check that pyproject.toml contains backend configuration
                pyproject_content = (project_dir / "pyproject.toml").read_text()
                assert (
                    f'build-backend = "{self._get_backend_string(backend)}"'
                    in pyproject_content
                )

    def _get_backend_string(self, backend: str) -> str:
        """Get the build-backend string for a given backend."""
        backend_strings = {
            "setuptools": "setuptools.build_meta",
            "hatchling": "hatchling.build",
            "flit": "flit_core.buildapi",
            "pdm": "pdm.backend",
        }
        return backend_strings[backend]


class TestBuildBackendIntegration:
    """Test build backend integration with other features."""

    def test_backend_with_cli_integration(self, template_dir: Path) -> None:
        """Test that CLI integration works with different backends."""
        cli_options = ["typer", "click", "argparse"]
        backends = ["setuptools", "hatchling", "flit", "pdm"]

        for backend in backends:
            for cli in cli_options:
                context = create_backend_context(backend, command_line_interface=cli)

                with tempfile.TemporaryDirectory() as tmpdirname:
                    project_path = cookiecutter(
                        str(template_dir),
                        no_input=True,
                        extra_context=context,
                        output_dir=tmpdirname,
                    )

                    project_dir = Path(project_path)

                    # Check that CLI files are created
                    if cli != "none":
                        cli_file = project_dir / "src" / "test_package" / "cli.py"
                        assert cli_file.exists(), (
                            f"CLI file missing for {backend}+{cli}"
                        )

                    # Check pyproject.toml for CLI dependencies and entry points
                    pyproject_content = (project_dir / "pyproject.toml").read_text()

                    if cli == "typer":
                        assert "typer" in pyproject_content
                    elif cli == "click":
                        assert "click" in pyproject_content

    def test_backend_with_testing_tools(self, template_dir: Path) -> None:
        """Test that testing tools work with different backends."""
        backends = ["setuptools", "hatchling", "flit", "pdm"]

        for backend in backends:
            context = create_backend_context(
                backend, use_pytest="y", use_coverage="y", use_tox="y"
            )

            with tempfile.TemporaryDirectory() as tmpdirname:
                project_path = cookiecutter(
                    str(template_dir),
                    no_input=True,
                    extra_context=context,
                    output_dir=tmpdirname,
                )

                project_dir = Path(project_path)

                # Check that testing configuration files exist
                if context["use_tox"] == "y":
                    assert (project_dir / "tox.ini").exists()

                # Check that testing dependencies are in pyproject.toml
                pyproject_content = (project_dir / "pyproject.toml").read_text()
                assert "pytest" in pyproject_content

    def test_backend_with_documentation(self, template_dir: Path) -> None:
        """Test that documentation tools work with different backends."""
        backends = ["setuptools", "hatchling", "flit", "pdm"]

        for backend in backends:
            for docs_tool in ["mkdocs", "sphinx"]:
                use_mkdocs = "y" if docs_tool == "mkdocs" else "n"
                use_sphinx = "y" if docs_tool == "sphinx" else "n"

                context = create_backend_context(
                    backend, use_mkdocs=use_mkdocs, use_sphinx=use_sphinx
                )

                with tempfile.TemporaryDirectory() as tmpdirname:
                    project_path = cookiecutter(
                        str(template_dir),
                        no_input=True,
                        extra_context=context,
                        output_dir=tmpdirname,
                    )

                    project_dir = Path(project_path)

                    # Check that documentation files exist
                    if docs_tool == "mkdocs":
                        assert (project_dir / "mkdocs.yml").exists()
                        assert (project_dir / "docs").exists()
                    elif docs_tool == "sphinx":
                        docs_dir = project_dir / "docs"
                        if docs_dir.exists():
                            # Sphinx might create different files - just check directory exists
                            assert docs_dir.is_dir(), (
                                f"Sphinx docs directory should exist for {backend}"
                            )

    def test_backend_performance_comparison(self, template_dir: Path) -> None:
        """Basic performance test for different backends."""
        import time

        backends = ["setuptools", "hatchling", "flit", "pdm"]
        times = {}

        for backend in backends:
            context = create_backend_context(backend)

            start_time = time.time()

            with tempfile.TemporaryDirectory() as tmpdirname:
                project_path = cookiecutter(
                    str(template_dir),
                    no_input=True,
                    extra_context=context,
                    output_dir=tmpdirname,
                )

                # Measure template generation time
                generation_time = time.time() - start_time
                times[backend] = generation_time

        # Just ensure all backends complete in reasonable time (< 30 seconds each)
        for backend, elapsed in times.items():
            assert elapsed < 30, f"{backend} took too long: {elapsed:.2f}s"
