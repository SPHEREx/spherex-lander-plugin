"""Parsing plugin for SPHEREx PM (project management) documents."""

from __future__ import annotations

from logging import getLogger

from ..spherexparser import SpherexParser
from .datamodel import SpherexProjectManagementMetadata

__all__ = ["SpherexProjectManagementParser"]

logger = getLogger(__name__)


class SpherexProjectManagementParser(
    SpherexParser[SpherexProjectManagementMetadata]
):
    """Lander metadata parser for SPHEREx Project Management (PM) documents."""

    def extract_metadata(self) -> SpherexProjectManagementMetadata:
        """Plugin entrypoint for metadata extraction."""
        m = self._collect_common_metadata()
        m["approval"] = self._parse_approved()
        metadata = SpherexProjectManagementMetadata(**m)
        return metadata
