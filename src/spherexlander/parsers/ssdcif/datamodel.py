from __future__ import annotations

from typing import Optional

from pydantic import Field

from ..spherexdata import ApprovalInfo, SpherexMetadata

__all__ = ["SpherexSsdcIfMetadata"]


class SpherexSsdcIfMetadata(SpherexMetadata):
    """Metadata container for describing SSDC-IF documents.

    This metadata is gathered from the content of the document as well as from
    configuration files provided during the build. This metadata is used to
    populate the landing page.
    """

    approval: Optional[ApprovalInfo] = None

    interface_partner: Optional[str] = Field(
        None, description="The name of the interface partner, if available."
    )
