"""Parsing plugin for SPHEREx SSDC-IF documents."""

from __future__ import annotations

from logging import getLogger
from typing import Optional

from lander.ext.parser.texutils.extract import (
    LaTeXCommand,
    LaTeXCommandElement,
)

from ..spherexparser import SpherexParser, convert_tex_span
from .datamodel import SpherexSsdcIfMetadata

__all__ = ["SpherexSsdcIfParser"]

logger = getLogger(__name__)


class SpherexSsdcIfParser(SpherexParser[SpherexSsdcIfMetadata]):
    """Lander metadata parser for SPHEREx SSDC-IF documents."""

    def extract_metadata(self) -> SpherexSsdcIfMetadata:
        """Plugin entrypoint for metadata extraction."""
        m = self._collect_common_metadata()
        m["interface_partner"] = self._parse_interface_partner()
        m["approval"] = self._parse_approved()
        metadata = SpherexSsdcIfMetadata(**m)
        return metadata

    def _parse_interface_partner(self) -> Optional[str]:
        command_name = "interfacepartner"
        command = LaTeXCommand(
            command_name,
            LaTeXCommandElement(name="name", required=True, bracket="{"),
        )
        instances = [i for i in command.parse(self.tex_source)]
        if len(instances) == 0:
            logger.warning("No %s command detected", command_name)
            return None

        instance = instances[-1]
        name = convert_tex_span(instance["name"])
        return name
