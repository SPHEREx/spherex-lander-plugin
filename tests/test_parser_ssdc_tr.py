"""Test for the SSDC-TR parser."""

from __future__ import annotations

from pathlib import Path

from lander.settings import BuildSettings

from spherexlander.parsers.ssdctr import DoorsID, SpherexSsdcTrParser


def test_tr_req() -> None:
    """Test with the req demo (tests/data/ssdc-tr-req/SSDC-TR-000.tex)."""
    data_root = Path(__file__).parent / "data" / "ssdc-tr-req"
    output_dir = Path("_build")

    settings = BuildSettings.load(
        source_path=data_root / "SSDC-TR-000.tex",
        pdf=data_root / "SSDC-TR-000.pdf",
        output_dir=output_dir,
        parser="spherex-ssdc-tr",
        theme="spherex",
    )

    parser = SpherexSsdcTrParser(settings=settings)
    m = parser.metadata

    assert m.title == "Requirements Title"
    assert m.version == "1.0"
    assert m.identifier == "SSDC-TR-000"
    assert m.document_handle_prefix == "SSDC-TR"
    assert len(m.authors) == 1
    assert len(m.other_authors) == 0
    assert m.ipac_lead is not None
    assert m.ipac_lead.name == "Galileo Galilei"
    assert m.ipac_lead.email == "galileo@example.com"
    assert m.approval is not None
    assert m.approval.name == "Edwin Hubble"
    assert m.approval.date == "2021-01-01"
    assert m.ipac_jira_id == "SVV-999"
    assert m.req_doors_id == DoorsID(
        id="12345", url="https://example.org/12345"
    )
    assert m.va_doors_id is None


def test_tr_va() -> None:
    """Test with the va demo (tests/data/ssdc-tr-va/SSDC-TR-000.tex)."""
    data_root = Path(__file__).parent / "data" / "ssdc-tr-va"
    output_dir = Path("_build")

    settings = BuildSettings.load(
        source_path=data_root / "SSDC-TR-000.tex",
        pdf=data_root / "SSDC-TR-000.pdf",
        output_dir=output_dir,
        parser="spherex-ssdc-tr",
        theme="spherex",
    )

    parser = SpherexSsdcTrParser(settings=settings)
    m = parser.metadata

    assert m.title == "Verification Activity Title"
    assert m.version == "1.0"
    assert m.identifier == "SSDC-TR-000"
    assert m.document_handle_prefix == "SSDC-TR"
    assert len(m.authors) == 1
    assert len(m.other_authors) == 0
    assert m.ipac_lead is not None
    assert m.ipac_lead.name == "Galileo Galilei"
    assert m.ipac_lead.email == "galileo@example.com"
    assert m.approval is not None
    assert m.approval.name == "Edwin Hubble"
    assert m.approval.date == "2021-01-01"
    assert m.ipac_jira_id == "SVV-999"
    assert m.va_doors_id == DoorsID(
        id="12345", url="https://example.org/12345"
    )
    assert m.req_doors_id is None
