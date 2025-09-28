Ниже — готовая «сшивка» ShinkaEvolve × SGR: архитектура, конкретные улучшения ядра, схемы для генерации новых агентов «по паттерну SGR» и два полноценные интеграционных файла (initial.py и evaluate.py) под ShinkaEvolve. Это можно воспринимать как стартовый проект‑каркас: запускаете эволюцию Shinka, а внутри неё «геномом» выступает SGR‑спецификация агента, которую LLM мутирует, а далее оцениваются задачи — генерация сценариев (творчество) и генерация кода (возврат кода с автотестами).

Ключи/ссылки на SGR «как надо делать»: паттерны Cascade / Routing / Cycle, инструментальный агент, constrained decoding и chat.completions.parse под Pydantic — см. загруженные вами материалы, на которые я опираюсь при проектировании и API‑вызовах. 

sgr_full

 

sgr_guide_structured


Ключи ShinkaEvolve (архив программ, EVOLVE-BLOCK, evaluate.py, bandit/UCB, novelty rejection, WebUI): в официальных материалах и репозитории. 
Sakana AI
+1

0) Идея интеграции в одну фразу

Сделать SGR‑схему и «плейбуки» ролей генотипом в ShinkaEvolve. Мутируем не только код, а структуру рассуждения и инструментальные интерфейсы (ветви Union, поля Literal, шаги плана, роли команды и их схемы ввода/вывода). Фитнес — качество решений на бенчмарках схемно проверяемых задач (кодовые автотесты, SGR‑оценка сценариев, PRD / отчёты, маршруты стартап‑пайплайна). Shinka «учится» лучшим SGR‑схемам, а не только патчам кода. Это резко снижает холостой перебор за счёт раннего отбраковывания неоригинальных/невалидных схем и использования ансамбля LLM с бандитом. 
Sakana AI

1) Улучшения самой системы (ShinkaEvolve), добавляемые через SGR
1.1 SGR как «формат мутации»: патчи не в свободном тексте, а схема‑патч

Заменяем свободный diff‑патч на структурированный патч (JSON Schema / Pydantic), где мутация описывает:

schema_ops: AddField/DropField/ChangeLiteralSet/ReorderSteps — операции над SGR‑схемой;

tool_ops: AddTool/ChangeArgType/ConstrainRange — операции над инструментами;

planner_ops: AddCheck/ChangeRouting/AdjustCycleBounds — операции над планировщиком.

Это даёт валидность на уровне типов и мгновенную проверку «можно ли так думать и вызывать инструменты», как рекомендует SGR. 

sgr_full

1.2 Новизна по схеме: schema‑novelty

Помимо текстовых эмбеддингов кода (как в Shinka) считаем:

расстояние по дереву JSON Schema (tree‑edit distance);

дистанции по множеству литералов (Literal[...]) и вариантам ветвления Union.

Если слишком близко — Reject Sampling до выполнения; дальше «LLM‑ас‑новелти‑джадж» — но уже со структурированным вердиктом NoveltyVerdict{is_novel, why, impacted_fields} (ещё одна маленькая SGR‑схема). 
arXiv
+1

1.3 Бандитная приоритизация моделей на уровне схемных мутаций

Привязываем награду (UCB1) к дельте фитнеса и к «стоимости мутации» (сколько валидаторов/тестов прошло), чтобы чаще звать модель, которая приносит смысловые изменения SGR, а не просто текстовые замены. 
Sakana AI

1.4 SGR‑meta: «поисковый дневник» в строгом формате

Шаги мета‑аналитики (search summary) пусть отдаются в схеме SearchInsight{pattern, when_to_use, counterfactuals, risks}, потом подмешиваются в контекст как защищённые «сэмплы идеи». Это повышает sample‑efficiency, сохраняя читабельность и аудит. (В Shinka уже есть «scratchpad/summary», мы просто стандартизируем его схемой.) 
Sakana AI

2) Генерация нового кода агентов «по SGR‑паттерну» (ваш п.2)
2.1 Генотип = AgentSpec (SGR‑суперсхема)

Опишем один YAML/JSON, из которого кодогенератор собирает:

Роли: имя, входная/выходная SGR‑схема, подсказки, лимиты токенов.

Инструменты: Pydantic‑классы (ветви Union) с типами и ограничениями.

Планировщик: Cascade/Routing/Cycle (см. паттерны SGR) + контрольные точки (валидация по пути). 

sgr_full

