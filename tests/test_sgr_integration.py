"""
Test SGR integration in ShinkaEvolve.

This module provides unit tests and integration tests for the SGR functionality.
"""

import pytest
import json
from unittest.mock import Mock, patch
from shinka.core.sgr_schemas import (
    CodeAnalysis,
    MutationStrategy,
    CodeMutationPlan,
    EvaluationFeedback,
    NoveltyAssessment,
    MetaRecommendation,
)
from shinka.core.sgr_mutation_planner import SGRMutationPlanner
from shinka.core.sgr_prompt_sampler import SGRPromptSampler
from shinka.database import Program
from shinka.llm import LLMClient, QueryResult


class TestSGRSchemas:
    """Test SGR Pydantic schemas."""

    def test_code_analysis_schema(self):
        """Test CodeAnalysis schema validation."""
        analysis = CodeAnalysis(
            complexity="medium",
            main_algorithm="bubble sort algorithm",
            performance_bottlenecks=["nested loops", "unnecessary comparisons"],
            code_quality_issues=["missing comments"],
            optimization_opportunities=["use quicksort", "early termination"]
        )

        assert analysis.complexity == "medium"
        assert "bubble sort" in analysis.main_algorithm
        assert len(analysis.performance_bottlenecks) == 2

        # Test validation
        with pytest.raises(ValueError):
            CodeAnalysis(complexity="invalid", main_algorithm="test")

    def test_mutation_strategy_schema(self):
        """Test MutationStrategy schema validation."""
        strategy = MutationStrategy(
            strategy_type="diff",
            confidence=0.85,
            reasoning="Code has localized performance issues",
            target_areas=["sorting function", "input validation"],
            expected_improvement="performance",
            risk_level="low"
        )

        assert strategy.strategy_type == "diff"
        assert 0.8 <= strategy.confidence <= 0.9
        assert strategy.risk_level == "low"

        # Test confidence bounds
        with pytest.raises(ValueError):
            MutationStrategy(
                strategy_type="diff",
                confidence=1.5,  # Invalid confidence > 1.0
                reasoning="test",
                expected_improvement="performance"
            )

    def test_code_mutation_plan_schema(self):
        """Test complete CodeMutationPlan schema."""
        analysis = CodeAnalysis(
            complexity="low",
            main_algorithm="linear search",
            performance_bottlenecks=["O(n) search"],
            optimization_opportunities=["binary search"]
        )

        strategy = MutationStrategy(
            strategy_type="focused",
            confidence=0.9,
            reasoning="Simple optimization case",
            expected_improvement="performance"
        )

        plan = CodeMutationPlan(
            analysis=analysis,
            strategy=strategy,
            mutation_focus=["search_function"],
            success_criteria="Reduce time complexity to O(log n)"
        )

        assert plan.analysis.complexity == "low"
        assert plan.strategy.strategy_type == "focused"
        assert "search_function" in plan.mutation_focus


class TestSGRMutationPlanner:
    """Test SGR Mutation Planner."""

    def create_mock_program(self, code="def test(): pass", score=0.5):
        """Create a mock Program object."""
        return Program(
            id="test-id",
            code=code,
            language="python",
            parent_id=None,
            generation=0,
            archive_inspiration_ids=[],
            top_k_inspiration_ids=[],
            code_diff=None,
            embedding=[],
            correct=True,
            combined_score=score,
            public_metrics={"accuracy": score},
            private_metrics={},
            text_feedback="",
            metadata={}
        )

    def create_mock_llm_client(self):
        """Create a mock LLM client."""
        mock_client = Mock(spec=LLMClient)
        mock_client.model_names = ["gpt-4o-mini"]
        mock_client.llm_selection = None
        mock_client.verbose = False
        return mock_client

    def test_sgr_planner_initialization(self):
        """Test SGR planner initialization."""
        mock_llm = self.create_mock_llm_client()
        planner = SGRMutationPlanner(
            llm_client=mock_llm,
            language="python",
            fallback_to_random=True
        )

        assert planner.language == "python"
        assert planner.fallback_to_random is True
        assert planner.analysis_llm is not None
        assert planner.strategy_llm is not None

    @patch('shinka.core.sgr_mutation_planner.LLMClient')
    def test_code_analysis_success(self, mock_llm_class):
        """Test successful code analysis."""
        # Create mock LLM client
        mock_llm = self.create_mock_llm_client()

        # Create mock query result with structured output
        mock_analysis = CodeAnalysis(
            complexity="medium",
            main_algorithm="sorting algorithm",
            performance_bottlenecks=["nested loops"],
            optimization_opportunities=["use built-in sort"]
        )

        mock_result = Mock(spec=QueryResult)
        mock_result.parsed_content = mock_analysis

        # Setup mock LLM client to return our mock analysis
        mock_analysis_llm = Mock()
        mock_analysis_llm.query.return_value = mock_result

        # Create planner with mocked LLM
        planner = SGRMutationPlanner(mock_llm)
        planner.analysis_llm = mock_analysis_llm

        # Test analysis
        program = self.create_mock_program("def sort_array(arr): return sorted(arr)")
        result = planner.analyze_code(program)

        assert result is not None
        assert result.complexity == "medium"
        assert "sorting algorithm" in result.main_algorithm

    def test_code_analysis_failure(self):
        """Test code analysis failure handling."""
        mock_llm = self.create_mock_llm_client()
        planner = SGRMutationPlanner(mock_llm)

        # Mock LLM to return None (failure case)
        planner.analysis_llm = Mock()
        planner.analysis_llm.query.return_value = None

        program = self.create_mock_program()
        result = planner.analyze_code(program)

        assert result is None

    def test_fallback_strategy(self):
        """Test fallback strategy selection."""
        mock_llm = self.create_mock_llm_client()
        planner = SGRMutationPlanner(mock_llm, fallback_to_random=True)

        fallback = planner._get_fallback_strategy()
        assert fallback in ["diff", "full"]

        # Test disabled fallback
        planner.fallback_to_random = False
        fallback = planner._get_fallback_strategy()
        assert fallback is None


