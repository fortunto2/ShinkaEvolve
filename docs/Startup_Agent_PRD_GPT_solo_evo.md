1) Что именно эволюционируем (а что — нет)

Не эволюционируем: код продукта, фичи, стек — это отдельно, позже.
Эволюционируем: именно процесс рождения PRD и его схемы/чек‑листы, чтобы каждый цикл давал лучший PRD для разработки и маркетинга.

Геном (что мутирует Shinka):

SGR‑схемы модулей PRD‑конвейера (Trend→Idea→Research→Marketing→Analytics→PRD), их поля и ограничения (Literal/Annotated/Union). 

sgr_guide_structured

 

sgr_full

Плейбук шагов (Routing/Cascade/Cycle): порядок и условия обязательных проверок, где требовать источники/цитаты, где включать LLM‑критика. 

sgr_full

Веса фитнеса (функции качества PRD; см. §3) и параметры бюджета (сколько токенов на этап/критика).

Языки локализации (EN базово + выбранные локали) и правила i18n (глоссарий/терминология).

Фенотип (что исполняется каждый прогон):

SGR‑агент, который структурированно собирает PRD (и промежуточные артефакты: ниши, маркетинг, аналитика) и валидирует их по схемам. 

sgr_full

2) «Без выдумок»: как заставить аналитику опираться на факты

Чтобы аналитик не придумывал цифры, в схемах делаем обязательными поля источников/доказательств и «флажки уверенности»; плюс работаем по локальным снимкам данных:

Вводим типы:

Evidence{source_url, source_type, captured_at, quote_or_number, confidence} — обязательно для любой числовой оценки/утверждения.

SerpWeakSpot{kind, evidence_url, note} — фиксирует «слабые места выдачи» с ссылками. (Мы уже так делали для ниш. )

NicheCandidate{keyword, locale, serp_score, weak_spots[], demand_signals[]} — «сигналы спроса» — это короткие цитаты или формулировки боли со ссылками. 

sgr_guide_structured

Работаем по офлайн‑снимкам (SERP‑json, выгрузки), чтобы Shinka не трогала сеть: эвал детерминированный, повторяемый.

В PRD‑схеме поля TAM/SAM/SOM делаем опциональными и добавляем sources: List[Evidence]. Без источников — штраф в фитнесе (см. §3). 

sgr_guide_structured

3) Фитнес для эволюции PRD (что максимизируем)

Сводный скор (нормирован 0..1):

Fitness = 0.4 * PRD_Quality
        + 0.3 * Market_Coverage
        + 0.2 * Innovation_Score
        + 0.1 * Speed_Efficiency


(Вы уже это фиксировали, я сохраняю, чтобы Shinka работала по тем же рельсам. ) 

sgr_guide_structured

PRD_Quality — структурная полнота PRD (§, KPI, NFR, риски, приемочные критерии): считается детерминированно по схеме. 

sgr_guide_structured

Market_Coverage — покрытие конкурентов/регуляторики/тех‑ландшафта + корректные цепочки TAM≥SAM≥SOM, и наличие источников. 

sgr_guide_structured

Innovation_Score — средний innovation_score по идеям + семантическая диверсификация связанных трендов (по ключам из схемы). 

sgr_guide_structured

Speed_Efficiency — мягкая экспонента по времени (быстрее таргета → 1.0; дольше → плавно падает). (Важна для режима соло‑фаундера.)

Вся свёртка — детерминированная: оцениваем структуру и наличие доказательств, а не вкус текста. Для стиля/ясности можно опционально включить LLM‑критика, но он отчитывается по SGR‑схеме (например, PRDReview{clarity, completeness, red_flags[], score}) и влияет ограниченно (например, ≤ +0.05). 

sgr_full

4) Новизна: «не тратить попытки на одно и то же»

До запуска кандидата Shinka делает schema‑novelty:

сравнение дерева схемы (tree‑edit / нормализованный JSON‑fingerprint) и множеств Literal/Union (как менялись ветви);

текстовая близость по ключевым секциям PRD (эмбеддинги заголовков/UVP).
Если слишком похоже — отбрасываем до выполнения (экономим бюджет). Идея опирается на схематизацию SGR и общий механизм новизны/архива Shinka; мы просто используем структурные сигналы, которые SGR даёт «бесплатно». 

sgr_full

