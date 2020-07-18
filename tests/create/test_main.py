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


@pytest.fixture
def user_config_file(tmp_path: Path) -> Path:
    """Configure cookiecutter to write to temporary directories."""
    path = tmp_path / ".cookiecutterrc"
    cookiecutters_dir = tmp_path / "cookiecutters_dir"
    replay_dir = tmp_path / "replay_dir"
    config = f"""\
    cookiecutters_dir: {cookiecutters_dir}
    replay_dir: {replay_dir}
    """
    path.write_text(dedent(config))
    return path


def test_create(
    runner: CliRunner,
    user_cache_dir: Path,
    user_config_file: Path,
    template: git.Repository,
) -> None:
    """It generates a project from the template."""
    result = runner.invoke(
        __main__.main,
        [str(template.path), f"--config-file={user_config_file}"],
        input="example",
        catch_exceptions=False,
    )
    assert result.exit_code == 0


def _replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    text = text.replace(old, new)
    path.write_text(text)


def test_undefined_variable(
    runner: CliRunner,
    user_cache_dir: Path,
    user_config_file: Path,
    template: git.Repository,
) -> None:
    """It displays an informative error message if a variable is undefined."""
    _replace(template.path / "cookiecutter.json", "project", "XXproject")

    template.git("add", ".")
    template.git("commit", "--message=Typo")
    template.git("tag", "v1.0.1")

    result = runner.invoke(
        __main__.main,
        [str(template.path), f"--config-file={user_config_file}"],
        input="example",
        catch_exceptions=False,
    )

    assert "has no attribute 'project'" in result.output


def test_output_directory_exists(
    runner: CliRunner,
    user_cache_dir: Path,
    user_config_file: Path,
    template: git.Repository,
) -> None:
    """It displays an informative error message if the output directory exists."""
    Path("example").mkdir()

    result = runner.invoke(
        __main__.main,
        [str(template.path), f"--config-file={user_config_file}"],
        input="example",
        catch_exceptions=False,
    )

    assert "already exists" in result.output


def test_checkout(
    runner: CliRunner,
    user_cache_dir: Path,
    user_config_file: Path,
    template: git.Repository,
) -> None:
    """It checks out the specified revision."""
    _replace(
        template.path / "{{cookiecutter.project}}" / "README.md",
        "# {{cookiecutter.project}}",
        "## {{cookiecutter.project}}",
    )

    template.git("add", ".")
    template.git("commit", "--message=Style")

    runner.invoke(
        __main__.main,
        [str(template.path), f"--config-file={user_config_file}", "--checkout=master"],
        input="example",
        catch_exceptions=False,
    )

    assert (Path("example") / "README.md").read_text().startswith("## ")
