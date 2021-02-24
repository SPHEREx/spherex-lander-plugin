from __future__ import annotations

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
