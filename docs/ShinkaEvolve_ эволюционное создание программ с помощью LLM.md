# ShinkaEvolve: эволюционное создание программ с помощью LLM

## Обзор и цели проекта ShinkaEvolve

**ShinkaEvolve** – это новая открытая платформа от Sakana AI для
эволюционного улучшения программ и алгоритмов с использованием больших
языковых моделей
(LLM)[\[1\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=Sakana%20AI%20has%20released%20ShinkaEvolve%2C,research%20report%20and%20public%20code).
Главная задача ShinkaEvolve – автоматизировать **поиск новых
алгоритмических решений** на основе идей LLM при существенном снижении
числа попыток/итераций, необходимых для достижения высококачественного
решения. В классических подходах эволюционного программирования на LLM
(например, в недавно представленном закрытом проекте DeepMind под
названием AlphaEvolve) наблюдалась крайне низкая эффективность по
выборке – требовались тысячи запусков программ, чтобы найти хорошее
решение[\[2\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=number%20of%20evaluations%20needed%20to,with%20a%20research%20report%20and).
ShinkaEvolve решает эту проблему: в **референтной задаче упаковки
окружностей** (классический бенчмарк, размещение 26 кругов в квадрате)
новая система нашла рекордную конфигурацию примерно за *150 оценок*
программ, тогда как предыдущим системам требовались тысячи
запусков[\[3\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=language%20models%20,research%20report%20and%20public%20code)[\[4\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=,10%20tasks%20and%20pushes%20one).
Таким образом, ShinkaEvolve демонстрирует **прорыв в эффективности
поиска**, сохраняя при этом мощь LLM для генерации кода и открыто
предоставляя сообществу код и
инструменты[\[5\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20is%20an%20Apache,Code%20and%20report%20are%20public).

Основная идея ShinkaEvolve – вдохновиться принципами *эволюции в
природе* и перенести их на поиск программ и решений при помощи
ИИ[\[6\]](https://sakana.ai/shinka-evolve/#:~:text=At%20Sakana%20AI%2C%20we%20are,driven%20discovery).
Система использует **популяцию программ**, которые постепенно улучшаются
поколение за поколением. Крупные языковые модели выступают в роли
«мутационных операторов» – они предлагают изменения в коде или новые
фрагменты
алгоритмов[\[7\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=search%2C%20,operators%20that%20suggest%20code%20improvements).
Затем каждая новая программа **автоматически оценивается** специальным
скриптом на предмет качества решения задачи (фитнес-функция), и на
основе результатов обновляется архив лучших
решений[\[8\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20High,programs%2C%20and%20evaluates%20their%20fitness).
Благодаря продуманным механизмам отбора и отброса неэффективных мутаций
(о них ниже), ShinkaEvolve удаётся найти инновационные решения
значительно быстрее и дешевле, чем прежние подходы, сохраняя или улучшая
качество
результатов[\[9\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=AlphaEvolve%20demonstrated%20strong%20closed,contributes%20to%20the%20observed%20efficiency).

## Ключевые нововведения для повышения эффективности

ShinkaEvolve достигает впечатляющей эффективности поиска за счёт трёх
основных алгоритмических инноваций:

1.  **Адаптивный выбор родителей** (баланс *exploration* vs
    *exploitation*): вместо случайного выбора или всегда сильнейшего
    решения, ShinkaEvolve использует умную стратегию отбора
    «родительских» программ для
    мутаций[\[10\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=1,yielding%20the%20biggest%20relative%20fitness).
    Популяция разделена на несколько **«островов»** (подпопуляций) для
    поддержания разнообразия, и родители выбираются с учётом как их
    качества (фитнеса), так и *новизны*. Реализованы политики выбора:
    например, **power-law (степенной закон)**, который чаще выбирает
    более успешные программы, но с элементом случайности, и
    **novelty-weighted** отбор, который даёт шанс менее похожим/более
    оригинальным
    решениям[\[10\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=1,yielding%20the%20biggest%20relative%20fitness).
    Это предотвращает преждевременную конвергенцию на одном решении и
    обеспечивает исследование пространства решений шире, чем простое
    жадное улучшение.

2.  **Отсеивание мутантов с низкой новизной** (*Novelty-based
    rejection*): система старается не тратить вычислительные ресурсы на
    повторную оценку программ, почти идентичных уже известным. Для
    каждого сгенерированного варианта вычисляется эмбеддинг кода; если
    косинусное сходство с каким-либо из уже испытанных решений выше
    заданного порога, этот мутант считается *неоригинальным* и
    отбрасывается ещё до
    запуска[\[11\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=weighted%20by%20performance%20and%20offspring,style%20update%20on%20improvement).
    Дополнительно вводится концепция LLM-«судьи новизны»: отдельная
    языковая модель может проанализировать изменения и оценить, несут ли
    они творческую ценность, прежде чем допустить программу к
    выполнению[\[11\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=weighted%20by%20performance%20and%20offspring,style%20update%20on%20improvement).
    Такой **отбор по новизне** существенно экономит попытки, фильтруя
    «микромутации» и тривиальные вариации известных идей.

3.  **Динамический ансамбль LLM с бандитным алгоритмом**: ShinkaEvolve
    умеет работать сразу с несколькими языковыми моделями и
    **автоматически учится выбирать наиболее полезную из них** по ходу
    эволюции[\[12\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=secondary%20LLM%20acts%20as%20a,style%20update%20on%20improvement).
    Используется подход многорукого бандита (алгоритм Upper Confidence
    Bound, UCB1): каждая модель (например, GPT-4, Gemini, Claude, или
    специализированные модели от DeepSeek) рассматривается как «рука
    бандита», и системе начисляется награда, если её мутации приводят к
    улучшению результата по сравнению с родителем. На основе этих данных
    ShinkaEvolve динамически перенаправляет больше запросов к тем
    моделям, которые дают наибольший прирост фитнеса, но при этом не
    забывает пробовать и другие (для сбалансированного
    исследования)[\[12\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=secondary%20LLM%20acts%20as%20a,style%20update%20on%20improvement).
    Этот механизм, по сути, позволяет системе **самой учиться**, какая
    LLM лучше подходит для текущей задачи, и повышать эффективность
    поиска за счёт использования сильнейших «советчиков» в ансамбле.

Совокупность этих трёх идей – продвинутый выбор родителей, фильтр
новизны и адаптивный выбор модели – даёт *синергетический эффект*. В
абляционных экспериментах было показано, что **каждый** из компонентов
заметно улучшает эффективность, а вместе они позволяют сокращать число
попыток на
порядки[\[13\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20Method%20Ablations%20on,contribute%20to%20ShinkaEvolve%27s%20sample%20efficiency)[\[14\]](https://sakana.ai/shinka-evolve/#:~:text=stepping%20stone%20collection%20dynamics%20of,contribute%20to%20ShinkaEvolve%27s%20sample%20efficiency).
В итоге ShinkaEvolve превращает эволюционный поиск из грубого перебора в
гораздо более **разумный и целенаправленный процесс**, не жертвуя при
этом его открытостью к неожиданных решениям.

## Процесс работы ShinkaEvolve: цикл эволюции программ

Основной цикл эволюции в ShinkaEvolve выглядит следующим образом:

- **Архив решений**: Система ведёт *архив* всех уже сгенерированных и
  оценённых программ, храня для каждой её код, полученные метрики
  (фитнес) и другую информацию (например, краткое текстовое
  описание/отзыв от
  модели)[\[15\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20maintains%20an%20archive%20of,prompts%20to%20accelerate%20later%20generations).
  Архив также разбит на несколько «островов», чтобы в нём поддерживалось
  разнообразие – разные острова могут фокусироваться на различных
  участках пространства решений.

- **Выбор родителя**: В начале каждого поколения ShinkaEvolve случайным
  образом выбирает один из островов, а затем из него – одну или
  нескольких *родительских*
  программ[\[15\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20maintains%20an%20archive%20of,prompts%20to%20accelerate%20later%20generations).
  Этот выбор не равновероятный: вероятность зависит от стратегии (как
  упоминалось, может учитываться фитнес, количество потомков уже от этой
  программы, новизна и т.п. для
  баланса)[\[10\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=1,yielding%20the%20biggest%20relative%20fitness).
  Если используется, например, стратегия *power-law*, то более успешные
  программы имеют больше шансов быть родителем, но не 100%, чтобы дать
  шанс и менее изученным
  решениям[\[10\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=1,yielding%20the%20biggest%20relative%20fitness).

- **Формирование контекста мутации**: Для выбранных родителей система
  формирует контекст, в который включаются лучшие найденные решения
  (топ-K из архива) и некоторые случайные «вдохновляющие» программы из
  архива[\[15\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20maintains%20an%20archive%20of,prompts%20to%20accelerate%20later%20generations).
  Этот контекст предоставляется LLM, чтобы она могла использовать
  **существующие хорошие идеи** при генерации изменений, но также
  увидеть различные альтернативы. Таким образом, LLM получает не пустой
  лист, а информацию о том, что уже пробовано и что сработало или нет.

- **Генерация новых программ (мутация/кроссовер)**: На основе контекста
  одна из языковых моделей ансамбля (выбранная по бандитной схеме)
  генерирует **предложение изменения программы**. ShinkaEvolve
  предусматривает три основных типа операций:

- *Diff-правка*: локальное редактирование кода родителя (патч), похожее
  на git-дифф. LLM предлагает точечные изменения внутри отмеченных
  секций кода.

- *Полный перезапись (rewrite)*: LLM может сгенерировать целиком новый
  вариант целевой функции или блока кода, заменив существующий
  (радикальная мутация).

- *Кроссовер*: комбинация частей двух разных программ. LLM может взять
  элементы одного решения и вставить в контекст другого, объединяя их
  идеи[\[16\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=parent,prompts%20to%20accelerate%20later%20generations).

Важная деталь: **в коде родителя помечаются специальные зоны, которые
можно менять** (например, комментариями
`EVOLVE-BLOCK-START/END`)[\[17\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60initial.py%60%20)[\[18\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,maximization).
LLM ограничена изменением только внутри этих областей, что защищает
остальную часть программы (например, неизменную инфраструктуру или
важные функции проверки) от случайного
нарушения[\[19\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=parent,The%20system%20periodically%20produces%20a).
Это обеспечивает корректность: эволюция влияет лишь на те части, где
содержится алгоритм решения, а не на код загрузки данных или формат
отчёта и т.д.

- **Предварительная проверка новизны**: Прежде чем действительно
  запускать новую программу, ShinkaEvolve применяет **фильтр новизны**.
  Сгенерированный код сравнивается с архивом: вычисляется эмбеддинг и
  ищется ближайшее
  сходство[\[11\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=weighted%20by%20performance%20and%20offspring,style%20update%20on%20improvement).
  Если новая программа слишком похожа на уже существующие (превышает
  порог схожести), она отбраковывается без выполнения, поскольку
  считается бессмысленно тратить на неё вычисления (скорее всего, её
  результат будет близок к уже известному). Также, если включён
  LLM-«новизны судья», его мнение может учесть творческую ценность
  изменений[\[11\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=weighted%20by%20performance%20and%20offspring,style%20update%20on%20improvement).
  Таким образом, к следующему шагу допускаются только действительно
  *новые и потенциально интересные* программы.

- **Выполнение и оценка**: Допущенная программа запускается в
  специальной среде оценки. Пользователь задачи предоставляет скрипт
  `evaluate.py`, который знает, как проверить решение на корректность и
  как вычислить **метрику качества
  (фитнес)**[\[20\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=To%20use%20EvolutionRunner%2C%20you%20need,improved%20by%20LLMs%20across%20generations).
  Например, в задачах оптимизации это может быть численный показатель
  (суммарный вес, точность, площадь и т.д.), в творческих задачах –
  какая-то совокупная метрика или оценка. Скрипт может выполнить
  программу несколько раз для усреднения результата или проведения
  разных тестов, и затем возвращает агрегированный **итоговый
  скор**[\[21\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=def%20main,evals%20to%20aggreg.%20get_experiment_kwargs%3Dget_kwargs%2C%20aggregate_metrics_fn%3Daggregate_fn)[\[22\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=return%20%7B).
  Кроме того, `evaluate.py` может возвращать **публичные метрики**
  (видимые Shinka для отбора) и **приватные** (скрытые, напр. для
  доп.проверки переобучения), а также текстовый отзыв или дополнительные
  данные[\[23\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=score%20%3D%20results,str%20fb).
  Формат результата оговаривается: обычно есть поле `combined_score`
  (которое Shinka старается **максимизировать** – т.е. больше =
  лучше)[\[24\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%2A%20Use%20%60EVOLVE,maximization).
  Если при запуске программа выдаёт ошибку или некорректный результат,
  это фиксируется как неудачная попытка.

- **Обновление архивов и статистики**: После оценки новый экземпляр
  программы с её результатами добавляется в архив. Если архив на острове
  переполнен, возможно, вытесняется худший или неинтересный экземпляр
  (архив ограничен по размеру). Также обновляются **статистики для
  бандитного выбора модели**: система смотрит, насколько улучшился (или
  ухудшился) фитнес относительно родителя и, например, относительно
  глобального базового уровня, и обновляет «очки» той LLM, которая
  предложила
  мутацию[\[12\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=secondary%20LLM%20acts%20as%20a,style%20update%20on%20improvement).
  Это повлияет на выбор модели в следующих поколениях (успешным моделям
  – больше веса).

- **Meta-LLM и накопление знаний**: Через определённые интервалы
  поколений ShinkaEvolve генерирует *мета-отчёт* о ходе поиска. Для
  этого задействуется отдельная LLM, которой предоставляется история
  недавних изменений, их результаты, **scratchpad** с инсайтами. Она
  формирует **резюме успешных стратегий и рекомендации**, которые
  сохраняются и могут быть добавлены к подсказкам для следующих
  мутаций[\[25\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20generates%20a%20search,humans%20in%20achieving%20further%20improvements).
  Идея в том, чтобы система могла извлекать обобщённые уроки: например,
  заметить, что «рандомизация параметра X помогла выйти из локального
  оптимума» или «комбинация метода A и B дала прирост» – и направить
  дальнейшую эволюцию с учётом этих наблюдений. Такой мета-подход
  ускоряет поиск на поздних стадиях и также может помочь
  человеку-исследователю понять, что нашёл
  ИИ[\[26\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20generates%20a%20search,humans%20in%20achieving%20further%20improvements).

- **Следующее поколение**: Цикл повторяется – выбор новых родителей
  (возможно, с других островов), мутация, оценка, … – пока не будет
  достигнут заданный критерий остановки (например, определённое число
  поколений или удовлетворяющее значение метрики). В процессе система
  строит **генеалогическое дерево программ** с отмеченными улучшениями.
  Пользователь может наблюдать за ходом эксперимента через
  **веб-интерфейс**: ShinkaEvolve предоставляет интерактивный WebUI, где
  в реальном времени визуализируется эволюционный процесс, деревья
  решений и метрики
  поколений[\[27\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=Interactive%20WebUI).
  Это удобно для мониторинга и анализа экспериментов.

**Схема работы ShinkaEvolve:** на высоком уровне, система поддерживает
архив оценённых программ, генерирует новые программы с помощью ансамбля
LLM и оценивает их “фитнес” на задаче. Цикл повторяется многократно,
постепенно **эволюционно улучшая** решения
задачи[\[8\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20High,programs%2C%20and%20evaluates%20their%20fitness).
(На диаграмме показаны блоки: архив решений, выбор родителя, генерация
потомков LLM-моделями, проверка новизны, запуск и оценка, обновление
архива и мета-анализа.)

## Примеры применений и достижения ShinkaEvolve

Авторы ShinkaEvolve продемонстрировали её возможности на **четырёх
различных доменах**, что подчёркивает общность и гибкость
подхода[\[28\]](https://sakana.ai/shinka-evolve/#:~:text=The%20Japanese%20word%20%E2%80%98Shinka%E2%80%99%20,its%20power%2C%20generality%2C%20and%20efficiency):

- **1. Математическая оптимизация: задача упаковки окружностей.**
  Классическая задача – упаковать 26 окружностей внутри единичного
  квадрата с максимально возможным минимальным радиусом (чем больше
  радиус – тем плотнее упаковка). Предыдущие эволюционные системы
  (включая AlphaEvolve) нашли одно из лучших известных решений, но ценой
  тысяч запусков алгоритма. ShinkaEvolve же *открыла новое состояние
  искусства* для этой задачи, достигнув рекордной конфигурации радиусов
  примерно за **150
  поколений**[\[29\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=number%20of%20evaluations%20needed%20to,research%20report%20and%20public%20code)[\[4\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=,10%20tasks%20and%20pushes%20one).
  Это огромный скачок в эффективности. Более того, найденный Shinka
  алгоритм не был заранее заложен людьми – система самостоятельно
  скомбинировала несколько идей: **спиральная инициализация по золотому
  углу**, градиентный локальный поиск для уточнения расположения и
  элемент *симулированного отжига* (вероятностные перестановки) для
  выхода из локальных
  оптимумов[\[30\]](https://sakana.ai/shinka-evolve/#:~:text=ShinkaEvolve%20discovered%20a%20new%20state,annealing%20to%20escape%20local%20optima)[\[31\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=,that%20push%20scores).
  В результате удалось обойти предыдущее решение AlphaEvolve по
  плотности упаковки, причём с минимальными вычислительными
  затратами[\[32\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20Circle%20Packing%3A%20ShinkaEvolve%27s%20discovered,solution%20in%20only%20150%20generations)[\[33\]](https://sakana.ai/shinka-evolve/#:~:text=match%20at%20L72%20Circle%20Packing%3A,solution%20in%20only%20150%20generations).
  На графике из статьи показано дерево эволюции: ShinkaEvolve нашла
  сложное гибридное решение, которое человек не программировал
  явно[\[34\]](https://sakana.ai/shinka-evolve/#:~:text=26,annealing%20to%20escape%20local%20optima).

- **2. Проектирование агентной системы: математические рассуждения
  (AIME).** Ещё один эксперимент – использовать ShinkaEvolve для
  **автоматического конструирования архитектуры агента**, способного
  решать сложные математические задачи (конкурсные задачи AIME, American
  Invitational Mathematics Examination). Здесь «программой» выступала не
  конкретная формула, а **сценарий работы многоэтапного агентного
  метода**: какие роли LLM выполняет, как взаимодействуют шаги решения.
  ShinkaEvolve за ~75 поколений эволюции разработала **эффективный
  трёхэтапный конвейер** решения
  задач[\[35\]](https://sakana.ai/shinka-evolve/#:~:text=We%20tasked%20ShinkaEvolve%20with%20designing,and%20even%20different%20underlying%20LLMs).
  В этой эволюционировавшей схеме:

- Генерацию решения осуществляют несколько *экспертов-персон* (разные
  стилевые LLM-подходы к задаче).

- Затем ответы проходят через стадию *критического peer-review* – другой
  агент анализирует и выискивает ошибки или улучшает решения.

- Наконец, *синтезирующий* этап объединяет и формирует окончательный
  ответ.

Такой ансамблевый подход, включающий **разнообразие экспертов,
критический анализ и итоговый синтез**, оказался чрезвычайно
результативным[\[36\]](https://sakana.ai/shinka-evolve/#:~:text=We%20tasked%20ShinkaEvolve%20with%20designing,and%20even%20different%20underlying%20LLMs).
На датасете AIME-2024 полученная архитектура превзошла сильные
рукотворные базовые методы по точности решения, причём особенно в режиме
ограниченного бюджета запросов к LLM (т.е. достигла *лучшего
компромисса* точность vs число вызовов
модели)[\[37\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=mechanisms%20,batch)[\[5\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20is%20an%20Apache,Code%20and%20report%20are%20public).
Интересно, что найденный шаблон решения **оказался устойчивым**: его
можно применять к задачам других лет AIME и даже заменять используемую
LLM на другую – структура метода по-прежнему даёт прирост
результатов[\[38\]](https://sakana.ai/shinka-evolve/#:~:text=peer%20review%2C%20and%20a%20final,and%20even%20different%20underlying%20LLMs)[\[39\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=hand,batch).
Это говорит о том, что ShinkaEvolve открыла обобщённый принцип решения
(разбиение на роли и проверку), который не привязан к конкретным данным
или модели.

- **3. Соревновательное программирование: оптимизация решений
  ALE-Bench.** В этой демонстрации ShinkaEvolve выступала в роли
  «другого уровня» оптимизатора для уже неплохих решений. Взят агент
  ALE-Agent – передовой на тот момент алгоритм, участвовавший в
  соревнованиях AtCoder по эвристическому решению NP-трудных задач
  (ALE-Бенчмарк включает 10 задач
  оптимизации)[\[40\]](https://sakana.ai/shinka-evolve/#:~:text=We%20took%20the%20best%20solutions,novel%20%E2%80%9Ctargeted%20edge%20move%E2%80%9D%20operators).
  Этот агент уже выдавал приличные решения, но авторы хотели проверить,
  сможет ли Shinka *ещё улучшить* их. ShinkaEvolve получила на вход код
  решений ALE-Agent для каждой задачи и сгенерировала его мутации с
  целью улучшить итоговый **скор (очки)**, рассчитываемый по правилам
  конкурса. Результат: в среднем по 10 задачам удалось повысить качество
  решений ~на **2.3%** относительно исходных (публичного лучшего
  результата
  агента)[\[41\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20Competitive%20Programming%3A%20ShinkaEvolve%20improves,for%20AtCoder%20heuristic%20programming%20competitions).
  На одной из задач ShinkaEvolve настолько продвинула решение, что если
  бы этот улучшенный код участвовал в конкурсе, он бы занял *2-е место*
  вместо 5-го, где изначально был
  ALE-Agent[\[42\]](https://sakana.ai/shinka-evolve/#:~:text=successfully%20found%20improvements%20across%20multiple,novel%20%E2%80%9Ctargeted%20edge%20move%E2%80%9D%20operators)[\[43\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=baselines%20under%20limited%20query%20budgets,batch%20LBL).
  Примечательно, что улучшения не сводились к полной перестройке
  алгоритмов – скорее Shinka предложила **точечные оптимизации**:
  например, более продвинутый кэширование промежуточных вычислений
  (использование k-d дерева для хранения частичных решений), или новый
  оператор мутации графового решения (*«прицельное перемещение ребра»*),
  позволивший исправлять ранее неизменяемые
  конфликты[\[44\]](https://sakana.ai/shinka-evolve/#:~:text=performance%20of%20the%20agent,novel%20%E2%80%9Ctargeted%20edge%20move%E2%80%9D%20operators)[\[45\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=retaining%20robustness%20when%20swapped%20to,perplexity%2Fbenchmarks%20as%20layer%20routing%20concentrates).
  Эти идеи были неочевидны авторам ALE-Agent, но оказались совместимы с
  его кодом и улучшили результат без переобучения на тестовых данных
  (переоснащение на публичных случаях было
  минимальным)[\[46\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20On%20average%20the%20performance,to%20the%20public%20test%20cases)[\[45\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=retaining%20robustness%20when%20swapped%20to,perplexity%2Fbenchmarks%20as%20layer%20routing%20concentrates).

- **4. Проектирование обучения LLM: функция потерь для
  Mixture-of-Experts.** Четвёртый сценарий сильно отличается от первых
  трёх – здесь ShinkaEvolve применили для **оптимизации части процесса
  обучения больших моделей**. Задача: найти лучшую функцию потерь
  (loss), которая балансирует загрузку экспертов в модели-«миксе
  экспертов» (MoE), чем существующая на тот момент лучшая ручная
  разработка (Global Load Balancing Loss, предложенная командой
  DeepSeek)[\[47\]](https://sakana.ai/shinka-evolve/#:~:text=In%20a%20domain%20very%20relevant,future%20generations%20of%20AI%20models).
  Эволюция происходила не на самих весах модели (они обучаются обычным
  способом), а на выражении для дополнительного слагаемого loss, которое
  штрафует дисбаланс в активации экспертов. ShinkaEvolve всего за ~30
  поколений вывела новую формулу **Adaptive LBL**, которая *превзошла*
  state-of-the-art Global LBL по нескольким
  показателям[\[48\]](https://sakana.ai/shinka-evolve/#:~:text=load%20balancing%20loss%20,generations%20of%20AI%20models%20themselves).
  Новый loss динамически добавляет энтропийный штраф за
  недоиспользование некоторых экспертов (если некоторые эксперты
  практически не получали токенов, система их дополнительно мотивирует
  задействоваться)[\[49\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=,perplexity%2Fbenchmarks%20as%20layer%20routing%20concentrates).
  В результате при тренировке крупных MoE-моделей наблюдается:

- *Снижение* неэффективной маршрутизации токенов на ~5.8% (меньше
  ситуаций, где один эксперт перегружен, а другие простаивают).

- *Рост* среднего качества на задачах (перплексия по языковым данным и
  точность по downstream-бенчмаркам улучшились ~на
  1.7%)[\[50\]](https://sakana.ai/shinka-evolve/#:~:text=outperformed%20the%20state,generations%20of%20AI%20models%20themselves)[\[51\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=,perplexity%2Fbenchmarks%20as%20layer%20routing%20concentrates).

Важно, что найденное решение **обобщилось**: его эффект подтверждён на
семи разных тестовых наборах и на более крупных моделях с в 5 раз
большим числом активных
экспертов[\[52\]](https://sakana.ai/shinka-evolve/#:~:text=After%20only%2030%20ShinkaEvolve%20generations%2C,generations%20of%20AI%20models%20themselves).
Для области обучения LLM это значимый результат, поскольку любые
улучшения в процессе обучения, дающие даже проценты прироста, очень
ценны (учитывая огромные затраты). ShinkaEvolve показала, что может
помочь и в «саморефлексии» ИИ – улучшении самого процесса создания
будущих поколений моделей.

Все эти примеры показывают, что ShinkaEvolve – по-настоящему **общая
платформа** для поиска решений. Она не заточена под одну узкую задачу: с
равным успехом была применена и в комбинаторной оптимизации, и в
мета-обучении, и в создании агентных пайплайнов, и в настройке
алгоритмов обучения. Везде отмечается существенный прирост эффективности
по сравнению с ручными или предшествующими решениями, что подтверждает
ценность введённых методик (новый отбор, фильтрация,
ансамбль)[\[5\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20is%20an%20Apache,Code%20and%20report%20are%20public).

## Технические детали и алгоритмические особенности

Рассмотрим некоторые детали реализации ShinkaEvolve и то, как они
связаны с вышеописанными идеями:

- **Островная модель и отбор родителей:** В конфигурации по умолчанию
  ShinkaEvolve создает несколько параллельных *островов* (например, 4),
  каждые из которых эволюционирует свою популяцию
  программ[\[53\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,Sharpness%20of%20sigmoid%20for%20weighted).
  Периодически между островами происходят *миграции* – обмен лучшими
  особями, чтобы удачные решения могли распространяться, но
  контролируемо (сохраняя
  разнообразие)[\[53\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,Sharpness%20of%20sigmoid%20for%20weighted).
  Отбор родителя на одном острове настроен по стратегии **power_law** с
  параметрами: вероятность выбора пропорциональна
  \$(\text{фитнес})^\alpha\$ (где \$\alpha=1.0\$ по умолчанию – то есть
  линейная по фитнесу) и при этом всегда есть шанс выбрать решение не из
  топа благодаря случайности (exploitation_ratio
  ~0.2)[\[54\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,beams%20for%20beam%20search%20selection).
  Также поддерживаются режимы **weighted** (взвешенное случайное по
  фитнесу) и **beam_search** (просмотр нескольких
  кандидатов)[\[54\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,beams%20for%20beam%20search%20selection).
  Такой гибкий выбор обеспечивает, что система **и** использует
  накопленные хорошие решения, **и** время от времени пробует варианты с
  более низким фитнесом, если они могут внести новизну. Кроме того, за
  счёт островов ShinkaEvolve может одновременно исследовать несколько
  участков пространства решений (каждый остров – свое направление
  поиска), что повышает шанс избежать локальных максимумов.

- **Novelty-регуляция и отсеивание дубликатов:** Как отмечалось, перед
  запуском программы выполняется проверка на новизну. Для этого
  ShinkaEvolve может использовать комбинацию методов: 1) *Embedding
  similarity* – код программы (или его изменяемой части) прогоняется
  через модель эмбеддинга (например, модель для кодовых текстов) и
  сравнивается косинусное сходство с эмбеддингами программ в
  архиве[\[11\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=weighted%20by%20performance%20and%20offspring,style%20update%20on%20improvement).
  Если сходство слишком высоко (\> порога, по умолчанию 1.0 что означает
  фактически идентичность, но на практике
  настраивается)[\[55\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=if%20None%29%20,use%20text%20feedback%20in%20evolution),
  программа признаётся **слишком похожей** на уже виденное. 2) *LLM
  novelty judge* – ShinkaEvolve может вызвать отдельную LLM, дав ей
  старую и новую версии кода, и попросить оценить, насколько новая идея
  отличается от
  известных[\[11\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=weighted%20by%20performance%20and%20offspring,style%20update%20on%20improvement).
  Например, модель может ответить, что изменение тривиально (просто
  перемена переменных местами) или, наоборот, содержит принципиально
  иной подход. Такой экспертный фильтр сложнее, но помогает отсеять
  случаи, когда формально код отличается, а по сути – нет (LLM поймёт
  семантическую разницу).

Эти механизмы работают в паре: сначала отсеиваются явные дубли на уровне
текста/эмбеддинга, потом оценивается творческая ценность. **Результат –
экономия вычислений**: тысячи потенциально бесполезных запусков просто
не происходят, ShinkaEvolve фокусируется на реально новых мутациях.
Авторы показывают, что без novelty-фильтра эволюция протекает намного
медленнее – модель тратит время на повторение уже пройденных
шагов[\[13\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20Method%20Ablations%20on,contribute%20to%20ShinkaEvolve%27s%20sample%20efficiency).

- **Ансамбль моделей и бандитная оптимизация:** В ShinkaEvolve
  пользователь может указать список языковых моделей, доступных для
  генерации кода (`llm_models`), например
  `["azure-gpt-4.1-mini", "claude2", "gemini-2.5"]` и
  т.д.[\[56\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,recommendations).
  Если включена опция `llm_dynamic_selection`, то используется бандитный
  алгоритм – изначально обращения равномерно распределяются, затем по
  мере появления результатов обновляется рейтинг моделей. Реализация
  основана на классическом **UCB1**: выбирается модель, максимизирующая
  \$Q_j + c\sqrt{\frac{\ln N}{n_j}}\$, где \$Q_j\$ – текущая средняя
  *польза* от модели \$j\$ (например, среднее улучшение фитнеса потомков
  этой моделью над родителями), \$N\$ – общее число запросов, \$n_j\$ –
  число запросов к модели \$j\$, \$c\$ – параметр
  разведки[\[12\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=secondary%20LLM%20acts%20as%20a,style%20update%20on%20improvement).
  Таким образом, если одна модель (скажем, GPT-4) стабильно даёт большие
  приросты, её \$Q\$ растёт и её будут выбирать чаще, но даже менее
  успешные модели периодически будут пробоваться, особенно если они мало
  вызывались (исследовать вдруг упустили потенциал). Такой подход
  позволил ShinkaEvolve **эффективно комбинировать сильные стороны
  разных LLM**. Например, отмечалось, что у DeepMind AlphaEvolve
  использовались две модели Gemini – быстрая (для широкой генерации
  идей) и мощная (для глубоких
  улучшений)[\[57\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L470%20AlphaEvolve%20leverages,Together%2C%20these%20models%20propose).
  ShinkaEvolve даёт аналогичный эффект автоматически: быстрые модели
  могут генерировать больше вариантов, а топ-модели – точечно улучшать
  сложные фрагменты, причём система *сама учится*, как их лучше
  чередовать.

- **Операторы мутации (diff, full, crossover):** В течение одного
  поколения ShinkaEvolve может сгенерировать несколько кандидатов
  (обычно от каждого родителя можно получить несколько потомков). Тип
  генерируемого изменения выбирается случайно согласно заданным
  вероятностям (`patch_types` и `patch_type_probs` в
  конфиге)[\[58\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60task_sys_msg%60%20%60None%60%20%60Optional,a%20patch%20if%20it%20fails).
  По умолчанию основной тип – **diff-патчи**, так как они чаще приводят
  к валидному коду, сохраняя общую структуру. Но время от времени
  система пробует **full rewrite** (полностью переписать функцию) или
  **cross** (перекомбинация двух
  решений)[\[58\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60task_sys_msg%60%20%60None%60%20%60Optional,a%20patch%20if%20it%20fails).
  *Кроссовер* особенно полезен при наличии нескольких островов – можно
  взять сильные части из решений с разных островов и объединить. Все
  изменения ограничены *языком программирования*, указанным в конфиге
  (`language: "python"` по
  умолчанию)[\[59\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60job_type%60%20%60,Kwargs%20for%20dynamic%20selection),
  – сейчас ShinkaEvolve ориентирована в основном на Python-код, но в
  принципе поддерживает и другие языки. В процессе генерации LLM
  снабжается промптом, где описывается задача (system message содержит
  описание оптимизируемой цели), показан текущий код и, возможно,
  примеры патчей. Также указываются специальные маркеры, например *не
  изменять* код вне блоков
  `EVOLVE-BLOCK`[\[18\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,maximization),
  и формат ответа (например, если diff – то требуются участки кода в
  определённом виде). Благодаря этому LLM-генерации довольно точно
  встраиваются в существующий код, минимизируя синтаксические ошибки.
  Если модель всё же вернула некорректный или пустой патч, ShinkaEvolve
  попробует сгенерировать снова (до `max_patch_attempts`
  раз)[\[60\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=task%20%60patch_types%60%20%60%5B,slurm_docker)
  или возьмёт другой тип патча.

- **Оценка, скрипты и метрики:** Пользователь, решающий конкретную
  задачу с ShinkaEvolve, готовит два основных файла:

- `initial.py` – начальная реализация решения. Она задаёт исходную
  точку, от которой будет идти эволюция. Внутри него выделяется функция
  или блок, помеченный для эволюции (например, в комментариях), – именно
  её код будет менять
  LLM[\[17\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60initial.py%60%20).
  Также `initial.py` должен содержать функцию
  `run_experiment(**kwargs)`, которую будет вызывать оценщик, и любую
  необходимую логику запуска
  решения[\[17\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60initial.py%60%20).

- `evaluate.py` – скрипт оценки. Он может использовать готовую
  функцию-утилиту
  `run_shinka_eval`[\[61\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60evaluate.py%60%20),
  которая автоматизирует многократный запуск решения и сбор результатов.
  В этом скрипте определяются:
  - функция `get_kwargs(run_idx)` – возвращает параметры (например,
    случайный seed, или разные тестовые случаи) для каждого из
    нескольких запусков, если нужна
    агрегация[\[62\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=);
  - функция `aggregate_fn(results)` – сводит список результатов в
    итоговые метрики (например, усредняет счёт) и формирует словарь с
    ключами `combined_score`, `public`, `private`, `text_feedback` и
    пр.[\[22\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=return%20%7B);
  - опционально `validate_fn` – для проверки корректности результатов.

При запуске программы ShinkaEvolve передаёт пути к сгенерированному коду
и папке для результатов в `evaluate.py`. Скрипт выполняется либо
локально, либо на кластере (Shinka имеет конфиги для локального или
SLURM-запуска с Docker/Conda
окружениями[\[63\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=LocalJobConfig%20)[\[64\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=SlurmCondaJobConfig%20)).
Это даёт гибкость: можно эволюционировать как простые функции на CPU,
так и запускать, например, обучение нейросети на GPU в каждом поколении
(было бы достаточно ресурсов). В конечном счёте `evaluate.py` должен
вернуть числовой показатель – **чем он выше, тем лучше решение**.
ShinkaEvolve всегда *максимизирует*
`combined_score`[\[65\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%2A%20Auto,maximization)
(если задача минимизации, пользователь может просто инвертировать
метрику). Такой чёткий сигнал позволяет сопоставлять программы по
качеству и выбирать элиту для следующего поколения.

- **Метапамять и выводы LLM:** Как упоминалось, ShinkaEvolve генерирует
  *search summary document* – по сути, отчёт об открытых «инсайтах» во
  время
  эволюции[\[26\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20generates%20a%20search,humans%20in%20achieving%20further%20improvements).
  Это уникальная особенность, превращающая систему в своего рода
  **ассистента исследователя**. В этом документе (который можно
  просмотреть через WebUI) перечисляются: краткие описания предыдущих
  предложений кода, какие идеи были опробованы, что из них сработало или
  нет, и рекомендации, что попробовать
  дальше[\[25\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20generates%20a%20search,humans%20in%20achieving%20further%20improvements).
  Например, там может быть запись: «последние успешные программы
  применяли алгоритм X; можно попробовать комбинировать X с подходом Y
  для дальнейшего улучшения». Эти сведения затем могут быть *включены в
  промпт* следующих поколений (ShinkaEvolve поддерживает настройку
  интервала генерации мета-рекомендаций `meta_rec_interval` и
  использование отдельной модели или той же для их
  формирования[\[66\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=selection%20strategy%20%60llm_dynamic_selection_kwargs%60%20%60,str%5D%60%20Model%20for%20code%20embeddings)).
  Таким образом, со временем LLM начинает работать не вслепую, а
  основываясь на накопленных знаниях. Фактически, ShinkaEvolve реализует
  идею, что **LLM может не только генерировать решения, но и
  анализировать собственный поиск**, делая каждый следующий шаг умнее
  предыдущего.

- **Параллелизм и визуализация:** Для практического использования важно,
  что ShinkaEvolve **поддерживает параллельное выполнение**. В
  конфигурации можно задать `max_parallel_jobs` – например, запускать
  сразу 4 или 8 кандидатов в разных
  процессах[\[67\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,LLM%20models%20for%20code%20generation).
  На кластерах SLURM можно в каждой задаче запрашивать нужное число
  CPU/GPU и Shinka сама отправит
  задания[\[68\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=SlurmDockerJobConfig%20)[\[69\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60mem%60%20%60,request).
  Благодаря этому, хотя эволюция итеративна, поколение не обязательно =
  1 запуск, можно существенно ускорить перебор. Web-интерфейс Shinka
  (`shinka_visualize`) позволяет отслеживать, как **в реальном времени**
  растут показатели, какие изменения были внесены, как связаны поколения
  (генеалогическое
  дерево)[\[27\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=Interactive%20WebUI).
  Это делает использование системы прозрачным: исследователь может
  понять, почему тот или иной вариант считается хорошим, и какие
  направления пробовались. Вдобавок, Shinka хранит все результаты и
  артефакты (например, можно получить логи запуска каждой программы,
  дополнительные данные `extra_data` из evaluate), что важно для
  воспроизводимости научных результатов.

## Адаптация ShinkaEvolve для творческих и сложных задач

ShinkaEvolve разрабатывалась с прицелом на научные и инженерные задачи,
где есть явная метрика качества. Однако её подход применим и к более
**креативным сценариям**, если суметь сформулировать критерии оценки.
Пользователь запроса интересуется адаптацией Shinka для создания новых
агентов, творчества (видео, изображения, сценарии), генерации кода под
реальные приложения, поддержки глубоких исследований и написания
отчётов/ТЗ. Рассмотрим, как можно использовать принципы ShinkaEvolve в
этих областях:

- **Расширение на генерацию искусства и медиа:** Творческие задачи –
  генерация изображений, видео, музыки – сложно формализовать единой
  численной метрикой «красоты» или «качества». Однако ShinkaEvolve можно
  приспособить, если задать прокси-метрики или комбинированные критерии.
  В самом репозитории есть пример под названием **Novelty Generator**,
  где цель – получать *неожиданные/оригинальные выходы*, например
  ASCII-арт[\[70\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%E2%AD%95%20Circle%20Packing%20%20Optimize,LocalJobConfig).
  Там, очевидно, в качестве фитнеса выступает некий показатель новизны
  или удивительности результата. Подобно этому, для изображений можно
  использовать:
- Предобученные модели оценки (например, **CLIP** или специальные модели
  эстетической оценки) – они могут выдавать балл, насколько изображение
  соответствует задуманной концепции или насколько оно визуально
  привлекательно.
- Меры разнообразия – например, по эмбеддингам изображений измерять,
  насколько новое изображение отличается от ранее сгенерированных,
  поощряя оригинальность.
- Человеческие предпочтения – в некоторой степени можно привлечь
  человека для оценки или имитировать их моделью.

Тогда **процесс эволюции** может выглядеть так: программа, которую
эволюционирует Shinka, – это, скажем, *набор инструкций или промптов
генеративной модели*. Например, для видео это последовательность
текстовых подсказок для модели генерирования видео (такие как Gen-2),
или даже небольшой скрипт, который компонует несколько моделей (одна
генерирует фон, другая персонажей, потом накладывает). Shinka могла бы
мутировать эти инструкции, постепенно улучшая, скажем, *сюжетность
видео, визуальное качество кадров или соответствие заданной теме*.
Каждый вариант прогоняется через генеративную модель, результат
оценивается скриптом: вычисляются метрики плавности видео, соответствие
желаемому контенту (через распознавание), оценка зрелищности (через ту
же CLIP или LLM-оценку описания видео) и т.п. – и агрегируется в фитнес.
Конечно, такая оценка будет лишь приближением к человеческому вкусу, но
уже сейчас известны модели, достаточно хорошо коррелирующие с
восприятием. Важное, что ShinkaEvolve **не зависит от типа контента** –
для неё видео или картинка ничем не отличаются от числа, если есть
функция, выдающая «сколько это видео хорошее». В перспективе, возможно,
сам ShinkaEvolve сможет генерировать и собственные критерии оценки
творческих работ (об этом ниже, в плане
самообучения)[\[71\]](https://sakana.ai/shinka-evolve/#:~:text=releases%20such%20as%20GPT,1).

- **Генерация сценариев и историй (LLM-контент):** Создание сценариев
  (например, диалогов, историй, игровых ситуаций) – тоже творческая
  задача, но здесь на помощь могут прийти сами языковые модели как часть
  цикла. Представим, что нужно сгенерировать **сюжет для игры или
  сценарий**. Можно оформить это как оптимизационную задачу:
- Программа-кандидат – это текст сценария или скрипт действий.
- Оценка – комбинация критериев: логичность развития сюжета,
  оригинальность, соответствие некоторым вводным требованиям (жанр,
  наличие определённых событий).

Как оценить *сюжет автоматически*? Один путь – использовать **другую LLM
как судью**. Уже сегодня практикуется, что ChatGPT или аналог оценивают
тексты по ряду свойств, ставят оценки по шкале. Например, можно
попросить модель: «Оцени этот сценарий по 10-балльной шкале по следующим
критериям: креативность, coherence, эмоциональный отклик». Эти оценки и
будут фитнесом (или свёрткой). Такой подход не идеален (LLM-судья
субъективна и может быть обманута), но в отсутстви объективной метрики
это рабочий вариант. Другой путь – задать *формальные ограничения*:
например, сценарий должен содержать минимум X реплик, 3 поворотных
момента, 5 именованных персонажей – их легко проверить, чтобы отсеивать
тривиальные решения.

ShinkaEvolve могла бы **эволюционировать сценарий** следующим образом:
начальный сценарий может быть пустым или простым (например, шаблон с
завязкой). LLM-мутатор предлагает изменения: добавить новый диалог,
изменить концовку, ввести нового персонажа. Оценка (LLM-критик или
скрипт) возвращает баллы. За несколько поколений, особенно если
использовать несколько различных «критиков» (ансамбль мнений или бандит
для критиков), можно получить весьма интересные сюжеты. Фактически, это
похожий процесс на эволюцию кода, только вместо правильности программы
мы оптимизируем «интересность» текста. Кстати, похожие эксперименты были
в научной среде: алгоритмы эволюционного творчества, эволюция рассказов
и т.п., но с приходом LLM такая система становится значительно умнее,
потому что LLM может делать осмысленные крупные правки, а не случайно
менять буквы.

- **Генерация кода и агентов для приложений (AutoGPT-подобные
  сценарии):** ShinkaEvolve уже доказала пользу на примере
  соревновательного программирования. Если ставится цель **автоматически
  создавать приложения или модули**, подход может быть таким:
- Разбить задачу на подзадачи, которые можно оценить автоматически.
  Например, генерация веб-приложения: можно иметь тесты для бэкенда (API
  должен возвращать правильные ответы), метрики производительности
  (время отклика), оценки UI (например, сравнить DOM с эталоном дизайна)
  и т.д. Тогда эволюция может происходить на уровне отдельных модулей.
- Либо же можно попытаться эволюционировать *пошаговый план разработки*.
  Например, агент-программист, который сам решает в каком порядке писать
  код, какие библиотеки подключать. Здесь *программа* – это сценарий
  действий агента (например, последовательность команд: «сгенерируй
  компонент X, протестируй, исправь ошибку Y…»). Фитнесом может быть
  успех в достижении конечной цели (приложение проходит интеграционные
  тесты). Это ближе к области автоагентов (AutoGPT, GPT-Engineer), но
  ShinkaEvolve может придать им структурированность через эволюционный
  поиск лучшего плана действий.

Уже сейчас известно, что LLM неплохо справляются с написанием небольших
программ по описанию. Но для **сложных проектов** (множество файлов,
интеграция систем) однократного прохода недостаточно – нужен итеративный
подход. ShinkaEvolve может стать таким итеративным механизмом: агент
пишет код → оценивается (тесты, метрики) → агент изменяется.
Представьте, например, эволюцию Git-репозитория: LLM предлагает
*коммит-патч* (набор изменений в нескольких файлах) с целью улучшить
совокупный показатель (тесты+скорость+стиль кода). Затем эти изменения
проверяются. Этот процесс повторяется, постепенно рождая всё более
совершенную кодовую базу. В принципе, ShinkaEvolve с diff-мутациями и
задумана для подобного – она гарантирует, что **каждое изменение валидно
синтаксически** и (в идеале) не ломает уже пройденные тесты, если ломает
– фитнес упадёт.

Конечно, для реальных приложений метрик может быть много, и они иногда
противоречат друг другу (например, добавление фичи может замедлить
программу). Но ShinkaEvolve может оптимизировать и в многокритериальной
постановке: авторы показывали, что в задаче AIME получилась
*Pareto-фронтир* решений с разным балансом точность/количество
запросов[\[72\]](https://sakana.ai/shinka-evolve/#:~:text=AIME%20Agent%20Scaffold%20Design%3A%20Evolving,the%20number%20of%20LLM%20queries).
Аналогично, можно собирать Pareto-фронт по критериям «функциональность
vs производительность vs простота кода» и предоставлять пользователю
выбор компромиса. Эволюционные алгоритмы хорошо подходят для таких
задач, т.к. поддерживают **диверсификацию решений** вместо единственного
ответа. Таким образом, агент-программист, обученный Shinka, мог бы
предлагать несколько вариантов архитектур приложения, и все будут
работоспособны, но с разными плюсами.

- **Агенты для глубокого ресёрча и написания отчётов:** Создание
  развернутых текстов (статей, технических заданий) – задача, требующая
  анализа информации, планирования структуры, ясности изложения. Чтобы
  применить ShinkaEvolve, можно попробовать **эволюционировать сам
  процесс написания**:
- Допустим, у нас есть некоторая исходная заготовка (например, короткий
  план отчёта или список ключевых вопросов). Это будет «начальной
  программой».
- Агент для написания отчёта можно представить как последовательность
  действий: (1) сбор информации (поиск источников, чтение), (2)
  составление плана, (3) написание черновика, (4) проверка фактов и
  улучшение текста. У разных стратегий разные результаты: один агент
  может писать быстро, но поверхностно, другой – глубоко исследует, но
  долго.

**Фитнес-функция** для отчёта может быть сложной комбинацией: - Проверка
фактов: встроить модуль, который выявляет противоречия или
несоответствия источникам (например, с помощью LLM-вопросов по
тексту). - Стилевые и языковые метрики: есть модели, оценивающие
связность текста, грамотность, соответствие заданному тону. - Полнота:
сравнить ключевые слова отчёта с требуемыми (например, вычислить
покрытие заданных тем).

Ещё вариант – *оценка другим LLM*: например, запросить у ChatGPT
рецензию на сгенерированный отчёт по критериям «полнота, точность,
читабельность» и преобразовать её в числовые оценки.

Теперь ShinkaEvolve может **мутировать агента-автора**. Это похоже на
пример с AIME, где мутировалась архитектура решения задачи. Здесь
мутировать можно последовательность шагов агента: например, добавить
этап «спроси эксперта-модель по узкому вопросу», или изменить порядок –
сначала сгенерировать черновик, потом искать источники для проверки (или
наоборот). LLM в роли «мутагена» будет предлагать новые скрипты
поведения: фактически, писать код агента (возможно, на каком-то языке
автоматизации, или псевдокод). Выполняя такого агента, мы получим
конечный текст отчёта, который и оцениваем. Через поколения агент может
научиться находить оптимальный баланс между временем на исследование и
качеством текста.

Это, конечно, сложная задача, но **принцип самообучения** в том и
состоит, чтобы агент сам улучшал свои методы. Уже сейчас есть работы,
где LLM самокорректируется, просит у себя улучшений – но Shinka придаст
этому **структуру эволюционного поиска**: будут одновременно пробоваться
разные подходы к написанию и выживать лучшие. Интересно, что Sakana AI
также разрабатывает тему *самоулучшающихся агентов*: так, их работа
**Darwin Gödel Machine (DGM)** как раз описывает агента, который сам
переписывает свой код, чтобы лучше решать задачи
программирования[\[73\]](https://arxiv.org/abs/2505.22954#:~:text=beneficial%20is%20impossible%20in%20practice,paths%20through%20the%20search%20space).
Там продемонстрировано, что агент со временем улучшил свои способности
(например, научился лучше использовать инструменты разработки,
удерживать больше контекста), повысив результат на кодовых бенчмарках с
20% до 50%
самостоятельно[\[74\]](https://arxiv.org/abs/2505.22954#:~:text=Empirically%2C%20the%20DGM%20automatically%20improves,that%20unfold%20into%20endless%20innovation).
В контексте написания текстов – это аналогично, агент бы учился все
лучше писать тексты. ShinkaEvolve может послужить основой для такого
**самообучающегося писателя**.

- **Самообучаемость и открытость критериев:** В особенно творческих или
  плохо определённых задачах может возникнуть ситуация: мы не знаем,
  *что именно* оптимизировать. Авторы ShinkaEvolve осознают это и
  упоминают видение на будущее – **выход за пределы человечески
  определённых
  метрик**[\[71\]](https://sakana.ai/shinka-evolve/#:~:text=releases%20such%20as%20GPT,1).
  То есть, система сама генерирует новые проблемы и оценивает решения по
  каким-то внутренним критериям. Например, в области дизайна или
  медицины успех трудно измерить одним числом; возможно, эволюционная
  система могла бы придумывать промежуточные задачи, решать их и тем
  самым находить интересные решения без явного целевого показателя. Для
  творческих агентов это значит, что **эстетический критерий тоже может
  эволюционировать**. Скажем, можно начать с примитивной метрики
  разнообразия, ShinkaEvolve генерирует множество артов, затем сама же
  анализирует их и формирует новую метрику «интересности» на основе
  выявленных паттернов (например, заметит, что людям нравятся
  контрастные композиции, и начнёт это поощрять). Это уже ближе к теме
  открытой эволюции и искусственного творчества, выходящей за рамки
  данной системы, но ShinkaEvolve заложила фундамент: у неё **открытая
  архитектура**, куда можно добавлять новые источники обратной связи,
  вплоть до полностью автономных циклов постановки
  задач[\[75\]](https://sakana.ai/shinka-evolve/#:~:text=Furthermore%2C%20a%20compelling%20future%20extension,success%20cannot%20be%20easily%20measured).
  В сочетании с растущими возможностями LLM (в тексте отмечено, что с
  приходом GPT-5, Claude 4.1 и др. эффективность Shinka только
  улучшается, т.к. модели становятся умнее и
  креативнее)[\[76\]](https://sakana.ai/shinka-evolve/#:~:text=Looking%20ahead%2C%20we%20see%20ShinkaEvolve,5%20and%20Claude%204.1),
  мы можем ожидать появление всё более *самостоятельных
  AI-исследователей и AI-творцов*.

## Связанные разработки и альтернативные подходы

ShinkaEvolve стоит в ряду новых систем, где AI используется для
**автоматического открытия алгоритмов и решений**. Ниже кратко упомянем
другие похожие и свежие работы в этой области:

- **AlphaEvolve (Google DeepMind, 2025):** это закрытая на данный момент
  система, предшествующая ShinkaEvolve по идее. AlphaEvolve –
  **эволюционный агент на базе LLM Gemini** для поиска
  алгоритмов[\[77\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=Today%2C%20we%E2%80%99re%20announcing%20AlphaEvolve%2C%20an,with%20automated%20evaluators%20that%20verify).
  Его достижения произвели фурор: сообщалось, что AlphaEvolve сумела
  **улучшить разнообразные задачи**, от оптимизации работы дата-центров
  Google до новых алгоритмов умножения матриц и решений задач из
  математики[\[78\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=AlphaEvolve%20enhanced%20the%20efficiency%20of,to%20open%20mathematical%20problems%2C%20showing)[\[79\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L564%20AlphaEvolve%E2%80%99s%20procedure,advance%20over%20our%20previous%20work).
  Например, AlphaEvolve нашла способ перемножать 4×4 комплексные матрицы
  с 48 умножениями – улучшив знаменитый алгоритм Штрассена 1969 года
  (лучший известный на тот момент для такого
  случая)[\[79\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L564%20AlphaEvolve%E2%80%99s%20procedure,advance%20over%20our%20previous%20work).
  Также она предложила новые эвристики для планировщика Borg (что дало
  +0.7% вычислительных ресурсов в масштабах
  Google)[\[80\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L505%20AlphaEvolve%20discovered,This),
  оптимизировала аппаратный модуль (переписала участок Verilog-кода в
  чипе)[\[81\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=AlphaEvolve%20proposed%20a%20Verilog%20rewrite,This),
  ускорила на 32% ядро FlashAttention для
  GPU[\[82\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L539%20AlphaEvolve%20can,the%20FlashAttention%20kernel%20implementation%20in),
  и даже продвинулась в классической задаче о «числе поцелуев» в
  11-мерном пространстве, улучшив рекорд (найдено размещение 593 сфер
  вокруг
  центральной)[\[83\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=The%20system%E2%80%99s%20flexibility%20enabled%20us,art%20solutions%2C%20to)[\[84\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L582%20AlphaEvolve%20discovered,lower%20bound%20in%2011%20dimensions).
  Эти результаты впечатляют – фактически AlphaEvolve показала, что **ИИ
  может самостоятельно изобретать новые алгоритмы**, опережая людей.
  Однако, AlphaEvolve пока не доступна широкой публике: DeepMind
  ограниченно делится доступом через Early Access и, видимо, использует
  её преимущественно для внутренних
  задач[\[85\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L587%20AlphaEvolve%20displays,as%20they%20become%20even%20better)[\[86\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=building%20a%20friendly%20user%20interface,interest%2C%20please%20complete%20this%20form).
  Кроме того, AlphaEvolve требует очень больших вычислительных ресурсов
  и множества итераций (хотя он эффективнее brute force, но всё же
  отчёты говорят о *тысячах* запусков для сложных задач). ShinkaEvolve,
  по сути, родилась как ответ сообщества: **сделать аналогичный
  инструмент доступным и более лёгким**. И действительно, ShinkaEvolve
  **воспроизводит и превосходит** один из ключевых результатов
  AlphaEvolve (упаковку окружностей) **на порядки
  быстрее**[\[9\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=AlphaEvolve%20demonstrated%20strong%20closed,contributes%20to%20the%20observed%20efficiency).
  При этом ShinkaEvolve – открытый проект (лицензия Apache
  2.0)[\[87\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=4,2.0),
  что позволяет любому исследователю его использовать и модифицировать.
  В ShinkaEvolve изначально заложены идеи, отсутствовавшие (или неявные)
  в AlphaEvolve: например, novelty-фильтр и бандитный выбор моделей –
  поэтому он часто находит решения не хуже, но значительно дешевле по
  вычислениям[\[9\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=AlphaEvolve%20demonstrated%20strong%20closed,contributes%20to%20the%20observed%20efficiency)[\[5\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20is%20an%20Apache,Code%20and%20report%20are%20public).

- **OpenEvolve:** После появления новостей об AlphaEvolve, независимые
  разработчики (под именем codelion) создали проект **OpenEvolve** –
  *опенсорсный клон* подхода
  DeepMind[\[88\]](https://github.com/codelion/openevolve#:~:text=The%20most%20advanced%20open,coding%20agent).
  OpenEvolve позиционируется как «самый продвинутый открытый
  эволюционный кодовый
  агент»[\[88\]](https://github.com/codelion/openevolve#:~:text=The%20most%20advanced%20open,coding%20agent).
  По функционалу он весьма близок к ShinkaEvolve: использует LLM для
  автономного поиска оптимизаций, заявляет 2-3х ускорение кода на
  реальном железе, state-of-the-art в упаковке кругов, новые алгоритмы
  сортировки и
  т.п.[\[89\]](https://github.com/codelion/openevolve#:~:text=Autonomous%20Discovery)[\[90\]](https://github.com/codelion/openevolve#:~:text=Domain%20Achievement%20Example%20GPU%20Optimization,R%2C%20Metal%20shaders%20All%20Examples).
  Упор сделан на **исследовательскую ценность**: полная
  воспроизводимость, строгие пайплайны оценки, детерминированность при
  seed для сравнительных
  экспериментов[\[91\]](https://github.com/codelion/openevolve#:~:text=Research%20Grade)[\[92\]](https://github.com/codelion/openevolve#:~:text=Scientific%20Reproducibility).
  В архитектуре OpenEvolve тоже есть *качественно-разнообразная эволюция
  (MAP-Elites)*, острова, ансамбль LLM с fallback-стратегиями, и даже
  учёт текстового фидбэка из ошибок компиляции (если код не
  скомпилировался, агент анализирует ошибку и учитывает в следующем
  поколении)[\[93\]](https://github.com/codelion/openevolve#:~:text=OpenEvolve%20implements%20a%20sophisticated%20evolutionary,goes%20far%20beyond%20simple%20optimization)[\[94\]](https://github.com/codelion/openevolve#:~:text=convergence%20,Error%20feedback%20improves%20subsequent%20generations).
  Это говорит о том, что идеи витали в сообществе и быстро развивались.
  У OpenEvolve большие звёзды на GitHub и активное сообщество; вероятно,
  ShinkaEvolve ознакомлена с ним, что видно по ссылкам: в документации
  ShinkaEvolve перечислены родственные проекты, включая
  OpenEvolve[\[95\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=Related%20Open).
  Отличие ShinkaEvolve – как мы обсуждали, особый акцент на
  **эффективность**. Если OpenEvolve – просто открытая реализация, то
  ShinkaEvolve привносит новые компоненты (новизна-фильтр, адаптивный
  выбор модели) и **показывает на абляциях вклад
  каждого**[\[13\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20Method%20Ablations%20on,contribute%20to%20ShinkaEvolve%27s%20sample%20efficiency).
  Таким образом, ShinkaEvolve можно рассматривать как следующую эволюцию
  публичных эволюционных агентов, вобравшую лучшее от
  OpenEvolve/AlphaEvolve и добавившую свои усовершенствования.

- **LLM4AD (Large Language Model for Algorithm Design):** этот проект
  (опубликован командой Optima, CityU) представляет собой платформу для
  проектирования алгоритмов при помощи
  LLM[\[95\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=Related%20Open).
  Судя по описанию, LLM4AD позволяет интерактивно решать задачи
  алгоритмического дизайна, возможно, тоже посредством генерации кода и
  проверки. В репозитории LLM4AD и на сайте (llm4ad.com) приведены
  примеры использования, обсуждения. Хотя деталей в нашем распоряжении
  мало, сам факт появления такого проекта показывает, что методология
  «LLM + поиск решений» становится популярной. LLM4AD может быть более
  ориентирован на удобство пользователя и интерактивность, в то время
  как ShinkaEvolve – на автономный глубокий поиск. Стоит отметить, что
  LLM4AD, OpenEvolve, ShinkaEvolve – **не конкуренты, а скорее разные
  инструменты одной парадигмы**. Исследователи могут выбирать, что им
  ближе по интерфейсу и функциям. Для нашего пользователя,
  заинтересованного в творческих агентах и самообучении, вероятно
  наиболее ценна **открытость к модификации** ShinkaEvolve и близость её
  идеологии к агентам, которые улучшают себя (в отличие, скажем, от
  чисто прикладного LLM4AD).

- **Darwin–Gödel Machine (DGM):** упоминавшаяся ранее работа Sakana AI
  имеет непосредственную связь с идеей самоулучшения AI. **DGM** – это
  архитектура, где агент *переписывает свой собственный код*, причём
  делает это эволюционно и бесконечно, пока видит возможность
  улучшиться[\[73\]](https://arxiv.org/abs/2505.22954#:~:text=beneficial%20is%20impossible%20in%20practice,paths%20through%20the%20search%20space).
  Название отсылает к теоретической «машине Гёделя» Юргена Шмидхубера
  (которая могла бы доказательно модифицировать себя) и принципам
  Дарвиновской эволюции. Практический DGM снимает требование строгого
  доказательства полезности изменений и вместо этого *эмпирически
  валидирует* каждое изменение: запускает нового агента на наборе задач
  и сравнивает
  результаты[\[73\]](https://arxiv.org/abs/2505.22954#:~:text=beneficial%20is%20impossible%20in%20practice,paths%20through%20the%20search%20space)[\[96\]](https://arxiv.org/abs/2505.22954#:~:text=also%20improving%20its%20ability%20to,g).
  В DGM, как и в Shinka, есть **архив агентов**, откуда берётся базовый
  агент, на основе него LLM генерирует нового, затем проверяется улучшил
  ли он показатели – если да, он остаётся в
  архиве[\[97\]](https://arxiv.org/abs/2505.22954#:~:text=also%20improving%20its%20ability%20to,review).
  Со временем DGM построила **дерево всё более сильных агентов**,
  которые, например, научились лучше редактировать код (AGI-Ability:
  редактирование своего источника), эффективнее управлять длинным
  контекстом, внедрили механизм peer-review в своё решение – и это
  привело к росту метрик на наборах SWE-Bench и Polyglot почти
  вдвое[\[74\]](https://arxiv.org/abs/2505.22954#:~:text=Empirically%2C%20the%20DGM%20automatically%20improves,that%20unfold%20into%20endless%20innovation).
  Фактически, DGM – это *особый случай* эволюции программ, где
  программой является *сам улучшайзер* (мета-алгоритм). ShinkaEvolve
  более прикладна – она улучшает решение внешней задачи, а не
  собственный код фреймворка. Однако, концепции overlap-ятся: и там и
  там заложена идея **open-ended эволюции**, когда нет фиксированного
  предела улучшения. Неудивительно, что ключевые авторы пересекаются (в
  командах Shinka и DGM фигурируют Robert Lange, Jeff Clune). Можно
  ожидать, что дальнейшие разработки Sakana AI объединят эти подходы:
  эволюционный оптимизатор Shinka может стать частью
  самосовершенствующегося агента DGM, или наоборот – DGM может дать
  идею, как ShinkaEvolve самой изменять свои правила для ещё большей
  универсальности.

- **Прочие системы эволюции и саморефлексии:** Помимо прямых потомков
  AlphaEvolve, стоит отметить общий тренд на **итеративные улучшения
  вывода LLM**. Например, подход *Self-Refine* (2023) – когда LLM сам
  критикует свой ответ и переделывает, пока не будет удовлетворён. Или
  проекты вроде **Voyager** (2023, Microsoft/OpenAI) – агент в
  Minecraft, который сам придумывает цели, пишет код (на Python) для
  решения задач в игре, учится навыкам и сохраняет их. Хотя Voyager не
  назывался эволюционным, по сути он также имел внутренний цикл
  улучшения: на основе неудач он генерировал новые попытки кода, а на
  основе удач – сохранял полезные функции. В более широком смысле, мы
  видим рождение **autonomous AI researcher** – ИИ, который сам ставит
  гипотезы, проверяет, корректирует. ShinkaEvolve пока требует, чтобы
  человек задал исходную задачу и метрику, но она предоставляет
  *платформу для автономного исследования в рамках этой задачи*. Добавив
  модуль генерации новых задач или вариаций (как было предложено
  авторами на
  будущее[\[71\]](https://sakana.ai/shinka-evolve/#:~:text=releases%20such%20as%20GPT,1)),
  получим приближение к AI, который открывает новое знание бесконечно
  (как *вечный научный исследователь*). Похожие амбиции высказываются и
  OpenAI, и DeepMind – например, проект **AI Scientist** (упомянутый
  Sakana AI в своем
  блоге[\[6\]](https://sakana.ai/shinka-evolve/#:~:text=At%20Sakana%20AI%2C%20we%20are,driven%20discovery))
  – идея, что ИИ будет сам делать научные открытия. Пока что
  ShinkaEvolve можно считать одним из конкретных воплощений такого AI
  Scientist, сфокусированного на сфере алгоритмов и программного кода.

## Заключение

**ShinkaEvolve** демонстрирует мощь симбиоза эволюционных алгоритмов и
больших языковых моделей. Система способна с минимальным участием
человека (после постановки задачи) **открывать новые, неожиданные
решения**, автоматически улучшая их от поколения к поколению. Благодаря
новаторским приёмам – балансированному отбору родителей, отсеиванию
банальных изменений, динамическому выбору наилучшего «советчика»-LLM –
ShinkaEvolve добивается результатов, ранее считавшихся невозможными без
огромных вычислительных
затрат[\[5\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20is%20an%20Apache,Code%20and%20report%20are%20public).
В нескольких различных областях она уже установила новые планки качества
решений (SOTA) и сделала это *более доступно* в вычислительном плане,
чем до того было нужно. Но не менее важно, что ShinkaEvolve – **не
закрытая «магическая» коробка**, а открытый инструмент для сообщества.
Исследователи и инженеры могут запускать его эксперименты, изучать через
WebUI, модифицировать под свои нужды. Авторы называют ShinkaEvolve
«копилотом для учёных и инженеров» – и уже сейчас видно, как система
может помогать в ежедневной работе: будь то оптимизация кода, подбор
гиперпараметров, поиск новых архитектур нейросетей или генерация
контента[\[98\]](https://sakana.ai/shinka-evolve/#:~:text=Our%20competitive%20programming%20results%20demonstrate,their%20research%20and%20development%20work)[\[99\]](https://sakana.ai/shinka-evolve/#:~:text=tandem%20with%20other%20agents%20as,their%20research%20and%20development%20work).

Перспективы развития ShinkaEvolve и подобных систем огромны. По мере
появления новых, более мощных моделей (GPT-5, Gemini, и т.д.),
эволюционный поиск станет ещё богаче идеями и
контекстом[\[76\]](https://sakana.ai/shinka-evolve/#:~:text=Looking%20ahead%2C%20we%20see%20ShinkaEvolve,5%20and%20Claude%204.1).
Вероятно, будет расти интеграция с доменно-специфичными инструментами:
например, для генерации изображений – соединение с диффузионными
моделями, для написания кода – с системами статического анализа, для
научных открытий – с симуляторами реальных процессов. Также, как мы
обсудили, важным направлением станет **открытое окончание
(open-endedness)** – когда система сама усложняет себе задачи, выходя за
рамки одного метрика. Уже намечен курс на то, чтобы ShinkaEvolve могла
генерировать свои собственные проблемы и черновую оценку решений для
областей, где нет точной функции
цели[\[71\]](https://sakana.ai/shinka-evolve/#:~:text=releases%20such%20as%20GPT,1).
Это делает её фундаментом для будущих **самотворящих ИИ**, которые
смогут исследовать области знаний без постоянного надзора человека.

В заключение, ShinkaEvolve – это не просто очередной фреймворк для
AutoML или оптимизации кода, а шаг к **новой парадигме** разработки:
когда мы не программируем решение вручную, а **растим** его подобно
живому организму в цифровой среде. Используя этот подробный обзор как
карту, можно ориентироваться в устройстве ShinkaEvolve и смежных работ,
а также продумывать **новые решения на его основе** – будь то творческие
агенты, способные генерировать искусство, или самообучающиеся помощники,
пишущие за нас проекты стартапов. Мир, где ИИ эволюционирует вместе с
задачами, уже не за горами, и ShinkaEvolve – один из инструментов,
приближающих его.

**Sources:**

- Sakana AI – *ShinkaEvolve: Evolving New Algorithms with LLMs, Orders
  of Magnitude More Efficiently* (блог-анонс, 25 сентября
  2025)[\[100\]](https://sakana.ai/shinka-evolve/#:~:text=In%20our%20new%20work%2C%20%E2%80%9CShinkaEvolve%3A,art%20performance%20and%20incredible%20efficiency)[\[35\]](https://sakana.ai/shinka-evolve/#:~:text=We%20tasked%20ShinkaEvolve%20with%20designing,and%20even%20different%20underlying%20LLMs)[\[47\]](https://sakana.ai/shinka-evolve/#:~:text=In%20a%20domain%20very%20relevant,future%20generations%20of%20AI%20models).
- Arxiv preprint – *“ShinkaEvolve: Towards Open-Ended And
  Sample-Efficient Program Evolution”* (Robert Lange et al.,
  2025)[\[10\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=1,yielding%20the%20biggest%20relative%20fitness)[\[15\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20maintains%20an%20archive%20of,prompts%20to%20accelerate%20later%20generations)[\[9\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=AlphaEvolve%20demonstrated%20strong%20closed,contributes%20to%20the%20observed%20efficiency).
- GitHub – *SakanaAI/ShinkaEvolve* (репозиторий кодовой базы и
  документации
  ShinkaEvolve)[\[7\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=search%2C%20,operators%20that%20suggest%20code%20improvements)[\[20\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=To%20use%20EvolutionRunner%2C%20you%20need,improved%20by%20LLMs%20across%20generations).
- MarkTechPost – *“Sakana AI Released ShinkaEvolve…”* (Asif Razzaq, 26
  Sep 2025) – новостной обзор с разбором идей и результатов
  ShinkaEvolve[\[101\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=Most%20%E2%80%9Cagentic%E2%80%9D%20code,explicitly%20with%20three%20interacting%20components)[\[5\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20is%20an%20Apache,Code%20and%20report%20are%20public).
- Google DeepMind Blog – *“AlphaEvolve: A Gemini-powered coding agent
  for designing advanced algorithms”* (14 May
  2025)[\[78\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=AlphaEvolve%20enhanced%20the%20efficiency%20of,to%20open%20mathematical%20problems%2C%20showing)[\[79\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L564%20AlphaEvolve%E2%80%99s%20procedure,advance%20over%20our%20previous%20work).
- Arxiv – *“Darwin Gödel Machine: Open-Ended Evolution of Self-Improving
  Agents”* (Jenny Zhang et al., May
  2025)[\[73\]](https://arxiv.org/abs/2505.22954#:~:text=beneficial%20is%20impossible%20in%20practice,paths%20through%20the%20search%20space)[\[74\]](https://arxiv.org/abs/2505.22954#:~:text=Empirically%2C%20the%20DGM%20automatically%20improves,that%20unfold%20into%20endless%20innovation).
- GitHub – *codelion/openevolve* (OpenEvolve: открытая реализация
  AlphaEvolve)[\[89\]](https://github.com/codelion/openevolve#:~:text=Autonomous%20Discovery)[\[102\]](https://github.com/codelion/openevolve#:~:text=How%20OpenEvolve%20Works).
- И другие источники, цитируемые по тексту.

------------------------------------------------------------------------

[\[1\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=Sakana%20AI%20has%20released%20ShinkaEvolve%2C,research%20report%20and%20public%20code)
[\[2\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=number%20of%20evaluations%20needed%20to,with%20a%20research%20report%20and)
[\[3\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=language%20models%20,research%20report%20and%20public%20code)
[\[4\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=,10%20tasks%20and%20pushes%20one)
[\[5\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20is%20an%20Apache,Code%20and%20report%20are%20public)
[\[9\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=AlphaEvolve%20demonstrated%20strong%20closed,contributes%20to%20the%20observed%20efficiency)
[\[10\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=1,yielding%20the%20biggest%20relative%20fitness)
[\[11\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=weighted%20by%20performance%20and%20offspring,style%20update%20on%20improvement)
[\[12\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=secondary%20LLM%20acts%20as%20a,style%20update%20on%20improvement)
[\[15\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=ShinkaEvolve%20maintains%20an%20archive%20of,prompts%20to%20accelerate%20later%20generations)
[\[16\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=parent,prompts%20to%20accelerate%20later%20generations)
[\[19\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=parent,The%20system%20periodically%20produces%20a)
[\[29\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=number%20of%20evaluations%20needed%20to,research%20report%20and%20public%20code)
[\[31\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=,that%20push%20scores)
[\[37\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=mechanisms%20,batch)
[\[39\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=hand,batch)
[\[43\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=baselines%20under%20limited%20query%20budgets,batch%20LBL)
[\[45\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=retaining%20robustness%20when%20swapped%20to,perplexity%2Fbenchmarks%20as%20layer%20routing%20concentrates)
[\[49\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=,perplexity%2Fbenchmarks%20as%20layer%20routing%20concentrates)
[\[51\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=,perplexity%2Fbenchmarks%20as%20layer%20routing%20concentrates)
[\[87\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=4,2.0)
[\[101\]](https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/#:~:text=Most%20%E2%80%9Cagentic%E2%80%9D%20code,explicitly%20with%20three%20interacting%20components)
Sakana AI Released ShinkaEvolve: An Open-Source Framework that Evolves
Programs for Scientific Discovery with Unprecedented Sample-Efficiency -
MarkTechPost

<https://www.marktechpost.com/2025/09/26/sakana-ai-released-shinkaevolve-an-open-source-framework-that-evolves-programs-for-scientific-discovery-with-unprecedented-sample-efficiency/>

[\[6\]](https://sakana.ai/shinka-evolve/#:~:text=At%20Sakana%20AI%2C%20we%20are,driven%20discovery)
[\[8\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20High,programs%2C%20and%20evaluates%20their%20fitness)
[\[13\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20Method%20Ablations%20on,contribute%20to%20ShinkaEvolve%27s%20sample%20efficiency)
[\[14\]](https://sakana.ai/shinka-evolve/#:~:text=stepping%20stone%20collection%20dynamics%20of,contribute%20to%20ShinkaEvolve%27s%20sample%20efficiency)
[\[25\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20generates%20a%20search,humans%20in%20achieving%20further%20improvements)
[\[26\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20ShinkaEvolve%20generates%20a%20search,humans%20in%20achieving%20further%20improvements)
[\[28\]](https://sakana.ai/shinka-evolve/#:~:text=The%20Japanese%20word%20%E2%80%98Shinka%E2%80%99%20,its%20power%2C%20generality%2C%20and%20efficiency)
[\[30\]](https://sakana.ai/shinka-evolve/#:~:text=ShinkaEvolve%20discovered%20a%20new%20state,annealing%20to%20escape%20local%20optima)
[\[32\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20Circle%20Packing%3A%20ShinkaEvolve%27s%20discovered,solution%20in%20only%20150%20generations)
[\[33\]](https://sakana.ai/shinka-evolve/#:~:text=match%20at%20L72%20Circle%20Packing%3A,solution%20in%20only%20150%20generations)
[\[34\]](https://sakana.ai/shinka-evolve/#:~:text=26,annealing%20to%20escape%20local%20optima)
[\[35\]](https://sakana.ai/shinka-evolve/#:~:text=We%20tasked%20ShinkaEvolve%20with%20designing,and%20even%20different%20underlying%20LLMs)
[\[36\]](https://sakana.ai/shinka-evolve/#:~:text=We%20tasked%20ShinkaEvolve%20with%20designing,and%20even%20different%20underlying%20LLMs)
[\[38\]](https://sakana.ai/shinka-evolve/#:~:text=peer%20review%2C%20and%20a%20final,and%20even%20different%20underlying%20LLMs)
[\[40\]](https://sakana.ai/shinka-evolve/#:~:text=We%20took%20the%20best%20solutions,novel%20%E2%80%9Ctargeted%20edge%20move%E2%80%9D%20operators)
[\[41\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20Competitive%20Programming%3A%20ShinkaEvolve%20improves,for%20AtCoder%20heuristic%20programming%20competitions)
[\[42\]](https://sakana.ai/shinka-evolve/#:~:text=successfully%20found%20improvements%20across%20multiple,novel%20%E2%80%9Ctargeted%20edge%20move%E2%80%9D%20operators)
[\[44\]](https://sakana.ai/shinka-evolve/#:~:text=performance%20of%20the%20agent,novel%20%E2%80%9Ctargeted%20edge%20move%E2%80%9D%20operators)
[\[46\]](https://sakana.ai/shinka-evolve/#:~:text=Image%20On%20average%20the%20performance,to%20the%20public%20test%20cases)
[\[47\]](https://sakana.ai/shinka-evolve/#:~:text=In%20a%20domain%20very%20relevant,future%20generations%20of%20AI%20models)
[\[48\]](https://sakana.ai/shinka-evolve/#:~:text=load%20balancing%20loss%20,generations%20of%20AI%20models%20themselves)
[\[50\]](https://sakana.ai/shinka-evolve/#:~:text=outperformed%20the%20state,generations%20of%20AI%20models%20themselves)
[\[52\]](https://sakana.ai/shinka-evolve/#:~:text=After%20only%2030%20ShinkaEvolve%20generations%2C,generations%20of%20AI%20models%20themselves)
[\[71\]](https://sakana.ai/shinka-evolve/#:~:text=releases%20such%20as%20GPT,1)
[\[72\]](https://sakana.ai/shinka-evolve/#:~:text=AIME%20Agent%20Scaffold%20Design%3A%20Evolving,the%20number%20of%20LLM%20queries)
[\[75\]](https://sakana.ai/shinka-evolve/#:~:text=Furthermore%2C%20a%20compelling%20future%20extension,success%20cannot%20be%20easily%20measured)
[\[76\]](https://sakana.ai/shinka-evolve/#:~:text=Looking%20ahead%2C%20we%20see%20ShinkaEvolve,5%20and%20Claude%204.1)
[\[98\]](https://sakana.ai/shinka-evolve/#:~:text=Our%20competitive%20programming%20results%20demonstrate,their%20research%20and%20development%20work)
[\[99\]](https://sakana.ai/shinka-evolve/#:~:text=tandem%20with%20other%20agents%20as,their%20research%20and%20development%20work)
[\[100\]](https://sakana.ai/shinka-evolve/#:~:text=In%20our%20new%20work%2C%20%E2%80%9CShinkaEvolve%3A,art%20performance%20and%20incredible%20efficiency)
ShinkaEvolve: Evolving New Algorithms with LLMs, Orders of Magnitude
More Efficiently

<https://sakana.ai/shinka-evolve/>

[\[7\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=search%2C%20,operators%20that%20suggest%20code%20improvements)
[\[17\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60initial.py%60%20)
[\[18\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,maximization)
[\[20\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=To%20use%20EvolutionRunner%2C%20you%20need,improved%20by%20LLMs%20across%20generations)
[\[21\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=def%20main,evals%20to%20aggreg.%20get_experiment_kwargs%3Dget_kwargs%2C%20aggregate_metrics_fn%3Daggregate_fn)
[\[22\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=return%20%7B)
[\[23\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=score%20%3D%20results,str%20fb)
[\[24\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%2A%20Use%20%60EVOLVE,maximization)
[\[27\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=Interactive%20WebUI)
[\[53\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,Sharpness%20of%20sigmoid%20for%20weighted)
[\[54\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,beams%20for%20beam%20search%20selection)
[\[55\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=if%20None%29%20,use%20text%20feedback%20in%20evolution)
[\[56\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,recommendations)
[\[58\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60task_sys_msg%60%20%60None%60%20%60Optional,a%20patch%20if%20it%20fails)
[\[59\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60job_type%60%20%60,Kwargs%20for%20dynamic%20selection)
[\[60\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=task%20%60patch_types%60%20%60%5B,slurm_docker)
[\[61\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60evaluate.py%60%20)
[\[62\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=)
[\[63\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=LocalJobConfig%20)
[\[64\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=SlurmCondaJobConfig%20)
[\[65\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%2A%20Auto,maximization)
[\[66\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=selection%20strategy%20%60llm_dynamic_selection_kwargs%60%20%60,str%5D%60%20Model%20for%20code%20embeddings)
[\[67\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=,LLM%20models%20for%20code%20generation)
[\[68\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=SlurmDockerJobConfig%20)
[\[69\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%60mem%60%20%60,request)
[\[70\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=%E2%AD%95%20Circle%20Packing%20%20Optimize,LocalJobConfig)
[\[95\]](https://github.com/SakanaAI/ShinkaEvolve#:~:text=Related%20Open)
GitHub - SakanaAI/ShinkaEvolve: ShinkaEvolve: Towards Open-Ended and
Sample-Efficient Program Evolution

<https://github.com/SakanaAI/ShinkaEvolve>

[\[57\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L470%20AlphaEvolve%20leverages,Together%2C%20these%20models%20propose)
[\[77\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=Today%2C%20we%E2%80%99re%20announcing%20AlphaEvolve%2C%20an,with%20automated%20evaluators%20that%20verify)
[\[78\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=AlphaEvolve%20enhanced%20the%20efficiency%20of,to%20open%20mathematical%20problems%2C%20showing)
[\[79\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L564%20AlphaEvolve%E2%80%99s%20procedure,advance%20over%20our%20previous%20work)
[\[80\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L505%20AlphaEvolve%20discovered,This)
[\[81\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=AlphaEvolve%20proposed%20a%20Verilog%20rewrite,This)
[\[82\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L539%20AlphaEvolve%20can,the%20FlashAttention%20kernel%20implementation%20in)
[\[83\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=The%20system%E2%80%99s%20flexibility%20enabled%20us,art%20solutions%2C%20to)
[\[84\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L582%20AlphaEvolve%20discovered,lower%20bound%20in%2011%20dimensions)
[\[85\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=match%20at%20L587%20AlphaEvolve%20displays,as%20they%20become%20even%20better)
[\[86\]](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/#:~:text=building%20a%20friendly%20user%20interface,interest%2C%20please%20complete%20this%20form)
AlphaEvolve: A Gemini-powered coding agent for designing advanced
algorithms - Google DeepMind

<https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/>

[\[73\]](https://arxiv.org/abs/2505.22954#:~:text=beneficial%20is%20impossible%20in%20practice,paths%20through%20the%20search%20space)
[\[74\]](https://arxiv.org/abs/2505.22954#:~:text=Empirically%2C%20the%20DGM%20automatically%20improves,that%20unfold%20into%20endless%20innovation)
[\[96\]](https://arxiv.org/abs/2505.22954#:~:text=also%20improving%20its%20ability%20to,g)
[\[97\]](https://arxiv.org/abs/2505.22954#:~:text=also%20improving%20its%20ability%20to,review)
\[2505.22954\] Darwin Godel Machine: Open-Ended Evolution of
Self-Improving Agents

<https://arxiv.org/abs/2505.22954>

[\[88\]](https://github.com/codelion/openevolve#:~:text=The%20most%20advanced%20open,coding%20agent)
[\[89\]](https://github.com/codelion/openevolve#:~:text=Autonomous%20Discovery)
[\[90\]](https://github.com/codelion/openevolve#:~:text=Domain%20Achievement%20Example%20GPU%20Optimization,R%2C%20Metal%20shaders%20All%20Examples)
[\[91\]](https://github.com/codelion/openevolve#:~:text=Research%20Grade)
[\[92\]](https://github.com/codelion/openevolve#:~:text=Scientific%20Reproducibility)
[\[93\]](https://github.com/codelion/openevolve#:~:text=OpenEvolve%20implements%20a%20sophisticated%20evolutionary,goes%20far%20beyond%20simple%20optimization)
[\[94\]](https://github.com/codelion/openevolve#:~:text=convergence%20,Error%20feedback%20improves%20subsequent%20generations)
[\[102\]](https://github.com/codelion/openevolve#:~:text=How%20OpenEvolve%20Works)
GitHub - codelion/openevolve: Open-source implementation of AlphaEvolve

<https://github.com/codelion/openevolve>
