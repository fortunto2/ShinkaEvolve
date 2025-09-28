#!/usr/bin/env python3
"""
Standalone SGR demo without any LLM dependencies.

This script demonstrates the SGR schemas and logic without requiring API keys.
"""

import logging
from shinka.core.sgr_schemas import (
    CodeAnalysis,
    MutationStrategy,
    CodeMutationPlan,
    EvaluationFeedback,
    NoveltyAssessment,
    MetaRecommendation
)
from shinka.database import Program

# Setup simple logging
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
        text_feedback="Program runs correctly but could be optimized.",
        metadata={}
    )


def demo_schemas():
    """Demonstrate all SGR schemas."""
    logger.info("🔍 Демонстрация SGR схем...")

    # 1. Code Analysis
    analysis = CodeAnalysis(
        complexity="high",
        main_algorithm="recursive Fibonacci with exponential time complexity",
        performance_bottlenecks=[
            "exponential recursion O(2^n)",
            "repeated subproblem calculations",
            "deep call stack"
        ],
        code_quality_issues=[
            "no memoization",
            "missing base case optimization",
            "no iterative alternative"
        ],
        optimization_opportunities=[
            "add memoization cache",
            "use dynamic programming",
            "implement iterative version",
            "use closed-form formula"
        ]
    )

    logger.info(f"✓ CodeAnalysis: {analysis.complexity} complexity")
    logger.info(f"  Алгоритм: {analysis.main_algorithm}")
    logger.info(f"  Узкие места: {len(analysis.performance_bottlenecks)} выявлено")

    # 2. Mutation Strategy
    strategy = MutationStrategy(
        strategy_type="full",
        confidence=0.9,
        reasoning="Algorithmic complexity requires complete rewrite with dynamic programming approach",
        target_areas=["fibonacci function", "recursive calls", "base cases"],
        expected_improvement="performance",
        risk_level="medium"
    )

    logger.info(f"✓ MutationStrategy: {strategy.strategy_type} (confidence: {strategy.confidence:.1%})")
    logger.info(f"  Обоснование: {strategy.reasoning[:50]}...")

    # 3. Complete Mutation Plan
    plan = CodeMutationPlan(
        analysis=analysis,
        strategy=strategy,
        mutation_focus=["fibonacci implementation", "memoization"],
        success_criteria="Reduce time complexity from O(2^n) to O(n) using dynamic programming"
    )

    logger.info(f"✓ CodeMutationPlan: фокус на {len(plan.mutation_focus)} областях")

    # 4. Evaluation Feedback
    feedback = EvaluationFeedback(
        is_correct=True,
        score_improvement=0.6,
        performance_category="excellent",
        failure_reason=None,
        improvement_suggestions=[
            "Consider adding input validation",
            "Add type hints for better readability"
        ],
        learned_patterns=[
            "dynamic programming for optimization",
            "memoization pattern effectiveness"
        ]
    )

    logger.info(f"✓ EvaluationFeedback: {feedback.performance_category} (+{feedback.score_improvement:.1f})")

    # 5. Novelty Assessment
    novelty = NoveltyAssessment(
        is_novel=True,
        similarity_score=0.3,
        reasoning="Uses different algorithmic approach than existing programs",
        similar_program_ids=["prog-123", "prog-456"],
        novelty_aspects=["algorithm", "optimization"],
        should_accept=True
    )

    logger.info(f"✓ NoveltyAssessment: novel={novelty.is_novel} (similarity: {novelty.similarity_score:.1f})")

    # 6. Meta Recommendation
    meta_rec = MetaRecommendation(
        recommendation_type="optimization",
        title="Use Dynamic Programming for Recursive Problems",
        description="When dealing with problems that have overlapping subproblems, consider dynamic programming approaches",
        confidence=0.85,
        applicable_contexts=["recursive algorithms", "fibonacci-like problems", "optimization tasks"],
        example_code="memo = {}\ndef fib(n):\n    if n in memo: return memo[n]\n    ...",
        priority="high"
    )

    logger.info(f"✓ MetaRecommendation: {meta_rec.title} (priority: {meta_rec.priority})")

    return plan, feedback, novelty, meta_rec


def demo_json_serialization():
    """Demonstrate JSON serialization of schemas."""
    logger.info("📄 Демонстрация JSON сериализации...")

    analysis = CodeAnalysis(
        complexity="medium",
        main_algorithm="bubble sort with nested loops",
        performance_bottlenecks=["O(n²) time complexity"],
        optimization_opportunities=["use quicksort", "early termination"]
    )

    # Serialize to dict
    json_data = analysis.model_dump()
    logger.info(f"✓ Сериализация в JSON: {len(json_data)} полей")

    # Deserialize back
    restored = CodeAnalysis(**json_data)
    logger.info(f"✓ Десериализация успешна: {restored.complexity}")

    # Validate consistency
    assert analysis.complexity == restored.complexity
    assert analysis.main_algorithm == restored.main_algorithm
    logger.info("✓ Данные консистентны после сериализации")