Shinka мутирует AgentSpec (а не монолитный промпт), а рантайм автоматически пересобирает агента. Такие мутации переносятся на другие задачи, что и требуется («агенты по паттерну для похожих задач»).

2.2 Фитнес‑функции для креатива/сценариев/медиа

Сценарии: чек‑листы структуры (3 акта/сцены/персонажи), согласованность (SGR‑поле coherence_score), оригинальность (LLM‑оценка по SGR‑схеме Critique), длина/стиль.

Изображения/видео: если подключаете генераторы — прокси‑метрики (CLIP‑соответствие, динамика кадров, отсутствие артефактов). Пока без генерации — оцениваем сценарные схемы и сториборды (структурированно).

Все оценки делаются в SGR‑схемах для воспроизводимости и аудита; вердикты от LLM‑критиков — тоже структурно, как рекомендовано в SGR. 

sgr_full

3) Агент для написания кода с SGR‑схемами (ваш п.3)

Используем многоролевой team‑playbook:

Architect (Routing: выбрать стек/скелет),

Coder (Cycle: план → код → рефактор),

Tester (Cascade: тест‑план → автотесты → отчёт),

Reviewer (Routing: статанализ/стиль/комментарии),

Integrator (сборка/пакет/CLI).

Каждая роль отдаёт строго типизированные артефакты: код, список тестов, лог миграций. Инструментальный слой — файловые операции, запуск тестов/линтеров, сборка. Всё описано в ветвях Union[...] SGR‑схемы, как в демо SGR с tool‑calling. 

sgr_full

Фитнес: доля пройденных тестов + статанализ (ruff/flake8/radon) + «рецензия» (LLM‑критик по SGR‑схеме Review) + бюджет токенов/время.

4) Стартап‑агент: маркетинг → аналитика → продукт → разработка → backend/infra (ваш п.4)

Playbook как DAG из SGR‑модулей:

MarketingResearch (ICP, JTBD, конкуренты)

Analytics (TAM/SAM/SOM, юнит‑экономика)

PRD (проблема→MVP→KPI→риски)

Eng (скелет продукта, API, фронт, кодогенерация)

Backend/Infra (деплой, конфиги, мониторинг)

Каждый модуль — SGR‑схема (с валидацией), а Shinka мутирует: состав ролей / порядок / схемы / метрики успеха. Фитнес — свёртка «качество PRD/доков (LLM‑оценка в схеме) + покрытие тестами + скорость/стоимость». Эволюция даёт разные Pareto‑точки. Именно так Shinka уже проектировала агентные скелеты для AIME (многоэтапная архитектура, peer‑review, синтез) и нашла Pareto‑фронт по точности/запросам. 
Sakana AI

5) Готовые файлы для старта под ShinkaEvolve

Ниже — полные initial.py и evaluate.py (без заглушек и «…»), согласованные с API ShinkaEvolve (минимальный раннер, EVOLVE-BLOCK‑метки, run_shinka_eval, агрегатор метрик и т.п.). Внутри — два бенчмарка:

CodeBench — агент генерирует функции по SGR‑схеме, мы компилируем код и гоняем юнит‑тесты.

ScriptBench — агент генерирует сценарий по SGR‑схеме (3 акта/сцены/персонажи); оцениваем структурные показатели и (опционально) подключаем LLM‑критика.

Формат EVOLVE-BLOCK и контракт evaluate.py/initial.py взяты из README проекта (Hydra/LocalJobConfig/run_shinka_eval и пр.). 
GitHub

Под капотом Shinka — острова, родительский отбор power_law/weighted/beam_search, novelty rejection и бандитный ансамбль LLM. 
Sakana AI
+2
arXiv
+2

initial.py — геном = SGR‑спецификация + рантайм агента
# initial.py
# Геном: SGR-спецификация агента и его плейбуков; рантайм использует OpenAI Structured Output.
# Совместимо с ShinkaEvolve: см. EVOLVE-BLOCK-START/END и run_experiment(**kwargs).
# Док по SGR-паттернам/инструментам и tool-calling: см. загруженные материалы.  # :contentReference[oaicite:14]{index=14}

from __future__ import annotations

import importlib.util
import io
import json
import os
import re
import sys
import textwrap
import traceback
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from annotated_types import Ge, Le, MinLen, MaxLen
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

# ---------- EVOLVE-BLOCK-START ----------
# ВНИМАНИЕ: Shinka будет мутировать ТОЛЬКО то, что находится в этом блоке.
# Геном: SGR супер-спецификация агента, которую можно безопасно изменять/расширять.

