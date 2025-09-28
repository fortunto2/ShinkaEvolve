"""
SGR Schemas for Startup Agent Analysis.

These Pydantic models define structured outputs for startup strategy development:
- Market niche analysis
- Competitive intelligence
- Strategy development and evaluation
- PRD generation
"""

from __future__ import annotations
from typing import List, Optional, Literal, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field
from annotated_types import Ge, Le, MinLen, MaxLen


# === Market Analysis Schemas ===

class MarketOpportunity(BaseModel):
    """Specific market opportunity identified."""
    opportunity: str = Field(description="Description of the opportunity")
    market_size_usd: float = Field(ge=0, description="Estimated market size in USD")
    growth_rate: float = Field(ge=-1.0, le=5.0, description="Annual growth rate")
    difficulty: Literal["low", "medium", "high"] = Field(description="Market entry difficulty")
    evidence: str = Field(description="Supporting evidence from research")

class CustomerSegment(BaseModel):
    """Target customer segment analysis."""
    segment_name: str = Field(description="Name of customer segment")
    size_estimate: int = Field(ge=0, description="Estimated segment size")
    pain_points: List[str] = Field(description="Key pain points this segment faces")
    willingness_to_pay: Literal["low", "medium", "high"] = Field(description="Payment willingness")
    acquisition_channels: List[str] = Field(description="Best channels to reach this segment")

class NicheAnalysis(BaseModel):
    """Comprehensive market niche analysis."""
    market_segment: str = Field(description="Primary market segment description")
    market_size: MarketOpportunity = Field(description="Market size and opportunity")
    target_customers: List[CustomerSegment] = Field(description="Customer segments")
    key_trends: List[str] = Field(description="Important market trends")
    entry_barriers: List[str] = Field(description="Barriers to market entry")
    success_factors: List[str] = Field(description="Critical success factors")
    validation_signals: List[str] = Field(description="Market validation evidence")


# === Competitive Analysis Schemas ===

class Competitor(BaseModel):
    """Individual competitor analysis."""
    name: str = Field(description="Competitor name")
    category: Literal["direct", "indirect", "substitute"] = Field(description="Competition type")
    strengths: List[str] = Field(description="Competitor strengths")
    weaknesses: List[str] = Field(description="Competitor weaknesses")
    market_share: Optional[float] = Field(ge=0, le=1, description="Estimated market share")
    pricing_model: str = Field(description="How they monetize")
    differentiation: str = Field(description="What makes them unique")

class CompetitiveAdvantage(BaseModel):
    """Potential competitive advantage."""
    advantage: str = Field(description="Description of the advantage")
    sustainability: Literal["low", "medium", "high"] = Field(description="How sustainable")
    importance: Literal["low", "medium", "high"] = Field(description="Strategic importance")
    feasibility: Literal["low", "medium", "high"] = Field(description="Implementation feasibility")

class CompetitorProfile(BaseModel):
    """Complete competitive landscape analysis."""
    competitors: List[Competitor] = Field(description="List of competitors")
    market_gaps: List[str] = Field(description="Gaps in current market offerings")
    competitive_advantages: List[CompetitiveAdvantage] = Field(description="Potential advantages")
    positioning_opportunities: List[str] = Field(description="Market positioning opportunities")
    competitive_threats: List[str] = Field(description="Main competitive threats")


# === Strategy Development Schemas ===

class ValueProposition(BaseModel):
    """Core value proposition definition."""
    primary_benefit: str = Field(description="Main benefit delivered to customers")
    unique_differentiator: str = Field(description="What makes this unique")
    proof_points: List[str] = Field(description="Evidence supporting the value claim")

class MonetizationModel(BaseModel):
    """Revenue and monetization strategy."""
    model_type: Literal["subscription", "one_time", "freemium", "marketplace", "advertising"]
    pricing_strategy: str = Field(description="How pricing is determined")
    revenue_streams: List[str] = Field(description="Different ways to generate revenue")
    unit_economics: str = Field(description="Basic unit economics assumptions")

class GoToMarketStrategy(BaseModel):
    """Customer acquisition and growth strategy."""
    acquisition_channels: List[str] = Field(description="How to acquire customers")
    launch_strategy: str = Field(description="Product launch approach")
    growth_tactics: List[str] = Field(description="Strategies for scaling")
    partnership_opportunities: List[str] = Field(description="Potential partnerships")

class MarketStrategy(BaseModel):
    """Comprehensive market strategy."""
    approach: str = Field(description="High-level strategic approach")
    value_proposition: ValueProposition = Field(description="Core value proposition")
    target_customer: str = Field(description="Primary target customer")
    monetization: MonetizationModel = Field(description="How to make money")
    go_to_market: GoToMarketStrategy = Field(description="Customer acquisition strategy")
    key_milestones: List[str] = Field(description="Critical milestones for success")
    resource_requirements: List[str] = Field(description="Resources needed for execution")


# === Critical Evaluation Schemas ===

class StrengthWeakness(BaseModel):
    """Strength or weakness assessment."""
    aspect: str = Field(description="What aspect is being evaluated")
    description: str = Field(description="Detailed description")
    impact: Literal["low", "medium", "high"] = Field(description="Potential impact level")