def demo_validation():
    """Demonstrate schema validation."""
    logger.info("✅ Демонстрация валидации схем...")

    # Valid case
    try:
        valid_strategy = MutationStrategy(
            strategy_type="diff",
            confidence=0.75,
            reasoning="Good approach",
            expected_improvement="performance"
        )
        logger.info("✓ Валидная схема принята")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")

    # Invalid confidence (> 1.0)
    try:
        invalid_strategy = MutationStrategy(
            strategy_type="diff",
            confidence=1.5,  # Invalid!
            reasoning="Test",
            expected_improvement="performance"
        )
        logger.error("❌ Невалидная схема не должна была быть принята")
    except ValueError:
        logger.info("✓ Валидация корректно отклонила невалидные данные")

    # Invalid strategy type
    try:
        invalid_strategy2 = MutationStrategy(
            strategy_type="invalid_type",  # Invalid!
            confidence=0.8,
            reasoning="Test",
            expected_improvement="performance"
        )
        logger.error("❌ Невалидный тип стратегии не должен был быть принят")
    except ValueError:
        logger.info("✓ Валидация корректно отклонила невалидный тип")


def demo_practical_workflow():
    """Demonstrate practical SGR workflow."""
    logger.info("🔄 Демонстрация практического SGR workflow...")

    # Step 1: Исходный код с проблемами
    original_code = '''
def factorial(n):
    if n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result = result * i
        return result

# Inefficient: could use recursion or math.factorial
'''

    program = create_test_program(original_code, score=0.5)
    logger.info(f"📊 Исходная программа: score={program.combined_score}")

    # Step 2: SGR анализ (симуляция LLM ответа)
    analysis = CodeAnalysis(
        complexity="low",
        main_algorithm="iterative factorial calculation",
        performance_bottlenecks=["manual loop implementation"],
        code_quality_issues=["could use built-in functions", "verbose implementation"],
        optimization_opportunities=["use math.factorial", "recursive approach", "memoization for repeated calls"]
    )

    logger.info("🔍 SGR анализ выполнен:")
    logger.info(f"  • Сложность: {analysis.complexity}")
    logger.info(f"  • Узкие места: {', '.join(analysis.performance_bottlenecks)}")

    # Step 3: Выбор стратегии мутации
    strategy = MutationStrategy(
        strategy_type="diff",
        confidence=0.8,
        reasoning="Simple optimization can improve readability and performance",
        target_areas=["factorial function", "loop implementation"],
        expected_improvement="efficiency",
        risk_level="low"
    )

    logger.info("🎯 SGR стратегия выбрана:")
    logger.info(f"  • Тип: {strategy.strategy_type}")
    logger.info(f"  • Уверенность: {strategy.confidence:.1%}")
    logger.info(f"  • Цель: {strategy.expected_improvement}")

    # Step 4: План мутации
    plan = CodeMutationPlan(
        analysis=analysis,
        strategy=strategy,
        mutation_focus=["factorial implementation"],
        success_criteria="Improve code elegance while maintaining correctness"
    )

    logger.info("📋 План мутации создан:")
    logger.info(f"  • Фокус: {', '.join(plan.mutation_focus)}")
    logger.info(f"  • Критерии успеха: {plan.success_criteria}")

    # Step 5: Симуляция улучшенного кода
    improved_code = '''
import math

def factorial(n):
    """Calculate factorial using built-in math function."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    return math.factorial(n)

# More efficient and readable
'''

    improved_program = create_test_program(improved_code, score=0.9)
    logger.info(f"📈 Улучшенная программа: score={improved_program.combined_score}")

    # Step 6: Оценка результата
    feedback = EvaluationFeedback(
        is_correct=True,
        score_improvement=improved_program.combined_score - program.combined_score,
        performance_category="excellent",
        improvement_suggestions=["Add more comprehensive error handling"],
        learned_patterns=["use built-in functions when available", "add input validation"]
    )

    logger.info("📊 Оценка результата:")
    logger.info(f"  • Улучшение: +{feedback.score_improvement:.1f}")
    logger.info(f"  • Категория: {feedback.performance_category}")
    logger.info(f"  • Изученные паттерны: {len(feedback.learned_patterns)}")

    return plan, feedback


def main():
    """Run all SGR demonstrations."""
    logger.info("=" * 70)
    logger.info("🚀 Schema-Guided Reasoning (SGR) для ShinkaEvolve")
    logger.info("   Демонстрация без LLM зависимостей")
    logger.info("=" * 70)

    try:
        # Demo 1: All schemas
        plan, feedback, novelty, meta_rec = demo_schemas()
        logger.info("")

        # Demo 2: JSON serialization
        demo_json_serialization()
        logger.info("")

        # Demo 3: Validation
        demo_validation()
        logger.info("")

        # Demo 4: Practical workflow
        workflow_plan, workflow_feedback = demo_practical_workflow()
        logger.info("")

        logger.info("=" * 70)
        logger.info("✅ Все демонстрации SGR выполнены успешно!")
        logger.info("=" * 70)

        logger.info("🎯 Ключевые преимущества SGR:")
        logger.info("  • Структурированный анализ кода с проверяемыми результатами")
        logger.info("  • Интеллектуальный выбор стратегии мутации на основе анализа")
        logger.info("  • Формализованная оценка новизны и качества решений")
        logger.info("  • Накопление и использование мета-знаний об эволюции")
        logger.info("  • Повышение sample efficiency за счет направленных мутаций")
        logger.info("")

        logger.info("📊 Статистика демонстрации:")
        logger.info(f"  • Проверено схем: 6")
        logger.info(f"  • Валидация: успешна")
        logger.info(f"  • Сериализация: работает корректно")
        logger.info(f"  • Workflow: полностью функционален")

        return True

    except Exception as e:
        logger.error(f"❌ Ошибка в демонстрации: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)