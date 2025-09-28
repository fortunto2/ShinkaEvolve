"""
Minimal schemas for reliable JSON generation without truncation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class MinimalMarketData(BaseModel):
    """Minimal market data."""
    market_size_usd: int = Field(ge=0, description="Market size in USD")
    growth_rate: float = Field(ge=0, le=2, description="Annual growth rate")
    customer_acquisition_cost: float = Field(ge=0, description="CAC in USD")
    lifetime_value: float = Field(ge=0, description="LTV in USD")

class MinimalSEOOpportunity(BaseModel):
    """Minimal SEO opportunity."""
    keyword: str = Field(description="Target keyword")
    monthly_searches: int = Field(ge=0, description="Monthly search volume")
    difficulty: int = Field(ge=0, le=100, description="SEO difficulty 0-100")
    seasonal_boost: float = Field(ge=1, le=20, description="Christmas multiplier")

class MinimalCompetitor(BaseModel):
    """Minimal competitor data."""
    name: str = Field(description="Competitor name")
    estimated_revenue: int = Field(ge=0, description="Estimated revenue USD")
    market_share: float = Field(ge=0, le=100, description="Market share %")

class MinimalFinancialProjection(BaseModel):
    """Minimal financial projection."""
    month: int = Field(ge=1, le=24, description="Month number")
    revenue: int = Field(ge=0, description="Projected revenue USD")
    costs: int = Field(ge=0, description="Projected costs USD")

class MinimalStartupAnalysis(BaseModel):
    """Minimal startup analysis - designed to avoid JSON truncation."""
    product_name: str = Field(description="Product name")
    elevator_pitch: str = Field(description="Brief elevator pitch")

    # Simplified data structures
    market_data: MinimalMarketData = Field(description="Market data")
    seo_opportunities: List[MinimalSEOOpportunity] = Field(description="SEO keywords", max_length=3)
    competitors: List[MinimalCompetitor] = Field(description="Main competitors", max_length=2)

    # Essential features and projections
    core_features: List[str] = Field(description="Core features", max_length=5)
    financial_projections: List[MinimalFinancialProjection] = Field(description="Financial projections", max_length=4)

    # Simple strings instead of complex structures
    unique_value_proposition: str = Field(description="Value proposition")
    pricing_model: str = Field(description="Pricing model")
    seo_strategy: str = Field(description="SEO strategy")

    # Basic metrics
    funding_requirements: int = Field(ge=0, description="Funding needed USD")
    break_even_month: int = Field(ge=1, le=24, description="Break even month")

    # Simple lists
    key_risks: List[str] = Field(description="Key risks", max_length=3)
    kpi_targets: List[str] = Field(description="KPI targets", max_length=3)
    competitive_advantages: List[str] = Field(description="Competitive advantages", max_length=3)