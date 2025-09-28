#!/usr/bin/env python3
"""
Run startup agent for Christmas AI greeting card generator idea.
Full pipeline with web research via Tavily.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

# SGR and ShinkaEvolve imports
from shinka.llm import LLMClient

# Simplified schemas for reliable parsing
from pydantic import BaseModel, Field
from typing import Literal

# Web Research Integration
from tavily_integration import TavilyWebResearch

logger = logging.getLogger(__name__)

# Simplified but comprehensive schemas
class MarketInsight(BaseModel):
    """Market research insight."""
    insight: str = Field(description="Key market insight")
    source_type: Literal["trend", "competitor", "demand", "size"] = Field(description="Type of insight")
    confidence: Literal["low", "medium", "high"] = Field(description="Confidence in insight")

class CompetitorInfo(BaseModel):
    """Competitor information."""
    name: str = Field(description="Competitor name or type")
    strengths: List[str] = Field(description="Key strengths")
    weaknesses: List[str] = Field(description="Potential weaknesses")
    market_position: str = Field(description="Market position description")

class StrategyOption(BaseModel):
    """Strategic approach option."""
    strategy_name: str = Field(description="Name of strategy")
    approach: str = Field(description="Strategic approach description")
    target_audience: str = Field(description="Primary target audience")
    value_proposition: str = Field(description="Core value proposition")
    monetization: str = Field(description="How to make money")
    differentiation: str = Field(description="Key differentiator")
    confidence_score: float = Field(ge=0, le=1, description="Confidence in strategy")

class StrategyEvaluation(BaseModel):
    """Evaluation of a strategy."""
    overall_score: float = Field(ge=0, le=1, description="Overall strategy score")
    strengths: List[str] = Field(description="Strategy strengths")
    weaknesses: List[str] = Field(description="Strategy weaknesses")
    market_fit: float = Field(ge=0, le=1, description="Product-market fit score")
    execution_difficulty: Literal["low", "medium", "high"] = Field(description="Execution difficulty")
    recommendations: List[str] = Field(description="Improvement recommendations")

class FinalPRD(BaseModel):
    """Final Product Requirements Document."""
    product_name: str = Field(description="Product name")
    vision: str = Field(description="Product vision")
    target_market: str = Field(description="Primary target market")
    value_proposition: str = Field(description="Core value proposition")

    # Core features
    key_features: List[str] = Field(description="Key product features")
    technical_requirements: List[str] = Field(description="Technical requirements")

    # Business model
    monetization_strategy: str = Field(description="How to make money")
    pricing_model: str = Field(description="Pricing approach")

    # Go-to-market
    marketing_channels: List[str] = Field(description="Marketing channels")
    launch_strategy: str = Field(description="Launch approach")

    # Metrics and validation
    success_metrics: List[str] = Field(description="Key success metrics")
    validation_plan: List[str] = Field(description="How to validate the idea")

    # Risk management
    key_risks: List[str] = Field(description="Main risks")
    risk_mitigation: List[str] = Field(description="Risk mitigation strategies")

@dataclass
class ChristmasAgentConfig:
    """Configuration for Christmas startup agent."""
    model_names: List[str] = None
    tavily_port: int = 8013
    max_strategies: int = 3
    max_iterations: int = 2

    def __post_init__(self):
        if self.model_names is None:
            self.model_names = ["gpt-5-mini"]

class ChristmasStartupAgent:
    """Startup agent for Christmas greeting card generator."""

    def __init__(self, config: ChristmasAgentConfig):
        self.config = config

        # Initialize LLM clients
        self.market_llm = LLMClient(
            model_names=config.model_names,
            output_model=MarketInsight,
            verbose=True
        )

        self.competitor_llm = LLMClient(
            model_names=config.model_names,
            output_model=CompetitorInfo,
            verbose=True
        )

        self.strategy_llm = LLMClient(
            model_names=config.model_names,
            output_model=StrategyOption,
            verbose=True
        )

        self.evaluation_llm = LLMClient(
            model_names=config.model_names,
            output_model=StrategyEvaluation,
            verbose=True
        )

        self.prd_llm = LLMClient(
            model_names=config.model_names,
            output_model=FinalPRD,
            verbose=True
        )

        # Web research
        self.web_research = TavilyWebResearch(f"http://localhost:{config.tavily_port}")

        # Results storage
        self.market_insights: List[MarketInsight] = []
        self.competitors: List[CompetitorInfo] = []
        self.strategies: List[StrategyOption] = []
        self.evaluations: List[StrategyEvaluation] = []
        self.final_prd: Optional[FinalPRD] = None

    async def analyze_christmas_idea(self, idea: str) -> FinalPRD:
        """
        Full analysis pipeline for Christmas greeting card idea.
        """
        logger.info(f"🎄 Starting Christmas startup analysis...")

        # Phase 1: Market Research
        await self._research_market(idea)
        logger.info(f"📊 Market research: {len(self.market_insights)} insights")

        # Phase 2: Competitive Analysis
        await self._research_competitors(idea)
        logger.info(f"🏢 Competitor analysis: {len(self.competitors)} competitors")

        # Phase 3: Strategy Development
        await self._develop_strategies(idea)
        logger.info(f"🎯 Strategy development: {len(self.strategies)} strategies")

        # Phase 4: Strategy Evaluation
        await self._evaluate_strategies()
        logger.info(f"⚖️ Strategy evaluation completed")

        # Phase 5: Final PRD Generation
        final_prd = await self._generate_final_prd(idea)
        logger.info(f"📋 PRD generated: {final_prd.product_name}")

        self.final_prd = final_prd
        return final_prd

    async def _research_market(self, idea: str):
        """Research market for Christmas greeting cards."""

        # Market size research
        market_data = await self.web_research.research_market_size(
            "Christmas greeting cards AI generated USA market"
        )

        # Trends research
        trends_data = await self.web_research.research_trends(
            "Christmas digital greeting cards AI 2024"
        )

        # Generate market insights
        for research_type, data in [("market_size", market_data), ("trends", trends_data)]:
            prompt = f"""
            Analyze this market research data and provide ONE key insight:

            RESEARCH TYPE: {research_type}
            DATA: {data[:1000]}...

            Focus on Christmas greeting card market in USA.
            Provide specific, actionable market insight.
            """

            result = self.market_llm.query(
                msg=prompt,
                system_msg="You are a market research analyst specializing in seasonal digital products.",
                msg_history=[]
            )

            if result and result.parsed_content:
                self.market_insights.append(result.parsed_content)

    async def _research_competitors(self, idea: str):
        """Research competitors in Christmas greeting space."""

        competitor_data = await self.web_research.research_competitors(
            "AI Christmas greeting card generator apps"
        )

        # Generate competitor analysis
        for i in range(2):  # Analyze 2 competitor segments
            prompt = f"""
            Analyze competitors in Christmas greeting card space:

            RESEARCH DATA: {competitor_data[:1500]}...
            FOCUS: {"Direct AI competitors" if i == 0 else "Traditional greeting card companies"}

            Identify ONE main competitor type or specific competitor.
            Focus on Christmas/holiday greeting market in USA.
            """

            result = self.competitor_llm.query(
                msg=prompt,
                system_msg="You are a competitive intelligence analyst for digital products.",
                msg_history=[]
            )

            if result and result.parsed_content:
                self.competitors.append(result.parsed_content)

    async def _develop_strategies(self, idea: str):
        """Develop strategic approaches."""

        # Context from research
        market_context = "\n".join([f"- {insight.insight}" for insight in self.market_insights])
        competitor_context = "\n".join([f"- {comp.name}: {comp.market_position}" for comp in self.competitors])

        strategy_approaches = [
            "AI-first personalized Christmas greeting platform",
            "B2B Christmas marketing automation tool",
            "Social media Christmas content generator"
        ]

        for i, approach in enumerate(strategy_approaches):
            prompt = f"""
            Develop strategic approach for Christmas AI greeting idea:

            STARTUP IDEA: {idea}
            STRATEGIC APPROACH: {approach}

            MARKET INSIGHTS:
            {market_context}

            COMPETITOR LANDSCAPE:
            {competitor_context}

            Create specific strategy for Christmas greeting card generator targeting USA market.
            Focus on seasonal opportunity and AI differentiation.
            """

            result = self.strategy_llm.query(
                msg=prompt,
                system_msg="You are a startup strategist specializing in seasonal digital products.",
                msg_history=[]
            )

            if result and result.parsed_content:
                self.strategies.append(result.parsed_content)

    async def _evaluate_strategies(self):
        """Evaluate and score strategies."""

        for strategy in self.strategies:
            prompt = f"""
            Critically evaluate this Christmas greeting strategy:

            STRATEGY: {strategy.strategy_name}
            APPROACH: {strategy.approach}
            TARGET: {strategy.target_audience}
            VALUE PROP: {strategy.value_proposition}
            MONETIZATION: {strategy.monetization}

            Consider:
            - Christmas seasonal market dynamics
            - AI technology feasibility
            - USA market competition
            - Execution complexity for startup
            - Revenue potential during holiday season

            Provide honest, critical evaluation.
            """

            result = self.evaluation_llm.query(
                msg=prompt,
                system_msg="You are a critical business strategy evaluator. Be thorough and objective.",
                msg_history=[]
            )

            if result and result.parsed_content:
                self.evaluations.append(result.parsed_content)

    async def _generate_final_prd(self, idea: str) -> FinalPRD:
        """Generate comprehensive PRD."""

        # Select best strategy
        best_strategy_idx = 0
        if self.evaluations:
            best_strategy_idx = max(range(len(self.evaluations)),
                                  key=lambda i: self.evaluations[i].overall_score)

        best_strategy = self.strategies[best_strategy_idx] if self.strategies else None
        best_evaluation = self.evaluations[best_strategy_idx] if self.evaluations else None

        # Compile research context
        market_context = "\n".join([f"- {insight.insight}" for insight in self.market_insights])
        competitor_context = "\n".join([f"- {comp.name}" for comp in self.competitors])

        prompt = f"""
        Create comprehensive Product Requirements Document:

        ORIGINAL IDEA: {idea}

        CHOSEN STRATEGY: {best_strategy.strategy_name if best_strategy else "AI Christmas Greeting Generator"}
        APPROACH: {best_strategy.approach if best_strategy else "Direct consumer AI greeting platform"}

        MARKET RESEARCH:
        {market_context}

        COMPETITORS:
        {competitor_context}

        Generate complete PRD for Christmas AI greeting card generator targeting USA market.
        Include specific Christmas/holiday features, seasonal marketing approach,
        and AI technology requirements. Focus on December 2024 launch timing.

        Make it actionable and specific for a startup team.
        """

        result = self.prd_llm.query(
            msg=prompt,
            system_msg="You are a senior product manager creating PRDs for seasonal AI products.",
            msg_history=[]
        )

        return result.parsed_content

    def save_analysis_results(self, output_dir: str = None):
        """Save complete analysis results in ShinkaEvolve format."""

        if output_dir is None:
            # Follow ShinkaEvolve convention: results/{example_name}/{timestamp}/
            base_results = Path("/Users/rustam/projects/ShinkaEvolve/results")
            timestamp = datetime.now().strftime("%Y.%m.%d%H%M%S")
            output_dir = base_results / "startup_agent" / timestamp

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        timestamp_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save market insights
        with open(f"{output_dir}/market_insights_{timestamp_suffix}.json", "w") as f:
            json.dump([{
                "insight": insight.insight,
                "source_type": insight.source_type,
                "confidence": insight.confidence
            } for insight in self.market_insights], f, indent=2)

        # Save competitors
        with open(f"{output_dir}/competitors_{timestamp_suffix}.json", "w") as f:
            json.dump([{
                "name": comp.name,
                "strengths": comp.strengths,
                "weaknesses": comp.weaknesses,
                "position": comp.market_position
            } for comp in self.competitors], f, indent=2)

        # Save strategies and evaluations
        strategy_analysis = []
        for i, (strategy, evaluation) in enumerate(zip(self.strategies, self.evaluations)):
            strategy_analysis.append({
                "strategy_name": strategy.strategy_name,
                "approach": strategy.approach,
                "target_audience": strategy.target_audience,
                "confidence_score": strategy.confidence_score,
                "evaluation_score": evaluation.overall_score,
                "strengths": evaluation.strengths,
                "weaknesses": evaluation.weaknesses,
                "recommendations": evaluation.recommendations
            })

        with open(f"{output_dir}/strategy_analysis_{timestamp_suffix}.json", "w") as f:
            json.dump(strategy_analysis, f, indent=2)

        # Save final PRD
        if self.final_prd:
            with open(f"{output_dir}/final_prd_{timestamp_suffix}.json", "w") as f:
                json.dump({
                    "product_name": self.final_prd.product_name,
                    "vision": self.final_prd.vision,
                    "target_market": self.final_prd.target_market,
                    "value_proposition": self.final_prd.value_proposition,
                    "key_features": self.final_prd.key_features,
                    "technical_requirements": self.final_prd.technical_requirements,
                    "monetization_strategy": self.final_prd.monetization_strategy,
                    "pricing_model": self.final_prd.pricing_model,
                    "marketing_channels": self.final_prd.marketing_channels,
                    "success_metrics": self.final_prd.success_metrics,
                    "key_risks": self.final_prd.key_risks
                }, f, indent=2)

        logger.info(f"💾 Analysis results saved to {output_dir}")

    async def close(self):
        """Close web research connection."""
        await self.web_research.close()

async def run_christmas_analysis():
    """Run full Christmas greeting card analysis."""

    christmas_idea = """
    An AI-powered Christmas greeting card generator that creates personalized,
    beautiful holiday cards with custom messages, images, and designs.
    Users can input recipient details, preferred style, and personal messages,
    and the AI generates unique Christmas cards that can be sent digitally
    or printed. Target market is USA consumers during Christmas season 2024.
    """

    config = ChristmasAgentConfig(
        model_names=["gpt-5-mini"],
        tavily_port=8013,
        max_strategies=3,
        max_iterations=2
    )

    agent = ChristmasStartupAgent(config)

    try:
        # Run full analysis
        final_prd = await agent.analyze_christmas_idea(christmas_idea)

        # Save results
        agent.save_analysis_results()

        # Display summary
        print(f"\n🎄 CHRISTMAS GREETING CARD GENERATOR ANALYSIS")
        print(f"=" * 60)
        print(f"🎯 Product: {final_prd.product_name}")
        print(f"📋 Vision: {final_prd.vision}")
        print(f"🏢 Target: {final_prd.target_market}")
        print(f"💡 Value: {final_prd.value_proposition}")
        print(f"\n🔧 Key Features ({len(final_prd.key_features)}):")
        for i, feature in enumerate(final_prd.key_features, 1):
            print(f"   {i}. {feature}")
        print(f"\n💰 Monetization: {final_prd.monetization_strategy}")
        print(f"📊 Success Metrics ({len(final_prd.success_metrics)}):")
        for i, metric in enumerate(final_prd.success_metrics, 1):
            print(f"   {i}. {metric}")
        print(f"\n⚠️ Key Risks ({len(final_prd.key_risks)}):")
        for i, risk in enumerate(final_prd.key_risks, 1):
            print(f"   {i}. {risk}")

        return {
            "prd": final_prd,
            "market_insights": len(agent.market_insights),
            "competitors": len(agent.competitors),
            "strategies": len(agent.strategies),
            "success": True
        }

    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        return {"error": str(e), "success": False}

    finally:
        await agent.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = asyncio.run(run_christmas_analysis())

    if result.get("success"):
        print(f"\n✅ Analysis completed successfully!")
        print(f"📊 Market insights: {result['market_insights']}")
        print(f"🏢 Competitors analyzed: {result['competitors']}")
        print(f"🎯 Strategies evaluated: {result['strategies']}")
    else:
        print(f"\n❌ Analysis failed: {result.get('error')}")