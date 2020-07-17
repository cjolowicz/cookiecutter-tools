"""Command-line interface."""
import click

from .create import create


@click.command()
@click.argument("template")
@click.version_option()
def main(template: str) -> None:
    """Create a project from a Cookiecutter template."""
    create(template)


if __name__ == "__main__":
    main(prog_name="cookiecutter-create")  # pragma: no cover
