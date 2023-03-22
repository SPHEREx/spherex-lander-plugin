from __future__ import annotations

from typing import Optional

from ..spherexdata import ApprovalInfo, SpherexMetadata

__all__ = ["SpherexProjectManagementMetadata"]


class SpherexProjectManagementMetadata(SpherexMetadata):
    """Metadata container for describing SPHEREx Project Management (PM)
    documents.

    This metadata is gathered from the content of the document as well as from
    configuration files provided during the build. This metadata is used to
    populate the landing page.
    """

    approval: Optional[ApprovalInfo] = None
