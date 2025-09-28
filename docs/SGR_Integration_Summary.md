# Schema-Guided Reasoning (SGR) Integration в ShinkaEvolve

## Обзор

Успешно реализована интеграция Schema-Guided Reasoning (SGR) в ShinkaEvolve для повышения эффективности эволюции кода через структурированное принятие решений LLM.

## 🎯 Основные цели SGR интеграции

1. **Структурированный анализ кода** - формализованная оценка сложности, узких мест и возможностей оптимизации
2. **Интеллектуальный выбор стратегии мутации** - выбор оптимальной стратегии на основе анализа контекста
3. **Проверяемые и воспроизводимые решения** - все решения LLM имеют структурированный формат с обоснованиями
4. **Повышение sample efficiency** - снижение количества неудачных мутаций за счет более разумного планирования

## 📁 Реализованные компоненты

### 1. SGR Схемы (`shinka/core/sgr_schemas.py`)

- **`CodeAnalysis`** - анализ сложности кода, алгоритмов, узких мест
- **`MutationStrategy`** - выбор стратегии с уверенностью и обоснованием
- **`CodeMutationPlan`** - полный план мутации с критериями успеха
- **`EvaluationFeedback`** - структурированная обратная связь по результатам
- **`NoveltyAssessment`** - оценка новизны для rejection sampling
- **`MetaRecommendation`** - мета-рекомендации для направления эволюции

### 2. SGR Mutation Planner (`shinka/core/sgr_mutation_planner.py`)

- **`SGRMutationPlanner`** - основной класс для планирования мутаций
- Двухэтапный процесс: анализ кода → выбор стратегии
- Автоматический fallback при недоступности LLM
- Поддержка structured output через Pydantic

### 3. SGR-Enhanced PromptSampler (`shinka/core/sgr_prompt_sampler.py`)

- **`SGRPromptSampler`** - расширенная версия оригинального PromptSampler
- Полная обратная совместимость
- Интеграция SGR логики с сохранением fallback механизмов
- Детальная статистика использования SGR

## 🧪 Тестирование

### Unit Tests (`tests/test_sgr_integration.py`)
- ✅ Тестирование всех SGR схем
- ✅ Валидация Pydantic моделей
- ✅ Мокирование LLM взаимодействий
- ✅ Тестирование fallback механизмов

### Standalone Demo (`tests/test_sgr_standalone.py`)
- ✅ Демонстрация всех схем без LLM зависимостей
- ✅ JSON сериализация/десериализация
- ✅ Валидация данных
- ✅ Практический workflow

### Integration Example (`examples/sgr_integration_example.py`)
- ✅ Сравнение original vs SGR sampler
- ✅ Различные сценарии использования
- ✅ Конфигурационные опции

## 📊 Результаты тестирования

```bash
# Unit тесты
$ python -m pytest tests/test_sgr_integration.py -v
============================= test session starts ==============================
collected 12 items
tests/test_sgr_integration.py::TestSGRSchemas::test_code_analysis_schema PASSED [  8%]
tests/test_sgr_integration.py::TestSGRSchemas::test_mutation_strategy_schema PASSED [ 16%]
# ... все 12 тестов прошли успешно

# Standalone демонстрация
$ python tests/test_sgr_standalone.py
INFO: ✅ Все демонстрации SGR выполнены успешно!
INFO: 📊 Статистика демонстрации:
INFO:   • Проверено схем: 6
INFO:   • Валидация: успешна
INFO:   • Сериализация: работает корректно
INFO:   • Workflow: полностью функционален
```

## 🔧 Использование

### Простая интеграция

```python
from shinka.core.sgr_prompt_sampler import SGRPromptSampler

# Замените оригинальный PromptSampler на SGR версию
prompt_sampler = SGRPromptSampler(
    sgr_enabled=True,
    sgr_confidence_threshold=0.7,
    sgr_fallback_to_random=True,
    language="python",
    use_text_feedback=True
)

# Использование полностью идентично оригинальному
sys_msg, user_msg, patch_type = prompt_sampler.sample(
    parent_program, archive_inspirations, top_k_inspirations
)
```

### Конфигурационные опции

- **`sgr_enabled`** - включить/выключить SGR (default: True)
- **`sgr_confidence_threshold`** - минимальная уверенность для принятия SGR решения (default: 0.7)
- **`sgr_fallback_to_random`** - использовать fallback при неудаче SGR (default: True)
- **`sgr_llm_client`** - настроенный LLM клиент для SGR (optional)

### Мониторинг SGR

```python
# Получение статистики использования
stats = prompt_sampler.get_sgr_statistics()
print(f"SGR success rate: {stats['sgr_success_rate']:.1%}")
print(f"Fallback rate: {stats['fallback_rate']:.1%}")

# Сброс статистики
prompt_sampler.reset_sgr_statistics()
```

## 🎨 Архитектурные преимущества

### 1. Обратная совместимость
- SGRPromptSampler наследует от оригинального PromptSampler
- Все существующие конфиги и API остаются неизменными
- Постепенная миграция без breaking changes

### 2. Надежность
- Автоматический fallback при недоступности LLM
- Валидация всех structured outputs
- Graceful degradation при ошибках

### 3. Мониторинг
- Детальная статистика использования SGR
- Отслеживание confidence levels
- Метрики fallback usage

### 4. Расширяемость
- Легко добавлять новые SGR схемы
- Модульная архитектура для новых типов анализа
- Поддержка различных LLM провайдеров

## 🚀 Ожидаемые улучшения

### Sample Efficiency
- **Более разумный выбор стратегий** на основе анализа кода
- **Снижение неудачных мутаций** за счет структурированного планирования
- **Ускорение конвергенции** к оптимальным решениям

### Воспроизводимость
- **Проверяемые решения** с explicit reasoning
- **Структурированные logs** для анализа эволюционного процесса
- **Лучшая отладка** благодаря формализованным решениям

### Масштабируемость
- **Параллельная обработка** SGR анализа
- **Кэширование** результатов анализа для повторных запусков
- **Адаптивные пороги** confidence на основе производительности

## 📈 Следующие шаги

### 1. Продвинутые возможности
- **Meta-learning** для улучшения SGR решений на основе истории
- **Multi-objective optimization** с учетом нескольких критериев
- **Adaptive confidence thresholds** на основе performance feedback

### 2. Дополнительные интеграции
- **NoveltyJudge SGR enhancement** для структурированной оценки новизны
- **MetaSummarizer SGR integration** для лучших мета-рекомендаций
- **Evaluation feedback SGR** для структурированной обратной связи

### 3. Оптимизации
- **Кэширование SGR анализа** для повторных программ
- **Batch processing** для multiple candidates
- **Model selection** для SGR на основе task complexity

## 💡 Заключение

SGR интеграция в ShinkaEvolve представляет значительный шаг вперед в направлении более интеллектуальной и эффективной эволюции кода. Структурированный подход к принятию решений LLM обеспечивает:

- **Повышенную надежность** эволюционного процесса
- **Лучшую интерпретируемость** принимаемых решений
- **Улучшенную sample efficiency** за счет более разумных мутаций
- **Простую интеграцию** с существующим кодом

Реализация готова к production использованию и демонстрирует успешное применение принципов Schema-Guided Reasoning в контексте автоматической эволюции кода.