#!/usr/bin/env python3
"""
Demo test for SGR integration without real LLM calls.

This script demonstrates the SGR functionality with mocked LLM responses
to show how the system works end-to-end.
"""

import logging
from unittest.mock import Mock, patch
from shinka.core.sgr_schemas import CodeAnalysis, MutationStrategy, CodeMutationPlan
from shinka.core.sgr_mutation_planner import SGRMutationPlanner
from shinka.core.sgr_prompt_sampler import SGRPromptSampler
from shinka.database import Program
from shinka.llm import LLMClient, QueryResult

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
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


def demo_sgr_schemas():
    """Demonstrate SGR schema validation."""
    logger.info("🔍 Демонстрация SGR схем...")

    # Code Analysis schema
    analysis = CodeAnalysis(
        complexity="high",
        main_algorithm="recursive Fibonacci with exponential complexity",
        performance_bottlenecks=["exponential time complexity", "repeated calculations"],
        code_quality_issues=["no memoization", "deep recursion"],
        optimization_opportunities=["add memoization", "use iterative approach", "use dynamic programming"]
    )

    logger.info(f"✓ Анализ кода: сложность={analysis.complexity}")
    logger.info(f"  Алгоритм: {analysis.main_algorithm}")
    logger.info(f"  Узкие места: {', '.join(analysis.performance_bottlenecks)}")

    # Mutation Strategy schema
    strategy = MutationStrategy(
        strategy_type="full",
        confidence=0.85,
        reasoning="Code has fundamental algorithmic inefficiency requiring complete rewrite",
        target_areas=["fibonacci function", "main algorithm"],
        expected_improvement="performance",
        risk_level="medium"
    )

    logger.info(f"✓ Стратегия мутации: {strategy.strategy_type} (уверенность: {strategy.confidence:.1%})")
    logger.info(f"  Обоснование: {strategy.reasoning}")

    # Complete plan
    plan = CodeMutationPlan(
        analysis=analysis,
        strategy=strategy,
        mutation_focus=["fibonacci implementation"],
        success_criteria="Reduce time complexity from O(2^n) to O(n)"
    )

    logger.info(f"✓ План мутации создан: фокус на {', '.join(plan.mutation_focus)}")
    return plan


def demo_sgr_with_mocked_llm():
    """Demonstrate SGR with mocked LLM responses."""
    logger.info("🤖 Демонстрация SGR с мокированными LLM ответами...")

    # Create mock LLM client
    mock_llm_client = Mock(spec=LLMClient)
    mock_llm_client.model_names = ["gpt-4o-mini"]
    mock_llm_client.llm_selection = None
    mock_llm_client.verbose = False

    # Mock analysis response
    mock_analysis = CodeAnalysis(
        complexity="medium",
        main_algorithm="bubble sort algorithm implementation",
        performance_bottlenecks=["nested loops O(n²)", "unnecessary swaps"],
        code_quality_issues=["missing type hints", "no early termination"],
        optimization_opportunities=["use quicksort", "add early termination", "in-place optimization"]
    )

    mock_analysis_result = Mock(spec=QueryResult)
    mock_analysis_result.parsed_content = mock_analysis
    mock_analysis_result.content = '{"complexity": "medium", "main_algorithm": "bubble sort"}'

    # Mock strategy response
    mock_strategy = MutationStrategy(
        strategy_type="diff",
        confidence=0.75,
        reasoning="Code structure is good but needs algorithmic improvements",
        target_areas=["sorting loop", "swap logic"],
        expected_improvement="performance",
        risk_level="low"
    )

    mock_strategy_result = Mock(spec=QueryResult)
    mock_strategy_result.parsed_content = mock_strategy

    # Create planner with mocked responses
    with patch('shinka.core.sgr_mutation_planner.LLMClient') as mock_llm_class:
        # Setup mocked LLM clients
        mock_analysis_llm = Mock()
        mock_analysis_llm.query.return_value = mock_analysis_result

        mock_strategy_llm = Mock()
        mock_strategy_llm.query.return_value = mock_strategy_result

        # Create planner
        planner = SGRMutationPlanner(mock_llm_client)
        planner.analysis_llm = mock_analysis_llm
        planner.strategy_llm = mock_strategy_llm

        # Test with bubble sort code
        test_code = '''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def main():
    data = [64, 34, 25, 12, 22, 11, 90]
    sorted_data = bubble_sort(data.copy())
    print(f"Sorted: {sorted_data}")
'''

        test_program = create_test_program(test_code, score=0.4)
        inspiration = create_test_program("def quick_sort(arr): pass", score=0.8)

        # Test mutation planning
        plan, fallback = planner.plan_mutation(
            test_program,
            archive_inspirations=[inspiration],
            top_k_inspirations=[],
            meta_recommendations="Consider using more efficient sorting algorithms like quicksort or mergesort"
        )

        if plan:
            logger.info("✓ SGR планирование успешно!")
            logger.info(f"  Анализ: {plan.analysis.main_algorithm}")
            logger.info(f"  Стратегия: {plan.strategy.strategy_type} (уверенность: {plan.strategy.confidence:.1%})")
            logger.info(f"  Обоснование: {plan.strategy.reasoning}")
            logger.info(f"  Цель: {plan.strategy.expected_improvement}")
            logger.info(f"  Критерии успеха: {plan.success_criteria}")
        else:
            logger.warning(f"SGR планирование не удалось, fallback: {fallback}")

        return plan


