"""Test cases for the __main__ module."""
from click.testing import CliRunner

from cookiecutter_tools.update import __main__


def test_help_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main, ["--help"])
    assert result.exit_code == 0
