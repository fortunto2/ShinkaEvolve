А. Идеи «круто и нетипично»
1) Counterfactual PRD / Pre‑mortem‑гейт

Система к каждому PRD автоматически строит «анти‑PRD» — предсмертный отчёт: какие гипотезы слабые, где нет источников, где технический риск>награда. Это не вкусовой LLM‑комментарий, а структурная SGR‑схема (например, PreMortem{assumption, failure_mode, likelihood, mitigation}), которая входит в фитнес как штраф (≤ 0.05). Эволюция в Shinka начнёт усиливать те чек‑листы, что уменьшают «красные флаги». 

sgr_full

2) SERP‑«симулятор конкурента»

Помимо «снимка» выдачи, прогоняем мутатор SERP: искусственно добавляем в топ‑10 «большое медиа» и «видеокарточки» и смотрим, насколько рухнет наш детерминированный SERP‑скор. Если падение > Δ‑порога — PRD помечается «fragile SEO». Это учит эволюцию выбирать устойчивые ниши (robustness‑оптимизация). Ниже — рабочий serp_mutator.py.

3) Schema‑Novelty не только по структуре, а по «паблику»

Помимо tree‑edit по JSON‑схеме, вводим «публикационную новизну»: сравнение UVP/Problem‑фраз с корпусом из ваших уже опубликованных лендингов и LI‑постов (n‑gram/Jaccard). Если новый PRD слишком близок — reject до генерации контента. Это экономит недельные итерации. (SGR помогает: поля UVP/Problem заданы явно, их легко извлечь и сравнить.) 

sgr_full

4) PRD‑компилятор в лендинг (Astro) + A/B от CF Workers «из коробки»

PRD → .astro/.mdx с фронтматтером (hreflang, OG, JSON‑LD) + edge A/B: Worker режет трафик 50/50 на две версии копирайта, выбранные Shinka. A/B‑выбор тоже может быть «геномом»: эволюция подбирает формулировки CTA и порядок секций. Код ниже: prd2astro.py + cf_worker_ab.ts.

5) Evidence‑Linter для PRD

Жёсткий линтер, который ловит «цифры без источников», невалидные KPI, небезопасные API‑пути. Это не LLM — чистые правила: если в тексте есть числа → ожидаем URL‑источник в связанных полях, KPI ≥ 0, endpoints начинаются с /api/…. Очки линдера входят в PRD_Quality. SGR очень дружит с такими «контрольными» полями. 

sgr_full

6) PRD‑миграции и Changelog, как в БД

PRD — версионируемый артефакт: авто‑генерация CHANGELOG.md из PRD vN → vN+1 через SGR‑дифф‑схему (PrdDiff{added, removed, changed}), а лейаут лендинга пересобирается миграцией (например, переместили KPI → переразметка карточек). Это сделает быстрые релизы безопаснее.

7) Founder‑Bandwidth Scorer

Отдельная модель оценивает «сколько часов соло‑фаундеру» до MVP на вашей базе: 1‑функциональные продукты имеют свой трение‑профиль (UI/инфра/данные). Этот скор входит в Speed_Efficiency (порог «берём/не берём»). Эволюция будет отбраковывать PRD, где «1 боль → 1 функция» раздувается в «платформу».

8) I18N‑Gating по SERP‑сигналам

Локали — тоже «геном»: включаем язык, если у него устойчивый SERP‑зазор (по мутатору из п.2) и есть локальные «demand signals». Это экономит время на ненужных переводах и даёт edge‑позиции в малоконкурентных рынках.

9) «Лига персонажей» PRD‑агентов

Пусть Shinka эволюционирует не только схемы, но и микс ролей‑персон (Growth‑редактор, Tech‑редактор, Compliance‑редактор). Веса рецензентов — гены; их вклад в PRD_Quality малый, но повышает «здравый смысл» без вкусовщины. SGR делает такие роли управляемыми (структурные отзывы). 

sgr_full

10) Shadow‑PRD для соседнего «угла боли»

К каждому основному PRD генерить «тень» — соседнюю формулировку той же боли (другая терминология/ICP), и в реальном A/B (см. п.4) сравнивать CTR/lead‑rate. Шинка со временем «учится» лексике, которая надёжней конвертит.

Б. Готовые мини‑утилиты (подключайте сразу)
1) evidence_linter.py — жёсткий линтер PRD (детерминированный)
# evidence_linter.py
from __future__ import annotations
import json, re, sys
from typing import Dict, Any, List, Tuple

