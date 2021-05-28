"""Parsing plugin implementation for SPHEREx LaTeX documents."""

from __future__ import annotations

from collections import UserDict
from logging import getLogger
from typing import Any, Dict, List, Optional

from lander.ext.parser import CiPlatform, Contributor, Parser
from lander.ext.parser.pandoc import convert_text
from lander.ext.parser.texutils.extract import (
    LaTeXCommand,
    LaTeXCommandElement,
)

from spherexlander.parsers.pipelinemodule.datamodel import (
    Difficulty,
    SpherexPipelineModuleMetadata,
)

__all__ = ["SpherexPipelineModuleParser"]

logger = getLogger(__name__)


class SpherexPipelineModuleParser(Parser):
    """Lander metadata parser for SPHEREx documents."""

    def extract_metadata(self) -> SpherexPipelineModuleMetadata:
        """Plugin entrypoint for metadata extraction."""
        m: Dict[str, Any] = {
            "title": self._parse_module_name(),
            "version": self._parse_version(),
            "pipeline_level": self._parse_pipeline_level(),
            "difficulty": self._parse_difficulty(),
            "diagram_index": self._parse_diagram_index(),
            "authors": self._parse_authors(),
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


class KVOptionMap(UserDict):
    @classmethod
    def parse(self, options: str) -> KVOptionMap:
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