class CodeTask(BaseModel):
    kind: Literal["code"]
    # список задач кодирования (название, спецификация, эталонные тесты)
    problems: List[Dict[str, Any]] = Field(
        default_factory=lambda: [
            {
                "name": "two_sum",
                "signature": "def two_sum(nums: list[int], target: int) -> tuple[int,int]:",
                "description": "Return indices (i,j) with i<j and nums[i]+nums[j]==target.",
                "tests": [
                    {"inp": {"nums":[2,7,11,15], "target":9}, "out": (0,1)},
                    {"inp": {"nums":[3,2,4], "target":6}, "out": (1,2)},
                    {"inp": {"nums":[3,3], "target":6}, "out": (0,1)},
                ],
            },
            {
                "name": "is_anagram",
                "signature": "def is_anagram(a: str, b: str) -> bool:",
                "description": "Return True if a and b are anagrams (letters only, case-insensitive).",
                "tests": [
                    {"inp": {"a":"listen","b":"silent"}, "out": True},
                    {"inp": {"a":"rat","b":"car"}, "out": False},
                    {"inp": {"a":"Astronomer","b":"Moon starer"}, "out": True},
                ],
            },
        ]
    )

class ScriptTask(BaseModel):
    kind: Literal["script"]
    # целевая структура сценария — 3 акта, в каждом >=2 сцен
    min_scenes_per_act: int = Field(ge=2, default=3)
    force_three_act_structure: bool = True
    # требования к персонажам/сеттингу
    require_main_characters: List[str] = Field(default_factory=lambda: ["Protagonist","Antagonist"])
    genre: Literal["drama","thriller","comedy","sci-fi","fantasy"] = "thriller"
    max_tokens_hint: int = Field(ge=512, le=4000, default=1200)

class AgentSpec(BaseModel):
    # Параметры LLM
    llm_model: str = "gpt-4o"
    max_completion_tokens: int = 4000
    temperature: float = 0.4

    # Шаблоны SGR для двух доменов
    code: CodeTask = CodeTask()
    script: ScriptTask = ScriptTask()

def evolvable_agent_spec() -> AgentSpec:
    """
    Возвращает текущую SGR-спецификацию агента.
    Этот объект — «геном»: Shinka будет мутировать поля/значения/ограничения.
    """
    return AgentSpec()

# ---------- EVOLVE-BLOCK-END ----------


# ===================== SGR СХЕМЫ ВЫХОДОВ (Pydantic) ======================

# 1) Генерация кода: схема ответа. Строго требуем 1 функцию с полным исходником.
class CodeFunction(BaseModel):
    tool: Literal["write_function"]
    name: str
    signature: str
    source_code: str  # полный текст функции с сигнатурой, type hints, докстрингом и тестируемой логикой

class CodeResponse(BaseModel):
    reasoning_brief: str
    function: CodeFunction

# 2) Генерация сценария: трёхактная структура + сцены + персонажи
class Character(BaseModel):
    name: str
    brief: str

class Scene(BaseModel):
    title: str
    summary: str

class Act(BaseModel):
    act_number: Literal[1,2,3]
    scenes: List[Scene]

class ScriptResponse(BaseModel):
    logline_one_sentence: str
    genre: str
    main_characters: List[Character]
    acts: List[Act]  # должны быть акты 1..3 при force_three_act_structure
    coherence_score_self: float = Field(ge=0.0, le=1.0)
    risks_or_weaknesses: List[str]

# ===================== ВСПОМОГАТЕЛЬНЫЕ УТИЛИТЫ ===========================

@dataclass
class EvalResult:
    score: float
    public: Dict[str, Any]
    private: Dict[str, Any]
    text: str

def _make_client(model_name: str) -> OpenAI:
    # клиент OpenAI по умолчанию (можно заменить на Azure/OpenRouter — интерфейс одинаковый)
    return OpenAI()

