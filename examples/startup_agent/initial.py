#!/usr/bin/env python3
"""
Evolving Startup Agent with SGR and Web Research.

EVOLVE-BLOCK contains parameters that ShinkaEvolve will mutate to find
optimal startup analysis strategies. Focus on SEO-driven seasonal business
launching in 3 months for Christmas 2025-2026 season.

EVOLVE-BLOCK-START
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import random

# SGR and ShinkaEvolve imports
from shinka.llm import LLMClient
from tavily_integration import TavilyWebResearch
from startup_sgr_schemas import KeywordOpportunity, NicheKeywordCluster, KeywordEvolutionStrategy

# Enhanced schemas with quantitative focus
from pydantic import BaseModel, Field
from typing import Literal
from startup_minimal_schemas import MinimalStartupAnalysis

logger = logging.getLogger(__name__)

# EVOLVE-BLOCK: Mutable parameters for genetic algorithm
@dataclass
class StartupAgentEvolutionConfig:
    """Evolutionary parameters for startup analysis optimization."""

    # Market research parameters (quick defaults)
    market_research_depth: int = 2  # Number of market research queries
    competitor_analysis_depth: int = 2  # Number of competitor research queries
    seo_keyword_research_depth: int = 3  # SEO keyword research queries

    # Strategy generation parameters
    strategy_count: int = 5  # Number of strategies to generate
    strategy_iteration_count: int = 3  # Refinement iterations

    # Analysis weights (must sum to 1.0)
    market_size_weight: float = 0.25
    seo_opportunity_weight: float = 0.30  # Higher weight for SEO focus
    competition_weight: float = 0.20
    execution_feasibility_weight: float = 0.15
    seasonal_timing_weight: float = 0.10

    # LLM parameters
    temperature: float = 0.8
    model_selection_strategy: Literal["random", "best_cost", "best_quality"] = "best_quality"

    # SEO focus parameters
    target_season: str = "Christmas 2025-2026"
    launch_timeline_months: int = 3
    primary_seo_focus: Literal["high_volume", "low_competition", "seasonal_surge", "long_tail"] = "seasonal_surge"

    # Report detail parameters
    quantitative_detail_level: int = 8  # 1-10 scale for data depth
    financial_projection_months: int = 12
    seo_metrics_count: int = 15

# Enhanced schemas with quantitative focus
# EVOLVE-BLOCK-START: seo_schemas
class SEOOpportunity(BaseModel):
    """SEO opportunity with specific metrics."""
    keyword: str = Field(description="Target keyword")
    monthly_search_volume: int = Field(ge=0, description="Monthly search volume")
    keyword_difficulty: int = Field(ge=0, le=100, description="SEO difficulty score")
    seasonal_multiplier: float = Field(ge=1.0, le=20.0, description="Holiday season traffic multiplier")
    competition_level: Literal["low", "medium", "high"] = Field(description="Competition level")
    estimated_cpc: float = Field(ge=0, description="Estimated cost per click in USD")
    commercial_intent: Literal["low", "medium", "high"] = Field(description="Commercial intent")
    # Evolvable: competitor_analysis, content_gap_score, local_search_volume, featured_snippet_potential
# EVOLVE-BLOCK-END: seo_schemas

# EVOLVE-BLOCK-START: market_data_schema
class QuantitativeMarketData(BaseModel):
    """Market data with specific numbers."""
    market_size_usd: int = Field(ge=0, description="Total addressable market in USD")
    growth_rate_annual: float = Field(ge=-0.5, le=2.0, description="Annual growth rate")
    seasonal_peak_multiplier: float = Field(ge=1.0, le=10.0, description="Peak season multiplier")
    target_customer_count: int = Field(ge=0, description="Estimated target customers")
    customer_acquisition_cost: float = Field(ge=0, description="Estimated CAC in USD")
    lifetime_value: float = Field(ge=0, description="Customer LTV in USD")
    market_penetration_percent: float = Field(ge=0, le=100, description="Achievable market penetration %")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # geographic_focus: Optional[List[str]] = Field(description="Primary geographic markets")
    # market_maturity: Optional[Literal["emerging", "growing", "mature", "declining"]] = Field(description="Market maturity stage")
    # barrier_to_entry_score: Optional[float] = Field(ge=1, le=10, description="Market entry difficulty (1=easy, 10=hard)")
    # regulatory_risk_score: Optional[float] = Field(ge=1, le=10, description="Regulatory risk assessment")
    # market_volatility: Optional[float] = Field(ge=0, le=1, description="Market volatility factor")
# EVOLVE-BLOCK-END: market_data_schema

# EVOLVE-BLOCK-START: competitor_metrics_schema
class CompetitorMetrics(BaseModel):
    """Competitor with specific metrics."""
    name: str = Field(description="Competitor name")
    estimated_revenue_usd: Optional[int] = Field(ge=0, description="Estimated annual revenue")
    market_share_percent: float = Field(ge=0, le=100, description="Market share percentage")
    seo_domain_authority: int = Field(ge=0, le=100, description="Domain authority score")
    organic_traffic_monthly: Optional[int] = Field(ge=0, description="Estimated monthly organic traffic")
    paid_ad_spend_monthly: Optional[int] = Field(ge=0, description="Estimated monthly ad spend")
    weakness_score: int = Field(ge=1, le=10, description="Weakness/opportunity score (1=strong, 10=weak)")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # funding_stage: Optional[Literal["bootstrap", "seed", "series_a", "series_b", "public"]] = Field(description="Funding stage")
    # employee_count: Optional[int] = Field(ge=1, description="Estimated employee count")
    # social_media_followers: Optional[int] = Field(ge=0, description="Total social media following")
    # customer_satisfaction_score: Optional[float] = Field(ge=1, le=10, description="Customer satisfaction rating")
    # innovation_score: Optional[float] = Field(ge=1, le=10, description="Innovation and R&D capability")
    # geographic_presence: Optional[List[str]] = Field(description="Countries/regions where active")
    # pricing_strategy: Optional[str] = Field(description="Pricing model and strategy")
# EVOLVE-BLOCK-END: competitor_metrics_schema

# EVOLVE-BLOCK-START: financial_projection_schema
class FinancialProjection(BaseModel):
    """Monthly financial projection."""
    month: int = Field(ge=1, le=24, description="Month number")
    projected_revenue: int = Field(ge=0, description="Projected revenue in USD")
    projected_costs: int = Field(ge=0, description="Projected costs in USD")
    user_acquisition_count: int = Field(ge=0, description="New users acquired")
    organic_traffic: int = Field(ge=0, description="Organic traffic visitors")
    conversion_rate: float = Field(ge=0, le=1, description="Conversion rate")
    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # paid_traffic: Optional[int] = Field(ge=0, description="Paid traffic visitors")
    # cost_breakdown: Optional[Dict[str, int]] = Field(description="Detailed cost breakdown")
    # revenue_breakdown: Optional[Dict[str, int]] = Field(description="Revenue by source/product")
    # churn_rate: Optional[float] = Field(ge=0, le=1, description="Customer churn rate")
    # gross_margin: Optional[float] = Field(ge=0, le=1, description="Gross margin percentage")
    # cash_flow: Optional[int] = Field(description="Net cash flow for the month")
    # burn_rate: Optional[int] = Field(ge=0, description="Monthly burn rate")
    # runway_months: Optional[int] = Field(ge=0, description="Remaining runway in months")
# EVOLVE-BLOCK-END: financial_projection_schema

# EVOLVE-BLOCK-START: main_analysis_schema
class QuantitativeStartupAnalysis(BaseModel):
    """Comprehensive quantitative startup analysis."""
    product_name: str = Field(description="Product name")
    elevator_pitch: str = Field(description="30-second elevator pitch")

    # Market analysis
    market_data: QuantitativeMarketData = Field(description="Quantitative market data")
    seo_opportunities: List[SEOOpportunity] = Field(description="SEO opportunities with metrics")
    competitors: List[CompetitorMetrics] = Field(description="Competitor analysis with metrics")

    # EVOLVABLE SEO STRATEGY - genetic algorithm can modify these
    keyword_strategy: KeywordEvolutionStrategy = Field(description="Evolving keyword discovery and targeting strategy")

    # Product strategy
    core_features: List[str] = Field(description="Core product features")
    unique_value_proposition: str = Field(description="Unique value proposition")
    pricing_model: str = Field(description="Pricing model and tiers")

    # SEO & Marketing strategy
    seo_strategy: str = Field(description="SEO strategy for seasonal traffic")
    content_marketing_plan: List[str] = Field(description="Content marketing tactics")
    launch_timeline: List[str] = Field(description="3-month launch timeline")

    # Financial projections
    financial_projections: List[FinancialProjection] = Field(description="12-month financial projections")
    funding_requirements: int = Field(ge=0, description="Funding needed in USD")
    break_even_month: int = Field(ge=1, le=24, description="Break-even month")

    # Risk analysis
    key_risks: List[str] = Field(description="Main business risks")
    mitigation_strategies: List[str] = Field(description="Risk mitigation strategies")

    # Success metrics
    kpi_targets: List[str] = Field(description="Specific KPI targets with numbers (format: 'metric: target')")
    competitive_advantages: List[str] = Field(description="Key competitive advantages")

    # EVOLVABLE FIELDS - these can be added/modified by genetic algorithm:
    # tech_stack: Optional[List[str]] = Field(description="Technology stack recommendations")
    # user_personas: Optional[List[UserPersona]] = Field(description="Detailed user personas")
    # growth_metrics: Optional[GrowthMetrics] = Field(description="Growth and virality metrics")
    # regulatory_compliance: Optional[List[str]] = Field(description="Regulatory requirements")
    # partnership_opportunities: Optional[List[Partnership]] = Field(description="Strategic partnerships")
    # internationalization: Optional[InternationalizationPlan] = Field(description="Global expansion plan")
# EVOLVE-BLOCK-END: main_analysis_schema

class EvolvingStartupAgent:
    """Evolving startup agent with genetic algorithm parameters."""

    def __init__(self, config: StartupAgentEvolutionConfig):
        self.config = config

        # Initialize LLM client based on evolution parameters
        model_names = self._select_models()

        # Structured output LLM for key metrics only
        self.metrics_llm = LLMClient(
            model_names=model_names,
            output_model=MinimalStartupAnalysis,
            verbose=True
        )

        # Text generation LLM for detailed PRD content
        self.text_llm = LLMClient(
            model_names=model_names,
            output_model=None,  # No structured output - free text
            verbose=True
        )

        # Web research
        self.web_research = TavilyWebResearch("http://localhost:8013")

        # Results storage
        self.market_research_data: str = ""
        self.seo_research_data: str = ""
        self.competitor_research_data: str = ""
        self.final_analysis: Optional[QuantitativeStartupAnalysis] = None

        # Generated content storage
        self.generated_prd_text: str = ""
        self.generated_metrics: Optional[MinimalStartupAnalysis] = None

        # Quality tracking
        self.generation_stats = {
            "hybrid_success": 0,
            "metrics_only": 0,
            "template_fallback": 0,
            "generation_errors": 0
        }

    def _create_analysis_template(self, idea: str) -> QuantitativeStartupAnalysis:
        """Create a basic template analysis to ensure valid structure."""
        return QuantitativeStartupAnalysis(
            product_name=f"AI-Powered {idea.split()[0].title()} Solution",
            elevator_pitch=f"Revolutionary solution that transforms {idea[:50]}... using AI and modern technology.",

            # Market data with reasonable defaults
            market_data=QuantitativeMarketData(
                market_size_usd=500_000_000,  # $500M default market
                growth_rate_annual=0.15,      # 15% growth
                seasonal_peak_multiplier=3.0, # 3x Christmas peak
                target_customer_count=100_000,
                customer_acquisition_cost=25.0,
                lifetime_value=150.0,
                market_penetration_percent=2.0
            ),

            # SEO template - 3+ for high quality
            seo_opportunities=[
                SEOOpportunity(
                    keyword="christmas gift ideas",
                    monthly_search_volume=450000,
                    keyword_difficulty=65,
                    seasonal_multiplier=8.0,
                    competition_level="high",
                    estimated_cpc=1.25,
                    commercial_intent="high"
                ),
                SEOOpportunity(
                    keyword="holiday shopping 2025",
                    monthly_search_volume=200000,
                    keyword_difficulty=45,
                    seasonal_multiplier=12.0,
                    competition_level="medium",
                    estimated_cpc=0.85,
                    commercial_intent="high"
                ),
                SEOOpportunity(
                    keyword="christmas cards personalized",
                    monthly_search_volume=180000,
                    keyword_difficulty=55,
                    seasonal_multiplier=15.0,
                    competition_level="medium",
                    estimated_cpc=0.95,
                    commercial_intent="high"
                )
            ],

            # Competitor template - 2+ for high quality
            competitors=[
                CompetitorMetrics(
                    name="Canva",
                    estimated_revenue_usd=15_000_000,
                    market_share_percent=25.0,
                    seo_domain_authority=85,
                    organic_traffic_monthly=2500000,
                    paid_ad_spend_monthly=200000,
                    weakness_score=7
                ),
                CompetitorMetrics(
                    name="Hallmark Digital",
                    estimated_revenue_usd=50_000_000,
                    market_share_percent=35.0,
                    seo_domain_authority=75,
                    organic_traffic_monthly=1200000,
                    paid_ad_spend_monthly=150000,
                    weakness_score=8
                )
            ],

            # Core features template
            core_features=[
                "AI-powered personalization engine",
                "Seasonal content optimization",
                "Multi-channel distribution",
                "Real-time analytics dashboard",
                "Mobile-first user experience"
            ],

            unique_value_proposition="First-to-market AI solution combining personalization with seasonal optimization for maximum Christmas 2025-2026 impact",
            pricing_model="Freemium with premium tiers: Free (basic), Pro ($29/month), Enterprise ($199/month)",

            # SEO strategy template
            seo_strategy="Target high-volume Christmas keywords with seasonal multipliers, create evergreen + seasonal content mix, optimize for December 2025 search surge",

            content_marketing_plan=[
                "Holiday gift guides with AI recommendations",
                "Seasonal trend analysis blog posts",
                "Video tutorials and demos",
                "Social media Christmas countdown campaigns",
                "Email sequences targeting holiday shoppers"
            ],

            launch_timeline=[
                "Month 1: MVP development and testing",
                "Month 2: Beta launch and user feedback",
                "Month 3: Full launch with Christmas campaign"
            ],

            # Financial projections template
            financial_projections=[
                FinancialProjection(month=1, projected_revenue=5000, projected_costs=15000, user_acquisition_count=100, organic_traffic=2000, conversion_rate=0.02),
                FinancialProjection(month=3, projected_revenue=25000, projected_costs=20000, user_acquisition_count=500, organic_traffic=15000, conversion_rate=0.035),
                FinancialProjection(month=6, projected_revenue=75000, projected_costs=35000, user_acquisition_count=1200, organic_traffic=45000, conversion_rate=0.05),
                FinancialProjection(month=12, projected_revenue=200000, projected_costs=80000, user_acquisition_count=2500, organic_traffic=120000, conversion_rate=0.08)
            ],

            funding_requirements=250_000,
            break_even_month=8,

            key_risks=[
                "Seasonal revenue concentration in Q4",
                "High customer acquisition costs during peak season",
                "Competition from established players",
                "Technology scalability during traffic spikes"
            ],

            mitigation_strategies=[
                "Develop year-round product extensions",
                "Build organic traffic to reduce paid CAC",
                "Focus on unique AI differentiators",
                "Implement auto-scaling infrastructure"
            ],

            kpi_targets=[
                "Revenue: $200k by month 12",
                "Users: 10,000 active by Christmas 2025",
                "Organic Traffic: 100k monthly by launch",
                "Conversion Rate: 5% average",
                "CAC Payback: <6 months"
            ],

            competitive_advantages=[
                "First-mover advantage in AI-powered seasonal optimization",
                "Superior personalization algorithms",
                "Integrated SEO and content strategy",
                "Rapid time-to-market for Christmas 2025"
            ],

            # EVOLVABLE KEYWORD STRATEGY - genetic algorithm will evolve this
            keyword_strategy=KeywordEvolutionStrategy(
                base_topic=idea[:50],
                target_niches=[
                    NicheKeywordCluster(
                        cluster_name="Seasonal Holiday Cards",
                        primary_keywords=[
                            KeywordOpportunity(
                                keyword="christmas cards",
                                search_volume=450000,
                                competition_score=75,
                                commercial_intent="high",
                                seasonal_multiplier=8.0
                            ),
                            KeywordOpportunity(
                                keyword="holiday greeting cards",
                                search_volume=200000,
                                competition_score=65,
                                commercial_intent="high",
                                seasonal_multiplier=6.0
                            )
                        ],
                        long_tail_keywords=[
                            KeywordOpportunity(
                                keyword="personalized christmas cards online",
                                search_volume=35000,
                                competition_score=45,
                                commercial_intent="high",
                                seasonal_multiplier=9.0
                            ),
                            KeywordOpportunity(
                                keyword="ai generated holiday cards",
                                search_volume=8000,
                                competition_score=25,
                                commercial_intent="medium",
                                seasonal_multiplier=10.0
                            )
                        ],
                        niche_score=8.5,
                        entry_difficulty="medium",
                        market_size_estimate=700000
                    )
                ],
                expansion_vectors=[
                    "AI-powered personalization",
                    "Corporate holiday solutions",
                    "Year-round greeting cards",
                    "Social media card sharing"
                ],
                competitive_gaps=[
                    "Real-time AI customization",
                    "Bulk corporate ordering",
                    "International shipping automation"
                ],
                innovation_keywords=[
                    "ai christmas card maker",
                    "automated holiday greetings",
                    "smart seasonal marketing"
                ]
            )
        )

    def _select_models(self) -> List[str]:
        """Select LLM models based on evolution strategy."""
        if self.config.model_selection_strategy == "best_quality":
            return ["gpt-5-mini"]
        elif self.config.model_selection_strategy == "best_cost":
            return ["gpt-4o-mini"]
        else:  # random
            return random.choice([["gpt-5-mini"], ["gpt-4o-mini"]])

    async def analyze_startup_idea_evolving(self, idea: str) -> QuantitativeStartupAnalysis:
        """
        Evolving startup analysis with quantitative focus and SEO emphasis.
        """
        logger.info(f"🧬 Starting evolving startup analysis...")
        logger.info(f"📊 Config: depth={self.config.market_research_depth}, SEO={self.config.seo_keyword_research_depth}")

        # Phase 0: Create base analysis with evolving keyword strategy
        base_analysis = self._create_analysis_template(idea)
        keyword_strategy = base_analysis.keyword_strategy

        # Phase 1: Enhanced Market Research
        await self._conduct_enhanced_market_research(idea)

        # Phase 2: SEO Opportunity Research with evolving keywords
        await self._conduct_seo_research(idea, keyword_strategy)

        # Phase 3: Competitive Intelligence
        await self._conduct_competitive_research(idea)

        # Phase 4: Generate Quantitative Analysis
        final_analysis = await self._generate_quantitative_analysis(idea)

        # Preserve the evolving keyword strategy in final analysis
        final_analysis.keyword_strategy = keyword_strategy

        self.final_analysis = final_analysis
        return final_analysis

    async def _conduct_enhanced_market_research(self, idea: str):
        """Enhanced market research with configurable depth."""

        market_queries = [
            f"Christmas greeting cards market size revenue 2024 2025 growth statistics",
            f"Holiday card industry trends USA consumer spending data",
            f"AI greeting card market opportunity revenue projections",
            f"Christmas ecard digital vs print market share statistics",
            f"Seasonal greeting card customer demographics spending patterns",
            f"Holiday marketing automation tools market size revenue",
            f"Christmas gift personalization market trends growth data",
            f"AI content generation market size holiday applications"
        ]

        research_data_parts = []
        for i, query in enumerate(market_queries[:self.config.market_research_depth]):
            logger.info(f"📊 Market research {i+1}/{self.config.market_research_depth}: {query[:50]}...")
            data = await self.web_research.research_market_size(query)
            research_data_parts.append(f"QUERY {i+1}: {query}\nDATA: {data}\n\n")

        self.market_research_data = "".join(research_data_parts)
        logger.info(f"📊 Market research completed: {len(self.market_research_data)} characters")

    async def _conduct_seo_research(self, idea: str, keyword_strategy: KeywordEvolutionStrategy):
        """Deep SEO research with top-5 site analysis per keyword."""

        # Extract core keywords from evolving strategy
        core_keywords = []

        # Get primary keywords from all niches
        for niche in keyword_strategy.target_niches:
            for keyword_opp in niche.primary_keywords:
                core_keywords.append(keyword_opp.keyword)

        # Add innovation keywords for exploration
        core_keywords.extend(keyword_strategy.innovation_keywords)

        # Remove duplicates and take first few for deep analysis
        core_keywords = list(dict.fromkeys(core_keywords))  # Remove duplicates while preserving order

        logger.info(f"🔍 Starting deep SEO analysis for {len(core_keywords)} keywords...")

        seo_analyses = []
        combined_semantic_core = []
        combined_marketing_hooks = []
        combined_competitive_gaps = []

        # Perform deep analysis for each core keyword
        for i, keyword in enumerate(core_keywords[:3]):  # Limit to 3 to avoid timeout
            logger.info(f"🎯 Deep SEO analysis {i+1}/3: {keyword}")

            try:
                # Perform deep analysis - this will parse top-5 sites
                analysis = await self.web_research.deep_seo_analysis(keyword, max_sites=5)
                seo_analyses.append(analysis)

                # Aggregate insights across all keywords
                combined_semantic_core.extend(analysis.get("semantic_core", []))
                combined_marketing_hooks.extend(analysis.get("marketing_hooks", []))
                combined_competitive_gaps.extend(analysis.get("competitive_gaps", []))

                logger.info(f"✅ Keyword '{keyword}' analysis: {len(analysis.get('top_sites', []))} sites, {len(analysis.get('semantic_core', []))} keywords")

            except Exception as e:
                logger.warning(f"⚠️ Deep analysis failed for '{keyword}': {e}")

        # Format comprehensive SEO research data
        self.seo_research_data = self._format_deep_seo_data(
            seo_analyses,
            combined_semantic_core,
            combined_marketing_hooks,
            combined_competitive_gaps
        )

        logger.info(f"🔍 Deep SEO research completed: {len(self.seo_research_data)} characters")

    def _format_deep_seo_data(self, analyses: List[Dict], semantic_core: List[str],
                              marketing_hooks: List[str], gaps: List[str]) -> str:
        """Format deep SEO analysis into comprehensive summary."""

        summary = "DEEP SEO COMPETITIVE ANALYSIS:\n\n"

        # Semantic core summary
        unique_keywords = list(set(semantic_core))[:20]
        summary += f"SEMANTIC CORE ({len(unique_keywords)} keywords):\n"
        for kw in unique_keywords:
            summary += f"- {kw}\n"
        summary += "\n"

        # Marketing hooks summary
        unique_hooks = list(set(marketing_hooks))[:15]
        summary += f"COMPETITOR MARKETING HOOKS ({len(unique_hooks)} hooks):\n"
        for hook in unique_hooks:
            summary += f"- {hook}\n"
        summary += "\n"

        # Competitive gaps
        unique_gaps = list(set(gaps))
        summary += f"COMPETITIVE GAPS & OPPORTUNITIES ({len(unique_gaps)} gaps):\n"
        for gap in unique_gaps:
            summary += f"- {gap}\n"
        summary += "\n"

        # Top sites analysis per keyword
        summary += "TOP COMPETITORS BY KEYWORD:\n"
        for analysis in analyses:
            keyword = analysis.get("keyword", "unknown")
            top_sites = analysis.get("top_sites", [])

            summary += f"\n'{keyword}' top competitors:\n"
            for i, site in enumerate(top_sites[:3]):
                domain = site.get("domain", "unknown")
                positioning = ", ".join(site.get("positioning", []))
                summary += f"  {i+1}. {domain} - {positioning}\n"

        return summary

    async def _conduct_competitive_research(self, idea: str):
        """Competitive intelligence with metrics focus."""

        competitor_queries = [
            f"Canva Christmas card generator revenue traffic statistics",
            f"Hallmark ecard digital revenue market share data",
            f"AI greeting card competitors revenue funding statistics",
            f"Christmas card creator apps download revenue statistics",
            f"Jacquie Lawson cards revenue subscriber statistics data",
            f"Paperless Post holiday cards pricing revenue model",
            f"Christmas card maker competitors SEO traffic data"
        ]

        competitor_data_parts = []
        for i, query in enumerate(competitor_queries[:self.config.competitor_analysis_depth]):
            logger.info(f"🏢 Competitor research {i+1}/{self.config.competitor_analysis_depth}: {query[:50]}...")
            data = await self.web_research.research_competitors(query)
            competitor_data_parts.append(f"COMPETITOR QUERY {i+1}: {query}\nDATA: {data}\n\n")

        self.competitor_research_data = "".join(competitor_data_parts)
        logger.info(f"🏢 Competitor research completed: {len(self.competitor_research_data)} characters")

    async def _generate_quantitative_analysis(self, idea: str) -> QuantitativeStartupAnalysis:
        """Generate analysis using hybrid approach: structured metrics + text PRD."""
        return await self._generate_hybrid_analysis(idea)

    async def _generate_hybrid_analysis(self, idea: str) -> QuantitativeStartupAnalysis:
        """Generate comprehensive quantitative analysis with template fallback."""

        # Create fallback template first
        template = self._create_analysis_template(idea)

        # Calculate launch timing
        launch_date = datetime.now() + timedelta(days=30 * self.config.launch_timeline_months)

        try:
            # Step 1: Generate structured metrics (small, reliable)
            metrics_prompt = f"""
            STARTUP IDEA: {idea}
            TARGET: Christmas 2025-2026 launch

            RESEARCH: Market {self.market_research_data[:400]}, SEO {self.seo_research_data[:300]}, Competitors {self.competitor_research_data[:300]}

            Generate MinimalStartupAnalysis with essential metrics only:
            - Product name and pitch
            - Market size, CAC, LTV numbers
            - 3 Christmas SEO keywords with search volumes
            - 2 competitors with revenue estimates
            - 4 financial projections (months 1,3,6,12)
            - Core features, funding, break-even

            Use REAL numbers from research data.
            """

            logger.info("🔢 Generating structured metrics...")
            metrics_result = self.metrics_llm.query(
                msg=metrics_prompt,
                system_msg="Generate minimal structured startup metrics for Christmas 2025 seasonal business. Use specific numbers.",
                msg_history=[]
            )

            if metrics_result and metrics_result.parsed_content:
                self.generated_metrics = metrics_result.parsed_content
                logger.info("✅ Structured metrics generated successfully")

                # Step 2: Generate detailed PRD text (no structure limits)
                prd_prompt = f"""
                Based on these validated metrics for {self.generated_metrics.product_name}:

                Market: ${self.generated_metrics.market_data.market_size_usd:,} size, ${self.generated_metrics.market_data.customer_acquisition_cost} CAC
                SEO: {', '.join(opp.keyword for opp in self.generated_metrics.seo_opportunities)}
                Competitors: {', '.join(comp.name for comp in self.generated_metrics.competitors)}

                Generate comprehensive PRD document with:
                - Detailed product vision and strategy
                - Complete feature specifications with acceptance criteria
                - Technical requirements and architecture
                - Go-to-market strategy for Christmas 2025-2026
                - Risk assessment and mitigation plans
                - Development roadmap and milestones

                Focus on SEO-driven seasonal strategy. Be thorough and specific.
                """

                logger.info("📄 Generating detailed PRD text...")
                prd_result = self.text_llm.query(
                    msg=prd_prompt,
                    system_msg="Generate comprehensive PRD document for Christmas seasonal business. Be detailed and thorough.",
                    msg_history=[]
                )

                if prd_result and prd_result.parsed_content:
                    self.generated_prd_text = prd_result.parsed_content
                    logger.info("✅ PRD text generated successfully")

                # Step 3: Convert minimal analysis to full analysis
                full_analysis = self._convert_minimal_to_full(self.generated_metrics, template)
                self.generation_stats["hybrid_success"] += 1
                return full_analysis

            else:
                logger.warning("⚠️ Metrics generation failed, using template")
                self.generation_stats["metrics_only"] += 1
                return template

            # Validate result has HIGH QUALITY data - fallback only for real failures
            analysis = result.parsed_content
            if (analysis and
                # Strong validation - require substantial content
                len(analysis.seo_opportunities) >= 3 and
                len(analysis.competitors) >= 2 and
                len(analysis.financial_projections) >= 4 and
                len(analysis.core_features) >= 3 and
                len(analysis.kpi_targets) >= 3 and
                # Market data quality check
                analysis.market_data.market_size_usd >= 1_000_000 and
                analysis.market_data.customer_acquisition_cost > 0 and
                analysis.market_data.lifetime_value > 0 and
                # SEO quality check - seasonal focus
                any("christmas" in opp.keyword.lower() or "holiday" in opp.keyword.lower()
                    for opp in analysis.seo_opportunities) and
                # Financial realism check
                any(proj.projected_revenue > 0 for proj in analysis.financial_projections) and
                analysis.funding_requirements > 0 and
                1 <= analysis.break_even_month <= 24):

                logger.info("✅ LLM generated HIGH QUALITY analysis - using LLM result")
                self.generation_stats["llm_high_quality"] += 1
                return analysis

            elif analysis and len(analysis.seo_opportunities) >= 1:
                # Partial success - enhance LLM result instead of replacing
                logger.info("⚡ LLM analysis partial - enhancing with template data")
                self.generation_stats["llm_enhanced"] += 1

                # Keep LLM's creative content, supplement weak areas
                if len(analysis.seo_opportunities) < 3:
                    analysis.seo_opportunities.extend(template.seo_opportunities[:3-len(analysis.seo_opportunities)])

                if len(analysis.competitors) < 2:
                    analysis.competitors.extend(template.competitors[:2-len(analysis.competitors)])

                if len(analysis.financial_projections) < 4:
                    analysis.financial_projections.extend(template.financial_projections[:4-len(analysis.financial_projections)])

                if len(analysis.kpi_targets) < 3:
                    analysis.kpi_targets.extend(template.kpi_targets[:3-len(analysis.kpi_targets)])

                # Fix market data if needed
                if analysis.market_data.market_size_usd < 1_000_000:
                    analysis.market_data.market_size_usd = template.market_data.market_size_usd

                return analysis
            else:
                logger.warning("❌ LLM analysis insufficient quality - using template fallback")
                self.generation_stats["template_fallback"] += 1
                # Only use template as last resort
                if analysis and analysis.product_name and len(analysis.product_name) > 3:
                    template.product_name = analysis.product_name
                if analysis and analysis.elevator_pitch and len(analysis.elevator_pitch) > 10:
                    template.elevator_pitch = analysis.elevator_pitch
                return template

        except Exception as e:
            logger.error(f"❌ Hybrid analysis failed: {e}, using template fallback")
            self.generation_stats["generation_errors"] += 1
            return template

    def _convert_minimal_to_full(self, minimal: MinimalStartupAnalysis, template: QuantitativeStartupAnalysis) -> QuantitativeStartupAnalysis:
        """Convert minimal analysis to full QuantitativeStartupAnalysis."""

        # Convert minimal structures to full structures
        full_market_data = QuantitativeMarketData(
            market_size_usd=minimal.market_data.market_size_usd,
            growth_rate_annual=minimal.market_data.growth_rate,
            seasonal_peak_multiplier=3.0,  # Default seasonal multiplier
            target_customer_count=minimal.market_data.market_size_usd // 100,  # Estimate
            customer_acquisition_cost=minimal.market_data.customer_acquisition_cost,
            lifetime_value=minimal.market_data.lifetime_value,
            market_penetration_percent=2.0  # Default penetration
        )

        full_seo_opportunities = [
            SEOOpportunity(
                keyword=opp.keyword,
                monthly_search_volume=opp.monthly_searches,
                keyword_difficulty=opp.difficulty,
                seasonal_multiplier=opp.seasonal_boost,
                competition_level="medium",
                estimated_cpc=1.0,
                commercial_intent="high"
            ) for opp in minimal.seo_opportunities
        ]

        full_competitors = [
            CompetitorMetrics(
                name=comp.name,
                estimated_revenue_usd=comp.estimated_revenue,
                market_share_percent=comp.market_share,
                seo_domain_authority=75,  # Default DA
                organic_traffic_monthly=500000,  # Default traffic
                paid_ad_spend_monthly=50000,  # Default ad spend
                weakness_score=7  # Default weakness
            ) for comp in minimal.competitors
        ]

        full_financial_projections = [
            FinancialProjection(
                month=proj.month,
                projected_revenue=proj.revenue,
                projected_costs=proj.costs,
                user_acquisition_count=proj.revenue // 50,  # Estimate users
                organic_traffic=proj.revenue * 10,  # Estimate traffic
                conversion_rate=0.05  # Default conversion
            ) for proj in minimal.financial_projections
        ]

        # Create full analysis
        return QuantitativeStartupAnalysis(
            product_name=minimal.product_name,
            elevator_pitch=minimal.elevator_pitch,
            market_data=full_market_data,
            seo_opportunities=full_seo_opportunities,
            competitors=full_competitors,
            keyword_strategy=template.keyword_strategy,  # Use keyword strategy from template
            core_features=minimal.core_features,
            unique_value_proposition=minimal.unique_value_proposition,
            pricing_model=minimal.pricing_model,
            seo_strategy=minimal.seo_strategy,
            content_marketing_plan=["SEO-focused content", "Seasonal campaigns", "Social media"],
            launch_timeline=["Month 1: Development", "Month 2: Testing", "Month 3: Launch"],
            financial_projections=full_financial_projections,
            funding_requirements=minimal.funding_requirements,
            break_even_month=minimal.break_even_month,
            key_risks=minimal.key_risks,
            mitigation_strategies=["Market research", "Competitive analysis", "Risk monitoring"],
            kpi_targets=minimal.kpi_targets,
            competitive_advantages=minimal.competitive_advantages
        )

    def calculate_evolution_fitness(self) -> float:
        """Calculate fitness score for genetic algorithm."""
        if not self.final_analysis:
            return 0.0

        analysis = self.final_analysis
        fitness_components = []

        # Market size score
        market_score = min(analysis.market_data.market_size_usd / 1_000_000_000, 1.0)  # Normalize by $1B
        fitness_components.append(market_score * self.config.market_size_weight)

        # SEO opportunity score
        seo_score = min(len(analysis.seo_opportunities) / self.config.seo_metrics_count, 1.0)
        avg_search_volume = sum(opp.monthly_search_volume for opp in analysis.seo_opportunities) / max(len(analysis.seo_opportunities), 1)
        seo_score *= min(avg_search_volume / 10000, 1.0)  # Normalize by 10k searches
        fitness_components.append(seo_score * self.config.seo_opportunity_weight)

        # Competition score (lower competition = higher score)
        if analysis.competitors:
            avg_weakness = sum(comp.weakness_score for comp in analysis.competitors) / len(analysis.competitors)
            competition_score = avg_weakness / 10.0  # Normalize weakness score
            fitness_components.append(competition_score * self.config.competition_weight)

        # Execution feasibility score
        feasibility_score = min(len(analysis.core_features) / 8, 1.0)  # Normalize by 8 features
        if analysis.break_even_month <= 12:
            feasibility_score *= 1.0
        else:
            feasibility_score *= 0.5
        fitness_components.append(feasibility_score * self.config.execution_feasibility_weight)

        # Seasonal timing score
        seasonal_score = 1.0 if "Christmas" in self.config.target_season else 0.5
        fitness_components.append(seasonal_score * self.config.seasonal_timing_weight)

        total_fitness = sum(fitness_components)
        logger.info(f"🧬 Evolution fitness: {total_fitness:.3f} (components: {[f'{c:.3f}' for c in fitness_components]})")

        return total_fitness

    def save_evolution_results(self, output_dir: str = None):
        """Save results in ShinkaEvolve format with evolution metrics."""

        if output_dir is None:
            import os

            # Check if ShinkaEvolve provides a results directory via environment variable
            shinka_results_dir = os.getenv('SHINKA_RESULTS_DIR')
            if shinka_results_dir:
                output_dir = Path(shinka_results_dir)
            else:
                # Fallback to timestamp-based directory for standalone runs
                base_results = Path("/Users/rustam/projects/ShinkaEvolve/results")
                timestamp = datetime.now().strftime("%Y.%m.%d%H%M%S")
                output_dir = base_results / "startup_agent" / timestamp

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Save evolution config
        config_data = {
            "evolution_config": {
                "market_research_depth": self.config.market_research_depth,
                "competitor_analysis_depth": self.config.competitor_analysis_depth,
                "seo_keyword_research_depth": self.config.seo_keyword_research_depth,
                "strategy_count": self.config.strategy_count,
                "weights": {
                    "market_size_weight": self.config.market_size_weight,
                    "seo_opportunity_weight": self.config.seo_opportunity_weight,
                    "competition_weight": self.config.competition_weight,
                    "execution_feasibility_weight": self.config.execution_feasibility_weight,
                    "seasonal_timing_weight": self.config.seasonal_timing_weight
                },
                "seo_focus": self.config.primary_seo_focus,
                "target_season": self.config.target_season,
                "launch_timeline_months": self.config.launch_timeline_months
            },
            "fitness_score": self.calculate_evolution_fitness(),
            "timestamp": datetime.now().isoformat(),
            "generation_quality_stats": self.generation_stats  # Track fallback usage
        }

        with open(output_dir / "evolution_config.json", "w") as f:
            json.dump(config_data, f, indent=2)

        # Save complete analysis
        if self.final_analysis:
            analysis_data = {
                "product_name": self.final_analysis.product_name,
                "elevator_pitch": self.final_analysis.elevator_pitch,
                "market_data": {
                    "market_size_usd": self.final_analysis.market_data.market_size_usd,
                    "growth_rate_annual": self.final_analysis.market_data.growth_rate_annual,
                    "seasonal_peak_multiplier": self.final_analysis.market_data.seasonal_peak_multiplier,
                    "target_customer_count": self.final_analysis.market_data.target_customer_count,
                    "customer_acquisition_cost": self.final_analysis.market_data.customer_acquisition_cost,
                    "lifetime_value": self.final_analysis.market_data.lifetime_value
                },
                "seo_opportunities": [
                    {
                        "keyword": opp.keyword,
                        "monthly_search_volume": opp.monthly_search_volume,
                        "keyword_difficulty": opp.keyword_difficulty,
                        "seasonal_multiplier": opp.seasonal_multiplier,
                        "estimated_cpc": opp.estimated_cpc
                    } for opp in self.final_analysis.seo_opportunities
                ],
                "competitors": [
                    {
                        "name": comp.name,
                        "market_share_percent": comp.market_share_percent,
                        "seo_domain_authority": comp.seo_domain_authority,
                        "weakness_score": comp.weakness_score
                    } for comp in self.final_analysis.competitors
                ],
                "financial_projections": [
                    {
                        "month": proj.month,
                        "projected_revenue": proj.projected_revenue,
                        "projected_costs": proj.projected_costs,
                        "user_acquisition_count": proj.user_acquisition_count,
                        "organic_traffic": proj.organic_traffic,
                        "conversion_rate": proj.conversion_rate
                    } for proj in self.final_analysis.financial_projections
                ],
                "core_features": self.final_analysis.core_features,
                "seo_strategy": self.final_analysis.seo_strategy,
                "launch_timeline": self.final_analysis.launch_timeline,
                "kpi_targets": self.final_analysis.kpi_targets,
                "funding_requirements": self.final_analysis.funding_requirements,
                "break_even_month": self.final_analysis.break_even_month
            }

            with open(output_dir / "quantitative_analysis.json", "w") as f:
                json.dump(analysis_data, f, indent=2)

        # Save raw research data
        with open(output_dir / "research_data.txt", "w") as f:
            f.write(f"MARKET RESEARCH ({len(self.market_research_data)} chars):\n")
            f.write(self.market_research_data)
            f.write(f"\n\nSEO RESEARCH ({len(self.seo_research_data)} chars):\n")
            f.write(self.seo_research_data)
            f.write(f"\n\nCOMPETITOR RESEARCH ({len(self.competitor_research_data)} chars):\n")
            f.write(self.competitor_research_data)

        # Save formatted PRD document
        if self.generated_prd_text:
            with open(output_dir / "PRD_Document.md", "w", encoding="utf-8") as f:
                f.write(f"# Product Requirements Document: {self.final_analysis.product_name if self.final_analysis else 'Startup Analysis'}\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Target Season:** {self.config.target_season}\n")
                f.write(f"**Evolution Fitness:** {self.calculate_evolution_fitness():.3f}\n\n")
                f.write("---\n\n")
                f.write(self.generated_prd_text)

        # Save executive summary
        if self.final_analysis:
            summary = self._generate_executive_summary()
            with open(output_dir / "Executive_Summary.md", "w", encoding="utf-8") as f:
                f.write(summary)

        logger.info(f"💾 Evolution results saved to: {output_dir}")
        return output_dir

    def _generate_executive_summary(self) -> str:
        """Generate executive summary from analysis data."""
        if not self.final_analysis:
            return "# Executive Summary\n\nNo analysis data available."

        analysis = self.final_analysis

        summary = f"""# Executive Summary: {analysis.product_name}

