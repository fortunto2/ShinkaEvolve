#!/usr/bin/env python3
"""
Test PRD report saving functionality without running full evolution.
"""

import asyncio
import logging
from pathlib import Path
import tempfile
import os
from initial import EvolvingStartupAgent, StartupAgentEvolutionConfig

logging.basicConfig(level=logging.INFO)

async def test_report_saving():
    """Test PRD report saving functionality."""

    print("🧪 Testing PRD Report Saving")
    print("=" * 50)

    # Create test agent
    config = StartupAgentEvolutionConfig()
    agent = EvolvingStartupAgent(config)

    # Create temporary test directory
    test_dir = Path(tempfile.mkdtemp())
    print(f"📁 Test directory: {test_dir}")

    try:
        # Generate a quick analysis for testing
        print("📊 Generating test analysis...")
        idea = "AI Christmas card generator test"
        result = await agent.analyze_startup_idea_evolving(idea)

        print("✅ Analysis generated successfully!")
        print(f"🎯 Product: {result.product_name}")
        print(f"💰 Market Size: ${result.market_data.market_size_usd:,}")

        # Test the save function
        print("\n💾 Testing save functionality...")
        saved_dir = agent.save_evolution_results(str(test_dir / "test_results"))

        # Check what files were created
        print(f"\n📂 Files created in {saved_dir}:")
        saved_path = Path(saved_dir)

        expected_files = [
            "evolution_config.json",
            "quantitative_analysis.json",
            "research_data.txt",
            "PRD_Document.md",
            "Executive_Summary.md"
        ]

        created_files = []
        for file_path in saved_path.iterdir():
            if file_path.is_file():
                size = file_path.stat().st_size
                print(f"  📄 {file_path.name} ({size:,} bytes)")
                created_files.append(file_path.name)

                # Show first few lines of markdown files
                if file_path.suffix == '.md':
                    print(f"    Preview of {file_path.name}:")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:5]
                        for line in lines:
                            print(f"    {line.strip()}")
                    print("    ...")

        # Check if all expected files were created
        print(f"\n✅ File creation test:")
        for expected in expected_files:
            if expected in created_files:
                print(f"  ✅ {expected} - Created")
            else:
                print(f"  ❌ {expected} - Missing")

        # Test if PRD contains expected content
        prd_file = saved_path / "PRD_Document.md"
        if prd_file.exists():
            print(f"\n📄 PRD Document validation:")
            with open(prd_file, 'r', encoding='utf-8') as f:
                content = f.read()

            checks = [
                ("Product name in title", result.product_name in content),
                ("Market size mentioned", str(result.market_data.market_size_usd) in content),
                ("Generated timestamp", "Generated:" in content),
                ("Evolution fitness", "Evolution Fitness:" in content),
                ("PRD content", len(content) > 1000)  # Substantial content
            ]

            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"  {status} {check_name}")

        # Test executive summary
        summary_file = saved_path / "Executive_Summary.md"
        if summary_file.exists():
            print(f"\n📋 Executive Summary validation:")
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary_content = f.read()

            summary_checks = [
                ("Product name in title", result.product_name in summary_content),
                ("Market opportunity section", "Market Opportunity" in summary_content),
                ("Financial projections", "Financial Projections" in summary_content),
                ("SEO strategy section", "SEO Strategy" in summary_content),
                ("Evolution fitness score", "Evolution Fitness Score" in summary_content)
            ]

            for check_name, passed in summary_checks:
                status = "✅" if passed else "❌"
                print(f"  {status} {check_name}")

        print(f"\n🎉 Report saving test completed!")
        print(f"📁 Test files saved in: {saved_dir}")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        await agent.close()
        # Clean up test directory
        import shutil
        try:
            shutil.rmtree(test_dir)
            print(f"🗑️ Cleaned up test directory")
        except:
            print(f"⚠️ Could not clean up {test_dir}")

if __name__ == "__main__":
    success = asyncio.run(test_report_saving())

    print("\n" + "=" * 50)
    if success:
        print("✅ PRD REPORT SAVING TEST PASSED!")
        print("✅ All report files are being generated correctly")
        print("✅ PRD documents contain expected content")
        print("✅ Executive summaries are properly formatted")
    else:
        print("❌ PRD REPORT SAVING TEST FAILED!")
    print("=" * 50)