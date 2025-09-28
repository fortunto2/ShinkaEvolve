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

# EVOLVE-BLOCK-START: market_schemas
class MarketOpportunity(BaseModel):
    """Specific market opportunity identified."""
    opportunity: str = Field(description="Description of the opportunity")
    market_size_usd: float = Field(ge=0, description="Estimated market size in USD")
    growth_rate: float = Field(ge=-1.0, le=5.0, description="Annual growth rate")
    difficulty: Literal["low", "medium", "high"] = Field(description="Market entry difficulty")
    evidence: str = Field(description="Supporting evidence from research")
    # Fields that can be evolved: risk_score, competitive_density, seasonality, etc.
# EVOLVE-BLOCK-END: market_schemas

# EVOLVE-BLOCK-START: customer_schemas
class CustomerSegment(BaseModel):
    """Target customer segment analysis."""
    segment_name: str = Field(description="Name of customer segment")
    size_estimate: int = Field(ge=0, description="Estimated segment size")
    pain_points: List[str] = Field(description="Key pain points this segment faces")
    willingness_to_pay: Literal["low", "medium", "high"] = Field(description="Payment willingness")
    acquisition_channels: List[str] = Field(description="Best channels to reach this segment")
    # Evolvable fields: demographics, psychographics, behavior_patterns, conversion_funnel, etc.
# EVOLVE-BLOCK-END: customer_schemas

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

# EVOLVE-BLOCK-START: value_proposition_schema
class ValueProposition(BaseModel):
    """Core value proposition definition."""
    primary_benefit: str = Field(description="Main benefit delivered to customers")
    unique_differentiator: str = Field(description="What makes this unique")
    proof_points: List[str] = Field(description="Evidence supporting the value claim")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # target_audience: Optional[str] = Field(description="Specific target audience segment")
    # emotional_trigger: Optional[str] = Field(description="Primary emotional motivator")
    # urgency_factor: Optional[str] = Field(description="What creates urgency to buy")
    # risk_mitigation: Optional[List[str]] = Field(description="How we reduce customer risk")
# EVOLVE-BLOCK-END: value_proposition_schema

# EVOLVE-BLOCK-START: monetization_schema
class MonetizationModel(BaseModel):
    """Revenue and monetization strategy."""
    model_type: Literal["subscription", "one_time", "freemium", "marketplace", "advertising"]
    pricing_strategy: str = Field(description="How pricing is determined")
    revenue_streams: List[str] = Field(description="Different ways to generate revenue")
    unit_economics: str = Field(description="Basic unit economics assumptions")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # price_elasticity: Optional[float] = Field(ge=0, le=2, description="Price sensitivity factor")
    # seasonal_pricing: Optional[bool] = Field(description="Whether to use seasonal pricing")
    # competitor_pricing_gap: Optional[float] = Field(description="Pricing vs average competitor")
    # upsell_potential: Optional[float] = Field(ge=0, le=1, description="Upselling opportunity")
    # retention_incentives: Optional[List[str]] = Field(description="Strategies to retain customers")
# EVOLVE-BLOCK-END: monetization_schema

# EVOLVE-BLOCK-START: gtm_strategy_schema
class GoToMarketStrategy(BaseModel):
    """Customer acquisition and growth strategy."""
    acquisition_channels: List[str] = Field(description="How to acquire customers")
    launch_strategy: str = Field(description="Product launch approach")
    growth_tactics: List[str] = Field(description="Strategies for scaling")
    partnership_opportunities: List[str] = Field(description="Potential partnerships")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # beta_testing_strategy: Optional[str] = Field(description="Beta testing and feedback approach")
    # influencer_strategy: Optional[str] = Field(description="Influencer marketing approach")
    # community_building: Optional[str] = Field(description="How to build user community")
    # viral_mechanics: Optional[List[str]] = Field(description="Built-in viral growth features")
    # geographic_rollout: Optional[List[str]] = Field(description="Geographic expansion plan")
# EVOLVE-BLOCK-END: gtm_strategy_schema

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

# EVOLVE-BLOCK-START: risk_assessment_schema
class RiskAssessment(BaseModel):
    """Risk evaluation."""
    risk: str = Field(description="Description of the risk")
    probability: Literal["low", "medium", "high"] = Field(description="Likelihood of occurrence")
    impact: Literal["low", "medium", "high"] = Field(description="Impact if it occurs")
    mitigation: str = Field(description="How to mitigate this risk")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # risk_category: Optional[Literal["market", "technical", "financial", "operational", "regulatory"]] = Field(description="Risk category")
    # timeline: Optional[str] = Field(description="When this risk might materialize")
    # monitoring_metrics: Optional[List[str]] = Field(description="Early warning indicators")
    # contingency_plan: Optional[str] = Field(description="Backup plan if mitigation fails")
    # cost_of_mitigation: Optional[float] = Field(ge=0, description="Cost to implement mitigation")
# EVOLVE-BLOCK-END: risk_assessment_schema

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

# EVOLVE-BLOCK-START: product_feature_schema
class ProductFeature(BaseModel):
    """Individual product feature specification."""
    name: str = Field(description="Feature name")
    description: str = Field(description="What the feature does")
    priority: Literal["must_have", "should_have", "nice_to_have"] = Field(description="Feature priority")
    acceptance_criteria: List[str] = Field(description="Criteria for feature completion")
    effort_estimate: Literal["small", "medium", "large"] = Field(description="Development effort")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # user_value_score: Optional[float] = Field(ge=1, le=10, description="User value rating")
    # technical_risk: Optional[Literal["low", "medium", "high"]] = Field(description="Implementation risk")
    # dependencies: Optional[List[str]] = Field(description="Feature dependencies")
    # usage_frequency: Optional[Literal["daily", "weekly", "monthly", "occasional"]] = Field(description="Expected usage")
    # monetization_impact: Optional[Literal["none", "indirect", "direct"]] = Field(description="Revenue impact")
