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

    m = parser.metadata
    assert m.title == "Perform Forced Photometry"
    assert m.version == "1.1"
    assert m.pipeline_level == "L3"

    assert len(m.authors) == 4
    assert len(m.other_authors) == 2
    assert m.ipac_lead.name == "Francis Carrillo"
    assert m.ipac_lead.email == "francis@example.com"
    assert m.spherex_lead.name == "Ursula Gomez"
    assert m.spherex_lead.email == "ursula@example.com"
    assert m.authors[2].name == "Stephanie Lowe"
    assert m.authors[2].email == "stephanie@example.com"
    assert m.authors[3].name == "Efren Archer"
    assert m.authors[3].email == "efren@example.com"
