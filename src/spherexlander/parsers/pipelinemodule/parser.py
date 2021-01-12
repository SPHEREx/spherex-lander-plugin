"""Parsing plugin implementation for SPHEREx LaTeX documents."""

from __future__ import annotations

from logging import getLogger
from typing import Dict

from lander.ext.parser import DocumentMetadata, Parser
from lander.ext.parser.pandoc import convert_text

__all__ = ["SpherexPipelineModuleParser"]

logger = getLogger(__name__)


class SpherexPipelineModuleParser(Parser):
    """Lander metadata parser for SPHEREx documents."""

    def extract_metadata(self, tex_source: str) -> DocumentMetadata:
        """Plugin entrypoint for metadata extraction."""
        metadata = DocumentMetadata(
            title=self._parse_module_name(self.tex_macros)
        )
        return metadata

    def _parse_module_name(self, newcommands: Dict[str, str]) -> str:
        """Parse the pipeline module name."""
        try:
            name_content = newcommands[r"\modulename"]
            name = convert_text(
                content=name_content, source_fmt="latex", output_fmt="plain"
            )
        except KeyError:
            logger.warning("No modulename command detected")
            return ""

        return name
