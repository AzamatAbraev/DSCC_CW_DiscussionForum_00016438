FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim AS production
# Create non-root user FIRST
RUN groupadd --gid 1000 appgroup && \
useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser
WORKDIR /app
# Install runtime dependencies as root
RUN apt-get update && apt-get install -y --no-install-recommends \
libpq5 \
&& rm -rf /var/lib/apt/lists/* \
&& apt-get clean
# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Copy application code
COPY --chown=appuser:appgroup . .
# Create directories for static/media with correct permissions
RUN mkdir -p staticfiles media && \
chown -R appuser:appgroup staticfiles media
# Switch to non-root user
USER appuser
# Collect static files
RUN python discussion_forum_00016438/manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "--config", "gunicorn.conf.py", "discussion_forum_00016438.config.wsgi:application"]