"""Series configuration: visual style and axis mapping for each chart series."""

from enum import StrEnum

from pydantic import BaseModel


class SeriesType(StrEnum):
    """Supported chart trace types."""

    AREA = "area"
    SPLINE = "spline"
    LINE = "line"
    BAR = "bar"


class AxisSide(StrEnum):
    """Y-axis position on the chart."""

    LEFT = "left"
    RIGHT = "right"


class SeriesConfig(BaseModel):
    """Visual configuration for a single chart series."""

    name: str
    field_name: str
    series_type: SeriesType
    color: str
    fill_color: str | None = None
    line_width: int = 2
    marker_symbol: str | None = None
    marker_size: int = 7
    tick_prefix: str = ""
    tick_suffix: str = ""
    visible_axis: bool = True
    axis_side: AxisSide = AxisSide.LEFT
    shared_yaxis: int | None = None


def get_default_series_configs() -> list[SeriesConfig]:
    """Return the 4 default series matching the reference screenshot."""
    return [
        SeriesConfig(
            name="Cost ($)",
            field_name="cost",
            series_type=SeriesType.AREA,
            color="rgba(255, 193, 7, 0.9)",
            fill_color="rgba(255, 193, 7, 0.3)",
            line_width=2,
            tick_prefix="$",
        ),
        SeriesConfig(
            name="ROI confirmed (%)",
            field_name="roi",
            series_type=SeriesType.SPLINE,
            color="#1B5E20",
            line_width=3,
            tick_suffix="%",
            axis_side=AxisSide.RIGHT,
        ),
        SeriesConfig(
            name="CPA ($)",
            field_name="cpa",
            series_type=SeriesType.BAR,
            color="#1976D2",
            line_width=0,
            tick_prefix="$",
            visible_axis=False,
            shared_yaxis=0,
        ),
        SeriesConfig(
            name="Conversions",
            field_name="conversions",
            series_type=SeriesType.LINE,
            color="#9C27B0",
            line_width=2,
            marker_symbol="square",
            marker_size=5,
            visible_axis=False,
        ),
    ]
