"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Cookiecutter Tools."""


if __name__ == "__main__":
    main(prog_name="cookiecutter-tools")  # pragma: no cover
