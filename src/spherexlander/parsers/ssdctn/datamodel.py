from __future__ import annotations

from ..spherexdata import SpherexMetadata

__all__ = ["SpherexSsdcTnMetadata"]


class SpherexSsdcTnMetadata(SpherexMetadata):
    """Metadata container for describing SSDC-TN documents.

    This metadata is gathered from the content of the document as well as from
    configuration files provided during the build. This metadata is used to
    populate the landing page.
    """
