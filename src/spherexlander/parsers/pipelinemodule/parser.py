"""Parsing plugin implementation for SPHEREx LaTeX documents."""

from __future__ import annotations

import re
from logging import getLogger
from typing import List, Optional

from lander.ext.parser import Contributor, Parser
from lander.ext.parser.pandoc import convert_text

from spherexlander.parsers.pipelinemodule.datamodel import (
    SpherexPipelineModuleMetadata,
)

__all__ = ["SpherexPipelineModuleParser"]

logger = getLogger(__name__)


class SpherexPipelineModuleParser(Parser):
    """Lander metadata parser for SPHEREx documents."""

    def extract_metadata(
        self, tex_source: str
    ) -> SpherexPipelineModuleMetadata:
        """Plugin entrypoint for metadata extraction."""
        metadata = SpherexPipelineModuleMetadata(
            title=self._parse_module_name(),
            version=self._parse_version(),
            pipeline_level=self._parse_pipeline_level(),
            authors=self._parse_authors(),
        )
        return metadata

    def _parse_module_name(self) -> str:
        """Parse the pipeline module name."""
        try:
            name_content = self.tex_macros[r"\modulename"]
            name = convert_text(
                content=name_content, source_fmt="latex", output_fmt="plain"
            )
        except KeyError:
            logger.warning("No modulename command detected")
            return ""

        return name

    def _parse_version(self) -> Optional[str]:
        """Parse the version command."""
        try:
            version = self.tex_macros[r"\version"]
        except KeyError:
            logger.warning("No version command detected")
            return None

        return version

    def _parse_pipeline_level(self) -> Optional[str]:
        """Parse the pipelevel command."""
        try:
            pipeline_level = self.tex_macros[r"\pipelevel"]
        except KeyError:
            logger.warning("No pipelevel command detected")
            return ""

        return pipeline_level

    def _parse_authors(self) -> List[Contributor]:
        """Parse author information, including lead and other authors."""
        authors: List[Contributor] = []

        ipac_match = re.search(
            # Because of normalization, "\ipac\" becomes "IPAC"
            r"IPAC Lead:\s+(?P<author>\S[A-Za-z@\.\s]+)\}",
            self.tex_source,
        )
        if ipac_match:
            authors.append(
                self._split_author_info(ipac_match["author"], role="IPAC Lead")
            )
        else:
            logger.warning("Did not detect IPAC lead")

        spherex_match = re.search(
            # Because of normalization, "\ipac\" becomes "IPAC"
            r"SPHEREx Lead:\s+(?P<author>\S[A-Za-z@\.\s]+)\}",
            self.tex_source,
        )
        if spherex_match:
            authors.append(
                self._split_author_info(
                    spherex_match["author"], role="SPHEREx Lead"
                )
            )
        else:
            logger.warning("Did not detect SPHEREx lead")

        # Parsing "other authors"
        # Sample in the source:
        #
        # {\noindent\bf Other Authors:}\\
        # Stephanie Lowe stephanie@example.com\\
        # Efren Archer efren@example.com\\
        #
        other_match = re.search(
            r"Other Authors:[\{\}\s]+\\\\\n"
            r"(?P<authors>((\S[A-Za-z\s@\.]+)\\\\\n)+)",
            self.tex_source,
        )
        if other_match:
            for author_info in other_match["authors"].strip().split("\n"):
                author_info = author_info.rstrip(r"\\")
                authors.append(self._split_author_info(author_info))

        return authors

    def _split_author_info(
        self, author_string: str, role: Optional[str] = None
    ) -> Contributor:
        """Extract the author name and email into a Contributor object."""
        parts = author_string.strip().split()
        name = " ".join(parts[:-1])
        email = parts[-1]
        return Contributor(name=name, email=email, role=role)
