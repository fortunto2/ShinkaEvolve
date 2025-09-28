#!/usr/bin/env python3
"""
Simple test for startup agent without web research.
Tests core SGR functionality and PRD generation.
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import List, Optional

# SGR imports
from shinka.llm import LLMClient
from startup_sgr_schemas import (
    NicheAnalysis, CompetitorProfile, MarketStrategy,
    CriticalEvaluation, StartupPRD, MarketOpportunity,
    CustomerSegment, ValueProposition, MonetizationModel,
    GoToMarketStrategy
)

logger = logging.getLogger(__name__)

@dataclass
class SimpleTestConfig:
    """Simple test configuration."""
    model_names: List[str] = None

    def __post_init__(self):
        if self.model_names is None:
            self.model_names = ["gpt-5-mini"]

class SimpleStartupAgent:
    """Simplified startup agent for testing without web research."""

    def __init__(self, config: SimpleTestConfig):
        self.config = config

        # Initialize LLM client for PRD generation
        self.prd_llm = LLMClient(
            model_names=config.model_names,
            output_model=StartupPRD,
            verbose=True
        )

    async def analyze_startup_simple(self, idea: str) -> StartupPRD:
        """
        Simple startup analysis without web research.
        """
        logger.info(f"🚀 Simple analysis for: '{idea[:50]}...'")

        # Generate PRD directly from idea
        prompt = f"""
        Create a comprehensive Product Requirements Document for this startup idea:

        STARTUP IDEA: {idea}

        Generate a complete PRD including:
        1. Product name and vision
        2. Target market analysis
        3. Core features (5-8 features minimum)
        4. Technical requirements
        5. Value proposition and differentiation
        6. Monetization strategy
        7. Success metrics (3-5 KPIs)
        8. Development milestones
        9. Risk assessment

        Make realistic assumptions about market size and competition.
        Focus on creating a actionable, detailed PRD.
        """

        result = self.prd_llm.query(
            msg=prompt,
            system_msg="You are a senior product manager creating comprehensive PRDs for startups. Be detailed and specific.",
            msg_history=[]
        )

        if result and hasattr(result, 'parsed_content') and result.parsed_content:
            logger.info(f"✅ PRD generated: {result.parsed_content.product_name}")
            return result.parsed_content
        else:
            raise Exception("Failed to generate PRD")

def test_simple_startup_agent():
    """Test simple startup agent."""

    logging.basicConfig(level=logging.INFO)

    startup_idea = """
    A productivity tool that uses AI to automatically organize and prioritize
    daily tasks based on deadlines, importance, and personal work patterns.
    The tool learns from user behavior and integrates with popular calendar
    and project management apps.
    """

    config = SimpleTestConfig(model_names=["gpt-5-mini"])
    agent = SimpleStartupAgent(config)

    try:
        # Run simple analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        prd = loop.run_until_complete(
            agent.analyze_startup_simple(startup_idea)
        )

        # Display results
        print(f"\n🎯 Product: {prd.product_name}")
        print(f"📋 Vision: {prd.vision}")
        print(f"🏢 Target Market: {prd.target_market}")
        print(f"💡 Features: {len(prd.core_features)} features")
        print(f"📊 Metrics: {len(prd.success_metrics)} KPIs")
        print(f"⚠️ Risks: {len(prd.key_risks)} risks identified")

        # Return results for evaluation
        return {
            "prd": prd,
            "iterations": 1,  # Simple test = 1 iteration
            "best_strategy": "Direct PRD generation"
        }

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return {"error": str(e)}
    finally:
        loop.close()

if __name__ == "__main__":
    result = test_simple_startup_agent()
    if "error" not in result:
        print("\n✅ Simple test completed successfully!")
        print(f"📄 PRD generated with {len(result['prd'].core_features)} features")
    else:
        print(f"\n❌ Test failed: {result['error']}")