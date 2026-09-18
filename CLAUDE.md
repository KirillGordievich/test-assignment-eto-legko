# CLAUDE.md — Chart Builder

## Project Overview

Test assignment for the Python Developer position at Eto Legko.
Task spec is in `TASK.md` — always follow it as the source of truth.

## Tech Stack

- Python 3.13+, uv package manager
- Pydantic for data models
- Highcharts (JS) for chart rendering via self-contained HTML
- Plotly kept as alternative renderer (not the default)
- Linting: ruff, Type checking: mypy (strict mode)

## Key Commands

```bash
make install    # Install dependencies
make run        # Build chart and open in browser
make check      # Run lint + typecheck
make format     # Auto-format code
```

## Project Structure

```
src/chart_builder/
├── __main__.py       # Entry point, reads data.json or falls back to demo_data
├── models.py         # Pydantic models: DataPoint, ChartData, ChartConfig
├── series.py         # SeriesConfig model and default series configs
├── demo_data.py      # 5 hardcoded demo data points
├── js_renderer.py    # Highcharts HTML renderer (default)
├── chart.py          # Plotly renderer (alternative, not used by default)
├── renderer.py       # Plotly base renderer
└── templates/
    └── chart.html    # Highcharts HTML template with interactive JSON editor
data.json             # Input data file (project root)
TASK.md               # Original task specification
```

## Code Rules

### Follow the Task Spec
- Always check `TASK.md` before making changes to the chart
- The chart must have exactly 4 time-series: Cost (area), ROI (spline), CPA (bar), Conversions (line)
- Match the reference styling: pink background (#FFF0F3), no axes/labels/legend/grid

### Python Style
- Line length: 100 chars (configured in pyproject.toml)
- Use double quotes for strings
- Use type hints everywhere — mypy is strict
- Use `from __future__ import annotations` is NOT needed (Python 3.13+)
- Use `X | None` instead of `Optional[X]`
- Imports: stdlib → third-party → local, sorted by ruff

### Naming
- snake_case for functions, variables, modules
- PascalCase for classes
- Descriptive names: `series_config` not `sc`, `data_points` not `dp`
- Boolean variables/params: use `is_`, `has_`, `should_` prefixes

### Code Quality
- No dead code — delete unused functions/imports, don't comment them out
- No magic numbers — use named constants or config fields
- Keep functions short and single-purpose
- Prefer early returns over deep nesting
- Run `make check` before considering work done

### Data Flow
- Input: `data.json` in project root (or CLI arg) → fallback to `demo_data.py`
- Chart page also supports interactive JSON input via "Use your own data" button
- All data validated through Pydantic models

### HTML/JS (chart.html)
- Self-contained — all JS/CSS inline, Highcharts loaded from CDN
- User-facing error messages must be clear: `Invalid JSON at line X: message`
- No console.log left in production template
