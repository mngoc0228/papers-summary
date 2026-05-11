FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["uv", "run main.py"]

EXPOSE 8000
