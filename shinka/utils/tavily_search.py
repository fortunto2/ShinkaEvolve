import logging

from tavily import TavilyClient
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class SourceData(BaseModel):
    """Data about a research source."""

    number: int = Field(description="Citation number")
    title: str | None = Field(default="Untitled", description="Page title")
    url: str = Field(description="Source URL")
    snippet: str = Field(default="", description="Search snippet or summary")
    full_content: str = Field(default="", description="Full scraped content")
    char_count: int = Field(default=0, description="Character count of full content")

    def __str__(self):
        return f"[{self.number}] {self.title or 'Untitled'} - {self.url}"


class TavilySearchService:
    def __init__(self):
        # Use a dummy API key if none provided (for custom servers that don't need authentication)
        api_key = "dummy-key-for-custom-server"
        self._client = TavilyClient(
            api_key=api_key, api_base_url="http://localhost:8013"
        )
        # Simple in-memory cache
        self._cache = {}

    @staticmethod
    def rearrange_sources(
        sources: list[SourceData], starting_number=1
    ) -> list[SourceData]:
        for i, source in enumerate(sources, starting_number):
            source.number = i
        return sources

    def search(
        self,
        query: str,
        max_results: int | None = None,
        include_raw_content: bool = False,
    ) -> (str, list[SourceData]):
        """Perform search through Tavily API and return results with
        SourceData.

        Args:
            query: Search query
            max_results: Maximum number of results (default from config)
            include_raw_content: Include raw page content

        Returns:
            Tuple with tavily answer and list of SourceData
        """
        max_results = max_results or 5  # Default fallback

        # Create cache key
        cache_key = f"{query}_{max_results}_{include_raw_content}"

        # Check cache first
        if cache_key in self._cache:
            logger.info(f"🎯 Cache hit for: '{query}' (max_results={max_results})")
            return self._cache[cache_key]

        logger.info(f"🔍 Tavily search: '{query}' (max_results={max_results})")

        # Execute search through Tavily
        response = self._client.search(
            query=query,
            max_results=max_results,
            include_raw_content=include_raw_content,
        )

        # Convert results to SourceData
        sources = self._convert_to_source_data(response)

        # Store in cache
        self._cache[cache_key] = sources
        logger.info(f"💾 Cached result for: '{query}'")

        return sources

    def _convert_to_source_data(self, response: dict) -> list[SourceData]:
        """Convert Tavily response to SourceData list."""
        sources = []

        for i, result in enumerate(response.get("results", [])):
            if not result.get("url", ""):
                continue

            source = SourceData(
                number=i,
                title=result.get("title", ""),
                url=result.get("url", ""),
                snippet=result.get("content", ""),
            )
            if result.get("raw_content", ""):
                source.full_content = result["raw_content"]
                source.char_count = len(source.full_content)
            sources.append(source)
        return sources
