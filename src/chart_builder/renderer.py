"""Chart renderer: saves Plotly figure to HTML and opens in browser."""

import webbrowser
from pathlib import Path
from tempfile import NamedTemporaryFile

import plotly.graph_objects as go


class ChartRenderer:
    """Handles rendering a Plotly figure to HTML and displaying it."""

    def render_to_html(self, fig: go.Figure, output_path: Path | None = None) -> Path:
        """Save the figure as a self-contained HTML file.

        If output_path is None, a temporary file is created.
        Returns the path to the written file.
        """
        if output_path is not None:
            fig.write_html(str(output_path), include_plotlyjs=True, full_html=True)
            return output_path

        with NamedTemporaryFile(
            mode="w",
            suffix=".html",
            delete=False,
            prefix="chart_",
        ) as f:
            fig.write_html(f, include_plotlyjs=True, full_html=True)
            return Path(f.name)

    @staticmethod
    def open_in_browser(path: Path) -> None:
        """Open an HTML file in the default browser."""
        webbrowser.open(path.as_uri())
