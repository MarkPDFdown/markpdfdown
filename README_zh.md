<div align="center">

<h1>MarkPDFDown</h1>
<p align="center"><a href="./README.md">English</a> | 中文 | <a href="./README_ja.md">日本語</a> | <a href="./README_ru.md">Русский</a> | <a href="./README_fa.md">فارسی</a> | <a href="./README_ar.md">العربية</a></p>

[![Size]][hub_url]
[![Pulls]][hub_url]
[![Tag]][tag_url]
[![License]][license_url]
<p>一个强大的工具，利用多模态大语言模型将PDF文件转录为Markdown格式。</p>

![markpdfdown](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/markpdfdown.png)

</div>

## 概述

MarkPDFDown 旨在简化将PDF文档转换为干净、可编辑的Markdown文本的过程。通过LiteLLM利用先进的多模态AI模型，它可以准确提取文本、保持格式，并处理包括表格、公式和图表在内的复杂文档结构。

## 功能特性

- **PDF转Markdown转换**：将任何PDF文档转换为格式良好的Markdown
- **图像转Markdown转换**：将图像转换为格式良好的Markdown
- **多提供商支持**：通过LiteLLM支持OpenAI和OpenRouter
- **灵活的CLI**：支持基于文件和管道的使用模式
- **格式保持**：保持标题、列表、表格和其他格式元素
- **页面范围选择**：从PDF文档转换特定页面范围
- **模块化架构**：清洁、可维护的代码库，关注点分离

## 演示
![](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/demo_02.png)

## 安装

### 使用 uv（推荐）

```bash
# 如果还没有安装uv，先安装
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆仓库
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# 安装依赖并创建虚拟环境
uv sync

# 以开发模式安装包
uv pip install -e .
```

### 使用 conda

```bash
conda create -n markpdfdown python=3.9
conda activate markpdfdown

# 克隆仓库
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# 安装依赖
pip install -e .
```

## 配置

MarkPDFDown 使用环境变量进行配置。在项目目录中创建 `.env` 文件：

```bash
# 复制示例配置
cp .env.sample .env
```

编辑 `.env` 文件设置您的配置：

```bash
# 模型配置
MODEL_NAME=gpt-4o

# API密钥（LiteLLM自动检测这些）
OPENAI_API_KEY=your-openai-api-key
# 或者使用OpenRouter
OPENROUTER_API_KEY=your-openrouter-api-key

# 可选参数
TEMPERATURE=0.3
MAX_TOKENS=8192
RETRY_TIMES=3
```

### 支持的模型

#### OpenAI 模型
```bash
MODEL_NAME=gpt-4o
MODEL_NAME=gpt-4o-mini
MODEL_NAME=gpt-4-vision-preview
```

#### OpenRouter 模型
```bash
MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet
MODEL_NAME=openrouter/google/gemini-pro-vision
MODEL_NAME=openrouter/meta-llama/llama-3.2-90b-vision
```

## 使用方法

### 文件模式（推荐）

```bash
# 基本转换
markpdfdown --input document.pdf --output output.md

# 转换特定页面范围
markpdfdown --input document.pdf --output output.md --start 1 --end 10

# 将图像转换为markdown
markpdfdown --input image.png --output output.md

# 使用python模块
python -m markpdfdown --input document.pdf --output output.md
```

### 管道模式（Docker友好）

```bash
# 通过管道将PDF转换为markdown
markpdfdown < document.pdf > output.md

# 使用python模块
python -m markpdfdown < document.pdf > output.md
```

### 高级用法

```bash
# 转换PDF的第5-15页
markpdfdown --input large_document.pdf --output chapter.md --start 5 --end 15

# 处理多个文件
for file in *.pdf; do
    markpdfdown --input "$file" --output "${file%.pdf}.md"
done
```

## Docker 使用

```bash
# 构建镜像（如果需要）
docker build -t markpdfdown .

# 使用环境变量运行
docker run -i \
  -e MODEL_NAME=gpt-4o \
  -e OPENAI_API_KEY=your-api-key \
  markpdfdown < input.pdf > output.md

# 使用OpenRouter
docker run -i \
  -e MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet \
  -e OPENROUTER_API_KEY=your-openrouter-key \
  markpdfdown < input.pdf > output.md
```

## 开发设置

### 代码质量工具

此项目使用 `ruff` 进行代码检查和格式化，使用 `pre-commit` 进行自动化代码质量检查。

#### 安装开发依赖

```bash
# 如果使用uv
uv sync --group dev

# 如果使用pip
pip install -e ".[dev]"
```

#### 设置pre-commit钩子

```bash
# 安装pre-commit钩子
pre-commit install

# 在所有文件上运行pre-commit（可选）
pre-commit run --all-files
```

#### 代码格式化和检查

```bash
# 使用ruff格式化代码
ruff format

# 运行代码检查
ruff check

# 修复可自动修复的问题
ruff check --fix
```

## 系统要求
- Python 3.9+
- [uv](https://astral.sh/uv/)（推荐用于包管理）或 conda/pip
- `pyproject.toml` 中指定的依赖项
- 访问支持的LLM提供商（OpenAI或OpenRouter）

## 架构

项目采用模块化架构：

```
src/markpdfdown/
├── __init__.py          # 包初始化
├── __main__.py          # python -m 入口点
├── cli.py               # 命令行接口
├── main.py              # 核心转换逻辑
├── config.py            # 配置管理
└── core/                # 核心模块
    ├── llm_client.py    # LiteLLM集成
    ├── file_worker.py   # 文件处理
    └── utils.py         # 工具函数
```

## 贡献

欢迎贡献！请随时提交Pull Request。

1. Fork 仓库
2. 创建您的功能分支 ( `git checkout -b feature/amazing-feature` )
3. 设置开发环境：
   ```bash
   uv sync --group dev
   pre-commit install
   ```
4. 进行更改并确保代码质量：
   ```bash
   ruff format
   ruff check --fix
   pre-commit run --all-files
   ```
5. 提交您的更改 ( `git commit -m 'feat: Add some amazing feature'` )
6. 推送到分支 ( `git push origin feature/amazing-feature` )
7. 打开Pull Request

请确保您的代码通过运行代码检查和格式化工具来遵循项目的编码标准。

## 许可证
此项目根据Apache License 2.0许可。详情请参阅LICENSE文件。

## 致谢
- 感谢LiteLLM开发者提供统一的LLM访问接口
- 感谢为此工具提供支持的多模态AI模型开发者
- 受到对更好的PDF转Markdown转换工具需求的启发

[hub_url]: https://hub.docker.com/r/jorbenzhu/markpdfdown/
[tag_url]: https://github.com/markpdfdown/markpdfdown/releases
[license_url]: https://github.com/markpdfdown/markpdfdown/blob/main/LICENSE

[Size]: https://img.shields.io/docker/image-size/jorbenzhu/markpdfdown/latest?color=066da5&label=size
[Pulls]: https://img.shields.io/docker/pulls/jorbenzhu/markpdfdown.svg?style=flat&label=pulls&logo=docker
[Tag]: https://img.shields.io/github/release/markpdfdown/markpdfdown.svg
[License]: https://img.shields.io/github/license/markpdfdown/markpdfdown