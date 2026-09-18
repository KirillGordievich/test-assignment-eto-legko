"""Hardcoded demo dataset with realistic campaign metrics."""

from datetime import date

from chart_builder.models import ChartData, DataPoint


def get_demo_data() -> ChartData:
    """Return 5 data points of realistic campaign performance metrics."""
    return ChartData(
        title="Campaign Performance — Demo",
        points=[
            DataPoint(date=date(2026, 6, 10), cost=2.04, roi=610.78, cpa=0.68, conversions=3),
            DataPoint(date=date(2026, 6, 11), cost=25.85, roi=180.50, cpa=0.86, conversions=30),
            DataPoint(date=date(2026, 6, 12), cost=44.36, roi=161.47, cpa=1.23, conversions=36),
            DataPoint(date=date(2026, 6, 13), cost=55.65, roi=56.33, cpa=0.79, conversions=70),
            DataPoint(date=date(2026, 6, 14), cost=63.75, roi=357.25, cpa=0.71, conversions=90),
        ],
    )
