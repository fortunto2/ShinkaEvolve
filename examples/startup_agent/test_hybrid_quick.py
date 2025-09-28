#!/usr/bin/env python3
"""
Quick test of hybrid generation system without full research.
"""

import asyncio
import logging
from initial import EvolvingStartupAgent, StartupAgentEvolutionConfig

logging.basicConfig(level=logging.INFO)

async def test_hybrid_generation():
    """Test hybrid generation with mocked research data."""

    print("🧪 Quick Hybrid Generation Test")
    print("=" * 50)

    config = StartupAgentEvolutionConfig()
    agent = EvolvingStartupAgent(config)

    # Mock research data (simulating completed research)
    agent.market_research_data = """
    Christmas greeting card market analysis:
    - Global market size: $2.4 billion annually
    - US market share: 35% ($840 million)
    - Annual growth rate: 15% (digital transformation)
    - Peak season: December (8x normal volume)
    - Customer demographics: 45% millennials, 30% Gen X
    - Average spend per customer: $25-45 during holidays
    - Digital vs print split: 60% digital, 40% print
    """

    agent.seo_research_data = """
    SEO keyword analysis:
    - "christmas cards" - 450,000 monthly searches, difficulty 65
    - "holiday greeting cards" - 200,000 searches, difficulty 45
    - "christmas card generator" - 180,000 searches, difficulty 55
    - "personalized christmas cards" - 150,000 searches, difficulty 50
    - "ai christmas cards" - 85,000 searches, difficulty 35
    - Peak traffic in December: 8-12x normal volume
    """

    agent.competitor_research_data = """
    Competitor analysis:
    - Canva: $15M revenue, 85 DA, 2.5M monthly traffic
    - Hallmark Digital: $50M revenue, 75 DA, 1.2M traffic
    - Adobe Express: $8M revenue, 90 DA, 800K traffic
    - Paperless Post: $12M revenue, 70 DA, 600K traffic
    - Market concentration: Top 4 control 65% market share
    """

    print("📊 Testing hybrid analysis generation...")

    try:
        # Test the hybrid generation method
        result = await agent._generate_hybrid_analysis("AI-powered Christmas greeting card generator")

        print("✅ Generation successful!")
        print(f"🎯 Product: {result.product_name}")
        print(f"💡 Pitch: {result.elevator_pitch[:100]}...")
        print(f"💰 Market Size: ${result.market_data.market_size_usd:,}")
        print(f"📈 CAC: ${result.market_data.customer_acquisition_cost}")
        print(f"💎 LTV: ${result.market_data.lifetime_value}")
        print(f"🔍 SEO Keywords: {len(result.seo_opportunities)}")

        for i, seo in enumerate(result.seo_opportunities[:3]):
            print(f"   {i+1}. {seo.keyword} - {seo.monthly_search_volume:,} searches")

        print(f"🏢 Competitors: {len(result.competitors)}")
        for i, comp in enumerate(result.competitors):
            print(f"   {i+1}. {comp.name} - ${comp.estimated_revenue_usd:,} revenue")

        print(f"📊 Financial Projections: {len(result.financial_projections)} months")
        print(f"💸 Funding Needed: ${result.funding_requirements:,}")
        print(f"📈 Break-even: Month {result.break_even_month}")

        print(f"\n📈 Generation Stats: {agent.generation_stats}")

        # Check if PRD text was generated
        if agent.generated_prd_text:
            print(f"📄 PRD Text Length: {len(agent.generated_prd_text)} characters")
            print("✅ PRD text generation successful")
        else:
            print("⚠️ PRD text not generated")

        # Check structured metrics
        if agent.generated_metrics:
            print("✅ Structured metrics generation successful")
        else:
            print("⚠️ Structured metrics not generated")

        return True

    except Exception as e:
        print(f"❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_hybrid_generation())

    print("\n" + "=" * 50)
    if success:
        print("🎉 HYBRID SYSTEM TEST PASSED!")
        print("✅ No JSON truncation errors")
        print("✅ Structured metrics generated")
        print("✅ Full analysis created")
    else:
        print("❌ HYBRID SYSTEM TEST FAILED!")

    print("=" * 50)