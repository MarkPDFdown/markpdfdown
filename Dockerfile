# 第一阶段：构建环境
FROM python:3.9-slim as builder

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 安装Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# 安装uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# 设置工作目录并复制文件
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY README.md ./
COPY .env.sample ./

# 安装依赖和包
RUN uv sync --frozen
RUN uv pip install -e .

# 第二阶段：运行环境
FROM python:3.9-slim

# 安装运行时依赖（如果有的话）
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 从构建阶段复制虚拟环境
COPY --from=builder /app/.venv .venv

# 复制源代码（确保可执行文件能找到模块）
COPY --from=builder /app/src ./src
COPY --from=builder /app/pyproject.toml ./
COPY --from=builder /app/README.md ./

# 设置环境变量
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1

# 使用Python模块方式运行（更可靠）
ENTRYPOINT ["python", "-m", "markpdfdown"]
