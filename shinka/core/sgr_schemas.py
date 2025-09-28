"""
Schema-Guided Reasoning (SGR) schemas for ShinkaEvolve.

This module defines Pydantic models for structured LLM outputs in the evolution process.
Based on the SGR approach for more predictable and verifiable LLM reasoning.
"""

from typing import List, Dict, Optional, Literal, Union
from pydantic import BaseModel, Field
from annotated_types import Ge, Le


class CodeAnalysis(BaseModel):
    """Analysis of a code program for mutation strategy selection."""

    complexity: Literal["low", "medium", "high"]
    main_algorithm: str = Field(description="Brief description of the main algorithm")
    performance_bottlenecks: List[str] = Field(default_factory=list)
    code_quality_issues: List[str] = Field(default_factory=list)
    optimization_opportunities: List[str] = Field(default_factory=list)


class MutationStrategy(BaseModel):
    """Structured decision for code mutation approach."""

    strategy_type: Literal["diff", "full", "cross", "focused"]
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in this strategy choice")
    reasoning: str = Field(description="Explanation for why this strategy was chosen")
    target_areas: List[str] = Field(
        default_factory=list,
        description="Specific code areas to focus mutations on"
    )
    expected_improvement: Literal["performance", "correctness", "efficiency", "readability"]
    risk_level: Literal["low", "medium", "high"] = "medium"


class CodeMutationPlan(BaseModel):
    """Complete plan for code mutation including analysis and strategy."""

    analysis: CodeAnalysis
    strategy: MutationStrategy
    mutation_focus: List[str] = Field(
        default_factory=list,
        description="Specific functions/blocks to modify"
    )
    success_criteria: str = Field(
        description="How to measure if the mutation was successful"
    )


class EvaluationFeedback(BaseModel):
    """Structured feedback from code evaluation."""

    is_correct: bool
    score_improvement: float = Field(description="Change in combined score from parent")
    performance_category: Literal["excellent", "good", "average", "poor", "failed"]
    failure_reason: Optional[Literal["syntax", "logic", "timeout", "memory", "other"]] = None
    improvement_suggestions: List[str] = Field(default_factory=list)
    learned_patterns: List[str] = Field(
        default_factory=list,
        description="Patterns that can be reused in future mutations"
    )


class NoveltyAssessment(BaseModel):
    """Assessment of code novelty for rejection sampling."""

    is_novel: bool
    similarity_score: float = Field(ge=0.0, le=1.0)
    reasoning: str
    similar_program_ids: List[str] = Field(default_factory=list)
    novelty_aspects: List[Literal["algorithm", "approach", "optimization", "structure"]] = Field(
        default_factory=list
    )
    should_accept: bool = Field(description="Final decision on whether to accept this mutation")


class MetaRecommendation(BaseModel):
    """Structured meta-recommendation for evolution guidance."""

    recommendation_type: Literal["technique", "pattern", "optimization", "debugging", "strategy"]
    title: str = Field(description="Short title for the recommendation")
    description: str = Field(description="Detailed description of the recommendation")
    confidence: float = Field(ge=0.0, le=1.0)
    applicable_contexts: List[str] = Field(
        default_factory=list,
        description="When this recommendation applies"
    )
    example_code: Optional[str] = None
    priority: Literal["high", "medium", "low"] = "medium"


class MetaSummary(BaseModel):
    """Structured summary of meta-learning insights."""

    successful_patterns: List[str] = Field(default_factory=list)
    failed_approaches: List[str] = Field(default_factory=list)
    key_insights: List[str] = Field(default_factory=list)
    recommendations: List[MetaRecommendation] = Field(default_factory=list)
    evolution_stage: Literal["early", "middle", "late", "converged"]
    next_focus_areas: List[str] = Field(default_factory=list)