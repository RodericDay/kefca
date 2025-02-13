FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
ENV UV_SYSTEM_PYTHON=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app/
COPY pyproject.toml .
RUN uv sync
