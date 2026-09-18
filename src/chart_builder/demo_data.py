"""Hardcoded demo dataset with realistic campaign metrics."""

from datetime import date

from chart_builder.models import ChartData, DataPoint


def get_demo_data() -> ChartData:
    """Return ~15 data points of realistic campaign performance metrics."""
    return ChartData(
        title="Campaign Performance — Demo",
        points=[
            DataPoint(date=date(2026, 6, 1), cost=25.0, roi=180.0, cpa=1.2, conversions=21),
            DataPoint(date=date(2026, 6, 2), cost=32.0, roi=155.0, cpa=1.5, conversions=22),
            DataPoint(date=date(2026, 6, 3), cost=28.0, roi=110.0, cpa=1.1, conversions=25),
            DataPoint(date=date(2026, 6, 4), cost=45.0, roi=70.0, cpa=1.8, conversions=18),
            DataPoint(date=date(2026, 6, 5), cost=52.0, roi=45.0, cpa=2.1, conversions=15),
            DataPoint(date=date(2026, 6, 6), cost=58.0, roi=30.0, cpa=1.9, conversions=14),
            DataPoint(date=date(2026, 6, 7), cost=60.0, roi=25.0, cpa=2.0, conversions=16),
            DataPoint(date=date(2026, 6, 8), cost=55.0, roi=35.0, cpa=1.8, conversions=20),
            DataPoint(date=date(2026, 6, 9), cost=48.0, roi=50.0, cpa=1.6, conversions=24),
            DataPoint(date=date(2026, 6, 10), cost=65.0, roi=60.0, cpa=2.2, conversions=28),
            DataPoint(date=date(2026, 6, 11), cost=72.0, roi=90.0, cpa=2.4, conversions=30),
            DataPoint(date=date(2026, 6, 12), cost=44.0, roi=120.0, cpa=1.2, conversions=36),
            DataPoint(date=date(2026, 6, 13), cost=42.0, roi=145.0, cpa=1.4, conversions=33),
            DataPoint(date=date(2026, 6, 14), cost=35.0, roi=161.0, cpa=1.0, conversions=35),
            DataPoint(date=date(2026, 6, 15), cost=50.0, roi=175.0, cpa=1.7, conversions=29),
        ],
    )
