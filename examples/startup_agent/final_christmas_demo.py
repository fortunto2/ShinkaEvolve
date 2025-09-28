#!/usr/bin/env python3
"""
Final demo of Christmas startup agent with proper results saving.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from shinka.llm import LLMClient
from tavily_integration import TavilyWebResearch
from pydantic import BaseModel, Field
from typing import List

logger = logging.getLogger(__name__)

class ChristmasStartupResult(BaseModel):
    """Complete startup analysis result."""
    product_name: str = Field(description="Product name")
    vision: str = Field(description="Product vision")
    target_market: str = Field(description="Target market")
    value_proposition: str = Field(description="Value proposition")
    key_features: List[str] = Field(description="Core features")
    monetization_strategy: str = Field(description="Revenue model")
    marketing_channels: List[str] = Field(description="Marketing channels")
    success_metrics: List[str] = Field(description="Success KPIs")
    key_risks: List[str] = Field(description="Main risks")
    competitive_advantages: List[str] = Field(description="Competitive advantages")

async def run_christmas_startup_demo():
    """Run complete Christmas startup analysis demo."""

    logging.basicConfig(level=logging.INFO)

    christmas_idea = """
    AI-powered Christmas greeting card generator targeting USA consumers in 2024.
    Creates personalized holiday cards with custom messages, AI-generated images,
    and designs. Users input recipient details and preferences, AI generates unique cards
    that can be sent digitally or printed. Focus on December 2024 seasonal opportunity.
    """

    logger.info("🎄 Starting Christmas Startup Analysis Demo")

    # Web research phase
    logger.info("🔍 Phase 1: Market Research")
    research = TavilyWebResearch("http://localhost:8013")

    try:
        # Research market data
        market_data = await research.research_market_size(
            "Christmas greeting cards AI USA market size 2024"
        )

        competitor_data = await research.research_competitors(
            "AI Christmas card generators Canva Hallmark competition"
        )

        trends_data = await research.research_trends(
            "Christmas digital greeting cards trends 2024 AI personalization"
        )

        logger.info(f"📊 Market research completed")
        logger.info(f"   Market data: {len(market_data)} chars")
        logger.info(f"   Competitor data: {len(competitor_data)} chars")
        logger.info(f"   Trends data: {len(trends_data)} chars")

        # Analysis phase
        logger.info("🎯 Phase 2: Strategy Analysis")

        research_context = f"""
        MARKET RESEARCH:
        {market_data[:1000]}...

        COMPETITOR ANALYSIS:
        {competitor_data[:1000]}...

        TRENDS ANALYSIS:
        {trends_data[:800]}...
        """

        # Generate comprehensive startup analysis
        startup_llm = LLMClient(
            model_names=["gpt-5-mini"],
            output_model=ChristmasStartupResult,
            verbose=True
        )

        analysis_prompt = f"""
        Create comprehensive startup analysis for Christmas AI greeting card generator:

        STARTUP IDEA: {christmas_idea}

        {research_context}

        Based on market research, create complete startup strategy including:
        1. Product positioning for Christmas 2024 market
        2. Specific AI features for greeting card generation
        3. Competitive differentiation from existing players
        4. Seasonal marketing strategy for Oct-Dec 2024
        5. Revenue model suitable for seasonal business
        6. Success metrics for holiday season
        7. Key risks and mitigation strategies
        8. Competitive advantages in AI greeting card space

        Focus on USA market, Christmas season timing, and AI differentiation.
        """

        result = startup_llm.query(
            msg=analysis_prompt,
            system_msg="You are a startup strategist specializing in seasonal AI consumer products for USA market.",
            msg_history=[]
        )

        if result and result.parsed_content:
            startup_result = result.parsed_content

            # Save results in ShinkaEvolve format
            logger.info("💾 Phase 3: Saving Results")

            base_results = Path("/Users/rustam/projects/ShinkaEvolve/results")
            timestamp = datetime.now().strftime("%Y.%m.%d%H%M%S")
            output_dir = base_results / "startup_agent" / timestamp
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save complete analysis
            analysis_data = {
                "timestamp": datetime.now().isoformat(),
                "startup_idea": christmas_idea,
                "market_research": {
                    "market_data_length": len(market_data),
                    "competitor_data_length": len(competitor_data),
                    "trends_data_length": len(trends_data)
                },
                "analysis_result": {
                    "product_name": startup_result.product_name,
                    "vision": startup_result.vision,
                    "target_market": startup_result.target_market,
                    "value_proposition": startup_result.value_proposition,
                    "key_features": startup_result.key_features,
                    "monetization_strategy": startup_result.monetization_strategy,
                    "marketing_channels": startup_result.marketing_channels,
                    "success_metrics": startup_result.success_metrics,
                    "key_risks": startup_result.key_risks,
                    "competitive_advantages": startup_result.competitive_advantages
                }
            }

            # Save main result
            with open(output_dir / "christmas_startup_analysis.json", "w") as f:
                json.dump(analysis_data, f, indent=2)

            # Save market research
            with open(output_dir / "market_research.txt", "w") as f:
                f.write(f"MARKET DATA:\n{market_data}\n\n")
                f.write(f"COMPETITOR DATA:\n{competitor_data}\n\n")
                f.write(f"TRENDS DATA:\n{trends_data}\n")

            logger.info(f"💾 Results saved to: {output_dir}")

            # Display results
            print(f"\n🎄 CHRISTMAS AI GREETING CARD GENERATOR")
            print(f"=" * 60)
            print(f"🎯 Product: {startup_result.product_name}")
            print(f"📋 Vision: {startup_result.vision}")
            print(f"🏢 Target: {startup_result.target_market}")
            print(f"💡 Value: {startup_result.value_proposition}")

            print(f"\n🔧 Key Features ({len(startup_result.key_features)}):")
            for i, feature in enumerate(startup_result.key_features, 1):
                print(f"   {i}. {feature}")

            print(f"\n💰 Monetization: {startup_result.monetization_strategy}")

            print(f"\n📈 Marketing Channels ({len(startup_result.marketing_channels)}):")
            for i, channel in enumerate(startup_result.marketing_channels, 1):
                print(f"   {i}. {channel}")

            print(f"\n📊 Success Metrics ({len(startup_result.success_metrics)}):")
            for i, metric in enumerate(startup_result.success_metrics, 1):
                print(f"   {i}. {metric}")

            print(f"\n⚠️ Key Risks ({len(startup_result.key_risks)}):")
            for i, risk in enumerate(startup_result.key_risks, 1):
                print(f"   {i}. {risk}")

            print(f"\n🏆 Competitive Advantages ({len(startup_result.competitive_advantages)}):")
            for i, advantage in enumerate(startup_result.competitive_advantages, 1):
                print(f"   {i}. {advantage}")

            print(f"\n📁 Results saved to: {output_dir}")

            return {
                "success": True,
                "product_name": startup_result.product_name,
                "features_count": len(startup_result.key_features),
                "metrics_count": len(startup_result.success_metrics),
                "risks_count": len(startup_result.key_risks),
                "advantages_count": len(startup_result.competitive_advantages),
                "output_directory": str(output_dir),
                "market_research_chars": len(market_data) + len(competitor_data) + len(trends_data)
            }

        else:
            logger.error("❌ No analysis result generated")
            return {"success": False, "error": "No analysis generated"}

    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        return {"success": False, "error": str(e)}
    finally:
        await research.close()

if __name__ == "__main__":
    result = asyncio.run(run_christmas_startup_demo())

    if result["success"]:
        print(f"\n✅ Christmas Startup Demo Completed Successfully!")
        print(f"🎯 Product: {result['product_name']}")
        print(f"🔧 Features: {result['features_count']}")
        print(f"📊 Metrics: {result['metrics_count']}")
        print(f"⚠️ Risks: {result['risks_count']}")
        print(f"🏆 Advantages: {result['advantages_count']}")
        print(f"📄 Market Research: {result['market_research_chars']} characters")
        print(f"📁 Saved to: {result['output_directory']}")
    else:
        print(f"\n❌ Demo failed: {result['error']}")