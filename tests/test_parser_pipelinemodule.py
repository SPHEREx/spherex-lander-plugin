"""Test the SPHEREx parser using the "pipeline-module" sample dataset."""

from __future__ import annotations

from pathlib import Path

from lander.settings import BuildSettings

from spherexlander.parsers.pipelinemodule import SpherexPipelineModuleParser
from spherexlander.parsers.pipelinemodule.datamodel import Difficulty


def test_demodoc() -> None:
    """Test with the demodoc (tests/data/pipeline-module/ssdc-ms-001.tex)."""
    data_root = Path(__file__).parent / "data" / "pipeline-module"
    output_dir = Path("_build")

    settings = BuildSettings.load(
        source_path=data_root / "ssdc-ms-001.tex",
        pdf=data_root / "SSDC-MS-001.pdf",
        output_dir=output_dir,
        parser="spherex-pipeline-module",
        theme="spherex",
    )

    parser = SpherexPipelineModuleParser(settings=settings)

    m = parser.metadata
    assert m.title == "Perform Forced Photometry"
    assert m.version == "1.1"
    assert m.diagram_index == 2
    assert m.pipeline_level == "L3"
    assert m.difficulty == Difficulty.High

    assert len(m.authors) == 4
    assert len(m.other_authors) == 2
    assert m.ipac_lead is not None
    assert m.ipac_lead.name == "Francis Carrillo"
    assert m.ipac_lead.email == "francis@example.com"
    assert m.spherex_poc is not None
    assert m.spherex_poc.name == "Ursula Gomez"
    assert m.spherex_poc.email == "ursula@example.com"
    assert m.authors[2].name == "Stephanie Lowe"
    assert m.authors[2].email == "stephanie@example.com"
    assert m.authors[3].name == "Efren Archer"
    assert m.authors[3].email == "efren@example.com"
    assert m.approval is None
