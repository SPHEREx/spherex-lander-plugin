"""Parsing plugin for SPHEREx SSDC-TR documents."""

from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, Optional

from lander.ext.parser import CiPlatform
from lander.ext.parser.texutils.extract import (
    LaTeXCommand,
    LaTeXCommandElement,
)

from ..spherexparser import SpherexParser
from .datamodel import DoorsID, SpherexSsdcTrMetadata

__all__ = ["SpherexSsdcTrParser"]

logger = getLogger(__name__)


class SpherexSsdcTrParser(SpherexParser):
    """Lander metadata parser for SPHEREx SSDC-TR documents."""

    def extract_metadata(self) -> SpherexSsdcTrMetadata:
        """Plugin entrypoint for metadata extraction."""
        m: Dict[str, Any] = {
            "title": self._parse_title(),
            "version": self._parse_version(),
            "authors": self._parse_authors(),
            "date_modified": self._parse_date(),
            "identifier": self._parse_handle(),
            "approval": self._parse_approved(),
            "ipac_jira_id": self._parse_ipac_jira_id(),
            "va_doors_id": self._parse_va_doors_id(),
            "req_doors_id": self._parse_req_doors_id(),
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
        metadata = SpherexSsdcTrMetadata(**m)
        return metadata

    def _parse_ipac_jira_id(self) -> Optional[str]:
        """Parse the IPACJiraID command."""
        command = LaTeXCommand(
            "IPACJiraID",
            LaTeXCommandElement(name="id", required=True, bracket="{"),
        )
        instances = [i for i in command.parse(self.tex_source)]
        if len(instances) == 0:
            logger.warning("No IPACJiraID command detected")
            return None

        return instances[-1]["id"]

    def _parse_req_doors_id(self) -> Optional[DoorsID]:
        """Parse the ReqDoorsID command."""
        command = LaTeXCommand(
            "ReqDoorsID",
            LaTeXCommandElement(name="url", required=False, bracket="["),
            LaTeXCommandElement(name="id", required=True, bracket="{"),
        )
        instances = [i for i in command.parse(self.tex_source)]
        if len(instances) == 0:
            logger.warning("No ReqDoorsID command detected")
            return None

        return DoorsID(id=instances[-1]["id"], url=instances[-1]["url"])

    def _parse_va_doors_id(self) -> Optional[DoorsID]:
        """Parse the ReqDoorsID command."""
        command = LaTeXCommand(
            "VADoorsID",
            LaTeXCommandElement(name="url", required=False, bracket="["),
            LaTeXCommandElement(name="id", required=True, bracket="{"),
        )
        instances = [i for i in command.parse(self.tex_source)]
        if len(instances) == 0:
            logger.warning("No VADoorsID command detected")
            return None

        return DoorsID(id=instances[-1]["id"], url=instances[-1]["url"])
