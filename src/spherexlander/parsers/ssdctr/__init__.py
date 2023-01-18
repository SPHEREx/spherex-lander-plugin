"""Parser for SPHEREx SSDC-TR documents."""

from spherexlander.parsers.ssdctr.datamodel import (
    DoorsID,
    SpherexSsdcTrMetadata,
)
from spherexlander.parsers.ssdctr.parser import SpherexSsdcTrParser

__all__ = ["SpherexSsdcTrMetadata", "DoorsID", "SpherexSsdcTrParser"]
