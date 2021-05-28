from __future__ import annotations

import urllib.parse
from enum import Enum
from typing import List, Optional

from lander.ext.parser import Contributor, DocumentMetadata
from pydantic import HttpUrl


class Status(str, Enum):
    """Document status states."""

    Delivered = "Delivered"
    Unknown = "Unknown"

    def __str__(self) -> str:
        return self.value


class Difficulty(str, Enum):
    """Difficulty level."""

    Low = "Low"
    Medium = "Medium"
    High = "High"
    Unassigned = "Unassigned"

    def __str__(self) -> str:
        return self.value


class SpherexPipelineModuleMetadata(DocumentMetadata):
    """Metadata container for describing SPHEREx pipeline module documents.

    This metadata is gathered from the content of the document as well as from
    configuration files provided during the build. This metadata is used to
    populate the landing page.
    """

    pipeline_level: str
    """The pipeline level designation."""

    status: Status = Status.Unknown
    """Document status.

    May be one of the choices from the `Status` type.
    """

    difficulty: Difficulty = Difficulty.Unassigned
    """Technical difficulty."""

    diagram_index: Optional[int]

    git_commit_sha: Optional[str]
    """Git Commit SHA."""

    git_ref: Optional[str]
    """Git ref (branch or tag)."""

    git_ref_type: Optional[str]
    """Git ref type (branch or tag)."""

    ci_build_id: Optional[str]
    """CI build ID."""

    ci_build_url: Optional[HttpUrl]
    """URL of the CI job/build."""

    github_slug: Optional[str]
    """The slug (``org/name``) of the repository on GitHub."""

    @property
    def ipac_lead(self) -> Optional[str]:
        """The lead IPAC author."""
        for author in self.authors:
            if author.role == "IPAC Lead":
                return author
        return None

    @property
    def spherex_lead(self) -> Optional[Contributor]:
        """The lead SPHEREx author."""
        for author in self.authors:
            if author.role == "SPHEREx Lead":
                return author
        return None

    @property
    def other_authors(self) -> List[Contributor]:
        """Additional authors."""
        return [
            a
            for a in self.authors
            if a.role not in {"IPAC Lead", "SPHEREx Lead"}
        ]

    @property
    def github_ref_url(self) -> Optional[str]:
        """The GitHub web URL corresponding to the branch or tag."""
        # Ensure sufficient data and GitHub hosting
        if self.repository_url and self.github_slug and self.git_ref:
            repo_url = self.repository_url
            if not repo_url.endswith("/"):
                repo_url = f"{repo_url}/"
            return urllib.parse.urljoin(repo_url, f"tree/{self.git_ref}")
        else:
            return None

    @property
    def github_commit_url(self) -> Optional[str]:
        """The GitHub web URL corresponding to the commit."""
        # Ensure sufficient data and GitHub hosting
        if self.repository_url and self.github_slug and self.git_commit_sha:
            repo_url = self.repository_url
            if not repo_url.endswith("/"):
                repo_url = f"{repo_url}/"
            return urllib.parse.urljoin(
                repo_url, f"commit/{self.git_commit_sha}"
            )
        else:
            return None

    @property
    def dashboard_url(self) -> Optional[str]:
        """URL to the edition dashboard."""
        if self.canonical_url:
            return urllib.parse.urljoin(self.canonical_url, "/v")
        else:
            return None

    @property
    def document_handle_prefix(self) -> Optional[str]:
        """The document handle prefix."""
        if not self.identifier:
            return None

        try:
            code = "-".join(self.identifier.split("-")[:2])
            return code
        except Exception:
            return None
