import os
import json
import time
import argparse
import importlib.util
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from shinka.utils.tavily_search import TavilySearchService


class PydanticJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles Pydantic models and datetime objects."""
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def evaluate_advanced_seo_research_quality(
    program_path: str,
    results_dir: str,
    test_niches: List[str] = ["ai generate christmas card 2026", "ai christmas card generator", "personalized christmas cards ai"],
    use_tavily_search: bool = True,
    max_search_results: int = 3,
    enable_content_analysis: bool = True
):
    """
    Evaluate the quality of advanced SEO research strategies with competitor content analysis.
    """
    # Load the program module
    spec = importlib.util.spec_from_file_location("program", program_path)
    if spec is None:
        print(f"Error: Could not load spec for module at {program_path}")
        return
    if spec.loader is None:
        print(f"Error: No loader found for module at {program_path}")
        return

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    start_t = time.time()
    error = ""
    correct = True

    try:
        # Run the advanced SEO research experiment
        research_results = module.run_experiment(test_niches)

        # Calculate quality metrics with enhanced scoring
        total_score = 0
        detailed_scores = {}

        for result in research_results:
            niche = result["niche"]
            strategy = result["strategy"]  # Now an AdvancedSEOStrategy Pydantic model

            # Enhanced scoring criteria for advanced strategy

            # 1. Keyword diversity and quality (25% weight)
            keyword_count = len(strategy.primary_keywords)
            keyword_diversity_score = min(keyword_count / 20.0, 1.0)  # Target: 20+ keywords

            # Keyword intent diversity bonus
            intents = set(kw.search_intent for kw in strategy.primary_keywords)
            intent_diversity_bonus = len(intents) / 4.0  # Max 4 intent types
            keyword_diversity_score = min(1.0, keyword_diversity_score + intent_diversity_bonus * 0.2)

            # 2. Competitor analysis depth (20% weight)
            competitor_count = len(strategy.competitor_analyses)
            competitor_analysis_score = min(competitor_count / 15.0, 1.0)  # Target: 15+ competitors

            # Content analysis bonus
            competitors_with_content = sum(1 for comp in strategy.competitor_analyses if comp.content_data)
            if competitor_count > 0:
                content_analysis_bonus = competitors_with_content / competitor_count
                competitor_analysis_score = min(1.0, competitor_analysis_score + content_analysis_bonus * 0.3)

            # 3. Strategy comprehensiveness (15% weight)
            strategy_count = len(strategy.search_strategies)
            strategy_depth_score = min(strategy_count / 15.0, 1.0)  # Target: 15+ strategies

            # 4. Keyword opportunity quality (25% weight)
            keyword_quality_score = 0.0

            if strategy.primary_keywords:
                # Analyze keyword opportunities
                low_competition_keywords = strategy.get_low_competition_keywords(max_difficulty=0.4)
                high_opportunity_keywords = [kw for kw in strategy.primary_keywords if kw.opportunity_score > 0.7]
                long_tail_keywords = [kw for kw in strategy.primary_keywords if kw.word_count >= 4]

                # Quality metrics
                low_comp_ratio = len(low_competition_keywords) / len(strategy.primary_keywords)
                high_opp_ratio = len(high_opportunity_keywords) / len(strategy.primary_keywords)
                long_tail_ratio = len(long_tail_keywords) / len(strategy.primary_keywords)

                keyword_quality_score = (
                    low_comp_ratio * 0.4 +      # Low competition opportunities
                    high_opp_ratio * 0.3 +      # High opportunity scores
                    long_tail_ratio * 0.3       # Long-tail focus
                )

            # 5. Content strategy effectiveness (15% weight)
            content_strategy_score = 0.0

            if hasattr(strategy, 'content_strategy'):
                cs = strategy.content_strategy

                # Content gaps identification
                gaps_score = min(len(cs.content_gaps) / 10.0, 1.0)  # Target: 10+ gaps

                # Strategic recommendations
                topics_score = min(len(cs.recommended_topics) / 8.0, 1.0)  # Target: 8+ topics
                angles_score = min(len(cs.content_angles) / 8.0, 1.0)  # Target: 8+ angles
                advantages_score = min(len(cs.competitive_advantages) / 5.0, 1.0)  # Target: 5+ advantages

                content_strategy_score = (
                    gaps_score * 0.3 +
                    topics_score * 0.25 +
                    angles_score * 0.25 +
                    advantages_score * 0.2
                )

            # Optional: Real search validation using Tavily
            search_validation_score = 0
            if use_tavily_search:
                try:
                    tavily_service = TavilySearchService()
                    # Test keyword opportunities with actual search
                    search_count = 0
                    keywords_to_test = [kw.keyword for kw in strategy.get_top_opportunities(5)]

                    for keyword in keywords_to_test:
                        sources = tavily_service.search(keyword, max_results=max_search_results)
                        if sources and len(sources) > 0:
                            search_count += 1

                    if keywords_to_test:
                        search_validation_score = search_count / len(keywords_to_test)
                except Exception as e:
                    print(f"Tavily search failed: {e}")
                    search_validation_score = 0.5  # Default score if search fails

            # Combined score with enhanced weighting
            niche_score = (
                keyword_diversity_score * 0.25 +
                competitor_analysis_score * 0.20 +
                strategy_depth_score * 0.15 +
                keyword_quality_score * 0.25 +
                content_strategy_score * 0.15
            )

            # Bonus for advanced features
            if strategy.content_scraping_enabled:
                niche_score = min(1.0, niche_score + 0.05)
            if strategy.tavily_enabled:
                niche_score = min(1.0, niche_score + 0.03)

            detailed_scores[niche] = {
                "keyword_diversity": keyword_diversity_score,
                "competitor_analysis": competitor_analysis_score,
                "strategy_depth": strategy_depth_score,
                "keyword_quality": keyword_quality_score,
                "content_strategy": content_strategy_score,
                "search_validation": search_validation_score,
                "niche_score": niche_score,
                "advanced_features": {
                    "content_scraping": strategy.content_scraping_enabled,
                    "tavily_enabled": strategy.tavily_enabled,
                    "content_gaps_found": len(strategy.get_content_gaps()),
                    "low_competition_keywords": len(strategy.get_low_competition_keywords()),
                    "top_opportunities": len(strategy.get_top_opportunities())
                }
            }

            total_score += niche_score

        # Average score across all niches
        combined_score = total_score / len(test_niches)

        metrics = {
            "runtime": time.time() - start_t,
            "public": {
                "combined_score": combined_score,
                "total_niches": len(test_niches),
                "detailed_scores": detailed_scores,
                "average_keywords_per_niche": sum(len(r["strategy"].primary_keywords) for r in research_results) / len(research_results),
                "average_competitors_per_niche": sum(len(r["strategy"].competitor_analyses) for r in research_results) / len(research_results),
                "average_content_gaps_per_niche": sum(len(r["strategy"].get_content_gaps()) for r in research_results) / len(research_results)
            },
            "private": {
                "tavily_search_enabled": use_tavily_search,
                "content_analysis_enabled": enable_content_analysis,
                "raw_results": research_results  # Keep Pydantic models in memory
            },
            "combined_score": combined_score
        }

        error = ""
        correct = True

    except Exception as e:
        print(f"Error: {e}")
        metrics = {
            "combined_score": 0,
            "public": {},
            "private": {},
            "runtime": 0,
        }
        error = str(e)
        correct = False

    print(metrics)
    elapsed = metrics["runtime"]
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    print(f"Completed after {hours}h {minutes}m {seconds}s")

    # Save correct to JSON file
    correct_file = os.path.join(results_dir, "correct.json")
    with open(correct_file, "w") as f:
        json.dump({"correct": correct, "error": error}, f, indent=4)
    print(f"Correct saved to {correct_file}")

    # Save metrics to JSON file with custom encoder
    metrics_file = os.path.join(results_dir, "metrics.json")
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=4, cls=PydanticJSONEncoder)
    print(f"Metrics saved to {metrics_file}")
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advanced SEO research evaluation script"
    )
    parser.add_argument(
        "--program_path",
        type=str,
        default="advanced_initial.py",
        help="Path to the program to evaluate",
    )
    parser.add_argument(
        "--results_dir",
        type=str,
        default="results",
        help="Directory to save results and logs",
    )
    parser.add_argument(
        "--use_tavily_search",
        action="store_true",
        default=True,
        help="Enable Tavily search validation (default: True)",
    )
    parser.add_argument(
        "--enable_content_analysis",
        action="store_true",
        default=True,
        help="Enable competitor content analysis (default: True)",
    )

    parsed_args = parser.parse_args()
    Path(parsed_args.results_dir).mkdir(parents=True, exist_ok=True)
    evaluate_advanced_seo_research_quality(
        parsed_args.program_path,
        parsed_args.results_dir,
        use_tavily_search=parsed_args.use_tavily_search,
        enable_content_analysis=parsed_args.enable_content_analysis
    )