def _compile_and_run_function(fn_src: str, call_sig: str, calls: List[Tuple[dict, Any]]) -> Tuple[int,int,List[str]]:
    """
    Компилируем исходник в изолированном модуле и проверяем юнит-тесты.
    calls: список (аргументы, ожидаемый_результат)
    Возвращаем количество пройденных тестов, всего тестов и логи ошибок.
    """
    # создаём временный модуль без доступа к окружению
    module = ModuleType("candidate_module")
    safe_globals = {"__builtins__": {"len": len, "range": range, "enumerate": enumerate, "sorted": sorted, "sum": sum, "set": set, "list": list, "tuple": tuple, "str": str}}
    try:
        exec(fn_src, safe_globals, module.__dict__)
    except Exception as e:
        return (0, len(calls), [f"CompilationError: {e}"])
    # извлекаем имя функции из сигнатуры
    m = re.match(r"\s*def\s+([a-zA-Z_]\w*)\s*\(", call_sig)
    if not m:
        return (0, len(calls), [f"BadSignature: cannot parse {call_sig!r}"])
    fn_name = m.group(1)
    if fn_name not in module.__dict__:
        return (0, len(calls), [f"FunctionMissing: {fn_name} not defined"])

    passed = 0
    logs: List[str] = []
    func = module.__dict__[fn_name]
    for idx, (kwargs, expected) in enumerate(calls, 1):
        try:
            got = func(**kwargs)
            ok = got == expected
        except Exception as e:
            ok = False
            logs.append(f"Test#{idx} raised: {e}")
        if ok:
            passed += 1
        else:
            logs.append(f"Test#{idx} failed: got={got!r} expected={expected!r}")
    return (passed, len(calls), logs)

def _score_script_structure(resp: ScriptResponse, spec: ScriptTask) -> Tuple[float, Dict[str, Any]]:
    """Структурные метрики сценария без LLM-критика (детерминированные)."""
    acts = resp.acts or []
    ok_three_acts = (len(acts) == 3 and {a.act_number for a in acts} == {1,2,3}) if spec.force_three_act_structure else True
    scenes_ok = all(len(a.scenes) >= spec.min_scenes_per_act for a in acts)
    has_chars = all(any(c.name == need for c in resp.main_characters) for need in spec.require_main_characters)
    coherence = float(resp.coherence_score_self)
    # базовый скор: структура (0.5) + персонажи (0.2) + self-coherence (0.3)
    score = (0.5 * (1.0 if (ok_three_acts and scenes_ok) else 0.0)
             + 0.2 * (1.0 if has_chars else 0.0)
             + 0.3 * coherence)
    details = {
        "ok_three_acts": ok_three_acts,
        "min_scenes_per_act": spec.min_scenes_per_act,
        "scenes_per_act": [len(a.scenes) for a in acts],
        "has_required_characters": has_chars,
        "self_coherence": coherence,
        "genre": resp.genre,
    }
    return score, details

# ===================== РАНТАЙМ АГЕНТА (SGR) ===============================

def run_code_bench(spec: AgentSpec) -> EvalResult:
    client = _make_client(spec.llm_model)

    # Для каждой задачи запрашиваем строго структурированный ответ и тестируем
    total_passed = 0
    total = 0
    failures: List[str] = []
    per_problem = []

    for pb in spec.code.problems:
        system = "You are a senior Python engineer. Generate a single correct, clean function."
        user = f"""
Task: {pb['description']}
Required signature exactly:\n{pb['signature']}\n
Rules:
- Return only one function inside 'source_code'. No extra prints, no I/O.
- Use type hints and docstring.
- Handle edge cases carefully.
- Be efficient and readable.
"""
        completion = client.beta.chat.completions.parse(
            model=spec.llm_model,
            response_format=CodeResponse,
            messages=[
                {"role": "developer", "content": system},
                {"role": "user", "content": user}
            ],
            max_completion_tokens=spec.max_completion_tokens,
            temperature=spec.temperature,
        )
        parsed: CodeResponse = completion.choices[0].message.parsed
        func = parsed.function
        # Компиляция и тесты
        calls = [ (t["inp"], t["out"]) for t in pb["tests"] ]
        passed, ttotal, logs = _compile_and_run_function(func.source_code, pb["signature"], calls)
        total_passed += passed
        total += ttotal
        per_problem.append({"name": pb["name"], "passed": passed, "total": ttotal, "logs": logs})
        if logs:
            failures.extend([f"{pb['name']}: {msg}" for msg in logs])

    acc = total_passed / max(total, 1)
    public = {"code_tests": per_problem, "acc": acc}
    private = {}
    text = "CodeBench: {}/{} tests passed".format(total_passed, total)
    return EvalResult(score=acc, public=public, private=private, text=text)