## Overview
{analysis.elevator_pitch}

## Market Opportunity
- **Market Size:** ${analysis.market_data.market_size_usd:,}
- **Annual Growth Rate:** {analysis.market_data.growth_rate_annual:.1%}
- **Target Customers:** {analysis.market_data.target_customer_count:,}
- **Seasonal Peak Multiplier:** {analysis.market_data.seasonal_peak_multiplier}x

## Financial Projections
- **Funding Required:** ${analysis.funding_requirements:,}
- **Break-even Month:** {analysis.break_even_month}
- **Customer Acquisition Cost:** ${analysis.market_data.customer_acquisition_cost}
- **Customer Lifetime Value:** ${analysis.market_data.lifetime_value}

## SEO Strategy
- **Primary Keywords:** {len(analysis.seo_opportunities)} opportunities identified
- **Top Keywords:**
"""

        # Add top 3 SEO keywords
        for i, seo in enumerate(analysis.seo_opportunities[:3]):
            summary += f"  {i+1}. **{seo.keyword}** - {seo.monthly_search_volume:,} monthly searches\n"

        summary += f"""
## Competition Analysis
- **Main Competitors:** {len(analysis.competitors)} analyzed
"""

        # Add top competitors
        for i, comp in enumerate(analysis.competitors[:3]):
            summary += f"  {i+1}. **{comp.name}** - {comp.market_share_percent:.1f}% market share\n"

        summary += f"""
