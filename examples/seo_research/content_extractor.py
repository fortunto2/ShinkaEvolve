"""
Content extraction utilities for competitor analysis using Tavily API.
"""

import re
from typing import List, Optional, Dict, Set
from urllib.parse import urlparse
from datetime import datetime

from shinka.utils.tavily_search import TavilySearchService, SourceData
from examples.seo_research.models import CompetitorContent, CompetitorAnalysis, KeywordOpportunity


class ContentExtractor:
    """Extract and analyze competitor content using Tavily API."""

    def __init__(self):
        self.tavily = TavilySearchService()

    def extract_content_from_source(self, source: SourceData) -> CompetitorContent:
        """Extract content from a Tavily SourceData object."""

        # Extract headings from raw content if available
        headings = []
        if source.full_content:
            # Simple heading extraction from markdown-like content
            lines = source.full_content.split('\n')
            for line in lines[:20]:  # Check first 20 lines
                line = line.strip()
                if line.startswith('#'):
                    # Markdown heading
                    heading_text = re.sub(r'^#+\s*', '', line).strip()
                    if heading_text:
                        headings.append(heading_text)
                elif line and len(line) < 100 and line.isupper():
                    # Potential heading (all caps, short)
                    headings.append(line)

        # Use snippet as meta description if available
        meta_description = source.snippet[:160] if source.snippet else None

        # Content snippet from full content or snippet
        content_text = source.full_content or source.snippet or ""
        content_snippet = content_text[:500] if content_text else None

        return CompetitorContent(
            url=source.url,
            domain=urlparse(source.url).netloc,
            title=source.title,
            meta_description=meta_description,
            headings=headings[:10],  # Limit to top 10 headings
            content_snippet=content_snippet,
            keywords_found=[],  # Will be populated by keyword analysis
            content_length=len(content_text),
            last_scraped=datetime.now()
        )

    def analyze_keyword_presence(self, content: CompetitorContent, target_keywords: List[str]) -> CompetitorContent:
        """Analyze keyword presence in competitor content."""
        if not content.content_snippet:
            return content

        keywords_found = []
        content_lower = (content.content_snippet + ' ' + (content.title or '')).lower()

        for keyword in target_keywords:
            if keyword.lower() in content_lower:
                keywords_found.append(keyword)

        content.keywords_found = keywords_found
        return content

    def estimate_content_quality(self, content: CompetitorContent) -> float:
        """Estimate content quality based on various factors."""
        score = 0.0

        # Title quality (0.2 weight)
        if content.title and len(content.title) > 30:
            score += 0.2

        # Meta description (0.15 weight)
        if content.meta_description and 120 <= len(content.meta_description) <= 160:
            score += 0.15

        # Heading structure (0.25 weight)
        if len(content.headings) >= 3:
            score += 0.25

        # Content length (0.25 weight)
        if content.content_length > 1000:
            score += 0.25
        elif content.content_length > 500:
            score += 0.15

        # Keyword usage (0.15 weight)
        if content.keywords_found:
            score += min(0.15, len(content.keywords_found) * 0.05)

        return min(1.0, score)

    def discover_ranking_keywords(self, domain: str, niche: str) -> List[str]:
        """Discover what keywords a domain might be ranking for using Tavily."""
        try:
            # Search for site-specific queries with content retrieval
            queries = [
                f"site:{domain} {niche}",
                f"site:{domain} {niche} guide",
                f"site:{domain} best {niche}"
            ]

            ranking_keywords = set()

            for query in queries:
                try:
                    sources = self.tavily.search(query, max_results=2, include_raw_content=True)
                    for source in sources:
                        if source.title:
                            # Extract potential keywords from titles
                            title_words = re.findall(r'\b\w+\b', source.title.lower())
                            for i in range(len(title_words) - 1):
                                bigram = f"{title_words[i]} {title_words[i+1]}"
                                if niche.lower() in bigram:
                                    ranking_keywords.add(bigram)

                        # Also extract from content snippet
                        if source.snippet:
                            snippet_words = re.findall(r'\b\w+\b', source.snippet.lower())
                            for i in range(len(snippet_words) - 2):
                                trigram = f"{snippet_words[i]} {snippet_words[i+1]} {snippet_words[i+2]}"
                                if niche.lower() in trigram:
                                    ranking_keywords.add(trigram)

                except Exception:
                    continue

            return list(ranking_keywords)[:10]  # Limit to 10 keywords

        except Exception as e:
            print(f"Failed to discover ranking keywords for {domain}: {e}")
            return []

    def analyze_competitor(self, domain: str, niche: str, target_keywords: List[str]) -> CompetitorAnalysis:
        """Perform comprehensive competitor analysis using Tavily search."""

        # Search for the domain with niche-related content
        # Use specific niche searches that are likely to return relevant content
        clean_domain = domain.replace("www.", "")
        niche_terms = niche.split()[-2:]  # Get last 2 words, e.g. "christmas cards" from "ai generate christmas card 2026"
        niche_query = " ".join(niche_terms)

        search_queries = [
            f"{clean_domain.split('.')[0]} {niche_query}",  # e.g. "canva christmas cards"
            f"site:{clean_domain}",
            f"{clean_domain}",
        ]

        content_data = None
        best_source = None

        # Try to get content from Tavily search results
        for query in search_queries:
            try:
                sources = self.tavily.search(query, max_results=2, include_raw_content=True)
                for source in sources:
                    if domain in source.url and (source.full_content or source.snippet):
                        if not best_source or len(source.full_content or source.snippet) > len(best_source.full_content or best_source.snippet):
                            best_source = source
                            break
                if best_source:
                    break
            except Exception:
                continue

        if best_source:
            content_data = self.extract_content_from_source(best_source)
            content_data = self.analyze_keyword_presence(content_data, target_keywords)
            content_quality = self.estimate_content_quality(content_data)
            keyword_overlap = len(content_data.keywords_found) / max(len(target_keywords), 1)
        else:
            content_quality = 0.0
            keyword_overlap = 0.0

        # Estimate authority score based on domain patterns
        authority_score = 0.5  # Default middle score
        if any(auth_domain in domain for auth_domain in ['wikipedia', 'github', 'medium', 'forbes']):
            authority_score = 0.9
        elif any(tech_domain in domain for tech_domain in ['techcrunch', 'wired', 'theverge']):
            authority_score = 0.8
        elif any(ai_domain in domain for ai_domain in ['openai', 'anthropic', 'google', 'microsoft']):
            authority_score = 0.85

        # Simplified ranking keywords discovery (skip for speed)
        ranking_keywords = []

        # Identify content gaps based on Tavily content
        content_gaps = []
        if content_data:
            if content_data.content_length < 1000:
                content_gaps.append("Short content - opportunity for comprehensive guides")
            if not content_data.keywords_found:
                content_gaps.append("Poor keyword optimization - opportunity for targeted content")
            if len(content_data.headings) < 3:
                content_gaps.append("Poor heading structure - opportunity for better organization")
            if not content_data.meta_description or len(content_data.meta_description) < 120:
                content_gaps.append("Poor meta description - opportunity for better SERP optimization")
        else:
            content_gaps.append("No accessible content found - opportunity for comprehensive coverage")

        return CompetitorAnalysis(
            domain=domain,
            authority_score=authority_score,
            content_quality=content_quality,
            keyword_overlap=keyword_overlap,
            content_gaps=content_gaps,
            content_data=content_data,
            ranking_keywords=ranking_keywords
        )