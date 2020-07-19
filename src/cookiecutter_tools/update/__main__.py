"""Command-line interface."""
import click

from .core import update


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(None, "-V", "--version")
def main() -> None:
    """Update a project from a Cookiecutter template."""
    update()


if __name__ == "__main__":
    main(prog_name="cookiecutter-update")  # pragma: no cover