NUM_RE = re.compile(r"\b\d[\d\.,%]*\b", flags=re.U)
URL_RE = re.compile(r"https?://", flags=re.I)

def _contains_number(s: str) -> bool:
    return bool(NUM_RE.search(s or ""))

def _has_url(s: str) -> bool:
    return bool(URL_RE.search(s or ""))

def lint_prd(prd: Dict[str, Any]) -> Tuple[float, List[str]]:
    issues: List[str] = []

    # 1) KPI sanity
    for k in prd.get("kpi_definitions", []):
        if float(k.get("target_value", -1)) < 0:
            issues.append(f"KPI '{k.get('name','?')}' target_value < 0")

    # 2) endpoints hygiene
    for ep in prd.get("technical_requirements", {}).get("api_endpoints", []):
        if not isinstance(ep, str) or not ep.startswith("/api/"):
            issues.append(f"API endpoint must start with /api/: got {ep!r}")

    # 3) numbers without sources in key narrative fields
    narrative_fields = [
        ("problem_statement", prd.get("problem_statement","")),
        ("uvp_solution", prd.get("function",{}).get("solution","")),
        ("target_audience", prd.get("target_audience",{}).get("segment_name","")),
    ]
    text_with_numbers = [name for name, val in narrative_fields if _contains_number(val)]
    if text_with_numbers:
        # ищем URLы в weak_spots/demand_signals как прокси-источник
        evidences = " ".join([w.get("evidence_url","") for w in prd.get("niche",{}).get("weak_spots",[])])
        evidences += " " + " ".join(prd.get("niche",{}).get("demand_signals",[]))
        if not _has_url(evidences):
            issues.append(f"Numbers in {text_with_numbers} but no evidence URLs in niche.weak_spots/demand_signals")

    # 4) acceptance criteria presence
    feats = prd.get("key_features", [])
    if feats and any(not f.get("acceptance_criteria") for f in feats):
        issues.append("Some features have empty acceptance_criteria")

    # score: 1.0 if no issues, else degrade linearly
    score = max(0.0, 1.0 - 0.1*len(issues))
    return score, issues

if __name__ == "__main__":
    path = sys.argv[1]
    prd = json.loads(open(path,"r",encoding="utf-8").read())
    score, issues = lint_prd(prd)
    print(json.dumps({"lint_score":score, "issues":issues}, ensure_ascii=False, indent=2))


Подключите lint_score в PRD_Quality как ещё один множитель. SGR‑контракты удобны для такого стат‑контроля (строго заданные поля). 

sgr_full

2) schema_novelty_fingerprint.py — быстрый структурный «отпечаток» PRD
# schema_novelty_fingerprint.py
from __future__ import annotations
import json, sys
from typing import Any, Iterable, Set

def _walk(obj: Any, prefix: str = "") -> Iterable[str]:
    if isinstance(obj, dict):
        for k, v in sorted(obj.items()):
            yield prefix + "/" + k
            yield from _walk(v, prefix + "/" + k)
    elif isinstance(obj, list):
        yield prefix + "[]"
        for i, v in enumerate(obj):
            yield from _walk(v, prefix + f"[{i}]")
    else:
        t = type(obj).__name__
        yield prefix + f":{t}"

def fingerprint(d: Any) -> Set[str]:
    return set(_walk(d, ""))

def jaccard(a: Set[str], b: Set[str]) -> float:
    return len(a & b) / max(1, len(a | b))

if __name__ == "__main__":
    a = json.loads(open(sys.argv[1],"r",encoding="utf-8").read())
    b = json.loads(open(sys.argv[2],"r",encoding="utf-8").read())
    fa, fb = fingerprint(a), fingerprint(b)
    sim = jaccard(fa, fb)
    print(json.dumps({"similarity": sim, "novelty": 1.0 - sim}, indent=2))


Используйте «novelty» как пре‑фильтр в Shinka (отсекаем почти одинаковые PRD до выполнения). SGR гарантирует стабильные поля/структуры, поэтому отпечатки работают чисто. 

sgr_full

3) serp_mutator.py — стресс‑тест «что если завтра зайдёт гигант»
# serp_mutator.py
from __future__ import annotations
import json, sys, copy, random
from typing import List, Dict, Tuple