# EVOLVE-BLOCK-END: product_feature_schema

# EVOLVE-BLOCK-START: technical_requirement_schema
class TechnicalRequirement(BaseModel):
    """Technical implementation requirement."""
    requirement: str = Field(description="Technical requirement description")
    category: Literal["performance", "security", "scalability", "integration"] = Field(description="Requirement type")
    specification: str = Field(description="Detailed specification")
    priority: Literal["high", "medium", "low"] = Field(description="Implementation priority")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # compliance_standards: Optional[List[str]] = Field(description="Required compliance standards")
    # third_party_dependencies: Optional[List[str]] = Field(description="External service dependencies")
    # testing_requirements: Optional[List[str]] = Field(description="Testing and validation needs")
    # maintenance_complexity: Optional[Literal["low", "medium", "high"]] = Field(description="Ongoing maintenance complexity")
    # cost_impact: Optional[Literal["low", "medium", "high"]] = Field(description="Impact on development cost")
# EVOLVE-BLOCK-END: technical_requirement_schema

# EVOLVE-BLOCK-START: success_metric_schema
class SuccessMetric(BaseModel):
    """Key performance indicator."""
    metric_name: str = Field(description="Name of the metric")
    description: str = Field(description="What this metric measures")
    target_value: str = Field(description="Target value to achieve")
    measurement_method: str = Field(description="How to measure this metric")
    timeframe: str = Field(description="When to measure/achieve this")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # metric_type: Optional[Literal["leading", "lagging", "diagnostic"]] = Field(description="Metric classification")
    # baseline_value: Optional[str] = Field(description="Current baseline measurement")
    # frequency: Optional[Literal["daily", "weekly", "monthly", "quarterly"]] = Field(description="Measurement frequency")
    # owner: Optional[str] = Field(description="Who is responsible for this metric")
    # threshold_alerts: Optional[List[str]] = Field(description="Alert conditions if underperforming")
# EVOLVE-BLOCK-END: success_metric_schema

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


# === SEO Keyword Evolution ===

# EVOLVE-BLOCK-START: keyword_strategy_schema
class KeywordOpportunity(BaseModel):
    """Individual keyword opportunity with competitive metrics."""
    keyword: str = Field(description="The keyword phrase")
    search_volume: int = Field(ge=0, description="Monthly search volume")
    competition_score: float = Field(ge=0, le=100, description="Competition difficulty (0=easy, 100=hard)")
    commercial_intent: Literal["low", "medium", "high"] = Field(description="Commercial purchase intent")
    seasonal_multiplier: float = Field(ge=0.1, le=10.0, description="Seasonal traffic multiplier")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # trend_direction: Optional[Literal["rising", "stable", "declining"]] = Field(description="Search trend direction")
    # geographic_focus: Optional[List[str]] = Field(description="Best performing regions")
    # related_keywords: Optional[List[str]] = Field(description="Semantically related terms")
    # content_gap_score: Optional[float] = Field(ge=0, le=10, description="Content opportunity score")
    # voice_search_potential: Optional[float] = Field(ge=0, le=1, description="Voice search optimization potential")
# EVOLVE-BLOCK-END: keyword_strategy_schema

# EVOLVE-BLOCK-START: niche_discovery_schema
class NicheKeywordCluster(BaseModel):
    """Cluster of related keywords defining a market niche."""
    cluster_name: str = Field(description="Name for this keyword cluster/niche")
    primary_keywords: List[KeywordOpportunity] = Field(description="Main high-volume keywords")
    long_tail_keywords: List[KeywordOpportunity] = Field(description="Long-tail opportunities")
    niche_score: float = Field(ge=0, le=10, description="Overall niche opportunity score")
    entry_difficulty: Literal["easy", "medium", "hard"] = Field(description="Market entry difficulty")
    market_size_estimate: int = Field(ge=0, description="Estimated total addressable searches")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # competitor_density: Optional[float] = Field(ge=0, le=1, description="How crowded the niche is")
    # monetization_potential: Optional[Literal["low", "medium", "high"]] = Field(description="Revenue potential")
    # content_requirements: Optional[List[str]] = Field(description="Types of content needed")
    # user_intent_mix: Optional[Dict[str, float]] = Field(description="Distribution of search intents")
    # seasonal_patterns: Optional[List[str]] = Field(description="Seasonal traffic patterns")
# EVOLVE-BLOCK-END: niche_discovery_schema

# EVOLVE-BLOCK-START: keyword_evolution_strategy
class KeywordEvolutionStrategy(BaseModel):
    """Strategy for evolving and discovering new keyword opportunities."""
    base_topic: str = Field(description="Core business/product topic")
    target_niches: List[NicheKeywordCluster] = Field(description="Identified niche opportunities")
    expansion_vectors: List[str] = Field(description="Directions for keyword expansion")
    competitive_gaps: List[str] = Field(description="Under-served keyword areas")
    innovation_keywords: List[str] = Field(description="Emerging/innovative keyword opportunities")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # keyword_generation_prompts: Optional[List[str]] = Field(description="AI prompts for generating new keywords")
    # semantic_expansion_rules: Optional[List[str]] = Field(description="Rules for semantic keyword expansion")
    # competitor_keyword_gaps: Optional[List[str]] = Field(description="Keywords competitors are missing")
    # emerging_trend_keywords: Optional[List[str]] = Field(description="Keywords from emerging trends")
    # localization_opportunities: Optional[List[str]] = Field(description="Geographic keyword variations")
# EVOLVE-BLOCK-END: keyword_evolution_strategy

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