5) Ансамбль LLM и роли (бандит выбирает «кто за что»)

Минимум три «роли» в ансамбле:

Draft — быстрая модель для черновиков идей/ниш.

Analyst — модель посильнее, когда нужно аккуратно заполнить схемы с Evidence.

Critic — компактный SGR‑критик PRD.

Награда для бандита — не только прирост Fitness, но и «стоимость шага» (токены/время) → чаще вызываем модель, которая приносит смысловые улучшения схем/проверок за разумную цену. 

sgr_full

6) Данные для офлайн‑эвалюации (без сети, воспроизводимо)

SERP‑snapshots (JSON 10–20 результатов): флаги is_forum/is_big_media/updated_days_ago/has_video/is_brand_strong/domain/url — хватает для скоринга «занимаемости выдачи» (взял из предыдущего варианта).

Короткие сырьевые «сигналы спроса»: пары цитата–ссылка из Reddit/форумов; можно положить их в один JSON, агент обязан сослаться.

Тестовые топики/локали: 5–10 штук (EN базово + 1–2 других), чтобы эволюция не переобучалась на один сюжет.

Все это подключается на вход SGR‑агента как «внешние артефакты», а Shinka эволюционирует схемы и порядок проверки, а не сами данные. 

sgr_full

7) Как выглядит полный цикл

Выбор родителя (по качеству/диверсификации) →

Мутация генома: изменения SGR‑схем/плейбука/весов/локалей →

Пре‑фильтр новизны (schema‑novelty + лёгкая текстовая близость) →

Запуск агента: собрать PRD по схемам с обязательными Evidence (работаем по офлайн‑данным) →

Скоринг (детерминированный) →

Обновить архив/бандит; каждые N поколений — SGR‑meta summary: что сработало и почему (в схеме SearchInsight{pattern, when_to_use, risks}). 

sgr_full

8) Мини‑код «Shinka‑пак для PRD»: два файла

Ниже полные файлы без заглушек, чтобы запускать эволюцию именно PRD (не код/скрипты). Они опираются на SGR‑подход (Structured Output), используют офлайн‑SERP‑снимки и дают детерминированный fitness.

Схемы/паттерны SGR (инструментальная форма, Union/Annotated, строгая валидация) — из вашего руководства; минимальные структуры для ниш/PRD — из вашего PRD‑документа. 

sgr_full

 

sgr_guide_structured

initial_prd.py — геном (EVOLVE‑BLOCK) + SGR‑агент + скоринг
# initial_prd.py
# Эволюционируем процесс получения PRD: SGR-схемы, чек-листы, веса.
# Работает по офлайн SERP-снимку (JSON), без сетевых вызовов.
from __future__ import annotations

import json, os, re, time
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from annotated_types import Ge, Le, MinLen, MaxLen
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

# ---------- EVOLVE-BLOCK-START ----------
# Shinka будет менять только содержимое этого блока.

class EvoWeights(BaseModel):
    w_prd: float = Field(0.4, ge=0.0, le=1.0)
    w_market: float = Field(0.3, ge=0.0, le=1.0)
    w_innov: float = Field(0.2, ge=0.0, le=1.0)
    w_speed: float = Field(0.1, ge=0.0, le=1.0)
    target_seconds: float = Field(1800.0, ge=60.0, le=7200.0)

class EvoI18N(BaseModel):
    locales: List[Literal["en","es","de","fr","ru","pt","it","pl","hi","ja","zh"]] = ["en","ru"]

class EvoLLM(BaseModel):
    model_draft: str = "gpt-4o-mini"
    model_analyst: str = "gpt-4o"
    temperature: float = Field(0.3, ge=0.0, le=1.0)
    max_tokens: int = Field(4000, ge=512, le=16000)

class AgentSpecPRD(BaseModel):
    weights: EvoWeights = EvoWeights()
    i18n: EvoI18N = EvoI18N()
    llm: EvoLLM = EvoLLM()

def evolvable_agent_spec() -> AgentSpecPRD:
    return AgentSpecPRD()

# ---------- EVOLVE-BLOCK-END ----------

# ------------------- SGR СХЕМЫ (из вашего PRD/SGR) -------------------

class SerpWeakSpot(BaseModel):
    kind: Literal["forums","outdated","thin_content","low_brand","no_video"]
    evidence_url: str
    note: str

