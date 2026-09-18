"""Entry point: ``uv run python -m chart_builder``."""

from chart_builder.chart import ChartBuilder
from chart_builder.demo_data import get_demo_data
from chart_builder.renderer import ChartRenderer
from chart_builder.series import get_default_series_configs


def main() -> None:
    # Replace get_demo_data() with your own ChartData to use custom data.
    # See README.md for a full example.
    data = get_demo_data()
    series_configs = get_default_series_configs()

    builder = ChartBuilder(data, series_configs)
    fig = builder.build()

    renderer = ChartRenderer()
    path = renderer.render_to_html(fig)
    print(f"Chart saved to: {path}")
    renderer.open_in_browser(path)


if __name__ == "__main__":
    main()
