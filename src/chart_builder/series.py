"""Series configuration: visual style and axis mapping for each chart series."""

from enum import StrEnum

from pydantic import BaseModel


class SeriesType(StrEnum):
    """Supported chart trace types."""

    AREA = "area"
    SPLINE = "spline"
    LINE = "line"
    BAR = "bar"


class SeriesConfig(BaseModel):
    """Visual configuration for a single chart series."""

    name: str
    series_type: SeriesType
    color: str
    fill_color: str | None = None
    line_width: int = 2
    marker_symbol: str | None = None
    marker_size: int = 7
    y_axis_label: str
    tick_prefix: str = ""
    tick_suffix: str = ""
    hover_format: str = "%{y}"
    visible_axis: bool = True
    axis_side: str = "left"
    shared_yaxis: int | None = None


def get_default_series_configs() -> list[SeriesConfig]:
    """Return the 4 default series matching the reference screenshot."""
    return [
        SeriesConfig(
            name="Cost ($)",
            series_type=SeriesType.AREA,
            color="rgba(255, 193, 7, 0.9)",
            fill_color="rgba(255, 193, 7, 0.3)",
            line_width=2,
            y_axis_label="Cost ($)",
            tick_prefix="$",
            hover_format="Cost: $%{y:.2f}",
        ),
        SeriesConfig(
            name="ROI confirmed (%)",
            series_type=SeriesType.SPLINE,
            color="#1B5E20",
            line_width=3,
            y_axis_label="ROI (%)",
            tick_suffix="%",
            hover_format="ROI: %{y:.1f}%%",
            axis_side="right",
        ),
        SeriesConfig(
            name="CPA ($)",
            series_type=SeriesType.BAR,
            color="#1976D2",
            line_width=0,
            y_axis_label="CPA ($)",
            tick_prefix="$",
            hover_format="CPA: $%{y:.2f}",
            visible_axis=False,
            shared_yaxis=0,
        ),
        SeriesConfig(
            name="Conversions",
            series_type=SeriesType.LINE,
            color="#9C27B0",
            line_width=2,
            marker_symbol="square",
            marker_size=5,
            y_axis_label="Conversions",
            hover_format="Conversions: %{y}",
            visible_axis=False,
        ),
    ]