def run_script_bench(spec: AgentSpec) -> EvalResult:
    client = _make_client(spec.llm_model)

    system = "You are a story architect. Produce structured screenplay per response schema."
    user = f"""
Create a {spec.script.genre} story with a 3-act structure and strong characters.
Return acts and scenes per the schema. Keep within ~{spec.script.max_tokens_hint} tokens.
"""

    completion = client.beta.chat.completions.parse(
        model=spec.llm_model,
        response_format=ScriptResponse,
        messages=[
            {"role": "developer", "content": system},
            {"role": "user", "content": user},
        ],
        max_completion_tokens=spec.max_completion_tokens,
        temperature=spec.temperature,
    )
    parsed: ScriptResponse = completion.choices[0].message.parsed
    # Структурные детерминированные метрики (LLM-критик можно добавить позднее)
    s_score, details = _score_script_structure(parsed, spec.script)

    public = {"script_metrics": details, "logline": parsed.logline_one_sentence}
    private = {"risks": parsed.risks_or_weaknesses}
    text = "ScriptBench: structural score={:.3f}".format(s_score)
    return EvalResult(score=s_score, public=public, private=private, text=text)

# ===================== ТОЧКА ВХОДА ДЛЯ SHINKA ============================

def run_experiment(**kwargs) -> Tuple[float, str]:
    """
    Главная функция, которую вызывает Shinka evaluator.
    Возвращает кортеж (score, text_feedback).
    """
    spec = evolvable_agent_spec()  # мутируемый геном
    # 50/50 свёртка двух задач (вес можно эволюционировать)
    r_code = run_code_bench(spec)
    r_script = run_script_bench(spec)
    combined = 0.5 * r_code.score + 0.5 * r_script.score
    text = f"{r_code.text}\n{r_script.text}"
    return combined, text

if __name__ == "__main__":
    # Локальный тест (необязательно для Shinka)
    score, txt = run_experiment()
    print("Score:", score)
    print("Text:", txt)


Что именно здесь эволюционирует? Всё внутри EVOLVE-BLOCK: модель, т‑параметры, конфигурация задач, жанр/структура, ограничения валидации. Это и есть SGR‑геном. Shinka будет предлагать патчи (diff/full/cross), мы валидируем их схемно и тестируем (evaluate.py). Именно так рекомендует Shinka: initial.py содержит «ядро алгоритма» (здесь — препроцессор SGR и рантайм агента), evaluate.py — проверку и агрегацию метрик. 
GitHub

Паттерны SGR (Routing/Cascade/Cycle), инструментальные ветви, строгие ответы — как в руководстве SGR. 

sgr_full

evaluate.py — многозапусковая агрегация метрик под Shinka
# evaluate.py
# Контракт оценщика под ShinkaEvolve: многозапусковая агрегация, combined_score, public/private.
# См. пример API в README репозитория ShinkaEvolve.  # :contentReference[oaicite:17]{index=17}

import argparse
import json
import os
from typing import Any, Dict, Tuple, List

from shinka.core import run_shinka_eval  # предоставляется ShinkaEvolve

def get_kwargs(run_idx: int) -> Dict[str, Any]:
    # Можно варьировать параметры/seed. Пока — детерминировано.
    return {"seed": run_idx}

def aggregate_fn(results: List[Tuple[float, str]]) -> Dict[str, Any]:
    """
    results: список кортежей (score, text) из run_experiment(**kwargs)
    """
    if not results:
        return {
            "combined_score": 0.0,
            "public": {"note": "no results"},
            "private": {},
            "text_feedback": "empty",
        }
    scores = [r[0] for r in results]
    texts = [r[1] for r in results]
    score = sum(scores) / len(scores)
    text = "\n---\n".join(texts)

    # public/private можно расширять сериализованными деталями
    return {
        "combined_score": float(score),     # Shinka максимизирует это значение
        "public": {"runs": len(results), "mean_score": float(score)},
        "private": {},
        "text_feedback": text,
    }

def validate_fn(result: Tuple[float, str]) -> bool:
    """Простая валидация: скор в [0,1], текст не пустой."""
    try:
        sc, tx = result
        return (0.0 <= sc <= 1.0) and bool(tx)
    except Exception:
        return False

