"""Determining the versions tagged in a Git repository."""
from __future__ import annotations

import contextlib
from dataclasses import dataclass
from typing import Iterable
from typing import Optional

from packaging.specifiers import SpecifierSet
from packaging.version import InvalidVersion
from packaging.version import Version

from . import git


@dataclass
class VersionTag:
    """Git tag for a version according to PEP 440."""

    name: str
    version: Version

    @classmethod
    def create(cls, name: str) -> VersionTag:
        """Parse the tag name as a PEP 440 version."""
        version = Version(name[1:] if name.startswith("v") else name)
        return cls(name, version)


def load(repository: git.Repository) -> Iterable[VersionTag]:
    """Load versions tagged in the repository."""
    for tag in repository.tags():
        with contextlib.suppress(InvalidVersion):
            yield VersionTag.create(tag)


def filter(tags: Iterable[VersionTag], specifier: str) -> Iterable[VersionTag]:
    """Return only the version tags that satisfy the given specifier."""
    mapping = {tag.version: tag for tag in tags}
    versions = SpecifierSet(specifier).filter(mapping.keys())
    return [mapping[version] for version in versions]


def find_latest(
    repository: git.Repository, *, specifier: Optional[str] = None
) -> Optional[str]:
    """Return the Git tag for the latest version."""
    tags = list(load(repository))

    if tags and specifier is not None:
        tags = filter(tags, specifier)

    if tags:
        latest = max(tags, key=lambda tag: tag.version)
        return latest.name

    return None
