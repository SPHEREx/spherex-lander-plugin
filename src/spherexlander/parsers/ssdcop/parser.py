"""Parsing plugin for SPHEREx SSDC-TR documents."""

from __future__ import annotations

from logging import getLogger

from ..spherexparser import SpherexParser
from .datamodel import SpherexSsdcOpMetadata

__all__ = ["SpherexSsdcOpParser"]

logger = getLogger(__name__)


class SpherexSsdcOpParser(SpherexParser):
    """Lander metadata parser for SPHEREx SSDC-OP documents."""

    def extract_metadata(self) -> SpherexSsdcOpMetadata:
        """Plugin entrypoint for metadata extraction."""
        m = self._collect_common_metadata()
        m["approval"] = self._parse_approved()
        metadata = SpherexSsdcOpMetadata(**m)
        return metadata
