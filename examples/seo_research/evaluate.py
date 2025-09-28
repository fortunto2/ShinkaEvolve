import os
import json
import time
import argparse
import importlib.util
from pathlib import Path
from typing import List
from pydantic import BaseModel

from shinka.utils.tavily_search import TavilySearchService


class PydanticJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles Pydantic models."""

    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        return super().default(obj)


def evaluate_seo_research_quality(
    program_path: str,
    results_dir: str,
    test_niches: List[str] = [
        "digital marketing",
        "fitness equipment",
        "online courses",
    ],
    use_tavily_search: bool = False,
    max_search_results: int = 3,
):
    """
    Evaluate the quality of SEO research strategies.
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
        # Run the SEO research experiment
        research_results = module.run_experiment(test_niches)

        # Calculate quality metrics
        total_score = 0
        detailed_scores = {}

        for result in research_results:
            niche = result["niche"]
            strategy_dict = result[
                "strategy"
            ]  # Now a dict (converted from Pydantic model)

            # More critical scoring criteria
            keyword_diversity_score = min(
                len(strategy_dict["primary_keywords"]) / 15.0, 1.0
            )  # Harder: Max 15 keywords for full score
            competitor_analysis_score = min(
                len(strategy_dict["competitor_domains"]) / 10.0, 1.0
            )  # Harder: Max 10 competitors
            strategy_depth_score = min(
                len(strategy_dict["search_strategies"]) / 12.0, 1.0
            )  # Harder: Max 12 strategies

            # More critical keyword quality scoring
            keyword_quality_score = 0
            unique_keywords = set()
            long_tail_count = 0
            commercial_intent_count = 0

            for keyword in strategy_dict["primary_keywords"]:
                if isinstance(keyword, str):  # Safety check
                    keyword_lower = keyword.lower()

                    # Penalty for duplicates or very similar keywords
                    if keyword_lower in unique_keywords:
                        keyword_quality_score -= 0.1
                        continue
                    unique_keywords.add(keyword_lower)

                    # Long-tail keywords (3+ words) get higher score
                    word_count = len(keyword.split())
                    if word_count >= 4:
                        keyword_quality_score += 0.15
                        long_tail_count += 1
                    elif word_count >= 3:
                        keyword_quality_score += 0.1
                    elif word_count == 2:
                        keyword_quality_score += 0.05
                    # Single word keywords get 0 points

                    # Commercial intent keywords
                    if any(
                        word in keyword_lower
                        for word in [
                            "buy",
                            "price",
                            "cost",
                            "cheap",
                            "best",
                            "review",
                            "compare",
                        ]
                    ):
                        keyword_quality_score += 0.08
                        commercial_intent_count += 1

                    # Informational intent keywords
                    if any(
                        word in keyword_lower
                        for word in ["how to", "what is", "guide", "tutorial", "tips"]
                    ):
                        keyword_quality_score += 0.05

                    # AI/tech specific terms
                    if any(
                        word in keyword_lower
                        for word in ["ai", "automated", "generator", "tool", "software"]
                    ):
                        keyword_quality_score += 0.03

            # Bonus for diversity of keyword types
            if long_tail_count >= 3:
                keyword_quality_score += 0.1
            if commercial_intent_count >= 2:
                keyword_quality_score += 0.1

            keyword_quality_score = max(0, min(keyword_quality_score, 1.0))

            # Optional: Real search validation using Tavily
            search_validation_score = 0
            if use_tavily_search:
                try:
                    tavily_service = TavilySearchService()
                    # Test a few keywords with actual search
                    search_count = 0
                    for keyword in strategy_dict["primary_keywords"][
                        :3
                    ]:  # Test first 3 keywords
                        sources = tavily_service.search(
                            keyword,
                            max_results=max_search_results,
                            include_raw_content=False,
                        )
                        if sources and len(sources) > 0:
                            search_count += 1
                    search_validation_score = search_count / 3.0
                except Exception as e:
                    print(f"Tavily search failed: {e}")
                    search_validation_score = 0.5  # Default score if search fails

            # More critical combined scoring with higher weight on quality
            niche_score = (
                keyword_diversity_score * 0.20
                + competitor_analysis_score * 0.15
                + strategy_depth_score * 0.20
                + keyword_quality_score * 0.35  # Higher weight on quality
                + search_validation_score * 0.10
            )

            detailed_scores[niche] = {
                "keyword_diversity": keyword_diversity_score,
                "competitor_analysis": competitor_analysis_score,
                "strategy_depth": strategy_depth_score,
                "keyword_quality": keyword_quality_score,
                "search_validation": search_validation_score,
                "niche_score": niche_score,
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
                "average_keywords_per_niche": sum(
                    len(r["strategy"]["primary_keywords"]) for r in research_results
                )
                / len(research_results),
                "average_competitors_per_niche": sum(
                    len(r["strategy"]["competitor_domains"]) for r in research_results
                )
                / len(research_results),
            },
            "private": {
                "tavily_search_enabled": use_tavily_search,
                "raw_results": research_results,  # Now contains dicts instead of Pydantic models
            },
            "combined_score": combined_score,
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

    # Save metrics to JSON file
    metrics_file = os.path.join(results_dir, "metrics.json")
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to {metrics_file}")
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO research evaluation script")
    parser.add_argument(
        "--program_path",
        type=str,
        default="initial.py",
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
        help="Enable Tavily search validation (requires API access)",
    )

    parsed_args = parser.parse_args()
    Path(parsed_args.results_dir).mkdir(parents=True, exist_ok=True)
    evaluate_seo_research_quality(
        parsed_args.program_path,
        parsed_args.results_dir,
        use_tavily_search=parsed_args.use_tavily_search,
    )
