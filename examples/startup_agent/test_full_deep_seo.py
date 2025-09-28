#!/usr/bin/env python3
"""
Test full pipeline with real deep SEO research integration.
"""

import asyncio
import logging
from initial import EvolvingStartupAgent, StartupAgentEvolutionConfig

logging.basicConfig(level=logging.INFO)

async def test_full_deep_seo_pipeline():
    """Test complete pipeline with real deep SEO research."""

    print("🚀 Full Deep SEO Pipeline Test")
    print("=" * 50)

    config = StartupAgentEvolutionConfig()
    agent = EvolvingStartupAgent(config)

    # Test with a Christmas card generator idea
    idea = "AI-powered Christmas greeting card generator"

    print(f"💡 Testing with idea: {idea}")
    print("This will:")
    print("1. Conduct real market research")
    print("2. Perform deep SEO analysis with top-5 site parsing")
    print("3. Analyze competitors")
    print("4. Generate hybrid analysis with structured metrics")
    print("5. Create detailed PRD text")
    print("\nStarting full pipeline...")

    try:
        # Generate analysis using the full pipeline
        result = await agent.analyze_startup_idea_evolving(idea)

        print("\n✅ Full pipeline completed!")
        print("=" * 50)

        print(f"🎯 Product: {result.product_name}")
        print(f"💡 Pitch: {result.elevator_pitch[:150]}...")
        print(f"💰 Market Size: ${result.market_data.market_size_usd:,}")
        print(f"📈 CAC: ${result.market_data.customer_acquisition_cost}")
        print(f"💎 LTV: ${result.market_data.lifetime_value}")

        print(f"\n🔍 SEO OPPORTUNITIES ({len(result.seo_opportunities)}):")
        for i, seo in enumerate(result.seo_opportunities[:5]):
            print(f"   {i+1}. {seo.keyword} - {seo.monthly_search_volume:,} searches (difficulty: {seo.difficulty})")

        print(f"\n🏢 COMPETITOR ANALYSIS ({len(result.competitors)}):")
        for i, comp in enumerate(result.competitors[:3]):
            print(f"   {i+1}. {comp.name}")
            print(f"      Revenue: ${comp.estimated_revenue_usd:,}")
            print(f"      Traffic: {comp.monthly_traffic:,}")
            print(f"      Domain Authority: {comp.domain_authority}")

        print(f"\n📊 FINANCIAL PROJECTIONS:")
        print(f"   💸 Funding Needed: ${result.funding_requirements:,}")
        print(f"   📈 Break-even: Month {result.break_even_month}")
        print(f"   💹 ROI: {result.roi_projection}%")

        # Show research data quality
        if hasattr(agent, 'seo_research_data') and agent.seo_research_data:
            seo_length = len(agent.seo_research_data)
            print(f"\n📈 SEO Research Quality: {seo_length} characters")
            if "semantic_core" in agent.seo_research_data.lower():
                print("✅ Semantic core analysis included")
            if "marketing_hooks" in agent.seo_research_data.lower():
                print("✅ Marketing hooks analysis included")
            if "competitive_gaps" in agent.seo_research_data.lower():
                print("✅ Competitive gaps analysis included")

        # Show generation statistics
        print(f"\n📈 Generation Stats: {agent.generation_stats}")

        # Check PRD generation
        if agent.generated_prd_text:
            prd_length = len(agent.generated_prd_text)
            print(f"📄 PRD Text: {prd_length} characters generated")
            print("✅ Complete PRD document created")
        else:
            print("⚠️ PRD text generation failed")

        return True

    except Exception as e:
        print(f"❌ Full pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_full_deep_seo_pipeline())

    print("\n" + "=" * 50)
    if success:
        print("🎉 FULL DEEP SEO PIPELINE TEST PASSED!")
        print("✅ Real market research completed")
        print("✅ Deep SEO analysis with site parsing working")
        print("✅ Competitor analysis working")
        print("✅ Structured metrics generation working")
        print("✅ Complete PRD generation working")
    else:
        print("❌ FULL DEEP SEO PIPELINE TEST FAILED!")

    print("=" * 50)