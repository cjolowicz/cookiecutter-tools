"""Command-line interface."""
from typing import Tuple

import click
from cookiecutter.cli import validate_extra_context

from .create import create


@click.command()
@click.argument("template")
@click.argument("extra_context", nargs=-1, callback=validate_extra_context)
@click.version_option()
def main(template: str, extra_context: Tuple[str]) -> None:
    """Create a project from a Cookiecutter template."""
    create(template, extra_context)


if __name__ == "__main__":
    main(prog_name="cookiecutter-create")  # pragma: no cover
