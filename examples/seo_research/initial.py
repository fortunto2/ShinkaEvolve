from typing import List, Dict, Any, Tuple, Optional
import json
import re
from urllib.parse import urlparse

from shinka.utils.tavily_search import TavilySearchService


def seo_research_strategy(niche_topic: str) -> Dict[str, Any]:
    """
    SEO research strategy for finding profitable niches and keywords.
    This function will be evolved to optimize keyword research and competitor analysis.
    """
    # EVOLVE-BLOCK-START
    # Basic keyword expansion strategy
    base_keywords = [
        f"{niche_topic}",
        f"best {niche_topic}",
        f"how to {niche_topic}",
        f"{niche_topic} guide",
        f"{niche_topic} tips",
    ]

    # Get real competitors from search results using Tavily
    tavily_service = TavilySearchService()

    # Search for main topic to find competitors
    sources = tavily_service.search(f"best {niche_topic}", max_results=5)

    # Extract unique domains from search results
    competitor_domains = []
    seen_domains = set()
    for source in sources:
        if hasattr(source, "url") and source.url:
            domain = urlparse(source.url).netloc
            if domain and domain not in seen_domains:
                seen_domains.add(domain)
                competitor_domains.append(domain)

    # Generate search strategies based on found competitors
    search_strategies = [
        f"{niche_topic} reviews",
        f"{niche_topic} comparison",
        f"cheap {niche_topic}",
        f"{niche_topic} vs alternatives",
    ]
    # EVOLVE-BLOCK-END

    return {
        "niche": niche_topic,
        "primary_keywords": base_keywords,
        "competitor_domains": competitor_domains[:5],  # Limit to top 5
        "search_strategies": search_strategies,
        "analysis_depth": "tavily_enhanced",
    }


def perform_seo_research(niches: List[str]) -> List[Dict[str, Any]]:
    """
    Perform SEO research for multiple niches using the evolved strategy.
    """
    results = []

    for niche in niches:
        strategy = seo_research_strategy(niche)

        # Simulate research execution
        research_result = {
            "niche": niche,
            "strategy": strategy,
            "keyword_count": len(strategy["primary_keywords"]),
            "competitor_count": len(strategy["competitor_domains"]),
            "search_strategy_count": len(strategy["search_strategies"]),
        }

        results.append(research_result)
        print(
            f"SEO research for '{niche}': {research_result['keyword_count']} keywords, {research_result['competitor_count']} competitors"
        )

    return results


def run_experiment(test_niches: List[str]) -> List[Dict[str, Any]]:
    """
    Main experiment function required by ShinkaEvolve framework.
    """
    return perform_seo_research(test_niches)
