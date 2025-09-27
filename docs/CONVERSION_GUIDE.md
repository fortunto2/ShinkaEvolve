# Конвертация материалов ShinkaEvolve

Ниже собраны быстрые рецепты, которые уже проверены в этой папке.
Все пути указаны относительно `projects/ShinkaEvolve/docs`.

## HTML → Markdown (arXiv)

```bash
# 1. Скачиваем HTML
curl -L https://arxiv.org/html/<article_id> -o <article_id>.html

# 2. Конвертируем в Markdown без HTML-тегов
tool=/Users/rustam/projects/ShinkaEvolve/docs/strip_html.lua
pandoc <article_id>.html -f html -t gfm --lua-filter="$tool" --wrap=preserve -o <article_id>.md
```

- Фильтр `strip_html.lua` лежит рядом; он убирает лишние теги и нормализует ссылки/рисунки.
- После конвертации можно заменить локальные пути на публичные, выполнив:
  ```bash
  python3 - <<'PY'
  from pathlib import Path
  path = Path('<article_id>.md')
  text = path.read_text()
  path.write_text(text.replace('](/html/', '](https://arxiv.org/html/')))
  PY
  ```

## PDF → Markdown

```bash
pdftotext -layout "<name>.pdf" "<name>.txt"
pandoc "<name>.txt" -f markdown -t gfm -o "<name>_pdf.md"
rm "<name>.txt"
```

- Ключ `-layout` сохраняет колонку/таблицы как в оригинале; уберите его, если нужен «плоский» текст.
- Полученный Markdown может потребовать ручной уборки разрывов строк и восстановление заголовков.

## DOCX → Markdown

```bash
pandoc "<name>.docx" -t gfm -o "<name>.md"
```

- DOCX сохраняет стили лучше всего, обычно редактирование минимальное.

## Очистка Markdown после конвертации

- Удаление остатков HTML/LaTeX (теги `\figure`, `\sidecaption` и т.п.) удобно делать через `python` + `re` или `rg` + `sed`.
- Для встроенных изображений `data:image/...` можно вытянуть файл:
  ```bash
  python3 - <<'PY'
  import base64, pathlib, re
  path = pathlib.Path('<name>.md')
  text = path.read_text()
  for i, match in enumerate(re.finditer(r'!\[[^\]]*\]\(data:image/[^;]+;base64,([^\)]+)\)', text), 1):
      data = base64.b64decode(match.group(1))
      fname = f"{path.stem}_inline{i}.svg"
      (path.parent / fname).write_bytes(data)
      text = text.replace(match.group(0), f'![Inline {i}]({fname})', 1)
  path.write_text(text)
  PY
  ```

## Полезные заметки

- `rg` помогает найти остаточные теги: `rg '<' <file>.md`.
- Если `pdftotext` или `pandoc` ругаются на формат, проверьте, что пакет установлен (`which pdftotext`, `pandoc --version`).
- Для повторной конвертации достаточно удалить старый `.md` и заново запустить нужную команду.