class RiskAssessment(BaseModel):
    """Risk evaluation."""
    risk: str = Field(description="Description of the risk")
    probability: Literal["low", "medium", "high"] = Field(description="Likelihood of occurrence")
    impact: Literal["low", "medium", "high"] = Field(description="Impact if it occurs")
    mitigation: str = Field(description="How to mitigate this risk")

class CriticalEvaluation(BaseModel):
    """Critical evaluation of a strategy."""
    overall_score: float = Field(ge=0, le=1, description="Overall strategy score")
    strengths: List[StrengthWeakness] = Field(description="Strategy strengths")
    weaknesses: List[StrengthWeakness] = Field(description="Strategy weaknesses")
    market_fit_score: float = Field(ge=0, le=1, description="Product-market fit potential")
    execution_feasibility: float = Field(ge=0, le=1, description="How feasible to execute")
    competitive_position: float = Field(ge=0, le=1, description="Competitive positioning strength")
    risks: List[RiskAssessment] = Field(description="Key risks identified")
    recommendations: List[str] = Field(description="Recommendations for improvement")


# === PRD Generation Schemas ===

class ProductFeature(BaseModel):
    """Individual product feature specification."""
    name: str = Field(description="Feature name")
    description: str = Field(description="What the feature does")
    priority: Literal["must_have", "should_have", "nice_to_have"] = Field(description="Feature priority")
    acceptance_criteria: List[str] = Field(description="Criteria for feature completion")
    effort_estimate: Literal["small", "medium", "large"] = Field(description="Development effort")

class TechnicalRequirement(BaseModel):
    """Technical implementation requirement."""
    requirement: str = Field(description="Technical requirement description")
    category: Literal["performance", "security", "scalability", "integration"] = Field(description="Requirement type")
    specification: str = Field(description="Detailed specification")
    priority: Literal["high", "medium", "low"] = Field(description="Implementation priority")

class SuccessMetric(BaseModel):
    """Key performance indicator."""
    metric_name: str = Field(description="Name of the metric")
    description: str = Field(description="What this metric measures")
    target_value: str = Field(description="Target value to achieve")
    measurement_method: str = Field(description="How to measure this metric")
    timeframe: str = Field(description="When to measure/achieve this")

class MilestoneDefinition(BaseModel):
    """Development milestone."""
    milestone: str = Field(description="Milestone name")
    description: str = Field(description="What needs to be achieved")
    timeline: str = Field(description="Expected timeline")
    success_criteria: List[str] = Field(description="Criteria for milestone completion")
    dependencies: List[str] = Field(description="What this milestone depends on")

class StartupPRD(BaseModel):
    """Complete Product Requirements Document for startup."""
    product_name: str = Field(description="Product name")
    vision: str = Field(description="Product vision statement")
    target_market: str = Field(description="Primary target market")

    # Core product definition
    core_features: List[ProductFeature] = Field(description="Essential product features")
    technical_requirements: List[TechnicalRequirement] = Field(description="Technical specs")

    # Strategy and positioning
    value_proposition: str = Field(description="Core value proposition")
    competitive_differentiation: str = Field(description="How we differentiate from competitors")

    # Business model
    monetization_strategy: str = Field(description="How the product makes money")
    pricing_model: str = Field(description="Pricing structure")

    # Success measurement
    success_metrics: List[SuccessMetric] = Field(description="Key performance indicators")

    # Implementation
    development_milestones: List[MilestoneDefinition] = Field(description="Development roadmap")
    launch_strategy: str = Field(description="Product launch approach")

    # Risk management
    key_risks: List[str] = Field(description="Major risks and challenges")
    risk_mitigation: List[str] = Field(description="How to address key risks")


# === Evolution Tracking Schemas ===

class StrategyIteration(BaseModel):
    """Tracking of strategy evolution iterations."""
    iteration_number: int = Field(ge=1, description="Iteration number")
    strategies: List[MarketStrategy] = Field(description="Strategies in this iteration")
    evaluations: List[CriticalEvaluation] = Field(description="Strategy evaluations")
    best_strategy_index: int = Field(ge=0, description="Index of best strategy")
    improvement_areas: List[str] = Field(default=[], description="Areas for next iteration")


# === Web Research Integration ===

class ResearchSource(BaseModel):
    """Source of research information."""
    url: str = Field(description="Source URL")
    title: str = Field(description="Source title")
    relevance_score: float = Field(ge=0, le=1, description="How relevant to the research")
    key_insights: List[str] = Field(description="Key insights from this source")

class MarketResearch(BaseModel):
    """Market research results from web search."""
    query: str = Field(description="Research query used")
    market_insights: List[str] = Field(description="Key market insights found")
    trend_analysis: List[str] = Field(description="Trend analysis from research")
    competitive_intelligence: List[str] = Field(description="Competitive insights")
    sources: List[ResearchSource] = Field(description="Research sources")
    confidence: Literal["low", "medium", "high"] = Field(description="Confidence in research")