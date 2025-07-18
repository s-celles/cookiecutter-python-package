"""Tests for template documentation and examples."""

import re
import tempfile
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


class TestDocumentation:
    """Test template documentation quality and completeness."""

    @pytest.fixture
    def template_dir(self) -> Path:
        """Return the path to the template directory."""
        return Path(__file__).parent.parent

    def test_readme_structure(self, template_dir: Path) -> None:
        """Test that template README has proper structure."""
        readme_file = template_dir / "README.md"
        assert readme_file.exists(), "Template should have README.md"

        content = readme_file.read_text(encoding="utf-8")

        # Check for required sections in streamlined README
        required_sections = [
            "# ",  # Main title
            "Quick Start",  # Quick start section
            "What You Get",  # Features overview (renamed from "Features")
            "Documentation",  # Documentation section pointing to docs site
            "Contributing",  # Contributing section
            "License",  # License section
        ]

        for section in required_sections:
            assert section in content, f"README should contain {section} section"

        # Check that README points to documentation site for detailed information
        assert "s-celles.github.io/cookiecutter-python-package" in content, (
            "README should link to documentation site"
        )

        # Check that README mentions key features briefly
        key_features = [
            "Modern packaging",
            "Build backend",
            "Testing",
            "Code quality",
        ]

        for feature in key_features:
            assert feature in content, f"README should mention {feature}"

    def test_documentation_contains_detailed_info(self, template_dir: Path) -> None:
        """Test that documentation contains detailed information moved from README."""
        docs_dir = template_dir / "docs"

        # Check that index.md contains template options overview
        index_file = docs_dir / "index.md"
        if index_file.exists():
            content = index_file.read_text(encoding="utf-8")

            # Should contain template options overview that was in README
            assert "Template Options" in content, (
                "Documentation index should contain template options overview"
            )
            assert "Build Backend" in content, (
                "Documentation should mention build backends"
            )
            assert "Code Quality" in content, (
                "Documentation should mention code quality tools"
            )

        # Check that quick-start.md contains usage instructions
        quick_start_file = docs_dir / "getting-started" / "quick-start.md"
        if quick_start_file.exists():
            content = quick_start_file.read_text(encoding="utf-8")

            # Should contain detailed usage instructions that were in README
            assert (
                "Set Up Development Environment" in content
                or "development environment" in content
            ), "Quick start should contain development setup instructions"
            assert "pip install" in content, (
                "Quick start should contain installation instructions"
            )

        # Check that configuration guide exists and contains template options
        config_file = docs_dir / "configuration" / "template-options.md"
        if config_file.exists():
            content = config_file.read_text(encoding="utf-8")

            # Should contain detailed template options
            assert "build_backend" in content, (
                "Configuration should document build_backend option"
            )
            assert "setuptools" in content, (
                "Configuration should mention setuptools backend"
            )
            assert "hatchling" in content, (
                "Configuration should mention hatchling backend"
            )

    def test_tools_documentation_structure(self, template_dir: Path) -> None:
        """Test that tools documentation structure exists in docs/ folder."""
        docs_tools_dir = template_dir / "docs" / "tools"
        assert docs_tools_dir.exists(), "Should have docs/tools/ directory"

        # Dynamically discover documentation files
        actual_docs = [f.name for f in docs_tools_dir.glob("*.md")]

        # Ensure we have a reasonable number of documentation files
        assert len(actual_docs) >= 5, (
            f"Should have at least 5 tool docs, found: {actual_docs}"
        )

        # Check for critical documentation files that must exist
        critical_docs = [
            "overview.md",  # Required: Tools overview
            "build-backends.md",  # Required: Our new build backends guide
        ]

        for doc_file in critical_docs:
            file_path = docs_tools_dir / doc_file
            assert file_path.exists(), (
                f"Critical documentation missing: docs/tools/{doc_file}"
            )

        # Check that security.md mentions major security tools (if it exists)
        security_doc = docs_tools_dir / "security.md"
        if security_doc.exists():
            content = security_doc.read_text(encoding="utf-8")
            security_tools = ["bandit", "safety"]
            for tool in security_tools:
                assert tool.lower() in content.lower(), (
                    f"Security doc should mention {tool}"
                )

            # Check for sections explaining importance in security doc
            assert "Why important" in content or "important" in content.lower(), (
                "Security doc should explain why tools are important"
            )
            assert "best practice" in content.lower(), (
                "Security doc should mention best practices"
            )

        # Check that overview.md exists and has good content
        overview_doc = docs_tools_dir / "overview.md"
        if overview_doc.exists():
            content = overview_doc.read_text(encoding="utf-8")
            assert "tool" in content.lower(), "Overview should mention tools"

    def test_template_summary_accuracy(self, template_dir: Path) -> None:
        """Test that TEMPLATE_SUMMARY.md accurately reflects template."""
        if not (template_dir / "TEMPLATE_SUMMARY.md").exists():
            pytest.skip("TEMPLATE_SUMMARY.md not found")

        summary_file = template_dir / "TEMPLATE_SUMMARY.md"
        content = summary_file.read_text(encoding="utf-8")

        # Should mention key features
        key_features = ["pyproject.toml", "src layout", "pytest", "CI/CD"]

        for feature in key_features:
            assert feature in content, f"Summary should mention {feature}"

    def test_cookiecutter_json_documentation(self, template_dir: Path) -> None:
        """Test that cookiecutter.json options are well-documented."""
        import json

        cookiecutter_json = template_dir / "cookiecutter.json"

        with open(cookiecutter_json) as f:
            config = json.load(f)

        # Check that boolean options have reasonable defaults
        boolean_options = [
            "use_ruff",
            "use_mypy",
            "use_pytest",
            "use_coverage",
            "use_pre_commit",
            "use_bandit",
            "use_safety",
        ]

        for option in boolean_options:
            if option in config:
                # Options can be either string or list format
                if isinstance(config[option], list):
                    assert "y" in config[option] and "n" in config[option], (
                        f"{option} should have 'y' and 'n' options"
                    )
                else:
                    assert config[option] in [
                        "y",
                        "n",
                    ], f"{option} should be 'y' or 'n'"

    def test_generated_project_documentation(self, template_dir: Path) -> None:
        """Test that generated projects have good documentation."""
        context = {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": "Test Package Docs",
            "project_slug": "test_package_docs",
            "project_short_description": "A test package for documentation testing",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            "use_ruff": "y",
            "use_mypy": "y",
            "use_pytest": "y",
            "use_coverage": "y",
            "use_pre_commit": "n",
            "use_bandit": "n",
            "use_safety": "n",
            "use_sphinx": "n",
            "use_mkdocs": "y",
            "use_github_actions": "y",
            "use_dependabot": "n",
            "use_codecov": "n",
            "command_line_interface": "typer",
            "use_tox": "n",
            "use_nox": "n",
            "use_commitizen": "n",
            "use_semantic_release": "n",
            "create_changelog": "y",
            "create_contributing": "y",
            "create_code_of_conduct": "y",
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

            # Check README content
            readme_file = project_path / "README.md"
            readme_content = readme_file.read_text(encoding="utf-8")

            # Should have project-specific content
            assert context["project_name"] in readme_content
            assert context["project_short_description"] in readme_content

            # Should have installation instructions
            assert "pip install" in readme_content
            assert "Installation" in readme_content

            # Should have usage examples
            assert "Usage" in readme_content

            # Check CONTRIBUTING.md if enabled
            if context["create_contributing"] == "y":
                contributing_file = project_path / "CONTRIBUTING.md"
                assert contributing_file.exists()

                contributing_content = contributing_file.read_text(encoding="utf-8")
                assert "Contributing" in contributing_content
                assert "development" in contributing_content.lower()

            # Check CHANGELOG.md if enabled
            if context["create_changelog"] == "y":
                changelog_file = project_path / "CHANGELOG.md"
                assert changelog_file.exists()

                changelog_content = changelog_file.read_text(encoding="utf-8")
                assert (
                    "Changelog" in changelog_content or "CHANGELOG" in changelog_content
                )
                assert context["version"] in changelog_content

    def test_code_examples_validity(self, template_dir: Path) -> None:
        """Test that code examples in documentation are valid."""
        # Check tools guide for code examples
        tools_guide = template_dir / "TOOLS_GUIDE.md"

        if tools_guide.exists():
            content = tools_guide.read_text(encoding="utf-8")

            # Extract Python code blocks
            python_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)

            for i, code_block in enumerate(python_blocks):
                try:
                    # Try to compile the code (syntax check)
                    compile(code_block, f"<tools_guide_example_{i}>", "exec")
                except SyntaxError as e:
                    pytest.fail(
                        f"Invalid Python syntax in TOOLS_GUIDE.md example {i}: {e}"
                    )

            # Extract bash/shell code blocks and check for common issues
            bash_blocks = re.findall(r"```bash\n(.*?)\n```", content, re.DOTALL)

            for i, code_block in enumerate(bash_blocks):
                # Check for common shell issues
                lines = code_block.strip().split("\n")
                for line in lines:
                    if line.strip():
                        # Should not have Windows-style paths in bash examples
                        assert not re.match(r"[A-Z]:\\", line), (
                            f"Windows path in bash example: {line}"
                        )

    def test_template_examples_work(self, template_dir: Path) -> None:
        """Test that examples in template documentation actually work."""
        # Test the quick start example
        context = {
            "full_name": "Your Name",
            "email": "your.email@example.com",
            "github_username": "yourusername",
            "project_name": "My Awesome Package",
            "project_slug": "my_awesome_package",
            "project_short_description": "A short description of the package",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            "use_ruff": "y",
            "use_mypy": "y",
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
            "command_line_interface": "typer",
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

            # Project should be created successfully
            assert project_path.exists()
            assert (project_path / "pyproject.toml").exists()
            assert (
                project_path / "src" / "my_awesome_package" / "__init__.py"
            ).exists()

    def test_license_documentation(self, template_dir: Path) -> None:
        """Test that license options are properly documented."""
        import json

        cookiecutter_json = template_dir / "cookiecutter.json"

        with open(cookiecutter_json) as f:
            config = json.load(f)

        if "license" in config and isinstance(config["license"], list):
            license_options = config["license"]

            # Should have common licenses
            common_licenses = ["MIT", "Apache-2.0", "BSD-3-Clause"]

            for license_type in common_licenses:
                assert license_type in license_options, (
                    f"Should support {license_type} license"
                )

            # Test that license template works for each option
            project_template = template_dir / "{{cookiecutter.project_slug}}"
            license_template = project_template / "LICENSE"

            if license_template.exists():
                license_content = license_template.read_text(encoding="utf-8")

                # Should have conditional content for different licenses
                for license_type in license_options:
                    if license_type != "Proprietary":
                        # For SPDX format, check if license is in template variable or explicit
                        if license_type in ["MIT", "BSD-3-Clause"]:
                            assert license_type in license_content, (
                                f"License template should handle {license_type}"
                            )
                        else:
                            # SPDX fallback handles other licenses
                            assert "{{ cookiecutter.license }}" in license_content, (
                                f"Template should handle {license_type} via SPDX"
                            )


class TestExamples:
    """Test example configurations and use cases."""

    @pytest.fixture
    def template_dir(self) -> Path:
        """Return the path to the template directory."""
        return Path(__file__).parent.parent

    @pytest.mark.parametrize(
        "config_name,config",
        [
            (
                "minimal",
                {
                    "use_ruff": "n",
                    "use_mypy": "n",
                    "use_github_actions": "n",
                    "command_line_interface": "none",
                },
            ),
            (
                "basic",
                {
                    "use_ruff": "y",
                    "use_mypy": "n",
                    "use_github_actions": "n",
                    "command_line_interface": "typer",
                },
            ),
            (
                "quality",
                {
                    "use_ruff": "y",
                    "use_mypy": "y",
                    "use_coverage": "y",
                    "use_pre_commit": "y",
                    "command_line_interface": "typer",
                },
            ),
            (
                "enterprise",
                {
                    "use_ruff": "y",
                    "use_mypy": "y",
                    "use_coverage": "y",
                    "use_pre_commit": "y",
                    "use_bandit": "y",
                    "use_safety": "y",
                    "use_github_actions": "y",
                    "use_dependabot": "y",
                    "command_line_interface": "typer",
                },
            ),
        ],
    )
    def test_example_configurations(
        self, template_dir: Path, config_name: str, config: dict[str, str]
    ) -> None:
        """Test different example configurations work correctly."""
        base_context = {
            "full_name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser",
            "project_name": f"Test Package {config_name.title()}",
            "project_slug": f"test_package_{config_name}",
            "project_short_description": f"A test package for {config_name} configuration",
            "version": "0.1.0",
            "python_requires": ">=3.9",
            "license": "MIT",
            # Default all options to 'n'
            "use_ruff": "n",
            "use_mypy": "n",
            "use_pytest": "y",  # Always enable pytest
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

        # Override with specific config
        context = {**base_context, **config}

        with tempfile.TemporaryDirectory() as temp_dir:
            result = cookiecutter(
                str(template_dir),
                no_input=True,
                extra_context=context,
                output_dir=temp_dir,
            )

            project_path = Path(result)
            assert project_path.exists()

            # Check that enabled features have their files
            if config.get("use_ruff") == "y":
                pyproject_file = project_path / "pyproject.toml"
                content = pyproject_file.read_text(encoding="utf-8")
                assert "[tool.ruff" in content, "Ruff config should be present"

            if config.get("use_mypy") == "y":
                pyproject_file = project_path / "pyproject.toml"
                content = pyproject_file.read_text(encoding="utf-8")
                assert "[tool.mypy" in content, "MyPy config should be present"

            if config.get("use_github_actions") == "y":
                ci_file = project_path / ".github" / "workflows" / "ci.yml"
                assert ci_file.exists(), "CI workflow should exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
