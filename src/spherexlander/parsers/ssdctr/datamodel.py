from __future__ import annotations

from typing import List, Optional

from lander.ext.parser import Contributor
from pydantic import BaseModel, Field

from ..spherexdata import ApprovalInfo, SpherexMetadata

__all__ = ["SpherexSsdcTrMetadata"]


class DoorsID(BaseModel):
    """A model for a Doors ID (either VA or Req)"""

    id: str = Field(..., description="Doors ID")

    url: str = Field(..., description="Doors URL")


class SpherexSsdcTrMetadata(SpherexMetadata):
    """Metadata container for describing SSDC-TR documents.

    This metadata is gathered from the content of the document as well as from
    configuration files provided during the build. This metadata is used to
    populate the landing page.
    """

    approval: Optional[ApprovalInfo] = None

    ipac_jira_id: Optional[str] = Field(
        None, description="IPAC Jira issue ID for test report."
    )

    va_doors_id: Optional[DoorsID] = Field(
        None, description="VA (verification activity) Doors ID"
    )

    req_doors_id: Optional[DoorsID] = Field(
        None, description="REQ (requirement) Doors ID"
    )

    @property
    def ipac_lead_v2(self) -> Optional[Contributor]:
        """The lead IPAC author."""
        for author in self.authors:
            if author.role == "IPAC Lead":
                return author
        return None

    @property
    def other_authors(self) -> List[Contributor]:
        """Additional authors."""
        return [a for a in self.authors if a.role not in {"IPAC Lead"}]
