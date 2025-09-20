<div align="center" dir="rtl">

<h1>MarkPDFDown</h1>
<p align="center"><a href="./README.md">English</a> | <a href="./README_zh.md">中文</a> | <a href="./README_ja.md">日本語</a> | <a href="./README_ru.md">Русский</a> | فارسی | <a href="./README_ar.md">العربية</a></p>

[![Size]][hub_url]
[![Pulls]][hub_url]
[![Tag]][tag_url]
[![License]][license_url]
<p>ابزاری قدرتمند که از مدل‌های زبانی بزرگ چندوجهی برای تبدیل فایل‌های PDF به فرمت Markdown استفاده می‌کند.</p>

![markpdfdown](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/markpdfdown.png)

</div>

<div dir="rtl">

## بررسی اجمالی

MarkPDFDown برای ساده‌سازی فرآیند تبدیل اسناد PDF به متن Markdown تمیز و قابل ویرایش طراحی شده است. با استفاده از مدل‌های هوش مصنوعی چندوجهی پیشرفته از طریق LiteLLM، می‌تواند متن را به دقت استخراج کند، قالب‌بندی را حفظ کند و ساختارهای پیچیده سند از جمله جداول، فرمول‌ها و نمودارها را مدیریت کند.

## ویژگی‌ها

- **تبدیل PDF به Markdown**: هر سند PDF را به Markdown با قالب‌بندی مناسب تبدیل کنید
- **تبدیل تصویر به Markdown**: تصویر را به Markdown با قالب‌بندی مناسب تبدیل کنید
- **پشتیبانی از چندین ارائه‌دهنده**: پشتیبانی از OpenAI و OpenRouter از طریق LiteLLM
- **CLI انعطاف‌پذیر**: حالت‌های استفاده مبتنی بر فایل و مبتنی بر پایپ
- **حفظ قالب‌بندی**: سرفصل‌ها، لیست‌ها، جداول و سایر عناصر قالب‌بندی را حفظ می‌کند
- **انتخاب محدوده صفحه**: تبدیل محدوده‌های خاص صفحه از اسناد PDF
- **معماری ماژولار**: کدبیس تمیز و قابل نگهداری با تفکیک دغدغه‌ها

## نمایش
![](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/demo_02.png)

## نصب

### استفاده از uv (توصیه می‌شود)

</div>

```bash
# نصب uv اگر قبلاً نصب نکرده‌اید
curl -LsSf https://astral.sh/uv/install.sh | sh

# کلون کردن مخزن
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# نصب وابستگی‌ها و ایجاد محیط مجازی
uv sync

# نصب بسته در حالت توسعه
uv pip install -e .
```

<div dir="rtl">

### استفاده از conda

</div>

```bash
conda create -n markpdfdown python=3.9
conda activate markpdfdown

# کلون کردن مخزن
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# نصب وابستگی‌ها
pip install -e .
```

<div dir="rtl">

## پیکربندی

MarkPDFDown از متغیرهای محیطی برای پیکربندی استفاده می‌کند. یک فایل `.env` در دایرکتوری پروژه خود ایجاد کنید:

</div>

```bash
# کپی پیکربندی نمونه
cp .env.sample .env
```

<div dir="rtl">

فایل `.env` را با تنظیمات خود ویرایش کنید:

</div>

```bash
# پیکربندی مدل
MODEL_NAME=gpt-4o

# کلیدهای API (LiteLLM به طور خودکار این‌ها را تشخیص می‌دهد)
OPENAI_API_KEY=your-openai-api-key
# یا برای OpenRouter
OPENROUTER_API_KEY=your-openrouter-api-key

# پارامترهای اختیاری
TEMPERATURE=0.3
MAX_TOKENS=8192
RETRY_TIMES=3
```

<div dir="rtl">

### مدل‌های پشتیبانی شده

#### مدل‌های OpenAI

</div>

```bash
MODEL_NAME=gpt-4o
MODEL_NAME=gpt-4o-mini
MODEL_NAME=gpt-4-vision-preview
```

<div dir="rtl">

#### مدل‌های OpenRouter

</div>

```bash
MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet
MODEL_NAME=openrouter/google/gemini-pro-vision
MODEL_NAME=openrouter/meta-llama/llama-3.2-90b-vision
```

<div dir="rtl">

## استفاده

### حالت فایل (توصیه شده)

</div>

```bash
# تبدیل پایه
markpdfdown --input document.pdf --output output.md

# تبدیل محدوده صفحه خاص
markpdfdown --input document.pdf --output output.md --start 1 --end 10

# تبدیل تصویر به markdown
markpdfdown --input image.png --output output.md

# استفاده از ماژول پایتون
python -m markpdfdown --input document.pdf --output output.md
```

<div dir="rtl">

### حالت پایپ (سازگار با Docker)

</div>

```bash
# PDF به markdown از طریق پایپ
markpdfdown < document.pdf > output.md

# استفاده از ماژول پایتون
python -m markpdfdown < document.pdf > output.md
```

<div dir="rtl">

### استفاده پیشرفته

