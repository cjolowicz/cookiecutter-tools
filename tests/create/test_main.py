"""Test cases for the __main__ module."""
from pathlib import Path
from textwrap import dedent
from typing import Iterator

import pytest
from click.testing import CliRunner

from cookiecutter_tools import git
from cookiecutter_tools.create import __main__


@pytest.fixture
def runner() -> Iterator[CliRunner]:
    """Fixture for invoking command-line interfaces."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main, ["--help"])
    assert result.exit_code == 0


@pytest.fixture
def template(repository: git.Repository) -> git.Repository:
    """Set up a minimal template repository."""
    cookiecutter_json = """\
    {
      "project": "example"
    }
    """

    readme = """\
    # {{cookiecutter.project}}
    """

    (repository.path / "{{cookiecutter.project}}").mkdir()
    (repository.path / "{{cookiecutter.project}}" / "README.md").write_text(
        dedent(readme)
    )
    (repository.path / "cookiecutter.json").write_text(dedent(cookiecutter_json))

    repository.git("add", ".")
    repository.git("commit", "--message=Initial commit")
    repository.git("tag", "v1.0.0")

    return repository


def test_create(
    runner: CliRunner, user_cache_dir: Path, template: git.Repository
) -> None:
    """It generates a project from the template."""
    result = runner.invoke(
        __main__.main, [str(template.path)], input="example", catch_exceptions=False
    )
    assert result.exit_code == 0
