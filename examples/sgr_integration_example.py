#!/usr/bin/env python3
"""
Example of SGR integration in ShinkaEvolve.

This example shows how to use the new SGR-enhanced PromptSampler
in place of the original PromptSampler for intelligent mutation strategy selection.
"""

import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

# SGR imports
from shinka.core.sgr_prompt_sampler import SGRPromptSampler
from shinka.database import Program

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class SGREvolutionConfig:
    """Enhanced evolution config with SGR parameters."""

    # Original parameters
    task_sys_msg: Optional[str] = None
    patch_types: List[str] = field(default_factory=lambda: ["diff", "full"])
    patch_type_probs: List[float] = field(default_factory=lambda: [0.7, 0.3])
    language: str = "python"
    use_text_feedback: bool = False

    # SGR-specific parameters
    sgr_enabled: bool = True
    sgr_confidence_threshold: float = 0.7
    sgr_fallback_to_random: bool = True


def create_sample_program(code: str, score: float = 0.5, correct: bool = True) -> Program:
    """Create a sample Program object for testing."""
    return Program(
        id=f"prog-{hash(code) % 10000}",
        code=code,
        language="python",
        parent_id=None,
        generation=0,
        archive_inspiration_ids=[],
        top_k_inspiration_ids=[],
        code_diff=None,
        embedding=[],
        correct=correct,
        combined_score=score,
        public_metrics={"accuracy": score, "performance": score * 0.9},
        private_metrics={"memory_usage": 1000 + int(score * 500)},
        text_feedback=f"Program performance: {'good' if score > 0.7 else 'needs improvement'}",
        metadata={}
    )


def demo_original_vs_sgr_sampler():
    """Compare original PromptSampler with SGR-enhanced version."""
    logger.info("🔄 Сравнение оригинального PromptSampler с SGR версией...")

    # Test programs
    parent_code = '''
def bubble_sort(arr):
    """Inefficient bubble sort implementation."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def main():
    data = [64, 34, 25, 12, 22, 11, 90]
    result = bubble_sort(data)
    print(f"Sorted: {result}")
'''

    inspiration_code = '''
def quick_sort(arr):
    """Efficient quicksort implementation."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
'''

    parent = create_sample_program(parent_code, score=0.3)
    inspiration = create_sample_program(inspiration_code, score=0.8)

    # Test original sampler (through SGR with disabled SGR)
    logger.info("📊 Тестирование baseline (SGR отключен)...")
    baseline_sampler = SGRPromptSampler(
        sgr_enabled=False,  # Use original logic
        language="python",
        patch_types=["diff", "full", "cross"],
        patch_type_probs=[0.5, 0.3, 0.2],
        use_text_feedback=True
    )

    baseline_sys, baseline_user, baseline_strategy = baseline_sampler.sample(
        parent, [inspiration], []
    )

    logger.info(f"  • Выбранная стратегия: {baseline_strategy}")
    logger.info(f"  • Длина системного сообщения: {len(baseline_sys)}")
    logger.info(f"  • Упоминание кода родителя: {'✓' if 'bubble_sort' in baseline_user else '✗'}")

    # Test SGR sampler (will fall back since no real LLM)
    logger.info("🧠 Тестирование SGR (с fallback)...")
    sgr_sampler = SGRPromptSampler(
        sgr_enabled=True,
        sgr_confidence_threshold=0.6,
        sgr_fallback_to_random=True,
        language="python",
        patch_types=["diff", "full", "cross"],
        patch_type_probs=[0.5, 0.3, 0.2],
        use_text_feedback=True
    )

    sgr_sys, sgr_user, sgr_strategy = sgr_sampler.sample(
        parent, [inspiration], []
    )

    logger.info(f"  • Выбранная стратегия: {sgr_strategy}")
    logger.info(f"  • Длина системного сообщения: {len(sgr_sys)}")
    logger.info(f"  • Упоминание кода родителя: {'✓' if 'bubble_sort' in sgr_user else '✗'}")

    # Check SGR statistics
    stats = sgr_sampler.get_sgr_statistics()
    logger.info(f"  • SGR статистика: {stats}")

    return baseline_strategy, sgr_strategy, stats


