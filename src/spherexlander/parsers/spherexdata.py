"""Core data model for SPHEREx documents."""

from __future__ import annotations

import urllib.parse
from typing import Optional

from lander.ext.parser import DocumentMetadata
from pydantic import BaseModel, Field, HttpUrl

__all__ = ["SpherexMetadata", "ApprovalInfo"]


class SpherexMetadata(DocumentMetadata):
    """A basic metadata container for describing SPHEREx documents.

    Individual documents can inherit and add to this base set of metadata.
    """

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
            if self.canonical_url.endswith("/"):
                return f"{self.canonical_url}v/"
            else:
                return f"{self.canonical_url}/v/"
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


class ApprovalInfo(BaseModel):
    """A document's approval metadata."""

    name: str = Field(..., description="Name of the approver.")

    date: str = Field(..., description="Date of the approval.")
