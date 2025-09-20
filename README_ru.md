<div align="center">

<h1>MarkPDFDown</h1>
<p align="center"><a href="./README.md">English</a> | <a href="./README_zh.md">中文</a> | <a href="./README_ja.md">日本語</a> | Русский | <a href="./README_fa.md">فارسی</a> | <a href="./README_ar.md">العربية</a></p>

[![Size]][hub_url]
[![Pulls]][hub_url]
[![Tag]][tag_url]
[![License]][license_url]
<p>Мощный инструмент, использующий мультимодальные большие языковые модели для преобразования PDF-файлов в формат Markdown.</p>

![markpdfdown](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/markpdfdown.png)

</div>

## Обзор

MarkPDFDown разработан для упрощения процесса преобразования PDF-документов в чистый, редактируемый текст Markdown. Используя передовые мультимодальные модели ИИ через LiteLLM, он может точно извлекать текст, сохранять форматирование и обрабатывать сложные структуры документов, включая таблицы, формулы и диаграммы.

## Возможности

- **Преобразование PDF в Markdown**: Преобразование любого PDF-документа в хорошо отформатированный Markdown
- **Преобразование изображения в Markdown**: Преобразование изображения в хорошо отформатированный Markdown
- **Поддержка нескольких провайдеров**: Поддержка OpenAI и OpenRouter через LiteLLM
- **Гибкий CLI**: Режимы использования на основе файлов и на основе конвейера
- **Сохранение формата**: Сохраняет заголовки, списки, таблицы и другие элементы форматирования
- **Выбор диапазона страниц**: Преобразование определенных диапазонов страниц из PDF-документов
- **Модульная архитектура**: Чистая, поддерживаемая кодовая база с разделением ответственности

## Демонстрация
![](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/demo_02.png)

## Установка

### Использование uv (Рекомендуется)

```bash
# Установите uv, если еще не установлен
curl -LsSf https://astral.sh/uv/install.sh | sh

# Клонируйте репозиторий
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# Установите зависимости и создайте виртуальное окружение
uv sync

# Установите пакет в режиме разработки
uv pip install -e .
```

### Использование conda

```bash
conda create -n markpdfdown python=3.9
conda activate markpdfdown

# Клонируйте репозиторий
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# Установите зависимости
pip install -e .
```

## Конфигурация

MarkPDFDown использует переменные окружения для конфигурации. Создайте файл `.env` в директории вашего проекта:

```bash
# Скопируйте образец конфигурации
cp .env.sample .env
```

Отредактируйте файл `.env` с вашими настройками:

```bash
# Конфигурация модели
MODEL_NAME=gpt-4o

# API ключи (LiteLLM автоматически определяет их)
OPENAI_API_KEY=your-openai-api-key
# или для OpenRouter
OPENROUTER_API_KEY=your-openrouter-api-key

# Опциональные параметры
TEMPERATURE=0.3
MAX_TOKENS=8192
RETRY_TIMES=3
```

### Поддерживаемые модели

#### Модели OpenAI
```bash
MODEL_NAME=gpt-4o
MODEL_NAME=gpt-4o-mini
MODEL_NAME=gpt-4-vision-preview
```

#### Модели OpenRouter
```bash
MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet
MODEL_NAME=openrouter/google/gemini-pro-vision
MODEL_NAME=openrouter/meta-llama/llama-3.2-90b-vision
```

## Использование

### Файловый режим (Рекомендуется)

```bash
# Базовое преобразование
markpdfdown --input document.pdf --output output.md

# Преобразование определенного диапазона страниц
markpdfdown --input document.pdf --output output.md --start 1 --end 10

# Преобразование изображения в markdown
markpdfdown --input image.png --output output.md

# Использование python модуля
python -m markpdfdown --input document.pdf --output output.md
```

### Режим конвейера (Удобно для Docker)

```bash
# PDF в markdown через конвейер
markpdfdown < document.pdf > output.md

# Использование python модуля
python -m markpdfdown < document.pdf > output.md
```

### Расширенное использование