def demo_sgr_with_different_scenarios():
    """Test SGR behavior with different code scenarios."""
    logger.info("🎯 Тестирование SGR с различными сценариями...")

    scenarios = [
        {
            "name": "Простая оптимизация",
            "code": '''
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
''',
            "score": 0.6,
            "description": "Линейный поиск - можно оптимизировать"
        },
        {
            "name": "Сложный алгоритм",
            "code": '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
''',
            "score": 0.2,
            "description": "Экспоненциальная сложность - нужна полная переписка"
        },
        {
            "name": "Хороший код",
            "code": '''
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
''',
            "score": 0.9,
            "description": "Эффективный алгоритм - минимальные изменения"
        }
    ]

    sgr_sampler = SGRPromptSampler(
        sgr_enabled=True,
        sgr_fallback_to_random=True,
        language="python"
    )

    for scenario in scenarios:
        logger.info(f"\n  📝 Сценарий: {scenario['name']}")
        logger.info(f"     {scenario['description']}")

        program = create_sample_program(scenario['code'], scenario['score'])

        # Sample multiple times to see consistency
        strategies = []
        for i in range(3):
            _, _, strategy = sgr_sampler.sample(program, [], [])
            strategies.append(strategy)

        logger.info(f"     Выбранные стратегии: {', '.join(strategies)}")

        # Reset stats for clean measurement
        sgr_sampler.reset_sgr_statistics()

    final_stats = sgr_sampler.get_sgr_statistics()
    logger.info(f"\n  📊 Итоговая статистика: {final_stats}")


def demo_sgr_configuration_options():
    """Demonstrate different SGR configuration options."""
    logger.info("⚙️  Демонстрация опций конфигурации SGR...")

    test_program = create_sample_program('''
def inefficient_sort(arr):
    # Very inefficient implementation
    for i in range(len(arr)):
        for j in range(len(arr)):
            for k in range(len(arr)):
                if j < k and arr[j] > arr[k]:
                    arr[j], arr[k] = arr[k], arr[j]
    return arr
''', score=0.1)

    configs = [
        {
            "name": "Консервативный SGR",
            "config": {
                "sgr_enabled": True,
                "sgr_confidence_threshold": 0.9,  # Высокий порог
                "sgr_fallback_to_random": True
            }
        },
        {
            "name": "Агрессивный SGR",
            "config": {
                "sgr_enabled": True,
                "sgr_confidence_threshold": 0.3,  # Низкий порог
                "sgr_fallback_to_random": True
            }
        },
        {
            "name": "SGR без fallback",
            "config": {
                "sgr_enabled": True,
                "sgr_confidence_threshold": 0.7,
                "sgr_fallback_to_random": False  # Строгий режим
            }
        }
    ]

    for config_test in configs:
        logger.info(f"\n  🔧 Конфигурация: {config_test['name']}")

        sampler = SGRPromptSampler(**config_test['config'], language="python")

        # Test multiple samples
        for i in range(2):
            _, _, strategy = sampler.sample(test_program, [], [])

        stats = sampler.get_sgr_statistics()
        success_rate = stats.get('sgr_success_rate', 0.0)
        fallback_rate = stats.get('fallback_rate', 0.0)

        logger.info(f"     SGR успех: {success_rate:.1%}")
        logger.info(f"     Fallback: {fallback_rate:.1%}")


def main():
    """Run SGR integration example."""
    logger.info("=" * 70)
    logger.info("🚀 Пример интеграции SGR в ShinkaEvolve")
    logger.info("=" * 70)

    try:
        # Demo 1: Compare original vs SGR
        baseline_strategy, sgr_strategy, sgr_stats = demo_original_vs_sgr_sampler()
        logger.info("")

        # Demo 2: Different scenarios
        demo_sgr_with_different_scenarios()
        logger.info("")

        # Demo 3: Configuration options
        demo_sgr_configuration_options()
        logger.info("")

        logger.info("=" * 70)
        logger.info("✅ Демонстрация SGR интеграции завершена успешно!")
        logger.info("=" * 70)

        logger.info("🎯 Основные возможности SGR интеграции:")
        logger.info("  • Простая замена PromptSampler на SGRPromptSampler")
        logger.info("  • Автоматический fallback при недоступности LLM")
        logger.info("  • Гибкая настройка confidence threshold")
        logger.info("  • Детальная статистика использования SGR")
        logger.info("  • Обратная совместимость с существующим кодом")
        logger.info("")

        logger.info("📈 Ожидаемые улучшения:")
        logger.info("  • Более разумный выбор стратегий мутации")
        logger.info("  • Снижение количества неудачных мутаций")
        logger.info("  • Ускорение конвергенции к оптимальным решениям")
        logger.info("  • Лучшее использование контекста и истории эволюции")

        return True

    except Exception as e:
        logger.error(f"❌ Ошибка в демонстрации: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)