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

The chart opens in your default browser automatically.

## Custom Data

To use your own data, edit `src/chart_builder/demo_data.py` — each `DataPoint` contains 4 values for a given date:

- `cost` — Cost in USD
- `roi` — ROI confirmed, %
- `cpa` — Cost per acquisition in USD
- `conversions` — Number of conversions

Then run `make run`.
