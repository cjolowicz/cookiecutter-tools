"""Command-line interface."""
from typing import Optional

import click
from cookiecutter.log import configure_logger

from ..create.__main__ import validate_extra_context
from ..types import StrMapping
from .core import update


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("extra_context", nargs=-1, callback=validate_extra_context)
@click.option(
    "--interactive",
    is_flag=True,
    default=False,
    help="Prompt for parameters",
    show_default=True,
)
@click.option(
    "-c", "--checkout", help="branch, tag or commit to checkout after git clone"
)
@click.option(
    "--directory",
    help=(
        "Directory within repo that holds cookiecutter.json file "
        "for advanced repositories with multi templates in it"
    ),
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Print debug information", default=False
)
@click.version_option(None, "-V", "--version")
def main(
    extra_context: StrMapping,
    interactive: bool,
    checkout: Optional[str],
    directory: Optional[str],
    verbose: bool,
) -> None:
    """Update a project from a Cookiecutter template."""
    configure_logger(stream_level="DEBUG" if verbose else "INFO")
    update(
        extra_context, interactive=interactive, checkout=checkout, directory=directory
    )


if __name__ == "__main__":
    main(prog_name="cookiecutter-update")  # pragma: no cover
