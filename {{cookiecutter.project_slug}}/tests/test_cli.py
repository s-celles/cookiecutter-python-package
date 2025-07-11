"""Tests for CLI functionality."""
{%- if cookiecutter.use_pytest == "y" and cookiecutter.command_line_interface != "none" %}
{%- if cookiecutter.command_line_interface == "typer" %}

from typer.testing import CliRunner

from {{ cookiecutter.project_slug.replace('-', '_') }}.cli import app

runner = CliRunner()


def test_cli_version():
    """Test version option."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "{{ cookiecutter.project_name }}" in result.stdout


def test_cli_greet_default():
    """Test greet command with default name."""
    result = runner.invoke(app, ["greet"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout


def test_cli_greet_custom():
    """Test greet command with custom name."""
    result = runner.invoke(app, ["greet", "Python"])
    assert result.exit_code == 0
    assert "Hello, Python!" in result.stdout


def test_cli_help():
    """Test help message."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "{{ cookiecutter.project_short_description }}" in result.stdout

{%- elif cookiecutter.command_line_interface == "click" %}
from click.testing import CliRunner

from {{ cookiecutter.project_slug.replace('-', '_') }}.cli import main


runner = CliRunner()


def test_cli_version():
    """Test version option."""
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0


def test_cli_greet_default():
    """Test greet command with default name."""
    result = runner.invoke(main, ["greet"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_cli_greet_custom():
    """Test greet command with custom name."""
    result = runner.invoke(main, ["greet", "Python"])
    assert result.exit_code == 0
    assert "Hello, Python!" in result.output

{%- elif cookiecutter.command_line_interface == "argparse" %}
import io
import sys
from unittest.mock import patch

from {{ cookiecutter.project_slug.replace('-', '_') }}.cli import main, create_parser


def test_parser_creation():
    """Test parser creation."""
    parser = create_parser()
    assert parser is not None


def test_greet_command(capsys):
    """Test greet command."""
    with patch.object(sys, 'argv', ['{{ cookiecutter.project_slug }}', 'greet', 'Python']):
        main()
    captured = capsys.readouterr()
    assert "Hello, Python!" in captured.out


def test_greet_default(capsys):
    """Test greet command with default name."""
    with patch.object(sys, 'argv', ['{{ cookiecutter.project_slug }}', 'greet']):
        main()
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out
{%- endif %}

{%- elif cookiecutter.command_line_interface != "none" %}
"""Simple CLI tests without pytest."""

from {{ cookiecutter.project_slug }}.cli import main


def test_main_function():
    """Test that main function exists and can be called."""
    try:
        # This will likely fail due to missing arguments, but we just want to ensure it's callable
        main()
    except SystemExit:
        # Expected for argparse when no args provided
        pass
    except Exception as e:
        # For typer/click, they handle help differently
        if "No such command" not in str(e):
            raise


if __name__ == "__main__":
    test_main_function()
    print("CLI tests passed!")
{%- endif %}
