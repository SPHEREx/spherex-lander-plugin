"""Parsing plugin for SPHEREx SSDC-IF documents."""

from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, List, Optional

from lander.ext.parser import CiPlatform, Contributor
from lander.ext.parser.texutils.extract import (
    LaTeXCommand,
    LaTeXCommandElement,
)

from ..spherexparser import KVOptionMap, SpherexParser, convert_tex_span
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

    def _parse_authors(self) -> List[Contributor]:
        authors = super()._parse_authors()

        interface_partner = self._parse_interface_partner()
        if interface_partner:
            authors.append(interface_partner)

        return authors

    def _parse_interface_partner(self) -> Optional[Contributor]:
        command_name = "interfaceparter"
        command = LaTeXCommand(
            command_name,
            LaTeXCommandElement(name="options", required=False, bracket="["),
            LaTeXCommandElement(name="name", required=True, bracket="{"),
        )
        instances = [i for i in command.parse(self.tex_source)]
        if len(instances) == 0:
            logger.warning("No %s command detected", command_name)
            return None

        instance = instances[-1]
        name = convert_tex_span(instance["name"])
        if "options" in instance:
            option_map = KVOptionMap.parse(instance["options"])
        else:
            option_map = KVOptionMap()
        if "email" in option_map:
            email = option_map["email"]
        else:
            email = None
        return Contributor(name=name, email=email, role="Interface Partner")
