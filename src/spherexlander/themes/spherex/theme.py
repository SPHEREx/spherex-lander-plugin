from __future__ import annotations

from pathlib import Path

from lander.ext.theme import ThemePlugin

__all__ = ["SpherexTheme"]


class SpherexTheme(ThemePlugin):
    """A theme plugin for SPHEREx PDF landing pages."""

    @property
    def name(self) -> str:
        """Name of this theme."""
        return "spherex"

    @property
    def base_theme_name(self) -> str:
        """Name of the theme this theme inherits from."""
        return "base"

    @property
    def site_dir(self) -> Path:
        """Site directory containing assets and stub files to render."""
        return Path(__file__).parent.joinpath("site")

    @property
    def templates_dir(self) -> Path:
        """Directory containing Jinja templates included by Jinja-templated
        files in the site.
        """
        return Path(__file__).parent.joinpath("templates")

    def run_post_build(self, output_dir: Path) -> None:
        pass
