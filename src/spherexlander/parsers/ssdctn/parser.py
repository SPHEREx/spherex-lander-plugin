"""Parsing plugin for SPHEREx SSDC-TR documents."""

from __future__ import annotations

from logging import getLogger
from typing import Any, Dict

from lander.ext.parser import CiPlatform

from ..spherexparser import SpherexParser
from .datamodel import SpherexSsdcTnMetadata

__all__ = ["SpherexSsdcTnParser"]

logger = getLogger(__name__)


class SpherexSsdcTnParser(SpherexParser):
    """Lander metadata parser for SPHEREx SSDC-TN documents."""

    def extract_metadata(self) -> SpherexSsdcTnMetadata:
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
        metadata = SpherexSsdcTnMetadata(**m)
        return metadata
