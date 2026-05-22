# ── Build stage ────────────────────────────────────────────────────────────────
FROM python:3.14-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy dependency files first (better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment, no editable installs
RUN uv sync --frozen --no-install-project --no-editable

# Copy the rest of the source
COPY . .

# Install the project itself
RUN uv sync --frozen --no-editable


# ── Runtime stage ──────────────────────────────────────────────────────────────
FROM python:3.14-slim AS runtime

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY --from=builder /app/seaweedfs_s3_event_notifier seaweedfs_s3_event_notifier

# Put the venv on PATH so `python` and scripts resolve correctly
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Drop to a non-root user for security
RUN useradd --create-home appuser
USER appuser

CMD ["python", "-m", "granian", "--interface", "asgi", "--host", "0.0.0.0", "--port", "8081", "seaweedfs_s3_event_notifier.main:app"]