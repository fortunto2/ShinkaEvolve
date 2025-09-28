#!/usr/bin/env python3
"""
Debug test for SGR structured output parsing.
"""

import logging
import sys
from shinka.core.sgr_mutation_planner import SGRMutationPlanner
from shinka.database import Program
from shinka.llm import LLMClient

# Enable DEBUG logging to see structured output details
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_test_program():
    """Create a test program."""
    test_code = '''
def fibonacci(n):
    """Inefficient recursive Fibonacci."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''

    return Program(
        id="test-id",
        code=test_code,
        language="python",
        parent_id=None,
        generation=0,
        archive_inspiration_ids=[],
        top_k_inspiration_ids=[],
        code_diff=None,
        embedding=[],
        correct=True,
        combined_score=0.3,
        public_metrics={"accuracy": 0.3},
        private_metrics={},
        text_feedback="Slow recursive implementation",
        metadata={}
    )

def test_sgr_with_debug():
    """Test SGR with full debug logging."""
    logger.info("🧪 Testing SGR with DEBUG logging...")

    try:
        # Create LLM client
        llm_client = LLMClient(
            model_names=["gpt-5-mini"],
            verbose=True,
        )
        logger.info("✓ LLM client created")

        # Create SGR planner
        planner = SGRMutationPlanner(
            llm_client=llm_client,
            language="python",
            fallback_to_random=False  # Disable fallback to see raw errors
        )
        logger.info("✓ SGR planner created")

        # Create test program
        test_program = create_test_program()
        logger.info("✓ Test program created")

        # Test analysis
        logger.info("🔍 Starting SGR code analysis...")
        analysis = planner.analyze_code(test_program)

        if analysis:
            logger.info(f"✅ SGR analysis successful!")
            logger.info(f"   Complexity: {analysis.complexity}")
            logger.info(f"   Algorithm: {analysis.main_algorithm}")
            logger.info(f"   Bottlenecks: {analysis.performance_bottlenecks}")

            # Test strategy selection
            logger.info("🎯 Starting SGR strategy selection...")
            strategy = planner.select_strategy(
                analysis, test_program, [], [],
                "Consider optimizing for performance"
            )

            if strategy:
                logger.info(f"✅ SGR strategy successful!")
                logger.info(f"   Type: {strategy.strategy_type}")
                logger.info(f"   Confidence: {strategy.confidence}")
                logger.info(f"   Reasoning: {strategy.reasoning}")
            else:
                logger.error("❌ SGR strategy selection failed")

        else:
            logger.error("❌ SGR analysis failed")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sgr_with_debug()