class NicheCandidate(BaseModel):
    keyword: str
    locale: Literal["en","es","de","fr","ru","pt","it","pl","hi","ja","zh"]
    serp_score: float = Field(ge=0.0, le=1.0)
    weak_spots: List[SerpWeakSpot]
    demand_signals: List[str] = Field(default_factory=list)

class OneFunctionSpec(BaseModel):
    title: str
    pain: str
    solution: str
    success_criterion: str
    input_output_example: Dict[str,str]

class CustomerProfile(BaseModel):
    segment_name: str
    pains: List[str]
    gains: List[str]
    channels: List[str]

class FeatureSpec(BaseModel):
    name: str
    user_story: str
    acceptance_criteria: List[str]
    priority: Literal["must","should","could"]

class KPIDefinition(BaseModel):
    name: str
    target_value: float
    measure: Literal["daily","weekly","monthly","quarterly"]

class RiskFactor(BaseModel):
    explanation: str
    severity: Literal["low","medium","high"]

class TechnicalSpec(BaseModel):
    api_endpoints: List[str]
    integrations: List[str]
    data_model_notes: Optional[str] = None
    non_functional: Dict[str, Any] = Field(default_factory=dict)

class PRDMinimal(BaseModel):
    niche: NicheCandidate
    function: OneFunctionSpec
    pricing: Literal["free","one_time","subscription"]
    stripe_needed: bool
    i18n: List[str]
    problem_statement: str
    target_audience: CustomerProfile
    key_features: List[FeatureSpec]
    kpi_definitions: List[KPIDefinition]
    risk_assessment: List[RiskFactor]
    technical_requirements: TechnicalSpec

# ------------------- УТИЛИТЫ -------------------

@dataclass
class EvalResult:
    score: float
    public: Dict[str, Any]
    text: str

def _make_client() -> OpenAI:
    return OpenAI()

def score_serp(items: List[Dict]) -> Tuple[float, Dict[str, Any]]:
    """Детерминированный скоринг 'занимаемости выдачи' по топ-10."""
    if not items: 
        return 0.0, {"note":"no serp items"}
    n = min(len(items), 10)
    forums = sum(1 for x in items[:n] if x.get("is_forum") or x.get("is_reddit"))
    big = sum(1 for x in items[:n] if x.get("is_big_media"))
    fresh = sum(1 for x in items[:n] if (x.get("updated_days_ago", 9999) <= 60))
    video = sum(1 for x in items[:n] if x.get("has_video"))
    brands = sum(1 for x in items[:n] if x.get("is_brand_strong"))
    uniq = len({x.get("domain") for x in items[:n]})
    s = 0.0
    s += 0.12 * (forums / n)
    s += 0.10 * (1.0 - min(fresh / max(n,1), 1.0))
    s += 0.08 * (1.0 - min(video / max(n,1), 1.0))
    s += 0.10 * (1.0 - min(brands / max(n,1), 1.0))
    s -= 0.15 * (big / n)
    s += 0.08 * (1.0 - (n - uniq)/max(n,1))
    s_norm = max(0.0, min(1.0, s + 0.5))
    details = dict(n=n, forums=forums, big=big, fresh=fresh, video=video, brands=brands, uniq_domains=uniq)
    return s_norm, details

# ---- СКОРИНГ PRD (детерминированный; соответствует вашему PRD) ----

def prd_quality(prd: PRDMinimal) -> Tuple[float, Dict[str, Any]]:
    has_problem = 1.0 if prd.problem_statement and len(prd.problem_statement) >= 30 else 0.0
    has_target = 1.0 if prd.target_audience and prd.target_audience.segment_name else 0.0
    features_ok = 0.0
    if prd.key_features:
        filled = sum(1 for f in prd.key_features if f.acceptance_criteria)
        features_ok = filled / len(prd.key_features)
    features_count_bonus = min(len(prd.key_features) / 6.0, 1.0)
    kpis_ok = min(len(prd.kpi_definitions) / 5.0, 1.0)
    tech_ok = 1.0 if (len(prd.technical_requirements.api_endpoints) >= 3 and prd.technical_requirements.non_functional) else 0.0
    risks_div = min(len(prd.risk_assessment) / 5.0, 1.0)
    score = 0.2*has_problem + 0.15*has_target + 0.2*features_ok + 0.1*features_count_bonus \
          + 0.15*kpis_ok + 0.1*tech_ok + 0.1*risks_div
    return max(0.0, min(1.0, score)), {
        "has_problem": has_problem, "has_target": has_target,
        "features_ok": features_ok, "features_count_bonus": features_count_bonus,
        "kpis_ok": kpis_ok, "tech_ok": tech_ok, "risks_div": risks_div
    }

