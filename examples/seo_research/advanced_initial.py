from typing import *
import json
import re
from urllib.parse import urlparse

from shinka.utils.tavily_search import TavilySearchService
from examples.seo_research.models import (
    AdvancedSEOStrategy,
    KeywordOpportunity,
    CompetitorAnalysis,
    ContentStrategy,
)
from examples.seo_research.content_extractor import ContentExtractor


def advanced_seo_research_strategy(niche_topic: str) -> AdvancedSEOStrategy:
    """
    Advanced SEO research strategy with competitor content analysis.
    This function will be evolved to optimize keyword research and competitor analysis.
    Returns a comprehensive Pydantic-validated SEO strategy.
    """
    # EVOLVE-BLOCK-START
    # Initialize strategy with required fields
    strategy = AdvancedSEOStrategy(niche=niche_topic)

    # Advanced keyword generation with intent classification
    keyword_templates = [
        # Commercial intent
        f"buy {niche_topic}",
        f"best {niche_topic} 2026",
        f"{niche_topic} price comparison",
        f"cheap {niche_topic} deals",
        f"{niche_topic} reviews 2026",
        # Informational intent
        f"how to use {niche_topic}",
        f"{niche_topic} tutorial guide",
        f"what is {niche_topic}",
        f"{niche_topic} tips and tricks",
        f"learn {niche_topic} fast",
        # Transactional intent
        f"create {niche_topic} online",
        f"{niche_topic} generator free",
        f"make {niche_topic} with ai",
        f"design {niche_topic} tool",
        f"{niche_topic} maker app",
    ]

    # Create keyword opportunities with intent analysis
    for template in keyword_templates:
        intent = (
            "commercial"
            if any(
                word in template
                for word in ["buy", "best", "price", "cheap", "reviews"]
            )
            else "informational"
            if any(
                word in template
                for word in ["how to", "what is", "tutorial", "learn", "tips"]
            )
            else "transactional"
        )

        opportunity = KeywordOpportunity(
            keyword=template,
            search_intent=intent,
            difficulty_score=0.5,  # Will be refined through evolution
            opportunity_score=0.7,  # Will be refined through evolution
            competing_domains=[],
            word_count=len(template.split()),
        )
        strategy.primary_keywords.append(opportunity)

    # Get real competitors from search results using Tavily
    tavily_service = TavilySearchService()
    strategy.tavily_enabled = True

    # Multiple specific search queries to find real competitors
    search_queries = [
        f"{niche_topic} generator",
        f"Canva {niche_topic.split()[-1]}",  # e.g., "Canva christmas cards"
        f"personalized {niche_topic.split()[-1]} online",  # e.g., "personalized christmas cards online"
    ]

    all_competitors = set()
    for query in search_queries:
        try:
            sources = tavily_service.search(query, max_results=5)
            for source in sources:
                if hasattr(source, "url") and source.url:
                    domain = urlparse(source.url).netloc
                    if domain:
                        all_competitors.add(domain)
        except Exception as e:
            print(f"Search failed for {query}: {e}")
            continue

    # Perform competitor content analysis
    content_extractor = ContentExtractor()
    strategy.content_scraping_enabled = True

    target_keywords = [kw.keyword for kw in strategy.primary_keywords]

    for domain in list(all_competitors)[
        :3
    ]:  # Limit to top 3 competitors for faster testing
        try:
            competitor_analysis = content_extractor.analyze_competitor(
                domain, niche_topic, target_keywords
            )
            strategy.competitor_analyses.append(competitor_analysis)
        except Exception as e:
            print(f"Failed to analyze competitor {domain}: {e}")
            continue

    # Update keyword difficulty scores based on competitor analysis
    for keyword_opp in strategy.primary_keywords:
        competing_domains = []
        total_authority = 0

        for comp in strategy.competitor_analyses:
            if any(
                kw.lower() in keyword_opp.keyword.lower()
                for kw in comp.ranking_keywords
            ):
                competing_domains.append(comp.domain)
                total_authority += comp.authority_score

        keyword_opp.competing_domains = competing_domains
        if competing_domains:
            avg_authority = total_authority / len(competing_domains)
            keyword_opp.difficulty_score = min(0.9, avg_authority * 0.8)
            keyword_opp.opportunity_score = max(0.1, 1.0 - keyword_opp.difficulty_score)

    # Generate comprehensive search strategies
    strategy.search_strategies = [
        f"{niche_topic} comprehensive guide",
        f"{niche_topic} vs alternatives comparison",
        f"{niche_topic} for beginners tutorial",
        f"advanced {niche_topic} techniques",
        f"{niche_topic} case studies",
        f"{niche_topic} best practices 2026",
        f"free {niche_topic} resources",
        f"{niche_topic} integration guide",
        f"{niche_topic} pricing analysis",
        f"{niche_topic} user reviews",
        f"{niche_topic} security considerations",
        f"{niche_topic} troubleshooting guide",
    ]

    # Develop content strategy based on competitor analysis
    all_content_gaps = []
    competitive_advantages = []

    for comp in strategy.competitor_analyses:
        all_content_gaps.extend(comp.content_gaps)

        # Identify competitive advantages
        if comp.content_quality < 0.6:
            competitive_advantages.append(f"Higher quality content than {comp.domain}")
        if comp.keyword_overlap < 0.3:
            competitive_advantages.append(
                f"Better keyword targeting than {comp.domain}"
            )

    # Generate content strategy
    strategy.content_strategy = ContentStrategy(
        recommended_topics=[
            f"{niche_topic} complete guide",
            f"{niche_topic} comparison matrix",
            f"{niche_topic} implementation tutorial",
            f"{niche_topic} ROI calculator",
            f"{niche_topic} best practices checklist",
        ],
        content_gaps=list(set(all_content_gaps)),
        content_angles=[
            f"Comprehensive {niche_topic} resource hub",
            f"Data-driven {niche_topic} comparisons",
            f"Step-by-step {niche_topic} implementation",
            f"Cost-effective {niche_topic} solutions",
            f"Future-proof {niche_topic} strategies",
        ],
        target_keywords=[kw.keyword for kw in strategy.get_top_opportunities(10)],
        competitive_advantages=list(set(competitive_advantages)),
    )

    # Set analysis depth
    strategy.analysis_depth = "advanced_with_content_analysis"
    # EVOLVE-BLOCK-END

    # Return Pydantic model directly
    return strategy


def perform_advanced_seo_research(niches: List[str]) -> List[Dict[str, Any]]:
    """
    Perform advanced SEO research for multiple niches using content analysis.
    """
    results = []

    for niche in niches:
        strategy = advanced_seo_research_strategy(niche)

        # Simulate research execution
        research_result = {
            "niche": niche,
            "strategy": strategy,  # Keep as Pydantic model
            "keyword_count": len(strategy.primary_keywords),
            "competitor_count": len(strategy.competitor_analyses),
            "content_gaps_count": len(strategy.get_content_gaps()),
            "top_opportunities_count": len(strategy.get_top_opportunities()),
            "low_competition_count": len(strategy.get_low_competition_keywords()),
        }

        results.append(research_result)
        print(
            f"Advanced SEO research for '{niche}': {research_result['keyword_count']} keywords, "
            f"{research_result['competitor_count']} competitors analyzed, "
            f"{research_result['content_gaps_count']} content gaps identified"
        )

    return results


def run_experiment(test_niches: List[str]) -> List[Dict[str, Any]]:
    """
    Main experiment function required by ShinkaEvolve framework.
    """
    return perform_advanced_seo_research(test_niches)