def demo_sgr_prompt_sampler():
    """Demonstrate SGR PromptSampler with fallback."""
    logger.info("📝 Демонстрация SGR PromptSampler...")

    # Test with SGR disabled (baseline)
    baseline_sampler = SGRPromptSampler(sgr_enabled=False)

    test_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''

    test_program = create_test_program(test_code, score=0.3)

    # Sample with baseline
    sys_msg, user_msg, patch_type = baseline_sampler.sample(
        test_program, [], []
    )

    logger.info("✓ Baseline PromptSampler:")
    logger.info(f"  Выбранная стратегия: {patch_type}")
    logger.info(f"  Длина системного сообщения: {len(sys_msg)}")
    logger.info(f"  Длина пользовательского сообщения: {len(user_msg)}")

    # Test with SGR enabled but will fallback due to no LLM
    sgr_sampler = SGRPromptSampler(
        sgr_enabled=True,
        sgr_fallback_to_random=True,
        sgr_confidence_threshold=0.7
    )

    sys_msg_sgr, user_msg_sgr, patch_type_sgr = sgr_sampler.sample(
        test_program, [], []
    )

    logger.info("✓ SGR PromptSampler (с fallback):")
    logger.info(f"  Выбранная стратегия: {patch_type_sgr}")
    logger.info(f"  Длина системного сообщения: {len(sys_msg_sgr)}")

    # Check statistics
    stats = sgr_sampler.get_sgr_statistics()
    logger.info(f"  SGR статистика: попыток={stats['total_attempts']}, fallback={stats['fallback_used']}")

    return patch_type_sgr


def demo_sgr_integration_workflow():
    """Demonstrate complete SGR integration workflow."""
    logger.info("🔄 Демонстрация полного SGR workflow...")

    # Step 1: Create test program with performance issues
    inefficient_code = '''
def find_max(numbers):
    max_val = numbers[0]
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if numbers[j] > max_val:
                max_val = numbers[j]
    return max_val

def main():
    data = [3, 7, 1, 9, 2, 8, 5]
    result = find_max(data)
    print(f"Maximum: {result}")
'''

    program = create_test_program(inefficient_code, score=0.2)
    logger.info(f"📊 Исходная программа: score={program.combined_score}")

    # Step 2: Demonstrate manual schema creation (simulating LLM output)
    analysis = CodeAnalysis(
        complexity="low",
        main_algorithm="nested loop maximum finding with O(n²) complexity",
        performance_bottlenecks=["unnecessary nested loop", "repeated comparisons"],
        code_quality_issues=["inefficient algorithm"],
        optimization_opportunities=["single pass algorithm", "use built-in max function"]
    )

    strategy = MutationStrategy(
        strategy_type="diff",
        confidence=0.9,
        reasoning="Simple algorithmic fix can dramatically improve performance",
        target_areas=["find_max function", "loop structure"],
        expected_improvement="performance",
        risk_level="low"
    )

    plan = CodeMutationPlan(
        analysis=analysis,
        strategy=strategy,
        mutation_focus=["find_max algorithm"],
        success_criteria="Reduce time complexity from O(n²) to O(n)"
    )

    logger.info("✓ SGR анализ и планирование:")
    logger.info(f"  Стратегия: {plan.strategy.strategy_type}")
    logger.info(f"  Уверенность: {plan.strategy.confidence:.1%}")
    logger.info(f"  Фокус: {', '.join(plan.mutation_focus)}")
    logger.info(f"  Ожидаемое улучшение: {plan.strategy.expected_improvement}")

    # Step 3: Simulate improved program
    improved_code = '''
def find_max(numbers):
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def main():
    data = [3, 7, 1, 9, 2, 8, 5]
    result = find_max(data)
    print(f"Maximum: {result}")
'''

    improved_program = create_test_program(improved_code, score=0.9)
    logger.info(f"📈 Улучшенная программа: score={improved_program.combined_score}")
    logger.info(f"📊 Улучшение: {(improved_program.combined_score - program.combined_score):.1f}")

    return plan


def main():
    """Run SGR demo."""
    logger.info("=" * 60)
    logger.info("🚀 Schema-Guided Reasoning (SGR) для ShinkaEvolve - Демонстрация")
    logger.info("=" * 60)

    try:
        # Demo 1: Basic schemas
        plan1 = demo_sgr_schemas()
        logger.info("")

        # Demo 2: Mocked LLM interaction
        plan2 = demo_sgr_with_mocked_llm()
        logger.info("")

        # Demo 3: PromptSampler integration
        strategy = demo_sgr_prompt_sampler()
        logger.info("")

        # Demo 4: Complete workflow
        plan3 = demo_sgr_integration_workflow()
        logger.info("")

        logger.info("=" * 60)
        logger.info("✅ Все демонстрации SGR выполнены успешно!")
        logger.info("=" * 60)
        logger.info("Ключевые возможности SGR:")
        logger.info("• 🔍 Структурированный анализ кода")
        logger.info("• 🎯 Интеллектуальный выбор стратегии мутации")
        logger.info("• 📊 Проверяемые и воспроизводимые решения")
        logger.info("• 🔄 Интеграция с существующим workflow ShinkaEvolve")
        logger.info("• 📈 Повышение эффективности эволюции кода")

        return True

    except Exception as e:
        logger.error(f"❌ Ошибка в демонстрации: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)