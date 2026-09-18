"""Highcharts-based renderer: generates a self-contained HTML file."""

from __future__ import annotations

import json
import webbrowser
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from chart_builder.models import ChartConfig, ChartData
from chart_builder.series import AxisSide, SeriesConfig, SeriesType


def _highcharts_type(series_type: SeriesType) -> str:
    """Map internal SeriesType to Highcharts chart type name."""
    return "column" if series_type == SeriesType.BAR else series_type.value


@lru_cache(maxsize=1)
def _load_template() -> str:
    template_file = files("chart_builder").joinpath("templates/chart.html")
    return template_file.read_text(encoding="utf-8")


class JsChartRenderer:
    """Renders chart data into a Highcharts-powered HTML file."""

    def __init__(self, config: ChartConfig | None = None) -> None:
        self._config = config or ChartConfig()

    def render(
        self,
        data: ChartData,
        series_configs: list[SeriesConfig],
        output_path: Path | None = None,
    ) -> Path:
        """Build HTML with embedded Highcharts config and write to file."""
        html = self._render_to_string(data, series_configs)

        if output_path is not None:
            output_path.write_text(html, encoding="utf-8")
            return output_path

        with NamedTemporaryFile(
            mode="w",
            suffix=".html",
            delete=False,
            prefix="chart_",
            encoding="utf-8",
        ) as f:
            f.write(html)
            return Path(f.name)

    def _render_to_string(
        self, data: ChartData, series_configs: list[SeriesConfig]
    ) -> str:
        """Build the complete HTML string without writing to disk."""
        template = _load_template()
        chart_json = self._build_chart_json(data, series_configs)
        chart_config = self._build_chart_config(series_configs)

        html = template.replace("{{ TITLE }}", data.title)
        html = html.replace("{{ DATA_JSON }}", json.dumps(chart_json, indent=2))
        html = html.replace("{{ CHART_CONFIG }}", json.dumps(chart_config, indent=2))
        return html

    @staticmethod
    def open_in_browser(path: Path) -> None:
        """Open an HTML file in the default browser."""
        webbrowser.open(path.as_uri())

    @staticmethod
    def _build_chart_json(
        data: ChartData, series_configs: list[SeriesConfig]
    ) -> dict[str, Any]:
        """Convert ChartData + SeriesConfig list into Highcharts-compatible JSON."""
        dates = [d.isoformat() for d in data.dates]

        y_axes: list[dict[str, Any]] = []
        series_list: list[dict[str, Any]] = []

        for i, cfg in enumerate(series_configs):
            y_axes.append(JsChartRenderer._build_yaxis(cfg))

            yaxis_idx = cfg.shared_yaxis if cfg.shared_yaxis is not None else i
            values = [getattr(p, cfg.field_name) for p in data.points]

            series_entry: dict[str, Any] = {
                "name": cfg.name,
                "type": _highcharts_type(cfg.series_type),
                "data": values,
                "yAxis": yaxis_idx,
                "color": cfg.color,
                "zIndex": 0 if cfg.series_type == SeriesType.BAR else 1,
            }

            if cfg.series_type == SeriesType.AREA and cfg.fill_color:
                series_entry["fillColor"] = cfg.fill_color

            if cfg.tick_prefix:
                series_entry["tooltip"] = {"valuePrefix": cfg.tick_prefix}
            elif cfg.tick_suffix:
                series_entry["tooltip"] = {"valueSuffix": cfg.tick_suffix}

            series_list.append(series_entry)

        return {
            "title": data.title,
            "dates": dates,
            "yAxes": y_axes,
            "series": series_list,
        }

    @staticmethod
    def _build_chart_config(series_configs: list[SeriesConfig]) -> dict[str, Any]:
        """Build config passed to JS for dynamic chart rebuilds."""
        series_info = [
            {"color": cfg.color, "fillColor": cfg.fill_color} for cfg in series_configs
        ]
        y_axes = [JsChartRenderer._build_yaxis(cfg) for cfg in series_configs]
        return {"series": series_info, "yAxes": y_axes}

    @staticmethod
    def _build_yaxis(cfg: SeriesConfig) -> dict[str, Any]:
        """Build a single Highcharts yAxis config."""
        axis: dict[str, Any] = {
            "opposite": cfg.axis_side == AxisSide.RIGHT,
            "title": {"text": None},
            "labels": {"enabled": False},
            "lineWidth": 0,
            "gridLineWidth": 0,
        }

        if not cfg.visible_axis:
            axis["min"] = 0

        return axis
