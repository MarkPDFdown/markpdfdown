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

تم تصميم MarkPDFDown لتبسيط عملية تحويل مستندات PDF إلى نص Markdown نظيف وقابل للتعديل. من خلال الاستفادة من نماذج الذكاء الاصطناعي متعددة الوسائط المتقدمة، يمكنها استخراج النص بدقة، والحفاظ على التنسيق، والتعامل مع هياكل المستندات المعقدة بما في ذلك الجداول والصيغ والرسوم البيانية.

## المميزات

- **تحويل PDF إلى Markdown**: تحويل أي مستند PDF إلى Markdown منسق بشكل جيد
- **تحويل الصور إلى Markdown**: تحويل الصور إلى Markdown منسق بشكل جيد
- **الفهم متعدد الوسائط**: يستفيد من الذكاء الاصطناعي لفهم هيكل المستند ومحتواه
- **الحفاظ على التنسيق**: يحافظ على العناوين والقوائم والجداول وعناصر التنسيق الأخرى
- **نموذج قابل للتخصيص**: قم بتكوين النموذج ليناسب احتياجاتك

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

## الاستخدام

</div>

```bash
# إعداد مفتاح OpenAI API الخاص بك
export OPENAI_API_KEY="your-api-key"
# اختياري: إعداد قاعدة OpenAI API
export OPENAI_API_BASE="your-api-base"
# اختياري: إعداد نموذج OpenAI API
export OPENAI_DEFAULT_MODEL="your-model"

# PDF إلى Markdown
python main.py < tests/input.pdf > output.md

# صورة إلى Markdown
python main.py < input_image.png > output.md
```

<div dir="rtl">

## الاستخدام المتقدم

</div>

```bash
python main.py page_start page_end < tests/input.pdf > output.md
```

<div dir="rtl">

## استخدام Docker

</div>

```bash
docker run -i -e OPENAI_API_KEY=your-api-key -e OPENAI_API_BASE=your-api-base -e OPENAI_DEFAULT_MODEL=your-model jorbenzhu/markpdfdown < input.pdf > output.md
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
- الوصول إلى نموذج الذكاء الاصطناعي متعدد الوسائط المحدد

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