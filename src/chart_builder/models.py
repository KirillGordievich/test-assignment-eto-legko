"""Data models for the chart builder."""

from datetime import date

from pydantic import BaseModel, Field


class DataPoint(BaseModel):
    """A single day's metrics across all series."""

    date: date
    cost: float = Field(ge=0, description="Cost in USD")
    roi: float = Field(description="ROI confirmed, percent value (e.g. 150.0 means 150%)")
    cpa: float = Field(ge=0, description="Cost per acquisition in USD")
    conversions: int = Field(ge=0, description="Number of conversions")


class ChartData(BaseModel):
    """Complete dataset for the chart."""

    title: str = "Campaign Performance"
    points: list[DataPoint] = Field(min_length=1)

    @property
    def dates(self) -> list[date]:
        return [p.date for p in self.points]


class ChartConfig(BaseModel):
    """Visual and dimensional configuration for the chart."""

    width: int = 1200
    height: int = 600
