{%- if cookiecutter.command_line_interface != "none" %}
"""Command line interface for {{ cookiecutter.project_name }}."""

{%- if cookiecutter.command_line_interface == "typer" %}
from typing import Annotated

import typer

from . import __version__
from .core import hello_world


app = typer.Typer(
    name="{{ cookiecutter.project_slug }}",
    help="{{ cookiecutter.project_short_description }}",
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        typer.echo(f"{{ cookiecutter.project_name }} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = False,
) -> None:
    """{{ cookiecutter.project_short_description }}"""


@app.command()
def greet(
    name: Annotated[
        str,
        typer.Argument(help="Name to greet"),
    ] = "World",
) -> None:
    """Greet someone."""
    message = hello_world(name)
    typer.echo(message)


if __name__ == "__main__":
    app()

{%- elif cookiecutter.command_line_interface == "click" %}
import click

from . import __version__
from .core import hello_world


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def main(ctx: click.Context) -> None:
    """{{ cookiecutter.project_short_description }}"""
    ctx.ensure_object(dict)


@main.command()
@click.argument("name", default="World")
def greet(name: str) -> None:
    """Greet someone."""
    message = hello_world(name)
    click.echo(message)


if __name__ == "__main__":
    main()

{%- elif cookiecutter.command_line_interface == "argparse" %}
import argparse
import sys

from . import __version__
from .core import hello_world


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="{{ cookiecutter.project_slug }}",
        description="{{ cookiecutter.project_short_description }}",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{{ cookiecutter.project_name }} v{__version__}",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Greet command
    greet_parser = subparsers.add_parser("greet", help="Greet someone")
    greet_parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name to greet (default: World)",
    )
    
    return parser


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "greet":
        message = hello_world(args.name)
        print(message)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
{%- endif %}
{%- else %}
"""No command line interface configured."""

def main() -> None:
    """Placeholder main function."""
    print("No command line interface configured for this package.")


if __name__ == "__main__":
    main()
{%- endif %}
