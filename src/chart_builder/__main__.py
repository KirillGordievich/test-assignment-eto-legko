"""Entry point for chart_builder."""

import json
import sys
from pathlib import Path

from chart_builder.demo_data import get_demo_data
from chart_builder.js_renderer import JsChartRenderer
from chart_builder.models import ChartData
from chart_builder.series import get_default_series_configs


def _load_from_json(path: Path) -> ChartData:
    """Load chart data from a JSON file."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    return ChartData(points=raw)


def main() -> None:
    json_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data.json")

    try:
        data = _load_from_json(json_path)
    except FileNotFoundError:
        data = get_demo_data()

    renderer = JsChartRenderer()
    path = renderer.render(data, get_default_series_configs())
    print(f"Chart saved to: {path}")
    renderer.open_in_browser(path)


if __name__ == "__main__":
    main()
