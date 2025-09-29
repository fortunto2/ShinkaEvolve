import logging
import json
import hashlib
import os
from pathlib import Path

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
    def __init__(self, cache_dir: str = ".tavily_cache"):
        # Use a dummy API key if none provided (for custom servers that don't need authentication)
        api_key = "dummy-key-for-custom-server"
        self._client = TavilyClient(
            api_key=api_key, api_base_url="http://localhost:8013"
        )
        # Simple in-memory cache
        self._cache = {}

        # File-based persistent cache
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        logger.info(f"📁 Tavily cache directory: {self.cache_dir.absolute()}")

    def _get_cache_key(self, query: str, max_results: int, include_raw_content: bool) -> str:
        """Generate a hash-based cache key for the query."""
        cache_string = f"{query}_{max_results}_{include_raw_content}"
        return hashlib.md5(cache_string.encode('utf-8')).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the file path for a cache key."""
        return self.cache_dir / f"{cache_key}.json"

    def _load_from_cache(self, cache_key: str) -> list[SourceData] | None:
        """Load cached results from disk."""
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)

            # Convert back to SourceData objects
            sources = [SourceData(**source_data) for source_data in cached_data]
            return sources

        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            logger.warning(f"Failed to load cache {cache_key}: {e}")
            return None

    def _save_to_cache(self, cache_key: str, sources: list[SourceData]) -> None:
        """Save search results to disk cache."""
        cache_path = self._get_cache_path(cache_key)

        try:
            # Convert SourceData to dict for JSON serialization
            cached_data = [source.model_dump() for source in sources]

            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, indent=2, ensure_ascii=False)

            logger.debug(f"💾 Saved to cache: {cache_path}")

        except Exception as e:
            logger.warning(f"Failed to save cache {cache_key}: {e}")

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
    ) -> list[SourceData]:
        """Perform search through Tavily API and return results with
        SourceData.

        Args:
            query: Search query
            max_results: Maximum number of results (default from config)
            include_raw_content: Include raw page content

        Returns:
            List of SourceData
        """
        max_results = max_results or 5  # Default fallback

        # Generate cache key
        cache_key = self._get_cache_key(query, max_results, include_raw_content)

        # Check memory cache first
        if cache_key in self._cache:
            logger.info(f"🎯 Memory cache hit for: '{query}' (max_results={max_results})")
            return self._cache[cache_key]

        # Check file cache
        cached_sources = self._load_from_cache(cache_key)
        if cached_sources is not None:
            logger.info(f"📁 File cache hit for: '{query}' (max_results={max_results})")
            # Store in memory cache for faster next access
            self._cache[cache_key] = cached_sources
            return cached_sources

        logger.info(f"🔍 Tavily search: '{query}' (max_results={max_results})")

        # Execute search through Tavily
        response = self._client.search(
            query=query,
            max_results=max_results,
            include_raw_content=include_raw_content,
        )

        # Convert results to SourceData
        sources = self._convert_to_source_data(response)

        # Store in both memory and file cache
        self._cache[cache_key] = sources
        self._save_to_cache(cache_key, sources)
        logger.info(f"💾 Cached result for: '{query}' (found {len(sources)} sources)")

        return sources

    def clear_cache(self, older_than_hours: int = None) -> int:
        """Clear cache files, optionally only those older than specified hours.

        Args:
            older_than_hours: Only clear files older than this many hours. If None, clear all.

        Returns:
            Number of files cleared
        """
        import time

        if not self.cache_dir.exists():
            return 0

        cleared_count = 0
        current_time = time.time()

        for cache_file in self.cache_dir.glob("*.json"):
            should_clear = True

            if older_than_hours is not None:
                file_age_hours = (current_time - cache_file.stat().st_mtime) / 3600
                should_clear = file_age_hours > older_than_hours

            if should_clear:
                try:
                    cache_file.unlink()
                    cleared_count += 1
                except Exception as e:
                    logger.warning(f"Failed to clear cache file {cache_file}: {e}")

        # Clear memory cache as well
        self._cache.clear()

        logger.info(f"🗑️ Cleared {cleared_count} cache files")
        return cleared_count

    def get_cache_stats(self) -> dict:
        """Get statistics about the cache."""
        if not self.cache_dir.exists():
            return {"file_count": 0, "total_size_mb": 0.0, "memory_cache_size": 0}

        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)

        return {
            "file_count": len(cache_files),
            "total_size_mb": total_size / (1024 * 1024),
            "memory_cache_size": len(self._cache),
            "cache_dir": str(self.cache_dir.absolute())
        }

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
