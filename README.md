# Chart Builder

Test assignment for the Python Developer (AD Robot) position at Eto Legko.

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

Two ways to provide your own data:

**1. JSON file** — edit `data.json` in the project root and run `make run`:

```json
[
  { "date": "2026-06-10", "cost": 2.04, "roi": 610.78, "cpa": 0.68, "conversions": 3 },
  { "date": "2026-06-11", "cost": 25.85, "roi": 180.50, "cpa": 0.86, "conversions": 30 }
]
```

**2. On the page** — the generated HTML has a data table at the bottom where you can add, edit, and remove rows, then click "Update chart".