def market_coverage(prd: PRDMinimal) -> Tuple[float, Dict[str, Any]]:
    # Прокси по нише и структурам (без «придуманных цифр»)
    ws = prd.niche.weak_spots or []
    ws_div = min(len(ws)/4.0, 1.0)
    icp_ok = 1.0 if prd.target_audience and prd.target_audience.segment_name else 0.0
    uvp_ok = 1.0 if prd.function and len(prd.function.solution) >= 30 else 0.0
    # Для TAM/SAM/SOM в PRDMinimal нет чисел — не штрафуем, пока они не включены со sources
    score = 0.35*ws_div + 0.325*icp_ok + 0.325*uvp_ok
    return max(0.0, min(1.0, score)), {"weak_spots_div": ws_div, "icp_ok": icp_ok, "uvp_ok": uvp_ok}

def innovation_score(prd: PRDMinimal) -> Tuple[float, Dict[str, Any]]:
    # эвристика: диверсификация related_keywords и оригинальность pain/solution (по длине/наличию конкретики)
    kw = set()
    for w in prd.niche.weak_spots:  # используем заметки как «углы»
        kw.update(re.findall(r"[a-zA-Z0-9\-]{3,}", w.note or ""))
    diversity = min(len(kw)/12.0, 1.0)
    spec_len = len(prd.function.solution or "")
    originality = 1.0 if spec_len >= 200 else spec_len/200.0
    score = 0.6*diversity + 0.4*originality
    return max(0.0, min(1.0, score)), {"diversity": diversity, "originality_proxy": originality}

def speed_efficiency(seconds_elapsed: float, target_sec: float) -> float:
    if seconds_elapsed <= target_sec: return 1.0
    # мягкий спад: вдвое дольше → ≈0.37
    from math import exp
    return max(0.0, min(1.0, exp(-(seconds_elapsed - target_sec)/target_sec)))

def total_fitness(prd: PRDMinimal, t_elapsed: float, weights: EvoWeights) -> Tuple[float, Dict[str, Any]]:
    p_q, p_d = prd_quality(prd)
    m_c, m_d = market_coverage(prd)
    inn, i_d = innovation_score(prd)
    sp = speed_efficiency(t_elapsed, weights.target_seconds)
    total = weights.w_prd*p_q + weights.w_market*m_c + weights.w_innov*inn + weights.w_speed*sp
    details = {
        "PRD_Quality": p_q, **{f"PRD::{k}":v for k,v in p_d.items()},
        "Market_Coverage": m_c, **{f"MC::{k}":v for k,v in m_d.items()},
        "Innovation_Score": inn, **{f"INNOV::{k}":v for k,v in i_d.items()},
        "Speed_Efficiency": sp
    }
    return max(0.0, min(1.0, total)), details

# ------------------- SGR-АГЕНТ: генерим нишу и PRD -------------------

def _sg_output(client: OpenAI, model: str, resp_model: type[BaseModel], messages: List[Dict[str,str]], max_tokens: int, temperature: float):
    comp = client.beta.chat.completions.parse(
        model=model,
        response_format=resp_model,
        messages=messages,
        max_completion_tokens=max_tokens,
        temperature=temperature,
    )
    return comp.choices[0].message.parsed

