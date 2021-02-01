"""Test the ``spherex`` theme with the pipeline-module test dataset."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from lander.ext.parser import DocumentMetadata
from lander.ext.theme import ThemePluginDirectory
from lander.settings import BuildSettings, DownloadableFile

# from bs4 import BeautifulSoup


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

    data_root = Path(__file__).parent / "data" / "pipeline-module"
    output_dir = Path("_build")
    # Mock up metadata to isolate the test case
    metadata = DocumentMetadata(title="Perform Forced Photometry")
    # Mock build settings as well
    settings = BuildSettings(
        source_path=data_root / "main.tex",
        pdf=DownloadableFile.load(data_root / "main.pdf"),
        output_dir=output_dir,
        parser="spherex-pipeline-module",
        theme="spherex",
    )

    # Load from the plugin system, though directly importing the
    # SpherexTheme is also valid for this test.
    themes = ThemePluginDirectory.load_plugins()
    Theme = themes["spherex"]
    theme = Theme(metadata=metadata, settings=settings)

    assert theme.base_theme_name == "base"
    assert isinstance(theme.base_theme, themes["base"])
    assert theme.metadata == metadata
    assert theme.settings == settings

    theme.build_site()

    assert output_dir.is_dir()

    index_html_path = output_dir / "index.html"
    assert index_html_path.exists()
    pdf_path = output_dir / "main.pdf"
    assert pdf_path.exists()
    # Check that the JS bundle from the base theme is included
    js_path = output_dir / "lander.bundle.js"
    assert js_path.exists()
    # Check that the metadata file exists
    metadata_path = output_dir / "metadata.json"
    assert metadata_path.exists()