def mutate(items: List[Dict], inject_big_media: bool = True, inject_video: bool = True) -> List[Dict]:
    m = copy.deepcopy(items[:10])
    if inject_big_media:
        m[0]["is_big_media"] = True; m[0]["domain"] = "bigmedia.com"
    if inject_video:
        for i in range(0, min(3, len(m))):
            m[i]["has_video"] = True
    # обновим свежесть «конкурентов»
    for i in range(len(m)//2):
        m[i]["updated_days_ago"] = random.randint(1, 14)
    return m

def score_serp(items: List[Dict]) -> float:
    n = min(len(items), 10) or 1
    forums = sum(1 for x in items[:n] if x.get("is_forum") or x.get("is_reddit"))
    big = sum(1 for x in items[:n] if x.get("is_big_media"))
    fresh = sum(1 for x in items[:n] if (x.get("updated_days_ago", 9999) <= 60))
    video = sum(1 for x in items[:n] if x.get("has_video"))
    brands = sum(1 for x in items[:n] if x.get("is_brand_strong"))
    uniq = len({x.get("domain") for x in items[:n]})
    s = 0.0
    s += 0.12 * (forums / n)
    s += 0.10 * (1.0 - min(fresh / n, 1.0))
    s += 0.08 * (1.0 - min(video / n, 1.0))
    s += 0.10 * (1.0 - min(brands / n, 1.0))
    s -= 0.15 * (big / n)
    s += 0.08 * (1.0 - (n - uniq)/n)
    return max(0.0, min(1.0, s + 0.5))

if __name__ == "__main__":
    path = sys.argv[1]
    items = json.loads(open(path,"r",encoding="utf-8").read())
    base = score_serp(items)
    mutated = mutate(items)
    after = score_serp(mutated)
    print(json.dumps({"baseline": base, "after_injection": after, "delta": after - base}, indent=2))


Если delta << 0 — ниша хрупкая. Включите это в фитнес как «robustness‑penalty».

4) prd2astro.py — компилятор PRD → Astro‑страница
# prd2astro.py
from __future__ import annotations
import json, os, sys
from datetime import datetime

TPL = """---
title: "{title}"
description: "{desc}"
pubDate: "{date}"
lang: "{lang}"
layout: "@/layouts/Base.astro"
og:
  image: "/og/{slug}.png"
  title: "{title}"
  description: "{desc}"
hreflang:
{hreflang}
---

# {h1}

> {logline}

## Problem
{problem}

## Solution (One function)
{solution}

## Acceptance criteria
{ac}

## KPI
{kpi}

## Target audience
- Segment: {segment}
- Channels: {channels}

## Tech notes
- API: {apis}
- Integrations: {integrations}
"""

def slugify(s: str) -> str:
    return "-".join("".join(c.lower() if c.isalnum() else "-" for c in s).split("-")).strip("-")

def main(prd_json: str, out_dir: str, lang: str = "en"):
    prd = json.loads(open(prd_json,"r",encoding="utf-8").read())
    title = prd["function"]["title"]
    h1 = title
    desc = prd["function"]["success_criterion"]
    problem = prd["problem_statement"]
    solution = prd["function"]["solution"]
    ac = "\n".join([f"- {', '.join(f['acceptance_criteria'])}" for f in prd.get("key_features", []) if f.get("acceptance_criteria")])
    kpi = "\n".join([f"- {k['name']}: {k['target_value']} ({k['measure']})" for k in prd.get("kpi_definitions", [])])
    segment = prd["target_audience"]["segment_name"]
    channels = ", ".join(prd["target_audience"]["channels"])
    apis = ", ".join(prd["technical_requirements"]["api_endpoints"])
    integrations = ", ".join(prd["technical_requirements"]["integrations"])
    logline = prd["niche"]["keyword"]
    slug = slugify(title)

    hreflang = ""
    for loc in prd.get("i18n", []):
        hreflang += f"  - {loc}\n"

    body = TPL.format(
        title=title, desc=desc, date=datetime.utcnow().isoformat(),
        lang=lang, h1=h1, logline=logline, problem=problem, solution=solution,
        ac=ac or "- TBD", kpi=kpi or "- TBD",
        segment=segment, channels=channels or "-",
        apis=apis or "-", integrations=integrations or "-", slug=slug, hreflang=hreflang or "  - en"
    )

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{slug}.mdx")
    open(path,"w",encoding="utf-8").write(body)
    print(path)

if __name__ == "__main__":
    # python prd2astro.py artifact_prd.json ./site/src/pages en
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "en")


Это «компилятор лендинга» из PRD. SGR‑структура упрощает экспорт (полям уже даны места). 

sgr_full

 

sgr_guide_structured

