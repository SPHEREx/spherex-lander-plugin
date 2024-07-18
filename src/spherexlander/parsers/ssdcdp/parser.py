"""Parsing plugin for SPHEREx SSDC-DP documents."""

from __future__ import annotations

from logging import getLogger

from ..spherexparser import SpherexParser
from .datamodel import SpherexSsdcDpMetadata

__all__ = ["SpherexSsdcDpParser"]

logger = getLogger(__name__)


class SpherexSsdcDpParser(SpherexParser[SpherexSsdcDpMetadata]):
    """Lander metadata parser for SPHEREx SSDC-DP documents."""

    def extract_metadata(self) -> SpherexSsdcDpMetadata:
        """Plugin entrypoint for metadata extraction."""
        m = self._collect_common_metadata()
        m["approval"] = self._parse_approved()
        metadata = SpherexSsdcDpMetadata(**m)
        return metadata
