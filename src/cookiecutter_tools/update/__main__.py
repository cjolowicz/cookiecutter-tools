"""Command-line interface."""
import click

from ..create.__main__ import validate_extra_context
from ..types import StrMapping
from .core import update


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("extra_context", nargs=-1, callback=validate_extra_context)
@click.version_option(None, "-V", "--version")
def main(extra_context: StrMapping) -> None:
    """Update a project from a Cookiecutter template."""
    update(extra_context)


if __name__ == "__main__":
    main(prog_name="cookiecutter-update")  # pragma: no cover
