"""Highcharts-based renderer: generates a self-contained HTML file."""

from __future__ import annotations

import json
import webbrowser
from importlib.resources import files
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from chart_builder.models import ChartConfig, ChartData
from chart_builder.series import SeriesConfig, SeriesType

_SERIES_TYPE_MAP: dict[SeriesType, str] = {
    SeriesType.AREA: "area",
    SeriesType.SPLINE: "spline",
    SeriesType.LINE: "line",
    SeriesType.BAR: "column",
}


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
        template = self._load_template()
        chart_json = self._build_chart_json(data, series_configs)

        html = template.replace("{{ TITLE }}", data.title)
        html = html.replace("{{ DATA_JSON }}", json.dumps(chart_json, indent=2))

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

    @staticmethod
    def open_in_browser(path: Path) -> None:
        """Open an HTML file in the default browser."""
        webbrowser.open(path.as_uri())

    @staticmethod
    def _load_template() -> str:
        template_file = files("chart_builder").joinpath("templates/chart.html")
        return template_file.read_text(encoding="utf-8")

    def _build_chart_json(
        self, data: ChartData, series_configs: list[SeriesConfig]
    ) -> dict[str, Any]:
        """Convert ChartData + SeriesConfig list into Highcharts-compatible JSON."""
        dates = [d.strftime(self._config.date_format) for d in data.dates]

        data_map: dict[str, list[float | int]] = {
            "Cost ($)": [float(v) for v in data.costs],
            "ROI confirmed (%)": [float(v) for v in data.rois],
            "CPA ($)": [float(v) for v in data.cpas],
            "Conversions": list(data.conversions_values),
        }

        y_axes: list[dict[str, Any]] = []
        series_list: list[dict[str, Any]] = []

        for i, cfg in enumerate(series_configs):
            y_axes.append(self._build_yaxis(cfg, is_first=(i == 0)))

            yaxis_idx = cfg.shared_yaxis if cfg.shared_yaxis is not None else i

            series_entry: dict[str, Any] = {
                "name": cfg.name,
                "type": _SERIES_TYPE_MAP[cfg.series_type],
                "data": data_map[cfg.name],
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
    def _build_yaxis(cfg: SeriesConfig, *, is_first: bool) -> dict[str, Any]:
        """Build a single Highcharts yAxis config."""
        opposite = cfg.axis_side == "right"

        axis: dict[str, Any] = {
            "opposite": opposite,
            "title": {"text": None},
            "labels": {"enabled": False},
            "lineWidth": 0,
            "gridLineWidth": 0,
        }

        if not cfg.visible_axis:
            axis["min"] = 0

        return axis