## Core Features
"""
        for i, feature in enumerate(analysis.core_features[:5]):
            summary += f"{i+1}. {feature}\n"

        summary += f"""
## Launch Timeline
Target season: **{self.config.target_season}**
Launch window: **{self.config.launch_timeline_months} months**

## Key Success Metrics
"""
        for kpi in analysis.kpi_targets[:3]:
            summary += f"- {kpi}\n"

        summary += f"""
## Evolution Fitness Score
**{self.calculate_evolution_fitness():.3f}/1.0** - Genetic algorithm optimization score

---
*Generated by ShinkaEvolve Startup Agent*
*Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        return summary

    async def close(self):
        """Close web research connection."""
        await self.web_research.close()

# EVOLVE-BLOCK-END

def run_evolving_startup_analysis():
    """Main function for evolving startup analysis."""

    # Christmas AI greeting card idea for 2025-2026 season
    startup_idea = """
    AI-powered Christmas greeting card generator targeting USA consumers for Christmas 2025-2026 season.
    Focus on SEO-driven organic traffic capture during October-December peak search period.
    Creates personalized holiday cards with AI-generated images and messages.
    Launch in 3 months (January 2025) to capture pre-season content creation and SEO positioning.
    Revenue model: freemium digital cards + premium print/mail + corporate bulk packages.
    """

    # Evolution config (these parameters will be mutated by ShinkaEvolve)
    config = StartupAgentEvolutionConfig(
        market_research_depth=2,
        competitor_analysis_depth=2,
        seo_keyword_research_depth=3,
        strategy_count=3,
        strategy_iteration_count=2,
        market_size_weight=0.20,
        seo_opportunity_weight=0.35,  # Higher weight for SEO focus
        competition_weight=0.25,
        execution_feasibility_weight=0.15,
        seasonal_timing_weight=0.05,
        temperature=0.7,
        model_selection_strategy="best_quality",
        target_season="Christmas 2025-2026",
        launch_timeline_months=3,
        primary_seo_focus="seasonal_surge",
        quantitative_detail_level=9,
        seo_metrics_count=12
    )

    agent = EvolvingStartupAgent(config)

    try:
        # Run evolving analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        final_analysis = loop.run_until_complete(
            agent.analyze_startup_idea_evolving(startup_idea)
        )

        # Calculate fitness
        fitness = agent.calculate_evolution_fitness()

        # Save results - try to save in current directory if it's a ShinkaEvolve generation
        import os
        current_dir = os.getcwd()

        # Check if we're in a ShinkaEvolve generation directory
        if 'gen_' in current_dir and 'results' in current_dir:
            # We're in a generation/results directory, save here
            output_dir = agent.save_evolution_results(current_dir)
        else:
            # Use default behavior (create timestamp directory)
            output_dir = agent.save_evolution_results()

        # Display key results
        print(f"\n🧬 EVOLVING STARTUP ANALYSIS RESULTS")
        print(f"=" * 60)
        print(f"🎯 Product: {final_analysis.product_name}")
        print(f"📊 Fitness Score: {fitness:.3f}")
        print(f"💰 Market Size: ${final_analysis.market_data.market_size_usd:,}")
        print(f"🔍 SEO Keywords: {len(final_analysis.seo_opportunities)}")
        print(f"🏢 Competitors: {len(final_analysis.competitors)}")
        print(f"📈 Break-even: Month {final_analysis.break_even_month}")
        print(f"💎 Funding: ${final_analysis.funding_requirements:,}")
        print(f"📁 Saved to: {output_dir}")

        return {
            "combined_score": fitness,
            "correct": True,
            "public_metrics": {
                "fitness_score": fitness,
                "market_size_usd": final_analysis.market_data.market_size_usd,
                "seo_opportunities_count": len(final_analysis.seo_opportunities),
                "competitors_count": len(final_analysis.competitors),
                "break_even_month": final_analysis.break_even_month,
                "funding_requirements": final_analysis.funding_requirements,
                "features_count": len(final_analysis.core_features)
            },
            "private_metrics": {
                "evolution_config": config.__dict__,
                "analysis_result": final_analysis
            },
            "text_feedback": f"Fitness: {fitness:.3f}, Market: ${final_analysis.market_data.market_size_usd:,}, SEO: {len(final_analysis.seo_opportunities)} keywords"
        }

    except Exception as e:
        logger.error(f"❌ Evolving analysis failed: {e}")
        return {
            "combined_score": 0.0,
            "correct": False,
            "public_metrics": {"error": str(e)},
            "private_metrics": {},
            "text_feedback": f"Evolution failed: {str(e)}"
        }
    finally:
        loop.run_until_complete(agent.close())
        loop.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_evolving_startup_analysis()
    print(f"\n📊 Evolution Result: {json.dumps(result, indent=2, default=str)}")