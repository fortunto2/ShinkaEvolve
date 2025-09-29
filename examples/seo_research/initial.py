from typing import List, Dict, Any, Tuple, Optional, Union, AnyStr
from urllib.parse import urlparse
import re, time
from pydantic import BaseModel, Field

from shinka.utils.tavily_search import TavilySearchService


class SEOStrategy(BaseModel):
    """Pydantic model for SEO research strategy to ensure data consistency."""

    niche: str = Field(description="The target niche/topic")
    primary_keywords: List[str] = Field(
        default_factory=list, description="Main keywords to target"
    )
    competitor_domains: List[str] = Field(
        default_factory=list, description="Competitor websites"
    )
    search_strategies: List[str] = Field(
        default_factory=list, description="Search approaches for market research"
    )
    analysis_depth: str = Field(
        default="basic", description="Depth of analysis performed"
    )


def seo_research_strategy(niche_topic: str) -> SEOStrategy:
    """
    SEO research strategy for finding profitable niches and keywords.
    This function will be evolved to optimize keyword research and competitor analysis.
    Returns a Pydantic-validated SEO strategy.

    Available imports: List, Dict, Any, Tuple, Optional, Union from typing

    Example type hints:
    - def helper_func(data: List[str]) -> Tuple[int, float]:
    - def process_keywords(keywords: List[str]) -> Optional[Dict[str, Any]]:
    """
    # EVOLVE-BLOCK-START
    # Initialize strategy with required fields
    strategy = SEOStrategy(niche=niche_topic)

    # Basic keyword expansion strategy
    strategy.primary_keywords = [
        f"{niche_topic}",
        f"best {niche_topic}",
        f"how to {niche_topic}",
        f"{niche_topic} guide",
        f"{niche_topic} tips",
    ]

    # Get real competitors from search results using Tavily
    tavily_service = TavilySearchService()

    # Search for main topic to find competitors
    sources = tavily_service.search(
        f"best {niche_topic}", max_results=5, include_raw_content=False
    )

    # Extract unique domains from search results
    seen_domains = set()
    for source in sources:
        if hasattr(source, "url") and source.url:
            domain = urlparse(source.url).netloc
            if domain and domain not in seen_domains:
                seen_domains.add(domain)
                strategy.competitor_domains.append(domain)

    # Generate search strategies based on found competitors
    strategy.search_strategies = [
        f"{niche_topic} reviews",
        f"{niche_topic} comparison",
        f"cheap {niche_topic}",
        f"{niche_topic} vs alternatives",
    ]

    # Set analysis depth
    strategy.analysis_depth = "tavily_enhanced"
    # EVOLVE-BLOCK-END

    # Return Pydantic model directly
    return strategy


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
            "strategy": strategy.model_dump(),  # Convert Pydantic model to dict
            "keyword_count": len(strategy.primary_keywords),
            "competitor_count": len(strategy.competitor_domains),
            "search_strategy_count": len(strategy.search_strategies),
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
