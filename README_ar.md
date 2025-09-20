<div align="center" dir="rtl">

<h1>MarkPDFDown</h1>
<p align="center"><a href="./README.md">English</a> | <a href="./README_zh.md">中文</a> | <a href="./README_ja.md">日本語</a> | <a href="./README_ru.md">Русский</a> | <a href="./README_fa.md">فارسی</a> | العربية</p>

[![Size]][hub_url]
[![Pulls]][hub_url]
[![Tag]][tag_url]
[![License]][license_url]
<p>أداة قوية تستخدم نماذج اللغة الكبيرة متعددة الوسائط لتحويل ملفات PDF إلى تنسيق Markdown.</p>

![markpdfdown](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/markpdfdown.png)

</div>

<div dir="rtl">

## نظرة عامة

تم تصميم MarkPDFDown لتبسيط عملية تحويل مستندات PDF إلى نص Markdown نظيف وقابل للتعديل. من خلال الاستفادة من نماذج الذكاء الاصطناعي متعددة الوسائط المتقدمة عبر LiteLLM، يمكنها استخراج النص بدقة، والحفاظ على التنسيق، والتعامل مع هياكل المستندات المعقدة بما في ذلك الجداول والصيغ والرسوم البيانية.

## المميزات

- **تحويل PDF إلى Markdown**: تحويل أي مستند PDF إلى Markdown منسق بشكل جيد
- **تحويل الصور إلى Markdown**: تحويل الصور إلى Markdown منسق بشكل جيد
- **دعم متعدد المزودين**: يدعم OpenAI وOpenRouter من خلال LiteLLM
- **واجهة سطر أوامر مرنة**: أوضاع استخدام تعتمد على الملفات والأنابيب
- **الحفاظ على التنسيق**: يحافظ على العناوين والقوائم والجداول وعناصر التنسيق الأخرى
- **اختيار نطاق الصفحات**: تحويل نطاقات صفحات محددة من مستندات PDF
- **بنية معمارية نمطية**: قاعدة شيفرة نظيفة وقابلة للصيانة مع فصل المسؤوليات

## عرض توضيحي
![](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/demo_02.png)

## التثبيت

### باستخدام uv (موصى به)

</div>

```bash
# تثبيت uv إذا لم يكن مثبتًا بالفعل
curl -LsSf https://astral.sh/uv/install.sh | sh

# استنساخ المستودع
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# تثبيت التبعيات وإنشاء بيئة افتراضية
uv sync

# تثبيت الحزمة في وضع التطوير
uv pip install -e .
```

<div dir="rtl">

### باستخدام conda

</div>

```bash
conda create -n markpdfdown python=3.9
conda activate markpdfdown

# استنساخ المستودع
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# تثبيت التبعيات
pip install -e .
```

<div dir="rtl">

## التكوين

يستخدم MarkPDFDown متغيرات البيئة للتكوين. قم بإنشاء ملف `.env` في دليل مشروعك:

</div>

```bash
# نسخ التكوين النموذجي
cp .env.sample .env
```

<div dir="rtl">

قم بتحرير ملف `.env` بإعداداتك:

</div>

```bash
# تكوين النموذج
MODEL_NAME=gpt-4o

# مفاتيح API (يكتشفها LiteLLM تلقائيًا)
OPENAI_API_KEY=your-openai-api-key
# أو لـ OpenRouter
OPENROUTER_API_KEY=your-openrouter-api-key

# معلمات اختيارية
TEMPERATURE=0.3
MAX_TOKENS=8192
RETRY_TIMES=3
```

<div dir="rtl">

### النماذج المدعومة

#### نماذج OpenAI

</div>

```bash
MODEL_NAME=gpt-4o
MODEL_NAME=gpt-4o-mini
MODEL_NAME=gpt-4-vision-preview
```

<div dir="rtl">

#### نماذج OpenRouter

</div>

```bash
MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet
MODEL_NAME=openrouter/google/gemini-pro-vision
MODEL_NAME=openrouter/meta-llama/llama-3.2-90b-vision
```

<div dir="rtl">

## الاستخدام

### وضع الملف (موصى به)

</div>

```bash
# التحويل الأساسي
markpdfdown --input document.pdf --output output.md

# تحويل نطاق صفحات محدد
markpdfdown --input document.pdf --output output.md --start 1 --end 10

# تحويل صورة إلى markdown
markpdfdown --input image.png --output output.md

# استخدام وحدة python
python -m markpdfdown --input document.pdf --output output.md
```

<div dir="rtl">

### وضع الأنبوب (متوافق مع Docker)

</div>

```bash
# PDF إلى markdown عبر الأنبوب
markpdfdown < document.pdf > output.md

# استخدام وحدة python
python -m markpdfdown < document.pdf > output.md
```

<div dir="rtl">

### الاستخدام المتقدم

</div>

