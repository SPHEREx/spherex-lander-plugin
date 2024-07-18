"""Test for the spherex-project-management parser."""

from __future__ import annotations

from pathlib import Path

from lander.settings import BuildSettings

from spherexlander.parsers.projectmanagement import (
    SpherexProjectManagementParser,
)


def test_demo() -> None:
    """Test with the demo (tests/data/pm-document/SSDC-PM-001.tex)."""
    data_root = Path(__file__).parent / "data" / "pm-document"
    output_dir = Path("_build")

    settings = BuildSettings.load(
        source_path=data_root / "SSDC-PM-001.tex",
        pdf=data_root / "SSDC-PM-001.pdf",
        output_dir=output_dir,
        parser="spherex-project-management",
        theme="spherex",
    )

    parser = SpherexProjectManagementParser(settings=settings)
    m = parser.metadata

    assert m.title == "Example Title"
    assert m.version == "1.0"
    assert m.identifier == "SSDC-PM-001"
    assert m.document_handle_prefix == "SSDC-PM"
    assert len(m.authors) == 3
    assert len(m.other_authors) == 2
    assert m.ipac_lead is not None
    assert m.ipac_lead.name == "Example Lead"
    assert m.ipac_lead.email == "person@example.edu"
    assert m.spherex_poc is None
    assert m.authors[1].name == "Galileo Galilei"
    assert m.authors[1].email == "galileo@example.com"
    assert m.authors[2].name == "Isaac Newton"
    assert m.authors[2].email is None
    assert m.approval is not None
    assert m.approval.name == "Approver Name"
    assert m.approval.date == "2021-12-10"
