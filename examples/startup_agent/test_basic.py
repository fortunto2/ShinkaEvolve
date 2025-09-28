#!/usr/bin/env python3
"""
Basic test for startup agent with simplified schemas.
"""

import json
import logging
from shinka.llm import LLMClient
from pydantic import BaseModel, Field
from typing import List

logger = logging.getLogger(__name__)

# Simplified schema for testing
class SimpleStartupPRD(BaseModel):
    """Simplified PRD for testing."""
    product_name: str = Field(description="Product name")
    vision: str = Field(description="Product vision statement")
    target_market: str = Field(description="Primary target market")
    value_proposition: str = Field(description="Core value proposition")
    key_features: List[str] = Field(description="List of key features")
    success_metrics: List[str] = Field(description="Key performance indicators")

def test_basic_prd_generation():
    """Test basic PRD generation with simplified schema."""

    logging.basicConfig(level=logging.INFO)

    startup_idea = """
    AI-powered task management app that learns user patterns
    and automatically prioritizes tasks.
    """

    # Create LLM client with simplified schema
    prd_llm = LLMClient(
        model_names=["gpt-5-mini"],
        output_model=SimpleStartupPRD,
        verbose=True
    )

    prompt = f"""
    Create a Product Requirements Document for this startup idea:

    STARTUP IDEA: {startup_idea}

    Provide:
    1. Product name (concise, memorable)
    2. Vision statement (1-2 sentences)
    3. Target market (specific customer segment)
    4. Value proposition (unique benefit)
    5. Key features (3-5 core features)
    6. Success metrics (3-5 measurable KPIs)

    Keep responses concise and specific.
    """

    try:
        result = prd_llm.query(
            msg=prompt,
            system_msg="You are a product manager creating concise PRDs. Be specific and actionable.",
            msg_history=[]
        )

        if result and hasattr(result, 'parsed_content') and result.parsed_content:
            prd = result.parsed_content
            print(f"\n✅ PRD Generated Successfully!")
            print(f"🎯 Product: {prd.product_name}")
            print(f"📋 Vision: {prd.vision}")
            print(f"🏢 Target: {prd.target_market}")
            print(f"💡 Value: {prd.value_proposition}")
            print(f"🔧 Features ({len(prd.key_features)}):")
            for i, feature in enumerate(prd.key_features, 1):
                print(f"   {i}. {feature}")
            print(f"📊 Metrics ({len(prd.success_metrics)}):")
            for i, metric in enumerate(prd.success_metrics, 1):
                print(f"   {i}. {metric}")

            return {
                "prd": prd,
                "success": True,
                "features_count": len(prd.key_features),
                "metrics_count": len(prd.success_metrics)
            }
        else:
            print("❌ No parsed content received")
            return {"success": False, "error": "No parsed content"}

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    result = test_basic_prd_generation()
    print(f"\n📊 Test Result: {json.dumps(result, indent=2, default=str)}")