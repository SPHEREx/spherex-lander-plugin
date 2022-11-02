"""Parsing plugin implementation for SPHEREx MS (module specificationLaTeX
documents.
"""

from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, Optional

from lander.ext.parser import CiPlatform
from lander.ext.parser.texutils.extract import (
    LaTeXCommand,
    LaTeXCommandElement,
)

from ..spherexparser import SpherexParser
from .datamodel import Difficulty, SpherexPipelineModuleMetadata

__all__ = ["SpherexPipelineModuleParser"]

logger = getLogger(__name__)


class SpherexPipelineModuleParser(SpherexParser):
    """Lander metadata parser for SPHEREx Module Specification (MS)
    documents.
    """

    def extract_metadata(self) -> SpherexPipelineModuleMetadata:
        """Plugin entrypoint for metadata extraction."""
        m: Dict[str, Any] = {
            "title": self._parse_module_name(),
            "version": self._parse_version(),
            "pipeline_level": self._parse_pipeline_level(),
            "difficulty": self._parse_difficulty(),
            "diagram_index": self._parse_diagram_index(),
            "authors": self._parse_authors(),
            "date_modified": self._parse_date(),
            "identifier": self._parse_handle(),
        }

        # Incorporate metadata from the CI environment
        if self.ci_metadata.platform is not CiPlatform.null:
            m["git_commit_sha"] = self.ci_metadata.git_sha
            m["git_ref"] = self.ci_metadata.git_ref
            m["git_ref_type"] = self.ci_metadata.git_ref_type
            m["ci_build_id"] = self.ci_metadata.build_id
            m["ci_build_url"] = self.ci_metadata.build_url
            m["repository_url"] = self.ci_metadata.github_repository
            m["github_slug"] = self.ci_metadata.github_slug

        # Apply overrides from the command line or lander.yaml
        if self.settings.canonical_url:
            m["canonical_url"] = self.settings.canonical_url
        m.update(self.settings.metadata)
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
