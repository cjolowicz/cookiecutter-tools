"""Tests for the cache module."""
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

from .utils import commit
from cookiecutter_tools import cache
from cookiecutter_tools import git


@pytest.fixture
def user_cache_dir(monkeypatch: MonkeyPatch, tmp_path: Path) -> Path:
    """Replace the application cache directory by a temporary directory."""
    path = tmp_path / ".cache" / cache.appname
    path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("appdirs.user_cache_dir", lambda *args, **kwargs: path)
    return path


def test_repository_clones(user_cache_dir: Path, repository: git.Repository) -> None:
    """It clones the repository if it does not exist."""
    commit(repository)
    location = str(repository.path)
    mirror = cache.repository(location)
    origin = mirror.git(
        "remote", "get-url", "origin", text=True, capture_output=True
    ).stdout.strip()
    assert origin == location


def test_repository_uses_unique_path(
    user_cache_dir: Path, repository: git.Repository
) -> None:
    """It returns the same path when called multiple times."""
    commit(repository)
    location = str(repository.path)
    mirror1 = cache.repository(location)
    mirror2 = cache.repository(location)
    assert mirror1.path == mirror2.path


def test_repository_updates(user_cache_dir: Path, repository: git.Repository) -> None:
    """It updates the repository if it exists."""
    commit(repository)
    location = str(repository.path)
    cache.repository(location)
    head = commit(repository)
    mirror = cache.repository(location)
    assert mirror.rev_parse("HEAD") == head


def test_worktree_creates(user_cache_dir: Path, repository: git.Repository) -> None:
    """It creates a worktree."""
    head = commit(repository)
    location = str(repository.path)
    cache.repository(location)
    with cache.worktree(location, "HEAD") as worktree:
        assert worktree.rev_parse("HEAD") == head


def test_worktree_removes(user_cache_dir: Path, repository: git.Repository) -> None:
    """It removes the worktree after use."""
    commit(repository)
    location = str(repository.path)
    cache.repository(location)
    with cache.worktree(location, "HEAD") as worktree:
        path = worktree.path
    assert not path.exists()