def main(program_path: str, results_dir: str):
    metrics, correct, err = run_shinka_eval(
        program_path=program_path,
        results_dir=results_dir,
        experiment_fn_name="run_experiment",
        num_runs=3,  # усреднение
        get_experiment_kwargs=get_kwargs,
        aggregate_metrics_fn=aggregate_fn,
        validate_fn=validate_fn,
    )
    # печать для отладки
    print(json.dumps({"metrics": metrics, "correct": correct, "error": err}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--program_path", type=str, required=True)
    parser.add_argument("--results_dir", type=str, required=True)
    args = parser.parse_args()
    main(args.program_path, args.results_dir)

6) Как этим покрыть ваши 4 пункта

Улучшить саму систему.
Выше — четыре улучшения ядра (структурные патчи, schema‑novelty, бандитка по «смыслам», SGR‑мета). Вшивается в EvolutionConfig/DatabaseConfig (родительский отбор power_law/weighted/beam) и в промпты генерации патчей — знакомый Shinka путь. 
GitHub

Генерить новый код агентов по этому паттерну, «искать лучший формат схем/моделей».
Делает AgentSpec (геном) + рантайм: Shinka мутирует AgentSpec → рантайм собирает SGR‑агента → evaluate.py меряет. Для «сценариев через SGR» — уже есть ScriptBench с обязательными полями акта/сцен/персонажей; эволюция пробует иные схемы (число сцен, self‑coherence как hard/soft‑constraint, жанровые ограничения, смена роли LLM‑критика и т.д.). 

sgr_full

Агент для написания кода с SGR‑схемами, роли команды.
Расширяем AgentSpec: добавляем блок team_playbook (Architect/Coder/Tester/Reviewer/Integrator), где каждая роль — ветка Union с собственной SGR‑схемой ввода/вывода. Инструменты — «создать файл», «запустить тесты», «запустить линтер». Фитнес — тесты+статанализ+review. Shinka будет менять состав ролей/порядок/ограничения. Все это укладывается в Routing/Cycle/Cascade паттерны SGR. 

sgr_full

Стартап‑агент (маркетинг/аналитика/прод/разработка/backend/сервер)
Такой плейбук — DAG из модулей‑схем. На каждом шаге мы имеем валидное, проверяемое SGR‑представление результата (исследование рынка, PRD, KPI, юнит‑экономика, дорожная карта). Эволюция ищет: порядок шагов, набор ролей, критерии качества (и их вес), глубину каждого блока. Это прямое продолжение идеи «эволюционного проектирования агентных систем», уже показанной Shinka на AIME (многостадийный пайплайн с peer‑review и синтезом). 
Sakana AI

7) Практические замечания и советы

Стабильность и воспроизводимость: фиксируйте версии моделей и response schemas. При каждом улучшении схемы — мгновенно появляются новые eval‑кейсы (это бонус SGR). 

sgr_full

WebUI: включайте shinka_visualize — удобно смотреть «генеалогию» найденных SGR‑схем и дерево программ. 
GitHub

Бюджет: начните с num_generations=10..20, max_parallel_jobs=2..4, code_embed_sim_threshold≈0.95 и включите novelty‑судью для контрпримеров. 
arXiv

Мультиобъективность: используйте Pareto‑фронт — Shinka это уже демонстрировала (AIME: точность↔число запросов). Для стартап‑пайплайна — качество PRD / полнота / стоимость / скорость. 
Sakana AI

Безопасность инструментов: все tool‑вызовы из SGR — строго типизированные ветви Union[...] с диапазонами (см. пример Le(50) в SGR демо), чтобы модель не могла выйти за лимиты. 

sgr_full

8) Ссылки, на которые опирается дизайн

ShinkaEvolve: обзор, примеры (Circle Packing / AIME / ALE‑Bench / MoE‑Loss), новизна/бандит/острова, WebUI, контракт evaluate.py и EVOLVE-BLOCK. 
Sakana AI
+1

Тех.отчёт (arXiv): метод (родительская выборка power‑law/weighted, novelty rejection, LLM‑ансамбль), диаграммы и абляции. 
arXiv
+1

SGR: паттерны Cascade / Routing / Cycle, инструментальный агент с Union[...], структурированные ответы и constrained decoding (OpenAI chat.completions.parse). 

sgr_full

 

sgr_guide_structured

Что дальше можно докрутить быстро

Добавить LLM‑критика для сценариев (SGR‑схема ScriptCritique{clarity, originality, pacing, score}) и включить его в свёртку фитнеса.

Расширить CodeBench до набора из 8–12 задач, добавить статанализ (ruff/radon) и метрику когнитивной сложности.

Ввести schema‑linter (простые правила: запрет слишком общих str, требование явных Literal/ограничений).

Подключить внешние генераторы изображений/видео и CLIP‑метрики для «сториборд → кадры».