def build_prd(spec: AgentSpecPRD, topic: str, serp_items: List[Dict], locale: str) -> PRDMinimal:
    client = _make_client()
    serp_score, serp_meta = score_serp(serp_items)
    # 1) Ниша
    niche: NicheCandidate = _sg_output(
        client, spec.llm.model_draft, NicheCandidate,
        messages=[
            {"role":"developer","content":"You are a niche miner. Be factual; include weak spots with URLs; do not invent numbers."},
            {"role":"user","content":f"Find a sharp micro-niche around: {topic}; locale={locale}. Base it on provided SERP snapshot only."}
        ],
        max_tokens=spec.llm.max_tokens, temperature=spec.llm.temperature
    )
    # принудительно перезапишем serp_score из детерминированного скорера:
    niche.serp_score = serp_score

    # 2) PRD
    prd: PRDMinimal = _sg_output(
        client, spec.llm.model_analyst, PRDMinimal,
        messages=[
            {"role":"developer","content":"You are a product architect. Produce PRDMinimal strictly by schema; include acceptance criteria; be concise and specific."},
            {"role":"user","content":f"Build a one-function product PRD for niche={niche.model_dump_json()} in locale={locale}. Keep it implementable in 2 days."}
        ],
        max_tokens=spec.llm.max_tokens, temperature=spec.llm.temperature
    )
    # синхронизируем поля, чтобы схемы были согласованы:
    prd.niche = niche
    if locale not in prd.i18n:
        prd.i18n = [locale] + [x for x in prd.i18n if x != locale]
    return prd

# ------------------- ТОЧКА ВХОДА ДЛЯ SHINKA -------------------

def run_experiment(**kwargs) -> Tuple[float, str]:
    """
    Вход для Shinka: kwargs ожидает:
      - topic: str
      - serp_file: путь к JSON со списком SERP-объектов (см. README)
      - locale: str (например, 'en')
    """
    started = time.time()
    spec = evolvable_agent_spec()

    topic = kwargs.get("topic", "ai micro-saas pdf signing")
    serp_file = kwargs.get("serp_file")
    locale = kwargs.get("locale", spec.i18n.locales[0])

    if not serp_file or not os.path.exists(serp_file):
        raise FileNotFoundError("serp_file is required and must exist")

    serp_items = json.loads(open(serp_file,"r",encoding="utf-8").read())
    prd = build_prd(spec, topic, serp_items, locale)

    elapsed = time.time() - started
    total, details = total_fitness(prd, elapsed, spec.weights)

    # сохраняем артефакт PRD (чтобы можно было открыть WebUI/архив)
    out_dir = kwargs.get("results_dir",".")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir,"artifact_prd.json"),"w",encoding="utf-8") as f:
        f.write(prd.model_dump_json(indent=2, ensure_ascii=False))

    text = f"PRD fitness={total:.3f}; elapsed={elapsed:.1f}s; serp={prd.niche.serp_score:.2f}"
    return float(total), text

if __name__ == "__main__":
    # Локальный пример: python initial_prd.py
    path = os.environ.get("SERP_FILE","serp_sample.json")
    print(run_experiment(topic="micro-saas screenshot-to-pdf", serp_file=path, locale="en"))


Примечания по коду:

EVOLVE‑BLOCK содержит только то, что Shinka должна менять: веса фитнеса/таргет времени, локали, конфиг LLM. 

sgr_full

Агент жёстко привязан к офлайн‑SERP JSON — без него бросаем ошибку (никаких «выдуманных» цифр).

Все оценки — детерминированные; Structured Output/SGR уводит вариативность в границы схем. 

sgr_full

evaluate_prd.py — многозапусковая агрегация без внешних зависимостей
# evaluate_prd.py
# Запускает initial_prd.run_experiment() несколько раз и печатает JSON-метрики.
from __future__ import annotations
import argparse, importlib.util, json, os
from typing import Any, Dict, Tuple, List

