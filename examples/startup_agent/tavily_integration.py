"""
Tavily Web Research Integration for Startup Agent.

Integrates with Tavily search service (via localhost) to gather market intelligence,
competitive analysis, and trend research for startup strategy development.
"""

import json
import logging
import asyncio
from typing import List, Dict, Any, Optional
import aiohttp
from urllib.parse import quote

logger = logging.getLogger(__name__)


class TavilyWebResearch:
    """Web research client using Tavily search via localhost."""

    def __init__(self, localhost_url: str = "http://localhost:8000"):
        """
        Initialize Tavily research client.

        Args:
            localhost_url: Base URL for local Tavily service
        """
        self.base_url = localhost_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Execute search query via Tavily localhost API.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of search results
        """
        session = await self._get_session()

        try:
            # Format search request for localhost Tavily API
            search_data = {
                "query": query,
                "max_results": max_results,
                "include_raw_content": True
            }

            async with session.post(
                f"{self.base_url}/search",
                json=search_data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("results", [])
                else:
                    logger.warning(f"Search failed with status {response.status}")
                    return []

        except aiohttp.ClientError as e:
            logger.error(f"Search request failed: {e}")
            return []
        except asyncio.TimeoutError:
            logger.error(f"Search timeout for query: {query}")
            return []

    async def research_market_size(self, startup_idea: str) -> str:
        """
        Research market size and opportunity for startup idea.

        Args:
            startup_idea: Description of startup idea

        Returns:
            Formatted market research summary
        """
        logger.info(f"🔍 Researching market size for: {startup_idea[:50]}...")

        # Generate market research queries
        queries = [
            f"market size {startup_idea} industry",
            f"{startup_idea} market opportunity 2024",
            f"TAM SAM SOM {startup_idea}",
            f"{startup_idea} industry growth trends"
        ]

        all_results = []
        for query in queries:
            results = await self._search(query, max_results=5)
            all_results.extend(results)

        # Process and format results
        market_summary = self._format_market_research(all_results, startup_idea)
        logger.info(f"📊 Market research completed: {len(all_results)} sources")

        return market_summary

    async def research_competitors(self, startup_idea: str) -> str:
        """
        Research competitive landscape for startup idea.

        Args:
            startup_idea: Description of startup idea

        Returns:
            Formatted competitive analysis
        """
        logger.info(f"🏢 Researching competitors for: {startup_idea[:50]}...")

        # Generate competitor research queries
        queries = [
            f"{startup_idea} competitors",
            f"companies similar to {startup_idea}",
            f"{startup_idea} alternatives",
            f"{startup_idea} competitive analysis"
        ]

        all_results = []
        for query in queries:
            results = await self._search(query, max_results=7)
            all_results.extend(results)

        # Process and format results
        competitor_summary = self._format_competitor_research(all_results, startup_idea)
        logger.info(f"🏢 Competitor research completed: {len(all_results)} sources")

        return competitor_summary

    async def research_trends(self, startup_idea: str) -> str:
        """
        Research market trends related to startup idea.

        Args:
            startup_idea: Description of startup idea

        Returns:
            Formatted trend analysis
        """
        logger.info(f"📈 Researching trends for: {startup_idea[:50]}...")

        # Generate trend research queries
        queries = [
            f"{startup_idea} trends 2024",
            f"future of {startup_idea}",
            f"{startup_idea} market predictions",
            f"emerging trends {startup_idea} industry"
        ]

        all_results = []
        for query in queries:
            results = await self._search(query, max_results=5)
            all_results.extend(results)

        # Process and format results
        trends_summary = self._format_trends_research(all_results, startup_idea)
        logger.info(f"📈 Trends research completed: {len(all_results)} sources")

        return trends_summary

    async def research_validation_signals(self, startup_idea: str) -> str:
        """
        Research market validation signals for startup idea.

        Args:
            startup_idea: Description of startup idea

        Returns:
            Formatted validation research
        """
        logger.info(f"✅ Researching validation signals for: {startup_idea[:50]}...")

        # Generate validation research queries
        queries = [
            f"{startup_idea} customer demand",
            f"people asking for {startup_idea}",
            f"{startup_idea} pain points",
            f"need for {startup_idea} solution"
        ]

        all_results = []
        for query in queries:
            results = await self._search(query, max_results=5)
            all_results.extend(results)

        # Process and format results
        validation_summary = self._format_validation_research(all_results, startup_idea)
        logger.info(f"✅ Validation research completed: {len(all_results)} sources")

        return validation_summary

    async def deep_seo_analysis(self, keyword: str, max_sites: int = 5) -> Dict[str, Any]:
        """
        Perform deep SEO analysis for a keyword:
        1. Get top search results
        2. Parse each site's content
        3. Extract keywords, marketing hooks, positioning
        4. Build semantic core and insights

        Args:
            keyword: Target keyword to analyze
            max_sites: Number of top sites to analyze (default 5)

        Returns:
            Comprehensive SEO analysis with competitive insights
        """
        logger.info(f"🔍 Deep SEO analysis for: {keyword}")

        # Step 1: Get top search results
        search_results = await self._search(f"{keyword}", max_results=max_sites)

        analysis = {
            "keyword": keyword,
            "top_sites": [],
            "semantic_core": [],
            "marketing_hooks": [],
            "positioning_insights": [],
            "content_patterns": [],
            "competitive_gaps": []
        }

        # Step 2: Analyze each top site
        for i, result in enumerate(search_results[:max_sites]):
            site_url = result.get('url', '')
            site_title = result.get('title', '')
            site_content = result.get('content', '')

            logger.info(f"🌐 Analyzing site {i+1}/{max_sites}: {site_url[:50]}...")

            # Extract site analysis
            site_analysis = await self._analyze_site_content(
                site_url, site_title, site_content, keyword
            )

            analysis["top_sites"].append(site_analysis)

            # Aggregate insights
            analysis["semantic_core"].extend(site_analysis.get("keywords", []))
            analysis["marketing_hooks"].extend(site_analysis.get("hooks", []))
            analysis["positioning_insights"].extend(site_analysis.get("positioning", []))
            analysis["content_patterns"].extend(site_analysis.get("patterns", []))

        # Step 3: Generate competitive gaps and opportunities
        analysis["competitive_gaps"] = await self._identify_gaps(analysis, keyword)

        # Step 4: Clean and deduplicate
        analysis = await self._consolidate_analysis(analysis)

        logger.info(f"✅ Deep SEO analysis completed for {keyword}")
        return analysis

    async def _analyze_site_content(self, url: str, title: str, content: str, target_keyword: str) -> Dict[str, Any]:
        """
        Analyze individual site content for SEO insights.

        Args:
            url: Site URL
            title: Site title
            content: Site content
            target_keyword: Target keyword we're analyzing

        Returns:
            Site-specific SEO analysis
        """

        try:
            site_analysis = {
                "url": url,
                "title": title,
                "domain": url.split('/')[2] if '/' in url else url,
                "keywords": self._extract_keywords(content, target_keyword),
                "hooks": self._extract_marketing_hooks(content),
                "positioning": self._extract_positioning(content, title),
                "patterns": self._extract_content_patterns(content),
                "cta_strategies": self._extract_cta_strategies(content)
            }

            return site_analysis

        except Exception as e:
            logger.warning(f"⚠️ Site analysis failed for {url}: {e}")
            return {
                "url": url,
                "title": title,
                "error": str(e),
                "keywords": [],
                "hooks": [],
                "positioning": [],
                "patterns": [],
                "cta_strategies": []
            }

    def _extract_keywords(self, content: str, target_keyword: str) -> List[str]:
        """Extract relevant keywords from content."""
        import re

        # Simple keyword extraction - in real implementation could use NLP
        content_lower = content.lower()

        # Common keyword patterns for Christmas/holiday market
        holiday_patterns = [
            r'\b(christmas|holiday|festive|seasonal|winter|december)\s+\w+',
            r'\w+\s+(cards?|greetings?|gifts?|wishes)',
            r'(personalized?|custom|unique|special)\s+\w+',
            r'(ai|artificial\s+intelligence|automated?|smart)\s+\w+',
            r'(design|create|make|generate|build)\s+\w+'
        ]

        keywords = []
        for pattern in holiday_patterns:
            matches = re.findall(pattern, content_lower)
            keywords.extend([match.strip() for match in matches if len(match.strip()) > 3])

        # Remove duplicates and target keyword
        keywords = list(set(keywords))
        keywords = [kw for kw in keywords if target_keyword.lower() not in kw.lower()]

        return keywords[:10]  # Top 10 most relevant

    def _extract_marketing_hooks(self, content: str) -> List[str]:
        """Extract marketing hooks and value propositions."""
        import re

        # Patterns for marketing hooks
        hook_patterns = [
            r'(save|get|create|make|design|build|generate)\s+[^.]{10,50}',
            r'(free|instant|quick|easy|simple|fast)\s+[^.]{10,50}',
            r'(professional|premium|high-quality|custom|personalized)\s+[^.]{10,50}',
            r'(within\s+minutes?|in\s+seconds?|instantly|immediately)\s+[^.]{10,50}'
        ]

        hooks = []
        for pattern in hook_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            hooks.extend([match.strip() for match in matches])

        return hooks[:8]  # Top 8 hooks

    def _extract_positioning(self, content: str, title: str) -> List[str]:
        """Extract positioning statements and differentiation."""
        positioning = []

        # Look for positioning in title and key content sections
        if "ai" in title.lower() or "artificial intelligence" in content.lower():
            positioning.append("AI-powered solution")

        if "professional" in content.lower():
            positioning.append("Professional-grade tools")

        if "easy" in content.lower() or "simple" in content.lower():
            positioning.append("User-friendly approach")

        if "custom" in content.lower() or "personalized" in content.lower():
            positioning.append("Personalization focus")

        return positioning

    def _extract_content_patterns(self, content: str) -> List[str]:
        """Extract content structure patterns."""
        patterns = []

        # Analyze content structure
        if "step" in content.lower() or "how to" in content.lower():
            patterns.append("Step-by-step guidance")

        if "template" in content.lower():
            patterns.append("Template-based approach")

        if "gallery" in content.lower() or "examples" in content.lower():
            patterns.append("Example showcase")

        return patterns

    def _extract_cta_strategies(self, content: str) -> List[str]:
        """Extract call-to-action strategies."""
        import re

        cta_patterns = [
            r'(start|begin|create|try|get started|sign up|download)\s+[^.]{5,30}',
            r'(free trial|free version|no credit card)\s+[^.]{5,30}'
        ]

        ctas = []
        for pattern in cta_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            ctas.extend([match.strip() for match in matches])

        return ctas[:5]

    async def _identify_gaps(self, analysis: Dict[str, Any], keyword: str) -> List[str]:
        """Identify competitive gaps and opportunities."""

        gaps = []

        # Analyze what's missing in the competitive landscape
        all_keywords = analysis.get("semantic_core", [])
        all_hooks = analysis.get("marketing_hooks", [])

        # Check for gaps in AI positioning
        ai_mentions = sum(1 for kw in all_keywords if "ai" in kw.lower())
        if ai_mentions < 2:
            gaps.append("Limited AI positioning in top results")

        # Check for seasonal focus gaps
        seasonal_mentions = sum(1 for kw in all_keywords if any(season in kw.lower() for season in ["christmas", "holiday", "seasonal"]))
        if seasonal_mentions < 5:
            gaps.append("Insufficient seasonal optimization")

        # Check for personalization gaps
        personal_mentions = sum(1 for hook in all_hooks if "personal" in hook.lower())
        if personal_mentions < 3:
            gaps.append("Personalization not well emphasized")

        return gaps

    async def _consolidate_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and consolidate analysis data."""

        # Remove duplicates and rank by frequency
        semantic_core = list(set(analysis.get("semantic_core", [])))
        marketing_hooks = list(set(analysis.get("marketing_hooks", [])))

        # Sort by length/quality (longer = more specific)
        semantic_core.sort(key=len, reverse=True)
        marketing_hooks.sort(key=len, reverse=True)

        analysis["semantic_core"] = semantic_core[:15]  # Top 15 keywords
        analysis["marketing_hooks"] = marketing_hooks[:10]  # Top 10 hooks

        return analysis

    def _format_market_research(self, results: List[Dict[str, Any]], idea: str) -> str:
        """Format market research results into summary."""
        if not results:
            return "No market research data found."

        summary = f"MARKET RESEARCH SUMMARY for '{idea}':\n\n"

        # Extract key insights
        market_insights = []
        size_mentions = []
        growth_mentions = []

        for result in results[:10]:  # Limit to top 10 results
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")

            # Look for market size indicators
            content_lower = content.lower()
            if any(term in content_lower for term in ["billion", "million", "market size", "revenue"]):
                size_mentions.append(f"• {title}: {content[:200]}... [Source: {url}]")

            # Look for growth indicators
            if any(term in content_lower for term in ["growth", "increase", "expand", "cagr"]):
                growth_mentions.append(f"• {title}: {content[:200]}... [Source: {url}]")

        summary += "MARKET SIZE INDICATORS:\n"
        for mention in size_mentions[:5]:
            summary += f"{mention}\n"

        summary += "\nGROWTH INDICATORS:\n"
        for mention in growth_mentions[:5]:
            summary += f"{mention}\n"

        return summary

    def _format_competitor_research(self, results: List[Dict[str, Any]], idea: str) -> str:
        """Format competitor research results into summary."""
        if not results:
            return "No competitor research data found."

        summary = f"COMPETITIVE LANDSCAPE for '{idea}':\n\n"

        # Extract competitor mentions
        competitors = []
        positioning = []

        for result in results[:15]:  # More results for competitive analysis
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")

            # Look for company names and competitive mentions
            content_lower = content.lower()
            if any(term in content_lower for term in ["company", "startup", "competitor", "alternative"]):
                competitors.append(f"• {title}: {content[:250]}... [Source: {url}]")

        summary += "COMPETITOR INSIGHTS:\n"
        for comp in competitors[:8]:
            summary += f"{comp}\n"

        return summary

    def _format_trends_research(self, results: List[Dict[str, Any]], idea: str) -> str:
        """Format trends research results into summary."""
        if not results:
            return "No trends research data found."

        summary = f"MARKET TRENDS for '{idea}':\n\n"

        # Extract trend insights
        trends = []

        for result in results[:10]:
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")

            # Look for trend indicators
            content_lower = content.lower()
            if any(term in content_lower for term in ["trend", "future", "prediction", "forecast", "emerging"]):
                trends.append(f"• {title}: {content[:200]}... [Source: {url}]")

        summary += "TREND ANALYSIS:\n"
        for trend in trends[:6]:
            summary += f"{trend}\n"

        return summary

    def _format_validation_research(self, results: List[Dict[str, Any]], idea: str) -> str:
        """Format validation research results into summary."""
        if not results:
            return "No validation research data found."

        summary = f"VALIDATION SIGNALS for '{idea}':\n\n"

        # Extract validation insights
        signals = []

        for result in results[:10]:
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")

            # Look for demand/pain point indicators
            content_lower = content.lower()
            if any(term in content_lower for term in ["need", "problem", "pain", "demand", "want", "looking for"]):
                signals.append(f"• {title}: {content[:200]}... [Source: {url}]")

        summary += "DEMAND SIGNALS:\n"
        for signal in signals[:6]:
            summary += f"{signal}\n"

        return summary

    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# Test function for standalone usage
async def test_tavily_research():
    """Test Tavily research integration."""

    test_idea = "AI-powered task management app that learns user patterns"

    async with TavilyWebResearch() as research:
        print("🔍 Testing market research...")
        market_data = await research.research_market_size(test_idea)
        print(f"Market Data: {market_data[:300]}...")

        print("\n🏢 Testing competitor research...")
        competitor_data = await research.research_competitors(test_idea)
        print(f"Competitor Data: {competitor_data[:300]}...")

        print("\n📈 Testing trends research...")
        trends_data = await research.research_trends(test_idea)
        print(f"Trends Data: {trends_data[:300]}...")


if __name__ == "__main__":
    # Run test
    asyncio.run(test_tavily_research())