# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build-essential tools to compile psycopg2/other C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install to a local folder to easily copy to the next stage
RUN pip install --upgrade pip \
    && pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim AS production

# 1. Create user and directories in one step to keep layers small
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appgroup /app

WORKDIR /app

# 2. Copy dependencies from builder
COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local
ENV PATH="/home/appuser/.local/bin:$PATH"

# 3. Copy project files
COPY --chown=appuser:appgroup . .

# 4. Install ONLY the runtime database library (much smaller than libpq-dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser

# 5. Fix: Use the nested path for manage.py
RUN python discussion_forum_00016438/manage.py collectstatic --noinput

EXPOSE 8000

# 6. Fix: Tell Gunicorn to look inside your project folder for the config
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--chdir", "discussion_forum_00016438", "config.wsgi:application"]