</div>

```bash
# تبدیل صفحات 5-15 یک PDF
markpdfdown --input large_document.pdf --output chapter.md --start 5 --end 15

# پردازش چندین فایل
for file in *.pdf; do
    markpdfdown --input "$file" --output "${file%.pdf}.md"
done
```

<div dir="rtl">

## استفاده از Docker

</div>

```bash
# ساخت تصویر (در صورت نیاز)
docker build -t markpdfdown .

# اجرا با متغیرهای محیطی
docker run -i \
  -e MODEL_NAME=gpt-4o \
  -e OPENAI_API_KEY=your-api-key \
  markpdfdown < input.pdf > output.md

# استفاده از OpenRouter
docker run -i \
  -e MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet \
  -e OPENROUTER_API_KEY=your-openrouter-key \
  markpdfdown < input.pdf > output.md
```

<div dir="rtl">

## راه‌اندازی توسعه

### ابزارهای کیفیت کد

این پروژه از `ruff` برای linting و قالب‌بندی، و `pre-commit` برای بررسی‌های خودکار کیفیت کد استفاده می‌کند.

#### نصب وابستگی‌های توسعه

</div>

```bash
# اگر از uv استفاده می‌کنید
uv sync --group dev

# اگر از pip استفاده می‌کنید
pip install -e ".[dev]"
```

<div dir="rtl">

#### راه‌اندازی هوک‌های pre-commit

</div>

```bash
# نصب هوک‌های pre-commit
pre-commit install

# اجرای pre-commit روی همه فایل‌ها (اختیاری)
pre-commit run --all-files
```

<div dir="rtl">

#### قالب‌بندی و linting کد

</div>

```bash
# قالب‌بندی کد با ruff
ruff format

# اجرای بررسی‌های linting
ruff check

# رفع مشکلات قابل رفع خودکار
ruff check --fix
```

<div dir="rtl">

## نیازمندی‌ها
- Python 3.9+
- [uv](https://astral.sh/uv/) (برای مدیریت بسته توصیه می‌شود) یا conda/pip
- وابستگی‌های مشخص شده در `pyproject.toml`
- دسترسی به ارائه‌دهندگان LLM پشتیبانی شده (OpenAI یا OpenRouter)

## معماری

این پروژه از یک معماری ماژولار پیروی می‌کند:

</div>

```
src/markpdfdown/
├── __init__.py          # مقداردهی اولیه بسته
├── __main__.py          # نقطه ورود برای python -m
├── cli.py               # رابط خط فرمان
├── main.py              # منطق اصلی تبدیل
├── config.py            # مدیریت پیکربندی
└── core/                # ماژول‌های اصلی
    ├── llm_client.py    # ادغام LiteLLM
    ├── file_worker.py   # پردازش فایل
    └── utils.py         # توابع کمکی
```

<div dir="rtl">

## مشارکت
مشارکت‌ها خوش‌آمدید! لطفاً در ارسال Pull Request دریغ نکنید.

1. مخزن را Fork کنید
2. شاخه ویژگی خود را ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. محیط توسعه را راه‌اندازی کنید:

</div>

   ```bash
   uv sync --group dev
   pre-commit install
   ```

<div dir="rtl">

4. تغییرات خود را اعمال کرده و کیفیت کد را تضمین کنید:

</div>

   ```bash
   ruff format
   ruff check --fix
   pre-commit run --all-files
   ```

<div dir="rtl">

5. تغییرات خود را Commit کنید (`git commit -m 'feat: Add some amazing feature'`)
6. به شاخه Push کنید (`git push origin feature/amazing-feature`)
7. یک Pull Request باز کنید

لطفاً قبل از ارسال مطمئن شوید که کد شما با اجرای ابزارهای linting و قالب‌بندی از استانداردهای کدنویسی پروژه پیروی می‌کند.


## مجوز
این پروژه تحت مجوز Apache License 2.0 منتشر شده است. برای جزئیات به فایل LICENSE مراجعه کنید.

## قدردانی
- با تشکر از توسعه‌دهندگان LiteLLM برای فراهم کردن دسترسی یکپارچه به LLM
- با تشکر از توسعه‌دهندگان مدل‌های هوش مصنوعی چندوجهی که این ابزار را قدرتمند می‌کنند
- الهام گرفته از نیاز به ابزارهای بهتر تبدیل PDF به Markdown

</div>

[hub_url]: https://hub.docker.com/r/jorbenzhu/markpdfdown/
[tag_url]: https://github.com/markpdfdown/markpdfdown/releases
[license_url]: https://github.com/markpdfdown/markpdfdown/blob/main/LICENSE

[Size]: https://img.shields.io/docker/image-size/jorbenzhu/markpdfdown/latest?color=066da5&label=size
[Pulls]: https://img.shields.io/docker/pulls/jorbenzhu/markpdfdown.svg?style=flat&label=pulls&logo=docker
[Tag]: https://img.shields.io/github/release/markpdfdown/markpdfdown.svg
[License]: https://img.shields.io/github/license/markpdfdown/markpdfdown