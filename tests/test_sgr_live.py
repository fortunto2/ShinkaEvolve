#!/usr/bin/env python3
"""
Live test for SGR integration with real LLM calls.

This script tests the SGR functionality with actual LLM interactions to verify
the end-to-end workflow works correctly.

Note: This requires API keys to be configured.
"""

import os
import logging
from pathlib import Path
from shinka.core.sgr_schemas import CodeAnalysis, MutationStrategy
from shinka.core.sgr_mutation_planner import SGRMutationPlanner
from shinka.core.sgr_prompt_sampler import SGRPromptSampler
from shinka.database import Program
from shinka.llm import LLMClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_test_program(code: str, score: float = 0.5) -> Program:
    """Create a test Program object."""
    return Program(
        id="test-program-id",
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
        public_metrics={"accuracy": score, "performance": score * 0.8},
        private_metrics={"memory_usage": 1000},
        text_feedback="Program runs correctly but could be optimized for performance.",
        metadata={}
    )


def test_sgr_code_analysis():
    """Test SGR code analysis with real LLM."""
    logger.info("Testing SGR Code Analysis...")

    # Create a simple LLM client for testing
    try:
        llm_client = LLMClient(
            model_names=["gpt-4o-mini-2024-07-18"],
            verbose=True,
        )
    except Exception as e:
        logger.error(f"Failed to create LLM client: {e}")
        logger.error("Make sure API keys are configured in environment or .env file")
        return False

    # Create SGR planner
    planner = SGRMutationPlanner(
        llm_client=llm_client,
        language="python",
        fallback_to_random=True
    )

    # Test with a simple inefficient code
    test_code = '''
def fibonacci(n):
    """Inefficient recursive Fibonacci implementation."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    result = fibonacci(10)
    print(f"Fibonacci(10) = {result}")
'''

    test_program = create_test_program(test_code, score=0.3)

    try:
        analysis = planner.analyze_code(test_program)

        if analysis:
            logger.info("✓ SGR analysis successful!")
            logger.info(f"  Complexity: {analysis.complexity}")
            logger.info(f"  Algorithm: {analysis.main_algorithm}")
            logger.info(f"  Bottlenecks: {analysis.performance_bottlenecks}")
            logger.info(f"  Opportunities: {analysis.optimization_opportunities}")
            return True
        else:
            logger.warning("✗ SGR analysis failed - returned None")
            return False

    except Exception as e:
        logger.error(f"✗ SGR analysis failed with error: {e}")
        return False


def test_sgr_strategy_selection():
    """Test SGR mutation strategy selection."""
    logger.info("Testing SGR Strategy Selection...")

    try:
        llm_client = LLMClient(
            model_names=["gpt-4o-mini-2024-07-18"],
            verbose=True,
        )
    except Exception as e:
        logger.error(f"Failed to create LLM client: {e}")
        return False

    planner = SGRMutationPlanner(
        llm_client=llm_client,
        language="python"
    )

    # Create test program and inspirations
    parent_code = '''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
'''

    inspiration_code = '''
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
'''

    parent_program = create_test_program(parent_code, score=0.4)
    inspiration_program = create_test_program(inspiration_code, score=0.8)

    try:
        # Test complete mutation planning
        plan, fallback = planner.plan_mutation(
            parent_program,
            archive_inspirations=[inspiration_program],
            top_k_inspirations=[],
            meta_recommendations="Consider using more efficient sorting algorithms"
        )

        if plan:
            logger.info("✓ SGR mutation planning successful!")
            logger.info(f"  Strategy: {plan.strategy.strategy_type}")
            logger.info(f"  Confidence: {plan.strategy.confidence:.2f}")
            logger.info(f"  Reasoning: {plan.strategy.reasoning}")
            logger.info(f"  Expected improvement: {plan.strategy.expected_improvement}")
            return True
        elif fallback:
            logger.info(f"✓ SGR fallback strategy: {fallback}")
            return True
        else:
            logger.warning("✗ SGR planning failed - no plan or fallback")
            return False

    except Exception as e:
        logger.error(f"✗ SGR strategy selection failed: {e}")
        return False


def test_sgr_prompt_sampler():
    """Test SGR-enhanced PromptSampler."""
    logger.info("Testing SGR PromptSampler...")

    try:
        # Test with SGR enabled
        sgr_sampler = SGRPromptSampler(
            sgr_enabled=True,
            sgr_confidence_threshold=0.6,  # Lower threshold for testing
            language="python",
            use_text_feedback=True
        )

        test_code = '''
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
'''

        parent = create_test_program(test_code, score=0.5)
        archive_inspirations = []
        top_k_inspirations = []

        # Sample with SGR
        sys_msg, user_msg, patch_type = sgr_sampler.sample(
            parent, archive_inspirations, top_k_inspirations
        )

        logger.info("✓ SGR PromptSampler completed!")
        logger.info(f"  Selected strategy: {patch_type}")
        logger.info(f"  System message length: {len(sys_msg)}")
        logger.info(f"  User message length: {len(user_msg)}")

        # Check statistics
        stats = sgr_sampler.get_sgr_statistics()
        logger.info(f"  SGR Statistics: {stats}")

        return True

    except Exception as e:
        logger.error(f"✗ SGR PromptSampler test failed: {e}")
        return False


def test_sgr_without_api_keys():
    """Test SGR behavior when API keys are not available."""
    logger.info("Testing SGR fallback behavior...")

    try:
        # Create sampler with fallback enabled
        sampler = SGRPromptSampler(
            sgr_enabled=True,
            sgr_fallback_to_random=True,
            language="python"
        )

        test_program = create_test_program("def test(): pass")

        # This should work even without API keys by falling back
        sys_msg, user_msg, patch_type = sampler.sample(
            test_program, [], []
        )

        logger.info("✓ SGR fallback behavior working!")
        logger.info(f"  Strategy: {patch_type}")

        stats = sampler.get_sgr_statistics()
        logger.info(f"  Fallback rate: {stats.get('fallback_rate', 0.0):.2f}")

        return True

    except Exception as e:
        logger.error(f"✗ SGR fallback test failed: {e}")
        return False


def main():
    """Run all SGR live tests."""
    logger.info("=" * 60)
    logger.info("SGR Live Integration Tests")
    logger.info("=" * 60)

    tests = [
        ("Code Analysis", test_sgr_code_analysis),
        ("Strategy Selection", test_sgr_strategy_selection),
        ("PromptSampler", test_sgr_prompt_sampler),
        ("Fallback Behavior", test_sgr_without_api_keys),
    ]

    results = []
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Results Summary:")
    logger.info("=" * 60)

    passed = 0
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        logger.info(f"  {test_name}: {status}")
        if success:
            passed += 1

    logger.info(f"\nOverall: {passed}/{len(results)} tests passed")

    if passed == len(results):
        logger.info("🎉 All SGR tests passed!")
        return True
    else:
        logger.warning(f"⚠️  {len(results) - passed} tests failed")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)