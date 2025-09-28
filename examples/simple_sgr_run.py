#!/usr/bin/env python3
"""
Простой запуск ShinkaEvolve с SGR без внешних API.

Демонстрирует работу SGR в mock режиме для понимания workflow.
"""

import logging
import tempfile
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

from shinka.core.sgr_prompt_sampler import SGRPromptSampler
from shinka.database import Program, ProgramDatabase, DatabaseConfig
from shinka.launch import LocalJobConfig

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def create_simple_evaluation_script():
    """Создает простой evaluation script."""
    eval_code = '''#!/usr/bin/env python3
"""Simple evaluation script for testing."""

import sys
import json
import importlib.util

def run_shinka_eval():
    """Run evaluation and return results."""
    # Import the program to evaluate
    spec = importlib.util.spec_from_file_location("program", "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Test the program
    try:
        if hasattr(module, 'test_function'):
            result = module.test_function()
            score = 1.0 if result else 0.0
        elif hasattr(module, 'fibonacci'):
            # Test fibonacci function
            result = module.fibonacci(5)
            expected = 5  # F(5) = 5
            score = 1.0 if result == expected else 0.5
        elif hasattr(module, 'factorial'):
            # Test factorial function
            result = module.factorial(5)
            expected = 120  # 5! = 120
            score = 1.0 if result == expected else 0.5
        else:
            score = 0.5  # Program exists but no known function

        return {
            "correct": {"correct": score >= 0.8},
            "metrics": {
                "combined_score": score,
                "public": {"accuracy": score, "performance": score * 0.9},
                "private": {"test_cases_passed": int(score * 10)},
                "text_feedback": f"Program evaluation completed. Score: {score}"
            }
        }
    except Exception as e:
        return {
            "correct": {"correct": False},
            "metrics": {
                "combined_score": 0.0,
                "public": {"accuracy": 0.0, "performance": 0.0},
                "private": {"error": str(e)},
                "text_feedback": f"Program failed with error: {e}"
            }
        }

if __name__ == "__main__":
    result = run_shinka_eval()
    print(json.dumps(result, indent=2))
'''
    return eval_code


def create_initial_program():
    """Создает начальную программу для эволюции."""
    initial_code = '''# EVOLVE-BLOCK-START
def fibonacci(n):
    """Inefficient recursive Fibonacci implementation."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
# EVOLVE-BLOCK-END

def test_function():
    """Test the fibonacci function."""
    return fibonacci(5) == 5

if __name__ == "__main__":
    print(f"Fibonacci(5) = {fibonacci(5)}")
    print(f"Test passed: {test_function()}")
'''
    return initial_code


def simulate_evolution_step(
    sampler: SGRPromptSampler,
    parent_program: Program,
    generation: int
):
    """Симулирует один шаг эволюции."""
    logger.info(f"🔄 Генерация {generation}: эволюция программы...")

    # Используем SGR sampler для выбора стратегии
    sys_msg, user_msg, strategy = sampler.sample(
        parent_program,
        archive_inspirations=[],
        top_k_inspirations=[]
    )

    logger.info(f"   • SGR выбрал стратегию: {strategy}")
    logger.info(f"   • Длина системного сообщения: {len(sys_msg)}")
    logger.info(f"   • Родительский score: {parent_program.combined_score:.2f}")

    # Симулируем улучшение (в реальности здесь был бы LLM call)
    if strategy == "full":
        # Полная переписка - большое улучшение
        new_score = min(1.0, parent_program.combined_score + 0.3)
        improved_code = '''# EVOLVE-BLOCK-START
def fibonacci(n):
    """Efficient iterative Fibonacci implementation."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
# EVOLVE-BLOCK-END

def test_function():
    """Test the fibonacci function."""
    return fibonacci(5) == 5

if __name__ == "__main__":
    print(f"Fibonacci(5) = {fibonacci(5)}")
    print(f"Test passed: {test_function()}")
'''
    elif strategy == "diff":
        # Частичное улучшение - меньшее улучшение
        new_score = min(1.0, parent_program.combined_score + 0.1)
        improved_code = '''# EVOLVE-BLOCK-START
def fibonacci(n):
    """Slightly optimized recursive Fibonacci with base case."""
    if n <= 1:
        return n
    if n == 2:
        return 1  # Early termination for small cases
    return fibonacci(n-1) + fibonacci(n-2)
# EVOLVE-BLOCK-END

def test_function():
    """Test the fibonacci function."""
    return fibonacci(5) == 5

if __name__ == "__main__":
    print(f"Fibonacci(5) = {fibonacci(5)}")
    print(f"Test passed: {test_function()}")
'''
    else:
        # Cross или другие стратегии
        new_score = min(1.0, parent_program.combined_score + 0.05)
        improved_code = parent_program.code  # Минимальные изменения

    # Создаем новую программу
    new_program = Program(
        id=f"prog-gen-{generation}",
        code=improved_code,
        language="python",
        parent_id=parent_program.id,
        generation=generation,
        archive_inspiration_ids=[],
        top_k_inspiration_ids=[],
        code_diff=None,
        embedding=[],
        correct=new_score >= 0.8,
        combined_score=new_score,
        public_metrics={"accuracy": new_score, "performance": new_score * 0.9},
        private_metrics={"generation": generation},
        text_feedback=f"Generation {generation} improvement using {strategy} strategy",
        metadata={
            "strategy_used": strategy,
            "score_improvement": new_score - parent_program.combined_score,
            "parent_score": parent_program.combined_score
        }
    )

    logger.info(f"   • Новый score: {new_score:.2f} (улучшение: +{new_score - parent_program.combined_score:.2f})")
    logger.info(f"   • Корректность: {'✓' if new_program.correct else '✗'}")

    return new_program


