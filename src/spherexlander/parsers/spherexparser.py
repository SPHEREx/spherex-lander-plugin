"""Common parsing code for spherex-tex documents."""

from __future__ import annotations

import datetime
from collections import UserDict
from logging import getLogger
from typing import Any, List, Optional

import dateutil.parser
from lander.ext.parser import CiPlatform, Contributor, Parser
from lander.ext.parser.pandoc import convert_text
from lander.ext.parser.texutils.extract import (
    LaTeXCommand,
    LaTeXCommandElement,
)

from .spherexdata import ApprovalInfo

__all__ = ["SpherexParser", "KVOptionMap"]

logger = getLogger(__name__)


class SpherexParser(Parser):
    """A base parser for documents that use the ``spherex`` tex class.

    Parsers for specific document types can inherit from this base class
    to implement their specific data models.
    """

    def _collect_common_metadata(self) -> dict[str, Any]:
        """Collect metadata common to most SPHEREx documents.

        The extract_metadata methods of individual documents can enrich this
        data as necessary.
        """
        m: dict[str, Any] = {
            "version": self._parse_version(),
            "authors": self._parse_authors(),
            "date_modified": self._parse_date(),
            "identifier": self._parse_handle(),
        }
        try:
            # some documents may have other ways of setting the title
            # than the \title attribute
            m["title"] = self._parse_title()
        except Exception:
            pass

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

        return m

    def _parse_title(self) -> str:
        """Parse the title command.

        If the title command includes an optional short version, this method
        parsers only the required longer version.
        """
        command = LaTeXCommand(
            "title",
            LaTeXCommandElement(
                name="short_title", required=False, bracket="["
            ),
            LaTeXCommandElement(name="long_title", required=True, bracket="{"),
        )
        titles = [t for t in command.parse(self.tex_source)]
        if len(titles) == 0:
            raise RuntimeError("Could not parse a title command.")
        return titles[-1]["long_title"]

    def _parse_version(self) -> Optional[str]:
        """Parse the version command."""
        command = LaTeXCommand(
            "version",
            LaTeXCommandElement(name="version", required=True, bracket="{"),
        )
        versions = [v for v in command.parse(self.tex_source)]
        if len(versions) == 0:
            logger.warning("No version command detected")
            return None
        return versions[-1]["version"]

    def _parse_authors(self) -> List[Contributor]:
        """Parse author information, including lead and other authors."""
        authors: List[Contributor] = []

        spherex_lead = self._parse_lead(kind="spherex", role="SPHEREx Lead")
        if spherex_lead:
            authors.append(spherex_lead)

        ipac_lead = self._parse_lead(kind="ipac", role="IPAC Lead")
        if ipac_lead:
            authors.append(ipac_lead)

        author_command = LaTeXCommand(
            "author",
            LaTeXCommandElement(name="body", required=True, bracket="{"),
        )
        person_command = LaTeXCommand(
            "person",
            LaTeXCommandElement(name="options", required=False, bracket="["),
            LaTeXCommandElement(name="name", required=True, bracket="{"),
        )

        for author_instance in author_command.parse(self.tex_source):
            for person_instance in person_command.parse(
                author_instance["body"]
            ):
                name = convert_tex_span(person_instance["name"])
                if "options" in person_instance:
                    option_map = KVOptionMap.parse(person_instance["options"])
                else:
                    option_map = KVOptionMap()
                if "email" in option_map:
                    email = option_map["email"]
                else:
                    email = None
                authors.append(Contributor(name=name, email=email))

        return authors

    def _parse_lead(self, *, kind: str, role: str) -> Optional[Contributor]:
        command_name = f"{kind}lead"
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
        return Contributor(name=name, email=email, role=role)

    def _parse_date(self) -> Optional[datetime.date]:
        """Parse the date from either the docDate or vcsDate commands."""
        # Try docDate first
        value = None
        if r"\docDate" in self.tex_macros:
            value = self.tex_macros[r"\docDate"]
        elif r"\vcsDate" in self.tex_macros:
            value = self.tex_macros[r"\vcsDate"]

        if value:
            return dateutil.parser.isoparse(value).date()
        else:
            return None

    def _parse_handle(self) -> Optional[str]:
        """Parse the sphereHandle command."""
        command = LaTeXCommand(
            "spherexHandle",
            LaTeXCommandElement(name="value", required=True, bracket="{"),
        )
        instances = [i for i in command.parse(self.tex_source)]
        if len(instances) == 0:
            logger.warning("No spherexHandle command detected")
            return None

        return instances[-1]["value"]

    def _parse_approved(self) -> Optional[ApprovalInfo]:
        """Parse the approved command."""
        command = LaTeXCommand(
            "approved",
            LaTeXCommandElement(name="date", required=True, bracket="{"),
            LaTeXCommandElement(name="name", required=True, bracket="{"),
        )
        instances = [i for i in command.parse(self.tex_source)]
        if len(instances) == 0:
            logger.warning("No approved command detected")
            return None

        return ApprovalInfo(
            name=instances[-1]["name"],
            date=instances[-1]["date"],
        )


class KVOptionMap(UserDict):
    """A model for the attributes encoded as key-value pairs in the
    options of a tex command.
    """

    @classmethod
    def parse(self, options: str) -> KVOptionMap:
        """Parse the key-value options."""
        keyvalues = [kv.strip() for kv in options.split(",")]
        split_keyvalues = [tuple(kv.split("=")[:2]) for kv in keyvalues]
        # A work-around for type checking; could be improved
        return KVOptionMap({k: v for k, v in split_keyvalues})


def convert_tex_span(content: str) -> str:
    return convert_text(
        content=content,
        source_fmt="latex",
        output_fmt="plain",
        deparagraph=True,
    )
