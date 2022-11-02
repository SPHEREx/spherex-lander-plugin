"""Test the ``spherex`` theme with the test datasets."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from lander.ext.theme import ThemePluginDirectory
from lander.settings import BuildSettings

from spherexlander.parsers.pipelinemodule import SpherexPipelineModuleParser
from spherexlander.parsers.projectmanagement import (
    SpherexProjectManagementParser,
)

if TYPE_CHECKING:
    from _pytest.logging import LogCaptureFixture


def test_spherex_pipelinemodule(
    caplog: LogCaptureFixture, temp_cwd: Path
) -> None:
    """Test the spherex theme plugin using the ``tests/data/pipeline-module``
    sample.
    """
    caplog.set_level(logging.DEBUG, logger="lander")
    caplog.set_level(logging.DEBUG, logger="spherexlander")

    root_dir = Path(__file__).parent / "data" / "pipeline-module"
    # Located in the _build/ dir of root project directory for
    # visual review
    output_dir = Path(__file__).parent / ".." / "_build" / "pipeline-module"

    settings = BuildSettings.load(
        source_path=root_dir / "ssdc-ms-001.tex",
        pdf=root_dir / "SSDC-MS-001.pdf",
        output_dir=output_dir,
        parser="spherex-pipeline-module",
        theme="spherex",
    )
    parser = SpherexPipelineModuleParser(settings=settings)

    # Load from the plugin system, though directly importing the
    # SpherexTheme is also valid for this test.
    themes = ThemePluginDirectory.load_plugins()
    Theme = themes["spherex"]
    theme = Theme(metadata=parser.metadata, settings=settings)

    assert theme.base_theme_name == "base"
    assert isinstance(theme.base_theme, themes["base"])
    assert theme.metadata == parser.metadata
    assert theme.settings == settings

    theme.build_site()

    assert output_dir.is_dir()

    index_html_path = output_dir / "index.html"
    assert index_html_path.exists()
    pdf_path = output_dir / "SSDC-MS-001.pdf"
    assert pdf_path.exists()
    # Check that the JS bundle from the base theme is included
    js_path = output_dir / "lander.bundle.js"
    assert js_path.exists()
    # Check that the metadata file exists
    metadata_path = output_dir / "metadata.json"
    assert metadata_path.exists()

    metadata = json.loads(metadata_path.read_text())
    assert metadata["title"] == "Perform Forced Photometry"
    assert metadata["pipeline_level"] == "L3"
    assert metadata["diagram_index"] == 2
    assert metadata["difficulty"] == "High"


def test_spherex_projectmanagement(
    caplog: LogCaptureFixture, temp_cwd: Path
) -> None:
    """Test the spherex theme plugin using the ``tests/data/pm-document``
    sample.
    """
    caplog.set_level(logging.DEBUG, logger="lander")
    caplog.set_level(logging.DEBUG, logger="spherexlander")

    root_dir = Path(__file__).parent / "data" / "pm-document"
    # Located in the _build/ dir of root project directory for
    # visual review
    output_dir = Path(__file__).parent / ".." / "_build" / "pm-document"

    settings = BuildSettings.load(
        source_path=root_dir / "SSDC-PM-001.tex",
        pdf=root_dir / "SSDC-PM-001.pdf",
        output_dir=output_dir,
        parser="spherex-project-management",
        theme="spherex",
    )
    parser = SpherexProjectManagementParser(settings=settings)

    # Load from the plugin system, though directly importing the
    # SpherexTheme is also valid for this test.
    themes = ThemePluginDirectory.load_plugins()
    Theme = themes["spherex"]
    theme = Theme(metadata=parser.metadata, settings=settings)

    assert theme.base_theme_name == "base"
    assert isinstance(theme.base_theme, themes["base"])
    assert theme.metadata == parser.metadata
    assert theme.settings == settings

    theme.build_site()

    assert output_dir.is_dir()

    index_html_path = output_dir / "index.html"
    assert index_html_path.exists()
    pdf_path = output_dir / "SSDC-PM-001.pdf"
    assert pdf_path.exists()
    # Check that the JS bundle from the base theme is included
    js_path = output_dir / "lander.bundle.js"
    assert js_path.exists()
    # Check that the metadata file exists
    metadata_path = output_dir / "metadata.json"
    assert metadata_path.exists()

    metadata = json.loads(metadata_path.read_text())
    assert metadata["title"] == "Example Title"
