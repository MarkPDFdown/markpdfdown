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

MarkPDFDown разработан для упрощения процесса преобразования PDF-документов в чистый, редактируемый текст Markdown. Используя передовые мультимодальные модели ИИ, он может точно извлекать текст, сохранять форматирование и обрабатывать сложные структуры документов, включая таблицы, формулы и диаграммы.

## Возможности

- **Преобразование PDF в Markdown**: Преобразование любого PDF-документа в хорошо отформатированный Markdown
- **Преобразование изображения в Markdown**: Преобразование изображения в хорошо отформатированный Markdown
- **Мультимодальное понимание**: Использует ИИ для понимания структуры и содержания документа
- **Сохранение формата**: Сохраняет заголовки, списки, таблицы и другие элементы форматирования
- **Настраиваемая модель**: Настройте модель в соответствии с вашими потребностями

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
## Использование
```bash
# Настройте ваш OpenAI API ключ
export OPENAI_API_KEY="your-api-key"
# Опционально, настройте базу OpenAI API
export OPENAI_API_BASE="your-api-base"
# Опционально, настройте модель OpenAI API
export OPENAI_DEFAULT_MODEL="your-model"

# PDF в Markdown
python main.py < tests/input.pdf > output.md

# Изображение в Markdown
python main.py < input_image.png > output.md
```
## Расширенное использование
```bash
python main.py page_start page_end < tests/input.pdf > output.md
```

## Использование Docker
```bash
docker run -i -e OPENAI_API_KEY=your-api-key -e OPENAI_API_BASE=your-api-base -e OPENAI_DEFAULT_MODEL=your-model jorbenzhu/markpdfdown < input.pdf > output.md
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
- Доступ к указанной мультимодальной модели ИИ

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
- Спасибо разработчикам мультимодальных моделей ИИ, которые поддерживают этот инструмент
- Вдохновлен необходимостью в лучших инструментах преобразования PDF в Markdown

[hub_url]: https://hub.docker.com/r/jorbenzhu/markpdfdown/
[tag_url]: https://github.com/markpdfdown/markpdfdown/releases
[license_url]: https://github.com/markpdfdown/markpdfdown/blob/main/LICENSE

[Size]: https://img.shields.io/docker/image-size/jorbenzhu/markpdfdown/latest?color=066da5&label=size
[Pulls]: https://img.shields.io/docker/pulls/jorbenzhu/markpdfdown.svg?style=flat&label=pulls&logo=docker
[Tag]: https://img.shields.io/github/release/markpdfdown/markpdfdown.svg
[License]: https://img.shields.io/github/license/markpdfdown/markpdfdown