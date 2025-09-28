#!/usr/bin/env python3
"""
Quick test to generate PRD and see actual outputs
"""

import asyncio
import json
from initial import run_evolving_startup_analysis

def test_prd_creation():
    """Test PRD generation with minimal timeout."""
    print("🧬 Testing PRD generation...")

    # Run with shorter timeout for testing
    result = run_evolving_startup_analysis()

    if result.get("correct"):
        print("✅ Analysis successful!")

        # Look for PRD-related outputs
        public_metrics = result.get("public_metrics", {})

        print("\n📊 Key Metrics:")
        print(f"Market Size: ${public_metrics.get('market_size_usd', 0):,}")
        print(f"SEO Opportunities: {public_metrics.get('seo_opportunities_count', 0)}")
        print(f"Competitors: {public_metrics.get('competitors_count', 0)}")
        print(f"Break-even Month: {public_metrics.get('break_even_month', 'N/A')}")
        print(f"Funding: ${public_metrics.get('funding_requirements', 0):,}")

        # Check for saved files
        print("\n📁 Looking for saved files...")
        import os
        for root, dirs, files in os.walk('.'):
            for file in files:
                if any(keyword in file.lower() for keyword in ['prd', 'analysis', 'startup', 'result']):
                    print(f"Found: {os.path.join(root, file)}")

    else:
        print("❌ Analysis failed:")
        print(result.get("public_metrics", {}).get("error", "Unknown error"))

    return result

if __name__ == "__main__":
    result = test_prd_creation()
    print(f"\n🎯 Final Result: {json.dumps(result, indent=2, default=str)}")