```bash
# Преобразование страниц 5-15 PDF
markpdfdown --input large_document.pdf --output chapter.md --start 5 --end 15

# Обработка нескольких файлов
for file in *.pdf; do
    markpdfdown --input "$file" --output "${file%.pdf}.md"
done
```

## Использование Docker

```bash
# Соберите образ (при необходимости)
docker build -t markpdfdown .

# Запустите с переменными окружения
docker run -i \
  -e MODEL_NAME=gpt-4o \
  -e OPENAI_API_KEY=your-api-key \
  markpdfdown < input.pdf > output.md

# Использование OpenRouter
docker run -i \
  -e MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet \
  -e OPENROUTER_API_KEY=your-openrouter-key \
  markpdfdown < input.pdf > output.md
```

## Настройка разработки

### Инструменты качества кода

Этот проект использует `ruff` для линтинга и форматирования, и `pre-commit` для автоматических проверок качества кода.

#### Установка зависимостей разработки

```bash
# При использовании uv
uv sync --group dev

# При использовании pip
pip install -e ".[dev]"
```

#### Настройка хуков pre-commit

```bash
# Установка хуков pre-commit
pre-commit install

# Запуск pre-commit на всех файлах (опционально)
pre-commit run --all-files
```

#### Форматирование и линтинг кода

```bash
# Форматирование кода с помощью ruff
ruff format

# Запуск проверок линтинга
ruff check

# Исправление автоматически исправляемых проблем
ruff check --fix
```

## Требования
- Python 3.9+
- [uv](https://astral.sh/uv/) (рекомендуется для управления пакетами) или conda/pip
- Зависимости, указанные в `pyproject.toml`
- Доступ к поддерживаемым провайдерам LLM (OpenAI или OpenRouter)

## Архитектура

Проект следует модульной архитектуре:

```
src/markpdfdown/
├── __init__.py          # Инициализация пакета
├── __main__.py          # Точка входа для python -m
├── cli.py               # Интерфейс командной строки
├── main.py              # Основная логика преобразования
├── config.py            # Управление конфигурацией
└── core/                # Основные модули
    ├── llm_client.py    # Интеграция LiteLLM
    ├── file_worker.py   # Обработка файлов
    └── utils.py         # Служебные функции
```

## Вклад в проект
Вклады приветствуются! Пожалуйста, не стесняйтесь отправлять Pull Request.

1. Форкните репозиторий
2. Создайте ветку для функции (`git checkout -b feature/amazing-feature`)
3. Настройте среду разработки:
   ```bash
   uv sync --group dev
   pre-commit install
   ```
4. Внесите изменения и обеспечьте качество кода:
   ```bash
   ruff format
   ruff check --fix
   pre-commit run --all-files
   ```
5. Зафиксируйте ваши изменения (`git commit -m 'feat: Add some amazing feature'`)
6. Отправьте в ветку (`git push origin feature/amazing-feature`)
7. Откройте Pull Request

Пожалуйста, убедитесь, что ваш код соответствует стандартам кодирования проекта, запустив инструменты линтинга и форматирования перед отправкой.

## Лицензия
Этот проект лицензирован под Apache License 2.0. Подробности смотрите в файле LICENSE.

## Благодарности
- Спасибо разработчикам LiteLLM за предоставление унифицированного доступа к LLM
- Спасибо разработчикам мультимодальных моделей ИИ, которые поддерживают этот инструмент
- Вдохновлен необходимостью в лучших инструментах преобразования PDF в Markdown

[hub_url]: https://hub.docker.com/r/jorbenzhu/markpdfdown/
[tag_url]: https://github.com/markpdfdown/markpdfdown/releases
[license_url]: https://github.com/markpdfdown/markpdfdown/blob/main/LICENSE

[Size]: https://img.shields.io/docker/image-size/jorbenzhu/markpdfdown/latest?color=066da5&label=size
[Pulls]: https://img.shields.io/docker/pulls/jorbenzhu/markpdfdown.svg?style=flat&label=pulls&logo=docker
[Tag]: https://img.shields.io/github/release/markpdfdown/markpdfdown.svg
[License]: https://img.shields.io/github/license/markpdfdown/markpdfdown