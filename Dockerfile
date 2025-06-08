FROM --platform=linux/arm64 python:3.13-slim

RUN apt-get update && \
    apt-get install -y \
    curl

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG USER_IDS
ARG BOT_TOKEN
ARG OPENAI_API_KEY

COPY ./uv.lock /app/uv.lock
COPY ./pyproject.toml /app/pyproject.toml

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

ENV \
  USER_IDS=${USER_IDS} \
  BOT_TOKEN=${BOT_TOKEN} \
  OPENAI_API_KEY=${OPENAI_API_KEY}

COPY . /app

# Run the application.
CMD ["/app/.venv/bin/python", "main.py", "--port", "8081", "--host", "0.0.0.0"]