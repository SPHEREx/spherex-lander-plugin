"""Parsing plugin implementation for SPHEREx MS (module specificationLaTeX
documents.
"""

from __future__ import annotations

from logging import getLogger
from typing import Optional

from lander.ext.parser.texutils.extract import (
    LaTeXCommand,
    LaTeXCommandElement,
)

from ..spherexparser import SpherexParser
from .datamodel import Difficulty, SpherexPipelineModuleMetadata

__all__ = ["SpherexPipelineModuleParser"]

logger = getLogger(__name__)


class SpherexPipelineModuleParser(
    SpherexParser[SpherexPipelineModuleMetadata]
):
    """Lander metadata parser for SPHEREx Module Specification (MS)
    documents.
    """

    def extract_metadata(self) -> SpherexPipelineModuleMetadata:
        """Plugin entrypoint for metadata extraction."""
        m = self._collect_common_metadata()
        m["title"] = self._parse_module_name()
        m["pipeline_level"] = self._parse_pipeline_level()
        m["difficulty"] = self._parse_difficulty()
        m["diagram_index"] = self._parse_diagram_index()
        m["approval"] = self._parse_approved()
        metadata = SpherexPipelineModuleMetadata(**m)
        return metadata

    def _parse_module_name(self) -> str:
        """Parse the pipeline module name."""
        command = LaTeXCommand(
            "modulename",
            LaTeXCommandElement(name="name", required=True, bracket="{"),
        )
        names = [n for n in command.parse(self.tex_source)]
        if len(names) == 0:
            raise RuntimeError("Could not parse a modulename command.")
        return names[-1]["name"]

    def _parse_pipeline_level(self) -> Optional[str]:
        """Parse the pipelevel command."""
        command = LaTeXCommand(
            "pipelevel",
            LaTeXCommandElement(name="level", required=True, bracket="{"),
        )
        levels = [i for i in command.parse(self.tex_source)]
        if len(levels) == 0:
            logger.warning("No pipelevel command detected")
            return None
        return levels[-1]["level"]

    def _parse_difficulty(self) -> Difficulty:
        """Parse the difficulty command."""
        command = LaTeXCommand(
            "difficulty",
            LaTeXCommandElement(name="difficulty", required=True, bracket="{"),
        )
        difficulties = [d for d in command.parse(self.tex_source)]
        if len(difficulties) == 0:
            logger.warning("No difficulty command detected")
            return Difficulty.Unassigned

        value = difficulties[-1]["difficulty"]
        try:
            return Difficulty[value]
        except Exception:
            logger.warning(
                "Difficulty value %s is not one of: %s",
                value,
                str([d.name for d in Difficulty]),
            )
            return Difficulty.Unassigned

    def _parse_diagram_index(self) -> Optional[int]:
        """Parse the diagramindex command."""
        command = LaTeXCommand(
            "diagramindex",
            LaTeXCommandElement(name="di", required=True, bracket="{"),
        )
        diagramindices = [di for di in command.parse(self.tex_source)]
        if len(diagramindices) == 0:
            logger.warning("No diagramindex command detected")
            return None

        return int(diagramindices[-1]["di"])