```bash
# تحويل الصفحات 5-15 من PDF
markpdfdown --input large_document.pdf --output chapter.md --start 5 --end 15

# معالجة ملفات متعددة
for file in *.pdf; do
    markpdfdown --input "$file" --output "${file%.pdf}.md"
done
```

<div dir="rtl">

## استخدام Docker

</div>

```bash
# بناء الصورة (إذا لزم الأمر)
docker build -t markpdfdown .

# التشغيل مع متغيرات البيئة
docker run -i \
  -e MODEL_NAME=gpt-4o \
  -e OPENAI_API_KEY=your-api-key \
  markpdfdown < input.pdf > output.md

# استخدام OpenRouter
docker run -i \
  -e MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet \
  -e OPENROUTER_API_KEY=your-openrouter-key \
  markpdfdown < input.pdf > output.md
```

<div dir="rtl">

## إعداد التطوير

### أدوات جودة الكود

يستخدم هذا المشروع `ruff` للتحقق والتنسيق، و `pre-commit` لفحوصات جودة الكود التلقائية.

#### تثبيت تبعيات التطوير

</div>

```bash
# إذا كنت تستخدم uv
uv sync --group dev

# إذا كنت تستخدم pip
pip install -e ".[dev]"
```

<div dir="rtl">

#### إعداد خطافات pre-commit

</div>

```bash
# تثبيت خطافات pre-commit
pre-commit install

# تشغيل pre-commit على جميع الملفات (اختياري)
pre-commit run --all-files
```

<div dir="rtl">

#### تنسيق الكود والتحقق منه

</div>

```bash
# تنسيق الكود باستخدام ruff
ruff format

# تشغيل فحوصات التحقق
ruff check

# إصلاح المشكلات القابلة للإصلاح التلقائي
ruff check --fix
```

<div dir="rtl">

## المتطلبات
- Python 3.9+
- [uv](https://astral.sh/uv/) (موصى به لإدارة الحزم) أو conda/pip
- التبعيات المحددة في `pyproject.toml`
- الوصول إلى مزودي LLM المدعومين (OpenAI أو OpenRouter)

## البنية المعمارية

يتبع المشروع بنية معمارية نمطية:

</div>

```
src/markpdfdown/
├── __init__.py          # تهيئة الحزمة
├── __main__.py          # نقطة الدخول لـ python -m
├── cli.py               # واجهة سطر الأوامر
├── main.py              # منطق التحويل الأساسي
├── config.py            # إدارة التكوين
└── core/                # الوحدات الأساسية
    ├── llm_client.py    # تكامل LiteLLM
    ├── file_worker.py   # معالجة الملفات
    └── utils.py         # الوظائف المساعدة
```

<div dir="rtl">

## المساهمة
نرحب بالمساهمات! لا تتردد في إرسال طلب سحب.

1. انسخ المستودع (Fork)
2. أنشئ فرع الميزة الخاص بك (`git checkout -b feature/amazing-feature`)
3. قم بإعداد بيئة التطوير:

</div>

   ```bash
   uv sync --group dev
   pre-commit install
   ```

<div dir="rtl">

4. قم بإجراء تغييراتك وتأكد من جودة الكود:

</div>

   ```bash
   ruff format
   ruff check --fix
   pre-commit run --all-files
   ```

<div dir="rtl">

5. قم بتنفيذ تغييراتك (`git commit -m 'feat: Add some amazing feature'`)
6. ادفع إلى الفرع (`git push origin feature/amazing-feature`)
7. افتح طلب سحب

يرجى التأكد من أن الكود الخاص بك يتبع معايير الترميز الخاصة بالمشروع عن طريق تشغيل أدوات التحقق والتنسيق قبل الإرسال.

## الترخيص
هذا المشروع مرخص بموجب Apache License 2.0. راجع ملف LICENSE للحصول على التفاصيل.

## شكر وتقدير
- شكرًا لمطوري LiteLLM لتوفير وصول موحد إلى LLM
- شكرًا لمطوري نماذج الذكاء الاصطناعي متعددة الوسائط التي تدعم هذه الأداة
- مستوحى من الحاجة إلى أدوات أفضل لتحويل PDF إلى Markdown

</div>

[hub_url]: https://hub.docker.com/r/jorbenzhu/markpdfdown/
[tag_url]: https://github.com/markpdfdown/markpdfdown/releases
[license_url]: https://github.com/markpdfdown/markpdfdown/blob/main/LICENSE

[Size]: https://img.shields.io/docker/image-size/jorbenzhu/markpdfdown/latest?color=066da5&label=size
[Pulls]: https://img.shields.io/docker/pulls/jorbenzhu/markpdfdown.svg?style=flat&label=pulls&logo=docker
[Tag]: https://img.shields.io/github/release/markpdfdown/markpdfdown.svg
[License]: https://img.shields.io/github/license/markpdfdown/markpdfdown