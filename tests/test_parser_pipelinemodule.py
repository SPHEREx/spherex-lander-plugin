"""Test the SPHEREx parser using the "pipeline-module" sample dataset."""

from __future__ import annotations

from pathlib import Path

from spherexlander.parsers.pipelinemodule import SpherexPipelineModuleParser


def test_demodoc() -> None:
    """Test with the demodoc (tests/data/pipeline-module/main.tex)."""
    root_tex_path = (
        Path(__file__).parent / "data" / "pipeline-module" / "main.tex"
    )

    parser = SpherexPipelineModuleParser(root_tex_path)

    assert parser.metadata.title == "Perform Forced Photometry"
