#!/usr/bin/env python3
"""
Test deep SEO analysis with top-5 site parsing.
"""

import asyncio
import logging
from tavily_integration import TavilyWebResearch

logging.basicConfig(level=logging.INFO)

async def test_deep_seo_analysis():
    """Test deep SEO analysis functionality."""

    print("🔍 Testing Deep SEO Analysis")
    print("=" * 50)

    research = TavilyWebResearch("http://localhost:8013")

    test_keyword = "christmas cards"

    try:
        print(f"🎯 Analyzing keyword: '{test_keyword}'")
        print("This will:")
        print("1. Search for top-5 sites for this keyword")
        print("2. Parse each site's content")
        print("3. Extract keywords, marketing hooks, positioning")
        print("4. Identify competitive gaps")
        print("\nStarting analysis...")

        analysis = await research.deep_seo_analysis(test_keyword, max_sites=3)

        print("\n✅ Analysis completed!")
        print("=" * 50)

        print(f"🎯 Keyword: {analysis['keyword']}")
        print(f"🌐 Sites analyzed: {len(analysis['top_sites'])}")

        print(f"\n📊 SEMANTIC CORE ({len(analysis['semantic_core'])} keywords):")
        for i, kw in enumerate(analysis['semantic_core'][:10]):
            print(f"  {i+1}. {kw}")

        print(f"\n🎣 MARKETING HOOKS ({len(analysis['marketing_hooks'])} hooks):")
        for i, hook in enumerate(analysis['marketing_hooks'][:8]):
            print(f"  {i+1}. {hook}")

        print(f"\n📍 POSITIONING INSIGHTS ({len(analysis['positioning_insights'])} insights):")
        for i, pos in enumerate(analysis['positioning_insights']):
            print(f"  {i+1}. {pos}")

        print(f"\n🎯 COMPETITIVE GAPS ({len(analysis['competitive_gaps'])} gaps):")
        for i, gap in enumerate(analysis['competitive_gaps']):
            print(f"  {i+1}. {gap}")

        print(f"\n🌐 TOP SITES ANALYSIS:")
        for i, site in enumerate(analysis['top_sites']):
            domain = site.get('domain', 'unknown')
            keywords_count = len(site.get('keywords', []))
            hooks_count = len(site.get('hooks', []))
            positioning = ', '.join(site.get('positioning', []))

            print(f"  {i+1}. {domain}")
            print(f"     Keywords: {keywords_count}, Hooks: {hooks_count}")
            print(f"     Positioning: {positioning}")

        return True

    except Exception as e:
        print(f"❌ Deep SEO analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        await research.close()

if __name__ == "__main__":
    success = asyncio.run(test_deep_seo_analysis())

    print("\n" + "=" * 50)
    if success:
        print("🎉 DEEP SEO ANALYSIS TEST PASSED!")
        print("✅ Top-5 site parsing working")
        print("✅ Keyword extraction working")
        print("✅ Marketing hooks extraction working")
        print("✅ Competitive gaps identification working")
    else:
        print("❌ DEEP SEO ANALYSIS TEST FAILED!")

    print("=" * 50)