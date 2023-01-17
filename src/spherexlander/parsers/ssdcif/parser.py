"""Parsing plugin for SPHEREx SSDC-IF documents."""

from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, Optional

from lander.ext.parser import CiPlatform
from lander.ext.parser.texutils.extract import (
    LaTeXCommand,
    LaTeXCommandElement,
)

from ..spherexparser import SpherexParser, convert_tex_span
from .datamodel import SpherexSsdcIfMetadata

__all__ = ["SpherexSsdcIfParser"]

logger = getLogger(__name__)


class SpherexSsdcIfParser(SpherexParser):
    """Lander metadata parser for SPHEREx SSDC-IF documents."""

    def extract_metadata(self) -> SpherexSsdcIfMetadata:
        """Plugin entrypoint for metadata extraction."""
        m: Dict[str, Any] = {
            "title": self._parse_title(),
            "version": self._parse_version(),
            "authors": self._parse_authors(),
            "date_modified": self._parse_date(),
            "identifier": self._parse_handle(),
            "interface_partner": self._parse_interface_partner(),
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
