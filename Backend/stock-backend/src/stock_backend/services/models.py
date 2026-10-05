from typing import Literal

from pydantic import BaseModel, Field


class StockAnalysis(BaseModel):
    analysis: str = Field(description="Short stock analysis")
    price: float = Field(description="Current stock price")
    recommendation: str = Field(description="BUY, HOLD, or SELL")
    risk: str = Field(description="LOW, MEDIUM, HIGH")


class Recommendation(BaseModel):
    recommendation: Literal["BUY", "HOLD", "SELL"]


class Risk(BaseModel):
    risk: Literal["LOW", "MEDIUM", "HIGH"]


class Summary(BaseModel):
    summary: str