class TestSGRPromptSampler:
    """Test SGR-enhanced PromptSampler."""

    def create_mock_program(self, code="def test(): pass", score=0.5):
        """Create a mock Program object."""
        return Program(
            id="test-id",
            code=code,
            language="python",
            parent_id=None,
            generation=0,
            archive_inspiration_ids=[],
            top_k_inspiration_ids=[],
            code_diff=None,
            embedding=[],
            correct=True,
            combined_score=score,
            public_metrics={"accuracy": score},
            private_metrics={},
            text_feedback="Test feedback",
            metadata={}
        )

    def test_sgr_prompt_sampler_initialization(self):
        """Test SGR prompt sampler initialization."""
        sampler = SGRPromptSampler(
            sgr_enabled=True,
            sgr_confidence_threshold=0.8,
            sgr_fallback_to_random=True
        )

        assert sampler.sgr_enabled is True
        assert sampler.sgr_confidence_threshold == 0.8
        assert sampler.sgr_planner is not None
        assert sampler.sgr_stats["total_attempts"] == 0

    def test_sgr_disabled_fallback(self):
        """Test that disabled SGR falls back to original behavior."""
        sampler = SGRPromptSampler(sgr_enabled=False)

        parent = self.create_mock_program()
        archive_inspirations = []
        top_k_inspirations = []

        # This should use the original sampler logic
        sys_msg, user_msg, patch_type = sampler.sample(
            parent, archive_inspirations, top_k_inspirations
        )

        assert isinstance(sys_msg, str)
        assert isinstance(user_msg, str)
        assert patch_type in ["diff", "full", "cross"]
        assert sampler.sgr_stats["fallback_used"] == 1

    def test_sgr_statistics_tracking(self):
        """Test SGR statistics tracking."""
        sampler = SGRPromptSampler(sgr_enabled=True)

        # Initial stats
        stats = sampler.get_sgr_statistics()
        assert stats["total_attempts"] == 0

        # Mock a failed SGR attempt
        sampler.sgr_stats["total_attempts"] = 5
        sampler.sgr_stats["sgr_failures"] = 2
        sampler.sgr_stats["fallback_used"] = 3

        stats = sampler.get_sgr_statistics()
        assert stats["fallback_rate"] == 0.6

        # Reset stats
        sampler.reset_sgr_statistics()
        assert sampler.sgr_stats["total_attempts"] == 0


class TestSGRIntegration:
    """Integration tests for SGR components."""

    def create_mock_program(self, code="def test(): pass", score=0.5):
        """Create a mock Program object."""
        return Program(
            id="test-id",
            code=code,
            language="python",
            parent_id=None,
            generation=0,
            archive_inspiration_ids=[],
            top_k_inspiration_ids=[],
            code_diff=None,
            embedding=[],
            correct=True,
            combined_score=score,
            public_metrics={"accuracy": score},
            private_metrics={},
            text_feedback="Test feedback",
            metadata={}
        )

    def test_schema_serialization(self):
        """Test that schemas can be serialized/deserialized."""
        analysis = CodeAnalysis(
            complexity="high",
            main_algorithm="complex sorting",
            performance_bottlenecks=["memory usage"],
            optimization_opportunities=["parallel processing"]
        )

        # Test JSON serialization
        json_data = analysis.model_dump()
        assert json_data["complexity"] == "high"

        # Test deserialization
        restored = CodeAnalysis(**json_data)
        assert restored.complexity == analysis.complexity
        assert restored.main_algorithm == analysis.main_algorithm

    def test_end_to_end_mock_workflow(self):
        """Test end-to-end SGR workflow with mocked LLM responses."""
        # Create a sampler with SGR disabled for baseline
        baseline_sampler = SGRPromptSampler(sgr_enabled=False)

        # Create test data
        parent = self.create_mock_program(
            code="def fibonacci(n):\n    if n <= 1: return n\n    return fibonacci(n-1) + fibonacci(n-2)",
            score=0.3
        )

        archive_inspirations = [
            self.create_mock_program("def fib_memo(n, memo={}): pass", 0.8)
        ]
        top_k_inspirations = []

        # Test baseline behavior
        sys_msg, user_msg, patch_type = baseline_sampler.sample(
            parent, archive_inspirations, top_k_inspirations
        )

        assert isinstance(sys_msg, str)
        assert isinstance(user_msg, str)
        assert patch_type in ["diff", "full", "cross"]

        # Verify fibonacci code is in the user message
        assert "fibonacci" in user_msg


if __name__ == "__main__":
    # Run basic tests if executed directly
    test_schemas = TestSGRSchemas()
    test_schemas.test_code_analysis_schema()
    test_schemas.test_mutation_strategy_schema()
    test_schemas.test_code_mutation_plan_schema()
    print("✓ SGR schemas tests passed")

    test_integration = TestSGRIntegration()
    test_integration.test_schema_serialization()
    test_integration.test_end_to_end_mock_workflow()
    print("✓ SGR integration tests passed")

    print("All SGR tests completed successfully!")