def run_simple_evolution():
    """Запускает простую эволюцию с SGR."""
    logger.info("=" * 60)
    logger.info("🚀 Простой запуск ShinkaEvolve с SGR")
    logger.info("=" * 60)

    # Создаем временную директорию
    temp_dir = Path(tempfile.mkdtemp(prefix="shinka_sgr_"))
    logger.info(f"📁 Рабочая директория: {temp_dir}")

    try:
        # 1. Создаем файлы для эволюции
        eval_script = temp_dir / "evaluate.py"
        eval_script.write_text(create_simple_evaluation_script())
        eval_script.chmod(0o755)

        initial_py = temp_dir / "initial.py"
        initial_py.write_text(create_initial_program())

        logger.info("✓ Созданы evaluation script и initial program")

        # 2. Настраиваем SGR PromptSampler с правильным LLM клиентом
        from shinka.llm import LLMClient

        # Создаем LLM клиент с правильной Azure моделью
        sgr_llm_client = LLMClient(
            model_names=["gpt-5-mini"],  # Используем Azure модель
            verbose=True,
        )

        sgr_sampler = SGRPromptSampler(
            sgr_enabled=True,
            sgr_confidence_threshold=0.6,  # Низкий порог для демонстрации
            sgr_fallback_to_random=True,
            sgr_llm_client=sgr_llm_client,  # Передаем настроенный клиент
            language="python",
            patch_types=["diff", "full", "cross"],
            patch_type_probs=[0.5, 0.3, 0.2],
            use_text_feedback=True
        )

        logger.info("✓ SGR PromptSampler настроен")

        # 3. Создаем начальную программу
        initial_program = Program(
            id="initial-program",
            code=create_initial_program(),
            language="python",
            parent_id=None,
            generation=0,
            archive_inspiration_ids=[],
            top_k_inspiration_ids=[],
            code_diff=None,
            embedding=[],
            correct=False,  # Неэффективная реализация
            combined_score=0.3,  # Низкий начальный score
            public_metrics={"accuracy": 0.3, "performance": 0.2},
            private_metrics={"initial": True},
            text_feedback="Initial inefficient recursive implementation",
            metadata={"generation": 0}
        )

        logger.info(f"📊 Начальная программа: score={initial_program.combined_score:.2f}")

        # 4. Запускаем несколько поколений эволюции
        current_program = initial_program
        generations = 5

        for gen in range(1, generations + 1):
            new_program = simulate_evolution_step(sgr_sampler, current_program, gen)
            current_program = new_program

            # Показываем статистику SGR
            if gen % 2 == 0:
                stats = sgr_sampler.get_sgr_statistics()
                logger.info(f"   📈 SGR статистика: успех={stats.get('sgr_success_rate', 0):.1%}, "
                          f"fallback={stats.get('fallback_rate', 0):.1%}")

        # 5. Финальные результаты
        logger.info("")
        logger.info("=" * 60)
        logger.info("📊 Результаты эволюции:")
        logger.info("=" * 60)
        logger.info(f"🎯 Начальный score: {initial_program.combined_score:.2f}")
        logger.info(f"🎯 Финальный score: {current_program.combined_score:.2f}")
        logger.info(f"📈 Общее улучшение: +{current_program.combined_score - initial_program.combined_score:.2f}")
        logger.info(f"✅ Корректность: {'Да' if current_program.correct else 'Нет'}")

        # SGR статистика
        final_stats = sgr_sampler.get_sgr_statistics()
        logger.info("")
        logger.info("🧠 SGR Статистика:")
        for key, value in final_stats.items():
            if isinstance(value, float):
                logger.info(f"   • {key}: {value:.1%}" if 'rate' in key else f"   • {key}: {value:.2f}")
            else:
                logger.info(f"   • {key}: {value}")

        # Показываем финальный код
        logger.info("")
        logger.info("💻 Финальный код:")
        logger.info("-" * 40)
        print(current_program.code)
        logger.info("-" * 40)

        return True

    except Exception as e:
        logger.error(f"❌ Ошибка в эволюции: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Очищаем временную директорию
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.info(f"🧹 Очищена временная директория")


if __name__ == "__main__":
    success = run_simple_evolution()
    if success:
        logger.info("🎉 Простой запуск SGR эволюции завершен успешно!")
    else:
        logger.error("💥 Простой запуск SGR эволюции завершился с ошибкой!")

    exit(0 if success else 1)