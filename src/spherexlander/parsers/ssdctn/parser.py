"""Parsing plugin for SPHEREx SSDC-TR documents."""

from __future__ import annotations

from logging import getLogger

from ..spherexparser import SpherexParser
from .datamodel import SpherexSsdcTnMetadata

__all__ = ["SpherexSsdcTnParser"]

logger = getLogger(__name__)


class SpherexSsdcTnParser(SpherexParser[SpherexSsdcTnMetadata]):
    """Lander metadata parser for SPHEREx SSDC-TN documents."""

    def extract_metadata(self) -> SpherexSsdcTnMetadata:
        """Plugin entrypoint for metadata extraction."""
        m = self._collect_common_metadata()
        metadata = SpherexSsdcTnMetadata(**m)
        return metadata
