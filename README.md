# Chart Builder

Interactive multi-axis time-series chart generator. Builds a self-contained HTML chart with 4 series types (area, spline, line, bar) and opens it in the browser.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Quick Start

```bash
make install   # install dependencies
make run       # build chart and open in browser
```

Or without Make:

```bash
uv sync
uv run python -m chart_builder
```

The chart opens in your default browser automatically. The generated HTML file is fully self-contained.

## Custom Data

The chart accepts exactly **4 time-series**: Cost, ROI, CPA, and Conversions. To use your own data, create a `ChartData` object with your `DataPoint` list — each point contains all 4 values for a given date:

```python
from datetime import date

from chart_builder.chart import ChartBuilder
from chart_builder.models import ChartData, DataPoint
from chart_builder.renderer import ChartRenderer
from chart_builder.series import get_default_series_configs

data = ChartData(
    title="My Campaign",
    points=[
        DataPoint(date=date(2026, 7, 1), cost=30.0, roi=120.0, cpa=1.5, conversions=25),
        DataPoint(date=date(2026, 7, 2), cost=45.0, roi=140.0, cpa=1.8, conversions=30),
        DataPoint(date=date(2026, 7, 3), cost=28.0, roi=110.0, cpa=1.1, conversions=22),
        # ... add as many data points as needed
    ],
)

fig = ChartBuilder(data, get_default_series_configs()).build()

renderer = ChartRenderer()
path = renderer.render_to_html(fig)
renderer.open_in_browser(path)
```

Alternatively, edit `src/chart_builder/demo_data.py` directly and run `make run`.

### Data Fields

| Field         | Type    | Description                       |
|---------------|---------|-----------------------------------|
| `date`        | `date`  | Day of the data point             |
| `cost`        | `float` | Cost in USD (>= 0)               |
| `roi`         | `float` | ROI confirmed, % (e.g. 150.0)    |
| `cpa`         | `float` | Cost per acquisition in USD (>= 0)|
| `conversions` | `int`   | Number of conversions (>= 0)     |

## Custom Styles

Pass custom `SeriesConfig` list to `ChartBuilder` to change colors, line widths, marker styles, and axis labels. See `src/chart_builder/series.py` for the configuration model.

## Development

```bash
make lint       # run ruff linter
make format     # run ruff formatter
make typecheck  # run mypy
make check      # run all checks
```

## Project Structure

```
src/chart_builder/
├── __init__.py     # package init
├── __main__.py     # entry point
├── chart.py        # ChartBuilder — assembles Plotly figure
├── demo_data.py    # sample dataset
├── models.py       # Pydantic data models
├── renderer.py     # HTML rendering and browser opening
└── series.py       # series style configuration
```
