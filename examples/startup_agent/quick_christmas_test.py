#!/usr/bin/env python3
"""
Quick test of Christmas startup agent with web research.
"""

import asyncio
import json
import logging
from shinka.llm import LLMClient
from tavily_integration import TavilyWebResearch
from pydantic import BaseModel, Field
from typing import List

logger = logging.getLogger(__name__)

class QuickPRD(BaseModel):
    """Quick PRD for Christmas greeting generator."""
    product_name: str = Field(description="Product name")
    vision: str = Field(description="Product vision")
    target_market: str = Field(description="Target market")
    key_features: List[str] = Field(description="Core features")
    monetization: str = Field(description="How to make money")
    success_metrics: List[str] = Field(description="Success metrics")

async def quick_christmas_analysis():
    """Quick analysis with web research."""

    logging.basicConfig(level=logging.INFO)

    christmas_idea = """
    AI-powered Christmas greeting card generator for USA market.
    Creates personalized holiday cards with custom messages and designs.
    """

    # Web research
    logger.info("🔍 Starting web research...")
    research = TavilyWebResearch("http://localhost:8013")

    try:
        # Quick market research
        market_data = await research.research_market_size(
            "Christmas greeting cards market USA 2024"
        )
        logger.info(f"📊 Market research completed: {len(market_data)} chars")

        # Generate PRD with market data
        prd_llm = LLMClient(
            model_names=["gpt-5-mini"],
            output_model=QuickPRD,
            verbose=True
        )

        prompt = f"""
        Create PRD for Christmas AI greeting card generator:

        IDEA: {christmas_idea}

        MARKET RESEARCH: {market_data[:800]}...

        Target USA Christmas market 2024. Include specific Christmas features,
        seasonal marketing approach, and AI capabilities.
        """

        result = prd_llm.query(
            msg=prompt,
            system_msg="You are creating PRD for seasonal AI product targeting Christmas 2024.",
            msg_history=[]
        )

        if result and result.parsed_content:
            prd = result.parsed_content

            print(f"\n🎄 CHRISTMAS GREETING CARD GENERATOR PRD")
            print(f"=" * 50)
            print(f"🎯 Product: {prd.product_name}")
            print(f"📋 Vision: {prd.vision}")
            print(f"🏢 Target: {prd.target_market}")
            print(f"💰 Monetization: {prd.monetization}")

            print(f"\n🔧 Features ({len(prd.key_features)}):")
            for i, feature in enumerate(prd.key_features, 1):
                print(f"   {i}. {feature}")

            print(f"\n📊 Success Metrics ({len(prd.success_metrics)}):")
            for i, metric in enumerate(prd.success_metrics, 1):
                print(f"   {i}. {metric}")

            return {
                "success": True,
                "prd": prd,
                "market_research_length": len(market_data),
                "features_count": len(prd.key_features),
                "metrics_count": len(prd.success_metrics)
            }
        else:
            return {"success": False, "error": "No PRD generated"}

    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        return {"success": False, "error": str(e)}
    finally:
        await research.close()

if __name__ == "__main__":
    result = asyncio.run(quick_christmas_analysis())

    if result["success"]:
        print(f"\n✅ Quick analysis completed!")
        print(f"📄 Market research: {result['market_research_length']} characters")
        print(f"🔧 Features: {result['features_count']}")
        print(f"📊 Metrics: {result['metrics_count']}")
    else:
        print(f"\n❌ Analysis failed: {result['error']}")