def load_module(mod_path: str):
    spec = importlib.util.spec_from_file_location("candidate_program", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main(program_path: str, results_dir: str, serp_file: str, topic: str, locale: str, runs: int):
    mod = load_module(program_path)
    results: List[Tuple[float,str]] = []
    for i in range(runs):
        score, text = mod.run_experiment(topic=topic, serp_file=serp_file, locale=locale, results_dir=results_dir)
        results.append((float(score), str(text)))
    scores = [s for s,_ in results]
    mean_score = sum(scores)/len(scores) if scores else 0.0
    out = {
        "combined_score": float(mean_score),
        "public": {
            "runs": runs,
            "by_run": [{"score":float(s),"text":t} for s,t in results],
        },
        "private": {},
        "text_feedback": f"mean={mean_score:.3f} over {runs} runs"
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--program_path", required=True)
    ap.add_argument("--results_dir", required=True)
    ap.add_argument("--serp_file", required=True, help="path to SERP JSON snapshot")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--locale", default="en")
    ap.add_argument("--runs", type=int, default=3)
    args = ap.parse_args()
    os.makedirs(args.results_dir, exist_ok=True)
    main(args.program_path, args.results_dir, args.serp_file, args.topic, args.locale, args.runs)


Формат SERP JSON (пример):

[
  {"url":"https://www.reddit.com/r/SomeSub/...", "domain":"reddit.com", "is_forum":true, "is_reddit":true,
   "is_big_media":false, "updated_days_ago":120, "has_video":false, "is_brand_strong":false},
  {"url":"https://example.com/old-guide", "domain":"example.com", "is_forum":false,
   "is_big_media":false, "updated_days_ago":365, "has_video":false, "is_brand_strong":false}
]

9) Где именно Shinka «вплетается» (и за счёт чего будет прогресс)

Точки мутаций (genes):
AgentSpecPRD.weights/*, i18n.locales, llm.*, а также шаблоны/поля внутри SGR‑схем (добавлять/ужесточать обязательные поля в PRD, вводить новые чек‑листы маркетинга/аналитики, обязательность Evidence). Это делает PRD более полным, проверяемым и пригодным для разработки. 

sgr_guide_structured

 

sgr_full

Новизна отсеивает «почти то же самое PRD» до запуска: экономия бюджета и быстрее приход к сильным рецептам заполнения PRD.

Ансамбль LLM будет «сам» распределять роли (через награду) между черновиками/аналитикой/критиком под ваши ограничения. 

sgr_full

SGR‑meta (поиск инсайтов) фиксирует повторяемые удачные паттерны формулировок KPI, NFR, UVP и т.п., чтобы следующие поколения лучше закрывали недочёты. 

sgr_full

10) Операционный режим соло‑фаундера

1 SERP‑снимок → 1 PRD (EN + ещё один язык) за один цикл; цель: ≤ 30 минут на PRD.

Еженедельно — 3–5 тем/ниш, выбираете лучшую по combined_score, по ней делаете лендинг/видео/LI‑пост.

Когда появятся первые реальные поведенческие сигналы (CTR/конверсия), добавляете их в фитнес как слабый доп. критерий (например, +0.05 за превышение таргета) — но офлайн‑оценка остаётся главной.

11) Риски и как их гасить

Переоптимизация под структурный скор → включайте крохотный вес SGR‑критика (контролируемый, повторяемый), используйте разные темы/локали в датасете. 

sgr_full

Фейковые цифры → любые числа/утверждения допускайте только с Evidence; без источника — ноль в соответствующем подпоказателе. 

sgr_guide_structured

Дубли PRD → schema‑novelty до запуска.

Стоимость инференса → бандитка + ограничения на токены по ролям.

12) Что сделать прямо сейчас (чёткий чек‑лист)

Сохранить два файла из §8 в ваш проект (initial_prd.py, evaluate_prd.py).

Подготовить 3–5 SERP JSON по вашим нишам (по образцу).

Первый прогон (без Shinka):

python evaluate_prd.py --program_path ./initial_prd.py --results_dir ./out \
  --serp_file ./serp_my_niche.json --topic "micro-saas screenshot-to-pdf" --locale en --runs 3


Подключить в ShinkaEvolve как «задачу»: initial_prd.py (программа) + evaluate_prd.py (оценка).

В Shinka включить novelty‑filter по схеме и ансамбль LLM (хотя бы 2 модели: draft/analyst).

Провести 10–20 поколений, посмотреть WebUI/архив артефактов PRD, отобрать лучший.

Почему это соответствует вашему подходу

SGR даёт типобезопасность и предсказуемость (и дешёвые модели ведут себя аккуратно); PRD формируется по явным схемам/чек‑листам. 

sgr_full

ShinkaEvolve обеспечивает эволюционное улучшение самих схем/процедур, а не текста; итог — лучшее PRD (полнота, структура, проверяемость) за меньшее число попыток. И это отлично ложится на ваш «продукт‑как‑фабрику» (1 боль → 1 функция). 

sgr_guide_structured

Если хотите, следующий шаг — добавляю «микро‑критика PRD» (SGR‑схема Review) и schema‑novelty‑фингерпринт, плюс шаблон экспорта PRD в Cloudflare Pages/Workers (лендинг/оглавление/KPI‑таблица) — но ядро, вокруг которого строить «пункт 9», у вас уже готово и запускаемо.