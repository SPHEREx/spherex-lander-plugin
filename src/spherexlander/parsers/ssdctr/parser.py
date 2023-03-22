"""Parsing plugin for SPHEREx SSDC-TR documents."""

from __future__ import annotations

from logging import getLogger
from typing import Optional

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
        m = self._collect_common_metadata()
        m["approval"] = self._parse_approved()
        m["ipac_jira_id"] = self._parse_ipac_jira_id()
        m["va_doors_id"] = self._parse_va_doors_id()
        m["req_doors_id"] = self._parse_req_doors_id()
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
