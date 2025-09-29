"""
Advanced Pydantic models for SEO research with competitor content analysis.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CompetitorContent(BaseModel):
    """Content extracted from competitor website."""
    url: str = Field(description="Full URL of the competitor page")
    domain: str = Field(description="Domain name")
    title: Optional[str] = Field(default=None, description="Page title")
    meta_description: Optional[str] = Field(default=None, description="Meta description")
    headings: List[str] = Field(default_factory=list, description="H1, H2, H3 headings")
    content_snippet: Optional[str] = Field(default=None, description="First 500 chars of content")
    keywords_found: List[str] = Field(default_factory=list, description="Keywords found in content")
    content_length: int = Field(default=0, description="Total content character count")
    last_scraped: datetime = Field(default_factory=datetime.now, description="When content was scraped")


class CompetitorAnalysis(BaseModel):
    """Analysis of a competitor based on content and search presence."""
    domain: str = Field(description="Competitor domain")
    authority_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Estimated domain authority (0-1)")
    content_quality: float = Field(default=0.0, ge=0.0, le=1.0, description="Content quality score (0-1)")
    keyword_overlap: float = Field(default=0.0, ge=0.0, le=1.0, description="Keyword overlap with target niche")
    content_gaps: List[str] = Field(default_factory=list, description="Content gaps we can exploit")
    content_data: Optional[CompetitorContent] = Field(default=None, description="Scraped content data")
    ranking_keywords: List[str] = Field(default_factory=list, description="Keywords they seem to rank for")


class KeywordOpportunity(BaseModel):
    """A keyword opportunity with competitive analysis."""
    keyword: str = Field(description="The target keyword")
    search_intent: str = Field(description="informational, commercial, transactional, navigational")
    difficulty_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Keyword difficulty (0=easy, 1=hard)")
    opportunity_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Overall opportunity score")
    competing_domains: List[str] = Field(default_factory=list, description="Domains competing for this keyword")
    content_angle: Optional[str] = Field(default=None, description="Recommended content approach")
    word_count: int = Field(description="Number of words in keyword")


class ContentStrategy(BaseModel):
    """Content strategy recommendations based on competitive analysis."""
    recommended_topics: List[str] = Field(default_factory=list, description="Topics to target")
    content_gaps: List[str] = Field(default_factory=list, description="Gaps in competitor content")
    content_angles: List[str] = Field(default_factory=list, description="Unique angles to pursue")
    target_keywords: List[str] = Field(default_factory=list, description="Priority keywords to target")
    competitive_advantages: List[str] = Field(default_factory=list, description="Our potential advantages")


class AdvancedSEOStrategy(BaseModel):
    """Advanced SEO research strategy with competitor content analysis."""
    niche: str = Field(description="The target niche/topic")
    primary_keywords: List[KeywordOpportunity] = Field(default_factory=list, description="Keyword opportunities")
    competitor_analyses: List[CompetitorAnalysis] = Field(default_factory=list, description="Detailed competitor analyses")
    search_strategies: List[str] = Field(default_factory=list, description="Search approaches for market research")
    content_strategy: ContentStrategy = Field(default_factory=ContentStrategy, description="Content strategy recommendations")
    analysis_depth: str = Field(default="basic", description="Depth of analysis performed")
    tavily_enabled: bool = Field(default=False, description="Whether Tavily search was used")
    content_scraping_enabled: bool = Field(default=False, description="Whether content scraping was performed")


    def get_top_opportunities(self, limit: int = 10) -> List[KeywordOpportunity]:
        """Get top keyword opportunities sorted by opportunity score."""
        return sorted(
            self.primary_keywords,
            key=lambda x: x.opportunity_score,
            reverse=True
        )[:limit]

    def get_low_competition_keywords(self, max_difficulty: float = 0.3) -> List[KeywordOpportunity]:
        """Get keywords with low competition difficulty."""
        return [
            kw for kw in self.primary_keywords
            if kw.difficulty_score <= max_difficulty
        ]

    def get_content_gaps(self) -> List[str]:
        """Get all unique content gaps across competitors."""
        gaps = set()
        for comp in self.competitor_analyses:
            gaps.update(comp.content_gaps)
        gaps.update(self.content_strategy.content_gaps)
        return list(gaps)