"""Chart builder: constructs a Plotly figure from data and series configs."""

from typing import Any

import plotly.graph_objects as go

from chart_builder.models import ChartConfig, ChartData
from chart_builder.series import SeriesConfig, SeriesType


class ChartBuilder:
    """Builds an interactive multi-axis Plotly figure.

    Each series gets its own Y-axis for independent scaling.
    Only axes with ``visible_axis=True`` show labels/ticks.
    """

    def __init__(
        self,
        data: ChartData,
        series_configs: list[SeriesConfig],
        config: ChartConfig | None = None,
    ) -> None:
        self._data = data
        self._series_configs = series_configs
        self._config = config or ChartConfig()
        self._series_data_map: dict[str, list[float | int]] = {
            "Cost ($)": [float(v) for v in data.costs],
            "ROI confirmed (%)": [float(v) for v in data.rois],
            "CPA ($)": [float(v) for v in data.cpas],
            "Conversions": list(data.conversions_values),
        }

    def build(self) -> go.Figure:
        """Construct and return the complete Plotly figure."""
        fig = go.Figure()
        date_strings = self._format_dates()

        # Render bars first so they stay behind lines/areas.
        bar_indices = [
            i for i, c in enumerate(self._series_configs) if c.series_type == SeriesType.BAR
        ]
        other_indices = [
            i for i, c in enumerate(self._series_configs) if c.series_type != SeriesType.BAR
        ]

        for i in bar_indices + other_indices:
            cfg = self._series_configs[i]
            y_values = self._series_data_map[cfg.name]
            yaxis_key = self._yaxis_ref(i)
            trace = self._create_trace(cfg, date_strings, y_values, yaxis_key)
            fig.add_trace(trace)

        layout = self._build_layout(date_strings)
        fig.update_layout(**layout)
        return fig

    def _format_dates(self) -> list[str]:
        return [d.strftime(self._config.date_format) for d in self._data.dates]

    @staticmethod
    def _yaxis_ref(index: int) -> str:
        return "y" if index == 0 else f"y{index + 1}"

    def _create_trace(
        self,
        cfg: SeriesConfig,
        x: list[str],
        y: list[float | int],
        yaxis: str,
    ) -> go.Scatter | go.Bar:
        builders: dict[SeriesType, Any] = {
            SeriesType.AREA: self._build_area_trace,
            SeriesType.SPLINE: self._build_spline_trace,
            SeriesType.LINE: self._build_line_trace,
            SeriesType.BAR: self._build_bar_trace,
        }
        return builders[cfg.series_type](cfg, x, y, yaxis)

    @staticmethod
    def _build_area_trace(
        cfg: SeriesConfig, x: list[str], y: list[float | int], yaxis: str
    ) -> go.Scatter:
        return go.Scatter(
            x=x,
            y=y,
            name=cfg.name,
            mode="lines",
            fill="tozeroy",
            fillcolor=cfg.fill_color,
            line={"color": cfg.color, "width": cfg.line_width},
            yaxis=yaxis,
            hovertemplate=f"{cfg.hover_format}<extra></extra>",
        )

    @staticmethod
    def _build_spline_trace(
        cfg: SeriesConfig, x: list[str], y: list[float | int], yaxis: str
    ) -> go.Scatter:
        return go.Scatter(
            x=x,
            y=y,
            name=cfg.name,
            mode="lines",
            line={
                "color": cfg.color,
                "width": cfg.line_width,
                "shape": "spline",
                "smoothing": 1.3,
            },
            yaxis=yaxis,
            hovertemplate=f"{cfg.hover_format}<extra></extra>",
        )

    @staticmethod
    def _build_line_trace(
        cfg: SeriesConfig, x: list[str], y: list[float | int], yaxis: str
    ) -> go.Scatter:
        marker: dict[str, Any] = {"size": cfg.marker_size, "color": cfg.color}
        if cfg.marker_symbol:
            marker["symbol"] = cfg.marker_symbol

        return go.Scatter(
            x=x,
            y=y,
            name=cfg.name,
            mode="lines+markers",
            line={"color": cfg.color, "width": cfg.line_width},
            marker=marker,
            yaxis=yaxis,
            hovertemplate=f"{cfg.hover_format}<extra></extra>",
        )

    @staticmethod
    def _build_bar_trace(
        cfg: SeriesConfig, x: list[str], y: list[float | int], yaxis: str
    ) -> go.Bar:
        return go.Bar(
            x=x,
            y=y,
            name=cfg.name,
            marker={"color": cfg.color, "opacity": 0.7},
            width=0.5,
            yaxis=yaxis,
            hovertemplate=f"{cfg.hover_format}<extra></extra>",
        )

    def _build_layout(self, date_strings: list[str]) -> dict[str, Any]:
        """Build layout with pink background, clean axes, and proper layering."""
        layout: dict[str, Any] = {
            "title": {"text": self._data.title, "x": 0.5},
            "width": self._config.width,
            "height": self._config.height,
            "hovermode": "x unified",
            "plot_bgcolor": "#FFF0F3",
            "paper_bgcolor": "#FFFFFF",
            "barmode": "overlay",
            "legend": {
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "center",
                "x": 0.5,
                "itemclick": "toggle",
                "itemdoubleclick": "toggleothers",
            },
            "xaxis": {
                "domain": [0.05, 0.95],
                "showgrid": True,
                "gridcolor": "rgba(220, 180, 190, 0.4)",
                "showline": True,
                "linecolor": "rgba(180, 140, 150, 0.6)",
                "tickangle": -45,
                "categoryorder": "array",
                "categoryarray": date_strings,
            },
        }

        for i, series_cfg in enumerate(self._series_configs):
            axis_key = "yaxis" if i == 0 else f"yaxis{i + 1}"
            layout[axis_key] = self._build_yaxis(series_cfg, is_primary=(i == 0))

        return layout

    @staticmethod
    def _build_yaxis(cfg: SeriesConfig, *, is_primary: bool) -> dict[str, Any]:
        """Build a single Y-axis configuration."""
        axis: dict[str, Any] = {
            "side": cfg.axis_side,
        }

        if cfg.visible_axis:
            axis["title"] = {"text": cfg.y_axis_label, "font": {"color": cfg.color}}
            axis["tickfont"] = {"color": cfg.color}
            axis["showticklabels"] = True
            axis["showline"] = True
            axis["linecolor"] = cfg.color
            if cfg.tick_prefix:
                axis["tickprefix"] = cfg.tick_prefix
            if cfg.tick_suffix:
                axis["ticksuffix"] = cfg.tick_suffix
        else:
            axis["title"] = None
            axis["showticklabels"] = False
            axis["showline"] = False

        if is_primary:
            axis["showgrid"] = True
            axis["gridcolor"] = "rgba(220, 180, 190, 0.3)"
        else:
            axis["overlaying"] = "y"
            axis["showgrid"] = False

        return axis
