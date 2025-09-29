# =============================================================================
# Stage 1: Base image with system dependencies
# =============================================================================
FROM python:3.12-slim-bookworm AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_CACHE_DIR=/opt/uv-cache \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Create cache directory with proper permissions
RUN mkdir -p /opt/uv-cache && chmod 777 /opt/uv-cache

# Create non-root user
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# =============================================================================
# Stage 2: Dependencies installation
# =============================================================================
FROM base AS deps

# Set working directory
WORKDIR /app

# Copy dependency files and README (required by hatchling)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Clean up cache to avoid permission issues
RUN rm -rf /opt/uv-cache/*

# =============================================================================
# Stage 3: Development dependencies (optional)
# =============================================================================
FROM deps AS deps-dev

# Install development dependencies
RUN uv sync --frozen

# Clean up cache to avoid permission issues
RUN rm -rf /opt/uv-cache/*

# =============================================================================
# Stage 4: Production image
# =============================================================================
FROM deps AS production

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser alembic/ ./alembic/
COPY --chown=appuser:appuser alembic.ini ./

# Create necessary directories
RUN mkdir -p /app/logs /app/htmlcov && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set runtime environment variables
ENV UV_CACHE_DIR=/tmp/uv-cache

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/docs || exit 1

# Default command
CMD ["uv", "run", "granian", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# =============================================================================
# Stage 5: Development image
# =============================================================================
FROM deps-dev AS development

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser alembic/ ./alembic/
COPY --chown=appuser:appuser alembic.ini ./
COPY --chown=appuser:appuser tests/ ./tests/
COPY --chown=appuser:appuser docs/ ./docs/
COPY --chown=appuser:appuser Makefile ./

# Create necessary directories
RUN mkdir -p /app/logs /app/htmlcov && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set runtime environment variables
ENV UV_CACHE_DIR=/tmp/uv-cache

# Expose port
EXPOSE 8000

# Default command for development
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# =============================================================================
# Stage 6: Testing image
# =============================================================================
FROM deps-dev AS testing

# Set working directory
WORKDIR /app

# Copy application code and tests
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser tests/ ./tests/
COPY --chown=appuser:appuser alembic/ ./alembic/
COPY --chown=appuser:appuser alembic.ini ./
COPY --chown=appuser:appuser Makefile ./

# Create necessary directories
RUN mkdir -p /app/logs /app/htmlcov && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set runtime environment variables
ENV UV_CACHE_DIR=/tmp/uv-cache

# Ensure dev dependencies are installed (including pytest-cov and pytest-asyncio)
RUN uv sync --dev

# Install setuptools to provide distutils module for aioredis compatibility with Python 3.12
ENV SETUPTOOLS_USE_DISTUTILS=stdlib
RUN uv pip install setuptools

# Explicitly install redis, pytest-cov, pytest-asyncio, and aiosqlite to ensure they're available
RUN uv pip install pytest-cov pytest-asyncio aiosqlite

# Default command for testing
CMD ["uv", "run", "pytest", "tests/", "-v", "--cov=src", "--cov-report=html", "--cov-report=term"]
