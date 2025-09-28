#!/usr/bin/env python3
"""
Quick test of startup agent with minimal research parameters.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from initial import EvolvingStartupAgent, StartupAgentEvolutionConfig

logging.basicConfig(level=logging.INFO)

async def test_quick_startup_analysis():
    """Test startup analysis with minimal parameters for speed."""

    print("⚡ Quick Startup Analysis Test")
    print("=" * 50)

    # Create quick config with minimal research
    config = StartupAgentEvolutionConfig(
        # Minimal research for speed (2 instead of 6, 5, 10)
        market_research_depth=2,
        competitor_analysis_depth=2,
        seo_keyword_research_depth=2,

        # Single strategy for speed
        strategy_count=1,
        strategy_iteration_count=1,

        # Lower detail levels
        quantitative_detail_level=5,
        financial_projection_months=6,
        seo_metrics_count=5,

        # Fast model settings
        temperature=0.5,
        model_selection_strategy="best_quality"
    )

    print(f"📊 Quick Config:")
    print(f"  Market research depth: {config.market_research_depth}")
    print(f"  Competitor analysis depth: {config.competitor_analysis_depth}")
    print(f"  SEO keyword research depth: {config.seo_keyword_research_depth}")
    print(f"  Strategy count: {config.strategy_count}")

    try:
        agent = EvolvingStartupAgent(config)

        # Test idea
        idea = "AI Christmas card generator for 2025-2026 season"

        print(f"\n💡 Testing idea: {idea}")
        print("🚀 Starting quick analysis...")

        # Generate analysis
        result = await agent.analyze_startup_idea_evolving(idea)

        print("\n✅ Quick analysis completed!")
        print("=" * 50)

        # Show key results
        print(f"🎯 Product: {result.product_name}")
        print(f"💰 Market Size: ${result.market_data.market_size_usd:,}")
        print(f"📈 CAC: ${result.market_data.customer_acquisition_cost}")
        print(f"💎 LTV: ${result.market_data.lifetime_value}")
        print(f"💸 Funding: ${result.funding_requirements:,}")
        print(f"📅 Break-even: Month {result.break_even_month}")

        print(f"\n🔍 SEO Opportunities ({len(result.seo_opportunities)}):")
        for i, seo in enumerate(result.seo_opportunities[:3]):
            print(f"  {i+1}. {seo.keyword} - {seo.monthly_search_volume:,} searches")

        print(f"\n🏢 Competitors ({len(result.competitors)}):")
        for i, comp in enumerate(result.competitors[:3]):
            print(f"  {i+1}. {comp.name} - {comp.market_share_percent:.1f}% market share")

        # Test saving results
        print(f"\n💾 Testing save functionality...")
        output_dir = agent.save_evolution_results()

        saved_path = Path(output_dir)
        print(f"📂 Results saved to: {output_dir}")

        # List saved files
        for file_path in saved_path.iterdir():
            if file_path.is_file():
                size = file_path.stat().st_size
                print(f"  📄 {file_path.name} ({size:,} bytes)")

        # Show generation stats
        print(f"\n📈 Generation Stats:")
        for key, value in agent.generation_stats.items():
            print(f"  {key}: {value}")

        return True

    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        await agent.close()

if __name__ == "__main__":
    success = asyncio.run(test_quick_startup_analysis())

    print("\n" + "=" * 50)
    if success:
        print("✅ QUICK STARTUP ANALYSIS TEST PASSED!")
        print("✅ Minimal research parameters working")
        print("✅ PRD generation with reports working")
        print("✅ Ready for fast testing")
    else:
        print("❌ QUICK STARTUP ANALYSIS TEST FAILED!")
    print("=" * 50)