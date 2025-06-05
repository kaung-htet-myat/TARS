FROM --platform=linux/amd64 python:3.13-slim

RUN apt-get update && \
    apt-get install -y \
    curl

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG USER_ID
ARG BOT_TOKEN
ARG OPENAI_API_KEY
ARG TIMEZONE

COPY ./uv.lock /app/uv.lock
COPY ./pyproject.toml /app/pyproject.toml

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

ENV \
  USER_ID=${USER_ID} \
  BOT_TOKEN=${BOT_TOKEN} \
  OPENAI_API_KEY=${OPENAI_API_KEY} \
  TIMEZONE=${TIMEZONE}

COPY . /app

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/app.py", "--port", "8080", "--host", "0.0.0.0"]