5) cf_worker_ab.ts — A/B сплит на Cloudflare Workers (полноценный, без библиотек)
// cf_worker_ab.ts
export interface Env {}
const COOKIE = "ab_bucket";

function pickBucket(): "A" | "B" {
  return Math.random() < 0.5 ? "A" : "B";
}
function getCookie(req: Request, name: string): string | null {
  const h = req.headers.get("Cookie") || "";
  const m = h.match(new RegExp(`${name}=([^;]+)`));
  return m ? decodeURIComponent(m[1]) : null;
}
function setCookie(name: string, val: string): string {
  const expires = new Date(Date.now() + 1000*60*60*24*365).toUTCString();
  return `${name}=${encodeURIComponent(val)}; Path=/; Expires=${expires}; Secure; SameSite=Lax`;
}
export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    const existing = getCookie(req, COOKIE) as "A" | "B" | null;
    const bucket = existing || pickBucket();

    // Пример: / => /a/ или /b/ (серверим предварительно собранные Astro-страницы)
    if (url.pathname === "/" || url.pathname === "/index.html") {
      url.pathname = bucket === "A" ? "/a/index.html" : "/b/index.html";
    }

    const r = await fetch(url.toString(), {
      headers: { "cf-cache-status": "DYNAMIC" },
    });
    const res = new Response(r.body, r);
    if (!existing) res.headers.append("Set-Cookie", setCookie(COOKIE, bucket));
    res.headers.set("x-ab-bucket", bucket);
    return res;
  }
} satisfies ExportedHandler<Env>;


Как использовать: положите две версии лендинга site/a/index.html и site/b/index.html (простейшая разница — порядок секций/CTA). Worker раздаёт и проставляет cookie для стабильного бакета.

6) sg_prd_review_schema.py — SGR‑критик «микродоля» (структурный, повторяемый)
# sg_prd_review_schema.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Literal
from annotated_types import Ge, Le, MinLen, MaxLen

class PRDReview(BaseModel):
    clarity: float = Field(ge=0.0, le=1.0)
    completeness: float = Field(ge=0.0, le=1.0)
    red_flags: List[str] = Field(default_factory=list)
    final_score: float = Field(ge=0.0, le=1.0)
    recommendation: Literal["ship","iterate","kill"]

# пример использования:
# completion = client.beta.chat.completions.parse(
#   model="gpt-4o", response_format=PRDReview,
#   messages=[{"role":"developer","content":"Review PRD structurally, no style."},
#             {"role":"user","content": json.dumps(prd)}])
# review = completion.choices[0].message.parsed
# затем финальный фитнес += 0.05*review.final_score


Структура SGR гарантирует предсказуемую и слабую (≤ 0.05) добавку к фитнесу без «поехавших вкусовых оценок». 

sgr_full

В. Как это вкрутить в текущий «эволюционный контур»

Добавьте evidence_linter.py, schema_novelty_fingerprint.py, serp_mutator.py в ваш evaluate_prd и:

lint_score → множитель к PRD_Quality,

novelty → пре‑фильтр родителей,

delta из serp_mutator → «robustness‑penalty» к Market_Coverage.
Всё детерминированно → воспроизводимо. 

sgr_guide_structured

В геном Shinka добавьте пороги lint_min, robustness_delta_min, языки i18n и веса. Shinka начнёт сама крутить гайки до нужных компромиссов. 

sgr_full

Компилятор PRD → Astro поставьте в пост‑шаг evaluate: каждый кандидат с score>τ получает страницу. Дополнительно — маршрут в CF Worker для A/B (п.4).

Counterfactual PRD и PRD‑миграции — оформите SGR‑моделями (как в примере PRDReview) и включите в пайплайн как лёгкие шаги перед экспортом. 

sgr_full

Что именно вы могли «упустить»

Устойчивость к конкуренции: большинство систем смотрят на текущую SERP, но не тестируют «что если завтра зайдёт гигант». Мутатор SERP (п.2) радикально снижает риск.

Доказательная дисциплина: без Evidence‑линтера PRD часто содержит «красивые числа» → неверные приоритеты. Линтер уберёт это на 0‑дне.

Авто‑доставка PRD‑контента: PRD→Astro+Workers (п.4–5) даёт «ship fast» без ручных сборок.

**Эволюция не только «что писать», но и как публиковать (A/B, порядок секций, лексика UVP).

Персон‑редакторы с малыми весами (микросудьи) вносят дисциплину, не ломая детерминизм.